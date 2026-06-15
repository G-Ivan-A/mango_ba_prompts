---
status: draft
version: 0.1.0
updated: 2026-06-15
---

# Glossary Context Generation

## purpose

**Name.** Glossary Context Generation / Формирование глоссария и бизнес-контекста.

**Intent.** Паттерн помогает БА превратить сырой запрос, встречу, письмо или
фрагмент тендерного ТЗ в общий словарь задачи: термины, проблему, цель, задачи,
границы продукта, открытые вопросы и допущения. Это первый слой перед User
Story, Use Case, ФТ или tender-fit анализом.

Применяйте паттерн, когда вход неполный, терминология клиента отличается от
терминологии Mango, есть риск скрытых предположений или нужно быстро выровнять
контекст между БА, PO/PM, SME и заказчиком.

Не применяйте паттерн как замену экспертного решения о продуктовой возможности:
если вопрос требует подтверждения владельца capability, результат паттерна
только фиксирует гипотезу и вопрос для review.

Полный URL репозитория: <https://github.com/G-Ivan-A/mango_ba_prompts>.

## process_stage

- **Process**: Формирование ФТ/ТЗ; Анализ тендерных ТЗ; вспомогательно -
  Формирование UC/US.
- **Operation**: `understanding`.
- **Pattern registry source of truth**:
  [docs/ba-processes/00-index.md](../../docs/ba-processes/00-index.md).
- **Taxonomy**: [docs/taxonomy.md](../../docs/taxonomy.md).
- **Prompt matrix**: [prompts/README.md](../../prompts/README.md).
- **Ecosystem map**: [docs/ba-ecosystem.md](../../docs/ba-ecosystem.md).
- **Related prompt implementations**:
  [`glossary-context-understanding-stepwise.md`](../../prompts/glossary-context-understanding-stepwise.md),
  [`glossary-context-understanding-oneshot.md`](../../prompts/glossary-context-understanding-oneshot.md).

## context_requirements

**Context.** Паттерн применяется на входе аналитического маршрута, когда нужно
создать общий язык задачи до моделирования или документирования.

- **Product Layer**: UCaaS, CCaaS, integrations and adjacent Mango capabilities.
  Если capability неизвестна, сначала фиксируется candidate capability и вопрос к
  product owner.
- **Commercial Layer**:
  - `client-order`: выделить договорной scope, ограничения клиента, SLA/ИБ/ПДн и
    вопросы, влияющие на стоимость или сроки.
  - `internal-product`: выделить продуктовую цель, метрики, NFR-гипотезы и
    влияние на roadmap.
  - `tender-rfp`: сохранить терминологию источника, отметить coverage/gap
    hypotheses и вопросы для tender Q&A.
- **Правила адаптации**: глубина глоссария зависит от направления разработки.
  Для клиентского заказа достаточно терминов, которые влияют на ФТ/ТЗ; для
  внутренней доработки нужны capability, метрики и quality overlay; для тендера
  каждая спорная интерпретация получает evidence или статус "требует уточнения".

Обязательные входы: исходный запрос или выдержка из документа, известный продукт
или затронутая область, цель работы, источник входа и ограничения использования
данных. Стоп-фактор: нельзя превращать неизвестную продуктовую возможность в
утверждённое требование без owner review.

## prompt_template

LLM-агностичный шаблон:

```markdown
Ты помогаешь бизнес-аналитику Mango собрать общий контекст задачи.

Вход:
- Сырой запрос: {{raw_request}}
- Product Layer: {{product_layer}}
- Commercial Layer: {{commercial_layer}}
- Известные ограничения: {{constraints}}
- Цель анализа: {{analysis_goal}}

Сделай:
1. Выдели термины клиента и сопоставь их с терминами Mango, если соответствие видно.
2. Сформулируй проблему, цель и задачи без добавления неподтвержденных решений.
3. Отметь Product Layer и Commercial Layer, которые влияют на будущие ФТ/ТЗ.
4. Раздели факты, допущения и открытые вопросы.
5. Сформируй вопросы заказчику или owner review, если контекста недостаточно.

Не делай:
- Не выдумывай capability, сроки, SLA, интеграции и ограничения.
- Не превращай вопрос в требование.
- Не смешивай термин клиента с внутренним термином Mango без пометки.
```

## quality_gates

**Forces.** Главные ограничения: не перепутать термин клиента с термином Mango,
не превратить допущение в требование и не потерять коммерческий слой задачи.

- Термины связаны с источником или помечены как допущение.
- Проблема, цель и задачи не дублируют друг друга.
- Product Layer и Commercial Layer указаны явно.
- Вопросы отделены от решений и сформулированы так, чтобы их можно было задать
  заказчику, PO/PM или SME.
- Для тендерного входа спорные пункты не получают статус covered без evidence.
- Нет закрытой клиентской информации, персональных данных или внутренних ссылок,
  не предназначенных для PR.

## examples

Минимальный few-shot пример:

- **Вход**: "Клиент просит добавить в контакт-центр уведомление супервизору, если
  оператор не перезвонил VIP-клиенту за 15 минут".
- **Выход**: термины "VIP-клиент", "супервизор", "перезвон"; Product Layer -
  CCaaS / Contact Center routing and notifications; Commercial Layer -
  `client-order`; вопросы - кто определяет VIP, где хранится SLA 15 минут, какой
  канал уведомления нужен.

Расширенный пример: [examples/basic-example.md](examples/basic-example.md).

## output_schema

**Solution.** Результат паттерна - Glossary Context Pack, который можно передать
в US/UC, FR generation, tender analysis or meeting summary без повторного разбора
сырого входа.

```markdown
# Glossary Context Pack

## Source
- Source type:
- Product Layer:
- Commercial Layer:

## Terms
| Термин источника | Рабочее определение | Mango mapping | Статус |

## Business context
- Problem:
- Goal:
- Tasks:
- Scope boundaries:

## Assumptions
| Допущение | Почему появилось | Как проверить |

## Open questions
| Вопрос | Кому адресован | Зачем нужен ответ | Блокирует ли следующий шаг |
```

## governance_rules

- Статус `draft` означает, что паттерн можно применять как рабочий шаблон, но
  `canonical` требует human review и хотя бы одного зафиксированного применения.
- source of truth для связей процесс -> паттерн -> prompt находится в
  [docs/ba-processes/00-index.md](../../docs/ba-processes/00-index.md); ссылки
  выше являются навигацией, а не отдельным реестром.
- Паттерн не должен добавлять новые prompt-файлы и не меняет существующие
  промпты; он использует текущие реализации из `prompts/`.
- При изменении Product Layer, Commercial Layer или связанных prompt-файлов
  обновляйте этот README, `patterns/README.md` и центральный процессный индекс в
  одном PR.
- Версионирование следует SemVer из
  [ADR-002](../../docs/adr/002-pattern-standard.md): patch для уточнений,
  minor для новых входов/выходов, major для смены назначения паттерна.
