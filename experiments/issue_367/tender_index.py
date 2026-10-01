#!/usr/bin/env python3
"""Индекс пунктов «Шаблона ТЗ для тендеров v4»: п/п -> [страница PDF, полный текст] -> tender_index.json.

Пункт начинается с номера вида 2.16.1. в начале строки либо после значения «наличие»
(часть пунктов в извлечённом тексте склеена с предыдущим); пункт может переходить на
следующую страницу — тогда указывается страница начала.
"""
import json, re, sys
from pathlib import Path
import pymupdf
pdf = sys.argv[1] if len(sys.argv) > 1 else "/tmp/i367/tender.pdf"
chunks = []
for pno, page in enumerate(pymupdf.open(pdf), 1):
    text = re.sub(r"\s*\d*\s*№ п/п\s+Требование\s+Требуемое\s+значение\s*", "\n", page.get_text())
    chunks.append(f"\n@@PAGE{pno}@@\n{text}")
full = "".join(chunks)
idx, page = {}, 1
tokens = re.split(r"(@@PAGE\d+@@|(?:^|(?<=наличие))\s*\d+(?:\.\d+)+\.(?=\s))", full, flags=re.M)
cur = None
for tok in tokens:
    if not tok:
        continue
    m = re.fullmatch(r"@@PAGE(\d+)@@", tok)
    if m:
        page = int(m.group(1)); continue
    n = re.fullmatch(r"\s*(\d+(?:\.\d+)+)\.", tok)
    if n and re.fullmatch(r"\d+(\.\d+)+", n.group(1)):
        cur = n.group(1); idx.setdefault(cur, [page, ""]); continue
    if cur:
        idx[cur][1] += " " + tok
for k, v in idx.items():
    v[1] = re.sub(r"\s+", " ", v[1].replace("@@", "")).strip()
Path(__file__).with_name("tender_index.json").write_text(json.dumps(idx, ensure_ascii=False, indent=0) + "\n")
print(len(idx), "items")
