---
status: draft
version: 0.1
updated: 2026-11-05
temperature: 0.1
---

# Результат RUN-0088

Вывод — в [`report.md`](report.md). Пересчитать вердикты из JSON судей: `python3 experiments/issue_454/run0088_summary.py`.

| Файл | Что внутри |
| --- | --- |
| [`report.md`](report.md) | Итог, вердикты по стадиям, находки, ограничения |
| [`summary.json`](summary.json) | Вердикты стадий, сквозные проверки, пакеты, сводка пар |
| [`mechanical-checks.json`](mechanical-checks.json) | Блоки, слова, бюджеты, длинные предложения. Покрытие ФТ механика не проверила: см. [журнал](../logs/experiment-log.md) |
| [`ba-missing.json`](ba-missing.json) | Что БА нужно от комплекта и чего не было, по стадиям |
| [`judge-chain/`](judge-chain/) | Судьи стадий: `a-in.json`, `a-core.json`, итог `final.json`, выпуск `release.json` |
| [`judge-pairs/`](judge-pairs/), [`judge-pairs-key.json`](judge-pairs-key.json) | Слепые судьи пар A и T на Ш-3, Ш-4, Ш-5 и их повторах, ключ X/Y |
| `steps/<шаг>/` | `transcript.md` — диалог шага, `blocks.md` — блоки документа и журнал исполнителя. `T-Ш-*` — плечо T, `*в` — проход после возврата |
| `steps/Ш-В-правки/` | Что БА-редактор сделал с 34 замечаниями Ш-В: `edit-log.md` |
| `document/after-<шаг>.md` | Документ после каждого шага. Итог перед выпуском — `after-Ш-В-правки.md`, после выпуска — `after-Ш-Р.md` |
| `document/current.json` | Текущий документ по блокам |
| `document/sc-input.md` | Вход Ш-С: блок состояния и разделы 1, 2, ＋2.5, 3 |
