---
status: draft
version: 0.1
updated: 2026-06-18
ai-generated: true
type: index
scope: mango-only
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/109"
---

# Кейс: Многоканальная нагрузка агента (early-stage разбор)

> **Что это.** Полный прогон цепочки промптов библиотеки по сырому требованию из
> [issue #109](https://github.com/G-Ivan-A/mango_ba_prompts/issues/109): дать агенту
> возможность вести одновременно максимум 3 активных контакта из разных каналов
> (голос/чат/e-mail) с приоритетом голос > чат > e-mail.
>
> **Тип результата:** **ранний разбор** (нормализация + вопросы + US/UC + варианты
> доработки / Раздел 3). **НЕ финальное ТЗ.**

## Принципы прогона

- Промпты **не изменялись**; предложения по их улучшению — отдельным
  [RFC](../../../../docs/rfc/prompt-improvement-multichannel-proposal.md).
- Факты о продукте — только из 2 PDF-руководств через выжимку, с цитатами
  `[Документ, §Раздел, с.Страница]`; чего нет — помечено «не найдено в документации».
- Каждый шаг — отдельный файл с промежуточным результатом (FT-2).

## Навигация по артефактам

| Этап | Артефакт |
| --- | --- |
| Вход: сырое требование | [`inputs/raw-requirement.md`](../inputs/raw-requirement.md) |
| Вход: БЗ (PDF) + выжимка As-Is | [`inputs/kb-files.md`](../inputs/kb-files.md) |
| Цепочка промптов + обоснование | [`prompts-chain.md`](./prompts-chain.md) |
| Шаг 1 — глоссарий + As-Is | [`steps/step-1-glossary.md`](./steps/step-1-glossary.md) |
| Шаг 2 — нормализация + 5 Whys + gap | [`steps/step-2-normalization.md`](./steps/step-2-normalization.md) |
| Шаг 3 — вопросы заказчику | [`steps/step-3-questions.md`](./steps/step-3-questions.md) |
| Шаг 4 — User Story + Use Case | [`steps/step-4-story.md`](./steps/step-4-story.md) |
| Шаг 5 — варианты доработки (Раздел 3) | [`steps/step-5-options.md`](./steps/step-5-options.md) |
| Итоговый артефакт + рекомендация | [`final-artifact.md`](../outputs/final-artifact.md) |
| Лог эксперимента (6 метрик) | [`experiment-log.md`](../logs/experiment-log.md) |
| RFC по промптам (proposed) | [`../../../docs/rfc/prompt-improvement-multichannel-proposal.md`](../../../../docs/rfc/prompt-improvement-multichannel-proposal.md) |

## Ключевой вывод (TL;DR)

Корневой gap — **нет единой межканальной модели загрузки агента** (общий счётчик
активных контактов + сквозной приоритет каналов). Сегодня лимит есть только для текста
(Ф3), очереди голоса/текста независимы (Ф2), межканального приоритета нет (Ф8).
Предложены 3 варианта (A/B/C); предварительно — A как MVP с эволюцией в B, после
ответов на ключевые вопросы В1/В3/В4/В5.
