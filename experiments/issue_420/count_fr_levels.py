#!/usr/bin/env python3
"""Issue #420: empirical check of the 5±2 rule on BCREQ section 3 in runs/.

Counts top-level FR items and the number of children per top-level item in
real run outputs (BA-edited and model drafts). Read-only; prints a Markdown
table used in docs/analysis/2026-10-31-standards-page-review.md.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# (run file, origin, top-level regex, child regex, start marker, end marker)
CASES = [
    ("runs/2026/RUN-0017/outputs/final-artifact.md", "редакция БА",
     r"^4\.\d+\. ", r"^4\.\d+\.\d+\. ", "### Функциональные требования", "### Нефункциональные"),
    ("runs/2026/RUN-0015/outputs/final-artifact.md", "итог прогона после правок БА",
     r"^\*\*4\.\d+\. ", r"^- 4\.\d+\.\d+\. ", "## Функциональные требования", "## Что осталось"),
    ("runs/2026/RUN-0063/outputs/functional-requirements-bcreq-1074.md", "черновик модели",
     r"^### FR-\d+", None, "## 3.", "## 4."),
    ("runs/2026/RUN-0064/outputs/functional-requirements.md", "черновик модели",
     r"^### FR-\d+", None, "## 3.", "## 4."),
    ("runs/2026/RUN-0078/outputs/bcreq-draft.md", "черновик модели",
     r"^\| FR-\d+", None, "## 3.", "## 4."),
]


def block(text, start, end):
    s = text.index(start)
    e = text.index(end, s + 1)
    return text[s:e].splitlines()


def main():
    print("| Прогон | Происхождение | Пунктов верхнего уровня | Подпунктов на пункт |")
    print("| --- | --- | --- | --- |")
    for rel, origin, top, child, start, end in CASES:
        lines = block((ROOT / rel).read_text(encoding="utf-8"), start, end)
        tops, children, current = [], {}, None
        for line in lines:
            if re.match(top, line):
                current = line
                tops.append(line)
                children[current] = 0
            elif child and current and re.match(child, line):
                children[current] += 1
        per = ", ".join(str(children[t]) for t in tops) if child else "—"
        print(f"| {rel.split('/')[2]} | {origin} | {len(tops)} | {per} |")


if __name__ == "__main__":
    main()
