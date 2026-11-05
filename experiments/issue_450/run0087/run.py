#!/usr/bin/env python3
"""RUN-0087: правила многоходовой сессии в Ш-0 (BL-168). prepare|judge|score WORK."""
import importlib.util, json, sys, hashlib, subprocess
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]; HERE = Path(__file__).resolve().parent
def load(n, p):
    s = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(s); sys.modules[n] = m; s.loader.exec_module(m); return m
H = load("gen_harness", HERE.parent / "gen_harness.py"); S = load("scen87", HERE / "scenarios.py"); R = load("rules87", HERE / "session_rules.py")
BASE = "519be3ce"; ARMS = ("C", "B"); SEEDS = {"r1": 8787, "r2": 8788, "r3": 8789}


def prepare(w):
    t = subprocess.run(["git", "show", f"{BASE}:{R.PROMPT}"], cwd=ROOT, capture_output=True, text=True, check=True).stdout
    tx = {"C": t, "B": R.apply(t)}
    for rep in H.REPS:
        ex = w / rep / "exec"; ex.mkdir(parents=True, exist_ok=True)
        for a, x in tx.items():
            (ex / f"prompt-{a}.md").write_text(x, encoding="utf-8"); (w / rep / "out" / a).mkdir(parents=True, exist_ok=True)
        for c in S.GROUPS["SES"]:
            for i, turn in enumerate(c["turns"], 1):
                (ex / f"{c['id']}-t{i}.md").write_text(turn, encoding="utf-8")
    print({a: hashlib.sha256(x.encode()).hexdigest() for a, x in tx.items()}); return 0


def out(rep, g, a, c):
    r = H.replies(rep / "out" / a)
    return "\n\n".join(f"#### Ход {i} — ответ\n{r[f'''{c['id']}-t{i}''']}" for i in range(1, len(c["turns"]) + 1))


def render(g, c, rs):
    turns = "\n\n".join(f"#### Реплика БА, ход {i}\n{t}" for i, t in enumerate(c["turns"], 1))
    return f"## {c['id']}\nКритерии: {S.COMMON} {c['criteria']}\nЭталонное пояснение: {c['note']}\n\n{turns}" + "".join(f"\n\n### Выход {l}\n{t}" for l, t in rs.items())


def judge(w):
    H.blind(w, S.GROUPS, ARMS, SEEDS, render, out); return 0


def count(cid, v):
    crit = {k: x for k, x in v.items() if k != "note"}
    return int(all(x is not False for x in crit.values())), int(v["G1"] is True), int(v["G1"] is False or v.get("N1") is False or v.get("N2") is False)


def benefit(row):
    return sum(count(c, v)[0] for c, v in row.items() if c != "S5")


def score(w):
    s = H.decide(H.decode(w, S.GROUPS, ARMS)["SES"], ARMS, count, benefit)
    (w / "summary.json").write_text(json.dumps(s, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(s, ensure_ascii=False, indent=1)); return 0


if __name__ == "__main__":
    raise SystemExit({"prepare": prepare, "judge": judge, "score": score}[sys.argv[1]](Path(sys.argv[2]).resolve()))
