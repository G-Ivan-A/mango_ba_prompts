---
status: canonical
version: 1.0
updated: 2026-06-21
ai-generated: true
type: adr
scope: industry-taxonomy
issue: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/139"
validated_by:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/146"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/148"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/150"
hub_research: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/mango/classification.md"
hub_research_sha: "73e94c6e69995ccf9e746c19d9c18359971285f2"
related_prs:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/pull/140"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/pull/149"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/pull/151"
related_artifacts:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/product-classification-contract.md"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/hub-research-dependencies.md"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/adr/008-industry-standards-standard.md"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/analysis/voice-digital-channels-comparison.md"
---

# ADR-011: Industry Taxonomy для классификации продуктов Mango Office

> **Статус:** Canonical · **Дата:** 2026-06-21 · **Issue:**
> <https://github.com/G-Ivan-A/mango_ba_prompts/issues/139> · **Доисследование:**
> <https://github.com/G-Ivan-A/mango_ba_prompts/issues/150> · **Hub research:**
> <https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/mango/classification.md>

> **Numbering note.** ADR-011 продолжает трёхзначную дорожку ADR стандартов
> (ADR-003...010). Размещение `standards/decisions/` выбрано потому, что issue
> #139 явно требует путь `standards/decisions/ADR-XXX-industry-taxonomy.md`.
> Этот ADR не создаёт сам стандарт, Mango Taxonomy, KB-данные или research-копию.

## Контекст

Issue #139 требует создать только ADR по **Industry Taxonomy**: эталонной
отраслевой таксономии, относительно которой позже можно будет проектировать
Mango Taxonomy и KB-классификацию. Жёсткие ограничения issue:

- не создавать сам стандарт Industry Taxonomy;
- не создавать Mango Taxonomy;
- не создавать KB-данные и `research/`;
- не менять структуру проекта сверх необходимого для ADR;
- не переводить решение в финальный статус без проверки человеком.

Входная база из Hub:

- `hybrid-Intelligence-lab/research/mango/classification.md`, версия 3.0,
  `status: reviewed`, `updated: 2026-05-27`;
- проверенный на 2026-06-20 `main` SHA:
  `73e94c6e69995ccf9e746c19d9c18359971285f2`;
- базовая модель:
  `Domain -> Capability -> Feature -> Function`;
- пилотные домены:
  `voice-ucaas`, `contact-center`, `digital-channels`, `ai-automation`,
  `analytics`, `hardware`, `security`;
- отдельный cross-domain блок `platform`:
  `platform-integration`, `open-api`, `cpaas`, `service-desk`,
  `vendor-support-services`;
- Product Layer отделён от Commercial Layer: цены, тарифы, procurement-коды,
  российские реестры и compliance-признаки не смешиваются с продуктовой
  классификацией.

Hub research уже содержит сильную Mango-ориентированную модель, но issue #139
требует сверить её с отраслевыми источниками и зафиксировать, какие отличия
нужно учесть перед будущим стандартом.

## Research: источники

Проверка выполнена 2026-06-20 по официальным страницам вендоров. Пять источников
заданы issue #139; ещё три выбраны дополнительно и обоснованы ниже.

| Источник | Тип сигнала | Что проверено |
| --- | --- | --- |
| Cisco Webex: <https://www.webex.com/>; Webex Contact Center: <https://www.webex.com/us/en/products/customer-experience/contact-center.html> | UCaaS + CCaaS + CPaaS + devices | Webex группирует calling, meetings, messaging, webinars/events, contact center, CPaaS, AI и devices в единую коммуникационную платформу. |
| MTS Exolve: <https://exolve.ru/> | VATS + CPaaS + robots | Exolve выделяет виртуальную АТС, номера, IP-телефонию, robots, SMS/Voice/Numbering API и омниканальные диалоги. |
| Twilio: <https://www.twilio.com/en-us> | CPaaS + conversations + data/AI | Twilio даёт сильный отраслевой сигнал для programmable messaging, voice, conversations, verification, customer data и orchestration. |
| RingCentral RingEX: <https://www.ringcentral.com/ringex.html>; RingCX: <https://www.ringcentral.com/ringcx.html> | UCaaS + CCaaS | RingCentral разделяет employee communications (messaging, video, phone) и AI contact-center/customer-experience слой. |
| Amazon Connect: <https://aws.amazon.com/products/connect/customer/features/> | Cloud contact center | Amazon Connect показывает CCaaS как workspace + voice/chat/email/tasks + routing + queues + analytics + management. |
| Genesys Cloud: <https://www.genesys.com/genesys-cloud> | CCaaS + WEM + journey | Выбран как зрелый enterprise CCaaS-ориентир: omnichannel, routing, workforce engagement, journey management, analytics, AI. |
| Microsoft Teams: <https://www.microsoft.com/en-us/microsoft-teams/group-chat-software>; Teams Phone: <https://www.microsoft.com/en-us/microsoft-teams/microsoft-teams-phone> | UCaaS/collaboration baseline | Выбран как массовый рынок employee collaboration: chat/channels, meetings/events, phone, rooms, premium AI/security. |
| 8x8 Work: <https://www.8x8.com/products/unified-communications>; 8x8 CPaaS: <https://cpaas.8x8.com/en/> | UCaaS + CCaaS + CPaaS | Выбран как вендор, который явно соединяет calling, meetings, messaging, contact center и programmable communications. |

