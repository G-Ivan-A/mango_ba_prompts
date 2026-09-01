# -*- coding: utf-8 -*-
"""Аудит пагинации RUN-0065: сверка страниц из его ссылок с frontmatter БЗ."""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
OLD = os.path.join(REPO, "runs/2026/RUN-0065/outputs/L0-customer-form-with-assessment.md")
CITE = re.compile(r"\[([^\],]+?), §([^\],]*?)\s*«([^»]*)», с\.([^\]]+?)\]")

index = json.load(open(os.path.join(HERE, "kb_index.json"), encoding="utf-8"))


def truth(section, title):
    hits = [s for s in index
            if (s.get("pdf_section") or s.get("section")) == section
            and s.get("title", "").strip().lower() == title.strip().lower()]
    if not hits:
        hits = [s for s in index if s.get("title", "").strip().lower() == title.strip().lower()]
    return hits


text = open(OLD, encoding="utf-8").read()
seen = {}
for doc, sec, title, pages in CITE.findall(text):
    seen.setdefault((doc, sec, title, pages), 0)
    seen[(doc, sec, title, pages)] += 1

for (doc, sec, title, pages), count in sorted(seen.items(), key=lambda kv: -kv[1]):
    hits = truth(sec, title)
    real = ", ".join(sorted({h.get("pages", "?") for h in hits})) if hits else "раздел в БЗ не найден"
    norm = pages.replace("–", "-").replace("—", "-")
    verdict = "OK" if hits and norm in {h.get("pages", "") for h in hits} else "РАСХОЖДЕНИЕ"
    print("%-12s x%-4d %s §%s «%s»: в отчёте с.%s | в БЗ с.%s" % (verdict, count, doc, sec, title, pages, real))
