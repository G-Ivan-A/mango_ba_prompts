#!/usr/bin/env python3
"""Cascade-fill kb/mango-taxonomy/mango-registry.json with REAL documented modules/functions.

Additive only: loads the current registry and APPENDS new modules + functions, each
grounded in a verified kb/mango-product-docs/processed/ section. New entities inherit
their parent's primary industry_alignment (industry_ref + facets are copied verbatim,
so they stay resolvable and infra-rule-safe). No industry nodes are invented.

Evidence is resolved by (directory, section-number) via glob, so a wrong slug can never
slip in: a number that does not resolve is skipped and logged (issue #170 forbids
undocumented entities — gaps are recorded in docs/analysis/, not the registry).
"""
import copy
import glob
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "kb/mango-taxonomy/mango-registry.json"
PROCESSED = ROOT / "kb/mango-product-docs/processed"


def resolve(dirp, num):
    """Return repo-relative path to processed/<dirp>/sections/<num>-*.md or None."""
    base = PROCESSED / dirp / "sections"
    for pat in (f"{num:02d}-*.md", f"{num}-*.md"):
        hits = sorted(base.glob(pat))
        if hits:
            return str(hits[0].relative_to(ROOT))
    return None


def ev_paths(ev):
    """Resolve a list of (dir, num) pairs; return (resolved, missing)."""
    res, miss = [], []
    for dirp, num in ev:
        p = resolve(dirp, num)
        (res if p else miss).append(p or f"{dirp}#{num}")
    # de-dup, keep order
    seen, out = set(), []
    for p in res:
        if p not in seen:
            seen.add(p)
            out.append(p)
    return out, miss


