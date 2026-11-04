#!/usr/bin/env python3
"""RUN-0080: подготовка слепого сравнения промпта Ш-В «по тесту» с v0.1 (issue #438).

A — опубликованный промпт `prompts/bcreq-review-validation-oneshot.md`
    (версия 0.1; после BL-156 в нём только тип гейта в строке CB-0.5).
D — черновик «по тесту» `prompts/drafts/bcreq-review-validation-oneshot.md`
    (v0.1 + базовый стандарт + профили ANALYZE, VERIFY, TRANSFORM + контракты
    операций + ссылки И-N по SHA; собран `scripts/build_bcreq_step_prompts.py`).

Кейсы — те же 62 кейса golden set и та же обезличенная раскладка T-NN, что в
RUN-0079 (seed 79, 2 пакета по 31). Раскладка пересчитывается и сверяется с
`runs/2026/RUN-0079/inputs/mapping.json`: расхождение — ошибка.

Использование:
    python3 experiments/issue_438/run0080/prepare.py WORKDIR
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import random
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PROMPT_A = "prompts/bcreq-review-validation-oneshot.md"
PROMPT_D = "prompts/drafts/bcreq-review-validation-oneshot.md"
BASELINE = ROOT / "runs/2026/RUN-0079/inputs/mapping.json"
SEED = 79
BATCHES = 2


def load_validator():
    path = ROOT / "scripts/validate_issue_411_lessons_pipeline.py"
    spec = importlib.util.spec_from_file_location("v411", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=True).stdout


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main() -> int:
    work = Path(sys.argv[1]).resolve()
    (work / "exec").mkdir(parents=True, exist_ok=True)
    (work / "out").mkdir(parents=True, exist_ok=True)
    cases = load_validator().golden_cases()
    rng = random.Random(SEED)
    order = list(range(len(cases)))
    rng.shuffle(order)
    mapping = {}
    anonymized = []
    for number, index in enumerate(order, start=1):
        case = cases[index]
        tid = f"T-{number:02d}"
        mapping[tid] = case["case-id"]
        anonymized.append({"case": tid, "input": case["Вход"], "context": case["Контекст"]})
    baseline = json.loads(BASELINE.read_text(encoding="utf-8"))["mapping"]
    if mapping != baseline:
        print("раскладка T-NN не совпадает с RUN-0079", file=sys.stderr)
        return 1

    prompts = {"A": (ROOT / PROMPT_A).read_text(encoding="utf-8"), "D": (ROOT / PROMPT_D).read_text(encoding="utf-8")}
    for label, text in prompts.items():
        (work / f"exec/prompt-{label}.md").write_text(text, encoding="utf-8")

    size = (len(anonymized) + BATCHES - 1) // BATCHES
    for batch in range(BATCHES):
        chunk = anonymized[batch * size:(batch + 1) * size]
        lines = [f"# Фрагменты на проверку, пакет {batch + 1}", ""]
        for item in chunk:
            lines += [f"## {item['case']}", "", f"**Вход:** {item['input']}", "", f"**Контекст:** {item['context']}", ""]
        (work / f"exec/cases-batch{batch + 1}.md").write_text("\n".join(lines), encoding="utf-8")

    head = git("rev-parse", "HEAD").strip()
    meta = {
        "seed": SEED,
        "baseline_run": "RUN-0079",
        "prompt_A": {"path": PROMPT_A, "ref": head, "version": "0.1", "bytes": len(prompts["A"].encode("utf-8")), "sha256": sha256(prompts["A"])},
        "prompt_D": {"path": PROMPT_D, "ref": head, "version": "0.1-by-test", "bytes": len(prompts["D"].encode("utf-8")), "sha256": sha256(prompts["D"])},
        "batches": BATCHES,
        "cases": len(cases),
        "mapping": mapping,
    }
    (work / "mapping.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in meta.items() if k != "mapping"}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
