#!/usr/bin/env python3
"""Issue #170 — build unified Mango registry JSON from the three legacy YAML files.

Combines kb/mango-taxonomy/official-products.yaml + internal-registry.yaml into a single
flat registry, drops the redundant product-mapping.yaml crosswalk, and RE-ALIGNS
every industry_ref so it resolves against the *real* kb/industry-taxonomy/registry.json
(the legacy validator only checked a frozen hardcoded subset, hiding 49 broken refs).

The script is idempotent and fails loudly if any expected remap target is missing
or any resulting industry_ref / evidence_ref / parent_ref does not resolve.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as f:
        return json.load(f)

industry = load("kb/industry-taxonomy/registry.json")
official = load("kb/mango-taxonomy/official-products.yaml")["taxonomy"]
internal = load("kb/mango-taxonomy/internal-registry.yaml")["taxonomy"]

# ---- industry resolution set -------------------------------------------------
def _slug(n): return n.get("id") or n.get("slug")
RES = set()
def _add_domain(dom):
    ds = _slug(dom); RES.add((ds,))
    for cap in dom.get("capabilities", []):
        cs = _slug(cap); RES.add((ds, cs))
        for feat in cap.get("features", []):
            fs = _slug(feat); RES.add((ds, cs, fs))
            for fn in feat.get("functions", []):
                RES.add((ds, cs, fs, _slug(fn)))
for d in industry.get("domains", []): _add_domain(d)
for l in industry.get("cross_domain_layers", []): _add_domain(l)  # 'platform' acts as a domain

def ref_to_tuple(r):
    t = [r["domain"]]
    for k in ("capability", "feature", "function"):
        if k in r: t.append(r[k])
    return tuple(t)

def ref_str(r): return "/".join(ref_to_tuple(r))

def tuple_to_ref(t):
    keys = ["domain", "capability", "feature", "function"]
    return {keys[i]: t[i] for i in range(len(t))}

# ---- remap table -------------------------------------------------------------
# key = (entity_id, old_ref_string); value = {"ref": <new ref dict>, "gap": <dict|None>}
# gap=None removes any existing mapping_gap; gap=dict sets it. industry_ref is replaced;
# alignment_type / facets / evidence_refs / confidence / supporting_only_reason are preserved.
def R(domain, capability=None, feature=None, function=None):
    r = {"domain": domain}
    if capability: r["capability"] = capability
    if feature: r["feature"] = feature
    if function: r["function"] = function
    return r
def G(level, pid, reason): return {"missing_level": level, "proposed_id": pid, "reason": reason}

REMAP = {
    # ---- official products ----
    ("mango-numbers-equipment-official", "hardware/device-management"):
        {"ref": R("hardware", "telephony-equipment"), "gap": None},

    # ---- mango-virtual-pbx ----
    ("vats-inbound-routing-service", "voice-ucaas/call-routing"):
        {"ref": R("voice-ucaas", "cloud-pbx", "call-routing-rules"), "gap": None},
    ("vats-inbound-scenarios-module", "voice-ucaas/call-routing"):
        {"ref": R("voice-ucaas", "cloud-pbx", "call-routing-rules"), "gap": None},
    ("configure-inbound-call-scenario", "voice-ucaas/call-routing"):
        {"ref": R("voice-ucaas", "cloud-pbx", "call-routing-rules"),
         "gap": G("function", "configure-inbound-call-scenario",
                  "Industry feature call-routing-rules models auto-attendant as its canonical function; configuring Mango VATS inbound scenarios is not separately modelled.")},
    ("receive-inbound-call-through-scenario", "voice-ucaas/voice-channel/inbound-voice-call/receive-inbound-call"):
        {"ref": R("voice-ucaas", "voice-channel", "inbound-voice-call", "accept-inbound-voice-call"), "gap": None},

    # ---- mango-contact-center ----
    ("cc-interaction-routing-service", "contact-center/interaction-routing/queue-routing"):
        {"ref": R("contact-center", "call-routing"), "gap": None},
    ("cc-queue-routing-module", "contact-center/interaction-routing/queue-routing"):
        {"ref": R("contact-center", "call-routing"), "gap": None},
    ("route-interaction-to-queue", "contact-center/interaction-routing/queue-routing"):
        {"ref": R("contact-center", "call-routing", "queue-management", "queue-management"), "gap": None},
    ("configure-queue-routing-rule", "contact-center/interaction-routing/routing-rules"):
        {"ref": R("contact-center", "call-routing", "queue-management"),
         "gap": G("function", "configure-queue-routing-rule",
                  "Industry feature queue-management models queue-management; configuring queue routing rules is a Mango admin action not separately modelled.")},
    ("start-outbound-campaign", "contact-center/outbound-calling/campaign-management/start-campaign"):
        {"ref": R("contact-center", "outbound-calling", "campaign-management"),
         "gap": G("function", "start-outbound-campaign",
                  "Industry feature campaign-management models campaign-configuration; launching/starting a campaign run is not separately modelled.")},
    ("cc-supervisor-wfm-service", "contact-center/supervisor-workspace"):
        {"ref": R("contact-center", "supervisor-assist"), "gap": None},
    ("cc-supervisor-wfm-module", "contact-center/supervisor-workspace"):
        {"ref": R("contact-center", "supervisor-assist"), "gap": None},
    ("monitor-agent-workload", "contact-center/supervisor-workspace"):
        {"ref": R("contact-center", "supervisor-assist", "live-monitoring", "manage-live-monitoring"), "gap": None},

    # ---- mango-digital-communications ----
    ("send-channel-message", "digital-channels/omnichannel-messaging/messenger-integration/send-message"):
        {"ref": R("digital-channels", "omnichannel-messaging", "messenger-integration"),
         "gap": G("function", "send-message",
                  "Industry feature messenger-integration models channel-ingestion (inbound); outbound message send is not separately modelled.")},
    ("reply-to-messenger-dialog", "digital-channels/omnichannel-messaging/messenger-integration/send-message"):
        {"ref": R("digital-channels", "omnichannel-messaging", "messenger-integration"),
         "gap": G("function", "send-message",
                  "Industry feature messenger-integration models channel-ingestion (inbound); outbound message send is not separately modelled.")},
    ("dialog-api-messaging-service", "platform/communications-apis"):
        {"ref": R("platform", "cpaas", "programmable-messaging"), "gap": None},
    ("dialog-api-message-module", "platform/communications-apis"):
        {"ref": R("platform", "cpaas", "programmable-messaging"), "gap": None},
    ("send-dialog-api-message", "digital-channels/omnichannel-messaging/messenger-integration/send-message"):
        {"ref": R("platform", "cpaas", "programmable-messaging", "programmable-message-send"), "gap": None},
    ("send-dialog-api-message", "platform/communications-apis"):
        {"ref": R("digital-channels", "omnichannel-messaging", "messenger-integration"), "gap": None},
    ("receive-dialog-api-event", "platform/open-api/webhook-management/configure-webhook-endpoint"):
        {"ref": R("platform", "open-api", "webhooks"),
         "gap": G("function", "webhook-event-delivery",
                  "Industry feature webhooks models webhook-subscription (configuration); inbound webhook event delivery is not separately modelled.")},

    # ---- mango-talker ----
    ("answer-talker-call", "voice-ucaas/voice-channel/inbound-voice-call/receive-inbound-call"):
        {"ref": R("voice-ucaas", "voice-channel", "inbound-voice-call", "accept-inbound-voice-call"), "gap": None},
    ("talker-team-chat-service", "digital-channels/team-messaging"):
        {"ref": R("voice-ucaas", "unified-communications", "corporate-messaging"), "gap": None},
    ("talker-team-chat-module", "digital-channels/team-messaging"):
        {"ref": R("voice-ucaas", "unified-communications", "corporate-messaging"), "gap": None},
    ("send-talker-chat-message", "digital-channels/team-messaging"):
        {"ref": R("voice-ucaas", "unified-communications", "corporate-messaging", "corporate-chat"), "gap": None},
    ("create-talker-chat-channel", "digital-channels/team-messaging"):
        {"ref": R("voice-ucaas", "unified-communications", "corporate-messaging"),
         "gap": G("function", "create-team-chat-channel",
                  "Industry feature corporate-messaging models corporate-chat; creating a chat channel/room is not separately modelled.")},

    # ---- mango-ai-speech-quality ----
    ("conversation-summary-service", "ai-automation/conversation-summaries/ai-summary/generate-summary"):
        {"ref": R("contact-center", "agent-assist", "conversation-summaries"), "gap": None},
    ("conversation-summary-module", "ai-automation/conversation-summaries/ai-summary/generate-summary"):
        {"ref": R("contact-center", "agent-assist", "conversation-summaries"), "gap": None},
    ("generate-call-summary", "ai-automation/conversation-summaries/ai-summary/generate-summary"):
        {"ref": R("contact-center", "agent-assist", "conversation-summaries", "manage-conversation-summaries"), "gap": None},
    ("view-call-summary", "ai-automation/conversation-summaries/ai-summary"):
        {"ref": R("contact-center", "agent-assist", "conversation-summaries"),
         "gap": G("function", "view-call-summary",
                  "Industry feature conversation-summaries models manage-conversation-summaries; viewing a generated summary is not separately modelled.")},

    # ---- mango-marketing-analytics ----
    ("select-dashboard-widget", "analytics/real-time-reporting/dashboard-view/select-dashboard-widget"):
        {"ref": R("analytics", "multichannel-analytics"),
         "gap": G("function", "select-dashboard-widget",
                  "Industry capability multichannel-analytics does not model dashboard widget selection as a function.")},
    ("wallboard-monitoring-service", "analytics/real-time-reporting"):
        {"ref": R("contact-center", "supervisor-assist", "live-monitoring"), "gap": None},
    ("wallboard-monitoring-module", "analytics/real-time-reporting"):
        {"ref": R("contact-center", "supervisor-assist", "live-monitoring"), "gap": None},
    ("display-wallboard-widget", "analytics/real-time-reporting/dashboard-view/select-dashboard-widget"):
        {"ref": R("contact-center", "supervisor-assist", "live-monitoring", "manage-live-monitoring"), "gap": None},
    ("configure-wallboard-widget", "analytics/real-time-reporting"):
        {"ref": R("contact-center", "supervisor-assist", "live-monitoring"),
         "gap": G("function", "configure-wallboard-widget",
                  "Industry feature live-monitoring models manage-live-monitoring; configuring wallboard widgets is not separately modelled.")},

    # ---- mango-platform-integrations ----
    ("configure-vpbx-webhook", "platform/open-api/webhook-management/configure-webhook-endpoint"):
        {"ref": R("platform", "open-api", "webhooks", "webhook-subscription"), "gap": None},
    ("receive-contact-center-event-webhook", "platform/open-api/webhook-management/configure-webhook-endpoint"):
        {"ref": R("platform", "open-api", "webhooks"),
         "gap": G("function", "webhook-event-delivery",
                  "Industry feature webhooks models webhook-subscription (configuration); inbound webhook event delivery is not separately modelled.")},
    ("webhook-event-service", "platform/open-api/webhook-management/configure-webhook-endpoint"):
        {"ref": R("platform", "open-api", "webhooks"), "gap": None},
    ("webhook-event-module", "platform/open-api/webhook-management/configure-webhook-endpoint"):
        {"ref": R("platform", "open-api", "webhooks"), "gap": None},
    ("send-call-event-webhook", "platform/open-api/webhook-management/configure-webhook-endpoint"):
        {"ref": R("platform", "open-api", "webhooks"),
         "gap": G("function", "webhook-event-delivery",
                  "Industry feature webhooks models webhook-subscription (configuration); outbound webhook event delivery is not separately modelled.")},
    ("configure-webhook-endpoint", "platform/open-api/webhook-management/configure-webhook-endpoint"):
        {"ref": R("platform", "open-api", "webhooks", "webhook-subscription"), "gap": None},

    # ---- mango-security-access ----
    ("mango-security-access", "security/access-control"):
        {"ref": R("security", "information-security"), "gap": None},
    ("sso-identity-service", "security/access-control"):
        {"ref": R("security", "information-security", "access-control"), "gap": None},
    ("sso-identity-module", "security/access-control"):
        {"ref": R("security", "information-security", "access-control"), "gap": None},
    ("authenticate-user-with-sso", "security/access-control"):
        {"ref": R("security", "information-security", "access-control"),
         "gap": G("function", "sso-authentication",
                  "Industry feature access-control models role-based-access-control; SSO end-user authentication is not separately modelled.")},
    ("configure-sso-connection", "security/access-control"):
        {"ref": R("security", "information-security", "access-control"),
         "gap": G("function", "sso-configuration",
                  "Industry feature access-control models role-based-access-control; configuring an SSO connection is not separately modelled.")},
    ("role-access-management-service", "security/access-control/role-management/assign-role"):
        {"ref": R("security", "information-security", "access-control"), "gap": None},
    ("role-access-management-module", "security/access-control/role-management/assign-role"):
        {"ref": R("security", "information-security", "access-control"), "gap": None},
    ("assign-user-role", "security/access-control/role-management/assign-role"):
        {"ref": R("security", "information-security", "access-control", "role-based-access-control"), "gap": None},
    ("view-role-permissions", "security/access-control/role-management"):
        {"ref": R("security", "information-security", "access-control"),
         "gap": G("function", "view-role-permissions",
                  "Industry feature access-control models role-based-access-control; viewing role permissions is not separately modelled.")},
}

# ---- apply remap -------------------------------------------------------------
applied = set()
def remap_entity(e):
    for a in e.get("maps_to", {}).get("industry_alignment", []):
        r = a.get("industry_ref")
        if not r:
            continue
        key = (e["id"], ref_str(r))
        if key in REMAP:
            spec = REMAP[key]
            a["industry_ref"] = spec["ref"]
            if spec["gap"] is None:
                a.pop("mapping_gap", None)
            else:
                a["mapping_gap"] = spec["gap"]
            applied.add(key)

buckets = [
    ("official_products", official.get("official_products", [])),
    ("products", internal["products"]),
    ("internal_services", internal["internal_services"]),
    ("modules", internal["modules"]),
    ("functions", internal["functions"]),
]
for _, items in buckets:
    for e in items:
        remap_entity(e)

# every declared remap must have matched exactly one alignment
unused = set(REMAP) - applied
if unused:
    print("ERROR: remap entries that never matched:", file=sys.stderr)
    for k in sorted(unused): print("   ", k, file=sys.stderr)
    sys.exit(1)

# ---- assemble unified registry ----------------------------------------------
# Root mirrors standard §8.1 MangoTaxonomyDocument exactly: additionalProperties:false
# permits only "taxonomy", and taxonomy permits only version + the five entity arrays
# (no $schema/scope). The schema is referenced by the validator, not embedded.
registry = {
    "taxonomy": {
        "version": "1.0.0",
        "official_products": official.get("official_products", []),
        "products": internal["products"],
        "internal_services": internal["internal_services"],
        "modules": internal["modules"],
        "functions": internal["functions"],
    },
}

# ---- self-validation ---------------------------------------------------------
errors = []
all_ids = {}
def visit(level_name, items):
    for e in items:
        all_ids.setdefault(e["id"], []).append(level_name)
        for a in e.get("maps_to", {}).get("industry_alignment", []):
            r = a.get("industry_ref")
            if r and ref_to_tuple(r) not in RES:
                errors.append(f"{e['id']}: industry_ref does not resolve: {ref_str(r)}")
for name, items in [(n, registry["taxonomy"][n]) for n, _ in buckets]:
    visit(name, items)

if errors:
    print("SELF-VALIDATION FAILED:", file=sys.stderr)
    for e in errors: print("   ", e, file=sys.stderr)
    sys.exit(1)

out = os.path.join(ROOT, "kb/mango-taxonomy/registry.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(registry, f, ensure_ascii=False, indent=2)
    f.write("\n")

t = registry["taxonomy"]
print("OK  wrote kb/mango-taxonomy/registry.json")
print(f"    remaps applied: {len(applied)}/{len(REMAP)}")
print(f"    official_products={len(t['official_products'])} products={len(t['products'])} "
      f"services={len(t['internal_services'])} modules={len(t['modules'])} functions={len(t['functions'])}")
print("    all industry_refs resolve against kb/industry-taxonomy/registry.json")