# ---------------------------------------------------------------------------
# NEW MODULES — each attaches to an existing service and ships >=2 functions.
# fn: (id, name_ru, function_type, interaction_surface, [(dir, section_no), ...])
# ---------------------------------------------------------------------------
NEW_MODULES = [
    # ===================== vats-core (mango-virtual-pbx) =====================
    {"id": "vats-blacklist-whitelist-module", "name_ru": "Чёрный и белый списки номеров",
     "parent_service": "vats-inbound-routing-service", "functions": [
        ("add-number-to-blacklist", "Добавить номер в чёрный список", "configuration", "admin-ui", [("mango-lk-manual", 110)]),
        ("add-number-to-whitelist", "Добавить номер в белый список", "configuration", "admin-ui", [("mango-lk-manual", 110)]),
     ]},
    {"id": "vats-time-based-routing-module", "name_ru": "Маршрутизация по расписанию",
     "parent_service": "vats-inbound-routing-service", "functions": [
        ("configure-time-based-routing", "Настроить маршрутизацию по рабочему времени", "configuration", "admin-ui", [("mango-lk-manual", 84)]),
        ("configure-holiday-schedule", "Настроить расписание праздничных дней", "configuration", "admin-ui", [("mango-lk-manual", 84)]),
     ]},
    {"id": "vats-voicemail-management-module", "name_ru": "Управление голосовой почтой",
     "parent_service": "vats-recording-history-service", "functions": [
        ("enable-voicemail-transcription", "Включить расшифровку голосовой почты", "configuration", "admin-ui", [("mango-lk-manual", 296)]),
        ("configure-voicemail-notification-actions", "Настроить уведомления о голосовой почте", "configuration", "admin-ui", [("mango-lk-manual", 296)]),
     ]},
    # ================== contact-center-core (mango-contact-center) ==================
    {"id": "cc-call-hold-module", "name_ru": "Удержание вызовов",
     "parent_service": "cc-agent-workspace-service", "functions": [
        ("hold-call", "Поставить вызов на удержание", "business", "operator-ui", [("mango-cc-manual", 49)]),
        ("resume-held-call", "Снять вызов с удержания", "business", "operator-ui", [("mango-cc-manual", 49)]),
     ]},
    {"id": "cc-call-transfer-module", "name_ru": "Перевод вызовов",
     "parent_service": "cc-agent-workspace-service", "functions": [
        ("transfer-call-with-consultation", "Перевести вызов с консультацией", "business", "operator-ui", [("mango-cc-manual", 48)]),
        ("transfer-call-without-consultation", "Перевести вызов без консультации", "business", "operator-ui", [("mango-cc-manual", 48)]),
     ]},
    {"id": "cc-agent-conferencing-module", "name_ru": "Организация конференций",
     "parent_service": "cc-agent-workspace-service", "functions": [
        ("initiate-conference-call", "Организовать конференц-вызов", "business", "operator-ui", [("mango-cc-manual", 50)]),
        ("add-participant-to-conference", "Добавить участника в конференцию", "business", "operator-ui", [("mango-cc-manual", 50)]),
     ]},
    {"id": "cc-call-recording-module", "name_ru": "Запись разговоров КЦ",
     "parent_service": "cc-agent-workspace-service", "functions": [
        ("enable-cc-call-recording", "Включить запись разговоров", "configuration", "admin-ui", [("mango-cc-manual", 54)]),
        ("access-cc-call-recording", "Получить доступ к записи разговора", "business", "operator-ui", [("mango-cc-manual", 54)]),
     ]},
    {"id": "cc-supervisor-monitoring-module", "name_ru": "Контроль и прослушивание операторов",
     "parent_service": "cc-supervisor-wfm-service", "functions": [
        ("monitor-agents-realtime", "Контролировать операторов в реальном времени", "business", "operator-ui", [("mango-cc-manual", 88)]),
        ("listen-to-agent-conversation", "Прослушать разговор оператора", "business", "operator-ui", [("mango-cc-manual", 111)]),
     ]},
    # ================== digital-channels (mango-digital-communications) ==================
    {"id": "social-messenger-channels-module", "name_ru": "Каналы соцсетей и мессенджеров",
     "parent_service": "messenger-channel-service", "functions": [
        ("connect-whatsapp-channel", "Подключить канал WhatsApp", "configuration", "admin-ui", [("mango-lk-manual", 191)]),
        ("connect-vkontakte-channel", "Подключить канал ВКонтакте", "configuration", "admin-ui", [("mango-lk-manual", 190)]),
        ("connect-avito-channel", "Подключить канал Avito", "configuration", "admin-ui", [("mango-lk-manual", 209)]),
     ]},
    {"id": "dialog-api-session-management-module", "name_ru": "Управление сессиями Dialog API",
     "parent_service": "dialog-api-messaging-service", "functions": [
        ("take-dialog-session", "Взять сессию диалога в работу", "business", "api", [("mdialogi-api", 40)]),
        ("transfer-dialog-session", "Перевести сессию на другого сотрудника", "business", "api", [("mdialogi-api", 41)]),
        ("close-dialog-session", "Закрыть сессию диалога", "business", "api", [("mdialogi-api", 42)]),
        ("get-active-dialog-sessions", "Получить список активных сессий", "business", "api", [("mdialogi-api", 37)]),
        ("get-dialog-chat-history", "Загрузить историю чата", "business", "api", [("mdialogi-api", 44)]),
     ]},
    {"id": "dialog-api-webhook-module", "name_ru": "Вебхуки Dialog API",
     "parent_service": "dialog-api-messaging-service", "functions": [
        ("receive-new-message-webhook", "Получить вебхук о новом сообщении", "business", "webhook", [("mdialogi-api", 53)]),
        ("receive-session-taken-webhook", "Получить вебхук о взятии сессии в работу", "business", "webhook", [("mdialogi-api", 47)]),
        ("receive-session-waiting-webhook", "Получить вебхук об ожидающей сессии", "business", "webhook", [("mdialogi-api", 46)]),
     ]},
    # ===================== mango-talker =====================
    {"id": "talker-call-control-module", "name_ru": "Управление вызовом в Mango Talker",
     "parent_service": "talker-softphone-service", "functions": [
        ("hold-talker-call", "Поставить вызов на удержание", "business", "end-user-ui", [("mtalker/windows-mac-working", 129)]),
        ("transfer-talker-call", "Перевести вызов на другого сотрудника", "business", "end-user-ui", [("mtalker/windows-mac-working", 130)]),
        ("mute-talker-microphone", "Выключить микрофон", "ui-action", "end-user-ui", [("mtalker/windows-mac-working", 133)]),
        ("record-talker-call", "Записать разговор", "business", "end-user-ui", [("mtalker/windows-mac-working", 134)]),
     ]},
    {"id": "talker-message-operations-module", "name_ru": "Операции с сообщениями Mango Talker",
     "parent_service": "talker-team-chat-service", "functions": [
        ("edit-talker-message", "Редактировать отправленное сообщение", "ui-action", "end-user-ui", [("mtalker/windows-mac-working", 56)]),
        ("cancel-talker-message", "Отменить отправленное сообщение", "ui-action", "end-user-ui", [("mtalker/windows-mac-working", 57)]),
        ("quote-talker-message", "Процитировать сообщение", "ui-action", "end-user-ui", [("mtalker/windows-mac-working", 78)]),
        ("search-talker-chat-history", "Найти сообщение в истории чата", "ui-action", "end-user-ui", [("mtalker/windows-mac-working", 76)]),
     ]},
    {"id": "talker-file-sharing-module", "name_ru": "Обмен файлами в Mango Talker",
     "parent_service": "talker-team-chat-service", "functions": [
        ("send-talker-file", "Отправить файл", "ui-action", "end-user-ui", [("mtalker/windows-mac-working", 59)]),
        ("send-talker-image", "Отправить изображение", "ui-action", "end-user-ui", [("mtalker/windows-mac-working", 59)]),
     ]},
    {"id": "talker-video-effects-module", "name_ru": "Видео-эффекты и демонстрация в Mango Talker",
     "parent_service": "talker-video-meeting-service", "functions": [
        ("share-talker-screen", "Включить демонстрацию экрана", "ui-action", "end-user-ui", [("mtalker/windows-mac-working", 161)]),
        ("change-talker-background", "Изменить фоновые эффекты", "ui-action", "end-user-ui", [("mtalker/windows-mac-working", 164)]),
        ("raise-hand-in-talker", "Поднять руку", "ui-action", "end-user-ui", [("mtalker/windows-mac-working", 165)]),
     ]},
    {"id": "talker-favorites-groups-module", "name_ru": "Избранное и группы контактов",
     "parent_service": "talker-contact-history-service", "functions": [
        ("add-talker-favorite", "Добавить контакт в избранное", "ui-action", "end-user-ui", [("mtalker/windows-mac-working", 190)]),
        ("remove-talker-favorite", "Удалить контакт из избранного", "ui-action", "end-user-ui", [("mtalker/windows-mac-working", 191)]),
        ("view-talker-favorites", "Открыть список избранного", "ui-action", "end-user-ui", [("mtalker/windows-mac-working", 189)]),
        ("filter-talker-contact-groups", "Фильтровать контакты по группам", "ui-action", "end-user-ui", [("mtalker/windows-mac-working", 183)]),
     ]},
    {"id": "talker-presence-status-module", "name_ru": "Статус присутствия и уведомления",
     "parent_service": "talker-softphone-service", "functions": [
        ("change-talker-presence-status", "Сменить статус присутствия пользователя", "ui-action", "end-user-ui", [("mtalker/windows-mac-working", 222), ("mtalker/android-user-guide", 115)]),
        ("disable-talker-notifications", "Отключить показ уведомлений из всех чатов и каналов", "ui-action", "end-user-ui", [("mtalker/windows-mac-working", 220), ("mtalker/windows-mac-working", 223)]),
     ]},
    # ===================== ai-speech-quality (mango-ai-speech-quality) =====================
    {"id": "quality-appeal-module", "name_ru": "Апелляции по оценке качества",
     "parent_service": "quality-checklist-service", "functions": [
        ("submit-quality-appeal", "Подать апелляцию на оценку", "business", "operator-ui", [("quality-managment", 30)]),
        ("review-quality-appeal", "Обработать апелляцию контролёром", "business", "operator-ui", [("quality-managment", 31)]),
        ("configure-appeal-settings", "Настроить правила апелляций", "configuration", "admin-ui", [("quality-managment", 9)]),
     ]},
    {"id": "quality-call-randomizer-module", "name_ru": "Рандомайзер выборки звонков",
     "parent_service": "quality-checklist-service", "functions": [
        ("configure-call-randomizer", "Настроить рандомайзер выборки", "configuration", "admin-ui", [("quality-managment", 15)]),
        ("select-random-calls-for-review", "Сформировать случайную выборку для проверки", "business", "admin-ui", [("quality-managment", 15)]),
     ]},
    {"id": "ai-assistant-module", "name_ru": "ИИ-помощник оператора",
     "parent_service": "conversation-summary-service", "functions": [
        ("create-ai-assistant", "Создать ИИ-помощника", "configuration", "admin-ui", [("quality-managment", 45)]),
        ("configure-ai-assistant", "Настроить ИИ-помощника", "configuration", "admin-ui", [("quality-managment", 46)]),
     ]},
    {"id": "speech-analytics-search-module", "name_ru": "Поиск и прослушивание разговоров",
     "parent_service": "speech-analytics-service", "functions": [
        ("search-conversations-by-content", "Найти разговоры по содержанию", "business", "admin-ui", [("speech-analytics/rukovodstvo-polzovatelya-rechevaya-analitika", 19), ("speech-analytics/rukovodstvo-polzovatelya-rechevaya-analitika", 23)]),
        ("listen-to-found-recording", "Прослушать найденную запись разговора", "business", "admin-ui", [("speech-analytics/rukovodstvo-polzovatelya-rechevaya-analitika", 25)]),
     ]},
    {"id": "speech-analytics-tagging-module", "name_ru": "Тегирование разговоров",
     "parent_service": "speech-analytics-service", "functions": [
        ("tag-conversation", "Проставить теги разговору", "business", "admin-ui", [("speech-analytics/rukovodstvo-polzovatelya-rechevaya-analitika", 26)]),
        ("configure-ai-tagging", "Настроить ИИ-тегирование разговоров", "configuration", "admin-ui", [("speech-analytics/rukovodstvo-polzovatelya-rechevaya-analitika", 11)]),
     ]},
    # ===================== analytics-marketing (mango-marketing-analytics) =====================
    {"id": "static-calltracking-module", "name_ru": "Статический коллтрекинг",
     "parent_service": "calltracking-attribution-service", "functions": [
        ("setup-static-calltracking", "Настроить статический коллтрекинг", "configuration", "admin-ui", [("mango-lk-manual", 146)]),
        ("view-static-calltracking-report", "Открыть отчёт статического коллтрекинга", "business", "admin-ui", [("mango-lk-manual", 147)]),
     ]},
    {"id": "analytics-goals-integration-module", "name_ru": "Цели и интеграции веб-аналитики",
     "parent_service": "end-to-end-analytics-service", "functions": [
        ("integrate-web-analytics", "Интегрировать Google Analytics и Яндекс.Метрику", "configuration", "admin-ui", [("mango-lk-manual", 230)]),
        ("configure-event-goal", "Настроить цель по событию", "configuration", "admin-ui", [("mango-lk-manual", 232)]),
     ]},
    # ===================== platform-integrations (mango-platform-integrations) =====================
    {"id": "bitrix24-connector-module", "name_ru": "Коннектор Битрикс24",
     "parent_service": "crm-erp-integration-service", "functions": [
        ("configure-bitrix24-integration", "Настроить интеграцию с Битрикс24", "configuration", "admin-ui", [("integration-bitrix24", 2)]),
        ("auto-create-bitrix24-lead", "Автоматически создавать лид при звонке", "business", "system-rule", [("integration-bitrix24", 30)]),
     ]},
    {"id": "amocrm-connector-module", "name_ru": "Коннектор amoCRM",
     "parent_service": "crm-erp-integration-service", "functions": [
        ("configure-amocrm-integration", "Настроить интеграцию с amoCRM", "configuration", "admin-ui", [("integration_amocrm", 2)]),
        ("pop-amocrm-card-on-incoming-call", "Показать карточку контакта при входящем звонке", "business", "system-rule", [("integration_amocrm", 3)]),
        ("click-to-call-from-amocrm", "Позвонить из карточки amoCRM", "business", "end-user-ui", [("integration_amocrm", 4)]),
     ]},
    {"id": "onec-connector-module", "name_ru": "Коннектор 1С",
     "parent_service": "crm-erp-integration-service", "functions": [
        ("configure-onec-integration", "Настроить интеграцию с 1С", "configuration", "admin-ui", [("integration_1c", 2)]),
        ("pop-onec-card-on-incoming-call", "Показать карточку контакта 1С при входящем звонке", "business", "system-rule", [("integration_1c", 4)]),
        ("click-to-call-from-onec", "Позвонить из 1С", "business", "end-user-ui", [("integration_1c", 5)]),
     ]},
    # ===================== security-access (mango-security-access) =====================
    {"id": "custom-role-management-module", "name_ru": "Управление пользовательскими ролями",
     "parent_service": "role-access-management-service", "functions": [
        ("create-custom-role", "Создать пользовательскую роль", "configuration", "admin-ui", [("Rolevaya-model-vats", 5)]),
        ("copy-custom-role", "Скопировать роль", "configuration", "admin-ui", [("Rolevaya-model-vats", 8)]),
        ("delete-custom-role", "Удалить роль", "configuration", "admin-ui", [("Rolevaya-model-vats", 9)]),
     ]},
    {"id": "sso-idp-configuration-module", "name_ru": "Настройка провайдера SSO",
     "parent_service": "sso-identity-service", "functions": [
        ("configure-sso-idp", "Настроить Identity Provider (IdP)", "configuration", "admin-ui", [("lk-vats-sso", 4), ("lk-vats-sso", 6)]),
        ("add-identity-provider", "Добавить провайдера идентификации", "configuration", "admin-ui", [("lk-vats-sso", 5)]),
        ("map-sso-attributes", "Сопоставить поля SSO с атрибутами", "configuration", "admin-ui", [("lk-vats-sso", 7)]),
     ]},
]

