---
status: draft
version: 1.0
updated: 2026-06-21
ai-generated: true
type: analysis
scope: mango-taxonomy-registry-inventory
issue: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/170"
related_artifacts:
  - "kb/mango-taxonomy/mango-registry.json"
  - "kb/mango-taxonomy/mango-registry.schema.json"
  - "kb/mango-taxonomy/README.md"
  - "scripts/validate_issue_170_mango_registry.py"
  - "standards/mango-taxonomy-standard.md"
  - "standards/decisions/ADR-012-mango-taxonomy.md"
  - "experiments/cascade_fill.py"
  - "experiments/gen_inventory_doc.py"
---

# Инвентаризация Mango-реестра и перевод в JSON (issue #170)

> Документ сгенерирован из живого реестра скриптом [`experiments/gen_inventory_doc.py`](../../experiments/gen_inventory_doc.py) и отражает [`kb/mango-taxonomy/mango-registry.json`](../../kb/mango-taxonomy/mango-registry.json) один-в-один. Перегенерируйте после изменения реестра.

## 1. Резюме

Issue #170 требовал: (1) свести три YAML-файла Mango-реестра в единый JSON, (2) устранить дублирование (отдельный crosswalk `product-mapping.yaml`), (3) дозаполнить иерархию `Продукт → Сервис → Модуль → Функция` из реальной документации сверху вниз, (4) добавить JSON Schema, (5) обеспечить ссылочную целостность с Industry-реестром и (6) подготовить этот аналитический документ с полными списками сущностей, сравнением со старой структурой и фиксацией пробелов.

Итог — единый файл [`kb/mango-taxonomy/mango-registry.json`](../../kb/mango-taxonomy/mango-registry.json) (версия `1.0.0`) со следующим наполнением:

| Массив | Уровень | Кол-во |
| --- | --- | ---: |
| `official_products` | official-product | 10 |
| `products` | product | 8 |
| `internal_services` | service | 32 |
| `modules` | module | 61 |
| `functions` | function | 160 |

Все нижние пороги стандарта превышены, число верхнеуровневых продуктов сохранено ровно равным восьми (ADR-012). Реестр проходит проектный валидатор, JSON Schema (draft 2020-12) и сквозную проверку целостности «родитель ↔ ребёнок».

## 2. Метод и источник истины

**Источник истины** — извлечённые руководства в [`kb/mango-product-docs/processed/`](../../kb/mango-product-docs/processed/). Каждая добавленная сущность привязана к проверенной секции (`evidence_refs` указывает на реальный `*.md`).

**Запрет на выдумку.** Evidence резолвится по паре «(каталог, номер секции)» глоб-ом `sections/NN-*.md`; номер, который не находит файл, не попадает в реестр, а фиксируется как пробел в этом документе. Поэтому неверный slug физически не может «протечь» в данные.

**Наследование выравнивания.** Новая сущность копирует *primary* `industry_alignment` своего родителя (`industry_ref` и `facets` — дословно). Это гарантирует, что каждая ссылка резолвится против [`kb/industry-taxonomy/reference-taxonomy.json`](../../kb/industry-taxonomy/reference-taxonomy.json) и что не выдумываются новые отраслевые узлы. Для функций уровень `function` из `industry_ref` отбрасывается (в текущих данных это no-op).

**Использованные корпуса** (число различных секций/файлов, на которые ссылается реестр):

| Корпус (processed/) | Цитируемых файлов |
| --- | ---: |
| `mango-lk-manual` | 29 |
| `mtalker` | 28 |
| `mango-cc-manual` | 24 |
| `vpbx-api` | 13 |
| `mdialogi-api` | 9 |
| `quality-managment` | 7 |
| `speech-analytics` | 6 |
| `lk-vats-sso` | 5 |
| `Rolevaya-model-vats` | 4 |
| `integration_1c` | 4 |
| `integration_amocrm` | 4 |
| `integration-bitrix24` | 3 |
| `wallboard` | 2 |
| `sip-trunk` | 1 |

## 3. Сравнение со старой YAML-структурой

До issue #170 реестр состоял из трёх файлов. Их содержимое свёрнуто в один JSON:

| Старый файл | Что содержал | Судьба |
| --- | --- | --- |
| `official-products.yaml` | 10 официальных продуктов | перенесён в массив `official_products` |
| `internal-registry.yaml` | 8 продуктов / 32 сервисов / 32 модулей / 64 функций | стал основой единого JSON, дозаполнен |
| `product-mapping.yaml` | 146 записей crosswalk к Industry Taxonomy | **удалён**, выравнивания внесены в `maps_to.industry_alignment` каждой сущности |

Crosswalk содержал ровно 146 записей — это 10 + 8 + 32 + 32 + 64 = 146, то есть по одной записи на каждую сущность всех пяти уровней. Отдельный mapping-файл дублировал данные и был источником рассинхрона; теперь выравнивание живёт внутри сущности, и дублирования нет.

