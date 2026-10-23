---
status: draft
version: 0.1
updated: 2026-10-23
temperature: 0.1
analysis-subtype: recommendation
source: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/387"
scope: repo
based_on: "issue #387, экспорт чата «манго промпт» за 21–23.10.2026 (реестр experiments/issue_387/chat-2026-10-22-23-register.md), docs/analysis/2026-10-23-prompts-catalog-audit.md, docs/adr/003-ba-ontology.md, standards/ba-ontology.md, standards/industry-standards-standard.md"
related_artifacts:
  - "docs/adr/2026-10-adr-012-bcreq-meta-standards.md"
  - "standards/bcreq-sections/README.md"
  - "standards/bcreq-sections/01-glossary.md"
  - "standards/bcreq-composition-standard.md"
  - "standards/bcreq-prompt-architecture.md"
  - "docs/rfc/2026-10-bcreq-meta-standards-rfc.md"
  - "experiments/issue_387/chat-2026-10-22-23-register.md"
---

# Третье мнение: достаточность стека стандартов BCREQ

## Summary / BLUF

Стек BABOK + arc42 + C4 + OpenAPI **достаточен для структуры** BCREQ: каждому
из восьми разделов есть основной стандарт. Он **недостаточен для качества
формулировок** разделов 3 и 4 и для **асинхронных интеграций** раздела 5:
BABOK описывает, *что* выявлять, но не даёт правил записи требования, а
OpenAPI не описывает события и webhooks. Закрыть разрывы можно четырьмя
открытыми или частично открытыми дополнениями без нового фреймворка:
ISO/IEC/IEEE 29148 + EARS (формулировка ФТ), ISO/IEC 25010 (каталог НФТ),
AsyncAPI (события), IREB CPRE Glossary (сверка терминов). Риск «один стандарт
на все продукты» реален в обе стороны; его снимает правило «один стандарт
раздела + доменный профиль на подпункт» (К1–К7 композиции). TM Forum ODA
остаётся альтернативой: открыты только TMF Open APIs. Для речевой аналитики
открытого отраслевого стандарта нет — это зафиксированный пробел, а не
недосмотр. Словари для сверки Глоссария восстановлены из ADR-003 и
ba-ontology (D1, D2, D4, D9, D10) и дополнены доменными (D3, D5–D8, D11).

## 1. Context / Scope

