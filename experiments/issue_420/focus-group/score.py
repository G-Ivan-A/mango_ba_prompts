#!/usr/bin/env python3
"""Issue #420: deterministic scoring of the synthetic executive focus group.

    python3 experiments/issue_420/focus-group/score.py            # score all rounds, write results.md
    python3 experiments/issue_420/focus-group/score.py --check    # exit 1 if results.md is stale

Layout: round-N/stimuli/stimulus-<X>.md (what agents read), round-N/responses/<X>-<P>.json
(one agent = one persona + one stimulus), round-N/unblinding.json ({"X": "baseline", ...}).

An answer counts as *identified* when it matches the answer key below AND the persona marked it
`однозначно`. A persona counts as *satisfied* at satisfaction >= 4 of 5. Targets from issue #420:
identification >= 85 %, satisfied >= 95 % (with 7 personas that is 7 of 7).
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "results.md"
TARGET_ID, TARGET_SAT = 0.85, 0.95


def has(*patterns):
    return lambda text: all(re.search(p, text, re.I) for p in patterns)


# Answer key: what the BCREQ standards (standards/bcreq-sections/*, docs/contracts/bcreq-stage-gates.md,
# docs/adr/003-ba-ontology.md) say, plus the RFC-420 proposals the issue asks for (Q5: Mango
# agreed-terms reference as the priority base; Q6: one counting unit).
KEY = {
    "Q1": has(r"(?<![\d.])8(?![\d.])|восем"),
    "Q2": has(r"2\.1", r"2\.2", r"2\.3", r"2\.4"),
    "Q3": has(r"1\s*[–—-]\s*4|1, 2, 3,? и 4|1, 2, 3, 4|с 1 по 4|перв\w+ четыр"),
    "Q4": has(r"владел\w* продукт", r"архитектор", r"КК|крупн\w* клиент"),
    "Q5": has(r"согласованн\w* термин|D0"),
    "Q6": has(r"3\s*[–—-]\s*7|от 3 до 7|от тр[её]х до семи|5\s*±\s*2", r"ФТ|функциональн|раздел\w* 3|требовани|уровн|пункт|групп"),
    "Q7": has(r"кажд\w*\s+(отдельн\w*\s+)?(элемент|пункт|требован|термин)|отдельн\w+ (элемент|пункт)|удал", r"набор|целиком|в целом|полнот|совокупн|все вместе|весь (раздел|список)"),
    "Q8": has(r"(?<![\d.])7(?![\d.])|UC|сценари"),
    "Q9": has(r"особенност|ограничени|претензи|ожида|не снять|нельзя снять"),
    "Q10": has(r"БА", r"реш|утвержд|выбира|рекоменд|показ"),
}
QUESTIONS = list(KEY)


def load_round(path):
    unblind = json.loads((path / "unblinding.json").read_text(encoding="utf-8"))
    rows = []
    for file in sorted((path / "responses").glob("*.json")):
        data = json.loads(file.read_text(encoding="utf-8"))
        stimulus = file.stem.split("-")[0]
        per_q = {}
        for q in QUESTIONS:
            a = data["answers"].get(q, {})
            text = f"{a.get('answer', '')}"
            correct = KEY[q](text)
            sure = a.get("certainty", "").strip().lower() == "однозначно"
            per_q[q] = correct and sure
        rows.append({
            "variant": unblind[stimulus], "persona": data.get("persona", file.stem.split("-")[1]),
            "per_q": per_q, "satisfaction": int(data["satisfaction"]),
            "exec_ready": data.get("exec_ready", ""), "top_issues": data.get("top_issues", []),
        })
    return rows


def summarize(rows):
    by_variant = {}
    for r in rows:
        by_variant.setdefault(r["variant"], []).append(r)
    out = {}
    for variant, rs in by_variant.items():
        answers = [ok for r in rs for ok in r["per_q"].values()]
        out[variant] = {
            "n": len(rs),
            "identification": sum(answers) / len(answers),
            "satisfied": sum(r["satisfaction"] >= 4 for r in rs) / len(rs),
            "mean_satisfaction": sum(r["satisfaction"] for r in rs) / len(rs),
            "per_q": {q: sum(r["per_q"][q] for r in rs) / len(rs) for q in QUESTIONS},
            "exec_ready": {k: sum(r["exec_ready"] == k for r in rs) for k in ("да", "только стилистика", "нет")},
            "rows": sorted(rs, key=lambda r: r["persona"]),
        }
    return out


def pct(x):
    return f"{round(100 * x)} %"


def render():
    rounds = sorted((p for p in HERE.glob("round-*") if (p / "unblinding.json").exists()), key=lambda p: int(p.name.split("-")[1]))
    lines = [
        "# Синтетическая фокус-группа — результаты (issue #420)",
        "",
        "> Сгенерировано `score.py` из `round-*/responses/*.json`. Не редактировать вручную.",
        f"> Цели постановки: однозначная идентификация ≥ {pct(TARGET_ID)}, удовлетворённость (оценка ≥ 4 из 5) ≥ {pct(TARGET_SAT)}.",
        "",
        "| Раунд | Вариант | Персон | Идентификация | Удовлетворены | Средняя оценка | Готова для руководителей: да / стилистика / нет | Цели |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    details = []
    for path in rounds:
        summary = summarize(load_round(path))
        for variant in sorted(summary, key=lambda v: v != "baseline"):
            s = summary[variant]
            met = s["identification"] >= TARGET_ID and s["satisfied"] >= TARGET_SAT
            er = s["exec_ready"]
            lines.append(f"| {path.name} | {variant} | {s['n']} | {pct(s['identification'])} | {pct(s['satisfied'])} | {s['mean_satisfaction']:.1f} | {er['да']} / {er['только стилистика']} / {er['нет']} | {'✅ достигнуты' if met else '❌ нет'} |")
            details += [f"## {path.name} · {variant}", "", "| Вопрос | " + " | ".join(QUESTIONS) + " |", "| --- |" + " --- |" * len(QUESTIONS),
                        "| Однозначно и верно | " + " | ".join(pct(s["per_q"][q]) for q in QUESTIONS) + " |", "",
                        "| Персона | Оценка | Готова | Верно и однозначно | Главная претензия |", "| --- | --- | --- | --- | --- |"]
            for r in s["rows"]:
                issue = (r["top_issues"] or ["—"])[0].replace("|", "/")
                details.append(f"| {r['persona']} | {r['satisfaction']} | {r['exec_ready']} | {sum(r['per_q'].values())}/{len(QUESTIONS)} | {issue} |")
            details.append("")
    return "\n".join(lines + [""] + details).rstrip() + "\n"


def main():
    text = render()
    if "--check" in sys.argv:
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != text:
            print("results.md is stale: run score.py")
            sys.exit(1)
        print("results.md is up to date")
        return
    OUT.write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