**Изменение количеств (старое → новое):**

| Уровень | Старое | Новое | Δ |
| --- | ---: | ---: | ---: |
| official_products | 10 | 10 | +0 |
| products | 8 | 8 | +0 |
| internal_services | 32 | 32 | +0 |
| modules | 32 | 61 | +29 |
| functions | 64 | 160 | +96 |

**Возможное устаревание.** Ни одна сущность из старых YAML не удалена — все идентификаторы сохранены 1:1, переопределения верхнеуровневых продуктов (ADR-012) не было. Признаков устаревания не обнаружено.

## 4. Полный реестр: дерево `Продукт → Сервис → Модуль → Функция`

Знаком **`+`** отмечены сущности, добавленные дозаполнением в issue #170; остальные перенесены из `internal-registry.yaml`. В скобках у функции — `function_type`/`interaction_surface`.

### Mango Virtual PBX — `mango-virtual-pbx`

_Сервисов: 4._

- **Входящая маршрутизация ВАТС** — `vats-inbound-routing-service` _(модулей: 3)_
  - **Сценарии входящих звонков** — `vats-inbound-scenarios-module` _(функций: 3)_
    - Принять входящий звонок по сценарию — `receive-inbound-call-through-scenario` (business/system-rule)
    - Настроить сценарий входящего звонка — `configure-inbound-call-scenario` (configuration/admin-ui)
    - + Настроить переадресацию по номеру клиента — `configure-callback-forwarding` (configuration/admin-ui)
  - + **Чёрный и белый списки номеров** — `vats-blacklist-whitelist-module` _(функций: 2)_
    - + Добавить номер в чёрный список — `add-number-to-blacklist` (configuration/admin-ui)
    - + Добавить номер в белый список — `add-number-to-whitelist` (configuration/admin-ui)
  - + **Маршрутизация по расписанию** — `vats-time-based-routing-module` _(функций: 2)_
    - + Настроить маршрутизацию по рабочему времени — `configure-time-based-routing` (configuration/admin-ui)
    - + Настроить расписание праздничных дней — `configure-holiday-schedule` (configuration/admin-ui)
- **Голосовое меню ВАТС** — `vats-ivr-service` _(модулей: 1)_
  - **Голосовое меню** — `vats-ivr-menu-module` _(функций: 4)_
    - Проиграть голосовое меню звонящему — `play-ivr-menu-to-caller` (business/system-rule)
    - Изменить ветку голосового меню — `edit-ivr-menu-branch` (configuration/admin-ui)
    - + Настроить ветви голосового меню — `configure-ivr-menu-branches` (configuration/admin-ui)
    - + Включить распознавание речи в меню — `enable-speech-recognition-menu` (configuration/admin-ui)
- **Управление номерами ВАТС** — `vats-number-management-service` _(модулей: 1)_
  - **Подключённые номера** — `vats-connected-numbers-module` _(функций: 2)_
    - Назначить маршрут подключённому номеру — `assign-connected-number-route` (configuration/admin-ui)
    - Открыть список подключённых номеров — `view-connected-number-list` (ui-action/admin-ui)
- **Записи и история звонков ВАТС** — `vats-recording-history-service` _(модулей: 2)_
  - **Запись разговоров** — `vats-call-recording-module` _(функций: 3)_
    - Включить правило записи разговора — `enable-call-recording-rule` (configuration/admin-ui)
    - Прослушать запись разговора — `play-call-recording` (ui-action/admin-ui)
    - + Настроить режимы записи — `configure-recording-rules` (configuration/admin-ui)
  - + **Управление голосовой почтой** — `vats-voicemail-management-module` _(функций: 2)_
    - + Включить расшифровку голосовой почты — `enable-voicemail-transcription` (configuration/admin-ui)
    - + Настроить уведомления о голосовой почте — `configure-voicemail-notification-actions` (configuration/admin-ui)

### Mango Contact Center — `mango-contact-center`

_Сервисов: 4._

- **Рабочее место оператора КЦ** — `cc-agent-workspace-service` _(модулей: 5)_
  - **Обработка обращений оператором** — `cc-agent-call-handling-module` _(функций: 3)_
    - Принять обращение из очереди — `accept-queue-interaction` (business/operator-ui)
    - Изменить статус оператора — `set-agent-status` (ui-action/operator-ui)
    - + Завершить поствызывную обработку — `complete-after-call-work` (business/operator-ui)
  - + **Удержание вызовов** — `cc-call-hold-module` _(функций: 2)_
    - + Поставить вызов на удержание — `hold-call` (business/operator-ui)
    - + Снять вызов с удержания — `resume-held-call` (business/operator-ui)
  - + **Перевод вызовов** — `cc-call-transfer-module` _(функций: 2)_
    - + Перевести вызов с консультацией — `transfer-call-with-consultation` (business/operator-ui)
    - + Перевести вызов без консультации — `transfer-call-without-consultation` (business/operator-ui)
  - + **Организация конференций** — `cc-agent-conferencing-module` _(функций: 2)_
    - + Организовать конференц-вызов — `initiate-conference-call` (business/operator-ui)
    - + Добавить участника в конференцию — `add-participant-to-conference` (business/operator-ui)
  - + **Запись разговоров КЦ** — `cc-call-recording-module` _(функций: 2)_
    - + Включить запись разговоров — `enable-cc-call-recording` (configuration/admin-ui)
    - + Получить доступ к записи разговора — `access-cc-call-recording` (business/operator-ui)
