---
status: active
version: 1.0
updated: 2026-06-22
ai-generated: true
type: convergence-test
scope: mango-taxonomy-to-industry-taxonomy-mapping
issue: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/176"
operating_mode: "Creative (Deep Dive)"
related_artifacts:
  - "standards/mango-taxonomy-standard.md"
  - "standards/industry-taxonomy-standard.md"
  - "kb/mango/mango-registry.json"
  - "kb/industry/reference-taxonomy.json"
  - "standards/decisions/ADR-012-mango-taxonomy.md"
  - "standards/decisions/ADR-011-industry-taxonomy.md"
test_artifacts:
  - "experiments/issue-176-convergence/gold.json"
  - "experiments/issue-176-convergence/blind-inputs.json"
  - "experiments/issue-176-convergence/ai-predictions.json"
  - "experiments/issue-176-convergence/scored.json"
  - "experiments/issue-176-convergence/score.py"
---

# Тест на сходимость маппинга Mango Taxonomy на Industry Taxonomy

> **TL;DR.** Независимый AI-агент сошёлся с эталоном на **уровне Domain — 81 %** и
> на **точном полном пути — 37 %** (формула ДоД). Ноль галлюцинаций: 100 % выбранных
> AI узлов реально существуют в `reference-taxonomy.json`. Все расхождения сводятся к
> **четырём конкретным, воспроизводимым причинам**, две из которых — дефекты самих
> артефактов (дублирующиеся id-узлы Industry Taxonomy и недомаппленная глубина в
> Mango-реестре), а не ошибки агента. **Рекомендация: НЕ фиксировать v1.0
> сейчас**, выполнить 4 точечных доработки и повторить тест.

---

## 1. Мета

