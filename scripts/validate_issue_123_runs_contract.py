#!/usr/bin/env python3
"""Regression check for issue #123 — unified runs/ execution records.

The check locks the Phase 0 contract from issue #123:

- every run lives under ``runs/YYYY/RUN-XXXX/``;
- each run has ``metadata.yaml`` with the minimal required fields;
- each run contains ``inputs/``, ``outputs/``, ``feedback/`` and ``logs/``;
- existing execution results were moved out of ``docs/ba-process/...``,
  ``prompts/experiments/`` and ``governance/analysis-*`` into run records;
- canonical docs, data generation and CI point at ``runs/``.

Issue #293 extends the contract with explicit run types:

- ``metadata.yaml`` MAY declare ``run_type``; allowed values are ``execution``,
  ``statistics`` and ``legacy``. A missing field is read as ``execution``
  (backward compatibility with runs recorded before issue #293);
- a run MUST NOT reach outside its own directory: every path in ``inputs``,
  ``outputs``, ``logs``, ``feedback`` and ``source_paths`` stays inside
  ``runs/YYYY/RUN-XXXX/`` and never points at ``prompts/``, ``kb/``,
  ``site/data/`` or ``patterns/``;
- the standard and the registry document both rules.
"""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_METADATA_FIELDS = ("run_id", "process", "version", "date", "author", "model", "status")
RUN_ID_PATTERN = re.compile(r"^RUN-\d{4}$")
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")

# issue #293: explicit run types.
ALLOWED_RUN_TYPES = ("execution", "statistics", "legacy")
DEFAULT_RUN_TYPE = "execution"
# Path fields whose values are artifacts of the run itself and therefore
# MUST stay inside runs/YYYY/RUN-XXXX/. ``related_artifacts`` is traceability,
# not an artifact of the run, so it is deliberately excluded.
RUN_PATH_FIELDS = ("inputs", "outputs", "logs", "feedback", "source_paths")
# Working artifacts a run is never allowed to touch.
PROTECTED_DIRS = ("prompts/", "kb/", "site/data/", "patterns/")

