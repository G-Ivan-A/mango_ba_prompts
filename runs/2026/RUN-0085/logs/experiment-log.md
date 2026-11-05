---
status: draft
version: 0.1
updated: 2026-11-05
temperature: 0.1
---

# Журнал RUN-0085

## Цель

Ш-В: уточнение правила против избыточной декомпозиции (A3) против контроля A2 (v0.2). Бюджет подтверждён владельцем в issue [#450](https://github.com/G-Ivan-A/mango_ba_prompts/issues/450).

## Процедура

1. Коммит пред-регистрации `b94d5cc0` — до запуска подагентов.
2. `experiments/issue_450/run0085/run.py prepare`, запуск изолированных подагентов opus (исполнители, затем слепые судьи).
3. `run.py judge`, `run.py score`; итог в `outputs/summary.json`.
4. `experiments/issue_450/fixate.py` и `write_records.py` — фиксация.

## Отклонения

- Инструкции подавались подагентам файлом `/tmp/ins/*.txt` — один дополнительный вызов Read у каждого; на сравнение не влияет: одинаково в обоих плечах.