| Параметр | Значение |
| --- | --- |
| Дата теста | 2026-06-22 |
| Тип теста | Inter-rater reliability (слепой маппинг независимым агентом против эталона) |
| Количество тестовых сущностей | **27** |
| AI-агент (rater) | Claude (Opus 4.x), 6 независимых сессий без общего контекста |
| Источник сущностей | [`kb/mango/mango-registry.json`](../../kb/mango/mango-registry.json) `taxonomy.version 1.0.0` |
| Целевая таксономия | [`kb/industry/reference-taxonomy.json`](../../kb/industry/reference-taxonomy.json) `version 1.1.0` |
| Стандарты | [`mango-taxonomy-standard.md`](../../standards/mango-taxonomy-standard.md) `v0.2`, [`industry-taxonomy-standard.md`](../../standards/industry-taxonomy-standard.md) |
| Эталонный маппинг | `maps_to.industry_alignment[]` из реестра (созданы независимо от rater, по аудиту #164/#170) |

### 1.1 Методология (как обеспечена независимость)

1. **Эталон (gold).** Для каждой сущности взят `primary`-элемент
   `maps_to.industry_alignment[]` из `mango-registry.json`. Эталон создавался
   ранее и независимо от теста (см. историю аудита таксономии).
2. **Слепой вход.** Из каждой записи реестра удалены поля `maps_to` и
   `evidence_refs`; агенту переданы только `id`, `level`, `name_ru`,
   `description` и (где есть) `cluster` / `function_type` /
   `interaction_surface`. Слепые входы зафиксированы в
   [`blind-inputs.json`](../../experiments/issue-176-convergence/blind-inputs.json).
3. **Изоляция.** 27 сущностей разбиты на 6 чанков; каждый чанк обработан
   **отдельной свежей сессией агента без общего контекста** (6 независимых
   «оценщиков»). Каждому агенту было **явно запрещено** открывать
   `kb/mango/mango-registry.json` или любой файл из `kb/mango/` (там лежит
   эталон). Разрешённые источники: два стандарта + `reference-taxonomy.json`.
4. **Задача агента.** Выбрать лучший путь `domain → capability → feature →
   function` из `reference-taxonomy.json` (точные id) и `alignment_type`
   согласно §7.2 Mango-стандарта.
5. **Подсчёт.** Скрипт [`score.py`](../../experiments/issue-176-convergence/score.py)
   сравнивает предсказания агента
   ([`ai-predictions.json`](../../experiments/issue-176-convergence/ai-predictions.json))
   с эталоном по каждому уровню, проверяет существование выбранного узла в реестре
   Industry (резолвер учитывает `domains` и `cross_domain_layers`) и классифицирует
   расхождения.

### 1.2 Репрезентативность набора

27 сущностей покрывают **все 5 уровней**, **все 8 кластеров**, **все 3 типа
функций** и **все типы alignment**:

| Срез | Покрытие |
| --- | --- |
| Уровни | official-product ×4, product ×3, service ×8, module ×5, function ×7 |
| Кластеры | vats-core ×2, contact-center-core ×2, digital-channels ×1, mango-talker ×2, ai-speech-quality ×2, analytics-marketing ×1, platform-integrations ×2, security-access ×1 |
| Типы функций | business ×5, configuration ×1, ui-action ×1 |
| Поверхности | system-rule, admin-ui, end-user-ui, api, webhook, background-job, operator-ui |
| Multi-alignment | 4 сущности с `primary + secondary/supporting` (#9, #10, #24, #25) |

---

## 2. Результаты

### 2.1 Общий процент корректности маппинга

По нормативной формуле ДоД (`полные совпадения / всего`):

```
Корректность (точный полный путь) = 10 / 27 = 37 %
```

Однако одно число скрывает структуру расхождений. Ниже — три согласованных
метрики, от строгой к содержательной:

| Метрика | Значение | Что считает |
| --- | --- | --- |
| **Точный полный путь** (формула ДоД) | **10/27 = 37 %** | путь агента побайтово равен эталону |
| **Префиксное совпадение** | **17/27 = 63 %** | агент совпал со всеми уровнями, которые задаёт эталон (агент мог уйти глубже, не противореча) |
| **Согласие по Domain** | **22/27 = 81 %** | верхний уровень классификации |
| **Резолвимость узлов агента** | **27/27 = 100 %** | агент не выдумал ни одного узла — все пути существуют в `reference-taxonomy.json` |
| **Совпадение `alignment_type`** | **27/27 = 100 %** | агент корректно определил primary как основной смысл |

### 2.2 Корректность по уровням

| Уровень | Совпадений | % | Комментарий |
| --- | --- | --- | --- |
| Domain | 22/27 | **81 %** | сильная сходимость верхнего уровня |
| Capability | 18/27 | **67 %** | граничные кейсы между доменами/смежными capability |
| Feature | 1/8 | **12 %** | где эталон задаёт feature — почти всегда расхождение (см. причины A/B/C) |
| Function | 0/1 | **0 %** | единственный кейс с эталонной function (#24) ушёл в другой домен (причина B) |
| Alignment type | 27/27 | **100 %** | все сущности корректно классифицированы как primary |

> **Важно для интерпретации.** Низкие Feature/Function — это **не** случайные
> ошибки агента: из 8 эталонных feature-узлов 7 относятся к причинам A/B/C
> (структурные дефекты артефактов либо законные judgment-calls), а в 7 других
> сущностях агент, наоборот, **углубился точнее эталона** (причина D).

### 2.3 Детальные результаты

Легенда: ✅ — точное совпадение пути; 🟡 — совпал со всеми уровнями эталона, но
ушёл глубже (непротиворечивое уточнение); ❌ — расхождение по domain/capability.

| # | Mango сущность | Level | Эталон (primary) | AI-агент | Итог | Причина |
|---|---|---|---|---|:---:|:---:|
| 1 | `mango-virtual-pbx-official` | official-product | `voice-ucaas/cloud-pbx` | `voice-ucaas/cloud-pbx` | ✅ | — |
| 2 | `mango-contact-center-official` | official-product | `contact-center/omnichannel-contact-center` | `contact-center/omnichannel-contact-center` | ✅ | — |
| 3 | `mango-speech-analytics-official` | official-product | `ai-automation/speech-analytics` | `ai-automation/speech-analytics` | ✅ | — |
| 4 | `mango-talker-official` | official-product | `voice-ucaas/unified-communications` | `voice-ucaas/unified-communications` | ✅ | — |
| 5 | `mango-digital-communications` | product | `digital-channels/omnichannel-messaging` | `digital-channels/omnichannel-messaging` | ✅ | — |
| 6 | `mango-marketing-analytics` | product | `analytics/call-tracking` | `analytics/call-tracking` | ✅ | — |
| 7 | `mango-security-access` | product | `security/information-security` | `security/information-security` | ✅ | — |
| 8 | `vats-ivr-service` | service | `voice-ucaas/ivr-voice-menu` | `voice-ucaas/ivr-voice-menu/ivr-scenarios` | 🟡 | D |
| 9 | `cc-supervisor-wfm-service` | service | `contact-center/workforce-management` | `contact-center/workforce-management` | ✅ | — |
| 10 | `dialog-api-messaging-service` | service | `platform/cpaas/programmable-messaging` | `digital-channels/omnichannel-messaging` | ❌ | B |
| 11 | `talker-video-meeting-service` | service | `voice-ucaas/unified-communications` | `voice-ucaas/video-conferencing` | ❌ | C |
| 12 | `conversation-summary-service` | service | `contact-center/agent-assist/conversation-summaries` | `ai-automation/conversation-summaries/ai-summary` | ❌ | A |
| 13 | `end-to-end-analytics-service` | service | `analytics/end-to-end-analytics` | `analytics/end-to-end-analytics` | ✅ | — |
| 14 | `crm-erp-integration-service` | service | `platform/platform-integration` | `platform/platform-integration` | ✅ | — |
| 15 | `sso-identity-service` | service | `security/information-security/access-control` | `security/information-security` | ❌ | A |
| 16 | `vats-voicemail-management-module` | module | `voice-ucaas/call-recording` | `voice-ucaas/cloud-pbx/voicemail` | ❌ | C |
| 17 | `cc-supervisor-monitoring-module` | module | `contact-center/workforce-management` | `contact-center/supervisor-assist/live-monitoring` | ❌ | C |
| 18 | `talker-file-sharing-module` | module | `voice-ucaas/unified-communications/corporate-messaging` | `digital-channels/team-messaging/team-chat` | ❌ | B |
| 19 | `ai-assistant-module` | module | `contact-center/agent-assist/conversation-summaries` | `ai-automation/conversation-summaries/ai-summary` | ❌ | A |
| 20 | `bitrix24-connector-module` | module | `platform/platform-integration` | `platform/platform-integration/crm-connectors` | 🟡 | D |
| 21 | `run-voice-robot-dialog` | function | `ai-automation/voice-bot` | `ai-automation/voice-bot/voice-dialog-orchestration/voice-dialog-flow` | 🟡 | D |
| 22 | `configure-sso-connection` | function | `security/information-security/access-control` | `security/access-control` | ❌ | A |
| 23 | `mute-talker-microphone` | function | `voice-ucaas/unified-communications` | `voice-ucaas/unified-communications/softphone` | 🟡 | D |
| 24 | `send-dialog-api-message` | function | `platform/cpaas/programmable-messaging/programmable-message-send` | `digital-channels/omnichannel-messaging/messenger-integration/send-message` | ❌ | B |
| 25 | `send-call-event-webhook` | function | `platform/open-api/webhooks` | `platform/open-api/webhooks/webhook-subscription` | 🟡 | D |
| 26 | `attribute-call-to-ad-source` | function | `analytics/call-tracking` | `analytics/call-tracking/source-attribution/source-attribution` | 🟡 | D |
| 27 | `transfer-call-with-consultation` | function | `contact-center/agent-workspace` | `contact-center/agent-workspace/agent-desktop/interaction-handling` | 🟡 | D |

**Итого:** ✅ 10 · 🟡 7 · ❌ 10.

---

## 3. Анализ расхождений

17 несовпадений с точным путём группируются в **4 причины**. Ключевой вывод:
**ни одно расхождение не является галлюцинацией или случайной ошибкой агента** —
каждый раз агент выбирал реально существующий узел по защитимой логике.

### Причина A — Дублирующиеся id-узлы в Industry Taxonomy (4 кейса: #12, #15, #19, #22)

Это **дефект целевой таксономии**, а не агента. В `reference-taxonomy.json` один
и тот же `id` существует под двумя разными родителями, без правила
дизамбигуации в стандарте. Когда агент выбирает семантически идентичный узел —
он попадает «не в ту ветку».

- **`conversation-summaries`** существует в **двух** местах:
  `contact-center/agent-assist/conversation-summaries` (эталон #12, #19) **и**
  `ai-automation/conversation-summaries` (выбор агента). AI-конспекты разговоров —
  это буквально «conversation summaries», и агент выбрал одноимённый узел в
  AI-домене. Оба варианта легитимны; стандарт не говорит, какой канонический.
- **`access-control`** существует в **двух** местах:
  `security/information-security/access-control` (эталон #15, #22) **и**
  `security/access-control` (выбор агента #22). Для #15 агент остановился на
  родителе `information-security` (правомерно по правилу «nearest canonical
  parent», §7.3), для #22 — выбрал короткий путь `security/access-control`.

Проверка резолвером (см. лог теста) подтверждает дубли; помимо этих двух, в
таксономии есть и другие кросс-веточные дубли (`call-routing`,
`interaction-routing`, `live-monitoring`, `device-provisioning`), которые с
высокой вероятностью дадут расхождения на других выборках.

> **Корень:** структурная неоднозначность Industry Taxonomy (одинаковые id под
> разными родителями) + отсутствие правила выбора канонической ветки в стандарте.

### Причина B — Граница «CPaaS/API/UC ↔ digital-channels» без правила маршрутизации (3 кейса: #10, #18, #24)

Эталон относит программные/корпоративные коммуникации к одному домену, агент —
к семантически эквивалентному узлу в другом домене:

- **#10 / #24 Dialog API.** Эталон: `platform/cpaas/programmable-messaging`
  (это API → CPaaS). Слепое описание «программный обмен сообщениями цифровых
  диалогов» агент закономерно прочитал как `digital-channels/omnichannel-messaging`.
  Граница «программный канал = CPaaS vs цифровой канал» в стандарте не
  формализована для маппинга на Industry.
- **#18 File sharing в Talker.** Эталон:
  `voice-ucaas/unified-communications/corporate-messaging` (Talker = UC). Агент:
  `digital-channels/team-messaging/team-chat`. «Командный чат + файлы» одинаково
  валидно читается и как UC-corporate-messaging, и как digital-channels
  team-messaging. Стандарт даёт правило только для **Mango-кластера** Talker
  (§ «Mango Talker chats … remain under `mango-talker` primary»), но не для
  выбора **Industry**-домена.

> **Корень:** отсутствие в стандарте явного boundary-правила «API/CPaaS vs
> digital-channel» и «UC corporate-messaging vs team-messaging» при маппинге на
> Industry.

### Причина C — Гранулярность capability: roll-up vs специфичный sibling (3 кейса: #11, #16, #17)

Законные judgment-calls в пределах **верного домена**:

- **#11 Видео Talker.** Эталон сворачивает всё Talker в `unified-communications`;
  агент выбрал существующий sibling `video-conferencing`. Стандарт не говорит,
  катить ли видео в UC-зонтик или выделять.
- **#16 Голосовая почта.** Эталон: `voice-ucaas/call-recording` (модуль внутри
  сервиса «Записи и история»); агент: `voice-ucaas/cloud-pbx/voicemail`. Оба
  родителя для voicemail правдоподобны.
- **#17 Супервизорский мониторинг.** Эталон: `workforce-management` (унаследовано
  от родительского сервиса cc-supervisor-**wfm**-service); агент:
  `supervisor-assist/live-monitoring` — **семантически точнее** («контроль и
  прослушивание операторов» — это supervisor-assist, не WFM). Здесь расхождение —
  сигнал к перепроверке **эталона/реестра**, а не ошибка агента.

> **Корень:** недостаток правил гранулярности (когда сворачивать в родительский
> capability) + потенциальная ошибка наследования capability в реестре (#17).

### Причина D — Реестр Mango недомаппливает глубину против §7.3 стандарта (7 кейсов: #8, #20, #21, #23, #25, #26, #27)

Это **дефект Mango-реестра**, а не агента. §7.3 Mango-стандарта рекомендует:

| Mango level | Recommended industry_ref |
| --- | --- |
| Module | `domain` + `capability` + `feature` |
| Function | `domain` + `capability` + `feature` + `function` |

В 7 сущностях **эталон останавливается мельче рекомендации**, а агент углубился
до реально существующего канонического узла, **точно следуя §7.3**:

| # | Level | Эталон (глубина) | AI-агент (глубина) | §7.3 рекомендует |
| --- | --- | --- | --- | --- |
| 20 | module | `platform/platform-integration` (2) | `…/crm-connectors` (3) | 3 |
| 21 | function | `ai-automation/voice-bot` (2) | `…/voice-dialog-orchestration/voice-dialog-flow` (4) | 4 |
| 23 | function | `voice-ucaas/unified-communications` (2) | `…/softphone` (3) | 4 |
| 25 | function | `platform/open-api/webhooks` (3) | `…/webhook-subscription` (4) | 4 |
| 26 | function | `analytics/call-tracking` (2) | `…/source-attribution/source-attribution` (4) | 4 |
| 27 | function | `contact-center/agent-workspace` (2) | `…/agent-desktop/interaction-handling` (4) | 4 |
| 8 | service | `voice-ucaas/ivr-voice-menu` (2) | `…/ivr-scenarios` (3) | 2 (service) |

Во всех 7 случаях путь агента **содержит эталонный путь как префикс** и резолвится
в реестре. Формально это «несовпадение», по сути — агент оказался **дисциплинированнее
реестра** по части глубины.

> **Корень:** эталонные `maps_to` в `mango-registry.json` систематически мельче
> рекомендации §7.3 для уровней Module/Function.

### 3.1 Сводка причин

| Причина | Кейсы | Кол-во | Чей дефект | Действие |
| --- | --- | :---: | --- | --- |
| A. Дубли id-узлов Industry + нет правила выбора ветки | #12,#15,#19,#22 | 4 | Industry Taxonomy + оба стандарта | Дедуп/алиасы + disambiguation rule |
| B. Нет boundary-правила CPaaS/API/UC ↔ digital-channels | #10,#18,#24 | 3 | Mango/Industry стандарты | Явное правило маршрутизации домена |
| C. Гранулярность capability / возможная ошибка наследования (#17) | #11,#16,#17 | 3 | Стандарт + реестр | Правило roll-up + ревизия #17 |
| D. Реестр мельче §7.3 по глубине | #8,#20,#21,#23,#25,#26,#27 | 7 | Mango-реестр | Доуглубить `maps_to` до §7.3 |

---

## 4. Выводы

1. **Сходимость по смыслу — высокая, по форме — нет.** Агент стабильно
   определяет домен (81 %) и тип alignment (100 %) и **не галлюцинирует**
   (100 % узлов реальны). Это значит: стандарты **достаточно понятны**, чтобы
   независимый аналитик выбирал правильную «область», но **недостаточно точны**,
   чтобы детерминированно выбрать конкретный узел.

2. **Большинство «провалов» — дефекты артефактов, а не агента.** Из 17
   несовпадений 11 (причины A и D) объясняются дублями узлов Industry Taxonomy и
   недомаппленной глубиной Mango-реестра. По строгой формуле это «ошибки», но
   корень — в данных/стандартах.

3. **Mango Taxonomy НЕ готова к фиксации v1.0 как есть.** По нормативной формуле
   ДоД корректность = **37 % < 80 %**. Даже по мягкой префиксной метрике
   63 % < 80 %. Порог не достигнут — но разрыв закрывается **четырьмя точечными
   доработками**, а не переработкой модели.

4. **Тест полезен как регрессия.** Артефакты (`gold.json`, `blind-inputs.json`,
   `ai-predictions.json`, `score.py`) воспроизводимы и могут быть переиспользованы
   после доработок.

---

## 5. Рекомендации

> **Явная рекомендация: НЕ фиксировать Mango Taxonomy v1.0 сейчас.** Выполнить
> доработки P1–P3 ниже, затем повторить тест. Ожидаемый результат после доработок —
> ≥ 80 % по префиксной метрике и ≥ 80 % по Domain/Capability.

Доработки выставляются **отдельными задачами** (по ограничению issue #176 — этот
тест не меняет стандарты и реестры):

| # | Приоритет | Действие | Адресует | Артефакт |
| --- | :---: | --- | --- | --- |
| R1 | **P1** | Дедуплицировать кросс-веточные id-узлы Industry Taxonomy (`conversation-summaries`, `access-control`, `call-routing`, `live-monitoring`, …) — оставить один canonical, остальные оформить как alias (§10.2 industry-стандарта). Добавить в оба стандарта правило выбора канонической ветки при совпадении смысла. | Причина A | `kb/industry/reference-taxonomy.json`, оба стандарта |
| R2 | **P1** | Доуглубить эталонные `maps_to` для Module/Function в `mango-registry.json` до рекомендации §7.3 (или явно проставить `mapping_gap`, если узла нет). | Причина D | `kb/mango/mango-registry.json` |
| R3 | **P2** | Добавить в Mango-стандарт boundary-правило для Industry-маппинга: «API/CPaaS vs digital-channel» и «UC corporate-messaging vs team-messaging» — с однозначным критерием. | Причина B | `standards/mango-taxonomy-standard.md` |
| R4 | **P2** | Добавить правило гранулярности (когда сворачивать в родительский capability) и **проверить эталон #17** (`cc-supervisor-monitoring-module`: `workforce-management` vs `supervisor-assist/live-monitoring`). | Причина C | стандарт + реестр |
| R5 | **P3** | После R1–R4 повторно прогнать этот тест (тот же набор) и зафиксировать v1.0 при ≥ 80 %. | — | этот документ |

### 5.1 Критерий успеха повторного теста

- **≥ 80 %** префиксной корректности **и** **≥ 80 %** по Domain и Capability → фиксировать **v1.0**.
- Иначе — повторить анализ расхождений и доработку.

---

## 6. Воспроизводимость

```bash
# из корня репозитория
python3 experiments/issue-176-convergence/score.py
```

Входные/выходные артефакты:

- [`experiments/issue-176-convergence/gold.json`](../../experiments/issue-176-convergence/gold.json) — эталонные primary-маппинги 27 сущностей.
- [`experiments/issue-176-convergence/blind-inputs.json`](../../experiments/issue-176-convergence/blind-inputs.json) — слепые входы (без `maps_to`).
- [`experiments/issue-176-convergence/chunk-A..F.json`](../../experiments/issue-176-convergence/) — разбиение по 6 независимым агентам.
- [`experiments/issue-176-convergence/ai-predictions.json`](../../experiments/issue-176-convergence/ai-predictions.json) — ответы агентов.
- [`experiments/issue-176-convergence/scored.json`](../../experiments/issue-176-convergence/scored.json) — результат сравнения.
- [`experiments/issue-176-convergence/score.py`](../../experiments/issue-176-convergence/score.py) — скрипт подсчёта.

> ⚠️ Ограничение метода: эталон взят из `mango-registry.json`, который сам
> содержит дефекты (причины C/D). Поэтому строгая корректность (37 %)
> **занижает** реальное качество понимания стандартов агентом; содержательная
> сходимость отражена в метриках Domain (81 %) и резолвимости (100 %).
