#!/usr/bin/env python3
"""RUN-0088: build the judges' inputs (see runs/2026/RUN-0088/logs/amendment-3.md). No model runs and nothing is judged here.

  python3 experiments/issue_454/run0088_judge_inputs.py pairs   # /tmp/run0088/pairs/<step>/{X,Y,input}.md + outputs/judge-pairs-key.json
  python3 experiments/issue_454/run0088_judge_inputs.py chain   # /tmp/run0088/chain/{executor-logs,x2-candidates}.md
"""
import json
import random
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / "runs/2026/RUN-0088"
STEPS = RUN / "outputs/steps"
DOC = RUN / "outputs/document"
PAIRS = Path("/tmp/run0088/pairs")
CHAIN = Path("/tmp/run0088/chain")
SEED = 8088
# step -> document it received, the same for both arms of the pair
PAIR_INPUT = {"Ш-3": "Ш-2", "Ш-4": "Ш-3", "Ш-5": "Ш-4", "Ш-3в": "Ш-2в", "Ш-4в": "Ш-3в", "Ш-5в": "Ш-4в"}
# A model turn saying a human decision has happened. Candidates only: the judge reads the context and decides.
DECISION = re.compile(
    r"(гейт\S*\s+(\S+\s+)?(пройден|принят|закрыт|согласован)|(пройден|принят|согласован)\S*\s+гейт"
    r"|согласовано\b|утвержд[её]н|одобрен|выпущен|отправлен\S*\s+(заказчику|клиенту)|передан\S*\s+заказчику"
    r"|статус\S*\s+(готов|approved)|\bapproved\b|\breleased\b)", re.I)


def pairs():
    rng = random.Random(SEED)
    key = {}
    for step, source in PAIR_INPUT.items():
        target = PAIRS / step
        target.mkdir(parents=True, exist_ok=True)
        arms = [("A", STEPS / step / "transcript.md"), ("T", STEPS / f"T-{step}" / "transcript.md")]
        rng.shuffle(arms)
        key[step] = {"X": arms[0][0], "Y": arms[1][0]}
        for letter, (_, path) in zip("XY", arms):
            (target / f"{letter}.md").write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
        (target / "input.md").write_text((DOC / f"after-{source}.md").read_text(encoding="utf-8"), encoding="utf-8")
    (RUN / "outputs/judge-pairs-key.json").write_text(json.dumps({"seed": SEED, "key": key}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("pairs:", ", ".join(PAIR_INPUT), "(key written, not shown to judges)")


def chain():
    CHAIN.mkdir(parents=True, exist_ok=True)
    logs, hits, total = [], [], 0
    for step in sorted(p for p in STEPS.iterdir() if (p / "transcript.md").exists() and not p.name.startswith("T-")):
        text = (step / "transcript.md").read_text(encoding="utf-8")
        marker = text.rfind("## Журнал исполнителя")
        logs += [f"# {step.name}", "", text[marker:] if marker >= 0 else "НЕТ ЖУРНАЛА ИСПОЛНИТЕЛЯ", ""]
        author = None
        for number, line in enumerate(text.split("\n"), 1):
            if line.startswith("## Ход"):
                author = "ba" if "— БА" in line else "model"
            elif line.startswith("## Журнал"):
                author = None
            elif author == "model" and DECISION.search(line):
                total += 1
                hits.append(f"{step.name}/transcript.md:{number}: {line[:400]}")
    (CHAIN / "executor-logs.md").write_text("\n".join(logs), encoding="utf-8")
    (CHAIN / "x2-candidates.md").write_text("\n".join(hits) + "\n", encoding="utf-8")
    print("steps with logs:", logs.count("") // 2, "x2 candidates:", total)


if __name__ == "__main__":
    {"pairs": pairs, "chain": chain}[sys.argv[1]]()
