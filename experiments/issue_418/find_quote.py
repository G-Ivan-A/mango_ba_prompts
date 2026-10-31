#!/usr/bin/env python3
"""Найти фразу в Markdown-файле и показать заголовок раздела и якорь.

Использование: python3 experiments/issue_418/find_quote.py <файл> "<фраза>" [...]
Нормализация совпадает с scripts/validate_issue_418_backlog.py.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
import validate_issue_418_backlog as v  # noqa: E402

path = Path(sys.argv[1])
for phrase in sys.argv[2:]:
    hits = v.locate_quote(path, phrase)
    print(f"{phrase!r} ->", hits or "НЕ НАЙДЕНО")
