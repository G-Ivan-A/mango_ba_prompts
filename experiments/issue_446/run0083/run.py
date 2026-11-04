#!/usr/bin/env python3
"""RUN-0083: синтетический прогон A-IN, P (v0.1) против T (черновики «по тесту»), issue #446.

Правило решения — в `preregistration.md` (закоммичено до запуска подагентов):
T идёт в комплект прогона как `by-test`, если сдал не меньше критериев,
чем P, и не провалил ни одного из критических J03, J07, J11.

Использование:
    python3 experiments/issue_446/run0083/run.py blind  WORK   # X/Y по seed 8085
    python3 experiments/issue_446/run0083/run.py score  WORK   # summary.json
    python3 experiments/issue_446/run0083/run.py fixate WORK   # runs/2026/RUN-0083/

WORK — каталог прогона (`/tmp/run83`): `out/{P,T}-transcript.md`,
`judge/{X,Y}.md`, `judge/key.json`, `judge/scores.json`.
"""
from __future__ import annotations

import hashlib
import json
import random
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
RUN = ROOT / "runs/2026/RUN-0083"
SEED = 8085
CRITICAL = ("J03", "J07", "J11")
CRITERIA = tuple(f"J{n:02d}" for n in range(1, 13))
STEPS = {
    "Ш-0": "bcreq-constitution-governance-oneshot.md",
    "Ш-1": "bcreq-context-understanding-stepwise.md",
    "Ш-2": "bcreq-products-impact-analysis-stepwise.md",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path: Path, data) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def blind(work: Path) -> int:
    order = ["P", "T"]
    random.Random(SEED).shuffle(order)
    key = {"X": order[0], "Y": order[1], "seed": SEED}
    (work / "judge").mkdir(exist_ok=True)
    for label in ("X", "Y"):
        shutil.copyfile(work / f"out/{key[label]}-transcript.md", work / f"judge/{label}.md")
    dump(work / "judge/key.json", key)
    print("blinded", "X" if key["X"] == "P" else "Y", "= P")
    return 0


def score(work: Path) -> int:
    key = json.loads((work / "judge/key.json").read_text(encoding="utf-8"))
    scores = json.loads((work / "judge/scores.json").read_text(encoding="utf-8"))
    arms = {key["X"]: "X", key["Y"]: "Y"}
    passed, failed = {}, {}
    for arm, label in arms.items():
        verdicts = {c: scores[label][c]["verdict"] for c in CRITERIA}
        passed[arm] = sum(v == "pass" for v in verdicts.values())
        failed[arm] = [c for c, v in verdicts.items() if v != "pass"]
    critical_t = sorted(set(CRITICAL) & set(failed["T"]))
    summary = {
        "rule": {"text": "T — by-test, если passed T ≥ passed P и нет провала T по критическим", "critical": list(CRITICAL)},
        "judge_seed": SEED,
        "passed": passed,
        "failed": failed,
        "overall": {"winner": key.get(scores.get("overall"), scores.get("overall")), "reason": scores.get("overall_reason", "")},
        "decision": {"t_not_fewer": passed["T"] >= passed["P"], "t_critical_fails": critical_t,
                     "by_test": passed["T"] >= passed["P"] and not critical_t},
        "prompts": {arm: {step: sha256(ROOT / ("prompts/drafts" if arm == "T" else "prompts") / name)
                          for step, name in STEPS.items()} for arm in ("P", "T")},
    }
    previous = work / "summary.json"
    if previous.exists():
        # Обработка провалов T дописывается вручную после разбора (п. 2 правила).
        summary["t_fail_handling"] = json.loads(previous.read_text(encoding="utf-8")).get("t_fail_handling", {})
    dump(previous, summary)
    print(json.dumps({k: summary[k] for k in ("passed", "failed", "decision", "overall")}, ensure_ascii=False))
    return 0


def fixate(work: Path) -> int:
    for sub in ("inputs", "outputs", "logs", "feedback"):
        (RUN / sub).mkdir(parents=True, exist_ok=True)
    for name in ("input-pack.md", "ba-script.md"):
        shutil.copyfile(HERE / name, RUN / f"inputs/{name}")
    for name in ("executor-instruction.md", "judge-instruction.md", "preregistration.md"):
        shutil.copyfile(HERE / name, RUN / f"logs/{name}")
    for arm in ("P", "T"):
        shutil.copyfile(work / f"out/{arm}-transcript.md", RUN / f"outputs/{arm}-transcript.md")
    shutil.copyfile(work / "judge/scores.json", RUN / "outputs/judge-scores.json")
    shutil.copyfile(work / "judge/key.json", RUN / "outputs/judge-key.json")
    shutil.copyfile(work / "summary.json", RUN / "outputs/summary.json")
    print(f"fixated into {RUN.relative_to(ROOT)}")
    return 0


def main() -> int:
    command, work = sys.argv[1], Path(sys.argv[2]).resolve()
    return {"blind": blind, "score": score, "fixate": fixate}[command](work)


if __name__ == "__main__":
    raise SystemExit(main())
