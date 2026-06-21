#!/usr/bin/env python3
"""Regression check for issue #154: canonical ADR-012 and Mango standard.

Issue #154 finalizes ADR-012 and adds a machine-readable Mango Taxonomy
standard aligned with ADR-011 canonical v1.0 and the Industry Taxonomy standard.
"""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

ADR_012 = "standards/decisions/ADR-012-mango-taxonomy.md"
STANDARD = "standards/mango-taxonomy-standard.md"
INDUSTRY_STANDARD = "standards/industry-taxonomy-standard.md"
INDUSTRY_REGISTRY = "kb/industry/reference-taxonomy.json"
MANGO_OFFICIAL = "kb/mango/official-products.yaml"
MANGO_INTERNAL = "kb/mango/internal-registry.yaml"
MANGO_MAPPING = "kb/mango/product-mapping.yaml"
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


def extract_json_schema() -> tuple[dict[str, object] | None, list[str]]:
    text = read_text(STANDARD)
    match = re.search(r"```json\n(.*?)\n```", text, re.S)
    if not match:
        return None, [f"{STANDARD}: missing JSON schema fenced block"]
    try:
        schema = json.loads(match.group(1))
    except json.JSONDecodeError as exc:
        return None, [f"{STANDARD}: JSON schema block is not valid JSON: {exc}"]
    if not isinstance(schema, dict):
        return None, [f"{STANDARD}: JSON schema root must be object"]
    return schema, []


def load_industry_paths() -> set[str]:
    data = json.loads((ROOT / INDUSTRY_REGISTRY).read_text(encoding="utf-8"))
    paths: set[str] = set()
    for collection in ("domains", "cross_domain_layers"):
        for domain in data.get(collection, []):
            domain_id = domain["id"]
            paths.add(domain_id)
            for capability in domain.get("capabilities", []):
                capability_id = capability["id"]
                paths.add(f"{domain_id}/{capability_id}")
                for feature in capability.get("features", []):
                    feature_id = feature["id"]
                    paths.add(f"{domain_id}/{capability_id}/{feature_id}")
                    for function in feature.get("functions", []):
                        paths.add(f"{domain_id}/{capability_id}/{feature_id}/{function['id']}")
    return paths


def collect_example_industry_refs() -> list[tuple[str, str]]:
    text = read_text(STANDARD)
    refs: list[tuple[str, str]] = []
    current: dict[str, str] = {}
    current_lines: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if re.match(r"^(domain|capability|feature|function): ", stripped):
            key, value = stripped.split(":", 1)
            current[key] = value.strip().split()[0].strip("'\"")
            current_lines.append(stripped)
            continue
        if stripped.startswith("alignment_type:") or stripped.startswith("facets:") or stripped.startswith("mapping_gap:") or not stripped:
            if "domain" in current:
                path = "/".join(current[key] for key in ("domain", "capability", "feature", "function") if key in current)
                refs.append((path, " | ".join(current_lines)))
                current = {}
                current_lines = []
    if "domain" in current:
        path = "/".join(current[key] for key in ("domain", "capability", "feature", "function") if key in current)
        refs.append((path, " | ".join(current_lines)))
    return refs


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


