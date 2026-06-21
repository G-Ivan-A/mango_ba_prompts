---
status: draft
version: 0.1
updated: 2026-06-21
ai-generated: true
type: standard
scope: industry-taxonomy
issue: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/152"
depends_on:
  - "standards/decisions/ADR-011-industry-taxonomy.md"
  - "standards/decisions/ADR-012-mango-taxonomy.md"
related_artifacts:
  - "docs/analysis/voice-digital-channels-comparison.md"
  - "kb/industry/reference-taxonomy.json"
  - "kb/industry/reference-taxonomy.schema.json"
  - "standards/product-classification-contract.md"
validated_by:
  - "scripts/validate_issue_152_industry_taxonomy_standard.py"
  - "scripts/validate_issue_156_industry_taxonomy_registry.py"
---

# Стандарт Industry Taxonomy

> Носитель архитектурного решения:
> [ADR-011 Industry Taxonomy](decisions/ADR-011-industry-taxonomy.md).
> Связанный вендорский слой:
> [ADR-012 Mango Taxonomy](decisions/ADR-012-mango-taxonomy.md).
> Нормативный словарь: RFC 2119 / BCP 14
> (**ДОЛЖЕН**, **НЕ ДОЛЖЕН**, **СЛЕДУЕТ**, **МОЖНО**).

Этот стандарт задаёт правила применения Industry Taxonomy как эталонной
отраслевой классификации для коммуникационных продуктов, возможностей,
требований, KB-источников и валидаторов. ADR-011 объясняет, почему принята
модель; этот стандарт объясняет, как её использовать. Machine-readable registry
для canonical nodes находится в
[`kb/industry/reference-taxonomy.json`](../kb/industry/reference-taxonomy.json),
а его структурный контракт - в
[`kb/industry/reference-taxonomy.schema.json`](../kb/industry/reference-taxonomy.schema.json).

## 1. Область применения

### 1.1 Что регулирует стандарт

Стандарт ДОЛЖЕН применяться к любому артефакту репозитория, который:

- ссылается на отраслевой taxonomy node;
- маппит Mango Taxonomy на отраслевой слой;
- классифицирует продуктовую возможность, requirement, KB-фрагмент, API-операцию,
  UI-действие, настройку или бизнес-правило;
- генерирует или проверяет `industry_ref`;
- строит валидатор для taxonomy tags, mapping files или product registry.

Стандарт регулирует:

- уровни `Domain -> Capability -> Feature -> Function`;
- обязательные и опциональные атрибуты taxonomy nodes;
- cross-cutting facets, включая `channel`;
- формат строгих ссылок `industry_ref`;
- правила выбора `alignment_type`;
- правила классификации граничных случаев;
- процесс изменения таксономии;
- минимальный контракт CI-валидатора;
- правила для AI-агентов, которые создают или изменяют taxonomy mapping.

### 1.2 Что стандарт НЕ регулирует

Стандарт НЕ ДОЛЖЕН использоваться как:

- стандарт Mango Taxonomy;
- реестр конкретных продуктов Mango;
- коммерческий каталог, прайс-лист или procurement-реестр;
- описание тарифов, пакетов, SLA, российских реестров ПО или договорных условий;
- replacement для ADR-011, ADR-012 или processed KB evidence.

Конкретные продукты Mango, их публичные названия, внутренние сервисы, модули и
registry entries ДОЛЖНЫ описываться в будущих Mango-артефактах, совместимых с
ADR-012. В этом стандарте допускаются только абстрактные примеры или примеры
уровня отраслевого класса, не являющиеся описанием конкретного Mango-продукта.

### 1.3 Приоритет источников

При конфликте источников применяется такой порядок:

1. явное issue/ADR/PR-review решение, помеченное как taxonomy override and
   accepted by maintainer/founder;
2. этот стандарт для правил применения Industry Taxonomy;
3. `kb/industry/reference-taxonomy.json` для canonical node ids below Domain;
4. ADR-011 в статусе `canonical` как архитектурное решение;
5. ADR-012 и `standards/mango-taxonomy-standard.md` только для Mango-specific
   Product/Service/Module/Function layer;
6. аналитика `docs/analysis/voice-digital-channels-comparison.md`;
7. `standards/product-classification-contract.md`;
8. source evidence из processed KB или внешних отраслевых источников.

Обычный комментарий в issue не отменяет taxonomy contract сам по себе. Если
ADR-012 противоречит ADR-011, применяется ADR-011. Если Mango Taxonomy
противоречит этому стандарту, конфликт ДОЛЖЕН быть вынесен в PR с явным
решением: изменить Industry Taxonomy, изменить Mango Taxonomy или зафиксировать
vendor-specific extension.

### 1.4 Industry vs Mango responsibility boundary

Industry Taxonomy ДОЛЖНА отвечать на вопрос: "какой отраслевой node описывает
возможность?" Mango Taxonomy ДОЛЖНА отвечать на вопрос: "какой публичный продукт,
внутренний service/module/function or registry entry Mango реализует эту
возможность?"

Правила выбора стандарта:

- использовать этот стандарт и `kb/industry/reference-taxonomy.json`, когда
  артефакт создаёт, проверяет или выбирает `industry_ref`;
- использовать Mango Taxonomy Standard, когда артефакт описывает Product,
  Service, Module, Function, official URLs, clusters, internal services or
  Mango-specific mappings;
- не создавать Industry slug из Mango label; если canonical Industry node
  отсутствует, использовать nearest canonical parent with `mapping_gap`;
- не переносить Mango cluster/id в Industry hierarchy without source-backed
  change request.

## 2. Нормативные термины

### 2.1 Taxonomy

**Taxonomy** - управляемая иерархия понятий с устойчивыми идентификаторами,
строгими границами уровней, правилами изменения и проверяемыми ссылками.
Taxonomy НЕ ДОЛЖНА быть списком свободных тегов.

### 2.2 Taxonomy node

**Taxonomy node** - один канонический элемент таксономии на уровне Domain,
Capability, Feature или Function. Каждый node ДОЛЖЕН иметь:

- canonical `id`;
- `level`;
- краткое определение;
- parent reference, если уровень не Domain;
- lifecycle status;
- evidence или ссылку на решение, которое его вводит.

### 2.3 Domain

**Domain** - верхняя отраслевая область коммуникационного рынка, объединяющая
устойчивый набор capability по общей business/product semantics.

Domain отвечает на вопрос: "В какой крупной отраслевой области находится
возможность?"

Domain ДОЛЖЕН:

- быть достаточно крупным, чтобы содержать несколько Capability;
- описывать область рынка, а не экран, API, тариф, команду или конкретный
  вендорский продукт;
- иметь устойчивую границу относительно соседних domains;
- быть пригодным для верхнеуровневой аналитики, ownership и navigation.

