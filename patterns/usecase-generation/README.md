---
status: draft
version: 0.1.0
updated: 2026-06-15
---

# Use Case Generation

## purpose

**Name.** Use Case Generation / Генерация Use Case.

**Intent.** Паттерн помогает БА описать сценарий взаимодействия actor/system:
цель, акторы, предусловия, основной поток, альтернативы, исключения,
постусловия и открытые вопросы. Use Case становится мостом между бизнес-целью и
ФТ.

Применяйте паттерн, когда важны последовательность действий, ветвления,
исключения, границы системы или интеграционное взаимодействие.

Не применяйте паттерн для простой value statement без сценария; для этого
достаточно [`user-story-generation`](../user-story-generation/).

Полный URL репозитория: <https://github.com/G-Ivan-A/mango_ba_prompts>.

## process_stage

- **Process**: Формирование UC/US; дополнительно Формирование ФТ/ТЗ как вход для
  раздела 4.
- **Operation**: `modeling`.
- **Pattern registry source of truth**:
  [docs/ba-processes/00-index.md](../../docs/ba-processes/00-index.md).
- **Taxonomy**: [docs/taxonomy.md](../../docs/taxonomy.md).
- **Prompt matrix**: [prompts/README.md](../../prompts/README.md).
- **Ecosystem map**: [docs/ba-ecosystem.md](../../docs/ba-ecosystem.md).
- **Related prompt implementations**:
  [`uc-modeling-stepwise.md`](../../prompts/uc-modeling-stepwise.md),
  [`uc-modeling-oneshot.md`](../../prompts/uc-modeling-oneshot.md).

## context_requirements

**Context.** Паттерн применяется, когда требование нужно развернуть в сценарий
взаимодействия с явными границами actor/system.

- **Product Layer**: affected capability, actor/system boundary, roles, states,
  channels, integrations and known product constraints.
- **Commercial Layer**:
  - `client-order`: сценарий фиксирует границы поставки и исключения, важные для
    ТЗ.
  - `internal-product`: сценарий раскрывает value, edge cases, NFR triggers и
    impact.
  - `integration-project`: сценарий явно разделяет Mango system, external system
    and user actions.
- **Правила адаптации**: для договорного ТЗ не оставляйте "магические" шаги без
  акторов; для внутренних изменений добавляйте edge cases; для интеграций
  фиксируйте ownership каждого шага.

Обязательные входы: требование или User Story, actor, goal, Product Layer,
Commercial Layer, known preconditions and constraints. Стоп-фактор: нет
понимания, где заканчивается актор и начинается система.

## prompt_template

LLM-агностичный шаблон:

```markdown
Ты помогаешь бизнес-аналитику Mango оформить Use Case.

Вход:
- Требование или User Story: {{requirement_or_story}}
- Product Layer: {{product_layer}}
- Commercial Layer: {{commercial_layer}}
- Actors: {{actors}}
- Known constraints: {{constraints}}

Сделай:
1. Определи primary actor, supporting actors and system boundary.
2. Сформулируй goal, trigger, preconditions and postconditions.
3. Опиши main success scenario как последовательность actor/system steps.
4. Добавь alternative flows and exceptions.
5. Отметь вопросы, где не хватает source или owner decision.

Не делай:
- Не смешивай действия пользователя и системы в одном шаге.
- Не придумывай интеграционные API или статусы без source.
- Не переносите технические детали в UC, если они нужны только разделу 7.
```

## quality_gates

**Forces.** Главные ограничения: не смешать действия актора и системы, не
додумать альтернативы без source и не превратить Use Case в технический дизайн.

- Primary actor, system boundary and goal указаны явно.
- Main flow содержит проверяемые шаги и не смешивает actor/system actions.
- Альтернативы и исключения привязаны к конкретным шагам основного потока.
- Preconditions and postconditions не противоречат Product Layer.
- Commercial Layer влияет на глубину исключений и договорные boundaries.
- Вопросы и assumptions не маскируются под подтверждённые шаги.

## examples

Минимальный few-shot пример:

- **Вход**: супервизор контролирует просроченные callback-задачи.
- **Выход**: Use Case "Просмотреть просроченные обратные звонки" с actor
  "Супервизор", precondition "есть задачи с контрольным сроком", main flow
  "открыть список -> система показывает просрочки -> супервизор фильтрует".

Расширенный пример: [examples/basic-example.md](examples/basic-example.md).

## output_schema

**Solution.** Результат паттерна - Use Case по Cockburn-like структуре,
пригодный как вход для ФТ, диаграмм or validation.

```markdown
# Use Case

## Overview
- Name:
- Primary actor:
- Supporting actors:
- Goal:
- Product Layer:
- Commercial Layer:

## Preconditions

## Trigger

## Main success scenario
1. Actor:
2. System:

## Alternative flows
| ID | Step | Flow |

## Exceptions
| ID | Step | Condition | System response |

## Postconditions

## Open questions
```

## governance_rules

- Статус `draft` допускает применение как шаблон сценариев; `canonical` требует
  review и подтверждённого использования.
- source of truth для связей процесс -> паттерн -> prompt находится в
  [docs/ba-processes/00-index.md](../../docs/ba-processes/00-index.md).
- Use Case не должен утверждать технические интерфейсы без Product/SME review.
- Архивные генераторы Use Case остаются в `prompts/archive/`; активные
  реализации перечислены выше.
- Версионирование следует SemVer из
  [ADR-002](../../docs/adr/002-pattern-standard.md).
