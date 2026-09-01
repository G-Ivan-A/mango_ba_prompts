# -*- coding: utf-8 -*-
"""Генератор отчёта RUN-0066: L0-оценка исполнимости ТЗ задачи 1099 (повторный прогон).

Колонки 1-3 переносятся из исходного XLSX без изменений (переводы строк -> `<br>`,
символ `|` экранируется). Колонки 4-6 берутся из авторской таблицы оценок
`assessments.py`. Атомарные ссылки собираются резолвером `cite.py`, который
читает §, заголовок и страницы из frontmatter разделов `kb/processed`, поэтому
номера страниц не могут разойтись с базой знаний.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from assessments import ASSESSMENTS
from cite import cites

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(REPO, "runs/2026/RUN-0066/outputs/L0-feasibility-assessment-1099-2.md")

STRUCTURAL = "Структурная строка исходного XLSX (заголовок раздела); оценка не выполняется."

HEADER = """---
status: draft
version: "1.0"
updated: 2026-09-01
ai-generated: true
type: analysis
scope: task-1099-only
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/351"
related_runs:
  - RUN-0065
---

# L0 — оценка исполнимости ТЗ «Телефония» (задача 1099, повторный прогон)

Повторный прогон того же ТЗ альтернативной моделью (Claude Opus) для A/B-сравнения
с RUN-0065. Колонки 1-3 воспроизводятся из исходного XLSX без изменений: нумерация,
формулировки и отметки участника сохранены как есть, переводы строк представлены
`<br>`. Колонка 4 использует только шкалу `Да / Частично / Нет / пусто`; `Частично`
применяется к требованиям, декомпозируемым на атомарные части, из которых
подтверждена не каждая. Колонка 5 содержит обоснование и атомарную ссылку
`[ИСТОЧНИК, §X, с.Y]`; номер страницы вычисляется из frontmatter соответствующего
раздела `kb/processed` в момент генерации, а не задаётся вручную. Колонка 6 —
независимый технический аудит.

Соответствие колонок исходному файлу: `№` = колонка A «№ требования»,
`Требование` = колонка B «Требования к системе», `Комментарий участника` =
колонка D «Факт реализации». Исходная колонка C «Является блок-фактором?»
сохранена как явная пометка `БЛОК-ФАКТОР` в колонке 6, чтобы соблюсти контракт
ровно шести колонок и не потерять данные источника.

| № | Требование | Комментарий участника | Оценка | Обоснование + атомарная ссылка | Технический критик-аудит |
| --- | --- | --- | --- | --- | --- |
"""


def esc(value):
    """Экранирование для ячейки markdown-таблицы без изменения содержимого."""
    return value.replace("|", "\\|").replace("\n", "<br>")


def main():
    rows = json.load(open(os.path.join(HERE, "sheet1.json"), encoding="utf-8"))
    lines = [HEADER]
    assessed = set()
    for row in rows:
        cells = row["cells"]
        num, req, block, fact = (cells.get(k, "") for k in ("A", "B", "C", "D"))
        if not (num or req or fact):
            continue
        if num in ASSESSMENTS:
            verdict, keys, comment, audit = ASSESSMENTS[num]
            assessed.add(num)
            link = cites(keys) if keys else ""
            reason = (comment + " " + link).strip() if link else comment
        else:
            verdict, reason, audit = "", "—", STRUCTURAL
        if block:
            audit = "%s БЛОК-ФАКТОР (исходная колонка C: «%s»): требуется решение владельца продукта до принятия обязательства." % (audit, block)
        lines.append("| %s | %s | %s | %s | %s | %s |\n" % (
            esc(num), esc(req), esc(fact), verdict, reason, audit))

    missing = set(ASSESSMENTS) - assessed
    assert not missing, "оценки без строки в источнике: %s" % sorted(missing)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.writelines(lines)
    print("написано:", OUT, "строк оценки:", len(assessed))


if __name__ == "__main__":
    main()
