---
status: draft
version: 0.1
updated: 2026-06-25
ai-generated: true
type: analysis
scope: research
operating_mode: creative
issue: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/233"
related_artifacts:
  - "kb/practices/source-backed-analysis.md"
  - "docs/analysis/2026-06-21-industry-inventory.md"
  - "standards/industry-standards-standard.md"
---

# Эмпирическая база: BA/Requirements-практики телеком-вендоров и операторов

> **Назначение.** Эмпирический вход для issue #233 (Этап 2 — телеком-компании,
> Этап 3 — фреймворки). Источниковая дисциплина — по
> [`kb/practices/source-backed-analysis.md`](../../kb/practices/source-backed-analysis.md)
> (C1-C4): каждое фактическое утверждение сопровождается URL и уровнем
> доказательности. Это **research**, не стандарт; решений не принимает.
>
> **Дата сбора:** 2026-06-25. Сбор выполнен через WebSearch/WebFetch + браузерные
> проверки PDF (TM Forum хостит отчёты о сертификации как открытые PDF).

## 0. Легенда уровней доказательности

| Метка | Значение |
| --- | --- |
| **[CONFIRMED]** | прямой публичный источник (приведён URL, проверен на существование) |
| **[INFERRED]** | разумный вывод из вакансий / косвенных свидетельств (приведён URL) |
| **[HYPOTHESIS]** | правдоподобно, но не подтверждено (указана причина) |
| **NOT FOUND** | источник не найден — утверждение НЕ выпускается как факт |

**Метод-оговорка (честно).** Домен `tmforum.org`, большинство официальных доменов
операторов (att.com, verizon.com, gsma.com), ATS-страницы вакансий (Greenhouse,
Workday, JS-SPA jobs.amdocs.com) и SEC EDGAR HTML систематически отдают HTTP 403
ботам (Cloudflare). Там, где первичная страница заблокирована, факт подтверждался
(а) сниппетами поисковой выдачи, (б) дочерним агентом, забравшим реальные PDF
TM Forum через browser-UA (HTTP 200), (в) корректно открывавшимися зеркалами
(inform.tmforum.org, newsroom.orange.com, developer.*). Конверсии валют в USD —
собственная арифметика по датированным курсам, приблизительны.

---

## ЧАСТЬ A — ТЕЛЕКОМ-ВЕНДОРЫ (ПО, BSS/OSS/CPaaS)

### A1. Netcracker Technology (BSS/OSS) — дочерняя компания NEC

- **Выручка: NOT CONFIRMED.** NEC **не** выделяет Netcracker отдельным
  сегментом. Сторонние агрегаторы расходятся катастрофически (Growjo/RocketReach
  дают «$1.0-5.0B», в одном срезе «$2.7B»), поэтому как факт не используются.
  Порядок величины **$1B+** — [INFERRED] из позиционирования (конкуренция с
  Amdocs/Ericsson/Huawei/Oracle) и ~11-12 тыс. сотрудников.
  Контекст NEC [CONFIRMED]: <https://www.nec.com/en/global/ir/pdf/library/250428/250428_01.pdf>
  - **Band: «leader (much larger)» [INFERRED]** — это вывод из размера, НЕ из
    проверенной цифры выручки. Это самая слабая точка данных в исследовании.
- **TM Forum [CONFIRMED]:** Platinum Badge for Open API + ODA Compliance «Ready
  for ODA» **Level 6**. Цитата: *«…the TM Forum Platinum Badge for Open API and
  ODA Compliance at Ready for ODA Level 6.»*
  <https://www.netcracker.com/portfolio/products/netcracker-api-management-and-integration.html>
  Стандарты на той же странице: TM Forum, MEF, ETSI, 3GPP, CAMARA, O-RAN.
  Конкретный конформанс-отчёт **TMF620 Product Catalog Management API v4.1.0**
  (CloudBSS Rel. 2023.2): <https://s3.us-east-1.amazonaws.com/tmf-sfdc-public/Conformance/CON-02033/Netcracker-Certification%20Report-TMF620%20API-Sep2023.pdf>
- **Артефакты [INFERRED из вакансий]:** Use Cases + Information Models +
  Operation Process Specifications + Functional Requirements + Solution/Design
  Documents; data-mapping/transformation rules (миграционные роли); TMF Open API
  specs. Классические **BRD/FRD/SRS как термины — NOT FOUND**; Netcracker
  использует TM-Forum-окрашенный словарь. Подтверждённая вакансия:
  <https://builtin.com/job/migration-business-data-analyst/7857458>
- **Фреймворки:** TM Forum Frameworx/ODA/Open API [CONFIRMED]; **BABOK
  principles**, Agile (SCRUM) + Waterfall, 3GPP/ETSI/TM Forum — [INFERRED] из той
  же Built-In-вакансии (*«Familiarity with BABOK principles…»*, *«Agile (SCRUM)…
  and Waterfall delivery models»*). MEF/CAMARA/O-RAN [CONFIRMED]. SAFe, IREB,
  PMI-PBA, ISO 29148 — **NOT FOUND**.

| Поле | Значение |
| --- | --- |
| Выручка | NOT CONFIRMED (NEC не выделяет). Порядок $1B+ [INFERRED] |
| Band | leader (much larger) [INFERRED, не из цифры] |
| Артефакты | Use Cases, Information Models, Operation Process Specs, Functional Requirements, Solution Design, TMF Open API specs (BRD/FRD/SRS — не используются как термины) |
| Фреймворки | TM Forum ODA/Open API (Platinum + Ready-for-ODA L6); BABOK/Agile/Waterfall; 3GPP/ETSI/MEF/CAMARA/O-RAN |
| Источники | netcracker.com API-Management page · TMF620 conformance PDF · builtin.com BA posting · nec.com IR PDF |

### A2. Amdocs (BSS/OSS) — NASDAQ: DOX

