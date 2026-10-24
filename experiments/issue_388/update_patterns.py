#!/usr/bin/env python3
"""Issue #388: паттерны ссылаются на набор BCREQ; архивные промпты — предшественники."""
import re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
NEW = {
    "glossary-context-generation": ["bcreq-context-understanding-stepwise", "bcreq-in-understanding-oneshot"],
    "fr-generation": ["bcreq-fr-documentation-stepwise", "bcreq-core-documentation-oneshot"],
    "fr-validation": ["bcreq-review-validation-oneshot"],
    "user-story-generation": ["bcreq-scenarios-modeling-oneshot"],
    "usecase-generation": ["bcreq-uc-modeling-stepwise", "bcreq-scenarios-modeling-oneshot"],
}
ARCH_LINK = re.compile(r"\[`([\w-]+\.md)`\]\(((?:\.\./)+)prompts/archive/\1\)")

for slug, new in NEW.items():
    p = ROOT / "patterns" / slug / "README.md"
    t = p.read_text(encoding="utf-8")
    m = re.search(r"- \*\*Related prompt implementations\*\*:\n((?:  .*\n)+)", t)
    old_block = m.group(1)
    olds = ARCH_LINK.findall(old_block)
    lines = ",\n".join(f"  [`{n}.md`](../../prompts/{n}.md)" for n in new) + ".\n"
    arch = ", ".join(f"[`{n}`](../../prompts/archive/{n})" for n, _ in olds)
    block = (lines + "- **Архивные предшественники (issue #388)**: " + arch + ".\n")
    t = t[: m.start(1)] + block + t[m.end(1):]
    p.write_text(t, encoding="utf-8")

p = ROOT / "patterns/README.md"
t = p.read_text(encoding="utf-8")
out = []
for line in t.split("\n"):
    m = re.match(r"\| \[`([\w-]+)`\]\(\1/\) \|", line)
    if m and m.group(1) in NEW:
        cells = line.split(" | ")
        olds = ARCH_LINK.findall(cells[-1])
        new = ", ".join(f"[`{n}.md`](../prompts/{n}.md)" for n in NEW[m.group(1)])
        arch = ", ".join(f"[`{n}`](../prompts/archive/{n})" for n, _ in olds)
        cells[-1] = f"{new}; архив: {arch} |"
        line = " | ".join(cells)
    out.append(line)
p.write_text("\n".join(out), encoding="utf-8")

v = ROOT / "scripts/validate_issue_85_patterns_library.py"
s = v.read_text(encoding="utf-8")
for slug, new in NEW.items():
    s = re.sub(
        rf'(    "{slug}": \{{\n(?:        "(?:operation|processes)".*\n)+        "prompts": )\[[^\]]*\]',
        lambda m: m.group(1) + "[" + ", ".join(f'"{n}.md"' for n in new) + "]",
        s,
    )
v.write_text(s, encoding="utf-8")
