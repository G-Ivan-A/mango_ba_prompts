#!/usr/bin/env python3
"""Generate the issue #160 Mango Taxonomy registry artifacts.

The committed registry files intentionally use a JSON-compatible YAML subset so
the lightweight CI validator can stay stdlib-only.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "kb" / "mango-taxonomy"

PRODUCTS_URL = "https://www.mango-office.ru/products/"
VATS_URL = "https://www.mango-office.ru/products/virtualnaya_ats/"
CC_URL = "https://www.mango-office.ru/products/contact-center/"
CC_FEATURES_URL = "https://www.mango-office.ru/products/contact-center/vozmozhnosti/"
CALLTRACKING_URL = "https://www.mango-office.ru/products/calltracking/"
SPEECH_URL = "https://www.mango-office.ru/products/virtualnaya_ats/vozmozhnosti/speech-analytics/"
ROBOT_URL = "https://www.mango-office.ru/products/contact-center/ai/voice-robot/"
TALKER_URL = "https://www.mango-office.ru/products/mango-talker/"
INTEGRATIONS_URL = "https://www.mango-office.ru/products/integraciya/"
DEVICES_URL = "https://www.mango-office.ru/shop/devices/"

LK_INDEX = "kb/mango-product-docs/processed/mango-lk-manual/index.md"
LK_IVR = "kb/mango-product-docs/processed/mango-lk-manual/sections/104-golosovoe-menyu-i-raspredelenie-zvonkov.md"
LK_LINES = "kb/mango-product-docs/processed/mango-lk-manual/sections/105-nastroyki-dlya-vhodyaschih-liniy.md"
LK_NUMBERS = "kb/mango-product-docs/processed/mango-lk-manual/sections/100-nomera-podklyuchennye-k-ats.md"
LK_EMPLOYEES = "kb/mango-product-docs/processed/mango-lk-manual/sections/111-sotrudniki-i-gruppy.md"
LK_GROUPS = "kb/mango-product-docs/processed/mango-lk-manual/sections/118-rabota-s-gruppami.md"
LK_RECORDING = "kb/mango-product-docs/processed/mango-lk-manual/sections/134-zapis-razgovorov.md"
LK_RECORDINGS = "kb/mango-product-docs/processed/mango-lk-manual/sections/135-zapisannye-razgovory.md"
LK_TEXT = "kb/mango-product-docs/processed/mango-lk-manual/sections/179-tekstovye-kommunikacii.md"
LK_CHAT = "kb/mango-product-docs/processed/mango-lk-manual/sections/189-chat-na-sayte.md"
LK_WHATSAPP = "kb/mango-product-docs/processed/mango-lk-manual/sections/191-whatsapp.md"
LK_TELEGRAM = "kb/mango-product-docs/processed/mango-lk-manual/sections/192-telegram.md"
LK_ANALYTICS = "kb/mango-product-docs/processed/mango-lk-manual/sections/148-analitika.md"
LK_WALLBOARD = "kb/mango-product-docs/processed/mango-lk-manual/sections/234-wallboard.md"
LK_ROLES = "kb/mango-product-docs/processed/mango-lk-manual/sections/286-nastroyka-prav-dostupa-roli.md"
LK_SECURITY = "kb/mango-product-docs/processed/mango-lk-manual/sections/289-bezopasnost-pro.md"

CC_INDEX = "kb/mango-product-docs/processed/mango-cc-manual/index.md"
CC_AGENT_STATUS = "kb/mango-product-docs/processed/mango-cc-manual/sections/05-upravlenie-statusom.md"
CC_QUEUE = "kb/mango-product-docs/processed/mango-cc-manual/sections/07-ochered-obrascheniy.md"
CC_OUTBOUND = "kb/mango-product-docs/processed/mango-cc-manual/sections/46-sovershenie-ishodyaschih-vyzovov.md"
CC_ROUTING = "kb/mango-product-docs/processed/mango-cc-manual/sections/64-avtomaticheskoe-raspredelenie-obrascheni.md"
CC_CAMPAIGNS = "kb/mango-product-docs/processed/mango-cc-manual/sections/123-ishodyaschiy-obzvon.md"
CC_ADD_CAMPAIGN = "kb/mango-product-docs/processed/mango-cc-manual/sections/127-dobavlenie-kampanii.md"
CC_DASHBOARD = "kb/mango-product-docs/processed/mango-cc-manual/sections/57-dashboard.md"
CC_WIDGET = "kb/mango-product-docs/processed/mango-cc-manual/sections/58-sozdanie-i-nastroyka-vidzheta.md"
CC_WFM = "kb/mango-product-docs/processed/mango-cc-manual/sections/100-planirovanie-vhodyaschih.md"
CC_SPEECH = "kb/mango-product-docs/processed/mango-cc-manual/sections/178-rechevaya-analitika.md"
CC_CHECKLIST = "kb/mango-product-docs/processed/mango-cc-manual/sections/184-konstruktor-chek-listov.md"
CC_ROLES = "kb/mango-product-docs/processed/mango-cc-manual/sections/217-prilozhenie-1-upravlenie-pravami-dostupa.md"

TALKER_INDEX = "kb/mango-product-docs/processed/mtalker/android-user-guide/index.md"
TALKER_CALL = "kb/mango-product-docs/processed/mtalker/android-user-guide/sections/11-zvonok-sotrudniku.md"
TALKER_ANSWER = "kb/mango-product-docs/processed/mtalker/android-user-guide/sections/15-kak-prinyat-vhodyaschiy-zvonok.md"
TALKER_CHAT = "kb/mango-product-docs/processed/mtalker/android-user-guide/sections/17-otpravka-soobscheniya-v-chat.md"
TALKER_CHANNEL = "kb/mango-product-docs/processed/mtalker/android-user-guide/sections/47-sozdanie-novogo-chata-ili-kanala.md"
TALKER_VIDEO = "kb/mango-product-docs/processed/mtalker/android-user-guide/sections/14-kak-nachat-gruppovoy-videozvonok.md"
TALKER_CONFERENCE = "kb/mango-product-docs/processed/mtalker/android-user-guide/sections/42-kak-prisoedinitsya-k-konferencii-po-ssyl.md"
TALKER_CONTACT = "kb/mango-product-docs/processed/mtalker/android-user-guide/sections/97-opisanie-kartochki-kontakta.md"
TALKER_HISTORY = "kb/mango-product-docs/processed/mtalker/android-user-guide/sections/78-opisanie-zhurnala-vyzovov.md"

VPBX_API_INDEX = "kb/mango-product-docs/processed/vpbx-api/index.md"
VPBX_API_CALL = "kb/mango-product-docs/processed/vpbx-api/sections/246-iniciirovanie-ishodyaschego-vyzova.md"
VPBX_API_ROUTE = "kb/mango-product-docs/processed/vpbx-api/sections/42-marshrutizaciya-vyzova.md"
VPBX_API_WEBHOOK = "kb/mango-product-docs/processed/vpbx-api/sections/245-uvedomlenie-o-vyzove.md"
VPBX_API_SMS = "kb/mango-product-docs/processed/vpbx-api/sections/39-otpravka-sms.md"
VPBX_API_RECORD = "kb/mango-product-docs/processed/vpbx-api/sections/40-vklyuchenie-zapisi-razgovora.md"
VPBX_API_STATS = "kb/mango-product-docs/processed/vpbx-api/sections/58-poluchenie-statistiki-vyzovov.md"
VPBX_API_CC_TASK = "kb/mango-product-docs/processed/vpbx-api/sections/157-sozdanie-zadachi-na-avtoperezvon.md"
VPBX_API_CC_EVENT = "kb/mango-product-docs/processed/vpbx-api/sections/215-sobytiya.md"
VPBX_API_DIALOG_SEND = "kb/mango-product-docs/processed/vpbx-api/sections/238-otpravka-soobscheniya.md"
VPBX_API_DIALOG_EVENT = "kb/mango-product-docs/processed/vpbx-api/sections/239-opoveschenie-o-tom-chto-polzovatel-nabir.md"

MDIALOGI_API_INDEX = "kb/mango-product-docs/processed/mdialogi-api/index.md"
BITRIX_INDEX = "kb/mango-product-docs/processed/integration-bitrix24/index.md"
ONE_C_INDEX = "kb/mango-product-docs/processed/integration_1c/index.md"
AMOCRM_INDEX = "kb/mango-product-docs/processed/integration_amocrm/index.md"
SSO_INDEX = "kb/mango-product-docs/processed/lk-vats-sso/index.md"
ROLE_MODEL_INDEX = "kb/mango-product-docs/processed/Rolevaya-model-vats/index.md"
QUALITY_INDEX = "kb/mango-product-docs/processed/quality-managment/index.md"
SPEECH_INDEX = "kb/mango-product-docs/processed/speech-analytics/index.md"
WALLBOARD_INDEX = "kb/mango-product-docs/processed/wallboard/index.md"
SIP_TRUNK_INDEX = "kb/mango-product-docs/processed/sip-trunk/index.md"


def channel(kind: str, sync: str, direction: str) -> dict[str, Any]:
    return {
        "channel": {
            "channel_kind": kind,
            "synchronicity": sync,
            "direction": direction,
        }
    }


def gap(level: str, proposed_id: str, reason: str) -> dict[str, Any]:
    return {"missing_level": level, "proposed_id": proposed_id, "reason": reason}


def align(
    domain: str,
    capability: str | None = None,
    feature: str | None = None,
    function: str | None = None,
    *,
    alignment_type: str = "primary",
    evidence_refs: list[str] | None = None,
    facets: dict[str, Any] | None = None,
    mapping_gap: dict[str, Any] | None = None,
    supporting_only_reason: str | None = None,
) -> dict[str, Any]:
    industry_ref: dict[str, str] = {"domain": domain}
    if capability:
        industry_ref["capability"] = capability
    if feature:
        industry_ref["feature"] = feature
    if function:
        industry_ref["function"] = function
    item: dict[str, Any] = {
        "alignment_type": alignment_type,
        "industry_ref": industry_ref,
        "evidence_refs": evidence_refs or [],
    }
    if facets:
        item["facets"] = facets
    if mapping_gap:
        item["mapping_gap"] = mapping_gap
    if supporting_only_reason:
        item["supporting_only_reason"] = supporting_only_reason
    return item


def with_evidence(alignments: list[dict[str, Any]], evidence_refs: list[str]) -> list[dict[str, Any]]:
    result = []
    for item in alignments:
        clone = dict(item)
        if not clone.get("evidence_refs"):
            clone["evidence_refs"] = evidence_refs
        result.append(clone)
    return result


def entity(
    entity_id: str,
    level: str,
    name_ru: str,
    description: str,
    evidence_refs: list[str],
    alignments: list[dict[str, Any]],
    **extra: Any,
) -> dict[str, Any]:
    item: dict[str, Any] = {
        "id": entity_id,
        "level": level,
        "name_ru": name_ru,
        "description": description,
        "lifecycle_status": "active",
        "evidence_refs": evidence_refs,
        "maps_to": {"industry_alignment": with_evidence(alignments, evidence_refs)},
    }
    item.update(extra)
    return item


official_products = [
    entity(
        "mango-virtual-pbx-official",
        "official-product",
        "Виртуальная АТС",
        "Публичный продукт Mango Office для облачной офисной телефонии, маршрутизации звонков и управления номерами.",
        [VATS_URL, LK_INDEX],
        [align("voice-ucaas", "cloud-pbx")],
        aliases=["ВАТС", "Virtual PBX", "Облачная АТС"],
        owner="Mango Office",
        official_urls=[VATS_URL],
        supported_by_services=[
            "vats-inbound-routing-service",
            "vats-ivr-service",
            "vats-number-management-service",
            "vats-recording-history-service",
        ],
    ),
    entity(
        "mango-sip-trunk-official",
        "official-product",
        "SIP Trunk и гибридная телефония",
        "Публичный набор возможностей подключения внешней телефонии и SIP-инфраструктуры к Виртуальной АТС.",
        [PRODUCTS_URL, SIP_TRUNK_INDEX],
        [align("voice-ucaas", "sip-connectivity")],
        aliases=["SIP Trunk", "Гибридная АТС"],
        owner="Mango Office",
        official_urls=[PRODUCTS_URL],
        supported_by_services=["vats-number-management-service", "vpbx-open-api-service"],
    ),
    entity(
        "mango-contact-center-official",
        "official-product",
        "Контакт-центр",
        "Публичный продукт для обработки обращений, рабочих мест операторов, очередей и супервизорского контроля.",
        [CC_URL, CC_INDEX],
        [align("contact-center", "omnichannel-contact-center")],
        aliases=["КЦ", "Contact Center"],
        owner="Mango Office",
        official_urls=[CC_URL, CC_FEATURES_URL],
        supported_by_services=[
            "cc-agent-workspace-service",
            "cc-interaction-routing-service",
            "cc-outbound-campaign-service",
            "cc-supervisor-wfm-service",
            "quality-checklist-service",
        ],
    ),
    entity(
        "mango-text-communications-official",
        "official-product",
        "Текстовые коммуникации",
        "Публичный продуктовый слой для сайта, мессенджеров, шаблонов и цифровых диалогов.",
        [PRODUCTS_URL, LK_TEXT],
        [align("digital-channels", "omnichannel-messaging", facets=channel("text", "async", "inbound"))],
        aliases=["Текстовые коммуникации", "Digital channels"],
        owner="Mango Office",
        official_urls=[PRODUCTS_URL],
        supported_by_services=[
            "digital-channel-group-service",
            "website-chat-service",
            "messenger-channel-service",
            "dialog-api-messaging-service",
        ],
    ),
    entity(
        "mango-calltracking-official",
        "official-product",
        "Коллтрекинг и маркетинговая аналитика",
        "Публичный продукт для привязки звонков к рекламным источникам и оценки эффективности маркетинга.",
        [CALLTRACKING_URL, LK_ANALYTICS],
        [align("analytics", "call-tracking")],
        aliases=["Calltracking", "Коллтрекинг", "Сквозная аналитика"],
        owner="Mango Office",
        official_urls=[CALLTRACKING_URL],
        supported_by_services=[
            "calltracking-attribution-service",
            "end-to-end-analytics-service",
            "reporting-dashboard-service",
        ],
    ),
    entity(
        "mango-speech-analytics-official",
        "official-product",
        "Речевая аналитика",
        "Публичный AI-продукт для распознавания и анализа разговоров.",
        [SPEECH_URL, SPEECH_INDEX, CC_SPEECH],
        [align("ai-automation", "speech-analytics", facets={"ai_assisted": True})],
        aliases=["Speech Analytics", "Речевая аналитика"],
        owner="Mango Office",
        official_urls=[SPEECH_URL],
        supported_by_services=[
            "speech-analytics-service",
            "conversation-summary-service",
            "quality-checklist-service",
        ],
    ),
    entity(
        "mango-robots-official",
        "official-product",
        "Роботы",
        "Публичный AI-продукт для автоматизированных голосовых сценариев и диалогов.",
        [ROBOT_URL, PRODUCTS_URL],
        [align("ai-automation", "voice-bot", facets={"ai_assisted": True, **channel("voice", "sync", "outbound")})],
        aliases=["Голосовые роботы", "Voice Robot"],
        owner="Mango Office",
        official_urls=[ROBOT_URL],
        supported_by_services=["voice-robot-service"],
    ),
    entity(
        "mango-talker-official",
        "official-product",
        "Mango Talker",
        "Публичный продукт корпоративных звонков, чатов, видеозвонков и контактной истории.",
        [TALKER_URL, TALKER_INDEX],
        [align("voice-ucaas", "unified-communications")],
        aliases=["Mango Talker", "MTalker"],
        owner="Mango Office",
        official_urls=[TALKER_URL],
        supported_by_services=[
            "talker-softphone-service",
            "talker-team-chat-service",
            "talker-video-meeting-service",
            "talker-contact-history-service",
        ],
    ),
    entity(
        "mango-integrations-official",
        "official-product",
        "Интеграции",
        "Публичный продуктовый слой интеграций Mango Office с CRM, ERP, API и webhooks.",
        [INTEGRATIONS_URL, BITRIX_INDEX, ONE_C_INDEX, AMOCRM_INDEX],
        [align("platform", "platform-integration")],
        aliases=["Интеграции", "CRM integrations"],
        owner="Mango Office",
        official_urls=[INTEGRATIONS_URL],
        supported_by_services=[
            "vpbx-open-api-service",
            "contact-center-api-service",
            "crm-erp-integration-service",
            "webhook-event-service",
        ],
    ),
    entity(
        "mango-numbers-equipment-official",
        "official-product",
        "Номера и оборудование",
        "Публичный продуктовый слой подключения номеров, устройств и телефонной инфраструктуры.",
        [DEVICES_URL, LK_NUMBERS],
        [align("hardware", "device-management")],
        aliases=["Оборудование", "Номера", "Devices"],
        owner="Mango Office",
        official_urls=[DEVICES_URL],
        supported_by_services=["vats-number-management-service"],
    ),
]


product_specs = [
    {
        "id": "mango-virtual-pbx",
        "name": "Mango Virtual PBX",
        "description": "Внутренний продуктовый кластер Виртуальной АТС: входящие сценарии, IVR, номера и записи разговоров.",
        "official_refs": ["mango-virtual-pbx-official", "mango-sip-trunk-official", "mango-numbers-equipment-official"],
        "services": [
            "vats-inbound-routing-service",
            "vats-ivr-service",
            "vats-number-management-service",
            "vats-recording-history-service",
        ],
        "evidence": [VATS_URL, LK_INDEX],
        "alignments": [align("voice-ucaas", "cloud-pbx")],
    },
    {
        "id": "mango-contact-center",
        "name": "Mango Contact Center",
        "description": "Внутренний продуктовый кластер Контакт-центра: операторские рабочие места, очереди, кампании и WFM.",
        "official_refs": ["mango-contact-center-official"],
        "services": [
            "cc-agent-workspace-service",
            "cc-interaction-routing-service",
            "cc-outbound-campaign-service",
            "cc-supervisor-wfm-service",
        ],
        "evidence": [CC_URL, CC_INDEX],
        "alignments": [align("contact-center", "omnichannel-contact-center")],
    },
    {
        "id": "mango-digital-communications",
        "name": "Mango Digital Communications",
        "description": "Внутренний продуктовый кластер текстовых каналов, чата на сайте, мессенджеров и Dialog API.",
        "official_refs": ["mango-text-communications-official"],
        "services": [
            "digital-channel-group-service",
            "website-chat-service",
            "messenger-channel-service",
            "dialog-api-messaging-service",
        ],
        "evidence": [PRODUCTS_URL, LK_TEXT, MDIALOGI_API_INDEX],
        "alignments": [align("digital-channels", "omnichannel-messaging", facets=channel("text", "async", "inbound"))],
    },
    {
        "id": "mango-talker",
        "name": "Mango Talker",
        "description": "Внутренний продуктовый кластер приложения Mango Talker: софтфон, командные чаты, видео и контакты.",
        "official_refs": ["mango-talker-official"],
        "services": [
            "talker-softphone-service",
            "talker-team-chat-service",
            "talker-video-meeting-service",
            "talker-contact-history-service",
        ],
        "evidence": [TALKER_URL, TALKER_INDEX],
        "alignments": [align("voice-ucaas", "unified-communications")],
    },
    {
        "id": "mango-ai-speech-quality",
        "name": "Mango AI Speech and Quality",
        "description": "Внутренний продуктовый кластер AI, речевой аналитики, конспектов, чек-листов качества и голосовых роботов.",
        "official_refs": ["mango-speech-analytics-official", "mango-robots-official"],
        "services": [
            "speech-analytics-service",
            "conversation-summary-service",
            "quality-checklist-service",
            "voice-robot-service",
        ],
        "evidence": [SPEECH_URL, SPEECH_INDEX, QUALITY_INDEX],
        "alignments": [align("ai-automation", "speech-analytics", facets={"ai_assisted": True})],
    },
    {
        "id": "mango-marketing-analytics",
        "name": "Mango Marketing Analytics",
        "description": "Внутренний продуктовый кластер коллтрекинга, сквозной аналитики, отчётов и real-time панелей.",
        "official_refs": ["mango-calltracking-official"],
        "services": [
            "calltracking-attribution-service",
            "end-to-end-analytics-service",
            "reporting-dashboard-service",
            "wallboard-monitoring-service",
        ],
        "evidence": [CALLTRACKING_URL, LK_ANALYTICS, WALLBOARD_INDEX],
        "alignments": [align("analytics", "call-tracking")],
    },
    {
        "id": "mango-platform-integrations",
        "name": "Mango Platform Integrations",
        "description": "Внутренний продуктовый кластер API, webhooks и CRM/ERP-интеграций.",
        "official_refs": ["mango-integrations-official"],
        "services": [
            "vpbx-open-api-service",
            "contact-center-api-service",
            "crm-erp-integration-service",
            "webhook-event-service",
        ],
        "evidence": [INTEGRATIONS_URL, VPBX_API_INDEX, BITRIX_INDEX],
        "alignments": [align("platform", "open-api")],
    },
    {
        "id": "mango-security-access",
        "name": "Mango Security and Access",
        "description": "Внутренний cross-product кластер ролей, SSO, доступа к записям и аудита безопасности.",
        "internal_only_reason": "Кластер выделен как внутренний слой поверх публичных продуктов, потому что права доступа и безопасность обслуживают несколько продуктовых линий.",
        "services": [
            "role-access-management-service",
            "sso-identity-service",
            "recording-access-security-service",
            "security-audit-settings-service",
        ],
        "evidence": [ROLE_MODEL_INDEX, SSO_INDEX, LK_SECURITY],
        "alignments": [align("security", "access-control")],
    },
]


service_specs = [
    {
        "id": "vats-inbound-routing-service",
        "product": "mango-virtual-pbx",
        "cluster": "vats-core",
        "name": "Входящая маршрутизация ВАТС",
        "description": "Сервис входящих схем, правил и распределения голосовых вызовов.",
        "module": ("vats-inbound-scenarios-module", "Сценарии входящих звонков"),
        "evidence": [LK_IVR, LK_LINES, VPBX_API_ROUTE],
        "alignments": [align("voice-ucaas", "call-routing", facets=channel("voice", "sync", "inbound"))],
        "functions": [
            ("receive-inbound-call-through-scenario", "Принять входящий звонок по сценарию", "business", "system-rule", [align("voice-ucaas", "voice-channel", "inbound-voice-call", "receive-inbound-call", facets=channel("voice", "sync", "inbound"))], LK_LINES),
            ("configure-inbound-call-scenario", "Настроить сценарий входящего звонка", "configuration", "admin-ui", [align("voice-ucaas", "call-routing", facets=channel("voice", "sync", "inbound"), mapping_gap=gap("feature", "inbound-call-scenario", "Industry Taxonomy фиксирует capability call-routing, но не выделяет сценарии ВАТС как feature."))], LK_IVR),
        ],
    },
    {
        "id": "vats-ivr-service",
        "product": "mango-virtual-pbx",
        "cluster": "vats-core",
        "name": "Голосовое меню ВАТС",
        "description": "Сервис IVR-меню, приветствий и ветвления входящих звонков.",
        "module": ("vats-ivr-menu-module", "Голосовое меню"),
        "evidence": [LK_IVR],
        "alignments": [align("voice-ucaas", "ivr-voice-menu", facets=channel("voice", "sync", "inbound"))],
        "functions": [
            ("play-ivr-menu-to-caller", "Проиграть голосовое меню звонящему", "business", "system-rule", [align("voice-ucaas", "ivr-voice-menu", facets=channel("voice", "sync", "inbound"), mapping_gap=gap("function", "play-ivr-menu", "Industry Taxonomy не содержит leaf-функцию проигрывания IVR."))], LK_IVR),
            ("edit-ivr-menu-branch", "Изменить ветку голосового меню", "configuration", "admin-ui", [align("voice-ucaas", "ivr-voice-menu", facets=channel("voice", "sync", "inbound"), mapping_gap=gap("function", "edit-ivr-branch", "Industry Taxonomy не содержит leaf-функцию редактирования веток IVR."))], LK_IVR),
        ],
    },
    {
        "id": "vats-number-management-service",
        "product": "mango-virtual-pbx",
        "cluster": "vats-core",
        "name": "Управление номерами ВАТС",
        "description": "Сервис подключённых номеров, входящих линий и SIP-инфраструктуры.",
        "module": ("vats-connected-numbers-module", "Подключённые номера"),
        "evidence": [LK_NUMBERS, SIP_TRUNK_INDEX],
        "alignments": [align("voice-ucaas", "number-management")],
        "functions": [
            ("assign-connected-number-route", "Назначить маршрут подключённому номеру", "configuration", "admin-ui", [align("voice-ucaas", "number-management", mapping_gap=gap("function", "assign-number-route", "Industry Taxonomy не содержит leaf-функцию назначения маршрута номеру."))], LK_NUMBERS),
            ("view-connected-number-list", "Открыть список подключённых номеров", "ui-action", "admin-ui", [align("voice-ucaas", "number-management", mapping_gap=gap("function", "view-number-list", "Industry Taxonomy не содержит UI leaf-функцию просмотра списка номеров."))], LK_NUMBERS),
        ],
    },
    {
        "id": "vats-recording-history-service",
        "product": "mango-virtual-pbx",
        "cluster": "vats-core",
        "name": "Записи и история звонков ВАТС",
        "description": "Сервис записи разговоров, журнала вызовов и доступа к сохранённым разговорам.",
        "module": ("vats-call-recording-module", "Запись разговоров"),
        "evidence": [LK_RECORDING, LK_RECORDINGS, VPBX_API_RECORD],
        "alignments": [align("voice-ucaas", "call-recording", facets=channel("voice", "sync", "inbound"))],
        "functions": [
            ("enable-call-recording-rule", "Включить правило записи разговора", "configuration", "admin-ui", [align("voice-ucaas", "call-recording", facets=channel("voice", "sync", "inbound"), mapping_gap=gap("function", "enable-call-recording-rule", "Industry Taxonomy не содержит leaf-функцию включения правила записи."))], LK_RECORDING),
            ("play-call-recording", "Прослушать запись разговора", "ui-action", "admin-ui", [align("voice-ucaas", "call-recording", facets=channel("voice", "sync", "inbound"), mapping_gap=gap("function", "play-call-recording", "Industry Taxonomy не содержит UI leaf-функцию прослушивания записи."))], LK_RECORDINGS),
        ],
    },
    {
        "id": "cc-agent-workspace-service",
        "product": "mango-contact-center",
        "cluster": "contact-center-core",
        "name": "Рабочее место оператора КЦ",
        "description": "Сервис операторского интерфейса для звонков, статусов и обработки обращений.",
        "module": ("cc-agent-call-handling-module", "Обработка обращений оператором"),
        "evidence": [CC_AGENT_STATUS, CC_QUEUE, CC_OUTBOUND],
        "alignments": [align("contact-center", "agent-workspace")],
        "functions": [
            ("accept-queue-interaction", "Принять обращение из очереди", "business", "operator-ui", [align("contact-center", "agent-workspace", mapping_gap=gap("function", "accept-queue-interaction", "Industry Taxonomy не содержит leaf-функцию принятия обращения оператором."))], CC_QUEUE),
            ("set-agent-status", "Изменить статус оператора", "ui-action", "operator-ui", [align("contact-center", "agent-workspace", mapping_gap=gap("function", "set-agent-status", "Industry Taxonomy не содержит UI leaf-функцию смены статуса оператора."))], CC_AGENT_STATUS),
        ],
    },
    {
        "id": "cc-interaction-routing-service",
        "product": "mango-contact-center",
        "cluster": "contact-center-core",
        "name": "Маршрутизация обращений КЦ",
        "description": "Сервис очередей, автоматического распределения и правил маршрутизации обращений.",
        "module": ("cc-queue-routing-module", "Очереди и правила распределения"),
        "evidence": [CC_QUEUE, CC_ROUTING],
        "alignments": [align("contact-center", "interaction-routing", "queue-routing")],
        "functions": [
            ("route-interaction-to-queue", "Распределить обращение в очередь", "business", "system-rule", [align("contact-center", "interaction-routing", "queue-routing", mapping_gap=gap("function", "route-interaction-to-queue", "Industry Taxonomy фиксирует queue-routing, но не содержит leaf-функцию распределения обращения."))], CC_ROUTING),
            ("configure-queue-routing-rule", "Настроить правило очереди", "configuration", "admin-ui", [align("contact-center", "interaction-routing", "routing-rules", mapping_gap=gap("function", "configure-queue-routing-rule", "Industry Taxonomy фиксирует routing-rules, но не содержит leaf-функцию настройки правила."))], CC_ROUTING),
        ],
    },
    {
        "id": "cc-outbound-campaign-service",
        "product": "mango-contact-center",
        "cluster": "contact-center-core",
        "name": "Исходящие кампании КЦ",
        "description": "Сервис кампаний исходящего обзвона, карточек кампаний и запуска задач.",
        "module": ("cc-outbound-campaign-module", "Кампании исходящего обзвона"),
        "evidence": [CC_CAMPAIGNS, CC_ADD_CAMPAIGN],
        "alignments": [align("contact-center", "outbound-calling", "campaign-management")],
        "functions": [
            ("start-outbound-campaign", "Запустить исходящую кампанию", "business", "operator-ui", [align("contact-center", "outbound-calling", "campaign-management", "start-campaign", facets=channel("voice", "sync", "outbound"))], CC_CAMPAIGNS),
            ("configure-outbound-campaign", "Настроить исходящую кампанию", "configuration", "admin-ui", [align("contact-center", "outbound-calling", "campaign-management", mapping_gap=gap("function", "configure-outbound-campaign", "Industry Taxonomy содержит start-campaign, но не содержит отдельную функцию конфигурации кампании."))], CC_ADD_CAMPAIGN),
        ],
    },
    {
        "id": "cc-supervisor-wfm-service",
        "product": "mango-contact-center",
        "cluster": "contact-center-core",
        "name": "Супервизорский контроль и WFM",
        "description": "Сервис супервизорских панелей, графиков и планирования нагрузки.",
        "module": ("cc-supervisor-wfm-module", "Планирование и супервизорский мониторинг"),
        "evidence": [CC_DASHBOARD, CC_WFM, CC_WIDGET],
        "alignments": [align("contact-center", "workforce-management"), align("contact-center", "supervisor-workspace", alignment_type="secondary")],
        "functions": [
            ("monitor-agent-workload", "Просмотреть нагрузку операторов", "ui-action", "operator-ui", [align("contact-center", "supervisor-workspace", mapping_gap=gap("function", "monitor-agent-workload", "Industry Taxonomy не содержит UI leaf-функцию просмотра нагрузки операторов."))], CC_DASHBOARD),
            ("configure-workforce-schedule", "Настроить график входящих обращений", "configuration", "admin-ui", [align("contact-center", "workforce-management", mapping_gap=gap("function", "configure-workforce-schedule", "Industry Taxonomy не содержит leaf-функцию настройки графика WFM."))], CC_WFM),
        ],
    },
    {
        "id": "digital-channel-group-service",
        "product": "mango-digital-communications",
        "cluster": "digital-channels",
        "name": "Группы текстовых каналов",
        "description": "Сервис объединения цифровых каналов, расписаний и правил обработки диалогов.",
        "module": ("digital-channel-group-module", "Группы каналов коммуникации"),
        "evidence": [LK_TEXT, LK_WHATSAPP, LK_TELEGRAM],
        "alignments": [align("digital-channels", "omnichannel-messaging", facets=channel("text", "async", "inbound"))],
        "functions": [
            ("send-channel-message", "Отправить сообщение в цифровом канале", "business", "operator-ui", [align("digital-channels", "omnichannel-messaging", "messenger-integration", "send-message", facets=channel("text", "async", "outbound"))], LK_TEXT),
            ("configure-channel-group", "Настроить группу каналов", "configuration", "admin-ui", [align("digital-channels", "omnichannel-messaging", facets=channel("text", "async", "inbound"), mapping_gap=gap("function", "configure-channel-group", "Industry Taxonomy не содержит leaf-функцию настройки группы каналов."))], LK_TEXT),
        ],
    },
    {
        "id": "website-chat-service",
        "product": "mango-digital-communications",
        "cluster": "digital-channels",
        "name": "Чат на сайте",
        "description": "Сервис виджета сайта, кода установки и обработки входящих чат-диалогов.",
        "module": ("website-chat-widget-module", "Виджет чата на сайте"),
        "evidence": [LK_CHAT],
        "alignments": [align("digital-channels", "website-chat", facets=channel("text", "async", "inbound"))],
        "functions": [
            ("receive-website-chat", "Принять обращение из чата сайта", "business", "operator-ui", [align("digital-channels", "website-chat", facets=channel("text", "async", "inbound"), mapping_gap=gap("function", "receive-website-chat", "Industry Taxonomy не содержит leaf-функцию приёма обращения из сайта."))], LK_CHAT),
            ("install-website-chat-widget", "Установить код виджета чата", "configuration", "admin-ui", [align("digital-channels", "website-chat", mapping_gap=gap("function", "install-website-chat-widget", "Industry Taxonomy не содержит leaf-функцию установки виджета сайта."))], LK_CHAT),
        ],
    },
    {
        "id": "messenger-channel-service",
        "product": "mango-digital-communications",
        "cluster": "digital-channels",
        "name": "Мессенджер-каналы",
        "description": "Сервис подключения Telegram, WhatsApp и других мессенджеров к группам каналов.",
        "module": ("messenger-channel-connector-module", "Подключение мессенджеров"),
        "evidence": [LK_WHATSAPP, LK_TELEGRAM],
        "alignments": [align("digital-channels", "omnichannel-messaging", "messenger-integration", facets=channel("text", "async", "inbound"))],
        "functions": [
            ("connect-telegram-channel", "Подключить Telegram-канал", "configuration", "admin-ui", [align("digital-channels", "omnichannel-messaging", "messenger-integration", facets=channel("text", "async", "inbound"), mapping_gap=gap("function", "connect-telegram-channel", "Industry Taxonomy не содержит leaf-функцию подключения конкретного мессенджера."))], LK_TELEGRAM),
            ("reply-to-messenger-dialog", "Ответить в диалоге мессенджера", "business", "operator-ui", [align("digital-channels", "omnichannel-messaging", "messenger-integration", "send-message", facets=channel("text", "async", "outbound"))], LK_WHATSAPP),
        ],
    },
    {
        "id": "dialog-api-messaging-service",
        "product": "mango-digital-communications",
        "cluster": "digital-channels",
        "name": "Dialog API",
        "description": "Сервис программного обмена сообщениями и событиями цифровых диалогов.",
        "module": ("dialog-api-message-module", "API сообщений Dialogi"),
        "evidence": [MDIALOGI_API_INDEX, VPBX_API_DIALOG_SEND, VPBX_API_DIALOG_EVENT],
        "alignments": [align("platform", "communications-apis"), align("digital-channels", "omnichannel-messaging", alignment_type="secondary", facets=channel("text", "async", "outbound"))],
        "functions": [
            ("send-dialog-api-message", "Отправить сообщение через Dialog API", "business", "api", [align("digital-channels", "omnichannel-messaging", "messenger-integration", "send-message", facets=channel("text", "async", "outbound")), align("platform", "communications-apis", alignment_type="supporting")], VPBX_API_DIALOG_SEND),
            ("receive-dialog-api-event", "Получить событие Dialog API", "business", "webhook", [align("platform", "open-api", "webhook-management", "configure-webhook-endpoint", facets=channel("text", "async", "inbound")), align("digital-channels", "omnichannel-messaging", alignment_type="secondary")], VPBX_API_DIALOG_EVENT),
        ],
    },
    {
        "id": "talker-softphone-service",
        "product": "mango-talker",
        "cluster": "mango-talker",
        "name": "Софтфон Mango Talker",
        "description": "Сервис звонков в приложении Mango Talker.",
        "module": ("talker-softphone-module", "Звонки в Talker"),
        "evidence": [TALKER_CALL, TALKER_ANSWER],
        "alignments": [align("voice-ucaas", "unified-communications", facets=channel("voice", "sync", "outbound"))],
        "functions": [
            ("call-colleague-in-talker", "Позвонить сотруднику из Talker", "business", "end-user-ui", [align("voice-ucaas", "voice-channel", "outbound-voice-call", facets=channel("voice", "sync", "outbound"))], TALKER_CALL),
            ("answer-talker-call", "Ответить на входящий звонок в Talker", "business", "end-user-ui", [align("voice-ucaas", "voice-channel", "inbound-voice-call", "receive-inbound-call", facets=channel("voice", "sync", "inbound"))], TALKER_ANSWER),
        ],
    },
    {
        "id": "talker-team-chat-service",
        "product": "mango-talker",
        "cluster": "mango-talker",
        "name": "Командные чаты Mango Talker",
        "description": "Сервис личных и групповых чатов, каналов и сообщений в Talker.",
        "module": ("talker-team-chat-module", "Чаты и каналы Talker"),
        "evidence": [TALKER_CHAT, TALKER_CHANNEL],
        "alignments": [align("digital-channels", "team-messaging", facets=channel("text", "async", "outbound"))],
        "functions": [
            ("send-talker-chat-message", "Отправить сообщение в Talker", "business", "end-user-ui", [align("digital-channels", "team-messaging", facets=channel("text", "async", "outbound"), mapping_gap=gap("function", "send-team-chat-message", "Industry Taxonomy не содержит leaf-функцию отправки командного сообщения."))], TALKER_CHAT),
            ("create-talker-chat-channel", "Создать чат или канал Talker", "configuration", "end-user-ui", [align("digital-channels", "team-messaging", mapping_gap=gap("function", "create-team-chat-channel", "Industry Taxonomy не содержит leaf-функцию создания командного канала."))], TALKER_CHANNEL),
        ],
    },
    {
        "id": "talker-video-meeting-service",
        "product": "mango-talker",
        "cluster": "mango-talker",
        "name": "Видео и конференции Talker",
        "description": "Сервис видеозвонков, аудиоконференций и конференц-комнат.",
        "module": ("talker-video-meeting-module", "Видео и конференции"),
        "evidence": [TALKER_VIDEO, TALKER_CONFERENCE],
        "alignments": [align("voice-ucaas", "unified-communications", facets=channel("video", "sync", "outbound"))],
        "functions": [
            ("start-talker-video-call", "Начать групповой видеозвонок", "business", "end-user-ui", [align("voice-ucaas", "unified-communications", facets=channel("video", "sync", "outbound"), mapping_gap=gap("function", "start-video-call", "Industry Taxonomy не содержит leaf-функцию старта видеозвонка внутри UCaaS."))], TALKER_VIDEO),
            ("join-talker-conference-room", "Присоединиться к конференции Talker", "business", "end-user-ui", [align("voice-ucaas", "unified-communications", facets=channel("video", "sync", "inbound"), mapping_gap=gap("function", "join-conference-room", "Industry Taxonomy не содержит leaf-функцию входа в конференц-комнату."))], TALKER_CONFERENCE),
        ],
    },
    {
        "id": "talker-contact-history-service",
        "product": "mango-talker",
        "cluster": "mango-talker",
        "name": "Контакты и история Talker",
        "description": "Сервис карточек контактов, истории вызовов и быстрых действий из журнала.",
        "module": ("talker-contact-history-module", "Контакты и журнал Talker"),
        "evidence": [TALKER_CONTACT, TALKER_HISTORY],
        "alignments": [align("voice-ucaas", "unified-communications")],
        "functions": [
            ("open-talker-contact-card", "Открыть карточку контакта Talker", "ui-action", "end-user-ui", [align("voice-ucaas", "unified-communications", mapping_gap=gap("function", "open-contact-card", "Industry Taxonomy не содержит UI leaf-функцию открытия карточки контакта."))], TALKER_CONTACT),
            ("call-contact-from-history", "Позвонить контакту из истории", "business", "end-user-ui", [align("voice-ucaas", "voice-channel", "outbound-voice-call", facets=channel("voice", "sync", "outbound"))], TALKER_HISTORY),
        ],
    },
    {
        "id": "speech-analytics-service",
        "product": "mango-ai-speech-quality",
        "cluster": "ai-speech-quality",
        "name": "Речевая аналитика",
        "description": "Сервис распознавания речи, тематик, тегов и аналитики разговоров.",
        "module": ("speech-analytics-topic-module", "Тематики речевой аналитики"),
        "evidence": [SPEECH_INDEX, CC_SPEECH],
        "alignments": [align("ai-automation", "speech-analytics", facets={"ai_assisted": True})],
        "functions": [
            ("recognize-recorded-call-speech", "Распознать речь в записи разговора", "business", "background-job", [align("ai-automation", "speech-analytics", facets={"ai_assisted": True, **channel("voice", "sync", "inbound")}, mapping_gap=gap("function", "recognize-call-speech", "Industry Taxonomy не содержит leaf-функцию распознавания записи разговора."))], SPEECH_INDEX),
            ("configure-speech-topic", "Настроить тематику речевой аналитики", "configuration", "admin-ui", [align("ai-automation", "speech-analytics", facets={"ai_assisted": True}, mapping_gap=gap("function", "configure-speech-topic", "Industry Taxonomy не содержит leaf-функцию настройки тематик речи."))], CC_SPEECH),
        ],
    },
    {
        "id": "conversation-summary-service",
        "product": "mango-ai-speech-quality",
        "cluster": "ai-speech-quality",
        "name": "AI-конспекты разговоров",
        "description": "Сервис генерации и просмотра конспектов разговоров по данным звонков.",
        "module": ("conversation-summary-module", "Конспекты разговоров"),
        "evidence": [VPBX_API_INDEX, VPBX_API_STATS],
        "alignments": [align("ai-automation", "conversation-summaries", "ai-summary", "generate-summary", facets={"ai_assisted": True})],
        "functions": [
            ("generate-call-summary", "Сформировать конспект разговора", "business", "background-job", [align("ai-automation", "conversation-summaries", "ai-summary", "generate-summary", facets={"ai_assisted": True})], VPBX_API_INDEX),
            ("view-call-summary", "Открыть конспект разговора", "ui-action", "admin-ui", [align("ai-automation", "conversation-summaries", "ai-summary", facets={"ai_assisted": True}, mapping_gap=gap("function", "view-call-summary", "Industry Taxonomy содержит generate-summary, но не содержит UI-функцию просмотра конспекта."))], VPBX_API_INDEX),
        ],
    },
    {
        "id": "quality-checklist-service",
        "product": "mango-ai-speech-quality",
        "cluster": "ai-speech-quality",
        "name": "Контроль качества и чек-листы",
        "description": "Сервис чек-листов, оценок операторов и контроля качества разговоров.",
        "module": ("quality-checklist-module", "Чек-листы качества"),
        "evidence": [QUALITY_INDEX, CC_CHECKLIST],
        "alignments": [align("contact-center", "quality-management")],
        "functions": [
            ("evaluate-call-by-checklist", "Оценить разговор по чек-листу", "business", "admin-ui", [align("contact-center", "quality-management", mapping_gap=gap("function", "evaluate-call-by-checklist", "Industry Taxonomy не содержит leaf-функцию оценки разговора по чек-листу."))], QUALITY_INDEX),
            ("configure-quality-checklist", "Настроить чек-лист качества", "configuration", "admin-ui", [align("contact-center", "quality-management", mapping_gap=gap("function", "configure-quality-checklist", "Industry Taxonomy не содержит leaf-функцию настройки чек-листа."))], CC_CHECKLIST),
        ],
    },
    {
        "id": "voice-robot-service",
        "product": "mango-ai-speech-quality",
        "cluster": "ai-speech-quality",
        "name": "Голосовой робот",
        "description": "Сервис автоматических голосовых диалогов и сценариев робота.",
        "module": ("voice-robot-scenario-module", "Сценарии голосового робота"),
        "evidence": [ROBOT_URL, PRODUCTS_URL],
        "alignments": [align("ai-automation", "voice-bot", facets={"ai_assisted": True, **channel("voice", "sync", "outbound")})],
        "functions": [
            ("run-voice-robot-dialog", "Запустить голосовой диалог робота", "business", "system-rule", [align("ai-automation", "voice-bot", facets={"ai_assisted": True, **channel("voice", "sync", "outbound")}, mapping_gap=gap("function", "run-voice-robot-dialog", "Industry Taxonomy не содержит leaf-функцию исполнения сценария голосового робота."))], ROBOT_URL),
            ("configure-voice-robot-scenario", "Настроить сценарий голосового робота", "configuration", "admin-ui", [align("ai-automation", "voice-bot", facets={"ai_assisted": True}, mapping_gap=gap("function", "configure-voice-robot-scenario", "Industry Taxonomy не содержит leaf-функцию настройки сценария голосового робота."))], ROBOT_URL),
        ],
    },
    {
        "id": "calltracking-attribution-service",
        "product": "mango-marketing-analytics",
        "cluster": "analytics-marketing",
        "name": "Атрибуция коллтрекинга",
        "description": "Сервис определения рекламного источника звонка и подстановки номеров.",
        "module": ("calltracking-attribution-module", "Атрибуция рекламных источников"),
        "evidence": [CALLTRACKING_URL, LK_ANALYTICS],
        "alignments": [align("analytics", "call-tracking")],
        "functions": [
            ("attribute-call-to-ad-source", "Привязать звонок к рекламному источнику", "business", "background-job", [align("analytics", "call-tracking", mapping_gap=gap("function", "attribute-call-to-ad-source", "Industry Taxonomy не содержит leaf-функцию атрибуции звонка к рекламе."))], LK_ANALYTICS),
            ("configure-calltracking-number", "Настроить номер коллтрекинга", "configuration", "admin-ui", [align("analytics", "call-tracking", mapping_gap=gap("function", "configure-calltracking-number", "Industry Taxonomy не содержит leaf-функцию настройки номера коллтрекинга."))], CALLTRACKING_URL),
        ],
    },
    {
        "id": "end-to-end-analytics-service",
        "product": "mango-marketing-analytics",
        "cluster": "analytics-marketing",
        "name": "Сквозная аналитика",
        "description": "Сервис связывания коммуникаций, сделок и маркетинговой воронки.",
        "module": ("end-to-end-analytics-module", "Сквозные отчёты"),
        "evidence": [CALLTRACKING_URL, VPBX_API_STATS],
        "alignments": [align("analytics", "end-to-end-analytics")],
        "functions": [
            ("join-call-and-sales-funnel", "Связать звонок с воронкой продаж", "business", "background-job", [align("analytics", "end-to-end-analytics", mapping_gap=gap("function", "join-call-and-sales-funnel", "Industry Taxonomy не содержит leaf-функцию связывания звонка с продажами."))], VPBX_API_STATS),
            ("open-end-to-end-analytics-report", "Открыть отчёт сквозной аналитики", "ui-action", "admin-ui", [align("analytics", "end-to-end-analytics", mapping_gap=gap("function", "open-end-to-end-analytics-report", "Industry Taxonomy не содержит UI leaf-функцию открытия отчёта сквозной аналитики."))], CALLTRACKING_URL),
        ],
    },
    {
        "id": "reporting-dashboard-service",
        "product": "mango-marketing-analytics",
        "cluster": "analytics-marketing",
        "name": "Отчёты и дашборды",
        "description": "Сервис отчётов, фильтров, графиков и табличной аналитики.",
        "module": ("reporting-dashboard-module", "Конструктор и просмотр отчётов"),
        "evidence": [CC_DASHBOARD, CC_WIDGET, LK_ANALYTICS],
        "alignments": [align("analytics", "multichannel-analytics")],
        "functions": [
            ("build-analytics-report", "Сформировать аналитический отчёт", "business", "background-job", [align("analytics", "multichannel-analytics", mapping_gap=gap("function", "build-analytics-report", "Industry Taxonomy не содержит leaf-функцию формирования отчёта."))], LK_ANALYTICS),
            ("select-dashboard-widget", "Выбрать виджет дашборда", "ui-action", "admin-ui", [align("analytics", "real-time-reporting", "dashboard-view", "select-dashboard-widget")], CC_WIDGET),
        ],
    },
    {
        "id": "wallboard-monitoring-service",
        "product": "mango-marketing-analytics",
        "cluster": "analytics-marketing",
        "name": "Wallboard-мониторинг",
        "description": "Сервис real-time экранов, групповых показателей и виджетов Wallboard.",
        "module": ("wallboard-monitoring-module", "Wallboard-виджеты"),
        "evidence": [WALLBOARD_INDEX, LK_WALLBOARD],
        "alignments": [align("analytics", "real-time-reporting")],
        "functions": [
            ("display-wallboard-widget", "Показать виджет Wallboard", "business", "end-user-ui", [align("analytics", "real-time-reporting", "dashboard-view", "select-dashboard-widget")], WALLBOARD_INDEX),
            ("configure-wallboard-widget", "Настроить виджет Wallboard", "configuration", "admin-ui", [align("analytics", "real-time-reporting", mapping_gap=gap("function", "configure-wallboard-widget", "Industry Taxonomy не содержит leaf-функцию настройки Wallboard-виджета."))], LK_WALLBOARD),
        ],
    },
    {
        "id": "vpbx-open-api-service",
        "product": "mango-platform-integrations",
        "cluster": "platform-integrations",
        "name": "ВАТС Open API",
        "description": "Сервис API-команд Виртуальной АТС, realtime-событий и программного управления вызовами.",
        "module": ("vpbx-open-api-module", "API Виртуальной АТС"),
        "evidence": [VPBX_API_INDEX, VPBX_API_CALL, VPBX_API_WEBHOOK],
        "alignments": [align("platform", "open-api")],
        "functions": [
            ("initiate-vpbx-api-call", "Инициировать звонок через API ВАТС", "business", "api", [align("voice-ucaas", "voice-channel", "outbound-voice-call", facets=channel("voice", "sync", "outbound")), align("platform", "open-api", alignment_type="supporting")], VPBX_API_CALL),
            ("configure-vpbx-webhook", "Настроить webhook ВАТС", "configuration", "api", [align("platform", "open-api", "webhook-management", "configure-webhook-endpoint")], VPBX_API_WEBHOOK),
        ],
    },
    {
        "id": "contact-center-api-service",
        "product": "mango-platform-integrations",
        "cluster": "platform-integrations",
        "name": "Contact Center API",
        "description": "Сервис API задач, событий и сущностей Контакт-центра.",
        "module": ("contact-center-api-module", "API Контакт-центра"),
        "evidence": [VPBX_API_INDEX, VPBX_API_CC_TASK, VPBX_API_CC_EVENT],
        "alignments": [align("platform", "open-api"), align("contact-center", "conversation-orchestration", alignment_type="secondary")],
        "functions": [
            ("create-contact-center-task-api", "Создать задачу Контакт-центра через API", "business", "api", [align("platform", "open-api", mapping_gap=gap("function", "create-contact-center-task", "Industry Taxonomy не содержит leaf-функцию создания задачи КЦ через API.")), align("contact-center", "conversation-orchestration", alignment_type="secondary")], VPBX_API_CC_TASK),
            ("receive-contact-center-event-webhook", "Получить событие Контакт-центра через webhook", "business", "webhook", [align("platform", "open-api", "webhook-management", "configure-webhook-endpoint"), align("contact-center", "conversation-orchestration", alignment_type="secondary")], VPBX_API_CC_EVENT),
        ],
    },
    {
        "id": "crm-erp-integration-service",
        "product": "mango-platform-integrations",
        "cluster": "platform-integrations",
        "name": "CRM и ERP-интеграции",
        "description": "Сервис интеграций с Bitrix24, 1C, amoCRM и внешними бизнес-системами.",
        "module": ("crm-erp-integration-module", "Коннекторы CRM и ERP"),
        "evidence": [BITRIX_INDEX, ONE_C_INDEX, AMOCRM_INDEX],
        "alignments": [align("platform", "platform-integration")],
        "functions": [
            ("sync-crm-call-card", "Синхронизировать карточку звонка с CRM", "business", "background-job", [align("platform", "platform-integration", mapping_gap=gap("function", "sync-crm-call-card", "Industry Taxonomy не содержит leaf-функцию синхронизации карточки звонка."))], BITRIX_INDEX),
            ("configure-crm-integration", "Настроить CRM-интеграцию", "configuration", "admin-ui", [align("platform", "platform-integration", mapping_gap=gap("function", "configure-crm-integration", "Industry Taxonomy не содержит leaf-функцию настройки CRM-коннектора."))], AMOCRM_INDEX),
        ],
    },
    {
        "id": "webhook-event-service",
        "product": "mango-platform-integrations",
        "cluster": "platform-integrations",
        "name": "Webhook-события",
        "description": "Сервис исходящих уведомлений, статусов и событий для внешних систем.",
        "module": ("webhook-event-module", "Webhook endpoints"),
        "evidence": [VPBX_API_WEBHOOK, VPBX_API_INDEX],
        "alignments": [align("platform", "open-api", "webhook-management", "configure-webhook-endpoint")],
        "functions": [
            ("send-call-event-webhook", "Передать событие звонка во внешний webhook", "business", "webhook", [align("platform", "open-api", "webhook-management", "configure-webhook-endpoint"), align("voice-ucaas", "voice-channel", "inbound-voice-call", alignment_type="secondary", facets=channel("voice", "sync", "inbound"))], VPBX_API_WEBHOOK),
            ("configure-webhook-endpoint", "Настроить endpoint webhook", "configuration", "admin-ui", [align("platform", "open-api", "webhook-management", "configure-webhook-endpoint")], VPBX_API_WEBHOOK),
        ],
    },
    {
        "id": "role-access-management-service",
        "product": "mango-security-access",
        "cluster": "security-access",
        "name": "Ролевое управление доступом",
        "description": "Сервис ролей, прав и ограничений доступа к разделам ЛК и Контакт-центра.",
        "module": ("role-access-management-module", "Роли и права доступа"),
        "evidence": [ROLE_MODEL_INDEX, LK_ROLES, CC_ROLES],
        "alignments": [align("security", "access-control", "role-management", "assign-role")],
        "functions": [
            ("assign-user-role", "Назначить роль пользователю", "configuration", "admin-ui", [align("security", "access-control", "role-management", "assign-role")], LK_ROLES),
            ("view-role-permissions", "Просмотреть права роли", "ui-action", "admin-ui", [align("security", "access-control", "role-management", mapping_gap=gap("function", "view-role-permissions", "Industry Taxonomy содержит assign-role, но не содержит UI-функцию просмотра прав роли."))], ROLE_MODEL_INDEX),
        ],
    },
    {
        "id": "sso-identity-service",
        "product": "mango-security-access",
        "cluster": "security-access",
        "name": "SSO и идентификация",
        "description": "Сервис единого входа и federated authentication для ЛК ВАТС.",
        "module": ("sso-identity-module", "SSO-подключение"),
        "evidence": [SSO_INDEX],
        "alignments": [align("security", "access-control")],
        "functions": [
            ("authenticate-user-with-sso", "Аутентифицировать пользователя через SSO", "business", "end-user-ui", [align("security", "access-control", mapping_gap=gap("function", "authenticate-user-with-sso", "Industry Taxonomy не содержит leaf-функцию SSO-аутентификации."))], SSO_INDEX),
            ("configure-sso-connection", "Настроить SSO-подключение", "configuration", "admin-ui", [align("security", "access-control", mapping_gap=gap("function", "configure-sso-connection", "Industry Taxonomy не содержит leaf-функцию настройки SSO."))], SSO_INDEX),
        ],
    },
    {
        "id": "recording-access-security-service",
        "product": "mango-security-access",
        "cluster": "security-access",
        "name": "Безопасность доступа к записям",
        "description": "Сервис ограничений, доступа и контроля операций с записями разговоров.",
        "module": ("recording-access-security-module", "Ограничения доступа к записям"),
        "evidence": [LK_RECORDING, LK_SECURITY],
        "alignments": [align("security", "information-security")],
        "functions": [
            ("restrict-recording-access", "Ограничить доступ к записям разговоров", "configuration", "admin-ui", [align("security", "information-security", mapping_gap=gap("function", "restrict-recording-access", "Industry Taxonomy не содержит leaf-функцию ограничения доступа к записям."))], LK_SECURITY),
            ("audit-recording-download", "Проверить доступ к скачиванию записи", "ui-action", "admin-ui", [align("security", "information-security", mapping_gap=gap("function", "audit-recording-download", "Industry Taxonomy не содержит UI leaf-функцию проверки доступа к скачиванию записи."))], LK_RECORDING),
        ],
    },
    {
        "id": "security-audit-settings-service",
        "product": "mango-security-access",
        "cluster": "security-access",
        "name": "Аудит и настройки безопасности",
        "description": "Сервис журнала действий, security-настроек и cross-product ограничений.",
        "module": ("security-audit-settings-module", "Журнал действий и политики безопасности"),
        "evidence": [LK_SECURITY, LK_INDEX],
        "alignments": [align("security", "information-security")],
        "functions": [
            ("view-security-audit-log", "Просмотреть журнал действий", "ui-action", "admin-ui", [align("security", "information-security", mapping_gap=gap("function", "view-security-audit-log", "Industry Taxonomy не содержит UI leaf-функцию просмотра журнала безопасности."))], LK_SECURITY),
            ("configure-security-policy", "Настроить политику безопасности", "configuration", "admin-ui", [align("security", "information-security", mapping_gap=gap("function", "configure-security-policy", "Industry Taxonomy не содержит leaf-функцию настройки политики безопасности."))], LK_SECURITY),
        ],
    },
]


def build_internal() -> dict[str, Any]:
    products = [
        entity(
            spec["id"],
            "product",
            spec["name"],
            spec["description"],
            spec["evidence"],
            spec["alignments"],
            **{
                key: spec[key]
                for key in ("official_refs", "internal_only_reason")
                if key in spec
            },
            services=spec["services"],
        )
        for spec in product_specs
    ]

    services = []
    modules = []
    functions = []
    for spec in service_specs:
        module_id, module_name = spec["module"]
        function_ids = [function[0] for function in spec["functions"]]
        services.append(
            entity(
                spec["id"],
                "service",
                spec["name"],
                spec["description"],
                spec["evidence"],
                spec["alignments"],
                cluster=spec["cluster"],
                parent_products=[spec["product"]],
                modules=[module_id],
            )
        )
        modules.append(
            entity(
                module_id,
                "module",
                module_name,
                f"Модуль сервиса «{spec['name']}» в Mango Taxonomy.",
                spec["evidence"],
                spec["alignments"],
                cluster=spec["cluster"],
                parent_services=[spec["id"]],
                functions=function_ids,
            )
        )
        for function_id, name, function_type, surface, alignments, evidence in spec["functions"]:
            functions.append(
                entity(
                    function_id,
                    "function",
                    name,
                    f"Атомарная функция модуля «{module_name}».",
                    [evidence],
                    alignments,
                    parent_module=module_id,
                    function_type=function_type,
                    interaction_surface=surface,
                )
            )

    return {
        "taxonomy": {
            "version": 1,
            "scope": "mango-internal-registry",
            "products": products,
            "internal_services": services,
            "modules": modules,
            "functions": functions,
        }
    }


def build_mapping(official: dict[str, Any], internal: dict[str, Any]) -> dict[str, Any]:
    entities = []
    collections = [
        official["taxonomy"]["official_products"],
        internal["taxonomy"]["products"],
        internal["taxonomy"]["internal_services"],
        internal["taxonomy"]["modules"],
        internal["taxonomy"]["functions"],
    ]
    for collection in collections:
        for item in collection:
            entities.append(
                {
                    "source_id": item["id"],
                    "source_level": item["level"],
                    "industry_alignment": item["maps_to"]["industry_alignment"],
                }
            )
    return {
        "taxonomy_mapping": {
            "version": 1,
            "mapping_scope": "mango-to-industry",
            "source_taxonomy": "mango-taxonomy",
            "target_taxonomy": "industry-taxonomy",
            "entities": entities,
        }
    }


def dump(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    missing = [
        ref
        for ref in {
            ref
            for product in official_products
            for ref in product["evidence_refs"]
            if not ref.startswith("http")
        }
        if not (ROOT / ref).exists()
    ]
    internal = build_internal()
    for collection in (
        internal["taxonomy"]["products"],
        internal["taxonomy"]["internal_services"],
        internal["taxonomy"]["modules"],
        internal["taxonomy"]["functions"],
    ):
        for item in collection:
            for ref in item["evidence_refs"]:
                if not ref.startswith("http") and not (ROOT / ref).exists():
                    missing.append(ref)
    if missing:
        raise SystemExit("Missing evidence refs:\n" + "\n".join(sorted(set(missing))))

    official = {
        "taxonomy": {
            "version": 1,
            "scope": "mango-official-products",
            "official_products": official_products,
        }
    }
    mapping = build_mapping(official, internal)

    OUT.mkdir(parents=True, exist_ok=True)
    dump(OUT / "official-products.yaml", official)
    dump(OUT / "internal-registry.yaml", internal)
    dump(OUT / "product-mapping.yaml", mapping)


if __name__ == "__main__":
    main()
