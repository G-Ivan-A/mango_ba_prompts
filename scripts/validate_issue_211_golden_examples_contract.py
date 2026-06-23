#!/usr/bin/env python3
"""Regression check for issue #211: Golden Examples lifecycle contract."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

GOLDEN_ROOT = "kb/golden-examples"
README = f"{GOLDEN_ROOT}/README.md"
CONTRACT = f"{GOLDEN_ROOT}/CONTRACT.md"
BCREQ_CONTRACT = "governance/bcreq-fr-generation-contract.md"
VALIDATOR = "scripts/validate_issue_211_golden_examples_contract.py"

ARTIFACT_DIRS = (
    f"{GOLDEN_ROOT}/bcreq-fr",
    f"{GOLDEN_ROOT}/rfc",
    f"{GOLDEN_ROOT}/adr",
)

REQUIRED_CONTRACT_TEXT = (
    "contract_id: golden-examples-lifecycle-contract",
    "status: draft",
    "version: 0.1",
    "type: contract",
    "scope: golden-examples",
    "issue: \"https://github.com/G-Ivan-A/mango_ba_prompts/issues/211\"",
    "rationale:",
    "base_path: \"kb/golden-examples/\"",
    "artifact_type: bcreq-fr # | rfc | adr",
    "status: draft # | approved",
    "related_contract: \"governance/bcreq-fr-generation-contract.md\"",
    "pattern: \"example-NNN-<short-description>.md\"",
    "path + sha",
    "source_attachments:",
    "- status: \"no-golden-standard\"",
    "requires_explicit_user_confirmation: true",
    "automatic_transition_allowed: false",
    "2-факторное подтверждение",
    "governance/approval-contract.md",
)

REQUIRED_README_TEXT = (
    "# Golden Examples",
    "kb/golden-examples/CONTRACT.md",
    "bcreq-fr/",
    "rfc/",
    "adr/",
    "no-golden-standard",
)

REQUIRED_BCREQ_TEXT = (
    "source_attachments:",
    "- status: \"no-golden-standard\"",
    "kb/golden-examples/CONTRACT.md",
    "2-факторное подтверждение",
    "governance/approval-contract.md",
    VALIDATOR,
)

FORBIDDEN_BCREQ_TEXT = (
    "github.com/user-attachments",
    'comment: "Вложения из PR #202"',
    'status: "temporary"',
    "Временная трассировка вложений PR #202",
    "`bcreq-fr.txt`",
)

REQUIRED_PROJECT_TEXT = {
    "CHANGELOG.md": ("Issue #211", CONTRACT, README, VALIDATOR),
    "README.md": (GOLDEN_ROOT,),
    "governance/artifact-map.md": (GOLDEN_ROOT,),
    ".github/workflows/github-pages.yml": (
        "Validate issue #211 Golden Examples contract",
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


def section_between(text: str, start: str, end: str) -> str:
    start_index = text.find(start)
    if start_index == -1:
        return ""

    end_index = text.find(end, start_index + len(start))
    if end_index == -1:
        return text[start_index:]

    return text[start_index:end_index]


def frontmatter(text: str) -> str:
    if not text.startswith("---\n"):
        return ""

    end_index = text.find("\n---", 4)
    if end_index == -1:
        return ""

    return text[: end_index + len("\n---")]


def check_golden_structure() -> list[str]:
    errors: list[str] = []
    errors += require_path(GOLDEN_ROOT)
    errors += require_path(README)
    errors += require_path(CONTRACT)

    for directory in ARTIFACT_DIRS:
        path = ROOT / directory
        if not path.is_dir():
            errors.append(f"{directory}: missing directory")
        errors += require_path(f"{directory}/.gitkeep")

    example_files = [
        path
        for directory in ARTIFACT_DIRS
        for path in (ROOT / directory).glob("*.md")
        if path.name != ".gitkeep"
    ]
    if example_files:
        files = ", ".join(str(path.relative_to(ROOT)) for path in example_files)
        errors.append(f"{GOLDEN_ROOT}: issue #211 must not create real golden artifacts: {files}")

    return errors


def check_contract_is_yaml_contract() -> list[str]:
    errors = require_path(CONTRACT)
    if errors:
        return errors

    text = read_text(CONTRACT)
    if "```" in text:
        errors.append(f"{CONTRACT}: must be YAML text with # comments, not Markdown fences")
    if "comment:" in text:
        errors.append(f"{CONTRACT}: use # comments, not comment: data fields")

    errors += require_text(CONTRACT, *REQUIRED_CONTRACT_TEXT)
    return errors


def check_bcreq_source_placeholder() -> list[str]:
    errors = require_path(BCREQ_CONTRACT)
    if errors:
        return errors

    text = read_text(BCREQ_CONTRACT)
    fm = frontmatter(text)
    if not fm:
        return [f"{BCREQ_CONTRACT}: missing YAML frontmatter"]

    source_attachments = section_between(fm, "source_attachments:", "integrates:")
    if not source_attachments:
        errors.append(f"{BCREQ_CONTRACT}: missing source_attachments frontmatter block")
    if '- status: "no-golden-standard"' not in source_attachments:
        errors.append(f"{BCREQ_CONTRACT}: source_attachments must use no-golden-standard placeholder")
    if "comment:" in source_attachments:
        errors.append(f"{BCREQ_CONTRACT}: source_attachments must not use comment: data fields")
    if "path:" in source_attachments or "sha:" in source_attachments:
        errors.append(f"{BCREQ_CONTRACT}: path+sha must wait for an approved real golden example")

    errors += require_text(BCREQ_CONTRACT, *REQUIRED_BCREQ_TEXT)
    errors += reject_text(BCREQ_CONTRACT, *FORBIDDEN_BCREQ_TEXT)
    return errors


def check_project_wiring() -> list[str]:
    errors: list[str] = []
    for path, needles in REQUIRED_PROJECT_TEXT.items():
        errors += require_text(path, *needles)
    return errors


def main() -> int:
    errors: list[str] = []
    errors += check_golden_structure()
    errors += require_text(README, *REQUIRED_README_TEXT)
    errors += check_contract_is_yaml_contract()
    errors += check_bcreq_source_placeholder()
    errors += check_project_wiring()

    if errors:
        print("Issue #211 Golden Examples contract validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Issue #211 Golden Examples contract validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
