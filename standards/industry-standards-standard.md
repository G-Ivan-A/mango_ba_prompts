---
status: draft
version: 0.2
updated: 2026-10-23
ai-generated: true
type: contract
scope: industry-standards
related_artifacts:
  - "docs/adr/008-industry-standards-standard.md"
  - "standards/kb-standard.md"
  - "standards/GLOSSARY.md"
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/97"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/387"
---

# Стандарт отраслевых стандартов и best practices

> Контракт-носитель [ADR-008](../docs/adr/008-industry-standards-standard.md).
> Нормативный словарь [RFC 2119](https://www.rfc-editor.org/info/bcp14)
> (**ДОЛЖНО** / **СЛЕДУЕТ** / **МОЖНО**). Версия `draft` до утверждения
> Пользователем (issue #97).

## Стороны и область

Контракт обязывает всех, кто ссылается на внешние стандарты и best practices в
артефактах, промптах и ADR. Термины уровня обязательности (Standard, Policy,
Practice, Guideline …) — в [GLOSSARY.md](GLOSSARY.md); здесь — различение
**внешних** источников и правила их применения.

## 1. Терминология

| Термин | Определение | Нормативность |
| --- | --- | --- |
| De jure стандарт | Утверждён органом стандартизации (ISO/IEC/IEEE, ГОСТ). | нормативный в своём контексте |
| De facto стандарт | Принят отраслью без формального органа (TM Forum). | по договорённости |
| Best practice | Рекомендуемый подход; не обязателен. | информативный |
| Framework/методология | Связная модель понятий и процессов (BABOK, ODA). | информативный/нормативный |
| Нормативная ссылка | Обязательна к применению в данном контексте. | нормативный |
| Информативная ссылка | Для справки. | информативный |

Различение «нормативное/информативное» — по ISO/IEC Directives, Part 2:
<https://www.iso.org/sites/directives/current/part2/index.xhtml>.

## 2. Правила применения

- **Правило И1 (верификация).** Источник **ДОЛЖЕН** быть проверен на
  существование (документ, редакция/год, полный URL) до цитирования; чек-лист —
  [KB: source-backed-analysis](../kb/practices/source-backed-analysis.md#чек-лист-проверки-источника).
- **Правило И2 (полный URL).** Каждая ссылка — **полным URL**.
- **Правило И3 (приоритет).** При конфликте применяется верхний tier: явное
  требование Пользователя → de jure → de facto → best practice → guideline;
  решение фиксируется ADR.
- **Правило И4 (локализация).** ГОСТ — РФ-контекст ТЗ; ISO/IEEE — международный;
  best practice — где нет обязательного стандарта.
- **Правило И5 (маркировка).** Ссылка помечается «нормативная» или
  «информативная».
- **Правило И6 (реестр).** Допускаются только источники из §3; новый — через
  issue/PR с подтверждённым URL.

## 3. Сверенный реестр источников

> Колонка «В issue #97» приведена для прослеживаемости. «⚠️ проверить» = указанный
> в issue идентификатор не сошёлся со сверенным; молча не заменяем — приводим оба.

| Источник | Tier | Норм/Инф | Сверенный URL | В issue #97 |
| --- | --- | --- | --- | --- |
| ISO/IEC/IEEE 29148:2018 | de jure | нормативный | <https://www.iso.org/standard/72089.html> · <https://standards.ieee.org/ieee/29148/6937/> | ⚠️ проверить: `iso.org/standard/72545.html` (действ. 72089); `ieee/29148/4378` |
| ISO/IEC 25010:2023 | de jure | нормативный | <https://www.iso.org/standard/78176.html> | ⚠️ проверить: `iso.org/standard/78405.html` (действ. 78176) |
| ГОСТ 34.602-2020 | de jure | нормативный (РФ) | <https://docs.cntd.ru/document/1200181804> | ⚠️ проверить: «ГОСТ 34.602-**2015**» (`1200124556`) — **редакции -2015 нет**; есть -89 и -2020 |
| ГОСТ 34.602-89 (истор.) | de jure | информативный | <https://standards.narod.ru/gosts/gost34/34-602-89.htm> | — |
| BABOK Guide v3 | framework/best practice | информативный | <https://www.iiba.org/career-resources/a-business-analysis-professionals-foundation-for-success/babok/> | `iiba.org/career-resources/a-body-of-knowledge` (вероятный редирект) |
| TM Forum Frameworx / ODA | de facto | информативный | <https://www.tmforum.org/oda/> · <https://www.tmforum.org/open-digital-architecture/> | `tmforum.org/oda/` |
| Anthropic Prompt Engineering Guide | best practice | информативный | <https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview> | то же |
| ISO/IEC Directives, Part 2 | de jure | нормативный (терминология) | <https://www.iso.org/sites/directives/current/part2/index.xhtml> | — |

### 3.1. Дополнение по issue #387 (мета-стандарты разделов BCREQ)

> Добавлено по правилу И6 через issue #387 / PR #389. Проверка 2026-10-23:
> HTTP 200 по URL, кроме строк с пометкой «403». Сайты ISO, IEC Electropedia и
> APA отвечают 403 автоматическим запросам; номер в каталоге ISO сверен по
> зеркалам каталога (committee.iso.org, национальные органы). Применение —
> в [мета-стандартах разделов](bcreq-sections/README.md) и
> [стандарте композиции](bcreq-composition-standard.md).

| Источник | Tier | Норм/Инф | Сверенный URL | Где применяется (issue #387) |
| --- | --- | --- | --- | --- |
| BABOK Guide v3 Glossary | framework/best practice | информативный | <https://www.iiba.org/career-resources/a-business-analysis-professionals-foundation-for-success/babok/glossary/> | раздел 1, словарь D1 |
| IREB CPRE Glossary | framework/best practice | информативный | <https://cpre.ireb.org/en/downloads-and-resources/glossary> | разделы 1, 3 |
| ISO/IEC/IEEE 24765:2017 · SEVOCAB | de jure | нормативный (терминология) | <https://www.iso.org/standard/71952.html> (403) · <https://pascal.computer.org/> | раздел 1, словарь D3 |
| 3GPP TR 21.905 | de jure | информативный | <https://portal.3gpp.org/desktopmodules/Specifications/SpecificationDetails.aspx?specificationId=558> | раздел 1, словарь D5 |
| ITU-T Terms and Definitions · ITU-T E.600 | de jure | информативный | <https://www.itu.int/br_tsb_terms/> · <https://www.itu.int/rec/T-REC-E.600> | раздел 1, словарь D6; профиль КЦ |
| IEC Electropedia (IEV) | de jure | информативный | <https://www.electropedia.org/> (403) | раздел 1, словарь D7 |
| IETF RFC 9110 (HTTP) · RFC 3261 (SIP) | de jure | нормативный для протоколов | <https://www.rfc-editor.org/rfc/rfc9110> · <https://www.rfc-editor.org/rfc/rfc3261> | раздел 1; профили API (HTTP) и ВАТС (SIP) |
| EARS (Mavin et al.) | best practice | информативный | <https://alistairmavin.com/ears/> | раздел 3 |
| arc42 | de facto | информативный | <https://arc42.org/overview> | разделы 2, 5 |
| C4 model | de facto | информативный | <https://c4model.com/> | раздел 5 L2 |
| OpenAPI Specification | de facto | нормативный для контракта API в 5 L2 | <https://spec.openapis.org/oas/latest.html> | раздел 5 L2, профиль API |
| AsyncAPI Specification | de facto | информативный | <https://www.asyncapi.com/docs/reference/specification/latest> | раздел 5 L2 (события) |
| TM Forum Open APIs | de facto | информативный | <https://github.com/tmforum-apis> | альтернатива ODA (ODA-1…ODA-3) |
| OMG UML 2.5.1 · OMG BPMN 2.0.2 · W3C SCXML | de jure | информативный | <https://www.omg.org/spec/UML/2.5.1/> · <https://www.omg.org/spec/BPMN/2.0.2/> · <https://www.w3.org/TR/scxml/> | разделы 5, 7; профиль КЦ |
| ISTQB Glossary | de facto | информативный | <https://glossary.istqb.org/> | раздел 7 (граничные кейсы) |
| ISO 31000:2018 | de jure | информативный | <https://www.iso.org/standard/65694.html> (403) | раздел 8.1 |
| W3C WCAG 2.2 | de jure | информативный | <https://www.w3.org/TR/WCAG22/> | профиль ЛК (только доработки интерфейса) |
| ISO 24495-1:2023 Plain language | de jure | информативный | <https://www.iso.org/standard/78907.html> (403) | короткий стиль КС1–КС7 |
| ASD-STE100 Simplified Technical English | de facto | информативный | <https://www.asd-ste100.org/> | короткий стиль |
| GOV.UK Writing for GOV.UK · Digital.gov Plain language · NN/g How users read on the web | best practice | информативный | <https://www.gov.uk/guidance/content-design/writing-for-gov-uk> · <https://digital.gov/guides/plain-language> · <https://www.nngroup.com/articles/how-users-read-on-the-web/> | короткий стиль |
| Главред | best practice (инструмент) | информативный | <https://glvrd.ru/> | короткий стиль, русский текст |
| Miller 1956 · Cowan 2001 · Brysbaert 2019 | исследование | информативный | <https://doi.org/10.1037/h0043158> (403) · <https://doi.org/10.1017/S0140525X01003922> · <https://doi.org/10.1016/j.jml.2019.104047> | размер чек-листа 3–7, бюджет слов КС7 |
| ISO/IEC/IEEE 42010:2022 · TOGAF · Volere Template | de jure / framework / best practice (платный) | информативный | <https://www.iso.org/standard/74393.html> (403) · <https://www.opengroup.org/togaf> · <https://www.volere.org/templates/volere-requirements-specification-template/> | альтернативы в третьем мнении |
| Anthropic, Building effective agents · Liu et al. 2023 «Lost in the Middle» | best practice / исследование | информативный | <https://www.anthropic.com/engineering/building-effective-agents> · <https://arxiv.org/abs/2307.03172> | архитектура промптов |

## Критерии соответствия (DoD)

- [ ] Каждая внешняя ссылка проверена (И1) и приведена полным URL (И2).
- [ ] Ссылка помечена нормативная/информативная (И5) и есть в реестре §3 (И6).
- [ ] Конфликты разрешены по tier (И3) и зафиксированы ADR.
- [ ] Расхождения с issue помечены «⚠️ проверить», а не заменены молча.
- [ ] `python3 scripts/validate_issue_97_ontology_standards.py` проходит.

## Источники

- ADR-008 (носитель): [docs/adr/008-industry-standards-standard.md](../docs/adr/008-industry-standards-standard.md)
- ISO/IEC Directives, Part 2: <https://www.iso.org/sites/directives/current/part2/index.xhtml>
- ISO/IEC/IEEE 29148:2018: <https://www.iso.org/standard/72089.html>
- ISO/IEC 25010:2023: <https://www.iso.org/standard/78176.html>
- ГОСТ 34.602-2020: <https://docs.cntd.ru/document/1200181804>
- BABOK Guide v3: <https://www.iiba.org/career-resources/a-business-analysis-professionals-foundation-for-success/babok/>
- TM Forum ODA: <https://www.tmforum.org/oda/>
- Anthropic Prompt Engineering Guide: <https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview>
- RFC 2119 / BCP 14: <https://www.rfc-editor.org/info/bcp14>
