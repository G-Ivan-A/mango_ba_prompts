---
status: draft
version: 0.1
updated: 2026-06-11
ai-generated: true
type: registry
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/52"
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

## Маппинг процессов

| № | Процесс | Операции | Паттерн | Рекомендуемые промпты |
| --- | --- | --- | --- | --- |
| 1 | Формирование ФТ/ТЗ | `ingestion`, `understanding`, `documentation`, `solution_design` | — (план) | `asr-ingestion-oneshot`, `glossary-context-understanding-*`, `fr-documentation-*`, `constraints-documentation-*`, `technical-details-solution-design-*` |
| 2 | Валидация ФТ/ТЗ | `validation`, `quality` | — (план) | `fr-validation-stepwise`, `fr-validation-oneshot` |
| 3 | Анализ тендерных ТЗ | `ingestion`, `understanding`, `validation`, `risk_analysis` | — (план) | — (промптов пока нет) |
| 4 | Формирование UC/US | `modeling`, `understanding` | — (план) | `uc-modeling-*`, `us-modeling-*` |
| 5 | Визуализация UML/BPMN | `modeling`, `documentation` | — (план) | — (промптов пока нет) |
| 6 | Помощь ПО/ПМ | `understanding`, `documentation` | — (план) | `meeting-team-documentation-stepwise`, `meeting-customer-documentation-stepwise`, `questions-customer-understanding-*`, `letter-customer-documentation-legacy` |
| 7 | Статистика | `quality`, `ingestion` | — (план) | — (legacy в `prompts/archive/`, активного промпта нет) |
| 8 | Impact Analysis | `impact_analysis`, `reverse_requirements` | — (план) | — (промптов пока нет) |
| 9 | Risk Analysis | `risk_analysis`, `release_readiness`, `validation` | — (план) | — (промптов пока нет) |

`*` — означает оба режима: `stepwise` и `oneshot`. Полные имена файлов —
в [`prompts/`](../../prompts/).

## Как пользоваться индексом

1. Найдите свой процесс в таблице.
2. Возьмите рекомендуемый промпт из `prompts/` (см. frontmatter:
   `temperature`, `status`).
3. Если промпта нет («—») — это known gap: создайте промпт по временному
   workflow из [CONTRIBUTING.md](../../CONTRIBUTING.md) или issue.

## Правила ведения

- Детальные описания процессов добавляются отдельными файлами
  `NN-<process-name>.md` в этом каталоге по мере необходимости
  (Anti-Inflation: файл создаётся только под реальный контент).
- При добавлении/архивации промпта обновите строку соответствующего
  процесса в этом индексе (проверяется в PR review).
- Колонка «Паттерн» заполняется по мере создания паттернов в
  [`patterns/`](../../patterns/).