Обоснование дополнительных источников:

1. **Genesys** нужен для проверки contact-center глубины: WEM/WFM, journey,
   routing, analytics и AI в enterprise-контуре.
2. **Microsoft Teams** нужен как внешний массовый UCaaS/collaboration эталон,
   чтобы не сводить industry taxonomy только к telephony/contact-center рынку.
3. **8x8** нужен как связующий пример UCaaS + CCaaS + CPaaS в одной платформе,
   близкий к гибридной форме Mango Office.

## Key findings

### 1. Четырёхуровневая модель Hub подтверждается

Модель `Domain -> Capability -> Feature -> Function` остаётся пригодной
для Industry Taxonomy. Вендоры различаются упаковкой продуктов, но повторяют
одни и те же уровни:

- domain: UCaaS, CCaaS, CPaaS/platform, AI automation, analytics, devices;
- capability: calling, messaging, meetings, routing, workforce management,
  programmable messaging, verification, bots, reporting;
- feature: queues, IVR, skills routing, conversation summaries, WhatsApp/SMS,
  call recording, CRM integration;
- function: send SMS, transfer call, assign agent, generate summary,
  verify number, create campaign.

### 2. Hub домены покрывают рынок, но `platform` нужно сделать явным слоем

Hub уже содержит основные домены Mango: `voice-ucaas`, `contact-center`,
`digital-channels`, `ai-automation`, `analytics`, `hardware`, `security`.
Отраслевые источники добавляют важное уточнение: CPaaS/API/platform у Cisco,
Twilio, Exolve и 8x8 является не технической сноской, а самостоятельным способом
упаковки коммуникационных возможностей.

Поэтому `platform` должен быть описан как **cross-domain layer** и
productizable family, когда он продаётся как API/CPaaS-продукт. Это не ломает
Hub-модель и не требует нового Product Layer.

### 3. AI становится cross-cutting layer, но не отменяет domain taxonomy

Cisco, Twilio, RingCentral, Amazon Connect, Genesys, Microsoft и 8x8 используют
AI в разных частях цепочки: virtual agents, agent assist, supervisor assist,
summaries, routing, quality management, analytics, journey orchestration.

Industry Taxonomy не должна заменять домены одним AI-доменом. Нужно:

- сохранить `ai-automation` для продаваемых AI/bot/automation продуктов;
- разрешить AI-assisted capabilities внутри `contact-center`,
  `digital-channels`, `analytics` и `voice-ucaas`;
- добавить в будущую Mango Taxonomy связь `ai_assisted: true/false` или
  аналогичный facet, если это понадобится для поиска и KB.

### 4. Contact center требует WEM/WFM/QM и journey orchestration как явных ветвей

Amazon Connect, Genesys, Cisco Webex Contact Center и RingCX показывают, что
современный CCaaS состоит не только из очередей и операторского рабочего места.
Минимальный отраслевой набор включает:

- omnichannel routing and queues;
- agent workspace;
- supervisor workspace;
- workforce management / workforce engagement management;
- quality management and recording;
- reporting and analytics;
- customer journey/conversation orchestration;
- integrations and data context.

