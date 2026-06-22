---
status: draft
version: 0.2
updated: 2026-06-21
ai-generated: true
type: standard
scope: mango-taxonomy
issue: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/154"
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/164"
depends_on:
  - "standards/industry-taxonomy-standard.md"
  - "standards/decisions/ADR-011-industry-taxonomy.md"
  - "standards/decisions/ADR-012-mango-taxonomy.md"
  - "kb/industry-taxonomy/reference-taxonomy.json"
related_artifacts:
  - "docs/analysis/voice-digital-channels-comparison.md"
  - "docs/audit/issue-146-mango-taxonomy-validation.md"
  - "docs/audit/taxonomy-standards-independent-review.md"
  - "kb/mango-taxonomy/official-products.yaml"
  - "kb/mango-taxonomy/internal-registry.yaml"
  - "kb/mango-taxonomy/product-mapping.yaml"
validated_by:
  - "scripts/validate_issue_154_mango_taxonomy_standard.py"
---

# Стандарт Mango Taxonomy

> Носитель архитектурного решения:
> [ADR-012 Mango Taxonomy](decisions/ADR-012-mango-taxonomy.md).
> Внешний reference layer:
> [ADR-011 Industry Taxonomy](decisions/ADR-011-industry-taxonomy.md) и
> [Industry Taxonomy Standard](industry-taxonomy-standard.md).
> Нормативный словарь: RFC 2119 / BCP 14
> (**ДОЛЖЕН**, **НЕ ДОЛЖЕН**, **СЛЕДУЕТ**, **МОЖНО**).

Этот стандарт задаёт строгий machine-readable контракт Mango Taxonomy для
будущих реестров, валидаторов CI, AI-агентов и генерации требований. ADR-012
объясняет принятое решение; этот стандарт определяет, как хранить, валидировать
и использовать Mango-specific taxonomy entities без догадок.

