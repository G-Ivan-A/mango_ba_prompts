---
status: draft
updated: 2026-10-11
ai-generated: true
type: evidence
---

# Выходы RUN-0071

| Файл | Назначение |
| --- | --- |
| [`L0-feasibility-assessment-1116.md`](L0-feasibility-assessment-1116.md) | L0-оценка исполнимости ТЗ BCREQ-1116 (6 колонок): блок 1 — «ТЕХНИЧЕСКОЕ ЗАДАНИЕ.doc» (125 строк), блок 2 — «Требования к ПО КЦ (4).xlsx» (74 строки) |

Итог по блокам:

- «ТЕХНИЧЕСКОЕ ЗАДАНИЕ.doc»: `Да` — 40, `Частично` — 16 (on-premise части
  требований к лицензиям и развёртыванию, интеграции 1С / stream telecom / Talkme,
  хранение отчётов 3 года в контуре Заказчика, схема резервирования, отдельные
  шаблоны и графический конструктор отчётов, приоритет вызовов в очереди, режим
  preview, звуковые алерты), `Нет` — 17 (бессрочные лицензии, готовые коннекторы к
  CRM/1С/СМС-шлюзам Заказчика, перенос истории за 12 месяцев, Mindbox, сайт,
  робот «Мия», планировщик рассылки отчётов, сроки реакции и устранения инцидентов
  поддержки — «Нет данных»), пусто — 52 (заголовки, шапки таблиц, цели проекта,
  проектные услуги и договорные условия — вне функционального контура);
- «Требования к ПО КЦ (4).xlsx»: `Да` — 59, `Частично` — 2 (отображение времени в
  регионе звонящего, web-ссылки в подсказках), `Нет` — 1 (Mindbox), пусто — 12
  (заголовки групп и вопрос о сроке внедрения).

Пересборка:

```bash
python3 experiments/issue_369/check_source.py /path/to/default.doc /path/to/4.xlsx
MANGO_BA_RUNTIME_MAIN=/path/to/mango-ba-ai-runtime python3 experiments/issue_369/generate_run.py
MANGO_BA_RUNTIME_MAIN=/path/to/mango-ba-ai-runtime python3 experiments/issue_369/verify_quotes.py
MANGO_BA_RUNTIME_MAIN=/path/to/mango-ba-ai-runtime python3 scripts/validate_issue_369_run.py
```
