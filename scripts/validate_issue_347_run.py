#!/usr/bin/env python3
"""Regression checks for issue #347 / RUN-0065."""

from __future__ import annotations

import hashlib
from pathlib import Path
import re
import xml.etree.ElementTree as ET
import zipfile


ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "runs/2026/RUN-0065"
SOURCE = ROOT / "experiments/issue_347/requirements.xlsx"
REPORT = RUN / "outputs/L0-customer-form-with-assessment.md"
EXPECTED_SHA256 = "4806288a13f03b4e972b726e92e267c4c627cab42ad4ade3929607c0fd4287ba"
NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"


def read(path: Path, errors: list[str]) -> str:
    if not path.is_file():
        errors.append(f"missing file: {path.relative_to(ROOT)}")
        return ""
    return path.read_text(encoding="utf-8")


def source_rows() -> list[tuple[str, str, str]]:
    data = SOURCE.read_bytes()
    assert hashlib.sha256(data).hexdigest() == EXPECTED_SHA256
    with zipfile.ZipFile(SOURCE) as book:
        strings_root = ET.fromstring(book.read("xl/sharedStrings.xml"))
        strings = ["".join(node.text or "" for node in item.iter(NS + "t")) for item in strings_root.findall(NS + "si")]
        sheet = ET.fromstring(book.read("xl/worksheets/sheet1.xml"))
        rows: list[tuple[str, str, str]] = []
        for row in sheet.findall(f".//{NS}sheetData/{NS}row"):
            cells: dict[str, str] = {}
            for cell in row.findall(NS + "c"):
                column = re.match(r"[A-Z]+", cell.attrib["r"])
                value_node = cell.find(NS + "v")
                value = "" if value_node is None else value_node.text or ""
                if cell.attrib.get("t") == "s" and value:
                    value = strings[int(value)]
                if column:
                    cells[column.group()] = value
            source = (cells.get("B", ""), cells.get("C", ""), cells.get("D", ""))
            if any(source):
                rows.append(source)
        return rows


def markdown_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\r\n", "\n").replace("\r", "\n").replace("\n", "<br>")


def split_row(line: str) -> list[str]:
    return [part.strip() for part in re.split(r"(?<!\\)\|", line.strip().strip("|"))]


def require_markers(text: str, markers: tuple[str, ...], label: str, errors: list[str]) -> None:
    for marker in markers:
        if marker not in text:
            errors.append(f"{label} missing marker: {marker}")


def main() -> int:
    errors: list[str] = []
    if not SOURCE.is_file():
        errors.append("missing source workbook")
    else:
        digest = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
        if digest != EXPECTED_SHA256:
            errors.append(f"source SHA-256 differs: {digest}")

    metadata = read(RUN / "metadata.yaml", errors)
    inputs = read(RUN / "inputs/README.md", errors)
    report = read(REPORT, errors)
    output_index = read(RUN / "outputs/README.md", errors)
    audit = read(RUN / "logs/technical-audit.md", errors)
    review = read(RUN / "feedback/review-notes.md", errors)
    registry = read(ROOT / "runs/README.md", errors)
    changelog = read(ROOT / "CHANGELOG.md", errors)

    require_markers(metadata, ("run_id: RUN-0065", "run_type: execution", "issues/347", "source_rows: 409", "worksheet_extent: 414"), "metadata", errors)
    require_markers(inputs, ("requirements.xlsx", EXPECTED_SHA256, "Требования к системе", "SLA поддержки", "Лист1", "hidden"), "input manifest", errors)
    require_markers(output_index, ("L0-customer-form-with-assessment.md", "409", "CBAP"), "output index", errors)
    require_markers(audit, ("CBAP", "трассируем", "Блок-фактор", "SLA", "human review"), "technical audit", errors)
    require_markers(review, ("Фокус human review", "Открытые решения", "Механизм проверки"), "review notes", errors)

    table_lines = [line for line in report.splitlines() if line.startswith("|")]
    widths = {len(split_row(line)) for line in table_lines}
    if widths != {8}:
        errors.append(f"table widths must be {{8}}, got {widths}")
    rendered: list[tuple[str, str, str, str]] = []
    verdicts: set[str] = set()
    for line in table_lines:
        cells = split_row(line)
        if len(cells) != 8 or cells[0] in {"Строка XLSX", "---"}:
            continue
        rendered.append(tuple(cells[:4]))
        verdict = re.match(r"^\*\*(Реализовано|Доработка|Реализация невозможна|Нет данных|Не оценивается)\.\*\*", cells[4])
        if not verdict:
            errors.append(f"invalid verdict at source row {cells[0]}: {cells[4][:80]}")
        else:
            verdicts.add(verdict.group(1))
        if cells[7] not in {"Да", "Нет"}:
            errors.append(f"invalid human-review flag at source row {cells[0]}: {cells[7]}")

    try:
        expected = [(str(index), *(markdown_cell(cell).strip() for cell in row)) for index, row in enumerate(source_rows(), 1)]
    except (AssertionError, KeyError, OSError, zipfile.BadZipFile) as exc:
        errors.append(f"cannot parse source workbook: {exc}")
        expected = []
    if rendered != expected:
        errors.append(f"source columns differ: expected {len(expected)} rows, got {len(rendered)}")
        for index, (want, got) in enumerate(zip(expected, rendered), 1):
            if want != got:
                errors.append(f"first mismatch at row {index}: {want!r} != {got!r}")
                break
    if len(rendered) != 409:
        errors.append(f"expected 409 source rows, got {len(rendered)}")
    if not {"Реализовано", "Доработка", "Нет данных", "Не оценивается"}.issubset(verdicts):
        errors.append(f"assessment must exercise controlled verdicts, got {sorted(verdicts)}")

    require_markers(report, ("CBAP", "Блок-фактор", "Уверенность", "Основание / технический комментарий", "Фокус human review"), "report", errors)
    if "RUN-0065" not in registry or "RUN-0065" not in changelog or "Issue #347" not in changelog:
        errors.append("RUN-0065 must be registered in runs/README.md and CHANGELOG.md")

    if errors:
        print("FAIL: issue #347 validation")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print("OK: issue #347 — 409 source rows, eight columns, source cells exact")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