- **Маршрутизация обращений КЦ** — `cc-interaction-routing-service` _(модулей: 1)_
  - **Очереди и правила распределения** — `cc-queue-routing-module` _(функций: 3)_
    - Распределить обращение в очередь — `route-interaction-to-queue` (business/system-rule)
    - Настроить правило очереди — `configure-queue-routing-rule` (configuration/admin-ui)
    - + Перевести обращение на оператора — `transfer-interaction-to-agent` (business/operator-ui)
- **Исходящие кампании КЦ** — `cc-outbound-campaign-service` _(модулей: 1)_
  - **Кампании исходящего обзвона** — `cc-outbound-campaign-module` _(функций: 3)_
    - Запустить исходящую кампанию — `start-outbound-campaign` (business/operator-ui)
    - Настроить исходящую кампанию — `configure-outbound-campaign` (configuration/admin-ui)
    - + Настроить набор с участием сотрудника — `configure-agent-assisted-dialing` (configuration/admin-ui)
- **Супервизорский контроль и WFM** — `cc-supervisor-wfm-service` _(модулей: 2)_
  - **Планирование и супервизорский мониторинг** — `cc-supervisor-wfm-module` _(функций: 4)_
    - Просмотреть нагрузку операторов — `monitor-agent-workload` (ui-action/operator-ui)
    - Настроить график входящих обращений — `configure-workforce-schedule` (configuration/admin-ui)
    - + Настроить автоматические действия WFM — `configure-wfm-auto-actions` (configuration/admin-ui)
    - + Спланировать прогноз входящих — `schedule-inbound-forecast` (configuration/admin-ui)
  - + **Контроль и прослушивание операторов** — `cc-supervisor-monitoring-module` _(функций: 2)_
    - + Контролировать операторов в реальном времени — `monitor-agents-realtime` (business/operator-ui)
    - + Прослушать разговор оператора — `listen-to-agent-conversation` (business/operator-ui)

### Mango Digital Communications — `mango-digital-communications`

_Сервисов: 4._

- **Группы текстовых каналов** — `digital-channel-group-service` _(модулей: 1)_
  - **Группы каналов коммуникации** — `digital-channel-group-module` _(функций: 3)_
    - Отправить сообщение в цифровом канале — `send-channel-message` (business/operator-ui)
    - Настроить группу каналов — `configure-channel-group` (configuration/admin-ui)
    - + Включить чат-бота для группы каналов — `enable-chatbot-for-channel-group` (configuration/admin-ui)
- **Чат на сайте** — `website-chat-service` _(модулей: 1)_
  - **Виджет чата на сайте** — `website-chat-widget-module` _(функций: 2)_
    - Принять обращение из чата сайта — `receive-website-chat` (business/operator-ui)
    - Установить код виджета чата — `install-website-chat-widget` (configuration/admin-ui)
- **Мессенджер-каналы** — `messenger-channel-service` _(модулей: 2)_
  - **Подключение мессенджеров** — `messenger-channel-connector-module` _(функций: 2)_
    - Подключить Telegram-канал — `connect-telegram-channel` (configuration/admin-ui)
    - Ответить в диалоге мессенджера — `reply-to-messenger-dialog` (business/operator-ui)
  - + **Каналы соцсетей и мессенджеров** — `social-messenger-channels-module` _(функций: 3)_
    - + Подключить канал WhatsApp — `connect-whatsapp-channel` (configuration/admin-ui)
    - + Подключить канал ВКонтакте — `connect-vkontakte-channel` (configuration/admin-ui)
    - + Подключить канал Avito — `connect-avito-channel` (configuration/admin-ui)
- **Dialog API** — `dialog-api-messaging-service` _(модулей: 3)_
  - **API сообщений Dialogi** — `dialog-api-message-module` _(функций: 2)_
    - Отправить сообщение через Dialog API — `send-dialog-api-message` (business/api)
    - Получить событие Dialog API — `receive-dialog-api-event` (business/webhook)
  - + **Управление сессиями Dialog API** — `dialog-api-session-management-module` _(функций: 5)_
    - + Взять сессию диалога в работу — `take-dialog-session` (business/api)
    - + Перевести сессию на другого сотрудника — `transfer-dialog-session` (business/api)
    - + Закрыть сессию диалога — `close-dialog-session` (business/api)
    - + Получить список активных сессий — `get-active-dialog-sessions` (business/api)
    - + Загрузить историю чата — `get-dialog-chat-history` (business/api)
  - + **Вебхуки Dialog API** — `dialog-api-webhook-module` _(функций: 3)_
    - + Получить вебхук о новом сообщении — `receive-new-message-webhook` (business/webhook)
    - + Получить вебхук о взятии сессии в работу — `receive-session-taken-webhook` (business/webhook)
    - + Получить вебхук об ожидающей сессии — `receive-session-waiting-webhook` (business/webhook)

