#!/usr/bin/env python3
"""RUN-0085: Ш-В, A2 (контроль) против A3 (BL-156г, issue #450).

Обвязка RUN-0084 с другими плечами и правилом решения. Пред-регистрация —
`preregistration.md`, закоммичена до запуска подагентов.
Команды: prepare | judge | score | fixate WORK.
"""
import importlib.util, json, statistics, subprocess, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("run84", ROOT / "experiments/issue_448/run0084/run.py")
R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
rule = R.load("a3_rule", HERE / "a3_rule.py")
PIN_COMMIT = "519be3ce"  # РТ-7 в prompts/: A2 — v0.2 на новом срезе


def texts(check=True):
    a2 = R.git("show", f"{PIN_COMMIT}:{R.PROMPT}")
    return {"A2": a2, "A3": rule.apply(a2)}


R.ARMS = ("A2", "A3"); R.LABELS = ("X", "Y"); R.RUN = ROOT / "runs/2026/RUN-0085"
R.SEEDS = {"r1": 8585, "r2": 8586, "r3": 8587}
R.BASE_COMMIT = PIN_COMMIT
R.texts = texts
T = texts()
R.SHA = {a: R.sha256(t) for a, t in T.items()}
R.VERSION = {"A2": "0.2 на срезе 68ad8fcf (опубликованный, контроль)", "A3": "A2 + уточнение BL-156г"}


def guardrail(fail, arm, control):
    """Р-18: кейс провален 3 из 3 у плеча и 0 из 3 у контроля."""
    return sorted(c for c, n in fail[arm].items() if n == 3 and fail[control].get(c, 0) == 0)


def score(work):
    v = R.load("v411", ROOT / "scripts/validate_issue_411_lessons_pipeline.py")
    cases = {c["case-id"]: c for c in v.golden_cases()}
    per = {rep: R.score_one(work / rep, cases) for rep in R.REPLICATES}
    s = {"replicates": {}, "median": {}, "fail_frequency": {}, "fail_by_criterion": {}}
    for arm in R.ARMS:
        rows = {rep: {"passed": per[rep][arm]["passed"], "core": R.first(per[rep][arm]["core"]),
                      "negatives_false_positive": R.first(per[rep][arm]["negatives_false_positive"]),
                      "failed": [f["case"] for f in per[rep][arm]["failed"]]} for rep in R.REPLICATES}
        s["replicates"][arm] = rows
        s["median"][arm] = {m: int(statistics.median(rows[r][m] for r in R.REPLICATES)) for m in R.METRICS}
        s["fail_frequency"][arm] = dict(sorted(Counter(c for r in rows.values() for c in r["failed"]).items(), key=lambda kv: (-kv[1], kv[0])))
        s["fail_by_criterion"][arm] = dict(sorted(Counter(c for rep in R.REPLICATES for f in per[rep][arm]["failed"] for c in f["failed"]).items()))
    nw = R.not_worse(s["median"]["A3"], s["median"]["A2"])
    g = guardrail(s["fail_frequency"], "A3", "A2")
    s["decision"] = {"A3_vs_A2": nw, "guardrail_R18": g, "publish": "A3" if nw["not_worse"] and not g else "A2"}
    s["secondary"] = {c: {a: s["fail_frequency"][a].get(c, 0) for a in R.ARMS} for c in ("GS-BCREQ-25", "GS-BCREQ-12", "GS-BCREQ-03", "GS-BCREQ-N05")}
    (work / "summary.json").write_text(json.dumps(s, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: s[k] for k in ("median", "decision", "secondary", "fail_frequency", "fail_by_criterion")}, ensure_ascii=False, indent=1))
    return 0


def main():
    cmd, work = sys.argv[1], Path(sys.argv[2]).resolve()
    return {"prepare": R.prepare, "judge": R.judge, "score": score, "fixate": R.fixate}[cmd](work)


if __name__ == "__main__":
    raise SystemExit(main())
