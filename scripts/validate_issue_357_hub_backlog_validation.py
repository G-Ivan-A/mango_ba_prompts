#!/usr/bin/env python3
"""Regression checks for issue #357 hub backlog validation artifact.

Проверяется не содержание вердиктов (оно — предмет human review), а контракт
артефакта из постановки issue #357:

1. Валидация покрывает все активные спринты бэклога Хаба (3-13) и блок
   отложенных задач.
2. Каждая задача, статус которой предлагается изменить, снабжена абсолютной
   ссылкой на подтверждающий артефакт.
3. Ссылки на артефакты экосистемы абсолютные (`https://`), относительных путей
   в таблицах доказательств нет.
4. Артефакт зарегистрирован в `pr-ops/artifact-map.md` и в `CHANGELOG.md`.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "docs/analysis/2026-09-03-hub-backlog-sprint-validation.md"
ARTIFACT_MAP = ROOT / "pr-ops/artifact-map.md"
CHANGELOG = ROOT / "CHANGELOG.md"

#: Активные спринты бэклога Хаба v1.53 — каждый обязан получить вердикт.
SPRINTS = tuple(range(3, 14))

#: Изменения статусов, объявленные в разделе 4.2 отчёта: ID -> целевой статус.
STATUS_CHANGES = {
    "B-081": "ЧАСТИЧНО",
    "B-098": "DONE",
    "B-103": "DONE",
    "B-104": "DONE",
}

#: Спринты, удаляемые из активного бэклога.
ARCHIVED_SPRINTS = ("Спринт 5", "Спринт 11", "Спринт 12")

ABSOLUTE_LINK = re.compile(r"\]\((https://github\.com/[^)]+)\)")
RELATIVE_LINK = re.compile(r"\]\((?!https://|#)([^)]+)\)")


def validate_report(text: str, errors: list[str]) -> None:
    for number in SPRINTS:
        if not re.search(rf"Спринт {number}\b", text):
            errors.append(f"отчёт не содержит вердикта по Спринту {number}")
    if "Отложенные задачи с триггером" not in text:
        errors.append("отчёт не содержит вердикта по блоку отложенных задач")

    for task_id, status in STATUS_CHANGES.items():
        if task_id not in text:
            errors.append(f"отчёт не упоминает задачу {task_id} с изменением статуса")
            continue
        rows = [line for line in text.splitlines() if line.startswith("|") and task_id in line]
        if not any(status in row for row in rows):
            errors.append(f"{task_id}: целевой статус {status} не зафиксирован в таблицах")
        if not any(ABSOLUTE_LINK.search(row) for row in rows):
            errors.append(f"{task_id}: изменение статуса не подкреплено абсолютной ссылкой")

    for sprint in ARCHIVED_SPRINTS:
        if sprint not in text:
            errors.append(f"архивируемый {sprint} не назван в дельте")

    for marker in (
        "version: 1.54",
        "backlog-instruction.md",
        "Не выполнено и вопросы",
        "permissions.push = false",
    ):
        if marker not in text:
            errors.append(f"отчёт не содержит обязательного элемента: {marker}")

    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        for target in RELATIVE_LINK.findall(line):
            errors.append(f"относительная ссылка в таблице доказательств: {target}")


def validate_registration(errors: list[str]) -> None:
    relative = "docs/analysis/2026-09-03-hub-backlog-sprint-validation.md"
    if relative not in ARTIFACT_MAP.read_text(encoding="utf-8"):
        errors.append("артефакт не зарегистрирован в pr-ops/artifact-map.md")
    changelog = CHANGELOG.read_text(encoding="utf-8")
    if "#357" not in changelog or relative not in changelog:
        errors.append("CHANGELOG.md не содержит записи о валидации бэклога с ссылкой на артефакт")


def main() -> int:
    errors: list[str] = []
    if not REPORT.exists():
        print(f"ERROR: отсутствует {REPORT.relative_to(ROOT)}", file=sys.stderr)
        return 1
    validate_report(REPORT.read_text(encoding="utf-8"), errors)
    validate_registration(errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"issue #357 validation failed with {len(errors)} error(s).", file=sys.stderr)
        return 1
    print("issue #357 hub backlog validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