### Mango Talker — `mango-talker`

_Сервисов: 4._

- **Софтфон Mango Talker** — `talker-softphone-service` _(модулей: 3)_
  - **Звонки в Talker** — `talker-softphone-module` _(функций: 2)_
    - Позвонить сотруднику из Talker — `call-colleague-in-talker` (business/end-user-ui)
    - Ответить на входящий звонок в Talker — `answer-talker-call` (business/end-user-ui)
  - + **Управление вызовом в Mango Talker** — `talker-call-control-module` _(функций: 4)_
    - + Поставить вызов на удержание — `hold-talker-call` (business/end-user-ui)
    - + Перевести вызов на другого сотрудника — `transfer-talker-call` (business/end-user-ui)
    - + Выключить микрофон — `mute-talker-microphone` (ui-action/end-user-ui)
    - + Записать разговор — `record-talker-call` (business/end-user-ui)
  - + **Статус присутствия и уведомления** — `talker-presence-status-module` _(функций: 2)_
    - + Сменить статус присутствия пользователя — `change-talker-presence-status` (ui-action/end-user-ui)
    - + Отключить показ уведомлений из всех чатов и каналов — `disable-talker-notifications` (ui-action/end-user-ui)
- **Командные чаты Mango Talker** — `talker-team-chat-service` _(модулей: 3)_
  - **Чаты и каналы Talker** — `talker-team-chat-module` _(функций: 2)_
    - Отправить сообщение в Talker — `send-talker-chat-message` (business/end-user-ui)
    - Создать чат или канал Talker — `create-talker-chat-channel` (configuration/end-user-ui)
  - + **Операции с сообщениями Mango Talker** — `talker-message-operations-module` _(функций: 4)_
    - + Редактировать отправленное сообщение — `edit-talker-message` (ui-action/end-user-ui)
    - + Отменить отправленное сообщение — `cancel-talker-message` (ui-action/end-user-ui)
    - + Процитировать сообщение — `quote-talker-message` (ui-action/end-user-ui)
    - + Найти сообщение в истории чата — `search-talker-chat-history` (ui-action/end-user-ui)
  - + **Обмен файлами в Mango Talker** — `talker-file-sharing-module` _(функций: 2)_
    - + Отправить файл — `send-talker-file` (ui-action/end-user-ui)
    - + Отправить изображение — `send-talker-image` (ui-action/end-user-ui)
- **Видео и конференции Talker** — `talker-video-meeting-service` _(модулей: 2)_
  - **Видео и конференции** — `talker-video-meeting-module` _(функций: 2)_
    - Начать групповой видеозвонок — `start-talker-video-call` (business/end-user-ui)
    - Присоединиться к конференции Talker — `join-talker-conference-room` (business/end-user-ui)
  - + **Видео-эффекты и демонстрация в Mango Talker** — `talker-video-effects-module` _(функций: 3)_
    - + Включить демонстрацию экрана — `share-talker-screen` (ui-action/end-user-ui)
    - + Изменить фоновые эффекты — `change-talker-background` (ui-action/end-user-ui)
    - + Поднять руку — `raise-hand-in-talker` (ui-action/end-user-ui)
- **Контакты и история Talker** — `talker-contact-history-service` _(модулей: 2)_
  - **Контакты и журнал Talker** — `talker-contact-history-module` _(функций: 2)_
    - Открыть карточку контакта Talker — `open-talker-contact-card` (ui-action/end-user-ui)
    - Позвонить контакту из истории — `call-contact-from-history` (business/end-user-ui)
  - + **Избранное и группы контактов** — `talker-favorites-groups-module` _(функций: 4)_
    - + Добавить контакт в избранное — `add-talker-favorite` (ui-action/end-user-ui)
    - + Удалить контакт из избранного — `remove-talker-favorite` (ui-action/end-user-ui)
    - + Открыть список избранного — `view-talker-favorites` (ui-action/end-user-ui)
    - + Фильтровать контакты по группам — `filter-talker-contact-groups` (ui-action/end-user-ui)

### Mango AI Speech and Quality — `mango-ai-speech-quality`

_Сервисов: 4._

