#!/usr/bin/env python3
"""Expand ``{{Ч-NN}}`` placeholders into absolute links to the quote register.

Issue #387: the meta-standards cite the chat only through rows of
``experiments/issue_387/chat-2026-10-22-23-register.md``. Authors write the
short placeholder ``{{Ч-NN}}``; this script replaces it with
``[р. TURN, Ч-NN](…/chat-2026-10-22-23-register.md?plain=1#LLINE)`` where TURN
and LINE are read from the register itself (no hard-coded table).

Usage::

    python3 experiments/issue_387_expand_quote_refs.py FILE [FILE ...]
    python3 experiments/issue_387_expand_quote_refs.py --check FILE [FILE ...]

``--check`` only reports remaining placeholders and unknown IDs (exit 1).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTER = ROOT / "experiments" / "issue_387" / "chat-2026-10-22-23-register.md"
BASE = (
    "https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/"
    "experiments/issue_387/chat-2026-10-22-23-register.md?plain=1"
)
ROW = re.compile(r"^\| (Ч-\d{2}) \| (\d+) \|")
PLACEHOLDER = re.compile(r"\{\{(Ч-\d{2})\}\}")


def load_register() -> dict[str, tuple[int, int]]:
    """Map Ч-NN → (turn, 1-based line number in the register)."""
    rows: dict[str, tuple[int, int]] = {}
    for lineno, line in enumerate(REGISTER.read_text(encoding="utf-8").splitlines(), 1):
        match = ROW.match(line)
        if match:
            rows[match.group(1)] = (int(match.group(2)), lineno)
    return rows


def link(qid: str, rows: dict[str, tuple[int, int]]) -> str:
    turn, line = rows[qid]
    return f"[р. {turn}, {qid}]({BASE}#L{line})"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("files", nargs="+", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    rows = load_register()
    status = 0
    for path in args.files:
        text = path.read_text(encoding="utf-8")
        ids = PLACEHOLDER.findall(text)
        unknown = sorted({qid for qid in ids if qid not in rows})
        if unknown:
            print(f"{path}: unknown register IDs {unknown}")
            status = 1
            continue
        if args.check:
            if ids:
                print(f"{path}: {len(ids)} placeholder(s) left")
                status = 1
            continue
        new = PLACEHOLDER.sub(lambda m: link(m.group(1), rows), text)
        if new != text:
            path.write_text(new, encoding="utf-8")
        print(f"{path}: expanded {len(ids)}")
    return status


if __name__ == "__main__":
    sys.exit(main())