EXPECTED_RUNS = {
    "RUN-0001": {
        "year": "2026",
        "run_type": "execution",
        "files": ["outputs/tz-stats-prototype-2026-05.md"],
        "old_paths": ["prompts/experiments/tz-stats-prototype-2026-05.md"],
    },
    "RUN-0002": {
        "year": "2026",
        "run_type": "execution",
        "files": ["outputs/user-story_gen-from-raw-request_2026-05-26.md"],
        "old_paths": ["prompts/experiments/user-story_gen-from-raw-request_2026-05-26.md"],
    },
    "RUN-0003": {
        "year": "2026",
        "run_type": "execution",
        "files": ["outputs/usecase_gen-stepwise-alignment_2026-05-26.md"],
        "old_paths": ["prompts/experiments/usecase_gen-stepwise-alignment_2026-05-26.md"],
    },
    "RUN-0004": {
        "year": "2026",
        "run_type": "statistics",
        "files": ["outputs/prompts-audit-2026-05-26.md"],
        "old_paths": ["prompts/experiments/prompts-audit-2026-05-26.md"],
    },
    "RUN-0005": {
        "year": "2026",
        "run_type": "statistics",
        "files": ["outputs/prompts-selftest-2026-05-26.md"],
        "old_paths": ["prompts/experiments/prompts-selftest-2026-05-26.md"],
    },
    "RUN-0006": {
        "year": "2026",
        "run_type": "execution",
        "files": ["outputs/session-debug-summarizer-2026-06-13.md"],
        "old_paths": ["prompts/experiments/session-debug-summarizer-2026-06-13.md"],
    },
    "RUN-0007": {
        "year": "2026",
        "run_type": "execution",
        "files": ["outputs/fr-generation-1027-live_2026-06-16.md"],
        "old_paths": ["prompts/experiments/fr-generation-1027-live_2026-06-16.md"],
    },
    "RUN-0008": {
        "year": "2026",
        "run_type": "statistics",
        "files": ["outputs/kb-citation-check-2026-06-16.md"],
        "old_paths": ["prompts/experiments/kb-citation-check-2026-06-16.md"],
    },
    "RUN-0009": {
        "year": "2026",
        "run_type": "statistics",
        "files": ["outputs/standards-applied-ab-2026-06-16.md"],
        "old_paths": ["prompts/experiments/standards-applied-ab-2026-06-16.md"],
    },
    "RUN-0010": {
        "year": "2026",
        "run_type": "statistics",
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
        "run_type": "execution",
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
        "run_type": "execution",
        "files": [
            "inputs/raw-requirement.md",
            "outputs/README.md",
            "outputs/final-artifact.md",
            "outputs/prompts-chain.md",
            "outputs/steps/step-1-glossary.md",
            "outputs/steps/step-2-normalization.md",
            "outputs/steps/step-3-questions.md",
            "outputs/steps/step-4-scenarios.md",
            "outputs/steps/step-5-fr.md",
            "outputs/steps/step-6-constraints.md",
            "logs/experiment-log.md",
        ],
        "old_paths": [],
    },
    "RUN-0013": {
        "year": "2026",
        "run_type": "statistics",
        "files": [
            "inputs/chat-export.md",
            "inputs/raw-requirement.md",
            "outputs/README.md",
            "outputs/final-artifact.md",
            "outputs/prompts-chain.md",
            "outputs/steps/step-1-research-and-questions.md",
            "outputs/steps/step-2-state-matrix.md",
            "outputs/steps/step-3-customer-answers.md",
            "outputs/steps/step-4-glossary-and-context.md",
            "outputs/steps/step-5-top-level-fr.md",
            "outputs/steps/step-6-fr-detail-and-constraints.md",
            "outputs/steps/step-7-rework-after-meeting.md",
            "outputs/steps/step-8-usecase-matrix.md",
            "feedback/review-notes.md",
            "logs/experiment-log.md",
        ],
        "old_paths": [],
    },
    "RUN-0014": {
        "year": "2026",
        "run_type": "statistics",
        "files": [
            "inputs/raw-requirement.md",
            "inputs/kb-files.md",
            "inputs/chat-export-1075.json",
            "outputs/README.md",
            "outputs/final-artifact.md",
            "outputs/prompts-chain.md",
            "outputs/steps/step-0-as-is.md",
            "outputs/steps/step-1-fact-check-and-uncertainty.md",
            "outputs/steps/step-2-contradictions.md",
            "feedback/ba-review.md",
            "logs/experiment-log.md",
            "logs/metrics.md",
            "logs/chat-transcript.md",
        ],
        "old_paths": [],
    },
    "RUN-0017": {
        "run_type": "statistics",
        "year": "2026",
        "files": [
            "inputs/README.md",
            "inputs/transcript.md",
            "inputs/1076-chat-export-1787301046512.json",
            "outputs/README.md",
            "outputs/final-artifact.md",
            "outputs/prompts-chain.md",
            "outputs/quality-findings.md",
            "outputs/steps/step-1-as-is-and-glossary.md",
            "outputs/steps/step-2-object-model.md",
            "outputs/steps/step-3-section-2-agreed.md",
            "outputs/steps/step-4-scenarios.md",
            "outputs/steps/step-5-mtalker-facts.md",
            "outputs/steps/step-6-fr-v1-and-rework.md",
            "outputs/steps/step-7-fr-detailed.md",
            "outputs/steps/step-8-constraints-and-matrix.md",
            "outputs/steps/step-9-responsibility-boundary.md",
            "outputs/steps/step-10-doc-verification.md",
            "outputs/steps/step-11-manager-comment.md",
            "feedback/ba-review-notes.md",
            "logs/experiment-log.md",
            "logs/turn-metrics.md",
        ],
        "old_paths": [],
    },
    "RUN-0018": {
        "year": "2026",
        "run_type": "statistics",
        "files": [
            "inputs/README.md",
            "inputs/chat-export.md",
            "inputs/raw-requirement.md",
            "inputs/kb-facts.md",
            "outputs/README.md",
            "outputs/final-artifact.md",
            "outputs/prompts-chain.md",
            "outputs/steps/step-1-init-strategy.md",
            "outputs/steps/step-2-audit-report.md",
            "outputs/steps/step-3-fr-v1.1.md",
            "outputs/steps/step-4-check-multiple-ids.md",
            "outputs/steps/step-5-contradiction-check.md",
            "outputs/steps/step-6-terminology-check.md",
            "outputs/steps/step-7-proofreading-v1.2.md",
            "outputs/steps/step-8-constraint-v1.3.md",
            "feedback/review-notes.md",
            "logs/experiment-log.md",
            "logs/metrics.md",
        ],
        "old_paths": [],
    },
    "RUN-0020": {
        "run_type": "statistics",
        "year": "2026",
        "files": [
            "inputs/README.md",
            "inputs/transcript.md",
            "inputs/1065-chat-export-1787301452625.json",
            "outputs/README.md",
            "outputs/final-artifact.md",
            "outputs/prompts-chain.md",
            "outputs/quality-findings.md",
            "outputs/steps/step-1-prompt-and-glossary.md",
            "outputs/steps/step-2-business-logic-shift.md",
            "outputs/steps/step-3-factcheck-failure.md",
            "outputs/steps/step-4-customer-docs-are-claims.md",
            "outputs/steps/step-5-pdn-role-model.md",
            "outputs/steps/step-6-block1-structure.md",
            "outputs/steps/step-7-numbering-and-regression.md",
            "outputs/steps/step-8-doc-errors-and-rule.md",
            "outputs/steps/step-9-invented-structure.md",
            "outputs/steps/step-10-block1-template-and-markers.md",
            "outputs/steps/step-11-factcheck-bitrix-fcr-fte.md",
            "outputs/steps/step-12-block2-fabrication.md",
            "outputs/steps/step-13-realtime-and-memory-rule.md",
            "outputs/steps/step-14-regeneration-loop.md",
            "feedback/ba-review-notes.md",
            "logs/experiment-log.md",
            "logs/turn-metrics.md",
        ],
        "old_paths": [],
    },
    "RUN-0021": {
        "year": "2026",
        "run_type": "statistics",
        "files": [
            "metadata.yaml",
            "inputs/README.md",
            "inputs/chat-transcript.md",
            "outputs/README.md",
            "outputs/prompts-chain.md",
            "outputs/final-artifact.md",
            "outputs/steps/step-1-glossary-init.md",
            "outputs/steps/step-2-fr-strategy-and-source-access.md",
            "outputs/steps/step-3-manual-audit-report.md",
            "outputs/steps/step-4-fr-v1.1.md",
            "outputs/steps/step-5-entity-hierarchy-fix.md",
            "outputs/steps/step-6-section-3-restructure.md",
            "outputs/steps/step-7-ui-vs-business-terms.md",
            "outputs/steps/step-8-kpi-item-rollback.md",
            "outputs/steps/step-9-variants-and-dialing-modes.md",
            "outputs/steps/step-10-defaults-and-atomicity.md",
            "outputs/steps/step-11-rule-term-and-audit.md",
            "outputs/steps/step-12-v1.5-and-call-vs-attempt.md",
            "outputs/steps/step-13-goal-2.3-cleanup.md",
            "outputs/steps/step-14-final-proofreading-rounds.md",
            "feedback/review-notes.md",
            "logs/experiment-log.md",
            "logs/metrics.md",
            "logs/turn-metrics.md",
        ],
        "old_paths": [],
    },
    "RUN-0023": {
        "year": "2026",
        "run_type": "statistics",
        "files": [
            "inputs/README.md",
            "inputs/transcript.md",
            "inputs/raw-requirement.md",
            "inputs/1040-chat-export-1787301483841.json",
            "outputs/README.md",
            "outputs/final-artifact.md",
            "outputs/prompts-chain.md",
            "outputs/quality-findings.md",
            "outputs/steps/step-1-init-handshake.md",
            "outputs/steps/step-2-fr-proposal-variant-1.md",
            "outputs/steps/step-3-revalidation-variant-2.md",
            "feedback/review-notes.md",
            "logs/experiment-log.md",
            "logs/metrics.md",
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


def parse_yaml_lists(path: Path) -> dict[str, list[str]]:
    """Collect ``key:`` blocks followed by ``  - value`` items.

    Deliberately minimal: run metadata uses flat scalars and flat lists only.
    """

    data: dict[str, list[str]] = {}
    current: str | None = None
    for line in path.read_text(encoding="utf-8").splitlines():
        key_match = re.match(r"^([A-Za-z0-9_-]+):\s*$", line)
        if key_match:
            current = key_match.group(1)
            data.setdefault(current, [])
            continue
        item_match = re.match(r"^\s+-\s+(.+?)\s*$", line)
        if item_match and current:
            data[current].append(item_match.group(1).strip().strip('"'))
            continue
        if re.match(r"^([A-Za-z0-9_-]+):\s*\S", line):
            current = None
    return data


def effective_run_type(metadata: dict[str, str]) -> str:
    """``run_type`` of a run; runs recorded before issue #293 default to execution."""

    return metadata.get("run_type") or DEFAULT_RUN_TYPE


def check_run_type(location: str, metadata: dict[str, str]) -> list[str]:
    declared = metadata.get("run_type")
    if declared is None:
        return []
    if declared not in ALLOWED_RUN_TYPES:
        return [
            f"{location}: run_type {declared!r} not in {list(ALLOWED_RUN_TYPES)}"
        ]
    return []


def check_run_boundaries(location: str, run_prefix: str, path: Path) -> list[str]:
    """Issue #293: run artifacts MUST stay inside runs/YYYY/RUN-XXXX/."""

    errors: list[str] = []
    lists = parse_yaml_lists(path)
    for field in RUN_PATH_FIELDS:
        for value in lists.get(field, []):
            if value.startswith(PROTECTED_DIRS):
                errors.append(
                    f"{location}: {field} points at protected working artifact {value!r}"
                )
                continue
            normalized = value if value.startswith("runs/") else f"{run_prefix}/{value}"
            if not normalized.startswith(f"{run_prefix}/"):
                errors.append(
                    f"{location}: {field} path {value!r} escapes {run_prefix}/"
                )
    return errors


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

        location = f"runs/{year}/{run_id}/metadata.yaml"
        errors += check_run_type(location, metadata)
        errors += check_run_boundaries(location, f"runs/{year}/{run_id}", metadata_path)

        expected_type = spec.get("run_type")
        if expected_type and effective_run_type(metadata) != expected_type:
            errors.append(
                f"{location}: run_type {effective_run_type(metadata)!r} != registry {expected_type!r}"
            )

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


def check_registry_run_types() -> list[str]:
    """Every run in the registry table carries its run_type column."""

    errors: list[str] = []
    text = read_text("runs/README.md")
    for run_id, spec in EXPECTED_RUNS.items():
        expected = str(spec["run_type"])  # type: ignore[index]
        row = [line for line in text.splitlines() if line.startswith(f"| [`{run_id}`]")]
        if not row:
            errors.append(f"runs/README.md: no registry row for {run_id}")
        elif f"`{expected}`" not in row[0]:
            errors.append(f"runs/README.md: {run_id} row missing run_type `{expected}`")
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
        "run_type",
        "execution",
        "statistics",
        "## Типы прогонов",
        "## Границы прогона",
    )
    errors += require_text(
        "standards/runs-contract-standard.md",
        "runs/YYYY/RUN-XXXX/",
        "metadata.yaml",
        "scripts/validate_issue_123_runs_contract.py",
        "run_type",
        "## Типы прогонов",
        "## Границы прогона",
        "`prompts/`, `kb/`, `site/data/`, `patterns/`",
    )
    errors += require_text("README.md", "runs/", "Единый каталог результатов")
    errors += require_text("docs/ba-process/README.md", "runs/")
    errors += require_text("docs/ba-processes/README.md", "runs/")
    errors += require_text("CHANGELOG.md", "Issue #123", "runs/", "Issue #293", "run_type")
    errors += require_path("docs/analysis/2026-08-21-runs-type-gap-analysis.md")
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
    errors += check_registry_run_types()

    if errors:
        print("issue-123 runs contract validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("issue-123 runs contract validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