- **Выручка FY2024 (до 30.09.2024): $5.00 млрд** (~$5,004,989K), +2.4% YoY.
  [CONFIRMED] *«Record Fiscal 2024 Revenue of $5.00 Billion…»*
  <https://www.amdocs.com/news-press/amdocs-limited-reports-fourth-quarter-and-full-fiscal-2024-results>
  Подтверждение (20-F): <https://www.amdocs.com/news-press/amdocs-limited-files-fiscal-2024-annual-report>
  - **Band: leader (much larger)** [CONFIRMED] — ~8-12× верхней границы $400-600M.
- **TM Forum [CONFIRMED]:** член и Diamond Sponsor DTW; активный контрибьютор ODA.
  Блог Amdocs: «67 Open APIs», «460+ conformance-certified implementations»,
  Async APIs, OAS 3.0. <https://www.amdocs.com/insights/blog/tm-forum-dtw-recap>
  Продукты с ODA Component Conformance (Service Orchestration, Catalog, AI & Data
  Platform, Network Inventory, Digital Identity): директория tmforum.org (403 при
  фетче, точные числа [INFERRED]). White paper «The case for API standardization»:
  <https://www.amdocs.com/sites/default/files/2023-08/The-case-for-API-standardization-white-paper.pdf>
- **Артефакты [CONFIRMED через зеркала вакансий]:** business documents, technical
  requirements, high-level solution designs, solution-related specifications,
  detailed test plans. *«…assembling business documents and technical
  requirements… Design holistic… high-level solutions… Prepare solution-related
  documents and specifications… test plans.»*
  <https://jobs.discovertechnata.com/companies/amdocs/jobs/48652992-business-analyst>
  Use Cases/User Stories/BRD/FRD/BPMN(Visio)/RFP reviews — [INFERRED]; UML/DOORS —
  [HYPOTHESIS].
- **Фреймворки:** TM Forum ODA/Open API/OAS 3.0 [CONFIRMED]; **eTOM + Amdocs ASOM**
  [CONFIRMED] — явно требуются в вакансии BA (*«…telecom industry and Amdocs
  business processes (ETOM, ASOM)»*) — сильнейшая находка по фреймворкам для
  Amdocs. Agile/SAFe/Scrum [INFERRED]. BABOK/IREB/PMI-PBA/ISO 29148 — **NOT FOUND**.

| Поле | Значение |
| --- | --- |
| Выручка FY2024 | $5.00 млрд, +2.4% YoY [CONFIRMED] |
| Band | leader (much larger) [CONFIRMED] |
| Артефакты | business/technical requirements, solution specs, high-level solution design, test plans, TMF Open API specs; (Use Cases/User Stories/BRD/FRD/BPMN/RFP — INFERRED) |
| Фреймворки | TM Forum ODA/Open API/OAS 3.0 + eTOM/ASOM [CONFIRMED]; Agile/SAFe [INFERRED] |
| Источники | amdocs.com FY2024 results · 20-F release · DTW/ODA blog · Discover Technata BA JD |

### A3. Mavenir (cloud-native networks) — частная (Siris Capital)

- **Выручка: ~$500-600M/год [CONFIRMED как оценка].** Mavenir не публикует
  отчётность. Наиболее достоверный источник — TelecomTV (31.05.2024): *«Its annual
  revenues are estimated to be in the region of $500 to $600m.»*
  <https://www.telecomtv.com/content/open-ran/more-moolah-for-mavenir-50501/>
  ~$650M **bookings** за FY до янв-2025 (≠ выручка). «$1 млрд» — это **промахнутая
  цель 2023**, не факт выручки; не цитировать как выручку. Рекапитализация долга
  (>$1.3B) в июле 2025: <https://www.mavenir.com/press-releases/mavenir-signs-debt-recapitalization-transaction-to-drive-continued-growth/>
  - **Band: in-band (~$400-600M).** Единственный реально «in-band» вендор группы A.
- **TM Forum [CONFIRMED]:** Open API **Platinum — 20 сертифицированных Open API**
  на платформе MDE (BSS), сент-2023; ранее Silver (5 API). Подписант Open API & ODA
  Manifesto. <https://www.mavenir.com/press-releases/mavenir-achieves-platinum-open-api-status-with-landmark-20-open-apis-certified-by-tm-forum/>
- **Артефакты [CONFIRMED, дословно из вакансий]:** RFP/RFQ/RFI responses,
  Functional specifications, Use cases/use scenarios, API specifications, Domain
  data modeling, Call-flow/Protocol-sequence/Network-design diagrams, Test plans.
  <https://builtin.com/job/solution-architect-mavenir-digital-enablement-platform/6708882>
  Метод: 4 фазы Plan→Pilot→Production→Operations, PMO-led:
  <https://www.mavenir.com/services/professional-services/development-and-deployment-process/>
  **Особенность:** выделенной роли «Business Analyst» НЕТ — BA-работа встроена в
  Solution Architect / Product Management. BRD/FRD/SRS/BPMN/UML/User Stories — **NOT FOUND**.
- **Фреймворки:** TM Forum Open API + ODA, 3GPP, O-RAN ALLIANCE, GSMA/NESAS,
  Agile/Scrum (встроенный) [CONFIRMED]; Frameworx/eTOM/SID [HYPOTHESIS];
  BABOK/IREB/PMI-PBA/SAFe/ISO 29148 — **NOT FOUND**.

| Поле | Значение |
| --- | --- |
| Выручка | ~$500-600M/год (оценка; $650M bookings; «$1B» = промах цели 2023) |
| Band | **in-band (~$400-600M)** |
| Артефакты | RFP/RFI/RFQ, Functional specs, Use cases, API specs, Domain data modeling, Call-flow/protocol/network diagrams, Test plans |
| Фреймворки | TM Forum Open API (Platinum-20) + ODA; 3GPP; O-RAN; GSMA/NESAS; Agile/Scrum |
| Источники | telecomtv.com Mavenir estimate · mavenir.com Platinum-API PR · builtin.com SA posting · mavenir.com dev/deploy-process |

### A4. CSG International / CSG Systems (BSS) — бывш. NASDAQ: CSGS

> **Корпоративный статус.** NEC завершила покупку CSG (~$2.9B, US$80.70/акция)
> **14.05.2026**; объединённым бизнесом руководит Netcracker. «NASDAQ: CSGS» как
> живой тикер — теперь история. (Подтверждено пресс-релизом netcracker.com.)
> Осторожно: «CSG Government Solutions» (csgdelivers.com) — ДРУГАЯ компания.

