# -*- coding: utf-8 -*-
"""Сводная таблица оценок требований №1-№386 для RUN-0066.

Собирает четыре части и проверяет полноту покрытия исходного файла.
"""

from assess_part1 import A as P1
from assess_part2 import A as P2
from assess_part3 import A as P3
from assess_part4 import A as P4

ALLOWED = {"Да", "Частично", "Нет", ""}

ASSESSMENTS = {}
for part in (P1, P2, P3, P4):
    for num, rec in part.items():
        assert num not in ASSESSMENTS, "дубликат требования: " + num
        ASSESSMENTS[num] = rec

EXPECTED = [str(i) for i in range(1, 387)]
missing = [n for n in EXPECTED if n not in ASSESSMENTS]
extra = [n for n in ASSESSMENTS if n not in EXPECTED]
assert not missing, "не оценены требования: %s" % missing
assert not extra, "лишние требования: %s" % extra

if __name__ == "__main__":
    from collections import Counter
    from evidence import EVIDENCE, WEB

    counts = Counter(v for v, _, _, _ in ASSESSMENTS.values())
    for num, (verdict, keys, comment, audit) in ASSESSMENTS.items():
        assert verdict in ALLOWED, (num, verdict)
        for key in keys:
            assert key in EVIDENCE or key in WEB, (num, key)
    print("всего требований:", len(ASSESSMENTS))
    for verdict in ("Да", "Частично", "Нет", ""):
        print("  %-10s %d" % (verdict or "(пусто)", counts.get(verdict, 0)))
