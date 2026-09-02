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


def run_case(
    citation: str, section_text: str = SECTION
) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        report = root / "reports/result.md"
        section = root / "kb/processed/mango-lk-manual/sections/138-nastroyki.md"
        report.parent.mkdir(parents=True)
        section.parent.mkdir(parents=True)
        report.write_text(f"Evidence: {citation}\n", encoding="utf-8")
        section.write_text(section_text, encoding="utf-8")
        return subprocess.run(
            [sys.executable, str(VALIDATOR), "--root", str(root), str(report)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )


def run_nested_title_case() -> subprocess.CompletedProcess[str]:
    nested_section = SECTION.replace(
        'title: "Настройки"', 'title: "Настройка виджета «Карусель»"'
    )
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        report = root / "reports/result.md"
        section = root / "kb/processed/mango-lk-manual/sections/138-nastroyki.md"
        report.parent.mkdir(parents=True)
        section.parent.mkdir(parents=True)
        report.write_text(
            "Evidence: "
            "[LK_manual_v-123, §4.5.3.4 «Настройка виджета «Карусель»», с.209–213]"
            "(../kb/processed/mango-lk-manual/sections/138-nastroyki.md)\n",
            encoding="utf-8",
        )
        section.write_text(nested_section, encoding="utf-8")
        return subprocess.run(
            [sys.executable, str(VALIDATOR), "--root", str(root), str(report)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )


def run_discovery_case(*, invalid_future: bool = False) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        section = root / "kb/processed/mango-lk-manual/sections/138-nastroyki.md"
        section.parent.mkdir(parents=True)
        section.write_text(SECTION, encoding="utf-8")
        target = "../../../../kb/processed/mango-lk-manual/sections/138-nastroyki.md"
        for run, citation in (
            (65, f"[broken]({target})"),
            (66, f"[LK_manual_v-123, §4.5.3.4 «Настройки», с.209–213]({target})"),
            (
                67,
                f"[LK_manual_v-123, §4.5.3.4 «Настройки», "
                f"с.{'226–231' if invalid_future else '209–213'}]({target})",
            ),
        ):
            report = root / f"runs/2026/RUN-{run:04d}/outputs/result.md"
            report.parent.mkdir(parents=True)
            report.write_text(f"Evidence: {citation}\n", encoding="utf-8")
        return subprocess.run(
            [sys.executable, str(VALIDATOR), "--root", str(root)],
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

    omitted = run_case(f"[LK_manual_v-123, §4.5.3.4]({target})")
    omitted_output = omitted.stdout + omitted.stderr
    if omitted.returncode == 0 or "pages omitted" not in omitted_output:
        errors.append(f"available pages could be silently omitted: {omitted_output}")

    pageless = run_case(
        f"[LK_manual_v-123, §4.5.3.4]({target})",
        SECTION.replace('pages: "209-213"\n', ""),
    )
    if pageless.returncode != 0:
        errors.append(f"page-less verified fallback rejected: {pageless.stderr or pageless.stdout}")

    untitled = run_case(f"[LK_manual_v-123, §4.5.3.4, с.209–213]({target})")
    untitled_output = untitled.stdout + untitled.stderr
    if untitled.returncode == 0 or "title is required" not in untitled_output:
        errors.append(f"page-bearing citation without title accepted: {untitled_output}")

    malformed = run_case(f"[Evidence for section]({target})")
    malformed_output = malformed.stdout + malformed.stderr
    if (
        malformed.returncode == 0
        or "invalid atomic citation label" not in malformed_output
    ):
        errors.append(f"malformed local KB citation ignored: {malformed_output}")

    wrong_document = run_case(
        f"[WRONG, §4.5.3.4 «Настройки», с.209–213]({target})"
    )
    if wrong_document.returncode == 0 or "frontmatter aliases" not in (
        wrong_document.stdout + wrong_document.stderr
    ):
        errors.append("document mismatch was not rejected")

    wrong_section = run_case(
        f"[LK_manual_v-123, §4.5.3.5 «Настройки», с.209–213]({target})"
    )
    if wrong_section.returncode == 0 or "frontmatter '4.5.3.4'" not in (
        wrong_section.stdout + wrong_section.stderr
    ):
        errors.append("section mismatch was not rejected")

    missing = run_case(
        "[LK_manual_v-123, §4.5.3.4 «Настройки», с.209–213]"
        "(../kb/processed/mango-lk-manual/sections/missing.md)"
    )
    if missing.returncode == 0 or "missing citation target" not in (
        missing.stdout + missing.stderr
    ):
        errors.append("missing citation target was not rejected")

    nested = run_nested_title_case()
    if nested.returncode != 0:
        errors.append(f"nested guillemet title rejected: {nested.stderr or nested.stdout}")

    sectionless = run_case(
        f"[LK_manual_v-123, «Настройки», с.209–213]({target})",
        SECTION.replace('pdf_section: "4.5.3.4"', 'pdf_section: "-"')
        .replace("# 4.5.3.4. Настройки", "# Настройки"),
    )
    if sectionless.returncode != 0:
        errors.append(
            "document without a numbered section rejected: "
            f"{sectionless.stderr or sectionless.stdout}"
        )

    discovered = run_discovery_case()
    if discovered.returncode != 0 or "2 citation(s)" not in discovered.stdout:
        errors.append(
            "default discovery did not gate RUN-0066+ while excluding RUN-0065: "
            f"{discovered.stderr or discovered.stdout}"
        )

    invalid_future = run_discovery_case(invalid_future=True)
    future_output = invalid_future.stdout + invalid_future.stderr
    if (
        invalid_future.returncode == 0
        or "RUN-0067" not in future_output
        or "226-231" not in future_output
    ):
        errors.append(f"shifted citation in future RUN-0067 was not rejected: {future_output}")

    if errors:
        print("FAIL: test_validate_pagination_shift")
        for error in errors:
            print(f"  - {error.strip()}")
        return 1

    print("OK: pagination validator accepts truth, rejects shifts, and permits page-less fallback")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
