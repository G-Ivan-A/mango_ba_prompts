# -*- coding: utf-8 -*-
"""A/B-сравнение RUN-0066 (Claude Opus) и RUN-0065 (gpt-5.6-sol).

Сопоставление построчное по тексту требования (в RUN-0065 колонка «№» отсутствует).
Сравниваются: вердикты, набор § в атомарных ссылках, номера страниц.
"""
import collections
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
NEW = os.path.join(REPO, "runs/2026/RUN-0066/outputs/L0-feasibility-assessment-1099-2.md")
OLD = os.path.join(REPO, "runs/2026/RUN-0065/outputs/L0-customer-form-with-assessment.md")

CITE_NEW = re.compile(r"\[([^\[\]]+?), (?:§([^\[\]«]+?) )?«[^»]*», с\.([^\[\]]+?)\]\(([^()]+)\)")
CITE_OLD = re.compile(r"\[([^\],]+?), §([^\],]+?), с\.([^\]]+?)\]")


def rows(path):
    out = []
    for line in open(path, encoding="utf-8"):
        if line.startswith("|"):
            out.append([c.strip() for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))])
    return out[2:]


def norm(text):
    return re.sub(r"\s+", " ", text.replace("<br>", " ")).strip().lower()


def verdict(cell):
    return re.sub(r"[*.]", "", cell).strip()


def main():
    new = {norm(r[1]): r for r in rows(NEW) if len(r) == 6 and r[0].isdigit()}
    old = {}
    for r in rows(OLD):
        if len(r) >= 6:
            old.setdefault(norm(r[0]), r)

    stats = collections.Counter()
    pages_mismatch = []
    verdict_diff = []
    for key, nrow in new.items():
        orow = old.get(key)
        if orow is None:
            stats["нет пары в RUN-0065"] += 1
            continue
        stats["сопоставлено"] += 1
        nv, ov = verdict(nrow[3]), verdict(orow[3])
        if nv == ov:
            stats["вердикт совпал"] += 1
        else:
            stats["вердикт разошёлся"] += 1
            verdict_diff.append((nrow[0], ov or "(пусто)", nv or "(пусто)"))
        ncites = {(d, s): p for d, s, p, _ in CITE_NEW.findall(nrow[4])}
        ocites = {(d, s): p for d, s, p in CITE_OLD.findall(orow[4])}
        for anchor in set(ncites) & set(ocites):
            stats["§ совпал"] += 1
            np, op = ncites[anchor], ocites[anchor].replace("–", "-").replace("—", "-")
            if np == op:
                stats["страницы совпали"] += 1
            else:
                stats["страницы разошлись"] += 1
                pages_mismatch.append((nrow[0], anchor[0], anchor[1], op, np))

    for k, v in stats.most_common():
        print("%-24s %d" % (k, v))
    print("\nПримеры расхождений по страницам (№, док, §, RUN-0065 → RUN-0066):")
    for item in pages_mismatch[:25]:
        print("  №%s %s §%s: с.%s → с.%s" % item)
    print("\nВсего расхождений по страницам: %d" % len(pages_mismatch))
    print("Всего расхождений по вердиктам: %d" % len(verdict_diff))
    counter = collections.Counter((o, n) for _, o, n in verdict_diff)
    for (o, n), c in counter.most_common():
        print("  %s → %s: %d" % (o, n, c))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
