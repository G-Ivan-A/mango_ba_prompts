#!/usr/bin/env python3
"""Regression checks for issue #349 corrective rewrite."""

from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
RUN62 = ROOT / "runs/2026/RUN-0062/outputs/L0-customer-form-with-assessment.md"
RUN65 = ROOT / "runs/2026/RUN-0065/outputs/L0-customer-form-with-assessment.md"
REPORT = ROOT / "docs/report/2026-09-01-kb-assessment-error-analysis.md"


def split_row(line: str) -> list[str]:
    return [part.strip() for part in re.split(r"(?<!\\)\|", line.strip().strip("|"))]


def require(text: str, markers: tuple[str, ...], label: str, errors: list[str]) -> None:
    for marker in markers:
        if marker not in text:
            errors.append(f"{label} missing marker: {marker}")


def validate_run65(text: str, errors: list[str]) -> None:
    lines = [line for line in text.splitlines() if line.startswith("|")]
    widths = {len(split_row(line)) for line in lines}
    if widths != {6}:
        errors.append(f"RUN-0065 table widths must be {{6}}, got {widths}")
    rows = [split_row(line) for line in lines[2:]]
    if len(rows) != 409:
        errors.append(f"RUN-0065 must contain 409 source rows, got {len(rows)}")
    verdicts: set[str] = set()
    for row in rows:
        if len(row) != 6:
            continue
        verdict = re.match(r"^\*\*(Да|Частично|Нет)\.\*\*", row[3])
        if row[3] and not verdict:
            errors.append(f"RUN-0065 invalid verdict near requirement {row[0][:40]}: {row[3][:80]}")
        if verdict:
            verdicts.add(verdict.group(1))
        if row[3] and not re.search(r"\[[^]]+, §[^]]+, с\.[^]]+\]\([^)]+\)", row[4]):
            errors.append(f"RUN-0065 lacks atomic [file, §, page] citation near requirement {row[0][:40]}")
        if len(row[5]) < 30:
            errors.append(f"RUN-0065 critic audit is not technical near requirement {row[0][:40]}")
    if not {"Да", "Частично", "Нет"}.issubset(verdicts):
        errors.append(f"RUN-0065 must exercise strict verdict scale, got {sorted(verdicts)}")
    for forbidden in ("Реализовано", "Доработка", "Не оценивается", "Нет данных", "Уверенность", "Фокус human review"):
        if forbidden in text:
            errors.append(f"RUN-0065 contains retired contract token: {forbidden}")


def validate_run62(text: str, errors: list[str]) -> None:
    require(text, ("LK_manual_v-123", "полной БЗ", "kb/processed/README.md"), "RUN-0062", errors)
    no_data = [line for line in text.splitlines() if line.startswith("|") and "Нет данных" in line]
    for line in no_data:
        if "Проверено: БЗ" not in line or "web" not in line or "mango-office.ru" not in line:
            errors.append("RUN-0062 has a non-escalated ‘Нет данных’ verdict")
            break


def validate_lk_reference_truth(texts: dict[str, str], errors: list[str]) -> None:
    """Pin reviewed LK section/page pairs, not merely their citation syntax."""
    expected = {
        "RUN-0062": ("§4.5.3.4", "с.209–213"),
        "RUN-0065": ("§4.5.3.4", "с.209–213"),
        "report": ("§4.5.3.4", "с.209–213", "§4.5.11.2.2", "с.339–345"),
    }
    stale = ("с.226–231", "§4.5.11.8", "с.348–354")
    for label, needles in expected.items():
        require(texts[label], needles, f"{label} reviewed LK references", errors)
        for needle in stale:
            if needle in texts[label]:
                errors.append(f"{label} contains stale LK reference: {needle}")


def main() -> int:
    errors: list[str] = []
    texts = {}
    for label, path in (("RUN-0062", RUN62), ("RUN-0065", RUN65), ("report", REPORT)):
        if not path.is_file():
            errors.append(f"missing {path.relative_to(ROOT)}")
            texts[label] = ""
        else:
            texts[label] = path.read_text(encoding="utf-8")
    validate_run62(texts["RUN-0062"], errors)
    validate_run65(texts["RUN-0065"], errors)
    validate_lk_reference_truth(texts, errors)
    require(
        texts["report"],
        ("RUN-0062", "RUN-0065", "kb/processed/README.md", "доверенным доменам", "ни БЗ, ни web", "Корневые причины", "Ресимуляция"),
        "report",
        errors,
    )
    if errors:
        print("FAIL: issue #349 validation")
        print("\n".join(f"- {error}" for error in errors[:30]))
        return 1
    print("OK: issue #349 — corrective report and both in-place artifacts satisfy the new contract")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
