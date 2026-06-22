#!/usr/bin/env python3
"""Issue #174 — taxonomy convergence (inter-rater reliability) scorer.

Compares the blind AI-agent classification (blind-agent-output.json) against the
independent reference classification (reference-classification.json) and reports
per-level and full-path convergence. Validates that every node id the AI agent
emitted is canonical (exists in kb/industry-taxonomy/registry.json).

Run from repo root:
    python3 experiments/issue-174/score_convergence.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def canonical_ids(tax):
    ids = {"domain": set(), "capability": set(), "feature": set(), "function": set()}
    for container in (tax["domains"], tax["cross_domain_layers"]):
        for dom in container:
            ids["domain"].add(dom["id"])
            for cap in dom.get("capabilities", []):
                ids["capability"].add(cap["id"])
                for feat in cap.get("features", []):
                    ids["feature"].add(feat["id"])
                    for fn in feat.get("functions", []):
                        ids["function"].add(fn["id"])
    return ids


def main():
    ref = {r["n"]: r for r in load(os.path.join(HERE, "reference-classification.json"))}
    ai = {a["n"]: a for a in load(os.path.join(HERE, "blind-agent-output.json"))}
    tax = load(os.path.join(ROOT, "kb", "industry-taxonomy", "registry.json"))
    valid = canonical_ids(tax)

    n_total = len(ref)
    counters = dict(dom=0, cap=0, ft=0, full=0)
    feat_total = feat_m = fn_total = fn_m = 0
    invalid = []
    rows = []

    for n in sorted(ref):
        r, a = ref[n], ai[n]
        for lvl in ("domain", "capability", "feature", "function"):
            v = a.get(lvl)
            if v and v not in valid[lvl]:
                invalid.append((n, lvl, v))
        dm = r["ref_domain"] == a["domain"]
        cm = r["ref_capability"] == a["capability"]
        counters["dom"] += dm
        counters["cap"] += cm
        fm = None
        if r["ref_feature"]:
            feat_total += 1
            fm = r["ref_feature"] == a.get("feature")
            feat_m += fm
        fnm = None
        if r["ref_function"]:
            fn_total += 1
            fnm = r["ref_function"] == a.get("function")
            fn_m += fnm
        ftm = r["function_type"] == a["function_type"]
        counters["ft"] += ftm
        full = dm and cm and (fm if r["ref_feature"] else True) and (fnm if r["ref_function"] else True)
        counters["full"] += full
        rows.append(dict(n=n, id=r["id"], dom=dm, cap=cm, feat=fm, fn=fnm, ft=ftm, full=full))

    pct = lambda a, b: (a / b * 100) if b else float("nan")
    print(f"N = {n_total} functions")
    print(f"Domain      : {counters['dom']}/{n_total} = {pct(counters['dom'], n_total):.1f}%")
    print(f"Capability  : {counters['cap']}/{n_total} = {pct(counters['cap'], n_total):.1f}%")
    print(f"Feature     : {feat_m}/{feat_total} = {pct(feat_m, feat_total):.1f}% (scored where reference specifies feature)")
    print(f"Function    : {fn_m}/{fn_total} = {pct(fn_m, fn_total):.1f}% (scored where reference specifies function)")
    print(f"func_type   : {counters['ft']}/{n_total} = {pct(counters['ft'], n_total):.1f}%")
    print(f"FULL path   : {counters['full']}/{n_total} = {pct(counters['full'], n_total):.1f}%")
    if invalid:
        print("INVALID (non-canonical) ids emitted by AI agent:", invalid)
        return 1
    print("All AI-agent node ids are canonical (present in registry.json).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
