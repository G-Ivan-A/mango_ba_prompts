---
status: draft
version: 0.2
updated: 2026-06-20
ai-generated: true
type: index
scope: runs
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/123"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/133"
related_artifacts:
  - "runs/CONTRACT.md"
  - "runs/REGISTRY.md"
  - "runs/stats/by-type.md"
---

# Runs: результаты выполнения процессов

## Что это

`runs/` — единый каталог результатов выполнения процессов. Здесь хранятся
зафиксированные прогоны промптов, BA-процессов, анализов и self-test сценариев.
Маршруты и правила работы остаются в `docs/`, `prompts/`, `patterns/` и
`standards/`; результат применения этих правил записывается сюда.

## Как использовать

- Найти существующий run: откройте [`REGISTRY.md`](REGISTRY.md) или статистику
  по типам, датам и процессам.
- Создать новый run: заведите каталог `runs/YYYY/RUN-XXXX/` с
  `metadata.yaml`, `inputs/`, `outputs/`, `feedback/` и `logs/`; в `logs/`
  сразу создайте основной Markdown-лог по `run_type`.
- Минимальные поля `metadata.yaml`: `run_id`, `process`, `run_type`,
  `version`, `date`, `author`, `model`, `status`.
- В `metadata.yaml` поле `logs:` должно ссылаться на основной Markdown-лог.
- Проверить контракт: сверяйтесь с [`CONTRACT.md`](CONTRACT.md) и запускайте
  локальную валидацию.

## Быстрый старт

```bash
find runs/2026 -maxdepth 1 -type d -name 'RUN-*' | sort
sed -n '1,80p' runs/REGISTRY.md
sed -n '1,120p' runs/stats/by-type.md
python3 scripts/validate_issue_123_runs_contract.py
python3 scripts/validate_issue_133_runs_restructure.py
python3 scripts/validate_issue_217_runs_log_contract.py
```

## Навигация

- [`CONTRACT.md`](CONTRACT.md) — контракт записи и обязательные поля
  `metadata.yaml`.
- [`REGISTRY.md`](REGISTRY.md) — полный реестр run'ов с типами и основными
  результатами.
- [`stats/by-type.md`](stats/by-type.md) — группировка по 5 типам run'ов.
- [`stats/by-date.md`](stats/by-date.md) — хронология и месячные тренды.
- [`stats/by-process.md`](stats/by-process.md) — статистика по процессам.
