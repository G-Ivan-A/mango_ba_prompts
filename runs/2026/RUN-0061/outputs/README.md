---
status: draft
version: 0.1
updated: 2026-08-28
ai-generated: true
type: index
scope: mango-only
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/336"
---

# Результаты прогона RUN-0061 — задача 1090, human review ссылок на twin

Прогон human review отчёта [`../../RUN-0057/outputs/L0-customer-form-with-assessment.md`](../../RUN-0057/outputs/L0-customer-form-with-assessment.md): БА проверял выводы, переходя по источникам, и добивался ссылок, пригодных для быстрой проверки.

Прогон имеет `run_type: statistics`: результатом является не артефакт требований, а замеры — объём выборки, распределение операций БА, расход ресурсов и адресность ссылок (см. [`standards/runs-contract-standard.md`](../../../../standards/runs-contract-standard.md)).

## Сводка

| Метрика | Значение |
| --- | --- |
| Реплик в ветке диалога | 30 |
| Эпизодов (реплик БА) | 15 |
| Ответов модели | 15 |
| Рабочих сессий (разрыв > 30 мин) | 2 |
| Активное время внутри сессий, мин | 91 |
| Календарный интервал, дн. | 2.1 |
| Модели | qwen3.7-plus |
| Токенов на выходе | 35847 |
| В том числе reasoning | 18098 |
| Токенов на входе (с переотправкой контекста) | 723648 |
| Максимум входа за один вызов | 74559 |
| Символов ввода БА | 17400 |
| Символов ответов модели | 54084 |
| Токенов `[twin: …]` в проверяемом отчёте | 132 (0 кликабельных, 0 с якорем) |
| Различных страниц вики, процитированных отчётом | 79 (все доступны, 71 с якорями) |
| Ссылок модели проверено в диалоге | 21 (0 с якорем; 1 из 13 заявленных разделов совпал с заголовком) |

## Состав записи

| Файл | Что содержит |
| --- | --- |
| [`link-review-statistics.md`](link-review-statistics.md) | основной разбор: чем неудобна проверка ссылок и что измерено |
| [`link-reference-contract-draft.md`](link-reference-contract-draft.md) | ненормативный черновик однозначного формата ссылки |
| [`prompt-usage.md`](prompt-usage.md) | распределение операций процесса БА, сессии, вложения |
| [`../logs/metrics.md`](../logs/metrics.md) | метрики по каждой реплике |
| [`../logs/link-verification.md`](../logs/link-verification.md) | журнал проверки 21 ссылки диалога и 79 страниц вики |
| [`../logs/experiment-log.md`](../logs/experiment-log.md) | как получена запись |
| [`../inputs/README.md`](../inputs/README.md) | провенанс исходного экспорта |
| [`../feedback/review-notes.md`](../feedback/review-notes.md) | ограничения чтения |
