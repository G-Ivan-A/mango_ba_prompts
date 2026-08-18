---
status: proposed
version: 0.1
updated: 2026-06-16
ai-generated: true
type: adr
scope: ba-ontology
issue: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/97"
related_standard: "https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/ba-ontology.md"
related_prs:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/pull/98"
related_artifacts:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/taxonomy.md"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/00-index.md"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/product-classification-contract.md"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/pr-ops/artifact-map.md"
---

# ADR-003: Онтология бизнес-анализа (Артефакт ↔ Процесс ↔ Операция)

> **Статус:** Proposed · **Дата:** 2026-06-16 · **Issue:**
> <https://github.com/G-Ivan-A/mango_ba_prompts/issues/97> · **Стандарт-контракт:**
> <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/ba-ontology.md>

> **Numbering note.** Этот ADR открывает трёхзначную дорожку стандартов
> (`001-prompt-standard`, `002-pattern-standard`, далее `003`-`010` из issue #97).
> Она не пересекается с четырёхзначной governance-дорожкой
> (`0001`, `0002`, `0003-creative-mode-governance`). В обсуждениях документ
> называется **ADR-003 (ba-ontology)**. Подход согласован с ADR-002, который уже
> зафиксировал параллельные нумерации при явном disambiguation:
> <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/adr/002-pattern-standard.md>

## Контекст

Репозиторий `mango_ba_prompts` к моменту issue #97 уже содержит три независимых,
но не связанных формально слоя знаний:

1. **Когнитивные операции** — 13 атомарных типов мыслительной работы БА
   ([docs/taxonomy.md](../taxonomy.md), §1).
2. **Процессы БА** — 9 повторяемых рабочих сценариев с пошаговыми workflow
   ([docs/ba-processes/00-index.md](../ba-processes/00-index.md)).
3. **Классификация функциональности** — иерархия
   `Domain → Capability → Feature → Atomic Function`
   ([standards/product-classification-contract.md](../../standards/product-classification-contract.md)).

При этом **артефакт** (то, что операция потребляет на входе и производит на
выходе) нигде не определён как самостоятельная сущность. Он появляется только как
свободный текст в колонке «Пример артефакта» таксономии и в полях «Входы/Выходы»
карты процессов. Это создаёт три проблемы:

- **Нет единого реестра типов артефактов.** ASR-расшифровка, ФТ, ТЗ, Use Case,
  Risk Register и Defect Report упоминаются десятки раз, но не перечислены в одном
  месте с определением, производящей операцией и применимым стандартом.
- **Связи неявны и однонаправлены.** Из таксономии нельзя ответить: «какие
  операции производят артефакт X», «какой человек или агент выполняет операцию
  Y», «какому международному стандарту соответствует артефакт Z». Связь
  «операция → пример артефакта» зафиксирована как 1:1 строка таблицы, хотя в
  реальности она многие-ко-многим.
- **Нет жизненного цикла артефакта.** Поле `status` (`draft`/`canonical`/
  `archived`) описано только для промптов ([ADR-001](001-prompt-standard.md)), но
  не для аналитических артефактов (ФТ, ТЗ, US/UC, отчётов).

**Ядро проблемы.** Чтобы масштабировать библиотеку (НФТ: 29 → 50+ артефактов,
24 → 50+ промптов) и подготовить её к RAG, нужна формальная **онтология** —
явная модель сущностей и связей, на которую смогут опираться промпты, паттерны,
GitHub Pages и будущий retrieval. Issue #97 (ФТ-1) требует формализовать триаду
**Артефакт ↔ Процесс ↔ Операция** (или обоснованную альтернативу),
классифицировать операции по исполнителю, построить граф связей с множественными
рёбрами, определить ≥20 типов артефактов и их жизненный цикл — и доказать каждое
решение ссылками на BABOK Guide v3, ISO/IEC/IEEE 29148, ISO/IEC 25010 и
ГОСТ 34.602.

Этот ADR фиксирует онтологию как архитектурное решение (по требованию
[ADR-0003 о Creative-mode governance](0003-creative-mode-governance.md): решения,
меняющие архитектурную практику, оформляются как ADR). Полный нормативный реестр
сущностей, граф и машина состояний вынесены в живой контракт
[standards/ba-ontology.md](../../standards/ba-ontology.md); этот ADR объясняет
контекст, модель, доказательную базу и последствия.

## Решение

### 1. Триада сохраняется как ядро, но расширяется в направленный граф

Триада **Операция → Процесс → Артефакт** недостаточна как линейная цепочка: НФТ
гибкости из issue #97 прямо требует «множественные связи (один артефакт — много
операций)». Поэтому онтология формализуется как **направленный размеченный граф**
(labeled property graph), где триада остаётся смысловым ядром (спина), а
остальные сущности и рёбра — обоснованное расширение. Это и есть «обоснованная
альтернатива», допускаемая ФТ-1.

