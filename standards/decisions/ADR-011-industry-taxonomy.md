---
status: proposed
version: 0.2
updated: 2026-06-20
ai-generated: true
type: adr
scope: industry-taxonomy
issue: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/139"
validated_by:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/146"
hub_research: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/mango/classification.md"
hub_research_sha: "73e94c6e69995ccf9e746c19d9c18359971285f2"
related_prs:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/pull/140"
related_artifacts:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/product-classification-contract.md"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/hub-research-dependencies.md"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/adr/008-industry-standards-standard.md"
---

# ADR-011: Industry Taxonomy для классификации продуктов Mango Office

> **Статус:** Proposed · **Дата:** 2026-06-20 · **Issue:**
> <https://github.com/G-Ivan-A/mango_ba_prompts/issues/139> · **Hub research:**
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
   procurement, industry vertical, geography/region.
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

Этот ADR не утверждает финальный стандарт и не создаёт KB. Он фиксирует решение,
которое должна проверить команда перед отдельными PR на стандарт, Mango Taxonomy
и KB reference data.

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

Отрицательные / технический долг:

- Перед стандартом нужно описать точные canonical slugs и правила alias mapping.
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