**Audit fix note (issue #164).** Версия 0.2 исправляет Mango-specific находки
независимого аудита
[`docs/audit/taxonomy-standards-independent-review.md`](../docs/audit/taxonomy-standards-independent-review.md).
ADR-011 имеет приоритет над ADR-012 для Industry reference layer и `industry_ref`.
Если ADR-012 или старый Mango crosswalk противоречит ADR-011, Industry Taxonomy
Standard или [`kb/industry-taxonomy/reference-taxonomy.json`](../kb/industry-taxonomy/reference-taxonomy.json),
этот стандарт применяет ADR-011/Industry registry и фиксирует расхождение как
материал для отдельной ADR-sync задачи.

**Ограничение источников.** Issue #154 ссылается на прикреплённое резюме
согласования ADR-012 как source of truth. В текущем checkout и через GitHub
issue body/comments/timeline/code search отдельный attachment URL или файл не
доступен. Нормативные решения ниже берутся из body issue #154, ADR-012,
ADR-011 canonical v1.0, Industry Taxonomy Standard, current Industry/Mango
registries, issue #146 audit, issue #164 audit и аналитики voice/digital
channels. Если attachment появится позже и будет
противоречить этому стандарту, изменение ДОЛЖНО идти отдельным PR с явным
diff of decisions.

## 1. Область применения

### 1.1 Что регулирует стандарт

Стандарт ДОЛЖЕН применяться к любому артефакту, который:

- описывает Mango Taxonomy entity;
- создаёт или проверяет future registry для Mango products/services/modules/functions;
- маппит Mango entity на Industry Taxonomy;
- читает или обновляет текущие registry files `kb/mango-taxonomy/official-products.yaml`,
  `kb/mango-taxonomy/internal-registry.yaml` and `kb/mango-taxonomy/product-mapping.yaml`;
- использует Mango taxonomy labels в requirements, KB, prompt, audit или CI;
- генерирует machine-readable YAML/JSON для AI-агентов или валидаторов.

Стандарт регулирует:

- двухслойную архитектуру Official Layer + Internal Layer;
- иерархию Internal Layer `Product -> Service -> Module -> Function`;
- восемь внутренних кластеров и правила отнесения entities к ним;
- обязательные и опциональные атрибуты для каждого уровня;
- типы Function: `business`, `configuration`, `ui-action`;
- нормализацию source terms: Component -> Module, Operation -> Function;
- формат `maps_to` и `industry_alignment`;
- JSON Schema/YAML contract для будущего реестра;
- граничные кейсы, anti-patterns, validator contract, AI-agent contract и
  процесс эволюции.

### 1.2 Что стандарт НЕ регулирует

Стандарт НЕ ДОЛЖЕН использоваться как:

- реестр конкретных продуктов, сервисов, модулей и функций Mango;
- коммерческий каталог, прайс-лист, тарифная матрица или procurement-реестр;
- замена Industry Taxonomy Standard;
- источник новых Industry Taxonomy slugs;
- место для загрузки processed KB данных;
- каталог исследований в споке.

Конкретные registry entries живут в `kb/mango-taxonomy/official-products.yaml`,
`kb/mango-taxonomy/internal-registry.yaml` and `kb/mango-taxonomy/product-mapping.yaml` или в
другом утверждённом registry path. Этот стандарт задаёт контракт, примеры и
boundary rules; он НЕ ДОЛЖЕН становиться полным продуктовым registry.

### 1.3 Приоритет источников

При конфликте применяется такой порядок:

1. явное issue/ADR/PR-review решение, помеченное as taxonomy override and
   accepted by maintainer/founder;
2. этот стандарт для Mango operational contract;
3. `kb/industry-taxonomy/reference-taxonomy.json` для canonical Industry node ids;
4. `standards/industry-taxonomy-standard.md`;
5. ADR-011 canonical v1.0;
6. `kb/mango-taxonomy/official-products.yaml`, `kb/mango-taxonomy/internal-registry.yaml` and
   `kb/mango-taxonomy/product-mapping.yaml` для конкретных Mango entries, если они
   соответствуют этому стандарту;
7. ADR-012 canonical v1.0 только для Mango-specific architecture where it does
   not conflict with ADR-011 or Industry registry;
8. `docs/analysis/voice-digital-channels-comparison.md`;
9. `docs/audit/issue-146-mango-taxonomy-validation.md` and
   `docs/audit/taxonomy-standards-independent-review.md`;
10. processed KB evidence.

ADR-011 имеет приоритет над ADR-012. Обычный issue comment не отменяет taxonomy
contract сам по себе; override ДОЛЖЕН быть явным, reviewable and accepted by
maintainer/founder. Если Mango-specific правило конфликтует с Industry Taxonomy
Standard or Industry registry, PR ДОЛЖЕН явно указать один из вариантов:
изменить Mango Taxonomy, предложить изменение Industry Taxonomy или зафиксировать
vendor-specific extension outside `industry_ref`.

### 1.4 Mango vs Industry responsibility boundary

Mango vs Industry responsibility boundary:

- Industry Taxonomy отвечает на вопрос: "какой canonical industry node описывает
  возможность?" и владеет `industry_ref` ids.
- Mango Taxonomy отвечает на вопрос: "какой Official Product, Product, Service,
  Module or Function Mango реализует эту возможность?"
- Mango Taxonomy НЕ ДОЛЖНА создавать Industry slug from Mango label. Если нужный
  deeper node отсутствует в `kb/industry-taxonomy/reference-taxonomy.json`, mapping
  ДОЛЖЕН ссылаться на nearest canonical parent and add `mapping_gap`.
- Mango cluster ids are Mango namespace only. Они НЕ ДОЛЖНЫ подменять Industry
  Domain/Capability ids, even when labels coincide, например `digital-channels`.

## 2. Нормативные термины

### 2.1 Mango Taxonomy

**Mango Taxonomy** - vendor-specific taxonomy для продуктов Mango Office. Она
связывает публичные product names и внутреннюю функциональную декомпозицию,
сохраняя строгий mapping на Industry Taxonomy.

Mango Taxonomy НЕ является Industry Taxonomy и НЕ создаёт отраслевые domains.

### 2.2 Official Layer

**Official Layer** фиксирует публичную витрину Mango Office: official product,
product family, публичный URL, aliases, lifecycle/status и source evidence.

Official Layer отвечает на вопрос: "Как Mango называет и показывает продукт
наружу?"

Official Layer ДОЛЖЕН:

- хранить публичный product id;
- иметь source refs на официальный сайт, каталог или иной approved public source;
- поддерживать aliases without changing canonical id;
- связываться с Internal Layer через many-to-many relations.

Official Layer НЕ ДОЛЖЕН:

- подменять внутренние service/module/function границы;
- создавать отдельную branch для тарифа, сегмента, vertical, региона или SLA;
- содержать leaf-level функции без Internal Layer entity.

### 2.3 Internal Layer

**Internal Layer** фиксирует функциональную и документационную структуру Mango:
Product, Service, Module, Function, evidence refs и Industry mapping.

Internal Layer отвечает на вопрос: "Какая функциональная единица реализует
возможность и как её проверить?"

Internal Layer ДОЛЖЕН использовать hierarchy:

```text
Product -> Service -> Module -> Function
```

### 2.4 Product

**Product** - Mango-specific продукт или семейство, которое связывает Official
Layer и Internal Layer. Product может быть видимым наружу или нормализованным
internal product group, если public packaging объединяет несколько сервисов.

Product ДОЛЖЕН:

- иметь `id`;
- ссылаться на one or more official products or explicit internal-only reason;
- иметь `maps_to` на Industry Taxonomy минимум до Domain;
- не содержать конкретные actions directly, если есть Service/Module/Function.

### 2.5 Service

**Service** - внутренняя capability-зона или функциональный сервис, который
поддерживает один или несколько Products.

Service ДОЛЖЕН:

- принадлежать минимум одному Product;
- иметь один primary internal cluster;
- маппиться на Industry Capability, если evidence позволяет;
- группировать Modules по устойчивой функциональной границе.

Service НЕ ДОЛЖЕН быть экраном, endpoint, single setting, тарифом или
marketing label.

### 2.6 Module

**Module** - конкретный модуль, экранная зона, API-группа, интеграционный блок,
настройка или эксплуатационный блок внутри Service.

Module ДОЛЖЕН:

- иметь parent service(s);
- маппиться на Industry Feature, если evidence позволяет;
- содержать Functions или обоснование, почему Functions ещё не выделены;
- хранить Component source terms as aliases/source_terms, not as a new level.

### 2.7 Function

**Function** - минимальная проверяемая единица поведения, настройки, API-команды,
UI-действия, параметра или бизнес-правила внутри Module.

Function ДОЛЖНА:

- иметь parent module;
- иметь ровно один `function_type`;
- иметь observable result, state change, emitted event, data retrieval,
  decision or UI interaction;
- маппиться на Industry Function or nearest canonical parent with `mapping_gap`;
- быть пригодной для acceptance criteria, test case, KB citation или requirement.

### 2.8 Internal cluster

**Internal cluster** - верхнеуровневая ось группировки Internal Layer. Cluster
не заменяет Product/Service/Module/Function hierarchy и не является Industry
Domain. Cluster нужен для ownership, navigation, validation и AI routing.

### 2.9 `maps_to`

`maps_to` - canonical relationship container для связей Mango entity с другими
слоями. В этом стандарте обязательный target - Industry Taxonomy через
`industry_alignment`. Допустимые future target types: `official_product`,
`processed_kb`, `source_document`, `owner_registry`.

`maps_to.industry_alignment[]` ДОЛЖЕН использовать typed objects, not free text.

### 2.10 `industry_ref`

`industry_ref` - строгая ссылка на Industry Taxonomy node. Она ДОЛЖНА
соответствовать `standards/industry-taxonomy-standard.md` and
`kb/industry-taxonomy/reference-taxonomy.json`. `domain` MAY reference canonical Industry
Domain or canonical `cross_domain_layer` such as `platform`, because the current
Industry registry exposes `platform` through the same `industry_ref` shape.
Every deeper field MUST resolve under its parent in the registry. If the exact
Industry node is absent, Mango mapping MUST stop at nearest canonical parent and
use `mapping_gap`.

Минимальная форма:

```yaml
maps_to:
  industry_alignment:
    - industry_ref:
        domain: contact-center
      alignment_type: primary
```

### 2.11 Evidence ref

**Evidence ref** - repo path или URL, подтверждающий existence, boundary,
status, mapping or naming decision. Free-text note НЕ заменяет evidence ref.

### 2.12 `confidence`

`confidence` - numeric confidence for one Industry alignment, from `0.0` to
`1.0`. It MAY be used together with `mapping_gap` or review notes when evidence
is incomplete. `confidence` NEVER makes an invented Industry slug canonical and
MUST NOT replace `evidence_refs`.

## 3. Архитектура таксономии

### 3.1 Двухслойная модель

Mango Taxonomy ДОЛЖНА состоять из двух слоёв:

```text
Official Layer <-> Internal Layer <-> Industry Taxonomy
```

Official Layer и Internal Layer связываются many-to-many:

- один official product может поддерживаться несколькими internal services;
- один internal service может поддерживать несколько official products;
- один module может быть reused across services;
- одна function может иметь primary business mapping и supporting platform/security mapping.

Industry Taxonomy остаётся external reference layer. Mango Taxonomy НЕ ДОЛЖНА
копировать Industry Taxonomy rules полностью; она ДОЛЖНА ссылаться на
`standards/industry-taxonomy-standard.md`.

### 3.2 Обязательные relationship types

| Relationship | Cardinality | Required on | Meaning |
| --- | --- | --- | --- |
| `official_product.supported_by_services[]` | many-to-many | Official Product | Internal services that realize public product promise. |
| `product.official_refs[]` | one-to-many | Product | Public official products/families represented by Product. |
| `product.services[]` | one-to-many | Product | Internal services inside Product. |
| `service.parent_products[]` | many-to-many | Service | Products supported by Service. |
| `service.modules[]` | one-to-many or many-to-many | Service | Modules implementing Service. |
| `module.parent_services[]` | many-to-many | Module | Services that use Module. |
| `module.functions[]` | one-to-many | Module | Leaf Functions. |
| `entity.maps_to.industry_alignment[]` | one-to-many | Product/Service/Module/Function | Strict Industry Taxonomy mapping. |
| `entity.evidence_refs[]` | one-to-many | All registry entities | Source-backed traceability. |

`supported_by_services[]` is the canonical relationship name for Official
Product -> Internal Service. ADR-012 prose and older drafts may mention
`internal_services[]`; those references are legacy wording and MUST be treated
as an ADR-sync drift unless an explicit future ADR changes this standard.

### 3.3 Architectural invariants

Mango Taxonomy artifacts ДОЛЖНЫ satisfy these invariants:

1. Official Layer never contains leaf-level Function directly.
2. Internal Layer uses canonical levels only: Product, Service, Module, Function.
3. Component is not a level; Component -> Module.
4. Operation is not a level; Operation -> Function.
5. Every registry-grade entity has stable slug id.
6. Every registry-grade entity has `lifecycle_status`.
7. Every mapping uses `maps_to.industry_alignment[]`.
8. Every `industry_ref` chain resolves in `kb/industry-taxonomy/reference-taxonomy.json`
   or stops at nearest canonical parent with `mapping_gap`.
9. Every `industry_ref` value is an Industry Taxonomy slug, not a Mango id.
10. Commercial/procurement labels stay approved facets when needed; customer
    segment stays metadata outside `industry_ref`; industry vertical and
    geography use `industry_vertical` and `geography_region`.
11. `channel` facet follows ADR-011 and Industry Taxonomy Standard.
12. Current Mango registry files under `kb/mango-taxonomy/` are concrete registry
    artifacts and SHOULD follow this contract when changed.

## 4. Internal Layer

### 4.1 Canonical hierarchy

Internal Layer hierarchy is:

```text
Product -> Service -> Module -> Function
```

Depth rules:

| Mango level | Industry mapping depth | Example source signal |
| --- | --- | --- |
| Official Product | none or supporting metadata | Public storefront/catalog item. |
| Product | Domain or Domain/Capability | Public product or product family. |
| Service | Capability | Stable internal capability-zone. |
| Module | Feature | Screen, API group, configuration block, report, dashboard or integration block. |
| Function | Function or nearest canonical parent | Action, setting, endpoint operation, event, rule or UI interaction. |

### 4.2 Восемь внутренних кластеров

Registry ДОЛЖЕН использовать один primary `cluster` for Service and Module.
`secondary_clusters[]` MAY be used only when evidence shows a Service or Module
is truly cross-product. Secondary clusters are Mango namespace metadata and MUST
NOT be serialized inside `industry_ref`.

| Cluster id | Label from issue #154 | Rule of assignment |
| --- | --- | --- |
| `vats-core` | VATS core | ВАТС, номера, сотрудники, группы, маршрутизация, IVR, SIP, запись, SMS, callback, автодозвон, базовая телефония. |
| `contact-center-core` | Contact Center core | Очереди, статусы операторов, рабочее место, исходящие кампании, supervisors, WFM/WEM/QM orchestration. |
| `digital-channels` | Digital channels | Сайт-чат, мессенджеры, email, SMS as interaction channel, обращения, Dialogi API, channel templates. |
| `mango-talker` | Mango Talker | UC client: desktop/mobile client, calls, chats, channels, contacts, statuses, video, client administration. |
| `ai-speech-quality` | AI/Speech/Quality | Speech analytics, AI summaries, quality management, scoring, checklists, categories, assistant and evaluation. |
| `analytics-marketing` | Analytics/Marketing | Calltracking, сквозная аналитика, reports, dashboards, wallboard, attribution, marketing analytics, exports. |
| `platform-integrations` | Platform integrations | Open API, webhooks, CPaaS-like surfaces, CRM/ERP integrations, API connector, SSO integration surfaces. |
| `security-access` | Security and access | Role model, access rights, SSO, LDAP, audit/security settings, recording access, permission boundaries. |

Assignment algorithm:

1. Identify observable behavior and evidence.
2. Exclude tariff, segment, region and commercial packaging.
3. Pick the cluster that owns the primary user/customer outcome.
4. If outcome is cross-cutting API/security, use `platform-integrations` or
   `security-access` as primary only when the entity itself is an integration or
   security/access function.
5. If a business function is exposed via API, keep business cluster primary and
   add platform mapping as supporting.
6. If AI assists a CC/VATS/digital function without becoming a sold AI feature,
   keep the business cluster primary and mark `facets.ai_assisted: true`.

Boundary rules from the audit:

- SMS used as bulk campaign/broadcast messaging belongs to
  `mango-text-communications` / `digital-channels` with `facets.channel` usually
  `channel_kind: text`, `synchronicity: async`, `direction: broadcast`. SMS used
  only as PBX notification or telecom infrastructure remains under `vats-core`
  or `voice-ucaas` supporting mapping.
- Mango Talker chats and presence remain under `mango-talker` primary when the
  UC client is the user-visible product. Use `digital-channels` only as
  secondary/supporting when the same behavior is a standalone digital-channel
  service.
- AI summaries attached to contact-center conversations keep the business owner
  primary, for example `contact-center/agent-assist/conversation-summaries`, and
  add `facets.ai_assisted: true` or secondary AI mapping when the AI surface is
  sold or governed separately.
- Calltracking, end-to-end analytics, marketing reports, dashboards and
  attribution belong to `analytics-marketing` primary unless the entity is only
  a telephony input signal.
- `voice-channel` is the Industry owner for actual voice interactions; SIP,
  numbering and equipment remain infrastructure/supporting mappings.

### 4.3 Product rules

Product ДОЛЖЕН aggregate Services and map public packaging to internal
capabilities. Product MUST NOT contain concrete module settings directly.

Required Product fields:

- `id`;
- `level: product`;
- `name_ru` or `name_en`;
- `official_refs[]` or `internal_only_reason`;
- `services[]`;
- `maps_to.industry_alignment[]`;
- `lifecycle_status`;
- `evidence_refs[]`.

### 4.4 Service rules

Service ДОЛЖЕН group modules around a stable capability-zone. A Service SHOULD
be reusable across products when evidence shows cross-product usage.

Required Service fields:

- `id`;
- `level: service`;
- `cluster`;
- `parent_products[]`;
- `modules[]` or `module_extraction_status`;
- `maps_to.industry_alignment[]`;
- `lifecycle_status`;
- `evidence_refs[]`.

### 4.5 Module rules

Module ДОЛЖЕН represent a concrete feature surface or configuration/integration
block. Component-like source terms normalize to Module.

Required Module fields:

- `id`;
- `level: module`;
- `cluster`;
- `secondary_clusters[]` when the module is deliberately cross-product;
- `parent_services[]`;
- `functions[]` or `function_extraction_status`;
- `maps_to.industry_alignment[]`;
- `lifecycle_status`;
- `evidence_refs[]`.

### 4.6 Function rules

Function ДОЛЖНА be atomic enough for independent validation.

A Function is atomic if:

- it has one action/condition/effect;
- it can become one acceptance criterion or test step;
- its primary result can be classified as business, configuration or UI action;
- it does not hide unrelated behavior.

Required Function fields:

- `id`;
- `level: function`;
- `function_type`;
- `interaction_surface`;
- `parent_module`;
- `maps_to.industry_alignment[]`;
- `lifecycle_status`;
- `evidence_refs[]`.

Function `cluster` is inherited from the parent Module unless an explicit
validator/reporting view computes it. Registry documents MUST NOT serialize
`cluster: inherited`; the inherited value is a computed property.

## 5. Атрибуты и типы

### 5.1 Canonical slug

Every canonical id ДОЛЖЕН match:

```text
^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$
```

Rules:

- lowercase ASCII only;
- hyphen as separator;
- no spaces, underscores, slashes or uppercase;
- stable after publication;
- unique within level and parent scope.

### 5.2 Lifecycle status

Allowed `lifecycle_status` values:

| Status | Meaning | Validator behavior |
| --- | --- | --- |
| `proposed` | Candidate entity; not production-grade. | Allowed in draft/proposed registry. |
| `active` | Canonical entity allowed for production mapping. | Accepted. |
| `deprecated` | Entity replaced or being phased out. | Warning with replacement required. |

`removed` is a legacy tombstone or migration marker, not an accepted current
registry value. Current registry schema MUST reject it unless a separate legacy
exemption artifact is introduced and explicitly named by a future migration.

### 5.3 Common attributes

All entities SHOULD use this common structure:

```yaml
id: entity-slug
level: product
name_ru: Название
name_en: Name
description: Short source-backed definition.
aliases: []
source_terms: []
lifecycle_status: proposed
owner: unknown
evidence_refs:
  - standards/decisions/ADR-012-mango-taxonomy.md
maps_to:
  industry_alignment:
    - industry_ref:
        domain: voice-ucaas
      alignment_type: primary
      confidence: 0.6
```

### 5.4 Attribute matrix

| Field | Official Product | Product | Service | Module | Function |
| --- | --- | --- | --- | --- | --- |
| `id` | required | required | required | required | required |
| `level` | `official-product` | `product` | `service` | `module` | `function` |
| `name_ru` or `name_en` | required | required | required | required | required |
| `official_urls` | required | optional | forbidden | forbidden | forbidden |
| `official_refs` | forbidden | required unless internal-only | optional | optional | optional |
| `cluster` | forbidden | optional | required | required | computed from parent module |
| `secondary_clusters` | forbidden | optional | optional | optional | forbidden |
| `parent_products` | forbidden | forbidden | required | forbidden | forbidden |
| `parent_services` | forbidden | forbidden | forbidden | required | forbidden |
| `parent_module` | forbidden | forbidden | forbidden | forbidden | required |
| `function_type` | forbidden | forbidden | forbidden | forbidden | required |
| `interaction_surface` | optional | optional | optional | optional | required |
| `maps_to.industry_alignment` | optional | required | required | required | required |
| `module_extraction_status` | forbidden | forbidden | required only when `modules[]` absent | forbidden | forbidden |
| `function_extraction_status` | forbidden | forbidden | forbidden | required only when `functions[]` absent | forbidden |
| `confidence` | mapping-only | mapping-only | mapping-only | mapping-only | mapping-only |
| `evidence_refs` | required | required | required | required | required |

### 5.5 `function_type`

Every Function ДОЛЖНА have exactly one `function_type`.

| `function_type` | When to use | Examples |
| --- | --- | --- |
| `business` | Function creates customer, operator or operational business outcome. | `transfer-call`, `send-dialog-message`, `create-outbound-campaign`, `generate-ai-summary`. |
| `configuration` | Function changes setting, policy, route, access, integration, lifecycle or service behavior. | `configure-webhook-url`, `enable-call-recording`, `set-queue-schedule`, `assign-agent-role`. |
| `ui-action` | Function describes a user interaction in UI that is required for scenario but is not standalone business/configuration capability. | `select-wallboard-widget`, `open-call-filter`, `switch-agent-tab`, `expand-report-section`. |

Rules:

- `function_type` classifies semantic result, not channel or surface.
- API endpoint can be `business`, `configuration` or `ui-action` depending on effect.
- UI action with configuration effect is `configuration`, not `ui-action`.
- UI action without standalone effect is `ui-action`.
- Channel marker belongs to `facets.channel`, not `function_type`.

### 5.6 `interaction_surface`

Allowed initial values:

| Value | Meaning |
| --- | --- |
| `admin-ui` | Administrator UI or settings panel. |
| `operator-ui` | Operator/agent/supervisor workspace. |
| `end-user-ui` | End-user client or user-facing application. |
| `api` | Public or integration API. |
| `webhook` | Event callback or webhook surface. |
| `background-job` | Scheduled or asynchronous internal process. |
| `system-rule` | Rule applied by platform/runtime. |
| `unknown` | Evidence is insufficient; requires review before active status. |

`interaction_surface: unknown` MAY be used only while an entity is `proposed`.
An `active` Function MUST have a concrete interaction surface.

### 5.7 Facets

Mango alignment facets MUST follow the canonical Industry facet names:

- `channel`;
- `ai_assisted`;
- `security_compliance`;
- `commercial`;
- `procurement`;
- `industry_vertical`;
- `geography_region`.

`segment` and `region` MUST NOT appear inside
`maps_to.industry_alignment[].facets`; use `commercial` or source metadata for
customer segment and `geography_region` for geography. Direction x
synchronicity MUST follow the Industry table: `inbound`, `outbound` and
`broadcast` MAY be `sync` or `async`, but SMS/push/email broadcast SHOULD be
`async` unless evidence justifies otherwise.

## 6. Нормализация терминов

### 6.1 Canonical levels

Mango Taxonomy has only these canonical levels:

```text
Official Product
Product
Service
Module
Function
```

Source terms do not create levels.

### 6.2 Component -> Module

`Component -> Module` is mandatory.

If processed KB, vendor docs or code comments use "Component", registry ДОЛЖЕН:

- store canonical `level: module`;
- preserve source term in `source_terms`;
- optionally add alias in `aliases`;
- avoid creating `component` in hierarchy, schema or mapping.

Example:

```yaml
id: webhook-management
level: module
source_terms:
  - Component
aliases:
  - webhook-component
```

### 6.3 Operation -> Function

`Operation -> Function` is mandatory.

API operation, user operation, operational step, action, command, endpoint,
parameter change or rule ДОЛЖЕН become Function if it is leaf-level and
verifiable.

Example:

```yaml
id: configure-webhook-url
level: function
function_type: configuration
source_terms:
  - Operation
  - endpoint
```

### 6.4 Aliases and ambiguity

Alias rules:

- one alias SHOULD resolve to one canonical entity;
- ambiguous alias ДОЛЖЕН require explicit parent context;
- aliases НЕ ДОЛЖНЫ appear inside `industry_ref`;
- source terms MAY be multilingual;
- canonical id remains ASCII slug.

## 7. Mapping на Industry Taxonomy

### 7.1 Required mapping container

Every Product, Service, Module and Function ДОЛЖЕН use:

```yaml
maps_to:
  industry_alignment:
    - industry_ref:
        domain: contact-center
        capability: omnichannel-contact-center
      alignment_type: primary
      evidence_refs:
        - standards/decisions/ADR-011-industry-taxonomy.md
```

`maps_to` MAY contain other relation families later, but
`maps_to.industry_alignment[]` is the normative form for Industry mapping.

### 7.2 `alignment_type`

Allowed values:

- `primary` - main industry meaning;
- `secondary` - significant additional meaning;
- `supporting` - platform, hardware, security, integration or operational support.

Rules:

- every mapped entity MUST have at least one `primary`, unless
  `supporting_only_reason` is present;
- `primary` is selected by customer/operational meaning, not technical surface;
- `supporting` must not hide the primary business meaning;
- many-to-many is expected and valid.

### 7.3 Depth by Mango level

| Mango level | Minimum industry_ref | Recommended industry_ref |
| --- | --- | --- |
| Official Product | none or supporting metadata | no direct Industry mapping unless needed |
| Product | `domain` | `domain` + `capability` |
| Service | `domain` + `capability` | `domain` + `capability` |
| Module | `domain` + `capability` + `feature` | `domain` + `capability` + `feature` |
| Function | nearest canonical parent | `domain` + `capability` + `feature` + `function` |

If a deeper Industry node is not canonical, mapping ДОЛЖЕН stop at nearest
canonical parent and add `mapping_gap`.

### 7.4 Mapping examples

Virtual PBX product:

```yaml
id: mango-virtual-pbx
level: product
maps_to:
  industry_alignment:
    - industry_ref:
        domain: voice-ucaas
        capability: cloud-pbx
      alignment_type: primary
      evidence_refs:
        - standards/decisions/ADR-012-mango-taxonomy.md
    - industry_ref:
        domain: voice-ucaas
        capability: sip-connectivity
      alignment_type: secondary
      evidence_refs:
        - standards/decisions/ADR-011-industry-taxonomy.md
```

Inbound voice interaction:

```yaml
id: accept-inbound-voice-call
level: function
function_type: business
maps_to:
  industry_alignment:
    - industry_ref:
        domain: voice-ucaas
        capability: voice-channel
        feature: inbound-voice-call
        function: accept-inbound-voice-call
      alignment_type: primary
      facets:
        channel:
          channel_kind: voice
          synchronicity: sync
          direction: inbound
```

SIP trunk as infrastructure:

```yaml
id: sip-trunk
level: module
maps_to:
  industry_alignment:
    - industry_ref:
        domain: voice-ucaas
        capability: sip-connectivity
      alignment_type: supporting
      supporting_only_reason: "Pure telecom infrastructure, not an interaction channel."
```

Contact center product:

```yaml
id: mango-contact-center
level: product
maps_to:
  industry_alignment:
    - industry_ref:
        domain: contact-center
        capability: omnichannel-contact-center
      alignment_type: primary
    - industry_ref:
        domain: digital-channels
        capability: omnichannel-messaging
      alignment_type: secondary
```

Outbound campaign function:

```yaml
id: start-outbound-campaign
level: function
function_type: business
maps_to:
  industry_alignment:
    - industry_ref:
        domain: contact-center
        capability: outbound-calling
        feature: campaign-management
        function: campaign-configuration
      alignment_type: primary
      facets:
        channel:
          channel_kind: voice
          synchronicity: sync
          direction: outbound
```

Text dialog channel:

```yaml
id: send-dialog-message
level: function
function_type: business
maps_to:
  industry_alignment:
    - industry_ref:
        domain: digital-channels
        capability: omnichannel-messaging
        feature: messenger-integration
        function: channel-ingestion
      alignment_type: primary
      facets:
        channel:
          channel_kind: text
          synchronicity: async
          direction: outbound
```

Mango Talker mixed UC client:

```yaml
id: mango-talker
level: product
maps_to:
  industry_alignment:
    - industry_ref:
        domain: voice-ucaas
        capability: unified-communications
        feature: softphone
        function: softphone-call
      alignment_type: primary
    - industry_ref:
        domain: voice-ucaas
        capability: unified-communications
        feature: corporate-messaging
        function: corporate-chat
      alignment_type: secondary
```

AI summary for contact center:

```yaml
id: generate-ai-summary
level: function
function_type: business
maps_to:
  industry_alignment:
    - industry_ref:
        domain: contact-center
        capability: agent-assist
        feature: conversation-summaries
        function: manage-conversation-summaries
      alignment_type: primary
      facets:
        ai_assisted: true
    - industry_ref:
        domain: ai-automation
        capability: speech-analytics
        feature: transcription
        function: call-transcription
      alignment_type: secondary
```

Wallboard:

```yaml
id: select-wallboard-widget
level: function
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
```

Open API endpoint supporting business function:

```yaml
id: create-callback-request
level: function
function_type: business
interaction_surface: api
maps_to:
  industry_alignment:
    - industry_ref:
        domain: voice-ucaas
        capability: callback
        feature: web-callback-widget
        function: callback-request-intake
      alignment_type: primary
    - industry_ref:
        domain: platform
        capability: open-api
        feature: rest-api
        function: api-rate-limiting
      alignment_type: supporting
```

Access control:

```yaml
id: assign-agent-role
level: function
function_type: configuration
maps_to:
  industry_alignment:
    - industry_ref:
        domain: security
        capability: information-security
        feature: access-control
        function: role-based-access-control
      alignment_type: primary
```

Mango Robots:

```yaml
id: mango-robots
level: product
maps_to:
  industry_alignment:
    - industry_ref:
        domain: ai-automation
        capability: process-robot
        feature: process-automation
        function: automated-action-execution
      alignment_type: primary
```

Mango Speech Analytics:

```yaml
id: mango-speech-analytics
level: product
maps_to:
  industry_alignment:
    - industry_ref:
        domain: ai-automation
        capability: speech-analytics
        feature: transcription
        function: call-transcription
      alignment_type: primary
```

Mango Marketing Analytics:

```yaml
id: mango-marketing-analytics
level: product
maps_to:
  industry_alignment:
    - industry_ref:
        domain: analytics
        capability: call-tracking
        feature: call-analytics
        function: call-analytics-reporting
      alignment_type: primary
```

Mango Text Communications:

```yaml
id: mango-text-communications
level: product
maps_to:
  industry_alignment:
    - industry_ref:
        domain: digital-channels
        capability: sms-messaging
        feature: bulk-sms
        function: bulk-sms-dispatch
      alignment_type: primary
      facets:
        channel:
          channel_kind: text
          synchronicity: async
          direction: broadcast
```

Mango Open Platform:

```yaml
id: mango-open-platform
level: product
maps_to:
  industry_alignment:
    - industry_ref:
        domain: platform
        capability: open-api
        feature: webhooks
        function: webhook-subscription
      alignment_type: primary
```

Mango Numbers and Equipment:

```yaml
id: mango-numbers-equipment
level: product
maps_to:
  industry_alignment:
    - industry_ref:
        domain: voice-ucaas
        capability: number-management
      alignment_type: primary
    - industry_ref:
        domain: voice-ucaas
        capability: cloud-pbx
      alignment_type: supporting
```

Mango Solution Pack:

```yaml
id: mango-solution-pack
level: official-product
official_urls:
  - https://www.mango-office.ru/products/
evidence_refs:
  - standards/decisions/ADR-012-mango-taxonomy.md
```

### 7.5 Mapping gaps

When Industry Function slug is absent:

```yaml
maps_to:
  industry_alignment:
    - industry_ref:
        domain: contact-center
        capability: call-routing
        feature: queue-management
      alignment_type: primary
      mapping_gap:
        missing_level: function
        proposed_id: configure-routing-condition
        reason: "Mango Function exists; Industry Function is not canonical yet."
```

`mapping_gap.proposed_id` ДОЛЖЕН match slug pattern and MUST NOT silently become
canonical.

## 8. Машиночитаемые схемы

This section defines the minimum JSON Schema contract. Future registry MAY split
schemas into files, but MUST preserve these required fields and enum values.

### 8.1 MangoTaxonomyDocument

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://github.com/G-Ivan-A/mango_ba_prompts/schemas/mango-taxonomy-document.schema.json",
  "title": "MangoTaxonomyDocument",
  "type": "object",
  "required": ["taxonomy"],
  "additionalProperties": false,
  "properties": {
    "taxonomy": { "$ref": "#/$defs/taxonomy" }
  },
  "$defs": {
    "slug": {
      "type": "string",
      "pattern": "^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$"
    },
    "lifecycleStatus": {
      "type": "string",
      "enum": ["proposed", "active", "deprecated"]
    },
    "cluster": {
      "type": "string",
      "enum": [
        "vats-core",
        "contact-center-core",
        "digital-channels",
        "mango-talker",
        "ai-speech-quality",
        "analytics-marketing",
        "platform-integrations",
        "security-access"
      ]
    },
    "functionType": {
      "type": "string",
      "enum": ["business", "configuration", "ui-action"]
    },
    "interactionSurface": {
      "type": "string",
      "enum": [
        "admin-ui",
        "operator-ui",
        "end-user-ui",
        "api",
        "webhook",
        "background-job",
        "system-rule",
        "unknown"
      ]
    },
    "evidenceRef": {
      "type": "string",
      "minLength": 1
    },
    "industryRef": {
      "type": "object",
      "required": ["domain"],
      "additionalProperties": false,
      "properties": {
        "domain": { "$ref": "#/$defs/slug" },
        "capability": { "$ref": "#/$defs/slug" },
        "feature": { "$ref": "#/$defs/slug" },
        "function": { "$ref": "#/$defs/slug" }
      }
    },
    "channelFacet": {
      "type": "object",
      "required": ["channel_kind", "synchronicity", "direction"],
      "additionalProperties": false,
      "properties": {
        "channel_kind": { "type": "string", "enum": ["voice", "text", "video"] },
        "synchronicity": { "type": "string", "enum": ["sync", "async"] },
        "direction": { "type": "string", "enum": ["inbound", "outbound", "broadcast"] }
      }
    },
    "facets": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "channel": { "$ref": "#/$defs/channelFacet" },
        "ai_assisted": { "type": "boolean" },
        "security_compliance": {
          "type": "object",
          "additionalProperties": {
            "type": ["string", "number", "boolean", "array", "object"]
          }
        },
        "commercial": {
          "type": "object",
          "additionalProperties": {
            "type": ["string", "number", "boolean", "array", "object"]
          }
        },
        "procurement": {
          "type": "object",
          "additionalProperties": {
            "type": ["string", "number", "boolean", "array", "object"]
          }
        },
        "industry_vertical": { "type": "array", "items": { "$ref": "#/$defs/slug" } },
        "geography_region": { "type": "array", "items": { "$ref": "#/$defs/slug" } }
      }
    },
    "mappingGap": {
      "type": "object",
      "required": ["missing_level", "proposed_id", "reason"],
      "additionalProperties": false,
      "properties": {
        "missing_level": {
          "type": "string",
          "enum": ["domain", "capability", "feature", "function"]
        },
        "proposed_id": { "$ref": "#/$defs/slug" },
        "reason": { "type": "string", "minLength": 1 }
      }
    },
    "industryAlignment": {
      "type": "object",
      "required": ["industry_ref", "alignment_type"],
      "additionalProperties": false,
      "properties": {
        "industry_ref": { "$ref": "#/$defs/industryRef" },
        "alignment_type": {
          "type": "string",
          "enum": ["primary", "secondary", "supporting"]
        },
        "evidence_refs": {
          "type": "array",
          "items": { "$ref": "#/$defs/evidenceRef" },
          "minItems": 1
        },
        "facets": { "$ref": "#/$defs/facets" },
        "mapping_gap": { "$ref": "#/$defs/mappingGap" },
        "supporting_only_reason": { "type": "string" },
        "confidence": { "type": "number", "minimum": 0, "maximum": 1 }
      }
    },
    "mapsTo": {
      "type": "object",
      "required": ["industry_alignment"],
      "additionalProperties": false,
      "properties": {
        "industry_alignment": {
          "type": "array",
          "items": { "$ref": "#/$defs/industryAlignment" },
          "minItems": 1
        }
      }
    },
    "commonEntity": {
      "type": "object",
      "required": ["id", "level", "lifecycle_status", "evidence_refs"],
      "anyOf": [
        { "required": ["name_ru"] },
        { "required": ["name_en"] }
      ],
      "properties": {
        "id": { "$ref": "#/$defs/slug" },
        "level": { "type": "string" },
        "name_ru": { "type": "string", "minLength": 1 },
        "name_en": { "type": "string" },
        "description": { "type": "string" },
        "aliases": { "type": "array", "items": { "type": "string" } },
        "source_terms": { "type": "array", "items": { "type": "string" } },
        "lifecycle_status": { "$ref": "#/$defs/lifecycleStatus" },
        "owner": { "type": "string" },
        "evidence_refs": {
          "type": "array",
          "items": { "$ref": "#/$defs/evidenceRef" },
          "minItems": 1
        },
        "maps_to": { "$ref": "#/$defs/mapsTo" }
      }
    },
    "officialProduct": {
      "unevaluatedProperties": false,
      "allOf": [
        { "$ref": "#/$defs/commonEntity" },
        {
          "type": "object",
          "required": ["official_urls", "supported_by_services"],
          "properties": {
            "level": { "const": "official-product" },
            "official_urls": {
              "type": "array",
              "items": { "type": "string", "format": "uri" },
              "minItems": 1
            },
            "supported_by_services": {
              "type": "array",
              "items": { "$ref": "#/$defs/slug" },
              "minItems": 1
            }
          }
        }
      ]
    },
    "product": {
      "unevaluatedProperties": false,
      "allOf": [
        { "$ref": "#/$defs/commonEntity" },
        {
          "type": "object",
          "required": ["services", "maps_to"],
          "anyOf": [
            { "required": ["official_refs"] },
            { "required": ["internal_only_reason"] }
          ],
          "properties": {
            "level": { "const": "product" },
            "official_refs": {
              "type": "array",
              "items": { "$ref": "#/$defs/slug" }
            },
            "internal_only_reason": { "type": "string", "minLength": 1 },
            "services": {
              "type": "array",
              "items": { "$ref": "#/$defs/slug" },
              "minItems": 1
            },
            "secondary_clusters": {
              "type": "array",
              "items": { "$ref": "#/$defs/cluster" },
              "uniqueItems": true
            }
          }
        }
      ]
    },
    "service": {
      "unevaluatedProperties": false,
      "allOf": [
        { "$ref": "#/$defs/commonEntity" },
        {
          "type": "object",
          "required": ["cluster", "parent_products", "maps_to"],
          "anyOf": [
            { "required": ["modules"] },
            { "required": ["module_extraction_status"] }
          ],
          "properties": {
            "level": { "const": "service" },
            "cluster": { "$ref": "#/$defs/cluster" },
            "parent_products": {
              "type": "array",
              "items": { "$ref": "#/$defs/slug" },
              "minItems": 1
            },
            "modules": {
              "type": "array",
              "items": { "$ref": "#/$defs/slug" },
              "minItems": 1
            },
            "module_extraction_status": {
              "type": "string",
              "enum": ["complete", "partial", "not-started"]
            },
            "secondary_clusters": {
              "type": "array",
              "items": { "$ref": "#/$defs/cluster" },
              "uniqueItems": true
            }
          }
        }
      ]
    },
    "module": {
      "unevaluatedProperties": false,
      "allOf": [
        { "$ref": "#/$defs/commonEntity" },
        {
          "type": "object",
          "required": ["cluster", "parent_services", "maps_to"],
          "anyOf": [
            { "required": ["functions"] },
            { "required": ["function_extraction_status"] }
          ],
          "properties": {
            "level": { "const": "module" },
            "cluster": { "$ref": "#/$defs/cluster" },
            "parent_services": {
              "type": "array",
              "items": { "$ref": "#/$defs/slug" },
              "minItems": 1
            },
            "functions": {
              "type": "array",
              "items": { "$ref": "#/$defs/slug" },
              "minItems": 1
            },
            "function_extraction_status": {
              "type": "string",
              "enum": ["complete", "partial", "not-started"]
            },
            "secondary_clusters": {
              "type": "array",
              "items": { "$ref": "#/$defs/cluster" },
              "uniqueItems": true
            }
          }
        }
      ]
    },
    "function": {
      "unevaluatedProperties": false,
      "allOf": [
        { "$ref": "#/$defs/commonEntity" },
        {
          "type": "object",
          "required": ["parent_module", "function_type", "interaction_surface", "maps_to"],
          "not": {
            "required": ["lifecycle_status", "interaction_surface"],
            "properties": {
              "lifecycle_status": { "const": "active" },
              "interaction_surface": { "const": "unknown" }
            }
          },
          "properties": {
            "level": { "const": "function" },
            "parent_module": { "$ref": "#/$defs/slug" },
            "function_type": { "$ref": "#/$defs/functionType" },
            "interaction_surface": { "$ref": "#/$defs/interactionSurface" }
          }
        }
      ]
    },
    "taxonomy": {
      "type": "object",
      "required": [
        "version",
        "official_products",
        "products",
        "internal_services",
        "modules",
        "functions"
      ],
      "additionalProperties": false,
      "properties": {
        "version": {
          "type": "string",
          "pattern": "^[0-9]+\\.[0-9]+\\.[0-9]+$"
        },
        "official_products": {
          "type": "array",
          "items": { "$ref": "#/$defs/officialProduct" }
        },
        "products": {
          "type": "array",
          "items": { "$ref": "#/$defs/product" }
        },
        "internal_services": {
          "type": "array",
          "items": { "$ref": "#/$defs/service" }
        },
        "modules": {
          "type": "array",
          "items": { "$ref": "#/$defs/module" }
        },
        "functions": {
          "type": "array",
          "items": { "$ref": "#/$defs/function" }
        }
      }
    }
  }
}
```

### 8.2 Schema validation rules beyond JSON Schema

Validator ДОЛЖЕН additionally check:

- referenced ids exist in the same taxonomy document or approved registry;
- no entity references itself as parent;
- each Service has exactly one primary `cluster`;
- each Service has `modules[]` or `module_extraction_status`;
- each Module has `functions[]` or `function_extraction_status`;
- every non-supporting-only entity has at least one `primary` alignment;
- `industry_ref` parent chain resolves in Industry Taxonomy registry when such
  registry exists;
- `facets` uses canonical Industry facet names and rejects unknown facet keys;
- `facets.channel` is absent for pure SIP/PSTN/numbering infrastructure mapping;
- `facets.channel.direction` follows the Industry direction x synchronicity table;
- `active` Functions do not use `interaction_surface: unknown`;
- `function_type` exists on every Function and only on Function;
- no source term creates extra level.

## 9. YAML contract

### 9.1 Minimal registry document

```yaml
taxonomy:
  version: "1.0.0"
  official_products:
    - id: mango-contact-center-official
      level: official-product
      name_ru: Омниканальный контакт-центр
      official_urls:
        - https://www.mango-office.ru/products/
      lifecycle_status: proposed
      evidence_refs:
        - standards/decisions/ADR-012-mango-taxonomy.md
      supported_by_services:
        - outbound-campaigns
  products:
    - id: mango-contact-center
      level: product
      name_ru: Контакт-центр Mango
      official_refs:
        - mango-contact-center-official
      services:
        - outbound-campaigns
      lifecycle_status: proposed
      evidence_refs:
        - standards/decisions/ADR-012-mango-taxonomy.md
      maps_to:
        industry_alignment:
          - industry_ref:
              domain: contact-center
              capability: omnichannel-contact-center
            alignment_type: primary
  internal_services:
    - id: outbound-campaigns
      level: service
      name_ru: Исходящие кампании
      cluster: contact-center-core
      parent_products:
        - mango-contact-center
      modules:
        - campaign-management
      lifecycle_status: proposed
      evidence_refs:
        - kb/mango-product-docs/processed/mango-cc-manual/index.md
      maps_to:
        industry_alignment:
          - industry_ref:
              domain: contact-center
              capability: outbound-calling
            alignment_type: primary
  modules:
    - id: campaign-management
      level: module
      name_ru: Управление кампаниями
      cluster: contact-center-core
      parent_services:
        - outbound-campaigns
      functions:
        - start-outbound-campaign
      lifecycle_status: proposed
      evidence_refs:
        - kb/mango-product-docs/processed/mango-cc-manual/index.md
      maps_to:
        industry_alignment:
          - industry_ref:
              domain: contact-center
              capability: outbound-calling
              feature: campaign-management
            alignment_type: primary
  functions:
    - id: start-outbound-campaign
      level: function
      name_ru: Запустить исходящую кампанию
      parent_module: campaign-management
      function_type: business
      interaction_surface: operator-ui
      lifecycle_status: proposed
      evidence_refs:
        - kb/mango-product-docs/processed/mango-cc-manual/index.md
      maps_to:
        industry_alignment:
          - industry_ref:
              domain: contact-center
              capability: outbound-calling
              feature: campaign-management
              function: campaign-configuration
            alignment_type: primary
            facets:
              channel:
                channel_kind: voice
                synchronicity: sync
                direction: outbound