```text
                 декомпозируется в            применяет
   Процесс ───────────────────────▶ Подпроцесс ──────────▶ Операция
      │                                  │                    │
      │ относится к направлению          │ имеет gate          │ выполняется
      ▼                                  ▼                    ▼
  Направление                       Контрольная точка     Исполнитель
  разработки                        (human gate)          (человек / LLM / гибрид)
                                                              │
                          потребляет вход │  │ производит выход │ соответствует
                                          ▼  ▼                  ▼
                                       Артефакт            Область знаний BABOK
                                          │
              ┌───────────────────────────┼───────────────────────────┐
              ▼                            ▼                           ▼
       классифицируется            имеет состояние             регулируется
       Domain→Capability→…         жизненного цикла            Стандартом
```

Реализующий слой (паттерн `реализует` операцию; промпт `исполняет` паттерн в
режиме `stepwise`/`oneshot`/`legacy`) уже описан в
[ADR-001](001-prompt-standard.md) и [ADR-002](002-pattern-standard.md) и
подключается к графу через операцию.

### 2. Сущности онтологии

| Сущность | Определение | Источник определения в репозитории |
| --- | --- | --- |
| **Операция** (Operation) | Атомарный тип когнитивной работы БА, который можно поручить промпту. 13 штук. | [docs/taxonomy.md §1](../taxonomy.md) |
| **Процесс** (Process) | Повторяемый рабочий сценарий БА. 9 штук. | [docs/taxonomy.md §2](../taxonomy.md) |
| **Подпроцесс** (Subprocess) | Шаг процесса: одна строка в детальной карте процесса (операция + цель + промпты + gate). | [docs/ba-processes/00-index.md](../ba-processes/00-index.md) |
| **Артефакт** (Artifact) | Информационный объект, который операция потребляет на входе или производит на выходе. ≥20 типов — см. §5 и стандарт. | **новое (этот ADR)** |
| **Исполнитель** (Performer) | Кто выполняет операцию: человек, LLM-агент или гибрид. | [pr-ops/artifact-map.md](../../pr-ops/artifact-map.md) (роли) + §4 |
| **Контрольная точка** (Gate) | Точка, где результат требует подтверждения человека до продолжения. | [docs/ba-processes/00-index.md](../ba-processes/00-index.md) (колонка Gate/gap) |
| **Направление разработки** (Direction) | Контекст задачи (`client-order`, `tender-rfp`, …), задающий глубину артефакта. | [docs/ba-ecosystem.md](../ba-ecosystem.md), [00-index.md](../ba-processes/00-index.md) |
| **Область знаний BABOK** (Knowledge Area) | Одна из 6 KA BABOK Guide v3, к которой относится операция. | **новое (этот ADR, §«Доказательная база»)** |
| **Класс функциональности** | Уровень `Domain → Capability → Feature → Atomic Function`, к которому относится артефакт-требование. | [standards/product-classification-contract.md](../../standards/product-classification-contract.md) |
| **Стандарт** (Standard) | Внешний нормативный источник (BABOK, ISO/IEC/IEEE 29148, ISO/IEC 25010, ГОСТ 34.602/34.601), которому соответствует артефакт. | **новое (этот ADR + [standards/industry-standards-standard.md](../../standards/industry-standards-standard.md))** |
| **Паттерн / Промпт** | Реализующий слой: паттерн — практика, промпт — исполняемый артефакт. | [ADR-002](002-pattern-standard.md), [ADR-001](001-prompt-standard.md) |

### 3. Граф связей (множественные рёбра)

