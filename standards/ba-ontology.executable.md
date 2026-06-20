---
status: draft
version: 0.2
updated: 2026-06-20
ai-generated: true
type: contract
layer: executable
full_version: "standards/ba-ontology.md"
related_standard: "cascading-context-loading-standard.md"
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/125"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/127"
---

# BA Ontology Standard — executable layer

Load this file first for ontology decisions. Do not load
`standards/ba-ontology.md` unless one escalation trigger below is true.

## Escalation triggers

- TRIGGER-1: пользователь явно просит полный стандарт, источники, rationale,
  нормативные ссылки или полный реестр артефактов с определениями.
- TRIGGER-2: нужно редактировать, валидировать или синхронизировать
  `standards/ba-ontology.md`.
- TRIGGER-3: текущая задача требует точной формулировки правила С1-С8/W1-W3,
  определения A01-A31, таблицы жизненного цикла или источников.
- TRIGGER-4: краткая онтология ниже конфликтует с ADR-003,
  `docs/ba-processes/00-index.executable.md`, `docs/taxonomy.md` или другим
  стандартом.

Если ни один триггер не сработал, применяй правила ниже.

## Execute

### Scope

Онтология связывает сущности БА: операции, процессы, подпроцессы, артефакты,
исполнителей, gates, направления разработки, стандарты и состояния жизненного
цикла. Реализующий слой регулируется `standards/pattern-standard.md` и
`standards/prompt-standard.md`.

### Entities

| Entity | Key / source of truth |
| --- | --- |
| Операция | `snake_case`, источник: `docs/taxonomy.md` |
| Процесс | 1-9, источник: `docs/taxonomy.md` и `docs/ba-processes/00-index.executable.md` |
| Подпроцесс | `<process>.<step>`, источник: строки process map |
| Артефакт | `kebab-case`, источник: registry A01-A31 |
| Исполнитель | `человек`, `llm`, `гибрид` |
| Gate | контрольная точка подпроцесса |
| Направление разработки | `client-order`, `internal-product`, `tender-rfp`, `technical-debt`, `integration-project`, `release-readiness` |
| Стандарт | standards/* |
| Уровень требования | `requirement_level` ∈ `business`, `user`, `functional`, `non-functional` |
| Состояние ЖЦ | `raw`, `draft`, `in-review`, `needs-clarification`, `validated`, `approved`, `baselined/released`, `superseded/archived` |

### Edges

- R1 `декомпозируется в`: Процесс -> Подпроцесс.
- R2 `применяет`: Подпроцесс -> Операция.
- R3 `выполняется`: Операция -> Исполнитель.
- R4 `потребляет`: Операция -> входной Артефакт.
- R5 `производит`: Операция -> выходной Артефакт.
- R6 `соответствует`: Операция -> BABOK knowledge area.
- R7 `регулируется`: Артефакт -> Стандарт.
- R8 `классифицируется`: Требование -> Domain -> Capability -> Feature -> Atomic Function.
- R9 `имеет состояние`: Артефакт -> lifecycle state.
- R10 `реализует`: Паттерн -> Операция.
- R11 `исполняет`: Промпт -> Паттерн.
- R12 `трассируется`: Артефакт -> Артефакт.
- R13 `имеет уровень требования`: Артефакт-требование -> `requirement_level`.
- R14 `порождает / ограничивает`: `business-rule` -> Артефакт-требование.

### Requirement level

`requirement_level` — ортогональная ось C1 из Hub RFC:

| Value | Meaning |
| --- | --- |
| `business` | бизнес-цель, outcome, KPI, причина изменения |
| `user` | потребность роли, пользовательский сценарий, observable value |
| `functional` | поведение системы, функция, обработка события |
| `non-functional` | качество, SLA, безопасность, производительность, ограничение |

Не заменяй Domain->Capability->Feature->Atomic Function и не выводи уровень
только из глубины BCREQ-дерева.

### Executor classification

| Операция | Исполнитель | Gate |
| --- | --- | --- |
| `ingestion` | `llm` | смысл сохранён |
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
| `risk_analysis` | `человек` | high/compliance risks имеют owner-review |
| `release_readiness` | `человек` | acceptance/rollback/comms подтверждены |

Операция со значением `человек` или `гибрид` не переводит артефакт в
`validated`, `approved` или `released` без human gate.

### Artifact registry keys

Используй эти коды как допустимые типы, а full-стандарт открывай только если
нужно точное определение:

`A01 asr-transcript-raw`, `A02 transcript-clean`, `A03 customer-letter`,
`A04 meeting-notes`, `A05 raw-requirement`, `A06 tender-spec-external`,
`A07 task-glossary`, `A08 customer-questions`, `A09 meeting-summary`,
`A10 business-alignment-pack`, `A11 user-story`, `A12 acceptance-criteria`,
`A13 use-case`, `A14 uml-bpmn-diagram`, `A15 fr-section`,
`A16 constraints-section`, `A17 technical-details-section`,
`A18 feature-spec-kk`, `A19 tz-contract`, `A20 defect-report`,
`A21 quality-summary`, `A22 risk-register`, `A23 impact-map`,
`A24 reverse-requirements`, `A25 release-readiness-checklist`,
`A26 coverage-matrix`, `A27 traceability-matrix`, `A28 analysis-note`,
`A29 status-backlog`, `A30 bcreq`, `A31 business-rule`.

`business-rule` имеет одну категорию: `fact`, `constraint`,
`operation-activator`, `inference` или `computation`. Правило трассируется к
функции, ограничению, BCREQ или разделу ФТ, который оно порождает или ограничивает.

### Lifecycle

```text
raw -> draft -> in-review -> validated -> approved -> baselined/released
              \-> needs-clarification -> draft/in-review
baselined/released -> superseded/archived
```

`needs-clarification` не блокирует весь процесс: зависимые подпроцессы могут
идти дальше с явной пометкой зависимости.

### Maintenance rules

- Новая операция или процесс сначала появляется в `docs/taxonomy.md`, затем в
  онтологии.
- Новый тип артефакта добавляется в registry A01-A30+ и при необходимости в
  `governance/artifact-map.md`.
- Типы артефактов не удаляются молча: для устаревших используй
  `superseded/archived`.
- Архитектурные/governance изменения онтологии фиксируются ADR.

## Issue #127 source links

- Hub RFC `requirements-engineering-ai-era-2026.md`:
  <https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/73e94c6e69995ccf9e746c19d9c18359971285f2/research/mango/requirements-engineering-ai-era-2026.md>
- Hub RFC `ai-classifications-formalization-2026-06.md`:
  <https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/73e94c6e69995ccf9e746c19d9c18359971285f2/research/mango/ai-classifications-formalization-2026-06.md>
