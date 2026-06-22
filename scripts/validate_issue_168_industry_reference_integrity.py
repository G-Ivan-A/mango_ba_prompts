#!/usr/bin/env python3
"""Issue #168: registry-backed referential-integrity check for Mango industry refs.

Where ``validate_issue_170`` validates the Mango registry against its own JSON
Schema, this check resolves every ``industry_ref`` in the Mango registry
(``kb/mango/mango-registry.json``) against the *actual* Industry reference registry
(``kb/industry/reference-taxonomy.json``) so the two artifacts cannot silently
drift apart. It implements the registry-resolvable subset of the standard's
§11.2 mapping-validator contract:

- (3) ``industry_ref.domain`` is required;
- (4) the domain resolves in ``domains[]`` / ``cross_domain_layers[]``;
- (5-7) capability / feature / function each resolve under their parent;
- (8) no deeper field appears without its parent field;
- (9) ``alignment_type`` is one of primary / secondary / supporting;
- (11-13) ``facets.channel`` enum values are valid;
- (18) ``evidence_refs`` resolve to an existing repo path or a full URL;
- (19) every ``industry_ref`` value is a valid slug;
- (20) ``industry_ref`` carries no free-text / unknown keys;
- (21) resolving onto a ``deprecated`` node is a warning (with replacement);
- (22) resolving onto a ``removed`` node is an error.

Resolution is alias-aware (standard §4.5): a node's ``aliases`` resolve to the
same canonical chain as its ``id``. A reference that does not resolve is an
error, *unless* its alignment carries a documented ``mapping_gap`` (standard
§8.4, DoD #7), in which case it is reported as a warning instead.

stdlib-only. The Mango registry is a JSON document, so ``json.loads`` parses it
without adding PyYAML to the lightweight KB job.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Iterator


ROOT = Path(__file__).resolve().parents[1]

REGISTRY = "kb/industry/reference-taxonomy.json"
# Issue #170 collapsed the three Mango YAML files into one JSON registry; this
# check now reads that single document. Its `industry_ref` objects keep the same
# shape (domain/capability/feature/function), so resolution is unchanged.
MANGO_FILES = [
    "kb/mango/mango-registry.json",
]
MAKEFILE = "Makefile"
KB_WORKFLOW = ".github/workflows/kb.yml"
VALIDATOR = "scripts/validate_issue_168_industry_reference_integrity.py"

SLUG_RE = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")
URL_RE = re.compile(r"^https?://")

REF_KEYS = ("domain", "capability", "feature", "function")
ALIGNMENT_TYPES = {"primary", "secondary", "supporting"}
CHANNEL_KIND = {"voice", "text", "video"}
SYNCHRONICITY = {"sync", "async"}
DIRECTION = {"inbound", "outbound", "broadcast"}


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def read_json(rel: str) -> Any:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def ref_exists(ref: str) -> bool:
    return bool(URL_RE.match(ref)) or (ROOT / ref).exists()


def names_with_aliases(node: dict) -> list[str]:
    """Canonical id plus any aliases (standard §4.5)."""
    out = [node["id"]]
    out.extend(node.get("aliases", []) or [])
    return out


# --------------------------------------------------------------------------- #
# registry index (alias-aware, carries lifecycle for each resolvable chain)
# --------------------------------------------------------------------------- #
class Registry:
    """Resolves parent-chains to canonical nodes, expanding aliases."""

    def __init__(self, registry: dict):
        self.domains: dict[str, dict] = {}
        self.capabilities: dict[tuple, dict] = {}
        self.features: dict[tuple, dict] = {}
        self.functions: dict[tuple, dict] = {}

        roots = list(registry.get("domains", [])) + list(
            registry.get("cross_domain_layers", [])
        )
        for dom in roots:
            for d in names_with_aliases(dom):
                self.domains[d] = dom
            for cap in dom.get("capabilities", []) or []:
                for d in names_with_aliases(dom):
                    for c in names_with_aliases(cap):
                        self.capabilities[(d, c)] = cap
                for feat in cap.get("features", []) or []:
                    for d in names_with_aliases(dom):
                        for c in names_with_aliases(cap):
                            for f in names_with_aliases(feat):
                                self.features[(d, c, f)] = feat
                    for fn in feat.get("functions", []) or []:
                        for d in names_with_aliases(dom):
                            for c in names_with_aliases(cap):
                                for f in names_with_aliases(feat):
                                    for n in names_with_aliases(fn):
                                        self.functions[(d, c, f, n)] = fn

    def resolve(self, ref: dict) -> tuple[dict | None, str | None]:
        """Return (deepest_resolved_node, error_message).

        ``error_message`` is None on success. On failure the node is None and a
        human-readable reason (unknown domain/capability/feature/function) is
        returned.
        """
        d = ref.get("domain")
        c = ref.get("capability")
        f = ref.get("feature")
        n = ref.get("function")

        if d not in self.domains:
            return None, f"unknown industry domain {d!r}"
        node = self.domains[d]
        if c is not None:
            node = self.capabilities.get((d, c))
            if node is None:
                return None, f"unknown capability {d}/{c}"
        if f is not None:
            node = self.features.get((d, c, f))
            if node is None:
                return None, f"unknown feature {d}/{c}/{f}"
        if n is not None:
            node = self.functions.get((d, c, f, n))
            if node is None:
                return None, f"unknown function {d}/{c}/{f}/{n}"
        return node, None


# --------------------------------------------------------------------------- #
# walk every alignment object (a dict carrying an ``industry_ref``)
# --------------------------------------------------------------------------- #
def iter_alignments(obj: Any, path: str = "$") -> Iterator[tuple[str, dict]]:
    if isinstance(obj, dict):
        if isinstance(obj.get("industry_ref"), dict):
            yield path, obj
        for k, v in obj.items():
            yield from iter_alignments(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from iter_alignments(v, f"{path}[{i}]")


def valid_mapping_gap(alignment: dict) -> bool:
    """A documented gap (§8.4) excuses an otherwise-unresolved reference."""
    gap = alignment.get("mapping_gap")
    if not isinstance(gap, dict):
        return False
    return (
        gap.get("missing_level") in set(REF_KEYS)
        and isinstance(gap.get("proposed_id"), str)
        and isinstance(gap.get("reason"), str)
        and bool(gap.get("reason", "").strip())
    )


def check_alignment(
    path: str, alignment: dict, reg: Registry
) -> tuple[list[str], list[str]]:
    """Return (errors, warnings) for a single alignment object."""
    errors: list[str] = []
    warnings: list[str] = []
    ref = alignment["industry_ref"]

    # (20) only canonical keys allowed inside industry_ref
    extra = sorted(set(ref) - set(REF_KEYS))
    if extra:
        errors.append(f"{path}: industry_ref has unexpected keys {extra}")

    # (19) slug pattern on every present value
    for field in REF_KEYS:
        if field in ref and not (
            isinstance(ref[field], str) and SLUG_RE.fullmatch(ref[field])
        ):
            errors.append(f"{path}: invalid slug in industry_ref.{field}: {ref[field]!r}")

    # (3) domain required
    if "domain" not in ref:
        errors.append(f"{path}: industry_ref.domain is required")

    # (8) no deeper field without its parent
    if ref.get("function") and not ref.get("feature"):
        errors.append(f"{path}: industry_ref.function requires feature")
    if ref.get("feature") and not ref.get("capability"):
        errors.append(f"{path}: industry_ref.feature requires capability")
    if ref.get("capability") and not ref.get("domain"):
        errors.append(f"{path}: industry_ref.capability requires domain")

    # (4-7) resolve the parent-chain against the registry (alias-aware)
    node, reason = reg.resolve(ref)
    if reason is not None:
        if valid_mapping_gap(alignment):
            warnings.append(f"{path}: {reason} (documented mapping_gap)")
        else:
            errors.append(f"{path}: {reason}")
    else:
        # (21-22) lifecycle of the resolved node
        status = node.get("lifecycle_status")
        if status == "removed":
            errors.append(
                f"{path}: industry_ref resolves to a removed node {node.get('id')!r}"
            )
        elif status == "deprecated":
            repl = node.get("replacement")
            tail = f"; replacement: {repl}" if repl else "; no replacement recorded"
            warnings.append(
                f"{path}: industry_ref resolves to a deprecated node "
                f"{node.get('id')!r}{tail}"
            )

    # (9) alignment_type, when present, must be valid
    if "alignment_type" in alignment and alignment["alignment_type"] not in ALIGNMENT_TYPES:
        errors.append(
            f"{path}: invalid alignment_type {alignment['alignment_type']!r}"
        )

    # (11-13) channel facet enums
    facets = alignment.get("facets")
    if isinstance(facets, dict):
        channel = facets.get("channel")
        if isinstance(channel, dict):
            if channel.get("channel_kind") not in CHANNEL_KIND:
                errors.append(
                    f"{path}: invalid channel_kind {channel.get('channel_kind')!r}"
                )
            if channel.get("synchronicity") not in SYNCHRONICITY:
                errors.append(
                    f"{path}: invalid synchronicity {channel.get('synchronicity')!r}"
                )
            if channel.get("direction") not in DIRECTION:
                errors.append(
                    f"{path}: invalid direction {channel.get('direction')!r}"
                )

    # (18) evidence refs, when present, must resolve
    for evref in alignment.get("evidence_refs", []) or []:
        if not isinstance(evref, str) or not ref_exists(evref):
            errors.append(f"{path}: evidence ref does not resolve: {evref!r}")

    return errors, warnings


# --------------------------------------------------------------------------- #
# self-wiring guard (keeps the check from silently dropping out of CI)
# --------------------------------------------------------------------------- #
def check_wiring() -> list[str]:
    errors: list[str] = []
    for rel in (MAKEFILE, KB_WORKFLOW):
        text = (ROOT / rel).read_text(encoding="utf-8") if (ROOT / rel).exists() else ""
        if VALIDATOR not in text:
            errors.append(f"{rel}: must invoke {VALIDATOR}")
    return errors


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    reg = Registry(read_json(REGISTRY))

    total = 0
    for rel in MANGO_FILES:
        data = read_json(rel)
        for path, alignment in iter_alignments(data):
            total += 1
            e, w = check_alignment(f"{rel}:{path}", alignment, reg)
            errors += e
            warnings += w

    errors += check_wiring()

    for w in warnings:
        print(f"WARN: {w}")

    if errors:
        print(f"Issue #168 industry reference integrity FAILED ({len(errors)} error(s)):")
        for e in errors:
            print(f"  - {e}")
        return 1

    print(
        f"Issue #168 industry reference integrity passed: "
        f"{total} industry_ref resolved against {REGISTRY}"
        + (f" ({len(warnings)} warning(s))" if warnings else "")
        + "."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