- **Выручка FY2024: $1,197.2M** (+2.4% YoY) [CONFIRMED]; FY2025: $1,223.3M.
  <https://ir.csgi.com/press-releases/press-release-details/2025/CSG-Systems-International-Reports-Fourth-Quarter-and-Full-Year-2024-Results/default.aspx>
  - **Band: leader (much larger)** — ~2× верхней границы band.
- **TM Forum [CONFIRMED]:** **Frameworx-сертификация Singleview Accelerate 8 — и
  eTOM (Business Process Framework), и SID (Information Framework)** (Frameworx
  12.5). Open API — **Silver**. Три продукта в ODA Component Directory (Ascendon,
  Encompass, Quote & Order). Encompass: *«Cloud-native and standards-based (ODA)…
  built for TM Forum conformity.»* <https://www.csgi.com/products/encompass>
  Dev-портал платежей Forte: <https://developers.forte.net/>
- **Артефакты [INFERRED из вакансий]:** Functional specifications/requirements,
  **User Stories + Acceptance Criteria**, Product Backlog/Epics, Solution Design,
  Configuration models, Test scripts/UAT; tools Jira/Azure DevOps/Confluence; certs
  CSPO/SAFe PO/PM; **PI Planning, system demos**. REST/OpenAPI [CONFIRMED].
  BRD/FRD/SRS/BPMN/UML/Use Cases/RFP — [HYPOTHESIS] (не найдено дословно).
- **Фреймворки:** TM Forum eTOM/SID/ODA/Open API (Silver) [CONFIRMED];
  Agile/Scrum, SAFe + PI Planning, CSPO [INFERRED]; BABOK/IREB/PMI-PBA/ISO 29148 —
  **NOT FOUND** (для CSG Systems Intl).

| Поле | Значение |
| --- | --- |
| Выручка | $1,197.2M (FY2024) / $1,223.3M (FY2025) [с мая 2026 — NEC/Netcracker] |
| Band | leader (much larger) |
| Артефакты | User stories + acceptance criteria, functional specs, backlog/epics, solution design, configuration models, test/UAT, REST/Open APIs |
| Фреймворки | TM Forum eTOM + SID + ODA + Open API (Silver); Agile/Scrum; SAFe + PI Planning; CSPO |
| Источники | ir.csgi.com FY2024/FY2025 · csgi.com/products/encompass · developers.forte.net · netcracker.com NEC-completes-acquisition |

### A5. Optiva (бывш. Comverse → Redknee, BSS) — бывш. TSX: OPT

> **Коррекция к брифу.** ESW взяла контроль в 2017 и **вышла в 2021** (не делала
> Optiva частной). Optiva оставалась на TSX и отчитывалась по 2025.
> **Qvantel (Финляндия) завершила покупку и делистинг 31.12.2025** (CAD $0.25/акция).
> <https://www.globenewswire.com/news-release/2025/12/31/3211824/0/en/Qvantel-Completes-Acquisition-of-Optiva-Creating-a-Global-Leader-in-AI-Powered-Telecom-Monetization-and-Digital-Operations.html>

- **Выручка FY2024: ~$47.1M USD** (чистый убыток $19.7M) [CONFIRMED]; FY2023
  $47.5M, FY2022 $61.8M, FY2019 ~$100M — нисходящий тренд.
  <https://www.globenewswire.com/news-release/2025/03/25/3049222/0/en/Optiva-Inc-Reports-Fourth-Quarter-2024-Financial-Results.html>
  - **Band: smaller/other** — на порядок ниже band.
- **TM Forum [CONFIRMED]:** Open API — **Silver Tier** (авг-2022, 5-я сертификация),
  подписант ODA Manifesto. **Frameworx/eTOM/SID-конформанс НЕ найден** (важное
  различие: Open API ≠ Frameworx).
  <https://www.optiva.com/press-releases/optiva-achieves-silver-tier-for-tm-forum-open-api-conformance-certification-and-signs-open-digital-architecture-manifesto>
- **Артефакты:** роль Business Analyst подтверждена careers-страницей [CONFIRMED];
  модель «configuration-not-customization», catalog-driven; основная «поверхность
  требований» — **product-catalog/configuration specs** + API specs [CONFIRMED].
  BRD/FRD/SRS/BPMN/UML — **NOT FOUND**.
- **Фреймворки:** TM Forum Open API (Silver, 5) + ODA Manifesto; 3GPP 5G SBA; SRE
  [CONFIRMED]. Frameworx/eTOM/SID, BABOK/IREB/PMI-PBA/SAFe — **NOT FOUND**.

| Поле | Значение |
| --- | --- |
| Выручка | ~$47.1M USD (FY2024) [с 31.12.2025 — Qvantel, делистинг] |
| Band | smaller/other |
| Артефакты | API specs (TM Forum Open API/REST), catalog-driven configuration specs, solution/integration design |
| Фреймворки | TM Forum Open API (Silver, 5) + ODA; 3GPP 5G; SRE |
| Источники | globenewswire Optiva Q4'24 · optiva.com Silver-Tier PR · globenewswire Qvantel-completes-acquisition |

### A6. Hansen Technologies (+ Sigma Systems) — ASX: HSN

- **Выручка FY2025 (до 30.06.2025): AUD ~392.5M** operating (FY2024 AUD 353.1M)
  [CONFIRMED, перепроверено]. <https://stockanalysis.com/quote/asx/HSN/revenue/>
  USD ≈ **$233-259M** при курсе AUD→USD ≈ 0.66 [курс — HYPOTHESIS].
  - **Band: smaller/other** — в USD ниже band (хотя в AUD близко к ~400M).
  - **Sigma Systems [CONFIRMED]:** куплена за C$157.0M (~US$116.8M), завершено
    31.05.2019; catalog/CPQ/Order Management для телеком.
    <https://www.lightreading.com/oss-bss-cx/hansen-acquires-sigma-systems-in-117m-deal>
