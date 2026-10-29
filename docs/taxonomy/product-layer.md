---
status: review
version: 0.1
updated: 2026-10-28
temperature: 0.1
---

# Product Layer Mango: полный каталог четырёх уровней

Узлы классификации не утверждают наличие функции в продукте. Исторические статусы и параметры
сохранены; связь исходных плоских списков Feature ↔ Atomic Function — редакционная гипотеза.
Новые операции имеют проверенный локатор страницы/заголовка. Для факта As-Is прочитайте статью.

Контракт: https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/product-classification-contract.md
Машинный каталог: https://github.com/konard/G-Ivan-A-mango_ba_prompts/blob/issue-399-c3c0e96510d8/docs/taxonomy/products.json
Метод и ограничения: https://github.com/konard/G-Ivan-A-mango_ba_prompts/blob/issue-399-c3c0e96510d8/docs/taxonomy/README.md

Полнота: Domain: 7, Capability: 43, Feature: 151, Atomic Function: 152.

## cloud-pbx — Виртуальная / облачная АТС

Domain: voice-ucaas.
Статус источника: Есть; историческая строка 1.
Источник: https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md

| Feature | Atomic Function / параметры | Источник операции |
| --- | --- | --- |
| extension-management | `extension-provisioning` (extension_range, sip_profile) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| call-routing-rules | `auto-attendant` (greeting_set, routing_tree) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| working-hours-schedule | `working-hours-routing` (schedule_id, holiday_calendar) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| voicemail | `voicemail-to-email` (mailbox_id, delivery_format) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| mobile-account | `mobile-account-login` (не заявлены) | https://www.mango-office.ru/support/3_produkty-i-prilozheniya/2_mobilnyi-lk/1_mob_lk_bystryy_start/2_dostup_k_mlk/2_2_vhod_v_mlk/ |
| account-session | `account-auto-logout-configure` (не заявлены) | https://www.mango-office.ru/support/3_produkty-i-prilozheniya/1_virtualnaya-ats-i-lichnyi-kabinet/10_Vhod/4_kak_nastroit_avtomaticheskii_vykhod_iz_sistemy_dlya_bezopasnosti/ |

## sip-connectivity — IP-телефония и SIP trunk

Domain: voice-ucaas.
Статус источника: Есть; историческая строка 2.
Источник: https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md

| Feature | Atomic Function / параметры | Источник операции |
| --- | --- | --- |
| sip-trunking | `sip-trunk-registration` (trunk_id, auth_credentials) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| sip-trunking | `sip-trunk-delete` (не заявлены) | https://www.mango-office.ru/support/3_produkty-i-prilozheniya/10_sip-trunk/1_sozdanie_i_redaktirovanie_sip_trunk/3_5_udalenie/ |
| codec-negotiation | `codec-selection` (codec_priority, dtmf_mode) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| failover-routing | `trunk-failover` (backup_trunk_id, retry_interval) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |

## number-management — Номерная ёмкость

Domain: voice-ucaas.
Статус источника: Есть; историческая строка 3.
Источник: https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md

| Feature | Atomic Function / параметры | Источник операции |
| --- | --- | --- |
| virtual-numbers | `number-assignment` (number_type, region_code) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| toll-free-8800 | `tollfree-routing` (number_8800, destination_map) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| mobile-numbers | `number-assignment` (number_type, region_code) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| number-porting | `number-porting` (donor_operator, port_window) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |

## ivr-voice-menu — Голосовое меню IVR и автоинформирование

Domain: voice-ucaas.
Статус источника: Есть; историческая строка 4.
Источник: https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md

| Feature | Atomic Function / параметры | Источник операции |
| --- | --- | --- |
| ivr-scenarios | `ivr-menu-navigation` (menu_tree, timeout_action) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| ivr-scenarios | `service-availability-routing` (queue_id, overflow_target) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| auto-secretary | `auto-secretary-greeting` (greeting_id, dtmf_map) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| voice-announcement | `auto-secretary-greeting` (greeting_id, dtmf_map) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |

## call-recording — Запись разговоров и журналирование

Domain: voice-ucaas.
Статус источника: Есть; историческая строка 6.
Источник: https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md

| Feature | Atomic Function / параметры | Источник операции |
| --- | --- | --- |
| call-recording | `call-recording-capture` (retention_period, storage_target) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| call-recording | `recording-access-control` (role_id, masking_policy) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| call-log | `call-log-export` (date_range, export_format) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| usage-statistics | `call-log-export` (date_range, export_format) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |

## callback — Обратный звонок с сайта

Domain: voice-ucaas.
Статус источника: Есть; историческая строка 7.
Источник: https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md

