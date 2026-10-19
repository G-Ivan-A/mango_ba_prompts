---
status: draft
version: 0.1
updated: 2026-10-19
ai-generated: true
type: index
scope: mango-only
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/378"
---

# Результаты прогона RUN-0074 — задача 1104, золотой набор ошибок ИИ

> Файл **порождён** скриптом [`experiments/issue_378_golden_set.py`](../../../../experiments/issue_378_golden_set.py) из разметки [`experiments/issue_378_golden_data.py`](../../../../experiments/issue_378_golden_data.py) — не редактируйте вручную. Каждая цитата сверена с экспортом чата ([`../logs/quote-verification.md`](../logs/quote-verification.md)).

Прогон фиксирует диалог генерации BCREQ-ФТ «Ручной режим обработки пропущенных вызовов (задание ЗОЗ) в карточке Группы операторов ЛК ВАТС» (задача 1104) ради статистики ошибок ИИ. Результат — не артефакт требований, а размеченный по вхождениям реестр ошибок с привязкой к продуктам, BABOK / TM Forum ODA и слотам mango-ba-ai-runtime, кандидаты в золотые наборы и критерии успеха для промптов, правил и навыков посекционной генерации ФТ.

## Сводка

| Метрика | Значение |
| --- | --- |
| Реплик в ветке диалога | 118 |
| Реплик БА / ответов модели | 59 / 59 |
| Модели | qwen3.7-plus |
| Рабочих сессий (разрыв > 30 мин) | 15 |
| Активное время внутри сессий, мин | 361 |
| Календарный интервал, дн. | 12.3 |
| Токенов на входе (с переотправкой контекста) | 21345501 |
| Токенов на выходе / в том числе reasoning | 174713 / 125603 |
| Вхождений ошибок ИИ | 168 |
| Категорий с вхождениями | 15 из 15 |
| Самые частые категории | C01 (48), C09 (16), C06 (16), C04 (11), C13 (11) |
| Поймано БА в диалоге | 60 (36%) |
| Наборов-кандидатов / кейсов | 6 / 53 |
| Критериев успеха / позитивных кейсов | 22 / 9 |

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
| [`prompt-usage.md`](prompt-usage.md) | распределение операций БА, сессии, вложения |
| [`../logs/metrics.md`](../logs/metrics.md) | метрики по каждой реплике |
| [`../logs/quote-verification.md`](../logs/quote-verification.md) | сверка каждой цитаты с экспортом |
| [`../logs/kb-verification.md`](../logs/kb-verification.md) | сверка утверждений модели с КБ runtime |
| [`../logs/experiment-log.md`](../logs/experiment-log.md) | как получена запись |
| [`../inputs/README.md`](../inputs/README.md) | провенанс исходного экспорта |
| [`../feedback/review-notes.md`](../feedback/review-notes.md) | ограничения чтения и открытые вопросы |