- **TM Forum [CONFIRMED — первичные PDF]:** **Sigma Catalog v7.1 — Frameworx 18.5
  и по eTOM, и по SID:**
  - eTOM (май 2019): <https://www.tmforum.org/wp-content/uploads/2019/06/Frameworx-18.5-Certification-Report-for-Sigma-Systems-SigmaCatalog-v7.1-v1.0.pdf>
  - SID (окт 2019): <https://www.tmforum.org/wp-content/uploads/2019/11/Frameworx-18.5-Certification-Report-Sigma-Systems-SigmaCatalog-v7.1-v.1.1-SID.pdf>

  Hansen — listed ODA software provider, «Ready for ODA», сертифицировал
  обязательные Open API для компонента Product Catalog Management (TMFC001).
  «My API Story» (Hansen, сент-2023) называет 7 ключевых Open API: TMF620, TMF622,
  TMF633, TMF637, TMF638, TMF641, TMF648.
  <https://www.tmforum.org/wp-content/uploads/2023/09/3081.MYAPISTORY.Hansen.pdf>
- **Артефакты:** SID-conformant catalog/data models, eTOM-aligned process designs,
  TMF Open API specs [CONFIRMED]; BRD/FRD/SRS (полный SDLC) [INFERRED из вакансии
  Sr BA]; Use cases/user stories [HYPOTHESIS].
  ⚠️ Дисамбигуация: вакансии «Hansen Talent Group» (US staffing) — НЕ Hansen
  Technologies, исключены.
- **Фреймворки:** TM Forum Frameworx (eTOM + SID + TAM + Open API) + ODA
  [CONFIRMED]; generic Agile/SDLC [INFERRED]; BABOK/IREB/PMI-PBA/SAFe/ISO 29148 —
  **NOT FOUND**.

| Поле | Значение |
| --- | --- |
| Выручка | FY2025 AUD ~392.5M (≈ USD $259M @0.66; курс — гипотеза) |
| Band | smaller/other (в USD ниже band) |
| Артефакты | SID-conformant catalog/data models; eTOM process designs; TMF Open API specs; SDLC requirements (BRD/FRD — inferred) |
| Фреймворки | TM Forum Frameworx (eTOM, SID), ODA, Open APIs [CONFIRMED]; Agile/SDLC [inferred] |
| Источники | tmforum.org Sigma Catalog eTOM PDF · SID PDF · My API Story PDF · lightreading Sigma-acquisition |

### A7. Twilio (CPaaS — для сравнения) — NYSE: TWLO

- **Выручка FY2024: $4.458 млрд** (+7% reported / +9% organic) [CONFIRMED].
  <https://www.twilio.com/en-us/press/releases/twilio-announces-fourth-quarter-and-full-year-2024-results>
  - **Band: leader (much larger)** — ~10× верхней границы band.
- **Ключевой артефакт = OpenAPI 3.0 [CONFIRMED]:** Twilio публикует официальную
  машиночитаемую OpenAPI-спецификацию всего API, автоматически поддерживаемую и
  используемую для валидации запросов.
  GitHub: <https://github.com/twilio/twilio-oai> · Docs: <https://www.twilio.com/docs/openapi>
  Богатый dev-портал: <https://www.twilio.com/docs>
- **TM Forum — NOT FOUND** (ожидаемо: developer-API CPaaS, не carrier-OSS/BSS;
  «стандарт» = OpenAPI, не Frameworx).
- **Артефакты:** OpenAPI 3.0 specs, API Reference/SDK docs, Postman collections,
  reference-architecture blueprints [CONFIRMED]; внутренняя BA-функция —
  Salesforce/Conga **CPQ Quote-to-Cash** (solution documentation) [INFERRED].
  <https://boards.greenhouse.io/twilio/jobs/3592151>
- **Фреймворки:** OpenAPI/OAS [CONFIRMED]; Agile + «paved path» platform
  engineering [INFERRED]; **TM Forum нет; именованного BA-BoK нет**;
  BABOK/IREB/PMI-PBA/ISO 29148 — **NOT FOUND**.

| Поле | Значение |
| --- | --- |
| Выручка FY2024 | $4.458 млрд [CONFIRMED] |
| Band | leader (much larger) |
| Артефакты | **OpenAPI 3.0 specs**, API Reference/SDK docs, Postman collections, reference-architecture blueprints; QTC solution docs (inferred) |
| Фреймворки | OpenAPI/OAS [CONFIRMED]; Agile/«paved path» [inferred]. Нет TM Forum, нет именованного BA-BoK |
| Источники | twilio.com FY2024 results · github.com/twilio/twilio-oai · twilio.com/docs/openapi |

### A8. RingCentral / 8x8 / Vonage (UCaaS/CPaaS)

**RingCentral (NYSE: RNG).** Выручка FY2024 **$2.400 млрд** (+9%) [CONFIRMED]:
<https://ir.ringcentral.com/news/press-release-details/2025/RingCentral-Announces-Fourth-Quarter-and-Fiscal-Year-2024-Results/>.
Band: leader. Публичные OpenAPI 2.0/3.0 specs + Postman:
<https://github.com/ringcentral/ringcentral-api-specifications>. Вакансия Business
Systems Analyst: requirements documentation, current/future-state process analysis,
test/UAT [CONFIRMED]. Compliance: ISO 27001/27017/27018, SOC 2/3, HITRUST, PCI DSS,
C5 [CONFIRMED]. **TM Forum / CAMARA / SAFe / BABOK — NOT FOUND** (только generic Agile).

**8x8 (NASDAQ: EGHT).** Выручка FY2024 (до 31.03.2024) **$728.7M** total / ~$700.6M
service [CONFIRMED]: <https://www.wallstreetzen.com/stocks/us/nasdaq/eght/revenue>.
Band: leader. Dev-портал <https://developer.8x8.com/>; владеет open-source **Jitsi**
(Apache-2.0) <https://github.com/jitsi/jitsi-meet>. Вакансия Business Systems Analyst:
Agile (sprint planning, backlog grooming), process/workflow documentation [CONFIRMED]:
<https://careers.franciscopartners.com/companies/8x8/jobs/40983657-business-systems-analyst>.
ISO 27001:2022, SOC 2 [CONFIRMED]. **TM Forum / CAMARA / SAFe / BABOK — NOT FOUND**.