Domain НЕ ДОЛЖЕН:

- создаваться ради одной функции;
- совпадать с маркетинговым названием продукта;
- описывать коммерческий пакет, сегмент клиента, регион или отраслевой vertical;
- заменять cross-cutting facet.

### 2.4 Capability

**Capability** - группа возможностей внутри Domain, выражающая способность
системы, продукта или сервиса достигать повторяемого результата.

Capability отвечает на вопрос: "Какую способность должен иметь продукт или
сервис?"

Capability ДОЛЖНА:

- принадлежать ровно одному primary Domain;
- объединять несколько Feature или достаточную группу Functions;
- иметь business or operational purpose;
- быть стабильнее, чем конкретный UI, API endpoint или настройка;
- быть достаточно конкретной, чтобы по ней можно было назначить owner и evidence.

Capability НЕ ДОЛЖНА:

- быть одноразовым действием пользователя;
- быть только техническим параметром;
- использоваться как "корзина" для unrelated features;
- заменять `alignment_type` при many-to-many mapping.

### 2.5 Feature

**Feature** - конкретная проверяемая возможность внутри Capability, реализуемая
на пользовательской, админской, интеграционной или автоматической поверхности.

Feature отвечает на вопрос: "Что именно используется, настраивается или
интегрируется?"

Feature ДОЛЖНА:

- принадлежать Capability;
- группировать связанные Functions;
- иметь observable behavior или configuration surface;
- быть применимой в сценарии пользователя, администратора, оператора,
  интеграции или автоматизации.

Feature НЕ ДОЛЖНА:

- описывать весь Domain;
- смешивать несколько unrelated capabilities;
- быть только label без проверяемого поведения;
- включать коммерческий статус, тариф или procurement condition.

### 2.6 Function

**Function** - минимальная проверяемая единица поведения, настройки,
API-действия, UI-действия, параметра или бизнес-правила внутри Feature.

Function отвечает на вопрос: "Что можно отдельно описать, проверить,
протрассировать или связать с acceptance criteria?"

Function ДОЛЖНА:

- принадлежать Feature;
- иметь один основной `function_type`;
- быть достаточно атомарной для независимой проверки;
- иметь effect, state change, decision, event, data retrieval or UI interaction;
- иметь evidence reference при включении в registry.

Function НЕ ДОЛЖНА:

- делиться дальше без потери смысла проверки;
- подменять Feature, если речь идёт о наборе сценариев;
- становиться отдельным Domain или Capability только из-за важности;
- смешивать бизнес-результат и UI-шаг, если их можно разделить через
  `function_type`.

### 2.7 Facet

**Facet** - ортогональная размерность классификации, которая описывает свойство
taxonomy node или mapping, но НЕ является уровнем иерархии.

Facet отвечает на вопрос: "Какая дополнительная ось нужна для поиска,
валидации или анализа, не меняя parent-child hierarchy?"

Facet ДОЛЖЕН:

- иметь закрытый словарь значений, если используется валидатором;
- быть независимым от primary hierarchy;
- применяться одинаково к совместимым domains;
- не создавать новую ветку hierarchy.

### 2.8 `industry_ref`

`industry_ref` - строгая typed reference на node Industry Taxonomy. Это не тег,
не строковое описание и не свободная метка.

Минимальная форма:

```yaml
industry_ref:
  domain: contact-center
alignment_type: primary
```

Полная форма:

```yaml
industry_ref:
  domain: contact-center
  capability: interaction-routing
  feature: queue-routing
  function: assign-interaction-to-agent
alignment_type: primary
```

### 2.9 `alignment_type`

`alignment_type` описывает роль связи между source entity и Industry Taxonomy.
Допустимы только значения:

- `primary` - основной отраслевой смысл entity;
- `secondary` - значимая дополнительная связь;
- `supporting` - platform, hardware, security, integration или operational
  support связь.

### 2.10 Свободный tag

Свободный tag - произвольная строка, которая не резолвится в canonical taxonomy
node или утверждённый facet value. Свободный tag НЕ ДОЛЖЕН использоваться внутри
`industry_ref`. Свободные labels МОЖНО хранить только вне Industry Taxonomy:
например, в `aliases`, `source_terms`, `notes`, `industry`, `segment`,
`region`, `use_case`.

### 2.11 RFC 2119 / BCP 14 terms

Нормативные слова используются в смысле RFC 2119 / BCP 14:

| Термин | Значение для этого стандарта |
| --- | --- |
| `ДОЛЖЕН` / `MUST` | Обязательное требование. Нарушение делает mapping или registry entry invalid. |
| `НЕ ДОЛЖЕН` / `MUST NOT` | Запрещённое поведение. Валидатор SHOULD report error unless explicitly marked legacy-exempt. |
| `СЛЕДУЕТ` / `SHOULD` | Рекомендуемое поведение. Отклонение требует documented rationale. |
| `МОЖЕТ` / `MAY` | Допустимое поведение, не обязательное для каждого артефакта. |

## 3. Каноническая модель

Industry Taxonomy использует ровно четыре уровня:

```text
Domain -> Capability -> Feature -> Function
```

### 3.1 Канонические domains

Начальный набор Domain берётся из ADR-011 canonical v1.0:

| Domain | Назначение | Обязательные границы |
| --- | --- | --- |
| `voice-ucaas` | Телеком-инфраструктура UCaaS и голосовой канал. | Включает `voice-channel`, но не поглощает contact-center orchestration. |
| `contact-center` | Customer operations, routing, queues, agent/supervisor workspace, WFM/QM and orchestration. | Оркестрирует каналы, но не становится каналом сам по себе. |
| `digital-channels` | Текстовые и digital interaction channels. | Канальный слой для text/async interactions; не включает голосовую телеком-инфраструктуру. |
| `ai-automation` | Продаваемые AI, bot and automation capabilities. | AI как домен не отменяет AI-assisted facet в других domains. |
| `analytics` | Reporting, dashboards, product/customer/marketing analytics. | Не включает внутреннюю commercial/deal analytics vendor-side без customer-facing product semantics. |
| `hardware` | Device/access edge: phones, headsets, rooms, physical access endpoints. | Поддерживает SaaS domains, но не заменяет их. |
| `security` | Access control, information security, compliance-related product capabilities. | Compliance facets не становятся security node без product behavior. |

`platform` is not an eighth Domain. It is fixed as a cross-domain/productizable
layer in the `cross_domain_layers` section of
`kb/industry/reference-taxonomy.json`. In `industry_ref`, the existing field
`domain` is retained for compatibility and MAY contain `platform`; validators
MUST resolve that value against `domains[]` plus `cross_domain_layers[]`.