| Feature | Atomic Function / параметры | Источник операции |
| --- | --- | --- |
| web-callback-widget | `callback-request-intake` (widget_id, consent_flag) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| consent-capture | `callback-request-intake` (widget_id, consent_flag) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| callback-scheduling | `callback-scheduling` (max_attempts, time_window) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |

## unified-communications — Корпоративный мессенджер и softphone — Mango Talker

Domain: voice-ucaas.
Статус источника: Есть; историческая строка 8.
Источник: https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md

| Feature | Atomic Function / параметры | Источник операции |
| --- | --- | --- |
| softphone | `softphone-call` (device_id, sip_account) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| corporate-messaging | `corporate-chat` (channel_id, retention_period) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| presence-status | `presence-update` (status_code, visibility_scope) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| presence-status | `talker-presence-change` (не заявлены) | https://www.mango-office.ru/support/3_produkty-i-prilozheniya/7_mango-talker/3_userguide_mtalker_4mobile/14_upravlenie_profilem_polzovatelya/smena_statusa_polzovatelya/ |
| file-sharing | `talker-shared-files-view` (не заявлены) | https://www.mango-office.ru/support/3_produkty-i-prilozheniya/7_mango-talker/3_userguide_mtalker_4mobile/10_administrirovanie_obschego_chata_ili_kanala/prosmotr_obschih_faylov/ |

## video-conferencing — Видеоконференции

Domain: voice-ucaas.
Статус источника: Есть; историческая строка 9.
Источник: https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md

| Feature | Atomic Function / параметры | Источник операции |
| --- | --- | --- |
| video-meetings | `meeting-host` (max_participants, meeting_id) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| meeting-recording | `meeting-recording` (retention_period, consent_flag) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| screen-sharing | `screen-share` (session_id, quality_profile) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |

## number-branding — Маркировка номера, «карусельные номера», защита дозваниваемости

Domain: voice-ucaas.
Статус источника: Не выявлено; историческая строка 38.
Источник: https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md

| Feature | Atomic Function / параметры | Источник операции |
| --- | --- | --- |
| number-labeling | `caller-id-labeling` (brand_label, aggregator_id) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| carousel-numbers | `carousel-number-rotation` (number_pool, rotation_policy) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| reachability-protection | `reachability-monitoring` (spam_score_threshold, alert_channel) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| anti-spam-marking | `reachability-monitoring` (spam_score_threshold, alert_channel) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |

## voice-sms-broadcast — Голосовые SMS / автоинформирование через голосовой канал

Domain: voice-ucaas.
Статус источника: Частично; историческая строка 39.
Источник: https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md

| Feature | Atomic Function / параметры | Источник операции |
| --- | --- | --- |
| voice-broadcast | `voice-message-broadcast` (contact_list, voice_template) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| auto-notification | `voice-message-broadcast` (contact_list, voice_template) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| auto-notification | `consent-filter` (opt_in_list, advertising_flag) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| delivery-confirmation | `delivery-confirmation` (dtmf_confirm, retry_policy) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |

## call-routing — Распределение звонков, очереди, маршрутизация

Domain: contact-center.
Статус источника: Есть; историческая строка 5.
Источник: https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md

| Feature | Atomic Function / параметры | Источник операции |
| --- | --- | --- |
| skill-based-routing | `skill-based-routing` (skill_group, priority_weight) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| queue-management | `queue-management` (max_wait_time, sla_threshold) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| overflow-rules | `overflow-routing` (overflow_target, abandon_threshold) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| overflow-routing | `failed-call-behavior-configure` (не заявлены) | https://www.mango-office.ru/support/3_produkty-i-prilozheniya/1_virtualnaya-ats-i-lichnyi-kabinet/1_4_obrabotka_zvonkov/4_4_3_nastroyki_dozvona_i_soobshcheniy_po_umolchaniyu/ |

## omnichannel-contact-center — Омниканальный контакт-центр / CCaaS

Domain: contact-center.
Статус источника: Есть; историческая строка 11.
Источник: https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md

| Feature | Atomic Function / параметры | Источник операции |
| --- | --- | --- |
| inbound-handling | `interaction-routing` (channel_type, routing_profile) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| omnichannel-desktop | `unified-agent-desktop` (layout_id, channel_set) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| channel-blending | `interaction-routing` (channel_type, routing_profile) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| wallboard | `wallboard-template-select` (не заявлены) | https://www.mango-office.ru/support/3_produkty-i-prilozheniya/11_wallboard/wallboard_setup/ |
| wallboard | `wallboard-custom-template-configure` (не заявлены) | https://www.mango-office.ru/support/3_produkty-i-prilozheniya/11_wallboard/wallboard_setup/ |
| web-dashboard | `web-dashboard-widget-create` (не заявлены) | https://www.mango-office.ru/support/3_produkty-i-prilozheniya/3_web_cc/2_dashboard/2_2_sozdanie_i_nastroyka_vidzheta/ |
| web-dashboard | `web-dashboard-widget-delete` (не заявлены) | https://www.mango-office.ru/support/3_produkty-i-prilozheniya/3_web_cc/2_dashboard/2_4_udalenie_vidzheta/ |