В Hub это частично покрыто. Для будущей таксономии стоит явно связать
`workforce-management`, `quality-management`, `agent-assist`,
`conversation-orchestration` и `journey-orchestration`.

### 5. Local/Commercial признаки не должны попадать в Industry Taxonomy как домены

Hub правильно отделяет Product Layer от Commercial Layer. Следующие элементы
нужно оставить как Mango extensions, commercial/compliance facets или региональные
признаки, а не делать обязательными доменами industry reference taxonomy:

- `number-branding`, `carousel-numbers`, `voice-sms-broadcast` как локальные или
  Mango-specific capabilities;
- российский реестр ПО, procurement-коды, тарифы и pricing;
- отраслевые vertical labels;
- deal/commercial analytics, если они описывают продажи Mango, а не продуктовую
  функцию клиента.

### 6. Devices остаются edge/access domain

Cisco devices, Microsoft Teams Rooms/phones и UCaaS-поставщики подтверждают, что
устройства важны для классификации, но они не должны растворять core SaaS-domain.
`hardware` лучше держать как access/device edge domain, связанный с
`voice-ucaas`, meetings/rooms и contact-center workplace.

## Отличия и дополнения к Hub classification

| Область | Hub classification | Вывод ADR |
| --- | --- | --- |
| Уровни | `Domain -> Capability -> Feature -> Function` | Принять с терминологическим уточнением: leaf-level называется `Function`. |
| Домены | 7 пилотных доменов + cross-domain `platform` | Принять, но явно описать `platform` как cross-domain/productizable layer. |
| CPaaS/API | Есть в `platform` (`open-api`, `cpaas`) | Усилить как обязательную часть industry reference taxonomy, потому что Cisco, Twilio, Exolve и 8x8 дают сильный рыночный сигнал. |
| CCaaS | `contact-center`, routing, analytics, WFM/QM в разных ветках | Явно зафиксировать WEM/WFM/QM, agent/supervisor assist и journey/conversation orchestration как будущие capability candidates. |
| AI | `ai-automation` как домен | Сохранить домен, но дополнить cross-domain AI facet для функций внутри UCaaS/CCaaS/digital/analytics. |
| Analytics | Отдельный домен, включая продуктовую/маркетинговую аналитику | Оставить analytics, но разделять product/customer analytics и внутреннюю commercial/deal analytics Mango. |
| Vertical/industry | Backlog tag, не продуктовый класс | Подтвердить: vertical должен быть facet/tag, не уровень hierarchy. |
| Commercial/compliance | Отдельный слой | Подтвердить: pricing, procurement, registry и compliance не становятся продуктовой веткой taxonomy. |

## Альтернативы

### A. Принять Hub classification v3.0 без изменений

Плюсы:

- минимальный риск расхождения с уже reviewed Hub research;
- нет изменения модели и связанных контрактов;
- быстрое внедрение.

Минусы:

- CPaaS/API/platform остаётся менее заметным, чем в рыночной упаковке Cisco,
  Twilio, Exolve и 8x8;
- AI-assisted функции в CCaaS/UCaaS могут оказаться размазанными между доменами;
- WEM/WFM/QM и journey orchestration недостаточно явно выделены для enterprise
  contact-center рынка.

### B. Заменить Hub модель vendor-product taxonomy

Плюсы:

- названия ближе к витринам вендоров;
- проще сопоставлять с внешними сайтами.

Минусы:

- сильный vendor lock-in: Cisco/Webex, Twilio, Amazon Connect, RingCentral,
  Genesys, Microsoft и 8x8 режут рынок разными продуктовыми границами;
- Mango Office продукты придётся искусственно подгонять под чужую упаковку;
- vendor taxonomy смешивает продуктовые функции, коммерческую упаковку и
  marketing naming.

### C. Принять hybrid reference taxonomy

Суть:

- оставить Hub v3.0 как базовый research-backed skeleton;
- сохранить четыре уровня `Domain -> Capability -> Feature -> Function`;
- принять домены Hub как начальный доменный набор;
- явно описать `platform` как cross-domain/productizable layer;
- добавить source-backed candidates для WEM/WFM/QM, AI assist и
  conversation/journey orchestration;
- оставить commercial, compliance и vertical признаки как facets/tags outside
  product hierarchy.

## Решение

Выбираем **альтернативу C: hybrid reference taxonomy**.

