#!/usr/bin/env python3
"""Replay three deterministic post-generation rules from commit acb6c7bc.

This does not replay the original LLM request: the complete system prompt and
model-call parameters are unavailable.  It executes the committed generator
code to reproduce rule propagation and precedence after generation.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = "acb6c7bc:experiments/issue_347/generate_run.py"
REQUIREMENTS = {
    "recording": "Система должна записывать и хранить голосовые записи взаимодействия в стерео-формате.",
    "avito": (
        'В системе должна быть возможность настройки интеграции с каналом "Авито Работа". '
        "Система должна позволять автоматически получать данные соискателей и информацию о "
        "вакансиях из канала \"Авито Работа\", автоматически вносить полученные данные в "
        "карточку контакта системы, вести переписку с кандидатами на вакансии в едином окне, "
        "просматривать статистику по обращениям с канала \"Авито Работа\" в отчетах системы."
    ),
    "carousel": (
        "- карусель номеров, которые будут использоваться при обзвоне "
        "(каждый номер может использоваться в неограниченном кол-ве кампаний)"
    ),
}


def main() -> int:
    source = subprocess.run(
        ["git", "show", SOURCE], cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout
    namespace = {"__file__": str(ROOT / "experiments/issue_347/generate_run.py"), "__name__": "replay"}
    exec(compile(source, SOURCE, "exec"), namespace)
    assess = namespace["assess"]
    result = {}
    for name, requirement in REQUIREMENTS.items():
        verdict, evidence, audit = assess(requirement)
        result[name] = {"verdict": verdict, "evidence": evidence, "audit": audit}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
