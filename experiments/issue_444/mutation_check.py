#!/usr/bin/env python3
"""НФТ-5 (issue #444): порча реестра, черновика, промпта или флага делает валидаторы красными.

Каждая мутация применяется к рабочему дереву, затем запускается валидатор,
затем файл восстанавливается из исходных байт. Запуск: из корня репозитория,
на чистом дереве; RUNTIME_CLONE необязателен.
"""
import os, pathlib, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
SHA = "f31dcde33f0bc120244128faab98fc0162e45701"
MUTATIONS = [
    ("реестр: SHA раздела 1 → срез BL-163", "standards/bcreq-runtime-references.md",
     lambda t: t.replace(SHA, "2db0ef5106883b01b096fe8c4af50334899e9fe0", 1), "scripts/validate_issue_430_runtime_refs.py"),
    ("черновик Ш-2: удалено звено М-4", "prompts/drafts/bcreq-products-impact-analysis-stepwise.md",
     lambda t: t.replace("М-4", "М-X"), "scripts/validate_issue_438_step_prompts.py"),
    ("промпт Ш-В v0.1: ссылка по SHA → main", "prompts/bcreq-review-validation-oneshot.md",
     lambda t: t.replace(f"blob/{SHA}/", "blob/main/", 1), "scripts/validate_issue_430_runtime_refs.py"),
    ("флаг TYPING_APPLIED = True без нового прогона", "scripts/validate_issue_438_step_prompts.py",
     lambda t: t.replace("\nTYPING_APPLIED = False\n", "\nTYPING_APPLIED = True\n", 1), "scripts/validate_issue_438_step_prompts.py"),
    ("RFC-RT-001: ссылка раздела 13 на срез BL-163", "docs/rfc/2026-11-runtime-product-catalog-golden-set.md",
     lambda t: t.replace(f"mango-products.yaml`](https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/{SHA}/",
                         "mango-products.yaml`](https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/2db0ef5106883b01b096fe8c4af50334899e9fe0/", 1),
     "scripts/validate_issue_434_runtime_tasks.py"),
    ("бэклог: BL-165 удалена из BACKLOG.md", "pr-ops/BACKLOG.md",
     lambda t: "\n".join(l for l in t.split("\n") if not l.startswith("| BL-165 ")), "scripts/validate_issue_418_backlog.py"),
]
bad = 0
for name, rel, mutate, validator in MUTATIONS:
    path = ROOT / rel
    orig = path.read_bytes()
    text = orig.decode()
    new = mutate(text)
    if new == text:
        print(f"SKIP  {name}: мутация не изменила файл"); bad += 1; continue
    try:
        path.write_text(new)
        rc = subprocess.run([sys.executable, validator], cwd=ROOT, capture_output=True, env=os.environ).returncode
    finally:
        path.write_bytes(orig)
    ok = rc != 0
    bad += not ok
    print(f"{'OK  ' if ok else 'MISS'}  {name}: {validator} rc={rc}")
print(f"# итог: {len(MUTATIONS) - bad}/{len(MUTATIONS)} мутаций пойманы")
sys.exit(1 if bad else 0)
