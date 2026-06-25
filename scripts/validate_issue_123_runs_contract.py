#!/usr/bin/env python3
"""Regression check for issue #123 — unified runs/ execution records.

The check locks the Phase 0 contract from issue #123:

- every run lives under ``runs/YYYY/RUN-XXXX/``;
- each run has ``metadata.yaml`` with the minimal required fields;
- each run contains ``inputs/``, ``outputs/``, ``feedback/`` and ``logs/``;
- existing execution results were moved out of ``docs/ba-process/...``,
  ``prompts/experiments/`` and ``governance/analysis-*`` into run records;
- canonical docs, data generation and CI point at ``runs/``.
"""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_METADATA_FIELDS = ("run_id", "process", "version", "date", "author", "model", "status")
RUN_ID_PATTERN = re.compile(r"^RUN-\d{4}$")
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")

EXPECTED_RUNS = {
    "RUN-0001": {
        "year": "2026",
        "files": ["outputs/tz-stats-prototype-2026-05.md"],
        "old_paths": ["prompts/experiments/tz-stats-prototype-2026-05.md"],
    },
    "RUN-0002": {
        "year": "2026",
        "files": ["outputs/user-story_gen-from-raw-request_2026-05-26.md"],
        "old_paths": ["prompts/experiments/user-story_gen-from-raw-request_2026-05-26.md"],
    },
    "RUN-0003": {
        "year": "2026",
        "files": ["outputs/usecase_gen-stepwise-alignment_2026-05-26.md"],
        "old_paths": ["prompts/experiments/usecase_gen-stepwise-alignment_2026-05-26.md"],
    },
    "RUN-0004": {
        "year": "2026",
        "files": ["outputs/prompts-audit-2026-05-26.md"],
        "old_paths": ["prompts/experiments/prompts-audit-2026-05-26.md"],
    },
    "RUN-0005": {
        "year": "2026",
        "files": ["outputs/prompts-selftest-2026-05-26.md"],
        "old_paths": ["prompts/experiments/prompts-selftest-2026-05-26.md"],
    },
    "RUN-0006": {
        "year": "2026",
        "files": ["outputs/session-debug-summarizer-2026-06-13.md"],
        "old_paths": ["prompts/experiments/session-debug-summarizer-2026-06-13.md"],
    },
    "RUN-0007": {
        "year": "2026",
        "files": ["outputs/fr-generation-1027-live_2026-06-16.md"],
        "old_paths": ["prompts/experiments/fr-generation-1027-live_2026-06-16.md"],
    },
    "RUN-0008": {
        "year": "2026",
        "files": ["outputs/kb-citation-check-2026-06-16.md"],
        "old_paths": ["prompts/experiments/kb-citation-check-2026-06-16.md"],
    },
    "RUN-0009": {
        "year": "2026",
        "files": ["outputs/standards-applied-ab-2026-06-16.md"],
        "old_paths": ["prompts/experiments/standards-applied-ab-2026-06-16.md"],
    },
    "RUN-0010": {
        "year": "2026",
        "files": [
            "outputs/2026-06-17-bcreq-1025-email-routing.md",
            "outputs/analysis-bcreq-1025-2026-06-17.md",
        ],
        "old_paths": [
            "prompts/experiments/2026-06-17-bcreq-1025-email-routing.md",
            "governance/analysis-bcreq-1025-2026-06-17.md",
        ],
    },
    "RUN-0011": {
        "year": "2026",
        "files": [
            "inputs/kb-files.md",
            "inputs/raw-requirement.md",
            "outputs/README.md",
            "outputs/final-artifact.md",
            "outputs/prompts-chain.md",
            "outputs/steps/step-1-glossary.md",
            "outputs/steps/step-2-normalization.md",
            "outputs/steps/step-3-questions.md",
            "outputs/steps/step-4-story.md",
            "outputs/steps/step-5-options.md",
            "logs/experiment-log.md",
        ],
        "old_paths": [
            "docs/ba-process/multichannel-agent-workload/README.md",
            "docs/ba-process/multichannel-agent-workload/experiment-log.md",
            "docs/ba-process/multichannel-agent-workload/final-artifact.md",
            "docs/ba-process/multichannel-agent-workload/inputs/kb-files.md",
            "docs/ba-process/multichannel-agent-workload/inputs/raw-requirement.md",
            "docs/ba-process/multichannel-agent-workload/prompts-chain.md",
            "docs/ba-process/multichannel-agent-workload/steps/step-1-glossary.md",
            "docs/ba-process/multichannel-agent-workload/steps/step-2-normalization.md",
            "docs/ba-process/multichannel-agent-workload/steps/step-3-questions.md",
            "docs/ba-process/multichannel-agent-workload/steps/step-4-story.md",
            "docs/ba-process/multichannel-agent-workload/steps/step-5-options.md",
        ],
    },
    "RUN-0012": {
        "year": "2026",
        "files": [
            "inputs/01-raw-task-and-change-decision.md",
            "inputs/02-previous-ft-audio-conference.md",
            "inputs/03-kb-extracts.md",
            "outputs/2026-06-22-bcreq-180-mt-group-video-call-ft.md",
            "outputs/summary-bcreq-180-2026-06-22.md",
            "logs/experiment-log.md",
        ],
        "old_paths": [],
    },
    "RUN-0013": {
        "year": "2026",
        "files": [
            "inputs/issue-1027.md",
            "outputs/section-4-3-api.md",
            "feedback/corrections.md",
            "feedback/contract-issues.md",
            "logs/generation.log",
        ],
        "old_paths": [
            "runs/bcreq-1027/README.md",
            "runs/bcreq-1027/metadata.yaml",
            "runs/bcreq-1027/artifacts/section-4-3-api.md",
        ],
    },
    "RUN-0014": {
        "year": "2026",
        "files": [
            "inputs/01-raw-request-and-qa.md",
            "inputs/02-kb-extracts.md",
            "outputs/2026-06-24-bcreq-1040-speech-analytics-direction-grouping-fr.md",
            "outputs/analysis-bcreq-1040-scope-2026-06-24.md",
            "logs/business-task-log.md",
        ],
        "old_paths": [],
    },
    "RUN-0015": {
        "year": "2026",
        "files": [
            "inputs/issue-226.md",
            "inputs/research-sources.md",
            "outputs/rfc-generation-contract-test-report.md",
            "logs/validation-log.md",
        ],
        "old_paths": [],
    },
    "RUN-0016": {
        "year": "2026",
        "files": [
            "inputs/01-raw-request-and-qa.md",
            "inputs/02-kb-extracts.md",
            "outputs/2026-06-25-bcreq-765-headhunter-chat-cc-integration-fr.md",
            "outputs/analysis-bcreq-765-scope-2026-06-25.md",
            "logs/business-task-log.md",
        ],
        "old_paths": [],
    },
}


