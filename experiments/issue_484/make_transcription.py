#!/usr/bin/env python3
"""Эталонная транскрипция исходника BCREQ-1199 v2 («SoC_внешний 29-10.xlsx», issue #484).

Колонки 1-2 отчёта RUN-0094 должны быть байт-в-байт равны исходнику, поэтому значения
ячеек фиксируются до генерации отчёта и независимо сверяются `check_source.py`
(stdlib: zipfile + xml.etree, без openpyxl).

    python3 experiments/issue_484/make_transcription.py /path/to/SoC_внешний\ 29-10.xlsx

Результат — `source_transcription.json`:
  sheets: [{title, dims, max_row, max_column, merged, header, rows: [[row_no, num, text, extra...]]}]
где `num` — значение колонки «№ пункта» (лист «Требования к системе») или «№» (лист «SLA»)
как в исходнике, `text` — значение колонки требования без правок.
"""
import hashlib
import json
import sys
from pathlib import Path

import openpyxl

HERE = Path(__file__).resolve().parent
DEFAULT_SRC = Path("/tmp/dl484/soc.xlsx")


def cell(value):
    """Значение ячейки как строка исходника (числа без .0), None -> ''."""
    if value is None:
        return ""
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


def main(src):
    data = src.read_bytes()
    wb = openpyxl.load_workbook(src, data_only=True)
    sheets = []
    for ws in wb.worksheets:
        rows = []
        for r in ws.iter_rows(min_row=1, max_row=ws.max_row, max_col=ws.max_column):
            values = [cell(c.value) for c in r]
            rows.append([r[0].row] + values)
        sheets.append({
            "title": ws.title,
            "dims": ws.dimensions,
            "max_row": ws.max_row,
            "max_column": ws.max_column,
            "state": ws.sheet_state,
            "merged": sorted(str(m) for m in ws.merged_cells.ranges),
            "rows": rows,
        })
    out = {
        "source": {
            "name": "SoC_внешний 29-10.xlsx",
            "sha256": hashlib.sha256(data).hexdigest(),
            "size": len(data),
            "sheetnames": wb.sheetnames,
        },
        "sheets": sheets,
    }
    (HERE / "source_transcription.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("sha256:", out["source"]["sha256"], "size:", out["source"]["size"])
    for s in sheets:
        nonempty = sum(1 for row in s["rows"] if any(v for v in row[1:]))
        print(f'{s["title"]!r}: dims {s["dims"]} rows {len(s["rows"])} non-empty {nonempty} '
              f'cols {s["max_column"]} merged {len(s["merged"])} state {s["state"]}')


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_SRC)
