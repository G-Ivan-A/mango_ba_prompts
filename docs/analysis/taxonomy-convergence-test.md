---
status: draft
version: 0.1
updated: 2026-06-22
ai-generated: true
type: analysis
scope: industry-taxonomy
issue: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/174"
depends_on:
  - "standards/industry-taxonomy-standard.md"
  - "kb/industry-taxonomy/reference-taxonomy.json"
  - "kb/mango-taxonomy/mango-registry.json"
related_artifacts:
  - "experiments/issue-174/blind-test-input.json"
  - "experiments/issue-174/reference-classification.json"
  - "experiments/issue-174/blind-agent-output.json"
  - "experiments/issue-174/comparison.json"
  - "experiments/issue-174/score_convergence.py"
---

# Тест на сходимость классификации функций по Industry Taxonomy Standard

> **Тип теста:** inter-rater reliability (согласованность независимых классификаторов).
> **Вопрос теста:** может ли независимый аналитик (AI-агент), имея на руках
> **только** стандарт и реестр, классифицировать атомарные функции с высокой
> степенью согласованности с эталоном?
> Это финальная проверка готовности `industry-taxonomy-standard.md` к фиксации **v1.0**.

---

## 1. Мета

| Параметр | Значение |
|---|---|
| Дата теста | 2026-06-22 |
| Количество тестовых функций | **25** (целевой диапазон 20–30) |
| Тестируемый стандарт | [`standards/industry-taxonomy-standard.md`](../../standards/industry-taxonomy-standard.md) (`version: 0.1`, `status: draft`) |
| Тестируемый реестр | [`kb/industry-taxonomy/reference-taxonomy.json`](../../kb/industry-taxonomy/reference-taxonomy.json) (`version: 1.1.0`, `status: active`) |
| Источник функций | [`kb/mango-taxonomy/mango-registry.json`](../../kb/mango-taxonomy/mango-registry.json) (160 атомарных функций) + processed-документация |
| AI-агент (классификатор) | Изолированный subagent (Claude), без доступа к эталону и mango-реестру |
| Эталонный классификатор | Документированный mapping `maps_to.industry_alignment` из mango-реестра (построен независимо в задачах #168/#170) |

### 1.1 Дизайн независимости

Тест построен как сравнение **двух независимых раздач** (raters) по одной и той же
шкале (Industry Taxonomy):

- **Rater A (эталон):** для каждой функции взят документированный `industry_ref`
  из `kb/mango-taxonomy/mango-registry.json`. Этот mapping строился ранее, в отдельных
  задачах (#168 дозаполнение реестра, #170 каскад mango-реестра), на основе
  evidence-ссылок на документацию — **до и независимо** от настоящего теста.
- **Rater B (AI-агент под тестом):** изолированный subagent, которому выданы
  **только** два артефакта — `standards/industry-taxonomy-standard.md` и
  `kb/industry-taxonomy/reference-taxonomy.json` — плюс список из 25 функций (русское имя,
  тонкое описание, имя продуктового модуля). Агенту **запрещено** открывать
  `kb/mango-taxonomy/`, `docs/`, `experiments/`, mango-taxonomy-standard и искать в вебе.
  Агент не видел ни эталонную классификацию, ни `industry_ref` из mango-реестра.

Совпадение между Rater A и Rater B измеряет, насколько стандарт + реестр
**самодостаточны**: даёт ли он одну и ту же классификацию двум компетентным,
не сговаривавшимся классификаторам.

### 1.2 Как воспроизвести

```bash
# вход для слепой классификации (без ответов):
cat experiments/issue-174/blind-test-input.json
# результат слепого AI-агента:
cat experiments/issue-174/blind-agent-output.json
# подсчёт сходимости (валидирует и каноничность всех id):
python3 experiments/issue-174/score_convergence.py
```

---

## 2. Методология выбора и подсчёта

### 2.1 Репрезентативность тестового набора (25 функций)

Набор подобран стратифицированно, чтобы покрыть разные домены, типы функций и
продуктовые кластеры (требование ДоД №1):

| Срез | Распределение в наборе |
|---|---|
| **Домены** | voice-ucaas ×6, contact-center ×6, digital-channels ×3, ai-automation ×3, analytics ×3, platform (cross-domain) ×2, security ×2 |
| **function_type** | business ×12, configuration ×9, ui-action ×4 |
| **Кластеры/продукты** | ВАТС, Mango Talker, Контакт-центр, Речевая аналитика, Голосовой робот, Коллтрекинг/сквозная аналитика, цифровые каналы/мессенджеры, Dialog API, CRM-коннекторы (Битрикс24), SSO/роли |
| **Сложность** | включены неочевидные и «пограничные» функции (перевод вызова, тегирование разговора, чёрный список, статус оператора), а также 1 multi-alignment функция (#22) |

> Домен `hardware` в mango-реестре не имеет сопоставленных функций (0 mapping'ов),
> поэтому в боевой набор не вошёл; это отражает реальный охват продуктовой линейки.

### 2.2 Уровни и правило подсчёта

Шкала имеет 4 уровня: **Domain → Capability → Feature → Function**, плюс
атрибут **function_type**.

Эталонный mapping в mango-реестре сознательно фиксируется на **той глубине, на
которой существует точный канонический узел**: 25/25 функций имеют Domain и
Capability, но только 10/25 — Feature и 4/25 — Function (на остальных эталон
останавливается на capability, т.к. более точного канонического узла нет).
Поэтому:

- **Domain / Capability / function_type** — считаются по всем 25 функциям.
- **Feature** — считается только там, где эталон задаёт feature (10 функций).
- **Function** — считается только там, где эталон задаёт function (4 функции).
- **Полная сходимость (Σ)** функции = совпадение на **всех уровнях, которые
  задаёт эталон** (Domain + Capability, и Feature/Function, если они указаны).
  Если эталон останавливается на capability, переуглубление AI-агента на более
  низкий уровень **не штрафуется** (эталон по этим уровням «молчит»).

Формула главного показателя (как в постановке задачи):

```
Сходимость = (число функций с полным совпадением Σ) / (общее число функций) × 100%
```

Дополнительно: все node-id, выданные AI-агентом, прогнаны через валидатор —
**100% (25/25) канонические**, т.е. реально существуют в `reference-taxonomy.json`
с корректной parent-цепочкой. Несуществующих/выдуманных узлов агент не породил.

---

## 3. Результаты

### 3.1 Общий процент сходимости

> ## **Полная сходимость (Σ): 17/25 = 68.0%**

### 3.2 Сходимость по уровням

| Уровень | Совпадения | Процент | Комментарий |
|---|---|---|---|
| **Domain** | 24/25 | **96.0%** | один промах (#18, тегирование разговора) |
| **Capability** | 19/25 | **76.0%** | основной источник расхождений — пересекающиеся capability |
| **Feature** | 6/10 | **60.0%** | считается на 10 функциях, где эталон задаёт feature |
| **Function** | 1/4 | **25.0%** | считается на 4 функциях; промахи — из-за дублей/синонимов узлов |
| **function_type** | 21/25 | **84.0%** | 4 промаха — ui-action vs business на «view/play/status» |
| **Σ Полная** | **17/25** | **68.0%** | главный показатель |

### 3.3 Детальные результаты

Легенда: ✅ совпало · ❌ расхождение · — уровень не оценивается (эталон не задаёт).

| # | Функция | Эталон (Domain/Cap/Feat/Fn) | AI-агент | D | C | F | Fn | Type | Σ |
|---|---------|------------------------------|----------|---|---|---|----|----|----|
| 1 | Принять входящий звонок по сценарию | `voice-ucaas/voice-channel/inbound-voice-call/accept-inbound-voice-call` | `voice-ucaas/voice-channel/inbound-voice-call/receive-inbound-call` | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ |
| 2 | Проиграть голосовое меню звонящему | `voice-ucaas/ivr-voice-menu` | `voice-ucaas/ivr-voice-menu/ivr-scenarios/ivr-menu-navigation` | ✅ | ✅ | — | — | ✅ | ✅ |
| 3 | Настроить маршрутизацию по рабочему времени | `voice-ucaas/cloud-pbx/call-routing-rules` | `voice-ucaas/cloud-pbx/working-hours-schedule/working-hours-routing` | ✅ | ✅ | ❌ | — | ✅ | ❌ |
| 4 | Добавить номер в чёрный список | `voice-ucaas/cloud-pbx/call-routing-rules` | `voice-ucaas/call-routing` | ✅ | ❌ | ❌ | — | ✅ | ❌ |
| 5 | Сменить статус присутствия пользователя | `voice-ucaas/unified-communications` | `voice-ucaas/unified-communications/presence-status/presence-update` | ✅ | ✅ | — | — | ❌ | ✅ |
| 6 | Прослушать запись разговора | `voice-ucaas/call-recording` | `voice-ucaas/call-recording/call-recording` | ✅ | ✅ | — | — | ❌ | ✅ |
| 7 | Распределить обращение в очередь | `contact-center/call-routing/queue-management/queue-management` | `contact-center/interaction-routing/queue-routing/assign-interaction-to-agent` | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ |
| 8 | Перевести вызов с консультацией | `contact-center/agent-workspace` | `contact-center/interaction-routing` | ✅ | ❌ | — | — | ✅ | ❌ |
| 9 | Оценить разговор по чек-листу | `contact-center/quality-management` | `contact-center/quality-management/scorecards/scorecard-evaluation` | ✅ | ✅ | — | — | ✅ | ✅ |
| 10 | Настроить исходящую кампанию | `contact-center/outbound-calling/campaign-management` | `contact-center/outbound-calling/campaign-management/campaign-configuration` | ✅ | ✅ | ✅ | — | ✅ | ✅ |
| 11 | Спланировать прогноз входящих | `contact-center/workforce-management` | `contact-center/workforce-management/load-forecasting/load-forecasting` | ✅ | ✅ | — | — | ❌ | ✅ |
| 12 | Изменить статус оператора | `contact-center/agent-workspace` | `contact-center/agent-workspace/agent-desktop` | ✅ | ✅ | — | — | ❌ | ✅ |
| 13 | Принять обращение из чата сайта | `digital-channels/website-chat` | `digital-channels/website-chat/chat-widget/chat-widget-embed` | ✅ | ✅ | — | — | ✅ | ✅ |
| 14 | Подключить Telegram-канал | `digital-channels/omnichannel-messaging/messenger-integration` | `digital-channels/omnichannel-messaging/messenger-integration/channel-ingestion` | ✅ | ✅ | ✅ | — | ✅ | ✅ |
| 15 | Отправить сообщение в цифровом канале | `digital-channels/omnichannel-messaging/messenger-integration` | `digital-channels/omnichannel-messaging/messenger-integration/send-message` | ✅ | ✅ | ✅ | — | ✅ | ✅ |
| 16 | Распознать речь в записи разговора | `ai-automation/speech-analytics` | `ai-automation/speech-analytics/transcription/call-transcription` | ✅ | ✅ | — | — | ✅ | ✅ |
| 17 | Настроить сценарий голосового робота | `ai-automation/voice-bot` | `ai-automation/voice-bot/voice-dialog-orchestration/voice-dialog-flow` | ✅ | ✅ | — | — | ✅ | ✅ |
| 18 | Проставить теги разговору | `ai-automation/speech-analytics` | `contact-center/agent-workspace` | ❌ | ❌ | — | — | ✅ | ❌ |
| 19 | Привязать звонок к рекламному источнику | `analytics/call-tracking` | `analytics/call-tracking/source-attribution/source-attribution` | ✅ | ✅ | — | — | ✅ | ✅ |
| 20 | Настроить статический коллтрекинг | `analytics/call-tracking` | `analytics/call-tracking` | ✅ | ✅ | — | — | ✅ | ✅ |
| 21 | Выбрать виджет дашборда | `analytics/multichannel-analytics` | `analytics/real-time-reporting/dashboard-view/select-dashboard-widget` | ✅ | ❌ | — | — | ✅ | ❌ |
| 22 | Отправить сообщение через Dialog API | `platform/cpaas/programmable-messaging/programmable-message-send` | `platform/cpaas/programmable-messaging/programmable-message-send` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 23 | Настроить интеграцию с Битрикс24 | `platform/platform-integration` | `platform/platform-integration/crm-connectors/crm-bidirectional-sync` | ✅ | ✅ | — | — | ✅ | ✅ |
| 24 | Назначить роль пользователю | `security/information-security/access-control/role-based-access-control` | `security/access-control/role-management/assign-role` | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ |
| 25 | Аутентифицировать пользователя через SSO | `security/information-security/access-control` | `security/information-security/access-control` | ✅ | ✅ | ✅ | — | ✅ | ✅ |

---

## 4. Анализ расхождений

Всего **8 функций** не дали полной сходимости (Σ ❌): #1, #3, #4, #7, #8, #18, #21, #24.
Каждое расхождение разобрано до первопричины и сгруппировано по типам проблем.

### Тип 1 — Структурная избыточность таксономии (пересекающиеся/дублирующиеся узлы) — **5 случаев**

Самый частый и самый важный класс. В реестре есть **несколько узлов с
пересекающимся смыслом**, и стандарт не даёт правила приоритета. Два компетентных
классификатора расходятся не по компетентности, а потому что узлов-кандидатов
больше одного.

- **#7 «Распределить обращение в очередь».** В домене `contact-center`
  одновременно существуют capability `call-routing` (feature `queue-management`),
  `interaction-routing` (feature `queue-routing`) и `omnichannel-contact-center`.
  Эталон выбрал `call-routing/queue-management`, агент — `interaction-routing/queue-routing`.
  Оба валидны → **дубль capability для маршрутизации**.
- **#24 «Назначить роль пользователю».** `access-control` присутствует в реестре
  **дважды**: как capability `security/access-control` (с function `assign-role`) и
  как feature `security/information-security/access-control` (с function
  `role-based-access-control`). Агент нашёл узел с буквально совпадающим именем
  (`assign-role`), эталон — другую ветку. **Прямое дублирование `access-control`.**
- **#1 «Принять входящий звонок».** Feature `inbound-voice-call` содержит **два
  функции-синонима** — `accept-inbound-voice-call` и `receive-inbound-call`.
  Domain/Capability/Feature совпали, разошлись только на function. **Синонимичные
  function-узлы без правила выбора.**
- **#3 «Маршрутизация по рабочему времени».** В `cloud-pbx` пересекаются features
  `call-routing-rules` и `working-hours-schedule/working-hours-routing`. Для
  «маршрутизации по расписанию» узел `working-hours-routing` (выбор агента) даже
  точнее эталона. **Пересечение features внутри одной capability.**
- **#21 «Выбрать виджет дашборда».** Эталон отнёс к `analytics/multichannel-analytics`,
  но в реестре есть **буквально одноимённый** function
  `analytics/real-time-reporting/dashboard-view/select-dashboard-widget`, который
  агент и выбрал. Здесь **точнее оказался AI-агент**, а эталонный mapping в
  mango-реестре — субоптимальный (см. §4.1).

### Тип 2 — Пробелы покрытия (нет точного канонического узла) — **3 случая**

Для функции в реестре **нет адекватного узла**, и оба классификатора вынуждены
выбирать «ближайший», но разный.

- **#4 «Добавить номер в чёрный список».** Нет узла для фильтрации/блокировки
  номеров (blacklist/whitelist, anti-spam). Эталон — `cloud-pbx/call-routing-rules`,
  агент (confidence **low**) — `voice-ucaas/call-routing`. **Отсутствует узел
  number-filtering / blacklist.**
- **#8 «Перевести вызов с консультацией».** Нет узла «перевод вызова /
  call-transfer». Эталон — `agent-workspace`, агент (**low**) — `interaction-routing`.
  **Отсутствует узел call-transfer.**
- **#18 «Проставить теги разговору».** Единственный промах на уровне **Domain**.
  Нет узла «тегирование разговоров/conversation-tagging». Эталон поместил в
  `ai-automation/speech-analytics` (тегирование — часть речевой аналитики Mango),
  агент (**low**) — в `contact-center/agent-workspace` (как действие оператора).
  **Отсутствует узел conversation-tagging + кросс-доменная неоднозначность.**

### Тип 3 — Неоднозначность определения `function_type` — **4 случая** (#5, #6, #11, #12)

Промахи по `function_type` не влияют на путь Domn→Fn, но снижают показатель типа
до 84%. Все 4 — на границе **business vs ui-action / configuration**:

- #5 «Сменить статус присутствия» — эталон `ui-action`, агент `business`.
- #6 «Прослушать запись разговора» — эталон `ui-action`, агент `business`.
- #12 «Изменить статус оператора» — эталон `ui-action`, агент `business`.
- #11 «Спланировать прогноз входящих» — эталон `configuration`, агент `business`.

§7.2 стандарта определяет `ui-action` как «UI-взаимодействие, не создающее
самостоятельного business/configuration-результата» (примеры: open panel, select
widget). «Прослушать запись», «сменить статус», «спланировать прогноз» —
пограничны: результат можно трактовать и как операционный (business), и как
UI-действие/настройку. **Определения §7.2 не дают однозначного теста для
«просмотровых/статусных» действий.**

### 4.1 Побочная находка: дефект эталона (mango-реестр)

Случай **#21** показывает, что субоптимален не AI-агент, а **эталонный mapping**:
для «Выбрать виджет дашборда» в Industry-реестре есть точный одноимённый узел
`analytics/real-time-reporting/dashboard-view/select-dashboard-widget`, а
mango-реестр сослался на `analytics/multichannel-analytics`. Это **отдельный
change request к `kb/mango-taxonomy/mango-registry.json`** (вне рамок данной задачи —
менять реестры запрещено постановкой). Аналогично спорны (агент точнее или
не хуже эталона) #3 и #24.

### 4.2 Сводка по первопричинам

| Тип проблемы | Случаи | Кол-во | Куда «лечить» |
|---|---|---|---|
| 1. Структурная избыточность (дубли/пересечения узлов) | #1, #3, #7, #21, #24 | **5** | Стандарт + реестр: дедупликация capability/feature, правило приоритета |
| 2. Пробелы покрытия (нет узла) | #4, #8, #18 | **3** | Реестр: добавить узлы (blacklist, call-transfer, conversation-tagging) |
| 3. Неоднозначность `function_type` | #5, #6, #11, #12 | **4** | Стандарт §7.2: уточнить тест business vs ui-action vs configuration |
| (побочно) дефект эталонного mapping | #21 (#3, #24) | 1–3 | mango-реестр: отдельный CR |

**Ключевой вывод анализа:** 7 из 8 полных расхождений (#1, #3, #4, #7, #8, #18,
#24) восходят к свойствам **стандарта/таксономии** (избыточность, пробелы,
определения типов), и лишь 1 (#21) — к ошибке эталонного реестра. То есть низкая
сходимость отражает **реальные дефекты стандарта**, а не случайный шум.

---

## 5. Выводы

1. **Грубое отнесение работает хорошо.** Domain-сходимость **96%** — независимый
   агент почти всегда попадает в правильный домен. На верхнем уровне таксономия
   готова к боевому использованию.
2. **Тонкое отнесение не сходится.** Capability **76%**, Feature **60%**, Function
   **25%**, полная сходимость **68%** — ниже порога **80%**. Причина системная:
   **пересекающиеся и дублирующиеся узлы** + **пробелы покрытия** + **размытые
   определения `function_type`**, а не ошибки классификатора (агент на спорных
   узлах честно ставил confidence `low`, а его id 100% канонические).
3. **Стандарт ещё `draft`/`v0.1`.** Тест выявил конкретные, воспроизводимые
   дефекты, которые делают классификацию неоднозначной для двух независимых
   аналитиков. Это именно тот сигнал, ради которого тест и проводился.

> ### Готов ли стандарт к фиксации v1.0? — **НЕТ.**
> Полная сходимость **68% < 80%**. Стандарт нуждается в доработке.

---

## 6. Рекомендации

Согласно критерию успеха (постановка задачи): при сходимости **< 80%** —
**доработать стандарт** и **повторить тест**. Конкретный план доработки (по
убыванию влияния на сходимость):

### P1 — Устранить структурную избыточность (тип 1, +до 5 функций к Σ)

1. **Дедуплицировать маршрутизацию в `contact-center`:** свести
   `call-routing` / `interaction-routing` (и пересечение с
   `omnichannel-contact-center`) к одному канону или задать явное правило выбора
   (#7).
2. **Устранить двойной `access-control`:** оставить либо capability
   `security/access-control`, либо feature
   `security/information-security/access-control`; смержить функции `assign-role`
   и `role-based-access-control` (#24).
3. **Снять синонимы function-узлов:** `accept-inbound-voice-call` vs
   `receive-inbound-call` под одним feature (#1); пересечение
   `call-routing-rules` vs `working-hours-schedule` в `cloud-pbx` (#3); дубль
   дашбордов `multichannel-analytics` vs `real-time-reporting/dashboard-view`
   (#21).
4. **Добавить в стандарт правило приоритета** на случай неустранимого
   пересечения: «выбирать узел с буквальным совпадением имени функции; при
   равенстве — наиболее специфичный/специализированный».

### P2 — Закрыть пробелы покрытия (тип 2, +до 3 функций к Σ)

5. Добавить канонические узлы (отдельная задача на правку реестра):
   **number-filtering/blacklist-whitelist** (#4),
   **call-transfer** (#8),
   **conversation-tagging** (#18, с явным решением: домен `ai-automation`
   speech-analytics vs `contact-center` agent-workspace).

### P3 — Уточнить определения `function_type` (тип 3, +до 4 функций к типу)

6. В §7.2 добавить **операционный тест-дерево** для разграничения
   `business` / `ui-action` / `configuration` на «просмотровых/статусных»
   действиях (прослушать запись, сменить статус, открыть панель, спланировать
   прогноз) с 3–5 разобранными примерами-прецедентами.

### P4 — Отдельный CR на эталонный реестр (вне рамок #174)

7. Исправить субоптимальные mapping'и в `kb/mango-taxonomy/mango-registry.json`,
   выявленные тестом: #21 (→ `real-time-reporting/dashboard-view/select-dashboard-widget`),
   при ревью также #3 и #24.

### Повторный прогон

8. После P1–P3 **повторить настоящий тест** (тот же набор 25 функций + желательно
   расширить до 30) тем же скриптом `experiments/issue-174/score_convergence.py`.
   Цель — Σ ≥ 80%. Только после этого фиксировать **v1.0**.

---

## 7. Артефакты теста

| Артефакт | Назначение |
|---|---|
| [`experiments/issue-174/blind-test-input.json`](../../experiments/issue-174/blind-test-input.json) | вход слепой классификации (25 функций, без ответов) |
| [`experiments/issue-174/reference-classification.json`](../../experiments/issue-174/reference-classification.json) | эталонная классификация (Rater A) |
| [`experiments/issue-174/blind-agent-output.json`](../../experiments/issue-174/blind-agent-output.json) | результат AI-агента (Rater B) |
| [`experiments/issue-174/comparison.json`](../../experiments/issue-174/comparison.json) | пофункциональное сравнение и флаги совпадений |
| [`experiments/issue-174/score_convergence.py`](../../experiments/issue-174/score_convergence.py) | скрипт подсчёта + валидатор канон-id |

> ⚠️ Стандарты и реестры в рамках задачи **не изменялись** (ограничение
> постановки). Все правки вынесены в раздел рекомендаций как отдельные задачи.