Связи — типизированные рёбра. Кардинальность подобрана так, чтобы выполнить НФТ
гибкости («один артефакт — много операций» и наоборот):

| Ребро | От | К | Кардинальность |
| --- | --- | --- | --- |
| `декомпозируется в` | Процесс | Подпроцесс | 1 → N |
| `применяет` | Подпроцесс | Операция | N → M |
| `выполняется` | Операция | Исполнитель | N → M (одна операция — разные исполнители в разных режимах) |
| `потребляет` (вход) | Операция | Артефакт | N → M |
| `производит` (выход) | Операция | Артефакт | N → M |
| `соответствует` | Операция | Область знаний BABOK | N → M |
| `регулируется` | Артефакт | Стандарт | N → M |
| `классифицируется` | Артефакт-требование | Domain→Capability→Feature→Atomic Function | 1 → 1..N |
| `имеет состояние` | Артефакт | Состояние жизненного цикла | 1 → 1 (в момент времени) |
| `реализует` | Паттерн | Операция | N → M |
| `исполняет` | Промпт | Паттерн | N → 1 |
| `трассируется` | Артефакт | Артефакт (вышестоящий/нижестоящий) | N → M |

Ребро `трассируется` замыкает граф в сеть traceability (НФТ трассируемости):
например, `Раздел 4 ФТ` трассируется вверх к `User Story` и `Use Case`, а вниз —
к `Раздел 7 Технические детали`. Полный машиночитаемый список рёбер с примерами —
в [стандарте](../../standards/ba-ontology.md).

### 4. Классификация операций по исполнителю

Каждая из 13 операций классифицируется по типичному исполнителю. Классификация
опирается на роли из [pr-ops/artifact-map.md](../../pr-ops/artifact-map.md)
(**Пользователь**, **Исполнитель**, **Внешний агент**, **Агент-исполнитель**) и
на модель human-gate из [ADR-0003](0003-creative-mode-governance.md).

- **LLM** — операцию агент выполняет преимущественно сам; человек проверяет
  результат на выходном gate.
- **Гибрид** — агент готовит черновик, человек обязательно дополняет суждением
  (приоритеты, риски, бизнес-ценность) до продолжения.
- **Человек** — решение принадлежит человеку; агент только подаёт вход или
  оформляет результат.

| Операция | Исполнитель | Почему | Обязательный human gate |
| --- | --- | --- | --- |
| `ingestion` | LLM | Нормализация формы без интерпретации смысла. | Сохранность смысла. |
| `understanding` | Гибрид | Агент извлекает термины и вопросы; человек подтверждает цель и допущения. | Нет критичных неотвеченных вопросов. |
| `validation` | Гибрид | Агент находит дефекты по чек-листу (аудит, см. [ADR-004](004-operations-taxonomy.md)); человек решает, что блокирует. | Дефекты привязаны к пунктам. |
| `modeling` | LLM | Структурирование в US/UC/диаграммы по известным шаблонам. | Actor/system boundary не смешаны. |
| `solution_design` | Гибрид | Агент предлагает технические варианты; архитектор/человек выбирает. | Бизнес-слой уже согласован. |
| `documentation` | LLM | Оформление согласованного содержания в целевой формат. | Не добавлены требования без источника. |
| `quality` | Гибрид | Агент собирает метрики; человек интерпретирует тренды. | Категории и правила подсчёта согласованы. |
| `research` | Гибрид | Агент собирает источники; человек отделяет факты от гипотез. | Выводы отделены от непроверенных гипотез. |
| `governance` | Человек | Статусы, приоритеты, владельцы, жизненный цикл — управленческое решение. | Изменение без владельца не идёт дальше. |
| `impact_analysis` | Гибрид | Агент строит карту влияния; человек подтверждает зоны без owner. | Нет high-impact зоны без владельца. |
| `reverse_requirements` | Гибрид | Агент реконструирует поведение; человек верифицирует по системе. | Реконструкция подтверждена evidence. |
| `risk_analysis` | Человек | Оценка вероятности/импакта и митигаций — ответственность человека; агент помогает. | High/compliance-риски имеют owner review. |
| `release_readiness` | Человек | Решение «готово к релизу» — управленческое и юридическое. | Acceptance/rollback/comms подтверждены. |