| Cross-domain layer | Назначение | Обязательные границы |
| --- | --- | --- |
| `platform` | APIs, integrations, CPaaS, events, extension points, service-desk/vendor-support extensions. | Используется как primary только для productizable platform/API capability; иначе supporting. |

### 3.2 Machine-readable registry coverage

Canonical node ids below Domain ДОЛЖНЫ браться из
[`kb/industry/reference-taxonomy.json`](../kb/industry/reference-taxonomy.json).
Schema registry contract ДОЛЖЕН соответствовать
[`kb/industry/reference-taxonomy.schema.json`](../kb/industry/reference-taxonomy.schema.json).

Минимальная проверяемая структура registry:

```text
domains[]
  capabilities[]
    features[]
      functions[]
cross_domain_layers[]
  capabilities[]
    features[]
      functions[]
facets
```

Registry v1.0.0 закрывает audit blocker "ниже Domain нет canonical registry":

| Area | Examples of canonical coverage |
| --- | --- |
| `voice-ucaas` | `voice-channel`, `cloud-pbx`, `number-management`, `call-recording`, `unified-communications` |
| `contact-center` | `omnichannel-contact-center`, `agent-workspace`, `outbound-calling`, `quality-management`, `workforce-management`, `agent-assist`, `supervisor-assist` |
| `digital-channels` | `sms-messaging`, `omnichannel-messaging`, `website-chat` |
| `ai-automation` | `chatbot`, `voice-bot`, `process-robot`, `speech-analytics` |
| `analytics` | `call-tracking`, `end-to-end-analytics`, `multichannel-analytics`, `product-analytics` |
| `security` | `information-security` with `access-control` and `role-based-access-control` |
| `platform` | `platform-integration`, `open-api`, `cpaas`, `service-desk`, `vendor-support-services` |

Если Mango или KB source использует неканонический candidate вроде
`team-messaging`, `conversation-analytics`, `supervisor-workspace` or
`role-management`, Industry mapping НЕ ДОЛЖЕН invent that slug silently. Mapping
ДОЛЖЕН выбрать nearest canonical parent from registry and add `mapping_gap`, or
создать change request по §10.3.

### 3.3 Правила parent-child

Каждый non-Domain node ДОЛЖЕН иметь parent:

- Capability -> Domain;
- Feature -> Capability;
- Function -> Feature.

Parent-child связь ДОЛЖНА означать semantic containment: дочерний node является
частью смысла parent, а не просто часто встречается рядом.

Parent-child связь НЕ ДОЛЖНА создаваться по таким основаниям:

- оба node продаются одним vendor;
- оба node упомянуты в одном PDF;
- оба node находятся на одном экране;
- оба node входят в один тариф;
- один node технически вызывает другой.

Если связь важна, но не является containment, она ДОЛЖНА фиксироваться отдельным
relationship или `alignment_type: supporting`, а не parent-child.

### 3.4 Many-to-many mapping

Между Mango Taxonomy и Industry Taxonomy many-to-many является нормой.

Правила:

- один source Product может иметь несколько `industry_alignment`;
- один source Service может поддерживать несколько Industry Capability;
- один Module может иметь primary Feature и supporting platform/security Feature;
- одна Function может иметь primary Function и secondary/supporting relations;
- каждый source entity ДОЛЖЕН иметь не более одного `primary` на одинаковой
  глубине, если не указано обоснование split semantics.

Пример корректной many-to-many формы:

```yaml
industry_alignment:
  - industry_ref:
      domain: contact-center
      capability: interaction-routing
    alignment_type: primary
  - industry_ref:
      domain: platform
      capability: open-api
    alignment_type: supporting
```

## 4. Идентификаторы и структура узлов

### 4.1 Canonical slug

Canonical slug ДОЛЖЕН:

- быть lowercase;
- использовать ASCII letters, digits and hyphen;
- начинаться с letter;
- не заканчиваться hyphen;
- быть stable после публикации;
- быть уникальным внутри своего уровня и parent scope.

Допустимый pattern:

```text
^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$
```

Примеры допустимых slug:

- `voice-ucaas`;
- `voice-channel`;
- `interaction-routing`;
- `agent-workspace`;
- `configure-webhook-endpoint`.

Недопустимые slug:

- `Voice_UCaaS` - uppercase and underscore;
- `mango-contact-center` - vendor/product specific для Industry Taxonomy;
- `ivr` без контекста, если parent не делает смысл однозначным;
- `best-feature` - marketing adjective;
- `api/v1/calls` - endpoint path вместо taxonomy slug.

### 4.2 Минимальная структура node

Machine-readable registry ДОЛЖЕН хранить node в JSON форме, проверяемой
`kb/industry/reference-taxonomy.schema.json`. Минимальный YAML-представимый
контракт:

```yaml
id: interaction-routing
level: capability
name_ru: Маршрутизация обращений
name_en: Interaction routing
definition: >
  Группа возможностей для выбора очереди, оператора, правила или следующего
  шага обработки обращения.
parent:
  domain: contact-center
lifecycle_status: active
evidence_refs:
  - standards/decisions/ADR-011-industry-taxonomy.md
```

Для Feature:

```yaml
id: queue-routing
level: feature
parent:
  domain: contact-center
  capability: interaction-routing
```

Для Function:

```yaml
id: assign-interaction-to-agent
level: function
function_type: business
parent:
  domain: contact-center
  capability: interaction-routing
  feature: queue-routing
```

### 4.3 JSON Schema contract

Canonical registry structure ДОЛЖНА валидироваться схемой
`kb/industry/reference-taxonomy.schema.json`. Mapping artifacts MAY use the
following JSON Schema fragment for `industry_ref`; parent-chain existence is
then checked by registry-aware validator logic.

```json
{
  "$id": "industry-taxonomy-mapping.schema.json",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$defs": {
    "slug": {
      "type": "string",
      "pattern": "^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$"
    },
    "referenceArea": {
      "enum": [
        "voice-ucaas",
        "contact-center",
        "digital-channels",
        "ai-automation",
        "analytics",
        "hardware",
        "security",
        "platform"
      ]
    },
    "industryRef": {
      "type": "object",
      "required": ["domain"],
      "additionalProperties": false,
      "properties": {
        "domain": { "$ref": "#/$defs/referenceArea" },
        "capability": { "$ref": "#/$defs/slug" },
        "feature": { "$ref": "#/$defs/slug" },
        "function": { "$ref": "#/$defs/slug" }
      }
    },
    "alignmentType": {
      "enum": ["primary", "secondary", "supporting"]
    },
    "industryAlignment": {
      "type": "object",
      "required": ["industry_ref", "alignment_type"],
      "additionalProperties": false,
      "properties": {
        "industry_ref": { "$ref": "#/$defs/industryRef" },
        "alignment_type": { "$ref": "#/$defs/alignmentType" },
        "evidence_refs": {
          "type": "array",
          "items": { "type": "string" }
        },
        "mapping_gap": {
          "type": "object"
        },
        "facets": {
          "type": "object"
        }
      }
    }
  },
  "type": "object",
  "properties": {
    "industry_alignment": {
      "type": "array",
      "items": { "$ref": "#/$defs/industryAlignment" }
    }
  }
}
```

