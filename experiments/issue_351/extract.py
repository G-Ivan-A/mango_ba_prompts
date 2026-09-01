#!/usr/bin/env python3
"""Extract source rows from the task 1099 XLSX (issue #351 attachment), stdlib only."""
from __future__ import annotations
import hashlib, json, re, sys, zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
SOURCE = Path(__file__).with_name("requirements.xlsx")

def shared_strings(book):
    root = ET.fromstring(book.read("xl/sharedStrings.xml"))
    out = []
    for si in root.findall(NS + "si"):
        parts = []
        for node in si.iter():
            if node.tag == NS + "t":
                parts.append(node.text or "")
            elif node.tag == NS + "br":
                parts.append("\n")
        out.append("".join(parts))
    return out

def sheet_rows(book, name, strings):
    sheet = ET.fromstring(book.read(name))
    rows = []
    for row in sheet.findall(f".//{NS}sheetData/{NS}row"):
        cells = {}
        for cell in row.findall(NS + "c"):
            col = re.match(r"[A-Z]+", cell.attrib["r"]).group()
            if cell.attrib.get("t") == "inlineStr":
                node = cell.find(NS + "is")
                value = "".join(t.text or "" for t in node.iter(NS + "t")) if node is not None else ""
            else:
                node = cell.find(NS + "v")
                value = "" if node is None else (node.text or "")
                if cell.attrib.get("t") == "s" and value:
                    value = strings[int(value)]
            cells[col] = value
        rows.append((int(row.attrib["r"]), cells))
    return rows

def main():
    data = SOURCE.read_bytes()
    print("sha256", hashlib.sha256(data).hexdigest(), "size", len(data), file=sys.stderr)
    with zipfile.ZipFile(SOURCE) as book:
        wb = ET.fromstring(book.read("xl/workbook.xml"))
        for s in wb.iter(NS + "sheet"):
            print("sheet", s.attrib, file=sys.stderr)
        strings = shared_strings(book)
        for name in ("xl/worksheets/sheet1.xml", "xl/worksheets/sheet2.xml"):
            rows = sheet_rows(book, name, strings)
            print(f"=== {name}: {len(rows)} rows", file=sys.stderr)
            if name.endswith("sheet1.xml"):
                json.dump([{"r": r, "cells": c} for r, c in rows], sys.stdout, ensure_ascii=False, indent=1)
            else:
                for r, c in rows[:60]:
                    print(r, c, file=sys.stderr)

main()