Industry Taxonomy для будущих артефактов Mango должна использовать следующую
рамку:

1. **Hierarchy:** `Domain -> Capability -> Feature -> Function`.
2. **Initial domains:** `voice-ucaas`, `contact-center`, `digital-channels`,
   `ai-automation`, `analytics`, `hardware`, `security`.
3. **Cross-domain/platform layer:** `platform-integration`, `open-api`, `cpaas`,
   communications APIs, integrations, service-desk/vendor-support extensions.
4. **Cross-cutting facets:** AI-assisted, security/compliance, commercial,
   procurement, industry vertical, geography/region, **channel** (см. раздел
   «Голосовой канал vs текстовые каналы»).
5. **Candidate additions before standardization:** WEM/WFM/QM, agent assist,
   supervisor assist, conversation summaries, conversation orchestration, journey
   orchestration, verification/identity flows.
6. **Mango-specific extensions:** local numbering/branding, operator mobile app,
   Russian procurement/compliance fields and internal deal/product analytics must
   map to the reference taxonomy without changing the industry core.

Термин leaf-level обновляется с прежнего research-термина `Atomic Function` до
канонического `Function`. Это не меняет гранулярность уровня: `Function`
остаётся минимальной проверяемой единицей поведения, настройки, API-действия или
бизнес-правила. Уточнение нужно для симметрии с Mango Taxonomy после проверки
processed KB в issue #146.

