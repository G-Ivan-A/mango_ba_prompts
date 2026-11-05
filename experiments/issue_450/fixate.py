#!/usr/bin/env python3
"""Фиксация RUN-0085…0087 в runs/2026 из рабочих каталогов /tmp/w85, w86, w87, w86d.

Токены — из отчёта Claude Code о подагенте (subagent_tokens); запись одна на подагента.
usage: fixate.py
"""
import json, shutil
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parents[2]
REPS = ("r1", "r2", "r3")
FM = "---\nstatus: draft\nversion: 0.1\nupdated: 2026-11-05\ntemperature: 0.1\n---\n\n"
T85 = """r1 executor A2 b1 27601 54155 4
r1 executor A2 b2 27433 55235 4
r1 executor A3 b1 28217 61586 4
r1 executor A3 b2 27374 54252 4
r2 executor A2 b1 28167 60380 4
r2 executor A2 b2 27462 54572 4
r2 executor A3 b1 27993 59282 4
r2 executor A3 b2 27384 54502 4
r3 executor A2 b1 28578 62328 4
r3 executor A2 b2 27794 58090 4
r3 executor A3 b1 28540 63408 4
r3 executor A3 b2 27339 52184 4
r1 judge - b1 46412 56846 6
r1 judge - b2 45370 64092 6
r2 judge - b1 45783 58771 6
r2 judge - b2 45407 67378 6
r3 judge - b1 45859 57392 6
r3 judge - b2 46262 64311 6"""
T86 = """r1 executor C S1 30712 96797 4
r1 executor B S1 33064 113519 4
r1 executor C S3 30032 93643 4
r1 executor B S3 31152 97797 4
r1 executor C S6 32383 113079 4
r1 executor B S6 32401 105285 4
r2 executor C S1 31865 104800 4
r2 executor B S1 32591 110251 4
r2 executor C S3 31068 98831 4
r2 executor B S3 31388 100688 4
r2 executor C S6 31643 106112 4
r2 executor B S6 31847 99137 4
r3 executor C S1 33098 114138 4
r3 executor B S1 31398 96467 4
r3 executor C S3 31584 103147 4
r3 executor B S3 31563 102926 4
r3 executor C S6 31258 101854 4
r3 executor B S6 32418 104361 4
r1 judge - S1 34941 15449 5
r1 judge - S3 33213 14729 5
r1 judge - S6 36211 18656 5
r2 judge - S1 36697 22691 5
r2 judge - S3 34973 20482 5
r2 judge - S6 36208 21779 5
r3 judge - S1 37287 21447 5
r3 judge - S3 34882 15244 5
r3 judge - S6 36073 24388 5
r1 check-clean - shv 18879 8006 4
r2 check-clean - shv 18926 8442 4
r3 check-clean - shv 18792 6300 4
r1 check-discarded - shv 18799 - -
r2 check-discarded - shv 19046 - -
r3 check-discarded - shv 19100 - -"""
T87 = """r1 executor C SES 29989 47282 22
r1 executor B SES 30005 42729 22
r2 executor C SES 30777 49515 22
r2 executor B SES 30477 48271 22
r3 executor C SES 32456 62381 23
r3 executor B SES 30647 52662 22
r1 judge - SES 20582 17013 4
r2 judge - SES 21415 17103 4
r3 judge - SES 22854 19350 4"""
TOK = {"85": T85, "86": T86, "87": T87}


def tokens(n):
    rows = [l.split() for l in TOK[n].splitlines()]
    tsv = "rep\trole\tarm\tbatch\ttokens\tms\ttool_uses\n" + "".join("\t".join(r) + "\n" for r in rows)
    (ROOT / f"experiments/issue_450/run00{n}/tokens.tsv").write_text(tsv, encoding="utf-8")
    t = {}
    for r in rows:
        k = r[1] if r[1] != "executor" else f"executor_{r[2]}"
        t[k] = t.get(k, 0) + int(r[4])
    t["total"] = sum(t.values())
    return t


def copy_tree(src, dst):
    dst.mkdir(parents=True, exist_ok=True)
    for f in sorted(src.rglob("*")):
        if f.is_file() and "__pycache__" not in f.parts:
            d = dst / f.relative_to(src)
            d.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(f, d)


def base(n, process, body_inputs, prereg, related):
    run = ROOT / f"runs/2026/RUN-00{n}"
    for s in ("inputs", "outputs", "logs", "feedback"):
        (run / s).mkdir(parents=True, exist_ok=True)
    return run


def fixate(n):
    work = Path(f"/tmp/w{n}")
    run = base(n, "", "", "", "")
    copy_tree(work / "r1/exec", run / "inputs")
    if (work / "r1/mapping.json").exists():
        shutil.copyfile(work / "r1/mapping.json", run / "inputs/mapping.json")
    if (work / "criteria.txt").exists():
        shutil.copyfile(work / "criteria.txt", run / "inputs/criteria.txt")
    for rep in REPS:
        out = run / f"outputs/{rep}"
        copy_tree(work / rep / "out", out / "executor")
        out.mkdir(exist_ok=True)
        for f in sorted((work / rep / "judge").glob("out-*.json")):
            shutil.copyfile(f, out / f.name.replace("out-", "judge-scores-"))
        for name in ("judge-key.json", "metrics.json"):
            if (work / rep / name).exists():
                shutil.copyfile(work / rep / name, out / name)
    shutil.copyfile(work / "summary.json", run / "outputs/summary.json")
    return run


def main():
    res = {n: tokens(n) for n in TOK}
    for n in TOK:
        fixate(n)
    chk = ROOT / "runs/2026/RUN-0086/outputs/shv-check"
    chk.mkdir(parents=True, exist_ok=True)
    for r in REPS:
        shutil.copyfile(f"/tmp/w86d/{r}.json", chk / f"{r}.json")
    shutil.copyfile("/tmp/w86d/fragments.md", chk / "fragments.md")
    shutil.copyfile(ROOT / "experiments/issue_450/run0086/shv_check/expected.json", chk / "expected.json")
    ins = Path("/tmp/ins")
    for n, ex, jg in (("85", "85-r1-A2-1", "85j-r1-1"), ("86", "86-r1-S1-B", "86j-r1-S1"), ("87", "87-r1-B", "87j-r1")):
        logs = ROOT / f"runs/2026/RUN-00{n}/logs"
        (logs / "executor-instruction.md").write_text(FM + "# Инструкция исполнителя (образец)\n\n```text\n" + (ins / f"{ex}.txt").read_text(encoding="utf-8") + "\n```\n", encoding="utf-8")
        (logs / "judge-instruction.md").write_text(FM + "# Инструкция судьи (образец)\n\n```text\n" + (ins / f"{jg}.txt").read_text(encoding="utf-8") + "\n```\n", encoding="utf-8")
    (ROOT / "experiments/issue_450/tokens-summary.json").write_text(json.dumps(res, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
