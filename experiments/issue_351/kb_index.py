#!/usr/bin/env python3
"""Build an index of kb/processed sections with their true page ranges (from frontmatter)."""
from __future__ import annotations
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
KB = ROOT / "kb/processed"

def frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    body = text.split("---", 2)[1]
    data = {}
    for line in body.splitlines():
        m = re.match(r'^([a-z_]+):\s*(.*)$', line)
        if m:
            data[m.group(1)] = m.group(2).strip().strip('"')
    return data

def build():
    items = []
    for path in sorted(KB.rglob("*.md")):
        if path.name in ("index.md", "verification.md", "README.md"):
            continue
        fm = frontmatter(path)
        if not fm:
            continue
        items.append({
            "path": str(path.relative_to(ROOT)),
            "doc": path.relative_to(KB).parts[0],
            "doc_code": fm.get("doc_code", ""),
            "doc_title": fm.get("doc_title", ""),
            "source": fm.get("source", ""),
            "section": fm.get("section", fm.get("pdf_section", "")),
            "title": fm.get("title", ""),
            "pages": fm.get("pages", ""),
        })
    return items

if __name__ == "__main__":
    items = build()
    json.dump(items, open(Path(__file__).with_name("kb_index.json"), "w"), ensure_ascii=False, indent=1)
    print(len(items), "sections")
