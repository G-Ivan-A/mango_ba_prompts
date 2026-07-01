#!/usr/bin/env python3
"""Regression check for issue #257: BCREQ-1027 FT v2 result without response."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

RUN_DIR = "runs/2026/RUN-0013"
OUTPUT = f"{RUN_DIR}/outputs/2026-07-01-bcreq-1027-processed-without-response-ft-v2.md"
FEEDBACK = f"{RUN_DIR}/feedback/issue-257-expert-review.md"
METADATA = f"{RUN_DIR}/metadata.yaml"
LOG = f"{RUN_DIR}/logs/business-task-log.md"
VALIDATOR = "scripts/validate_issue_257_bcreq_1027_ft_v2.py"
WORKFLOW = ".github/workflows/github-pages.yml"

REQUIRED_OUTPUT_TEXT = (
    "# BCREQ-1027. Обработано без ответа (ФТ, вариант 2)",
    "Считать завершение без ответа обработкой обращения",
    "Если оператор завершит обращение без отправленного ответа",
    "FR-01",
    "FR-02",
    "FR-03",
    "FR-04",
    "FR-05",
    "FR-06",
    "Обработано без ответа",
    "`result = 8`",
    "`8 - Завершено без ответа`",
    "существующая кнопка `Завершить обращение`",
    "существующей колонке `Результат`",
    "новой колонки нет",
    "POST /vpbx/cc/appeals/create-closed-appeals",
    "POST /events/md/onAppealClose",
    "POST /vpbx/stats/calls/result",
    "POST /cc/md/session/close",
    "first_answer",
    "История обращений",
    "Исходящие обращения",
    "CSV-экспорт",
    "Код `7` не используется",
    "Старые закрытые обращения не пересчитываются",
    "Комментарии: резюме тестирования и валидации",
    "AC-01",
    "AC-14",
)

REQUIRED_FEEDBACK_TEXT = (
    "шести ролям",
    "техлид ВАТС",
    "архитектор, PO и техлид КЦ",
    "Новый результат обращения",
    "result = 8",
    "новую кнопку не добавлять",
    "новую колонку",
    "Default",
    "выключено",
    "T-01",
    "T-09",
)

REQUIRED_PROJECT_TEXT = {
    METADATA: (
        "https://github.com/G-Ivan-A/mango_ba_prompts/issues/257",
        "outputs/2026-07-01-bcreq-1027-processed-without-response-ft-v2.md",
        "feedback/issue-257-expert-review.md",
        "POST /events/md/onAppealClose",
    ),
    LOG: (
        "Issue #257",
        "2026-07-01-bcreq-1027-processed-without-response-ft-v2.md",
        "Ход выполнения",
        "Итог",
    ),
    "runs/REGISTRY.md": (
        "RUN-0013",
        "2026-07-01-bcreq-1027-processed-without-response-ft-v2.md",
    ),
    "runs/stats/by-type.md": (
        "RUN-0013",
        "Обработано без ответа",
    ),
    "CHANGELOG.md": (
        "Issue #257",
        OUTPUT,
        VALIDATOR,
    ),
    WORKFLOW: (
        "Validate issue #257 BCREQ-1027 FT v2",
        VALIDATOR,
    ),
}


def read_text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def require_path(path: str) -> list[str]:
    return [] if (ROOT / path).exists() else [f"{path}: missing"]


def require_text(path: str, *needles: str) -> list[str]:
    errors = require_path(path)
    if errors:
        return errors

    text = read_text(path)
    return [f"{path}: missing {needle!r}" for needle in needles if needle not in text]


def reject_text(path: str, *needles: str) -> list[str]:
    errors = require_path(path)
    if errors:
        return errors

    text = read_text(path)
    return [f"{path}: forbidden text {needle!r}" for needle in needles if needle in text]


def check_project_wiring() -> list[str]:
    errors: list[str] = []
    for path, needles in REQUIRED_PROJECT_TEXT.items():
        errors += require_text(path, *needles)
    return errors


def main() -> int:
    errors: list[str] = []
    errors += require_text(OUTPUT, *REQUIRED_OUTPUT_TEXT)
    errors += require_text(FEEDBACK, *REQUIRED_FEEDBACK_TEXT)
    errors += reject_text(
        OUTPUT,
        "добавить отдельную кнопку",
        "добавить новую колонку в `Истории обращений`",
        "`result = 7`",
    )
    errors += check_project_wiring()

    if errors:
        print("Issue #257 BCREQ-1027 FT v2 validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Issue #257 BCREQ-1027 FT v2 validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
