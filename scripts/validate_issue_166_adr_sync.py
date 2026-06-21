#!/usr/bin/env python3
"""Regression check for issue #166: ADR-011/ADR-012 synchronization.

Issue #166 (Task #3 of the taxonomy audit follow-up) eliminates cross-standard
discrepancies between ADR-011 and ADR-012:

* a single, non-contradictory source priority (ADR-011 has priority over ADR-012)
  is stated symmetrically in both ADRs and matches §1.3 of both standards;
* drafted field names in ADR-012 machine-readable examples are replaced with the
  canonical ones from the Mango Taxonomy standard (`level`, `official_urls`,
  `supported_by_services`, `evidence_refs`, `maps_to.industry_alignment[]`);
* every `industry_ref` slug used in ADR examples resolves in the canonical
  Industry registry `kb/industry/reference-taxonomy.json`;
* the `select-wallboard-widget` alignment is realigned to the canonical chain.

The check is intentionally substring/structure based and stdlib-only so it runs
in the same lightweight CI lane as the other taxonomy validators.
"""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

ADR_011 = "standards/decisions/ADR-011-industry-taxonomy.md"
ADR_012 = "standards/decisions/ADR-012-mango-taxonomy.md"
INDUSTRY_STANDARD = "standards/industry-taxonomy-standard.md"
MANGO_STANDARD = "standards/mango-taxonomy-standard.md"
INDUSTRY_REGISTRY = "kb/industry/reference-taxonomy.json"
CHANGELOG = "CHANGELOG.md"
MAKEFILE = "Makefile"
KB_WORKFLOW = ".github/workflows/kb.yml"
VALIDATOR = "scripts/validate_issue_166_adr_sync.py"

PRIORITY_STATEMENT = "ADR-011 имеет приоритет над ADR-012"


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
                        paths.add(
                            f"{domain_id}/{capability_id}/{feature_id}/{function['id']}"
                        )
    return paths


def collect_example_industry_refs(path: str) -> list[tuple[str, str]]:
    """Collect domain/capability/feature/function chains from YAML examples.

    Mirrors the proven collector used by the issue #154 validator so the two
    documents are checked against the same canonical registry the same way.
    """
    text = read_text(path)
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
        if (
            stripped.startswith("alignment_type:")
            or stripped.startswith("facets:")
            or stripped.startswith("mapping_gap:")
            or not stripped
        ):
            if "domain" in current:
                chain = "/".join(
                    current[key]
                    for key in ("domain", "capability", "feature", "function")
                    if key in current
                )
                refs.append((chain, " | ".join(current_lines)))
                current = {}
                current_lines = []
    if "domain" in current:
        chain = "/".join(
            current[key]
            for key in ("domain", "capability", "feature", "function")
            if key in current
        )
        refs.append((chain, " | ".join(current_lines)))
    return refs


def check_priority_sync() -> list[str]:
    """Both ADRs must state the same, non-contradictory source priority.

    The single accepted order is: ADR-011 has priority over ADR-012. Both ADRs
    and the Mango standard state it verbatim; the Industry standard expresses the
    identical order through its §1.3 ordered list plus the conflict-resolution
    sentence (it is read-only here, so it is checked structurally).
    """
    errors: list[str] = []
    errors += require_text(ADR_011, PRIORITY_STATEMENT)
    errors += require_text(ADR_012, PRIORITY_STATEMENT)
    errors += require_text(MANGO_STANDARD, PRIORITY_STATEMENT)

    # Industry standard §1.3 must place ADR-011 above ADR-012 and resolve any
    # conflict in favor of ADR-011 — the same direction, different wording.
    errors += require_text(
        INDUSTRY_STANDARD,
        "ADR-012 противоречит ADR-011, применяется ADR-011",
    )
    industry_errors = require_path(INDUSTRY_STANDARD)
    if not industry_errors:
        text = read_text(INDUSTRY_STANDARD)
        section = text[text.find("### 1.3 Приоритет источников") :]
        section = section[: section.find("\n## ")] if "\n## " in section else section
        adr011_pos = section.find("ADR-011")
        adr012_pos = section.find("ADR-012")
        if adr011_pos == -1 or adr012_pos == -1 or adr011_pos > adr012_pos:
            errors.append(
                f"{INDUSTRY_STANDARD}: §1.3 must place ADR-011 before ADR-012"
            )
    else:
        errors += industry_errors

    # Each ADR must point readers at the canonical Industry registry so the
    # priority is actionable, not just declarative.
    errors += require_text(ADR_011, INDUSTRY_REGISTRY)
    errors += require_text(ADR_012, INDUSTRY_REGISTRY)
    return errors


def check_field_name_unification() -> list[str]:
    """ADR-012 machine-readable examples must use canonical field names."""
    errors: list[str] = []
    errors += require_text(
        ADR_012,
        "level: official-product",
        "level: service",
        "level: module",
        "level: function",
        "official_urls:",
        "supported_by_services:",
        "evidence_refs:",
        "maps_to:",
        "industry_alignment:",
    )
    # Drafted/legacy names must not survive in the YAML examples. These tokens
    # never legitimately appear as YAML keys in the canonical contract.
    errors += forbid_text(
        ADR_012,
        "layer: official",
        "layer: internal",
        "public_urls:",
        "kb_refs:",
        "evidence_level:",
    )
    return errors


def check_alignment_drift() -> list[str]:
    """select-wallboard-widget and webhook slugs must be realigned."""
    errors: list[str] = []
    # Canonical wallboard chain (primary contact-center supervisor-assist).
    errors += require_text(
        ADR_012,
        "capability: supervisor-assist",
        "feature: live-monitoring",
        "function: manage-live-monitoring",
    )
    # Canonical webhook slugs replace the non-resolving draft slugs.
    errors += require_text(ADR_012, "feature: webhooks", "function: webhook-subscription")
    errors += forbid_text(
        ADR_012,
        "feature: real-time-dashboard",
        "function: configure-dashboard-widget",
        "feature: webhook-management",
        "function: configure-webhook-endpoint",
    )
    return errors


def check_industry_refs_resolve() -> list[str]:
    """Every industry_ref chain in both ADR examples must resolve canonically."""
    errors: list[str] = []
    known_paths = load_industry_paths()
    for path in (ADR_011, ADR_012):
        for chain, source in collect_example_industry_refs(path):
            if chain not in known_paths:
                errors.append(
                    f"{path}: example industry_ref does not resolve in "
                    f"{INDUSTRY_REGISTRY}: {chain} ({source})"
                )
    return errors


def check_changelog_and_ci() -> list[str]:
    errors: list[str] = []
    errors += require_text(
        CHANGELOG,
        "Issue #166",
        "ADR-011",
        "ADR-012",
        VALIDATOR,
    )
    errors += require_text(MAKEFILE, VALIDATOR)
    errors += require_text(
        KB_WORKFLOW,
        "Validate issue #166 ADR sync",
        f"python3 {VALIDATOR}",
    )
    return errors


def main() -> int:
    errors: list[str] = []
    errors += check_priority_sync()
    errors += check_field_name_unification()
    errors += check_alignment_drift()
    errors += check_industry_refs_resolve()
    errors += check_changelog_and_ci()

    if errors:
        print("Issue #166 ADR sync validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Issue #166 ADR sync validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
