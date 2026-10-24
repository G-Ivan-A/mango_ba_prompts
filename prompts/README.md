---
status: draft
version: 0.1
updated: 2026-10-24
ai-generated: true
type: navigation
scope: prompts
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/65"
---

> **LLM Loading Contract — full layer.**
> Start with [`prompts/README.executable.md`](README.executable.md). Load this full file
> only when an escalation trigger in the executable companion is true: explicit
> request for full/rationale/history, missing required section in executable,
> need for exact wording/table/reference, or editing/validating this full file.
> Otherwise do not load this file into context.

# Prompts — навигация по библиотеке промптов

Этот README — точка входа в `prompts/` для бизнес-аналитика Mango. Он помогает за
5 минут выбрать нужный prompt-файл, понять режим (`stepwise`, `oneshot`,
`legacy`), увидеть связь с процессами БА и понять, как давать фидбек.

Полный стандарт промптов закреплён в
<https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/prompt-standard.md>
и ADR-001:
<https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/adr/001-prompt-standard.md>.

## Как быстро выбрать промпт

| Если задача | Начните с |
| --- | --- |
| Нужно создать спецификацию бизнес-требований и дизайна решения (BCREQ) | [`bcreq-constitution-governance-oneshot.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md) (Промпт 0), затем шаги по разделу [«BCREQ: маршрутизация»](#bcreq-маршрутизация) |
| Нужно собрать контекст, глоссарий и вопросы заказчику | [`bcreq-context-understanding-stepwise.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-context-understanding-stepwise.md) или [`bcreq-in-understanding-oneshot.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-in-understanding-oneshot.md) |
| Нужно определить затронутые продукты и команды | [`bcreq-products-impact-analysis-stepwise.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-products-impact-analysis-stepwise.md) |
| Нужно сформировать User Story или Use Case | [`bcreq-scenarios-modeling-oneshot.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-scenarios-modeling-oneshot.md) (`тип: US \| UC`) или [`bcreq-uc-modeling-stepwise.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-uc-modeling-stepwise.md) |
| Нужно написать функциональные требования | [`bcreq-fr-documentation-stepwise.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-fr-documentation-stepwise.md) или [`bcreq-core-documentation-oneshot.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-core-documentation-oneshot.md) |
| Нужно написать нефункциональные требования | [`bcreq-nfr-documentation-stepwise.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-nfr-documentation-stepwise.md) |
| Нужно проверить черновик требований | [`bcreq-review-validation-oneshot.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-review-validation-oneshot.md) |
| Нужно оформить ограничения и границы скоупа | [`bcreq-constraints-documentation-stepwise.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constraints-documentation-stepwise.md) |
| Нужно описать решение (ОРР) для разработки | [`bcreq-orr-solution-design-stepwise.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-orr-solution-design-stepwise.md) или [`bcreq-work-solution-design-oneshot.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-work-solution-design-oneshot.md) |
| Нужно собрать риски, зависимости и план приёмки | [`bcreq-extra-risk-analysis-stepwise.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-extra-risk-analysis-stepwise.md) |
| Нужно обработать ASR-расшифровку | [`asr-ingestion-oneshot.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/asr-ingestion-oneshot.md) |
| Нужно сделать резюме встречи | [`meeting-customer-documentation-stepwise.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/meeting-customer-documentation-stepwise.md) или [`meeting-team-documentation-stepwise.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/meeting-team-documentation-stepwise.md) |
| Нужно суммаризировать длинную сессию работы с LLM | [`session-debug-documentation-oneshot.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/session-debug-documentation-oneshot.md) |

## BCREQ: маршрутизация

