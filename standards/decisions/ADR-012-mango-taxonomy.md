---
status: proposed
version: 0.1
updated: 2026-06-20
ai-generated: true
type: adr
scope: mango-taxonomy
issue: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/142"
depends_on:
  - "standards/decisions/ADR-011-industry-taxonomy.md"
hub_research: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/mango/classification.md"
hub_research_sha: "3aa12727c9b87d5cf68301fa95d00a272408a97e"
site_sources:
  - "https://www.mango-office.ru/"
  - "https://www.mango-office.ru/products/"
related_prs:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/pull/143"
related_artifacts:
  - "standards/decisions/ADR-011-industry-taxonomy.md"
  - "standards/product-classification-contract.md"
  - "kb/mango-product-docs/processed/"
---

# ADR-012: Mango Taxonomy для корпоративной таксономии продуктов Mango Office

> **Статус:** Proposed · **Дата:** 2026-06-20 · **Issue:**
> <https://github.com/G-Ivan-A/mango_ba_prompts/issues/142> · **Depends on:**
> [`ADR-011`](ADR-011-industry-taxonomy.md)

> **Numbering note.** ADR-012 продолжает дорожку `standards/decisions/`
> вслед за ADR-011, потому что issue #142 явно требует путь
> `standards/decisions/ADR-012-mango-taxonomy.md`. Этот ADR не создаёт
> стандарт Mango Taxonomy, KB-данные, research-копию или дополнительные
> артефакты.

## Контекст

Issue #142 требует зафиксировать решение по **Mango Taxonomy**:
корпоративной таксономии продуктов Mango Office. Это не отраслевой эталон и не
финальный реестр продуктов. Таксономия должна описывать, как публичные
продуктовые названия Mango соотносятся с внутренними сервисами, модулями и
функциями, которые встречаются в обработанной базе знаний.

ADR-011 уже зафиксировал опорную Industry Taxonomy:

```text
Domain -> Capability -> Feature -> Atomic Function
```

Mango Taxonomy должна быть совместима с этой моделью, но решает другую задачу:
она нормализует продуктовый контур конкретного вендора Mango Office. Поэтому
она не заменяет ADR-011, а добавляет вендорский слой поверх него.

Жёсткие ограничения issue #142:

- создать только этот ADR;
- обновить только `CHANGELOG.md`;
- оставить статус `Proposed`;
- не создавать стандарт, KB-реестр, research-файл или дополнительные
  production-артефакты;
- использовать ADR-011, Hub classification, официальный сайт Mango Office и
  только обработанные markdown-документы в `kb/mango-product-docs/processed/`.

## Research: источники

| Источник | Что проверено | Роль в решении |
| --- | --- | --- |
| [`ADR-011`](ADR-011-industry-taxonomy.md) | Industry Taxonomy, домены, capability-уровень, cross-domain `platform` и отделение Product Layer от Commercial Layer. | Задаёт внешний слой выравнивания для Mango Taxonomy. |
| Hub classification: <https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/mango/classification.md> | Mango-ориентированная модель v3.0; свежий blob SHA `3aa12727c9b87d5cf68301fa95d00a272408a97e`. | Даёт исходную гипотезу по доменам, capability и Product/Commercial separation. |
| Официальный сайт: <https://www.mango-office.ru/> | Публичные продуктовые группы: бизнес-телефония, омниканальный контакт-центр, роботы и аналитика, маркетинговые технологии. | Показывает официальный внешний слой и маркетинговые группировки. |
| Каталог продуктов: <https://www.mango-office.ru/products/> | Публичный каталог: ВАТС, гибридная АТС, номера, контакт-центр, calltracking, оборудование, Mango Talker, API, интеграции, отраслевые/размерные решения. | Уточняет, какие названия допустимо считать official-layer сигналом. |
| `kb/mango-product-docs/processed/` | Обработанные markdown-документы по ВАТС, контакт-центру, API, интеграциям, Mango Talker, речевой аналитике, качеству, Wallboard, SIP Trunk, SSO и ролям. | Показывает внутренние сервисы, модули, операции и документационные границы. |

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

- документация подтверждает внутренние границы сервисов и модулей, но не даёт
  единого нормализованного product registry;
- публичные product names и внутренние document/module names часто не
  совпадают;
- часть возможностей является cross-product: роли, SSO, API, speech analytics,
  digital channels, отчёты и интеграции;
- коммерческие тарифы, решения по отраслям и procurement-признаки не должны
  попадать в иерархию Product -> Service -> Module.

## Рассмотренные альтернативы

| Вариант | Описание | Плюсы | Минусы |
| --- | --- | --- | --- |
| A. Flat product list | Вести один список публичных продуктов с URL и коротким описанием. | Быстро, понятно для витрины и changelog. | Не отражает внутренние модули, cross-product функции и связь с ADR-011; плохо подходит для KB/RAG и трассировки требований. |
| B. Two-layer taxonomy | Разделить Official Layer и Internal Layer, связав их many-to-many отношениями и выравниванием на ADR-011. | Сохраняет публичную семантику, объясняет внутренние границы, поддерживает трассировку и future KB registry. | Требует явного governance для ID, статусов, владельцев и source evidence. |
| C. Product -> Service -> Module без слоёв | Ввести только иерархию Product -> Service -> Module. | Даёт полезную структуру и похожа на будущий data model. | Смешивает публичные названия с внутренними границами; не объясняет, почему один модуль обслуживает несколько продуктов. |