def read_text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def require_path(path: str) -> list[str]:
    return [] if (ROOT / path).exists() else [f"{path}: missing"]


def require_text(path: str, *needles: str) -> list[str]:
    text = read_text(path)
    return [f"{path}: missing {needle!r}" for needle in needles if needle not in text]


def parse_simple_yaml(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.+?)\s*$", line)
        if match:
            data[match.group(1)] = match.group(2).strip().strip('"')
    return data


def check_run(run_id: str, spec: dict[str, object]) -> list[str]:
    errors: list[str] = []
    year = str(spec["year"])
    run_dir = ROOT / "runs" / year / run_id

    if not run_dir.exists():
        return [f"runs/{year}/{run_id}: missing run directory"]

    for subdir in ("inputs", "outputs", "feedback", "logs"):
        if not (run_dir / subdir).is_dir():
            errors.append(f"runs/{year}/{run_id}/{subdir}: missing required subdirectory")

    metadata_path = run_dir / "metadata.yaml"
    if not metadata_path.exists():
        errors.append(f"runs/{year}/{run_id}/metadata.yaml: missing")
    else:
        metadata = parse_simple_yaml(metadata_path)
        for field in REQUIRED_METADATA_FIELDS:
            if not metadata.get(field):
                errors.append(f"runs/{year}/{run_id}/metadata.yaml: missing {field!r}")
        if metadata.get("run_id") != run_id:
            errors.append(
                f"runs/{year}/{run_id}/metadata.yaml: run_id {metadata.get('run_id')!r} != {run_id!r}"
            )
        if metadata.get("run_id") and not RUN_ID_PATTERN.match(metadata["run_id"]):
            errors.append(f"runs/{year}/{run_id}/metadata.yaml: invalid run_id format")
        if metadata.get("date") and not DATE_PATTERN.match(metadata["date"]):
            errors.append(f"runs/{year}/{run_id}/metadata.yaml: invalid date format")

    for relative in spec["files"]:  # type: ignore[index]
        target = run_dir / str(relative)
        if not target.exists():
            errors.append(f"{target.relative_to(ROOT)}: expected moved artifact is missing")

    return errors


def check_expected_runs() -> list[str]:
    errors: list[str] = []

    for run_id in EXPECTED_RUNS:
        errors += check_run(run_id, EXPECTED_RUNS[run_id])

    actual_run_dirs = sorted(path.name for path in (ROOT / "runs" / "2026").glob("RUN-*") if path.is_dir()) if (ROOT / "runs" / "2026").exists() else []
    expected_run_dirs = sorted(EXPECTED_RUNS)
    if actual_run_dirs != expected_run_dirs:
        errors.append(f"runs/2026: expected {expected_run_dirs}, found {actual_run_dirs}")

    for spec in EXPECTED_RUNS.values():
        for old_path in spec["old_paths"]:  # type: ignore[index]
            if (ROOT / str(old_path)).exists():
                errors.append(f"{old_path}: moved execution result still exists at old path")

    return errors


def check_docs_and_ci() -> list[str]:
    errors: list[str] = []
    for path in (
        "runs/README.md",
        "standards/runs-contract-standard.md",
        "docs/ba-process/README.md",
        "docs/ba-processes/README.md",
        "README.md",
        "CHANGELOG.md",
        ".github/workflows/github-pages.yml",
        "scripts/generate-pages-data.mjs",
    ):
        errors += require_path(path)
    if errors:
        return errors

    errors += require_text(
        "runs/README.md",
        "run_id",
        "process",
        "version",
        "date",
        "author",
        "model",
        "status",
        "RUN-XXXX",
    )
    errors += require_text(
        "standards/runs-contract-standard.md",
        "runs/YYYY/RUN-XXXX/",
        "metadata.yaml",
        "scripts/validate_issue_123_runs_contract.py",
    )
    errors += require_text("README.md", "runs/", "Единый каталог результатов")
    errors += require_text("docs/ba-process/README.md", "runs/")
    errors += require_text("docs/ba-processes/README.md", "runs/")
    errors += require_text("CHANGELOG.md", "Issue #123", "runs/")
    errors += require_text(
        ".github/workflows/github-pages.yml",
        "Validate issue #123 runs contract",
        "scripts/validate_issue_123_runs_contract.py",
    )
    errors += require_text("scripts/generate-pages-data.mjs", "RUNS_DIR", "loadExperiments")
    return errors


def main() -> int:
    errors = []
    errors += check_expected_runs()
    errors += check_docs_and_ci()

    if errors:
        print("issue-123 runs contract validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("issue-123 runs contract validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
