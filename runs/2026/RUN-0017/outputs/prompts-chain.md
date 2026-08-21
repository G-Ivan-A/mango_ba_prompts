---
status: draft
version: 0.1
updated: 2026-08-21
ai-generated: true
type: index
scope: mango-only
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/270"
---

# Цепочка промптов и маршрут прогона 1076

> Восстановлено по транскрипту. Промпты подавались БА **дословно** и в ходе
> прогона не изменялись; маркеры промптов присутствуют в тексте реплик.

## Маршрут

| Эпизод | Реплики | Промпт / режим | Артефакт эпизода | Gate |
| --- | --- | --- | --- | --- |
| 1 | 0–7 | [`glossary-context-understanding-stepwise`](../../../../prompts/glossary-context-understanding-stepwise.md), Шаги 0–2 | [`steps/step-1-as-is-and-glossary.md`](steps/step-1-as-is-and-glossary.md) | human (реплики 4, 6) |
| 2 | 8–13 | тот же промпт, возврат к Шагу 2 | [`steps/step-2-object-model.md`](steps/step-2-object-model.md) | human |
| 3 | 14–17 | тот же промпт, Раздел 2 | [`steps/step-3-section-2-agreed.md`](steps/step-3-section-2-agreed.md) | **human G1** (структура задач) |
| 4 | 18–23 | [`fr-documentation-stepwise`](../../../../prompts/fr-documentation-stepwise.md), Шаги 1–2 | [`steps/step-4-scenarios.md`](steps/step-4-scenarios.md) | human |
| 5 | 24–28 | ad-hoc запрос на верификацию по документации | [`steps/step-5-mtalker-facts.md`](steps/step-5-mtalker-facts.md) | human |
| 6 | 29–33 | тот же промпт, Шаг 3 + ad-hoc ролевая проверка (аналитик/архитектор/техлид) | [`steps/step-6-fr-v1-and-rework.md`](steps/step-6-fr-v1-and-rework.md) | **human, отклонение** |
| 7 | 34–43 | тот же промпт, Шаг 3 (детализация и оформление) | [`steps/step-7-fr-detailed.md`](steps/step-7-fr-detailed.md) | human (фиксация 4.1–4.4) |
| 8 | 44–47 | ad-hoc: дополнение штатных ограничений; матрица покрытия по образцу | [`steps/step-8-constraints-and-matrix.md`](steps/step-8-constraints-and-matrix.md) | human |
| 9 | 48–51 | ad-hoc: контроль границы ответственности | [`steps/step-9-responsibility-boundary.md`](steps/step-9-responsibility-boundary.md) | **human, отклонение** |
| 10 | 52–53 | ad-hoc: сверка документа с двумя источниками документации | [`steps/step-10-doc-verification.md`](steps/step-10-doc-verification.md) | **human G2** (валидация) |
| 11 | 54–55 | ad-hoc: проверка коммуникации с менеджером | [`steps/step-11-manager-comment.md`](steps/step-11-manager-comment.md) | human |

## Отличия от «чистого» прогона библиотеки (важно для статистики)

1. Из библиотеки применены **два** промпта из цепочки BCREQ:
   `glossary-context-understanding-stepwise` и `fr-documentation-stepwise`.
   Промпты `questions-customer-understanding-stepwise` и
   `constraints-documentation-stepwise` **не применялись**: вопросы задавались БА
   вручную по ходу диалога, а Раздел 6 сформирован ad-hoc-запросом на дополнение
   штатных ограничений Заказчика.
2. Шесть из одиннадцати эпизодов — **ad-hoc-запросы БА** вне библиотеки
   (верификация по документации, ролевая проверка, матрица покрытия, контроль
   границы ответственности, финальная сверка, проверка письма). Это показывает
   реальную долю работы, которую библиотека сейчас не покрывает.
3. Прогон выполнялся в одном непрерывном контексте, поэтому вход каждого
   следующего шага — весь предыдущий диалог: к реплике 55 объём входного
   контекста достиг 197 064 токенов (см. [`../logs/turn-metrics.md`](../logs/turn-metrics.md)).
4. Смена модели по ходу прогона: реплики 1–33 — `qwen3.7-plus`, реплики 35–55 —
   `qwen3.8-max-preview`. Прогон **не** является контролируемым A/B-сравнением
   моделей: смена совпала с переходом к более сложным задачам.
