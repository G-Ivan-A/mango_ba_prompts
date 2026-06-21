---
status: canonical
version: 1.0
updated: 2026-06-21
ai-generated: true
type: adr
scope: mango-taxonomy
issue: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/142"
validated_by:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/146"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/148"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/154"
depends_on:
  - "standards/decisions/ADR-011-industry-taxonomy.md"
  - "standards/industry-taxonomy-standard.md"
hub_research: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/mango/classification.md"
hub_research_sha: "3aa12727c9b87d5cf68301fa95d00a272408a97e"
site_sources:
  - "https://www.mango-office.ru/"
  - "https://www.mango-office.ru/products/"
related_prs:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/pull/143"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/pull/149"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/pull/155"
related_artifacts:
  - "standards/decisions/ADR-011-industry-taxonomy.md"
  - "standards/industry-taxonomy-standard.md"
  - "standards/mango-taxonomy-standard.md"
  - "standards/product-classification-contract.md"
  - "docs/audit/issue-146-mango-taxonomy-validation.md"
  - "docs/analysis/voice-digital-channels-comparison.md"
  - "kb/mango-product-docs/processed/"
---

# ADR-012: Mango Taxonomy для корпоративной таксономии продуктов Mango Office

> **Статус:** Canonical · **Дата:** 2026-06-21 · **Issue:**
> <https://github.com/G-Ivan-A/mango_ba_prompts/issues/142> · **Canonicalized by:**
> <https://github.com/G-Ivan-A/mango_ba_prompts/issues/154> · **Depends on:**
> [`ADR-011`](ADR-011-industry-taxonomy.md)

> **Numbering note.** ADR-012 продолжает дорожку `standards/decisions/`
> вслед за ADR-011, потому что issue #142 явно требует путь
> `standards/decisions/ADR-012-mango-taxonomy.md`.

## Canonicalization note

Issue #154 завершает follow-up к issue #142: ADR-012 переведён в
`status: canonical`, `version: 1.0`, а нормативные machine-readable правила
вынесены в [`standards/mango-taxonomy-standard.md`](../mango-taxonomy-standard.md).
Стандарт является обязательным operational companion к этому ADR для AI-агентов,
валидаторов CI и будущих registry entries.

Canonicalization наследует решения ADR-011 canonical v1.0 и Industry Taxonomy
Standard: strict `industry_ref`, `alignment_type` (`primary`, `secondary`,
`supporting`), cross-cutting facets, first-class `voice-channel` внутри
`voice-ucaas` и facet `channel` (`channel_kind`, `synchronicity`, `direction`).
Голосовая инфраструктура (`sip-connectivity`, numbering) остаётся supporting
resource mapping, а голосовое interaction mapping ДОЛЖНО использовать
`voice-channel` and/or `channel`.

### Приоритет источников и синхронизация с ADR-011

