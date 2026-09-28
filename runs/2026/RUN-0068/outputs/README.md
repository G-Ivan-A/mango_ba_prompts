---
status: draft
updated: 2026-09-28
ai-generated: true
type: evidence
---

# Выходы RUN-0068

| Файл | Назначение |
| --- | --- |
| [`L0-feasibility-assessment-1114.md`](L0-feasibility-assessment-1114.md) | L0-оценка исполнимости 22 строк ТЗ BCREQ-1114 (6 колонок) |

Итог: `Да` — 3, `Частично` — 7, `Нет` — 11 (из них «Нет данных» — большинство),
пусто (вне функционального контура) — 1 (п.17).

Пересборка:

```bash
MANGO_BA_RUNTIME_MAIN=/path/to/mango-ba-ai-runtime python3 experiments/issue_363/generate_run.py
python3 scripts/validate_issue_363_run.py
```