**Vonage (в составе Ericsson; API-часть — бывш. Nexmo).** Standalone FY2021
**$1.409 млрд** (из них API $591M) [CONFIRMED]:
<https://www.globenewswire.com/news-release/2022/02/24/2391990/0/en/Vonage-Reports-Fourth-Quarter-2021-Financial-Results.html>.
Куплена Ericsson за $6.2B (завершено 21.07.2022):
<https://www.ericsson.com/en/press-releases/2022/7/ericsson-completes-acquisition-of-vonage>.
Band: leader. **Самая сильная стандарт-история тройки:**
- **OpenAPI-led/spec-first** («APIs are public contracts»):
  <https://developer.vonage.com/en/blog/openapi-led-development-at-nexmo>;
  **член OpenAPI Initiative** (с мест в Governance/TSC, 2021):
  <https://www.openapis.org/blog/2021/02/09/vonage-joins-openapi-initiative>
- **CAMARA Network APIs** (SIM Swap, Number Verification, Device Location):
  <https://developer.vonage.com/en/blog/how-to-get-started-with-vonage-network-apis-in-2025>;
  Ericsson («which includes Vonage») — Premium-спонсор CAMARA:
  <https://camaraproject.org/2024/09/16/camara-the-global-telco-api-alliance-delivers-first-major-release-with-innovative-apis-for-seamless-access-to-network-functions/>
- **SAFe явно и enterprise-wide:** «Lean Agile Center of Excellence (LACE)»,
  «implementing SAFe across the business», Jira & Confluence; Release Train
  Engineers, **User Stories** (Greenhouse-вакансии, [CONFIRMED-snippet]).
- **TM Forum** на уровне Ericsson (ODA-директория + конформанс TMF629), не на
  уровне продукта Vonage [CONFIRMED].

| Компания | Выручка | Band | Артефакты | Фреймворки |
| --- | --- | --- | --- | --- |
| RingCentral | FY2024 $2.40B | leader | OpenAPI 2.0/3.0 + Postman; requirements/process docs; test/UAT; RFP/RFI (snippet) | Agile; OpenAPI; ISO 27001/SOC2/HITRUST/PCI (нет TM Forum/CAMARA/SAFe/BABOK) |
| 8x8 | FY2024 $728.7M | leader | REST API portal; SDK (Jitsi/Kotlin); process/workflow docs; user stories (inferred) | Agile/Scrum; ISO 27001; Apache-2.0/Jitsi (нет TM Forum/CAMARA/SAFe/BABOK) |
| Vonage/Ericsson | FY2021 $1.409B (standalone) | leader | OpenAPI specs (core, «development contract»); Spectral CI; User Stories; SAFe backlog/PI | OpenAPI Initiative; **CAMARA + GSMA Open Gateway**; **SAFe + Scrum/Jira**; TM Forum (Ericsson-level) |

---

## ЧАСТЬ B — ТЕЛЕКОМ-ОПЕРАТОРЫ (бенчмарк лидеров)

> Все операторы ниже — **«leader (much larger)»** по выручке; их ценность для
> исследования — в **зрелых публичных BA/RE-практиках** (TM Forum ODA/Catalysts,
> developer-порталы, вакансии с явными артефактами/фреймворками).

### B1. Telenor Group (NOK)
- Выручка FY2024 **NOK 79,928M** (≈ **USD 7.3-7.4B**) [CONFIRMED]:
  <https://www.telenor.no/binaries/om/group/Annual-Report-2024-English.pdf> (стр. 159).
- TM Forum ODA + Open API Catalyst «Champion» (Async Open APIs → AsyncAPI)
  [CONFIRMED]: <https://inform.tmforum.org/research-and-analysis/proofs-of-concept/asynchronous-open-apis-to-support-event-driven-architecture>;
  GSMA Open Gateway MoU [CONFIRMED]: <https://www.gsma.com/newsroom/press-release/gsma-open-gateway/>
- **Важная находка:** публичные роли «Business Analyst» в Telenor — преимущественно
  **data/financial/commercial analysts** (SQL, Excel, Power BI/Qlik/Tableau;
  дашборды, прогнозы, бизнес-кейсы), **НЕ** классические requirements-engineering BA
  [CONFIRMED из вакансий]. Agile + Kanban [CONFIRMED]. BRD/FRD/SRS/Use Case/BPMN/UML —
  **NOT FOUND**. BABOK/IREB/PMI-PBA/ISO 29148 — **NOT FOUND**.

### B2. Orange (France, EUR)
- Выручка FY2024 **€40,260M** (≈ **USD 43.6B** @1.0822) [CONFIRMED]:
  <https://newsroom.orange.com/strong-2024-results-2025-organic-cash-flow-target-raised/?lang=eng>
- Co-founding ODA member; **«Running on ODA»** (DTW23) [CONFIRMED]:
  <https://www.telecomtv.com/content/digital-platforms-services/dt-orange-et-al-join-the-running-on-oda-club-48514/>;
  ведёт TM Forum ISA (ODA functional architecture, SID, eTOM); Catalyst «5G
  Enablement through Industry Standardized APIs» (унификация TMF+CAMARA)
  [CONFIRMED]: <https://inform.tmforum.org/features-and-opinion/dtw23-ignite-catalyst-awards-showcase-innovation-in-ai-automation-and-services>
- Dev-портал <https://developer.orange.com/products/network-apis/>; CAMARA + GSMA
  Open Gateway [CONFIRMED].
- **BA-вакансии — классические RE-роли** (orange.jobs, [CONFIRMED-snippet]):
  «capture requirements… SAFe and Jira… user stories and acceptance criteria»
  (150476); «functional specifications… Agile SCRUM/SAFe» (127600); «epics →
  features → user stories» (136451); «BPMN» (140523, 146722). Самое сильное
  публичное свидетельство формальной BA/RE-практики среди операторов наряду с
  Vodafone. BABOK/IREB/PMI-PBA/ISO 29148 — **NOT FOUND**.

