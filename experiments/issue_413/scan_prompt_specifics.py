"""Exploration: count task-level identifiers in active prompts (issue #413)."""
import re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
PATTERNS = {
    "question-id": re.compile(r"\bQ-\d+(?:\.\d+)+\b"),
    "task-id": re.compile(r"\bBCREQ-\d+\b"),
    "run-id": re.compile(r"\bRUN-\d{3,}\b"),
    "scenario-id": re.compile(r"\bSC-\d+\b"),
    "issue-ref": re.compile(r"(?<![\w&/#])#\d{2,}\b|issues/\d+"),
}
for path in sorted((ROOT / "prompts").glob("*.md")):
    text = path.read_text(encoding="utf-8")
    counts = {k: len(p.findall(text)) for k, p in PATTERNS.items()}
    if any(counts.values()):
        print(path.name, counts)
        for n, line in enumerate(text.splitlines(), 1):
            for k, p in PATTERNS.items():
                for m in p.findall(line):
                    print(f"   {n}: {k}: {m}")
