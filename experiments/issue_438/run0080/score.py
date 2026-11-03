#!/usr/bin/env python3
"""RUN-0080: подсчёт метрик по рубрике K1–K6 и решение о публикации (issue #438).

Читает оценки слепых судей (judge/out-batch*.json), ключ X/Y → A/D,
раскладку T-NN → case-id и golden set. Пишет metrics.json: метрики A и D,
разницу и сравнение D с базовой линией RUN-0079 (опубликованная v0.1).

Правило публикации (DEC-427-11, поправка 0.6 RFC #427): черновик «не хуже
базовой линии» — не меньше сданных кейсов и ядра, не больше ложных дефектов,
чем у v0.1, и в RUN-0079 (49/62, 10/11, 0/10), и в этом прогоне (A).

Использование:
    python3 experiments/issue_438/run0080/score.py WORKDIR
"""
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

from prepare import ROOT, load_validator

CRITERIA = ("K1", "K2", "K3", "K4", "K5", "K6")
VERSIONS = ("A", "D")
BASELINE = ROOT / "runs/2026/RUN-0079/outputs/metrics.json"


def ratio(text: str) -> tuple[int, int]:
    good, total = text.split("/")
    return int(good), int(total)


def not_worse(candidate: dict, reference: dict) -> dict:
    checks = {
        "passed": candidate["passed"] >= reference["passed"],
        "core": ratio(candidate["core"])[0] >= ratio(reference["core"])[0],
        "negatives_false_positive": ratio(candidate["negatives_false_positive"])[0] <= ratio(reference["negatives_false_positive"])[0],
    }
    return {"checks": checks, "not_worse": all(checks.values())}


def score_version(version: str, meta: dict, cases: dict, scores: dict) -> dict:
    per_criterion = {c: [0, 0] for c in CRITERIA}
    passed = core_passed = core_total = neg_total = neg_fp = 0
    failed_cases = []
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
        if negative:
            neg_total += 1
            neg_fp += not score.get("K1")
        if case["Ядро"] == "да":
            core_total += 1
            core_passed += ok
        passed += ok
        if not ok:
            failed_cases.append({
                "case": case_id, "tid": tid, "lesson": case["Урок"],
                "failed": [c for c in applicable if not score.get(c)], "note": score.get("note", ""),
            })
    return {
        "prompt_version": meta[f"prompt_{version}"]["version"],
        "prompt_path": meta[f"prompt_{version}"]["path"],
        "prompt_ref": meta[f"prompt_{version}"]["ref"],
        "prompt_sha256": meta[f"prompt_{version}"]["sha256"],
        "cases": len(meta["mapping"]),
        "passed": passed,
        "core": f"{core_passed}/{core_total}",
        "negatives_false_positive": f"{neg_fp}/{neg_total}",
        "criteria": {c: f"{v[0]}/{v[1]}" for c, v in per_criterion.items()},
        "failed": failed_cases,
    }


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
    metrics = {version: score_version(version, meta, cases, scores) for version in VERSIONS}
    both = defaultdict(list)
    for version in VERSIONS:
        for item in metrics[version]["failed"]:
            both[item["case"]].append(version)
    metrics["diff"] = {
        "only_A_failed": sorted(c for c, v in both.items() if v == ["A"]),
        "only_D_failed": sorted(c for c, v in both.items() if v == ["D"]),
        "both_failed": sorted(c for c, v in both.items() if v == ["A", "D"]),
    }
    baseline = json.loads(BASELINE.read_text(encoding="utf-8"))["A"]
    metrics["baseline_RUN_0079_A"] = {k: baseline[k] for k in ("prompt_version", "passed", "core", "negatives_false_positive")}
    metrics["publication"] = {
        "rule": "DEC-427-11: D не хуже v0.1 — по сданным кейсам, ядру и ложным дефектам",
        "vs_RUN_0079": not_worse(metrics["D"], baseline),
        "vs_A_same_judge": not_worse(metrics["D"], metrics["A"]),
    }
    metrics["publication"]["not_worse"] = metrics["publication"]["vs_RUN_0079"]["not_worse"] and metrics["publication"]["vs_A_same_judge"]["not_worse"]
    (work / "metrics.json").write_text(json.dumps(metrics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for version in VERSIONS:
        m = metrics[version]
        print(version, m["prompt_version"], "passed", m["passed"], "/", m["cases"], "core", m["core"], "fp", m["negatives_false_positive"], m["criteria"])
    print(metrics["diff"])
    print("publication", json.dumps(metrics["publication"], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
