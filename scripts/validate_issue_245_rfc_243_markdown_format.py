#!/usr/bin/env python3
"""Regression check for issue #245: RFC-243 must be readable Markdown."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

RFC = Path("governance/rfc/ba-processes-observability-implementation-proposal.md")
ISSUE_243_VALIDATOR = Path("scripts/validate_issue_243_ba_processes_observability_rfc.py")
VALIDATOR = Path("scripts/validate_issue_245_rfc_243_markdown_format.py")
WORKFLOW = Path(".github/workflows/github-pages.yml")
CHANGELOG = Path("CHANGELOG.md")

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

REQUIRED_DECISION_FRAGMENTS = (
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
    "applied_operations",
    "applied_prompts",
)

FORBIDDEN_BODY_YAML_KEYS = (
    "context:",
    "problems:",
    "alternatives:",
    "rationale:",
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


def fenced_yaml_ranges(body: str) -> list[tuple[int, int]]:
    ranges: list[tuple[int, int]] = []
    start = None
    for index, line in enumerate(body.splitlines(), start=1):
        if line.strip() == "```yaml":
            require(start is None, f"{RFC}: nested YAML fence starts at body line {index}")
            start = index
            continue
        if line.strip() == "```" and start is not None:
            ranges.append((start, index))
            start = None
    require(start is None, f"{RFC}: unterminated YAML fence starting at body line {start}")
    return ranges


def line_after_heading_is_yaml(body: str, heading: str) -> bool:
    lines = body.splitlines()
    for index, line in enumerate(lines):
        if line.strip() != heading:
            continue
        for next_line in lines[index + 1 :]:
            if not next_line.strip():
                continue
            return next_line.strip() == "```yaml"
    return False


def validate_rfc_format() -> None:
    text = read_text(RFC)
    _frontmatter, body = split_frontmatter(RFC, text)
    require_ordered_sections(RFC, body)

    for fragment in REQUIRED_DECISION_FRAGMENTS:
        require(fragment in text, f"{RFC}: missing agreed decision fragment {fragment!r}")

    root_cause_fragments = (
        "Причина нарушения формата",
        "machine_readable_shape",
        "L1",
        "L3 RFC",
        "YAML",
        "Markdown",
    )
    for fragment in root_cause_fragments:
        require(fragment in text, f"{RFC}: missing format root-cause fragment {fragment!r}")

    ranges = fenced_yaml_ranges(body)
    body_lines = body.splitlines()
    yaml_line_count = sum(end - start + 1 for start, end in ranges)
    yaml_ratio = yaml_line_count / max(len(body_lines), 1)
    require(
        yaml_ratio <= 0.45,
        f"{RFC}: YAML fences dominate the body ({yaml_line_count}/{len(body_lines)} lines)",
    )
    require(len(ranges) <= 5, f"{RFC}: too many fenced YAML blocks ({len(ranges)} > 5)")

    for heading in REQUIRED_SECTIONS[:6]:
        require(
            not line_after_heading_is_yaml(body, heading),
            f"{RFC}: {heading!r} must start with readable Markdown, not YAML",
        )

    for key in FORBIDDEN_BODY_YAML_KEYS:
        require(
            not re.search(rf"```yaml\s*\n{re.escape(key)}", body),
            f"{RFC}: body must not encode {key!r} as a top-level YAML block",
        )

    required_machine_readable_inserts = (
        "proposal_traceability:",
        "impact:",
        "implementation_plan:",
        "canonical_criteria:",
    )
    for key in required_machine_readable_inserts:
        require(
            re.search(rf"```yaml[\s\S]*\n{re.escape(key)}", body),
            f"{RFC}: missing required machine-readable insert {key!r}",
        )


def validate_project_hooks() -> None:
    workflow = read_text(WORKFLOW)
    require(
        "Validate issue #245 RFC-243 Markdown format" in workflow,
        f"{WORKFLOW}: missing validation step name",
    )
    require(VALIDATOR.as_posix() in workflow, f"{WORKFLOW}: missing validator path")

    changelog = read_text(CHANGELOG)
    for fragment in (
        "Issue #245",
        RFC.as_posix(),
        ISSUE_243_VALIDATOR.as_posix(),
        VALIDATOR.as_posix(),
        "Причина нарушения формата",
    ):
        require(fragment in changelog, f"{CHANGELOG}: missing {fragment!r}")


def main() -> None:
    validate_rfc_format()
    validate_project_hooks()
    print("OK: issue #245 RFC-243 Markdown format validated")


if __name__ == "__main__":
    main()
