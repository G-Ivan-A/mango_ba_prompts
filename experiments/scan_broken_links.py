#!/usr/bin/env python3
"""Разведочный скан относительных Markdown-ссылок в репозитории спицы.

Воспроизводит замер §4.3 анализа готовности Хаба (57 битых ссылок).
Плейсхолдеры вида <path> исключаются из счёта.
"""
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
SKIP_DIRS = {".git", "node_modules", "kb/processed"}

def is_external(target: str) -> bool:
    return bool(re.match(r"^(https?:|mailto:|tel:|#|data:|<)", target))

def main() -> int:
    broken = []
    total = 0
    for path in sorted(ROOT.rglob("*.md")):
        rel = path.relative_to(ROOT).as_posix()
        if rel.startswith(".git/"):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for m in LINK_RE.finditer(text):
            target = m.group(1).strip()
            if is_external(target):
                continue
            total += 1
            clean = target.split("#", 1)[0].split("?", 1)[0]
            if not clean:
                continue
            resolved = (path.parent / clean).resolve()
            if not resolved.exists():
                line = text[: m.start()].count("\n") + 1
                broken.append((rel, line, target))
    by_file = {}
    for rel, line, target in broken:
        by_file.setdefault(rel, []).append((line, target))
    for rel in sorted(by_file):
        print(f"\n{rel} ({len(by_file[rel])})")
        for line, target in by_file[rel]:
            print(f"  :{line} -> {target}")
    print(f"\nTOTAL relative links: {total}")
    print(f"TOTAL broken: {len(broken)} in {len(by_file)} files")
    return 0

if __name__ == "__main__":
    sys.exit(main())
