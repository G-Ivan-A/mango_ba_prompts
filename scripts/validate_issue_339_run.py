#!/usr/bin/env python3
"""Regression checks for issue #339 / RUN-0062.

The customer-owned columns are compared with the attached BIFF workbooks, not
with another generated artifact.  This makes accidental transcription edits,
row loss and column drift visible in the normal repository validation suite.
"""

from __future__ import annotations

import hashlib
import pathlib
import re
import sys

try:
    import xlrd
except ImportError:  # validate_all runs in a dependency-free CI environment
    print("SKIP: xlrd is required for the issue #339 source-cell audit")
    raise SystemExit(0)


ROOT = pathlib.Path(__file__).resolve().parents[1]
REPORT = ROOT / "runs/2026/RUN-0062/outputs/L0-customer-form-with-assessment.md"
SOURCES = (
    ("appendix-5-telephony.xls", 23, "a717f3f48fc526324cb0bb28f1a9810c6e9b3ba38c586f0d5e26492467984b20"),
    ("appendix-6-quality-control.xls", 17, "8a109fefcdd4dcfdf91d971ecaf102c3f35f97f8dcaa8266d9952d8f87871177"),
    ("appendix-7-nfr.xls", 47, "df27860bdee74555a23cbab6571dbc8ab9c028e4fa28c7049dc454383e57c7e0"),
)
DOWNLOADS = ROOT / "experiments/issue_339/downloads"


def displayed(book: xlrd.book.Book, sheet: xlrd.sheet.Sheet, row: int, col: int) -> str:
    cell = sheet.cell(row, col)
    if cell.ctype == xlrd.XL_CELL_NUMBER:
        if col == 1:
            return f"{cell.value:.1f}"
        if float(cell.value).is_integer():
            return str(int(cell.value))
    return str(cell.value)


def source_rows() -> list[tuple[str, str, str]]:
    rows: list[tuple[str, str, str]] = []
    for filename, expected_count, expected_sha in SOURCES:
        path = DOWNLOADS / filename
        data = path.read_bytes()
        assert hashlib.sha256(data).hexdigest() == expected_sha, filename
        book = xlrd.open_workbook(str(path), formatting_info=True)
        sheet = book.sheet_by_index(0)
        header = next(r for r in range(sheet.nrows) if displayed(book, sheet, r, 1).strip() == "№")
        actual = []
        for row in range(header + 1, sheet.nrows):
            values = tuple(displayed(book, sheet, row, col) for col in (1, 2, 3))
            if any(values):
                actual.append(values)
        assert len(actual) == expected_count, (filename, len(actual))
        rows.extend(actual)
    return rows


def markdown_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\r\n", "\n").replace("\r", "\n").replace("\n", "<br>")


def split_row(line: str) -> list[str]:
    return [part.strip() for part in re.split(r"(?<!\\)\|", line.strip().strip("|"))]


def main() -> int:
    errors: list[str] = []
    if not REPORT.exists():
        print(f"FAIL: missing {REPORT.relative_to(ROOT)}")
        return 1

    text = REPORT.read_text(encoding="utf-8")
    table_lines = [line for line in text.splitlines() if line.startswith("|")]
    widths = {len(split_row(line)) for line in table_lines}
    if widths != {6}:
        errors.append(f"table widths must be {{6}}, got {widths}")

    rendered = []
    for line in table_lines:
        cells = split_row(line)
        if cells[0] in {"№", "---"}:
            continue
        rendered.append(tuple(cells[:3]))
        for assessment in cells[3:]:
            if not re.match(r"^\*\*(Да(?:, частично)?|Нет|Нет данных|Не оценивается)\.", assessment):
                errors.append(f"invalid verdict: {assessment[:80]}")
            if not assessment.startswith("**Нет данных.") and not assessment.startswith("**Не оценивается."):
                links = re.findall(r"\[[^]]+\]\(([^)]+)\)", assessment)
                if not links or any(link.rstrip("/").endswith("kb/processed") for link in links):
                    errors.append(f"assessment lacks a direct SSOT link: {assessment[:80]}")

    expected = [tuple(markdown_cell(cell).strip() for cell in row) for row in source_rows()]
    if rendered != expected:
        errors.append(f"source columns differ: expected {len(expected)} rows, got {len(rendered)}")
        for index, (want, got) in enumerate(zip(expected, rendered), 1):
            if want != got:
                errors.append(f"first mismatch at row {index}: {want!r} != {got!r}")
                break

    documentation_rows = [
        split_row(line)
        for line in table_lines
        if "Руководство пользователя по использованию ППО" in line
        or "Документация к API системы" in line
        or "программы очного обучения" in line
    ]
    if len(documentation_rows) != 3:
        errors.append(f"expected 3 NFR documentation rows, got {len(documentation_rows)}")
    elif any("HTTP-запрос" in row[5] or "SOAP/REST/gRPC" in row[5] for row in documentation_rows):
        errors.append("duplicate NFR identifiers leaked integration assessments into documentation rows")

    required = {
        "runs/2026/RUN-0062/metadata.yaml",
        "runs/2026/RUN-0062/inputs/README.md",
        "runs/2026/RUN-0062/outputs/README.md",
        "runs/2026/RUN-0062/logs/experiment-log.md",
        "runs/2026/RUN-0062/feedback/review-notes.md",
    }
    for relpath in required:
        if not (ROOT / relpath).exists():
            errors.append(f"missing {relpath}")
    for relpath in ("runs/README.md", "CHANGELOG.md"):
        if "RUN-0062" not in (ROOT / relpath).read_text(encoding="utf-8"):
            errors.append(f"{relpath} does not register RUN-0062")

    if errors:
        print("FAIL: issue #339 validation")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print(f"OK: issue #339 — {len(rendered)} source rows, six columns, source cells exact")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
