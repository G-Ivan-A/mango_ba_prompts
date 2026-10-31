#!/usr/bin/env python3
"""RUN-0079: подготовка A/B-прогона golden set этапа 1 (issue #411).

A — промпт проверки до блока уроков (версия 0.1, коммит до реестра уроков).
B — тот же промпт с блоком «Уроки прогонов» (версия 0.2, текущий HEAD).

Кейсы обезличиваются: ID кейса golden set заменяется на T-NN в случайном
порядке (seed 79), чтобы номер кейса не подсказывал номер урока. Эталонные
вердикты исполнителю не передаются. Карта T-NN → case-id хранится в
outputs прогона и исполнителю не передаётся.

Использование:
    python3 experiments/issue_411/run0079/prepare.py WORKDIR
"""
from __future__ import annotations

import importlib.util
import json
import random
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PROMPT = "prompts/bcreq-review-validation-oneshot.md"
BASE_A = "2b6820a4~1"
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


def main() -> int:
    work = Path(sys.argv[1]).resolve()
    (work / "exec").mkdir(parents=True, exist_ok=True)
    (work / "out").mkdir(parents=True, exist_ok=True)
    validator = load_validator()
    cases = validator.golden_cases()
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

    prompt_a = git("show", f"{BASE_A}:{PROMPT}")
    prompt_b = (ROOT / PROMPT).read_text(encoding="utf-8")
    (work / "exec/prompt-A.md").write_text(prompt_a, encoding="utf-8")
    (work / "exec/prompt-B.md").write_text(prompt_b, encoding="utf-8")

    size = (len(anonymized) + BATCHES - 1) // BATCHES
    for batch in range(BATCHES):
        chunk = anonymized[batch * size:(batch + 1) * size]
        lines = [f"# Фрагменты на проверку, пакет {batch + 1}", ""]
        for item in chunk:
            lines += [f"## {item['case']}", "", f"**Вход:** {item['input']}", "", f"**Контекст:** {item['context']}", ""]
        (work / f"exec/cases-batch{batch + 1}.md").write_text("\n".join(lines), encoding="utf-8")

    meta = {
        "seed": SEED,
        "prompt": PROMPT,
        "prompt_A": {"ref": git("rev-parse", BASE_A).strip(), "version": "0.1"},
        "prompt_B": {"ref": git("rev-parse", "HEAD").strip(), "version": "0.2"},
        "batches": BATCHES,
        "cases": len(cases),
        "mapping": mapping,
    }
    (work / "mapping.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in meta.items() if k != "mapping"}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
