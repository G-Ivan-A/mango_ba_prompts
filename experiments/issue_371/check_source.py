#!/usr/bin/env python3
"""Независимая сверка колонок 1–2 транскрипции с исходником ТЗ 2026 (issue #371).

Текстовый слой PDF читается второй библиотекой — pypdf (транскрипция строилась pymupdf).
Сверка без учёта пробельных символов: из текста PDF и из ожидаемой последовательности
удаляются все пробелы и переводы строк, глифы SymbolMT U+F02D / U+F0B7 заменяются на «−» / «•».
Ожидаемая последовательность — строки транскрипции (`№` + `Требование`) и исключённые строки
(титул, «Термины и определения») в порядке документа. Документ должен покрываться ими
полностью и без остатка: любая пропущенная, лишняя, переставленная или изменённая буква —
ошибка. Дополнительно проверяется, что внутри строк колонки 2 нет двойных пробелов,
табуляций и PUA-глифов, а SHA-256 файла совпадает с записанным в транскрипции.

    python3 -I experiments/issue_371/check_source.py /path/to/tz2026.pdf
"""
import hashlib
import json
import re
import sys
from pathlib import Path

import pypdf

MARKERS = {"": "−", "": "•"}
data = json.loads(Path(__file__).with_name("source_transcription.json").read_text(encoding="utf-8"))
pdf = Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/dl371/tz2026/tz2026.pdf")
bad = 0
if hashlib.sha256(pdf.read_bytes()).hexdigest() != data["sha256"]:
    bad += 1
    print("SHA256 MISMATCH")

squash = lambda s: re.sub(r"\s+", "", s)  # noqa: E731
text = "".join(page.extract_text() for page in pypdf.PdfReader(pdf).pages)
for glyph, char in MARKERS.items():
    text = text.replace(glyph, char)
full = squash(text)

rows = [(rid, squash(num + req)) for rid, num, req, _ in data["rows"]]
excluded = [squash(line) for line in data["excluded"]]
pos = 0
while rows or excluded:
    if rows and full.startswith(rows[0][1], pos):
        pos += len(rows.pop(0)[1])
    elif excluded and full.startswith(excluded[0], pos):
        pos += len(excluded.pop(0))
    else:
        bad += 1
        print("MISMATCH at", pos, "next row", rows[0][0] if rows else None, "pdf:", repr(full[pos:pos + 80]))
        break
if pos != len(full):
    bad += 1
    print("непокрытый хвост:", repr(full[pos:pos + 80]))

for rid, num, req, _ in data["rows"]:
    if re.search(r"\s{2}|\t|[-]", req) or req != req.strip():
        bad += 1
        print("пробелы/PUA в строке", rid)

print("OK" if not bad else f"{bad} mismatches", f"{len(data['rows'])} rows, {len(data['excluded'])} excluded lines,",
      f"{len(full)} non-space chars covered")
sys.exit(1 if bad else 0)