## agent-workspace — Входящие обращения и рабочее место оператора

Domain: contact-center.
Статус источника: Есть; историческая строка 12.
Источник: https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md

| Feature | Atomic Function / параметры | Источник операции |
| --- | --- | --- |
| agent-desktop | `interaction-handling` (interaction_id, disposition_code) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| customer-card | `customer-card-popup` (crm_lookup_key, screen_pop_layout) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| interaction-history | `interaction-handling` (interaction_id, disposition_code) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| agent-status | `desktop-agent-status-change` (не заявлены) | https://www.mango-office.ru/support/3_produkty-i-prilozheniya/3_kontakt-tsentr/3_glavnoe_okno_programmy/2_1_upravlenie_statusom/ |
| agent-status | `agent-status-configure` (не заявлены) | https://www.mango-office.ru/support/3_produkty-i-prilozheniya/3_kontakt-tsentr/5_5_1_3_nastroyki/2_5_1_3_12_statusy_sotrudnikov/ |
| agent-status | `cc-api-user-status-set` (не заявлены) | https://www.mango-office.ru/support/5_api-i-razrabotka/1_api-mango-office/6_opisanie_metodov_api_kontakt_tsentra_mango/2_4_upravlenie_statusami_i_sessiyami/1_4_1_statusy/4_4_1_2_smena_statusa_polzovatelya/ |
| agent-status | `cc-api-status-list` (не заявлены) | https://www.mango-office.ru/support/5_api-i-razrabotka/1_api-mango-office/6_opisanie_metodov_api_kontakt_tsentra_mango/2_4_upravlenie_statusami_i_sessiyami/1_4_1_statusy/4_4_1_4_statusy_na_produkte/ |
| agent-session | `web-agent-login` (не заявлены) | https://www.mango-office.ru/support/3_produkty-i-prilozheniya/3_web_cc/1_avtorizatsiya/1_2_poryadok_vhoda/ |
| agent-session | `cc-api-session-status-set` (не заявлены) | https://www.mango-office.ru/support/5_api-i-razrabotka/1_api-mango-office/6_opisanie_metodov_api_kontakt_tsentra_mango/2_4_upravlenie_statusami_i_sessiyami/1_4_1_statusy/4_4_1_3_smena_statusa_sessii_polzovatelya/ |
| agent-session | `cc-api-presence-get` (не заявлены) | https://www.mango-office.ru/support/5_api-i-razrabotka/1_api-mango-office/6_opisanie_metodov_api_kontakt_tsentra_mango/2_4_upravlenie_statusami_i_sessiyami/1_4_1_statusy/4_4_1_3_statusy_polzovateley_produkta/ |
| working-time-report | `agent-working-time-view` (не заявлены) | https://www.mango-office.ru/support/3_produkty-i-prilozheniya/3_kontakt-tsentr/10_sotrudniki/7_3_rabochee_vremya/ |
| ai-assistance | `web-ai-hints-view` (не заявлены) | https://www.mango-office.ru/support/3_produkty-i-prilozheniya/3_web_cc/12_dopolnitelnye_uslugi/12_2_panel_podskazki_ii/ |

## outbound-calling — Исходящий обзвон и кампании

Domain: contact-center.
Статус источника: Есть; историческая строка 13.
Источник: https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md

| Feature | Atomic Function / параметры | Источник операции |
| --- | --- | --- |
| campaign-management | `callback-scheduling` (max_attempts, time_window) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| campaign-management | `disposition-code-assignment` (code_list, auto_tagging) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| campaign-management | `outbound-campaign-create` (не заявлены) | https://www.mango-office.ru/support/3_produkty-i-prilozheniya/3_kontakt-tsentr/14_iskhodyashchiy_obzvon/1_4_dobavlenie_kampanii/11_4_1_s_uchastiem_sotrudnika/ |
| dialing-modes | `predictive-dialing` (dial_ratio, abandon_rate_limit) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| realtime-analytics | `campaign-realtime-view` (не заявлены) | https://www.mango-office.ru/support/3_produkty-i-prilozheniya/3_kontakt-tsentr/14_iskhodyashchiy_obzvon/2_5_kartochka_kampanii/11_5_1_statistika_kampanii/ |
| historical-reports | `campaign-history-view` (не заявлены) | https://www.mango-office.ru/support/3_produkty-i-prilozheniya/3_kontakt-tsentr/14_iskhodyashchiy_obzvon/2_5_kartochka_kampanii/11_5_2_effektivnost_kampanii/ |

