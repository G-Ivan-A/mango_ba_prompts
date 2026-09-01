#!/usr/bin/env python3
"""Behavior tests for the generic KB citation pagination validator."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts/validate_pagination_shift.py"

SECTION = """---
doc_code: LK
pdf_section: "4.5.3.4"
title: "Настройки"
pages: "209-213"
source: kb/sources/mango-lk-manual/LK_manual_v-123.pdf
---
# 4.5.3.4. Настройки
"""


def run_case(citation: str) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        report = root / "reports/result.md"
        section = root / "kb/processed/mango-lk-manual/sections/138-nastroyki.md"
        report.parent.mkdir(parents=True)
        section.parent.mkdir(parents=True)
        report.write_text(f"Evidence: {citation}\n", encoding="utf-8")
        section.write_text(SECTION, encoding="utf-8")
        return subprocess.run(
            [sys.executable, str(VALIDATOR), "--root", str(root), str(report)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )


def main() -> int:
    errors: list[str] = []
    target = "../kb/processed/mango-lk-manual/sections/138-nastroyki.md"

    valid = run_case(
        f"[LK_manual_v-123, §4.5.3.4 «Настройки», с.209–213]({target})"
    )
    if valid.returncode != 0:
        errors.append(f"matching frontmatter rejected: {valid.stderr or valid.stdout}")

    shifted = run_case(
        f"[LK_manual_v-123, §4.5.3.4 «Настройки», с.226–231]({target})"
    )
    shifted_output = shifted.stdout + shifted.stderr
    if shifted.returncode == 0 or "226-231" not in shifted_output or "209-213" not in shifted_output:
        errors.append(f"shifted pages were not diagnosed: {shifted_output}")

    pageless = run_case(f"[LK_manual_v-123, §4.5.3.4]({target})")
    if pageless.returncode != 0:
        errors.append(f"page-less verified fallback rejected: {pageless.stderr or pageless.stdout}")

    if errors:
        print("FAIL: test_validate_pagination_shift")
        for error in errors:
            print(f"  - {error.strip()}")
        return 1

    print("OK: pagination validator accepts truth, rejects shifts, and permits page-less fallback")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
