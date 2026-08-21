#!/usr/bin/env python3
"""Единая точка запуска валидаторов репозитория (issue #299).

Зачем
-----
GitHub Actions в приватном репозитории отключены, поэтому валидаторы
запускаются локально и часто. Три требования формируют дизайн:

1. **Никаких хардкодных списков** — ни списка валидаторов, ни списка ожидаемых
   артефактов: любой такой список правится в каждом PR и конфликтует при
   параллельной работе. Валидаторы обнаруживаются по маске, зависимости
   каждого — наблюдаются во время выполнения (``scripts/_validator_trace.py``).
2. **Инкрементальность** — валидатор перезапускается только если изменился хоть
   один файл/каталог, который он в прошлый успешный раз читал. Сравнение идёт
   по содержимому (sha256), а не по ``git diff``: работают незакоммиченные и
   неотслеживаемые файлы, а откат правки корректно возвращает попадание в кэш.
3. **Параллелизм** — независимые валидаторы выполняются в пуле процессов.

Уровни проверки
---------------
``fast`` (по умолчанию)  инкрементально: пропускает валидаторы с неизменными
                         зависимостями. Цель — ≤1 с на типичной правке.
``full``                 прогон всех валидаторов без чтения кэша (кэш при этом
                         обновляется). Цель — ≤15 с на 1000 прогонов.

Запуск::

    python3 scripts/validate_all.py            # fast
    python3 scripts/validate_all.py --full
    python3 scripts/validate_all.py --list
    python3 scripts/validate_all.py --only 123 --only frontmatter
    python3 scripts/validate_all.py --clear-cache
    python3 scripts/validate_all.py --jobs 1 --no-cache

Кэш лежит в ``.validate-cache/`` (в ``.gitignore``), кэшируются только успешные
прогоны. Кэш — только ускорение: любое повреждение, устаревание или отсутствие
записи трактуется как промах и приводит к честному перезапуску валидатора.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE_DIR = ROOT / ".validate-cache"
STAT_CACHE = CACHE_DIR / "stat-cache.json"
ENTRIES_DIR = CACHE_DIR / "entries"

#: Версия формата кэша. Инкремент обесценивает все прошлые записи.
CACHE_VERSION = 1

#: Маски обнаружения валидаторов. Новый валидатор подхватывается без правки
#: этого файла — поэтому добавление валидатора не создаёт конфликта в раннере.
PY_PATTERNS = ("validate_issue_*.py", "test_*.py")
SH_PATTERNS = ("validate-*.sh",)

ABSENT = "\0absent"


# --------------------------------------------------------------------------
# Обнаружение валидаторов
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class Validator:
    name: str
    kind: str  # "py" | "sh"
    script: str  # путь относительно корня
    args: tuple[str, ...] = ()

    @property
    def command(self) -> list[str]:
        if self.kind == "py":
            return [sys.executable, str(ROOT / "scripts/_validator_trace.py"), str(ROOT / self.script), *self.args]
        return [str(ROOT / self.script), *self.args]


def frontmatter_scope() -> tuple[str, ...]:
    """Область проверки frontmatter — та же, что в Makefile (issue #267).

    Список корневых ``*.md`` вычисляется, а не хардкодится: новый корневой
    документ попадает под проверку сам.
    """

    return (*sorted(p.name for p in ROOT.glob("*.md")), "ai-rules", "tools")


#: Аргументы shell-валидаторов. Значение — функция, а не литерал: область
#: вычисляется на каждом запуске, поэтому новые файлы не требуют правки списка.
SH_ARGS = {"validate-frontmatter": frontmatter_scope}

#: Область чтения shell-валидаторов: bash-скрипт нельзя оттрассировать так же,
#: как python-модуль, поэтому его зона ответственности объявляется здесь —
#: не списком артефактов, а корнями обхода. Внутри корня файлы обнаруживаются
#: динамически, поэтому новый документ не требует правки этого словаря.
SH_SCOPES = {
    "tools/validate-frontmatter.sh": frontmatter_scope,
    # Валидатор имён обходит хронологические каталоги и читает allowlist.
    "tools/validate-file-naming.sh": lambda: (
        "docs/analysis",
        "docs/rfc",
        "docs/adr",
        "tools/file-naming-legacy-allowlist.txt",
    ),
}


def expand_scope(roots: tuple[str, ...]) -> dict:
    """Развернуть корни обхода в зависимости: файлы + перечни каталогов."""

    files: set[str] = set()
    dirs: set[str] = set()
    for root in roots:
        target = ROOT / root
        if target.is_dir():
            dirs.add(root)
            for path in target.rglob("*"):
                rel = path.relative_to(ROOT).as_posix()
                if path.is_dir():
                    dirs.add(rel)
                else:
                    files.add(rel)
        else:
            files.add(root)
    return {"files": sorted(files), "dirs": sorted(dirs)}


def scope_deps(script: str) -> dict | None:
    provider = SH_SCOPES.get(script)
    return None if provider is None else expand_scope(tuple(provider()))


def discover() -> list[Validator]:
    found: list[Validator] = []
    for pattern in PY_PATTERNS:
        for path in sorted((ROOT / "scripts").glob(pattern)):
            found.append(Validator(name=path.stem, kind="py", script=f"scripts/{path.name}"))
    for pattern in SH_PATTERNS:
        for path in sorted((ROOT / "tools").glob(pattern)):
            name = path.stem
            args = SH_ARGS.get(name, tuple)()
            found.append(Validator(name=name, kind="sh", script=f"tools/{path.name}", args=tuple(args)))
    return found


# --------------------------------------------------------------------------
# Хэширование с stat-кэшем
# --------------------------------------------------------------------------


class Hasher:
    """sha256 файлов с кэшем по (size, mtime_ns).

    Гонка «файл изменён, но хэш не обновился»: файл, записанный в ту же
    миллисекунду, что и предыдущее чтение, может сохранить (size, mtime_ns).
    Приём git («racily clean»): если mtime файла не старше момента записи
    stat-кэша, запись не используется и файл перехэшируется.
    """

    def __init__(self, path: Path = STAT_CACHE) -> None:
        self.path = path
        self.entries: dict[str, list] = {}
        self.saved_at_ns = 0
        self.dirty = False
        #: Мемоизация в пределах одного запуска: 24 валидатора делят тысячи
        #: общих зависимостей, а файл в пределах запуска считается неизменным.
        self._memo: dict[str, str] = {}
        self._load()

    def _load(self) -> None:
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
            if raw.get("version") != CACHE_VERSION:
                return
            self.entries = dict(raw.get("entries", {}))
            self.saved_at_ns = int(raw.get("saved_at_ns", 0))
        except (OSError, ValueError, TypeError):
            self.entries = {}  # повреждённый кэш == пустой кэш

    def file_hash(self, rel: str) -> str:
        memo = self._memo.get(rel)
        if memo is not None:
            return memo
        value = self._file_hash(rel)
        self._memo[rel] = value
        return value

    def _file_hash(self, rel: str) -> str:
        target = ROOT / rel
        try:
            info = target.stat()
        except OSError:
            if self.entries.pop(rel, None) is not None:
                self.dirty = True
            return ABSENT
        if not os.path.isfile(target):
            return f"dir:{self.dir_hash(rel)}" if os.path.isdir(target) else ABSENT
        cached = self.entries.get(rel)
        if (
            cached
            and cached[0] == info.st_size
            and cached[1] == info.st_mtime_ns
            and info.st_mtime_ns < self.saved_at_ns
        ):
            return cached[2]
        digest = hashlib.sha256(target.read_bytes()).hexdigest()
        self.entries[rel] = [info.st_size, info.st_mtime_ns, digest]
        self.dirty = True
        return digest

    def dir_hash(self, rel: str) -> str:
        """Хэш перечня имён каталога: новый или удалённый файл виден сразу."""

        key = f"d:{rel}"
        memo = self._memo.get(key)
        if memo is not None:
            return memo
        value = self._dir_hash(rel)
        self._memo[key] = value
        return value

    def _dir_hash(self, rel: str) -> str:
        target = ROOT if rel == "." else ROOT / rel
        try:
            names = sorted(os.listdir(target))
        except OSError:
            return ABSENT
        return hashlib.sha256("\n".join(names).encode("utf-8")).hexdigest()

    def exists_hash(self, rel: str) -> str:
        key = f"e:{rel}"
        memo = self._memo.get(key)
        if memo is None:
            memo = self._memo[key] = self._exists_hash(rel)
        return memo

    def _exists_hash(self, rel: str) -> str:
        return "1" if (ROOT / rel).exists() else "0"

    def save(self) -> None:
        if not self.dirty:
            return
        payload = {"version": CACHE_VERSION, "saved_at_ns": time.time_ns(), "entries": self.entries}
        _atomic_write_json(self.path, payload)


def _atomic_write_json(path: Path, payload: dict) -> None:
    """Атомарная запись: два параллельных раннера не портят файл друг другу."""

    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f"{path.name}.{os.getpid()}.tmp")
    try:
        tmp.write_text(json.dumps(payload), encoding="utf-8")
        os.replace(tmp, path)
    except OSError:
        tmp.unlink(missing_ok=True)  # кэш не критичен: не роняем проверку


# --------------------------------------------------------------------------
# Записи кэша валидаторов
# --------------------------------------------------------------------------


@dataclass
class Result:
    validator: Validator
    status: str  # "pass" | "cached" | "fail"
    seconds: float
    output: str = ""
    deps: dict = field(default_factory=dict)


def entry_path(name: str) -> Path:
    return ENTRIES_DIR / f"{name}.json"


def load_entry(name: str) -> dict | None:
    try:
        data = json.loads(entry_path(name).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None  # нет записи или мусор вместо JSON — промах кэша
    if not isinstance(data, dict) or data.get("version") != CACHE_VERSION:
        return None
    if not isinstance(data.get("deps"), dict):
        return None
    return data


def dep_fingerprint(deps_spec: dict, hasher: Hasher) -> dict[str, str]:
    """Текущее состояние зависимостей: путь -> хэш содержимого/перечня/наличия."""

    state: dict[str, str] = {}
    for rel in deps_spec.get("files", []):
        state[f"f:{rel}"] = hasher.file_hash(rel)
    for rel in deps_spec.get("stats", []):
        state[f"e:{rel}"] = hasher.exists_hash(rel)
    for rel in deps_spec.get("dirs", []):
        state[f"d:{rel}"] = hasher.dir_hash(rel)
    if deps_spec.get("impure"):
        state["*:worktree"] = worktree_fingerprint(hasher)
    return state


_WORKTREE_CACHE: dict[int, str] = {}


def worktree_fingerprint(hasher: Hasher) -> str:
    """Грубый слепок всего рабочего дерева для «непрозрачных» валидаторов.

    Валидатор, который порождает подпроцесс или пишет в репозиторий, нельзя
    трассировать до конца — его зависимостями считается всё отслеживаемое
    дерево. Считается один раз на запуск раннера.
    """

    if 0 in _WORKTREE_CACHE:
        return _WORKTREE_CACHE[0]
    try:
        listing = subprocess.run(
            ["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, check=True
        ).stdout.decode("utf-8", "surrogateescape")
        files = [name for name in listing.split("\0") if name]
    except (OSError, subprocess.CalledProcessError):
        files = [
            p.relative_to(ROOT).as_posix()
            for p in ROOT.rglob("*")
            if p.is_file() and ".git/" not in p.relative_to(ROOT).as_posix()
        ]
    digest = hashlib.sha256()
    for rel in sorted(files):
        digest.update(rel.encode("utf-8", "surrogateescape"))
        digest.update(hasher.file_hash(rel).encode())
    value = digest.hexdigest()
    _WORKTREE_CACHE[0] = value
    return value


# --------------------------------------------------------------------------
# Выполнение
# --------------------------------------------------------------------------


def run_validator(validator: Validator) -> tuple[int, str, dict]:
    trace_out = None
    env = dict(os.environ)
    if validator.kind == "py":
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        trace_out = CACHE_DIR / f"trace-{os.getpid()}-{validator.name}.json"
        env["VALIDATE_TRACE_OUT"] = str(trace_out)
    started = time.perf_counter()
    proc = subprocess.run(validator.command, cwd=ROOT, capture_output=True, env=env)
    elapsed = time.perf_counter() - started
    output = (proc.stdout + proc.stderr).decode("utf-8", "replace")

    opaque = {"files": [], "stats": [], "dirs": [], "impure": True}
    if trace_out is not None:
        try:
            deps = json.loads(trace_out.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            deps = dict(opaque)  # трасса не получена — падаем в консервативный режим
        finally:
            trace_out.unlink(missing_ok=True)
    else:
        # shell-валидатор трассировке не поддаётся: берём объявленную область,
        # а если она неизвестна — всё рабочее дерево.
        deps = scope_deps(validator.script) or dict(opaque)

    # Подпроцессы: область запущенного валидатора добавляется к зависимостям.
    for spawned in deps.pop("spawned", []):
        child = scope_deps(spawned)
        if child is None:
            deps["impure"] = True
        else:
            deps["files"] = sorted(set(deps.get("files", [])) | set(child["files"]))
            deps["dirs"] = sorted(set(deps.get("dirs", [])) | set(child["dirs"]))
    deps.setdefault("files", []).append(validator.script)
    deps["seconds"] = round(elapsed, 3)
    return proc.returncode, output, deps


def check_one(validator: Validator, hasher: Hasher, use_cache: bool) -> Result:
    if use_cache:
        entry = load_entry(validator.name)
        if entry is not None:
            current = dep_fingerprint(entry["deps"], hasher)
            if current == entry.get("state"):
                return Result(validator, "cached", 0.0)
    code, output, deps = run_validator(validator)
    seconds = float(deps.pop("seconds", 0.0))
    if code != 0:
        return Result(validator, "fail", seconds, output)
    return Result(validator, "pass", seconds, output, deps)


def store(result: Result, hasher: Hasher) -> None:
    if result.status == "cached":
        return  # запись уже актуальна, переписывать нечего
    if result.status != "pass":
        # Кэшируются только успехи: провал обязан воспроизводиться при каждом
        # запуске, пока причина не устранена.
        entry_path(result.validator.name).unlink(missing_ok=True)
        return
    payload = {
        "version": CACHE_VERSION,
        "deps": result.deps,
        "state": dep_fingerprint(result.deps, hasher),
        "seconds": result.seconds,
    }
    _atomic_write_json(entry_path(result.validator.name), payload)


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Запуск валидаторов репозитория")
    parser.add_argument("--full", action="store_true", help="прогнать все валидаторы, игнорируя кэш")
    parser.add_argument("--no-cache", action="store_true", help="не читать и не писать кэш")
    parser.add_argument("--clear-cache", action="store_true", help="удалить .validate-cache/ и выйти")
    parser.add_argument("--list", action="store_true", help="показать обнаруженные валидаторы")
    parser.add_argument("--only", action="append", default=[], metavar="SUBSTR",
                        help="запустить только валидаторы, чьё имя содержит подстроку (можно повторять)")
    parser.add_argument("--jobs", type=int, default=0, help="число параллельных процессов (0 = по числу CPU)")
    parser.add_argument("-v", "--verbose", action="store_true", help="печатать вывод успешных валидаторов")
    args = parser.parse_args(argv)

    if args.clear_cache:
        shutil.rmtree(CACHE_DIR, ignore_errors=True)
        print(f"кэш удалён: {CACHE_DIR.relative_to(ROOT)}/")
        return 0

    validators = discover()
    if args.only:
        validators = [v for v in validators if any(sub in v.name for sub in args.only)]
        if not validators:
            print(f"нет валидаторов по фильтру {args.only}", file=sys.stderr)
            return 2

    if args.list:
        for validator in validators:
            print(f"{validator.name:42s} {validator.script}")
        print(f"\nвсего: {len(validators)}")
        return 0

    use_cache = not (args.full or args.no_cache)
    hasher = Hasher()
    jobs = args.jobs if args.jobs > 0 else min(len(validators), (os.cpu_count() or 4))

    started = time.perf_counter()
    results: list[Result] = []
    if jobs > 1:
        # Кэш читается в главном процессе (Hasher не разделяется между
        # процессами), выполняются параллельно только промахи.
        pending: list[Validator] = []
        for validator in validators:
            hit = check_cached_only(validator, hasher) if use_cache else None
            if hit is not None:
                results.append(hit)
            else:
                pending.append(validator)
        with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as pool:
            for code, output, deps, validator in pool.map(_run_pair, pending):
                seconds = float(deps.pop("seconds", 0.0))
                if code != 0:
                    results.append(Result(validator, "fail", seconds, output))
                else:
                    results.append(Result(validator, "pass", seconds, output, deps))
    else:
        for validator in validators:
            results.append(check_one(validator, hasher, use_cache))

    if not args.no_cache:
        for result in results:
            store(result, hasher)
        hasher.save()
    total = time.perf_counter() - started

    order = {v.name: i for i, v in enumerate(validators)}
    results.sort(key=lambda r: order[r.validator.name])
    failed = [r for r in results if r.status == "fail"]
    for result in results:
        mark = {"pass": "PASS", "cached": "CACHED", "fail": "FAIL"}[result.status]
        print(f"{mark:6s} {result.validator.name:42s} {result.seconds:5.2f}s")
        if result.status == "fail" or (args.verbose and result.output):
            for line in result.output.rstrip().splitlines():
                print(f"       | {line}")

    cached = sum(1 for r in results if r.status == "cached")
    level = "full" if args.full else "fast"
    print(
        f"\n{level}: {len(results)} валидаторов, {cached} из кэша, "
        f"{len(failed)} провалов, {total:.2f}s"
    )
    return 1 if failed else 0


def check_cached_only(validator: Validator, hasher: Hasher) -> Result | None:
    entry = load_entry(validator.name)
    if entry is None:
        return None
    if dep_fingerprint(entry["deps"], hasher) != entry.get("state"):
        return None
    return Result(validator, "cached", 0.0)


def _run_pair(validator: Validator):  # type: ignore[no-untyped-def]
    code, output, deps = run_validator(validator)
    return code, output, deps, validator


if __name__ == "__main__":
    raise SystemExit(main())
