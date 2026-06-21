#!/usr/bin/env python3
"""Regression check for issue #156: Industry Taxonomy registry.

Issue #156 requires a machine-readable Industry Taxonomy registry under
``kb/industry/`` aligned with ADR-011 canonical v1.0 and the Industry Taxonomy
standard. The validator intentionally uses only Python stdlib so it can run in
the lightweight KB CI job.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

REGISTRY = "kb/industry/reference-taxonomy.json"
SCHEMA = "kb/industry/reference-taxonomy.schema.json"
README = "kb/industry/README.md"
KB_README = "kb/README.md"
CHANGELOG = "CHANGELOG.md"
MAKEFILE = "Makefile"
KB_WORKFLOW = ".github/workflows/kb.yml"
VALIDATOR = "scripts/validate_issue_156_industry_taxonomy_registry.py"

SLUG_RE = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")
PARAM_RE = re.compile(r"^[a-z][a-z0-9]*(?:_[a-z0-9]+)*$")

CANONICAL_DOMAINS = {
    "voice-ucaas",
    "contact-center",
    "digital-channels",
    "ai-automation",
    "analytics",
    "hardware",
    "security",
}

REQUIRED_CAPABILITIES = {
    "voice-channel",
    "cloud-pbx",
    "sip-connectivity",
    "number-management",
    "ivr-voice-menu",
    "call-recording",
    "callback",
    "unified-communications",
    "video-conferencing",
    "call-routing",
    "omnichannel-contact-center",
    "agent-workspace",
    "outbound-calling",
    "quality-management",
    "workforce-management",
    "knowledge-base",
    "sms-messaging",
    "omnichannel-messaging",
    "website-chat",
    "chatbot",
    "voice-bot",
    "speech-analytics",
    "platform-integration",
    "open-api",
    "cpaas",
}

REQUIRED_FEATURES = {
    "inbound-voice-call",
    "outbound-voice-call",
    "sip-trunking",
    "ivr-scenarios",
    "call-routing-rules",
    "campaign-management",
    "agent-desktop",
    "scorecards",
    "messenger-integration",
    "chat-widget",
    "transcription",
    "dynamic-number-pool",
    "access-control",
    "webhooks",
}

REQUIRED_FUNCTIONS = {
    "accept-inbound-voice-call",
    "initiate-outbound-voice-call",
    "sip-trunk-registration",
    "ivr-menu-navigation",
    "call-recording-capture",
    "predictive-dialing",
    "interaction-routing",
    "scorecard-evaluation",
    "bulk-sms-dispatch",
    "intent-classification",
    "call-transcription",
    "dynamic-number-substitution",
    "role-based-access-control",
    "webhook-subscription",
    "programmable-message-send",
}

ALLOWED_LEVELS = {"domain", "capability", "feature", "function"}
ALLOWED_LIFECYCLE = {"proposed", "active", "deprecated", "removed"}
ALLOWED_FUNCTION_TYPES = {"business", "configuration", "ui-action"}


def read_text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def read_json(path: str) -> Any:
    return json.loads(read_text(path))


def require_path(path: str) -> list[str]:
    return [] if (ROOT / path).exists() else [f"{path}: missing"]


def require_text(path: str, *needles: str) -> list[str]:
    errors = require_path(path)
    if errors:
        return errors
    text = read_text(path)
    return [f"{path}: missing {needle!r}" for needle in needles if needle not in text]


def valid_evidence(ref: str) -> bool:
    if ref.startswith(("http://", "https://")):
        return True
    return (ROOT / ref).exists()


def check_slug(value: str, path: str, errors: list[str]) -> None:
    if not SLUG_RE.fullmatch(value):
        errors.append(f"{path}: invalid slug {value!r}")


def require_node_fields(node: dict[str, Any], path: str, level: str, errors: list[str]) -> None:
    for field in ("id", "level", "name_en", "name_ru", "definition", "lifecycle_status", "evidence_refs"):
        if field not in node:
            errors.append(f"{path}: missing {field}")
    if node.get("level") != level:
        errors.append(f"{path}: expected level {level!r}, got {node.get('level')!r}")
    if node.get("level") not in ALLOWED_LEVELS:
        errors.append(f"{path}: invalid level {node.get('level')!r}")
    if isinstance(node.get("id"), str):
        check_slug(node["id"], path, errors)
    if node.get("lifecycle_status") not in ALLOWED_LIFECYCLE:
        errors.append(f"{path}: invalid lifecycle_status {node.get('lifecycle_status')!r}")
    refs = node.get("evidence_refs")
    if not isinstance(refs, list) or not refs:
        errors.append(f"{path}: evidence_refs must be a non-empty list")
    else:
        for ref in refs:
            if not isinstance(ref, str) or not valid_evidence(ref):
                errors.append(f"{path}: evidence ref does not resolve: {ref!r}")


def check_parameters(function: dict[str, Any], path: str, errors: list[str]) -> None:
    parameters = function.get("parameters")
    if not isinstance(parameters, list):
        errors.append(f"{path}: parameters must be a list")
        return
    for index, parameter in enumerate(parameters):
        param_path = f"{path}.parameters[{index}]"
        if not isinstance(parameter, dict):
            errors.append(f"{param_path}: must be an object")
            continue
        for field in ("name", "description"):
            if field not in parameter:
                errors.append(f"{param_path}: missing {field}")
        name = parameter.get("name")
        if isinstance(name, str) and not PARAM_RE.fullmatch(name):
            errors.append(f"{param_path}: invalid parameter name {name!r}")


def check_registry_nodes(registry: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    ids_by_level: dict[str, set[str]] = {level: set() for level in ALLOWED_LEVELS}
    counts = {"domains": 0, "layers": 0, "capabilities": 0, "features": 0, "functions": 0}

    domains = registry.get("domains")
    if not isinstance(domains, list):
        return ["kb/industry/reference-taxonomy.json: domains must be a list"]

    domain_ids = {domain.get("id") for domain in domains if isinstance(domain, dict)}
    if domain_ids != CANONICAL_DOMAINS:
        errors.append(f"{REGISTRY}: canonical domains mismatch: {sorted(domain_ids)!r}")

    cross_layers = registry.get("cross_domain_layers")
    if not isinstance(cross_layers, list):
        errors.append(f"{REGISTRY}: cross_domain_layers must be a list")
        cross_layers = []
    if {layer.get("id") for layer in cross_layers if isinstance(layer, dict)} != {"platform"}:
        errors.append(f"{REGISTRY}: platform must be the only cross-domain layer")

    def walk_container(container: dict[str, Any], container_path: str, is_layer: bool = False) -> None:
        level = "domain"
        require_node_fields(container, container_path, level, errors)
        if isinstance(container.get("id"), str):
            ids_by_level[level].add(container["id"])
        if is_layer:
            counts["layers"] += 1
            if container.get("taxonomy_role") != "cross-domain-layer":
                errors.append(f"{container_path}: platform must declare taxonomy_role=cross-domain-layer")
        else:
            counts["domains"] += 1
        capabilities = container.get("capabilities")
        if not isinstance(capabilities, list) or not capabilities:
            errors.append(f"{container_path}: capabilities must be a non-empty list")
            return
        for capability in capabilities:
            if not isinstance(capability, dict):
                errors.append(f"{container_path}.capabilities[?]: must be an object")
                continue
            cap_path = f"{container_path}.capabilities[{capability.get('id', '?')}]"
            require_node_fields(capability, cap_path, "capability", errors)
            if isinstance(capability.get("id"), str):
                ids_by_level["capability"].add(capability["id"])
            counts["capabilities"] += 1
            features = capability.get("features")
            if not isinstance(features, list) or not features:
                errors.append(f"{cap_path}: features must be a non-empty list")
                continue
            for feature in features:
                if not isinstance(feature, dict):
                    errors.append(f"{cap_path}.features[?]: must be an object")
                    continue
                feat_path = f"{cap_path}.features[{feature.get('id', '?')}]"
                require_node_fields(feature, feat_path, "feature", errors)
                if isinstance(feature.get("id"), str):
                    ids_by_level["feature"].add(feature["id"])
                counts["features"] += 1
                functions = feature.get("functions")
                if not isinstance(functions, list) or not functions:
                    errors.append(f"{feat_path}: functions must be a non-empty list")
                    continue
                for function in functions:
                    if not isinstance(function, dict):
                        errors.append(f"{feat_path}.functions[?]: must be an object")
                        continue
                    fn_path = f"{feat_path}.functions[{function.get('id', '?')}]"
                    require_node_fields(function, fn_path, "function", errors)
                    if isinstance(function.get("id"), str):
                        ids_by_level["function"].add(function["id"])
                    counts["functions"] += 1
                    if function.get("function_type") not in ALLOWED_FUNCTION_TYPES:
                        errors.append(
                            f"{fn_path}: invalid function_type {function.get('function_type')!r}"
                        )
                    check_parameters(function, fn_path, errors)

    for domain in domains:
        if isinstance(domain, dict):
            walk_container(domain, f"domains[{domain.get('id', '?')}]")
    for layer in cross_layers:
        if isinstance(layer, dict):
            walk_container(layer, f"cross_domain_layers[{layer.get('id', '?')}]", is_layer=True)

    minimums = {
        "domains": 7,
        "layers": 1,
        "capabilities": 43,
        "features": 120,
        "functions": 100,
    }
    for key, minimum in minimums.items():
        if counts[key] < minimum:
            errors.append(f"{REGISTRY}: expected at least {minimum} {key}, got {counts[key]}")

    missing_capabilities = REQUIRED_CAPABILITIES - ids_by_level["capability"]
    missing_features = REQUIRED_FEATURES - ids_by_level["feature"]
    missing_functions = REQUIRED_FUNCTIONS - ids_by_level["function"]
    if missing_capabilities:
        errors.append(f"{REGISTRY}: missing capabilities {sorted(missing_capabilities)!r}")
    if missing_features:
        errors.append(f"{REGISTRY}: missing features {sorted(missing_features)!r}")
    if missing_functions:
        errors.append(f"{REGISTRY}: missing functions {sorted(missing_functions)!r}")

    return errors


def check_registry_contract() -> list[str]:
    errors = require_path(REGISTRY)
    errors += require_path(SCHEMA)
    errors += require_path(README)
    if errors:
        return errors

    try:
        registry = read_json(REGISTRY)
    except json.JSONDecodeError as exc:
        return [f"{REGISTRY}: invalid JSON: {exc}"]
    try:
        schema = read_json(SCHEMA)
    except json.JSONDecodeError as exc:
        return [f"{SCHEMA}: invalid JSON: {exc}"]

    for field in ("taxonomy_id", "schema_version", "version", "last_updated", "status", "sources"):
        if field not in registry:
            errors.append(f"{REGISTRY}: missing top-level {field}")
    if registry.get("$schema") != "reference-taxonomy.schema.json":
        errors.append(f"{REGISTRY}: must reference local schema")
    if registry.get("taxonomy_id") != "industry-taxonomy":
        errors.append(f"{REGISTRY}: taxonomy_id must be industry-taxonomy")
    if registry.get("schema_version") != 1:
        errors.append(f"{REGISTRY}: schema_version must be 1")

    expected_levels = ["domain", "capability", "feature", "function"]
    if registry.get("levels") != expected_levels:
        errors.append(f"{REGISTRY}: levels must be {expected_levels!r}")
    if set(registry.get("lifecycle_statuses", [])) != ALLOWED_LIFECYCLE:
        errors.append(f"{REGISTRY}: lifecycle_statuses mismatch")
    if set(registry.get("function_types", [])) != ALLOWED_FUNCTION_TYPES:
        errors.append(f"{REGISTRY}: function_types mismatch")

    facets = registry.get("facets", {})
    channel_values = facets.get("channel", {}).get("allowed_values", {})
    if channel_values.get("channel_kind") != ["voice", "text", "video"]:
        errors.append(f"{REGISTRY}: channel_kind values mismatch")
    if channel_values.get("synchronicity") != ["sync", "async"]:
        errors.append(f"{REGISTRY}: synchronicity values mismatch")
    if channel_values.get("direction") != ["inbound", "outbound", "broadcast"]:
        errors.append(f"{REGISTRY}: direction values mismatch")
    for facet in ("ai_assisted", "security_compliance", "commercial", "procurement", "industry_vertical", "geography_region"):
        if facet not in facets:
            errors.append(f"{REGISTRY}: missing facet {facet!r}")

    if schema.get("$id") != "reference-taxonomy.schema.json":
        errors.append(f"{SCHEMA}: missing local $id")
    if "definitions" not in schema:
        errors.append(f"{SCHEMA}: missing definitions")

    errors += check_registry_nodes(registry)
    return errors


def check_docs_and_ci() -> list[str]:
    errors: list[str] = []
    errors += require_text(
        README,
        "# Industry Taxonomy",
        REGISTRY,
        SCHEMA,
        "Domain -> Capability -> Feature -> Function",
        "voice-ucaas",
        "contact-center",
        "digital-channels",
        "ai-automation",
        "analytics",
        "hardware",
        "security",
        "platform",
        "channel",
        "function_type",
        "evidence_refs",
    )
    errors += require_text(KB_README, "kb/industry/", "Industry Taxonomy")
    errors += require_text(
        CHANGELOG,
        "Issue #156",
        REGISTRY,
        SCHEMA,
        README,
        VALIDATOR,
    )
    errors += require_text(MAKEFILE, VALIDATOR)
    errors += require_text(
        KB_WORKFLOW,
        "Validate issue #156 Industry Taxonomy registry",
        f"python3 {VALIDATOR}",
    )
    return errors


def main() -> int:
    errors: list[str] = []
    errors += check_registry_contract()
    errors += check_docs_and_ci()

    if errors:
        print("Issue #156 Industry Taxonomy registry validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Issue #156 Industry Taxonomy registry validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
