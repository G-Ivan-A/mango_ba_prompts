#!/usr/bin/env python3
"""Registry validator for issue #170: unified Mango registry JSON.

Issue #170 converts the three legacy Mango YAML files (official-products.yaml,
internal-registry.yaml, product-mapping.yaml) into a single JSON registry
``kb/mango-taxonomy/mango-registry.json`` plus a JSON Schema ``mango-registry.schema.json``,
and demands real referential integrity against the Industry Taxonomy registry.

Unlike the retired ``validate_issue_160_mango_registry.py`` (which only checked a
frozen, hardcoded subset of the Industry taxonomy and therefore missed broken
``industry_ref`` chains), this validator resolves every ``industry_ref`` against
the *live* ``kb/industry-taxonomy/reference-taxonomy.json`` and implements the registry
contract from the Mango Taxonomy standard §8.2 and §11.2 (30 checks).

Stdlib only — no PyYAML, no jsonschema. The legacy YAML files are JSON-compatible
but here they are gone; the registry is genuine JSON parsed with ``json``.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

REGISTRY = "kb/mango-taxonomy/mango-registry.json"
SCHEMA = "kb/mango-taxonomy/mango-registry.schema.json"
INDUSTRY_REGISTRY = "kb/industry-taxonomy/reference-taxonomy.json"
STANDARD = "standards/mango-taxonomy-standard.md"
CHANGELOG = "CHANGELOG.md"
MAKEFILE = "Makefile"
KB_WORKFLOW = ".github/workflows/kb.yml"
README = "kb/mango-taxonomy/README.md"
VALIDATOR = "scripts/validate_issue_170_mango_registry.py"

LEGACY_YAML = (
    "kb/mango-taxonomy/official-products.yaml",
    "kb/mango-taxonomy/internal-registry.yaml",
    "kb/mango-taxonomy/product-mapping.yaml",
)

SLUG_RE = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")
SEMVER_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")

LIFECYCLE = {"proposed", "active", "deprecated"}
CLUSTERS = {
    "vats-core", "contact-center-core", "digital-channels", "mango-talker",
    "ai-speech-quality", "analytics-marketing", "platform-integrations", "security-access",
}
FUNCTION_TYPES = {"business", "configuration", "ui-action"}
INTERACTION_SURFACES = {
    "admin-ui", "operator-ui", "end-user-ui", "api",
    "webhook", "background-job", "system-rule", "unknown",
}
ALIGNMENT_TYPES = {"primary", "secondary", "supporting"}
CHANNEL_KINDS = {"voice", "text", "video"}
SYNCHRONICITY = {"sync", "async"}
DIRECTIONS = {"inbound", "outbound", "broadcast"}
MISSING_LEVELS = {"domain", "capability", "feature", "function"}
ALLOWED_FACET_KEYS = {
    "channel", "ai_assisted", "security_compliance", "commercial",
    "procurement", "industry_vertical", "geography_region",
}
EXTRACTION_STATUS = {"complete", "partial", "not-started"}

# Pure telecom / equipment infrastructure: SIP, numbering, hardware. Such mappings
# are supporting infrastructure and MUST NOT carry an interaction channel facet
# (standard §4, §10.3, §11.2 rule 20).
INFRA_CAPABILITIES = {"sip-connectivity", "number-management"}
INFRA_DOMAINS = {"hardware"}

# DoD / regression floors (current registry is the floor; cascade-fill only grows it).
FLOORS = {
    "official_products": 10,
    "products": 8,
    "internal_services": 32,
    "modules": 32,
    "functions": 64,
}

# Per-level required (beyond commonEntity id/level/lifecycle_status/evidence_refs/name).
REQUIRED_BY_LEVEL = {
    "official-product": ("official_urls", "supported_by_services"),
    "product": ("services", "maps_to"),
    "service": ("cluster", "parent_products", "maps_to"),
    "module": ("cluster", "parent_services", "maps_to"),
    "function": ("parent_module", "function_type", "interaction_surface", "maps_to"),
}


def read_json(path: str) -> Any:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


# --------------------------------------------------------------------------- #
# Industry registry resolution index
# --------------------------------------------------------------------------- #
def load_industry_index() -> set[tuple[str, ...]]:
    data = read_json(INDUSTRY_REGISTRY)
    res: set[tuple[str, ...]] = set()
    for collection in ("domains", "cross_domain_layers"):
        for domain in data.get(collection, []):
            d = domain["id"]
            res.add((d,))
            for cap in domain.get("capabilities", []):
                c = cap["id"]
                res.add((d, c))
                for feat in cap.get("features", []):
                    f = feat["id"]
                    res.add((d, c, f))
                    for fn in feat.get("functions", []):
                        res.add((d, c, f, fn["id"]))
    return res


def ref_tuple(ref: dict[str, Any]) -> tuple[str, ...]:
    out = [ref["domain"]]
    for key in ("capability", "feature", "function"):
        if key in ref:
            out.append(ref[key])
    return tuple(out)


def ref_str(ref: dict[str, Any]) -> str:
    return "/".join(ref_tuple(ref))


# --------------------------------------------------------------------------- #
# Schema-file checks (the deliverable schema must mirror standard §8.1)
# --------------------------------------------------------------------------- #
def check_schema_file() -> list[str]:
    errors: list[str] = []
    if not (ROOT / SCHEMA).exists():
        return [f"{SCHEMA}: missing"]
    try:
        schema = read_json(SCHEMA)
    except json.JSONDecodeError as exc:
        return [f"{SCHEMA}: invalid JSON: {exc}"]

    if "$schema" not in schema:
        errors.append(f"{SCHEMA}: missing $schema")
    if schema.get("$id") != "mango-registry.schema.json":
        errors.append(f"{SCHEMA}: $id must be 'mango-registry.schema.json'")
    if schema.get("title") != "MangoTaxonomyDocument":
        errors.append(f"{SCHEMA}: title must be 'MangoTaxonomyDocument'")
    if schema.get("required") != ["taxonomy"] or schema.get("additionalProperties") is not False:
        errors.append(f"{SCHEMA}: root must require only 'taxonomy' with additionalProperties false")

    defs = schema.get("$defs")
    if not isinstance(defs, dict):
        return errors + [f"{SCHEMA}: missing $defs"]

    expected_defs = {
        "slug", "lifecycleStatus", "cluster", "functionType", "interactionSurface",
        "evidenceRef", "industryRef", "channelFacet", "facets", "mappingGap",
        "industryAlignment", "mapsTo", "commonEntity", "officialProduct", "product",
        "service", "module", "function", "taxonomy",
    }
    missing = expected_defs - set(defs)
    if missing:
        errors.append(f"{SCHEMA}: $defs missing {sorted(missing)}")

    if defs.get("slug", {}).get("pattern") != SLUG_RE.pattern:
        errors.append(f"{SCHEMA}: slug pattern must equal {SLUG_RE.pattern!r}")
    if set(defs.get("lifecycleStatus", {}).get("enum", [])) != LIFECYCLE:
        errors.append(f"{SCHEMA}: lifecycleStatus enum must be {sorted(LIFECYCLE)} (no 'removed')")
    if set(defs.get("cluster", {}).get("enum", [])) != CLUSTERS:
        errors.append(f"{SCHEMA}: cluster enum must be the eight canonical clusters")
    if set(defs.get("functionType", {}).get("enum", [])) != FUNCTION_TYPES:
        errors.append(f"{SCHEMA}: functionType enum mismatch")
    if set(defs.get("interactionSurface", {}).get("enum", [])) != INTERACTION_SURFACES:
        errors.append(f"{SCHEMA}: interactionSurface enum mismatch")
    tax = defs.get("taxonomy", {})
    if tax.get("additionalProperties") is not False:
        errors.append(f"{SCHEMA}: taxonomy must close additionalProperties")
    if set(tax.get("required", [])) != {"version", *FLOORS}:
        errors.append(f"{SCHEMA}: taxonomy.required must list version + the five arrays")
    if tax.get("properties", {}).get("version", {}).get("pattern") != SEMVER_RE.pattern:
        errors.append(f"{SCHEMA}: taxonomy.version must be a semver string pattern")
    for level in ("officialProduct", "product", "service", "module", "function"):
        if defs.get(level, {}).get("unevaluatedProperties") is not False:
            errors.append(f"{SCHEMA}: {level} must set unevaluatedProperties false")
    return errors


# --------------------------------------------------------------------------- #
# Registry checks
# --------------------------------------------------------------------------- #
def check_registry() -> list[str]:
    errors: list[str] = []

    # The conversion must be complete: JSON present, legacy YAML/crosswalk gone.
    if not (ROOT / REGISTRY).exists():
        return [f"{REGISTRY}: missing — unified registry was not created"]
    for legacy in LEGACY_YAML:
        if (ROOT / legacy).exists():
            errors.append(f"{legacy}: legacy file must be removed after conversion to JSON")

    try:
        registry = read_json(REGISTRY)  # rule 1
    except json.JSONDecodeError as exc:
        return errors + [f"{REGISTRY}: invalid JSON: {exc}"]

    if set(registry) != {"taxonomy"}:
        errors.append(f"{REGISTRY}: root must contain only 'taxonomy' (got {sorted(registry)})")
    tax = registry.get("taxonomy", {})
    if not isinstance(tax, dict):
        return errors + [f"{REGISTRY}: taxonomy must be an object"]

    allowed_tax_keys = {"version", *FLOORS}
    extra = set(tax) - allowed_tax_keys
    if extra:
        errors.append(f"{REGISTRY}: taxonomy has unexpected keys {sorted(extra)}")

    version = tax.get("version")  # rule 2
    if not isinstance(version, str) or not SEMVER_RE.match(version):
        errors.append(f"{REGISTRY}: taxonomy.version must be a semver string, got {version!r}")

    buckets = {
        "official_products": ("official-product", tax.get("official_products", [])),
        "products": ("product", tax.get("products", [])),
        "internal_services": ("service", tax.get("internal_services", [])),
        "modules": ("module", tax.get("modules", [])),
        "functions": ("function", tax.get("functions", [])),
    }

    # Completeness floors (rule: DoD minimums / regression guard).
    for key, floor in FLOORS.items():
        n = len(buckets[key][1])
        if key == "products" and n != floor:
            errors.append(f"{REGISTRY}: products must be exactly {floor} (ADR-012 fixed set), got {n}")
        elif n < floor:
            errors.append(f"{REGISTRY}: {key} has {n}, expected >= {floor}")

    industry_index = load_industry_index()

    # ---- index every entity by id and collect per-level ids ----
    by_id: dict[str, dict[str, Any]] = {}
    level_ids: dict[str, set[str]] = {lvl: set() for lvl, _ in buckets.values()}
    for key, (level, items) in buckets.items():
        for e in items:
            eid = e.get("id")
            if not isinstance(eid, str):
                errors.append(f"{key}: entity without string id: {e!r:.80}")
                continue
            if not SLUG_RE.match(eid):  # rule 3
                errors.append(f"{eid}: id is not a canonical slug")
            if eid in by_id:  # rule 4 (global uniqueness across levels)
                errors.append(f"{eid}: duplicate id (also defined as {by_id[eid].get('level')})")
            by_id[eid] = e
            level_ids[level].add(eid)
            if e.get("level") != level:  # rule 6
                errors.append(f"{eid}: level must be {level!r}, got {e.get('level')!r}")

    def resolve(child_id: str, target_level: str, owner: str) -> None:
        target = by_id.get(child_id)
        if target is None:
            errors.append(f"{owner}: references unknown id {child_id!r}")
        elif target.get("level") != target_level:
            errors.append(f"{owner}: {child_id!r} must be a {target_level}, is {target.get('level')!r}")

    # ---- per-entity field + semantic checks ----
    for key, (level, items) in buckets.items():
        for e in items:
            eid = e.get("id", "<no-id>")

            # rule 5 — required fields by level + commonEntity essentials
            for field in ("level", "lifecycle_status", "evidence_refs"):
                if field not in e:
                    errors.append(f"{eid}: missing required field {field!r}")
            if "name_ru" not in e and "name_en" not in e:
                errors.append(f"{eid}: must have name_ru or name_en")
            for field in REQUIRED_BY_LEVEL.get(level, ()):  # rule 5
                if field not in e:
                    errors.append(f"{eid}: {level} missing required field {field!r}")

            # lifecycle
            ls = e.get("lifecycle_status")
            if ls not in LIFECYCLE:
                errors.append(f"{eid}: lifecycle_status {ls!r} not in {sorted(LIFECYCLE)}")
            if ls == "deprecated" and not (e.get("deprecation_reason") or e.get("replaced_by")):  # rule 29
                errors.append(f"{eid}: deprecated entity needs deprecation_reason or replaced_by")

            # evidence_refs resolve (rule 18)
            errors += check_evidence(eid, e.get("evidence_refs"))

            # rule 10 — function_type only on Function
            if "function_type" in e and level != "function":
                errors.append(f"{eid}: function_type present on non-function {level}")

            # source_terms / level discipline (rules 26-28)
            terms = e.get("source_terms", []) or []
            if "Component" in terms and level != "module":  # rule 27
                errors.append(f"{eid}: source_term 'Component' only allowed on level module")
            if "Operation" in terms and level != "function":  # rule 28
                errors.append(f"{eid}: source_term 'Operation' only allowed on level function")

            # level-specific structure
            if level == "official-product":
                for u in e.get("official_urls", []) or []:
                    if not (isinstance(u, str) and u.startswith(("http://", "https://"))):
                        errors.append(f"{eid}: official_urls must be URLs, got {u!r}")
                for sid in e.get("supported_by_services", []) or []:  # rule 7
                    resolve(sid, "service", f"{eid}.supported_by_services")

            elif level == "product":
                if e.get("cluster") is not None:
                    errors.append(f"{eid}: product must not carry cluster")
                has_official = bool(e.get("official_refs"))
                has_reason = bool(e.get("internal_only_reason"))
                if not (has_official or has_reason):
                    errors.append(f"{eid}: product needs official_refs or internal_only_reason")
                for oid in e.get("official_refs", []) or []:  # rule 7
                    resolve(oid, "official-product", f"{eid}.official_refs")
                if not e.get("services"):
                    errors.append(f"{eid}: product must have >=1 service")
                if len(e.get("services", []) or []) < 2:  # DoD: each product >=2 services
                    errors.append(f"{eid}: product should have >=2 services (DoD)")
                for sid in e.get("services", []) or []:  # rule 7 + DoD #4 consistency
                    resolve(sid, "service", f"{eid}.services")
                    child = by_id.get(sid)
                    if child and eid not in (child.get("parent_products") or []):
                        errors.append(f"{eid}: service {sid!r} does not list {eid!r} in parent_products")

            elif level == "service":
                errors += check_cluster(eid, e)
                for pid in e.get("parent_products", []) or []:  # rule 7 (explicit parent ref, DoD #4)
                    resolve(pid, "product", f"{eid}.parent_products")
                if not (e.get("parent_products")):
                    errors.append(f"{eid}: service must reference >=1 parent product")
                if not (e.get("modules") or e.get("module_extraction_status")):  # rule 24
                    errors.append(f"{eid}: service needs modules[] or module_extraction_status")
                if e.get("module_extraction_status") and e["module_extraction_status"] not in EXTRACTION_STATUS:
                    errors.append(f"{eid}: module_extraction_status invalid")
                for mid in e.get("modules", []) or []:  # rule 7 + consistency
                    resolve(mid, "module", f"{eid}.modules")
                    child = by_id.get(mid)
                    if child and eid not in (child.get("parent_services") or []):
                        errors.append(f"{eid}: module {mid!r} does not list {eid!r} in parent_services")

            elif level == "module":
                errors += check_cluster(eid, e)
                for sid in e.get("parent_services", []) or []:  # rule 7 (explicit parent ref)
                    resolve(sid, "service", f"{eid}.parent_services")
                if not e.get("parent_services"):
                    errors.append(f"{eid}: module must reference >=1 parent service")
                if not (e.get("functions") or e.get("function_extraction_status")):  # rule 25
                    errors.append(f"{eid}: module needs functions[] or function_extraction_status")
                if e.get("function_extraction_status") and e["function_extraction_status"] not in EXTRACTION_STATUS:
                    errors.append(f"{eid}: function_extraction_status invalid")
                fns = e.get("functions", []) or []
                if fns and len(fns) < 2:  # DoD: each module >=2 functions (when functions present)
                    errors.append(f"{eid}: module should have >=2 functions (DoD)")
                for fid in fns:  # rule 7 + consistency
                    resolve(fid, "function", f"{eid}.functions")
                    child = by_id.get(fid)
                    if child and child.get("parent_module") != eid:
                        errors.append(f"{eid}: function {fid!r} parent_module != {eid!r}")

            elif level == "function":
                pm = e.get("parent_module")
                if pm:  # rule 7 (explicit parent ref, DoD #4)
                    resolve(pm, "module", f"{eid}.parent_module")
                    if pm == eid:  # rule 8 (no self-parent / cycle)
                        errors.append(f"{eid}: function is its own parent_module")
                ft = e.get("function_type")
                if ft not in FUNCTION_TYPES:  # rules 10, 11
                    errors.append(f"{eid}: function_type {ft!r} invalid")
                surf = e.get("interaction_surface")
                if surf not in INTERACTION_SURFACES:  # rule 12
                    errors.append(f"{eid}: interaction_surface {surf!r} invalid")
                if ls == "active" and surf == "unknown":  # §8.2 / schema 'not'
                    errors.append(f"{eid}: active function must not use interaction_surface 'unknown'")
                if e.get("cluster") is not None:
                    errors.append(f"{eid}: function must not carry cluster")

            # maps_to / industry alignment (rules 13-23)
            errors += check_maps_to(eid, level, e, industry_index)

    return errors


def check_cluster(eid: str, e: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    cluster = e.get("cluster")
    if cluster not in CLUSTERS:  # rule 9
        errors.append(f"{eid}: cluster {cluster!r} not one of eight canonical ids")
    for sc in e.get("secondary_clusters", []) or []:
        if sc not in CLUSTERS:
            errors.append(f"{eid}: secondary cluster {sc!r} invalid")
        if sc == cluster:
            errors.append(f"{eid}: secondary cluster duplicates primary cluster")
    return errors


def check_evidence(owner: str, refs: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(refs, list) or not refs:
        errors.append(f"{owner}: evidence_refs must be a non-empty array")
        return errors
    for ref in refs:
        if not isinstance(ref, str) or not ref:
            errors.append(f"{owner}: evidence_ref must be a non-empty string")
        elif ref.startswith(("http://", "https://")):
            continue
        elif not (ROOT / ref).exists():  # rule 18
            errors.append(f"{owner}: evidence_ref does not resolve: {ref}")
    return errors


def check_maps_to(eid: str, level: str, e: dict[str, Any],
                  industry_index: set[tuple[str, ...]]) -> list[str]:
    errors: list[str] = []
    maps_to = e.get("maps_to")
    if maps_to is None:
        if level != "official-product":
            errors.append(f"{eid}: missing maps_to")
        return errors
    if set(maps_to) - {"industry_alignment"}:
        errors.append(f"{eid}: maps_to has unexpected keys {sorted(set(maps_to) - {'industry_alignment'})}")
    alignments = maps_to.get("industry_alignment")
    if not isinstance(alignments, list) or not alignments:  # rule 13
        errors.append(f"{eid}: maps_to.industry_alignment must be a non-empty array")
        return errors

    primaries = 0
    all_supporting = True
    for i, a in enumerate(alignments):
        loc = f"{eid}.industry_alignment[{i}]"
        atype = a.get("alignment_type")
        if atype not in ALIGNMENT_TYPES:  # rule 16
            errors.append(f"{loc}: alignment_type {atype!r} invalid")
        if atype == "primary":
            primaries += 1
        if atype != "supporting":
            all_supporting = False

        ref = a.get("industry_ref")
        if not isinstance(ref, dict) or "domain" not in ref:  # rule 14
            errors.append(f"{loc}: alignment must have industry_ref.domain")
        else:
            errors += check_industry_ref(loc, ref, industry_index)

        # evidence on the alignment (optional but if present must resolve) — rule 18
        if "evidence_refs" in a:
            errors += check_evidence(loc, a.get("evidence_refs"))

        # mapping_gap (rules from §8.1 mappingGap)
        gap = a.get("mapping_gap")
        if gap is not None:
            if set(gap) != {"missing_level", "proposed_id", "reason"}:
                errors.append(f"{loc}: mapping_gap keys must be missing_level/proposed_id/reason")
            if gap.get("missing_level") not in MISSING_LEVELS:
                errors.append(f"{loc}: mapping_gap.missing_level invalid")
            if not SLUG_RE.match(str(gap.get("proposed_id", ""))):
                errors.append(f"{loc}: mapping_gap.proposed_id not a slug")
            if not str(gap.get("reason", "")).strip():
                errors.append(f"{loc}: mapping_gap.reason must be non-empty")

        # confidence (rule 23)
        conf = a.get("confidence")
        if conf is not None and not (isinstance(conf, (int, float)) and 0.0 <= conf <= 1.0):
            errors.append(f"{loc}: confidence must be within [0.0, 1.0]")

        # facets (rules 19, 20, 22)
        errors += check_facets(loc, a.get("facets"), ref if isinstance(ref, dict) else {})

    if primaries == 0 and not all_supporting:  # rule 17
        errors.append(f"{eid}: non-supporting-only entity has no primary alignment")
    return errors


def check_industry_ref(loc: str, ref: dict[str, Any],
                       industry_index: set[tuple[str, ...]]) -> list[str]:
    errors: list[str] = []
    extra = set(ref) - {"domain", "capability", "feature", "function"}
    if extra:
        errors.append(f"{loc}: industry_ref has unknown keys {sorted(extra)}")
    # rule 15 — no deeper field without its parent
    if "function" in ref and "feature" not in ref:
        errors.append(f"{loc}: industry_ref has function without feature")
    if "feature" in ref and "capability" not in ref:
        errors.append(f"{loc}: industry_ref has feature without capability")
    if "capability" in ref and "domain" not in ref:
        errors.append(f"{loc}: industry_ref has capability without domain")
    for part in ref.values():
        if not (isinstance(part, str) and SLUG_RE.match(part)):
            errors.append(f"{loc}: industry_ref part {part!r} is not a slug")
    # §8.2 — industry_ref chain resolves in Industry registry
    t = ref_tuple(ref)
    if t not in industry_index:
        errors.append(f"{loc}: industry_ref does not resolve in Industry registry: {ref_str(ref)}")
    return errors


def check_facets(loc: str, facets: Any, ref: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if facets is None:
        return errors
    if not isinstance(facets, dict):
        errors.append(f"{loc}: facets must be an object")
        return errors
    unknown = set(facets) - ALLOWED_FACET_KEYS  # rule 22
    if unknown:
        errors.append(f"{loc}: facets has non-canonical keys {sorted(unknown)}")
    channel = facets.get("channel")
    if channel is not None:
        if set(channel) != {"channel_kind", "synchronicity", "direction"}:
            errors.append(f"{loc}: facets.channel must have channel_kind/synchronicity/direction")
        if channel.get("channel_kind") not in CHANNEL_KINDS:  # rule 19
            errors.append(f"{loc}: facets.channel.channel_kind invalid")
        if channel.get("synchronicity") not in SYNCHRONICITY:  # rule 19
            errors.append(f"{loc}: facets.channel.synchronicity invalid")
        if channel.get("direction") not in DIRECTIONS:  # rules 19, 21
            errors.append(f"{loc}: facets.channel.direction invalid")
        # rule 20 — pure SIP/numbering/hardware infrastructure carries no channel facet
        if ref.get("domain") in INFRA_DOMAINS or ref.get("capability") in INFRA_CAPABILITIES:
            errors.append(f"{loc}: pure infrastructure mapping ({ref_str(ref)}) must not carry channel facet")
    return errors


# --------------------------------------------------------------------------- #
# CI wiring + docs
# --------------------------------------------------------------------------- #
def check_wiring() -> list[str]:
    errors: list[str] = []

    def require_text(path: str, *needles: str) -> None:
        p = ROOT / path
        if not p.exists():
            errors.append(f"{path}: missing")
            return
        text = p.read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text:
                errors.append(f"{path}: missing {needle!r}")

    def forbid_text(path: str, *needles: str) -> None:
        p = ROOT / path
        if not p.exists():
            return
        text = p.read_text(encoding="utf-8")
        for needle in needles:
            if needle in text:
                errors.append(f"{path}: must not reference retired {needle!r}")

    require_text(CHANGELOG, "Issue #170", REGISTRY, SCHEMA, VALIDATOR)
    require_text(MAKEFILE, VALIDATOR)
    require_text(KB_WORKFLOW, f"python3 {VALIDATOR}")
    # The retired #160 validator must be gone everywhere.
    forbid_text(KB_WORKFLOW, "validate_issue_160_mango_registry.py")
    forbid_text(MAKEFILE, "validate_issue_160_mango_registry.py")
    if (ROOT / "scripts/validate_issue_160_mango_registry.py").exists():
        errors.append("scripts/validate_issue_160_mango_registry.py: retired script must be removed")
    return errors


def main() -> int:
    errors: list[str] = []
    errors += check_schema_file()
    errors += check_registry()
    errors += check_wiring()

    if errors:
        print("Issue #170 Mango registry validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Issue #170 Mango registry validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
