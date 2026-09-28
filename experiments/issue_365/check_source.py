#!/usr/bin/env python3
"""Сверка: нормализованный текст каждой строки транскрипции входит в текст PDF."""
import json, re, sys
from pathlib import Path
import pymupdf as fitz
pdf = sys.argv[1] if len(sys.argv) > 1 else "/tmp/att365/tz.pdf"
norm = lambda s: re.sub(r"\s+", "", s.replace("<br>", " ").replace("▪", "").replace("|", ""))
text = norm("".join(p.get_text() for p in fitz.open(pdf)).replace("\uf0a7", ""))
text = re.sub(r"Добавленопримечание\(\[ВР\d+\]\):", "", text)
bad = 0
for rid, num, req in json.loads(Path(__file__).with_name("source_transcription.json").read_text())["rows"]:
    if norm(req) not in text:
        bad += 1; print("MISS", rid, num, req[:80])
print("OK" if not bad else f"{bad} missing")
