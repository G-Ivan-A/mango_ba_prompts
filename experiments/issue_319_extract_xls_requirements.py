#!/usr/bin/env python3
"""Извлекает таблицы требований из приложений ТЗ в формате Excel BIFF (.xls).

Постановка issue #319: четыре приложения к ТЗ конкурсной документации № 004-К26
(STT, TTS, NLU, Dialogue Manager) приложены к задаче в виде .xls (OLE2/BIFF).
Скрипт печатает содержимое всех листов построчно, без переформулирования, —
именно в таком виде текст требований переносится в матрицу исполнимости
runs/2026/RUN-0057/outputs/L2-feasibility-matrix.md.

Запуск (вручную, локально; в CI не вызывается):

    pip install xlrd
    python3 experiments/issue_319_extract_xls_requirements.py 1._STT.xls ...

Зависимость: xlrd (BIFF .xls не читается openpyxl). Используется в
runs/2026/RUN-0057/inputs/README.md.
"""

import hashlib
import sys

import xlrd


def dump(path: str) -> None:
    data = open(path, "rb").read()
    print(f"##### {path}")
    print(f"# size={len(data)} md5={hashlib.md5(data).hexdigest()}")
    print(f"# sha256={hashlib.sha256(data).hexdigest()}")
    book = xlrd.open_workbook(path)
    for sheet in book.sheets():
        print(f"### sheet={sheet.name!r} rows={sheet.nrows} cols={sheet.ncols}")
        for row in range(sheet.nrows):
            cells = [str(sheet.cell_value(row, col)).strip() for col in range(sheet.ncols)]
            print(row, "|", "|".join(cells))


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 1
    for path in argv[1:]:
        dump(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
