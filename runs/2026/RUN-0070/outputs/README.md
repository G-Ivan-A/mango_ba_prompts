---
status: draft
updated: 2026-10-01
ai-generated: true
type: evidence
---

# Выходы RUN-0070

| Файл | Назначение |
| --- | --- |
| [`L0-feasibility-assessment-1115.md`](L0-feasibility-assessment-1115.md) | L0-оценка исполнимости 172 строк ТЗ BCREQ-1115 (6 колонок) |

Итог: `Да` — 128, `Частично` — 8 (интеграция с CRM НОТА «Юнион», пакеты минут,
эмоции-моменты, время сообщений чат-бота), `Нет` — 1 («Нет данных»: пакет
25 000 минут), пусто (заголовки групп и обязательство Заказчика — вне
функционального контура) — 35.

Пересборка:

```bash
MANGO_BA_RUNTIME_MAIN=/path/to/mango-ba-ai-runtime python3 experiments/issue_367/generate_run.py
python3 experiments/issue_367/check_source.py /path/to/BCREQ-1115.docx
MANGO_BA_RUNTIME_MAIN=/path/to/mango-ba-ai-runtime python3 experiments/issue_367/verify_quotes.py
MANGO_BA_RUNTIME_MAIN=/path/to/mango-ba-ai-runtime python3 scripts/validate_issue_367_run.py
```
