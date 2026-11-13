#!/usr/bin/env python3
r"""Независимая сверка эталона `source_transcription.json` с XLSX (issue #484).

Эталон строит `make_transcription.py` через openpyxl; здесь XLSX разбирается другой
реализацией — stdlib `zipfile` + `xml.etree` по OOXML (sharedStrings.xml + sheetN.xml),
без openpyxl. Сверяются: состав и порядок листов, скрытость, диапазон, объединённые
диапазоны, значение каждой ячейки, суммарное число символов и SHA-256 файла.

    python3 experiments/issue_484/check_source.py /path/to/SoC_внешний\ 29-10.xlsx

Код возврата 1, если есть расхождения.
"""
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

HERE = Path(__file__).resolve().parent
DEFAULT_SRC = Path("/tmp/dl484/soc.xlsx")
NS = {
    "m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}
CELL = re.compile(r"([A-Z]+)(\d+)")


def col_index(letters):
    n = 0
    for ch in letters:
        n = n * 26 + ord(ch) - 64
    return n


def shared_strings(z):
    if "xl/sharedStrings.xml" not in z.namelist():
        return []
    root = ET.fromstring(z.read("xl/sharedStrings.xml"))
    out = []
    for si in root.findall("m:si", NS):
        # текст = конкатенация t верхнего уровня и t внутри форматных прогонов r
        parts = []
        for node in si:
            tag = node.tag.split("}")[1]
            if tag == "t":
                parts.append(node.text or "")
            elif tag == "r":
                for sub in node:
                    if sub.tag.split("}")[1] == "t":
                        parts.append(sub.text or "")
        out.append("".join(parts))
    return out


def number(value):
    """Числовая ячейка -> строка как в эталоне (целые без .0)."""
    f = float(value)
    return str(int(f)) if f.is_integer() else str(f)


def read_sheets(path):
    with zipfile.ZipFile(path) as z:
        strings = shared_strings(z)
        wb = ET.fromstring(z.read("xl/workbook.xml"))
        rels = {rel.get("Id"): rel.get("Target")
                for rel in ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))}
        sheets = []
        for sh in wb.find("m:sheets", NS):
            target = rels[sh.get(f'{{{NS["r"]}}}id')].lstrip("/")
            name = target if target.startswith("xl/") else f"xl/{target}"
            root = ET.fromstring(z.read(name))
            dim = root.find("m:dimension", NS)
            cells, max_row, max_col = {}, 0, 0
            for row in root.iter(f'{{{NS["m"]}}}row'):
                for c in row:
                    if c.tag != f'{{{NS["m"]}}}c':
                        continue
                    letters, digits = CELL.match(c.get("r")).groups()
                    ri, ci = int(digits), col_index(letters)
                    t = c.get("t")
                    v = c.find("m:v", NS)
                    isnode = c.find("m:is", NS)
                    if t == "s" and v is not None:
                        text = strings[int(v.text)]
                    elif t == "inlineStr" and isnode is not None:
                        text = "".join(n.text or "" for n in isnode.iter()
                                       if n.tag == f'{{{NS["m"]}}}t')
                    elif t == "str" and v is not None:
                        text = v.text or ""
                    elif v is not None and v.text is not None:
                        text = number(v.text) if t in (None, "n") else v.text
                    else:
                        continue
                    if text == "":
                        continue
                    cells[(ri, ci)] = text
                    max_row, max_col = max(max_row, ri), max(max_col, ci)
            merged = sorted(m.get("ref") for m in root.iter(f'{{{NS["m"]}}}mergeCell'))
            sheets.append({
                "title": sh.get("name"),
                "state": sh.get("state") or "visible",
                "dims": dim.get("ref") if dim is not None else None,
                "cells": cells,
                "max_row": max_row,
                "max_column": max_col,
                "merged": merged,
            })
        return sheets


def main(src):
    ref = json.loads((HERE / "source_transcription.json").read_text(encoding="utf-8"))
    sheets = read_sheets(src)
    bad = []
    digest = hashlib.sha256(Path(src).read_bytes()).hexdigest()
    if digest != ref["source"]["sha256"]:
        bad.append(f"sha256 {digest} != {ref['source']['sha256']}")
    if [s["title"] for s in sheets] != ref["source"]["sheetnames"]:
        bad.append("sheetnames differ")
    chars_ref = chars_xml = cells_checked = 0
    for a, b in zip(ref["sheets"], sheets):
        if a["title"] != b["title"]:
            bad.append(f"title {a['title']} != {b['title']}")
        if a["state"] != b["state"]:
            bad.append(f"{a['title']}: state {a['state']} != {b['state']}")
        if a["dims"] != b["dims"]:
            bad.append(f"{a['title']}: dims {a['dims']} != {b['dims']}")
        if a["merged"] != b["merged"]:
            bad.append(f"{a['title']}: merged {a['merged']} != {b['merged']}")
        # openpyxl считает по оформленным ячейкам, XML-разбор — по непустым значениям:
        # сверяется экстент содержимого (последняя строка/колонка с непустым значением).
        content_rows = [row[0] for row in a["rows"] if any(v for v in row[1:])]
        content_cols = [ci for row in a["rows"] for ci, v in enumerate(row[1:], 1) if v]
        if (max(content_rows, default=0), max(content_cols, default=0)) != (b["max_row"], b["max_column"]):
            bad.append(f"{a['title']}: content extent {max(content_rows, default=0)}x"
                       f"{max(content_cols, default=0)} != {b['max_row']}x{b['max_column']}")
        for row in a["rows"]:
            ri, values = row[0], row[1:]
            for ci, value in enumerate(values, start=1):
                got = b["cells"].get((ri, ci), "")
                chars_ref += len(value)
                chars_xml += len(got)
                cells_checked += 1
                if value != got:
                    bad.append(f"{a['title']}!{ri}:{ci}: {value!r} != {got!r}")
        extra = set(b["cells"]) - {(row[0], ci) for row in a["rows"]
                                  for ci in range(1, len(row))}
        if extra:
            bad.append(f"{a['title']}: cells outside transcription {sorted(extra)}")
    print(f"sheets: {len(sheets)}; cells compared: {cells_checked}; "
          f"chars transcription={chars_ref} xml={chars_xml}; mismatches: {len(bad)}")
    for line in bad[:20]:
        print(" !", line)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_SRC))
