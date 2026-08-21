#!/usr/bin/env python3
"""Дочерний процесс-трассировщик для scripts/validate_all.py.

Запускает валидатор и записывает, какие файлы и каталоги он реально прочитал.
Набор зависимостей не объявляется вручную в валидаторе (это был бы ещё один
хардкодный список и ещё один источник конфликтов при параллельной работе), а
**наблюдается** во время выполнения — как в build-системах с динамическим
обнаружением зависимостей (Shake, Fabricate, ccache depend mode).

Перехватываются четыре точки ввода-вывода, которых достаточно для stdlib-кода:

* ``builtins.open``, ``io.open`` и ``io.open_code`` — чтение содержимого (в том числе импорт
  соседних модулей: importlib открывает ``.py`` именно через ``io.open_code``);
* ``os.stat``/``os.lstat`` — проверки существования (``Path.exists``);
* ``os.scandir``/``os.listdir`` — перечисление каталогов (``glob``/``rglob``).

Если валидатор порождает подпроцесс (``subprocess``), трассировка внутрь него
не идёт: такой валидатор помечается ``impure`` и кэшируется по грубому слепку
всего рабочего дерева (см. validate_all.py).

Не предназначен для прямого запуска человеком:

    VALIDATE_TRACE_OUT=/tmp/deps.json python3 scripts/_validator_trace.py <validator.py> [args...]
"""

from __future__ import annotations

import builtins
import io
import json
import os
import runpy
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_ROOT_STR = str(ROOT)

#: Волатильные каталоги, которые не являются зависимостями: их содержимое
#: меняется от самого запуска валидаторов (кэш раннера, __pycache__) и учёт
#: привёл бы к вечному промаху кэша.
IGNORED_PREFIXES = (".git/", ".validate-cache/", "node_modules/")
IGNORED_PARTS = ("__pycache__",)

FILES: set[str] = set()
STATS: set[str] = set()
DIRS: set[str] = set()
_MISS = object()

SPAWNED: set[str] = set()
STATE = {"impure": False}

_real_open = builtins.open
_real_io_open = io.open
_real_open_code = io.open_code
_real_stat = os.stat
_real_lstat = os.lstat
_real_scandir = os.scandir
_real_listdir = os.listdir
_real_popen = subprocess.Popen


_REL_CACHE: dict[str, str | None] = {}


def _rel(target: object) -> str | None:
    """Путь относительно корня репозитория в posix-виде или None.

    Вызывается на каждый stat/scandir валидатора (сотни тысяч раз на больших
    прогонах), поэтому: только строковые операции и мемоизация результата.
    """

    if isinstance(target, int):  # файловый дескриптор — источник неизвестен
        return None
    try:
        path = os.fspath(target)
    except TypeError:
        return None
    if isinstance(path, bytes):
        try:
            path = path.decode()
        except UnicodeDecodeError:
            return None
    cached = _REL_CACHE.get(path, _MISS)
    if cached is not _MISS:
        return cached  # type: ignore[return-value]
    result = _compute_rel(path)
    _REL_CACHE[path] = result
    return result


def _compute_rel(path: str) -> str | None:
    absolute = os.path.abspath(path)
    if absolute == _ROOT_STR:
        return "."
    prefix = _ROOT_STR + os.sep
    if not absolute.startswith(prefix):
        return None  # вне репозитория (stdlib, /tmp) — не зависимость
    rel = absolute[len(prefix):].replace(os.sep, "/")
    if rel.startswith(IGNORED_PREFIXES) or any(part in IGNORED_PARTS for part in rel.split("/")):
        return None
    return rel


def _traced_open(file, mode="r", *args, **kwargs):  # type: ignore[no-untyped-def]
    rel = _rel(file)
    if rel is not None:
        if any(flag in str(mode) for flag in ("w", "a", "x", "+")):
            STATE["impure"] = True  # валидатор пишет в репозиторий
        else:
            FILES.add(rel)
    return _real_open(file, mode, *args, **kwargs)


def _traced_open_code(path):  # type: ignore[no-untyped-def]
    rel = _rel(path)
    if rel is not None:
        FILES.add(rel)
    return _real_open_code(path)


def _traced_stat(path, *args, **kwargs):  # type: ignore[no-untyped-def]
    rel = _rel(path)
    if rel is not None:
        STATS.add(rel)
    return _real_stat(path, *args, **kwargs)


def _traced_lstat(path, *args, **kwargs):  # type: ignore[no-untyped-def]
    rel = _rel(path)
    if rel is not None:
        STATS.add(rel)
    return _real_lstat(path, *args, **kwargs)


def _traced_scandir(path="."):  # type: ignore[no-untyped-def]
    rel = _rel(path)
    if rel is not None:
        DIRS.add(rel)
    return _real_scandir(path)


def _traced_listdir(path="."):  # type: ignore[no-untyped-def]
    rel = _rel(path)
    if rel is not None:
        DIRS.add(rel)
    return _real_listdir(path)


class _TracedPopen(_real_popen):  # type: ignore[misc,valid-type]
    """Подпроцесс: внутрь трассировка не идёт, поэтому фиксируем, что запущено.

    Раннер сам решает, чем считать зависимости запущенного скрипта: если это
    известный валидатор репозитория — его областью, иначе — всем деревом.
    Команда вне репозитория (например, копия ``tools/`` во временной песочнице)
    зависимостей не добавляет: её содержимое уже прочитано и оттрассировано.
    """

    def __init__(self, args, *rest, **kwargs):  # type: ignore[no-untyped-def]
        command = args[0] if isinstance(args, (list, tuple)) and args else args
        rel = _rel(command)
        if rel is not None:
            FILES.add(rel)
            SPAWNED.add(rel)
        super().__init__(args, *rest, **kwargs)


def _install() -> None:
    builtins.open = _traced_open
    io.open = _traced_open
    io.open_code = _traced_open_code
    os.stat = _traced_stat
    os.lstat = _traced_lstat
    os.scandir = _traced_scandir
    os.listdir = _traced_listdir
    subprocess.Popen = _TracedPopen  # type: ignore[misc]


def _restore() -> None:
    builtins.open = _real_open
    io.open = _real_io_open
    io.open_code = _real_open_code
    os.stat = _real_stat
    os.lstat = _real_lstat
    os.scandir = _real_scandir
    os.listdir = _real_listdir
    subprocess.Popen = _real_popen  # type: ignore[misc]


def main(argv: list[str]) -> int:
    if not argv:
        print("usage: _validator_trace.py <validator.py> [args...]", file=sys.stderr)
        return 2
    target = argv[0]
    out = os.environ.get("VALIDATE_TRACE_OUT")

    sys.argv = list(argv)
    code = 0
    _install()
    try:
        runpy.run_path(target, run_name="__main__")
    except SystemExit as exc:  # валидаторы завершаются через sys.exit(main())
        code = exc.code if isinstance(exc.code, int) else (0 if exc.code is None else 1)
    except BaseException:  # noqa: BLE001 — падение валидатора это FAIL, не крэш раннера
        _restore()
        import traceback

        traceback.print_exc()
        code = 1
    finally:
        _restore()

    if out:
        payload = {
            "files": sorted(FILES),
            "stats": sorted(STATS - FILES),
            "dirs": sorted(DIRS),
            "spawned": sorted(SPAWNED),
            "impure": STATE["impure"],
        }
        tmp = f"{out}.tmp"
        with _real_open(tmp, "w", encoding="utf-8") as handle:
            json.dump(payload, handle)
        os.replace(tmp, out)
    return code


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