```

### 9.2 Serialization rules

YAML/JSON documents ДОЛЖНЫ:

- preserve field names exactly as defined;
- use arrays for all multi-value relationships;
- use `null` only when schema explicitly allows it; otherwise omit unknown optional fields;
- use `unknown` enum value only for `owner` or `interaction_surface`, not for taxonomy ids;
- keep evidence refs close to the entity or mapping they justify;
- be deterministic enough for diff review: stable ordering by level, then id.

## 10. Граничные кейсы и анти-паттерны

### 10.1 Public product vs internal service

Incorrect:

```yaml
id: omnichannel-contact-center
level: service
official_urls:
  - https://www.mango-office.ru/products/
```

Reason: official URL belongs to Official Layer or Product, not Service.

Correct: create official product, Product and internal Service separately.

### 10.2 API endpoint primary mapping

Incorrect:

```yaml
id: campaign-configuration-endpoint
level: function
maps_to:
  industry_alignment:
    - industry_ref:
        domain: platform
        capability: open-api
      alignment_type: primary
```

for an endpoint whose business effect is starting a contact-center campaign.

Correct: business mapping primary, `platform/open-api` supporting.

### 10.3 Pure infrastructure with channel facet

Incorrect:

```yaml
industry_ref:
  domain: voice-ucaas
  capability: sip-connectivity