# ---------------------------------------------------------------------------
# EXTRA FUNCTIONS — appended to EXISTING modules.
# (parent_module, id, name_ru, function_type, interaction_surface, [(dir, num)])
# ---------------------------------------------------------------------------
EXTRA_FUNCTIONS = [
    # vats-core
    ("vats-inbound-scenarios-module", "configure-callback-forwarding", "Настроить переадресацию по номеру клиента", "configuration", "admin-ui", [("mango-lk-manual", 109)]),
    ("vats-ivr-menu-module", "configure-ivr-menu-branches", "Настроить ветви голосового меню", "configuration", "admin-ui", [("mango-lk-manual", 104)]),
    ("vats-ivr-menu-module", "enable-speech-recognition-menu", "Включить распознавание речи в меню", "configuration", "admin-ui", [("mango-lk-manual", 105)]),
    ("vats-call-recording-module", "configure-recording-rules", "Настроить режимы записи", "configuration", "admin-ui", [("mango-lk-manual", 137)]),
    # contact-center-core
    ("cc-agent-call-handling-module", "complete-after-call-work", "Завершить поствызывную обработку", "business", "operator-ui", [("mango-cc-manual", 32)]),
    ("cc-queue-routing-module", "transfer-interaction-to-agent", "Перевести обращение на оператора", "business", "operator-ui", [("mango-cc-manual", 68)]),
    ("cc-outbound-campaign-module", "configure-agent-assisted-dialing", "Настроить набор с участием сотрудника", "configuration", "admin-ui", [("mango-cc-manual", 128)]),
    ("cc-supervisor-wfm-module", "configure-wfm-auto-actions", "Настроить автоматические действия WFM", "configuration", "admin-ui", [("mango-cc-manual", 105)]),
    ("cc-supervisor-wfm-module", "schedule-inbound-forecast", "Спланировать прогноз входящих", "configuration", "admin-ui", [("mango-cc-manual", 100)]),
    # digital-channels
    ("digital-channel-group-module", "enable-chatbot-for-channel-group", "Включить чат-бота для группы каналов", "configuration", "admin-ui", [("mango-lk-manual", 212)]),
    # analytics-marketing
    ("calltracking-attribution-module", "setup-calltracking-widget", "Настроить виджет коллтрекинга", "configuration", "admin-ui", [("mango-lk-manual", 68)]),
    ("reporting-dashboard-module", "build-cc-report", "Построить отчёт контакт-центра", "business", "admin-ui", [("mango-cc-manual", 205)]),
    ("reporting-dashboard-module", "view-cc-performance-panel", "Открыть панель показателей", "business", "operator-ui", [("mango-cc-manual", 11)]),
    ("wallboard-monitoring-module", "select-wallboard-template", "Выбрать шаблон Wallboard", "configuration", "admin-ui", [("wallboard", 4)]),
    ("wallboard-monitoring-module", "set-wallboard-metric-threshold", "Задать пороги метрик Wallboard", "configuration", "admin-ui", [("wallboard", 4)]),
    # platform-integrations
    ("vpbx-open-api-module", "hangup-call-via-api", "Завершить вызов через API", "business", "api", [("vpbx-api", 38)]),
    ("vpbx-open-api-module", "send-sms-via-api", "Отправить SMS через API", "business", "api", [("vpbx-api", 39)]),
    ("contact-center-api-module", "get-call-statistics-via-api", "Получить статистику вызовов через API", "business", "api", [("vpbx-api", 58)]),
    ("webhook-event-module", "receive-call-notification-webhook", "Получить вебхук-уведомление о вызове", "business", "webhook", [("vpbx-api", 27)]),
    # security-access
    ("security-audit-settings-module", "view-action-log", "Просмотреть журнал действий", "business", "admin-ui", [("mango-lk-manual", 279)]),
    ("security-audit-settings-module", "configure-ip-restriction", "Настроить ограничение доступа по IP", "configuration", "admin-ui", [("mango-lk-manual", 273)]),
]


