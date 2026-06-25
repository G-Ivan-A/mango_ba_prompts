---
status: draft
version: 1.0
updated: 2026-06-21
ai-generated: true
type: analysis
scope: industry-taxonomy-voice-digital-channels
issue: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/150"
related_artifacts:
  - "standards/decisions/ADR-011-industry-taxonomy.md"
  - "standards/decisions/ADR-012-mango-taxonomy.md"
hub_research:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/mango/classification.md"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/mango/classification-tz.md"
---

# Сравнительный анализ: голосовые vs текстовые каналы в Industry Taxonomy (ADR-011)

> **Назначение.** Доисследование асимметрии классификации голосовых и текстовых
> каналов, отложенное при согласовании ADR-011 (issue #150). Документ —
> аналитика спока (`docs/analysis/`), не research и не стандарт. Решение фиксируется
> в ADR-011; здесь — анализ, отраслевые свидетельства и trade-offs, на которых
> решение основано.

## 1. Постановка проблемы

ADR-011 фиксирует модель `Domain → Capability → Feature → Function` и доменный
набор `voice-ucaas`, `contact-center`, `digital-channels`, `ai-automation`,
`analytics`, `hardware`, `security` + cross-domain `platform`.

Текущее размещение каналов (по ADR-011, ADR-012 и Hub `classification.md` v3.0):

| Тип канала | Где смоделирован | Уровень | First-class capability? |
| --- | --- | --- | --- |
| Текстовые (chat, мессенджеры, соцсети, email, SMS) | `digital-channels` | **канальный** (channel) | **Да** — `omnichannel-messaging`, `website-chat`, `sms-messaging` |
| Голосовой (телефонный звонок) | `voice-ucaas` | **инфраструктурный** (infrastructure) | **Нет** — растворён в `cloud-pbx`, `call-routing`, `ivr-voice-menu` |

`voice-ucaas` смешивает два разных слоя: телеком-инфраструктуру
(`sip-connectivity`, `number-management`) и коммуникационные возможности
(`cloud-pbx`, `unified-communications`, `ivr-voice-menu`). Отдельной capability
«голосовой канал», симметричной текстовым каналам в `digital-channels`, нет.

**Вопрос founder'а (диалог согласования ADR-011, строки 686–853):** контакт-центр
оркеструет и текст, и голос; UCaaS — это про номера и маршрутизацию, а не про
коммуникацию. Почему тогда голосовое обращение не выделено как канал, а текстовое —
выделено?

## 2. Аналитическая рамка: три слоя

Ключ к разрешению — разделить **один** вопрос «почему асимметрия?» на **три**
независимых слоя. Канал «голос» и каналы «текст» сопоставимы только на одном из них.

| Слой | Что описывает | Голос | Текст | Симметрия? |
| --- | --- | --- | --- | --- |
| **Infrastructure / Resource** | Транспорт, доступность канала | PSTN, SIP-транки, номерная ёмкость, кодеки, carrier-grade маршрутизация | Generic IP/HTTPS + API сторонних платформ (WhatsApp, Telegram, SMS-агрегатор) | **Нет** — у голоса есть выделенный телеком-ресурс, у текста нет |
| **Channel / Interaction** | Среда диалога с клиентом | Голосовой звонок | Чат, мессенджер, email, SMS | **Да** — это равноправные каналы обращения |
| **Orchestration** | Маршрутизация, очереди, рабочее место | `channel_type: voice` | `channel_type: chat/email/...` | **Да** — уже симметрично в `contact-center` |

Вывод рамки: в постановке проблемы **смешаны две разные асимметрии**:

1. **Инфраструктурная асимметрия** (Infrastructure layer) — РЕАЛЬНА и
   ОБОСНОВАНА. Голос требует выделенного телеком-ресурса; текст — нет.
2. **Канальная асимметрия наименования** (Channel layer) — АРТЕФАКТ модели.
   Текстовый канал назван (`digital-channels`), голосовой канал не назван
   (неявно «зашит» в инфраструктурные capability `voice-ucaas`).

Их нужно разрешать по-разному: №1 сохранить, №2 устранить.

## 3. Отраслевые свидетельства

Проверка выполнена 2026-06-21 по официальным источникам вендоров и TM Forum.
Все три класса вендоров и отраслевой стандарт дают согласованный сигнал.

### 3.1 Сводная таблица

| Класс | Вендор | Инфраструктура (resource) | Голосовой канал | Текстовый канал | Вывод |
| --- | --- | --- | --- | --- | --- |
| **CPaaS** | Twilio | Phone Numbers, Elastic SIP Trunking, Super Network | **Programmable Voice** | **Programmable Messaging** | 3-слойное разделение; voice-канал **строится поверх** инфраструктуры |
| **CPaaS** | МТС Exolve (RU) | Numbering API, виртуальные номера | **Voice API** | **SMS API / Messaging API** | То же разделение у российского вендора |
| **UCaaS** | RingCentral RingEX | (внутри «Phone») | «**Phone**» (calling) | «**Message**» (team chat, SMS) | Инфраструктура + голос-канал упакованы в «Phone»; текст отдельно |
| **UCaaS** | Cisco Webex | (внутри «Calling») | «**Calling**» | «**Messaging**» | То же: calling = infra+канал; messaging отдельно |
| **CCaaS** | Amazon Connect | Telephony / BYOC (сменный carrier) | **voice channel** | chat, email, SMS, tasks | Голос — **канал** рядом с текстом; телефония — сменная инфра |
| **CCaaS** | Genesys Cloud | (BYOC / SIP) | phone как **media channel** | chat, email, messaging, social | Голос — медиа-канал в одном ряду с текстом |
| **Standard** | TM Forum SID / TMF681 | Resource layer (network/telephony) | — (interaction channel) | email, short message, push | Канал = **измерение взаимодействия**, отделён от Resource-слоя |

### 3.2 Что показывает каждый класс

**CPaaS (Twilio, МТС Exolve) — самое чистое разделение.** Twilio разносит на
отдельные продукты телеком-инфраструктуру (Phone Numbers, Elastic SIP Trunking,
Super Network) и каналы (Programmable Voice, Programmable Messaging). Critically:
Programmable Voice **строится поверх** инфраструктуры («builds on Twilio's
underlying infrastructure») — то есть инфраструктура и канал это разные слои, а
не один. МТС Exolve воспроизводит ту же декомпозицию по-русски: Numbering API
(инфраструктура) ≠ Voice API (голосовой канал) ≠ SMS/Messaging API (текстовый
канал). → **Голосовой канал и текстовый канал — siblings; инфраструктура — отдельный слой.**

**UCaaS (RingCentral, Cisco) — прагматичная упаковка.** RingEX = «Message, Video,
Phone»; Webex = «calling, meetings, messaging». «Phone»/«Calling» объединяет
телеком-инфраструктуру и голосовой канал в один продукт, а текст («Message»/
«Messaging») вынесен отдельным столпом. → **Это ровно текущая модель `voice-ucaas`
(infra + voice) vs `digital-channels` (text). UCaaS подтверждает практичность
объединения, но не декомпозирует голос на infra/channel.**

**CCaaS (Amazon Connect, Genesys) — канальная симметрия.** Amazon Connect ведёт
voice как один из каналов (voice, chat, email, SMS, tasks) в едином UI; телефония
(номера/DID/toll-free) — сменная инфраструктура (BYOC: можно заменить carrier, не
меняя контакт-центр). Genesys: «conversation … over at least one media channel
such as chat, phone, or email» — голос (phone) равноправен chat/email. →
**На оркестрационном слое голос уже трактуется как канал, симметрично тексту.**

**TM Forum (отраслевой стандарт).** SID — референсная информационная модель и
словарь ODA/Open API. TMF681 Communication Management: сообщение «can reach the
customer in different interaction channels, including: email, short message, mobile
app notification (push)» — канал моделируется как **измерение взаимодействия**
(interaction channel), отдельно от сетевых/телефонных ресурсов Resource-слоя. →
**Стандарт поддерживает трактовку «канал = cross-cutting измерение», а
телефония = Resource-слой.**

### 3.3 Главный вывод свидетельств

- Единого отраслевого ответа «голос = отдельный домен» **нет**: классификация
  зависит от слоя и от способа упаковки (CPaaS режет тоньше, UCaaS — грубее).
- На **инфраструктурном** слое голос объективно отличается от текста выделенным
  телеком-ресурсом → асимметрия №1 обоснована.
- На **канальном** слое голос и текст у всех вендоров — равноправные сущности
  (Programmable Voice ↔ Programmable Messaging; voice channel ↔ chat) →
  асимметрия №2 (ненаименованный голосовой канал) — артефакт.

## 4. Российский контекст: регуляторика не является дискриминатором

Founder уточнил (диалог, строки 825–853): в РФ текст **тоже** требует
инфраструктуры и регулируется государством (СОРМ, реестры), а голосовой канал
**не** требует контакт-центра (например, Asterisk PBX).

| Признак | Голос | Текст (в РФ) |
| --- | --- | --- |
| СОРМ / lawful interception | Да (126-ФЗ) | Да (для операторских сервисов) |
| 152-ФЗ (перс. данные) | Да | Да |
| Выделенный телеком-ресурс (номер, SIP, кодеки) | **Да** | **Нет** (generic IP + API платформ) |

Следствие: **регуляторика применима к обоим** и потому **не** объясняет
асимметрию. Дискриминатор — не «регулируется/не регулируется», а **«есть ли
выделенный телеком-ресурс»**. СОРМ/152-ФЗ — это `security/compliance` facet (по
ADR-011), а не признак канального слоя. Это сужает обоснование асимметрии №1
строго до инфраструктурного ресурса и снимает ложный аргумент «голос особый,
потому что регулируется».

## 5. Trade-offs: симметрия vs практичность

### Гипотеза 1 — асимметрию оставить как есть

| + | − |
| --- | --- |
| Ноль изменений, ноль churn в ADR-011/012 | Логический артефакт founder'а не устранён |
| Совпадает с упаковкой UCaaS (`voice-ucaas` = «Phone») | Голосовой канал остаётся «невидимым» для запросов по каналам |
| | Нельзя единообразно фильтровать «все каналы» (voice не размечен) |

### Гипотеза 2 — полная симметрия (split на 4 домена)

`voice-infrastructure` + `voice-channels` + `digital-channels` + `contact-center`.

| + | − |
| --- | --- |
| Концептуально «чисто», параллельно тексту | **Внутренне противоречива** (см. ниже) |
| Совпадает с декомпозицией CPaaS | Меняет число доменов (8 → 9/10) и **другие домены** — запрещено issue |
| | Принудительный ремаппинг ADR-012 (`mango-virtual-pbx`, `sip-trunk`, `mango-talker`) |
| | Противоречит рыночной упаковке UCaaS |

**Почему Гипотеза 2 внутренне противоречива.** Настоящая симметрия требует
параллелизма по **обоим** слоям. Если выделять `voice-infrastructure` +
`voice-channels`, то по симметрии нужен и `digital-infrastructure` +
`digital-channels`. Но у текста **нет выделенной телеком-инфраструктуры** —
текст идёт по generic IP и API сторонних платформ. Домен `digital-infrastructure`
оказался бы **пустым/искусственным**. Значит «симметричный» split на деле создаёт
**новую асимметрию** (infra-домен у голоса есть, у текста — нет) и противоречит
сам себе. Это решающий аргумент против наивного split.

## 6. Решение: уточнённая (обоснованная) асимметрия

Гибрид, разрешающий обе асимметрии по-разному. **Домены не делим, число доменов
не меняем; затрагиваются только `voice-ucaas` и `digital-channels` (разрешено
issue).**

1. **Инфраструктурную асимметрию сохранить.** `voice-ucaas` остаётся единым
   доменом: голос связан с выделенным телеком-ресурсом (PSTN/SIP/номера/кодеки),
   текст — нет. Обоснование — фактическое (см. §3, §4), а не «по соглашению».
2. **Канальный артефакт устранить.** Внутри `voice-ucaas` ввести first-class
   capability **`voice-channel` (Голосовой канал)**, симметричную текстовым
   capability в `digital-channels`. Голосовой канал становится **названным**, а не
   «зашитым» в `cloud-pbx`/`ivr-voice-menu`. `voice-ucaas` явно документируется как
   **«инфраструктурный слой + голосовой канал»** (двойная природа, как `ai-automation`
   = домен + AI-facet и `platform` = cross-domain layer в ADR-011).
3. **Добавить cross-cutting facet `channel`.** Размерности: `channel_kind`
   (`voice` | `text` | `video`), `synchronicity` (`sync` | `async`), `direction`
   (`inbound` | `outbound` | `broadcast`). Facet делает каналы единообразно
   запрашиваемыми поверх доменов (TM Forum-совместимо: канал = измерение
   взаимодействия). Это не меняет домены — facet ортогонален иерархии.
4. **Оркестрацию не трогать.** `contact-center` уже маршрутизирует все каналы по
   `channel_type` (`interaction-routing`, `channel-blending`) — симметрия на этом
   слое уже есть. Только зафиксировать это документально.

**Соответствие ограничениям issue:**

| Ограничение | Выполнение |
| --- | --- |
| НЕ менять другие домены | ✅ Меняются только `voice-ucaas` (capability) и `digital-channels` (уточнение); `channel` — новый facet, не домен |
| НЕ отменять согласования ADR-011 | ✅ Только дополнение: +1 capability, +1 facet, +документация |
| Показать trade-offs до решения | ✅ §5 |
| Решение обосновано фактами | ✅ §3 (вендоры + стандарт), §4 (RU-контекст) |
| Примеры маппинга для голоса | ✅ §7 |

## 7. Влияние на маппинг Mango и примеры голосовых каналов

`industry_ref` (по ADR-011/012) расширяется опциональным facet `channel`.
Иерархическая ссылка (`domain/capability/feature/function`) сохраняется без слома.

### 7.1 Пример: входящий голосовой звонок в ВАТС (`mango-virtual-pbx`)

**Было** (голосовой канал неявен — только инфраструктура):

```yaml
industry_ref:
  domain: voice-ucaas
  capability: cloud-pbx
  feature: call-routing-rules
alignment_type: primary
```

**Стало** (голосовой канал назван + facet):

```yaml
industry_ref:
  domain: voice-ucaas
  capability: voice-channel        # новый first-class канал
  feature: inbound-voice-call
alignment_type: primary
facets:
  channel:
    channel_kind: voice
    synchronicity: sync
    direction: inbound
```

### 7.2 Пример: текстовый канал (`mango-text-communications`) — для контраста

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

→ Голос и текст теперь **симметричны на канальном слое**: одинаковая форма
`industry_ref` + один и тот же facet `channel`, различается только значение
`channel_kind`.

### 7.3 Пример: исходящий обзвон в контакт-центре (`mango-contact-center`)

```yaml
industry_ref:
  domain: contact-center
  capability: outbound-calling
  feature: campaign-management
alignment_type: primary
facets:
  channel:
    channel_kind: voice
    synchronicity: sync
    direction: outbound
```

### 7.4 Сводка влияния на существующие маппинги ADR-012

| Mango entity | Текущий `industry_ref` (ADR-012) | Влияние |
| --- | --- | --- |
| `mango-virtual-pbx` | `voice-ucaas` / `cloud-pbx`, `sip-connectivity`, `number-management`, `ivr-voice-menu`, `call-recording` | +`voice-channel` для голосового обращения; инфраструктурные capability без изменений |
| `mango-talker` | `voice-ucaas` / `unified-communications`; secondary `digital-channels` | Голосовая часть размечается facet `channel_kind: voice`, чат — `text` |
| `sip-trunk` | `voice-ucaas` / `sip-connectivity` | Без изменений (чистая инфраструктура, не канал) |
| `mango-text-communications` | `digital-channels` / `omnichannel-messaging`, `website-chat`, `sms-messaging` | +facet `channel_kind: text` (домен не меняется) |
| `mango-contact-center` | `contact-center` / `omnichannel-contact-center`, `outbound-calling`, … | Каналы размечаются facet; структура домена не меняется |

**Важно:** ADR-012 в этом PR **не изменяется** (issue запрещает менять другие
домены). Таблица показывает, как существующие маппинги читаются под уточнённой
моделью; фактическое добавление facet в ADR-012 — отдельный follow-up.

## 8. Что меняется в ADR-011

- Frontmatter: `status: proposed → canonical`, `version: 0.3 → 1.0`, `updated`,
  ссылка на этот документ, ссылка на issue #150.
- Новая секция «Голосовой канал vs текстовые каналы (issue #150)» с решением §6.
- Cross-cutting facets: добавить `channel` (`channel_kind`/`synchronicity`/`direction`).
- `voice-ucaas`: документировать двойную природу (infra + voice-channel) и
  capability `voice-channel`.
- Секция маппинга: добавить пример голосового канала с facet `channel`.

## 9. Открытые вопросы и follow-ups

1. **Hub `research/mango/classification-tz.md`.** DoD issue #150 требует
   задокументировать результаты в Hub. Правило спока (CONTRIBUTING.md: «AI agents
   не создают `research/` в споке») и ограничение «push только в ветку
   issue-150-…» запрещают делать это из данного PR. Поэтому Hub-обновление —
   **отдельный follow-up PR в `hybrid-Intelligence-lab`**; готовый материал —
   §3–§6 этого документа. Зафиксировано как обход scope в описании PR.
2. **ADR-012 facet `channel`.** Фактическое добавление facet в crosswalk
   ADR-012 — отдельный PR (здесь только показано влияние, §7.4).
3. **Канонические slug'и.** Точные имена `voice-channel`, feature-узлов
   (`inbound-voice-call`, `outbound-voice-call`) и значений facet утверждаются
   при создании Industry Taxonomy registry (follow-up ADR-011).

## Источники

- Twilio — Elastic SIP Trunking: <https://www.twilio.com/docs/sip-trunking>;
  SIP Trunking: <https://www.twilio.com/en-us/sip-trunking>;
  Programmable Voice / Messaging: <https://www.twilio.com/en-us>
- МТС Exolve — Voice API: <https://exolve.ru/products/voice-api/>;
  SMS API: <https://exolve.ru/products/sms-api/>;
  Numbering API: <https://exolve.ru/products/numbering-api/>;
  Голосовые SMS: <https://exolve.ru/products/voice-sms/>
- RingCentral RingEX: <https://www.ringcentral.com/ringex.html>
- Cisco Webex: <https://www.webex.com/>
- Amazon Connect — voice channel / telephony:
  <https://docs.aws.amazon.com/connect/latest/adminguide/concepts-telephony.html>;
  features: <https://aws.amazon.com/connect/features/>
- Genesys Cloud — architecture:
  <https://www.genesys.com/capabilities/cloud-architecture>;
  conversations: <https://developer.genesys.cloud/routing/conversations/>
- TM Forum — Information Framework (SID):
  <https://www.tmforum.org/open-digital-architecture/information-framework-sid/>;
  TMF681 Communication Management:
  <https://github.com/tmforum-apis/TMF681_Communication>
- Hub research: `hybrid-Intelligence-lab/research/mango/classification.md` (v3.0);
  `classification-tz.md` (v1.0)
- ADR-011: `standards/decisions/ADR-011-industry-taxonomy.md`;
  ADR-012: `standards/decisions/ADR-012-mango-taxonomy.md`
- Диалог согласования ADR-011 (вложение issue #150), строки 686–853.
