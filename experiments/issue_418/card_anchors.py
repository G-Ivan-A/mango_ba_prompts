#!/usr/bin/env python3
"""Печатает ID карточки, файл и якорь заголовка (для ссылок из BACKLOG.md).

    python3 experiments/issue_418/card_anchors.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import validate_issue_418_backlog as v  # noqa: E402

for path in v.CARD_FILES:
    for number, level, anchor in v.headings(path):
        if anchor.startswith("bl-"):
            print(anchor[:6].upper(), path.name, anchor, sep="\t")
