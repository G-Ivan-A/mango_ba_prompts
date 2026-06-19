---
status: draft
version: 0.1
updated: 2026-06-19
ai-generated: true
type: index
scope: mango-only
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/113"
---

# Кейс: BCREQ-1059 — Email-маршрутизация по Точке входа в КЦ

> **Что это.** Полный прогон цепочки промптов библиотеки по задаче маршрутизации
> email-ответов в Контакт-центре MANGO OFFICE: когда оператор отвечает на входящее
> письмо, система автоматически использует почтовый ящик, на который это письмо
> пришло («Точка входа»).
>
> **Тип результата:** **финальное ТЗ** (Разделы 1, 2, 4, 6) — готово к передаче
> в разработку.

## Принципы прогона

- Промпты **не изменялись**; предложения по их улучшению — отдельным
  [RFC](../../../governance/rfc/prompt-improvement-bcreq-1059-proposal.md).
- Цепочка из 3 промптов применялась последовательно (stepwise).
- Все инсайты и методологические находки зафиксированы в `experiment-log.md`
  и детальном анализе `governance/analysis-bcreq-1059-2026-06-19.md`.

## Навигация по артефактам

| Этап | Артефакт |
| --- | --- |
| Вход: сырое требование | [`inputs/raw-requirement.md`](./inputs/raw-requirement.md) |
| Вход: источники БЗ + выжимка | [`inputs/kb-files.md`](./inputs/kb-files.md) |
| Цепочка промптов + обоснование | [`prompts-chain.md`](./prompts-chain.md) |
| Шаг 1 — глоссарий + терминология (Раздел 1) | [`steps/step-1-glossary.md`](./steps/step-1-glossary.md) |
| Шаг 2 — проблема, цель, задачи (Раздел 2) | [`steps/step-2-context.md`](./steps/step-2-context.md) |
| Шаг 3 — функциональные требования (Раздел 4) | [`steps/step-3-fr.md`](./steps/step-3-fr.md) |
| Шаг 4 — ограничения (Раздел 6) | [`steps/step-4-constraints.md`](./steps/step-4-constraints.md) |
| Финальное ТЗ (Разделы 1, 2, 4, 6) | [`final-artifact.md`](./final-artifact.md) |
| Лог эксперимента | [`experiment-log.md`](./experiment-log.md) |
| Детальный анализ | [`../../../governance/analysis-bcreq-1059-2026-06-19.md`](../../../governance/analysis-bcreq-1059-2026-06-19.md) |
| RFC по промптам (proposed) | [`../../../governance/rfc/prompt-improvement-bcreq-1059-proposal.md`](../../../governance/rfc/prompt-improvement-bcreq-1059-proposal.md) |

## Ключевой вывод (TL;DR)

Задача: при ответе на email-обращение оператор должен отправлять письмо с того
ящика, на который оно пришло («Точка входа»). Цепочка из трёх промптов успешно
довела требование до финального ТЗ (~30 итераций). Ключевые инсайты эксперимента:
выявлено 5 паттернов ошибок LLM, 6 успешных паттернов и 6 методологических правил
(M1–M6) для будущих стандартов БА. Предложены RFC-1059-P1…P6.
