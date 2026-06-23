#!/usr/bin/env python3
"""Regression check for issue #208: BCREQ-FR contract has no L3 runtime inputs."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

CONTRACT = "governance/bcreq-fr-generation-contract.md"
VALIDATOR = "scripts/validate_issue_208_bcreq_fr_l3_boundary.py"
DRY_RUN = "experiments/issue-208/bcreq-1027-l3-boundary-dry-run.md"

FORBIDDEN_RUNTIME_TEXT = (
    "governance/rfc/",
    "standards/industry-taxonomy-standard.md",
    "standards/mango-taxonomy-standard.md",
)

REQUIRED_CONTRACT_TEXT = (
    "status: active",
    "version: 0.4",
    "updated: 2026-06-23",
    "Правила RFC-184 встроены в §3 (BCREQ-FR-GEN-SCOPE-01/02)",
    'status: "no-golden-standard"',
    "kb/golden-examples/CONTRACT.md",
    "kb/industry-taxonomy/registry.json",
    "kb/mango-taxonomy/registry.json",
    "BCREQ-FR-GEN-SCOPE-01",
    "BCREQ-FR-GEN-SCOPE-02",
    "BCREQ-FR-GEN-SCOPE-01/02",
    "scripts/validate_issue_208_bcreq_fr_l3_boundary.py",
)

REQUIRED_DRY_RUN_TEXT = (
    "# Issue #208 — BCREQ-1027 L3 boundary dry run",
    "Architect",
    "BA expert",
    "AI engineer",
    "runs/bcreq-1027/metadata.yaml",
    "runs/bcreq-1027/artifacts/section-4-3-api.md",
    "kb/industry-taxonomy/registry.json",
    "kb/mango-taxonomy/registry.json",
    "governance/rfc/",
    "standards/",
    "не загружались",
)

REQUIRED_PROJECT_TEXT = {
    "CHANGELOG.md": (
        "Issue #208",
        CONTRACT,
        VALIDATOR,
        DRY_RUN,
    ),
    ".github/workflows/github-pages.yml": (
        "Validate issue #208 BCREQ-FR L3 boundary",
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


def check_frontmatter() -> list[str]:
    errors = require_path(CONTRACT)
    if errors:
        return errors

    text = read_text(CONTRACT)
    fm = frontmatter(text)
    if not fm:
        return [f"{CONTRACT}: missing YAML frontmatter"]

    for forbidden in FORBIDDEN_RUNTIME_TEXT:
        if forbidden in fm:
            errors.append(f"{CONTRACT}: frontmatter must not include L3 input {forbidden!r}")

    source_attachments = section_between(fm, "source_attachments:", "integrates:")
    if "github.com/user-attachments" in source_attachments:
        errors.append(f"{CONTRACT}: source_attachments must not use raw GitHub attachment URLs")
    if '- status: "no-golden-standard"' not in source_attachments:
        errors.append(f"{CONTRACT}: source_attachments must use no-golden-standard placeholder")
    if "comment:" in source_attachments:
        errors.append(f"{CONTRACT}: source_attachments must use YAML comments, not comment: data fields")
    if "path:" in source_attachments or "sha:" in source_attachments:
        errors.append(f"{CONTRACT}: path+sha requires approved Golden Example")

    integrates = section_between(fm, "integrates:", "validated_by:")
    for forbidden in FORBIDDEN_RUNTIME_TEXT:
        if forbidden in integrates:
            errors.append(f"{CONTRACT}: integrates must not include L3 dependency {forbidden!r}")
    for required in ("kb/industry-taxonomy/registry.json", "kb/mango-taxonomy/registry.json"):
        if required not in integrates:
            errors.append(f"{CONTRACT}: integrates must include L2 dependency {required!r}")

    return errors


def check_runtime_inputs() -> list[str]:
    errors = require_path(CONTRACT)
    if errors:
        return errors

    text = read_text(CONTRACT)
    inputs = section_between(text, "## 2. Входные данные", "## 3. Machine-readable index")
    if not inputs:
        return [f"{CONTRACT}: missing runtime input section"]

    if "`rfc_184`" in inputs:
        errors.append(f"{CONTRACT}: §2 must not require rfc_184 as an input")

    for forbidden in FORBIDDEN_RUNTIME_TEXT:
        if forbidden in inputs:
            errors.append(f"{CONTRACT}: §2 must not include L3 runtime input {forbidden!r}")

    taxonomy_row = "| `taxonomy_sources` | Да | `kb/industry-taxonomy/registry.json`, `kb/mango-taxonomy/registry.json`. |"
    if taxonomy_row not in inputs:
        errors.append(f"{CONTRACT}: §2 taxonomy_sources row must list only L2 registries")

    if "BCREQ-FR-GEN-SCOPE-01/02" not in inputs:
        errors.append(f"{CONTRACT}: §2 must point agents to embedded local scope rules")

    return errors


def check_embedded_scope_rules() -> list[str]:
    errors = require_path(CONTRACT)
    if errors:
        return errors

    text = read_text(CONTRACT)
    machine_index = section_between(text, "## 3. Machine-readable index", "## 4. Процесс генерации")
    if not machine_index:
        return [f"{CONTRACT}: missing machine-readable index"]

    for required in (
        "id: BCREQ-FR-GEN-SCOPE-01",
        "source_rule: RFC-184-S1",
        'statement: "BCREQ-FR describes the requested change, not current functionality."',
        "id: BCREQ-FR-GEN-SCOPE-02",
        "source_rule: RFC-184-S2",
        'statement: "A single-user request does not justify changing functionality already closed explicitly or alternatively."',
    ):
        if required not in machine_index:
            errors.append(f"{CONTRACT}: embedded scope rule missing {required!r}")

    for forbidden in FORBIDDEN_RUNTIME_TEXT:
        if forbidden in machine_index:
            errors.append(f"{CONTRACT}: machine-readable index must not include L3 path {forbidden!r}")

    return errors


def check_project_wiring() -> list[str]:
    errors: list[str] = []
    for path, needles in REQUIRED_PROJECT_TEXT.items():
        errors += require_text(path, *needles)
    return errors


def main() -> int:
    errors: list[str] = []
    errors += require_text(CONTRACT, *REQUIRED_CONTRACT_TEXT)
    errors += reject_text(
        CONTRACT,
        "github.com/user-attachments",
        'comment: "Вложения из PR #202"',
        'status: "temporary"',
        'trace: "https://github.com/G-Ivan-A/mango_ba_prompts/pull/202"',
    )
    errors += check_frontmatter()
    errors += check_runtime_inputs()
    errors += check_embedded_scope_rules()
    errors += require_text(DRY_RUN, *REQUIRED_DRY_RUN_TEXT)
    errors += check_project_wiring()

    if errors:
        print("Issue #208 BCREQ-FR L3 boundary validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Issue #208 BCREQ-FR L3 boundary validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