- **Речевая аналитика** — `speech-analytics-service` _(модулей: 3)_
  - **Тематики речевой аналитики** — `speech-analytics-topic-module` _(функций: 2)_
    - Распознать речь в записи разговора — `recognize-recorded-call-speech` (business/background-job)
    - Настроить тематику речевой аналитики — `configure-speech-topic` (configuration/admin-ui)
  - + **Поиск и прослушивание разговоров** — `speech-analytics-search-module` _(функций: 2)_
    - + Найти разговоры по содержанию — `search-conversations-by-content` (business/admin-ui)
    - + Прослушать найденную запись разговора — `listen-to-found-recording` (business/admin-ui)
  - + **Тегирование разговоров** — `speech-analytics-tagging-module` _(функций: 2)_
    - + Проставить теги разговору — `tag-conversation` (business/admin-ui)
    - + Настроить ИИ-тегирование разговоров — `configure-ai-tagging` (configuration/admin-ui)
- **AI-конспекты разговоров** — `conversation-summary-service` _(модулей: 2)_
  - **Конспекты разговоров** — `conversation-summary-module` _(функций: 2)_
    - Сформировать конспект разговора — `generate-call-summary` (business/background-job)
    - Открыть конспект разговора — `view-call-summary` (ui-action/admin-ui)
  - + **ИИ-помощник оператора** — `ai-assistant-module` _(функций: 2)_
    - + Создать ИИ-помощника — `create-ai-assistant` (configuration/admin-ui)
    - + Настроить ИИ-помощника — `configure-ai-assistant` (configuration/admin-ui)
- **Контроль качества и чек-листы** — `quality-checklist-service` _(модулей: 3)_
  - **Чек-листы качества** — `quality-checklist-module` _(функций: 2)_
    - Оценить разговор по чек-листу — `evaluate-call-by-checklist` (business/admin-ui)
    - Настроить чек-лист качества — `configure-quality-checklist` (configuration/admin-ui)
  - + **Апелляции по оценке качества** — `quality-appeal-module` _(функций: 3)_
    - + Подать апелляцию на оценку — `submit-quality-appeal` (business/operator-ui)
    - + Обработать апелляцию контролёром — `review-quality-appeal` (business/operator-ui)
    - + Настроить правила апелляций — `configure-appeal-settings` (configuration/admin-ui)
  - + **Рандомайзер выборки звонков** — `quality-call-randomizer-module` _(функций: 2)_
    - + Настроить рандомайзер выборки — `configure-call-randomizer` (configuration/admin-ui)
    - + Сформировать случайную выборку для проверки — `select-random-calls-for-review` (business/admin-ui)
- **Голосовой робот** — `voice-robot-service` _(модулей: 1)_
  - **Сценарии голосового робота** — `voice-robot-scenario-module` _(функций: 2)_
    - Запустить голосовой диалог робота — `run-voice-robot-dialog` (business/system-rule)
    - Настроить сценарий голосового робота — `configure-voice-robot-scenario` (configuration/admin-ui)

### Mango Marketing Analytics — `mango-marketing-analytics`

_Сервисов: 4._

- **Атрибуция коллтрекинга** — `calltracking-attribution-service` _(модулей: 2)_
  - **Атрибуция рекламных источников** — `calltracking-attribution-module` _(функций: 3)_
    - Привязать звонок к рекламному источнику — `attribute-call-to-ad-source` (business/background-job)
    - Настроить номер коллтрекинга — `configure-calltracking-number` (configuration/admin-ui)
    - + Настроить виджет коллтрекинга — `setup-calltracking-widget` (configuration/admin-ui)
  - + **Статический коллтрекинг** — `static-calltracking-module` _(функций: 2)_
    - + Настроить статический коллтрекинг — `setup-static-calltracking` (configuration/admin-ui)
    - + Открыть отчёт статического коллтрекинга — `view-static-calltracking-report` (business/admin-ui)
- **Сквозная аналитика** — `end-to-end-analytics-service` _(модулей: 2)_
  - **Сквозные отчёты** — `end-to-end-analytics-module` _(функций: 2)_
    - Связать звонок с воронкой продаж — `join-call-and-sales-funnel` (business/background-job)
    - Открыть отчёт сквозной аналитики — `open-end-to-end-analytics-report` (ui-action/admin-ui)
  - + **Цели и интеграции веб-аналитики** — `analytics-goals-integration-module` _(функций: 2)_
    - + Интегрировать Google Analytics и Яндекс.Метрику — `integrate-web-analytics` (configuration/admin-ui)
    - + Настроить цель по событию — `configure-event-goal` (configuration/admin-ui)
- **Отчёты и дашборды** — `reporting-dashboard-service` _(модулей: 1)_
  - **Конструктор и просмотр отчётов** — `reporting-dashboard-module` _(функций: 4)_
    - Сформировать аналитический отчёт — `build-analytics-report` (business/background-job)
    - Выбрать виджет дашборда — `select-dashboard-widget` (ui-action/admin-ui)
    - + Построить отчёт контакт-центра — `build-cc-report` (business/admin-ui)
    - + Открыть панель показателей — `view-cc-performance-panel` (business/operator-ui)