Эта классификация прямо реализует НФТ совместимости (не отменяет ни одну из 13
операций, включая `risk_analysis`) и НФТ provability (каждая строка имеет
обоснование и gate).

### 5. Реестр типов артефактов (30 ≥ 20)

Ниже — сводка; полный реестр с определениями, входными/выходными операциями и
стандартами ведётся в [standards/ba-ontology.md](../../standards/ba-ontology.md).
Все типы извлечены из реальных артефактов репозитория (таксономия, карта
процессов, классификация), фиктивные типы не вводятся (НФТ provability).

| # | Тип артефакта | Категория | Производящая операция | Стандарт-ориентир |
| --- | --- | --- | --- | --- |
| 1 | ASR-расшифровка (raw) | Вход | — (внешний) | — |
| 2 | Очищенная расшифровка | Промежуточный | `ingestion` | — |
| 3 | Письмо заказчика | Вход | — (внешний) | — |
| 4 | Заметки/нотатки встречи | Вход | — (внешний) | — |
| 5 | Сырое требование | Вход | — (внешний) | ISO/IEC/IEEE 29148 §стейкхолдерские потребности |
| 6 | Тендерное ТЗ (внешнее) | Вход | — (внешний) | ГОСТ 34.602 (как образец структуры) |
| 7 | Глоссарий задачи | Промежуточный | `understanding` | BABOK Glossary; IREB CPRE Glossary |
| 8 | Список вопросов заказчику | Промежуточный | `understanding` | BABOK Elicitation and Collaboration |
| 9 | Резюме встречи | Выход | `documentation` | BABOK Elicitation and Collaboration |
| 10 | Business Alignment Pack | Композит | `understanding`+`documentation` | BABOK Strategy Analysis |
| 11 | User Story | Выход | `modeling` | BABOK RADD; IREB user story |
| 12 | Acceptance criteria | Выход | `modeling`/`validation` | ISO/IEC/IEEE 29148 (verifiable) |
| 13 | Use Case (Cockburn) | Выход | `modeling` | BABOK RADD |
| 14 | UML/BPMN-диаграмма | Выход | `modeling` | BABOK RADD (modelling) |
| 15 | Раздел 4 ФТ (функц. требования) | Выход | `documentation` | ISO/IEC/IEEE 29148; ГОСТ 34.602 §4 |
| 16 | Раздел 6 «Ограничения» | Выход | `documentation` | ГОСТ 34.602 §4; ISO/IEC 25010 (NFR) |
| 17 | Раздел 7 «Технические детали» | Выход | `solution_design` | ГОСТ 34.602 §4-5 |
| 18 | ФТ КК (Feature Specification) | Композит-документ | `documentation` | ГОСТ 34.602 |
| 19 | ТЗ (Contract Tech Spec) | Композит-документ | `documentation` | **ГОСТ 34.602-2020** (см. ниже) |
| 20 | Defect report (отчёт о дефектах) | Выход | `validation` | ISO/IEC/IEEE 29148 (характеристики качества) |
| 21 | Quality summary / ТЗ-статистика | Выход | `quality` | ISO/IEC 25010 |
| 22 | Risk register (реестр рисков) | Выход | `risk_analysis` | BABOK (Risk Analysis); ISO/IEC/IEEE 29148 |
| 23 | Impact map (карта влияния) | Выход | `impact_analysis` | BABOK RLCM (Assess Requirements Changes) |
| 24 | Reverse requirements | Выход | `reverse_requirements` | BABOK RADD |
| 25 | Release-readiness чек-лист | Выход | `release_readiness` | BABOK Solution Evaluation |
| 26 | Coverage matrix / Tender Fit Pack | Композит | `quality`+`validation` | ISO/IEC/IEEE 29148 (traceability) |
| 27 | Traceability matrix | Выход | `governance`/`impact_analysis` | ISO/IEC/IEEE 29148; BABOK RLCM (Trace) |
| 28 | Аналитическая записка | Выход | `research` | BABOK Strategy Analysis |
| 29 | Чек-лист статусов / бэклог | Выход | `governance` | BABOK RLCM |
| 30 | BCREQ (многоуровневое требование) | Композит | несколько процессов | см. [ADR-009](009-bcreq-formation-process.md) |

### 6. Жизненный цикл артефакта