### 4.4 Lifecycle status

Node ДОЛЖЕН иметь один lifecycle status:

| Status | Значение | Использование валидатором |
| --- | --- | --- |
| `proposed` | Node предложен, но не является canonical. | Можно ссылаться только в draft/proposed artifacts. |
| `active` | Node canonical и разрешён для production mapping. | Валидатор принимает без warnings. |
| `deprecated` | Node заменён или выводится из использования. | Валидатор принимает с warning and replacement hint. |
| `removed` | Node больше не разрешён. | Валидатор ДОЛЖЕН падать, если mapping не legacy-exempt. |

Статус `active` НЕ ДОЛЖЕН назначаться без source evidence или ADR/standard
decision.

### 4.5 Alias and source terms

`aliases` и `source_terms` нужны для поиска и evidence, но не являются
canonical identifiers.

```yaml
id: interaction-routing
aliases:
  - omnichannel-routing
  - skills-routing
source_terms:
  - ACD
  - automatic call distribution
```

Правила:

- alias МОЖЕТ резолвиться в один canonical node;
- один alias НЕ ДОЛЖЕН silently резолвиться в несколько nodes;
- если alias ambiguous, валидатор ДОЛЖЕН требовать явного disambiguation;
- source term НЕ ДОЛЖЕН использоваться в `industry_ref`.

## 5. Правила классификации

### 5.1 Общий алгоритм

Классификатор ДОЛЖЕН использовать такой порядок:

1. Определить observable behavior or business meaning source entity.
2. Исключить commercial, geography_region, procurement, industry_vertical,
   segment and packaging labels.
3. Выбрать самый глубокий уровень, подтверждённый evidence.
4. Проверить parent-chain на semantic containment.
5. Выбрать `alignment_type`.
6. Добавить facets только если они ортогональны hierarchy.
7. Зафиксировать evidence refs.
8. Если canonical node отсутствует, создать proposed node или open question, но
   НЕ подставлять свободный tag.

### 5.2 Выбор уровня

| Если source entity описывает... | Уровень |
| --- | --- |
| крупную рыночную область | Domain |
| способность достигать повторяемого результата | Capability |
| конкретную возможность, сценарий, экранный/интеграционный блок | Feature |
| атомарное действие, параметр, команду, событие, настройку или правило | Function |
| канал, регион, vertical, AI-assisted, security/compliance property | Facet |
| segment, use_case, free source label | Metadata outside `industry_ref` |
| тариф, SKU, procurement code, договорный пакет | Не Industry Taxonomy |

### 5.3 Проверка атомарности Function

Function считается достаточно атомарной, если на все вопросы можно ответить
"да":

- можно ли проверить её отдельно?
- имеет ли она понятный input/action/condition?
- имеет ли она observable result, state change, emitted event or decision?
- можно ли связать с acceptance criterion without describing unrelated behavior?
- не скрывает ли она набор independent features?

Если хотя бы два ответа "нет", элемент СЛЕДУЕТ поднять на уровень Feature или
Capability.

### 5.4 Правило достаточной глубины

Mapping ДОЛЖЕН идти настолько глубоко, насколько позволяет evidence:

- если известен только Domain, ссылка останавливается на Domain;
- если известна Capability, Domain-only mapping считается неполным;
- если source Function известна, но Industry Function ещё не canonical, mapping
  ДОЛЖЕН ссылаться на ближайший canonical parent and mark gap;
- валидатор НЕ ДОЛЖЕН требовать Function-level mapping для Product-level entity.

### 5.5 Правило primary meaning

Primary meaning выбирается по основной ценности source entity для конечного
пользователя или customer organization, а не по техническому способу реализации.

Пример:

- функция "назначить обращение оператору" primary = `contact-center`;
- webhook delivery для этой функции supporting = `platform`;
- права доступа к этой функции supporting = `security`.

### 5.6 Правило инфраструктура vs канал

Голос в Industry Taxonomy имеет двойную природу:

- infrastructure/resource слой внутри `voice-ucaas`;
- named channel layer через capability `voice-channel`.

Правила:

- pure SIP/PSTN/numbering/resource capability НЕ ДОЛЖНА получать facet
  `channel`, если source entity не описывает interaction;
- голосовое взаимодействие ДОЛЖНО использовать `voice-channel` or compatible
  voice Feature and facet `channel.channel_kind: voice`;
- текстовое взаимодействие ДОЛЖНО использовать `digital-channels` and facet
  `channel.channel_kind: text`;
- contact-center orchestration МОЖЕТ иметь `channel` facet, но не становится
  channel domain.

### 5.7 Правило AI

AI может быть:

- Domain `ai-automation`, если source entity продаётся или описывается как
  AI/bot/automation capability;
- facet or metadata, если AI assists a capability in another domain;
- implementation detail, если AI не меняет product behavior or user-facing
  semantics.

AI НЕ ДОЛЖЕН автоматически переносить node из `contact-center`, `analytics`,
`voice-ucaas` или `digital-channels` в `ai-automation`.

### 5.8 Правило platform

`platform` используется для API, integrations, CPaaS, events, extension points,
developer surfaces and cross-domain enablement.

Platform mapping:

- primary, если source entity является API/CPaaS/platform productizable
  capability;
- supporting, если API/integration только обслуживает прикладную функцию;
- secondary, если API/integration является значимой частью customer value, но
  не единственной основной ценностью.

### 5.9 Правило security/compliance

Security node используется только когда source entity имеет product behavior:
authentication, authorization, access policy, audit, encryption, privacy control
or compliance workflow.

Compliance label, law, registry or certification alone НЕ ДОЛЖЕН становиться
Industry Taxonomy node. Такие признаки СЛЕДУЕТ хранить in
`facets.security_compliance` or metadata outside `industry_ref`.

### 5.10 Правило analytics

`analytics` используется для customer-facing analytics, reporting, dashboards,
attribution, quality insights and operational metrics.

Internal vendor deal analytics, sales pipeline analytics or commercial reporting
НЕ ДОЛЖНЫ попадать в Industry Taxonomy, если они не являются продуктовой
возможностью для клиента.

## 6. Cross-cutting facets

Facet применяется только тогда, когда свойство нужно искать, фильтровать,
валидировать или генерировать across domains. Facet НЕ ДОЛЖЕН дублировать
canonical hierarchy.