- **Wallboard-мониторинг** — `wallboard-monitoring-service` _(модулей: 1)_
  - **Wallboard-виджеты** — `wallboard-monitoring-module` _(функций: 4)_
    - Показать виджет Wallboard — `display-wallboard-widget` (business/end-user-ui)
    - Настроить виджет Wallboard — `configure-wallboard-widget` (configuration/admin-ui)
    - + Выбрать шаблон Wallboard — `select-wallboard-template` (configuration/admin-ui)
    - + Задать пороги метрик Wallboard — `set-wallboard-metric-threshold` (configuration/admin-ui)

### Mango Platform Integrations — `mango-platform-integrations`

_Сервисов: 4._

- **ВАТС Open API** — `vpbx-open-api-service` _(модулей: 1)_
  - **API Виртуальной АТС** — `vpbx-open-api-module` _(функций: 4)_
    - Инициировать звонок через API ВАТС — `initiate-vpbx-api-call` (business/api)
    - Настроить webhook ВАТС — `configure-vpbx-webhook` (configuration/api)
    - + Завершить вызов через API — `hangup-call-via-api` (business/api)
    - + Отправить SMS через API — `send-sms-via-api` (business/api)
- **Contact Center API** — `contact-center-api-service` _(модулей: 1)_
  - **API Контакт-центра** — `contact-center-api-module` _(функций: 3)_
    - Создать задачу Контакт-центра через API — `create-contact-center-task-api` (business/api)
    - Получить событие Контакт-центра через webhook — `receive-contact-center-event-webhook` (business/webhook)
    - + Получить статистику вызовов через API — `get-call-statistics-via-api` (business/api)
- **CRM и ERP-интеграции** — `crm-erp-integration-service` _(модулей: 4)_
  - **Коннекторы CRM и ERP** — `crm-erp-integration-module` _(функций: 2)_
    - Синхронизировать карточку звонка с CRM — `sync-crm-call-card` (business/background-job)
    - Настроить CRM-интеграцию — `configure-crm-integration` (configuration/admin-ui)
  - + **Коннектор Битрикс24** — `bitrix24-connector-module` _(функций: 2)_
    - + Настроить интеграцию с Битрикс24 — `configure-bitrix24-integration` (configuration/admin-ui)
    - + Автоматически создавать лид при звонке — `auto-create-bitrix24-lead` (business/system-rule)
  - + **Коннектор amoCRM** — `amocrm-connector-module` _(функций: 3)_
    - + Настроить интеграцию с amoCRM — `configure-amocrm-integration` (configuration/admin-ui)
    - + Показать карточку контакта при входящем звонке — `pop-amocrm-card-on-incoming-call` (business/system-rule)
    - + Позвонить из карточки amoCRM — `click-to-call-from-amocrm` (business/end-user-ui)
  - + **Коннектор 1С** — `onec-connector-module` _(функций: 3)_
    - + Настроить интеграцию с 1С — `configure-onec-integration` (configuration/admin-ui)
    - + Показать карточку контакта 1С при входящем звонке — `pop-onec-card-on-incoming-call` (business/system-rule)
    - + Позвонить из 1С — `click-to-call-from-onec` (business/end-user-ui)
- **Webhook-события** — `webhook-event-service` _(модулей: 1)_
  - **Webhook endpoints** — `webhook-event-module` _(функций: 3)_
    - Передать событие звонка во внешний webhook — `send-call-event-webhook` (business/webhook)
    - Настроить endpoint webhook — `configure-webhook-endpoint` (configuration/admin-ui)
    - + Получить вебхук-уведомление о вызове — `receive-call-notification-webhook` (business/webhook)

### Mango Security and Access — `mango-security-access`

_Сервисов: 4._

- **Ролевое управление доступом** — `role-access-management-service` _(модулей: 2)_
  - **Роли и права доступа** — `role-access-management-module` _(функций: 2)_
    - Назначить роль пользователю — `assign-user-role` (configuration/admin-ui)
    - Просмотреть права роли — `view-role-permissions` (ui-action/admin-ui)
  - + **Управление пользовательскими ролями** — `custom-role-management-module` _(функций: 3)_
    - + Создать пользовательскую роль — `create-custom-role` (configuration/admin-ui)
    - + Скопировать роль — `copy-custom-role` (configuration/admin-ui)
    - + Удалить роль — `delete-custom-role` (configuration/admin-ui)
- **SSO и идентификация** — `sso-identity-service` _(модулей: 2)_
  - **SSO-подключение** — `sso-identity-module` _(функций: 2)_
    - Аутентифицировать пользователя через SSO — `authenticate-user-with-sso` (business/end-user-ui)
    - Настроить SSO-подключение — `configure-sso-connection` (configuration/admin-ui)
  - + **Настройка провайдера SSO** — `sso-idp-configuration-module` _(функций: 3)_
    - + Настроить Identity Provider (IdP) — `configure-sso-idp` (configuration/admin-ui)
    - + Добавить провайдера идентификации — `add-identity-provider` (configuration/admin-ui)
    - + Сопоставить поля SSO с атрибутами — `map-sso-attributes` (configuration/admin-ui)
