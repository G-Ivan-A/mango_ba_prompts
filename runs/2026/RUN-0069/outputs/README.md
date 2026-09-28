---
status: draft
updated: 2026-09-28
ai-generated: true
type: evidence
---

# Выходы RUN-0069

| Файл | Назначение |
| --- | --- |
| [`L0-feasibility-assessment-1114-2.md`](L0-feasibility-assessment-1114-2.md) | L0-оценка исполнимости 59 строк ТЗ BCREQ-1114v2 (6 колонок) |

Итог: `Да` — 20, `Частично` — 15, `Нет` — 14 (в основном «Нет данных»: SLA, LLM, IVR,
цепочки звонков, дашборды), пусто (вне функционального контура / заголовки) — 10.

Пересборка:

```bash
MANGO_BA_RUNTIME_MAIN=/path/to/mango-ba-ai-runtime python3 experiments/issue_365/generate_run.py
python3 experiments/issue_365/verify_quotes.py
python3 scripts/validate_issue_365_run.py
```