### 6.1 Базовый контракт facets

```yaml
facets:
  channel:
    channel_kind: voice
    synchronicity: sync
    direction: inbound
  ai_assisted: true
  security_compliance:
    law:
      - ru-152fz
    personal_data: true
  geography_region:
    - ru
```

Каждый facet ДОЛЖЕН иметь:

- name;
- closed value set or documented value type;
- applicability rule;
- validation rule;
- examples.

### 6.2 Facet `channel`

`channel` описывает interaction medium. Он не описывает vendor product, tariff,
technical endpoint or infrastructure resource.

Allowed structure:

```yaml
facets:
  channel:
    channel_kind: voice
    synchronicity: sync
    direction: inbound
```

Allowed values:

| Field | Values | Rule |
| --- | --- | --- |
| `channel_kind` | `voice`, `text`, `video` | ДОЛЖЕН быть указан для channel facet. |
| `synchronicity` | `sync`, `async` | ДОЛЖЕН соответствовать interaction semantics. |
| `direction` | `inbound`, `outbound`, `broadcast` | ДОЛЖЕН соответствовать инициатору или pattern of communication. |

Allowed direction x synchronicity combinations:

| `direction` | Allowed `synchronicity` | Rule |
| --- | --- | --- |
| `inbound` | `sync`, `async` | Voice/video/live chat are usually `sync`; email, SMS and delayed messenger replies are usually `async`. |
| `outbound` | `sync`, `async` | Live calls are usually `sync`; campaigns, email and SMS dispatch are usually `async`. |
| `broadcast` | `sync`, `async` | Live voice/video broadcast MAY be `sync`; SMS/push/email broadcast SHOULD be `async`. Evidence must explain the choice when ambiguous. |

`channel_kind: voice`:

- используется для голосового interaction;
- обычно `synchronicity: sync`;
- может быть `inbound`, `outbound` или `broadcast`;
- ДОЛЖЕН отличаться от SIP/PSTN/number resource mapping.

`channel_kind: text`:

- используется для chat, messenger, email, SMS or similar text interaction;
- обычно `synchronicity: async`, но может быть `sync` для live chat;
- не требует выделенного telecom resource domain.

`channel_kind: video`:

- используется для video meeting, video call or visual realtime interaction;
- обычно `synchronicity: sync`.

### 6.3 Пример: входящий голосовой канал

```yaml
industry_ref:
  domain: voice-ucaas
  capability: voice-channel
  feature: inbound-voice-call
alignment_type: primary
facets:
  channel:
    channel_kind: voice
    synchronicity: sync
    direction: inbound
```

### 6.4 Пример: входящий текстовый канал

```yaml
industry_ref:
  domain: digital-channels
  capability: omnichannel-messaging
  feature: messenger-integration
alignment_type: primary
facets:
  channel:
    channel_kind: text
    synchronicity: async
    direction: inbound
```

### 6.5 Пример: pure voice infrastructure без channel facet

```yaml
industry_ref:
  domain: voice-ucaas
  capability: sip-connectivity
alignment_type: supporting
```

Такой mapping НЕ ДОЛЖЕН получать `facets.channel`, потому что SIP connectivity
сам по себе является resource/infrastructure capability, а не interaction
channel.

### 6.6 Other facets

Следующие facets являются canonical conceptual overlays. Их registry contract
ДОЛЖЕН быть синхронизирован с `kb/industry/reference-taxonomy.json`:

| Facet | Типичные значения | Применение |
| --- | --- | --- |
| `ai_assisted` | `true`, `false` | AI assists capability outside `ai-automation`. |
| `security_compliance` | controlled object | Law, privacy, access, audit, retention overlays. |
| `commercial` | controlled object | Packaging, SKU, tariff; outside `industry_ref`. |
| `procurement` | controlled object | Procurement code, registry, public-sector labels. |
| `industry_vertical` | controlled list or external code | Customer industry/vertical. |
| `geography_region` | ISO/country/market code | Region-specific availability or compliance. |

`segment` is intentionally not a canonical Industry facet in this standard.
Customer segment or market segment labels MAY be stored as source metadata
outside `industry_ref` until a separate change request adds a controlled facet.

Эти facets НЕ ДОЛЖНЫ использоваться как substitute for Domain/Capability.

## 7. Атрибуты и метаданные

### 7.1 Обязательные атрибуты registry node

| Field | Domain | Capability | Feature | Function |
| --- | --- | --- | --- | --- |
| `id` | required | required | required | required |
| `level` | required | required | required | required |
| `name_ru` or `name_en` | required | required | required | required |
| `definition` | required | required | required | required |
| `parent` | forbidden | required | required | required |
| `lifecycle_status` | required | required | required | required |
| `evidence_refs` | required | required | required | required |
| `function_type` | forbidden | forbidden | forbidden | required |

### 7.2 `function_type`

Every Function ДОЛЖНА have exactly one `function_type`.

Allowed values:

| `function_type` | Когда использовать | Примеры отраслевого смысла |
| --- | --- | --- |
| `business` | Function produces customer, operator or operational outcome. | transfer interaction, send message, generate summary, start campaign. |
| `configuration` | Function changes setting, policy, route, permission, lifecycle or integration configuration. | configure endpoint, set schedule, enable recording, assign role. |
| `ui-action` | Function describes UI interaction needed for scenario but not standalone business capability. | open panel, select widget, expand report, switch tab. |

Правила:

- `business` выбирается по результату, не по UI/API surface;
- `configuration` выбирается, если основной эффект - изменение управляемой
  настройки или политики;
- `ui-action` выбирается, если действие не создаёт самостоятельный business or
  configuration result;
- `function_type` НЕ ДОЛЖЕН использоваться как channel marker;
- API/UI/background surface ДОЛЖНА храниться отдельно, например в
  `interaction_surface`.

### 7.3 Рекомендуемые атрибуты Function

Следующий YAML fragment показывает Function-specific fields. Full registry node
also requires `name_ru`/`name_en`, `definition`, `lifecycle_status` and complete
parent-chain metadata from §4.2.

```yaml
id: configure-webhook-endpoint
level: function
function_type: configuration
interaction_surface: admin-ui
parent:
  domain: platform
  capability: open-api
  feature: webhook-management
aliases:
  - configure-callback-url
source_terms:
  - endpoint
  - callback
evidence_refs:
  - kb/mango-product-docs/processed/example/index.md
```

### 7.4 `interaction_surface`

`interaction_surface` describes where Function behavior is triggered or observed.
It is required for Function-level mapping artifacts that classify a concrete
source Function. Registry Function nodes SHOULD include it when source evidence
has a single dominant surface; otherwise the registry MAY omit it.

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
| `unknown` | Evidence is insufficient; allowed only for `proposed` entries and requires review before active status. |

