#!/usr/bin/env python3
"""Regression check for issue #243 RFC and implementation sprint."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

RFC = Path("governance/rfc/ba-processes-observability-implementation-proposal.md")
BACKLOG = Path("governance/BACKLOG.md")
REGISTER = Path("governance/rfc-register.md")
CHANGELOG = Path("CHANGELOG.md")
WORKFLOW = Path(".github/workflows/github-pages.yml")
VALIDATOR = Path("scripts/validate_issue_243_ba_processes_observability_rfc.py")

REQUIRED_SECTIONS = (
    "## 1. Context and motivation",
    "## 2. Problem",
    "## 3. Proposal",
    "## 4. Alternatives considered",
    "## 5. Rationale",
    "## 6. Impact",
    "## 7. Implementation plan",
    "## 8. Canonical criteria",
)


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


def split_frontmatter(path: Path, text: str) -> tuple[str, str]:
    require(text.startswith("---\n"), f"{path}: missing YAML frontmatter")
    end = text.find("\n---", 4)
    require(end != -1, f"{path}: unterminated YAML frontmatter")
    return text[4:end].strip(), text[end + len("\n---") :].strip()


def require_ordered_sections(path: Path, body: str) -> None:
    previous = -1
    for section in REQUIRED_SECTIONS:
        current = body.find(section)
        require(current != -1, f"{path}: missing section {section!r}")
        require(current > previous, f"{path}: section order is invalid at {section!r}")
        previous = current


def validate_rfc() -> None:
    text = read_text(RFC)
    frontmatter, body = split_frontmatter(RFC, text)

    frontmatter_needles = (
        "id: RFC-243",
        "status: draft",
        'title: "RFC-243: предложение по БА-процессам и observability"',
        'author: "OpenAI Codex"',
        "created: 2026-06-25",
        "updated: 2026-06-25",
        "layer: L3",
        "type: rfc",
        "related_contracts:",
        "target_artifacts:",
        "governance/rfc-generation-contract.md",
        "governance/bcreq-fr-generation-contract.md",
        "runs/CONTRACT.md",
        "standards/executable-contract-standard.md",
        "docs/ba-processes/00-index.md",
        "kb/operation-prompt-mapping/registry.json",
    )
    for needle in frontmatter_needles:
        require(needle in frontmatter, f"{RFC}: frontmatter missing {needle!r}")

    require_ordered_sections(RFC, body)

    required_machine_readable_inserts = (
        "proposal_traceability:",
        "impact:",
        "implementation_plan:",
        "canonical_criteria:",
    )
    for key in required_machine_readable_inserts:
        require(
            re.search(rf"(^|\n){re.escape(key)}", body),
            f"{RFC}: missing machine-readable insert {key}",
        )

    required_fragments = (
        "Почему RFC, а не ADR",
        "Причина нарушения формата",
        "machine_readable_shape",
        "Markdown-документом с YAML frontmatter",
        "requires_adr: false",
        "requires_standard: true",
        "docs/analysis/2026-06-25-runs-observability-research.md",
        "docs/analysis/2026-06-25-bcreq-fr-contract-process-analysis.md",
        "docs/analysis/2026-06-25-ba-processes-industry-analysis.md",
        "https://github.com/G-Ivan-A/mango_ba_prompts/pull/234",
        "docs/ba-processes/00-index.md",
        "governance/bcreq-fr-generation-contract.md",
        "runs/CONTRACT.md",
        "standards/executable-contract-standard.md",
        "Singular requirement",
        "User Story",
        "Use Case",
        "Business Rule",
        "Glossary term",
        "API specification",
        "OpenAPI/TMF Open API",
        "RTM entry",
        "BRD",
        "FRD/SRS",
        "RFP Response",
        "BCREQ-FR",
        "`type: frd`",
        "BCREQ-SR",
        "`type: srs`",
        "Elicitation",
        "Analysis",
        "Documentation",
        "Validation",
        "Verification",
        "Management",
        "operation_id -> prompt_id@version",
        "kb/operation-prompt-mapping/registry.json",
        "applied_operations",
        "applied_prompts",
        "research -> rfc/adr -> standard -> artifact",
        "не меняет стандарты",
    )
    for fragment in required_fragments:
        require(fragment in text, f"{RFC}: missing required fragment {fragment!r}")

    problems = set(re.findall(r"RFC-243-P[0-9]+", text))
    proposals = set(re.findall(r"RFC-243-R[0-9]+", text))
    require(len(problems) >= 6, f"{RFC}: expected at least 6 problem IDs, found {len(problems)}")
    require(len(proposals) >= 7, f"{RFC}: expected at least 7 proposal IDs, found {len(proposals)}")

    require(
        not (ROOT / "kb/operation-prompt-mapping/registry.json").exists(),
        "issue #243 must not implement kb/operation-prompt-mapping/registry.json",
    )


def validate_backlog() -> None:
    text = read_text(BACKLOG)
    marker = "## Спринт RFC-243"
    require(marker in text, f"{BACKLOG}: missing sprint section {marker!r}")
    sprint = text[text.index(marker) :]

    required_fragments = (
        "Issue #243",
        "| № | Title | Type | Priority | Dependencies | Issue in repo |",
        "Волна 0",
        "Волна 1",
        "Волна 2",
        "Волна 3",
        "independent",
        "dependent",
        "priority:P1",
        "type:implementation",
        "type:decision",
        "type:research",
        "sprint-3",
        "decision: зафиксировать RFC-243",
        "implementation: создать L2-реестр operation-prompt mapping",
        "implementation: сверить 00-index.md",
        "implementation: обновить БА-онтологию",
        "implementation: добавить applied_operations",
        "implementation: добавить applied_prompts",
        "implementation: обновить валидаторы",
        "research: оценить eTOM/SID",
    )
    for fragment in required_fragments:
        require(fragment in sprint, f"{BACKLOG}: sprint section missing {fragment!r}")

    issue_links = set(
        re.findall(
            r"https://github\.com/(?:G-Ivan-A/mango_ba_prompts|konard/G-Ivan-A-mango_ba_prompts)/issues/[0-9]+",
            sprint,
        )
    )
    require(len(issue_links) >= 8, f"{BACKLOG}: expected at least 8 issue links, found {len(issue_links)}")


def validate_register() -> None:
    text = read_text(REGISTER)
    required_fragments = (
        "RFC-243",
        RFC.as_posix(),
        "issue #243",
        "docs/analysis/2026-06-25-runs-observability-research.md",
        "docs/analysis/2026-06-25-bcreq-fr-contract-process-analysis.md",
        "docs/analysis/2026-06-25-ba-processes-industry-analysis.md",
    )
    for fragment in required_fragments:
        require(fragment in text, f"{REGISTER}: missing {fragment!r}")


def validate_project_hooks() -> None:
    changelog = read_text(CHANGELOG)
    for fragment in (
        "Issue #243",
        RFC.as_posix(),
        BACKLOG.as_posix(),
        VALIDATOR.as_posix(),
        "только proposal",
    ):
        require(fragment in changelog, f"{CHANGELOG}: missing {fragment!r}")

    workflow = read_text(WORKFLOW)
    require(
        "Validate issue #243 BA-processes observability RFC" in workflow,
        f"{WORKFLOW}: missing validation step name",
    )
    require(VALIDATOR.as_posix() in workflow, f"{WORKFLOW}: missing validator path")


def main() -> None:
    validate_rfc()
    validate_backlog()
    validate_register()
    validate_project_hooks()
    print("OK: issue #243 RFC and sprint deliverables validated")


if __name__ == "__main__":
    main()
