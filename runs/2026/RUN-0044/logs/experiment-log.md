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

# Журнал фиксации прогона RUN-0044

## Цель

Зафиксировать экспорт чата `908_2-chat-export-1787302303728.json` отдельной записью прогона с `run_type: statistics` (issue #309): накопить статистику применения промптов и операций процесса БА.

## Шаги

1. Вложение issue скачано и разобрано как JSON; экспорт читаем, ветка диалога восстановлена по `parentId` — 16 реплик.
2. Статистика посчитана `experiments/issue_309_run_stats.py` (объём, токены, сессии, вложения, эвристическая разметка операций).
3. Артефакты записи порождены `experiments/issue_309_fixate_runs.py`.
4. Исходный JSON в репозиторий не добавлялся — по требованию issue #309 исходные файлы в репозитории не остаются; вместо них в [`../inputs/README.md`](../inputs/README.md) зафиксирован провенанс (ссылка, размер, SHA-256).

## Наблюдения

- диалог шёл с 2025-12-18 по 2025-12-18 (1 рабочих сессий);
- моделей задействовано: 1 (qwen3-max-2025-10-30);
- вложений в диалоге: 0 различных файлов.