## Решение

Принять вариант **B: Two-layer taxonomy**. Иерархия
`Product -> Service -> Module` используется внутри этой двухслойной модели, но
не заменяет разделение Official/Internal.

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
- internal aliases;
- owning area/team, если известны;
- lifecycle/status, если известен;
- links на processed KB, API docs и integration docs;
- alignment на ADR-011 Domain/Capability/Feature/Atomic Function;
- confidence/evidence level.

### Иерархия

Mango Taxonomy использует три основных уровня:

```text
Product -> Service -> Module
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

Feature и Atomic Function не вводятся как отдельные Mango-уровни, потому что
они уже принадлежат Industry Taxonomy ADR-011. Вместо этого Mango `Service`
выравнивается на `Capability`, Mango `Module` выравнивается на `Feature`, а
конкретные операции модуля, API-команды и настройки выравниваются на
`Atomic Function`.

### Отношения

Минимальный набор отношений для будущего стандарта:

| Relationship | Кардинальность | Назначение |
| --- | --- | --- |
| `official_product.internal_services[]` | many-to-many | Связать публичную витрину с внутренними сервисами. |
| `internal_service.modules[]` | one-to-many или many-to-many | Показать, какие модули реализуют сервис. |
| `module.kb_refs[]` | one-to-many | Привязать модуль к processed KB evidence. |
| `service.industry_alignment[]` | one-to-many | Связать сервис с ADR-011 Domain/Capability. |
| `module.industry_alignment[]` | one-to-many | Связать модуль с ADR-011 Feature/Atomic Function. |
| `entity.facets[]` | many-to-many | Хранить commercial, segment, industry, compliance и region overlays вне иерархии. |

### Атрибуты

Рекомендуемый атрибутный минимум:

```yaml
official_product:
  id: mango-contact-center
  layer: official
  name_ru: Омниканальный контакт-центр
  public_urls:
    - https://www.mango-office.ru/products/
  aliases: []
  official_family: contact-center
  lifecycle_status: active
  facets:
    segment: []
    industry: []
    use_case: []
  internal_services:
    - agent-workspace
    - omnichannel-queue-management
    - outbound-campaigns
  source_refs:
    - type: official_site
      url: https://www.mango-office.ru/products/

internal_service:
  id: omnichannel-queue-management
  layer: internal
  name_ru: Управление очередями обращений
  supports_official_products:
    - mango-contact-center
  industry_alignment:
    - domain: contact-center
      capability: omnichannel-contact-center
      alignment_type: primary
  kb_refs:
    - kb/mango-product-docs/processed/mango-cc-manual/index.md
  owner: unknown
  evidence_level: processed_kb

module:
  id: wallboard
  layer: internal
  parent_services:
    - contact-center-monitoring
  industry_alignment:
    - domain: analytics
      capability: product-analytics
      feature: real-time-dashboard
      alignment_type: supporting
  kb_refs:
    - kb/mango-product-docs/processed/wallboard/index.md
  api_refs: []
```

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
| `vpbx-api` | Internal service/module group | `platform` / `open-api`, `cpaas`; feature/atomic mappings by endpoint | API не является отдельной публичной продуктовой веткой, но поддерживает несколько products. |
| `access-control` | Internal service | `security` / `information-security` | Роли, SSO и права доступа являются cross-cutting service. |
| `sip-trunk` | Module/service | `voice-ucaas` / `sip-connectivity` | Может быть частью ВАТС и telecom resource layer. |

Commercial Layer, procurement-коды, тарифы, отраслевые решения, размер бизнеса
и региональные признаки остаются фасетами. Они не должны создавать отдельные
ветки Product, Service или Module.

## Последствия

Положительные последствия:

- публичная витрина Mango Office не смешивается с внутренними сервисными
  границами;
- будущий product registry сможет трассировать каждый entity до официального
  сайта, processed KB и ADR-011;
- cross-product возможности вроде API, ролей, SSO, speech analytics и digital
  channels не дублируются в каждой продуктовой ветке;
- таксономия пригодна для RAG, анализа требований, gap analysis и future
  governance.

Отрицательные последствия:

- many-to-many mapping сложнее, чем flat list;
- потребуется governance для стабильных ID, владельцев, lifecycle-статусов и
  evidence policy;
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

Этот ADR не создаёт follow-up артефакты, но задаёт направление для будущих
issues:

- `standards/mango-taxonomy-standard.md`: формальный стандарт Mango Taxonomy;
- `kb/mango/product-registry.md`: curated registry official products,
  services, modules and facets;
- `kb/mango/product-mapping.md`: mapping Mango entities на ADR-011 и source
  evidence;
- validators for required IDs, links, status values and alignment cardinality.

## Связанные документы

- ADR-011 Industry Taxonomy:
  [`standards/decisions/ADR-011-industry-taxonomy.md`](ADR-011-industry-taxonomy.md)
- Hub Mango classification:
  <https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/mango/classification.md>
- Официальный сайт Mango Office: <https://www.mango-office.ru/>
- Каталог продуктов Mango Office: <https://www.mango-office.ru/products/>
- Processed KB:
  [`kb/mango-product-docs/processed/`](../../kb/mango-product-docs/processed/)
- Product classification contract:
  [`standards/product-classification-contract.md`](../product-classification-contract.md)
