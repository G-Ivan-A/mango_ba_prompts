#!/usr/bin/env python3
"""Regression check for issue #247 backlog contract and normalized backlog."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

BACKLOG = Path("governance/BACKLOG.md")
MIGRATION_REGISTRY = Path("governance/migration-issues-registry.md")
CHANGELOG = Path("CHANGELOG.md")
WORKFLOW = Path(".github/workflows/github-pages.yml")
VALIDATOR = Path("scripts/validate_issue_247_backlog_contract.py")

TABLE_HEADER = "| ID | Title | Type | Priority | Status | Blocked by | Blocks | Evidence |"

ALLOWED_PRIORITIES = {"P1", "P2", "P3"}
ALLOWED_STATUSES = {"TODO", "IN PROGRESS", "REVIEW", "DONE", "BLOCKED", "DEFERRED"}

REQUIRED_ITEM_IDS = {
    "M-001",
    "M-002",
    "M-003",
    "M-004",
    "M-005",
    "M-006",
    "M-007",
    "M-008",
    "M-009",
    "OQ-001",
    "OQ-002",
    "OQ-003",
    "OQ-004",
    "RFC-243-01",
    "RFC-243-02",
    "RFC-243-03",
    "RFC-243-04",
    "RFC-243-05",
    "RFC-243-06",
    "RFC-243-07",
    "RFC-243-08",
    "BKL-247-01",
    "BKL-247-02",
    "BKL-247-03",
    "BKL-247-04",
    "BKL-247-05",
}


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    sys.exit(1)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def read_text(path: Path) -> str:
    full_path = ROOT / path
    require(full_path.exists(), f"missing file: {path}")
    return full_path.read_text(encoding="utf-8")


def parse_backlog_rows(text: str) -> dict[str, list[str]]:
    rows: dict[str, list[str]] = {}
    item_id_re = re.compile(r"^(?:M|OQ|RFC-243|BKL-247)-[0-9]+$")

    for line in text.splitlines():
        if not line.startswith("| "):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 8 or not item_id_re.match(cells[0]):
            continue
        rows[cells[0]] = cells
    return rows


def validate_backlog() -> None:
    text = read_text(BACKLOG)

    required_fragments = (
        "title: \"Backlog: Mango BA Prompts\"",
        "updated: 2026-06-25",
        "# BACKLOG: Mango BA Prompts",
        "## 1. Backlog contract",
        "### 1.2. Root cause of inconsistency",
        "### 1.3. Industry baseline",
        "### 1.4. Project backlog format",
        "### 1.5. Write and read rules",
        "## 2. Sprint index",
        "## 3. Sprint: Migration Phase 1",
        "## 4. Sprint: Open questions",
        "## Sprint RFC-243: BA processes and observability",
        "## 6. Sprint: Backlog governance",
        "GitHub Projects",
        "Jira Scrum backlog",
        "Linear cycles",
        "Notion roadmap database",
        "https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/about-projects",
        "https://support.atlassian.com/jira-software-cloud/docs/use-your-scrum-backlog/",
        "https://linear.app/docs/use-cycles",
        "https://www.notion.com/use-case/project-management/ai-product-roadmap",
        "Причина неконсистентности",
        "Индустриальная норма",
        "Issue #247",
        "CHANGELOG.md",
    )
    for fragment in required_fragments:
        require(fragment in text, f"{BACKLOG}: missing {fragment!r}")

    require(text.count(TABLE_HEADER) >= 4, f"{BACKLOG}: expected normalized backlog tables")

    rows = parse_backlog_rows(text)
    missing = sorted(REQUIRED_ITEM_IDS - set(rows))
    require(not missing, f"{BACKLOG}: missing backlog item rows: {', '.join(missing)}")

    for item_id, cells in sorted(rows.items()):
        _, title, item_type, priority, status, blocked_by, blocks, evidence = cells
        require(title, f"{BACKLOG}: {item_id} has empty title")
        require(item_type, f"{BACKLOG}: {item_id} has empty type")
        require(priority in ALLOWED_PRIORITIES, f"{BACKLOG}: {item_id} invalid priority {priority!r}")
        require(status in ALLOWED_STATUSES, f"{BACKLOG}: {item_id} invalid status {status!r}")
        require(blocked_by, f"{BACKLOG}: {item_id} has empty Blocked by")
        require(blocks, f"{BACKLOG}: {item_id} has empty Blocks")
        require(evidence, f"{BACKLOG}: {item_id} has empty evidence")

    for item_id in [f"M-{number:03d}" for number in range(1, 10)]:
        require(rows[item_id][4] == "DONE", f"{BACKLOG}: {item_id} must reflect closed migration issue")

    for item_id in [f"RFC-243-{number:02d}" for number in range(1, 9)]:
        require(rows[item_id][3] in ALLOWED_PRIORITIES, f"{BACKLOG}: {item_id} missing priority")
        require(rows[item_id][4] in {"TODO", "BLOCKED"}, f"{BACKLOG}: {item_id} must remain not done")

    for item_id in [f"BKL-247-{number:02d}" for number in range(1, 6)]:
        require(rows[item_id][4] == "REVIEW", f"{BACKLOG}: {item_id} should be in PR review")


def validate_project_hooks() -> None:
    registry = read_text(MIGRATION_REGISTRY)
    require("Open" not in registry, f"{MIGRATION_REGISTRY}: must not retain stale Open statuses")
    for number in range(1, 10):
        require(f"M-{number:03d}" in registry, f"{MIGRATION_REGISTRY}: missing M-{number:03d}")
        require("Closed 2026-06-" in registry, f"{MIGRATION_REGISTRY}: missing closed dates")

    changelog = read_text(CHANGELOG)
    for fragment in (
        "Issue #247",
        BACKLOG.as_posix(),
        MIGRATION_REGISTRY.as_posix(),
        VALIDATOR.as_posix(),
        "Индустриальная норма",
    ):
        require(fragment in changelog, f"{CHANGELOG}: missing {fragment!r}")

    workflow = read_text(WORKFLOW)
    require(
        "Validate issue #247 backlog contract" in workflow,
        f"{WORKFLOW}: missing validation step name",
    )
    require(VALIDATOR.as_posix() in workflow, f"{WORKFLOW}: missing validator path")


def main() -> None:
    validate_backlog()
    validate_project_hooks()
    print("OK: issue #247 backlog contract validated")


if __name__ == "__main__":
    main()
