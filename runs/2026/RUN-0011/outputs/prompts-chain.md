---
status: draft
version: 0.1
updated: 2026-06-18
ai-generated: true
type: process
scope: mango-only
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/109"
related_artifacts:
  - "prompts/glossary-context-understanding-stepwise.md"
  - "prompts/questions-customer-understanding-stepwise.md"
  - "prompts/us-modeling-stepwise.md"
  - "prompts/uc-modeling-stepwise.md"
  - "prompts/technical-details-solution-design-stepwise.md"
---

# Цепочка промптов и её обоснование

> **Назначение.** Зафиксировать, какие промпты библиотеки и в каком порядке
> запускались для разбора сырого требования (issue #109), и почему именно эти.
> Это реализация требования FT-1 («цепочка с обоснованием»).
>
> **Граница задачи (важно).** Заказчику нужен **ранний разбор**: нормализация +
> вопросы + User Story/Use Case + варианты доработки (Раздел 3). Это **НЕ финальное
> ТЗ** — поэтому из цепочки СОЗНАТЕЛЬНО исключены промпты документирования
> требований (`fr-documentation-*`, `constraints-documentation-*`, `fr-validation-*`):
> они генерируют «Система должна …» (уровень Раздела 4), что преждевременно.

## Где задача стоит в карте процессов

По [`docs/ba-processes/00-index.md`](../../../../docs/ba-processes/00-index.md) задача
покрывает ранние процессы БА:

| Процесс БА | Когнитивная операция | Этап задачи |
| --- | --- | --- |
| Понимание контекста | `understanding` | Шаг 1 — глоссарий + As-Is |
| Нормализация требования | `understanding` / `analysis` | Шаг 2 |
| Прояснение с заказчиком | `understanding` | Шаг 3 — вопросы |
| Моделирование потребности | `modeling` | Шаг 4 — US/UC |
| Проектирование решения (варианты) | `solution-design` | Шаг 5 — Раздел 3 |

Выбран режим запуска **stepwise** для всех шагов: требование неоднозначно (есть
конфликт «лимит только текста vs лимит по всем каналам»), а stepwise-промпты дают
human-gate между шагами и снижают риск галлюцинаций по сравнению с oneshot.

## Цепочка (в порядке запуска)

| № | Промпт (id) | Операция | Зачем в цепочке | Артефакт-выход |
| --- | --- | --- | --- | --- |
| 0 | подготовка БЗ (по [ADR-007](../../../../docs/adr/007-kb-standard.md)) | — | Извлечь факты из 2 PDF, собрать выжимку, работать только с ней | [`inputs/kb-files.md`](../inputs/kb-files.md) |
| 1 | `mango-glossary-context-understanding-stepwise` | understanding | ШАГ 0: контекст As-Is из БЗ; ШАГ 1: глоссарий; ШАГ 2: проблема/цель/задачи (Раздел 2). Даёт общий язык и фиксирует As-Is до интерпретаций | [`steps/step-1-glossary.md`](./steps/step-1-glossary.md) |
| 2 | (тот же stepwise, ШАГ 2) + ручная нормализация БА | analysis | Свести требование к атомарным утверждениям, развести «боль» и «решение», 5 Whys, gap к As-Is | [`steps/step-2-normalization.md`](./steps/step-2-normalization.md) |
| 3 | `mango-questions-customer-understanding-stepwise` | understanding | Декомпозиция «заявленное решение vs боль», проверка существующих решений (Эксперт по продукту), атомарные вопросы заказчику | [`steps/step-3-questions.md`](./steps/step-3-questions.md) |
| 4 | `mango-us-modeling-stepwise` + `mango-uc-modeling-stepwise` | modeling | User Story (Job Story + INVEST + BDD) и Use Case (Cockburn): happy path, альтернативы, исключения | [`steps/step-4-story.md`](./steps/step-4-story.md) |
| 5 | `mango-technical-details-solution-design-stepwise` (адаптировано) | solution-design | Варианты доработки A/B/C (Раздел 3) с плюсами/минусами/сложностью/рисками | [`steps/step-5-options.md`](./steps/step-5-options.md) |
| — | консолидация (ручная) | — | Сборка итогового артефакта раннего разбора + рекомендация | [`final-artifact.md`](../outputs/final-artifact.md) |

## Обоснование выбора каждого звена

- **Шаг 1 — `glossary-context-understanding-stepwise`.** Это единственный промпт с
  встроенным ШАГ 0 «собрать контекст и извлечь As-Is из БЗ» и жёстким правилом «не
  писать "Система должна"». Идеален как вход: формирует глоссарий (агент, контакт,
  канал, приоритет) и Раздел 2 (проблема/цель/задачи) без забегания в проектирование.
- **Шаг 2 — нормализация.** Отдельного промпта «нормализация требования» в библиотеке
  нет; ближайшее — ШАГ 2 того же stepwise + ручной разбор БА. Это сознательный gap
  (см. [RFC](../../../../docs/rfc/prompt-improvement-multichannel-proposal.md)).
- **Шаг 3 — `questions-customer-understanding-stepwise`.** Содержит шаг «проверка
  существующих решений (Эксперт по продукту)», который напрямую вытаскивает уже
  существующую частичную функциональность (лимит текста Ф3, чекбокс Ф5) — критично,
  чтобы не задавать заказчику вопросы про то, что уже есть.
- **Шаг 4 — `us-modeling-stepwise` + `uc-modeling-stepwise`.** Требование заказчика
  сформулировано как бизнес-потребность («возможность одновременной работы»), что
  ложится на Job Story; UC добавляет потоки и исключения (входящий звонок при
  заполненном лимите) — это вход для вопросов и вариантов.
- **Шаг 5 — `technical-details-solution-design-stepwise`.** Единственный промпт,
  генерирующий «варианты решения». Применён в раннем режиме: только продуктовые
  варианты A/B/C верхнего уровня, без детального тех-дизайна (Раздел 7).

## Что осознанно НЕ запускалось и почему

| Не использован | Причина |
| --- | --- |
| `fr-documentation-stepwise`, `constraints-documentation-*` | Дают «Система должна …» (Раздел 4) — преждевременно для раннего разбора |
| `fr-validation-*` | Нечего валидировать: финальных ФТ ещё нет |
| `asr-ingestion-*`, `meeting-*`, `letter-*` | Нет входной ASR/встречи/письма — вход уже текстовый |
| `*-oneshot`, `*-legacy` | Требование неоднозначно → нужен human-gate stepwise; legacy устарели |

## Источники

- [issue #109](https://github.com/G-Ivan-A/mango_ba_prompts/issues/109)
- [`docs/ba-processes/00-index.md`](../../../../docs/ba-processes/00-index.md)
- [`standards/ba-ontology.md`](../../../../standards/ba-ontology.md)