Rules:

- `interaction_surface` is not a channel marker; channel belongs to
  `facets.channel`.
- `unknown` НЕ ДОЛЖЕН использоваться for `lifecycle_status: active`.
- API/webhook/background values do not automatically make `platform` primary;
  §5.8 still decides primary vs supporting.

### 7.5 Evidence refs

Каждый canonical node ДОЛЖЕН иметь evidence. Допустимые evidence refs:

- ADR or standard path;
- processed KB path;
- official vendor or standards URL;
- audit/analysis document path;
- registry path.

Evidence refs НЕ ДОЛЖНЫ быть:

- free-text "known by team";
- ссылка на недоступный локальный файл вне repository;
- screenshot без текстового пояснения;
- URL without stable context.

### 7.6 Confidence

Если mapping создаётся до полного registry, source entity МОЖЕТ иметь
`confidence`:

| Value | Meaning |
| --- | --- |
| `high` | exact canonical match with evidence |
| `medium` | stable parent match, deeper node missing |
| `low` | tentative mapping requiring SME review |

`confidence: low` НЕ ДОЛЖЕН использоваться для production registry без open
question or review marker.

## 8. Правила маппинга

### 8.1 Минимальный mapping object

```yaml
industry_alignment:
  - industry_ref:
      domain: contact-center
      capability: interaction-routing
    alignment_type: primary
    evidence_refs:
      - standards/decisions/ADR-011-industry-taxonomy.md
```

Правила:

- `industry_alignment` ДОЛЖЕН быть array;
- каждый item ДОЛЖЕН иметь `industry_ref` and `alignment_type`;
- `industry_ref.domain` ДОЛЖЕН присутствовать всегда and resolve to a registry
  `domains[].id` or `cross_domain_layers[].id`;
- deeper fields ДОЛЖНЫ присутствовать, если source level and evidence allow;
- `alignment_type` ДОЛЖЕН быть one of `primary`, `secondary`, `supporting`;
- `evidence_refs` ДОЛЖНЫ быть present for registry-grade mapping.

### 8.2 Depth by source level

| Source level | Минимальная глубина | Рекомендуемая глубина |
| --- | --- | --- |
| Mango Product | Domain | Domain/Capability |
| Mango Service | Capability | Capability |
| Mango Module | Feature | Feature |
| Mango Function | Function or nearest canonical parent | Function |
| KB section | Feature | Feature/Function |
| API endpoint | Function | Function |
| UI control | Function with `ui-action` or source term | Function |

Если source level unknown, mapping СЛЕДУЕТ начинать с closest observable
behavior and evidence.

Domain-only `industry_ref` is valid only when source level is Product, evidence
really stops at Domain, or the mapping explicitly carries `mapping_gap`.
Service, Module, Function, API endpoint and UI control mappings with known
behavior НЕ ДОЛЖНЫ stop at Domain without `mapping_gap`.

### 8.3 Primary, secondary, supporting

`primary`:

- ДОЛЖЕН отражать главный отраслевой смысл;
- ДОЛЖЕН быть present for every mapped entity, unless entity is purely
  supporting;
- НЕ ДОЛЖЕН использоваться дважды на same taxonomy depth без обоснования.

`secondary`:

- используется для significant additional semantics;
- не заменяет primary;
- ДОЛЖЕН иметь evidence.

`supporting`:

- используется для platform, hardware, security, integration or operational
  support relation;
- МОЖЕТ быть единственным type only if source entity itself is supporting by
  design;
- НЕ ДОЛЖЕН скрывать primary customer-facing meaning.

### 8.4 Mapping gaps

Если needed canonical node отсутствует:

```yaml
industry_alignment:
  - industry_ref:
      domain: contact-center
      capability: interaction-routing
    alignment_type: primary
    mapping_gap:
      missing_level: feature
      proposed_id: queue-routing
      reason: "Feature-level node is needed for queue assignment examples."
```

Правила:

- gap ДОЛЖЕН ссылаться на nearest canonical parent;
- `proposed_id` ДОЛЖЕН соответствовать slug rules;
- gap НЕ ДОЛЖЕН silently become free tag;
- production validator ДОЛЖЕН fail or warn according to artifact status.

Examples that require `mapping_gap` unless a change request adds canonical nodes:

- Mango source term `team-messaging` under `digital-channels` without a
  registry node;
- source term `conversation-analytics` when the registry only has nearest
  analytics or assist nodes;
- source term `supervisor-workspace` when the registry has `agent-workspace` and
  `supervisor-assist` but no canonical workspace node;
- source term `role-management` when the registry has
  `security/information-security/access-control/role-based-access-control`.

### 8.5 Запрещённые forms

Свободный tag внутри `industry_ref` запрещён:

```yaml
# bad
industry_ref: "contact center / routing / cool queue feature"
```

Vendor product as Industry Domain запрещён:

```yaml
# bad
industry_ref:
  domain: vendor-contact-center-suite
```

Facet as Domain запрещён:

```yaml
# bad
industry_ref:
  domain: healthcare
```

Commercial package as Capability запрещён:

```yaml
# bad
industry_ref:
  domain: contact-center
  capability: premium-plan
```

### 8.6 Формат для registry-backed mapping file

```yaml
taxonomy_mapping:
  version: 1
  mapping_scope: mango-to-industry
  source_taxonomy: mango-taxonomy
  target_taxonomy: industry-taxonomy
  entities:
    - source_id: source-entity-id
      source_level: module
      industry_alignment:
        - industry_ref:
            domain: contact-center
            capability: interaction-routing
            feature: queue-routing
          alignment_type: primary
          evidence_refs:
            - standards/decisions/ADR-011-industry-taxonomy.md
      facets:
        channel:
          channel_kind: voice
          synchronicity: sync
          direction: inbound
```

## 9. Граничные кейсы и анти-паттерны

### 9.1 Голосовая инфраструктура vs голосовой канал

Неправильно:

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

Почему плохо: SIP connectivity - infrastructure resource, not interaction.

Правильно:

```yaml
industry_ref:
  domain: voice-ucaas
  capability: sip-connectivity
alignment_type: supporting
```

Для interaction:

```yaml
industry_ref:
  domain: voice-ucaas
  capability: voice-channel
  feature: inbound-voice-call
alignment_type: primary
facets:
  channel:
    channel_kind: voice
    synchronicity: sync
    direction: inbound
```

### 9.2 Contact center не является каналом

Неправильно:

```yaml
industry_ref:
  domain: contact-center
  capability: voice-channel
```

Почему плохо: contact center orchestrates channels; voice channel belongs to
`voice-ucaas` as channel capability or appears as facet on contact-center
orchestration.

Правильно:

