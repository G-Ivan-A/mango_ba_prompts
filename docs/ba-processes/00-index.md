---
status: draft
version: 0.1
updated: 2026-06-11
ai-generated: true
type: registry
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/52"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/66"
---

# Процессы БА: индекс и маппинг на таксономию

Это **единственная централизованная точка** маппинга
«процесс ↔ когнитивные операции ↔ паттерн ↔ рекомендуемые промпты».
Маппинг сознательно **не дублируется во frontmatter** промптов и паттернов,
чтобы не перегружать файлы (см.
[standards/prompt-standard.md](../../standards/prompt-standard.md)) —
по аналогии с единым реестром research-зависимостей
[docs/hub-research-dependencies.md](../hub-research-dependencies.md).

Определения процессов и операций — в [docs/taxonomy.md](../taxonomy.md).
Граф связей экосистемы, классификации направлений, матрицы, подробная карта
workflow и примеры запуска процессов — в
[docs/ba-ecosystem.md](../ba-ecosystem.md).

## Маппинг процессов

Таблица ниже фиксирует расширенный рабочий маршрут процесса. Базовый смысл
процессов остаётся в [docs/taxonomy.md](../taxonomy.md), а дополнительные
операции показывают, какие шаги обычно нужны для полного запуска процесса в
экосистеме.

| № | Процесс | Операции | Паттерн | Рекомендуемые промпты |
| --- | --- | --- | --- | --- |
| 1 | Формирование ФТ/ТЗ | `ingestion`, `understanding`, `modeling`, `documentation`, `solution_design`, `validation` | — (план) | `asr-ingestion-oneshot`, `glossary-context-understanding-*`, `questions-customer-understanding-*`, `us-modeling-*`, `uc-modeling-*`, `fr-documentation-*`, `constraints-documentation-*`, `technical-details-solution-design-*`, `fr-validation-*` |
| 2 | Валидация ФТ/ТЗ | `validation`, `quality`, `risk_analysis` | — (план) | `fr-validation-stepwise`, `fr-validation-oneshot` |
| 3 | Анализ тендерных ТЗ | `ingestion`, `understanding`, `validation`, `risk_analysis`, `quality` | — (план) | `glossary-context-understanding-*`, `questions-customer-understanding-*`, `fr-validation-*` |
| 4 | Формирование UC/US | `understanding`, `modeling`, `validation` | — (план) | `uc-modeling-*`, `us-modeling-*`, `glossary-context-understanding-*` |
| 5 | Визуализация UML/BPMN | `modeling`, `documentation`, `quality` | — (план) | — (промптов пока нет) |
| 6 | Помощь ПО/ПМ | `ingestion`, `understanding`, `documentation`, `governance` | — (план) | `asr-ingestion-oneshot`, `meeting-team-documentation-stepwise`, `meeting-customer-documentation-stepwise`, `questions-customer-understanding-*`, `letter-customer-documentation-legacy` |
| 7 | Статистика | `ingestion`, `quality`, `research` | — (план) | — (legacy в `prompts/archive/`, активного промпта нет) |
| 8 | Impact Analysis | `reverse_requirements`, `impact_analysis`, `validation`, `governance` | — (план) | — (промптов пока нет) |
| 9 | Risk Analysis | `risk_analysis`, `release_readiness`, `validation`, `quality` | — (план) | — (промптов пока нет) |

`*` — означает оба режима: `stepwise` и `oneshot`. Полные имена файлов —
в [`prompts/`](../../prompts/).

## Как пользоваться индексом

1. Определите направление разработки и пакет документов по
   [экосистемной карте](../ba-ecosystem.md).
2. Найдите свой процесс в таблице.
3. Возьмите рекомендуемый промпт из `prompts/` (см. frontmatter:
   `temperature`, `status`).
4. Если промпта нет («—») — это known gap: создайте промпт по временному
   workflow из [CONTRIBUTING.md](../../CONTRIBUTING.md) или issue.

## Правила ведения

- Детальные описания процессов добавляются отдельными файлами
  `NN-<process-name>.md` в этом каталоге по мере необходимости
  (Anti-Inflation: файл создаётся только под реальный контент).
- При добавлении/архивации промпта обновите строку соответствующего
  процесса в этом индексе (проверяется в PR review).
- Колонка «Паттерн» заполняется по мере создания паттернов в
  [`patterns/`](../../patterns/).