### B3. Vodafone Group (EUR) + Vodafone Idea (mid-size OpCo)
- Vodafone Group FY (до 31.03.2025) **€37.448B** (≈ **USD ~$40.5B**) [CONFIRMED]:
  <https://reports.investors.vodafone.com/view/897876789>
- **Vodafone Idea (Vi)** FY 31.03.2025 ~INR 447bn ≈ **USD ~$5.1B**, убыточна,
  **mid-size** [CONFIRMED]: <https://companiesmarketcap.com/vodafone-idea/revenue/>
- TM Forum «Running on ODA» (с Axiata, Jio) [CONFIRMED]:
  <https://inform.tmforum.org/features-and-opinion/axiata-vodafone-and-jio-run-on-open-digital-architecture>;
  кейс Vodafone UK — ~20 Open API, в т.ч. TMF678/TMF632/TMF637 [CONFIRMED]:
  <https://inform.tmforum.org/research-and-analysis/case-studies/vodafone-uk-revitalizes-with-new-omnichannel-experience>
- **Сильнейшее в выборке свидетельство формальных BA-фреймворков [CONFIRMED]:**
  вакансии _VOIS требуют артефакты *«process flows, BRDs, user stories, use cases
  and data definitions»*, requirements traceability, и явно называют сертификации
  **IIBA (ECBA/CCBA/CBAP), PMI-PBA, Agile BA, Scrum, SAFe, ITIL 4**:
  <https://flexa.careers/jobs/vodafone-business-analyst-vois-69de826704c3133514437ee2>;
  PRINCE2/SAFe: <https://opportunities.vodafone.com/job/Pune-Business-Analyst-VOIS-Pune/1370339233/>
- CAMARA Sandbox / Open Gateway [CONFIRMED]: <https://developer.vodafone.com/camara>;
  **SAFe-трансформация** (>1000 чел., 6 ART, PI Planning) [CONFIRMED]:
  <https://seibert.group/blog/en/happy-pipping-vodafone-safe-agile-hive/>.
  IREB/ISO 29148 — **NOT FOUND**.

### B4. Deutsche Telekom (EUR)
- Выручка FY2024 **€115.8B** (≈ **USD ~$125B**) [CONFIRMED]:
  <https://report.telekom.com/annual-report-2024/management-report/development-of-business-in-the-group/results-of-operations-of-the-group.html>
- TM Forum Catalyst «AI-powered legacy modernization to ODA» (Moonshot) — генерит
  Open API definitions, service designs, test cases [CONFIRMED]:
  <https://inform.tmforum.org/features-and-opinion/dtw-ignite-agentic-ai-among-winners-in-tm-forum-catalyst-awards>;
  **DT chairs CAMARA Governing Board** [CONFIRMED]:
  <https://camaraproject.org/2025/10/07/camara-the-global-telco-api-alliance-issues-its-latest-meta-release-of-stable-network-apis-advancing-api-interoperability/>
- Вакансии DT IT Solutions: requirements workshops, functional requirements,
  Solution Design, **product model knowledge (e.g., TMF)**, Jira, **SAFe/SCRUM**
  [CONFIRMED]: <https://jobs.smartrecruiters.com/DeutscheTelekomITSolutions/744000122485079-business-analyst-with-english-and-german-ref5240v>
- **BPMN явно подтверждён** (Camunda case study) + SAFe [CONFIRMED]:
  <https://camunda.com/case-study/deutsche-telekom/>. BABOK/IREB/PMI-PBA — **NOT FOUND**
  (IREB немецкого происхождения и доминирует на родном рынке DT — но в источниках
  явно не назван; честно [HYPOTHESIS]).

### B5. AT&T (USD) и Verizon (USD)
- **AT&T** FY2024 **$122.3B** (−0.1%) [CONFIRMED]:
  <https://www.prnewswire.com/news-releases/att-finishes-2024-strong-delivering-growth-in-5g-and-fiber-subscribers-service-revenues-cash-from-operations-and-free-cash-flow-302360681.html>.
  AT&T **создала ECOMP → ONAP** (Linux Foundation) [CONFIRMED]; Catalyst Champion
  «SHINE», «5G Enablement» (TMF+CAMARA). Вакансия Senior Tech Business Analysis:
  *«requirements packages… user stories… requirements traceability… RFP
  development… UAT»*, Agile+Waterfall/SDLC [CONFIRMED]:
  <https://careers.techtitans.org/companies/at-t-2-91e8eb1f-f53b-4ef1-9ab3-ee91278661cb/jobs/49960609-senior-tech-business-analysis>.
  BABOK/IREB/PMI-PBA — **NOT FOUND**.
- **Verizon** FY2024 **$134.8B** (+0.6%) [CONFIRMED]:
  <https://stockanalysis.com/stocks/vz/financials/>. TM Forum **«Running on ODA»**
  (DTW Ignite 2025; «North Star Architecture»; −до ~6 недель к срокам разработки)
  [CONFIRMED]: <https://www.thefastmode.com/technology-solutions/42619-verizon-achieves-tm-forum-oda-accreditation-driving-digital-architecture-adoption>;
  CAMARA/Open Gateway (первые в США cross-carrier API-тесты) [CONFIRMED]. BA-вакансии
  — слабее (порталы 403): requirements/user stories/Agile/SAFe [INFERRED].
  BABOK/IREB/PMI-PBA — **NOT FOUND**.

---

## ЧАСТЬ C — ФРЕЙМВОРКИ И СТАНДАРТЫ (канонические URL, все [CONFIRMED])

**TM Forum (Frameworx → ODA):**
- Frameworx (overview): <https://www.tmforum.org/frameworx-evolution/>
- eTOM / Business Process Framework (**GB921**): <https://www.tmforum.org/open-digital-architecture/process-framework-etom/>
- SID / Information Framework (**GB922**): <https://www.tmforum.org/open-digital-architecture/information-framework-sid/>
- TAM → **Functional Framework** (**GB929**): <https://www.tmforum.org/open-digital-architecture/functional-framework/>
- ODA (**IG1167**): <https://www.tmforum.org/open-digital-architecture/>
- Open APIs (TMF6xx) + конформанс: <https://www.tmforum.org/open-digital-architecture/open-apis> · <https://www.tmforum.org/conformance-certification/open-api-conformance/>
- **Публичный member-directory есть:** <https://www.tmforum.org/about/membership/current-members/>

