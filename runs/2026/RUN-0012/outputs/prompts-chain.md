---
status: draft
version: 0.1
updated: 2026-07-14
ai-generated: true
type: index
scope: mango-only
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/261"
related_artifacts:
  - "prompts/glossary-context-understanding-stepwise.md"
  - "prompts/questions-customer-understanding-stepwise.md"
  - "prompts/fr-documentation-stepwise.md"
  - "prompts/constraints-documentation-stepwise.md"
  - "docs/adr/009-bcreq-formation-process.md"
---

# Цепочка промптов — BCREQ-1069 (ограниченный API-ключ для записей разговоров)

> **Что это.** Обоснование маршрута прогона: какие промпты библиотеки и в каком
> порядке применялись для формирования финального ФТ по сырому требованию из
> [issue #261](https://github.com/G-Ivan-A/mango_ba_prompts/issues/261).
> Промпты в ходе прогона **не изменялись**.

## Маппинг на конвейер BCREQ ([ADR-009](../../../../docs/adr/009-bcreq-formation-process.md))

| Подпроцесс ADR-009 | Шаг прогона | Промпт | Артефакт | Gate |
| --- | --- | --- | --- | --- |
| П1 приём и нормализация | Шаг 1 | [`glossary-context-understanding-stepwise`](../../../../prompts/glossary-context-understanding-stepwise.md) | [`step-1-glossary.md`](steps/step-1-glossary.md) | operation |
| П1/П2 нормализация контекста | Шаг 2 | тот же промпт (Раздел 2) | [`step-2-normalization.md`](steps/step-2-normalization.md) | **human G1** (структура задач) |
| П2 доопределение | Шаг 3 | [`questions-customer-understanding-stepwise`](../../../../prompts/questions-customer-understanding-stepwise.md) | [`step-3-questions.md`](steps/step-3-questions.md) | operation |
| П3 моделирование сценариев | Шаг 4 | [`fr-documentation-stepwise`](../../../../prompts/fr-documentation-stepwise.md) (Шаг 2 промпта) | [`step-4-scenarios.md`](steps/step-4-scenarios.md) | operation |
| П4 документирование (ФТ) | Шаг 5 | [`fr-documentation-stepwise`](../../../../prompts/fr-documentation-stepwise.md) (Шаг 3 промпта) | [`step-5-fr.md`](steps/step-5-fr.md) | operation |
| П4 документирование (ограничения) | Шаг 6 | [`constraints-documentation-stepwise`](../../../../prompts/constraints-documentation-stepwise.md) | [`step-6-constraints.md`](steps/step-6-constraints.md) | operation |
| П5 консолидация | Итог | — (сборка БА) | [`final-artifact.md`](final-artifact.md) | **human G2** (валидация/риски) |

## Порядок и обоснование

1. **Глоссарий раньше ФТ.** Задача смешивает понятия «API-ключ», «основной ключ»,
   «ограниченный ключ», «группа сотрудников», «запись разговора». Без глоссария
   (Шаг 1) требования Раздела 4 путали бы область действия ключей — тот же вывод,
   что в [RUN-0010](../../RUN-0010/outputs/2026-06-17-bcreq-1025-email-routing.md)
   (глоссарий как якорь).
2. **Вопросы отдельным шагом.** Ответ на В1 (бизнес-мотив/регулятор) Заказчик не
   дал; ряд границ (срок жизни ключа, поведение при изменении группы) не закрыт.
   Открытые вопросы зафиксированы явно (Шаг 3), а не «додуманы».
3. **Сценарная матрица до генерации ФТ.** Промпт `fr-documentation-stepwise`
   требует Шаг 2 (Happy Path + альтернативы + исключения) перед Разделом 4 —
   вынесен в отдельный файл (Шаг 4).
4. **Ограничения отдельным промптом.** Раздел 6 генерируется
   `constraints-documentation-stepwise`, как подтверждено практикой RUN-0010:
   роли и защита скоупа фиксируются в ограничениях, а не «размазываются» по ФТ.

## Принципы прогона

- Факты о продукте (что уже умеет ВАТС по API/записям) в БЗ репозитория не
  подтверждены документально ⇒ помечены «не найдено в документации» и вынесены в
  вопросы, а не утверждены как As-Is.
- Опциональные требования из ответов В5/В6 промаркированы `[ОПЦИЯ — отдельная
  оценка]` и не входят в MVP-скоуп.
- Human gate G1 (структура Раздела 2) и G2 (валидация ФТ + риски ПДн) в этом
  прогоне **не пройдены автоматически** — переданы человеку (см. правило B3
  ADR-009).
