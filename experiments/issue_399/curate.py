"""Curated atomic operations. Source selectors are reviewed, not inferred by LLM.

Run after audit.py; ignored cache supplies titles and exact heading locators.
New product assertions must still be checked against full article/visual context.
"""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
P = 'https://www.mango-office.ru/support/3_produkty-i-prilozheniya/'
CC = P + '3_kontakt-tsentr/'
WEB = P + '3_web_cc/'
STATUS_API = 'https://www.mango-office.ru/support/5_api-i-razrabotka/1_api-mango-office/6_opisanie_metodov_api_kontakt_tsentra_mango/2_4_upravlenie_statusami_i_sessiyami/1_4_1_statusy/'
ROLES = 'https://www.mango-office.ru/support/6_administrirovanie/1_roli-i-prava/1_rolevaya-model-vats/'
MD_API = 'https://www.mango-office.ru/support/5_api-i-razrabotka/3_api-mango-dialogi/3_rukovodstvo_po_api/3_api_upravleniya_sessiyami/'

# capability, feature, function, source URL, meaning, verification, optional heading
SELECTION = [
 ('outbound-calling', 'realtime-analytics', 'campaign-realtime-view', CC+'14_iskhodyashchiy_obzvon/2_5_kartochka_kampanii/11_5_1_statistika_kampanii/', 'Просмотр текущей статистики кампании', 'Открыть статистику кампании и проверить обновление показателей.'),
 ('outbound-calling', 'historical-reports', 'campaign-history-view', CC+'14_iskhodyashchiy_obzvon/2_5_kartochka_kampanii/11_5_2_effektivnost_kampanii/', 'Формирование отчёта эффективности за период', 'Установить период, сформировать отчёт, проверить границы периода.'),
 ('workforce-management', 'adherence-tracking', 'punctuality-report-view', CC+'11_plan_raboty/8_3_otchety/', 'Просмотр отчёта пунктуальности WFM', 'Сопоставить показатели отчёта с критериями пунктуальности; не переносить их автоматически в API.'),
 ('workforce-management', 'adherence-tracking', 'punctuality-criteria-configure', CC+'11_plan_raboty/8_3_otchety/', 'Настройка критериев пунктуальности', 'Изменить критерий пунктуальности и проверить его использование в отчёте.', 'Настройки критериев пунктуальности'),
 ('workforce-management', 'adherence-tracking', 'punctuality-penalty-configure', CC+'11_plan_raboty/8_3_otchety/', 'Настройка штрафа за нарушение пунктуальности', 'Изменить штраф и проверить отражение настройки в оценке.', 'Настройка штрафов за нарушение пунктуальности'),
 ('workforce-management', 'shift-scheduling', 'shift-exchange-request', CC+'11_plan_raboty/8_4_obmen_smenami/', 'Создание запроса на обмен сменами', 'Создать обмен сменами и проверить появление запроса.', 'Создание обмена'),
 ('workforce-management', 'shift-scheduling', 'holiday-calendar-configure', CC+'11_plan_raboty/2_5_nastroiki/8_5_2_kalendar/', 'Настройка рабочих и праздничных дней', 'Изменить тип дня и проверить использование календаря при планировании.'),
 ('workforce-management', 'adherence-tracking', 'working-time-notification-configure', CC+'11_plan_raboty/2_5_nastroiki/8_5_1_auto_wfm/', 'Настройка уведомления о нарушении рабочего времени', 'Изменить условие уведомления и проверить его отображение в настройках.'),
 ('agent-workspace', 'agent-status', 'desktop-agent-status-change', CC+'3_glavnoe_okno_programmy/2_1_upravlenie_statusom/', 'Изменение статуса сотрудника в десктопном КЦ', 'Выбрать статус в КЦ и проверить отображаемый статус; правила API проверять отдельно.'),
 ('agent-workspace', 'agent-status', 'agent-status-configure', CC+'5_5_1_3_nastroyki/2_5_1_3_12_statusy_sotrudnikov/', 'Настройка статусов сотрудников', 'Изменить пользовательский статус и проверить сохранение настройки.'),
 ('agent-workspace', 'agent-session', 'web-agent-login', WEB+'1_avtorizatsiya/1_2_poryadok_vhoda/', 'Вход сотрудника в web-КЦ', 'Выполнить вход в web-КЦ; начальный статус устанавливать только по прочитанному источнику.'),
 ('agent-workspace', 'working-time-report', 'agent-working-time-view', CC+'10_sotrudniki/7_3_rabochee_vremya/', 'Просмотр рабочего времени сотрудника', 'Открыть отчёт сотрудника за период и сверить строки времени/статусов с описанием отчёта.'),
 ('omnichannel-contact-center', 'wallboard', 'wallboard-template-select', P+'11_wallboard/wallboard_setup/', 'Выбор шаблона Wallboard', 'Выбрать шаблон и проверить появление соответствующих показателей.', 'Настройка Wallboard по шаблону'),
 ('omnichannel-contact-center', 'wallboard', 'wallboard-custom-template-configure', P+'11_wallboard/wallboard_setup/', 'Настройка собственного шаблона Wallboard', 'Сохранить свой набор показателей и проверить его отображение.', 'Настройка «своего шаблона» показателей Wallboard'),
 ('cloud-pbx', 'mobile-account', 'mobile-account-login', P+'2_mobilnyi-lk/1_mob_lk_bystryy_start/2_dostup_k_mlk/2_2_vhod_v_mlk/', 'Вход в мобильный Личный кабинет', 'Войти в мобильный ЛК с разрешённой учётной записью; не считать это входом оператора КЦ.'),
 ('information-security', 'access-control', 'mobile-account-access-check', P+'2_mobilnyi-lk/1_mob_lk_bystryy_start/2_dostup_k_mlk/2_1_prava_dostupa/', 'Проверка прав доступа к мобильному ЛК', 'Сопоставить доступ пользователя с описанными правами.'),
 ('agent-workspace', 'ai-assistance', 'web-ai-hints-view', WEB+'12_dopolnitelnye_uslugi/12_2_panel_podskazki_ii/', 'Просмотр подсказок ИИ в web-КЦ', 'Открыть панель подсказок; пилотность и доступность проверить по статье.'),
 ('omnichannel-contact-center', 'web-dashboard', 'web-dashboard-widget-create', WEB+'2_dashboard/2_2_sozdanie_i_nastroyka_vidzheta/', 'Создание виджета web Dashboard', 'Создать виджет и проверить его присутствие на панели.'),
 ('omnichannel-contact-center', 'web-dashboard', 'web-dashboard-widget-delete', WEB+'2_dashboard/2_4_udalenie_vidzheta/', 'Удаление виджета web Dashboard', 'Удалить виджет и проверить отсутствие его на панели.'),
 ('outbound-calling', 'campaign-management', 'outbound-campaign-create', CC+'14_iskhodyashchiy_obzvon/1_4_dobavlenie_kampanii/11_4_1_s_uchastiem_sotrudnika/', 'Создание кампании с участием сотрудника', 'Создать кампанию по описанному сценарию и проверить её появление в списке.'),
 ('sms-messaging', 'bulk-sms', 'cc-message-campaign-create', CC+'17_tekstovye_rassylki/14_1_tekstovye_rassylki/', 'Создание кампании текстовой рассылки', 'Создать кампанию, проверить выбранный канал; WhatsApp и SMS не считать взаимозаменяемыми.'),
 ('speech-analytics', 'transcription', 'recognition-settings-configure', P+'4_kontrol-kachestva/8_rechevaya_analitika/1_4_vkladka_nastroyki/9_4_2_nastroiki_raspoznavaniya_zapisei/', 'Настройка распознавания записей разговоров', 'Изменить параметр распознавания и проверить сохранение настройки.'),
 ('sip-connectivity', 'sip-trunking', 'sip-trunk-delete', P+'10_sip-trunk/1_sozdanie_i_redaktirovanie_sip_trunk/3_5_udalenie/', 'Удаление SIP Trunk', 'Проверить документированные условия удаления и результат удаления.'),
 ('cloud-pbx', 'account-session', 'account-auto-logout-configure', P+'1_virtualnaya-ats-i-lichnyi-kabinet/10_Vhod/4_kak_nastroit_avtomaticheskii_vykhod_iz_sistemy_dlya_bezopasnosti/', 'Настройка автоматического выхода из ЛК', 'Проверить настройку автоматического выхода; не приравнивать её к сессии КЦ.'),
 ('call-routing', 'overflow-routing', 'failed-call-behavior-configure', P+'1_virtualnaya-ats-i-lichnyi-kabinet/1_4_obrabotka_zvonkov/4_4_3_nastroyki_dozvona_i_soobshcheniy_po_umolchaniyu/', 'Настройка поведения при недозвоне', 'Проверить выбор настройки недозвона по статье.'),
 ('unified-communications', 'presence-status', 'talker-presence-change', P+'7_mango-talker/3_userguide_mtalker_4mobile/14_upravlenie_profilem_polzovatelya/smena_statusa_polzovatelya/', 'Изменение статуса Mango Talker', 'Проверить отображаемый статус Talker; связь со статусом КЦ не предполагается.'),
 ('unified-communications', 'file-sharing', 'talker-shared-files-view', P+'7_mango-talker/3_userguide_mtalker_4mobile/10_administrirovanie_obschego_chata_ili_kanala/prosmotr_obschih_faylov/', 'Просмотр общих файлов Talker', 'Проверить доступ к списку общих файлов; файлы в аудите не скачиваются.'),
 ('voice-bot', 'intent-dictionary', 'nlu-dictionary-create', P+'9_roboty-i-ai-roboty/7_ai_roboty/12_1_sozdanie_ai_robota/', 'Создание справочника NLU', 'Проверить создание справочника по описанному сценарию.'),
 ('voice-bot', 'http-action', 'robot-http-request-configure', P+'9_roboty-i-ai-roboty/4_konstruktor_skriptov/5_6_blok_otpravit_http_zapros/', 'Настройка HTTP-запроса в скрипте робота', 'Проверить параметры блока HTTP-запроса; не переносить их в публичный API.'),
 ('chatbot', 'dialog-analytics', 'chatbot-script-statistics-view', P+'9_roboty-i-ai-roboty/3_chat_boty/4_3_statistika_po_skriptu_chat_bota/', 'Просмотр статистики скрипта чат-бота', 'Проверить доступные показатели статистики скрипта.'),
 ('speech-analytics', 'keyword-detection', 'speech-topic-create', P+'8_rechevaya-analitika-i-skoring/1_rechevaya-analitika/2_avtomaticheskoe_tegirovanie_razgovorov/3_2_sozdanie_i_nastroyka_svoikh_tematik/', 'Создание своей тематики анализа разговоров', 'Проверить создание тематики; алгоритм классификации не выводится из заголовка.'),
 ('speech-analytics', 'text-communication-analysis', 'text-communications-list-view', P+'8_rechevaya-analitika-i-skoring/1_rechevaya-analitika/6_poisk_i_analiz_razgovorov/2_2_analitika_tekstovykh_kommunikatsiy/2_2_2_prosmotr_spiska_kommunikatsiy/', 'Просмотр списка текстовых коммуникаций', 'Проверить состав списка по статье.'),
 ('quality-management', 'scorecards', 'quality-scorecard-create', P+'4_kontrol-kachestva/2_nastroyka_blankov_otsenki/2_1_sozdanie_blanka_otsenki/', 'Создание бланка оценки', 'Проверить создание бланка оценки.'),
 ('quality-management', 'scorecards', 'quality-score-weights-configure', P+'4_kontrol-kachestva/2_nastroyka_blankov_otsenki/2_3_nastroyka_shkaly_otsenok_i_vesa_kriteriev/', 'Настройка шкалы оценок и весов критериев', 'Проверить сохранение весов и шкалы; расчёт сверять с таблицей источника.'),
 ('quality-management', 'evaluation-workflow', 'quality-appeal-enable', P+'4_kontrol-kachestva/2_nastroyka_blankov_otsenki/2_4_nastroyka_apellyatsii/', 'Настройка возможности апелляции', 'Проверить доступность подачи апелляции при выбранной настройке.'),
 ('call-tracking', 'dynamic-number-pool', 'calltracking-widget-create', P+'5_kolltreking-i-analitika/12_ustanovka_vidzheta_na_sayte/3_kakynastroitykodyvidzheta/', 'Создание кода виджета Коллтрекинга', 'Проверить создание кода; правила подмены номера читать отдельно.'),
 ('omnichannel-messaging', 'channel-configuration', 'mdialogi-channel-configure', P+'6_mango-dialogi/3_nastroyka_vidzheta_mkch/1_nastroyka_vidzheta_mkch/', 'Настройка каналов МангоДиалогов', 'Проверить выбор канала и его настройки по статье.'),
 ('messenger-marketing', 'whatsapp-templates', 'whatsapp-template-create', P+'6_mango-dialogi/3_nastroyka_vidzheta_mkch/12_shablonyywhatsapp/', 'Создание HSM-шаблона WhatsApp', 'Проверить создание черновика HSM-шаблона; регистрацию и доступность канала читать отдельно.', 'Создание HSM-шаблона'),
 ('report-builder', 'report-authoring', 'report-create', P+'12_konstruktor-otchetov/1_otchety/dobavlenie_otcheta/', 'Добавление отчёта в Конструкторе', 'Проверить появление нового отчёта.'),
 ('report-builder', 'report-authoring', 'report-view', P+'12_konstruktor-otchetov/1_otchety/prosmotr_otcheta/', 'Просмотр отчёта в Конструкторе', 'Проверить отображение выбранного отчёта.'),
 ('report-builder', 'dataset-modeling', 'custom-parameter-create', P+'12_konstruktor-otchetov/2_dannye/1_parametry/sozdanie_polzovatelskogo_parametra/', 'Создание пользовательского параметра отчёта', 'Проверить появление параметра в Конструкторе.'),
 ('report-builder', 'dataset-modeling', 'report-entity-create', P+'12_konstruktor-otchetov/2_dannye/2_suschnosti/sozdanie_suschnosti/', 'Создание сущности отчёта', 'Проверить появление сущности по сценарию статьи.'),
 ('platform-integration', 'crm-connectors', 'amocrm-employee-mapping', 'https://www.mango-office.ru/support/4_integratsii/1_vse-integratsii/3_amocrm/1_nachalo_raboty_s_integratsiey/05_shag_5_sopostavlenie_sotrudnikov_virtualnoy_ats_i_amocrm/1_kak_nastroit_sopostavlenie_sotrudnikov/', 'Сопоставление сотрудников ВАТС и amoCRM', 'Проверить пару сотрудников именно amoCRM; BPMSoft не является доказательством этой операции.'),
 ('platform-integration', 'crm-connectors', 'bpmsoft-cc-status-enable', 'https://www.mango-office.ru/support/4_integratsii/1_vse-integratsii/5_bpm-soft/2_dopolnitelnye_nastroyki_integratsii/4_4_dopolnitelnye_nastroyki_integratsii/7_ispolzovat_statusy_kontakt_tsentra/kak_vklyuchit_nastroyku_ispolzovat_statusy_kontakt_tsentra/', 'Включение статусов КЦ в BPMSoft', 'Проверить настройку только в интеграции BPMSoft.'),
 ('platform-integration', 'crm-connectors', 'bpmsoft-cc-status-change', 'https://www.mango-office.ru/support/4_integratsii/1_vse-integratsii/5_bpm-soft/2_dopolnitelnye_nastroyki_integratsii/4_4_dopolnitelnye_nastroyki_integratsii/7_ispolzovat_statusy_kontakt_tsentra/statusy_kontakt_tsentra_v_interfeyse_bpmsoft/', 'Изменение статуса КЦ через BPMSoft', 'Проверить изменение статуса в BPMSoft; свойства других CRM требуют отдельного источника.'),
 ('agent-workspace', 'agent-status', 'cc-api-user-status-set', STATUS_API+'4_4_1_2_smena_statusa_polzovatelya/', 'Смена статуса пользователя через API КЦ', 'Проверить статус пользователя, условия status/status_alias и ограничение offline строго по статье.'),
 ('agent-workspace', 'agent-session', 'cc-api-session-status-set', STATUS_API+'4_4_1_3_smena_statusa_sessii_polzovatelya/', 'Смена статуса сессии через API КЦ', 'Проверить статус выбранной сессии; не смешивать с методом статуса пользователя.'),
 ('agent-workspace', 'agent-status', 'cc-api-status-list', STATUS_API+'4_4_1_4_statusy_na_produkte/', 'Получение списка статусов на продукте КЦ', 'Проверить поля ответа списка статусов по таблице.'),
 ('agent-workspace', 'agent-session', 'cc-api-presence-get', STATUS_API+'4_4_1_3_statusy_polzovateley_produkta/', 'Получение статусов пользователей продукта', 'Проверить session_types и различия полей статуса КЦ и Talker по тексту статьи.'),
 ('information-security', 'access-control', 'role-create', ROLES+'3_upravlenie_rolyami/sozdanie_roli/', 'Создание пользовательской роли', 'Проверить создание роли и исходный набор прав; условия системных ролей читать отдельно.'),
 ('information-security', 'access-control', 'role-delete', ROLES+'3_upravlenie_rolyami/udalenie_roli/', 'Удаление пользовательской роли', 'Проверить удаление пользовательской роли и запрет для системной по статье.'),
 ('information-security', 'access-control', 'role-permission-configure', ROLES+'4_nastroyka_prav_dostupa_roli/', 'Настройка прав доступа роли', 'Проверить право и область влияния; визуальные настройки требуют дополнительной проверки.'),
 ('omnichannel-messaging', 'conversation-session', 'mdialogi-session-create', MD_API+'sozdat_novuyu_sessiyu/', 'Создание новой сессии МангоДиалогов через API', 'Проверить ответ создания сессии; не переносить семантику сессии на КЦ.'),
 ('omnichannel-messaging', 'conversation-session', 'mdialogi-session-close', MD_API+'zakryt_sessiyu/', 'Закрытие сессии МангоДиалогов через API', 'Проверить результат закрытия сессии по статье.'),
]


def main():
    public = BASE.parents[1]/'docs/taxonomy/portal-audit.jsonl'
    records = ([json.loads(s) for s in public.read_text().splitlines()] if public.exists() else
               [json.loads(p.read_text()) for p in (BASE/'cache').glob('*.json')])
    pages = {r['url']: r for r in records}
    additions = []
    for cap, feature, function, url, name, verification, *heading in SELECTION:
        page = pages[url]
        row = {'capability': cap, 'feature': feature, 'feature_name': feature,
               'function': function, 'name': name, 'url': url, 'title': page['title'],
               'verification': verification}
        if heading:
            assert any(heading[0] in h['text'] for h in page['headings']), row
            row['heading'] = heading[0]
        additions.append(row)
    (BASE/'additions.json').write_text(json.dumps(additions, ensure_ascii=False, indent=2)+'\n')
    print('Curated atomic operations:', len(additions))


if __name__ == '__main__':
    main()