## quality-management — Управление качеством операторов / QM

Domain: contact-center.
Статус источника: Есть; историческая строка 20.
Источник: https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md

| Feature | Atomic Function / параметры | Источник операции |
| --- | --- | --- |
| scorecards | `scorecard-evaluation` (checklist_id, sampling_rate) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| scorecards | `quality-scorecard-create` (не заявлены) | https://www.mango-office.ru/support/3_produkty-i-prilozheniya/4_kontrol-kachestva/2_nastroyka_blankov_otsenki/2_1_sozdanie_blanka_otsenki/ |
| scorecards | `quality-score-weights-configure` (не заявлены) | https://www.mango-office.ru/support/3_produkty-i-prilozheniya/4_kontrol-kachestva/2_nastroyka_blankov_otsenki/2_3_nastroyka_shkaly_otsenok_i_vesa_kriteriev/ |
| call-sampling | `scorecard-evaluation` (checklist_id, sampling_rate) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| evaluation-workflow | `evaluation-appeal` (case_id, reviewer_role) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| evaluation-workflow | `quality-appeal-enable` (не заявлены) | https://www.mango-office.ru/support/3_produkty-i-prilozheniya/4_kontrol-kachestva/2_nastroyka_blankov_otsenki/2_4_nastroyka_apellyatsii/ |

## workforce-management — WFM / управление рабочими ресурсами

Domain: contact-center.
Статус источника: Есть; историческая строка 21.
Источник: https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md

| Feature | Atomic Function / параметры | Источник операции |
| --- | --- | --- |
| shift-scheduling | `shift-scheduling` (agent_pool, coverage_target) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| shift-scheduling | `shift-exchange-request` (не заявлены) | https://www.mango-office.ru/support/3_produkty-i-prilozheniya/3_kontakt-tsentr/11_plan_raboty/8_4_obmen_smenami/ |
| shift-scheduling | `holiday-calendar-configure` (не заявлены) | https://www.mango-office.ru/support/3_produkty-i-prilozheniya/3_kontakt-tsentr/11_plan_raboty/2_5_nastroiki/8_5_2_kalendar/ |
| load-forecasting | `load-forecasting` (history_window, forecast_horizon) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| adherence-tracking | `punctuality-report-view` (не заявлены) | https://www.mango-office.ru/support/3_produkty-i-prilozheniya/3_kontakt-tsentr/11_plan_raboty/8_3_otchety/ |
| adherence-tracking | `punctuality-criteria-configure` (не заявлены) | https://www.mango-office.ru/support/3_produkty-i-prilozheniya/3_kontakt-tsentr/11_plan_raboty/8_3_otchety/ |
| adherence-tracking | `punctuality-penalty-configure` (не заявлены) | https://www.mango-office.ru/support/3_produkty-i-prilozheniya/3_kontakt-tsentr/11_plan_raboty/8_3_otchety/ |
| adherence-tracking | `working-time-notification-configure` (не заявлены) | https://www.mango-office.ru/support/3_produkty-i-prilozheniya/3_kontakt-tsentr/11_plan_raboty/2_5_nastroiki/8_5_1_auto_wfm/ |

## knowledge-base — База знаний и скрипты операторов

Domain: contact-center.
Статус источника: Есть; историческая строка 22.
Источник: https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md

| Feature | Atomic Function / параметры | Источник операции |
| --- | --- | --- |
| knowledge-articles | `article-lifecycle` (article_id, review_status) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| agent-scripts | `script-guidance` (scenario_id, branching_rules) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| version-control | `article-lifecycle` (article_id, review_status) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |

## deal-management — Управление сделками / лёгкий CRM-сценарий

Domain: contact-center.
Статус источника: Есть; историческая строка 23.
Источник: https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md

| Feature | Atomic Function / параметры | Источник операции |
| --- | --- | --- |
| deal-pipeline | `deal-pipeline-tracking` (pipeline_id, stage_map) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| contact-management | `communication-logging` (contact_id, channel_type) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| communication-history | `communication-logging` (contact_id, channel_type) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |

## crm-platform — Полноценная CRM как самостоятельная платформа

Domain: contact-center.
Статус источника: Частично; историческая строка 24.
Источник: https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md