- **Дата:** 2026-10-23. **Режим:** Creative, issue #387, Задача 2.
- **Что оценивается:** стек, предложенный БА: BABOK или IREB для раздела 3
  [р. 752, Ч-17](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_387/chat-2026-10-22-23-register.md?plain=1#L51), arc42 + C4 + OpenAPI + доменные для раздела 5
  [р. 752, Ч-18](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_387/chat-2026-10-22-23-register.md?plain=1#L52), TM Forum — альтернатива [р. 766, Ч-31](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_387/chat-2026-10-22-23-register.md?plain=1#L65). Постановка
  issue: «Независимая оценка достаточности предложенного стека
  (BABOK+Arc42+C4+OpenAPI)», риск «один стандарт на все продукты»,
  open-source альтернативы, восстановление словарей.
- **Позиция «третьего мнения».** Первое мнение — предложение БА, второе —
  ответы модели в чате (р. 748–796). Здесь стек проверен против того, что
  должен содержать каждый раздел по мета-стандартам
  [bcreq-sections](../../standards/bcreq-sections/README.md), а не против
  списка популярных фреймворков.
- **Критерий достаточности.** Стандарт раздела достаточен, если он даёт:
  (а) состав раздела, (б) правило формулировки или формат записи, (в) критерий
  проверки. Если покрыт только (а) — разрыв.
- **Граница.** Кросс-модельная проверка промптов не выполнялась: БА отложил её
  до тестирования промптов [р. 766, Ч-34](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_387/chat-2026-10-22-23-register.md?plain=1#L68).

## 2. Метод

1. Для каждого раздела выписаны элементы «необходимо и достаточно» из его
   мета-стандарта.
2. Для каждого элемента найден источник в стеке БА (BABOK v3, arc42, C4,
   OpenAPI, TM Forum).
3. Непокрытые элементы сопоставлены с открытыми стандартами из
   [industry-standards-standard](../../standards/industry-standards-standard.md)
   и с источниками, которые уже есть в репозитории.
4. Доступность проверена по официальным страницам (URL — в «Источниках»).
   Страницы ISO и TM Forum отдают 403 автоматическим клиентам; их статус
   доступа взят из описания на сайте и не проверялся загрузкой текста.

## 3. Findings

### 3.1. Достаточность стека по разделам

| Раздел | Стек БА | (а) состав | (б) формулировка | (в) проверка | Разрыв → дополнение |
| --- | --- | --- | --- | --- | --- |
| 1 Глоссарий | BABOK 10.23 Glossary | да | частично: нет правила одного термина на понятие | нет сверки с отраслью | IREB CPRE Glossary, ISO/IEC/IEEE 24765 (SEVOCAB), доменные словари D5–D8 |
| 2 Бизнес-контекст | BABOK 6.1 Analyze Current State, 6.2 Define Future State | да | нет | частично | правило короткого стиля КС1–КС7 (ISO 24495-1, ASD-STE100) |
| 3 ФТ | BABOK 7.1 Specify and Model Requirements | да | **нет**: BABOK не задаёт шаблон фразы требования | частично (7.2 Verify) | ISO/IEC/IEEE 29148 (характеристики требования), EARS (шаблоны фраз) |
| 4 НФТ | BABOK 10.30 Non-Functional Requirements Analysis | частично | нет | нет каталога характеристик | ISO/IEC 25010 (модель качества как чек-лист категорий) |
| 5 ОРР L1 | arc42 §3, C4 L1 | да | да (схема контекста) | да | — |
| 5 ОРР L2 | arc42 §5–6, C4 L2, OpenAPI | да | да для синхронного API | **нет для событий** | AsyncAPI (события, webhooks) |
| 6 Особенности и ограничения | arc42 §2 Architecture Constraints | да | частично | нет | ISO/IEC/IEEE 29148 (понятие constraint) |
| 7 UC | BABOK 10.47 Use Cases and Scenarios | да | да (формат Cockburn в ba-ontology A13) | частично: нет техники граничных кейсов | ISTQB Glossary (граничные значения, классы эквивалентности); UML 2.5.1 |
| 8 Дополнительные | BABOK 10.38 Risk Analysis and Management, 10.1 Acceptance and Evaluation Criteria | да | частично | частично | ISO 31000 (шкала и владелец риска) |

**Вывод 1.** Стек БА покрывает (а) во всех разделах. Без дополнений не
закрыты три места: формулировка ФТ (3), каталог НФТ (4), события (5 L2).
Все три закрываются стандартами того же класса — стандарты требований и
спецификаций. Это соответствует позиции БА «класс стандарта важнее
конкретного» [р. 748, Ч-10](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_387/chat-2026-10-22-23-register.md?plain=1#L44).

**Вывод 2.** Добавлять BPMN как основной стандарт не нужно. BPMN нужен только
сценариям КЦ (процесс оператора) и подключается профилем КЦ
([композиция §4](../../standards/bcreq-composition-standard.md#4-профили-продуктов)).
SCXML — там же, для состояний оператора и сценариев IVR.

### 3.2. Риск «один стандарт на все продукты»

БА сформулировал риск как гипотезу 2: один класс стандартов для разных
продуктов может привести к антипаттерну «описания доработок к определённым
продуктам» [р. 748, Ч-11](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_387/chat-2026-10-22-23-register.md?plain=1#L45).

Риск двусторонний:

| Сторона | Как проявляется в BCREQ | Признак в документе | Защита в стандартах |
| --- | --- | --- | --- |
| Недоспецификация: один стандарт без доменных | В L2 нет протокола ВАТС (SIP), состояний оператора КЦ, лимитов API. Разработка уточняет устно. | Раздел 5.2 одинаков по глубине для API и для КЦ. | Профили продуктов как данные; доменный стандарт к подпункту 5.2.x (К1, К3). |
| Фрагментация: стандарт на продукт | Документ распадается на «ФТ ВАТС», «ФТ КЦ»; стыковое ФТ описано дважды или ни разу. | Группировка раздела 3 по продуктам; разные шаблоны ОРР в одном документе. | Раздел 3 — один список по Capability (К2); единый каркас раздела 5 (К3); стыковое ФТ (К4). |

**Вывод 3.** Антипаттерн из гипотезы БА — это фрагментация документа по
продуктам. Его предотвращает не выбор другого стандарта, а **уровень
применения** доменного стандарта: раздел целиком подчиняется одному классу,
доменный стандарт — только подпункту одного продукта. Тот же принцип у arc42:
шаблон один, доменные детали — в Building Block View. Поэтому отдельные
промпты по продуктам не нужны; решение по гипотезе API vs КЦ/ЛК [р. 796, Ч-41](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_387/chat-2026-10-22-23-register.md?plain=1#L75) —
в [композиции §6](../../standards/bcreq-composition-standard.md#6-гипотеза-специализированные-промпты-для-api-и-кцлк).

### 3.3. Открытость и альтернативы

| Стандарт | Доступ | Роль в стеке |
| --- | --- | --- |
| BABOK Guide v3 | платный текст; глоссарий открыт | основной (1–4, 7, 8) |
| IREB CPRE (глоссарий, syllabus) | открыт | открытая замена BABOK для 1, 3 ([р. 752, Ч-17](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_387/chat-2026-10-22-23-register.md?plain=1#L51)) |
| arc42 | открыт (CC BY-SA 4.0) | основной (5, 6) |
| C4 model | открыт (CC BY 4.0) | основной (5) |
| OpenAPI 3.x | открыт (Apache-2.0) | основной (5 L2) |
| AsyncAPI 3.x | открыт (Apache-2.0) | дополнение (5 L2, события) |
| EARS | статьи открыты | дополнение (3) |
| ISO/IEC/IEEE 29148, ISO/IEC 25010, ISO 31000 | платные; термины — через SEVOCAB | дополнения (3, 4, 6, 8) |
| ISTQB Glossary | открыт | дополнение (7) |
| TM Forum Open APIs | открыты (Apache-2.0) | альтернатива (5 L2) |
| TM Forum SID, eTOM, ODA components | полный текст — участникам TM Forum | альтернатива при ODA-1…ODA-3 |

Рассмотренные открытые альтернативы основному стеку:

| Альтернатива | Чем могла бы заменить | Почему не основная |
| --- | --- | --- |
| IREB CPRE вместо BABOK | разделы 1, 3 | Равноценна по классу; BABOK уже в онтологии репозитория (ADR-003). Оставлена открытой заменой. |
| ISO/IEC/IEEE 42010 (architecture description) вместо arc42 | раздел 5 | Метастандарт описания архитектуры, без готового шаблона разделов; arc42 даёт шаблон. |
| Volere Requirements Specification Template | разделы 3, 4, 6 | Платный шаблон (лицензия на проект или площадку, бесплатно — только академическое использование); по составу пересекается с 29148. |
| ГОСТ 34.602-2020 | структура ТЗ | Это структура старой модели «ТЗ», которую аудит Задачи 1 признал источником расхождений; оставлен словарём D10. |
| TOGAF | архитектура предприятия | Уровень предприятия, избыточен для дельты доработки (Р6). |

**Вывод 4.** Замена основного стека не нужна. Открытость стека обеспечена:
все *обязательные к чтению* модели части (arc42, C4, OpenAPI, AsyncAPI, IREB,
ISTQB, EARS) открыты; платные ISO-стандарты используются как источник
понятий через открытый SEVOCAB.

### 3.4. Речевая аналитика: пробел

Для продукта РА (`analytics`) не найден открытый отраслевой стандарт
содержания требований: распознавание речи и оценка разговоров описываются
продуктовой документацией вендоров. Профиль РА в
[композиции §4](../../standards/bcreq-composition-standard.md#4-профили-продуктов)
поэтому не содержит доменного стандарта; сверка терминов — D11 и D3. Это
допустимо по правилу Р2 «не выдумывать»: выдуманный стандарт хуже явного
пробела. Если Mango примет внутренний стандарт метрик РА, он подключается
профилем без изменения мета-стандартов.

### 3.5. Восстановленные словари Глоссария

БА напомнил, что словари для сверки уже предлагались, и попросил их
восстановить [р. 796, Ч-37](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_387/chat-2026-10-22-23-register.md?plain=1#L71); расхождения термина БА с отраслью промпт должен
подсветить и порекомендовать [р. 796, Ч-38](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_387/chat-2026-10-22-23-register.md?plain=1#L72).

Что найдено в репозитории:

| Источник в репозитории | Что предлагалось | Статус в мета-стандарте |
| --- | --- | --- |
| [ADR-003 «Онтология BA»](../adr/003-ba-ontology.md) (issue #97, 2026-06-16) | BABOK Glossary, IREB CPRE Glossary для глоссария задачи; ISO/IEC/IEEE 29148, ISO/IEC 25010, ГОСТ 34.602 как стандарты | D1, D2, D4, D10 |
| [ba-ontology.md](../../standards/ba-ontology.md), артефакт A07 `task-glossary`, раздел источников | BABOK Glossary; IREB CPRE; TM Forum SID | D1, D2, D9 |
| [product-classification-contract.md](../../standards/product-classification-contract.md#маппинг-терминов-mango) | маппинг терминов Mango ↔ международные аналоги | D11 |

Новые (доменные) словари, которых в репозитории не было: ISO/IEC/IEEE 24765
(SEVOCAB, D3), 3GPP TR 21.905 (D5), ITU-T Terms и E.600 (D6), IEC Electropedia
(D7), OpenAPI + RFC 9110 (D8). Полная таблица D1–D11, порядок источников
истины и классы расхождения С0–С4 — в
[01-glossary](../../standards/bcreq-sections/01-glossary.md#сверка-с-индустриальными-словарями).

**Вывод 5.** Ранее предложенные словари восстановлены как базовый набор D1, D2,
D4, D9, D10. Он был ориентирован на термины БА и не покрывал телефонию и КЦ —
отсюда доменные словари. Отраслевой словарь используется **только для
сверки**: он не заменяет термин БА молча (порядок источников истины, п. 3).

### 3.6. Структура 2.1–2.14

БА просил подтвердить структуру шагов 2.1–2.14 или предложить альтернативу
[р. 778, Ч-35](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_387/chat-2026-10-22-23-register.md?plain=1#L69). Проверка — в
[архитектуре промптов §6](../../standards/bcreq-prompt-architecture.md#6-подтверждение-структуры-21214):
структура подтверждена с одним добавленным шагом Ш-В (оценка отклонения
около 7 %, в пределах правила 20 % [р. 766, Ч-33](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_387/chat-2026-10-22-23-register.md?plain=1#L67)).

## 4. Recommendations

1. Принять стек БА как основной без замены; закрепить четыре дополнения
   (29148 + EARS, 25010, AsyncAPI, IREB) в
   [композиции §1](../../standards/bcreq-composition-standard.md#1-стек-стандартов-по-разделам).
2. Применять доменные стандарты только к подпунктам одного продукта (К1);
   отдельные промпты по продуктам не создавать до выполнения критерия
   пересмотра (≥3 прогона с одной профильной правкой).
3. TM Forum ODA держать альтернативой с условиями ODA-1…ODA-3; в роль модели
   не включать (АП1 аудита).
4. Пробел РА закрывать внутренним стандартом Mango, когда он появится; до
   этого — только D11.
5. Проверить пороги стиля и чек-листов на прогонах Задачи 3; кросс-модельный
   прогон — после тестирования промптов [р. 766, Ч-34](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_387/chat-2026-10-22-23-register.md?plain=1#L68).
6. Решения, которые расходятся с текущими контрактами, — через
   [RFC-387-01…07](../rfc/2026-10-bcreq-meta-standards-rfc.md).

## 5. Related Artifacts

- [ADR-012](../adr/2026-10-adr-012-bcreq-meta-standards.md)
- [Мета-стандарты разделов](../../standards/bcreq-sections/README.md)
- [Стандарт композиции](../../standards/bcreq-composition-standard.md)
- [Архитектура промптов](../../standards/bcreq-prompt-architecture.md)
- [Контракт стадий и гейтов](../contracts/bcreq-stage-gates.md)
- [Аудит каталога `prompts/` (Задача 1)](2026-10-23-prompts-catalog-audit.md)
- [Реестр цитат чата](../../experiments/issue_387/chat-2026-10-22-23-register.md)

### Источники

- BABOK Guide v3: <https://www.iiba.org/career-resources/a-business-analysis-professionals-foundation-for-success/babok/>
- IREB CPRE Glossary: <https://cpre.ireb.org/en/downloads-and-resources/glossary>
- arc42: <https://arc42.org/overview> · C4 model: <https://c4model.com/>
- OpenAPI: <https://spec.openapis.org/oas/latest.html> · AsyncAPI: <https://www.asyncapi.com/docs/reference/specification/latest>
- EARS: <https://alistairmavin.com/ears/>
- ISO/IEC/IEEE 29148:2018: <https://www.iso.org/standard/72089.html> · ISO/IEC 25010:2023: <https://www.iso.org/standard/78176.html>
- ISO/IEC/IEEE 24765 / SEVOCAB: <https://www.iso.org/standard/71952.html> · <https://pascal.computer.org/>
- ISO/IEC/IEEE 42010:2022: <https://www.iso.org/standard/74393.html>
- ISTQB Glossary: <https://glossary.istqb.org/> · UML 2.5.1: <https://www.omg.org/spec/UML/2.5.1/>
- ISO 31000:2018: <https://www.iso.org/standard/65694.html>
- TM Forum ODA: <https://www.tmforum.org/oda/> · TM Forum Open APIs: <https://github.com/tmforum-apis>
- Volere Requirements Specification Template: <https://www.volere.org/templates/volere-requirements-specification-template/>
- TOGAF Standard: <https://www.opengroup.org/togaf>
