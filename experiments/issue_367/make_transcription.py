#!/usr/bin/env python3
"""Транскрипция колонок 1-2 ТЗ BCREQ-1115 (issue #367) -> source_transcription.json.

DOCX состоит из абзацев без автонумерации (numPr отсутствует): номера «1.»,
«14.» и маркеры «•» — литеральный текст. Колонка 1 = ведущий номер/маркер,
колонка 2 = остаток абзаца; `№ + " " + Требование == абзац.strip()`.
Пустые абзацы пропущены, раздел «Термины и определения» (абзацы 13-36) —
определения, не требования. Пропуск «13.» в исходнике сохранён.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

import docx

src = Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/i367/tz.docx")
paras = [p.text for p in docx.Document(str(src)).paragraphs]
assert paras[13].startswith("Термины и определения") and paras[37].startswith("Список необходимых услуг")
rows = []
for idx in [*range(2, 13), *range(37, len(paras))]:
    text = paras[idx].strip()
    if not text:
        continue
    m = re.match(r"(\d+\.|•) (.*)\Z", text, re.S)
    num, req = (m.group(1), m.group(2)) if m else ("", text)
    rows.append([f"R{len(rows) + 1:03d}", num, req, idx])
raw = src.read_bytes()
data = {
    "title": "Техническое задание -очиен в анализ.docx (BCREQ-1115)",
    "sha256": hashlib.sha256(raw).hexdigest(),
    "bytes": len(raw),
    "rows": rows,
}
Path(__file__).with_name("source_transcription.json").write_text(
    json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(len(rows), "rows")
