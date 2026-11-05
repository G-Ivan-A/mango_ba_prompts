#!/usr/bin/env python3
"""Мутации: каждая должна ронять валидатор issue #450; файл восстанавливается."""
import subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
M = [("prompts/bcreq-review-validation-oneshot.md", "version: 0.3", "version: 0.2"),
     ("prompts/bcreq-fr-documentation-stepwise.md", "### Отраслевая практика — на решение БА", "### Практика"),
     ("prompts/bcreq-constitution-governance-oneshot.md", "АД-12", "АД-99"),
     ("runs/2026/RUN-0087/outputs/summary.json", '"guardrail_R18": []', '"guardrail_R18": ["S1"]'),
     ("runs/2026/RUN-0086/outputs/shv-check/r1.json", '"defect":false', '"defect":true'),
     ("runs/2026/RUN-0086/logs/experiment-log.md", "загрязнённая подача", "подача"),
     ("runs/2026/RUN-0085/metadata.yaml", "ba_reviewed: false", "ba_reviewed: true"),
     ("pr-ops/BACKLOG.md", "BL-156г — `review` (PR #451)", "BL-156г — `TODO`"),
     ("docs/rfc/2026-11-runtime-product-catalog-golden-set.md", "Пробел Р-1 раздела 14.2 снят", "Р-1 открыт"),
     ("site/index.html", "v2.4.0", "v2.3.0")]
bad = 0
for path, a, b in M:
    f = ROOT / path; src = f.read_text(encoding="utf-8")
    assert a in src, (path, a)
    f.write_text(src.replace(a, b, 1), encoding="utf-8")
    try:
        rc = subprocess.run([sys.executable, str(ROOT / "scripts/validate_issue_450_bl156g_167_168.py")], capture_output=True).returncode
    finally:
        f.write_text(src, encoding="utf-8")
    print("caught" if rc else "MISSED", path, a[:30]); bad += not rc
print(f"мутаций: {len(M)}, пропущено: {bad}")
raise SystemExit(bad)