| Feature | Atomic Function / параметры | Источник операции |
| --- | --- | --- |
| crm-core | `crm-record-management` (entity_type, field_schema) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| sales-automation | `crm-record-management` (entity_type, field_schema) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |

## self-service-portal — Self-Service портал клиента / личный кабинет заказчика

Domain: contact-center.
Статус источника: Частично; историческая строка 40.
Источник: https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md

| Feature | Atomic Function / параметры | Источник операции |
| --- | --- | --- |
| customer-portal | `self-service-login` (account_id, auth_method) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| self-onboarding | `service-self-provisioning` (catalog_item, approval_flow) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| recording-access | `self-service-recording-access` (masking_policy, retention_period) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| service-catalog-selection | `service-self-provisioning` (catalog_item, approval_flow) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |

## operator-mobile-app — Мобильное приложение оператора CCaaS

Domain: contact-center.
Статус источника: Частично; историческая строка 41.
Источник: https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md

| Feature | Atomic Function / параметры | Источник операции |
| --- | --- | --- |
| mobile-agent-desktop | `mobile-interaction-handling` (device_id, channel_set) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| push-notifications | `push-notification-delivery` (notification_type, priority) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| offline-mode | `mobile-interaction-handling` (device_id, channel_set) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |

## sms-messaging — SMS-рассылки

Domain: digital-channels.
Статус источника: Есть; историческая строка 10.
Источник: https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md

| Feature | Atomic Function / параметры | Источник операции |
| --- | --- | --- |
| bulk-sms | `bulk-sms-dispatch` (contact_list, message_template) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| bulk-sms | `advertising-consent-check` (consent_source, advertising_flag) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| bulk-sms | `cc-message-campaign-create` (не заявлены) | https://www.mango-office.ru/support/3_produkty-i-prilozheniya/3_kontakt-tsentr/17_tekstovye_rassylki/14_1_tekstovye_rassylki/ |
| transactional-sms | `bulk-sms-dispatch` (contact_list, message_template) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| opt-out-management | `opt-out-handling` (stop_keyword, suppression_list) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |

## omnichannel-messaging — Омниканальные коммуникации: чат, мессенджеры, соцсети, email

Domain: digital-channels.
Статус источника: Есть; историческая строка 14.
Источник: https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md

| Feature | Atomic Function / параметры | Источник операции |
| --- | --- | --- |
| messenger-integration | `channel-ingestion` (channel_type, account_credentials) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| social-channels | `channel-ingestion` (channel_type, account_credentials) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| email-channel | `channel-ingestion` (channel_type, account_credentials) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| unified-inbox | `unified-inbox-routing` (inbox_id, routing_rules) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| channel-configuration | `mdialogi-channel-configure` (не заявлены) | https://www.mango-office.ru/support/3_produkty-i-prilozheniya/6_mango-dialogi/3_nastroyka_vidzheta_mkch/1_nastroyka_vidzheta_mkch/ |
| conversation-session | `mdialogi-session-create` (не заявлены) | https://www.mango-office.ru/support/5_api-i-razrabotka/3_api-mango-dialogi/3_rukovodstvo_po_api/3_api_upravleniya_sessiyami/sozdat_novuyu_sessiyu/ |
| conversation-session | `mdialogi-session-close` (не заявлены) | https://www.mango-office.ru/support/5_api-i-razrabotka/3_api-mango-dialogi/3_rukovodstvo_po_api/3_api_upravleniya_sessiyami/zakryt_sessiyu/ |

## website-chat — Чат для сайта

Domain: digital-channels.
Статус источника: Есть; историческая строка 15.
Источник: https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md

| Feature | Atomic Function / параметры | Источник операции |
| --- | --- | --- |
| chat-widget | `chat-widget-embed` (widget_id, trigger_rules) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| proactive-invitations | `chat-widget-embed` (widget_id, trigger_rules) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| visitor-tracking | `visitor-data-capture` (consent_flag, field_set) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |

## messenger-marketing — Мессенджер-маркетинг

Domain: digital-channels.
Статус источника: Есть; историческая строка 33.
Источник: https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md

| Feature | Atomic Function / параметры | Источник операции |
| --- | --- | --- |
| campaign-templates | `messenger-campaign-dispatch` (template_id, audience_segment) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| broadcast-lists | `messenger-campaign-dispatch` (template_id, audience_segment) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| opt-in-management | `messenger-optin-management` (optin_source, suppression_list) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| whatsapp-templates | `whatsapp-template-create` (не заявлены) | https://www.mango-office.ru/support/3_produkty-i-prilozheniya/6_mango-dialogi/3_nastroyka_vidzheta_mkch/12_shablonyywhatsapp/ |

