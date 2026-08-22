---
status: draft
version: 0.1
updated: 2026-08-22
ai-generated: true
type: log
scope: mango-only
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/309"
related_artifacts:
  - "standards/runs-contract-standard.md"
  - "experiments/issue_309_run_stats.py"
---

# Журнал фиксации прогона RUN-0032

## Цель

Зафиксировать экспорт чата `792_2-chat-export-1787302348708.json` отдельной записью прогона с `run_type: statistics` (issue #309): накопить статистику применения промптов и операций процесса БА.

## Шаги

1. Вложение issue скачано и разобрано как JSON; экспорт читаем, ветка диалога восстановлена по `parentId` — 62 реплик.
2. Статистика посчитана `experiments/issue_309_run_stats.py` (объём, токены, сессии, вложения, эвристическая разметка операций).
3. Артефакты записи порождены `experiments/issue_309_fixate_runs.py`.
4. Исходный JSON в репозиторий не добавлялся — по требованию issue #309 исходные файлы в репозитории не остаются; вместо них в [`../inputs/README.md`](../inputs/README.md) зафиксирован провенанс (ссылка, размер, SHA-256).

## Наблюдения

- диалог шёл с 2025-10-15 по 2025-11-14 (4 рабочих сессий);
- моделей задействовано: 2 (qwen3-coder-plus, qwen3-max);
- вложений в диалоге: 1 различных файлов.
