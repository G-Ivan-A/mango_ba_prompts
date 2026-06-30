#!/usr/bin/env python3
"""Regression check for issue #207: BCREQ-1027 canonical run and VPBX API."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

RUN_DIR = "runs/2026/RUN-0013"
METADATA = f"{RUN_DIR}/metadata.yaml"
INPUT = f"{RUN_DIR}/inputs/issue-1027.md"
OUTPUT = f"{RUN_DIR}/outputs/section-4-3-api.md"
GENERATION_LOG = f"{RUN_DIR}/logs/generation.log"
CORRECTIONS = f"{RUN_DIR}/feedback/corrections.md"
CONTRACT_ISSUES = f"{RUN_DIR}/feedback/contract-issues.md"
OLD_RUN_DIR = "runs/bcreq-1027"
VALIDATOR = "scripts/validate_issue_207_bcreq_1027_vpbx_run.py"

FORBIDDEN_ARTIFACT_TEXT = (
    "POST /events/md/onAppealClose",
    "POST /vpbx/cc/appeals/create-closed-appeals",
    "`completion_method`",
    "`with_response`",
    "`without_response`",
    "API MD",
)

REQUIRED_METADATA_TEXT = (
    "run_id: RUN-0013",
    "process: bcreq-1027",
    "run_type: business-task",
    'version: "0.1"',
    'date: "2026-06-24"',
    "author: human+LLM",
    "model: gpt-4",
    "status: draft",
    'contract_used: "governance/bcreq-fr-generation-contract.md"',
    '"POST /vpbx/stats/calls/result"',
    '"outputs/section-4-3-api.md"',
    "API изменён с MD на VPBX",
    "Структура runs исправлена согласно CONTRACT.md",
)

REQUIRED_ARTIFACT_TEXT = (
    "# BCREQ-1027. Раздел 4.3: API-методы",
    "## 4.3. API-методы",
    "4.3.1.",
    "4.3.2.",
    "4.3.3.",
    "4.3.4.",
    "4.3.5.",
    "4.3.6.",
    "4.3.7.",
    "POST /vpbx/stats/calls/result",
    "`key`",
    "`result`",
    "`status`",
    "`data`",
    "`context_status`",
    "`talk_duration`",
    "`call_answer_time`",
    "`call_end_time`",
    "kb/mango-product-docs/processed/vpbx-api/sections/62-poluchenie-statistiki-vyzovov.md",
)

REQUIRED_PROJECT_TEXT = {
    "runs/REGISTRY.md": (
        "RUN-0013",
        "2026-06-24",
        "bcreq-1027",
        "2026/RUN-0013/outputs/section-4-3-api.md",
    ),
    "CHANGELOG.md": (
        "Issue #207",
        OUTPUT,
        "POST /vpbx/stats/calls/result",
    ),
    ".github/workflows/github-pages.yml": (
        "Validate issue #207 BCREQ-1027 VPBX run",
        VALIDATOR,
    ),
    "runs/stats/by-type.md": ("Всего: 17", "RUN-0013", "bcreq-1027"),
    "runs/stats/by-date.md": ("2026-06 | 12", "RUN-0013", "2026-06-24"),
    "runs/stats/by-process.md": ("Уникальных процессов: 17", "bcreq-1027", "RUN-0013"),
}


def read_text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def require_path(path: str) -> list[str]:
    return [] if (ROOT / path).exists() else [f"{path}: missing"]


def reject_path(path: str) -> list[str]:
    return [f"{path}: obsolete path must be removed"] if (ROOT / path).exists() else []


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


def main() -> int:
    errors: list[str] = []
    for path in (RUN_DIR, METADATA, INPUT, OUTPUT, GENERATION_LOG, CORRECTIONS, CONTRACT_ISSUES):
        errors += require_path(path)
    errors += reject_path(OLD_RUN_DIR)
    errors += require_text(METADATA, *REQUIRED_METADATA_TEXT)
    errors += require_text(OUTPUT, *REQUIRED_ARTIFACT_TEXT)
    errors += reject_text(OUTPUT, *FORBIDDEN_ARTIFACT_TEXT)
    errors += require_text(CORRECTIONS, "API VPBX", "POST /vpbx/stats/calls/result")
    errors += require_text(CONTRACT_ISSUES, "runs/CONTRACT.md", "2-фактор")
    for path, needles in REQUIRED_PROJECT_TEXT.items():
        errors += require_text(path, *needles)

    if errors:
        print("Issue #207 BCREQ-1027 VPBX run validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Issue #207 BCREQ-1027 VPBX run validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
