#!/usr/bin/env python3
"""RUN-0082: замер Ш-В с повторами для BL-156б и Р-03 (issue #446).

Пред-регистрация (до запуска подагентов, правило — в
`experiments/issue_446/run0082/preregistration.md`):

- версии — ровно те, что измерил RUN-0081 (SHA-256 сверяются):
  A1 — `prompts/bcreq-review-validation-oneshot.md` v0.1 с 15 подстановками
  типа гейта (`experiments/issue_438/prompt-typing.json`), ссылки по SHA;
  D  — черновик «по тесту» Ш-В на типизированном v0.1 (коммит `36799e9e`);
- N = 3 независимых повтора r1…r3: в каждом свежие исполнители (A1×2, D×2
  пакета) и свежие слепые судьи (2 пакета) с собственным seed маскировки
  X/Y (8082, 8083, 8084);
- кейсы и раскладка T-NN — те же 62 кейса RUN-0079 (seed 79, 2 пакета);
- решение — по медиане трёх повторов, поэлементно: сданные кейсы, ядро,
  ложные дефекты; правило DEC-427-11 («не хуже» RUN-0079: 49/62, 10/11,
  0/10) применяется к медианам. RUN-0081 — справочный четвёртый замер, в
  решение не входит.

Использование:
    python3 experiments/issue_446/run0082/run.py prepare WORK
    python3 experiments/issue_446/run0082/run.py judge   WORK
    python3 experiments/issue_446/run0082/run.py score   WORK
    python3 experiments/issue_446/run0082/run.py fixate  WORK

WORK — корень, внутри которого `r1/`, `r2/`, `r3/` (как `/tmp/run81` RUN-0081).
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import statistics
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RUN81 = ROOT / "experiments/issue_444/run0081"
RUN = ROOT / "runs/2026/RUN-0082"
REPLICATES = ("r1", "r2", "r3")
SEEDS = {"r1": 8082, "r2": 8083, "r3": 8084}
PROMPT_A = "prompts/bcreq-review-validation-oneshot.md"
PROMPT_D = "prompts/drafts/bcreq-review-validation-oneshot.md"
#: Коммит, на котором RUN-0081 измерил D на типизированном v0.1.
D_COMMIT = "36799e9ebc7c538f8829d04870ac48da28042d4a"
SHA_A = "adf826634b2e8190da4d0f4ef307a59104a6f8fa3da6ef5a48a3c923ada90581"
SHA_D = "2e8391723f365fa34be3ad9012547fe6db7e379dadae9d787c65ecead046d990"
BASELINE = {"passed": 49, "core": 10, "negatives_false_positive": 0}
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


def prompts() -> dict[str, str]:
    typing = load("bl156a", ROOT / "experiments/issue_444/bl156a_prompt_changes.py")
    # С issue #448 опубликован v0.2 (RUN-0084): A1 = откат v0.2 к v0.1 + тип гейта.
    v01 = typing.SHV_V02.revert(PROMPT_A, (ROOT / PROMPT_A).read_text(encoding="utf-8"))
    a = typing.apply_typing(PROMPT_A, v01)
    d = git("show", f"{D_COMMIT}:{PROMPT_D}")
    assert sha256(a) == SHA_A, ("A1 не совпал с RUN-0081", sha256(a))
    assert sha256(d) == SHA_D, ("D не совпал с RUN-0081", sha256(d))
    return {"A": a, "D": d}


def prepare(work: Path) -> int:
    prep = load("prepare81", RUN81 / "prepare.py")
    texts = prompts()
    head = git("rev-parse", "HEAD").strip()
    for rep in REPLICATES:
        rdir = work / rep
        # prepare.py RUN-0081 пишет кейсы, раскладку (сверка с RUN-0079) и промпты
        # из рабочего дерева; промпты затем заменяются измеренными версиями.
        sys.argv = ["prepare.py", str(rdir)]
        if prep.main() != 0:
            return 1
        meta = json.loads((rdir / "mapping.json").read_text(encoding="utf-8"))
        for label, text in texts.items():
            (rdir / f"exec/prompt-{label}.md").write_text(text, encoding="utf-8")
        meta["replicate"] = rep
        meta["judge_seed"] = SEEDS[rep]
        meta["prompt_A"] = {"path": PROMPT_A, "ref": head, "version": "0.1 + тип гейта (prompt-typing.json), ссылки по SHA", "bytes": len(texts["A"].encode()), "sha256": sha256(texts["A"])}
        meta["prompt_D"] = {"path": PROMPT_D, "ref": D_COMMIT, "version": "0.1-by-test (реестр 0.4, на типизированном v0.1)", "bytes": len(texts["D"].encode()), "sha256": sha256(texts["D"])}
        (rdir / "mapping.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("prepared", " ".join(REPLICATES), "A", SHA_A[:8], "D", SHA_D[:8])
    return 0


def judge(work: Path) -> int:
    jp = load("judge81", RUN81 / "judge_prepare.py")
    status = 0
    for rep in REPLICATES:
        jp.SEED = SEEDS[rep]
        sys.argv = ["judge_prepare.py", str(work / rep)]
        print(rep, end=" ")
        status |= jp.main()
    return status


def median(values: list[int]) -> int:
    return int(statistics.median(values))


def score(work: Path) -> int:
    sc = load("score81", RUN81 / "score.py")
    ratio = sc.ratio
    per = {}
    for rep in REPLICATES:
        sys.argv = ["score.py", str(work / rep)]
        print(f"== {rep}")
        sc.main()
        per[rep] = json.loads((work / rep / "metrics.json").read_text(encoding="utf-8"))
    summary: dict = {"replicates": {}, "median": {}, "decision": {}}
    for version in ("A", "D"):
        rows = {rep: {"passed": per[rep][version]["passed"], "core": ratio(per[rep][version]["core"])[0],
                      "negatives_false_positive": ratio(per[rep][version]["negatives_false_positive"])[0],
                      "failed": [f["case"] for f in per[rep][version]["failed"]]} for rep in REPLICATES}
        summary["replicates"][version] = rows
        med = {k: median([rows[r][k] for r in REPLICATES]) for k in BASELINE}
        summary["median"][version] = med
        checks = {"passed": med["passed"] >= BASELINE["passed"], "core": med["core"] >= BASELINE["core"],
                  "negatives_false_positive": med["negatives_false_positive"] <= BASELINE["negatives_false_positive"]}
        summary["decision"][f"{version}_vs_RUN_0079"] = {"checks": checks, "not_worse": all(checks.values())}
        fails: dict[str, int] = {}
        for rep in REPLICATES:
            for case in rows[rep]["failed"]:
                fails[case] = fails.get(case, 0) + 1
        summary.setdefault("fail_frequency", {})[version] = dict(sorted(fails.items(), key=lambda kv: (-kv[1], kv[0])))
    mA, mD = summary["median"]["A"], summary["median"]["D"]
    d_vs_a = {"passed": mD["passed"] >= mA["passed"], "core": mD["core"] >= mA["core"],
              "negatives_false_positive": mD["negatives_false_positive"] <= mA["negatives_false_positive"]}
    summary["decision"]["D_vs_A_median"] = {"checks": d_vs_a, "not_worse": all(d_vs_a.values())}
    summary["decision"]["publish_typing"] = summary["decision"]["A_vs_RUN_0079"]["not_worse"]
    summary["decision"]["publish_draft"] = summary["decision"]["D_vs_RUN_0079"]["not_worse"] and summary["decision"]["D_vs_A_median"]["not_worse"]
    summary["baseline_RUN_0079_A"] = BASELINE
    run81 = json.loads((ROOT / "runs/2026/RUN-0081/outputs/metrics.json").read_text(encoding="utf-8"))
    summary["reference_RUN_0081"] = {v: {"passed": run81[v]["passed"], "core": run81[v]["core"], "negatives_false_positive": run81[v]["negatives_false_positive"]} for v in ("A", "D")}
    (work / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("== median", json.dumps(summary["median"], ensure_ascii=False))
    print("== decision", json.dumps(summary["decision"], ensure_ascii=False))
    print("== fail_frequency", json.dumps(summary["fail_frequency"], ensure_ascii=False))
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
    for name in ("executor-instruction", "judge-instruction"):
        (RUN / f"logs/{name}.md").write_text(FRONTMATTER + (work / f"{name}.txt").read_text(encoding="utf-8"), encoding="utf-8")
    for rep in REPLICATES:
        rdir = work / rep
        out = RUN / f"outputs/{rep}"
        out.mkdir(exist_ok=True)
        for version in ("A", "D"):
            dump(out / f"executor-{version}.json", merged(sorted((rdir / "out").glob(f"{version}-batch*.json"))))
        dump(out / "judge-scores.json", merged(sorted((rdir / "judge").glob("out-batch*.json"))))
        shutil.copyfile(rdir / "judge-key.json", out / "judge-key.json")
        shutil.copyfile(rdir / "metrics.json", out / "metrics.json")
    shutil.copyfile(work / "summary.json", RUN / "outputs/summary.json")
    print(f"fixated into {RUN.relative_to(ROOT)}")
    return 0


def main() -> int:
    command, work = sys.argv[1], Path(sys.argv[2]).resolve()
    return {"prepare": prepare, "judge": judge, "score": score, "fixate": fixate}[command](work)


if __name__ == "__main__":
    raise SystemExit(main())
