#!/usr/bin/env python3
"""Сопоставление версий ТЗ BCREQ-1199: v1 (RUN-0065) и v2 (RUN-0094), issue #484.

v1 — `experiments/issue_347/requirements.xlsx` (вложение issue #347, оценён в RUN-0065),
v2 — `SoC_внешний 29-10.xlsx` (вложение issue #484, эталон — `source_transcription.json`).

Сравнение механическое и двустороннее: каждая строка v1 сопоставляется с атомарными частями
v2 (`atoms.json`), каждая атомарная часть v2 — со строками v1. Метрики те же, что в правиле
> 90 % (`tender_similarity.py`): raw / core (difflib) и dice (5-символьные основы слов);
итог — максимум из трёх. Пороги: ≥ 0,9 — перенесено дословно, 0,6…0,9 — перенесено с
правками, < 0,6 — соответствия нет.

Результат: `version_diff.json` (полная матрица лучших соответствий).

    python3 experiments/issue_484/compare_versions.py
"""

from __future__ import annotations

import difflib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "issue_482"))
from tender_similarity import core, dice, low  # noqa: E402

V1 = HERE.parents[1] / "experiments/issue_347/requirements.xlsx"
V1_SHA = "4806288a13f03b4e972b726e92e267c4c627cab42ad4ade3929607c0fd4287ba"
NEAR, SAME = 0.6, 0.9


def v1_rows() -> list[dict]:
    """Непустые строки v1: лист требований (колонки B, C) и лист «SLA поддержки»."""
    import openpyxl

    wb = openpyxl.load_workbook(V1, data_only=True)
    out = []
    for title, col in (("Требования к системе", 2), ("SLA поддержки", 2)):
        ws = wb[title]
        for ri in range(1, ws.max_row + 1):
            values = [ws.cell(row=ri, column=c).value for c in range(1, ws.max_column + 1)]
            values = [str(v).strip() if v is not None else "" for v in values]
            text = values[col - 1] if title == "Требования к системе" else \
                " ".join(v for v in values if v)
            if not text:
                continue
            out.append({"rid": f"v1:{title}!{ri}", "sheet": title, "text": text,
                        "blocker": values[2] if title == "Требования к системе" else ""})
    return out


def best(text: str, pool: list[tuple[str, str]]) -> tuple[float, str]:
    """Лучшее соответствие текста в пуле: максимум из raw / core / dice."""
    a_low, a_core = low(text), core(text)
    top = (0.0, "")
    for rid, other in pool:
        score = max(difflib.SequenceMatcher(None, a_low, low(other)).ratio(),
                    difflib.SequenceMatcher(None, a_core, core(other)).ratio(),
                    dice(text, other))
        if score > top[0]:
            top = (score, rid)
    return top


def main() -> None:
    v1 = v1_rows()
    atoms = json.loads((HERE / "atoms.json").read_text(encoding="utf-8"))
    v2_atoms = [(f'{row["rid"]}#{i}', atom)
                for row in atoms for i, atom in enumerate(row["atoms"], start=1)]
    v2_pool = v2_atoms + [(row["rid"], "\n".join(t for t in (row["text"], row["tail"]) if t))
                          for row in atoms]
    v1_pool = [(r["rid"], r["text"]) for r in v1]

    forward = {}
    for row in v1:
        score, rid = best(row["text"], v2_pool)
        forward[row["rid"]] = {"score": round(score, 3), "match": rid, "sheet": row["sheet"],
                               "blocker": row["blocker"], "text": row["text"]}
    backward = {}
    for rid, atom in v2_atoms:
        score, match = best(atom, v1_pool)
        backward[rid] = {"score": round(score, 3), "match": match, "atom": atom}

    bucket = lambda d: (sum(v["score"] >= SAME for v in d.values()),
                        sum(NEAR <= v["score"] < SAME for v in d.values()),
                        sum(v["score"] < NEAR for v in d.values()))
    f_same, f_near, f_gone = bucket(forward)
    b_same, b_near, b_new = bucket(backward)
    print(f"v1 строк: {len(forward)} (требования {sum(v['sheet'] == 'Требования к системе' for v in forward.values())}, "
          f"SLA {sum(v['sheet'] == 'SLA поддержки' for v in forward.values())})")
    print(f"v1 -> v2: дословно {f_same}, с правками {f_near}, нет соответствия {f_gone}")
    print(f"v2 атомов: {len(backward)}")
    print(f"v2 -> v1: дословно {b_same}, с правками {b_near}, новых {b_new}")
    (HERE / "version_diff.json").write_text(
        json.dumps({"v1_sha256": V1_SHA, "forward": forward, "backward": backward},
                   ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