- **Безопасность доступа к записям** — `recording-access-security-service` _(модулей: 1)_
  - **Ограничения доступа к записям** — `recording-access-security-module` _(функций: 2)_
    - Ограничить доступ к записям разговоров — `restrict-recording-access` (configuration/admin-ui)
    - Проверить доступ к скачиванию записи — `audit-recording-download` (ui-action/admin-ui)
- **Аудит и настройки безопасности** — `security-audit-settings-service` _(модулей: 1)_
  - **Журнал действий и политики безопасности** — `security-audit-settings-module` _(функций: 4)_
    - Просмотреть журнал действий — `view-security-audit-log` (ui-action/admin-ui)
    - Настроить политику безопасности — `configure-security-policy` (configuration/admin-ui)
    - + Просмотреть журнал действий — `view-action-log` (business/admin-ui)
    - + Настроить ограничение доступа по IP — `configure-ip-restriction` (configuration/admin-ui)

## 5. Дозаполнение: что добавлено

Добавлено **29 модулей** и **96 функций**, сгруппированы по кластерам:

| Кластер | +модулей | +функций |
| --- | ---: | ---: |
| `ai-speech-quality` | +5 | +11 |
| `analytics-marketing` | +2 | +9 |
| `contact-center-core` | +5 | +15 |
| `digital-channels` | +3 | +12 |
| `mango-talker` | +6 | +19 |
| `platform-integrations` | +3 | +12 |
| `security-access` | +2 | +8 |
| `vats-core` | +3 | +10 |
| **Итого** | **+29** | **+96** |

Новые модули (с родительским сервисом):

- `vats-blacklist-whitelist-module` → `vats-inbound-routing-service` (2 функций)
- `vats-time-based-routing-module` → `vats-inbound-routing-service` (2 функций)
- `vats-voicemail-management-module` → `vats-recording-history-service` (2 функций)
- `cc-call-hold-module` → `cc-agent-workspace-service` (2 функций)
- `cc-call-transfer-module` → `cc-agent-workspace-service` (2 функций)
- `cc-agent-conferencing-module` → `cc-agent-workspace-service` (2 функций)
- `cc-call-recording-module` → `cc-agent-workspace-service` (2 функций)
- `cc-supervisor-monitoring-module` → `cc-supervisor-wfm-service` (2 функций)
- `social-messenger-channels-module` → `messenger-channel-service` (3 функций)
- `dialog-api-session-management-module` → `dialog-api-messaging-service` (5 функций)
- `dialog-api-webhook-module` → `dialog-api-messaging-service` (3 функций)
- `talker-call-control-module` → `talker-softphone-service` (4 функций)
- `talker-message-operations-module` → `talker-team-chat-service` (4 функций)
- `talker-file-sharing-module` → `talker-team-chat-service` (2 функций)
- `talker-video-effects-module` → `talker-video-meeting-service` (3 функций)
- `talker-favorites-groups-module` → `talker-contact-history-service` (4 функций)
- `talker-presence-status-module` → `talker-softphone-service` (2 функций)
- `quality-appeal-module` → `quality-checklist-service` (3 функций)
- `quality-call-randomizer-module` → `quality-checklist-service` (2 функций)
- `ai-assistant-module` → `conversation-summary-service` (2 функций)
- `speech-analytics-search-module` → `speech-analytics-service` (2 функций)
- `speech-analytics-tagging-module` → `speech-analytics-service` (2 функций)
- `static-calltracking-module` → `calltracking-attribution-service` (2 функций)
- `analytics-goals-integration-module` → `end-to-end-analytics-service` (2 функций)
- `bitrix24-connector-module` → `crm-erp-integration-service` (2 функций)
- `amocrm-connector-module` → `crm-erp-integration-service` (3 функций)
- `onec-connector-module` → `crm-erp-integration-service` (3 функций)
- `custom-role-management-module` → `role-access-management-service` (3 функций)
- `sso-idp-configuration-module` → `sso-identity-service` (3 функций)

## 6. Пробелы и риск устаревания

### 6.1. Качество извлечения корпуса `sip-trunk`

Корпус `kb/mango-product-docs/processed/sip-trunk/` существует (≈39 секций), но извлечение заголовков для него не сработало: slug-и секций деградировали в `01-section.md`, `07-section.md`, `08-3-1-1-0-a-b-9-0.md` и подобные. Сослаться на осмысленную секцию нельзя, поэтому отдельный модуль управления SIP-trunk **не смоделирован** (это нарушило бы запрет на выдумку). _Рекомендация:_ переизвлечь исходный PDF SIP-trunk и затем добавить модуль с корректными ссылками.

### 6.2. Сервисы с одним модулем