## chatbot — Чат-бот

Domain: ai-automation.
Статус источника: Есть; историческая строка 16.
Источник: https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md

| Feature | Atomic Function / параметры | Источник операции |
| --- | --- | --- |
| dialog-scenarios | `agent-handoff` (fallback_queue, context_payload) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| intent-recognition | `intent-classification` (model_id, confidence_threshold) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| agent-handoff | `agent-handoff` (fallback_queue, context_payload) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| dialog-analytics | `chatbot-script-statistics-view` (не заявлены) | https://www.mango-office.ru/support/3_produkty-i-prilozheniya/9_roboty-i-ai-roboty/3_chat_boty/4_3_statistika_po_skriptu_chat_bota/ |

## voice-bot — Голосовой робот / voice bot

Domain: ai-automation.
Статус источника: Есть; историческая строка 17.
Источник: https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md

| Feature | Atomic Function / параметры | Источник операции |
| --- | --- | --- |
| speech-recognition | `speech-to-text` (language_model, confidence_threshold) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| dialog-orchestration | `voice-dialog-flow` (scenario_id, fallback_action) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| tts-synthesis | `text-to-speech` (voice_profile, prosody_settings) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| intent-dictionary | `nlu-dictionary-create` (не заявлены) | https://www.mango-office.ru/support/3_produkty-i-prilozheniya/9_roboty-i-ai-roboty/7_ai_roboty/12_1_sozdanie_ai_robota/ |
| http-action | `robot-http-request-configure` (не заявлены) | https://www.mango-office.ru/support/3_produkty-i-prilozheniya/9_roboty-i-ai-roboty/4_konstruktor_skriptov/5_6_blok_otpravit_http_zapros/ |

## process-robot — Робот-администратор

Domain: ai-automation.
Статус источника: Есть; историческая строка 18.
Источник: https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md

| Feature | Atomic Function / параметры | Источник операции |
| --- | --- | --- |
| process-automation | `automated-action-execution` (process_id, permission_scope) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| action-orchestration | `automated-action-execution` (process_id, permission_scope) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| audit-logging | `action-audit-logging` (log_target, event_filter) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |

## speech-analytics — Речевая аналитика / conversation intelligence

Domain: ai-automation.
Статус источника: Есть; историческая строка 19.
Источник: https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md

| Feature | Atomic Function / параметры | Источник операции |
| --- | --- | --- |
| transcription | `call-transcription` (language_model, diarization_flag) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| transcription | `recognition-settings-configure` (не заявлены) | https://www.mango-office.ru/support/3_produkty-i-prilozheniya/4_kontrol-kachestva/8_rechevaya_analitika/1_4_vkladka_nastroyki/9_4_2_nastroiki_raspoznavaniya_zapisei/ |
| sentiment-analysis | `sentiment-scoring` (model_id, score_scale) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| keyword-detection | `keyword-spotting` (keyword_set, alert_rule) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| keyword-detection | `speech-topic-create` (не заявлены) | https://www.mango-office.ru/support/3_produkty-i-prilozheniya/8_rechevaya-analitika-i-skoring/1_rechevaya-analitika/2_avtomaticheskoe_tegirovanie_razgovorov/3_2_sozdanie_i_nastroyka_svoikh_tematik/ |
| text-communication-analysis | `text-communications-list-view` (не заявлены) | https://www.mango-office.ru/support/3_produkty-i-prilozheniya/8_rechevaya-analitika-i-skoring/1_rechevaya-analitika/6_poisk_i_analiz_razgovorov/2_2_analitika_tekstovykh_kommunikatsiy/2_2_2_prosmotr_spiska_kommunikatsiy/ |

## call-tracking — Коллтрекинг

Domain: analytics.
Статус источника: Есть; историческая строка 27.
Источник: https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md

| Feature | Atomic Function / параметры | Источник операции |
| --- | --- | --- |
| dynamic-number-pool | `dynamic-number-substitution` (number_pool, session_ttl) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| dynamic-number-pool | `calltracking-widget-create` (не заявлены) | https://www.mango-office.ru/support/3_produkty-i-prilozheniya/5_kolltreking-i-analitika/12_ustanovka_vidzheta_na_sayte/3_kakynastroitykodyvidzheta/ |
| source-attribution | `source-attribution` (utm_map, attribution_window) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| call-analytics | `source-attribution` (utm_map, attribution_window) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |

## end-to-end-analytics — Сквозная аналитика и ROMI

Domain: analytics.
Статус источника: Есть; историческая строка 28.
Источник: https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md

