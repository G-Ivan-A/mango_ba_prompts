#!/usr/bin/env python3
"""RUN-0086: блок отраслевой практики в Ш-1, Ш-3, Ш-6 (BL-167). prepare|judge|score WORK."""
import importlib.util, json, sys, hashlib
from pathlib import Path
import subprocess
ROOT = Path(__file__).resolve().parents[3]; HERE = Path(__file__).resolve().parent
def load(n, p):
    s = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(s); sys.modules[n] = m; s.loader.exec_module(m); return m
H = load("gen_harness", HERE.parent / "gen_harness.py"); C = load("cases86", HERE / "cases.py"); B = load("block86", HERE / "block_rule.py")
BASE = "519be3ce"; ARMS = ("C", "B"); SEEDS = {"r1": 8686, "r2": 8687, "r3": 8688}
PATH = {"S1": B.S1, "S3": B.S3, "S6": B.S6}
ROWS = {c["id"]: c for g in C.GROUPS.values() for c in g}


def texts(g):
    t = subprocess.run(["git", "show", f"{BASE}:{PATH[g]}"], cwd=ROOT, capture_output=True, text=True, check=True).stdout
    return {"C": t, "B": B.apply(PATH[g], t)}


def prepare(w):
    sha = {}
    for rep in H.REPS:
        ex = w / rep / "exec"; ex.mkdir(parents=True, exist_ok=True); (w / rep / "out").mkdir(exist_ok=True)
        for g, cases in C.GROUPS.items():
            for a, t in texts(g).items():
                (ex / f"prompt-{g}-{a}.md").write_text(t, encoding="utf-8"); sha[f"{g}-{a}"] = hashlib.sha256(t.encode()).hexdigest()
            (ex / f"cases-{g}.md").write_text("\n\n".join(f"=== {c['id']} ===\n{c['body']}" for c in cases), encoding="utf-8")
    (w / "sha.json").write_text(json.dumps(sha, indent=1)); print(sha); return 0


def out(rep, g, a, c):
    return H.replies(rep / "out" / f"{g}-{a}.md")[c["id"]]


def render(g, c, rs):
    head = f"## {c['id']}\nПрактика применима: {'да' if c['a'] else 'нет'}. Сверка API: {'да' if c.get('api') else 'нет'}.\nЭталонное пояснение: {c['note']}\n\n### Вход\n{c['body']}"
    return head + "".join(f"\n\n### Выход {l}\n{t}" for l, t in rs.items())


def judge(w):
    H.blind(w, C.GROUPS, ARMS, SEEDS, render, out); (w / "criteria.txt").write_text(C.CRITERIA, encoding="utf-8"); return 0


def count(cid, v):
    guards = v["G1"] and v["G2"]
    ok = guards and v["G3"] and all(v.get(k) is not False for k in ("P1", "P2", "P3", "P4"))
    return int(bool(ok)), int(bool(guards)), int((not guards) or v.get("P3") is False)


def benefit(row):
    return sum(1 for v in row.values() if v.get("P1") is True and v.get("P2") is not False)


def score(w):
    d = H.decode(w, C.GROUPS, ARMS)
    s = {g: H.decide(d[g], ARMS, count, benefit) for g in d}
    (w / "summary.json").write_text(json.dumps(s, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(s, ensure_ascii=False, indent=1)); return 0


if __name__ == "__main__":
    raise SystemExit({"prepare": prepare, "judge": judge, "score": score}[sys.argv[1]](Path(sys.argv[2]).resolve()))