alignment_type: primary
facets:
  channel:
    channel_kind: voice
    synchronicity: sync
    direction: inbound
```

Correct:

```yaml
industry_ref:
  domain: voice-ucaas
  capability: sip-connectivity
alignment_type: supporting
```

Use `voice-channel` only for interaction.

### 10.4 AI feature in wrong domain

Incorrect: move any AI-assisted routing into `ai-automation`.

Correct: keep routing under contact-center primary and add `facets.ai_assisted:
true`, unless the product is sold/described primarily as AI/bot/automation.

### 10.5 Commercial and segment labels

Tariff, package, SKU, "small business", region and vertical labels MUST NOT
become Product/Service/Module/Function. Store customer segment as metadata
outside `industry_ref`; use approved facets such as `commercial`,
`procurement`, `industry_vertical` and `geography_region` when needed.

### 10.6 Component/Operation as levels

Incorrect levels:

```yaml
level: component
level: operation
```

Correct:

```yaml
level: module
source_terms: ["Component"]
```

```yaml
level: function
source_terms: ["Operation"]
```

### 10.7 Duplicate modules per product

Do not copy a cross-product module into every product branch. Create one Module
and connect it to multiple parent services/products through relationships.

### 10.8 Unknown Industry slug

Do not invent Industry slugs inside `industry_ref`. Use nearest canonical parent
and `mapping_gap`.

## 11. Контракт валидатора

### 11.1 Document-level checks

Validator ДОЛЖЕН verify:

- `standards/mango-taxonomy-standard.md` exists;
- ADR-012 is `status: canonical`, `version: 1.0`;
- frontmatter fields exist: `status`, `version`, `updated`, `type`, `scope`,
  `issue`, `depends_on`, `validated_by`;
- sections 1-14 and `## Источники` exist in order;
- all eight cluster ids are present;
- hierarchy `Product -> Service -> Module -> Function` is present;
- Official Layer and Internal Layer are both defined;
- `function_type` enum has `business`, `configuration`, `ui-action`;
- term normalization includes Component -> Module and Operation -> Function;
- mapping section uses `maps_to`, `industry_ref`, `alignment_type`;
- JSON Schema includes `$schema`, `MangoTaxonomyDocument`, slug pattern and enums;
- YAML contract includes arrays for official_products, internal_services,
  modules and functions;