| Feature | Atomic Function / параметры | Источник операции |
| --- | --- | --- |
| revenue-attribution | `romi-calculation` (cost_source, revenue_source) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| romi-calculation | `romi-calculation` (cost_source, revenue_source) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| funnel-analysis | `funnel-tracking` (stage_map, conversion_window) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |

## multichannel-analytics — Мультиканальная аналитика и атрибуция

Domain: analytics.
Статус источника: Есть; историческая строка 29.
Источник: https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md

| Feature | Atomic Function / параметры | Источник операции |
| --- | --- | --- |
| channel-attribution | `attribution-modeling` (model_type, lookback_window) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| deduplication | `lead-deduplication` (match_keys, merge_policy) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| conversion-tracking | `attribution-modeling` (model_type, lookback_window) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |

## email-tracking — Email-трекинг

Domain: analytics.
Статус источника: Есть; историческая строка 30.
Источник: https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md

| Feature | Atomic Function / параметры | Источник операции |
| --- | --- | --- |
| open-tracking | `email-event-tracking` (tracking_pixel, event_type) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| click-tracking | `email-event-tracking` (tracking_pixel, event_type) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| unsubscribe-management | `unsubscribe-handling` (list_id, suppression_policy) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |

## product-analytics — Товарная аналитика / ecommerce analytics

Domain: analytics.
Статус источника: Есть; историческая строка 31.
Источник: https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md

| Feature | Atomic Function / параметры | Источник операции |
| --- | --- | --- |
| demand-analysis | `sku-performance-analysis` (catalog_source, metric_set) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| sku-performance | `sku-performance-analysis` (catalog_source, metric_set) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| data-quality | `data-quality-check` (quality_rules, threshold) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |

## competitor-analysis — Анализ конкурентов

Domain: analytics.
Статус источника: Есть; историческая строка 32.
Источник: https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md

| Feature | Atomic Function / параметры | Источник операции |
| --- | --- | --- |
| market-monitoring | `competitor-data-collection` (source_list, refresh_interval) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| benchmark-reports | `competitor-data-collection` (source_list, refresh_interval) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |

## telephony-equipment — SIP-телефоны, гарнитуры и устройства

Domain: hardware.
Статус источника: Вне SaaS-ядра; историческая строка 37.
Источник: https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md

| Feature | Atomic Function / параметры | Источник операции |
| --- | --- | --- |
| sip-phones | `device-provisioning` (device_model, firmware_version) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| headsets | `device-compatibility-check` (sip_profile, certification_id) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| accessories | `device-compatibility-check` (sip_profile, certification_id) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |

## information-security — Информационная безопасность

Domain: security.
Статус источника: Есть (сквозной слой); историческая строка 36.
Источник: https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md

| Feature | Atomic Function / параметры | Источник операции |
| --- | --- | --- |
| access-control | `role-based-access-control` (role_id, permission_scope) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| access-control | `mobile-account-access-check` (не заявлены) | https://www.mango-office.ru/support/3_produkty-i-prilozheniya/2_mobilnyi-lk/1_mob_lk_bystryy_start/2_dostup_k_mlk/2_1_prava_dostupa/ |
| access-control | `role-create` (не заявлены) | https://www.mango-office.ru/support/6_administrirovanie/1_roli-i-prava/1_rolevaya-model-vats/3_upravlenie_rolyami/sozdanie_roli/ |
| access-control | `role-delete` (не заявлены) | https://www.mango-office.ru/support/6_administrirovanie/1_roli-i-prava/1_rolevaya-model-vats/3_upravlenie_rolyami/udalenie_roli/ |
| access-control | `role-permission-configure` (не заявлены) | https://www.mango-office.ru/support/6_administrirovanie/1_roli-i-prava/1_rolevaya-model-vats/4_nastroyka_prav_dostupa_roli/ |
| audit-logging | `security-audit-logging` (log_target, retention_period) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| data-classification | `data-classification` (sensitivity_label, handling_policy) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| incident-management | `security-audit-logging` (log_target, retention_period) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |

## platform-integration — Интеграции с CRM, 1C, LDAP, marketplace

Domain: cross-domain: семь существующих Domain.
Статус источника: Есть; историческая строка 25.
Источник: https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md

