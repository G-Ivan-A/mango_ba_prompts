---
status: draft
version: 0.1
updated: 2026-08-21
ai-generated: true
type: index
scope: mango-only
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/277"
---

# Прогон 1020 — вопросы стейкхолдеру по интеграции OkDesk ↔ MANGO OFFICE

> **Что это.** Фиксация **реально состоявшегося** диалога БА с LLM по задаче
> 1020, приложенного к
> [issue #277](https://github.com/G-Ivan-A/mango_ba_prompts/issues/277).
> Прогон не воспроизводился заново: артефакты собраны из экспорта чата.
>
> **Тип прогона:** `statistics` — цель постановки «зафиксировать прогон и
> результаты» для накопления эмпирических данных, а не выполнение процесса ради
> артефакта.
>
> **Тип результата:** промежуточный. Явной приёмки не было, сессия оборвана на
> нераспознанном запросе (эпизод 4). **Это не согласованный шаблон и не golden
> case.** Известные дефекты — в [`final-artifact.md`](final-artifact.md) и
> [`quality-findings.md`](quality-findings.md).

## Формат записи

Прогон оформлен как **один комплексный run с разделением на 4 эпизода** и
отдельным вердиктом по каждому (вариант, предложенный в issue #277). Дробить на
отдельные `RUN-XXXX` нецелесообразно: все эпизоды идут в одном непрерывном
контексте одной сессии, а метрики токенов эпизодов неотделимы друг от друга
(история переотправляется в каждый запрос).

## Навигация

| Что | Файл |
| --- | --- |
| Вход: экспорт чата и транскрипт | [`../inputs/README.md`](../inputs/README.md) |
| Маршрут промптов и отличия от библиотеки | [`prompts-chain.md`](prompts-chain.md) |
| БА-анализ: успехи, дефекты, галлюцинации | [`quality-findings.md`](quality-findings.md) |
| Итоговое состояние вопросов + незакрытые замечания | [`final-artifact.md`](final-artifact.md) |
| Обратная связь и решения | [`../feedback/ba-review-notes.md`](../feedback/ba-review-notes.md) |
| Лог эксперимента | [`../logs/experiment-log.md`](../logs/experiment-log.md) |
| Пореплико́вые метрики | [`../logs/turn-metrics.md`](../logs/turn-metrics.md) |
| Проверка достоверности сносок | [`../logs/grounding-check.md`](../logs/grounding-check.md) |

## Эпизоды и вердикты

| № | Реплики | Эпизод | Вердикт |
| --- | --- | --- | --- |
| 1 | 0–1 | Понимание проблемы и первые вопросы — [`steps/step-1-problem-understanding-and-questions.md`](steps/step-1-problem-understanding-and-questions.md) | works-with-edits |
| 2 | 2–3 | Коррекция БА и ограничение OkDesk — [`steps/step-2-correction-and-okdesk-constraint.md`](steps/step-2-correction-and-okdesk-constraint.md) | works-with-edits |
| 3 | 4–5 | Вопросы стейкхолдеру на бизнес-языке — [`steps/step-3-stakeholder-questions.md`](steps/step-3-stakeholder-questions.md) | works-with-edits |
| 4 | 6–7 | Нераспознанный запрос, пустой ответ — [`steps/step-4-empty-answer.md`](steps/step-4-empty-answer.md) | fails |

Сводный вердикт прогона — **works-with-edits** (`success_rate: 0.75`): три из
четырёх эпизодов дали пригодный к использованию результат, все — с правками БА;
эпизод 4 завершился пустым ответом.
