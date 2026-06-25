#!/usr/bin/env python3
"""Issue #168 — deterministic cascade-fill builder for the Industry registry.

Inserts the capabilities/features/functions and the two aliases decided in
``docs/analysis/2026-06-21-industry-inventory.md`` into ``kb/industry-taxonomy/registry.json``,
bumps the registry version 1.0.0 -> 1.1.0 (additive == MINOR, standard §10.4),
adds a source entry and a registry note, and writes the file back with the same
serialization the registry already uses (``json.dumps(indent=2,
ensure_ascii=False) + "\\n"``) so the diff stays minimal.

Re-runnable: existing ids/aliases are not duplicated. stdlib-only.
"""
from __future__ import annotations

import json
import pathlib

REPO = pathlib.Path(__file__).resolve().parents[1]
REGISTRY = REPO / "kb" / "industry-taxonomy" / "registry.json"

EV = [
    "standards/decisions/ADR-011-industry-taxonomy.md",
    "standards/industry-taxonomy-standard.md",
    "docs/analysis/2026-06-21-industry-inventory.md",
]
SRC = "issue-168-cascade-fill"


# --------------------------------------------------------------------------- #
# node builders (match existing key ordering exactly)
# --------------------------------------------------------------------------- #
def channel(kind, sync, direction):
    return {"channel": {"channel_kind": kind, "synchronicity": sync, "direction": direction}}


def param(name):
    return {
        "name": name,
        "description": f"Canonical parameter `{name}` for configuring or executing this function.",
    }


def make_function(fid, en, ru, definition, ftype, params, parent, facets=None):
    node = {
        "id": fid,
        "level": "function",
        "name_en": en,
        "name_ru": ru,
        "definition": definition,
        "lifecycle_status": "active",
        "evidence_refs": list(EV),
        "parent": parent,
        "function_type": ftype,
        "parameters": [param(p) for p in params],
    }
    if facets:
        node["facets"] = facets
    node["source_status"] = SRC
    return node


def make_feature(fid, en, ru, definition, parent, functions, facets=None):
    node = {
        "id": fid,
        "level": "feature",
        "name_en": en,
        "name_ru": ru,
        "definition": definition,
        "lifecycle_status": "active",
        "evidence_refs": list(EV),
        "parent": parent,
        "functions": functions,
    }
    if facets:
        node["facets"] = facets
    node["source_status"] = SRC
    return node


def make_capability(cid, en, ru, definition, domain, features, facets=None):
    node = {
        "id": cid,
        "level": "capability",
        "name_en": en,
        "name_ru": ru,
        "definition": definition,
        "lifecycle_status": "active",
        "evidence_refs": list(EV),
        "parent": {"domain": domain},
        "features": features,
    }
    if facets:
        node["facets"] = facets
    node["source_status"] = SRC
    return node


# --------------------------------------------------------------------------- #
# registry navigation helpers
# --------------------------------------------------------------------------- #
def get_root(reg, domain_id):
    for r in reg["domains"] + reg["cross_domain_layers"]:
        if r["id"] == domain_id:
            return r
    raise KeyError(f"domain/layer not found: {domain_id}")


def get_capability(reg, domain_id, cap_id):
    for cap in get_root(reg, domain_id).get("capabilities", []):
        if cap["id"] == cap_id:
            return cap
    raise KeyError(f"capability not found: {domain_id}/{cap_id}")


def get_feature(reg, domain_id, cap_id, feat_id):
    for feat in get_capability(reg, domain_id, cap_id).get("features", []):
        if feat["id"] == feat_id:
            return feat
    raise KeyError(f"feature not found: {domain_id}/{cap_id}/{feat_id}")


def add_capability(reg, domain_id, cap):
    root = get_root(reg, domain_id)
    if any(c["id"] == cap["id"] for c in root["capabilities"]):
        return False
    root["capabilities"].append(cap)
    return True


def add_function(reg, domain_id, cap_id, feat_id, fn):
    feat = get_feature(reg, domain_id, cap_id, feat_id)
    if any(f["id"] == fn["id"] for f in feat["functions"]):
        return False
    feat["functions"].append(fn)
    return True


