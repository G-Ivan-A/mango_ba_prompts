#!/usr/bin/env python3
"""Независимая сверка колонок 1-2 транскрипции с исходниками BCREQ-1116 (issue #369).

DOC: текст читается из потока WordDocument таблицей фрагментов (`doc_text.py`, olefile,
без LibreOffice и python-docx) и режется на сегменты по концам абзацев (\\r) и
ячеек/строк таблиц (\\x07). Каждая строка транскрипции обязана совпасть побайтно с
очередным сегментом (абзац: `№ + " " + Требование`, кроме маркеров «•» списков Word,
которые в потоке текста не хранятся; строка таблицы: каждая ячейка `<br>` — отдельный
сегмент, `<sup>1</sup>` — знак сноски \\x02) в том же порядке. Непокрытые
непустые сегменты после глоссария допустимы только в удалённом исправлениями
разделе «1. Существующая проблема…» — они печатаются для контроля.

XLSX: значения столбца A листа «функционал» читаются из `xl/sharedStrings.xml` и
`xl/worksheets/sheet1.xml` (zipfile + regex, без openpyxl) и сравниваются побайтно с
колонкой 2; колонка 1 — номер строки листа.

    python3 experiments/issue_369/check_source.py <ТЕХНИЧЕСКОЕ ЗАДАНИЕ.doc> <Требования к ПО КЦ (4).xlsx>
"""
import hashlib
import html
import json
import re
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from doc_text import doc_text  # noqa: E402

DELETED = "1. Существующая проблема и обоснование необходимости закупки"
data = json.loads(Path(__file__).with_name("source_transcription.json").read_text(encoding="utf-8"))
doc_block, xlsx_block = data["blocks"]
bad = 0

# --- DOC -----------------------------------------------------------------------
doc_path, xlsx_path = sys.argv[1], sys.argv[2]
for block, path in ((doc_block, doc_path), (xlsx_block, xlsx_path)):
    if hashlib.sha256(Path(path).read_bytes()).hexdigest() != block["sha256"]:
        bad += 1
        print("SHA256 MISMATCH", block["title"])
segments = re.split(r"[\r\x07]", doc_text(doc_path))
pos = next(i for i, s in enumerate(segments) if s == "RPO (Recovery Point Objective)") + 2  # конец глоссария
skipped = []
for rid, num, req, _loc in doc_block["rows"]:
    if _loc.startswith("t"):
        want = [c.replace("<sup>1</sup>", "\x02") for c in req.split("<br>")]
    else:
        want = [req if num in ("", "•") else f"{num} {req}"]
    for cell in want:
        while pos < len(segments) and segments[pos] != cell:
            if segments[pos].strip():
                skipped.append(segments[pos])
            pos += 1
        if pos == len(segments):
            bad += 1
            print("NOT FOUND", rid, repr(cell[:80]))
            break
        pos += 1
for s in skipped:
    print("skipped segment:", repr(s[:90]))
deleted_ok = skipped and skipped[0] == DELETED and len(skipped) == 6
if skipped and not deleted_ok:
    bad += 1
    print("непокрытые сегменты вне удалённого раздела")
tail = [s for s in segments[pos:] if s.strip()]
if tail:
    bad += 1
    print("непокрытый хвост:", tail[:3])

# --- XLSX ----------------------------------------------------------------------
z = zipfile.ZipFile(xlsx_path)
unesc = lambda s: html.unescape(s)  # noqa: E731
strings = ["".join(unesc(t) for t in re.findall(r"<t(?: [^>]*)?>([^<]*)</t>", si, re.S))
           for si in re.findall(r"<si>(.*?)</si>", z.read("xl/sharedStrings.xml").decode("utf-8"), re.S)]
sheet = z.read("xl/worksheets/sheet1.xml").decode("utf-8")
col_a = {}
for ref, attrs, body in re.findall(r'<c r="A(\d+)"([^>]*?)(?:/>|>(.*?)</c>)', sheet, re.S):
    value = re.search(r"<v>([^<]*)</v>", body or "")
    if value and 't="s"' in attrs:
        col_a[ref] = strings[int(value.group(1))]
expected = [(r, v) for r, v in sorted(col_a.items(), key=lambda kv: int(kv[0])) if v.strip() and r != "1"]
got = [(num, req) for _rid, num, req, _loc in xlsx_block["rows"]]
if got != expected:
    bad += 1
    print("XLSX MISMATCH", set(got) ^ set(expected))

print("OK" if not bad else f"{bad} mismatches", f"DOC {len(doc_block['rows'])} rows / {len(segments)} segments,",
      f"XLSX {len(xlsx_block['rows'])} rows")
sys.exit(1 if bad else 0)
