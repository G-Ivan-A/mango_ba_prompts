---
status: draft
version: 0.1.0
updated: 2026-06-15
---

# User Story Generation

## purpose

**Name.** User Story Generation / Генерация User Story.

**Intent.** Паттерн помогает БА преобразовать исходное требование или идею в
User Story с ролью, потребностью, ценностью, acceptance criteria и вопросами,
которые нужно закрыть до ФТ/ТЗ.

Применяйте паттерн на раннем бизнес-слое, когда нужно быстро согласовать
ценность, actor, capability и критерии приемки до детализации сценария или
раздела 4 ФТ.

Не применяйте паттерн для описания длинного сценария с ветвлениями: если важны
preconditions, main flow и alternative flows, используйте
[`usecase-generation`](../usecase-generation/).

Полный URL репозитория: <https://github.com/G-Ivan-A/mango_ba_prompts>.

## process_stage

- **Process**: Формирование UC/US; дополнительно Формирование ФТ/ТЗ как
  предварительный бизнес-слой.
- **Operation**: `modeling`.
- **Pattern registry source of truth**:
  [docs/ba-processes/00-index.md](../../docs/ba-processes/00-index.md).
- **Taxonomy**: [docs/taxonomy.md](../../docs/taxonomy.md).
- **Prompt matrix**: [prompts/README.md](../../prompts/README.md).
- **Ecosystem map**: [docs/ba-ecosystem.md](../../docs/ba-ecosystem.md).
- **Related prompt implementations**:
  [`us-modeling-stepwise.md`](../../prompts/us-modeling-stepwise.md),
  [`us-modeling-oneshot.md`](../../prompts/us-modeling-oneshot.md).

## context_requirements

**Context.** Паттерн применяется на раннем бизнес-слое, когда нужно понять
ценность и критерии приемки до Use Case или ФТ.

- **Product Layer**: capability, actor, channel, system boundary and affected
  product area. Если capability не подтверждена, story получает статус draft.
- **Commercial Layer**:
  - `client-order`: story фиксирует ценность заказчика и границы scope, но не
    подменяет договорное ТЗ.
  - `internal-product`: story связывается с value, metrics, roadmap и release
    hypothesis.
  - `tender-rfp`: story используется как внутренний способ понять требование, а
    не как ответ в тендер без evidence.
- **Правила адаптации**: для клиентского заказа добавляйте acceptance context,
  влияющий на договорный scope; для внутренней доработки добавляйте metric/value;
  для интеграции явно указывайте external actor и system boundary.

Обязательные входы: исходное требование, stakeholder or actor, цель, Product
Layer, Commercial Layer и known constraints. Стоп-фактор: невозможно назвать
роль или ценность без домыслов.

## prompt_template

LLM-агностичный шаблон:

```markdown
Ты помогаешь бизнес-аналитику Mango оформить User Story.

Вход:
- Сырой запрос или требование: {{requirement}}
- Product Layer: {{product_layer}}
- Commercial Layer: {{commercial_layer}}
- Actor / stakeholder: {{actor}}
- Known constraints: {{constraints}}

Сделай:
1. Сформулируй одну основную User Story в формате "Как <роль>, я хочу <цель>,
   чтобы <ценность>".
2. Если в запросе несколько целей, предложи декомпозицию на несколько stories.
3. Добавь acceptance criteria в формате Given/When/Then или checklist.
4. Проверь INVEST и отметь слабые места.
5. Сформируй open questions без добавления неподтверждённых требований.

Не делай:
- Не смешивай actor и систему.
- Не превращай техническую реализацию в бизнес-ценность.
- Не скрывай, если story слишком крупная.
```

## quality_gates

**Forces.** Главные ограничения: не заменить бизнес-ценность техническим
решением, не спрятать несколько целей в одну story и не выдать draft за scope.

- Роль, цель и ценность различимы и не дублируют друг друга.
- Story описывает бизнес-ценность, а не только техническое действие.
- Acceptance criteria проверяемы.
- Product Layer и Commercial Layer указаны явно.
- Несколько независимых целей декомпозированы.
- Открытые вопросы не подменены предположениями.

## examples

Минимальный few-shot пример:

- **Вход**: "Нужно, чтобы супервизор видел просроченные обратные звонки".
- **Выход**: "Как супервизор контакт-центра, я хочу видеть просроченные
  обратные звонки, чтобы контролировать выполнение SLA"; acceptance criteria
  отделяют список просрочек, фильтр по оператору и статус обработки.

Расширенный пример: [examples/basic-example.md](examples/basic-example.md).

## output_schema

**Solution.** Результат паттерна - User Story Pack с одной или несколькими
stories, acceptance criteria, INVEST check and open questions.

```markdown
# User Story Pack

## Story
As a / Как:
I want / Я хочу:
So that / Чтобы:

## Acceptance criteria
- Given ...
- When ...
- Then ...

## INVEST check
| Criterion | Status | Notes |

## Product and commercial context
- Product Layer:
- Commercial Layer:

## Open questions
| Question | Owner | Blocks |
```

## governance_rules

- Статус `draft` допускает применение как шаблон моделирования; `canonical`
  требует review и подтверждённого использования.
- source of truth для связей процесс -> паттерн -> prompt находится в
  [docs/ba-processes/00-index.md](../../docs/ba-processes/00-index.md).
- Story не является договорным обязательством, пока не переведена в ФТ/ТЗ и не
  прошла human review.
- Архивные генераторы User Story остаются в `prompts/archive/`; активные
  реализации перечислены выше.
- Версионирование следует SemVer из
  [ADR-002](../../docs/adr/002-pattern-standard.md).
