#!/usr/bin/env python3
"""Извлечение текстового слоя PDF постранично (issue #313).

Используется для разбора ТЗ Заказчика перед оценкой исполнимости: текст
нужен постранично, потому что каждая оценка в отчёте обязана нести ссылку
на страницу источника.

Зависимость: pdfplumber (см. scripts/kb/requirements.txt).

    python3 experiments/issue_313_extract_pdf_text.py <src.pdf> <dst.txt>
"""
from __future__ import annotations

import sys
from pathlib import Path


def extract(src: Path, dst: Path) -> int:
    import pdfplumber

    pages = 0
    with pdfplumber.open(str(src)) as pdf, dst.open("w", encoding="utf-8") as out:
        for number, page in enumerate(pdf.pages, 1):
            out.write(f"\n\n===== PAGE {number} =====\n")
            out.write(page.extract_text() or "")
            pages = number
    return pages


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(__doc__, file=sys.stderr)
        return 2
    src, dst = Path(argv[1]), Path(argv[2])
    if not src.is_file():
        print(f"не найден файл: {src}", file=sys.stderr)
        return 1
    pages = extract(src, dst)
    print(f"{src} -> {dst}: страниц {pages}, символов {dst.stat().st_size}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