```yaml
industry_ref:
  domain: contact-center
  capability: interaction-routing
  feature: channel-based-routing
alignment_type: primary
facets:
  channel:
    channel_kind: voice
    synchronicity: sync
    direction: inbound
```

### 9.3 AI-assisted не всегда `ai-automation`

Неправильно:

```yaml
industry_ref:
  domain: ai-automation
  capability: agent-routing
```

Почему плохо: routing remains contact-center capability if AI only assists
decisioning.

Правильно:

```yaml
industry_ref:
  domain: contact-center
  capability: interaction-routing
  feature: skill-based-routing
alignment_type: primary
facets:
  ai_assisted: true
```

### 9.4 UI action не должен раздувать Capability

Неправильно:

```yaml
industry_ref:
  domain: analytics
  capability: open-dashboard-tab
```

Правильно:

```yaml
industry_ref:
  domain: analytics
  capability: real-time-reporting
  feature: dashboard-view
  function: open-dashboard-tab
alignment_type: primary
function_type: ui-action
```

### 9.5 Configuration не является отдельным Domain

Неправильно:

```yaml
industry_ref:
  domain: configuration
  capability: routing-settings
```

Правильно:

```yaml
industry_ref:
  domain: contact-center
  capability: interaction-routing
  feature: routing-rules
  function: configure-routing-rule
alignment_type: primary
function_type: configuration
```

### 9.6 Commercial package не входит в hierarchy

Неправильно:

```yaml
industry_ref:
  domain: voice-ucaas
  capability: enterprise-tariff
```

Правильно:

```yaml
industry_ref:
  domain: voice-ucaas
  capability: voice-channel
alignment_type: primary
facets:
  commercial:
    package: enterprise
```

### 9.7 Vertical не является Domain

Неправильно:

```yaml
industry_ref:
  domain: healthcare
```

Правильно:

```yaml
industry_ref:
  domain: contact-center
  capability: interaction-routing
alignment_type: primary
facets:
  industry_vertical:
    - healthcare
```

### 9.8 API endpoint не всегда platform primary

Неправильно:

```yaml
industry_ref:
  domain: platform
  capability: open-api
alignment_type: primary
```

для endpoint, который выполняет business function contact center.

Правильно:

```yaml
industry_alignment:
  - industry_ref:
      domain: contact-center
      capability: outbound-calling
      feature: campaign-management
      function: start-campaign
    alignment_type: primary
  - industry_ref:
      domain: platform
      capability: open-api
    alignment_type: supporting
```

## 10. Процесс эволюции

### 10.1 Когда можно добавлять node

Новый node МОЖНО предлагать, если:

- source evidence не маппится на existing canonical node;
- отличие является semantic, not naming;
- node нужен минимум двум examples or one strong standard/vendor evidence;
- parent-chain понятна;
- proposed slug соответствует правилам;
- описан impact on validators and mappings.

### 10.2 Когда нельзя добавлять node

Новый node НЕ ДОЛЖЕН добавляться, если:

- нужен только для одного vendor product name;
- является тарифом, commercial package, segment or vertical;
- дублирует existing node under alias;
- является implementation detail without taxonomy meaning;
- вводится без evidence;
- может быть facet instead of hierarchy node.

### 10.3 Change request contract

PR, который меняет Industry Taxonomy, ДОЛЖЕН содержать:

- problem statement;
- affected nodes and mappings;
- evidence refs;
- proposed YAML node(s);
- migration or compatibility note;
- validator changes;
- examples before/after;
- self-check against this standard.

### 10.4 Versioning

Стандарт и registry ДОЛЖНЫ использовать semantic meaning:

- patch: editorial clarification without behavior change;
- minor: additive node/facet/validator rule compatible with existing mappings;
- major: breaking change in hierarchy, required fields, allowed values or
  canonical slugs.

Canonical slugs НЕ ДОЛЖНЫ переименовываться без deprecation period and alias.

### 10.5 Deprecation

Deprecation ДОЛЖНА включать:

- old id;
- replacement id or reason no replacement exists;
- date/status;
- migration rule;
- validator severity;
- examples of old and new mapping.

Пример:

```yaml
id: old-routing-node
lifecycle_status: deprecated
replacement: interaction-routing
deprecation_reason: "Merged into broader canonical capability."
validator_severity: warning
```

### 10.6 Ownership

Если dedicated owner ещё не назначен, registry owner считается `unknown`, но PR
author ДОЛЖЕН указать review focus. Для canonical promotion owner SHOULD be
assigned to standard/governance maintainers or domain SME.

## 11. Контракт для валидатора

### 11.1 Минимальные проверки документа

Validator ДОЛЖЕН проверять:

- наличие `standards/industry-taxonomy-standard.md`;
- frontmatter fields: `status`, `version`, `updated`, `type`, `scope`,
  `issue`, `depends_on`;
- ссылки на ADR-011, ADR-012 and analysis;
- наличие разделов 1-13 and `## Источники`;
- наличие правил для Domain, Capability, Feature, Function;
- наличие `channel` facet with `channel_kind`, `synchronicity`, `direction`;
- наличие `function_type` with `business`, `configuration`, `ui-action`;
- наличие mapping format with `industry_ref` and `alignment_type`;
- наличие self-check section.

Implemented CI coverage:

| Validator | Implemented scope |
| --- | --- |
| `scripts/validate_issue_152_industry_taxonomy_standard.py` | Document structure, required normative sections, audit-regression tokens for this standard. |
| `scripts/validate_issue_156_industry_taxonomy_registry.py` | Registry JSON shape, canonical domains, `cross_domain_layers`, required capabilities/features/functions, evidence refs and core facet lists. |

Full generic validation of arbitrary mapping artifacts is not yet implemented
because no canonical mapping-file location exists in this repository. Until that
artifact exists, §11.2 is a normative contract for future mapping validators, not
a claim that every mapping check runs in current CI.

### 11.2 Минимальные проверки mapping object

Future mapping validator ДОЛЖЕН проверять:

1. `industry_alignment` exists and is array.
2. Each alignment has `industry_ref`.
3. `industry_ref.domain` is required.
4. `industry_ref.domain` exists in canonical registry `domains[]` or
   `cross_domain_layers[]`.
5. `industry_ref.capability`, if present, belongs to domain.
6. `industry_ref.feature`, if present, belongs to capability.
7. `industry_ref.function`, if present, belongs to feature.
8. No deeper field exists without parent field.
9. `alignment_type` is `primary`, `secondary` or `supporting`.
10. At least one `primary` exists unless entity is explicitly supporting-only.
11. `facets.channel.channel_kind` is one of `voice`, `text`, `video`.
12. `facets.channel.synchronicity` is one of `sync`, `async`.
13. `facets.channel.direction` is one of `inbound`, `outbound`, `broadcast`.
14. Function-level mappings include or inherit `function_type`.
15. `function_type` is `business`, `configuration` or `ui-action`.
16. Function-level mappings include or inherit allowed `interaction_surface`.
17. `facets.channel.direction` follows the direction x synchronicity table.
18. `evidence_refs` resolve to existing repo path or full URL.
19. No `industry_ref` value violates slug pattern.
20. No free-text taxonomy tag appears inside `industry_ref`.
21. Deprecated nodes produce warning with replacement.
22. Removed nodes produce failure unless legacy exemption is explicit.

