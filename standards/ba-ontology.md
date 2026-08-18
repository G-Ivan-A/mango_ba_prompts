---
status: draft
version: 0.1
updated: 2026-06-16
ai-generated: true
type: contract
scope: ba-ontology
related_artifacts:
  - "docs/adr/003-ba-ontology.md"
  - "docs/taxonomy.md"
  - "docs/ba-processes/00-index.md"
  - "standards/product-classification-contract.md"
  - "pr-ops/artifact-map.md"
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/97"
---

> **LLM Loading Contract — full layer.**
> Start with [`standards/ba-ontology.executable.md`](ba-ontology.executable.md).
> Load this full file only when an escalation trigger in the executable companion is true:
> explicit request for full/rationale/history, missing required section in
> executable, need for exact wording/table/reference, or editing/validating this
> full file. Otherwise do not load this file into context.

# Стандарт онтологии бизнес-анализа

> Контракт-носитель решения [ADR-003](../docs/adr/003-ba-ontology.md). Формат — по
> практике Хаба: обязательства сверху, обоснование — в ADR. Нормативный словарь
> [RFC 2119](https://www.rfc-editor.org/info/bcp14)
> (**ДОЛЖНО** / **СЛЕДУЕТ** / **МОЖНО**). Версия `draft` до утверждения
> Пользователем (issue #97).

## Стороны и область

Контракт описывает **онтологию** репозитория — сущности БА и связи между ними.
Он обязывает всех contributors и AI-агентов, которые добавляют или изменяют
операции, процессы, артефакты и их связи. Реализующий слой (паттерны, промпты)
регулируется [pattern-standard.md](pattern-standard.md) и
[prompt-standard.md](prompt-standard.md) и подключается к онтологии через
операцию.

## 1. Сущности (вершины графа)

| Сущность | Ключ | Кардинальность набора | Источник истины |
| --- | --- | --- | --- |
| Операция | `snake_case` (как в таксономии) | 13 | [docs/taxonomy.md §1](../docs/taxonomy.md) |
| Процесс | номер 1-9 | 9 | [docs/taxonomy.md §2](../docs/taxonomy.md) |
| Подпроцесс | `<процесс>.<шаг>` | N (строки карт процессов) | [docs/ba-processes/00-index.md](../docs/ba-processes/00-index.md) |
| Артефакт | `kebab-case` тип | ≥20 (см. §4) | этот стандарт |
| Исполнитель | `человек` \| `llm` \| `гибрид` | 3 | этот стандарт + [pr-ops/artifact-map.md](../pr-ops/artifact-map.md) |
| Контрольная точка (gate) | привязана к подпроцессу | N | [docs/ba-processes/00-index.md](../docs/ba-processes/00-index.md) |
| Направление разработки | `kebab-case` | 6 | [docs/ba-ecosystem.md](../docs/ba-ecosystem.md) |
| Область знаний BABOK | KA-код | 6 | [ADR-004](../docs/adr/004-operations-taxonomy.md) |
| Стандарт | имя+редакция | N | этот стандарт, [industry-standards-standard.md](industry-standards-standard.md) |
| Состояние жизненного цикла | см. §5 | 8 | этот стандарт |

**Правило С1.** Новая операция/процесс **ДОЛЖНА** сперва появиться в
`docs/taxonomy.md` (правила эволюции таксономии, §3 там же), затем — здесь как
вершина графа. Артефакт **ДОЛЖЕН** добавляться в реестр §4 этого стандарта.

## 2. Связи (рёбра графа)

Все рёбра — направленные и типизированные. Кардинальность подобрана под НФТ
гибкости (множественные связи).

| # | Ребро | От → К | Кардинальность |
| --- | --- | --- | --- |
| R1 | `декомпозируется в` | Процесс → Подпроцесс | 1 → N |
| R2 | `применяет` | Подпроцесс → Операция | N → M |
| R3 | `выполняется` | Операция → Исполнитель | N → M |
| R4 | `потребляет` (вход) | Операция → Артефакт | N → M |
| R5 | `производит` (выход) | Операция → Артефакт | N → M |
| R6 | `соответствует` | Операция → Область знаний BABOK | N → M |
| R7 | `регулируется` | Артефакт → Стандарт | N → M |
| R8 | `классифицируется` | Артефакт-требование → Domain→…→Atomic Function | 1 → 1..N |
| R9 | `имеет состояние` | Артефакт → Состояние ЖЦ | 1 → 1 (в момент t) |
| R10 | `реализует` | Паттерн → Операция | N → M |
| R11 | `исполняет` | Промпт → Паттерн | N → 1 |
| R12 | `трассируется` | Артефакт → Артефакт | N → M |

**Правило С2.** Ребро `трассируется` (R12) **ДОЛЖНО** связывать каждый
производный артефакт минимум с одним источником (НФТ трассируемости). Пример:
`Раздел 4 ФТ` ← `User Story` ← `Глоссарий задачи` ← `Очищенная расшифровка`.

## 3. Классификация операций по исполнителю

Полная классификация и обоснование каждой строки — в
[ADR-003 §4](../docs/adr/003-ba-ontology.md). Сводка-контракт:

| Операция | Исполнитель | Обязательный выходной gate |
| --- | --- | --- |
| `ingestion` | `llm` | сохранность смысла |
| `understanding` | `гибрид` | нет критичных открытых вопросов |
| `validation` | `гибрид` | дефекты привязаны к пунктам |
| `modeling` | `llm` | actor/system boundary не смешаны |
| `solution_design` | `гибрид` | бизнес-слой согласован |
| `documentation` | `llm` | нет требований без источника |
| `quality` | `гибрид` | правила подсчёта согласованы |
| `research` | `гибрид` | факты отделены от гипотез |
| `governance` | `человек` | у изменения есть владелец |
| `impact_analysis` | `гибрид` | нет high-impact зоны без owner |
| `reverse_requirements` | `гибрид` | реконструкция подтверждена evidence |
| `risk_analysis` | `человек` | high/compliance-риски имеют owner-review |
| `release_readiness` | `человек` | acceptance/rollback/comms подтверждены |

**Правило С3.** Операция со значением `человек` или `гибрид` **НЕ ДОЛЖНА**
переводить артефакт в состояние `validated`/`approved`/`released` без
подтверждения человека (см. §5).

## 4. Реестр типов артефактов (нормативный)

Колонки: **Тип** · **Категория** (вход / промежуточный / выход / композит) ·
**Определение** · **Вход для** (операции-потребители) · **Выход** (производящая
операция) · **Стандарт-ориентир**. Все типы извлечены из реальных артефактов
репозитория; фиктивные типы вводить **НЕ ДОЛЖНО** (НФТ provability).

| # | Тип | Категория | Определение (кратко) | Выход | Вход для | Стандарт |
| --- | --- | --- | --- | --- | --- | --- |
| A01 | `asr-transcript-raw` | вход | Необработанная ASR-расшифровка звонка/встречи. | — | `ingestion` | — |
| A02 | `transcript-clean` | промежуточный | Очищенная расшифровка (артефакты речи убраны, смысл сохранён). | `ingestion` | `understanding`,`documentation` | — |
| A03 | `customer-letter` | вход | Письмо/сообщение заказчика. | — | `understanding`,`documentation` | — |
| A04 | `meeting-notes` | вход | Заметки участника встречи. | — | `understanding`,`documentation` | — |
| A05 | `raw-requirement` | вход | Сырое требование от стейкхолдера. | — | `understanding`,`validation` | ISO/IEC/IEEE 29148 (stakeholder needs) |
| A06 | `tender-spec-external` | вход | Внешнее тендерное ТЗ для анализа. | — | `understanding`,`quality`,`validation` | ГОСТ 34.602 (образец структуры) |
| A07 | `task-glossary` | промежуточный | Глоссарий терминов задачи + допущения. | `understanding` | `documentation`,`modeling`,`validation` | BABOK Glossary; IREB CPRE |
| A08 | `customer-questions` | промежуточный | Список вопросов заказчику (gap-driven). | `understanding` | `documentation`,`governance` | BABOK Elicitation and Collaboration |
| A09 | `meeting-summary` | выход | Структурированное резюме встречи (решения, действия). | `documentation` | `governance` | BABOK Elicitation and Collaboration |
| A10 | `business-alignment-pack` | композит | Согласование бизнес-цели, scope, стейкхолдеров. | `understanding`+`documentation` | `solution_design`,`governance` | BABOK Strategy Analysis |
| A11 | `user-story` | выход | US в формате роль-цель-ценность + критерии. | `modeling` | `validation`,`documentation`,`impact_analysis` | BABOK RADD; IREB user story |
| A12 | `acceptance-criteria` | выход | Проверяемые критерии приёмки US/UC. | `modeling`,`validation` | `validation`,`release_readiness` | ISO/IEC/IEEE 29148 (verifiable) |
| A13 | `use-case` | выход | Use Case (формат Cockburn): акторы, потоки, исключения. | `modeling` | `validation`,`documentation` | BABOK RADD |
| A14 | `uml-bpmn-diagram` | выход | Диаграмма UML/BPMN (визуализация поведения/процесса). | `modeling` | `validation`,`documentation` | BABOK RADD (modelling) |
| A15 | `fr-section` | выход | Раздел 4 «Функциональные требования». | `documentation` | `validation`,`impact_analysis`,`reverse_requirements` | ISO/IEC/IEEE 29148; ГОСТ 34.602-2020 §4 |
| A16 | `constraints-section` | выход | Раздел 6 «Ограничения» (в т.ч. NFR). | `documentation` | `validation`,`solution_design` | ГОСТ 34.602-2020 §4; ISO/IEC 25010 |
| A17 | `technical-details-section` | выход | Раздел 7 «Технические детали»/список доработок. | `solution_design` | `validation`,`release_readiness` | ГОСТ 34.602-2020 §4-5 |
| A18 | `feature-spec-kk` | композит-документ | ФТ КК (Feature Specification Коммерческого слоя). | `documentation` | `validation`,`governance` | ГОСТ 34.602-2020 |
| A19 | `tz-contract` | композит-документ | ТЗ (договорная спецификация). | `documentation` | `validation`,`release_readiness` | **ГОСТ 34.602-2020** (не «-2015», см. ADR-003) |
| A20 | `defect-report` | выход | Отчёт о дефектах требований (привязка к пунктам). | `validation` | `governance`,`documentation` | ISO/IEC/IEEE 29148 (req characteristics) |
| A21 | `quality-summary` | выход | ТЗ-статистика / сводка качества. | `quality` | `governance`,`release_readiness` | ISO/IEC 25010 |
| A22 | `risk-register` | выход | Реестр рисков (вероятность, импакт, митигация, owner). | `risk_analysis` | `governance`,`release_readiness` | BABOK (Risk Analysis); ISO/IEC/IEEE 29148 |
| A23 | `impact-map` | выход | Карта влияния изменения на артефакты/компоненты. | `impact_analysis` | `governance`,`solution_design` | BABOK RLCM (Assess Changes) |
| A24 | `reverse-requirements` | выход | Реконструированные требования из существующей системы. | `reverse_requirements` | `validation`,`documentation` | BABOK RADD |
| A25 | `release-readiness-checklist` | выход | Чек-лист готовности к релизу. | `release_readiness` | `governance` | BABOK Solution Evaluation |
| A26 | `coverage-matrix` | композит | Матрица покрытия требований тендера (Tender Fit Pack). | `quality`+`validation` | `governance`,`release_readiness` | ISO/IEC/IEEE 29148 (traceability) |
| A27 | `traceability-matrix` | выход | Матрица трассируемости артефактов (вверх/вниз). | `governance`,`impact_analysis` | `validation`,`release_readiness` | ISO/IEC/IEEE 29148; BABOK RLCM (Trace) |
| A28 | `analysis-note` | выход | Аналитическая записка по research-вопросу. | `research` | `solution_design`,`governance` | BABOK Strategy Analysis |
| A29 | `status-backlog` | выход | Чек-лист статусов / бэклог управления. | `governance` | все процессы | BABOK RLCM |
| A30 | `bcreq` | композит | Многоуровневое требование BCREQ (см. ADR-009). | несколько процессов | `governance`,`release_readiness` | BABOK; ISO/IEC/IEEE 29148; ГОСТ 34.602-2020 |

> **Итого: 30 типов ≥ 20** (требование ФТ-1). Категории: вход (6), промежуточный
> (3), выход (15), композит/документ (6).

**Правило С4.** Каждый артефакт §4 **ДОЛЖЕН** иметь ≥1 производящую операцию
(кроме категории «вход») и ≥1 ребро `регулируется` со стандартом (кроме чисто
входных сырых данных A01-A04). Имя типа артефакта именуется по
[ADR-005](../docs/adr/005-artifact-team-naming.md).

## 5. Жизненный цикл артефакта (машина состояний)

```text
  raw ──ingestion──▶ draft ──▶ in-review ──▶ validated ──gate──▶ approved ──gate──▶ baselined/released
                       ▲           │              ▲                                        │
                       │           ▼              │                                        ▼
                    (правки)  needs-clarification ─┘                              superseded/archived
```

| Состояние | Значение | Допустимые переходы | Кто переводит |
| --- | --- | --- | --- |
| `raw` | сырой вход | → `draft` | внешний / `ingestion` |
| `draft` | черновик после первой операции | → `in-review`, → `needs-clarification` | `llm`/Исполнитель |
| `in-review` | на проверке/валидации | → `validated`, → `needs-clarification`, → `draft` | Исполнитель |
| `needs-clarification` | заблокирован: открытый вопрос, `⚠️ требует уточнения`, незавершённый подпроцесс | → `draft`, → `in-review` | любой участник |
| `validated` | прошёл аудит (критерии [ADR-004](../docs/adr/004-operations-taxonomy.md)) | → `approved`, → `needs-clarification` | `гибрид` + gate |
| `approved` | утверждён Пользователем | → `baselined`/`released`, → `superseded` | Человек (gate) |
| `baselined`/`released` | зафиксирован/выпущен | → `superseded`/`archived` | Человек (gate) |
| `superseded`/`archived` | заменён/выведен | терминальное | Человек |

**Правило С5.** Состояние `needs-clarification` — обязательный механизм для
незавершённых подпроцессов (ФТ-7). Артефакт в этом состоянии **НЕ ДОЛЖЕН**
блокировать остальной процесс: зависимые подпроцессы продолжаются с явной
пометкой зависимости (см. [ADR-009](../docs/adr/009-bcreq-formation-process.md)).

**Правило С6.** Переход в `validated`/`approved`/`baselined` **ДОЛЖЕН** проходить
human gate (модель «молчание = согласие»,
[ADR-0003](../docs/adr/0003-creative-mode-governance.md)).

## 6. Ведение реестра

- **Правило С7.** Добавление артефакта = новая строка §4 + (при необходимости)
  строка в [pr-ops/artifact-map.md](../pr-ops/artifact-map.md). Удалять
  типы **НЕ СЛЕДУЕТ** — для устаревших использовать состояние
  `superseded/archived`.
- **Правило С8.** Изменения онтологии, меняющие архитектуру/governance,
  **ДОЛЖНЫ** фиксироваться как ADR (требование
  [ADR-0003](../docs/adr/0003-creative-mode-governance.md)).

## Критерии соответствия (DoD)

- [ ] Каждая операция отнесена к исполнителю (§3) и имеет выходной gate.
- [ ] Реестр §4 содержит ≥20 типов (сейчас 30), у каждого выхода есть операция
      и стандарт.
- [ ] Машина состояний (§5) включает `needs-clarification` для незавершённых
      подпроцессов.
- [ ] Все внешние источники приведены полными URL (см. ADR-003).
- [ ] `python3 scripts/validate_issue_97_ontology_standards.py` проходит.

## Источники

- IIBA / BABOK Guide v3: <https://www.iiba.org/career-resources/a-business-analysis-professionals-foundation-for-success/babok/>
- BABOK Glossary: <https://www.iiba.org/career-resources/a-business-analysis-professionals-foundation-for-success/babok/glossary/>
- ISO/IEC/IEEE 29148:2018: <https://www.iso.org/standard/72089.html> · <https://standards.ieee.org/ieee/29148/6937/>
- ISO/IEC 25010:2011: <https://www.iso.org/standard/35733.html>
- ISO/IEC 25010:2023: <https://www.iso.org/standard/78176.html>
- ГОСТ 34.602-2020: <https://docs.cntd.ru/document/1200181804> · <https://allgosts.ru/01/040/gost_34.602-2020>
- ГОСТ 34.602-89: <https://standards.narod.ru/gosts/gost34/34-602-89.htm>
- ГОСТ 34.601-90: <https://docs.cntd.ru/document/1200006921>
- TM Forum SID: <https://www.tmforum.org/open-digital-architecture/information-framework-sid/>
- IREB CPRE Glossary: <https://cpre.ireb.org/en/downloads-and-resources/glossary>
