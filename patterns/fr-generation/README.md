---
status: draft
version: 0.1.0
updated: 2026-06-15
---

# FR Generation

## purpose

**Name.** FR Generation / Генерация функциональных требований.

**Intent.** Паттерн преобразует утверждённый бизнес-контекст, User Story, Use
Case, ограничения и решения в раздел 4 ФТ/ТЗ: атомарные, проверяемые
функциональные требования с понятной трассировкой к цели и сценарию.

Применяйте паттерн после сбора контекста и моделирования сценариев, когда нужно
получить рабочий черновик ФТ для клиентского заказа, внутренней доработки или
формального ТЗ.

Не применяйте паттерн для первичного discovery: если нет цели, акторов, границ
системы или Product Layer, сначала используйте
[`glossary-context-generation`](../glossary-context-generation/) и при
необходимости паттерны US/UC.

Полный URL репозитория: <https://github.com/G-Ivan-A/mango_ba_prompts>.

## process_stage

- **Process**: Формирование ФТ/ТЗ.
- **Operation**: `documentation`.
- **Pattern registry source of truth**:
  [docs/ba-processes/00-index.md](../../docs/ba-processes/00-index.md).
- **Taxonomy**: [docs/taxonomy.md](../../docs/taxonomy.md).
- **Prompt matrix**: [prompts/README.md](../../prompts/README.md).
- **Ecosystem map**: [docs/ba-ecosystem.md](../../docs/ba-ecosystem.md).
- **Related prompt implementations**:
  [`fr-documentation-stepwise.md`](../../prompts/fr-documentation-stepwise.md),
  [`fr-documentation-oneshot.md`](../../prompts/fr-documentation-oneshot.md).

## context_requirements

**Context.** Паттерн применяется после сбора бизнес-контекста, когда уже можно
отделить функциональное поведение от НФТ, ограничений и технических деталей.

- **Product Layer**: UCaaS, CCaaS, integration-project or another explicitly
  named Mango capability. Product Layer должен описывать затронутое поведение,
  границы системы, роли и известные ограничения.
- **Commercial Layer**:
  - `client-order`: формулировки ближе к договорному ТЗ, scope фиксируется
    жёстко, НФТ минимальны и только по ограничениям клиента.
  - `internal-product`: допустим более гибкий язык ФТ, нужны quality overlay,
    метрики, наблюдаемость и release-readiness hints.
  - `tender-rfp`: ФТ формируются только из covered/accepted требований; gaps и
    questions не превращаются в обещания.
- **Правила адаптации**: для ТЗ используйте однозначные "Система должна...";
  для ФТ КК допускайте бизнес-ориентированные формулировки; для внутренних
  доработок добавляйте trace to value и acceptance context.

Обязательные входы: Glossary Context Pack, цель, задачи, Product Layer,
Commercial Layer, User Story или Use Case при сценарной логике, ограничения и
известные решения. Стоп-фактор: нет source для функции или не согласована граница
actor/system.

## prompt_template

LLM-агностичный шаблон:

```markdown
Ты помогаешь бизнес-аналитику Mango оформить функциональные требования.

Вход:
- Glossary Context Pack: {{glossary_context}}
- User Story: {{user_story}}
- Use Case: {{use_case}}
- Product Layer: {{product_layer}}
- Commercial Layer: {{commercial_layer}}
- Ограничения и решения: {{constraints_and_decisions}}
- Целевой стиль: {{style_ft_or_tz}}

Сделай:
1. Проверь, хватает ли входа для раздела 4 ФТ. Если нет - перечисли блокеры.
2. Выдели функции системы, не смешивая их с НФТ и технической реализацией.
3. Сформулируй атомарные ФТ с нумерацией 4.x.
4. Для каждого ФТ укажи source: цель, US, UC, ограничение или решение.
5. Добавь краткие acceptance hints, если они помогают проверить требование.

Не делай:
- Не добавляй требования без source.
- Не переносите технические детали в раздел 4, если они относятся к разделу 7.
- Не смешивай варианты "может" и "должна" без явного статуса.
```

## quality_gates

**Forces.** Главные ограничения: не добавить неподтверждённый scope, не смешать
ФТ с технической реализацией и сохранить стиль, требуемый Commercial Layer.

- Каждое ФТ атомарно: один проверяемый результат поведения системы.
- У каждого ФТ есть source или пометка "требует уточнения"; неподтверждённые
  требования не попадают в финальный scope.
- НФТ, ограничения и технические детали не смешаны с функциональным поведением.
- Формулировки соответствуют Commercial Layer: договорная точность для ТЗ,
  бизнес-ясность для ФТ КК, evidence-first стиль для тендера.
- Термины соответствуют Glossary Context Pack.
- Результат готов для проверки через
  [`fr-validation`](../fr-validation/).

## examples

Минимальный few-shot пример:

- **Вход**: User Story о супервизоре, который получает уведомление при нарушении
  callback SLA.
- **Выход**: `4.1 Система должна определить нарушение SLA обратного звонка...`;
  `4.2 Система должна отправить уведомление супервизору...`; вопросы о канале
  уведомления остаются в backlog, если source отсутствует.

Расширенный пример: [examples/basic-example.md](examples/basic-example.md).

## output_schema

**Solution.** Результат паттерна - структурированный раздел 4 ФТ/ТЗ с
трассировкой к источникам и открытыми вопросами.

```markdown
# Section 4. Functional Requirements

## 4.1 <Requirement title>
- Requirement:
- Source:
- Actor / system boundary:
- Preconditions:
- Acceptance hints:
- Open questions:

## Traceability
| ФТ | Source | Product Layer | Commercial Layer | Статус |
```

## governance_rules

- Статус `draft` допускает применение в рабочем анализе; `canonical` требует
  human review и подтверждённого кейса применения.
- source of truth для связей процесс -> паттерн -> prompt находится в
  [docs/ba-processes/00-index.md](../../docs/ba-processes/00-index.md).
- Паттерн не меняет существующие prompt-файлы; он описывает аналитическую
  практику, а промпты в `prompts/` остаются исполняемыми реализациями.
- Для клиентских документов перед передачей наружу нужен ручной review БА и
  владельца коммерческого контекста.
- Версионирование следует SemVer из
  [ADR-002](../../docs/adr/002-pattern-standard.md).