Checks 1-22 are not yet implemented as one generic mapping-file validator in
current CI; registry-backed subsets are covered by issue #152/#156 validators as
listed in §11.1.

### 11.3 Severity

| Condition | Severity |
| --- | --- |
| Missing required field | error |
| Unknown canonical node | error |
| Invalid parent-chain | error |
| Invalid enum value | error |
| Free tag inside `industry_ref` | error |
| Missing evidence in draft | warning |
| Missing evidence in canonical registry | error |
| Deprecated node with replacement | warning |
| Ambiguous alias | error |
| Low confidence in production registry | error |
| `interaction_surface: unknown` on active node | error |

### 11.4 Validator pseudo-code

```text
for entity in mapping.entities:
  assert entity.industry_alignment is array
  primary_count = 0
  for alignment in entity.industry_alignment:
    ref = alignment.industry_ref
    require ref.domain
    validate_slug_chain(ref)
    validate_parent_chain(ref)
    validate_alignment_type(alignment.alignment_type)
    validate_facets(alignment.facets)
    if entity.level == "function":
      validate_interaction_surface(entity.interaction_surface, entity.lifecycle_status)
    validate_evidence(alignment.evidence_refs, entity.lifecycle_status)
    if alignment.alignment_type == "primary":
      primary_count += 1
  if primary_count == 0 and not entity.supporting_only_reason:
    error("missing primary alignment")
```

## 12. Контракт для AI-агентов

AI-агент, который создаёт taxonomy mapping, ДОЛЖЕН:

1. Прочитать issue, latest comments, ADR-011, ADR-012, this standard and relevant
   analysis before changing mapping.
2. Отличить ADR rationale from normative standard rules.
3. Искать existing canonical node before proposing a new one.
4. Использовать `industry_ref`, not free tags.
5. Заполнять `alignment_type`.
6. Добавлять evidence refs.
7. Не описывать concrete Mango products inside Industry Taxonomy standard.
8. Не создавать `research/` in this spoke.
9. Mark uncertainty as mapping gap or open question, not silent invented slug.
10. Run available validators before finalizing PR.

AI-агент НЕ ДОЛЖЕН:

- повышать proposed node to active without human-reviewable evidence;
- смешивать commercial/procurement/vertical facets with hierarchy;
- превращать source term into canonical id without checking aliases;
- считать UI label достаточным evidence для Domain/Capability;
- удалять existing taxonomy semantics without migration note.

### 12.1 Decision checklist для AI-агента

Перед добавлением mapping агент ДОЛЖЕН ответить:

- Какой source entity классифицируется?
- Какой observable behavior or business meaning evidence показывает?
- Какой nearest canonical node exists?
- Почему выбран уровень?
- Почему выбран `alignment_type`?
- Нужны ли facets?
- Есть ли `function_type`, если это Function?
- Какие evidence refs подтверждают mapping?
- Есть ли ambiguity, требующая `mapping_gap` или human review?

## 13. Самопроверка качества

### 13.1 Полнота

Стандарт покрывает все обязательные элементы issue #152:

- уровни Domain, Capability, Feature, Function;
- атрибуты node and mapping;
- `function_type`;
- cross-cutting facets including `channel`;
- canonical registry reference and JSON Schema contract;
- mapping rules;
- validation contract;
- evolution process;
- AI-agent contract;
- compatibility with ADR-011 and ADR-012.

### 13.2 Однозначность

Каждый normative term has:

- definition;
- level boundary;
- positive rules;
- negative rules;
- examples or validator implications.

Enum values are closed for:

- `alignment_type`;
- `function_type`;
- `channel_kind`;
- `synchronicity`;
- `direction`;
- `interaction_surface`;
- lifecycle status.

### 13.3 Отсутствие дублирования

Стандарт does not repeat ADR-011 source research tables, ADR-012 Mango product
crosswalk or the full `kb/industry/reference-taxonomy.json` registry. It
references them as source artifacts and defines application rules for validators
and mappings.

### 13.4 Отсутствие противоречий

Standard decisions align with:

- ADR-011 canonical v1.0: four-level hierarchy, domain set, `platform`,
  `voice-channel`, `channel` facet, strict mapping;
- `kb/industry/reference-taxonomy.json`: canonical below-Domain node ids and
  explicit `cross_domain_layers` for `platform`;
- ADR-012: Mango `Product -> Service -> Module -> Function`, `function_type`,
  many-to-many mapping and alias rules;
- voice/digital analysis: infrastructure asymmetry remains, channel naming
  asymmetry is resolved through `voice-channel` and `channel` facet.

### 13.5 Исполнимость

The validator contract is machine-actionable:

- required fields are explicit;
- enum values are listed;
- slug pattern is defined;
- parent-chain validation is defined;
- error/warning severity is defined;
- examples use YAML structures that can be parsed, and fragments are labelled;
- current CI validator scope is separated from not yet implemented generic
  mapping-file validation.

## Источники

- ADR-011 Industry Taxonomy:
  [`standards/decisions/ADR-011-industry-taxonomy.md`](decisions/ADR-011-industry-taxonomy.md)
- ADR-012 Mango Taxonomy:
  [`standards/decisions/ADR-012-mango-taxonomy.md`](decisions/ADR-012-mango-taxonomy.md)
- Voice/digital channels analysis:
  [`docs/analysis/voice-digital-channels-comparison.md`](../docs/analysis/voice-digital-channels-comparison.md)
- Industry Taxonomy registry:
  [`kb/industry/reference-taxonomy.json`](../kb/industry/reference-taxonomy.json)
- Industry Taxonomy registry schema:
  [`kb/industry/reference-taxonomy.schema.json`](../kb/industry/reference-taxonomy.schema.json)
- Product Classification Contract:
  [`standards/product-classification-contract.md`](product-classification-contract.md)
- RFC 2119 / BCP 14: <https://www.rfc-editor.org/info/bcp14>
- `dialog-taxonomy-approval.txt` - указан в issue #152 как обязательное
  вложение. В текущем checkout, issue API body, issue timeline, rendered issue
  HTML and GitHub code search attachment URL or file content were not available;
  substantive decisions from that dialog are represented in ADR-011 and
  `docs/analysis/voice-digital-channels-comparison.md`.