> Документы GB921/GB922/GB929 — **member-gated (403, не 404)**: существуют, но без
> аккаунта не скачиваются. Для открытого цитирования — landing-страницы выше +
> member-directory. **TAM переименован в Functional Framework** (номер GB929 тот же);
> **Frameworx вытесняется ODA**.

**BA Bodies of Knowledge:**
- IIBA BABOK Guide **v3 (2015)**: <https://www.iiba.org/career-resources/a-business-analysis-professionals-foundation-for-success/babok/>
- IREB CPRE (Foundation + Advanced: Elicitation/Management/Modeling/RE@Agile): <https://cpre.ireb.org/en>
- PMI-PBA: <https://www.pmi.org/certifications/business-analysis-pba> (handbook PDF, 200: <https://www.pmi.org/-/media/pmi/documents/public/pdf/certifications/professional-business-analysis-handbook.pdf>)
- BCS Business Analysis (книга *Business Analysis*, 4-е изд.): <https://www.bcs.org/qualifications-and-certifications/certifications-for-professionals/business-analysis/>
- SAFe **6.0** (нет роли «Business Analyst» — BA-работа распределена по PO/PM/Business Owner; модель Epics→Capabilities→Features→Stories): <https://framework.scaledagile.com/>

**Requirements / artifact standards:**
- ISO/IEC/IEEE **29148:2018** (StRS/SyRS/SRS, характеристики хороших требований): <https://www.iso.org/standard/72089.html>
- ISO/IEC/IEEE **12207:2017** / **15288:2015** (жизненный цикл): <https://www.iso.org/standard/63712.html> · <https://www.iso.org/standard/63711.html>
- OMG **BPMN 2.0** (ред. 2.0.2 = ISO/IEC 19510): <https://www.omg.org/spec/BPMN/2.0/About-BPMN/>
- OMG **UML 2.5.1** (SID публикуется в UML): <https://www.omg.org/spec/UML/2.5.1/>
- **OpenAPI Specification v3.2.0** (формат API-контракта; TMF6xx публикуются как OpenAPI): <https://spec.openapis.org/oas/v3.2.0.html>

---

## ЧАСТЬ D — СВОДНАЯ ТАБЛИЦА

| Компания | Выручка (последний FY, USD) | Band | Ключевые BA-артефакты | Фреймворки | Топ-источник |
| --- | --- | --- | --- | --- | --- |
| **Netcracker** | NOT CONFIRMED (порядок $1B+, INFERRED) | leader (INFERRED) | Use Cases, Information Models, Operation Process Specs, Functional Reqs, Solution Design, TMF Open API | TM Forum ODA/Open API (Platinum, Ready-for-ODA L6); BABOK/Agile; 3GPP/ETSI/MEF/CAMARA | netcracker.com API-Mgmt page |
| **Amdocs** | $5.00B (FY2024) | leader | business/technical reqs, solution specs, high-level design, test plans, Open API; (BRD/FRD/Use Cases/User Stories — inferred) | TM Forum ODA/Open API/OAS3 + **eTOM/ASOM**; Agile/SAFe | amdocs.com FY2024 results |
| **Mavenir** | ~$500-600M (оценка) | **in-band** | RFP/RFI/RFQ, Functional specs, Use cases, API specs, data modeling, call-flow/network diagrams, test plans | TM Forum Open API (Platinum-20)+ODA; 3GPP; O-RAN; GSMA/NESAS; Agile | telecomtv.com estimate + mavenir.com Platinum PR |
| **CSG Intl** | $1,197.2M (FY2024) | leader | User stories+AC, functional specs, backlog/epics, solution design, config models, test/UAT, REST/Open API | TM Forum **eTOM+SID**+ODA+Open API(Silver); Agile/Scrum; SAFe+PI Planning; CSPO | ir.csgi.com FY2024 |
| **Optiva** | ~$47.1M (FY2024) | smaller/other | API specs (Open API/REST), catalog/configuration specs, solution/integration design | TM Forum Open API(Silver,5)+ODA; 3GPP 5G; SRE | globenewswire Optiva Q4'24 |
| **Hansen / Sigma** | AUD ~392.5M ≈ $233-259M (FY2025) | smaller/other (в USD) | SID-conformant catalog/data models, eTOM process designs, TMF Open API; (BRD/FRD — inferred) | TM Forum Frameworx (**eTOM, SID**), ODA, Open APIs; Agile/SDLC | tmforum.org Sigma Catalog certs (PDF) |
| **Twilio** | $4.458B (FY2024) | leader | **OpenAPI 3.0 specs**, API Reference/SDK docs, Postman, reference blueprints; QTC solution docs (inferred) | OpenAPI/OAS; Agile/«paved path». Нет TM Forum, нет BA-BoK | twilio.com FY2024 + github.com/twilio/twilio-oai |
| **RingCentral** | $2.400B (FY2024) | leader | OpenAPI 2.0/3.0+Postman, requirements/process docs, test/UAT, RFP/RFI (snippet) | Agile; OpenAPI; ISO27001/SOC2/HITRUST/PCI. Нет TM Forum/CAMARA/SAFe/BABOK | ir.ringcentral.com FY2024 |
| **8x8** | $728.7M (FY2024) | leader | REST API portal, SDK (Jitsi/Kotlin), process/workflow docs, user stories (inferred) | Agile/Scrum; ISO27001; Apache-2.0/Jitsi. Нет TM Forum/CAMARA/SAFe/BABOK | wallstreetzen EGHT revenue |
| **Vonage/Ericsson** | $1.409B (FY2021 standalone) | leader | OpenAPI specs («development contract»), Spectral CI, User Stories, SAFe backlog/PI | OpenAPI Initiative; **CAMARA+GSMA Open Gateway**; **SAFe+Scrum/Jira**; TM Forum (Ericsson) | globenewswire Vonage FY2021 |
| **Telenor** | NOK 79,928M ≈ $7.3-7.4B (FY2024) | leader | дашборды/data models/прогнозы (BA=data analyst!); Open API+AsyncAPI; CAMARA defs; (user stories inferred) | TM Forum ODA/Open API; GSMA Open Gateway/CAMARA; Agile/Kanban. Нет BABOK/IREB | telenor.no Annual Report 2024 |
| **Orange** | €40,260M ≈ $43.6B (FY2024) | leader | **User Stories, Acceptance Criteria, Functional Specs, Epics/Features, BPMN**, OpenAPI/CAMARA, eTOM/SID | **SAFe**, Agile/Scrum, **BPMN**, TM Forum ODA/eTOM/SID/Open API, CAMARA. Нет BABOK/IREB | newsroom.orange.com 2024 results |
| **Vodafone** | €37.448B ≈ $40.5B (FY 31.03.25) | leader | **BRD, User Stories, Use Cases, Process Flows, Acceptance Criteria, Reqs Traceability**, UAT, API specs | **IIBA BABOK, PMI-PBA, SAFe/Agile, ITIL 4, PRINCE2**, TM Forum ODA/Open API, CAMARA | reports.investors.vodafone.com FY25 |
| **Vodafone Idea** | INR ~447bn ≈ $5.1B (FY 31.03.25) | mid-size | наследует Group/_VOIS BA-практику | наследует Group (SAFe/IIBA) | companiesmarketcap.com Vi revenue |
| **Deutsche Telekom** | €115.8B ≈ $125B (FY2024) | leader | business/functional reqs, Solution Design, Open API, **BPMN models**, service designs/test cases | **SAFe**, Agile, TM Forum ODA/Open API, CAMARA (DT chairs board), **BPMN** | report.telekom.com 2024 |
| **AT&T** | $122.3B (FY2024) | leader | **Requirements packages, User Stories, Reqs Traceability, RFP**, process docs, UAT, API specs (TMF+CAMARA) | Agile+Waterfall/SDLC, SAFe (inferred), TM Forum ODA/eTOM/SID, CAMARA, **ONAP/ECOMP** | prnewswire AT&T 2024 |
| **Verizon** | $134.8B (FY2024) | leader | API/OpenAPI design standards, ODA «North Star» architecture, Open API/CAMARA contracts, process models | TM Forum ODA/Open API, CAMARA, REST/OpenAPI; Agile/SAFe (inferred) | stockanalysis.com VZ financials |