- issue #164 audit-regression checks verify stale Industry examples, facets,
  lifecycle and schema contracts in this standard;
- no `research` directory is created in the spoke.

Current CI coverage is intentionally narrow:
`scripts/validate_issue_154_mango_taxonomy_standard.py` validates this standard
and selected issue #164 audit-regression tokens;
`scripts/validate_issue_160_mango_registry.py` validates current `kb/mango-taxonomy/*`
registry files. A generic validator that checks every future Mango mapping file
against `kb/industry-taxonomy/reference-taxonomy.json` is not yet implemented.

### 11.2 Registry-level checks

Future registry validator ДОЛЖЕН verify:

1. YAML/JSON parses.
2. Root object has `taxonomy.version`.
3. Entity ids match slug pattern.
4. Entity ids are unique inside level and parent scope.
5. Required fields by level are present.
6. Level values are allowed.
7. Parent ids resolve.
8. No cycles exist.
9. Cluster values are one of eight canonical ids.
10. `function_type` exists on Function only.
11. `function_type` value is allowed.
12. `interaction_surface` value is allowed.
13. `maps_to.industry_alignment` is array.
14. Each alignment has `industry_ref.domain`.
15. No deeper `industry_ref` field appears without parent field.
16. `alignment_type` is one of `primary`, `secondary`, `supporting`.
17. Non-supporting-only entity has at least one `primary`.
18. `evidence_refs` resolve to existing repo path or full URL.
19. `facets.channel` uses allowed `channel_kind`, `synchronicity`, `direction`.
20. Pure infrastructure mapping does not carry channel facet.
21. `facets.channel.direction` follows the direction x synchronicity table.
22. `facets` uses canonical Industry facet names.
23. `confidence` is between `0.0` and `1.0`.
24. Service has `modules[]` or `module_extraction_status`.
25. Module has `functions[]` or `function_extraction_status`.
26. Alias/source_terms do not create extra hierarchy levels.
27. `Component` source term appears only with `level: module`.
28. `Operation` source term appears only with `level: function`.
29. Deprecated entity has replacement or deprecation reason.
30. Legacy tombstone entity fails unless explicit legacy exemption exists.