def add_alias(node, alias):
    """Insert `alias` into node['aliases'] right after evidence_refs (in place)."""
    existing = node.get("aliases", [])
    if alias in existing:
        return False
    new = {}
    inserted = False
    for k, v in node.items():
        if k == "aliases":
            continue  # will be re-placed deterministically
        new[k] = v
        if k == "evidence_refs":
            new["aliases"] = existing + [alias]
            inserted = True
    if not inserted:  # no evidence_refs (shouldn't happen) -> append at end
        new["aliases"] = existing + [alias]
    node.clear()
    node.update(new)
    return True


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #
def cap_parent(domain):
    return {"domain": domain}


def feat_parent(domain, cap):
    return {"domain": domain, "capability": cap}


def fn_parent(domain, cap, feat):
    return {"domain": domain, "capability": cap, "feature": feat}


def build_new_capabilities():
    """Return list of (domain_id, capability_node) for the 8 new capabilities."""
    out = []

    # 1. ai-automation / conversation-summaries
    out.append((
        "ai-automation",
        make_capability(
            "conversation-summaries", "Conversation Summaries", "Сводки разговоров",
            "AI-generated summaries of voice and text conversations.",
            "ai-automation",
            [make_feature(
                "ai-summary", "AI Summary", "AI-сводка",
                "Feature of the Conversation Summaries capability covering ai summary.",
                feat_parent("ai-automation", "conversation-summaries"),
                [make_function(
                    "generate-summary", "Generate Summary", "Сформировать сводку",
                    "Executes the AI Summary feature within the Conversation Summaries capability.",
                    "business", ["conversation_id", "summary_format"],
                    fn_parent("ai-automation", "conversation-summaries", "ai-summary"),
                    facets={"ai_assisted": True},
                )],
                facets={"ai_assisted": True},
            )],
            facets={"ai_assisted": True},
        ),
    ))

    # 2. analytics / real-time-reporting
    out.append((
        "analytics",
        make_capability(
            "real-time-reporting", "Real-Time Reporting", "Отчётность в реальном времени",
            "Operational dashboards and live key-performance reporting.",
            "analytics",
            [make_feature(
                "dashboard-view", "Dashboard View", "Представление дашборда",
                "Feature of the Real-Time Reporting capability covering dashboard view.",
                feat_parent("analytics", "real-time-reporting"),
                [make_function(
                    "select-dashboard-widget", "Select Dashboard Widget", "Выбрать виджет дашборда",
                    "Executes the Dashboard View feature within the Real-Time Reporting capability.",
                    "ui-action", ["widget_id", "layout_position"],
                    fn_parent("analytics", "real-time-reporting", "dashboard-view"),
                )],
            )],
        ),
    ))

    # 3. contact-center / interaction-routing  (two features)
    out.append((
        "contact-center",
        make_capability(
            "interaction-routing", "Interaction Routing", "Маршрутизация обращений",
            "Channel-agnostic routing of customer interactions across queues and agents.",
            "contact-center",
            [
                make_feature(
                    "queue-routing", "Queue Routing", "Маршрутизация по очередям",
                    "Feature of the Interaction Routing capability covering queue routing.",
                    feat_parent("contact-center", "interaction-routing"),
                    [make_function(
                        "assign-interaction-to-agent", "Assign Interaction To Agent",
                        "Назначить обращение оператору",
                        "Executes the Queue Routing feature within the Interaction Routing capability.",
                        "business", ["interaction_id", "agent_id"],
                        fn_parent("contact-center", "interaction-routing", "queue-routing"),
                    )],
                ),
                make_feature(
                    "routing-rules", "Routing Rules", "Правила маршрутизации",
                    "Feature of the Interaction Routing capability covering routing rules.",
                    feat_parent("contact-center", "interaction-routing"),
                    [make_function(
                        "configure-routing-rule", "Configure Routing Rule", "Настроить правило маршрутизации",
                        "Executes the Routing Rules feature within the Interaction Routing capability.",
                        "configuration", ["rule_id", "condition"],
                        fn_parent("contact-center", "interaction-routing", "routing-rules"),
                    )],
                ),
            ],
        ),
    ))

    # 4. contact-center / supervisor-workspace
    out.append((
        "contact-center",
        make_capability(
            "supervisor-workspace", "Supervisor Workspace", "Рабочее место супервизора",
            "Supervisor environment for live monitoring and agent coaching.",
            "contact-center",
            [make_feature(
                "live-monitoring", "Live Monitoring", "Мониторинг в реальном времени",
                "Feature of the Supervisor Workspace capability covering live monitoring.",
                feat_parent("contact-center", "supervisor-workspace"),
                [make_function(
                    "monitor-live-interactions", "Monitor Live Interactions",
                    "Наблюдать за активными обращениями",
                    "Executes the Live Monitoring feature within the Supervisor Workspace capability.",
                    "ui-action", ["queue_id", "refresh_interval"],
                    fn_parent("contact-center", "supervisor-workspace", "live-monitoring"),
                )],
            )],
        ),
    ))

    # 5. digital-channels / team-messaging
    out.append((
        "digital-channels",
        make_capability(
            "team-messaging", "Team Messaging", "Командные сообщения",
            "Internal team chat and collaboration alongside customer channels.",
            "digital-channels",
            [make_feature(
                "team-chat", "Team Chat", "Командный чат",
                "Feature of the Team Messaging capability covering team chat.",
                feat_parent("digital-channels", "team-messaging"),
                [make_function(
                    "post-team-message", "Post Team Message", "Отправить командное сообщение",
                    "Executes the Team Chat feature within the Team Messaging capability.",
                    "business", ["channel_id", "message_body"],
                    fn_parent("digital-channels", "team-messaging", "team-chat"),
                    facets=channel("text", "async", "outbound"),
                )],
            )],
        ),
    ))

    # 6. hardware / device-management
    out.append((
        "hardware",
        make_capability(
            "device-management", "Device Management", "Управление устройствами",
            "Provisioning, configuration, and lifecycle management of communication devices.",
            "hardware",
            [make_feature(
                "device-provisioning", "Device Provisioning", "Подготовка устройств",
                "Feature of the Device Management capability covering device provisioning.",
                feat_parent("hardware", "device-management"),
                [make_function(
                    "provision-device", "Provision Device", "Подготовить устройство",
                    "Executes the Device Provisioning feature within the Device Management capability.",
                    "configuration", ["device_id", "configuration_profile"],
                    fn_parent("hardware", "device-management", "device-provisioning"),
                )],
            )],
        ),
    ))

    # 7. security / access-control  (IAM capability, distinct from information-security/access-control feature)
    out.append((
        "security",
        make_capability(
            "access-control", "Access Control", "Контроль доступа",
            "Identity and access management: authentication, authorization, and role assignment.",
            "security",
            [make_feature(
                "role-management", "Role Management", "Управление ролями",
                "Feature of the Access Control capability covering role management.",
                feat_parent("security", "access-control"),
                [make_function(
                    "assign-role", "Assign Role", "Назначить роль",
                    "Executes the Role Management feature within the Access Control capability.",
                    "configuration", ["user_id", "role_id"],
                    fn_parent("security", "access-control", "role-management"),
                    facets={"security_compliance": True},
                )],
                facets={"security_compliance": True},
            )],
            facets={"security_compliance": True},
        ),
    ))

    # 8. voice-ucaas / call-routing  (PBX call routing per ADR-011)
    out.append((
        "voice-ucaas",
        make_capability(
            "call-routing", "Call Routing", "Маршрутизация вызовов",
            "Cloud-PBX routing of voice calls to extensions, groups, and external numbers.",
            "voice-ucaas",
            [make_feature(
                "inbound-routing", "Inbound Routing", "Маршрутизация входящих вызовов",
                "Feature of the Call Routing capability covering inbound routing.",
                feat_parent("voice-ucaas", "call-routing"),
                [make_function(
                    "route-inbound-call", "Route Inbound Call", "Маршрутизировать входящий вызов",
                    "Executes the Inbound Routing feature within the Call Routing capability.",
                    "business", ["call_id", "destination"],
                    fn_parent("voice-ucaas", "call-routing", "inbound-routing"),
                    facets=channel("voice", "sync", "inbound"),
                )],
                facets=channel("voice", "sync", "inbound"),
            )],
            facets=channel("voice", "sync", "inbound"),
        ),
    ))

    return out