---

## ЧАСТЬ E — КЛЮЧЕВЫЕ ВЫВОДЫ ДЛЯ ИССЛЕДОВАНИЯ

1. **TM Forum ODA / Open API — самый цитируемый, наиболее [CONFIRMED] общий
   слой** для телеком-вендоров и операторов. Почти все держат Open API conformance
   и/или «Running on ODA»; операторы — ещё и CAMARA/GSMA Open Gateway. Это самый
   надёжный «индустриальный якорь» для таксономии артефактов.
2. **«Business Analyst» означает разное.** Спектр: от **data/financial analyst**
   (Telenor) до **классического requirements engineer** (Orange, Vodafone, AT&T,
   DT) до **встроенной в Solution Architect** функции (Mavenir, отчасти Optiva).
   Это прямо релевантно Факту 3 issue (смешение комплексных/атомарных артефактов).
3. **Явные BA-BoK (BABOK/PMI-PBA) публично подтверждены только у Vodafone**
   (вакансии _VOIS: IIBA ECBA/CCBA/CBAP, PMI-PBA, SAFe, ITIL 4). У Netcracker —
   только «BABOK principles» в одной вакансии. У всех остальных — **NOT FOUND**;
   честно помечено, не выдумано. **IREB CPRE и ISO/IEC/IEEE 29148 не названы НИ У
   КОГО** из 16 компаний в публичных источниках.
4. **Универсальный де-факто артефакт требований — OpenAPI-спецификация**
   (Twilio/Vonage прямо называют её «контрактом»). Для BSS/OSS-вендоров и
   операторов к нему добавляются **TMF Open API (TMF6xx), eTOM-процессы, SID-модели
   данных**. Классические **BRD/FRD/SRS как именованные шаблоны подтверждены лишь у
   немногих** (Vodafone — BRD; Hansen — INFERRED); чаще встречаются «functional
   specifications», «requirements packages», «solution design».
5. **BPMN явно [CONFIRMED] только у Orange и Deutsche Telekom**; у остальных —
   [HYPOTHESIS]. **SAFe/Agile-at-scale** — широко (Vodafone 6 ART, DT, Orange,
   Vonage LACE; AT&T/Verizon — INFERRED).
6. **Полоса $400-600M почти не населена.** Единственный реально **in-band** —
   **Mavenir** (~$500-600M, оценка). Vendors группы A либо лидеры (Amdocs $5B,
   Twilio $4.46B, CSG $1.2B), либо «smaller/other» (Optiva $47M, Hansen ~$250M USD).
   Гипотеза issue о «компаниях телекома с оборотом 400-600 млн $» как массовом
   классе — **не подтверждается публичными данными**; band разрежён.
7. **Корпоративные коррекции к брифу (все [CONFIRMED]):** CSG куплена **NEC**
   (завершено 14.05.2026, ведёт Netcracker); Optiva куплена **Qvantel** (делистинг
   31.12.2025; ESW вышла ещё в 2021, не делала частной); Vonage в составе
   **Ericsson** (с 2022). Netcracker — единственная значимая дыра в данных: выручка
   официально не раскрыта, агрегаторы противоречат друг другу ($1B-$5.5B).

> **Дисклеймер источников.** Где первичная страница отдавала 403 (tmforum.org,
> att.com/verizon.com, ATS-вакансии, SEC HTML), факт подтверждался через
> fetchable-зеркала + PDF TM Forum (HTTP 200) + сниппеты; такие места помечены
> [CONFIRMED-snippet]/[INFERRED]. Конверсии в USD — приблизительны (указаны курсы).
