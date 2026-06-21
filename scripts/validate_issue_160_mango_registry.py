#!/usr/bin/env python3
"""Regression check for issue #160: machine-readable Mango registry.

The registry is stored as YAML files serialized in a JSON-compatible subset so
the CI check can stay stdlib-only. JSON is valid YAML, while ``json.loads`` gives
us deterministic validation without adding PyYAML to the lightweight KB job.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

OFFICIAL = "kb/mango/official-products.yaml"
INTERNAL = "kb/mango/internal-registry.yaml"
MAPPING = "kb/mango/product-mapping.yaml"
README = "kb/mango/README.md"
CHANGELOG = "CHANGELOG.md"
MAKEFILE = "Makefile"
KB_WORKFLOW = ".github/workflows/kb.yml"
VALIDATOR = "scripts/validate_issue_160_mango_registry.py"

SLUG_RE = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")
URL_RE = re.compile(r"^https?://")

CLUSTERS = {
    "vats-core",
    "contact-center-core",
    "digital-channels",
    "mango-talker",
    "ai-speech-quality",
    "analytics-marketing",
    "platform-integrations",
    "security-access",
}
LEVELS = {"official-product", "product", "service", "module", "function"}
LIFECYCLE = {"proposed", "active", "deprecated", "removed"}
FUNCTION_TYPES = {"business", "configuration", "ui-action"}
INTERACTION_SURFACES = {
    "admin-ui",
    "operator-ui",
    "end-user-ui",
    "api",
    "webhook",
    "background-job",
    "system-rule",
    "unknown",
}
ALIGNMENT_TYPES = {"primary", "secondary", "supporting"}
CHANNEL_KIND = {"voice", "text", "video"}
SYNCHRONICITY = {"sync", "async"}
DIRECTION = {"inbound", "outbound", "broadcast"}

INDUSTRY: dict[str, dict[str, dict[str, set[str]]]] = {
    "voice-ucaas": {
        "cloud-pbx": {},
        "voice-channel": {
            "inbound-voice-call": {"receive-inbound-call"},
            "outbound-voice-call": set(),
            "callback": {"request-callback"},
        },
        "call-routing": {},
        "ivr-voice-menu": {},
        "call-recording": {},
        "number-management": {},
        "sip-connectivity": {},
        "unified-communications": {},
    },
    "contact-center": {
        "omnichannel-contact-center": {},
        "interaction-routing": {
            "queue-routing": set(),
            "routing-rules": set(),
            "channel-based-routing": set(),
        },
        "agent-workspace": {},
        "supervisor-workspace": {},
        "outbound-calling": {"campaign-management": {"start-campaign"}},
        "workforce-management": {},
        "quality-management": {},
        "conversation-orchestration": {},
        "journey-orchestration": {},
    },
    "digital-channels": {
        "omnichannel-messaging": {"messenger-integration": {"send-message"}},
        "website-chat": {},
        "sms-messaging": {},
        "team-messaging": {},
    },
    "ai-automation": {
        "speech-analytics": {},
        "conversation-summaries": {"ai-summary": {"generate-summary"}},
        "voice-bot": {},
        "chatbot": {},
        "process-robot": {},
        "agent-assist": {},
    },
    "analytics": {
        "conversation-analytics": {},
        "real-time-reporting": {"dashboard-view": {"select-dashboard-widget"}},
        "call-tracking": {},
        "end-to-end-analytics": {},
        "multichannel-analytics": {},
        "email-tracking": {},
        "competitor-analysis": {},
        "product-analytics": {},
    },
    "hardware": {
        "device-management": {},
    },
    "security": {
        "access-control": {"role-management": {"assign-role"}},
        "information-security": {},
    },
    "platform": {
        "open-api": {"webhook-management": {"configure-webhook-endpoint"}},
        "cpaas": {},
        "platform-integration": {},
        "communications-apis": {},
        "service-desk": {},
        "vendor-support-services": {},
    },
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


def load_json_yaml(path: str) -> tuple[dict[str, Any] | None, list[str]]:
    errors = require_path(path)
    if errors:
        return None, errors
    try:
        data = json.loads(read_text(path))
    except json.JSONDecodeError as exc:
        return None, [f"{path}: must be JSON-compatible YAML: {exc}"]
    if not isinstance(data, dict):
        return None, [f"{path}: root must be object"]
    return data, []


def is_slug(value: Any) -> bool:
    return isinstance(value, str) and bool(SLUG_RE.fullmatch(value))


def check_slug(path: str, field: str, value: Any) -> list[str]:
    return [] if is_slug(value) else [f"{path}: invalid slug in {field}: {value!r}"]


def check_nonempty_list(path: str, field: str, value: Any) -> list[str]:
    if not isinstance(value, list) or not value:
        return [f"{path}: {field} must be a non-empty array"]
    return []


def check_string(path: str, field: str, value: Any) -> list[str]:
    if not isinstance(value, str) or not value.strip():
        return [f"{path}: {field} must be a non-empty string"]
    return []


def ref_exists(ref: str) -> bool:
    return bool(URL_RE.match(ref)) or (ROOT / ref).exists()


def check_evidence(path: str, entity: dict[str, Any]) -> list[str]:
    errors = check_nonempty_list(path, "evidence_refs", entity.get("evidence_refs"))
    for ref in entity.get("evidence_refs", []):
        if not isinstance(ref, str) or not ref_exists(ref):
            errors.append(f"{path}: evidence ref does not resolve: {ref!r}")
    return errors


def check_industry_ref(path: str, ref: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(ref, dict):
        return [f"{path}: industry_ref must be object"]
    if set(ref) - {"domain", "capability", "feature", "function"}:
        errors.append(f"{path}: industry_ref has unexpected keys {sorted(set(ref) - {'domain', 'capability', 'feature', 'function'})}")
    for field in ("domain", "capability", "feature", "function"):
        if field in ref:
            errors += check_slug(path, f"industry_ref.{field}", ref[field])
    domain = ref.get("domain")
    capability = ref.get("capability")
    feature = ref.get("feature")
    function = ref.get("function")
    if domain not in INDUSTRY:
        errors.append(f"{path}: unknown industry domain {domain!r}")
        return errors
    if feature and not capability:
        errors.append(f"{path}: industry_ref.feature requires capability")
    if function and not feature:
        errors.append(f"{path}: industry_ref.function requires feature")
    if capability:
        capabilities = INDUSTRY[domain]
        if capability not in capabilities:
            errors.append(f"{path}: unknown capability {domain}/{capability}")
            return errors
        if feature:
            features = capabilities[capability]
            if feature not in features:
                errors.append(f"{path}: unknown feature {domain}/{capability}/{feature}")
                return errors
            if function and function not in features[feature]:
                errors.append(f"{path}: unknown function {domain}/{capability}/{feature}/{function}")
    return errors


def check_facets(path: str, alignment: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    facets = alignment.get("facets")
    if facets is None:
        return errors
    if not isinstance(facets, dict):
        return [f"{path}: facets must be object"]
    channel = facets.get("channel")
    if channel:
        if not isinstance(channel, dict):
            errors.append(f"{path}: channel facet must be object")
        else:
            if channel.get("channel_kind") not in CHANNEL_KIND:
                errors.append(f"{path}: invalid channel_kind {channel.get('channel_kind')!r}")
            if channel.get("synchronicity") not in SYNCHRONICITY:
                errors.append(f"{path}: invalid synchronicity {channel.get('synchronicity')!r}")
            if channel.get("direction") not in DIRECTION:
                errors.append(f"{path}: invalid direction {channel.get('direction')!r}")
    if "ai_assisted" in facets and not isinstance(facets["ai_assisted"], bool):
        errors.append(f"{path}: ai_assisted must be boolean")
    return errors


def check_mapping_gap(path: str, alignment: dict[str, Any]) -> list[str]:
    gap = alignment.get("mapping_gap")
    if gap is None:
        return []
    if not isinstance(gap, dict):
        return [f"{path}: mapping_gap must be object"]
    errors: list[str] = []
    if gap.get("missing_level") not in {"domain", "capability", "feature", "function"}:
        errors.append(f"{path}: invalid mapping_gap.missing_level {gap.get('missing_level')!r}")
    errors += check_slug(path, "mapping_gap.proposed_id", gap.get("proposed_id"))
    errors += check_string(path, "mapping_gap.reason", gap.get("reason"))
    return errors


def check_alignments(path: str, maps_to: Any) -> tuple[list[dict[str, Any]], list[str]]:
    errors: list[str] = []
    if not isinstance(maps_to, dict):
        return [], [f"{path}: maps_to must be object"]
    alignments = maps_to.get("industry_alignment")
    if not isinstance(alignments, list) or not alignments:
        return [], [f"{path}: maps_to.industry_alignment must be non-empty array"]
    primary_count = 0
    for index, alignment in enumerate(alignments):
        item_path = f"{path}.maps_to.industry_alignment[{index}]"
        if not isinstance(alignment, dict):
            errors.append(f"{item_path}: alignment must be object")
            continue
        if alignment.get("alignment_type") not in ALIGNMENT_TYPES:
            errors.append(f"{item_path}: invalid alignment_type {alignment.get('alignment_type')!r}")
        if alignment.get("alignment_type") == "primary":
            primary_count += 1
        errors += check_industry_ref(item_path, alignment.get("industry_ref"))
        evidence = alignment.get("evidence_refs", [])
        if not isinstance(evidence, list) or not evidence:
            errors.append(f"{item_path}: evidence_refs must be non-empty array")
        else:
            for ref in evidence:
                if not isinstance(ref, str) or not ref_exists(ref):
                    errors.append(f"{item_path}: evidence ref does not resolve: {ref!r}")
        errors += check_facets(item_path, alignment)
        errors += check_mapping_gap(item_path, alignment)
        ref = alignment.get("industry_ref", {})
        if (
            isinstance(ref, dict)
            and ref.get("domain") == "voice-ucaas"
            and ref.get("capability") in {"sip-connectivity", "number-management"}
            and isinstance(alignment.get("facets"), dict)
            and "channel" in alignment["facets"]
        ):
            errors.append(f"{item_path}: pure voice infrastructure must not carry channel facet")
    if primary_count == 0 and not any(
        isinstance(a, dict) and a.get("supporting_only_reason") for a in alignments
    ):
        errors.append(f"{path}: missing primary alignment and supporting_only_reason")
    return alignments, errors


def check_common(path: str, entity: dict[str, Any], expected_level: str, require_maps: bool = True) -> list[str]:
    errors: list[str] = []
    errors += check_slug(path, "id", entity.get("id"))
    if entity.get("level") != expected_level:
        errors.append(f"{path}: level must be {expected_level!r}, got {entity.get('level')!r}")
    if not entity.get("name_ru") and not entity.get("name_en"):
        errors.append(f"{path}: name_ru or name_en is required")
    if entity.get("lifecycle_status") not in LIFECYCLE:
        errors.append(f"{path}: invalid lifecycle_status {entity.get('lifecycle_status')!r}")
    errors += check_evidence(path, entity)
    if require_maps:
        _, map_errors = check_alignments(path, entity.get("maps_to"))
        errors += map_errors
    return errors


def check_entities(official_data: dict[str, Any], internal_data: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], list[str]]:
    errors: list[str] = []
    all_entities: dict[str, dict[str, Any]] = {}
    official_taxonomy = official_data.get("taxonomy", {})
    internal_taxonomy = internal_data.get("taxonomy", {})

    if official_taxonomy.get("version") != 1:
        errors.append(f"{OFFICIAL}: taxonomy.version must be 1")
    if internal_taxonomy.get("version") != 1:
        errors.append(f"{INTERNAL}: taxonomy.version must be 1")

    collections = {
        "official_products": official_taxonomy.get("official_products"),
        "products": internal_taxonomy.get("products"),
        "internal_services": internal_taxonomy.get("internal_services"),
        "modules": internal_taxonomy.get("modules"),
        "functions": internal_taxonomy.get("functions"),
    }
    minimums = {
        "official_products": 8,
        "products": 8,
        "internal_services": 24,
        "modules": 32,
        "functions": 64,
    }
    for name, value in collections.items():
        if not isinstance(value, list):
            errors.append(f"taxonomy.{name}: must be array")
        elif len(value) < minimums[name]:
            errors.append(f"taxonomy.{name}: expected at least {minimums[name]} entries, got {len(value)}")

    for collection_name, expected_level in (
        ("official_products", "official-product"),
        ("products", "product"),
        ("internal_services", "service"),
        ("modules", "module"),
        ("functions", "function"),
    ):
        for index, entity in enumerate(collections.get(collection_name) or []):
            path = f"taxonomy.{collection_name}[{index}]"
            if not isinstance(entity, dict):
                errors.append(f"{path}: entity must be object")
                continue
            errors += check_common(path, entity, expected_level)
            entity_id = entity.get("id")
            if entity_id in all_entities:
                errors.append(f"{path}: duplicate entity id {entity_id!r}")
            elif is_slug(entity_id):
                all_entities[entity_id] = entity

    official_ids = {e["id"] for e in collections.get("official_products") or [] if isinstance(e, dict) and is_slug(e.get("id"))}
    product_ids = {e["id"] for e in collections.get("products") or [] if isinstance(e, dict) and is_slug(e.get("id"))}
    service_ids = {e["id"] for e in collections.get("internal_services") or [] if isinstance(e, dict) and is_slug(e.get("id"))}
    module_ids = {e["id"] for e in collections.get("modules") or [] if isinstance(e, dict) and is_slug(e.get("id"))}
    function_ids = {e["id"] for e in collections.get("functions") or [] if isinstance(e, dict) and is_slug(e.get("id"))}

    for index, official in enumerate(collections.get("official_products") or []):
        path = f"taxonomy.official_products[{index}]"
        urls = official.get("official_urls") if isinstance(official, dict) else None
        errors += check_nonempty_list(path, "official_urls", urls)
        for url in urls or []:
            if not isinstance(url, str) or not URL_RE.match(url):
                errors.append(f"{path}: invalid official URL {url!r}")
        for service in official.get("supported_by_services", []):
            if service not in service_ids:
                errors.append(f"{path}: unknown supported_by_services id {service!r}")

    for index, product in enumerate(collections.get("products") or []):
        path = f"taxonomy.products[{index}]"
        if not product.get("official_refs") and not product.get("internal_only_reason"):
            errors.append(f"{path}: official_refs or internal_only_reason is required")
        for official_ref in product.get("official_refs", []):
            if official_ref not in official_ids:
                errors.append(f"{path}: unknown official_ref {official_ref!r}")
        errors += check_nonempty_list(path, "services", product.get("services"))
        for service in product.get("services", []):
            if service not in service_ids:
                errors.append(f"{path}: unknown service id {service!r}")

    cluster_hits: set[str] = set()
    for index, service in enumerate(collections.get("internal_services") or []):
        path = f"taxonomy.internal_services[{index}]"
        if service.get("cluster") not in CLUSTERS:
            errors.append(f"{path}: invalid cluster {service.get('cluster')!r}")
        else:
            cluster_hits.add(service["cluster"])
        errors += check_nonempty_list(path, "parent_products", service.get("parent_products"))
        for product in service.get("parent_products", []):
            if product not in product_ids:
                errors.append(f"{path}: unknown parent_product {product!r}")
        errors += check_nonempty_list(path, "modules", service.get("modules"))
        for module in service.get("modules", []):
            if module not in module_ids:
                errors.append(f"{path}: unknown module id {module!r}")

    missing_clusters = sorted(CLUSTERS - cluster_hits)
    if missing_clusters:
        errors.append(f"{INTERNAL}: missing service coverage for clusters {missing_clusters}")

    for index, module in enumerate(collections.get("modules") or []):
        path = f"taxonomy.modules[{index}]"
        if module.get("cluster") not in CLUSTERS:
            errors.append(f"{path}: invalid cluster {module.get('cluster')!r}")
        errors += check_nonempty_list(path, "parent_services", module.get("parent_services"))
        for service in module.get("parent_services", []):
            if service not in service_ids:
                errors.append(f"{path}: unknown parent_service {service!r}")
        if not module.get("functions") and not module.get("function_extraction_status"):
            errors.append(f"{path}: functions or function_extraction_status is required")
        for function in module.get("functions", []):
            if function not in function_ids:
                errors.append(f"{path}: unknown function id {function!r}")

    function_type_hits: set[str] = set()
    for index, function in enumerate(collections.get("functions") or []):
        path = f"taxonomy.functions[{index}]"
        if function.get("parent_module") not in module_ids:
            errors.append(f"{path}: unknown parent_module {function.get('parent_module')!r}")
        if function.get("function_type") not in FUNCTION_TYPES:
            errors.append(f"{path}: invalid function_type {function.get('function_type')!r}")
        else:
            function_type_hits.add(function["function_type"])
        if function.get("interaction_surface") not in INTERACTION_SURFACES:
            errors.append(f"{path}: invalid interaction_surface {function.get('interaction_surface')!r}")

    missing_types = sorted(FUNCTION_TYPES - function_type_hits)
    if missing_types:
        errors.append(f"{INTERNAL}: missing function_type coverage {missing_types}")

    return all_entities, errors


def check_mapping_file(mapping_data: dict[str, Any], all_entities: dict[str, dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    root = mapping_data.get("taxonomy_mapping")
    if not isinstance(root, dict):
        return [f"{MAPPING}: missing taxonomy_mapping object"]
    for field, expected in (
        ("version", 1),
        ("mapping_scope", "mango-to-industry"),
        ("source_taxonomy", "mango-taxonomy"),
        ("target_taxonomy", "industry-taxonomy"),
    ):
        if root.get(field) != expected:
            errors.append(f"{MAPPING}: {field} must be {expected!r}")
    entities = root.get("entities")
    if not isinstance(entities, list):
        return errors + [f"{MAPPING}: taxonomy_mapping.entities must be array"]

    mapped: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(entities):
        path = f"taxonomy_mapping.entities[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{path}: mapping entity must be object")
            continue
        source_id = item.get("source_id")
        source_level = item.get("source_level")
        if source_id not in all_entities:
            errors.append(f"{path}: unknown source_id {source_id!r}")
            continue
        if source_id in mapped:
            errors.append(f"{path}: duplicate source_id {source_id!r}")
        mapped[source_id] = item
        expected_level = all_entities[source_id]["level"]
        if source_level != expected_level:
            errors.append(f"{path}: source_level {source_level!r} != {expected_level!r}")
        _, map_errors = check_alignments(path, {"industry_alignment": item.get("industry_alignment")})
        errors += map_errors
        if item.get("industry_alignment") != all_entities[source_id].get("maps_to", {}).get("industry_alignment"):
            errors.append(f"{path}: mapping must match entity maps_to.industry_alignment")

    missing = sorted(set(all_entities) - set(mapped))
    if missing:
        errors.append(f"{MAPPING}: missing mapping entries for {missing}")
    return errors


def check_readme_changelog_ci() -> list[str]:
    errors: list[str] = []
    errors += require_text(
        README,
        "Mango Taxonomy Registry",
        "Official Layer",
        "Internal Layer",
        "Product -> Service -> Module -> Function",
        "vats-core",
        "contact-center-core",
        "digital-channels",
        "mango-talker",
        "ai-speech-quality",
        "analytics-marketing",
        "platform-integrations",
        "security-access",
        "AI-agent",
        "Industry Taxonomy",
        "standards/mango-taxonomy-standard.md",
        "standards/decisions/ADR-012-mango-taxonomy.md",
        "standards/industry-taxonomy-standard.md",
    )
    errors += require_text(
        CHANGELOG,
        "Issue #160",
        OFFICIAL,
        INTERNAL,
        MAPPING,
        README,
        VALIDATOR,
    )
    errors += require_text(MAKEFILE, VALIDATOR)
    errors += require_text(
        KB_WORKFLOW,
        "Validate issue #160 Mango registry",
        f"python3 {VALIDATOR}",
    )
    if (ROOT / "research").exists():
        errors.append("research/: forbidden by issue #160")
    return errors


def main() -> int:
    errors: list[str] = []
    official_data, load_errors = load_json_yaml(OFFICIAL)
    errors += load_errors
    internal_data, load_errors = load_json_yaml(INTERNAL)
    errors += load_errors
    mapping_data, load_errors = load_json_yaml(MAPPING)
    errors += load_errors

    all_entities: dict[str, dict[str, Any]] = {}
    if official_data and internal_data:
        all_entities, entity_errors = check_entities(official_data, internal_data)
        errors += entity_errors
    if mapping_data and all_entities:
        errors += check_mapping_file(mapping_data, all_entities)
    errors += check_readme_changelog_ci()

    if errors:
        print("Issue #160 Mango registry validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Issue #160 Mango registry validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