Чтобы исключить инверсию приоритета между документами (issue #166), фиксируется
единый, симметричный порядок источников:

> **ADR-011 имеет приоритет над ADR-012.** Если ADR-012, Mango Taxonomy Standard
> или старый Mango crosswalk противоречат ADR-011 либо каноничному реестру
> `kb/industry/reference-taxonomy.json` по slug'у домена, capability, feature,
> function или по форме `industry_ref` — применяется ADR-011. ADR-012 остаётся
> источником истины только для Mango-specific слоя
> `Product -> Service -> Module -> Function` там, где он не конфликтует с ADR-011.

Этот порядок дословно совпадает с §1.3 обоих стандартов
([`industry-taxonomy-standard.md`](../industry-taxonomy-standard.md) и
[`mango-taxonomy-standard.md`](../mango-taxonomy-standard.md)) и с разделом
«Приоритет источников и согласованность с ADR-012» в
[`ADR-011`](ADR-011-industry-taxonomy.md). Все machine-readable примеры в этом ADR
используют каноничные имена полей (`level`, `official_urls`,
`supported_by_services`, `evidence_refs`, `maps_to.industry_alignment[]`) и
каноничные slug'и из `kb/industry/reference-taxonomy.json`; устаревшие черновые
имена (`layer`, `public_urls`, `internal_services`, `kb_refs`, `evidence_level`)
больше не используются.

> **Reference integrity.** Все slug'и `domain`/`capability`/`feature`/`function`
> в примерах ниже резолвятся в каноничном реестре
> [`kb/industry/reference-taxonomy.json`](../../kb/industry/reference-taxonomy.json);
> Mango entity-имена и кластеры соответствуют
> [`mango-taxonomy-standard.md`](../mango-taxonomy-standard.md).

## Контекст

Issue #142 требует зафиксировать решение по **Mango Taxonomy**:
корпоративной таксономии продуктов Mango Office. Это не отраслевой эталон и не
финальный реестр продуктов. Таксономия должна описывать, как публичные
продуктовые названия Mango соотносятся с внутренними сервисами, модулями и
функциями, которые встречаются в обработанной базе знаний.

ADR-011 уже зафиксировал опорную Industry Taxonomy:

```text
Domain -> Capability -> Feature -> Function
```

Mango Taxonomy должна быть совместима с этой моделью, но решает другую задачу:
она нормализует продуктовый контур конкретного вендора Mango Office. Поэтому
она не заменяет ADR-011, а добавляет вендорский слой поверх него.

Исходные ограничения issue #142 действовали только на первый proposed ADR:

- создать только этот ADR;
- обновить только `CHANGELOG.md`;
- не создавать стандарт, KB-реестр или дополнительные production-артефакты;
- использовать ADR-011, Hub classification, официальный сайт Mango Office и
  только обработанные markdown-документы в `kb/mango-product-docs/processed/`.

Issue #154 явно снимает ограничение на стандарт и требует
`standards/mango-taxonomy-standard.md`; это не меняет исходное решение ADR-012,
а переводит его в canonical status и добавляет machine-readable операционный
контракт.

## Research: источники

| Источник | Что проверено | Роль в решении |
| --- | --- | --- |
| [`ADR-011`](ADR-011-industry-taxonomy.md) | Industry Taxonomy, домены, capability-уровень, cross-domain `platform`, leaf-level `Function` и отделение Product Layer от Commercial Layer. | Задаёт внешний слой выравнивания для Mango Taxonomy. |
| Hub classification: <https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/mango/classification.md> | Mango-ориентированная модель v3.0; свежий blob SHA `3aa12727c9b87d5cf68301fa95d00a272408a97e`. | Даёт исходную гипотезу по доменам, capability и Product/Commercial separation. |
| Официальный сайт: <https://www.mango-office.ru/> | Публичные продуктовые группы: бизнес-телефония, омниканальный контакт-центр, роботы и аналитика, маркетинговые технологии. | Показывает официальный внешний слой и маркетинговые группировки. |
| Каталог продуктов: <https://www.mango-office.ru/products/> | Публичный каталог: ВАТС, гибридная АТС, номера, контакт-центр, calltracking, оборудование, Mango Talker, API, интеграции, отраслевые/размерные решения. | Уточняет, какие названия допустимо считать official-layer сигналом. |
| `kb/mango-product-docs/processed/` | Обработанные markdown-документы по ВАТС, контакт-центру, API, интеграциям, Mango Talker, речевой аналитике, качеству, Wallboard, SIP Trunk, SSO и ролям. | Показывает внутренние сервисы, модули, операции и документационные границы. |
| [`docs/audit/issue-146-mango-taxonomy-validation.md`](../../docs/audit/issue-146-mango-taxonomy-validation.md) | Проверка 12 processed guides: CC, LK/VATS, Mango Talker, Bitrix24, SIP Trunk, API, Dialogi API, speech analytics, quality management, Wallboard. | Подтверждает, что операции, API-команды, настройки и действия нужно хранить как Mango `Function`. |

## Research: официальный слой

Официальный сайт даёт не техническую декомпозицию, а витрину продуктов,
решений и коммерчески понятных групп. Для Mango Taxonomy это означает, что
официальный слой должен фиксировать публичное имя, URL и продуктовую семантику,
но не обязан совпадать с внутренними сервисными границами.

| Official Product / Family | Сигнал с сайта | Роль в Mango Taxonomy | Выравнивание с ADR-011 |
| --- | --- | --- | --- |
| `mango-virtual-pbx` | Виртуальная АТС, гибридная АТС, IP-телефония, номера, IVR, запись, callback, SIP Trunk. | Главный official-layer продукт бизнес-телефонии. | `voice-ucaas`, `platform-integration`, частично `security`. |
| `mango-contact-center` | Омниканальный контакт-центр, каналы, рабочее место оператора, исходящие кампании, аналитика, WFM. | Official-layer продукт для customer operations. | `contact-center`, `digital-channels`, `analytics`, `ai-automation`. |
| `mango-talker` | Корпоративный мессенджер, звонки, чаты, каналы, видеосвязь, мобильные и desktop-клиенты. | UC-клиент и collaboration-продукт, связанный с ВАТС. | `voice-ucaas`, `digital-channels`. |
| `mango-robots` | Голосовые роботы, чат-боты, процессные роботы и AI-сценарии. | Official-layer группа автоматизации. | `ai-automation`, `contact-center`, `digital-channels`. |
| `mango-speech-analytics` | Речевая аналитика, контроль качества, AI-анализ коммуникаций. | Official-layer аналитический/AI-продукт. | `ai-automation`, `analytics`, `contact-center`. |
| `mango-marketing-analytics` | Calltracking, сквозная и мультиканальная аналитика, email tracking, competitor analysis. | Official-layer группа маркетинговой аналитики. | `analytics`, частично `voice-ucaas`. |
| `mango-text-communications` | Сайт-чат, мессенджеры, омниканальные диалоги, SMS и рассылки. | Official-layer продукт/набор каналов для digital communications. | `digital-channels`, `contact-center`, `cpaas`. |
| `mango-open-platform` | API, интеграции, webhooks, 1C, CRM-интеграции, сервисы подключения. | Platform/supporting official group, а не отдельный прикладной продукт. | `platform`, `open-api`, `platform-integration`, `cpaas`. |
| `mango-numbers-equipment` | Городские номера, 8-800, мобильные номера, SIP-телефоны, гарнитуры. | Resource/hardware слой, который поддерживает продукты. | `voice-ucaas`, `hardware`. |
| `mango-solution-pack` | Решения по размеру бизнеса, отраслям и задачам. | Facet/packaging layer; не должен становиться отдельной веткой Product. | `industry`, `segment`, `use_case` как фасеты. |

Вывод: официальный слой должен быть устойчив к публичным переименованиям и
маркетинговым группировкам. Один official product может покрывать несколько
отраслевых доменов, а одна внутренняя возможность может поддерживать несколько
official products.

## Research: внутренний слой

Обработанные markdown-документы в `kb/mango-product-docs/processed/` дают
другой сигнал: не витрину, а фактические функциональные зоны, операции,
интеграции и настройки. Этот слой пригоден для service/module границ и
evidence links. Исходные PDF из `kb/mango-product-docs/sources/` для этого ADR
не использовались.

| Внутренний кластер | Документы processed KB | Что фиксировать в Mango Taxonomy |
| --- | --- | --- |
| VATS core и администрирование | `mango-lk-manual`, `Rolevaya-model-vats`, `sip-trunk`, `vpbx-api` | Сотрудники, группы, номера, маршрутизация, IVR, запись, SIP, SMS, callback, автодозвон, роли, статистика, интеграции, webhooks, API. |
| Contact Center core | `mango-cc-manual`, `contact-center-manual-sample`, `wallboard` | Очереди обращений, статусы операторов, рабочее место, исходящие кампании, dashboard, WFM, сделки, задачи, отчёты, мониторинг. |
| Digital channels и диалоги | `mango-lk-manual`, `mango-cc-manual`, `mdialogi-api` | Чаты сайта, мессенджеры, email, Avito, MAX, шаблоны, каналы обращений, API диалогов. |
| Mango Talker / UC client | `mtalker/*` | Desktop/mobile клиент, звонки, контакты, статусы, чаты, каналы, видео, настройки и администрирование клиента. |
| AI, speech analytics и quality | `speech-analytics/*`, `quality-managment`, `mango-cc-manual` | Речевая аналитика, скоринг, контроль качества, чек-листы, категории, AI-темы, оценка звонков и чатов. |
| Analytics и marketing | `mango-lk-manual`, `wallboard`, `speech-analytics/*`, `vpbx-api` | Calltracking, отчёты, сквозная аналитика, product analytics, competitor analysis, real-time displays, выгрузки и события API. |
| Platform integrations | `integration-bitrix24`, `integration_1c`, `integration_amocrm`, `vpbx-api`, `lk-vats-sso` | CRM/ERP-интеграции, API, webhooks, SSO, LDAP, API connector, роли доступа и события. |
| Security and access | `Rolevaya-model-vats`, `lk-vats-sso`, security-разделы `mango-lk-manual` | Ролевая модель, SSO, права на модули, доступ к записям, настройкам, отчётам и интеграциям. |

Выводы по processed KB:

- документация подтверждает внутренние границы сервисов, модулей и функций, но
  не даёт единого нормализованного product registry;
- публичные product names и внутренние document/module names часто не
  совпадают;
- часть возможностей является cross-product: роли, SSO, API, speech analytics,
  digital channels, отчёты и интеграции;
- повторяющийся leaf-level сигнал — конкретные настройки, действия,
  API-команды, параметры и операции пользователя; их нужно фиксировать как
  `Function`, а не прятать в описании модуля;
- коммерческие тарифы, решения по отраслям и procurement-признаки не должны
  попадать в иерархию Product -> Service -> Module -> Function.

## Рассмотренные альтернативы

| Вариант | Описание | Плюсы | Минусы |
| --- | --- | --- | --- |
| A. Flat product list | Вести один список публичных продуктов с URL и коротким описанием. | Быстро, понятно для витрины и changelog. | Не отражает внутренние модули, cross-product функции и связь с ADR-011; плохо подходит для KB/RAG и трассировки требований. |
| B. Two-layer taxonomy + Function | Разделить Official Layer и Internal Layer, связав их many-to-many отношениями и выравниванием на ADR-011; внутри Internal Layer использовать четыре уровня `Product -> Service -> Module -> Function`. | Сохраняет публичную семантику, объясняет внутренние границы, поддерживает трассировку, future KB registry и симметрию с ADR-011. | Требует явного governance для ID, статусов, владельцев, function-granularity и source evidence. |
| C. Product -> Service -> Module без слоёв | Ввести только иерархию Product -> Service -> Module. | Даёт полезную структуру и похожа на будущий data model. | Смешивает публичные названия с внутренними границами; не объясняет, почему один модуль обслуживает несколько продуктов. |

## Решение

Принять вариант **B: Two-layer taxonomy + Function**. Иерархия
`Product -> Service -> Module -> Function` используется внутри этой двухслойной
модели, но не заменяет разделение Official/Internal.

### Слои

**Official Layer** фиксирует публичную продуктовую витрину Mango Office:

- official product id;
- публичное название и aliases;
- официальный URL;
- product family / solution family;
- публичные сегменты и use-case facets;
- lifecycle/status, если он явно известен;
- source references на официальный сайт.

**Internal Layer** фиксирует функциональную и документационную структуру:

- service id;
- module id;
- function id;
- internal aliases;
- owning area/team, если известны;
- lifecycle/status, если известен;
- links на processed KB, API docs и integration docs;
- alignment на ADR-011 Domain/Capability/Feature/Function;
- confidence/evidence level.

### Иерархия

Mango Taxonomy использует четыре основных уровня:

```text
Product -> Service -> Module -> Function
```

Границы уровней:

- **Product**: official-layer продукт или семейство продуктов, видимое снаружи
  и связанное с публичным URL. Примеры: `mango-virtual-pbx`,
  `mango-contact-center`, `mango-talker`, `mango-speech-analytics`.
- **Service**: внутренний функциональный сервис или capability-зона, которая
  реализует часть одного или нескольких products. Примеры:
  `voice-routing`, `number-management`, `agent-workspace`,
  `outbound-campaigns`, `digital-channel-management`, `open-api`,
  `crm-integrations`, `access-control`.
- **Module**: конкретный модуль, экран, API-группа, настройка или
  эксплуатационный блок, подтверждённый processed KB. Примеры:
  `ivr-rules`, `call-recording`, `sip-trunk`, `webhooks`, `sso`,
  `telegram-channel`, `wallboard`, `quality-scorecard`,
  `speech-analytics-checklist`.
- **Function**: минимальная проверяемая функция, операция, API-команда,
  настройка, параметр или правило внутри модуля. Примеры:
  `transfer-call`, `set-agent-status`, `create-outbound-campaign`,
  `configure-webhook-url`, `get-blacklist-mode`, `send-dialog-message`,
  `select-wallboard-widget`, `enable-ai-summary`.

Mango `Service` выравнивается на ADR-011 `Capability`, Mango `Module`
выравнивается на ADR-011 `Feature`. Mango `Function` выравнивается на ADR-011 `Function`.
Product может иметь более широкие many-to-many связи с Domain,
Capability и cross-domain facets, потому что публичные продукты Mango часто
объединяют несколько отраслевых доменов.

### Отношения

Минимальный набор отношений для будущего стандарта:

| Relationship | Кардинальность | Назначение |
| --- | --- | --- |
| `official_product.supported_by_services[]` | many-to-many | Связать публичную витрину с внутренними сервисами. |
| `internal_service.modules[]` | one-to-many или many-to-many | Показать, какие модули реализуют сервис. |
| `module.functions[]` | one-to-many | Показать leaf-level действия, настройки, API-команды и правила модуля. |
| `module.evidence_refs[]` | one-to-many | Привязать модуль к processed KB evidence. |
| `function.evidence_refs[]` | one-to-many | Привязать функцию к конкретному processed KB evidence. |
| `service.maps_to.industry_alignment[]` | one-to-many | Связать сервис с ADR-011 Domain/Capability. |
| `module.maps_to.industry_alignment[]` | one-to-many | Связать модуль с ADR-011 Feature. |
| `function.maps_to.industry_alignment[]` | one-to-many | Связать Mango function с ADR-011 Function. |
| `entity.facets[]` | many-to-many | Хранить commercial, segment, industry, compliance и region overlays вне иерархии. |

Каноничное имя связи official → internal — `supported_by_services[]`
(см. §3.2 [`mango-taxonomy-standard.md`](../mango-taxonomy-standard.md)); черновое
имя `internal_services[]` устарело. Industry-выравнивание всегда хранится внутри
контейнера `maps_to.industry_alignment[]`, а evidence — в `evidence_refs[]`.

### Атрибуты

Рекомендуемый атрибутный минимум:

```yaml
official_product:
  id: mango-contact-center
  level: official-product
  name_ru: Омниканальный контакт-центр
  official_urls:
    - https://www.mango-office.ru/products/
  aliases: []
  official_family: contact-center
  lifecycle_status: active
  facets:
    segment: []
    industry: []
    use_case: []
  supported_by_services:
    - agent-workspace
    - omnichannel-queue-management
    - outbound-campaigns
  evidence_refs:
    - standards/decisions/ADR-012-mango-taxonomy.md
    - https://www.mango-office.ru/products/

internal_service:
  id: omnichannel-queue-management
  level: service
  name_ru: Управление очередями обращений
  parent_products:
    - mango-contact-center
  lifecycle_status: active
  maps_to:
    industry_alignment:
      - industry_ref:
          domain: contact-center
          capability: omnichannel-contact-center
        alignment_type: primary
  evidence_refs:
    - kb/mango-product-docs/processed/mango-cc-manual/index.md

module:
  id: wallboard
  level: module
  parent_services:
    - contact-center-monitoring
  lifecycle_status: active
  maps_to:
    industry_alignment:
      - industry_ref:
          domain: contact-center
          capability: supervisor-assist
          feature: live-monitoring
        alignment_type: primary
      - industry_ref:
          domain: analytics
          capability: product-analytics
          feature: demand-analysis
        alignment_type: supporting
  evidence_refs:
    - kb/mango-product-docs/processed/wallboard/index.md

function:
  id: select-wallboard-widget
  level: function
  parent_module: wallboard
  function_type: ui-action
  maps_to:
    industry_alignment:
      - industry_ref:
          domain: contact-center
          capability: supervisor-assist
          feature: live-monitoring
          function: manage-live-monitoring
        alignment_type: primary
      - industry_ref:
          domain: analytics
          capability: product-analytics
          feature: demand-analysis
          function: demand-analysis
        alignment_type: supporting
  evidence_refs:
    - kb/mango-product-docs/processed/wallboard/sections/04-nastroyka-wallboard.md
```

### Атрибуты Function

`Function` остаётся leaf-level единицей Mango Taxonomy: минимальным
проверяемым поведением, настройкой, API-командой, UI-действием, параметром или
правилом внутри Module. Для будущего стандарта каждая Function должна иметь
следующий минимум:

```yaml
function:
  id: configure-webhook-url
  level: function
  parent_module: webhooks
  name_ru: Настроить URL webhook
  function_type: configuration
  interaction_surface: admin-ui
  source_terms:
    - operation
    - setting
  aliases:
    - configure-callback-url
  maps_to:
    industry_alignment:
      - industry_ref:
          domain: platform
          capability: open-api
          feature: webhooks
          function: webhook-subscription
        alignment_type: supporting
  evidence_refs:
    - kb/mango-product-docs/processed/vpbx-api/index.md
```

`function_type` классифицирует смысл функции, а не канал реализации. API,
экран или background job фиксируются отдельно в `interaction_surface`.

| `function_type` | Когда использовать | Примеры | Использование в требованиях |
| --- | --- | --- | --- |
| `business` | Функция создаёт клиентский или операционный бизнес-результат. | `transfer-call`, `send-dialog-message`, `create-outbound-campaign`, `generate-ai-summary`. | Генерировать ФТ, acceptance criteria, бизнес-правила и gap analysis. |
| `configuration` | Функция меняет настройку, политику, маршрутизацию, доступ или lifecycle параметр сервиса. | `configure-webhook-url`, `enable-call-recording`, `set-queue-schedule`, `assign-agent-role`. | Генерировать admin requirements, migration checklist, controls and rollback steps. |
| `ui-action` | Функция описывает пользовательское действие в интерфейсе, нужное для сценария, но не является самостоятельной бизнес-возможностью. | `select-wallboard-widget`, `open-call-filter`, `switch-agent-tab`, `expand-report-section`. | Генерировать UX/UI acceptance criteria, сценарии обучения и e2e шаги, не раздувая product capability list. |

Внешнее обоснование:

| Источник | Сигнал | Решение для Mango Taxonomy |
| --- | --- | --- |
| TM Forum SID: <https://www.tmforum.org/open-digital-architecture/information-framework-sid/> | SID даёт общий словарь и data reference model для business entities, function, application, component и API development. | `Function` остаётся leaf-level, а Component не становится отдельным уровнем: source-specific Component нормализуется в Mango `Module`. |
| TM Forum ODA Functional Framework: <https://www.tmforum.org/open-digital-architecture/functional-framework/> | Functional Framework описывает granular functions как базовые единицы, которые выполняют service and produce a complete result. | `business` фиксирует функции, которые дают завершённый результат, независимо от того, вызваны они UI или API. |
| ITIL 4 Service Configuration Management: <https://www.axelos.com/certifications/itil-service-management/itil-practices-manager/itil-4-specialist-plan-implement-and-control/itil-4-practitioner-service-configuration-management> | ITIL 4 отделяет configuration information/support items от остального service management. | `configuration` отделяет настройки и управление конфигурацией от бизнес-функций и UI-шагов. |
| ISO/IEC 25010:2023: <https://www.iso.org/standard/78176.html> | ISO/IEC 25010:2023 используется для requirements specification, evaluation, testing objectives and acceptance criteria of ICT products. | `business` и `ui-action` разделяют функциональный результат и interaction-oriented проверку, чтобы требования и acceptance criteria не смешивали capability с экранным шагом. |

### Алиасы терминов

Canonical taxonomy terms должны использоваться в ADR, standards, validators and
future registry. Source terms из Mango docs сохраняются как aliases/source_terms,
но не создают новые уровни.

| Source term | Canonical term | Правило использования |
| --- | --- | --- |
| Component | Module | Component=Module. Если processed KB или внешний источник говорит Component, в registry пишем `module`, а исходный термин сохраняем в `aliases` или `source_terms`. |
| Operation | Function | Operation=Function. API operation, user operation или operational step нормализуется в `Function`, если это проверяемое leaf-level действие, команда, настройка или правило. |

Дополнительные слова вроде action, setting, endpoint, command и parameter
являются evidence terms. Они помогают выбрать `function_type`, но не заменяют
canonical уровни `Product -> Service -> Module -> Function`.

### Формат маппинга

Product-to-Industry mapping хранится как typed YAML/JSON object с массивом
`industry_alignment`. Значения внутри `industry_ref` являются строгими ссылками
на Industry Taxonomy, не свободные теги.

```yaml
taxonomy_mapping:
  version: 1
  mapping_scope: mango-to-industry
  source_taxonomy: mango-taxonomy
  target_taxonomy: industry-taxonomy
  products:
    - product_id: mango-contact-center
      industry_alignment:
        - industry_ref:
            domain: contact-center
            capability: omnichannel-contact-center
          alignment_type: primary
          evidence_refs:
            - standards/decisions/ADR-012-mango-taxonomy.md
            - kb/mango-product-docs/processed/mango-cc-manual/index.md
        - industry_ref:
            domain: digital-channels
            capability: omnichannel-messaging
          alignment_type: secondary
          evidence_refs:
            - kb/mango-product-docs/processed/mdialogi-api/index.md
  services:
    - service_id: open-api
      supports_official_products:
        - mango-virtual-pbx
        - mango-contact-center
      industry_alignment:
        - industry_ref:
            domain: platform
            capability: open-api
          alignment_type: supporting
          evidence_refs:
            - kb/mango-product-docs/processed/vpbx-api/index.md
  functions:
    - function_id: configure-webhook-url
      function_type: configuration
      industry_alignment:
        - industry_ref:
            domain: platform
            capability: open-api
            feature: webhooks
            function: webhook-subscription
          alignment_type: supporting
          evidence_refs:
            - kb/mango-product-docs/processed/vpbx-api/index.md
```

Validation rules for future registry:

- `taxonomy_mapping.version`, `source_taxonomy`, `target_taxonomy` and
  `industry_alignment[]` are required.
- `industry_ref.domain` is required for every alignment; deeper fields are
  required by Mango level: Product may stop at Domain/Capability, Service at
  Capability, Module at Feature, Function at Function.
- `domain`, `capability`, `feature` and `function` values must resolve to
  canonical Industry Taxonomy slugs from ADR-011 or the future registry.
- `alignment_type` must be one of `primary`, `secondary`, `supporting`; every
  mapped entity must have at least one `primary` or an explicit reason why it is
  only `supporting`.
- `evidence_refs[]` must point to ADR, official site, processed KB or future
  registry evidence; free-text notes do not replace evidence refs.
- Facets such as `industry`, `segment`, `region`, `commercial_package` and
  `compliance` stay outside `industry_ref` so they cannot masquerade as
  taxonomy nodes.

## Taxonomy Alignment с ADR-011

Alignment должен быть явным, а не выводиться из названия. Для каждой связи
фиксируется `alignment_type`:

- `primary`: основной отраслевой смысл entity;
- `secondary`: значимая дополнительная связь;
- `supporting`: platform, hardware, security или operational support связь.

Пример начального crosswalk:

| Mango entity | Mango level | ADR-011 alignment | Комментарий |
| --- | --- | --- | --- |
| `mango-virtual-pbx` | Product | `voice-ucaas` / `cloud-pbx`, `sip-connectivity`, `number-management`, `ivr-voice-menu`, `call-recording` | Главный продукт бизнес-телефонии; часть модулей уходит в platform/security facets. |
| `mango-contact-center` | Product | `contact-center` / `omnichannel-contact-center`, `agent-workspace`, `outbound-calling`, `workforce-management`, `quality-management` | Покрывает CCaaS, digital channels и analytics. |
| `mango-talker` | Product | `voice-ucaas` / `unified-communications`; secondary `digital-channels` | UC-клиент с чатами, звонками, видео и статусами. |
| `mango-text-communications` | Product/Service family | `digital-channels` / `omnichannel-messaging`, `website-chat`, `sms-messaging` | Может поддерживать ВАТС, контакт-центр и CPaaS-сценарии. |
| `mango-speech-analytics` | Product/Service | `ai-automation` / `speech-analytics`; secondary `analytics` | AI/analytics cross-domain сервис. |
| `mango-robots` | Product family | `ai-automation` / `voice-bot`, `chatbot`, `process-robot` | Не должен смешиваться с human-agent contact-center modules. |
| `mango-marketing-analytics` | Product family | `analytics` / `call-tracking`, `end-to-end-analytics`, `multichannel-analytics`, `email-tracking`, `competitor-analysis` | Маркетинговая витрина, но внутренне содержит voice/resource dependencies. |
| `vpbx-api` | Internal service/module/function group | `platform` / `open-api`, `cpaas`; feature/function mappings by endpoint | API не является отдельной публичной продуктовой веткой, но поддерживает несколько products. |
| `access-control` | Internal service | `security` / `information-security` | Роли, SSO и права доступа являются cross-cutting service. |
| `sip-trunk` | Module/service | `voice-ucaas` / `sip-connectivity` | Может быть частью ВАТС и telecom resource layer. |

Commercial Layer, procurement-коды, тарифы, отраслевые решения, размер бизнеса
и региональные признаки остаются фасетами. Они не должны создавать отдельные
ветки Product, Service, Module или Function.

## Последствия

Положительные последствия:

- публичная витрина Mango Office не смешивается с внутренними сервисными
  границами;
- будущий product registry сможет трассировать каждый entity до официального
  сайта, processed KB и ADR-011;
- cross-product возможности вроде API, ролей, SSO, speech analytics и digital
  channels не дублируются в каждой продуктовой ветке;
- настройки, операции пользователя, API-команды и параметры получают явный
  leaf-level `Function`, пригодный для acceptance criteria и KB evidence;
- таксономия пригодна для RAG, анализа требований, gap analysis и future
  governance.

Отрицательные последствия:

- many-to-many mapping сложнее, чем flat list;
- потребуется governance для стабильных ID, владельцев, lifecycle-статусов,
  границ function-granularity и evidence policy;
- часть начальных полей останется `unknown`, потому что processed KB не
  является owner registry;
- публичные страницы могут меняться быстрее, чем processed KB.

Риски:

- дрейф между official layer и internal layer;
- устаревание обработанных документов относительно текущих продуктов;
- неоднозначность AI/analytics/calltracking сценариев между доменами
  `ai-automation`, `analytics`, `contact-center` и `voice-ucaas`;
- соблазн превратить отраслевые решения, тарифы или коммерческие пакеты в
  продуктовую иерархию;
- отсутствие единого источника правды по владельцам и lifecycle.

## Follow-up work

Issue #154 закрывает первый follow-up artifact: создан формальный стандарт
[`standards/mango-taxonomy-standard.md`](../mango-taxonomy-standard.md). Открыты
следующие future issues:

- `kb/mango/product-registry.md`: curated registry official products,
  services, modules and facets;
- `kb/mango/product-mapping.md`: mapping Mango entities на ADR-011 и source
  evidence;
- registry validators for required IDs, links, status values, function
  granularity, `channel` facet and alignment cardinality;
- migration checklist for concrete registry entries once processed KB evidence
  is promoted from source material to curated registry.

## Связанные документы

- ADR-011 Industry Taxonomy:
  [`standards/decisions/ADR-011-industry-taxonomy.md`](ADR-011-industry-taxonomy.md)
- Mango Taxonomy Standard:
  [`standards/mango-taxonomy-standard.md`](../mango-taxonomy-standard.md)
- Industry Taxonomy Standard:
  [`standards/industry-taxonomy-standard.md`](../industry-taxonomy-standard.md)
- Hub Mango classification:
  <https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/mango/classification.md>
- Официальный сайт Mango Office: <https://www.mango-office.ru/>
- Каталог продуктов Mango Office: <https://www.mango-office.ru/products/>
- Processed KB:
  [`kb/mango-product-docs/processed/`](../../kb/mango-product-docs/processed/)
- Issue #146 audit:
  [`docs/audit/issue-146-mango-taxonomy-validation.md`](../../docs/audit/issue-146-mango-taxonomy-validation.md)
- Product classification contract:
  [`standards/product-classification-contract.md`](../product-classification-contract.md)