Состояния и переходы (машина состояний). Переходы через **human gate** требуют
подтверждения Пользователя (модель «молчание = согласие» из
[ADR-0003](0003-creative-mode-governance.md)).

```text
  raw ──ingestion──▶ draft ──┬──▶ in-review ──┬──▶ validated ──gate──▶ approved
   │                  ▲       │                │                          │
   │                  │       │                ▼                          ▼
   │             (правки)     │          needs-clarification ──▶     baselined/released
   │                  └───────┘                │ (⚠ требует уточнения,         │
   │                                            │  незавершённый подпроцесс)    ▼
   └────────────────────────────────────────── └──────────────────────▶ superseded/archived
```

| Состояние | Значение | Кто переводит |
| --- | --- | --- |
| `raw` | Сырой вход без обработки. | внешний |
| `draft` | Черновик после первой операции. | LLM/Исполнитель |
| `in-review` | На проверке/валидации. | Исполнитель |
| `needs-clarification` | Заблокирован: открытый вопрос, `⚠️ требует уточнения`, незавершённый подпроцесс. | любой участник |
| `validated` | Прошёл аудит (см. [ADR-004](004-operations-taxonomy.md)). | Гибрид + gate |
| `approved` | Утверждён Пользователем. | Человек (gate) |
| `baselined`/`released` | Зафиксирован как база/выпущен. | Человек (gate) |
| `superseded`/`archived` | Заменён новой версией / выведен из работы. | Человек |

Состояние `needs-clarification` — формальный механизм для незавершённых
подпроцессов (требование ФТ-7), он встраивается в граф здесь, а используется в
[ADR-009](009-bcreq-formation-process.md).

## Доказательная база (соответствие стандартам)

ФТ-1 требует доказать онтологию ссылками на BABOK Guide v3, IEEE 29148, ISO 29148
и ГОСТ 34.602. Ниже — соответствие с **полными URL всех источников** (НФТ
provability; запрет на выдуманные источники).

### BABOK Guide v3 (IIBA)

BABOK Guide v3 определяет **6 областей знаний** (Knowledge Areas), на которые
ложатся 13 операций (полный маппинг — в [ADR-004](004-operations-taxonomy.md)):
Business Analysis Planning and Monitoring; Elicitation and Collaboration;
Requirements Life Cycle Management; Strategy Analysis; Requirements Analysis and
Design Definition; Solution Evaluation. BABOK формально различает **требование**
(«a usable representation of a need») и **дизайн** («a usable representation of a
solution») — это обосновывает разделение артефактов на требования (ФТ, US) и
проектные решения (Раздел 7). Источники:

- IIBA: <https://www.iiba.org/>
- BABOK Guide: <https://www.iiba.org/career-resources/a-business-analysis-professionals-foundation-for-success/babok/>
- BABOK Glossary (публичные определения): <https://www.iiba.org/career-resources/a-business-analysis-professionals-foundation-for-success/babok/glossary/>

### ISO/IEC/IEEE 29148:2018

Стандарт «Systems and software engineering — Life cycle processes — Requirements
engineering» задаёт характеристики качества требований: **9 для отдельного
требования** (Necessary, Appropriate, Unambiguous, Complete, Singular, Feasible,
Verifiable, Correct, Conforming) и **5 для набора** (Complete, Consistent,
Feasible, Comprehensible, Able to be validated). Эти характеристики — основа
критериев аудита артефактов 11-12, 15, 20, 27 и операции `validation`. Источники:

- ISO каталог: <https://www.iso.org/standard/72089.html>
- IEEE SA (активная редакция): <https://standards.ieee.org/ieee/29148/6937/>

### ISO/IEC 25010 (модель качества продукта)

Используется для нефункциональных требований (артефакт 16 «Ограничения» и
`quality`/`risk_analysis`). Редакция 2011 — 8 характеристик; редакция 2023
(«Product quality model») — 9 характеристик (добавлена Safety; Usability →
Interaction Capability; Portability → Flexibility). Источники:

- ISO/IEC 25010:2011: <https://www.iso.org/standard/35733.html>
- ISO/IEC 25010:2023: <https://www.iso.org/standard/78176.html>
- ISO OBP (свободный просмотр 2023): <https://www.iso.org/obp/ui/en/#!iso:std:78176:en>

