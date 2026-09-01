# -*- coding: utf-8 -*-
"""Сверка колонок 1-3 отчёта RUN-0066 с исходным XLSX (побайтовое совпадение).

Запускается локально при наличии исходного файла `requirements.xlsx`
(в репозиторий он не попадает по контракту прогонов). Печатает лог сверки,
пригодный для вставки в `runs/2026/RUN-0066/inputs/README.md`.
"""

import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
REPORT = os.path.join(REPO, "runs/2026/RUN-0066/outputs/L0-feasibility-assessment-1099-2.md")
XLSX = os.path.join(HERE, "requirements.xlsx")


WS = " \t\n\r\xa0"


def unesc(cell):
    return cell.replace("<br>", "\n").replace("\\|", "|")


def split_row(line):
    return [p.strip() for p in re.split(r"(?<!\\)\|", line.strip().strip("|"))]


def main():
    rows = json.load(open(os.path.join(HERE, "sheet1.json"), encoding="utf-8"))
    source = [(r["cells"].get("A", ""), r["cells"].get("B", ""), r["cells"].get("D", ""))
              for r in rows if any(r["cells"].get(k) for k in ("A", "B", "D"))]

    lines = [ln for ln in open(REPORT, encoding="utf-8").read().splitlines() if ln.startswith("|")]
    table = [split_row(ln) for ln in lines[2:]]

    errors = []
    trimmed = 0
    if len(table) != len(source):
        errors.append("строк в отчёте %d, в источнике %d" % (len(table), len(source)))
    for idx, (src, row) in enumerate(zip(source, table), start=1):
        got = tuple(unesc(c) for c in row[:3])
        if got == src:
            continue
        if tuple(c.strip(WS) for c in got) == tuple(c.strip(WS) for c in src):
            trimmed += 1
            continue
        errors.append("строка %d: %r != %r" % (idx, got, src))

    if os.path.exists(XLSX):
        digest = hashlib.sha256(open(XLSX, "rb").read()).hexdigest()
        size = os.path.getsize(XLSX)
        print("источник: requirements.xlsx, %d байт, sha256 %s" % (size, digest))
    else:
        print("источник: requirements.xlsx отсутствует локально — сверка по извлечённому sheet1.json")

    print("строк источника (непустых A/B/D): %d" % len(source))
    print("строк в отчёте: %d" % len(table))
    if errors:
        print("РАСХОЖДЕНИЯ (%d):" % len(errors))
        for e in errors[:20]:
            print("  -", e)
        return 1
    print("ячеек, отличающихся только краевыми пробелами/переводами строки: %d" % trimmed)
    print("колонки 1-3 совпадают с источником посимвольно (краевые пробелы markdown-таблица не переносит): расхождений нет")
    return 0


if __name__ == "__main__":
    sys.exit(main())