def primary_alignment(entity):
    aligns = entity["maps_to"]["industry_alignment"]
    for a in aligns:
        if a.get("alignment_type") == "primary":
            return a
    return aligns[0]


def make_alignment(parent_align, evidence, strip_function):
    ref = copy.deepcopy(parent_align["industry_ref"])
    if strip_function:
        ref.pop("function", None)
    a = {"alignment_type": "primary", "industry_ref": ref, "evidence_refs": list(evidence)}
    if "facets" in parent_align:
        a["facets"] = copy.deepcopy(parent_align["facets"])
    return a


def main():
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    tax = data["taxonomy"]
    svc_by_id = {s["id"]: s for s in tax["internal_services"]}
    mod_by_id = {m["id"]: m for m in tax["modules"]}
    used_ids = {e["id"] for key in ("products", "internal_services", "modules", "functions",
                                    "official_products") for e in tax[key]}

    log, skipped, already = [], [], []
    added_modules = added_functions = 0

    # ---- new modules ----
    for spec in NEW_MODULES:
        svc = svc_by_id.get(spec["parent_service"])
        if not svc:
            skipped.append(f"module {spec['id']}: parent service {spec['parent_service']} missing")
            continue
        if spec["id"] in used_ids:
            already.append(f"module {spec['id']}: already present")
            continue
        svc_align = primary_alignment(svc)
        mod_ref = copy.deepcopy(svc_align["industry_ref"])

        fn_objs, all_ev = [], []
        for fid, name_ru, ftype, surface, ev in spec["functions"]:
            res, miss = ev_paths(ev)
            if not res:
                skipped.append(f"function {fid}: no evidence resolved ({miss})")
                continue
            if fid in used_ids:
                already.append(f"function {fid}: already present")
                continue
            used_ids.add(fid)
            all_ev.extend(res)
            fn_objs.append((fid, name_ru, ftype, surface, res))

        if len(fn_objs) < 2:
            skipped.append(f"module {spec['id']}: <2 functions resolved, dropped")
            for fid, *_ in fn_objs:
                used_ids.discard(fid)
            continue

        mod_ev = []
        for p in all_ev:
            if p not in mod_ev:
                mod_ev.append(p)

        mod_align = {"alignment_type": "primary", "industry_ref": mod_ref, "evidence_refs": list(mod_ev)}
        if "facets" in svc_align:
            mod_align["facets"] = copy.deepcopy(svc_align["facets"])

        module = {
            "id": spec["id"], "level": "module", "name_ru": spec["name_ru"],
            "description": f"Модуль сервиса «{svc['name_ru']}» в Mango Taxonomy.",
            "lifecycle_status": "active", "evidence_refs": mod_ev,
            "maps_to": {"industry_alignment": [mod_align]},
            "cluster": svc["cluster"], "parent_services": [svc["id"]],
            "functions": [f[0] for f in fn_objs],
        }
        used_ids.add(spec["id"])
        tax["modules"].append(module)
        mod_by_id[spec["id"]] = module
        svc["modules"].append(spec["id"])
        added_modules += 1

        for fid, name_ru, ftype, surface, res in fn_objs:
            fn = {
                "id": fid, "level": "function", "name_ru": name_ru,
                "description": f"Атомарная функция модуля «{spec['name_ru']}».",
                "lifecycle_status": "active", "evidence_refs": res,
                "maps_to": {"industry_alignment": [make_alignment(mod_align, res, strip_function=True)]},
                "parent_module": spec["id"], "function_type": ftype, "interaction_surface": surface,
            }
            tax["functions"].append(fn)
            added_functions += 1
        log.append(f"+ module {spec['id']} ({len(fn_objs)} fn) -> {svc['id']}")

    # ---- extra functions on existing modules ----
    for parent_module, fid, name_ru, ftype, surface, ev in EXTRA_FUNCTIONS:
        mod = mod_by_id.get(parent_module)
        if not mod:
            skipped.append(f"function {fid}: parent module {parent_module} missing")
            continue
        if fid in used_ids:
            already.append(f"function {fid}: already present")
            continue
        res, miss = ev_paths(ev)
        if not res:
            skipped.append(f"function {fid}: no evidence resolved ({miss})")
            continue
        used_ids.add(fid)
        mod_align = primary_alignment(mod)
        fn = {
            "id": fid, "level": "function", "name_ru": name_ru,
            "description": f"Атомарная функция модуля «{mod['name_ru']}».",
            "lifecycle_status": "active", "evidence_refs": res,
            "maps_to": {"industry_alignment": [make_alignment(mod_align, res, strip_function=True)]},
            "parent_module": parent_module, "function_type": ftype, "interaction_surface": surface,
        }
        tax["functions"].append(fn)
        mod["functions"].append(fid)
        added_functions += 1
        log.append(f"+ function {fid} -> {parent_module}")

    REGISTRY.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("\n".join(log))
    if already:
        print(f"\n=== ALREADY PRESENT (no-op, {len(already)}) ===")
        print("\n".join(already))
    print("\n=== SKIPPED ===")
    print("\n".join(skipped) if skipped else "(none)")
    print(f"\nadded_modules={added_modules} added_functions={added_functions}")
    print(f"totals: services={len(tax['internal_services'])} modules={len(tax['modules'])} functions={len(tax['functions'])}")
    # Only real problems (missing evidence/parent) are failures; re-running on an
    # already-filled registry is a clean no-op.
    return 1 if skipped else 0


if __name__ == "__main__":
    sys.exit(main())