### ГОСТ 34.602 и ГОСТ 34.601 — важное предупреждение об источнике

> **Внимание (НФТ provability — запрет выдуманных источников).** Issue #97 и его
> список источников ссылаются на **«ГОСТ 34.602-2015»** с URL
> <https://docs.cntd.ru/document/1200124556>. Проверка по нескольким независимым
> каталогам показала, что **редакции 34.602-2015 не существует**. Реально
> действуют две редакции:
>
> - **ГОСТ 34.602-2020** «ТЗ на создание автоматизированной системы» (взамен
>   34.602-89; введён в действие 01.01.2022, приказ Росстандарта № 1522-ст),
>   10 разделов ТЗ: <https://docs.cntd.ru/document/1200181804>,
>   <https://allgosts.ru/01/040/gost_34.602-2020>;
> - **ГОСТ 34.602-89** (классическая редакция, 9 разделов):
>   <https://standards.narod.ru/gosts/gost34/34-602-89.htm>.
>
> Поэтому артефакт 19 «ТЗ» в этой онтологии привязывается к **реальной**
> редакции ГОСТ 34.602-2020 (с упоминанием 34.602-89 для исторической
> совместимости), а не к несуществующей «-2015». Ссылку из issue следует считать
> опечаткой в номере редакции.

Стадии создания АС (жизненный цикл документов §6) опираются на **ГОСТ 34.601-90**
«Автоматизированные системы. Стадии создания» (8 стадий: формирование требований
→ концепция → ТЗ → эскизный проект → технический проект → рабочая документация →
ввод в действие → сопровождение): <https://docs.cntd.ru/document/1200006921>,
<https://www.prj-exp.ru/gost/gost_34-601-90.php>.

### TM Forum и IREB (для классификации и терминологии)

Классификация артефактов-требований переиспользует уже принятые в репозитории
источники TM Forum (SID/eTOM) и IREB CPRE — см.
[product-classification-contract.md](../../standards/product-classification-contract.md):

- TM Forum SID: <https://www.tmforum.org/open-digital-architecture/information-framework-sid/>
- TM Forum eTOM: <https://www.tmforum.org/open-digital-architecture/process-framework-etom/>
- IREB CPRE Glossary: <https://cpre.ireb.org/en/downloads-and-resources/glossary>

## Примеры

**Пример A. Множественные рёбра «операция ↔ артефакт».** Артефакт 15 «Раздел 4
ФТ» производится операцией `documentation`, но потребляется операциями
`validation` (аудит), `impact_analysis` (карта влияния) и `reverse_requirements`
(сверка с поведением). Один артефакт — четыре связи: это и есть требуемая
гибкость, недостижимая в линейной цепочке.

**Пример B. Классификация по исполнителю на реальном маршруте.** В процессе
«Формирование ФТ/ТЗ» шаг 1 (`ingestion`, LLM) очищает ASR; шаг 4 (`documentation`,
LLM) оформляет ФТ; но шаг с `risk_analysis` остаётся за человеком — агент готовит
заготовку реестра рисков, owner-review обязателен.

**Пример C. Жизненный цикл с блокировкой.** Черновик ТЗ (`draft`) уходит в
`in-review`; валидация находит требование без критерия приёмки и помечает его
`⚠️ требует уточнения` → артефакт переходит в `needs-clarification`, а не в
`validated`. Это легальное незавершённое состояние (вход для [ADR-009](009-bcreq-formation-process.md)).

## Self-test

1. **Дано:** новый тип артефакта «Stakeholder map» из процесса «Помощь ПО/ПМ».
   **Ожидаемо:** он добавляется в реестр [стандарта](../../standards/ba-ontology.md)
   со ссылкой на `governance` как производящую операцию и BABOK
   «Elicitation and Collaboration» как стандарт; имена/связи не ломают
   существующие. **Acceptance:** граф остаётся связным, кардинальности соблюдены.
2. **Дано:** операция `risk_analysis`. **Ожидаемо:** исполнитель = «Человек»,
   операция не отменена (НФТ совместимости). **Acceptance:** строка присутствует
   в §4.
