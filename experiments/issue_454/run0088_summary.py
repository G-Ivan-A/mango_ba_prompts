#!/usr/bin/env python3
"""RUN-0088: recompute stage verdicts from the judges' JSON by the rules in logs/preregistration.md. Writes outputs/summary.json.

Rules: `готова` = steps complete, every section of the stage >= 80 % of its checklist on the document at the stage's gate,
no fail of X1/X2/X3, gate criteria covered without a human decision, nothing the BA needs is missing from the site.
`готова с дефектами` = steps complete, X1-X3 ok, but below the threshold or a workaround was needed.
`не готова` = a step incomplete or a fail of X1/X2/X3. Packets: `собирается` if P1-P5 pass for both.
Pairs repeat R2 only (amendment 2, A4): T passes at least as many criteria as A and T has no fail of J1, J2.
Judges' verdicts are read as they are; nothing is scored here.
"""
import json
from pathlib import Path

RUN = Path(__file__).resolve().parents[2] / "runs/2026/RUN-0088/outputs"
THRESHOLD = 0.8
STAGE = {"A-IN": ("a-in.json", ["1", "2"], "Г-IN"), "A-CORE": ("a-core.json", ["3", "4", "7"], "Г-С1"), "A-WORK": ("final.json", ["5", "6", "7", "8"], "Г-W")}
JUDGES = {"a-in": "a-in.json", "a-core": "a-core.json", "final": "final.json", "release": "release.json"}
# Steps BA could not take from the site, or took with a workaround: filled from step logs, not from judges.
BA_MISSING = json.loads((RUN / "ba-missing.json").read_text(encoding="utf-8")) if (RUN / "ba-missing.json").exists() else {}


def load(name):
    path = RUN / "judge-chain" / name
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def passed(block):
    return sum(1 for item in block.values() if item.get("verdict") == "pass"), len(block)


def section(judge, number):
    items = {k: v for k, v in judge.get("sections", {}).items() if k.startswith(f"S{number}.")}
    done, total = passed(items)
    return {"pass": done, "total": total, "share": round(done / total, 3) if total else None, "failed": sorted(k for k, v in items.items() if v.get("verdict") != "pass")}


def cross(judges):
    found = {}
    for judge in judges.values():
        if judge:
            found.update(judge.get("cross", {}))
    return {k: v.get("verdict") for k, v in sorted(found.items())}


def stage_verdict(name, judges, xs, completed=True):
    file, sections, gate = STAGE[name]
    judge = load(file)
    if not judge:
        return {"verdict": "нет данных"}
    table = {s: section(judge, s) for s in sections}
    gates = {k: {"verdict": v.get("verdict"), "report_accurate": v.get("report_accurate")} for k, v in judge.get("gates", {}).items() if k.startswith(gate)}
    critical = [x for x in ("X1", "X2", "X3") if xs.get(x) != "pass"]
    below = [s for s, row in table.items() if row["share"] is None or row["share"] < THRESHOLD]
    missing = BA_MISSING.get(name, [])
    if not completed or critical:
        verdict = "не готова"
    elif below or missing:
        verdict = "готова с дефектами"
    else:
        verdict = "готова"
    return {"verdict": verdict, "sections": table, "below_threshold": below, "critical_failed": critical, "gates": gates, "ba_missing": missing}


def pairs():
    key_path = RUN / "judge-pairs-key.json"
    if not key_path.exists():
        return {}
    key = json.loads(key_path.read_text(encoding="utf-8"))["key"]
    result = {}
    for step, letters in key.items():
        path = RUN / "judge-pairs" / f"{step}.json"
        if not path.exists():
            result[step] = {"verdict": "нет данных"}
            continue
        data = json.loads(path.read_text(encoding="utf-8"))[step]
        arm = {}
        for letter, name in letters.items():
            items = data[letter]
            arm[name] = {"J": {k: v.get("verdict") for k, v in items.items() if k.startswith("J")}, "C_pass": sum(1 for k, v in items.items() if k.startswith("C") and v.get("verdict") == "pass"),
                         "C_total": sum(1 for k in items if k.startswith("C")), "failed": sorted(k for k, v in items.items() if v.get("verdict") != "pass")}
        count = lambda name: sum(1 for k, v in data[next(l for l, n in letters.items() if n == name)].items() if v.get("verdict") == "pass")
        winner = data.get("overall")
        ok = count("T") >= count("A") and arm["T"]["J"].get("J1") == "pass" and arm["T"]["J"].get("J2") == "pass"
        result[step] = {"A": arm["A"], "T": arm["T"], "pass_A": count("A"), "pass_T": count("T"), "overall": letters.get(winner, "tie"), "R2_repeat": "T" if ok else "A"}
    return result


def main():
    judges = {k: load(v) for k, v in JUDGES.items()}
    xs = cross(judges)
    release = judges["release"] or {}
    packets = {}
    for name in ("ФТ", "ТЗ"):
        block = release.get("packets", {}).get(name, {})
        packets[name] = {"pass": sum(1 for v in block.values() if v.get("verdict") == "pass"), "total": len(block), "failed": sorted(k for k, v in block.items() if v.get("verdict") != "pass")}
    assembled = all(p["total"] == 5 and p["pass"] == 5 for p in packets.values())
    final = judges["final"]
    all_sections = {str(n): section(final, n) for n in range(1, 9)} if final else {}
    summary = {
        "ba_reviewed": False,
        "cross": xs,
        "stages": {name: stage_verdict(name, judges, xs) for name in STAGE},
        "final_document_sections": all_sections,
        "packets": packets,
        "packets_verdict": "собирается" if assembled else "не собирается",
        "pairs_repeat_of_R2": pairs(),
        "ba_missing_outside_stage_rule": {k: BA_MISSING.get(k, []) for k in ("A-RELEASE", "Ш-С")},
    }
    (RUN / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({"cross": xs, "stages": {k: v.get("verdict") for k, v in summary["stages"].items()}, "packets": packets}, ensure_ascii=False))


if __name__ == "__main__":
    main()