| Feature | Atomic Function / параметры | Источник операции |
| --- | --- | --- |
| crm-connectors | `crm-bidirectional-sync` (connector_id, sync_interval) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| crm-connectors | `amocrm-employee-mapping` (не заявлены) | https://www.mango-office.ru/support/4_integratsii/1_vse-integratsii/3_amocrm/1_nachalo_raboty_s_integratsiey/05_shag_5_sopostavlenie_sotrudnikov_virtualnoy_ats_i_amocrm/1_kak_nastroit_sopostavlenie_sotrudnikov/ |
| crm-connectors | `bpmsoft-cc-status-enable` (не заявлены) | https://www.mango-office.ru/support/4_integratsii/1_vse-integratsii/5_bpm-soft/2_dopolnitelnye_nastroyki_integratsii/4_4_dopolnitelnye_nastroyki_integratsii/7_ispolzovat_statusy_kontakt_tsentra/kak_vklyuchit_nastroyku_ispolzovat_statusy_kontakt_tsentra/ |
| crm-connectors | `bpmsoft-cc-status-change` (не заявлены) | https://www.mango-office.ru/support/4_integratsii/1_vse-integratsii/5_bpm-soft/2_dopolnitelnye_nastroyki_integratsii/4_4_dopolnitelnye_nastroyki_integratsii/7_ispolzovat_statusy_kontakt_tsentra/statusy_kontakt_tsentra_v_interfeyse_bpmsoft/ |
| erp-connectors | `crm-bidirectional-sync` (connector_id, sync_interval) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| directory-sync | `directory-sync` (ldap_endpoint, attribute_map) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| marketplace-apps | `crm-bidirectional-sync` (connector_id, sync_interval) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |

## open-api — Open API, webhook, API для УВК/CRM

Domain: cross-domain: семь существующих Domain.
Статус источника: Есть; историческая строка 26.
Источник: https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md

| Feature | Atomic Function / параметры | Источник операции |
| --- | --- | --- |
| rest-api | `api-rate-limiting` (rate_limit, quota_window) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| webhooks | `webhook-subscription` (event_type, callback_url) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| event-streaming | `webhook-subscription` (event_type, callback_url) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |

## cpaas — CPaaS / программируемые голосовые и messaging API

Domain: cross-domain: семь существующих Domain.
Статус источника: Частично; историческая строка 34.
Источник: https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md

| Feature | Atomic Function / параметры | Источник операции |
| --- | --- | --- |
| programmable-voice | `programmable-voice-call` (from_number, callflow_id) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| programmable-messaging | `programmable-message-send` (channel_type, message_payload) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| number-api | `programmable-voice-call` (from_number, callflow_id) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |

## service-desk — Service desk / ITSM helpdesk

Domain: cross-domain: семь существующих Domain.
Статус источника: Частично; историческая строка 35.
Источник: https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md

| Feature | Atomic Function / параметры | Источник операции |
| --- | --- | --- |
| ticketing | `ticket-lifecycle` (ticket_type, sla_policy) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| incident-management | `ticket-lifecycle` (ticket_type, sla_policy) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| request-fulfilment | `ticket-lifecycle` (ticket_type, sla_policy) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |

## vendor-support-services — Услуги поддержки и развития CRM/SaaS как vendor-service

Domain: cross-domain: семь существующих Domain.
Статус источника: Не выявлено; историческая строка 42.
Источник: https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md

| Feature | Atomic Function / параметры | Источник операции |
| --- | --- | --- |
| application-maintenance | `application-maintenance` (sla_tier, support_window) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| crm-development | `crm-customization` (scope_spec, change_request_id) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |
| professional-services | `application-maintenance` (sla_tier, support_window) | https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md |

## report-builder — Конструктор отчётов

Domain: voice-ucaas, contact-center, analytics.
Статус источника: Документация обнаружена; коммерческая доступность не проверялась; историческая строка новая capability.
Источник: https://www.mango-office.ru/support/3_produkty-i-prilozheniya/12_konstruktor-otchetov/

| Feature | Atomic Function / параметры | Источник операции |
| --- | --- | --- |
| report-authoring | `report-create` (не заявлены) | https://www.mango-office.ru/support/3_produkty-i-prilozheniya/12_konstruktor-otchetov/1_otchety/dobavlenie_otcheta/ |
| report-authoring | `report-view` (не заявлены) | https://www.mango-office.ru/support/3_produkty-i-prilozheniya/12_konstruktor-otchetov/1_otchety/prosmotr_otcheta/ |
| dataset-modeling | `custom-parameter-create` (не заявлены) | https://www.mango-office.ru/support/3_produkty-i-prilozheniya/12_konstruktor-otchetov/2_dannye/1_parametry/sozdanie_polzovatelskogo_parametra/ |
| dataset-modeling | `report-entity-create` (не заявлены) | https://www.mango-office.ru/support/3_produkty-i-prilozheniya/12_konstruktor-otchetov/2_dannye/2_suschnosti/sozdanie_suschnosti/ |