def build_new_functions_under_existing():
    """Return list of (domain, cap, feat, function_node) added to existing features."""
    out = []
    # webhooks (alias: webhook-management)
    out.append((
        "platform", "open-api", "webhooks",
        make_function(
            "configure-webhook-endpoint", "Configure Webhook Endpoint", "Настроить эндпоинт вебхука",
            "Executes the Webhooks feature within the Open API capability.",
            "configuration", ["endpoint_url", "event_type", "secret"],
            fn_parent("platform", "open-api", "webhooks"),
        ),
    ))
    # outbound campaign
    out.append((
        "contact-center", "outbound-calling", "campaign-management",
        make_function(
            "start-campaign", "Start Campaign", "Запустить кампанию",
            "Executes the Campaign Management feature within the Outbound Calling capability.",
            "business", ["campaign_id"],
            fn_parent("contact-center", "outbound-calling", "campaign-management"),
            facets={**channel("voice", "sync", "outbound"), "commercial": True},
        ),
    ))
    # messenger send
    out.append((
        "digital-channels", "omnichannel-messaging", "messenger-integration",
        make_function(
            "send-message", "Send Message", "Отправить сообщение",
            "Executes the Messenger Integration feature within the Omnichannel Messaging capability.",
            "business", ["conversation_id", "message_body"],
            fn_parent("digital-channels", "omnichannel-messaging", "messenger-integration"),
            facets=channel("text", "async", "outbound"),
        ),
    ))
    # inbound voice receive
    out.append((
        "voice-ucaas", "voice-channel", "inbound-voice-call",
        make_function(
            "receive-inbound-call", "Receive Inbound Call", "Принять входящий вызов",
            "Executes the Inbound Voice Call feature within the Voice Channel capability.",
            "business", ["call_id"],
            fn_parent("voice-ucaas", "voice-channel", "inbound-voice-call"),
            facets=channel("voice", "sync", "inbound"),
        ),
    ))
    return out


