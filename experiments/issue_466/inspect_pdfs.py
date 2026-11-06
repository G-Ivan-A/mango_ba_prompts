#!/usr/bin/env python3
"""Локальное извлечение для анализа формы; аргумент — временный каталог вне git.

Требует PyMuPDF. Не скачивает URL и не обращается к БЗ. PDF и извлечённые
тексты после анализа удаляет оператор; stdout содержит только метаданные.
"""
import hashlib
import json
import sys
from pathlib import Path

import pymupdf

directory = Path(sys.argv[1]).resolve()
repository = Path(__file__).resolve().parents[2]
if directory.is_relative_to(repository):
    raise SystemExit("Используйте временный каталог вне репозитория")
for source in sorted(directory.glob("*.pdf")):
    with pymupdf.open(source) as document:
        pages = [f"\n--- PDF page {i + 1} ---\n" + p.get_text(sort=True)
                 for i, p in enumerate(document)]
        source.with_suffix(".txt").write_text("".join(pages), encoding="utf-8")
        print(json.dumps({"file": source.name, "pages": len(document),
                          "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                          "annotations": sum(len(list(p.annots() or [])) for p in document)},
                         ensure_ascii=False))
