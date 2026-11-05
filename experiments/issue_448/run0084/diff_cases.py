"""RUN-0084: провалы плеч по кейсам с заметками судей (для отчёта).

python3 experiments/issue_448/run0084/diff_cases.py /tmp/run84 [GS-BCREQ-25 ...]
Без кейсов — печатает кейсы, где частота провала у плеч различается.
"""
import json
import sys
from pathlib import Path

work = Path(sys.argv[1])
wanted = set(sys.argv[2:])
fails = {}
for rep in ("r1", "r2", "r3"):
    metrics = json.loads((work / rep / "metrics.json").read_text(encoding="utf-8"))
    for arm, data in metrics.items():
        for item in data["failed"]:
            fails.setdefault(item["case"], {}).setdefault(arm, []).append((rep, item["tid"], item["failed"], item["note"]))
for case in sorted(fails):
    counts = {arm: len(fails[case].get(arm, [])) for arm in ("A0", "A1", "A2")}
    if wanted and case not in wanted:
        continue
    if not wanted and len(set(counts.values())) == 1:
        continue
    print(f"== {case} {counts}")
    for arm in ("A0", "A1", "A2"):
        for rep, tid, failed, note in fails[case].get(arm, []):
            print(f"  {arm} {rep} {tid} {failed}: {note[:300]}")
