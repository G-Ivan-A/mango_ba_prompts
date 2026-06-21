#!/usr/bin/env python3
"""Regression check for issue #154: canonical ADR-012 and Mango standard.

Issue #154 finalizes ADR-012 and adds a machine-readable Mango Taxonomy
standard aligned with ADR-011 canonical v1.0 and the Industry Taxonomy standard.
"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

ADR_012 = "standards/decisions/ADR-012-mango-taxonomy.md"
STANDARD = "standards/mango-taxonomy-standard.md"
INDUSTRY_STANDARD = "standards/industry-taxonomy-standard.md"
VOICE_ANALYSIS = "docs/analysis/voice-digital-channels-comparison.md"
CHANGELOG = "CHANGELOG.md"
MAKEFILE = "Makefile"
KB_WORKFLOW = ".github/workflows/kb.yml"
VALIDATOR = "scripts/validate_issue_154_mango_taxonomy_standard.py"


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


def forbid_text(path: str, *needles: str) -> list[str]:
    errors = require_path(path)
    if errors:
        return errors
    text = read_text(path)
    return [f"{path}: forbidden {needle!r}" for needle in needles if needle in text]


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


def check_adr_012() -> list[str]:
    errors = require_text(
        ADR_012,
        "status: canonical",
        "version: 1.0",
        "https://github.com/G-Ivan-A/mango_ba_prompts/issues/154",
        "## Canonicalization note",
        "standards/mango-taxonomy-standard.md",
        "Official Layer",
        "Internal Layer",
        "Product -> Service -> Module -> Function",
        "`voice-channel`",
        "`channel`",
        "`function_type`",
        "`business`",
        "`configuration`",
        "`ui-action`",
        "primary",
        "secondary",
        "supporting",
    )
    errors += forbid_text(
        ADR_012,
        "Статус:** Proposed",
        "status: proposed",
        "оставить статус `Proposed`",
        "`standards/mango-taxonomy-standard.md`: формальный стандарт Mango Taxonomy;",
    )
    return errors


def check_standard() -> list[str]:
    errors = require_text(
        STANDARD,
        "status: draft",
        "type: standard",
        "scope: mango-taxonomy",
        "https://github.com/G-Ivan-A/mango_ba_prompts/issues/154",
        "# Стандарт Mango Taxonomy",
        "## 1. Область применения",
        "## 2. Нормативные термины",
        "## 3. Архитектура таксономии",
        "Official Layer",
        "Internal Layer",
        "many-to-many",
        "Product -> Service -> Module -> Function",
        "## 4. Internal Layer",
        "`vats-core`",
        "`contact-center-core`",
        "`digital-channels`",
        "`mango-talker`",
        "`ai-speech-quality`",
        "`analytics-marketing`",
        "`platform-integrations`",
        "`security-access`",
        "## 5. Атрибуты и типы",
        "`function_type`",
        "`business`",
        "`configuration`",
        "`ui-action`",
        "`interaction_surface`",
        "## 6. Нормализация терминов",
        "Component -> Module",
        "Operation -> Function",
        "## 7. Mapping на Industry Taxonomy",
        "`maps_to`",
        "`industry_ref`",
        "`alignment_type`",
        "`primary`",
        "`secondary`",
        "`supporting`",
        "## 8. Машиночитаемые схемы",
        "MangoTaxonomyDocument",
        "\"$schema\"",
        "^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$",
        "## 9. YAML contract",
        "taxonomy:",
        "official_products:",
        "internal_services:",
        "modules:",
        "functions:",
        "## 10. Граничные кейсы и анти-паттерны",
        "## 11. Контракт валидатора",
        "## 12. Контракт AI-агента",
        "## 13. Процесс эволюции",
        "## 14. Самопроверка качества",
        "## Источники",
        INDUSTRY_STANDARD,
        ADR_012,
        "standards/decisions/ADR-011-industry-taxonomy.md",
        VOICE_ANALYSIS,
    )
    if errors:
        return errors

    text = read_text(STANDARD)
    minimum_examples = text.count("alignment_type:")
    if minimum_examples < 10:
        errors.append(f"{STANDARD}: expected at least 10 mapping examples, got {minimum_examples}")
    for marker in ("channel_kind: voice", "channel_kind: text", "voice-channel"):
        if marker not in text:
            errors.append(f"{STANDARD}: missing inherited ADR-011 channel marker {marker!r}")
    for forbidden in ("research/", "commercial_package as Product", "pricing as Product"):
        if forbidden in text:
            errors.append(f"{STANDARD}: forbidden or suspicious text {forbidden!r}")
    return errors


def check_changelog_and_ci() -> list[str]:
    errors: list[str] = []
    errors += require_text(
        CHANGELOG,
        "Issue #154",
        STANDARD,
        "ADR-012",
        "canonical",
        VALIDATOR,
    )
    errors += require_text(MAKEFILE, VALIDATOR)
    errors += require_text(
        KB_WORKFLOW,
        "Validate issue #154 Mango Taxonomy standard",
        f"python3 {VALIDATOR}",
    )
    return errors


def main() -> int:
    errors: list[str] = []
    errors += check_adr_012()
    errors += check_standard()
    errors += require_ordered_text(
        STANDARD,
        (
            "## 1. Область применения",
            "## 2. Нормативные термины",
            "## 3. Архитектура таксономии",
            "## 4. Internal Layer",
            "## 5. Атрибуты и типы",
            "## 6. Нормализация терминов",
            "## 7. Mapping на Industry Taxonomy",
            "## 8. Машиночитаемые схемы",
            "## 9. YAML contract",
            "## 10. Граничные кейсы и анти-паттерны",
            "## 11. Контракт валидатора",
            "## 12. Контракт AI-агента",
            "## 13. Процесс эволюции",
            "## 14. Самопроверка качества",
        ),
    )
    errors += check_changelog_and_ci()

    if errors:
        print("Issue #154 Mango Taxonomy standard validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Issue #154 Mango Taxonomy standard validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
