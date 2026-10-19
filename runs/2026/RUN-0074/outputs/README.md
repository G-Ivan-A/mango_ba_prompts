---
status: draft
version: 0.1
updated: 2026-10-19
ai-generated: true
type: index
scope: mango-only
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/375"
---

# Результаты прогона RUN-0074 — задача 1106, золотой набор ошибок ИИ

> Файл **порождён** скриптом [`experiments/issue_375_golden_set.py`](../../../../experiments/issue_375_golden_set.py) из разметки [`experiments/issue_375_golden_data.py`](../../../../experiments/issue_375_golden_data.py) — не редактируйте вручную. Каждая цитата сверена с экспортом чата ([`../logs/quote-verification.md`](../logs/quote-verification.md)).

Прогон фиксирует диалог генерации BCREQ-ФТ «Инфо-сообщение о записи разговора при исходящих вызовах ВАТС MANGO OFFICE» (задача 1106) ради статистики ошибок ИИ. Результат — не артефакт требований, а размеченный по вхождениям реестр ошибок с привязкой к продуктам, BABOK / TM Forum ODA и слотам mango-ba-ai-runtime, кандидаты в золотые наборы и критерии успеха для промптов, правил и навыков посекционной генерации ФТ.

## Сводка

| Метрика | Значение |
| --- | --- |
| Реплик в ветке диалога | 214 |
| Реплик БА / ответов модели | 107 / 107 |
| Модели | qwen3.7-plus, qwen3.8-max |
| Рабочих сессий (разрыв > 30 мин) | 19 |
| Активное время внутри сессий, мин | 660 |
| Календарный интервал, дн. | 16.3 |
| Токенов на входе (с переотправкой контекста) | 18074431 |
| Токенов на выходе / в том числе reasoning | 298909 / 190546 |
| Вхождений ошибок ИИ | 193 |
| Категорий с вхождениями | 23 из 25 |
| Самые частые категории | C10 (42), C09 (32), C01 (18), C06 (11), C24 (11) |
| Поймано БА в диалоге | 86 (45%) |
| Наборов-кандидатов / кейсов | 5 / 46 |
| Критериев успеха / позитивных кейсов | 28 / 14 |

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
