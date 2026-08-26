#!/usr/bin/env python3
"""Перестраивает L0 под требование #325: ровно шесть колонок.

Колонки 1–3 (`№`, `Требование`, `Комментарий участника`) переносятся **байт-в-байт**:
скрипт читает уже существующий L0 и переписывает эти ячейки без единого изменения —
изменять вердикт участника категорически запрещено. Единственная колонка анализа
RUN-0057 заменяется тремя колонками по источникам:

    4. Оценка по док. Mango «Роботы»            — kb/processed/cov-robot-fil
    5. Оценка по док. Mango «Речевая аналитика» — kb/processed/speech-analytics
    6. Оценка по публичной док. TWIN            — https://wiki.twin24.ai/ru/

Содержимое новых колонок ведётся вручную в `issue_325_doc_columns_data.py` и
сопоставляется по паре «номер приложения + номер строки формы». Строка без
записи печатается в stderr и попадает в вывод с маркером — молчаливых пропусков нет.

Запуск:

    python3 experiments/issue_325_add_doc_columns.py \
        --in runs/2026/RUN-0057/outputs/L0-customer-form-with-assessment.md \
        --out runs/2026/RUN-0057/outputs/L0-customer-form-with-assessment.md
"""

import argparse
import importlib.util
import pathlib
import re
import sys

GAP = "> ⚠️ **НЕДОСТАТОЧНО ДАННЫХ / ТРЕБУЕТСЯ УТОЧНЕНИЕ**"

NEW_HEADERS = [
    "Оценка по док. Mango «Роботы»",
    "Оценка по док. Mango «Речевая аналитика»",
    "Оценка по публичной док. TWIN",
]


def load_data():
    path = pathlib.Path(__file__).with_name("issue_325_doc_columns_data.py")
    spec = importlib.util.spec_from_file_location("issue_325_data", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def split_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def is_group_header(requirement: str, comment: str) -> bool:
    return requirement.rstrip().endswith(":") and not comment.strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--in", dest="source", required=True)
    parser.add_argument("--out", dest="target", required=True)
    args = parser.parse_args()

    data = load_data()
    lines = pathlib.Path(args.source).read_text(encoding="utf-8").splitlines()

    out: list[str] = []
    appendix = 0
    unmatched = 0
    rows = 0
    for line in lines:
        if re.match(r"^## Лист «", line):
            appendix += 1
            out.append(line)
            continue
        if not (appendix and line.startswith("|")):
            out.append(line)
            continue

        cells = split_row(line)
        if line.startswith("| ---"):
            out.append("| " + " | ".join(["---"] * 6) + " |")
            continue
        if cells[0] == "№":
            # заголовки колонок 1–3 — дословно из исходной формы
            out.append("| " + " | ".join(cells[:3] + NEW_HEADERS) + " |")
            continue

        num, requirement, comment = cells[0], cells[1], cells[2]
        rows += 1
        if is_group_header(requirement, comment):
            extra = [data.GROUP_HEADER] * 3
        else:
            entry = data.DATA.get((appendix, num))
            if entry is None:
                unmatched += 1
                print(
                    f"НЕ СОПОСТАВЛЕНО: приложение {appendix}, № {num}: {requirement[:60]!r}",
                    file=sys.stderr,
                )
                extra = [f"{GAP}: строка не имеет оценки по данному источнику"] * 3
            else:
                extra = list(entry)
        # колонки 1–3 переписываются ровно теми же строками, что прочитаны
        out.append("| " + " | ".join([num, requirement, comment] + extra) + " |")

    pathlib.Path(args.target).write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"строк формы: {rows}, несопоставленных: {unmatched}", file=sys.stderr)
    return 1 if unmatched else 0


if __name__ == "__main__":
    raise SystemExit(main())
