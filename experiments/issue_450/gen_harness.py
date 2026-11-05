"""Обвязка генеративных замеров RUN-0086/0087: подготовка, слепая сборка, подсчёт."""
import json, random, re, statistics
from pathlib import Path
REPS = ("r1", "r2", "r3")
SEP = re.compile(r"^=== (\S+) ===\s*$", re.M)


def replies(path: Path) -> dict:
    if path.is_dir():
        return {p.stem: p.read_text(encoding="utf-8") for p in sorted(path.glob("*.md"))}
    parts = SEP.split(path.read_text(encoding="utf-8"))
    return {parts[i]: parts[i + 1].strip() for i in range(1, len(parts), 2)}


def blind(work, groups, arms, seeds, render, out_path):
    """render(group, case, {label: reply-text}) -> markdown; ключ — отдельно."""
    for rep in REPS:
        rng = random.Random(seeds[rep]); key = {}
        (work / rep / "judge").mkdir(parents=True, exist_ok=True)
        for g, cases in groups.items():
            text = []
            for c in cases:
                labels = ["X", "Y"]; rng.shuffle(labels)
                m = dict(zip(arms, labels)); key[c["id"]] = m
                rs = {m[a]: out_path(work / rep, g, a, c) for a in arms}
                text.append(render(g, c, dict(sorted(rs.items()))))
            body = "\n\n".join(text)
            assert not re.search(r"prompt-[BC]\b|плеч", body), g
            (work / rep / "judge" / f"judge-{g}.md").write_text(body, encoding="utf-8")
        (work / rep / "judge-key.json").write_text(json.dumps(key, ensure_ascii=False, indent=1), encoding="utf-8")


def decode(work, groups, arms):
    """-> {group:{arm:{rep:{case:{crit:value}}}}} снятием меток."""
    res = {g: {a: {} for a in arms} for g in groups}
    for rep in REPS:
        key = json.loads((work / rep / "judge-key.json").read_text(encoding="utf-8"))
        for g, cases in groups.items():
            data = json.loads((work / rep / "judge" / f"out-{g}.json").read_text(encoding="utf-8"))
            assert [d["case"] for d in data] == [c["id"] for c in cases], (rep, g)
            for a in arms:
                res[g][a][rep] = {d["case"]: d[key[d["case"]][a]] for d in data}
    return res


def med(values):
    return int(statistics.median(values))


def decide(rows, arms, count, benefit):
    """rows: {arm:{rep:{case:{crit}}}}. count(case,row)->(passed,core,false). Р-03 + Р-18 + польза."""
    ctl, new = arms
    m, fails = {}, {}
    for a in arms:
        per = {r: [count(c, v) for c, v in rows[a][r].items()] for r in REPS}
        m[a] = {"passed": med(sum(x[0] for x in per[r]) for r in REPS), "core": med(sum(x[1] for x in per[r]) for r in REPS),
                "false": med(sum(x[2] for x in per[r]) for r in REPS), "benefit": med(benefit(rows[a][r]) for r in REPS),
                "replicates_passed": [sum(x[0] for x in per[r]) for r in REPS]}
        fails[a] = {}
        for r in REPS:
            for c, v in rows[a][r].items():
                if not count(c, v)[0]:
                    fails[a][c] = fails[a].get(c, 0) + 1
    nw = m[new]["passed"] >= m[ctl]["passed"] and m[new]["core"] >= m[ctl]["core"] and m[new]["false"] <= m[ctl]["false"]
    guard = sorted(c for c, n in fails[new].items() if n == 3 and fails[ctl].get(c, 0) == 0)
    gain = m[new]["benefit"] > m[ctl]["benefit"]
    return {"median": m, "fail_frequency": fails, "not_worse": nw, "guardrail_R18": guard, "benefit_gain": gain, "publish": bool(nw and not guard and gain)}
