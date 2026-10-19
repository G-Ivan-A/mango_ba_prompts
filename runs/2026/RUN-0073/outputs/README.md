---
status: draft
version: 0.1
updated: 2026-10-19
ai-generated: true
type: index
scope: mango-only
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/373"
---

# Результаты прогона RUN-0073 — задача 1123, золотой набор ошибок ИИ

> Файл **порождён** скриптом [`experiments/issue_373_golden_set.py`](../../../../experiments/issue_373_golden_set.py) из разметки [`experiments/issue_373_golden_data.py`](../../../../experiments/issue_373_golden_data.py) — не редактируйте вручную. Каждая цитата сверена с экспортом чата ([`../logs/quote-verification.md`](../logs/quote-verification.md)).

Прогон фиксирует диалог генерации BCREQ-ФТ «Сервис-коннектор ВАТС MANGO OFFICE → CallMentor» (задача 1123) ради статистики ошибок ИИ. Результат — не артефакт требований, а размеченный по вхождениям реестр ошибок с привязкой к продуктам, BABOK / TM Forum ODA и слотам mango-ba-ai-runtime, кандидаты в золотые наборы и критерии успеха для промптов, правил и навыков посекционной генерации ФТ.

## Сводка

| Метрика | Значение |
| --- | --- |
| Реплик в ветке диалога | 106 |
| Реплик БА / ответов модели | 53 / 53 |
| Модели | qwen3.7-plus, qwen3.8-max |
| Рабочих сессий (разрыв > 30 мин) | 7 |
| Активное время внутри сессий, мин | 247 |
| Календарный интервал, дн. | 3.1 |
| Токенов на входе (с переотправкой контекста) | 2566716 |
| Токенов на выходе / в том числе reasoning | 120519 / 70512 |
| Вхождений ошибок ИИ | 149 |
| Категорий с вхождениями | 18 из 19 |
| Самые частые категории | C09 (23), C01 (21), C19 (18), C10 (15), C12 (14) |
| Поймано БА в диалоге | 92 (62%) |
| Наборов-кандидатов / кейсов | 6 / 51 |
| Критериев успеха / позитивных кейсов | 22 / 12 |

## Состав записи

| Файл | Что содержит |
| --- | --- |
| [`incident-register.md`](incident-register.md) | реестр всех вхождений с цитатами и привязками |
| [`error-statistics.md`](error-statistics.md) | распределения: категории, продукты, разделы, модели, сессии, ответы, BABOK, ODA, правила runtime, задержка |
| [`how-not-to-do-by-product.md`](how-not-to-do-by-product.md) | «как не надо делать» по продуктам — все вхождения |
| [`golden-set-candidates.md`](golden-set-candidates.md) | кандидаты в золотые наборы по группам разделов (5–10 кейсов) |
| [`golden-set-candidates.json`](golden-set-candidates.json) | те же кейсы в структуре `golden/cases.yaml` runtime |
| [`rubric-candidates.md`](rubric-candidates.md) | бинарная рубрика: базовые критерии и стражи по категориям |
| [`success-criteria.md`](success-criteria.md) | золотой набор критериев успеха и позитивных кейсов |
| [`runtime-improvements.md`](runtime-improvements.md) | предложения для runtime и шаблона-промпта |
| [`section-prompts.md`](section-prompts.md) | структура разделов BCREQ-ФТ, требования к разделам, три промпта посекционной генерации и критерии приёмки (гибридный режим, без runtime и продуктовой принадлежности; написан вручную) |
| [`prompt-usage.md`](prompt-usage.md) | распределение операций БА, сессии, вложения |
| [`../logs/metrics.md`](../logs/metrics.md) | метрики по каждой реплике |
| [`../logs/quote-verification.md`](../logs/quote-verification.md) | сверка каждой цитаты с экспортом |
| [`../logs/kb-verification.md`](../logs/kb-verification.md) | сверка утверждений модели с КБ runtime |
| [`../logs/experiment-log.md`](../logs/experiment-log.md) | как получена запись |
| [`../inputs/README.md`](../inputs/README.md) | провенанс исходного экспорта |
| [`../feedback/review-notes.md`](../feedback/review-notes.md) | ограничения чтения и открытые вопросы |
