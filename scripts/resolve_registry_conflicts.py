#!/usr/bin/env python3
"""Автоматическое разрешение конфликтов параллельных PR в общих реестрах.

Зачем (issue #377, комментарий к PR #380)
-----------------------------------------
Каждый PR с прогоном дописывает строку в одни и те же места: раздел
`## Unreleased` в `CHANGELOG.md`, таблицы «Реестр записей» и «Локальные
инструменты воспроизводимости» в `runs/README.md`. Когда параллельный PR
мержится первым, второй получает конфликт `This branch has conflicts that must
be resolved`, хотя по смыслу правки независимы: нужно сохранить обе. Реплей
истории (`experiments/issue_377/simulate_registry_merges.py`) показывает, что
это основной источник конфликтов в репозитории.

Что делает
----------
Разрешает только «append-only» конфликты в файлах из `REGISTRIES`: в hunk'е
обе стороны **добавили** строки, базовая версия пуста (или состоит из пустых
строк). Тогда результат — объединение обеих сторон:

* строки таблицы реестра прогонов (`| [`RUN-NNNN`](…`) сортируются по номеру;
  два разных ряда с одним `RUN-NNNN` — коллизия номера, разрешение отклоняется;
* прочие строки таблиц — сначала сторона `main` (она смержена раньше), затем
  своя; одинаковые строки не дублируются;
* текстовые блоки (записи CHANGELOG) — сначала своя запись, затем запись `main`
  (новые записи `## Unreleased` идут сверху), между блоками пустая строка;
* поля frontmatter `version` и `updated` — берётся большее значение.

Всё остальное (обе стороны изменили одну и ту же строку, конфликт вне
реестров, add/add в каталоге прогона) не разрешается: скрипт печатает, что
осталось, и завершается с кодом 1. Для коллизии номера прогона есть режим
`--renumber`.

Использование
-------------
    git merge upstream/main                       # конфликт
    python3 scripts/resolve_registry_conflicts.py # реестры разрешены и git add
    python3 scripts/resolve_registry_conflicts.py --next-run-id --base upstream/main
    python3 scripts/resolve_registry_conflicts.py --renumber RUN-0076 RUN-0078 --base upstream/main

Только stdlib; из CI не вызывается (локальный инструмент агента).
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

#: Файлы, в которых append-only конфликты разрешаются автоматически.
REGISTRIES = ("CHANGELOG.md", "runs/README.md", ".gitignore")
#: Реестры, где новые текстовые блоки пишутся сверху (свой блок над блоком main).
NEWEST_FIRST = ("CHANGELOG.md",)

RUN_ROW = re.compile(r"^\|\s*\[`(RUN-\d{4})`\]")
TABLE_ROW = re.compile(r"^\|.*\|\s*$")
FRONTMATTER_FIELD = re.compile(r"^(version|updated):\s*(\S.*?)\s*$")
RUN_DIR = re.compile(r"^runs/(\d{4})/(RUN-\d{4})/")
RUN_ID = re.compile(r"RUN-(\d{4})")
#: Строка таблицы инструментов: ключ — путь в первой ячейке.
TOOL_ROW = re.compile(r"^\|\s*\[`([^`]+)`\]")
#: Хвост строки инструмента: «Используется в [`RUN-…`](…), … и [`RUN-…`](…). |».
USED_IN = re.compile(r"Используется в ((?:\[`RUN-\d{4}`\]\([^)]*\)(?:, | и )?)+)\.(\s*\|\s*)$")
RUN_LINK = re.compile(r"\[`(RUN-\d{4})`\]\([^)]*\)")


class UnresolvableConflict(Exception):
    """Конфликт не append-only — его должен разобрать человек или агент."""


def git(*args: str, check: bool = True) -> str:
    res = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)
    if check and res.returncode != 0:
        raise SystemExit(f"git {' '.join(args)}: {res.stderr.strip()}")
    return res.stdout


# --------------------------------------------------------------------------
# Разрешение одного файла


def _diff3(ours: str, base: str, theirs: str) -> str:
    with tempfile.TemporaryDirectory() as tmp:
        paths = []
        for name, text in (("ours", ours), ("base", base), ("theirs", theirs)):
            path = Path(tmp) / name
            path.write_text(text, encoding="utf-8")
            paths.append(str(path))
        res = subprocess.run(
            ["git", "merge-file", "-p", "--diff3", "-L", "ours", "-L", "base", "-L", "theirs", *paths],
            capture_output=True,
            text=True,
        )
        if res.returncode < 0 or res.returncode > 127:
            raise SystemExit(f"git merge-file failed: {res.stderr.strip()}")
        return res.stdout


def _version_key(value: str) -> tuple:
    return tuple(int(p) if p.isdigit() else p for p in re.split(r"[.\-]", value.strip("'\"")))


def _resolve_frontmatter(ours: list[str], theirs: list[str]) -> list[str]:
    fields_o = [FRONTMATTER_FIELD.match(line) for line in ours]
    fields_t = [FRONTMATTER_FIELD.match(line) for line in theirs]
    if not all(fields_o) or not all(fields_t):
        raise UnresolvableConflict("frontmatter: изменены поля кроме version/updated")
    keys_o = [m.group(1) for m in fields_o]
    keys_t = [m.group(1) for m in fields_t]
    if keys_o != keys_t:
        raise UnresolvableConflict("frontmatter: разный набор полей")
    out = []
    for line_o, line_t, m_o, m_t in zip(ours, theirs, fields_o, fields_t):
        if m_o.group(1) == "version":
            out.append(line_o if _version_key(m_o.group(2)) >= _version_key(m_t.group(2)) else line_t)
        else:  # updated: ISO-дата сравнивается как строка
            out.append(max(line_o, line_t, key=lambda s: FRONTMATTER_FIELD.match(s).group(2)))
    return out


def _union_lines(first: list[str], second: list[str]) -> list[str]:
    merged: list[str] = []
    for line in first + second:
        if line not in merged:
            merged.append(line)
    return merged


def _used_in(row: str) -> tuple[str, dict[str, str]]:
    """Разделить строку инструмента на «префикс» и ссылки на прогоны."""
    m = USED_IN.search(row)
    if not m:
        return row, {}
    links = {lm.group(1): lm.group(0) for lm in RUN_LINK.finditer(m.group(1))}
    return row[: m.start()] + "Используется в {}." + m.group(2), links


def _merge_tool_row(o: str, b: str, t: str) -> str:
    if o == b or o == t:
        return t
    if t == b:
        return o
    pre_o, links_o = _used_in(o)
    pre_t, links_t = _used_in(t)
    pre_b, links_b = _used_in(b)
    if not (pre_o == pre_t == pre_b and links_o and links_t):
        raise UnresolvableConflict("обе стороны по-разному изменили строку: " + o.strip()[:80])
    if set(links_b) - set(links_o) or set(links_b) - set(links_t):
        raise UnresolvableConflict("одна из сторон удалила ссылку на прогон: " + o.strip()[:80])
    links = {**links_t, **links_o}
    ordered = [links[k] for k in sorted(links)]
    text = ordered[0] if len(ordered) == 1 else ", ".join(ordered[:-1]) + " и " + ordered[-1]
    return pre_o.replace("{}", text, 1)


def _resolve_tool_rows(ours: list[str], base: list[str], theirs: list[str]) -> list[str]:
    """Обе стороны дописали прогоны в одну строку таблицы инструментов — объединить ссылки."""
    sides = []
    for lines in (ours, base, theirs):
        rows = [line for line in lines if line.strip()]
        if not all(TOOL_ROW.match(line) and TABLE_ROW.match(line) for line in rows):
            raise UnresolvableConflict(
                "обе стороны изменили одни и те же строки: " + (rows[0].strip()[:80] if rows else "")
            )
        sides.append({TOOL_ROW.match(line).group(1): line for line in rows})
    o, b, t = sides
    if set(b) - set(o) or set(b) - set(t):
        raise UnresolvableConflict("одна из сторон удалила строку таблицы")
    out = []
    for key in list(b) + [k for k in t if k not in b] + [k for k in o if k not in b and k not in t]:
        if key in b:
            out.append(_merge_tool_row(o[key], b[key], t[key]))
        elif key in o and key in t and o[key] != t[key]:
            raise UnresolvableConflict(f"обе стороны добавили разные строки для {key}")
        else:
            out.append(t.get(key) or o[key])
    return out


def _resolve_hunk(
    path: str, ours: list[str], base: list[str], theirs: list[str], in_frontmatter: bool
) -> list[str]:
    if in_frontmatter and ours and all(FRONTMATTER_FIELD.match(line) for line in ours + theirs):
        return _resolve_frontmatter(ours, theirs)
    if any(line.strip() for line in base):
        return _resolve_tool_rows(ours, base, theirs)
    side_o = [line for line in ours if line.strip()]
    side_t = [line for line in theirs if line.strip()]
    rows = side_o + side_t
    if rows and all(TABLE_ROW.match(line) for line in rows):
        if all(RUN_ROW.match(line) for line in rows):
            by_id: dict[str, str] = {}
            for line in rows:
                run_id = RUN_ROW.match(line).group(1)
                if by_id.setdefault(run_id, line) != line:
                    raise UnresolvableConflict(
                        f"коллизия номера прогона {run_id}: обе стороны регистрируют разные прогоны; "
                        "перенумеруйте свой прогон (--next-run-id, --renumber)"
                    )
            return [by_id[k] for k in sorted(by_id)]
        return _union_lines(side_t, side_o)  # main смержен раньше — его строки выше
    if in_frontmatter:  # добавленные элементы списков YAML (sources и т. п.)
        return _union_lines(side_t, side_o)
    # Текстовые блоки: в CHANGELOG своя запись сверху (новые записи Unreleased
    # идут первыми), в остальных реестрах — в порядке merge (main выше).
    block_o = _trim_blank(ours)
    block_t = _trim_blank(theirs)
    if block_o == block_t:
        return ours
    first, second = (block_o, block_t) if path in NEWEST_FIRST else (block_t, block_o)
    head = ours[: _first_non_blank(ours)]
    tail = ours[len(ours) - _trailing_blank(ours):] if _trailing_blank(ours) else []
    sep = [""] if path in NEWEST_FIRST else []
    return head + first + sep + second + tail


def _first_non_blank(lines: list[str]) -> int:
    for i, line in enumerate(lines):
        if line.strip():
            return i
    return len(lines)


def _trailing_blank(lines: list[str]) -> int:
    n = 0
    for line in reversed(lines):
        if line.strip():
            break
        n += 1
    return n


def _trim_blank(lines: list[str]) -> list[str]:
    start = _first_non_blank(lines)
    end = len(lines) - _trailing_blank(lines)
    return lines[start:end] if start < end else []


def resolve_text(path: str, ours: str, base: str, theirs: str) -> str:
    """Вернуть объединённый текст реестра или поднять `UnresolvableConflict`."""
    if path not in REGISTRIES:
        raise UnresolvableConflict(f"{path} не входит в реестры {REGISTRIES}")
    merged = _diff3(ours, base, theirs)
    lines = merged.split("\n")
    out: list[str] = []
    i = 0
    fm_open = bool(lines) and lines[0] == "---"
    fm_closed = not fm_open
    while i < len(lines):
        line = lines[i]
        if line.startswith("<<<<<<< "):
            sides: dict[str, list[str]] = {"ours": [], "base": [], "theirs": []}
            current = "ours"
            i += 1
            while not lines[i].startswith(">>>>>>> "):
                if lines[i].startswith("||||||| "):
                    current = "base"
                elif lines[i] == "=======":
                    current = "theirs"
                else:
                    sides[current].append(lines[i])
                i += 1
            out.extend(_resolve_hunk(path, sides["ours"], sides["base"], sides["theirs"], not fm_closed))
        else:
            if fm_open and not fm_closed and i > 0 and line == "---":
                fm_closed = True
            out.append(line)
        i += 1
    result = "\n".join(out)
    if re.search(r"^(<<<<<<<|=======|>>>>>>>)( |$)", result, re.M):
        raise UnresolvableConflict("в результате остались маркеры конфликта")
    return result


# --------------------------------------------------------------------------
# Режимы командной строки


def _stage(path: str, n: int) -> str:
    res = subprocess.run(["git", "show", f":{n}:{path}"], cwd=ROOT, capture_output=True, text=True)
    return res.stdout if res.returncode == 0 else ""


def resolve_in_progress_merge() -> int:
    unmerged = [p for p in git("diff", "--name-only", "--diff-filter=U").splitlines() if p]
    if not unmerged:
        print("Конфликтов нет: незавершённого merge с конфликтами не найдено.")
        return 0
    left: list[str] = []
    for path in unmerged:
        if path not in REGISTRIES:
            left.append(path)
            continue
        try:
            text = resolve_text(path, _stage(path, 2), _stage(path, 1), _stage(path, 3))
        except UnresolvableConflict as exc:
            print(f"✗ {path}: {exc}")
            left.append(path)
            continue
        (ROOT / path).write_text(text, encoding="utf-8")
        git("add", "--", path)
        print(f"✓ {path}: append-only конфликт разрешён (обе стороны сохранены)")
    collisions = sorted({m.group(2) for p in left if (m := RUN_DIR.match(p))})
    for run_id in collisions:
        print(
            f"✗ каталог {run_id} есть в обеих ветках — номер занят. Отмените merge "
            f"(git merge --abort) и выполните --renumber {run_id} <свободный номер> (--next-run-id)."
        )
    if left:
        print("Требуют ручного разбора: " + ", ".join(left))
        return 1
    print("Все конфликты разрешены. Проверьте `make validate-full` и завершите merge: git commit --no-edit")
    return 0


def _run_ids(ref: str) -> set[int]:
    ids = set()
    for path in git("ls-tree", "-r", "--name-only", ref, "--", "runs").splitlines():
        if m := RUN_DIR.match(path):
            ids.add(int(m.group(2)[4:]))
    return ids


def _open_pr_run_ids() -> set[int]:
    """Номера прогонов, занятые открытыми PR (через `gh`, если доступен)."""
    res = subprocess.run(
        ["gh", "pr", "list", "--repo", "G-Ivan-A/mango_ba_prompts", "--state", "open",
         "--limit", "100", "--json", "files", "--jq", ".[].files[].path"],
        cwd=ROOT, capture_output=True, text=True,
    )
    if res.returncode != 0:
        print("(gh недоступен: открытые PR не учтены)", file=sys.stderr)
        return set()
    return {int(m.group(2)[4:]) for p in res.stdout.splitlines() if (m := RUN_DIR.match(p))}


def next_run_id(base: str) -> str:
    taken = _run_ids(base) | _open_pr_run_ids() | _run_ids("HEAD")
    return f"RUN-{max(taken | {0}) + 1:04d}"


def renumber(old: str, new: str, base: str) -> int:
    """Перенумеровать прогон ветки: каталог, файлы ветки и добавленные веткой строки."""
    if not (RUN_ID.fullmatch(old) and RUN_ID.fullmatch(new)):
        raise SystemExit("ожидаются номера вида RUN-NNNN")
    if git("diff", "--name-only", "--diff-filter=U"):
        raise SystemExit("идёт merge с конфликтами: сначала git merge --abort")
    merge_base = git("merge-base", "HEAD", base).strip()
    repl = {old: new, old.lower(): new.lower()}

    def sub(text: str) -> str:
        for a, b in repl.items():
            text = re.sub(rf"{re.escape(a)}(?!\d)", b, text)
        return text

    for path in git("ls-tree", "-d", "--name-only", "HEAD", "runs/").splitlines():
        src = Path(path) / old
        if (ROOT / src).is_dir():
            git("mv", str(src), str(Path(path) / new))
    changed = git("diff", "--name-status", "-M", merge_base, "HEAD").splitlines()
    added_by_branch = set()
    modified = set()
    for row in changed:
        status, *paths = row.split("\t")
        target = sub(paths[-1])
        if status[0] in "AR":
            added_by_branch.add(target)
        elif status[0] == "M":
            modified.add(target)
    edited = 0
    for path in sorted(added_by_branch):
        file = ROOT / path
        if not file.is_file():
            continue
        try:
            text = file.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if sub(text) != text:
            file.write_text(sub(text), encoding="utf-8")
            edited += 1
    for path in sorted(modified):
        file = ROOT / path
        added_lines = {
            line[1:] for line in git("diff", "-U0", merge_base, "HEAD", "--", path).splitlines()
            if line.startswith("+") and not line.startswith("+++")
        }
        text = file.read_text(encoding="utf-8")
        new_text = "\n".join(sub(line) if line in added_lines else line for line in text.split("\n"))
        if new_text != text:
            file.write_text(new_text, encoding="utf-8")
            edited += 1
    git("add", "-A", "--", "runs", *sorted(added_by_branch | modified))
    print(f"{old} → {new}: изменено файлов {edited}. Проверьте `git diff --cached` и `make validate-full`.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--base", default="upstream/main", help="ветка, в которую мержится PR")
    parser.add_argument("--next-run-id", action="store_true", help="напечатать свободный номер прогона")
    parser.add_argument("--renumber", nargs=2, metavar=("OLD", "NEW"), help="перенумеровать свой прогон")
    args = parser.parse_args(argv)
    if args.next_run_id:
        print(next_run_id(args.base))
        return 0
    if args.renumber:
        return renumber(*args.renumber, base=args.base)
    return resolve_in_progress_merge()


if __name__ == "__main__":
    raise SystemExit(main())
