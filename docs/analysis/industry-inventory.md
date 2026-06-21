---
status: active
version: 1.0
updated: 2026-06-21
ai-generated: true
type: research-inventory
scope: industry-taxonomy-registry-cascade-fill
issue: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/168"
related_artifacts:
  - "standards/decisions/ADR-011-industry-taxonomy.md"
  - "standards/industry-taxonomy-standard.md"
  - "kb/industry/reference-taxonomy.json"
  - "kb/industry/reference-taxonomy.schema.json"
  - "scripts/validate_issue_168_industry_reference_integrity.py"
hub_research:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/038868ddde36e1409ee32d43c0421e59c72eb9f3/classification.md"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/038868ddde36e1409ee32d43c0421e59c72eb9f3/capability-decomposition-2026-05.md"
---

# Industry Inventory — аналитическое доисследование для дозаполнения реестра (issue #168)

> **Назначение.** Обязательный первый шаг по issue #168 (Task 0): аналитическое
> исследование industry-ландшафта по ADR-011 перед заполнением
> `kb/industry/reference-taxonomy.json`. Документ фиксирует полные списки
> Capabilities, Features и Functions, которые добавляются в реестр, с
> **обоснованием каждой сущности** на основе отраслевой логики и стандартов, а
> также описывает разрывы (gaps) и способ их закрытия.
>
> Документ оформлен одновременно как **change request по §10.3** стандарта
> `standards/industry-taxonomy-standard.md` (problem statement → affected nodes →
> evidence → proposed nodes → migration note → validator changes → before/after →
> self-check).

> **Примечание о размещении файла.** DoD issue #168 называет путь
> `research/industry-inventory.md` со словом «**например**» (то есть путь —
> рекомендация, а не жёсткое требование). Репозиторий при этом:
> (a) ограничивает задачу констрейнтом «**не изменять структуру каталогов**» —
> новый top-level каталог `research/` создавать нельзя;
> (b) запрещает `research/` в корне на уровне стандарта (§12.8) и проверяет это в
> CI (`scripts/validate_issue_160_mango_registry.py`), а DoD #9 требует зелёного
> CI; (c) запрещает трогать компоненты, не относящиеся к Industry (в т.ч. Mango-
> валидатор). Единственная трактовка, совместимая со **всеми** этими
> ограничениями одновременно, — разместить документ в **существующем** каталоге
> `docs/analysis/`, который уже служит домом для Industry-аналитики (ср.
> `docs/analysis/voice-digital-channels-comparison.md`, на который реестр
> ссылается как на evidence). Слово «например» в постановке задачи прямо даёт
> такую свободу выбора пути.

## 0. Метод исследования

1. Источник истины по верхнему уровню — **ADR-011** (семь канонических доменов и
   `platform` как cross-domain layer) и нормативный стандарт
   `standards/industry-taxonomy-standard.md`.
