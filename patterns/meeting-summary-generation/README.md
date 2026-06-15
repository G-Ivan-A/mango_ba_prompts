---
status: draft
version: 0.1.0
updated: 2026-06-15
---

# Meeting Summary Generation

## purpose

**Name.** Meeting Summary Generation / Генерация резюме встречи.

**Intent.** Паттерн помогает БА, PO или PM оформить встречу в практичный summary:
context, decisions, open questions, action items, owners, deadlines, risks and
next steps. Результат нужен для синхронизации команды, заказчика и дальнейших
аналитических шагов.

Применяйте паттерн после встречи, воркшопа, discovery-созвона, внутреннего
разбора или клиентского обсуждения, особенно если дальше нужно запустить
glossary, US/UC, FR или validation.

Не применяйте паттерн для генерации новых требований: summary фиксирует то, что
было сказано или решено, а не расширяет scope.

Полный URL репозитория: <https://github.com/G-Ivan-A/mango_ba_prompts>.

## process_stage

- **Process**: Помощь ПО/ПМ; дополнительно Формирование ФТ/ТЗ как источник
  входного контекста.
- **Operation**: `documentation`.
- **Pattern registry source of truth**:
  [docs/ba-processes/00-index.md](../../docs/ba-processes/00-index.md).
- **Taxonomy**: [docs/taxonomy.md](../../docs/taxonomy.md).
- **Prompt matrix**: [prompts/README.md](../../prompts/README.md).
- **Ecosystem map**: [docs/ba-ecosystem.md](../../docs/ba-ecosystem.md).
- **Related prompt implementations**:
  [`meeting-customer-documentation-stepwise.md`](../../prompts/meeting-customer-documentation-stepwise.md),
  [`meeting-team-documentation-stepwise.md`](../../prompts/meeting-team-documentation-stepwise.md).

## context_requirements

**Context.** Паттерн применяется после встречи или после ASR ingestion, когда
нужно зафиксировать итоги без расширения scope.

- **Product Layer**: продукт, capability, system boundary or backlog area,
  обсуждавшиеся на встрече. Если продукт не определён, summary должно это
  показать как open question.
- **Commercial Layer**:
  - `client-order`: выделить решения и обещания, влияющие на scope, сроки,
    договор, SLA, support or compliance.
  - `internal-product`: выделить decisions, owners, metrics, release impact and
    follow-up artifacts.
  - `tender-rfp`: выделить Q&A, no-bid triggers, coverage assumptions and risk
    owners.
- **Правила адаптации**: customer summary должен быть короче и аккуратнее в
  формулировках; team summary может включать внутренние blockers and owner
  details; tender summary должен сохранять evidence and unresolved questions.

Обязательные входы: notes or ASR Ingestion Pack, meeting goal, participants or
roles, Product Layer, Commercial Layer and target audience. Стоп-фактор: summary
нельзя отправлять наружу, если оно содержит внутренние комментарии или sensitive
context.

## prompt_template

LLM-агностичный шаблон:

```markdown
Ты помогаешь бизнес-аналитику Mango оформить резюме встречи.

Вход:
- Meeting notes or ASR Ingestion Pack: {{meeting_input}}
- Audience: {{audience_customer_or_team}}
- Product Layer: {{product_layer}}
- Commercial Layer: {{commercial_layer}}
- Meeting goal: {{meeting_goal}}
- Known privacy constraints: {{privacy_constraints}}

Сделай:
1. Сформируй короткий context summary.
2. Выдели decisions отдельно от discussion points.
3. Сформируй action items with owners and due dates, если они есть.
4. Сформируй open questions and blockers.
5. Отметь next analytical step: glossary, US/UC, FR, validation, risk or owner review.

Не делай:
- Не добавляй решения, которых нет во входе.
- Не отправляй внутренние риски в customer-facing summary без review.
- Не скрывай неизвестных owners or dates.
```

## quality_gates

**Forces.** Главные ограничения: не смешать discussion с decisions, не включить
внешне небезопасный текст в customer summary и не назначить owners без source.

- Decisions, discussion notes, questions and action items не смешаны.
- Owners and dates указаны только если они есть во входе; иначе используются TBD.
- Product Layer и Commercial Layer указаны явно.
- Customer-facing summary не содержит внутренних оценок, sensitive context or
  неутверждённых обещаний.
- Next steps проверяемы и назначены.
- Summary может стать входом для следующего паттерна без повторной расшифровки
  встречи.

## examples

Минимальный few-shot пример:

- **Вход**: notes о callback SLA, уведомлениях супервизора и вопросе по каналу
  уведомления.
- **Выход**: decision "нужен контроль просрочек", open question "канал
  уведомления", action "БА уточняет SLA source", next step
  `glossary-context-generation`.

Расширенный пример: [examples/basic-example.md](examples/basic-example.md).

## output_schema

**Solution.** Результат паттерна - Meeting Summary с decisions, open questions,
action items, risks and next analytical step.

```markdown
# Meeting Summary

## Context

## Decisions
| Decision | Owner | Source | External-safe |

## Discussion notes

## Open questions
| Question | Owner | Blocks | Audience |

## Action items
| Action | Owner | Due date | Status |

## Risks and blockers

## Next steps
- Next pattern:
- Product Layer:
- Commercial Layer:
```

## governance_rules

- Статус `draft` допускает применение как meeting documentation pattern;
  `canonical` требует review и подтверждённого применения.
- source of truth для связей процесс -> паттерн -> prompt находится в
  [docs/ba-processes/00-index.md](../../docs/ba-processes/00-index.md).
- Перед отправкой заказчику summary проходит human review на sensitive context,
  promises and commercial commitments.
- Если входом была сырая ASR-расшифровка, сначала применяйте
  [`asr-ingestion`](../asr-ingestion/) или явно помечайте спорные фрагменты.
- Версионирование следует SemVer из
  [ADR-002](../../docs/adr/002-pattern-standard.md).
