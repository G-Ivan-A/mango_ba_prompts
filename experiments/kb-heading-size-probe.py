#!/usr/bin/env python3
"""Разведка: какие размеры шрифта несут ненумерованные заголовки в PDF.

Нужна для issue #317: новые руководства Mango Talker (11.06.2026) потеряли
нумерацию разделов и PDF outline, поэтому нумерованный детект `extract.py`
собирает весь документ в 2 раздела. Скрипт печатает распределение размеров
шрифта по строкам-кандидатам, чтобы выбрать порог для типографского fallback.

Запуск: python3 experiments/kb-heading-size-probe.py <file.pdf>
"""
import re
import sys
from collections import Counter

import pdfplumber

DOT_LEADER = re.compile(r"\.{4,}")


def main(path: str) -> int:
    with pdfplumber.open(path) as pdf:
        sizes = Counter()
        cand = Counter()
        samples = {}
        for page in pdf.pages:
            for line in page.extract_text_lines(layout=False):
                text = (line.get("text") or "").strip()
                if not text:
                    continue
                size = max((round(c.get("size", 0), 1) for c in line.get("chars", [])), default=0)
                for c in line.get("chars", []):
                    sizes[round(c.get("size", 0), 1)] += 1
                if len(text) <= 100 and not DOT_LEADER.search(text) and not text.isdigit():
                    cand[size] += 1
                    samples.setdefault(size, []).append(text[:60])
        body = sizes.most_common(1)[0][0]
        print(f"{path}\n  body_size={body}")
        for size, count in sorted(cand.items(), reverse=True):
            if size <= body:
                continue
            print(f"  size={size:5} lines={count:5} e.g. {samples[size][:3]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1]))