2. Источник «спроса» на узлы — фактические внешние ссылки `industry_ref` в
   `kb/mango/*.yaml`. Эти ссылки **не меняются** (запрет issue): если ссылка не
   разрешается, это сигнал **пробела в Industry-реестре**, который нужно закрыть
   (issue #168, §1.4 / §11.3 стандарта: *Unknown canonical node = error*).
3. Каждая `industry_ref` была разобрана по цепочке
   `domain → capability → feature → function` и сопоставлена с вложенной
   структурой реестра (`domains[]` / `cross_domain_layers[]`). Полный разбор —
   воспроизводимый скрипт `experiments/analyze_issue_168_gaps.py` и
   `experiments/build_issue_168_registry.py`.
4. Перед добавлением каждый кандидат проверен по §10.1/§10.2 стандарта
   (когда узел добавлять можно/нельзя) и §3.3 (parent-child = semantic
   containment, а не «продаётся одним вендором» / «на одном экране»).
5. Если кандидат оказывался **алиасом существующего канонического узла**
   (§4.5), он закрывался через `aliases` существующего узла, а **не** новым
   дубликатом (запрет §10.2 «дублирует existing node under alias»).

### 0.1 Масштаб пробела (факт, воспроизводится `analyze_issue_168_gaps.py`)

| Метрика | Значение |
| --- | --- |
| Всего `industry_ref` в `kb/mango/*.yaml` | 316 |
| Не разрешалось до дозаполнения | 98 |
| Различных отсутствующих **capability** | 9 (одна из них — алиас) |
| Различных отсутствующих **feature** (parent существует) | 1 (алиас) |
| Различных отсутствующих **function** (parent существует) | 3 |
| Полных цепочек, востребованных под отсутствующими capability | 14 |

> Все 98 неразрешённых ссылок — без `mapping_gap`. По §8.4 `mapping_gap`
> ссылается на **ближайший существующий канонический parent**; здесь же
> отсутствовали сами capability/feature, поэтому ссылки были «жёстко» битыми
> (§11.3 *Invalid parent-chain = error*) и требовали закрытия добавлением
> канонических узлов.

## 1. Problem statement (§10.3)

Реестр `kb/industry/reference-taxonomy.json` v1.0.0 закрыл audit-blocker «ниже
Domain нет canonical registry», но оставался **неполным относительно
фактических внешних ссылок Mango**: 98 ссылок `industry_ref` не разрешались по
parent-chain. Это нарушает §11.3 («Unknown canonical node = error», «Invalid
parent-chain = error») и делает невозможной целостную проверку
referential-integrity (issue #168, Task 1.4 / Task 3).

Дополнительно: текущий Mango-валидатор
`scripts/validate_issue_160_mango_registry.py` проверяет ссылки против
**захардкоженного словаря `INDUSTRY`**, а не против реестра. Поэтому расхождение
«реестр ↔ реальные ссылки» было замаскировано (валидатор #160 проходил, хотя
ссылки не резолвились по реестру). Issue #168 требует добавить
**registry-backed** проверку (Task 3), не изменяя при этом сам Mango-валидатор.

## 2. Канонический контекст (ADR-011 + стандарт)

- Семь доменов (ADR-011 v1.0): `voice-ucaas`, `contact-center`,
  `digital-channels`, `ai-automation`, `analytics`, `hardware`, `security`.
- `platform` — cross-domain layer, не восьмой домен.
- Иерархия: `Domain → Capability → Feature → Function`; JSON Schema и hard
  contracts не нарушаются (issue #168, ограничения).
- §3.2 явно перечисляет неканонические кандидаты, которые **становятся
  каноническими только через change request §10.3**: `team-messaging`,
  `conversation-analytics`, `supervisor-workspace`, `role-management`.
  **Issue #168 — этот самый change request.**
- §8.4 даёт каноническую пару-пример: `contact-center / interaction-routing`
  c proposed feature `queue-routing`. §10.5 указывает `interaction-routing` как
  целевой `replacement` для устаревших routing-узлов. Это подтверждает
  каноничность `interaction-routing` и его подузлов.
- ADR-011 связывает `call-routing` с инфраструктурой `voice-ucaas`
  (`cloud-pbx`, `ivr-voice-menu`, `call-routing`) — основание для
  `voice-ucaas/call-routing`.

## 3. Принятые решения по спорным узлам

### 3.1 `platform/communications-apis` → **alias** существующего `cpaas`

`platform/cpaas` определён в реестре дословно как *«Programmable communications
APIs for voice, messaging, and numbers»* (features: `programmable-voice`,
`programmable-messaging`, `number-api`). Кандидат `communications-apis` —
**семантический алиас** этого узла. По §10.2 новый узел **нельзя** добавлять,
если он «дублирует existing node under alias». По §4.5 алиас МОЖЕТ резолвиться
в один канонический узел. **Решение:** добавить `communications-apis` в
`aliases` узла `cpaas`; новый узел НЕ создаётся. Ссылка
`platform/communications-apis` (только capability-уровень) разрешается через
alias.

### 3.2 `platform/open-api/webhook-management` → **alias** существующего `webhooks`

В `platform/open-api` уже есть feature `webhooks` («…covering webhooks»,
function `webhook-subscription`). Кандидат `webhook-management` покрывает тот же
жизненный цикл вебхуков (управление эндпоинтами). **Решение:** добавить
`webhook-management` в `aliases` feature `webhooks` и добавить недостающую
function `configure-webhook-endpoint` под `webhooks`. Ссылка
`open-api/webhook-management/configure-webhook-endpoint` разрешается через alias
+ новую function. Дубликат feature не создаётся (§10.2).

### 3.3 `security/access-control` — **новая capability** (IAM), не алиас

В реестре `access-control` существует как **feature** под
`security/information-security` (function `role-based-access-control`), что
соответствует §3.2 примеру. Mango ссылается на `security/access-control` как на
**capability** с feature `role-management` и function `assign-role`.

Identity & Access Management (IAM) — общепризнанная **самостоятельная
capability верхнего уровня** в отраслевых рамках (NIST SP 800-53 семейство
контролей **AC — Access Control**; ISO/IEC 27001:2022 Annex A **A.5.15–A.5.18**
управление доступом/правами; Gartner IAM как отдельный рынок). Её объём
(аутентификация, авторизация, роли, SSO, провижининг) **шире**, чем feature
`access-control` внутри программы информационной безопасности. Поэтому это **не**
алиас-дубликат по §10.2, а отдельная capability с собственным scope. Существующая
feature `information-security/access-control` сохраняется без изменений.

> **Рекомендация на будущее (не в этом PR):** провести консолидацию
> модели доступа — либо депрекация feature-узла в пользу capability
> `access-control`, либо явное разграничение scope через `aliases`. Любое
> изменение требует отдельного change request §10.3 + §10.5 (deprecation).

### 3.4 `voice-ucaas/call-routing` (новая) vs существующая `contact-center/call-routing`

ADR-011 относит `call-routing` к инфраструктуре `voice-ucaas`. Реестр исторически
разместил capability `call-routing` под `contact-center`. Slug уникален в
пределах level+parent (§4.1), поэтому одноимённая capability допустима под разными
доменами. **Решение:** добавить `voice-ucaas/call-routing` (маршрутизация на
уровне облачной АТС, по ADR-011); существующую `contact-center/call-routing` **не
удалять** (запрет на удаление без явного требования).

> **Рекомендация на будущее (не в этом PR):** депрекация
> `contact-center/call-routing` → `replacement: interaction-routing` по образцу
> §10.5 (omnichannel CC-routing концентрируется в `interaction-routing`, а PBX-
> маршрутизация — в `voice-ucaas/call-routing`).

## 4. Полный реестр добавляемых сущностей (с обоснованием)

Условные обозначения: **(M)** — сущность напрямую востребована ссылкой Mango;
**(filler)** — добавлена для выполнения schema-инварианта «у capability ≥1
feature, у feature ≥1 function» (`minItems:1`), но также отраслево осмысленна.
`function_type` ∈ {business, configuration, ui-action}. Evidence для всех новых
узлов: ADR-011 + стандарт + этот документ
(`docs/analysis/industry-inventory.md`).

### 4.1 Capabilities (parent → Domain)

| # | Capability | Parent Domain | Обоснование (industry) |
| --- | --- | --- | --- |
| C1 | `conversation-summaries` (M) | `ai-automation` | AI-генерация сводок разговоров (голос/текст) — самостоятельная CCaaS/AI-capability (generative AI summarization), отличная от `speech-analytics` (аналитика речи) и `chatbot`. Containment: материально обеспечивается AI → домен `ai-automation` (§5.7 «Правило AI»). |
| C2 | `real-time-reporting` (M) | `analytics` | Операционная отчётность/дашборды реального времени (wallboard, live KPI) — признанная analytics-capability, отличная от attribution-узлов (`call-tracking`, `end-to-end-analytics`) и `product-analytics`. Containment: измерение/визуализация → `analytics`. |
| C3 | `interaction-routing` (M) | `contact-center` | Канонический узел по §8.4 (пример) и §10.5 (`replacement`). Channel-agnostic маршрутизация обращений CC (ACD/omnichannel routing). Containment: распределение обращений между очередями/операторами → `contact-center`. |
| C4 | `supervisor-workspace` (M) | `contact-center` | §3.2/§8.4 явно называют `supervisor-workspace` кандидатом, который канонизируется через change request. Рабочая среда супервизора (live monitoring, coaching) — отдельная от `agent-workspace` и `supervisor-assist` (AI-подсказки). |
| C5 | `team-messaging` (M) | `digital-channels` | §3.2/§8.4 пример: `team-messaging` под `digital-channels` без узла в реестре. Внутрикомандный чат/коллаборация, дополняющий клиентские каналы. Containment: текстовый канал коммуникации → `digital-channels`. |
| C6 | `device-management` (M) | `hardware` | Провижининг/конфигурация/жизненный цикл телефонного и коммуникационного оборудования. Отличается от `telephony-equipment` (каталог устройств: `sip-phones`, `headsets`, `accessories`). Containment: управление физическими устройствами → `hardware`. |
| C7 | `access-control` (M) | `security` | IAM как самостоятельная capability верхнего уровня (NIST 800-53 AC; ISO/IEC 27001 A.5.15–A.5.18; Gartner IAM). Scope шире, чем feature `information-security/access-control`. См. §3.3. |
| C8 | `call-routing` (M) | `voice-ucaas` | По ADR-011 `call-routing` входит в инфраструктуру `voice-ucaas` (`cloud-pbx`, `ivr-voice-menu`, `call-routing`). PBX-маршрутизация вызовов. См. §3.4. |
| A1 | `communications-apis` (M) | `platform` | **Alias** существующего `cpaas` (§3.1). Новый узел не создаётся. |

### 4.2 Features (parent → Capability)

| # | Feature | Parent Capability | Обоснование |
| --- | --- | --- | --- |
| F1 | `ai-summary` (M) | `ai-automation/conversation-summaries` | Автоматическая генерация структурированной сводки одного разговора/треда. |
| F2 | `dashboard-view` (M) | `analytics/real-time-reporting` | Конфигурируемый дашборд реального времени (live KPI/метрики). |
| F3 | `queue-routing` (M) | `contact-center/interaction-routing` | §8.4 proposed feature `queue-routing`: назначение обращений по очередям и из очереди оператору. |
| F4 | `routing-rules` (M) | `contact-center/interaction-routing` | Конфигурируемые правила распределения обращений (skills/conditions). |
| F5 | `live-monitoring` (filler) | `contact-center/supervisor-workspace` | Наблюдение в реальном времени за активными обращениями/состоянием очередей и операторов. |
| F6 | `team-chat` (filler) | `digital-channels/team-messaging` | Канальный/прямой внутрикомандный чат. |
| F7 | `device-provisioning` (filler) | `hardware/device-management` | Регистрация, конфигурация и активация устройства. |
| F8 | `role-management` (M) | `security/access-control` | §3.2 пример: управление ролями и наборами прав; назначение ролей пользователям/группам. |
| F9 | `inbound-routing` (filler) | `voice-ucaas/call-routing` | Маршрутизация входящих вызовов по сценарию АТС на extension/группу/внешний номер. |
| A2 | `webhook-management` (M) | `platform/open-api` | **Alias** существующего feature `webhooks` (§3.2). Новый feature не создаётся. |

### 4.3 Functions (parent → Feature)

| # | Function | Parent Feature | `function_type` | Обоснование |
| --- | --- | --- | --- | --- |
| Fn1 | `generate-summary` (M) | `…/conversation-summaries/ai-summary` | business | Сформировать сводку по разговору. Facet `ai_assisted`. |
| Fn2 | `select-dashboard-widget` (M) | `…/real-time-reporting/dashboard-view` | ui-action | Выбор/размещение виджета метрики на дашборде. |
| Fn3 | `assign-interaction-to-agent` (filler) | `…/interaction-routing/queue-routing` | business | Канонический пример §3 стандарта: назначить обращение из очереди подходящему оператору. |
| Fn4 | `configure-routing-rule` (filler) | `…/interaction-routing/routing-rules` | configuration | Создать/обновить правило маршрутизации обращений. |
| Fn5 | `monitor-live-interactions` (filler) | `…/supervisor-workspace/live-monitoring` | ui-action | Представить супервизору активные обращения и состояния операторов. |
| Fn6 | `post-team-message` (filler) | `…/team-messaging/team-chat` | business | Отправить сообщение во внутренний командный канал/тред. Facet `channel` (text/async). |
| Fn7 | `provision-device` (filler) | `…/device-management/device-provisioning` | configuration | Зарегистрировать и сконфигурировать устройство. |
| Fn8 | `assign-role` (M) | `…/access-control/role-management` | configuration | Назначить роль пользователю/группе. Facet `security_compliance`. |
| Fn9 | `route-inbound-call` (filler) | `…/call-routing/inbound-routing` | business | Маршрутизировать входящий вызов по сценарию АТС. Facet `channel` (voice/sync/inbound). |
| Fn10 | `configure-webhook-endpoint` (M) | `…/open-api/webhooks` (alias `webhook-management`) | configuration | Зарегистрировать/обновить webhook-эндпоинт и параметры доставки. |
| Fn11 | `start-campaign` (M) | `…/outbound-calling/campaign-management` | business | Запустить исходящую обзвонную кампанию. Facet `channel` (voice/sync/outbound), `commercial`. |
| Fn12 | `send-message` (M) | `…/omnichannel-messaging/messenger-integration` | business | Отправить сообщение клиенту через интегрированный мессенджер. Facet `channel` (text/async/outbound). |
| Fn13 | `receive-inbound-call` (M) | `…/voice-channel/inbound-voice-call` | business | Принять входящий вызов в голосовом канале. Facet `channel` (voice/sync/inbound). |

### 4.4 Aliases (на существующие канонические узлы)

| Alias | Канонический узел | Уровень | Основание |
| --- | --- | --- | --- |
| `communications-apis` | `platform/cpaas` | capability | §3.1 / §4.5 / §10.2 |
| `webhook-management` | `platform/open-api/webhooks` | feature | §3.2 / §4.5 / §10.2 |

### 4.5 Карта «востребованная цепочка Mango → закрывающий узел»

Все 14 полных цепочек, востребованных Mango под отсутствующими подграфами,
после дозаполнения разрешаются полностью:

| Цепочка из `kb/mango/*.yaml` | Чем закрыта |
| --- | --- |
| `ai-automation/conversation-summaries/ai-summary` | C1+F1 |
| `ai-automation/conversation-summaries/ai-summary/generate-summary` | C1+F1+Fn1 |
| `analytics/real-time-reporting` | C2 |
| `analytics/real-time-reporting/dashboard-view/select-dashboard-widget` | C2+F2+Fn2 |
| `contact-center/interaction-routing/queue-routing` | C3+F3 |
| `contact-center/interaction-routing/routing-rules` | C3+F4 |
| `contact-center/supervisor-workspace` | C4 |
| `digital-channels/team-messaging` | C5 |
| `hardware/device-management` | C6 |
| `platform/communications-apis` | A1 (alias → `cpaas`) |
| `security/access-control` | C7 |
| `security/access-control/role-management` | C7+F8 |
| `security/access-control/role-management/assign-role` | C7+F8+Fn8 |
| `voice-ucaas/call-routing` | C8 |
| `platform/open-api/webhook-management` (+`/configure-webhook-endpoint`) | A2 (alias → `webhooks`) + Fn10 |
| `contact-center/outbound-calling/campaign-management/start-campaign` | Fn11 (под существующей feature) |
| `digital-channels/omnichannel-messaging/messenger-integration/send-message` | Fn12 (под существующей feature) |
| `voice-ucaas/voice-channel/inbound-voice-call/receive-inbound-call` | Fn13 (под существующей feature) |

## 5. Affected nodes and mappings (§10.3)

- **Реестр:** `kb/industry/reference-taxonomy.json` — добавлены 8 capabilities,
  9 features, 13 functions, 2 alias-записи; `version` 1.0.0 → 1.1.0; добавлены
  source-запись `issue-168-industry-inventory` и registry-note. Существующие узлы
  **не изменялись и не удалялись**. Evidence новых узлов:
  `standards/decisions/ADR-011-industry-taxonomy.md`,
  `standards/industry-taxonomy-standard.md`,
  `docs/analysis/industry-inventory.md` (этот документ).
- **JSON Schema:** изменения **не требуются** (вложенная модель уже поддерживает
  все уровни; `aliases` допустимы — у node_base нет `additionalProperties:false`).
- **Mango (`kb/mango/*.yaml`):** **не изменяются** (запрет issue). После
  дозаполнения все 316 ссылок `industry_ref` разрешаются по parent-chain (включая
  alias-резолвинг).
- **Стандарт, ADR-011 и Mango-валидатор:** **не изменяются** (запрет issue).

## 6. Migration / compatibility note (§10.3, §10.4)

- Изменение **additive** → по §10.4 это **minor**: `1.0.0 → 1.1.0`.
- Обратная совместимость: существующие mappings и узлы не затронуты; новые узлы
  только расширяют дерево. Канонические slug не переименовывались.
- Алиасы (`communications-apis`, `webhook-management`) не меняют канонические id;
  они лишь обеспечивают резолвинг существующих ссылок Mango в канонические узлы.

## 7. Validator changes (§10.3, issue Task 3)

Добавлен **registry-backed** валидатор
`scripts/validate_issue_168_industry_reference_integrity.py` (stdlib-only),
реализующий подмножество §11.2 для текущего артефакта-реестра:

- (4) `industry_ref.domain` существует в `domains[]`/`cross_domain_layers[]`;
- (5–7) `capability`/`feature`/`function` принадлежат своему parent (с учётом
  `aliases`, §4.5);
- (8) запрет «глубокого поля без parent» (function без feature и т.п.);
- (9) `alignment_type` ∈ {primary, secondary, supporting} (если задан);
- (11–13) enum-значения facet `channel`;
- (19) slug-pattern для значений `industry_ref`;
- (20) запрет произвольных ключей внутри `industry_ref`;
- (18) evidence_refs новых узлов резолвятся в существующий путь репозитория или
  полный URL;
- (21–22) lifecycle: `deprecated` → warning, `removed` → error при разрешении.

Валидатор подключён в `Makefile` (`kb-validate`) и в
`.github/workflows/kb.yml`. Существующие валидаторы #152/#156/#160 продолжают
проходить (additive-изменение; #156 использует множества и проверяет минимумы и
required-наборы; #160 не затронут, т.к. он Mango-side и не модифицируется).

## 8. Examples before/after (§10.3)

**Before** (ссылка не разрешалась → §11.3 error):

```jsonc
// kb/mango/internal-registry.yaml (industry_ref)
{ "domain": "contact-center", "capability": "interaction-routing", "feature": "queue-routing" }
// registry v1.0.0: contact-center.capabilities[] не содержит interaction-routing → UNRESOLVED
```

**After** (узлы добавлены → ссылка разрешается):

```jsonc
// registry v1.1.0
// contact-center → interaction-routing (capability) → queue-routing (feature)
//   → assign-interaction-to-agent (function)  ✔ resolved
```

**Alias before/after:**

```jsonc
// Before: { "domain": "platform", "capability": "communications-apis" }  → UNRESOLVED
// After:  platform/cpaas.aliases += ["communications-apis"]              → resolves to cpaas ✔
```

## 9. Самопроверка против стандарта (§10.3 self-check)

- [x] §3.2 неканонические кандидаты (`team-messaging`, `supervisor-workspace`,
  `role-management`) канонизированы **через change request** (этот документ), а
  не «молча».
- [x] §3.3 для каждого узла указан **semantic containment** в parent (а не
  «один вендор / один экран / один тариф»).
- [x] §10.1 у каждого нового узла есть evidence и понятная parent-chain;
  кандидаты с алиасами не дублируются (§10.2).
- [x] §10.2 алиас-дубликаты (`communications-apis`, `webhook-management`) закрыты
  через `aliases`, а не новыми узлами.
- [x] §4.1 slug-pattern соблюдён; уникальность в пределах level+parent.
- [x] §4.5 алиас резолвится в **один** канонический узел; нет ambiguous-алиасов.
- [x] §7 у functions заданы `function_type` и `parameters`; facets — где есть
  channel/ai/security/commercial-релевантность.
- [x] §10.4 версия реестра поднята minor (1.0.0 → 1.1.0).
- [x] §11.3 после дозаполнения нет «Unknown canonical node» / «Invalid
  parent-chain» среди ссылок Mango (0 из 316).
- [x] Стандарт, ADR-011, `kb/mango/*` и Mango-валидатор не изменялись;
  структура каталогов не менялась (документ размещён в существующем
  `docs/analysis/`).

> **Замечание о §12.8.** Стандарт §12.8 советует AI-агенту «не создавать
> `research/` in this spoke», и CI это проверяет. Issue #168 называет
> `research/industry-inventory.md` через «например». Конфликт разрешён
> размещением документа в существующем `docs/analysis/` (см. примечание в шапке)
> — это сохраняет зелёный CI (DoD #9) и не нарушает ни одного жёсткого
> ограничения.

## 10. Воспроизводимость

- `experiments/analyze_issue_168_gaps.py` — разбор всех `industry_ref` и список
  неразрешённых сущностей по уровням (alias-aware).
- `experiments/build_issue_168_registry.py` — детерминированная вставка узлов и
  алиасов в реестр с минимальным diff (round-trip `json.dumps(indent=2,
  ensure_ascii=False)`), bump версии, source-запись и registry-note.
- `scripts/validate_issue_168_industry_reference_integrity.py` — проверка
  целостности ссылок против реестра (CI, stdlib-only, alias-aware).