### 11.3 Severity

| Condition | Severity |
| --- | --- |
| Missing required field | error |
| Invalid enum | error |
| Invalid slug | error |
| Unknown parent id | error |
| Invalid `industry_ref` chain | error |
| Missing primary alignment | error |
| Missing evidence in active registry | error |
| Missing evidence in draft registry | error |
| Ambiguous alias | error |
| Deprecated reference | warning |
| Legacy tombstone reference | error |
| Attachment source unavailable but documented | warning |

## 12. Контракт AI-агента

AI-агент, который создаёт или изменяет Mango Taxonomy, ДОЛЖЕН:

1. Прочитать issue, latest comments, ADR-012, ADR-011, Industry Taxonomy
   Standard, this standard and relevant audit/analysis docs.
2. Treat Official Layer and Internal Layer separately.
3. Find existing entity before proposing a new id.
4. Use canonical levels only.
5. Normalize Component -> Module and Operation -> Function.
6. Select one primary internal cluster with evidence.
7. Use `maps_to.industry_alignment[]`, not free tags.
8. Add `alignment_type`, evidence refs and facets.
9. Mark uncertainty with `mapping_gap`, `confidence` in `[0.0, 1.0]` or open
   question.
10. Avoid concrete registry data unless the task explicitly asks for registry.
11. Avoid commercial/procurement/vertical labels as hierarchy nodes.
12. Run available validators before finalizing PR.

