#!/usr/bin/env python3
"""Issue #388: в docs/ba-processes/00-index.md заменить ссылки на архивные промпты
ссылками на набор BCREQ (stepwise -> stepwise, oneshot -> oneshot); дубли в ячейке
схлопнуть. Архивные файлы перечисляются отдельным разделом (трассируемость)."""
import re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
P = ROOT / "docs/ba-processes/00-index.md"
MAP = {
    "glossary-context-understanding-stepwise": "bcreq-context-understanding-stepwise",
    "glossary-context-understanding-oneshot": "bcreq-in-understanding-oneshot",
    "questions-customer-understanding-stepwise": "bcreq-context-understanding-stepwise",
    "questions-customer-understanding-legacy": "bcreq-in-understanding-oneshot",
    "fr-documentation-stepwise": "bcreq-fr-documentation-stepwise",
    "fr-documentation-oneshot": "bcreq-core-documentation-oneshot",
    "constraints-documentation-stepwise": "bcreq-constraints-documentation-stepwise",
    "constraints-documentation-oneshot": "bcreq-work-solution-design-oneshot",
    "technical-details-solution-design-stepwise": "bcreq-orr-solution-design-stepwise",
    "technical-details-solution-design-oneshot": "bcreq-work-solution-design-oneshot",
    "technical-details-solution-design-legacy": "bcreq-orr-solution-design-stepwise",
    "fr-validation-stepwise": "bcreq-review-validation-oneshot",
    "fr-validation-oneshot": "bcreq-review-validation-oneshot",
    "fr-validation-legacy": "bcreq-review-validation-oneshot",
    "uc-modeling-stepwise": "bcreq-uc-modeling-stepwise",
    "uc-modeling-oneshot": "bcreq-scenarios-modeling-oneshot",
    "us-modeling-stepwise": "bcreq-scenarios-modeling-oneshot",
    "us-modeling-oneshot": "bcreq-scenarios-modeling-oneshot",
}
LINK = re.compile(r"\[`([\w.-]+)\.md`\]\(\.\./\.\./prompts/archive/([\w.-]+)\.md\)")
text = P.read_text(encoding="utf-8")
out = []
for line in text.split("\n"):
    if line.startswith("|") and "prompts/archive/" in line:
        cells = line.split("|")
        for i, c in enumerate(cells):
            seen = set()
            def sub(m):
                name = m.group(2)
                new = MAP.get(name)
                if not new:
                    return m.group(0)
                link = f"[`{new}.md`](../../prompts/{new}.md)"
                if new in seen:
                    return "\x00"
                seen.add(new)
                return link
            c = LINK.sub(sub, c)
            # убрать схлопнутые дубли вместе с разделителями
            c = re.sub(r"(,\s*|\s*->\s*|;\s*legacy:\s*|;\s*)\x00", "", c)
            c = c.replace("\x00", "")
            cells[i] = c
        line = "|".join(cells)
    out.append(line)
P.write_text("\n".join(out), encoding="utf-8")
