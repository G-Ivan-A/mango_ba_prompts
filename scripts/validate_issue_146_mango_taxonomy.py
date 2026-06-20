#!/usr/bin/env python3
"""Regression check for issue #146: Mango Taxonomy validation and terminology.

Issue #146 validates Mango Taxonomy against processed Mango documentation and
unifies the taxonomy leaf term:

- Industry Taxonomy uses ``Domain -> Capability -> Feature -> Function``.
- Mango Taxonomy uses ``Product -> Service -> Module -> Function``.
- The decision is backed by real processed KB guides, not by assumption.
- Changelog, Makefile and CI run this validator.
"""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = "scripts/validate_issue_146_mango_taxonomy.py"
AUDIT = "docs/audit/issue-146-mango-taxonomy-validation.md"
CHANGELOG = "CHANGELOG.md"
MAKEFILE = "Makefile"
KB_WORKFLOW = ".github/workflows/kb.yml"

CURRENT_TAXONOMY_DOCS = (
    "standards/decisions/ADR-011-industry-taxonomy.md",
    "standards/decisions/ADR-012-mango-taxonomy.md",
    "standards/product-classification-contract.md",
    "standards/ba-ontology.md",
    "standards/ba-ontology.executable.md",
    "docs/adr/003-ba-ontology.md",
    "README.md",
)

SELECTED_GUIDES = (
    "mango-cc-manual",
    "mango-lk-manual",
    "mtalker/quick-start",
    "mtalker/windows-mac-working",
    "mtalker/windows-mac-admin",
    "integration-bitrix24",
    "sip-trunk",
    "vpbx-api",
    "mdialogi-api",
    "speech-analytics/rukovodstvo-polzovatelya-rechevaya-analitika",
    "quality-managment",
    "wallboard",
)

TERM_PATTERNS = {
    "service": r"\bсервис\w*|\bservice\w*",
    "module": r"\bмодул\w*|\bmodule\w*",
    "function": r"\bфункц\w*|\bfunction\w*",
    "operation": r"\bоперац\w*|\boperation\w*",
    "setting": r"\bнастрой\w*",
    "action": r"\bдейств\w*",
}


def read_text(path: str | Path) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def require_path(path: str) -> list[str]:
    return [] if (ROOT / path).exists() else [f"{path}: missing"]


def require_text(path: str, *needles: str) -> list[str]:
    errors = require_path(path)
    if errors:
        return errors
    text = read_text(path)
    return [f"{path}: missing {needle!r}" for needle in needles if needle not in text]


def forbid_text(path: str, *needles: str) -> list[str]:
    text = read_text(path)
    return [f"{path}: forbidden old terminology {needle!r}" for needle in needles if needle in text]


def read_guide(slug: str) -> str:
    base = ROOT / "kb" / "mango-product-docs" / "processed" / slug
    parts: list[str] = []
    for path in [base / "index.md", *sorted((base / "sections").glob("*.md"))]:
        if path.exists():
            parts.append(path.read_text(encoding="utf-8", errors="replace"))
    return "\n".join(parts)


def check_processed_kb_evidence() -> list[str]:
    errors: list[str] = []
    counts: Counter[str] = Counter()

    if len(SELECTED_GUIDES) < 10:
        errors.append("issue #146 must validate at least 10 processed guides")

    for slug in SELECTED_GUIDES:
        base = ROOT / "kb" / "mango-product-docs" / "processed" / slug
        errors += require_path(str(base / "index.md"))
        errors += require_path(str(base / "meta.json"))
        text = read_guide(slug)
        if not text.strip():
            errors.append(f"{base}: no readable processed KB text")
            continue
        lowered = text.lower()
        for key, pattern in TERM_PATTERNS.items():
            counts[key] += len(re.findall(pattern, lowered, flags=re.IGNORECASE))

    required_minimums = {
        "service": 150,
        "module": 150,
        "function": 250,
        "operation": 50,
        "setting": 1000,
        "action": 300,
    }
    for term, minimum in required_minimums.items():
        if counts[term] < minimum:
            errors.append(
                "kb/mango-product-docs/processed: "
                f"expected at least {minimum} {term} evidence terms, got {counts[term]}"
            )

    return errors


def check_audit() -> list[str]:
    errors = require_text(
        AUDIT,
        "Issue #146",
        "12 processed guides",
        "Product -> Service -> Module -> Function",
        "Domain -> Capability -> Feature -> Function",
        "service=235",
        "module=245",
        "function=371",
        "settings/actions",
        "sip-trunk",
        "mango-cc-manual",
        "mango-lk-manual",
        "integration-bitrix24",
        "mtalker/windows-mac-working",
        "vpbx-api",
        "mdialogi-api",
        "quality-managment",
        "wallboard",
    )
    return errors


def check_taxonomy_docs() -> list[str]:
    errors: list[str] = []
    errors += require_text(
        "standards/decisions/ADR-011-industry-taxonomy.md",
        "Domain -> Capability -> Feature -> Function",
        "function: send SMS, transfer call, assign agent, generate summary",
        "Hierarchy:** `Domain -> Capability -> Feature -> Function`",
    )
    errors += require_text(
        "standards/decisions/ADR-012-mango-taxonomy.md",
        "Product -> Service -> Module -> Function",
        "Mango Taxonomy использует четыре основных уровня",
        "Mango `Function` выравнивается на ADR-011 `Function`",
        AUDIT,
    )
    errors += require_text(
        "standards/product-classification-contract.md",
        "Domain -> Capability -> Feature -> Function",
        "| Function | Минимальная проверяемая единица функциональности.",
        "## 🔹 Function (Функция)",
    )
    errors += require_text(
        "standards/ba-ontology.md",
        "Domain→Capability→Feature→Function",
    )
    errors += require_text(
        "standards/ba-ontology.executable.md",
        "Domain -> Capability -> Feature -> Function",
    )
    errors += require_text(
        "docs/adr/003-ba-ontology.md",
        "Domain → Capability → Feature → Function",
    )
    errors += require_text(
        "README.md",
        "Domain → Capability → Feature → Function",
    )

    forbidden_fragments = (
        "Domain -> Capability -> Feature -> Atomic Function",
        "Domain → Capability → Feature → Atomic Function",
        "Domain→Capability→Feature→Atomic Function",
        "Product -> Service -> Module` используется",
        "Feature и Atomic Function не вводятся как отдельные Mango-уровни",
    )
    for path in CURRENT_TAXONOMY_DOCS:
        errors += forbid_text(path, *forbidden_fragments)

    return errors


def check_changelog_and_ci() -> list[str]:
    errors: list[str] = []
    errors += require_text(
        CHANGELOG,
        "Issue #146",
        "Atomic Function → Function",
        "Product -> Service -> Module -> Function",
        "ADR-011",
        "ADR-012",
        AUDIT,
        VALIDATOR,
    )
    errors += require_text(MAKEFILE, VALIDATOR)
    errors += require_text(
        KB_WORKFLOW,
        "Validate issue #146 Mango taxonomy validation",
        f"python3 {VALIDATOR}",
    )
    return errors


def check_issue_127_validator_sync() -> list[str]:
    return require_text(
        "scripts/validate_issue_127_hub_rfc_sync.py",
        "Domain→Capability→Feature→Function",
    )


def main() -> int:
    errors: list[str] = []
    errors += check_processed_kb_evidence()
    errors += check_audit()
    errors += check_taxonomy_docs()
    errors += check_changelog_and_ci()
    errors += check_issue_127_validator_sync()

    if errors:
        print("Issue #146 Mango taxonomy validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Issue #146 Mango taxonomy validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