def check_issue_164_audit_fixes() -> list[str]:
    errors = require_text(
        STANDARD,
        "https://github.com/G-Ivan-A/mango_ba_prompts/issues/164",
        INDUSTRY_REGISTRY,
        MANGO_OFFICIAL,
        MANGO_INTERNAL,
        MANGO_MAPPING,
        "ADR-011 имеет приоритет над ADR-012",
        "Mango vs Industry responsibility boundary",
        "supported_by_services",
        "confidence",
        "secondary_clusters",
        "module_extraction_status",
        "unevaluatedProperties",
        "security_compliance",
        "geography_region",
        "not yet implemented",
        "mango-robots",
        "mango-speech-analytics",
        "mango-marketing-analytics",
        "mango-text-communications",
        "mango-open-platform",
        "mango-numbers-equipment",
        "mango-solution-pack",
    )
    if errors:
        return errors

    text = read_text(STANDARD)
    obsolete_snippets = (
        "capability: team-messaging",
        "capability: conversation-analytics",
        "domain: security\n        capability: access-control",
        "capability: real-time-reporting",
        "feature: dashboard-view",
        "function: select-dashboard-widget",
        "function: generate-summary",
        "function: start-campaign",
        "function: receive-inbound-call",
        "capability: access-control\n        feature: role-management",
        '"segment": { "type": "array"',
        '"region": { "type": "array"',
        '"additionalProperties": true,\n      "properties": {\n        "channel"',
        '"version": { "type": "integer"',
        '"enum": ["proposed", "active", "deprecated", "removed"]',
        "| `removed` | Entity no longer allowed. | Error unless legacy exemption is explicit. |",
        "| Missing evidence in draft registry | warning |",
    )
    for obsolete in obsolete_snippets:
        if obsolete in text:
            errors.append(f"{STANDARD}: obsolete audit finding remains: {obsolete!r}")

    priority = text[text.find("### 1.3 Приоритет источников") : text.find("## 2. Нормативные термины")]
    adr011_pos = priority.find("ADR-011")
    adr012_pos = priority.find("ADR-012")
    if adr011_pos == -1 or adr012_pos == -1 or adr011_pos > adr012_pos:
        errors.append(f"{STANDARD}: §1.3 must place ADR-011 before ADR-012")

    schema, schema_errors = extract_json_schema()
    errors += schema_errors
    if schema:
        defs = schema.get("$defs")
        if not isinstance(defs, dict):
            errors.append(f"{STANDARD}: JSON schema must define $defs")
        else:
            lifecycle = defs.get("lifecycleStatus", {})
            if isinstance(lifecycle, dict) and "removed" in lifecycle.get("enum", []):
                errors.append(f"{STANDARD}: schema lifecycleStatus must reject removed without legacy exemption")
            facets = defs.get("facets", {})
            if isinstance(facets, dict):
                if facets.get("additionalProperties") is not False:
                    errors.append(f"{STANDARD}: facets schema must close additionalProperties")
                properties = facets.get("properties", {})
                if isinstance(properties, dict):
                    for required_facet in ("channel", "ai_assisted", "security_compliance", "commercial", "procurement", "industry_vertical", "geography_region"):
                        if required_facet not in properties:
                            errors.append(f"{STANDARD}: facets schema missing {required_facet!r}")
                    for obsolete_facet in ("segment", "region"):
                        if obsolete_facet in properties:
                            errors.append(f"{STANDARD}: facets schema still defines obsolete {obsolete_facet!r}")
            industry_alignment = defs.get("industryAlignment", {})
            if isinstance(industry_alignment, dict):
                props = industry_alignment.get("properties", {})
                if isinstance(props, dict) and "confidence" not in props:
                    errors.append(f"{STANDARD}: industryAlignment schema must define confidence")
            module = defs.get("module", {})
            if isinstance(module, dict) and "anyOf" not in json.dumps(module, ensure_ascii=False):
                errors.append(f"{STANDARD}: module schema must require functions or function_extraction_status with anyOf")
            service = defs.get("service", {})
            if isinstance(service, dict) and "module_extraction_status" not in json.dumps(service, ensure_ascii=False):
                errors.append(f"{STANDARD}: service schema must include module_extraction_status fallback")
            taxonomy = defs.get("taxonomy", {})
            if isinstance(taxonomy, dict):
                version = taxonomy.get("properties", {}).get("version", {}) if isinstance(taxonomy.get("properties"), dict) else {}
                if isinstance(version, dict) and version.get("type") != "string":
                    errors.append(f"{STANDARD}: taxonomy.version must be semver string")
            for level in ("officialProduct", "product", "service", "module", "function"):
                level_schema = defs.get(level, {})
                if isinstance(level_schema, dict) and level_schema.get("unevaluatedProperties") is not False:
                    errors.append(f"{STANDARD}: {level} schema must set unevaluatedProperties false")

    known_paths = load_industry_paths()
    for path, source in collect_example_industry_refs():
        if path not in known_paths:
            errors.append(f"{STANDARD}: example industry_ref does not resolve in {INDUSTRY_REGISTRY}: {path} ({source})")

    return errors


def check_changelog_and_ci() -> list[str]:
    errors: list[str] = []
    errors += require_text(
        CHANGELOG,
        "Issue #154",
        "Issue #164",
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
    errors += check_issue_164_audit_fixes()

    if errors:
        print("Issue #154 Mango Taxonomy standard validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Issue #154 Mango Taxonomy standard validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
