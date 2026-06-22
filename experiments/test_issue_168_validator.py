#!/usr/bin/env python3
"""Adversarial self-test for validate_issue_168_industry_reference_integrity.

Proves the registry-backed checker actually rejects malformed references rather
than rubber-stamping everything: resolution, alias handling, mapping_gap excuse,
deprecated/removed lifecycle, and the enum/slug/extra-key checks. stdlib-only.

Run: python3 experiments/test_issue_168_validator.py
"""
from __future__ import annotations

import importlib.util
import pathlib

REPO = pathlib.Path(__file__).resolve().parents[1]
MOD = REPO / "scripts" / "validate_issue_168_industry_reference_integrity.py"

spec = importlib.util.spec_from_file_location("v168", MOD)
v168 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v168)

reg = v168.Registry(v168.read_json(v168.REGISTRY))

PASS = 0
FAIL = 0


def expect(name, errors, warnings, *, want_err, want_warn):
    global PASS, FAIL
    ok_err = (len(errors) > 0) == want_err
    ok_warn = (len(warnings) > 0) == want_warn
    if ok_err and ok_warn:
        PASS += 1
        print(f"  ok  {name}")
    else:
        FAIL += 1
        print(f"FAIL  {name}: errors={errors} warnings={warnings} "
              f"(want_err={want_err} want_warn={want_warn})")


def run(alignment):
    return v168.check_alignment("test", alignment, reg)


# 1. fully valid canonical ref (added by this issue)
e, w = run({
    "alignment_type": "primary",
    "industry_ref": {"domain": "security", "capability": "access-control",
                     "feature": "role-management", "function": "assign-role"},
})
expect("valid 4-level ref resolves clean", e, w, want_err=False, want_warn=False)

# 2. alias resolution: communications-apis -> platform/cpaas
e, w = run({"industry_ref": {"domain": "platform", "capability": "communications-apis"}})
expect("capability alias resolves", e, w, want_err=False, want_warn=False)

# 3. alias resolution: webhook-management -> platform/open-api/webhooks (+ new fn)
e, w = run({"industry_ref": {"domain": "platform", "capability": "open-api",
                             "feature": "webhook-management",
                             "function": "configure-webhook-endpoint"}})
expect("feature alias + new function resolves", e, w, want_err=False, want_warn=False)

# 4. unknown capability, no gap -> error
e, w = run({"industry_ref": {"domain": "security", "capability": "does-not-exist"}})
expect("unknown capability is error", e, w, want_err=True, want_warn=False)

# 5. unknown capability WITH documented mapping_gap -> warning, not error
e, w = run({
    "industry_ref": {"domain": "security", "capability": "does-not-exist"},
    "mapping_gap": {"missing_level": "capability", "proposed_id": "does-not-exist",
                    "reason": "pending capability decision"},
})
expect("unknown capability with mapping_gap is warning", e, w, want_err=False, want_warn=True)

# 6. unknown domain -> error
e, w = run({"industry_ref": {"domain": "not-a-domain"}})
expect("unknown domain is error", e, w, want_err=True, want_warn=False)

# 7. parent-chain violation: feature without capability -> error
e, w = run({"industry_ref": {"domain": "security", "feature": "role-management"}})
expect("feature without capability is error", e, w, want_err=True, want_warn=False)

# 8. extra free-text key inside industry_ref -> error
e, w = run({"industry_ref": {"domain": "security", "tag": "iam"}})
expect("free-text key in industry_ref is error", e, w, want_err=True, want_warn=False)

# 9. invalid slug -> error
e, w = run({"industry_ref": {"domain": "Security"}})
expect("invalid slug is error", e, w, want_err=True, want_warn=False)

# 10. invalid alignment_type -> error
e, w = run({"alignment_type": "bogus",
            "industry_ref": {"domain": "security", "capability": "access-control"}})
expect("invalid alignment_type is error", e, w, want_err=True, want_warn=False)

# 11. invalid channel enum -> error
e, w = run({"industry_ref": {"domain": "security", "capability": "access-control"},
            "facets": {"channel": {"channel_kind": "telepathy",
                                   "synchronicity": "sync", "direction": "inbound"}}})
expect("invalid channel_kind is error", e, w, want_err=True, want_warn=False)

# 12. evidence ref that does not resolve -> error
e, w = run({"industry_ref": {"domain": "security", "capability": "access-control"},
            "evidence_refs": ["does/not/exist.md"]})
expect("non-resolving evidence ref is error", e, w, want_err=True, want_warn=False)

# 13. deprecated/removed lifecycle: synthesize nodes and resolve onto them
reg.capabilities[("security", "legacy-dep")] = {"id": "legacy-dep",
                                                "lifecycle_status": "deprecated",
                                                "replacement": "access-control"}
reg.capabilities[("security", "legacy-rm")] = {"id": "legacy-rm",
                                               "lifecycle_status": "removed"}
e, w = run({"industry_ref": {"domain": "security", "capability": "legacy-dep"}})
expect("deprecated node is warning", e, w, want_err=False, want_warn=True)
e, w = run({"industry_ref": {"domain": "security", "capability": "legacy-rm"}})
expect("removed node is error", e, w, want_err=True, want_warn=False)

print(f"\n{PASS} passed, {FAIL} failed")
raise SystemExit(1 if FAIL else 0)