AI-агент НЕ ДОЛЖЕН:

- invent Industry Taxonomy slugs;
- turn public product names into internal services without evidence;
- duplicate cross-product modules per product;
- promote `active` status without reviewable evidence;
- use UI label alone as proof of Product/Service boundary;
- remove existing semantics without migration note.

### 12.1 Decision checklist

Before adding entity or mapping, answer:

- What source entity is classified?
- Is it Official Layer, Product, Service, Module or Function?
- What evidence proves it?
- Which internal cluster owns primary meaning?
- What is the parent chain?
- What is the nearest Industry Taxonomy node?
- Why is `alignment_type` primary/secondary/supporting?
- Does it need `channel` or `ai_assisted` facet?
- If Function, what is `function_type` and `interaction_surface`?
- Are there aliases/source terms that must be normalized?
- Is uncertainty represented as `mapping_gap` or review question?

## 13. Процесс эволюции

### 13.1 Adding entity

New entity MAY be proposed when:

- source evidence exists;
- existing entity does not cover semantic meaning;
- parent chain is clear;
- id matches slug pattern;
- cluster assignment is justified;
- Industry mapping or mapping gap exists.

### 13.2 Rejecting entity

New entity MUST NOT be added when it is only:

- tariff, package, SKU or contract condition;
- customer segment, vertical or region;
- alias of existing entity;
- implementation detail without taxonomy semantics;
- one-off UI label without stable behavior;
- source term that normalizes to existing level.

