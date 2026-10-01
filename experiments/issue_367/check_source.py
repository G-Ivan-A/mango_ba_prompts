#!/usr/bin/env python3
"""Независимая сверка колонок 1-2: абзацы читаются из word/document.xml (zipfile+regex,
без python-docx) и сравниваются побайтно с `№ + " " + Требование` транскрипции."""
import html, json, re, sys, zipfile
from pathlib import Path
src = sys.argv[1] if len(sys.argv) > 1 else "/tmp/i367/tz.docx"
xml = zipfile.ZipFile(src).read("word/document.xml").decode("utf-8")
paras = ["".join(html.unescape(t) for t in re.findall(r"<w:t(?: [^>]*)?>([^<]*)</w:t>", p))
         for p in re.findall(r"<w:p[ >].*?</w:p>", xml, re.S)]
assert "numPr" not in xml, "автонумерация Word: номера не литеральны"
bad = 0
for rid, num, req, idx in json.loads(Path(__file__).with_name("source_transcription.json").read_text())["rows"]:
    if (f"{num} {req}" if num else req) != paras[idx].strip():
        bad += 1; print("MISMATCH", rid, idx, repr(paras[idx][:80]))
print("OK" if not bad else f"{bad} mismatches", len(paras), "paragraphs")
sys.exit(1 if bad else 0)
