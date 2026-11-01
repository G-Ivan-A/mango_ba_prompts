#!/usr/bin/env python3
"""Issue #420: check relative links and GitHub-style anchors in given Markdown files."""
import re, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def slug(h):
    h = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", h).strip().lower()
    h = re.sub(r"[`*]", "", h)
    return re.sub(r"[^\w\- ]", "", h).replace(" ", "-")


def anchors(path):
    found, seen, fenced = set(), Counter(), False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("```"):
            fenced = not fenced
            continue
        m = None if fenced else re.match(r"^(#{1,6})\s+(.*?)\s*#*\s*$", line)
        if m:
            b = slug(m.group(2))
            found.add(b if not seen[b] else f"{b}-{seen[b]}")
            seen[b] += 1
        found.update(re.findall(r'<a id="([^"]+)"', line))
    return found


bad = 0
for name in sys.argv[1:]:
    src = (ROOT / name).resolve()
    for target in re.findall(r"\]\(([^)\s]+)\)", src.read_text(encoding="utf-8")):
        if re.match(r"^(https?:|mailto:)", target):
            continue
        path, _, anchor = target.partition("#")
        dest = (src.parent / path).resolve() if path else src
        if not dest.exists():
            print(f"{name}: missing {target}"); bad += 1
        elif anchor and dest.suffix == ".md" and anchor not in anchors(dest):
            print(f"{name}: no anchor {target}"); bad += 1
print("OK" if not bad else f"{bad} problems")
sys.exit(1 if bad else 0)
