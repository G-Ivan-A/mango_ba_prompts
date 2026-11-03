#!/usr/bin/env python3
"""Измеряет общую часть 39 стандартов классов (issue #432, BL-151).

Строка считается общей, если она (без хвостовых пробелов) есть во всех
файлах standards/bcreq-manual-classes/NN-*.md. Доля — от непустых строк.
Запуск: python3 experiments/issue_432/measure_common_part.py
"""
import collections
import glob
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def main() -> int:
    files = sorted(glob.glob(os.path.join(ROOT, "standards/bcreq-manual-classes/[0-9][0-9]-*.md")))
    count = collections.Counter()
    per_file = []
    for path in files:
        with open(path, encoding="utf-8") as fh:
            lines = [line.rstrip() for line in fh if line.strip()]
        per_file.append(lines)
        for line in set(lines):
            count[line] += 1
    total = sum(len(lines) for lines in per_file)
    shared = sum(1 for lines in per_file for line in lines if count[line] == len(files))
    print(f"files={len(files)} nonempty_lines={total} common={shared} share={shared / total * 100:.1f}%")
    for line in per_file[0]:
        if count[line] == len(files):
            print("  ", line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