Команда проверила это решение (issue #146, #148, #150). После закрытия
доисследования асимметрии каналов (issue #150) ADR переведён в `status: canonical`,
`version: 1.0`. ADR фиксирует каноническое **решение**, но по-прежнему не создаёт
сам стандарт Industry Taxonomy, Mango Taxonomy и KB reference data — это отдельные
follow-up артефакты. Финальное решение по merge остаётся за человеком
(AI_GOVERNANCE).

### Приоритет источников и согласованность с ADR-012

ADR-011 — источник истины для Industry reference layer (доменов, capability,
feature, function и cross-cutting facets). Чтобы исключить инверсию приоритета
между документами (issue #166), фиксируется единый, симметричный порядок:

> **ADR-011 имеет приоритет над ADR-012** для всего, что касается Industry
> reference layer и значений внутри `industry_ref`. Если ADR-012, Mango Taxonomy
> Standard или старый Mango crosswalk противоречат ADR-011 по slug'у домена,
> capability, feature, function или по форме `industry_ref` — применяется
> ADR-011 и каноничный реестр `kb/industry-taxonomy/registry.json`.

Этот порядок дословно совпадает с §1.3 обоих стандартов
([`industry-taxonomy-standard.md`](../industry-taxonomy-standard.md) и
[`mango-taxonomy-standard.md`](../mango-taxonomy-standard.md)) и с §«Приоритет
источников и синхронизация с ADR-011» в [`ADR-012`](ADR-012-mango-taxonomy.md).
ADR-012 остаётся источником истины только для Mango-specific слоя
`Product -> Service -> Module -> Function` там, где он не конфликтует с ADR-011.

## Голосовой канал vs текстовые каналы (доисследование, issue #150)

**Проблема.** В модели текстовые каналы — first-class домен `digital-channels`
(`omnichannel-messaging`, `website-chat`, `sms-messaging`), а голосовой канал
неявно «зашит» в инфраструктурные capability `voice-ucaas` (`cloud-pbx`,
`ivr-voice-menu`, `call-routing`). Отдельной capability «голосовой канал»,
симметричной текстовым, нет. Полный анализ, отраслевые свидетельства и trade-offs:
[docs/analysis/voice-digital-channels-comparison.md](../../docs/analysis/voice-digital-channels-comparison.md).

**Две разные асимметрии.** Постановка смешивает два слоя:

1. *Инфраструктурная* (Infrastructure / Resource): голос требует выделенного
   телеком-ресурса (PSTN, SIP, номерная ёмкость, кодеки); текст идёт по generic IP
   и API сторонних платформ. → **Асимметрия обоснована.**
2. *Канальная* (Channel): голосовой канал и текстовые каналы — равноправные среды
   обращения, но голосовой не назван. → **Артефакт модели.**

**Отраслевые свидетельства (проверка 2026-06-21).**

- CPaaS (Twilio, МТС Exolve) разделяют инфраструктуру (Phone Numbers, SIP,
  Numbering API) и каналы (Programmable Voice / Voice API ↔ Programmable Messaging /
  SMS API); голосовой канал **строится поверх** инфраструктуры.
- UCaaS (RingCentral RingEX, Cisco Webex) упаковывают инфраструктуру + голос в
  «Phone»/«Calling», текст — отдельно (= текущая `voice-ucaas` vs `digital-channels`).
- CCaaS (Amazon Connect, Genesys) ведут голос как **канал** рядом с chat/email;
  телефония — сменная инфра (BYOC).
- TM Forum SID / TMF681: канал = измерение взаимодействия (email, SMS, push),
  отделённое от Resource-слоя.

Единого ответа «голос = отдельный домен» в отрасли нет; классификация зависит от
слоя. Регуляторика РФ (СОРМ, 126-ФЗ, 152-ФЗ) применима и к голосу, и к тексту,
поэтому **не** является дискриминатором — дискриминатор — наличие выделенного
телеком-ресурса.

**Решение: уточнённая (обоснованная) асимметрия.** Домены не делим (число доменов
не меняется); затрагиваются только `voice-ucaas` и `digital-channels`.

1. **Инфраструктурную асимметрию сохранить.** `voice-ucaas` — единый домен;
   обоснование фактическое (выделенный телеком-ресурс у голоса есть, у текста нет).
   Полная симметрия (split `voice-infrastructure` + `voice-channels`) отклонена:
   по симметрии потребовался бы и `digital-infrastructure`, который у текста пуст,
   → split внутренне противоречив и создаёт churn в других доменах (запрещено
   issue #150).
2. **Канальный артефакт устранить.** Ввести внутри `voice-ucaas` first-class
   capability **`voice-channel` (Голосовой канал)**, симметричную текстовым
   capability `digital-channels`. `voice-ucaas` явно описывается как
   **«телеком-инфраструктура + голосовой канал»** (двойная природа — как
   `ai-automation` = домен + AI-facet, `platform` = cross-domain layer).
3. **Cross-cutting facet `channel`.** Размерности: `channel_kind`
   (`voice` | `text` | `video`), `synchronicity` (`sync` | `async`), `direction`
   (`inbound` | `outbound` | `broadcast`). Делает каналы единообразно
   запрашиваемыми поверх доменов (TM Forum-совместимо); домены не меняет.
4. **Оркестрацию не трогать.** `contact-center` уже маршрутизирует все каналы
   (`interaction-routing` по `channel_type`, `channel-blending`) — симметрия на
   этом слое уже есть.

## Использование в маппинге

Industry Taxonomy используется как reference layer для Mango Taxonomy и будущих
KB-реестров. Связи с ним должны быть строгими ссылками на taxonomy nodes, а
не свободными тегами. Свободные labels допустимы только в фасетах вроде
`industry`, `segment`, `use_case` или `region`; они не заменяют
`industry_ref`.

Минимальная структура ссылки:

```yaml
industry_ref:
  domain: contact-center
  capability: omnichannel-contact-center
  feature: omnichannel-desktop
  function: unified-agent-desktop
alignment_type: primary
```

> **Reference integrity.** Slug'и `domain -> capability -> feature -> function`
> в примерах ADR-011 разрешаются в каноническом реестре
> [`kb/industry-taxonomy/registry.json`](../../kb/industry-taxonomy/registry.json).
> Цепочка выше — `contact-center -> omnichannel-contact-center ->
> omnichannel-desktop -> unified-agent-desktop` — существует как канонический
> путь. ADR-011 не вводит slug'и в обход реестра.

Правила применения:

- `industry_ref.domain` обязателен для любой связи и должен ссылаться на
  canonical Domain из ADR-011 или Industry Taxonomy registry
  (`kb/industry-taxonomy/registry.json`).
- `industry_ref.capability`, `industry_ref.feature` и `industry_ref.function`
  добавляются по мере глубины Mango entity: Product может ссылаться на несколько Domain/Capability,
  Service — на Capability, Module — на Feature, Mango `Function` — на Function.
- `alignment_type` принимает только `primary`, `secondary` или `supporting`.
  `primary` фиксирует главный отраслевой смысл; `secondary` — важную
  дополнительную связь; `supporting` — platform, hardware, security или
  operational support связь.
- Каждая связь должна иметь evidence в ADR, processed KB или future registry.
  Если canonical slug отсутствует, связь остаётся открытым вопросом, а не
  добавляется как произвольный tag.
- Many-to-many является нормой: один Mango Product может покрывать несколько
  Domain/Capability, а один Industry Capability может поддерживаться несколькими
  Mango Products, Services или Modules.

Эти правила нужны, чтобы Product-to-Industry mapping был проверяемым,
диффируемым и пригодным для генерации требований, а не зависел от локальных
синонимов в документации.

### Пример: голосовой канал с facet `channel`

Голосовой канал размечается симметрично текстовым: та же форма `industry_ref` +
cross-cutting facet `channel`. Различается только `channel_kind`.

Входящий голосовой звонок (например, `mango-virtual-pbx`):

```yaml
industry_ref:
  domain: voice-ucaas
  capability: voice-channel        # first-class голосовой канал
  feature: inbound-voice-call
alignment_type: primary
facets:
  channel:
    channel_kind: voice
    synchronicity: sync
    direction: inbound
```

Текстовый канал — для контраста (например, `mango-text-communications`):

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

Чистая телеком-инфраструктура (например, `sip-trunk`) каналом **не** является и
facet `channel` не получает:

```yaml
industry_ref:
  domain: voice-ucaas
  capability: sip-connectivity
alignment_type: supporting
```

Дополнительные примеры и влияние на crosswalk ADR-012:
[docs/analysis/voice-digital-channels-comparison.md](../../docs/analysis/voice-digital-channels-comparison.md), §7.

## Rationale

Hybrid reference taxonomy лучше других вариантов, потому что:

- сохраняет уже reviewed Hub research и совместимость с
  [product-classification-contract.md](../product-classification-contract.md);
- не смешивает taxonomy с коммерческой упаковкой и procurement/compliance;
- учитывает текущую рыночную упаковку CPaaS/API/platform;
- поддерживает разные способы продажи Mango Office без vendor lock-in;
- оставляет пространство для будущих source-backed corrections вместо
  преждевременного финального стандарта.

## Consequences

Положительные:

- Mango Taxonomy сможет маппить продукты на отраслевой reference layer, а не
  на случайные vendor labels.
- KB-классификация сможет хранить Product Layer отдельно от pricing,
  procurement, compliance и vertical tags.
- Будущий стандарт сможет ссылаться на проверенные источники и на этот ADR как
  на зафиксированное решение.
- CPaaS/API/platform и AI-assisted features не потеряются при классификации.
- Голосовой и текстовые каналы маппятся симметрично через facet `channel`;
  голосовой канал стал first-class capability, а инфраструктурная асимметрия
  `voice-ucaas` обоснована фактами, а не неявна (issue #150).

Отрицательные / технический долг:

- Перед стандартом нужно описать точные canonical slugs и правила alias mapping,
  включая `voice-channel`, feature-узлы голосового канала и значения facet
  `channel` (`channel_kind`/`synchronicity`/`direction`).
- Фактическое добавление facet `channel` в crosswalk ADR-012 — отдельный
  follow-up PR (в этом issue ADR-012 не меняется).
- Нужно решить, какие Mango-specific capabilities входят в Industry Taxonomy, а
  какие остаются Mango Taxonomy extensions.
- Нужно отдельно проверить русскоязычные и российские отраслевые источники, если
  команда захочет local-first taxonomy.
- `standards/decisions/` сейчас используется по требованию issue #139; если ADR
  catalog будет централизован только в `docs/adr/`, нужен отдельный governance PR
  на перенос или алиас, а не скрытое изменение в этом issue.

## Related docs

- Issue #139:
  <https://github.com/G-Ivan-A/mango_ba_prompts/issues/139>
- PR #140:
  <https://github.com/G-Ivan-A/mango_ba_prompts/pull/140>
- Hub classification research:
  <https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/mango/classification.md>
- Hub dependency registry:
  <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/hub-research-dependencies.md>
- Product classification contract:
  <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/product-classification-contract.md>
- Industry standards ADR:
  <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/adr/008-industry-standards-standard.md>
- Future follow-ups (not created by this ADR): `industry-taxonomy-standard.md`,
  Mango Taxonomy ADR/standard, KB reference taxonomy data.