def main() -> int:
    orig = REGISTRY.read_text(encoding="utf-8")
    reg = json.loads(orig)

    # round-trip guard: refuse to proceed if serialization isn't stable
    if json.dumps(reg, ensure_ascii=False, indent=2) + "\n" != orig:
        raise SystemExit("ABORT: registry does not round-trip; manual review needed")

    added = {"capabilities": 0, "features": 0, "functions": 0, "aliases": 0}

    for domain_id, cap in build_new_capabilities():
        if add_capability(reg, domain_id, cap):
            added["capabilities"] += 1
            added["features"] += len(cap["features"])
            added["functions"] += sum(len(f["functions"]) for f in cap["features"])

    for domain_id, cap_id, feat_id, fn in build_new_functions_under_existing():
        if add_function(reg, domain_id, cap_id, feat_id, fn):
            added["functions"] += 1

    # aliases on existing canonical nodes
    if add_alias(get_capability(reg, "platform", "cpaas"), "communications-apis"):
        added["aliases"] += 1
    if add_alias(get_feature(reg, "platform", "open-api", "webhooks"), "webhook-management"):
        added["aliases"] += 1

    # version bump (additive == MINOR, §10.4)
    reg["version"] = "1.1.0"

    # source entry
    if not any(s["id"] == "issue-168-industry-inventory" for s in reg["sources"]):
        reg["sources"].append({
            "id": "issue-168-industry-inventory",
            "path": "docs/analysis/2026-06-21-industry-inventory.md",
            "role": "cascade-fill change request and per-entity industry justification",
        })

    # registry note
    note = (
        "Issue #168 cascade-fill nodes (source_status=issue-168-cascade-fill) "
        "complete every external Mango industry_ref to a resolvable parent-chain; "
        "communications-apis and webhook-management are modeled as aliases of "
        "cpaas and webhooks rather than as duplicate nodes."
    )
    if note not in reg["registry_notes"]:
        reg["registry_notes"].append(note)

    REGISTRY.write_text(json.dumps(reg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("Added:", json.dumps(added))
    print("New version:", reg["version"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