14 сервисов содержат ровно один модуль. Это удовлетворяет минимуму стандарта (≥1 модуль на сервис), но глубина по ним фиксируется как пробел: документация пока не даёт второго отдельного модуля с ≥2 функций без выдумки. Кандидаты на дальнейшее дозаполнение по мере уточнения источников:

| Сервис | Единственный модуль |
| --- | --- |
| `cc-interaction-routing-service` (Маршрутизация обращений КЦ) | `cc-queue-routing-module` |
| `cc-outbound-campaign-service` (Исходящие кампании КЦ) | `cc-outbound-campaign-module` |
| `contact-center-api-service` (Contact Center API) | `contact-center-api-module` |
| `digital-channel-group-service` (Группы текстовых каналов) | `digital-channel-group-module` |
| `recording-access-security-service` (Безопасность доступа к записям) | `recording-access-security-module` |
| `reporting-dashboard-service` (Отчёты и дашборды) | `reporting-dashboard-module` |
| `security-audit-settings-service` (Аудит и настройки безопасности) | `security-audit-settings-module` |
| `vats-ivr-service` (Голосовое меню ВАТС) | `vats-ivr-menu-module` |
| `vats-number-management-service` (Управление номерами ВАТС) | `vats-connected-numbers-module` |
| `voice-robot-service` (Голосовой робот) | `voice-robot-scenario-module` |
| `vpbx-open-api-service` (ВАТС Open API) | `vpbx-open-api-module` |
| `wallboard-monitoring-service` (Wallboard-мониторинг) | `wallboard-monitoring-module` |
| `webhook-event-service` (Webhook-события) | `webhook-event-module` |
| `website-chat-service` (Чат на сайте) | `website-chat-widget-module` |

### 6.3. Недоиспользованные крупные корпуса

Несколько корпусов значительно больше, чем извлечённый из них объём; выбрана репрезентативная, но не исчерпывающая часть. Дальнейшее дозаполнение возможно итеративно (по одной партии модулей/функций со ссылками):

- `vpbx-api` (≈253 секции) и `contact-center-api` через `vpbx-api` — описано много методов Open API сверх внесённых;
- `mango-lk-manual` (≈348 секций) и `mango-cc-manual` (≈232 секции) — глубокие руководства ВАТС/КЦ;
- `integration-bitrix24` (≈192 секции) — детальный коннектор, внесена базовая пара функций;
- `mdialogi-api` (≈62 секции) — Dialog API внесён существенно, но не полностью.

### 6.4. Документированные, но отложенные области

Статусы присутствия пользователя Mango Talker внесены в этой итерации модулем `talker-presence-status-module` под `talker-softphone-service` (статус определяет готовность к приёму вызовов, поэтому естественный родитель — софтфон): функции `change-talker-presence-status` (`mtalker/windows-mac-working` секция 222, `mtalker/android-user-guide` секция 115) и `disable-talker-notifications` (`mtalker/windows-mac-working` секции 220, 223).

Остаются неразобранными на сущности руководства `mtalker/windows-mac-settings`, `mtalker/windows-mac-admin`, `mtalker/android-user-guide` (за пределами статуса), `mtalker/quick-start` — основное наполнение взято из `mtalker/windows-mac-working`. Это кандидаты на дальнейшее дозаполнение (настройки клиента, администрирование, мобильные особенности).

### 6.5. Сущности со слабым evidence (только маркетинговый URL)

6 перенесённых из YAML сущностей опираются только на ссылку на страницу продукта (без секции руководства). Они валидны (URL — допустимый evidence), но это кандидаты на усиление доказательной базы реальными секциями:

- `voice-robot-service` (internal_services)
- `voice-robot-scenario-module` (modules)
- `run-voice-robot-dialog` (functions)
- `configure-voice-robot-scenario` (functions)
- `configure-calltracking-number` (functions)
- `open-end-to-end-analytics-report` (functions)

## 7. Валидация и воспроизводимость

Реестр проверяется тремя независимыми способами, все проходят:

1. **Проектный валидатор** (stdlib-only, как в CI):
   ```bash
   python3 scripts/validate_issue_170_mango_registry.py
   ```
   Проверяет JSON Schema, резолвинг каждого `industry_ref` против живого Industry-реестра, целостность «родитель ↔ ребёнок» в обе стороны и полноту иерархии (пороги и минимумы).
2. **JSON Schema, draft 2020-12** — [`kb/mango-taxonomy/mango-registry.schema.json`](../../kb/mango-taxonomy/mango-registry.schema.json).
3. **Полный контур БЗ:**
   ```bash
   make kb-validate
   ```

Дозаполнение воспроизводится аддитивным билдером [`experiments/cascade_fill.py`](../../experiments/cascade_fill.py) поверх перенесённого реестра; перечень исходных секций — в [`experiments/doc_catalog.txt`](../../experiments/doc_catalog.txt). Этот документ перегенерируется скриптом [`experiments/gen_inventory_doc.py`](../../experiments/gen_inventory_doc.py).

