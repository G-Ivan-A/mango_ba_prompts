#!/usr/bin/env python3
"""Keyword search over kb/processed sections; prints doc, §, pages, title, score."""
from __future__ import annotations
import json, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
IDX = json.load(open(Path(__file__).with_name("kb_index.json")))

def main(argv):
    terms = [t.lower() for t in argv if not t.startswith("--")]
    doc = next((a.split("=",1)[1] for a in argv if a.startswith("--doc=")), None)
    limit = int(next((a.split("=",1)[1] for a in argv if a.startswith("--limit=")), 12))
    snip = "--snip" in argv
    hits = []
    for item in IDX:
        if doc and item["doc"] != doc:
            continue
        text = (ROOT / item["path"]).read_text(encoding="utf-8").lower()
        score = sum(text.count(t) for t in terms)
        if all(t in text for t in terms) and score:
            hits.append((score, item, text))
    hits.sort(key=lambda h: -h[0])
    for score, item, text in hits[:limit]:
        print(f"{score:4d}  {item['doc']:22s} §{item['section']:<12s} c.{item['pages']:<10s} {item['title'][:70]}  | {item['path']}")
        if snip:
            i = text.find(terms[0])
            print("      ..." + text[max(0,i-200):i+300].replace("\n"," ") + "...")
    print(f"-- {len(hits)} sections match all terms")

main(sys.argv[1:])
