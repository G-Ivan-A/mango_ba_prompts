#!/usr/bin/env python3
"""Regression check for issue #148: taxonomy extensions in ADR-011/ADR-012.

Issue #148 closes the open questions from the issue #146 audit:

- ADR-011 documents strict Industry Taxonomy references for mapping.
- ADR-012 documents Function attributes, term aliases, and mapping format.
- ``function_type`` is justified by external standards.
- The issue #146 audit is promoted to canonical.
- Changelog, Makefile and CI run this validator.
"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

ADR_011 = "standards/decisions/ADR-011-industry-taxonomy.md"
ADR_012 = "standards/decisions/ADR-012-mango-taxonomy.md"
AUDIT = "docs/audit/issue-146-mango-taxonomy-validation.md"
CHANGELOG = "CHANGELOG.md"
MAKEFILE = "Makefile"
KB_WORKFLOW = ".github/workflows/kb.yml"
VALIDATOR = "scripts/validate_issue_148_taxonomy_extensions.py"


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


def require_ordered_text(path: str, needles: tuple[str, ...]) -> list[str]:
    text = read_text(path)
    errors: list[str] = []
    last = -1
    for needle in needles:
        pos = text.find(needle)
        if pos == -1:
            errors.append(f"{path}: missing {needle!r}")
        elif pos < last:
            errors.append(f"{path}: {needle!r} is out of order")
        last = max(last, pos)
    return errors


def check_adr_011() -> list[str]:
    errors = require_text(
        ADR_011,
        "https://github.com/G-Ivan-A/mango_ba_prompts/issues/148",
        "## Использование в маппинге",
        "industry_ref",
        "`alignment_type`",
        "`primary`",
        "`secondary`",
        "`supporting`",
        "строгими ссылками",
        "не свободными тегами",
        "Product может ссылаться на несколько Domain/Capability",
        "Mango `Function`",
    )
    errors += require_ordered_text(
        ADR_011,
        (
            "## Решение",
            "## Использование в маппинге",
            "## Rationale",
        ),
    )
    return errors


def check_adr_012() -> list[str]:
    errors = require_text(
        ADR_012,
        "https://github.com/G-Ivan-A/mango_ba_prompts/issues/148",
        "### Атрибуты Function",
        "`function_type`",
        "`business`",
        "`configuration`",
        "`ui-action`",
        "TM Forum SID",
        "TM Forum ODA Functional Framework",
        "ITIL 4",
        "ISO/IEC 25010:2023",
        "https://www.tmforum.org/open-digital-architecture/information-framework-sid/",
        "https://www.tmforum.org/open-digital-architecture/functional-framework/",
        "https://www.axelos.com/certifications/itil-service-management/itil-practices-manager/itil-4-specialist-plan-implement-and-control/itil-4-practitioner-service-configuration-management",
        "https://www.iso.org/standard/78176.html",
        "### Алиасы терминов",
        "Component",
        "Module",
        "Operation",
        "Function",
        "### Формат маппинга",
        "taxonomy_mapping:",
        "industry_alignment:",
        "industry_ref:",
        "alignment_type: primary",
        "domain: contact-center",
        "capability: omnichannel-contact-center",
        "не свободные теги",
    )
    errors += require_ordered_text(
        ADR_012,
        (
            "### Атрибуты",
            "### Атрибуты Function",
            "### Алиасы терминов",
            "### Формат маппинга",
            "## Taxonomy Alignment с ADR-011",
        ),
    )
    return errors


def check_audit() -> list[str]:
    text = read_text(AUDIT)
    errors: list[str] = []
    for needle in (
        "status: canonical",
        "version: 1.0",
        "Canonicalization note",
        "https://github.com/G-Ivan-A/mango_ba_prompts/issues/148",
        "function_type",
        "Component=Module",
        "Operation=Function",
    ):
        if needle not in text:
            errors.append(f"{AUDIT}: missing {needle!r}")
    if "status: draft" in text:
        errors.append(f"{AUDIT}: must not remain draft")
    return errors


def check_changelog_and_ci() -> list[str]:
    errors: list[str] = []
    errors += require_text(
        CHANGELOG,
        "Issue #148",
        "function_type",
        "Component=Module",
        "Operation=Function",
        "ADR-011",
        "ADR-012",
        AUDIT,
        VALIDATOR,
    )
    errors += require_text(MAKEFILE, VALIDATOR)
    errors += require_text(
        KB_WORKFLOW,
        "Validate issue #148 taxonomy extensions",
        f"python3 {VALIDATOR}",
    )
    return errors


def main() -> int:
    errors: list[str] = []
    errors += check_adr_011()
    errors += check_adr_012()
    errors += check_audit()
    errors += check_changelog_and_ci()

    if errors:
        print("Issue #148 taxonomy extension validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Issue #148 taxonomy extension validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
