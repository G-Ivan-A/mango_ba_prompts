#!/usr/bin/env python3
"""Поиск по разделам БЗ с выводом стабильного адреса цитирования (issue #339)."""
import re, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2] / "kb/processed"
DOCS = sys.argv[1].split(",")
PATS = [re.compile(p, re.I) for p in sys.argv[2].split("|||")]
CTX = int(sys.argv[3]) if len(sys.argv) > 3 else 220
def fm(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    d = {}
    if m:
        for line in m.group(1).splitlines():
            k, _, v = line.partition(":")
            d[k.strip()] = v.strip().strip('"')
    return d
for doc in DOCS:
    for f in sorted((ROOT / doc / "sections").glob("*.md")):
        t = f.read_text(encoding="utf-8")
        for p in PATS:
            for m in p.finditer(t):
                meta = fm(t)
                s = max(0, m.start() - CTX); e = min(len(t), m.end() + CTX)
                print(f"### {doc}/{f.name} | §{meta.get('section','—')} | с.{meta.get('pages','—')} | {meta.get('title','')}")
                print("   ..." + re.sub(r"\s+", " ", t[s:e]) + "...")
                break
