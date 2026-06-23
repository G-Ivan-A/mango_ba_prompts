#!/usr/bin/env python3
"""Regression check for issue #199/#207: BCREQ-1027 section 4.3 API methods."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

OUTPUT = "runs/2026/RUN-0013/outputs/section-4-3-api.md"
VALIDATOR = "scripts/validate_issue_199_bcreq_1027_section_4_3.py"
TEMPORARY_ATTACHMENT_URLS = tuple(
    "https://github.com/" + f"user-attachments/files/{file_id}/{filename}"
    for file_id, filename in (
        ("29252399", "default.txt"),
        ("29252400", "1027.txt"),
    )
)

REQUIRED_OUTPUT_TEXT = (
    "https://github.com/G-Ivan-A/mango_ba_prompts/issues/207",
    "https://github.com/G-Ivan-A/mango_ba_prompts/issues/199",
    "https://github.com/G-Ivan-A/mango_ba_prompts/pull/202",
    "## 4.3. API-методы",
    "POST /vpbx/stats/calls/result",
    "`key`",
    "`result`",
    "`status`",
    "`data`",
    "`context_status`",
    "`talk_duration`",
    "`call_answer_time`",
    "`call_end_time`",
    "RFC-184-S1",
    "RFC-184-S2",
    "vats-core",
    "Резюме изменений",
    "Раздел 3 не формируется",
)

FORBIDDEN_OUTPUT_TEXT = (
    *TEMPORARY_ATTACHMENT_URLS,
    "… доработать",
    "POST /events/md/onAppealClose",
    "POST /vpbx/cc/appeals/create-closed-appeals",
    "post_call_processing_campaing_time",
    "cc/qm/mark-stats/result",
    "`completion_method`",
    "`with_response`",
    "`without_response`",
    "## 3.",
    "# 3.",
    "3. Описание разрабатываемого решения",
)

REQUIRED_PROJECT_TEXT = {
    "CHANGELOG.md": ("Issue #199", "Issue #207", OUTPUT, VALIDATOR),
    ".github/workflows/github-pages.yml": (
        "Validate issue #199 BCREQ-1027 section 4.3 API methods",
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


def check_output_order() -> list[str]:
    errors = require_path(OUTPUT)
    if errors:
        return errors

    text = read_text(OUTPUT)
    markers = (
        "## 4.3. API-методы",
        "## Резюме изменений",
        "## Проверка скоупа",
    )
    positions = []
    for marker in markers:
        position = text.find(marker)
        if position == -1:
            errors.append(f"{OUTPUT}: missing section marker {marker!r}")
        else:
            positions.append(position)

    if positions != sorted(positions):
        errors.append(f"{OUTPUT}: sections must preserve expected order")

    return errors


def check_project_wiring() -> list[str]:
    errors: list[str] = []
    for path, needles in REQUIRED_PROJECT_TEXT.items():
        errors += require_text(path, *needles)
    return errors


def main() -> int:
    errors: list[str] = []
    errors += require_text(OUTPUT, *REQUIRED_OUTPUT_TEXT)
    errors += reject_text(OUTPUT, *FORBIDDEN_OUTPUT_TEXT)
    errors += check_output_order()
    errors += check_project_wiring()

    if errors:
        print("Issue #199 BCREQ-1027 section 4.3 validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Issue #199 BCREQ-1027 section 4.3 validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
