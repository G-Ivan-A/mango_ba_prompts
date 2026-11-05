#!/usr/bin/env python3
"""RUN-0084: Ш-В на трёх плечах с одновременным контролем (BL-156б+в, issue #448).

Пред-регистрация — `experiments/issue_448/run0084/preregistration.md`,
закоммичена до запуска подагентов. Кратко:

- A0 — `prompts/bcreq-review-validation-oneshot.md` v0.1 (контроль, Р-03);
- A1 — A0 + подстановка типа гейта (`experiments/issue_438/prompt-typing.json`);
  побайтно равен A RUN-0081/RUN-0082 (SHA-256 `adf82663…`);
- A2 — A1 + правило «правка без добавлений» (`no_additions.py`), лестница;
- N = 3 повтора r1…r3; в каждом свежие исполнители (3 плеча × 2 пакета) и
  свежие слепые судьи (2 пакета), три выхода на кейс под метками X/Y/Z,
  seed маскировки 8484, 8485, 8486;
- кейсы и раскладка T-NN — 62 кейса RUN-0079 (seed 79, 2 пакета);
- решение (Р-03): медиана плеча не хуже медианы A0 по сданным, ядру и
  ложным дефектам.

Тексты A0 и A1 берутся из коммита `BASE_COMMIT` (до публикации), поэтому
сценарий воспроизводим и после правки `prompts/`.

Использование:
    python3 experiments/issue_448/run0084/run.py texts   WORK
    python3 experiments/issue_448/run0084/run.py prepare WORK
    python3 experiments/issue_448/run0084/run.py judge   WORK
    python3 experiments/issue_448/run0084/run.py score   WORK
    python3 experiments/issue_448/run0084/run.py fixate  WORK
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import random
import shutil
import statistics
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
RUN81 = ROOT / "experiments/issue_444/run0081"
RUN = ROOT / "runs/2026/RUN-0084"
REPLICATES = ("r1", "r2", "r3")
ARMS = ("A0", "A1", "A2")
LABELS = ("X", "Y", "Z")
SEEDS = {"r1": 8484, "r2": 8485, "r3": 8486}
BATCHES = 2
CRITERIA = ("K1", "K2", "K3", "K4", "K5", "K6")
PROMPT = "prompts/bcreq-review-validation-oneshot.md"
#: Коммит слияния PR #447: опубликованный v0.1 до issue #448.
BASE_COMMIT = "4a4df7bc"
SHA = {
    "A0": "56dee0cc777870cb33ddf5db18fd2577103bc7611f8d36f5a9b27e46a16e0f9e",
    "A1": "adf826634b2e8190da4d0f4ef307a59104a6f8fa3da6ef5a48a3c923ada90581",
    "A2": "158c743e03db5529db44d1cbafd82541d05935c2cb427259c19c620409f11551",
}
VERSION = {
    "A0": "0.1 (опубликованный, контроль)",
    "A1": "0.1 + тип гейта (prompt-typing.json)",
    "A2": "0.1 + тип гейта + «правка без добавлений»",
}
METRICS = ("passed", "core", "negatives_false_positive")
FRONTMATTER = "---\nstatus: draft\nversion: 0.1\nupdated: 2026-11-04\ntemperature: 0.1\n---\n\n"


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(path.parent))
    spec.loader.exec_module(module)
    return module


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=True).stdout


def texts(check: bool = True) -> dict[str, str]:
    typing = load("bl156a", ROOT / "experiments/issue_444/bl156a_prompt_changes.py")
    rule = load("no_additions", HERE / "no_additions.py")
    a0 = git("show", f"{BASE_COMMIT}:{PROMPT}")
    a1 = typing.apply_typing(PROMPT, a0)
    a2 = rule.apply_rule(a1)
    result = {"A0": a0, "A1": a1, "A2": a2}
    if check:
        for arm, text in result.items():
            assert sha256(text) == SHA[arm], (arm, sha256(text))
    return result


def cmd_texts(work: Path) -> int:
    for arm, text in texts(check=False).items():
        print(arm, sha256(text), len(text.encode("utf-8")))
    return 0


def prepare(work: Path) -> int:
    prep = load("prepare81", RUN81 / "prepare.py")
    arms = texts()
    head = git("rev-parse", "HEAD").strip()
    for rep in REPLICATES:
        rdir = work / rep
        # prepare.py RUN-0081 пишет кейсы и сверяет раскладку с RUN-0079;
        # его промпты A/D удаляются и заменяются тремя плечами.
        sys.argv = ["prepare.py", str(rdir)]
        if prep.main() != 0:
            return 1
        for old in ("A", "D"):
            (rdir / f"exec/prompt-{old}.md").unlink()
        meta = json.loads((rdir / "mapping.json").read_text(encoding="utf-8"))
        meta.pop("prompt_A"), meta.pop("prompt_D")
        for arm, text in arms.items():
            (rdir / f"exec/prompt-{arm}.md").write_text(text, encoding="utf-8")
            meta[f"prompt_{arm}"] = {"path": PROMPT, "ref": f"{BASE_COMMIT} + {head[:8]}", "version": VERSION[arm],
                                     "bytes": len(text.encode("utf-8")), "sha256": sha256(text)}
        meta["replicate"] = rep
        meta["judge_seed"] = SEEDS[rep]
        meta["baseline_run"] = "одновременный контроль A0 (Р-03)"
        (rdir / "mapping.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("prepared", " ".join(REPLICATES), " ".join(f"{a}={SHA[a][:8]}" for a in ARMS))
    return 0


def judge_one(work: Path, seed: int, jp) -> int:
    (work / "judge").mkdir(exist_ok=True)
    meta = json.loads((work / "mapping.json").read_text(encoding="utf-8"))
    cases = {case["case-id"]: case for case in jp.load_validator().golden_cases()}
    lessons = {item["id"]: item for item in json.loads((ROOT / "standards/bcreq-lessons/lessons.json").read_text(encoding="utf-8"))["lessons"]}
    outputs = {arm: jp.load_outputs(work, arm) for arm in ARMS}
    rng = random.Random(seed)
    key: dict = {}
    tids = sorted(meta["mapping"])
    size = (len(tids) + BATCHES - 1) // BATCHES
    leaks: list[str] = []
    import re
    for batch in range(BATCHES):
        lines = [f"# Слепая оценка, пакет {batch + 1}", ""]
        for tid in tids[batch * size:(batch + 1) * size]:
            case = cases[meta["mapping"][tid]]
            match = re.search(r"L-\d+", case["Урок"])
            lesson = lessons.get(match.group(0), {}) if match else {}
            order = list(ARMS)
            rng.shuffle(order)
            key[tid] = dict(zip(LABELS, order))
            negative = case["Эталонный вердикт"] == "дефекта нет"
            rendered = {label: jp.render(outputs[arm].get(tid)) for label, arm in key[tid].items()}
            leaks += [f"{tid}: {m}" for m in jp.LEAK_RE.findall("".join(rendered.values()))]
            lines += [
                f"## {tid}", "",
                f"**Вход:** {case['Вход']}", "",
                f"**Контекст:** {case['Контекст']}", "",
                f"**Эталонный вердикт:** {case['Эталонный вердикт']}", "",
                f"**Тип кейса:** {'негативный (K2 не применяется)' if negative else 'дефектный'}", "",
                f"**Правило урока:** {lesson.get('rule', '—')}", "",
                f"**Обоснование эталона:** {case['Обоснование эталона']}", "",
            ]
            for label in LABELS:
                lines += [f"### Выход {label}", "", rendered[label], ""]
        (work / f"judge/judge-batch{batch + 1}.md").write_text("\n".join(lines), encoding="utf-8")
    (work / "judge-key.json").write_text(json.dumps(key, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    rules = (ROOT / "runs/2026/RUN-0079/logs/judge-rules.md").read_text(encoding="utf-8")
    (work / "judge/rules.md").write_text(rules.split("---\n", 2)[2].lstrip("\n"), encoding="utf-8")
    print(f"cases={len(tids)} " + " ".join(f"{a}={len(outputs[a])}" for a in ARMS) + f" leaks={len(leaks)}")
    for leak in leaks:
        print("LEAK", leak)
    return 1 if leaks or any(len(outputs[a]) != len(tids) for a in ARMS) else 0


def judge(work: Path) -> int:
    jp = load("judge81", RUN81 / "judge_prepare.py")
    status = 0
    for rep in REPLICATES:
        print(rep, end=" ")
        status |= judge_one(work / rep, SEEDS[rep], jp)
    return status


def score_one(work: Path, cases: dict) -> dict:
    meta = json.loads((work / "mapping.json").read_text(encoding="utf-8"))
    key = json.loads((work / "judge-key.json").read_text(encoding="utf-8"))
    scores = {}
    for path in sorted((work / "judge").glob("out-batch*.json")):
        for item in json.loads(path.read_text(encoding="utf-8")):
            for label in LABELS:
                scores[(item["case"], key[item["case"]][label])] = item[label]
    metrics: dict = {}
    for arm in ARMS:
        per = {c: [0, 0] for c in CRITERIA}
        passed = core_ok = core_n = neg_n = neg_fp = 0
        failed = []
        for tid, case_id in sorted(meta["mapping"].items()):
            case = cases[case_id]
            score = scores[(tid, arm)]
            negative = case["Эталонный вердикт"] == "дефекта нет"
            applicable = [c for c in CRITERIA if not (negative and c == "K2")]
            ok = True
            for criterion in applicable:
                value = bool(score.get(criterion))
                per[criterion][0] += value
                per[criterion][1] += 1
                ok &= value
            if negative:
                neg_n += 1
                neg_fp += not score.get("K1")
            if case["Ядро"] == "да":
                core_n += 1
                core_ok += ok
            passed += ok
            if not ok:
                failed.append({"case": case_id, "tid": tid, "lesson": case["Урок"],
                               "failed": [c for c in applicable if not score.get(c)], "note": score.get("note", "")})
        metrics[arm] = {
            "prompt_version": meta[f"prompt_{arm}"]["version"], "prompt_sha256": meta[f"prompt_{arm}"]["sha256"],
            "cases": len(meta["mapping"]), "passed": passed, "core": f"{core_ok}/{core_n}",
            "negatives_false_positive": f"{neg_fp}/{neg_n}",
            "criteria": {c: f"{v[0]}/{v[1]}" for c, v in per.items()}, "failed": failed,
        }
    (work / "metrics.json").write_text(json.dumps(metrics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return metrics


def first(value) -> int:
    return int(str(value).split("/")[0])


def not_worse(candidate: dict, control: dict) -> dict:
    checks = {"passed": candidate["passed"] >= control["passed"], "core": candidate["core"] >= control["core"],
              "negatives_false_positive": candidate["negatives_false_positive"] <= control["negatives_false_positive"]}
    return {"checks": checks, "not_worse": all(checks.values())}


def score(work: Path) -> int:
    validator = load("v411", ROOT / "scripts/validate_issue_411_lessons_pipeline.py")
    cases = {case["case-id"]: case for case in validator.golden_cases()}
    per = {}
    for rep in REPLICATES:
        per[rep] = score_one(work / rep, cases)
        print(rep, " ".join(f"{a} {per[rep][a]['passed']}/{per[rep][a]['core']}/{per[rep][a]['negatives_false_positive']}" for a in ARMS))
    summary: dict = {"replicates": {}, "median": {}, "criteria_median": {}, "fail_frequency": {}, "decision": {}}
    for arm in ARMS:
        rows = {rep: {"passed": per[rep][arm]["passed"], "core": first(per[rep][arm]["core"]),
                      "negatives_false_positive": first(per[rep][arm]["negatives_false_positive"]),
                      "criteria": {c: first(v) for c, v in per[rep][arm]["criteria"].items()},
                      "failed": [f["case"] for f in per[rep][arm]["failed"]]} for rep in REPLICATES}
        summary["replicates"][arm] = rows
        summary["median"][arm] = {m: int(statistics.median(rows[r][m] for r in REPLICATES)) for m in METRICS}
        summary["criteria_median"][arm] = {c: int(statistics.median(rows[r]["criteria"][c] for r in REPLICATES)) for c in CRITERIA}
        counter = Counter(case for rep in REPLICATES for case in rows[rep]["failed"])
        summary["fail_frequency"][arm] = dict(sorted(counter.items(), key=lambda kv: (-kv[1], kv[0])))
        summary["fail_by_criterion"] = summary.get("fail_by_criterion", {})
        crit = Counter(c for rep in REPLICATES for f in per[rep][arm]["failed"] for c in f["failed"])
        summary["fail_by_criterion"][arm] = dict(sorted(crit.items()))
    med = summary["median"]
    decision = summary["decision"]
    decision["A1_vs_A0"] = not_worse(med["A1"], med["A0"])
    decision["A2_vs_A0"] = not_worse(med["A2"], med["A0"])
    decision["A2_vs_A1"] = not_worse(med["A2"], med["A1"])
    if decision["A2_vs_A0"]["not_worse"]:
        decision["publish"] = "A2"
    elif decision["A1_vs_A0"]["not_worse"]:
        decision["publish"] = "A1"
    else:
        decision["publish"] = None
    paired = {}
    for arm in ("A1", "A2"):
        paired[arm] = {rep: {m: summary["replicates"][arm][rep][m] - summary["replicates"]["A0"][rep][m] for m in METRICS} for rep in REPLICATES}
    summary["paired_minus_A0"] = paired
    summary["gs_bcreq_12_failed"] = {arm: summary["fail_frequency"][arm].get("GS-BCREQ-12", 0) for arm in ARMS}
    (work / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("== median", json.dumps(med, ensure_ascii=False))
    print("== criteria_median", json.dumps(summary["criteria_median"], ensure_ascii=False))
    print("== decision", json.dumps(decision, ensure_ascii=False))
    print("== paired", json.dumps(paired, ensure_ascii=False))
    print("== GS-BCREQ-12 failed", summary["gs_bcreq_12_failed"])
    print("== fail_by_criterion", json.dumps(summary["fail_by_criterion"], ensure_ascii=False))
    return 0


def merged(paths: list[Path]) -> list:
    items: list = []
    for path in paths:
        items.extend(json.loads(path.read_text(encoding="utf-8")))
    return sorted(items, key=lambda item: item["case"])


def dump(path: Path, data) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def fixate(work: Path) -> int:
    for sub in ("inputs", "outputs", "logs", "feedback"):
        (RUN / sub).mkdir(parents=True, exist_ok=True)
    shutil.copyfile(work / "r1/mapping.json", RUN / "inputs/mapping.json")
    for arm in ARMS:
        shutil.copyfile(work / f"r1/exec/prompt-{arm}.md", RUN / f"inputs/prompt-{arm}.md")
    for name in ("executor-instruction", "judge-instruction"):
        (RUN / f"logs/{name}.md").write_text(FRONTMATTER + (work / f"{name}.txt").read_text(encoding="utf-8"), encoding="utf-8")
    for rep in REPLICATES:
        rdir = work / rep
        out = RUN / f"outputs/{rep}"
        out.mkdir(exist_ok=True)
        for arm in ARMS:
            dump(out / f"executor-{arm}.json", merged(sorted((rdir / "out").glob(f"{arm}-batch*.json"))))
        dump(out / "judge-scores.json", merged(sorted((rdir / "judge").glob("out-batch*.json"))))
        shutil.copyfile(rdir / "judge-key.json", out / "judge-key.json")
        shutil.copyfile(rdir / "metrics.json", out / "metrics.json")
    shutil.copyfile(work / "summary.json", RUN / "outputs/summary.json")
    print(f"fixated into {RUN.relative_to(ROOT)}")
    return 0


def main() -> int:
    command, work = sys.argv[1], Path(sys.argv[2]).resolve()
    return {"texts": cmd_texts, "prepare": prepare, "judge": judge, "score": score, "fixate": fixate}[command](work)


if __name__ == "__main__":
    raise SystemExit(main())
