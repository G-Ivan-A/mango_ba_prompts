#!/usr/bin/env python3
"""Гигиена merge параллельных PR (issue #377, комментарий к PR #380).

Зачем
-----
Параллельные PR с прогонами конфликтуют в общих реестрах; при ручном разборе
конфликтов в репозиторий уже попадали следы незавершённого merge: маркеры
конфликта в `.gitignore` (merge-коммит `e38eb414` ветки issue #377), две
расходящиеся копии одной строки реестра (`cedafec3`, issue #281), служебный
`.gitkeep` в корне. Валидатор ловит такие следы до merge в `main`:

1. ни в одном версионируемом текстовом файле нет строк-маркеров конфликта
   (семь `<` или `>` с пробелом в начале строки);
2. в «Реестре записей» `runs/README.md` каждый `RUN-NNNN` встречается ровно один
   раз, номера идут по возрастанию;
3. `run_id` в `metadata.yaml` совпадает с именем каталога прогона, и один номер
   не занят двумя годами;
4. в корне нет служебного `.gitkeep` (его создаёт стартовый коммит агента).

Разрешение конфликтов: `scripts/resolve_registry_conflicts.py`.
Запуск: ``python3 scripts/validate_issue_377_merge_hygiene.py``
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARKER = re.compile("^(" + "<" * 7 + "|" + ">" * 7 + ")( |$)")
RUN_ROW = re.compile(r"^\|\s*\[`(RUN-\d{4})`\]\((\d{4})/")
RUN_ID = re.compile(r"^run_id:\s*\"?(RUN-\d{4})\"?\s*$", re.M)


def tracked_files() -> list[str]:
    out = subprocess.run(
        ["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout
    return [p for p in out.split("\0") if p]


def check_markers(files: list[str]) -> list[str]:
    errors = []
    for rel in files:
        path = ROOT / rel
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for n, line in enumerate(text.splitlines(), 1):
            if MARKER.match(line):
                errors.append(f"{rel}:{n}: маркер конфликта merge — {line[:40]!r}")
    return errors


def check_registry() -> list[str]:
    errors = []
    ids = [m.group(1) for line in (ROOT / "runs/README.md").read_text(encoding="utf-8").splitlines()
           if (m := RUN_ROW.match(line))]
    seen = set()
    for run_id in ids:
        if run_id in seen:
            errors.append(f"runs/README.md: {run_id} зарегистрирован дважды")
        seen.add(run_id)
    if ids != sorted(ids):
        errors.append("runs/README.md: строки реестра прогонов не по возрастанию номера")
    return errors


def check_run_dirs() -> list[str]:
    errors = []
    owner: dict[str, str] = {}
    for meta in sorted((ROOT / "runs").glob("*/RUN-*/metadata.yaml")):
        run_dir = meta.parent
        rel = run_dir.relative_to(ROOT).as_posix()
        if run_dir.name in owner:
            errors.append(f"{rel}: номер {run_dir.name} уже занят {owner[run_dir.name]}")
        owner[run_dir.name] = rel
        m = RUN_ID.search(meta.read_text(encoding="utf-8"))
        if not m or m.group(1) != run_dir.name:
            errors.append(f"{rel}/metadata.yaml: run_id {m.group(1) if m else '—'} ≠ {run_dir.name}")
    return errors


def main() -> int:
    files = tracked_files()
    errors = check_markers(files) + check_registry() + check_run_dirs()
    if ".gitkeep" in files:
        errors.append(".gitkeep: служебный файл стартового коммита агента в корне — удалите")
    for error in errors:
        print(f"✗ {error}")
    if errors:
        print("Подсказка: python3 scripts/resolve_registry_conflicts.py (см. CONTRIBUTING.md)")
        return 1
    print(f"✓ гигиена merge: {len(files)} файлов без маркеров конфликта, реестр и номера прогонов уникальны")
    return 0


if __name__ == "__main__":
    sys.exit(main())
