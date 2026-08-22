---
status: draft
version: 0.1
updated: 2026-08-21
ai-generated: true
type: index
scope: mango-only
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/283"
---

# Прогон 1007 — ФТ на перевод Сделки в АМО CRM по успешному дозвону

> **Что это.** Фиксация **реально состоявшегося** диалога БА с LLM по задаче
> 1007, приложенного к
> [issue #283](https://github.com/G-Ivan-A/mango_ba_prompts/issues/283).
> Прогон не воспроизводился заново: артефакты собраны из экспорта чата.
>
> **Тип прогона:** `statistics` — цель постановки «зафиксировать прогон и
> результаты» для накопления эмпирических данных, а не выполнение процесса ради
> артефакта.
>
> **Тип результата:** промежуточный. Явной приёмки не было: сессия закрыта на
> запросе подтверждения версии 1.1. **Это не согласованный шаблон и не golden
> case.** Известные дефекты — в [`final-artifact.md`](final-artifact.md) и
> [`quality-findings.md`](quality-findings.md).

## Формат записи

Прогон оформлен как **один комплексный run с разделением на 10 эпизодов** и
отдельным вердиктом по каждому. Дробить на отдельные `RUN-XXXX` нецелесообразно:
все эпизоды идут в одном непрерывном контексте одной сессии, а метрики токенов
эпизодов неотделимы друг от друга (история переотправляется в каждый запрос).

## Навигация

| Что | Файл |
| --- | --- |
| Вход: экспорт чата и транскрипт | [`../inputs/README.md`](../inputs/README.md) |
| Маршрут промптов и отличия от библиотеки | [`prompts-chain.md`](prompts-chain.md) |
| БА-анализ: успехи, дефекты, галлюцинации | [`quality-findings.md`](quality-findings.md) |
| Итоговое состояние ФТ + незакрытые замечания | [`final-artifact.md`](final-artifact.md) |
| Обратная связь и решения | [`../feedback/ba-review-notes.md`](../feedback/ba-review-notes.md) |
| Лог эксперимента | [`../logs/experiment-log.md`](../logs/experiment-log.md) |
| Пореплико́вые метрики | [`../logs/turn-metrics.md`](../logs/turn-metrics.md) |
| Проверка достоверности сносок | [`../logs/grounding-check.md`](../logs/grounding-check.md) |

## Эпизоды и вердикты

| № | Реплики | Эпизод | Вердикт |
| --- | --- | --- | --- |
| 1 | 0–1 | Постановка рамки и запрос контекста — [`steps/step-1-frame-and-context-request.md`](steps/step-1-frame-and-context-request.md) | works |
| 2 | 2–3 | Бизнес-контекст и фиксация терминологии — [`steps/step-2-context-and-glossary.md`](steps/step-2-context-and-glossary.md) | works |
| 3 | 4–5 | Первый черновик ФТ на допущениях — [`steps/step-3-first-fr-draft.md`](steps/step-3-first-fr-draft.md) | works-with-edits |
| 4 | 6–7 | Локализация настройки, переход на системный уровень — [`steps/step-4-settings-location-check.md`](steps/step-4-settings-location-check.md) | works |
| 5 | 8–9 | Ревью раздела 2 — [`steps/step-5-section-2-review.md`](steps/step-5-section-2-review.md) | works-with-edits |
| 6 | 10–11 | Проверка избыточности задачи 2.3.3 — [`steps/step-6-redundancy-check.md`](steps/step-6-redundancy-check.md) | works |
| 7 | 12–13 | Сборка документа версии 1.0 — [`steps/step-7-final-assembly-v1.md`](steps/step-7-final-assembly-v1.md) | works |
| 8 | 14–15 | Детализация под разработку по макету — [`steps/step-8-dev-level-detailing.md`](steps/step-8-dev-level-detailing.md) | works-with-edits |
| 9 | 16–17 | Снятие технического слоя — [`steps/step-9-api-removal.md`](steps/step-9-api-removal.md) | works-with-edits |
| 10 | 18–19 | «Классические» формулировки, версия 1.1 — [`steps/step-10-classic-wording-v1-1.md`](steps/step-10-classic-wording-v1-1.md) | fails |

Сводный вердикт прогона — **works-with-edits** (`success_rate: 0.5`): пять
эпизодов из десяти приняты БА без содержательных правок, четыре потребовали
правок, десятый исполнил указание по форме ценой смысла требований и приёмки не
получил.

## Главное для статистики

- Галлюцинаций — **4**, из них дошла до итога — **1** (метка поля интерфейса).
- Все три вызова веб-инструментов дали **0 прочитанных страниц**, но были поданы
  как «результаты проверки документации».
- Самый дешёвый способ получить пользу в этом прогоне — не генерация, а критика
  готового текста БА (эпизоды 5 и 6): реальное дублирование и расширение скоупа
  найдены за 14 028 входных токенов.
- Буквальное исполнение указания по форме (эпизод 10) обошлось дороже любой
  галлюцинации: испорчены три требования из семи, включая единственные
  тестируемые.
