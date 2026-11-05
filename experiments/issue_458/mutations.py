#!/usr/bin/env python3
"""Мутации: каждая должна ронять валидатор issue #458; файл восстанавливается."""
import subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
RFC = "docs/rfc/2026-11-bcreq-machine-run-baseline.md"
M = [("runs/2026/RUN-0090/metadata.yaml", "verdict: partial-success", "verdict: success"),
     ("runs/2026/RUN-0091/metadata.yaml", "ba_reviewed: false", "ba_reviewed: true"),
     ("runs/2026/RUN-0091/metadata.yaml", "  passed: 8", "  passed: 9"),
     ("runs/2026/RUN-0090/outputs/judge-scores.json", '"verdict": "fail"', '"verdict": "pass"'),
     ("runs/2026/RUN-0091/outputs/check.json", '"pass": true', '"pass": false'),
     ("runs/2026/RUN-0090/logs/gate-journal.md", "| Г-IN | гибрид | pending |", "| Г-IN | гибрид | approved |"),
     ("runs/2026/RUN-0091/logs/gate-journal.md", "| Г-IN | `гибрид` | `pending` |", "| Г-IN | `гибрид` | `approved` |"),
     ("runs/2026/RUN-0090/outputs/release-readiness.md", "Готово к выпуску человеком: нет", "Готово к выпуску человеком: да"),
     ("runs/2026/RUN-0091/outputs/release-readiness.md", "ready_for_human_release | **нет**", "ready_for_human_release | **да**"),
     ("runs/2026/RUN-0091/outputs/bcreq.md", "BCREQ-1137", "BCREQ-1135"),
     ("runs/README.md", "[`RUN-0091`](2026/RUN-0091/metadata.yaml)", "[`RUN-0091`](2026/RUN-0091/x.yaml)"),
     ("prompts/bcreq-review-validation-oneshot.md", "version: 0.3", "version: 0.31"),
     ("experiments/issue_458/preregistration.md", "**недоступен**", "доступен"),
     (RFC, "status: proposed", "status: accepted"),
     (RFC, "**не читая** RUN-0090", "RUN-0090"),
     ("docs/rfc/rfc-register.md", "[PR #459](https://github.com/G-Ivan-A/mango_ba_prompts/pull/459) |", "x |"),
     ("pr-ops/BACKLOG.md", "BL-156г — `DONE` (PR #451 слит", "BL-156г — `review` (PR #451"),
     ("pr-ops/BACKLOG.md", "BL-157г — `review` ([PR #459]", "BL-157г — `DONE` ([PR #459]"),
     ("pr-ops/BACKLOG.md", "| P1 | BL-157г | TODO |", "| P1 | BL-157г | DONE |"),
     ("pr-ops/BACKLOG.md", "машинный прогон её не закрывает", "закрыта"),
     ("pr-ops/backlog-ba-model.md", "**Статус.** `review` (PR #459).", "**Статус.** `DONE`."),
     ("docs/rfc/2026-11-runtime-product-catalog-golden-set.md", "(2026-11-bcreq-machine-run-baseline.md)", "(x.md)")]
bad = 0
for path, a, b in M:
    f = ROOT / path; src = f.read_text(encoding="utf-8")
    assert a in src, (path, a)
    f.write_text(src.replace(a, b, 1), encoding="utf-8")
    try:
        rc = subprocess.run([sys.executable, str(ROOT / "scripts/validate_issue_458_machine_runs.py")], capture_output=True).returncode
    finally:
        f.write_text(src, encoding="utf-8")
    print("caught" if rc else "MISSED", path, a[:30]); bad += not rc
print(f"мутаций: {len(M)}, пропущено: {bad}")
raise SystemExit(bad)
