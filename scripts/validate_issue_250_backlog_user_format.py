#!/usr/bin/env python3
"""Regression check for issue #250 backlog structure and Russian UX."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

BACKLOG = Path("governance/BACKLOG.md")
CHANGELOG = Path("CHANGELOG.md")
WORKFLOW = Path(".github/workflows/github-pages.yml")
VALIDATOR = Path("scripts/validate_issue_250_backlog_user_format.py")

TABLE_HEADER_RU = (
    "| ID | Название | Тип | Приоритет | Статус | Блокируется | Блокирует | Подтверждение |"
)

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
    "BKL-250-01",
    "BKL-250-02",
    "BKL-250-03",
    "BKL-250-04",
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


def require_order(text: str, path: Path, fragments: tuple[str, ...]) -> None:
    previous = -1
    for fragment in fragments:
        current = text.find(fragment)
        require(current != -1, f"{path}: missing {fragment!r}")
        require(current > previous, f"{path}: wrong order at {fragment!r}")
        previous = current


def parse_backlog_rows(text: str) -> dict[str, list[str]]:
    rows: dict[str, list[str]] = {}
    item_id_re = re.compile(r"^(?:M|OQ|RFC-243|BKL-(?:247|250))-[0-9]+$")

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
        "updated: 2026-06-26",
        'primary_issue: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/250"',
        "# Бэклог Mango BA Prompts",
        "## Содержание",
        "## Рабочие спринты",
        "### Приоритетный спринт: RFC-243",
        "### Запланированный спринт: Открытые вопросы",
        "### Служебный спринт: управление бэклогом",
        "## Инструкции по управлению бэклогом",
        "### Зависимости и контракты",
        "### Промпты для создания issue по спринту",
        "## Исторические спринты",
        "### Завершённый спринт: Backlog governance #247",
        "### Завершённый спринт: Migration Phase 1",
        "## Связанные артефакты",
        "Сначала показаны рабочие и запланированные спринты",
        "Исторические данные вынесены ниже инструкций",
        "Создай GitHub issue",
        "G-Ivan-A/mango_ba_prompts",
        "priority:P1",
        "type:implementation",
        "governance/rfc-generation-contract.md",
        "governance/bcreq-fr-generation-contract.md",
        "runs/CONTRACT.md",
        "standards/executable-contract-standard.md",
    )
    for fragment in required_fragments:
        require(fragment in text, f"{BACKLOG}: missing {fragment!r}")

    require_order(
        text,
        BACKLOG,
        (
            "# Бэклог Mango BA Prompts",
            "## Содержание",
            "## Рабочие спринты",
            "### Приоритетный спринт: RFC-243",
            "### Запланированный спринт: Открытые вопросы",
            "### Служебный спринт: управление бэклогом",
            "## Инструкции по управлению бэклогом",
            "## Исторические спринты",
            "### Завершённый спринт: Backlog governance #247",
            "### Завершённый спринт: Migration Phase 1",
            "## Связанные артефакты",
        ),
    )

    require(TABLE_HEADER_RU in text, f"{BACKLOG}: missing Russian backlog table header")
    require(text.count(TABLE_HEADER_RU) >= 5, f"{BACKLOG}: expected Russian tables for all sprints")

    rows = parse_backlog_rows(text)
    missing = sorted(REQUIRED_ITEM_IDS - set(rows))
    require(not missing, f"{BACKLOG}: missing backlog item rows: {', '.join(missing)}")

    for item_id, cells in sorted(rows.items()):
        _, title, item_type, priority, status, blocked_by, blocks, evidence = cells
        require(title, f"{BACKLOG}: {item_id} has empty title")
        require(item_type, f"{BACKLOG}: {item_id} has empty type")
        require(priority in {"P1", "P2", "P3"}, f"{BACKLOG}: {item_id} invalid priority")
        require(
            status in {"TODO", "IN PROGRESS", "REVIEW", "DONE", "BLOCKED", "DEFERRED"},
            f"{BACKLOG}: {item_id} invalid status",
        )
        require(blocked_by, f"{BACKLOG}: {item_id} has empty Blocked by")
        require(blocks, f"{BACKLOG}: {item_id} has empty Blocks")
        require(evidence, f"{BACKLOG}: {item_id} has empty evidence")

    for item_id in [f"M-{number:03d}" for number in range(1, 10)]:
        require(rows[item_id][4] == "DONE", f"{BACKLOG}: {item_id} must remain historical DONE")

    for item_id in [f"BKL-247-{number:02d}" for number in range(1, 6)]:
        require(rows[item_id][4] == "DONE", f"{BACKLOG}: {item_id} must reflect merged PR #249")

    for item_id in [f"BKL-250-{number:02d}" for number in range(1, 5)]:
        require(rows[item_id][4] == "REVIEW", f"{BACKLOG}: {item_id} should be in PR review")


def validate_project_hooks() -> None:
    changelog = read_text(CHANGELOG)
    for fragment in (
        "Issue #250",
        BACKLOG.as_posix(),
        VALIDATOR.as_posix(),
        "Содержание",
        "Промпты для создания issue по спринту",
    ):
        require(fragment in changelog, f"{CHANGELOG}: missing {fragment!r}")

    workflow = read_text(WORKFLOW)
    require(
        "Validate issue #250 backlog user format" in workflow,
        f"{WORKFLOW}: missing validation step name",
    )
    require(VALIDATOR.as_posix() in workflow, f"{WORKFLOW}: missing validator path")


def main() -> None:
    validate_backlog()
    validate_project_hooks()
    print("OK: issue #250 backlog user format validated")


if __name__ == "__main__":
    main()