### 13.3 Change request contract

PR changing Mango Taxonomy standard or future registry ДОЛЖЕН include:

- problem statement;
- affected entities and mappings;
- evidence refs;
- before/after YAML snippets;
- validator impact;
- migration/deprecation note if ids change;
- self-check against sections 1-14;
- risks and human-review focus.

### 13.4 Versioning

Version meaning:

- patch: editorial clarification, no schema or validator change;
- minor: additive field, enum value, cluster clarification or compatible rule;
- major: breaking hierarchy, required field, id or enum change.

Registry `taxonomy.version` MUST be a SemVer string such as `"1.0.0"`.
Canonical ids MUST NOT be renamed without deprecation period and replacement.

## 14. Самопроверка качества

### 14.1 Полнота

Стандарт covers all issue #154 mandatory elements:

- two-layer architecture Official Layer + Internal Layer;
- Internal Layer hierarchy Product, Service, Module, Function;
- eight internal clusters;
- attributes for each level;
- Function types business/configuration/ui-action;
- normalization Component -> Module and Operation -> Function;
- mapping to Industry Taxonomy with primary/secondary/supporting;
- inherited ADR-011 `voice-channel` and `channel` facet;
- inherited Industry canonical facets including `security_compliance` and
  `geography_region`;
- machine-readable JSON Schema and YAML contract;
- validator and AI-agent contracts;
- evolution process.

### 14.2 Однозначность

Closed enums are defined for:

- cluster;
- lifecycle_status;
- function_type;
- interaction_surface;
- alignment_type;
- channel_kind, synchronicity, direction.

Each level has definition, positive rules, negative rules and required fields.

### 14.3 Отсутствие дублирования

The standard references Industry Taxonomy Standard for Industry rules and does
not restate all Industry node semantics. Mango-specific content is limited to
layers, internal hierarchy, clusters, source-term normalization and registry
contract. Imported Industry constructs remain references to ADR-011, Industry
Taxonomy Standard and `kb/industry-taxonomy/reference-taxonomy.json`; Mango cluster ids
and product ids are not treated as Industry ids.

### 14.4 Отсутствие противоречий

The standard aligns with:

- ADR-012 canonical where it is Mango-specific: two-layer Mango Taxonomy and
  `Product -> Service -> Module -> Function`;
- ADR-011 canonical v1.0: Industry Taxonomy, `voice-channel`, `channel` facet;
- Industry Taxonomy Standard: strict `industry_ref`, `alignment_type`, facets;
- issue #146 audit: processed KB evidence for Function and terminology;
- issue #154 body: mandatory clusters, function types, mapping and
  machine-readable contracts.

Known ADR-012 synchronization drift remains documented rather than silently
absorbed: this standard uses `supported_by_services[]`, canonical Industry
registry paths and current Industry facet names because ADR-011 has priority over
ADR-012 for the Industry reference layer.

### 14.5 Машиночитаемость

Validator-ready elements are explicit:

- schema title `MangoTaxonomyDocument`;
- `$schema` and `$defs`;
- regex for slugs;
- required fields;
- enum values;
- mapping object shape;
- YAML examples;
- validation severity matrix.

## Источники

- ADR-012 Mango Taxonomy:
  [`standards/decisions/ADR-012-mango-taxonomy.md`](decisions/ADR-012-mango-taxonomy.md)
- ADR-011 Industry Taxonomy:
  [`standards/decisions/ADR-011-industry-taxonomy.md`](decisions/ADR-011-industry-taxonomy.md)
- Industry Taxonomy Standard:
  [`standards/industry-taxonomy-standard.md`](industry-taxonomy-standard.md)
- Industry reference taxonomy registry:
  [`kb/industry-taxonomy/reference-taxonomy.json`](../kb/industry-taxonomy/reference-taxonomy.json)
- Voice/digital channels analysis:
  [`docs/analysis/voice-digital-channels-comparison.md`](../docs/analysis/voice-digital-channels-comparison.md)
- Issue #146 Mango Taxonomy audit:
  [`docs/audit/issue-146-mango-taxonomy-validation.md`](../docs/audit/issue-146-mango-taxonomy-validation.md)
- Independent taxonomy standards audit:
  [`docs/audit/taxonomy-standards-independent-review.md`](../docs/audit/taxonomy-standards-independent-review.md)
- Mango official products registry:
  [`kb/mango-taxonomy/official-products.yaml`](../kb/mango-taxonomy/official-products.yaml)
- Mango internal registry:
  [`kb/mango-taxonomy/internal-registry.yaml`](../kb/mango-taxonomy/internal-registry.yaml)
- Mango product mapping registry:
  [`kb/mango-taxonomy/product-mapping.yaml`](../kb/mango-taxonomy/product-mapping.yaml)
- Issue #154:
  <https://github.com/G-Ivan-A/mango_ba_prompts/issues/154>
- Issue #164:
  <https://github.com/G-Ivan-A/mango_ba_prompts/issues/164>
