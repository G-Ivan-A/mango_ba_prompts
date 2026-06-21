#!/usr/bin/env python3
"""Issue #168 — gap analysis (research helper, not a CI gate).

Loads the Industry reference registry, builds the set of valid parent-chains
(Domain -> Capability -> Feature -> Function) including ``aliases``, then scans
every ``industry_ref`` in ``kb/mango/*.yaml`` and reports which entities do not
resolve. Output is grouped by level so the registry gap is explicit.

stdlib-only. Mango YAML files are JSON-compatible, so ``json`` parses them.
"""
from __future__ import annotations

import json
import pathlib
from collections import OrderedDict

REPO = pathlib.Path(__file__).resolve().parents[1]
REGISTRY = REPO / "kb" / "industry" / "reference-taxonomy.json"
MANGO_FILES = [
    REPO / "kb" / "mango" / "internal-registry.yaml",
    REPO / "kb" / "mango" / "official-products.yaml",
    REPO / "kb" / "mango" / "product-mapping.yaml",
]


def names_with_aliases(node: dict) -> list[str]:
    """Return the canonical id plus any aliases for a registry node."""
    out = [node["id"]]
    out.extend(node.get("aliases", []) or [])
    return out


def build_index(registry: dict):
    """Return resolver sets for domains, capabilities, features, functions.

    Each non-domain level is keyed by its full parent-chain tuple so that the
    same slug under different parents stays distinct. Aliases expand into
    additional keys that resolve to the same canonical chain.
    """
    domains: set[str] = set()
    capabilities: set[tuple] = set()
    features: set[tuple] = set()
    functions: set[tuple] = set()

    roots = list(registry.get("domains", [])) + list(
        registry.get("cross_domain_layers", [])
    )
    for dom in roots:
        for d_name in names_with_aliases(dom):
            domains.add(d_name)
        for cap in dom.get("capabilities", []) or []:
            for d_name in names_with_aliases(dom):
                for c_name in names_with_aliases(cap):
                    capabilities.add((d_name, c_name))
            for feat in cap.get("features", []) or []:
                for d_name in names_with_aliases(dom):
                    for c_name in names_with_aliases(cap):
                        for f_name in names_with_aliases(feat):
                            features.add((d_name, c_name, f_name))
                for fn in feat.get("functions", []) or []:
                    for d_name in names_with_aliases(dom):
                        for c_name in names_with_aliases(cap):
                            for f_name in names_with_aliases(feat):
                                for n_name in names_with_aliases(fn):
                                    functions.add((d_name, c_name, f_name, n_name))
    return domains, capabilities, features, functions


def iter_industry_refs(obj, _path="$"):
    """Yield every ``industry_ref`` dict found anywhere in a nested structure."""
    if isinstance(obj, dict):
        ref = obj.get("industry_ref")
        if isinstance(ref, dict):
            yield ref
        for k, v in obj.items():
            yield from iter_industry_refs(v, f"{_path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from iter_industry_refs(v, f"{_path}[{i}]")


def main() -> int:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    domains, capabilities, features, functions = build_index(registry)

    total = 0
    unresolved = 0
    with_gap = 0
    missing_caps: "OrderedDict[tuple,int]" = OrderedDict()
    missing_feats: "OrderedDict[tuple,int]" = OrderedDict()
    missing_fns: "OrderedDict[tuple,int]" = OrderedDict()

    for path in MANGO_FILES:
        data = json.loads(path.read_text(encoding="utf-8"))
        for ref in iter_industry_refs(data):
            total += 1
            d = ref.get("domain")
            c = ref.get("capability")
            f = ref.get("feature")
            n = ref.get("function")
            ok = True
            if d is not None and d not in domains:
                ok = False
            if ok and c is not None and (d, c) not in capabilities:
                ok = False
                missing_caps[(d, c)] = missing_caps.get((d, c), 0) + 1
            if ok and f is not None and (d, c, f) not in features:
                ok = False
                missing_feats[(d, c, f)] = missing_feats.get((d, c, f), 0) + 1
            if ok and n is not None and (d, c, f, n) not in functions:
                ok = False
                missing_fns[(d, c, f, n)] = missing_fns.get((d, c, f, n), 0) + 1
            if not ok:
                unresolved += 1
                if ref.get("mapping_gap"):
                    with_gap += 1

    print(f"Total industry_ref         : {total}")
    print(f"Unresolved                 : {unresolved}")
    print(f"  ...with mapping_gap      : {with_gap}")
    print(f"  ...without mapping_gap   : {unresolved - with_gap}")
    print()
    print(f"Distinct missing capabilities ({len(missing_caps)}):")
    for (d, c), cnt in missing_caps.items():
        print(f"  {d}/{c}  x{cnt}")
    print()
    print(f"Distinct missing features ({len(missing_feats)}):")
    for (d, c, f), cnt in missing_feats.items():
        print(f"  {d}/{c}/{f}  x{cnt}")
    print()
    print(f"Distinct missing functions ({len(missing_fns)}):")
    for (d, c, f, n), cnt in missing_fns.items():
        print(f"  {d}/{c}/{f}/{n}  x{cnt}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