3. **Дано:** ссылка «ГОСТ 34.602-2015». **Ожидаемо:** документ помечает её как
   несуществующую и подставляет 34.602-2020. **Acceptance:** см. предупреждение
   в «Доказательной базе».

Локальная проверка: `python3 scripts/validate_issue_97_ontology_standards.py`.

## Последствия

**Положительные:**

- Появляется единая система координат: промпты, паттерны, GitHub Pages и будущий
  RAG ссылаются на одни и те же сущности и связи.
- Артефакт становится первоклассной сущностью с реестром, стандартом и
  жизненным циклом — основа для трассируемости (НФТ) и для [ADR-005](005-artifact-team-naming.md)
  (именование артефактов).
- Граф расширяем без переписывания: добавление артефакта/операции — это новая
  вершина и рёбра, а не миграция (НФТ масштабируемости).
- Каждое решение привязано к реальному стандарту с полным URL; выявлена и
  исправлена ошибка источника в самом issue.

**Отрицательные / технический долг:**

- Полный граф пока ведётся в Markdown ([стандарт](../../standards/ba-ontology.md)),
  без машиночитаемого экспорта (JSON/RDF). Это сознательно: до RAG достаточно
  reviewable-таблиц; экспорт — отдельная задача.
- Реестр из 30 артефактов нужно поддерживать в синхронизации с таксономией и
  картой процессов; за это отвечает правило ведения в стандарте.

## Альтернативы (отклонены)

1. **Оставить триаду строго линейной (Операция → Процесс → Артефакт).** Отклонено:
   нарушает НФТ гибкости (один артефакт — много операций), не выражает
   traceability и классификацию по исполнителю.
2. **Хранить артефакты только как колонку в таксономии.** Отклонено: нет
   определений, стандартов, жизненного цикла; невозможно масштабировать к 50+.
3. **Сразу описать онтологию в RDF/OWL.** Отклонено: избыточно до появления RAG;
   повышает порог входа для БА и противоречит принципу «reviewable Markdown».
4. **Принять «ГОСТ 34.602-2015» как есть.** Отклонено: редакция не существует;
   нарушило бы НФТ provability.

## Связанные артефакты

- Issue #97: <https://github.com/G-Ivan-A/mango_ba_prompts/issues/97>
- PR #98: <https://github.com/G-Ivan-A/mango_ba_prompts/pull/98>
- Стандарт онтологии (контракт): <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/ba-ontology.md>
- Таксономия: <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/taxonomy.md>
- Индекс процессов БА: <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/00-index.md>
- Контракт классификации: <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/product-classification-contract.md>
- Карта артефактов: <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/pr-ops/artifact-map.md>
- ADR-001 (стандарт промптов): <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/adr/001-prompt-standard.md>
- ADR-002 (стандарт паттернов): <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/adr/002-pattern-standard.md>
- ADR-0003 (Creative-mode governance): <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/adr/0003-creative-mode-governance.md>

### Международные стандарты (полные URL)

- IIBA / BABOK Guide v3: <https://www.iiba.org/career-resources/a-business-analysis-professionals-foundation-for-success/babok/>
- BABOK Glossary: <https://www.iiba.org/career-resources/a-business-analysis-professionals-foundation-for-success/babok/glossary/>
- ISO/IEC/IEEE 29148:2018: <https://www.iso.org/standard/72089.html> · <https://standards.ieee.org/ieee/29148/6937/>
- ISO/IEC 25010:2011: <https://www.iso.org/standard/35733.html>
- ISO/IEC 25010:2023: <https://www.iso.org/standard/78176.html>
- ГОСТ 34.602-2020: <https://docs.cntd.ru/document/1200181804> · <https://allgosts.ru/01/040/gost_34.602-2020>
- ГОСТ 34.602-89: <https://standards.narod.ru/gosts/gost34/34-602-89.htm>
- ГОСТ 34.601-90: <https://docs.cntd.ru/document/1200006921> · <https://www.prj-exp.ru/gost/gost_34-601-90.php>
- TM Forum SID: <https://www.tmforum.org/open-digital-architecture/information-framework-sid/>
- TM Forum eTOM: <https://www.tmforum.org/open-digital-architecture/process-framework-etom/>
- IREB CPRE Glossary: <https://cpre.ireb.org/en/downloads-and-resources/glossary>
