---
id: RFC-243
status: draft
title: "RFC-243: предложение по БА-процессам и observability"
author: "OpenAI Codex"
created: 2026-06-25
updated: 2026-06-25
layer: L3
type: rfc
related_contracts:
  - "governance/rfc-generation-contract.md"
  - "governance/rfc-process.md"
  - "governance/bcreq-fr-generation-contract.md"
  - "runs/CONTRACT.md"
  - "standards/executable-contract-standard.md"
target_artifacts:
  - "docs/ba-processes/00-index.md"
  - "docs/ba-processes/00-index.executable.md"
  - "standards/ba-ontology.md"
  - "governance/bcreq-fr-generation-contract.md"
  - "runs/CONTRACT.md"
  - "kb/operation-prompt-mapping/registry.json"
  - "runs/REGISTRY.md"
  - "runs/stats/by-process.md"
  - "runs/stats/by-type.md"
---

# RFC-243: предложение по БА-процессам и observability

Статус этого документа - `draft`. RFC-243 является предложением, а не
реализацией: он не меняет стандарты, контракты, prompt assets, run metadata,
продуктовые документы или `kb/operation-prompt-mapping/registry.json`.

## 1. Context and motivation

Issue [#243](https://github.com/G-Ivan-A/mango_ba_prompts/issues/243) попросил
зафиксировать согласованные решения из цепочки исследований
`research -> rfc/adr -> standard -> artifact` и подготовить спринт дальнейшей
реализации. Входами для RFC являются:

- A3:
  [`docs/analysis/2026-06-25-runs-observability-research.md`](../../docs/analysis/2026-06-25-runs-observability-research.md)
  - исследование трассируемости prompt usage, версий и lineage в `runs/`.
- A4:
  [`docs/analysis/2026-06-25-bcreq-fr-contract-process-analysis.md`](../../docs/analysis/2026-06-25-bcreq-fr-contract-process-analysis.md)
  - анализ применения BCREQ-FR как монолитного L1-контракта вместо
  последовательности операций.
- PR #234:
  [`docs/analysis/2026-06-25-ba-processes-industry-analysis.md`](../../docs/analysis/2026-06-25-ba-processes-industry-analysis.md)
  - анализ BA-процессов, артефактов и индустриальных практик
  (<https://github.com/G-Ivan-A/mango_ba_prompts/pull/234>).
- Текущие артефакты процесса:
  [`docs/ba-processes/00-index.md`](../../docs/ba-processes/00-index.md),
  [`docs/ba-processes/00-index.executable.md`](../../docs/ba-processes/00-index.executable.md),
  [`governance/bcreq-fr-generation-contract.md`](../bcreq-fr-generation-contract.md),
  [`runs/CONTRACT.md`](../../runs/CONTRACT.md) и
  [`standards/executable-contract-standard.md`](../../standards/executable-contract-standard.md).

Product docs для этого RFC не применяются: предложение меняет governance,
таксономию БА-артефактов, mapping и observability, но не описывает поведение
конкретного продукта Mango.

### Почему RFC, а не ADR

RFC выбран потому, что задача формулирует проектное предложение "что изменить":
процессную карту, BA ontology, будущий L2 registry, поля контрактов и поля run
metadata. ADR нужен после review, если человек принимает архитектурное решение
или необратимую границу владения. Пока это не принятое решение, а проверяемое
предложение.

### Причина нарушения формата в PR #244

Причина нарушения формата: первичная версия RFC прочитала
`machine_readable_shape` и `yaml_blocks_required` из L1-контракта
[`governance/rfc-generation-contract.md`](../rfc-generation-contract.md) как
требование писать каждый раздел L3 RFC в YAML. Это была ошибка интерпретации:
L1-контракт описывает проверяемую структуру, но L3 RFC должен быть
Markdown-документом с YAML frontmatter. Машиночитаемые вставки нужны для
трассируемости и validation checks; они не должны заменять человеческий текст
RFC.

Исправленная версия сохраняет YAML только как compact machine-readable inserts:
traceability index, impact, implementation plan и canonical criteria. Контекст,
проблемы, предложение, альтернативы и rationale читаются как обычный Markdown.

## 2. Problem

| ID | Проблема | Источник | Последствие |
| --- | --- | --- | --- |
| `RFC-243-P1` | Решения из A3/A4/PR #234 не закреплены в RFC/ADR-артефакте. | Issue #243; A3; A4; PR #234 | Цепочка `research -> rfc/adr -> standard -> artifact` заблокирована. |
| `RFC-243-P2` | Atomic/composite taxonomy для BA artifacts не является canonical. | PR #234; `standards/ba-ontology.md` | API specification, RTM entry, FRD/SRS и BCREQ type semantics остаются неоднозначными. |
| `RFC-243-P3` | Верхний уровень операций смешан с проектной декомпозицией. | `docs/ba-processes/00-index.md`; PR #234 | Текущие 13 операций полезны, но не дают первого BABOK-compatible слоя. |
| `RFC-243-P4` | L1-контракты не декларируют, какие BA operations они исполняют. | A4; `governance/bcreq-fr-generation-contract.md` | BCREQ-FR выглядит как монолит, а не как traceable operation sequence. |
| `RFC-243-P5` | Runs не фиксируют prompt_id, prompt version, model settings, result и previous_run_id. | A3; `runs/CONTRACT.md` | Нельзя восстановить prompt lineage и объяснить различия между проходами. |
| `RFC-243-P6` | Реализация не разбита на issue-backed sprint с зависимостями. | Issue #243; `governance/BACKLOG.md` | Стандарты, контракты и статистика могут изменяться вне правильного порядка. |
| `RFC-243-P7` | Первая версия RFC была YAML-heavy и плохо читалась человеком. | Issue #245; `governance/rfc-generation-contract.md` | L3 proposal стал похож на L1 contract и нарушил требование "Markdown with YAML frontmatter". |

## 3. Proposal

RFC-243 фиксирует согласованные решения 1-5 из issue #243 и добавляет
implementation boundary: этот PR только оформляет proposal, а downstream changes
идут отдельными задачами после review.

| ID | Предложение | Покрывает |
| --- | --- | --- |
| `RFC-243-R1` | Оставить RFC-243 L3 RFC draft до human review; ADR создавать только если reviewer просит зафиксировать принятое архитектурное решение. | `RFC-243-P1` |
| `RFC-243-R2` | Принять atomic BA artifacts: Singular requirement, User Story, Use Case, Business Rule, Glossary term, API specification (OpenAPI/TMF Open API), RTM entry. Атомар = один источник, один владелец, одна проверка. | `RFC-243-P2` |
| `RFC-243-R3` | Принять composite artifacts: BRD, FRD/SRS, RFP Response/Bid Requirements. Классифицировать BCREQ-FR как `type: frd`, BCREQ-SR как `type: srs`. | `RFC-243-P2` |
| `RFC-243-R4` | Принять 6 BABOK-compatible operations как верхний слой: Elicitation, Analysis, Documentation, Validation, Verification, Management. Текущие 13 операций оставить project-specific suboperations. | `RFC-243-P3` |
| `RFC-243-R5` | Ввести L2 registry `kb/operation-prompt-mapping/registry.json` с key edge `operation_id -> prompt_id@version`. | `RFC-243-P4`, `RFC-243-P5` |
| `RFC-243-R6` | В будущих миграциях добавить `applied_operations` в generation contracts, `applied_prompts` и `previous_run_id` в runs. | `RFC-243-P4`, `RFC-243-P5` |
| `RFC-243-R7` | Реализовывать в порядке: сверка `00-index.md`, затем BA ontology, затем L2 registry, затем поля L1 contracts и runs. | `RFC-243-P6` |
| `RFC-243-R8` | Вести внедрение через issue-backed sprint backlog с волнами, priorities и dependencies. | `RFC-243-P6` |
| `RFC-243-R9` | Сохранить формат RFC как readable Markdown with YAML frontmatter; YAML в теле использовать только для compact machine-readable inserts. | `RFC-243-P7` |

Машиночитаемая вставка ниже нужна для проверки связей proposal -> problem и
target artifacts. Она не заменяет таблицу предложений.

```yaml
proposal_traceability:
  RFC-243-R1: {problem_ids: [RFC-243-P1], target_artifacts: ["governance/rfc/ba-processes-observability-implementation-proposal.md"]}
  RFC-243-R2: {problem_ids: [RFC-243-P2], target_artifacts: ["standards/ba-ontology.md"]}
  RFC-243-R3: {problem_ids: [RFC-243-P2], target_artifacts: ["standards/ba-ontology.md", "governance/bcreq-fr-generation-contract.md"]}
  RFC-243-R4: {problem_ids: [RFC-243-P3], target_artifacts: ["docs/ba-processes/00-index.md", "docs/ba-processes/00-index.executable.md"]}
  RFC-243-R5: {problem_ids: [RFC-243-P4, RFC-243-P5], target_artifacts: ["kb/operation-prompt-mapping/registry.json"]}
  RFC-243-R6: {problem_ids: [RFC-243-P4, RFC-243-P5], target_artifacts: ["governance/bcreq-fr-generation-contract.md", "runs/CONTRACT.md"]}
  RFC-243-R7: {problem_ids: [RFC-243-P6], target_artifacts: ["governance/BACKLOG.md"]}
  RFC-243-R8: {problem_ids: [RFC-243-P6], target_artifacts: ["governance/BACKLOG.md"]}
  RFC-243-R9: {problem_ids: [RFC-243-P7], target_artifacts: ["governance/rfc/ba-processes-observability-implementation-proposal.md"]}
```

## 4. Alternatives considered

| ID | Альтернатива | Решение | Причина |
| --- | --- | --- | --- |
| `RFC-243-A1` | Сразу написать ADR. | Not selected. | Issue #243 требует proposal across governance surfaces; ADR преждевременно фиксирует accepted decision. |
| `RFC-243-A2` | Реализовать стандарты и контракты прямо в issue #243. | Not selected. | Issue #243 явно запрещает implementation до согласования RFC/ADR. |
| `RFC-243-A3` | Оставить mapping process -> operation -> prompt только в `00-index.md`. | Not selected. | Prose удобен для навигации, но не подходит как L2 registry для validators и run metadata. |
| `RFC-243-A4` | Встроить prompt mapping в каждый L1 contract. | Not selected. | Это дублирует mapping, усиливает drift и нарушает границу L1 self-contained contract + L2 reusable data. |
| `RFC-243-A5` | Оставить RFC-243 в YAML-heavy форме. | Rejected. | Issue #245 подтвердил, что такой формат плохо читается и смешивает L1 contract style с L3 RFC style. |

## 5. Rationale

A3 показывает, что run observability требует prompt IDs, версий, lineage и
связи с результатом. Поэтому `RFC-243-R5` и `RFC-243-R6` вводят registry и поля
execution metadata, но не создают их в этом PR.

A4 показывает, что BCREQ-FR применяется как крупный L1-монолит. Чтобы сделать
его traceable, контракту нужен уровень applied BA operations, а конкретные
prompt versions должны фиксироваться на уровне run.

PR #234 показывает, что индустриальная модель различает atomic artifacts,
composite documents и top-level BA operations. Поэтому `RFC-243-R2`,
`RFC-243-R3` и `RFC-243-R4` не заменяют текущие 13 операций, а вводят над ними
совместимый верхний слой.

Порядок из `RFC-243-R7` нужен потому, что contracts и runs не должны ссылаться
на operation IDs до того, как процессная карта и BA ontology дадут этим IDs
устойчивый смысл.

Форматная правка `RFC-243-R9` нужна потому, что L3 RFC служит review artifact.
Машиночитаемые блоки остаются только там, где они дают проверяемую
трассируемость: proposal links, impact, implementation plan и canonical
criteria.

## 6. Impact

RFC-243 не требует ADR сейчас, потому что не принимает архитектурное решение.
Он требует будущих standard/contract changes, если станет canonical: изменятся
BA ontology, process documentation, mapping registry, generation contract fields
и run metadata rules. Переходные правила RFC -> ADR или RFC -> standard этот
документ не определяет.

```yaml
impact:
  requires_adr: false
  adr_reason: "RFC-243 is a reviewable proposal; no irreversible architecture decision is accepted here."
  requires_standard: true
  standard_reason: "Canonical RFC-243 requires later normative updates to BA ontology, process docs, contract fields, registry data, and run metadata."
  target_artifacts: ["docs/ba-processes/00-index.md", "docs/ba-processes/00-index.executable.md", "standards/ba-ontology.md", "governance/bcreq-fr-generation-contract.md", "runs/CONTRACT.md", "kb/operation-prompt-mapping/registry.json", "runs/REGISTRY.md", "runs/stats/by-process.md", "runs/stats/by-type.md"]
  affected_contracts: ["governance/bcreq-fr-generation-contract.md", "runs/CONTRACT.md"]
  migration_or_backfill: ["Add new metadata fields before backfill.", "Backfill prompt lineage only when source evidence exists."]
  risks: ["13-operation map can be misread as replaced.", "`type: contract` must not be reused for BCREQ-FR/BCREQ-SR document type classification.", "Fork tracking issues may need upstream recreation."]
```

## 7. Implementation plan

План ниже не выполняется в этом PR. Он задает порядок downstream work после
review. Fork issue URLs сохранены из PR #244, потому что upstream issue/label
creation был заблокирован правами токена.

```yaml
implementation_plan:
  status: "proposal_only"
  steps:
    - {id: RFC-243-STEP-1, wave: 0, action: "decision: зафиксировать RFC-243 governance proposal", issue: "https://github.com/konard/G-Ivan-A-mango_ba_prompts/issues/1", depends_on: []}
    - {id: RFC-243-STEP-2, wave: 1, action: "implementation: сверить 00-index.md с BABOK-операциями", issue: "https://github.com/konard/G-Ivan-A-mango_ba_prompts/issues/3", depends_on: ["https://github.com/konard/G-Ivan-A-mango_ba_prompts/issues/1"]}
    - {id: RFC-243-STEP-3, wave: 1, action: "implementation: обновить БА-онтологию для atomic-composite taxonomy", issue: "https://github.com/konard/G-Ivan-A-mango_ba_prompts/issues/4", depends_on: ["https://github.com/konard/G-Ivan-A-mango_ba_prompts/issues/1", "https://github.com/konard/G-Ivan-A-mango_ba_prompts/issues/3"]}
    - {id: RFC-243-STEP-4, wave: 2, action: "implementation: создать L2-реестр operation-prompt mapping", issue: "https://github.com/konard/G-Ivan-A-mango_ba_prompts/issues/2", depends_on: ["https://github.com/konard/G-Ivan-A-mango_ba_prompts/issues/1"]}
    - {id: RFC-243-STEP-5, wave: 2, action: "implementation: добавить applied_operations в generation contracts", issue: "https://github.com/konard/G-Ivan-A-mango_ba_prompts/issues/5", depends_on: ["https://github.com/konard/G-Ivan-A-mango_ba_prompts/issues/2", "https://github.com/konard/G-Ivan-A-mango_ba_prompts/issues/3"]}
    - {id: RFC-243-STEP-6, wave: 2, action: "implementation: добавить applied_prompts и lineage в runs contract", issue: "https://github.com/konard/G-Ivan-A-mango_ba_prompts/issues/6", depends_on: ["https://github.com/konard/G-Ivan-A-mango_ba_prompts/issues/2"]}
    - {id: RFC-243-STEP-7, wave: 3, action: "implementation: обновить валидаторы и статистику под трассируемость", issue: "https://github.com/konard/G-Ivan-A-mango_ba_prompts/issues/7", depends_on: ["https://github.com/konard/G-Ivan-A-mango_ba_prompts/issues/5", "https://github.com/konard/G-Ivan-A-mango_ba_prompts/issues/6"]}
    - {id: RFC-243-STEP-8, wave: 3, action: "research: оценить eTOM/SID как доменные БА-артефакты", issue: "https://github.com/konard/G-Ivan-A-mango_ba_prompts/issues/8", depends_on: ["https://github.com/konard/G-Ivan-A-mango_ba_prompts/issues/4"]}
  validation:
    - "python3 scripts/validate_issue_243_ba_processes_observability_rfc.py"
    - "python3 scripts/validate_issue_245_rfc_243_markdown_format.py"
```

## 8. Canonical criteria

Критерии ниже проверяют, что RFC можно переводить в canonical без скрытой
реализации. Каждый критерий связан хотя бы с одним proposal ID.

```yaml
canonical_criteria:
  - {id: RFC-243-C1, statement: "Reviewer accepts RFC artifact type or requests ADR conversion.", verifies: [RFC-243-R1], check: "Manual review."}
  - {id: RFC-243-C2, statement: "Atomic artifact set and definition are accepted.", verifies: [RFC-243-R2], check: "Review confirms atomic list."}
  - {id: RFC-243-C3, statement: "Composite hierarchy and BCREQ-FR/BCREQ-SR classification are accepted.", verifies: [RFC-243-R3], check: "Review confirms document types."}
  - {id: RFC-243-C4, statement: "Six-operation BABOK layer and 13-operation decomposition are accepted.", verifies: [RFC-243-R4], check: "Review confirms operation layer."}
  - {id: RFC-243-C5, statement: "operation_id -> prompt_id@version registry is accepted as a future target.", verifies: [RFC-243-R5], check: "Review confirms registry path."}
  - {id: RFC-243-C6, statement: "`applied_operations`, `applied_prompts`, and `previous_run_id` are accepted as future fields.", verifies: [RFC-243-R6], check: "Review confirms metadata boundary."}
  - {id: RFC-243-C7, statement: "Sprint backlog order and issue-backed sequence are accepted.", verifies: [RFC-243-R7, RFC-243-R8], check: "Review confirms waves and dependencies."}
  - {id: RFC-243-C8, statement: "RFC-243 remains readable Markdown with compact machine-readable inserts.", verifies: [RFC-243-R9], check: "python3 scripts/validate_issue_245_rfc_243_markdown_format.py"}
```
