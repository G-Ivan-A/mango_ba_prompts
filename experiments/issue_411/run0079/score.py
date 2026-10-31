#!/usr/bin/env python3
"""RUN-0079: подсчёт метрик по рубрике K1–K6 (issue #411).

Читает оценки слепых судей (judge/out-batch*.json), ключ X/Y → A/B
(judge-key.json), карту T-NN → case-id (mapping.json) и golden set.
Пишет metrics.json с метриками по версии промпта.

Использование:
    python3 experiments/issue_411/run0079/score.py WORKDIR
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

from prepare import load_validator

CRITERIA = ("K1", "K2", "K3", "K4", "K5", "K6")


def main() -> int:
    work = Path(sys.argv[1]).resolve()
    meta = json.loads((work / "mapping.json").read_text(encoding="utf-8"))
    key = json.loads((work / "judge-key.json").read_text(encoding="utf-8"))
    cases = {case["case-id"]: case for case in load_validator().golden_cases()}
    scores = {}
    for path in sorted((work / "judge").glob("out-batch*.json")):
        for item in json.loads(path.read_text(encoding="utf-8")):
            for label in ("X", "Y"):
                scores[(item["case"], key[item["case"]][label])] = item[label]
    metrics = {}
    for version in ("A", "B"):
        per_criterion = {c: [0, 0] for c in CRITERIA}
        passed = core_passed = core_total = 0
        neg_total = neg_fp = 0
        failed_cases = []
        lesson_fail = Counter()
        for tid, case_id in sorted(meta["mapping"].items()):
            case = cases[case_id]
            score = scores[(tid, version)]
            negative = case["Эталонный вердикт"] == "дефекта нет"
            applicable = [c for c in CRITERIA if not (negative and c == "K2")]
            ok = True
            for criterion in applicable:
                value = bool(score.get(criterion))
                per_criterion[criterion][1] += 1
                per_criterion[criterion][0] += value
                ok &= value
            lesson = re.search(r"L-\d+", case["Урок"]).group(0)
            if negative:
                neg_total += 1
                neg_fp += not score.get("K1")
            if case["Ядро"] == "да":
                core_total += 1
                core_passed += ok
            passed += ok
            if not ok:
                failed = [c for c in applicable if not score.get(c)]
                failed_cases.append({"case": case_id, "lesson": case["Урок"], "failed": failed, "note": score.get("note", "")})
                lesson_fail[lesson] += 1
        metrics[version] = {
            "prompt_version": meta[f"prompt_{version}"]["version"],
            "prompt_ref": meta[f"prompt_{version}"]["ref"],
            "cases": len(meta["mapping"]),
            "passed": passed,
            "core": f"{core_passed}/{core_total}",
            "negatives_false_positive": f"{neg_fp}/{neg_total}",
            "criteria": {c: f"{v[0]}/{v[1]}" for c, v in per_criterion.items()},
            "failed": failed_cases,
        }
    both = defaultdict(list)
    for version in ("A", "B"):
        for item in metrics[version]["failed"]:
            both[item["case"]].append(version)
    metrics["diff"] = {
        "only_A_failed": sorted(c for c, v in both.items() if v == ["A"]),
        "only_B_failed": sorted(c for c, v in both.items() if v == ["B"]),
        "both_failed": sorted(c for c, v in both.items() if v == ["A", "B"]),
    }
    (work / "metrics.json").write_text(json.dumps(metrics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for version in ("A", "B"):
        m = metrics[version]
        print(version, m["prompt_version"], "passed", m["passed"], "/", m["cases"], "core", m["core"], "fp", m["negatives_false_positive"], m["criteria"])
    print(metrics["diff"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
