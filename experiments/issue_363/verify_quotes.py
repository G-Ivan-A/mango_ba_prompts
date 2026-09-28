#!/usr/bin/env python3
"""Проверка: каждая цитата «…» в колонке 5 отчёта встречается дословно в разделе БЗ, указанном в колонке 4."""
import re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import generate_run as g
def norm(s): return re.sub(r"\s+", " ", s.replace(" ", " ")).strip()
bad = 0
for num, (_, why, quote, _) in g.A.items():
    files = re.findall(r"docs/kb/([^)]+\.md)\)", why)
    corpus = norm(" ".join((g.KB / f).read_text(encoding="utf-8") for f in files))
    for q in re.findall(r"«((?:[^«»]|«[^«»]*»)*)»", quote):
        for frag in q.split("…"):
            frag = norm(frag.strip(" .•"))
            if len(frag) > 8 and frag not in corpus and "mango-office.ru" not in quote:
                bad += 1; print(f"п.{num or '19-прод.'}: NOT FOUND: {frag[:90]}")
print("mismatches:", bad); sys.exit(1 if bad else 0)