Набор BCREQ (issue #388) создаёт спецификацию бизнес-требований и дизайна
решения по мета-стандартам Задачи 2:
[архитектура промптов](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-architecture.md),
[композиция документа](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-composition-standard.md),
[контракт гейтов](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/contracts/bcreq-stage-gates.md).
Каждый промпт начинается блоком «Конституция и позиция»: **пройдено / текущий /
рекомендуемый следующий** — и заканчивается блоком «Состояние BCREQ», который
БА вставляет в следующий вызов.

Два маршрута:

- **Ручной (stepwise)** — БА ведёт шаги сам, по одному чату на шаг; промпт
  ждёт ответа после каждого подшага («Стоп-гейт»). Пошаговая инструкция —
  на сайте, вкладка «Процессы».
- **Агентный (oneshot)** — ИИ-агент выполняет стадию A-IN, A-CORE или A-WORK
  одним вызовом, копит вопросы в 8.4 и заканчивает отчётом по гейту. Гейт
  агент не пересекает: его решают люди.

| Шаг | Разделы BCREQ | Ручной маршрут (stepwise) | Агентный маршрут (oneshot) | Гейт после шага |
| --- | --- | --- | --- | --- |
| Ш-0 | Каркас, параметры, конституция | [`bcreq-constitution-governance-oneshot.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md) | [`bcreq-constitution-governance-oneshot.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md) | — |
| Ш-1 | 1 Глоссарий, 2 Бизнес-контекст | [`bcreq-context-understanding-stepwise.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-context-understanding-stepwise.md) | [`bcreq-in-understanding-oneshot.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-in-understanding-oneshot.md) (стадия A-IN = Ш-1 + Ш-2) | — |
| Ш-2 | ＋2.5 Продукты и стейкхолдеры | [`bcreq-products-impact-analysis-stepwise.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-products-impact-analysis-stepwise.md) | A-IN | Г-IN (решает БА) |
| Ш-3 | 3 Функциональные требования | [`bcreq-fr-documentation-stepwise.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-fr-documentation-stepwise.md) | [`bcreq-core-documentation-oneshot.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-core-documentation-oneshot.md) (стадия A-CORE = Ш-3…Ш-5) | — |
| Ш-4 | 4 Нефункциональные требования | [`bcreq-nfr-documentation-stepwise.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-nfr-documentation-stepwise.md) | A-CORE | — |
| Ш-5 | 7 UC, прогон 1 | [`bcreq-uc-modeling-stepwise.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-uc-modeling-stepwise.md) (`прогон: 1`) | A-CORE | Г-С1 «Согласование 1» (решает Заказчик) |
| Ш-6 | 5 Описание решения (ОРР) | [`bcreq-orr-solution-design-stepwise.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-orr-solution-design-stepwise.md) | [`bcreq-work-solution-design-oneshot.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-work-solution-design-oneshot.md) (стадия A-WORK = Ш-6…Ш-9) | — |
| Ш-7 | 6 Особенности и ограничения | [`bcreq-constraints-documentation-stepwise.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constraints-documentation-stepwise.md) | A-WORK | — |
| Ш-8 | 7 UC, прогон 2 | [`bcreq-uc-modeling-stepwise.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-uc-modeling-stepwise.md) (`прогон: 2`) | A-WORK | — |
| Ш-9 | 8 Риски, зависимости, приёмка | [`bcreq-extra-risk-analysis-stepwise.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-extra-risk-analysis-stepwise.md) | A-WORK | — |
| Ш-В | Валидация документа второй ролью | [`bcreq-review-validation-oneshot.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-review-validation-oneshot.md) | [`bcreq-review-validation-oneshot.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-review-validation-oneshot.md) | Г-W (решают ПО продукта, архитектор, руководитель КК) |
| Ш-С | US или UC вне документа (2.12 / 2.13) | [`bcreq-scenarios-modeling-oneshot.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-scenarios-modeling-oneshot.md) (`тип: US \| UC`) | [`bcreq-scenarios-modeling-oneshot.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-scenarios-modeling-oneshot.md) | — |

Возвраты: если критерий гейта не выполнен, промпт рекомендует возврат в
формате «стадия · шаг · причина»; решение о возврате принимает БА.

## Матрица промптов

В активной библиотеке сейчас 20 файлов в `prompts/`: 14 промптов BCREQ и 6
сопутствующих. В архиве сохранены 24 файла в `prompts/archive/` для истории,
сравнения, аудита и ссылок из записанных прогонов.

Колонка **«Название»** — это поле `title` из frontmatter: человекочитаемое
название промпта на русском, которое выводится жирным заголовком в интерфейсе
[GitHub Pages](https://g-ivan-a.github.io/mango_ba_prompts/). Колонка
**«Токен»** — это поле `id`: уникальный идентификатор промпта для аналитики
использования, по схеме `mango-[операция]-[режим]` (совпадает с именем файла с
префиксом `mango-`). Оба поля обязательны и описаны в
<https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/prompt-standard.md>
и ADR-001.

### 0. BCREQ: спецификация бизнес-требований и дизайна решения

Новые промпты issue #388. Порядок вызова — в разделе
[«BCREQ: маршрутизация»](#bcreq-маршрутизация).

| Файл | Название | Токен | Назначение | Режим | Статус | Версия | Когнитивная операция | Процесс БА |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [`bcreq-constitution-governance-oneshot.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md) | BCREQ Ш-0: конституция | `mango-bcreq-constitution-governance-oneshot` | Промпт 0: задаёт структуру BCREQ из 8 разделов, стили, правила Р1–Р7, защиты АД-1…АД-7, параметры задачи и каркас документа со статусами. | `oneshot` | `draft` | `0.1` | `governance` | Формирование ФТ/ТЗ |
| [`bcreq-context-understanding-stepwise.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-context-understanding-stepwise.md) | BCREQ Ш-1: глоссарий и контекст | `mango-bcreq-context-understanding-stepwise` | Ш-1: пошагово формирует раздел 1 «Глоссарий» и раздел 2 «Бизнес-контекст» (проблема, цель, границы) из материалов Заказчика; вопросы — в 8.4. | `stepwise` | `draft` | `0.1` | `understanding` | Формирование ФТ/ТЗ; Анализ тендерных ТЗ; Формирование UC/US; Помощь ПО/ПМ |
| [`bcreq-products-impact-analysis-stepwise.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-products-impact-analysis-stepwise.md) | BCREQ Ш-2: продукты и команды | `mango-bcreq-products-impact-analysis-stepwise` | Ш-2: пошагово формирует пункт ＋2.5 — затронутые продукты по таксономии, продуктовые команды, согласующих и стыки; готовит отчёт к гейту Г-IN. | `stepwise` | `draft` | `0.1` | `impact_analysis` | Формирование ФТ/ТЗ; Impact Analysis |
| [`bcreq-fr-documentation-stepwise.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-fr-documentation-stepwise.md) | BCREQ Ш-3: функциональные требования | `mango-bcreq-fr-documentation-stepwise` | Ш-3: пошагово формирует раздел 3 «Функциональные требования» (вариант delta или new) с фильтрами Ф1–Ф4, условиями EARS и трассой к 2.4.1. | `stepwise` | `draft` | `0.1` | `documentation` | Формирование ФТ/ТЗ |
| [`bcreq-nfr-documentation-stepwise.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-nfr-documentation-stepwise.md) | BCREQ Ш-4: нефункциональные требования | `mango-bcreq-nfr-documentation-stepwise` | Ш-4: пошагово формирует раздел 4 «Нефункциональные требования» по ISO/IEC 25010:2023 — характеристика, метрика, порог, условие, источник; без выдуманных НФТ. | `stepwise` | `draft` | `0.1` | `documentation` | Формирование ФТ/ТЗ |
| [`bcreq-uc-modeling-stepwise.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-uc-modeling-stepwise.md) | BCREQ Ш-5/Ш-8: UC | `mango-bcreq-uc-modeling-stepwise` | Ш-5 и Ш-8: пошагово формирует раздел 7 Use Case — прогон 1 подтверждает ФТ сценариями (покрытие 100 %), прогон 2 добавляет граничные кейсы и ошибки. | `stepwise` | `draft` | `0.1` | `modeling` | Формирование ФТ/ТЗ; Формирование UC/US |
| [`bcreq-orr-solution-design-stepwise.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-orr-solution-design-stepwise.md) | BCREQ Ш-6 (2.6+2.7): ОРР | `mango-bcreq-orr-solution-design-stepwise` | Ш-6: пошагово формирует раздел 5 «Описание решения» — L1 ФДР и контекст C4, при `уровень: L1+L2` — L2 ТС, дельта API, данные; трассировка ФТ ↔ ОРР. | `stepwise` | `draft` | `0.1` | `solution_design` | Формирование ФТ/ТЗ; Impact Analysis |
| [`bcreq-constraints-documentation-stepwise.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constraints-documentation-stepwise.md) | BCREQ Ш-7 (2.8): ограничения | `mango-bcreq-constraints-documentation-stepwise` | Ш-7: пошагово формирует раздел 6 «Особенности реализации и ограничения» — особенность со ссылкой на раздел 5, ограничение с источником и последствием. | `stepwise` | `draft` | `0.1` | `documentation` | Формирование ФТ/ТЗ; Risk Analysis |
| [`bcreq-extra-risk-analysis-stepwise.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-extra-risk-analysis-stepwise.md) | BCREQ Ш-9 (2.14): риски, приёмка | `mango-bcreq-extra-risk-analysis-stepwise` | Ш-9: пошагово формирует раздел 8 — риски с мерой и владельцем, зависимости, план приёмки «Дано / Когда / Тогда», сводит 8.4 и 8.5; готовит данные к Г-W. | `stepwise` | `draft` | `0.1` | `risk_analysis` | Формирование ФТ/ТЗ; Risk Analysis |
| [`bcreq-review-validation-oneshot.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-review-validation-oneshot.md) | BCREQ Ш-В: валидация документа | `mango-bcreq-review-validation-oneshot` | Ш-В: проверяет документ BCREQ второй ролью по чек-листам разделов — «пункт → проблема → вариант»; не объявляет готовность, готовит отчёт к гейту Г-W. | `oneshot` | `draft` | `0.1` | `validation` | Валидация ФТ/ТЗ; Формирование ФТ/ТЗ; Анализ тендерных ТЗ; Impact Analysis; Risk Analysis |
| [`bcreq-scenarios-modeling-oneshot.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-scenarios-modeling-oneshot.md) | BCREQ Ш-С (2.12/2.13): US, UC | `mango-bcreq-scenarios-modeling-oneshot` | Ш-С: формирует User Story с критериями приёмки или Use Case (параметр `тип`: US или UC) вне документа BCREQ на основе контекста Ш-1; трассирует сценарии к ФТ. | `oneshot` | `draft` | `0.1` | `modeling` | Формирование UC/US; Формирование ФТ/ТЗ |
| [`bcreq-in-understanding-oneshot.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-in-understanding-oneshot.md) | BCREQ A-IN: контекст, продукты | `mango-bcreq-in-understanding-oneshot` | Стадия A-IN для ИИ-агента: Ш-1 и Ш-2 одним вызовом — разделы 1, 2 и ＋2.5, словари и расхождения терминов; заканчивается отчётом по гейту Г-IN. | `oneshot` | `draft` | `0.1` | `understanding` | Формирование ФТ/ТЗ; Анализ тендерных ТЗ; Помощь ПО/ПМ |
| [`bcreq-core-documentation-oneshot.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-core-documentation-oneshot.md) | BCREQ A-CORE: ФТ, НФТ, UC | `mango-bcreq-core-documentation-oneshot` | Стадия A-CORE для ИИ-агента: Ш-3…Ш-5 одним вызовом — разделы 3, 4 и 7 (прогон 1); заканчивается отчётом по гейту Г-С1 «Согласование 1» для Заказчика. | `oneshot` | `draft` | `0.1` | `documentation` | Формирование ФТ/ТЗ |
| [`bcreq-work-solution-design-oneshot.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-work-solution-design-oneshot.md) | BCREQ A-WORK: решение, риски | `mango-bcreq-work-solution-design-oneshot` | Стадия A-WORK для ИИ-агента: Ш-6…Ш-9 одним вызовом — разделы 5, 6, 7 (прогон 2) и 8; заканчивается предварительным отчётом по гейту Г-W. | `oneshot` | `draft` | `0.1` | `solution_design` | Формирование ФТ/ТЗ; Impact Analysis; Risk Analysis |

### 1. Формирование ФТ/ТЗ

| Файл | Название | Токен | Назначение | Режим | Статус | Версия | Когнитивная операция | Процесс БА |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [`asr-ingestion-oneshot.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/asr-ingestion-oneshot.md) | ASR: Нормализация транскрипции | `mango-asr-ingestion-oneshot` | Нормализует ASR-расшифровку в читаемый вход для анализа без потери смысла. | `oneshot` | `draft` | `0.1` | `ingestion` | Формирование ФТ/ТЗ; Помощь ПО/ПМ |
| [`asr-ingestion-legacy.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/asr-ingestion-legacy.md) | ASR: Обработка транскрипции (устаревший) | `mango-asr-ingestion-legacy` | Исторический итеративный вариант обработки ASR-транскрипций. | `legacy` | `draft` | `1.0` | `ingestion` | Формирование ФТ/ТЗ; Помощь ПО/ПМ |

### 2. Валидация ФТ/ТЗ и анализ тендерных ТЗ

| Файл | Название | Токен | Назначение | Режим | Статус | Версия | Когнитивная операция | Процесс БА |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

### 3. Формирование UC/US

| Файл | Название | Токен | Назначение | Режим | Статус | Версия | Когнитивная операция | Процесс БА |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

### 4. Помощь ПО/ПМ

| Файл | Название | Токен | Назначение | Режим | Статус | Версия | Когнитивная операция | Процесс БА |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [`meeting-customer-documentation-stepwise.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/meeting-customer-documentation-stepwise.md) | Встреча с клиентом: Резюме | `mango-meeting-customer-documentation-stepwise` | Пошагово формирует резюме встречи с заказчиком. | `stepwise` | `draft` | `0.1` | `documentation` | Помощь ПО/ПМ |
| [`meeting-team-documentation-stepwise.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/meeting-team-documentation-stepwise.md) | Встреча команды: Резюме | `mango-meeting-team-documentation-stepwise` | Пошагово формирует резюме внутренней встречи команды. | `stepwise` | `draft` | `0.1` | `documentation` | Помощь ПО/ПМ |
| [`letter-customer-documentation-legacy.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/letter-customer-documentation-legacy.md) | Письмо клиенту: Сопровождение (устаревший) | `mango-letter-customer-documentation-legacy` | Унаследованный промпт для сопроводительного письма заказчику. | `legacy` | `draft` | `1.0` | `documentation` | Помощь ПО/ПМ |

### 5. Отладка и суммаризация сессий

| Файл | Название | Токен | Назначение | Режим | Статус | Версия | Когнитивная операция | Процесс БА |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [`session-debug-documentation-oneshot.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/session-debug-documentation-oneshot.md) | Сессия LLM: Суммаризация | `mango-session-debug-documentation-oneshot` | Суммаризирует длинную сессию работы с LLM в структурированное резюме (контекст, ключевые решения, проблемы, открытые вопросы, шаги), совместимое с `pr-ops/session-digests.md`. | `oneshot` | `draft` | `0.1` | `documentation` | Помощь ПО/ПМ |

### 6. Архив: статистика и исторические генераторы

| Файл | Название | Токен | Назначение | Режим | Статус | Версия | Когнитивная операция | Процесс БА |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [`tz-stats-generator-legacy.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/tz-stats-generator-legacy.md) | ТЗ: Статистика, расширенный (архив) | `mango-tz-stats-generator-legacy` | Архивный расширенный генератор статистики по ТЗ. | `legacy` | `archived` | `1.0` | `quality` | Статистика |
| [`tz-stats-generator-simple-legacy.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/tz-stats-generator-simple-legacy.md) | ТЗ: Статистика, простой (архив) | `mango-tz-stats-generator-simple-legacy` | Архивный простой генератор статистики по ТЗ. | `legacy` | `archived` | `1.0` | `quality` | Статистика |
| [`usecase-stepwise-generator-legacy.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/usecase-stepwise-generator-legacy.md) | Use Case: Генератор (архив) | `mango-usecase-stepwise-generator-legacy` | Архивный Hub-style генератор Use Case в пошаговой логике. | `legacy` | `archived` | `1.0` | `modeling` | Формирование UC/US |
| [`usecase-stepwise-generator-simple-legacy.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/usecase-stepwise-generator-simple-legacy.md) | Use Case: Генератор, простой (архив) | `mango-usecase-stepwise-generator-simple-legacy` | Архивный простой генератор Use Case. | `legacy` | `archived` | `1.0` | `modeling` | Формирование UC/US |
| [`user-story-generator-legacy.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/user-story-generator-legacy.md) | User Story: Генератор (архив) | `mango-user-story-generator-legacy` | Архивный Hub-style генератор User Story из сырого запроса. | `legacy` | `archived` | `1.0` | `modeling` | Формирование UC/US |
| [`user-story-generator-simple-legacy.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/user-story-generator-simple-legacy.md) | User Story: Генератор, простой (архив) | `mango-user-story-generator-simple-legacy` | Архивный простой генератор User Story. | `legacy` | `archived` | `1.0` | `modeling` | Формирование UC/US |

### 7. Архив: промпты, заменённые набором BCREQ (issue #388)

Файлы перенесены в `prompts/archive/` и не удалены: на них ссылаются
записанные прогоны в `runs/`. Замена указана баннером в начале каждого файла.

| Файл | Название | Токен | Назначение | Режим | Статус | Версия | Когнитивная операция | Процесс БА |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [`constraints-documentation-oneshot.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/constraints-documentation-oneshot.md) | Ограничения: За один ответ | `mango-constraints-documentation-oneshot` | Формирует раздел 6 ограничений одним ответом. | `oneshot` | `archived` | `0.1` | `documentation` | Формирование ФТ/ТЗ |
| [`constraints-documentation-stepwise.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/constraints-documentation-stepwise.md) | Ограничения: Документирование | `mango-constraints-documentation-stepwise` | Пошагово формирует раздел 6 «Особенности реализации / Ограничения». | `stepwise` | `archived` | `0.1` | `documentation` | Формирование ФТ/ТЗ |
| [`fr-documentation-oneshot.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/fr-documentation-oneshot.md) | ФТ: Генерация за один ответ | `mango-fr-documentation-oneshot` | Формирует раздел 4 ФТ одним ответом при уже собранном контексте. | `oneshot` | `archived` | `0.1` | `documentation` | Формирование ФТ/ТЗ |
| [`fr-documentation-stepwise.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/fr-documentation-stepwise.md) | ФТ: Генерация требований | `mango-fr-documentation-stepwise` | Пошагово формирует раздел 4 «Функциональные требования» на основе контекста, US и UC. | `stepwise` | `archived` | `0.1` | `documentation` | Формирование ФТ/ТЗ |
| [`fr-validation-legacy.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/fr-validation-legacy.md) | ФТ: Валидация (устаревший) | `mango-fr-validation-legacy` | Унаследованный вариант анализа и валидации функциональных требований. | `legacy` | `archived` | `1.0` | `validation` | Валидация ФТ/ТЗ; Анализ тендерных ТЗ |
| [`fr-validation-oneshot.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/fr-validation-oneshot.md) | ФТ: Экспресс-валидация | `mango-fr-validation-oneshot` | Выполняет экспресс-валидацию и перегенерацию ФТ одним ответом. | `oneshot` | `archived` | `0.1` | `validation` | Валидация ФТ/ТЗ; Анализ тендерных ТЗ |
| [`fr-validation-stepwise.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/fr-validation-stepwise.md) | ФТ: Валидация и аудит | `mango-fr-validation-stepwise` | Пошагово проводит аудит ФТ и помогает перегенерировать требования по сырым данным. | `stepwise` | `archived` | `0.1` | `validation` | Валидация ФТ/ТЗ; Формирование ФТ/ТЗ; Анализ тендерных ТЗ |
| [`glossary-context-understanding-oneshot.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/glossary-context-understanding-oneshot.md) | Контекст: Терминология за один ответ | `mango-glossary-context-understanding-oneshot` | Формирует разделы 1-2 ТЗ за один ответ при достаточном входном контексте. | `oneshot` | `archived` | `0.1` | `understanding` | Формирование ФТ/ТЗ; Анализ тендерных ТЗ; Формирование UC/US |
| [`glossary-context-understanding-stepwise.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/glossary-context-understanding-stepwise.md) | Контекст: Терминология и цели | `mango-glossary-context-understanding-stepwise` | Пошагово формирует терминологию, проблему, цель и задачи для разделов 1-2 ТЗ. | `stepwise` | `archived` | `0.1` | `understanding` | Формирование ФТ/ТЗ; Анализ тендерных ТЗ; Формирование UC/US |
| [`questions-customer-understanding-legacy.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/questions-customer-understanding-legacy.md) | Вопросы: Подготовка заказчику (устаревший) | `mango-questions-customer-understanding-legacy` | Унаследованный вариант анализа запроса и подготовки вопросов заказчику. | `legacy` | `archived` | `1.0` | `understanding` | Формирование ФТ/ТЗ; Анализ тендерных ТЗ; Помощь ПО/ПМ |
| [`questions-customer-understanding-stepwise.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/questions-customer-understanding-stepwise.md) | Вопросы: Выявление потребностей | `mango-questions-customer-understanding-stepwise` | Пошагово нормализует сырой запрос и готовит точные уточняющие вопросы заказчику. | `stepwise` | `archived` | `0.1` | `understanding` | Формирование ФТ/ТЗ; Анализ тендерных ТЗ; Помощь ПО/ПМ |
| [`technical-details-solution-design-legacy.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/technical-details-solution-design-legacy.md) | Технические детали: Доработки (устаревший) | `mango-technical-details-solution-design-legacy` | Унаследованный вариант подготовки раздела 7 «Список доработок». | `legacy` | `archived` | `1.0` | `solution_design` | Формирование ФТ/ТЗ |
| [`technical-details-solution-design-oneshot.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/technical-details-solution-design-oneshot.md) | Технические детали: За один ответ | `mango-technical-details-solution-design-oneshot` | Формирует раздел 7 для разработки одним ответом. | `oneshot` | `archived` | `0.1` | `solution_design` | Формирование ФТ/ТЗ |
| [`technical-details-solution-design-stepwise.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/technical-details-solution-design-stepwise.md) | Технические детали: Проектирование | `mango-technical-details-solution-design-stepwise` | Пошагово формирует раздел 7 «Список доработок» для разработки. | `stepwise` | `archived` | `0.1` | `solution_design` | Формирование ФТ/ТЗ |
| [`uc-modeling-oneshot.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/uc-modeling-oneshot.md) | Use Case: Моделирование за один ответ | `mango-uc-modeling-oneshot` | Формирует Use Case по Cockburn одним ответом. | `oneshot` | `archived` | `0.1` | `modeling` | Формирование UC/US; Формирование ФТ/ТЗ |
| [`uc-modeling-stepwise.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/uc-modeling-stepwise.md) | Use Case: Моделирование | `mango-uc-modeling-stepwise` | Пошагово формирует Use Case по Cockburn из сырого описания. | `stepwise` | `archived` | `0.1` | `modeling` | Формирование UC/US; Формирование ФТ/ТЗ |
| [`us-modeling-oneshot.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/us-modeling-oneshot.md) | User Story: Формирование за один ответ | `mango-us-modeling-oneshot` | Формирует User Story одним ответом. | `oneshot` | `archived` | `0.1` | `modeling` | Формирование UC/US; Формирование ФТ/ТЗ |
| [`us-modeling-stepwise.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/us-modeling-stepwise.md) | User Story: Формирование | `mango-us-modeling-stepwise` | Пошагово формирует User Story из сырого запроса. | `stepwise` | `archived` | `0.1` | `modeling` | Формирование UC/US; Формирование ФТ/ТЗ |

Процесс «Визуализация UML/BPMN» пока не имеет активного рекомендуемого промпта;
«Impact Analysis» и «Risk Analysis» опираются на шаги BCREQ Ш-2, Ш-6, Ш-9 и Ш-В. Это зафиксировано в центральном индексе:
<https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/00-index.md>.

## Две структуры промптов

ADR-001 допускает две структуры. Новые промпты не обязаны быть одинаковыми по
заголовкам, но должны явно соответствовать одной из этих моделей.

### Структура A: Hub-style prompt

Скелет:

```markdown
# РОЛЬ
# КАК РАБОТАЕМ
# ПРАВИЛА
# ФОРМАТ ВЫВОДА
# НАЧНЕМ?
```

Когда использовать:

- промпт компактный и решает один понятный сценарий;
- не нужны длинные stop-gates и многошаговое согласование;
- промпт переносится из Хаба или готовится как переносимая hub-ready практика.

Преимущества: быстро читается, легко копируется, хорошо подходит для зрелых
role-prompting сценариев.

Ограничения: хуже выражает многошаговые проверки, согласования и сложный
workflow формирования ФТ/ТЗ.

Примеры:

- <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/user-story-generator-legacy.md>
- <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/usecase-stepwise-generator-legacy.md>

### Структура B: Mango BA workflow prompt

Скелет:

```markdown
# РОЛЬ
# ЖЕСТКИЕ ПРАВИЛА
# РЕЖИМ РАБОТЫ
# ШАГ 1
# ШАГ 2
# ФОРМАТ ВЫВОДА
# ОГРАНИЧЕНИЯ
```

Когда использовать:

- результат формируется через несколько шагов и требует подтверждений;
- есть риск домыслов, смешения бизнес-требований и реализации;
- нужно явно разделить сбор контекста, генерацию, проверку и ограничения;
- агент должен работать как workflow БА, а не как генератор одного ответа.

Преимущества: видны контрольные точки, правила, ограничения и формат результата.

Ограничения: структура длиннее и требует аккуратного выбора режима. Для коротких
зрелых prompt-assets она может быть избыточной.

Примеры:

- <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/glossary-context-understanding-stepwise.md>
- <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/fr-documentation-stepwise.md>
- <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/fr-validation-oneshot.md>

## Режимы: `stepwise`, `oneshot`, `legacy`

Режим — последний токен имени файла. Он описывает способ взаимодействия агента с
пользователем, а не роль агента.

| Токен | Значение | Когда использовать | Обоснование |
| --- | --- | --- | --- |
| `stepwise` | Агент делает работу по шагам, показывает промежуточный результат и ждёт подтверждения. | Сбор контекста, ФТ/ТЗ, UC/US, валидация с уточнениями. | Близко к ReAct-подходу `thought -> act -> observe`, где следующий шаг зависит от наблюдения и обратной связи. См. <https://arxiv.org/abs/2210.03629> и <https://www.promptingguide.ai/techniques/react>. |
| `oneshot` | Агент выдаёт полный результат одним ответом без промежуточного диалога. | Достаточный вход, быстрый аудит, нормализация, постобработка ASR, низкая цена уточнений. | Соответствует one-shot prompting / one-shot learning: задача решается за один проход. См. <https://www.promptingguide.ai/techniques/fewshot>. |
| `legacy` | Исторический или унаследованный вариант, сохранённый для совместимости, сравнения или аудита. | Старый стиль, миграция из Хаба, активный черновик до замены, архивный эталон. | `legacy` — стандартный технический термин для унаследованных артефактов. |

Устаревшие токены:

- `expert` не используется как режим, потому что это роль агента, а не способ
  взаимодействия.
- `express` не используется как режим, потому что это маркетинговое слово; для
  одношагового исполнения принят технический токен `oneshot`.

Важно: `legacy` и `archived` — разные вещи. `legacy` — режим в имени файла.
`archived` — статус во frontmatter. Поэтому файл `*-legacy.md` может оставаться
активным черновиком со `status: draft`, а архивный файл должен иметь
`status: archived` и жить в `prompts/archive/`.

## Как тестировать и давать фидбек

Перед переводом промпта из `draft` в `canonical` нужен минимум один
зафиксированный прогон в `runs/`. Для рабочей проверки лучше
сделать не меньше трёх прогонов на реальных, но обезличенных данных:

1. Типовой кейс: нормальный вход, ожидаемый результат, без пограничных условий.
2. Сложный кейс: неполный, шумный или противоречивый вход.
3. Регрессионный кейс: пример, где раньше промпт ошибался или требовал ручной
   доработки.

Фидбек создаётся через шаблон:
<https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/.github/ISSUE_TEMPLATE/prompt-feedback.yml>.
Такие issues получают лейбл `prompt:feedback`.

Что указать в фидбеке:

- имя prompt-файла, даже если помните его неточно;
- результат: работает, частично работает, не работает;
- что именно не так: галлюцинации, не тот формат, пропущены разделы, лишняя
  «вода», не учтён контекст;
- обезличенный фрагмент входа и выхода, если он помогает воспроизвести проблему.

Хороший фидбек:

```text
Промпт: bcreq-review-validation-oneshot.md
Результат: частично
Вход: обезличенный черновик ФТ на 12 пунктов.
Проблема: промпт сохранил 4.3 и 4.4, но пропустил противоречие между статусами
"Черновик" и "Отправлено". Ожидал отдельный дефект в отчёте валидации.
```

Плохой фидбек:

```text
Промпт плохой, результат не понравился.
```

Триаж фидбека выполняется в рамках weekly/sprint review: команда группирует
повторяющиеся проблемы, выбирает промпты для доработки, фиксирует изменения в PR
и при необходимости добавляет новый прогон в `runs/YYYY/RUN-XXXX/`.

### Модуль «Проверки» на GitHub Pages

Статус отладки промптов, число зафиксированных тестов из `runs/`,
обратная связь по лейблу `prompt:feedback` и активность использования промптов по
процессам БА агрегируются в модуле **«Проверки»** на
[GitHub Pages](https://g-ivan-a.github.io/mango_ba_prompts/). Данные формируются
скриптом `scripts/generate-pages-data.mjs` в `site/data/checks.json`. Статический
срез обратной связи живёт в `pr-ops/prompt-feedback.json` (поле `prompt` — id
промпта, т.е. имя файла без `.md`); его можно наполнять вручную или скриптом
синхронизации с GitHub Issues.

Назначение директорий проекта зафиксировано так: `scripts/` — вся автоматизация
(генерация GitHub Pages и Python-валидаторы регрессий), `runs/` — каноничное
место тестовых логов, self-test сценариев промптов и результатов процессов.
Отдельной корневой директории `experiments/` в проекте нет.

## Связь с таксономией и процессами БА

Таксономия задаёт 13 когнитивных операций:
<https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/taxonomy.md>.
Операция входит в имя файла по схеме `[домен]-[операция]-[режим].md`, где
`solution_design` записывается как `solution-design`.

Индекс процессов БА задаёт 9 процессов и централизованный маппинг
«процесс -> операции -> рекомендуемые промпты»:
<https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/00-index.md>.
Этот маппинг не дублируется во frontmatter промптов.

Пример процесса «Формирование ФТ/ТЗ»:

1. `asr-ingestion-oneshot.md` очищает расшифровку встречи.
2. `bcreq-constitution-governance-oneshot.md` (Промпт 0) задаёт конституцию,
   параметры задачи и каркас документа BCREQ.
3. `bcreq-context-understanding-stepwise.md` и
   `bcreq-products-impact-analysis-stepwise.md` формируют разделы 1, 2 и ＋2.5;
   гейт Г-IN решает БА.
4. `bcreq-fr-documentation-stepwise.md`, `bcreq-nfr-documentation-stepwise.md`
   и `bcreq-uc-modeling-stepwise.md` (прогон 1) формируют разделы 3, 4 и 7;
   гейт Г-С1 «Согласование 1» решает Заказчик.
5. `bcreq-orr-solution-design-stepwise.md`,
   `bcreq-constraints-documentation-stepwise.md`, `bcreq-uc-modeling-stepwise.md`
   (прогон 2) и `bcreq-extra-risk-analysis-stepwise.md` формируют разделы 5–8.
6. `bcreq-review-validation-oneshot.md` проверяет документ второй ролью перед
   гейтом Г-W.

## Связанные документы

- Репозиторий: <https://github.com/G-Ivan-A/mango_ba_prompts>
- Таксономия 13 операций: <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/taxonomy.md>
- Процессы БА и маппинг: <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/00-index.md>
- Стандарт промптов: <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/prompt-standard.md>
- ADR-001 по стандарту промптов: <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/adr/001-prompt-standard.md>
- Структура паттернов: <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/patterns/README.md>
- Шаблон фидбека: <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/.github/ISSUE_TEMPLATE/prompt-feedback.yml>
- PR #57: <https://github.com/G-Ivan-A/mango_ba_prompts/pull/57>
- PR #59: <https://github.com/G-Ivan-A/mango_ba_prompts/pull/59>
- PR #60: <https://github.com/G-Ivan-A/mango_ba_prompts/pull/60>
- Issue #61: <https://github.com/G-Ivan-A/mango_ba_prompts/issues/61>
- Issue #62: <https://github.com/G-Ivan-A/mango_ba_prompts/issues/62>
- Хаб `hybrid-Intelligence-lab`: <https://github.com/G-Ivan-A/hybrid-Intelligence-lab>
- `clarify-engine-ai`: <https://github.com/G-Ivan-A/clarify-engine-ai>
- `open-ai.ru`: <https://github.com/G-Ivan-A/open-ai.ru>
