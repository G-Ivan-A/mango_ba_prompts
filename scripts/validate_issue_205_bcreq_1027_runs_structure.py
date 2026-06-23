#!/usr/bin/env python3
"""Regression check for issue #205: BCREQ-1027 runs/ artifact structure."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

RUN_DIR = "runs/bcreq-1027"
README = f"{RUN_DIR}/README.md"
METADATA = f"{RUN_DIR}/metadata.yaml"
ARTIFACT = f"{RUN_DIR}/artifacts/section-4-3-api.md"
OLD_ARTIFACT = "outputs/" + "bcreq-1027-section-4-3.md"
ISSUE_205_VALIDATOR = "scripts/validate_issue_205_bcreq_1027_runs_structure.py"
ISSUE_199_VALIDATOR = "scripts/validate_issue_199_bcreq_1027_section_4_3.py"

TEMPORARY_ATTACHMENT_URLS = tuple(
    "https://github.com/" + f"user-attachments/files/{file_id}/{filename}"
    for file_id, filename in (
        ("29252399", "default.txt"),
        ("29252400", "1027.txt"),
    )
)

REQUIRED_METADATA_TEXT = (
    "run_id: bcreq-1027",
    'issue: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/1027"',
    'title: "BCREQ-1027: Раздел 4.3 API методов"',
    'created: "2026-06-23"',
    "status: draft",
    'contract_used: "governance/bcreq-fr-generation-contract.md"',
    'path: "artifacts/section-4-3-api.md"',
    'type: "bcreq-fr-section"',
    'section: "4.3"',
    "source_attachments:",
    "Заменить на permalink после исправления K-P2.1",
)

REQUIRED_README_TEXT = (
    "# RUN: BCREQ-1027",
    "Артефакт: Раздел 4.3 API методов (BCREQ-FR)",
    "Issue: #1027",
    "PR: #202",
    "`artifacts/section-4-3-api.md`",
    "`metadata.yaml`",
    "[x] Структура runs/ соблюдена",
    "[x] metadata.yaml создан",
    "[x] Ссылки обновлены",
)

REQUIRED_ARTIFACT_TEXT = (
    "https://github.com/G-Ivan-A/mango_ba_prompts/issues/199",
    "https://github.com/G-Ivan-A/mango_ba_prompts/pull/202",
    "TODO: заменить на permalink после задачи Golden Examples",
    "## 4.3. API-методы",
    "POST /events/md/onAppealClose",
    "POST /vpbx/cc/appeals/create-closed-appeals",
    "`completion_method`",
    "RFC-184-S1",
    "RFC-184-S2",
)

REQUIRED_PROJECT_TEXT = {
    "CHANGELOG.md": (
        "Issue #205",
        ARTIFACT,
        "перенесён из `outputs/` в `runs/bcreq-1027/`",
        "TODO: заменить на permalink",
    ),
    ".github/workflows/github-pages.yml": (
        "Validate issue #205 BCREQ-1027 runs structure",
        ISSUE_205_VALIDATOR,
    ),
    ISSUE_199_VALIDATOR: (ARTIFACT,),
}


def read_text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def require_path(path: str) -> list[str]:
    return [] if (ROOT / path).exists() else [f"{path}: missing"]


def reject_path(path: str) -> list[str]:
    return [f"{path}: old path must be removed"] if (ROOT / path).exists() else []


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


def check_paths() -> list[str]:
    errors: list[str] = []
    errors += require_path(RUN_DIR)
    errors += require_path(README)
    errors += require_path(METADATA)
    errors += require_path(ARTIFACT)
    errors += reject_path(OLD_ARTIFACT)
    return errors


def check_project_references() -> list[str]:
    errors: list[str] = []
    for path, needles in REQUIRED_PROJECT_TEXT.items():
        errors += require_text(path, *needles)
        errors += reject_text(path, OLD_ARTIFACT)
    return errors


def main() -> int:
    errors: list[str] = []
    errors += check_paths()
    errors += require_text(METADATA, *REQUIRED_METADATA_TEXT)
    errors += require_text(README, *REQUIRED_README_TEXT)
    errors += require_text(ARTIFACT, *REQUIRED_ARTIFACT_TEXT)
    errors += reject_text(ARTIFACT, *TEMPORARY_ATTACHMENT_URLS)
    errors += check_project_references()

    if errors:
        print("Issue #205 BCREQ-1027 runs structure validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Issue #205 BCREQ-1027 runs structure validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
