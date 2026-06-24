---
status: draft
version: 0.1
updated: 2026-06-24
ai-generated: true
type: analysis
scope: runs
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/217"
related_artifacts:
  - "runs/CONTRACT.md"
  - "standards/runs-contract-standard.md"
  - "scripts/validate_issue_217_runs_log_contract.py"
---

# Аудит контракта runs: Markdown-логи

## Контекст

Issue #217 зафиксировал проблему: в `runs/REGISTRY.md` видны основные
результаты в `outputs/`, но логи либо не записаны, либо записаны в разных
форматах. Требование: для каждого факта прохода должен существовать
Markdown-лог, чтобы можно было анализировать успешные, неуспешные и частично
успешные действия.

Запрошенный путь `docs/analisis` нормализован в существующий каталог
`docs/analysis/`.

## Проверенные контракты и артефакты

| Артефакт | Наблюдение до исправления | Решение |
| --- | --- | --- |
| `runs/CONTRACT.md` | Требовал каталог `logs/`, но не требовал Markdown-лог. Заголовок типов не связывал таблицу явно с `run_type`. | Добавлены `contract_id: runs-contract`, заголовок `# runs-contract`, таблица `Типы run'ов (run_type)` и обязательное правило Markdown-лога. |
| `standards/runs-contract-standard.md` | Для `logs/` использовалось SHOULD, а `run_type` отсутствовал в минимальных обязательных полях стандарта. | `run_type` и основной Markdown-лог переведены в MUST. |
| `runs/REGISTRY.md` | Таблица показывала основной результат, но не показывала лог прохода. | Добавлена колонка `Лог` с каноническим Markdown-логом каждого run. |
| `runs/2026/*/metadata.yaml` | RUN-0001..RUN-0010 не имели `logs:`; `RUN-0013` ссылался только на технический `.log`. | В metadata добавлены ссылки на канонические Markdown-логи. |
| `scripts/validate_issue_123_runs_contract.py` и `scripts/validate_issue_133_runs_restructure.py` | Проверяли структуру каталогов и типы run, но не наличие реального Markdown-лога. | Добавлен отдельный валидатор issue #217. |

## Найденные несоответствия

- RUN-0001..RUN-0010 содержали только `logs/.gitkeep`, то есть фактический лог
  отсутствовал.
- `RUN-0011` и `RUN-0012` имели `logs/experiment-log.md`, но как
  `business-task` не имели канонического `logs/business-task-log.md`.
- `RUN-0013` имел `logs/generation.log`, но не имел Markdown-лог, пригодный для
  просмотра как основной журнал прохода.
- Контракт не фиксировал, что `.gitkeep` не является логом.

## Принятое правило

Каждый факт прохода MUST иметь основной Markdown-лог в `logs/`, даже если проход
завершился ошибкой или частичным успехом. Имя основного лога выбирается по
`run_type`:

| `run_type` | Основной Markdown-лог |
| --- | --- |
| `experiment` | `logs/experiment-log.md` |
| `generation` | `logs/generation-log.md` |
| `validation` | `logs/validation-log.md` |
| `documentation` | `logs/documentation-log.md` |
| `business-task` | `logs/business-task-log.md` |

Дополнительные технические журналы могут оставаться рядом с основным
Markdown-логом, но не заменяют его. `metadata.yaml` должен содержать `logs:` со
ссылкой на основной Markdown-лог.

## Проверка

Регрессионная проверка:

```bash
python3 scripts/validate_issue_217_runs_log_contract.py
```

Проверка блокирует отсутствие Markdown-лога, отсутствие ссылки в `metadata.yaml`,
слабую формулировку контракта и отсутствие логов в `runs/REGISTRY.md`.
