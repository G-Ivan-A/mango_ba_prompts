#!/usr/bin/env python3
"""Правило >90%: сходство каждой строки ТЗ с пунктами «Шаблона ТЗ для тендеров v4» (difflib)."""
import difflib, json, re, sys
from pathlib import Path
import pymupdf
pdf = sys.argv[1] if len(sys.argv) > 1 else "/tmp/att365/tender.pdf"
raw = "\n".join(p.get_text() for p in pymupdf.open(pdf))
# пункты шаблона: строка-номер вида 2.18.3 и следующий за ней текст до следующего номера
parts = re.split(r"\n\s*(\d+(?:\.\d+)+)\.?\s*\n", "\n" + raw)
items = [(parts[i], re.sub(r"\s+", " ", parts[i + 1]).strip()) for i in range(1, len(parts) - 1, 2)]
low = lambda s: re.sub(r"\s+", " ", s.replace("<br>", " ").replace("▪", "")).lower().strip()
rows = json.loads(Path(__file__).with_name("source_transcription.json").read_text())["rows"]
best = {}
for rid, num, req in rows:
    r, n, t = max((difflib.SequenceMatcher(None, low(req), low(t[:len(req) + 40])).ratio(), n, t) for n, t in items)
    best[rid] = (round(r, 3), n)
    print(f"{rid} {num:6} {r:.3f} п/п {n}: {t[:70]}")
print("items:", len(items), "rows >0.9:", [k for k, v in best.items() if v[0] > 0.9])
