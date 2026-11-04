#!/usr/bin/env python3
"""Мутационная проверка валидатора #448 (BL-156б, BL-156в, BL-157в).

Каждая мутация меняет один файл, запускает валидатор и восстанавливает файл
байт в байт (в том числе при ошибке). rc=1 — мутация поймана.

Запуск: ``python3 experiments/issue_448/mutation.py > experiments/issue_448/mutation.log``
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = "scripts/validate_issue_448_bl156_bl157v.py"


def flip_judge(text: str) -> str:
    """r2: у первого кейса, где A2 сдан, судья ставит K3 = false."""
    key = json.loads((ROOT / "runs/2026/RUN-0084/outputs/r2/judge-key.json").read_text(encoding="utf-8"))
    items = json.loads(text)
    for item in items:
        label = next(lb for lb, arm in key[item["case"]].items() if arm == "A2")
        if all(v for k, v in item[label].items() if k != "note"):
            item[label]["K3"] = False
            break
    return json.dumps(items, ensure_ascii=False, indent=2) + "\n"


def publish_a1(text: str) -> str:
    return text.replace('"publish": "A2"', '"publish": "A1"', 1)


def prompt_extra(text: str) -> str:
    return text + "\n- Дополнительное правило вне замера.\n"


def analysis_number(text: str) -> str:
    return text.replace("**255 правок**", "**256 правок**", 1)


def coding_leak(text: str) -> str:
    items = json.loads(text)
    items[0]["summary"] = (items[0]["summary"] + " ivan@example.com")[:200]
    return json.dumps(items, ensure_ascii=False, indent=1) + "\n"


def coding_drop(text: str) -> str:
    items = json.loads(text)
    return json.dumps(items[1:], ensure_ascii=False, indent=1) + "\n"


def backlog_status(text: str) -> str:
    return text.replace("BL-156г — `TODO`", "BL-156г — `DONE`")


def card_status(text: str) -> str:
    head, tail = text.split("#### BL-156г.", 1)
    return head + "#### BL-156г." + tail.replace("**Статус.** `TODO`", "**Статус.** `DONE`", 1)


def copy_header(text: str) -> str:
    return text.replace("<!-- ${variant.id} · ${step.step} -->\\n\\n", "", 1)


def card_code(text: str) -> str:
    data = json.loads(text)
    data["steps"][3]["purpose"] += " (Ш-3)"
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n"


MUTATIONS = (
    ("M1", "RUN-0084 r2: судья провалил A2 по K3 на сданном кейсе", "runs/2026/RUN-0084/outputs/r2/judge-scores.json", flip_judge),
    ("M2", "summary.json: решение publish A1 вместо A2", "runs/2026/RUN-0084/outputs/summary.json", publish_a1),
    ("M3", "Ш-В v0.2 в prompts/ с правилом вне замера", "prompts/bcreq-review-validation-oneshot.md", prompt_extra),
    ("M4", "разбор BL-157в: 256 правок вместо 255", "docs/analysis/2026-11-04-bl-157v-chat-analysis.md", analysis_number),
    ("M5", "coding.json: e-mail в пересказе", "experiments/issue_448/bl157v/coding.json", coding_leak),
    ("M6", "coding.json: потеряна одна запись (свод не пересчитан)", "experiments/issue_448/bl157v/coding.json", coding_drop),
    ("M7", "BACKLOG: BL-156г `DONE` без замера", "pr-ops/BACKLOG.md", backlog_status),
    ("M8", "карточка BL-156г: `DONE` без замера", "pr-ops/backlog-ba-model.md", card_status),
    ("M9", "сайт: копия без имени промпта в первой строке", "site/app.js", copy_header),
    ("M10", "сайт: код шага в инструкции карточки", "site/data/test-kit.json", card_code),
)


def main() -> int:
    print("# Мутационная проверка валидатора 448 (issue #448), 2026-11-04")
    print("# Каждая мутация вносится в файл, файл восстанавливается после прогона. rc=1 — мутация поймана.")
    missed = 0
    for code, title, rel, mutate in MUTATIONS:
        path = ROOT / rel
        original = path.read_bytes()
        mutated = mutate(original.decode("utf-8"))
        assert mutated != original.decode("utf-8"), f"{code}: мутация не изменила файл"
        try:
            path.write_text(mutated, encoding="utf-8")
            proc = subprocess.run([sys.executable, VALIDATOR], cwd=ROOT, capture_output=True, text=True)
        finally:
            path.write_bytes(original)
        fails = " ".join(sorted(set(re.findall(r"(?m)^(?:FAIL|ERROR): (\w+)", proc.stderr))))
        missed += proc.returncode == 0
        print(f"{code} {title} | validator 448 rc={proc.returncode} | {fails}")
    print(f"# итог: поймано {len(MUTATIONS) - missed} из {len(MUTATIONS)}")
    return 1 if missed else 0


if __name__ == "__main__":
    raise SystemExit(main())
