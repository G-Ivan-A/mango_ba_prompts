#!/usr/bin/env python3
"""Regression check for issue #152: Industry Taxonomy standard.

The issue requires a formal, strict and validator-ready standard at
``standards/industry-taxonomy-standard.md`` aligned with ADR-011 canonical v1.0,
ADR-012 and the voice/digital channel analysis.
"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

STANDARD = "standards/industry-taxonomy-standard.md"
REGISTRY = "kb/industry-taxonomy/registry.json"
REGISTRY_SCHEMA = "kb/industry-taxonomy/registry.schema.json"
CHANGELOG = "CHANGELOG.md"
MAKEFILE = "Makefile"
KB_WORKFLOW = ".github/workflows/kb.yml"
VALIDATOR = "scripts/validate_issue_152_industry_taxonomy_standard.py"


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
    errors = require_path(path)
    if errors:
        return errors
    text = read_text(path)
    last = -1
    for needle in needles:
        pos = text.find(needle)
        if pos == -1:
            errors.append(f"{path}: missing {needle!r}")
        elif pos < last:
            errors.append(f"{path}: {needle!r} is out of order")
        last = max(last, pos)
    return errors


def check_standard() -> list[str]:
    errors = require_text(
        STANDARD,
        "status: draft",
        "type: standard",
        "scope: industry-taxonomy",
        "https://github.com/G-Ivan-A/mango_ba_prompts/issues/152",
        "# Стандарт Industry Taxonomy",
        "## 1. Область применения",
        "## 2. Нормативные термины",
        "## 3. Каноническая модель",
        "Domain -> Capability -> Feature -> Function",
        "`voice-ucaas`",
        "`contact-center`",
        "`digital-channels`",
        "`ai-automation`",
        "`analytics`",
        "`hardware`",
        "`security`",
        "`platform`",
        "## 4. Идентификаторы и структура узлов",
        "## 5. Правила классификации",
        "## 6. Cross-cutting facets",
        "`channel_kind`",
        "`synchronicity`",
        "`direction`",
        "`voice-channel`",
        "## 7. Атрибуты и метаданные",
        "`function_type`",
        "`business`",
        "`configuration`",
        "`ui-action`",
        "## 8. Правила маппинга",
        "`industry_ref`",
        "`alignment_type`",
        "`primary`",
        "`secondary`",
        "`supporting`",
        "## 9. Граничные кейсы и анти-паттерны",
        "## 10. Процесс эволюции",
        "## 11. Контракт для валидатора",
        "## 12. Контракт для AI-агентов",
        "## 13. Самопроверка качества",
        "## Источники",
        "standards/decisions/ADR-011-industry-taxonomy.md",
        "standards/decisions/ADR-012-mango-taxonomy.md",
        "docs/analysis/voice-digital-channels-comparison.md",
    )
    if errors:
        return errors

    text = read_text(STANDARD)
    if "dialog-taxonomy-approval.txt" not in text:
        errors.append(f"{STANDARD}: missing dialog-taxonomy-approval.txt source note")
    if "НЕ ДОЛЖЕН" not in text or "ДОЛЖЕН" not in text:
        errors.append(f"{STANDARD}: must use normative RFC 2119 style keywords")
    if "Свободный tag" not in text:
        errors.append(f"{STANDARD}: must forbid free taxonomy tags")
    if "channel_kind: voice" not in text or "channel_kind: text" not in text:
        errors.append(f"{STANDARD}: must include voice/text channel mapping examples")
    return errors


def check_issue_162_audit_fixes() -> list[str]:
    errors = require_text(
        STANDARD,
        REGISTRY,
        REGISTRY_SCHEMA,
        "Industry vs Mango responsibility boundary",
        "cross_domain_layers",
        "`platform` is not an eighth Domain",
        "security_compliance:",
        "geography_region:",
        "`security_compliance`",
        "`geography_region`",
        "`interaction_surface`",
        "`admin-ui`",
        "`operator-ui`",
        "`end-user-ui`",
        "`api`",
        "`webhook`",
        "`background-job`",
        "`system-rule`",
        "`unknown`",
        "direction x synchronicity",
        "`broadcast`",
        "JSON Schema contract",
        "\"industryRef\"",
        "\"additionalProperties\": false",
        "mapping_gap",
        "not yet implemented",
        "scripts/validate_issue_156_industry_taxonomy_registry.py",
    )
    if errors:
        return errors

    text = read_text(STANDARD)
    obsolete_facet_examples = (
        "  compliance:\n    region:",
        "`compliance` in §6.1",
        "`geography_region`/`region`",
    )
    for obsolete in obsolete_facet_examples:
        if obsolete in text:
            errors.append(f"{STANDARD}: obsolete facet drift remains: {obsolete!r}")
    if "| канал, регион, vertical, сегмент" in text:
        errors.append(f"{STANDARD}: segment must not be classified as an Industry facet")
    return errors


def check_changelog_and_ci() -> list[str]:
    errors: list[str] = []
    errors += require_text(
        CHANGELOG,
        "Issue #152",
        "Issue #162",
        STANDARD,
        REGISTRY,
        "Industry Taxonomy",
        VALIDATOR,
    )
    errors += require_text(MAKEFILE, VALIDATOR)
    errors += require_text(
        KB_WORKFLOW,
        "Validate issue #152 Industry Taxonomy standard",
        f"python3 {VALIDATOR}",
    )
    return errors


def main() -> int:
    errors: list[str] = []
    errors += check_standard()
    errors += require_ordered_text(
        STANDARD,
        (
            "## 1. Область применения",
            "## 2. Нормативные термины",
            "## 3. Каноническая модель",
            "## 4. Идентификаторы и структура узлов",
            "## 5. Правила классификации",
            "## 6. Cross-cutting facets",
            "## 7. Атрибуты и метаданные",
            "## 8. Правила маппинга",
            "## 9. Граничные кейсы и анти-паттерны",
            "## 10. Процесс эволюции",
            "## 11. Контракт для валидатора",
            "## 12. Контракт для AI-агентов",
            "## 13. Самопроверка качества",
        ),
    )
    errors += check_changelog_and_ci()
    errors += check_issue_162_audit_fixes()

    if errors:
        print("Issue #152 Industry Taxonomy standard validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Issue #152 Industry Taxonomy standard validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
