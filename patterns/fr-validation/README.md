---
status: draft
version: 0.1.0
updated: 2026-06-15
---

# FR Validation

## purpose

**Name.** FR Validation / Валидация функциональных требований и ТЗ.

**Intent.** Паттерн помогает БА проверить черновик ФТ/ТЗ на полноту,
непротиворечивость, тестируемость, соответствие Product Layer и Commercial Layer,
а также выделить дефекты, вопросы и риски до передачи документа дальше.

Применяйте паттерн после генерации или ручного написания ФТ, при ревью тендерных
требований, перед согласованием клиентского ТЗ или перед передачей внутренней
доработки в разработку.

Не применяйте паттерн как способ тихо переписать scope: любые новые требования,
найденные во время проверки, должны попасть в отдельный backlog или вернуться в
паттерн [`fr-generation`](../fr-generation/) после source review.

Полный URL репозитория: <https://github.com/G-Ivan-A/mango_ba_prompts>.

## process_stage

- **Process**: Валидация ФТ/ТЗ; дополнительно Формирование ФТ/ТЗ и Анализ
  тендерных ТЗ как review gate.
- **Operation**: `validation` с quality overlay из операции `quality`.
- **Pattern registry source of truth**:
  [docs/ba-processes/00-index.md](../../docs/ba-processes/00-index.md).
- **Taxonomy**: [docs/taxonomy.md](../../docs/taxonomy.md).
- **Prompt matrix**: [prompts/README.md](../../prompts/README.md).
- **Ecosystem map**: [docs/ba-ecosystem.md](../../docs/ba-ecosystem.md).
- **Related prompt implementations**:
  [`fr-validation-stepwise.md`](../../prompts/fr-validation-stepwise.md),
  [`fr-validation-oneshot.md`](../../prompts/fr-validation-oneshot.md),
  [`fr-validation-legacy.md`](../../prompts/fr-validation-legacy.md).

## context_requirements

**Context.** Паттерн применяется как review gate для готового или почти готового
черновика, а не как генератор нового scope.

- **Product Layer**: затронутые Mango capabilities, роли, каналы, интеграции,
  ограничения платформы и известные owner decisions.
- **Commercial Layer**:
  - `client-order`: проверять договорной scope, формулировки "должна",
    ответственность сторон, acceptance, SLA/ИБ/ПДн только в границах заказа.
  - `internal-product`: проверять value, NFR, метрики, observability, release и
    support impact.
  - `tender-rfp`: проверять evidence, coverage/gap, no-bid triggers,
    неоднозначные формулировки и вопросы для Q&A.
- **Правила адаптации**: severity дефектов зависит от слоя. Для клиентского ТЗ
  критичны двусмысленность и scope creep; для internal-product - неполный NFR и
  impact; для тендера - отсутствие evidence и риск обещаний без покрытия.

Обязательные входы: черновик ФТ/ТЗ, исходный контекст или source excerpts,
шаблон/стиль документа, Product Layer, Commercial Layer и известные ограничения.
Стоп-фактор: невозможно отличить дефект от нового требования из-за отсутствия
source.

## prompt_template

LLM-агностичный шаблон:

```markdown
Ты помогаешь бизнес-аналитику Mango проверить ФТ/ТЗ.

Вход:
- Черновик документа: {{draft_requirements}}
- Source context: {{source_context}}
- Product Layer: {{product_layer}}
- Commercial Layer: {{commercial_layer}}
- Шаблон или expected structure: {{document_structure}}
- Known decisions: {{known_decisions}}

Сделай:
1. Проверь полноту структуры и соответствие expected structure.
2. Найди дефекты: неполнота, противоречие, нетестируемость, неоднозначность,
   scope creep, смешение ФТ/НФТ/техники.
3. Для каждого дефекта укажи location, severity, evidence и recommended action.
4. Отдели вопросы от новых требований.
5. Дай итоговый статус: ready / ready with fixes / blocked.

Не делай:
- Не добавляй новые ФТ без source.
- Не исправляй документ молча; сначала покажи defect report.
- Не присваивай covered тендерному требованию без evidence.
```

## quality_gates

**Forces.** Главные ограничения: не переписать документ вместо review, не
скрыть блокирующие дефекты и не смешать defect report с новым backlog.

- Каждый дефект привязан к пункту документа или конкретному отсутствующему
  разделу.
- Severity объясняет влияние на согласование, разработку, договор или тендер.
- Новые требования, вопросы и редакционные правки разделены.
- Product Layer и Commercial Layer учтены явно.
- Compliance triggers (`ПДн`, реклама, услуга связи, КИИ), если встречаются,
  отправлены на ручной review.
- Итоговый статус не скрывает блокирующие вопросы.

## examples

Минимальный few-shot пример:

- **Вход**: ФТ "Система должна уведомлять ответственного сотрудника о просрочке".
- **Выход**: defect `ambiguity`: не определены "ответственный сотрудник",
  событие просрочки, канал уведомления и срок; severity high для client-order.

Расширенный пример: [examples/basic-example.md](examples/basic-example.md).

## output_schema

**Solution.** Результат паттерна - validation report с дефектами, вопросами,
scope notes и статусом готовности.

```markdown
# FR Validation Report

## Summary
- Status:
- Product Layer:
- Commercial Layer:
- Blocking issues:

## Defects
| ID | Location | Type | Severity | Evidence | Recommended action |

## Questions
| Question | Owner | Blocks |

## Scope notes
| Candidate new requirement | Source | Decision needed |

## Ready criteria
- [ ] All high defects closed or accepted.
- [ ] Open questions have owner.
- [ ] No unsupported scope added.
```

## governance_rules

- Статус `draft` допускает применение как review checklist; `canonical` требует
  human review и подтверждённого прогона на обезличенном документе.
- source of truth для связей процесс -> паттерн -> prompt находится в
  [docs/ba-processes/00-index.md](../../docs/ba-processes/00-index.md).
- Паттерн фиксирует дефекты и вопросы; финальное решение о готовности документа
  принимает человек.
- Для внешних документов обязательно удалить sensitive context из примеров и PR.
- Версионирование следует SemVer из
  [ADR-002](../../docs/adr/002-pattern-standard.md).
