#!/usr/bin/env python3
"""Read-only: найти ссылки на prompts/*.md в runs/ и docs и проверить, что цель существует."""
import re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
REL = re.compile(r"\]\(((?:\.\./)+prompts/[^)#?\s]+\.md)")
ABS = re.compile(r"https://github\.com/G-Ivan-A/mango_ba_prompts/blob/main/(prompts/[^)#?\s>`\"']+\.md)")
dirs = sys.argv[1:] or ["runs"]
broken = {}
total = 0
for d in dirs:
    for p in sorted((ROOT / d).rglob("*.md")):
        text = p.read_text(encoding="utf-8", errors="replace")
        for m in REL.finditer(text):
            total += 1
            tgt = (p.parent / m.group(1)).resolve()
            if not tgt.exists():
                broken.setdefault(str(tgt.relative_to(ROOT)) if str(tgt).startswith(str(ROOT)) else str(tgt), []).append(str(p.relative_to(ROOT)))
        for m in ABS.finditer(text):
            total += 1
            if not (ROOT / m.group(1)).exists():
                broken.setdefault(m.group(1), []).append(str(p.relative_to(ROOT)))
print("links:", total)
for k, v in sorted(broken.items()):
    print("BROKEN", k, len(v), sorted(set(v))[:3])
