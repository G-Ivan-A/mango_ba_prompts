#!/usr/bin/env python3
"""Regression checks for the issue #353 A/B RCA and citation contract."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from validate_pagination_shift import validate_report


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "docs/report/2026-09-01-run-0065-vs-0066-ab-rca.md"
DATA = ROOT / "docs/report/data/2026-09-01-run-0065-vs-0066-sample.json"
EVIDENCE = ROOT / "docs/report/evidence/2026-09-01-run-0065-acb6c7bc-redacted.txt"
MANIFEST = ROOT / "docs/report/evidence/README.md"
CONTRACT = ROOT / "docs/contracts/kb-citations.md"
RUN66 = ROOT / "runs/2026/RUN-0066/outputs/L0-feasibility-assessment-1099-2.md"
TARGET_SECTIONS = {"4.5.3.4", "4.5.11.2.2", "4.5.19", "4.6.3.5", "5"}
EVIDENCE_SHA256 = "01b45bb234c19b6ffb21e8c1e05428c15c272d7ed86981b919d3a61dac5147e1"
EXPECTED_METRICS = {
    "RUN-0065": {
        "rows": 65,
        "accuracy_verdict_count": 31,
        "accuracy_verdict_percent": 47.7,
        "accuracy_page_count": 17,
        "accuracy_page_eligible_rows": 45,
        "accuracy_page_percent": 37.8,
        "hallucination_count": 28,
        "hallucination_rate_percent": 43.1,
        "atomic_decomposition_count": 4,
        "decomposition_quality_percent": 6.2,
    },
    "RUN-0066": {
        "rows": 65,
        "accuracy_verdict_count": 65,
        "accuracy_verdict_percent": 100.0,
        "accuracy_page_count": 64,
        "accuracy_page_eligible_rows": 64,
        "accuracy_page_percent": 100.0,
        "hallucination_count": 0,
        "hallucination_rate_percent": 0.0,
        "atomic_decomposition_count": 65,
        "decomposition_quality_percent": 100.0,
    },
}


def required(text: str, markers: tuple[str, ...], label: str, errors: list[str]) -> None:
    for marker in markers:
        if marker not in text:
            errors.append(f"{label} missing marker: {marker}")


def calculate_metrics(rows: list[dict[str, object]], prefix: str) -> dict[str, float | int]:
    total = len(rows)
    verdict_hits = sum(row[f"{prefix}_verdict"] == row["fact_verdict"] for row in rows)
    page_eligible = sum(bool(row[f"{prefix}_page_eligible"]) for row in rows)
    page_hits = sum(bool(row[f"{prefix}_page_ok"]) for row in rows)
    hallucinations = sum(bool(row[f"{prefix}_hallucinated"]) for row in rows)
    atomic = sum(row[f"{prefix}_decomposition"] == "атомарно" for row in rows)
    return {
        "rows": total,
        "accuracy_verdict_count": verdict_hits,
        "accuracy_verdict_percent": round(100 * verdict_hits / total, 1),
        "accuracy_page_count": page_hits,
        "accuracy_page_eligible_rows": page_eligible,
        "accuracy_page_percent": round(100 * page_hits / page_eligible, 1),
        "hallucination_count": hallucinations,
        "hallucination_rate_percent": round(100 * hallucinations / total, 1),
        "atomic_decomposition_count": atomic,
        "decomposition_quality_percent": round(100 * atomic / total, 1),
    }


def main() -> int:
    errors: list[str] = []
    paths = (REPORT, DATA, EVIDENCE, MANIFEST, CONTRACT, RUN66)
    for path in paths:
        if not path.is_file():
            errors.append(f"missing {path.relative_to(ROOT)}")
    if errors:
        print("FAIL: issue #353 validation")
        print("\n".join(f"- {error}" for error in errors))
        return 1

    report = REPORT.read_text(encoding="utf-8")
    contract = CONTRACT.read_text(encoding="utf-8")
    manifest = MANIFEST.read_text(encoding="utf-8")
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    rows = payload.get("rows", [])
    metrics = payload.get("metrics", {})

    if len(rows) != 65:
        errors.append(f"comparison sample must contain 65 rows, got {len(rows)}")
    numbers = [row.get("number") for row in rows]
    if len(numbers) != len(set(numbers)):
        errors.append("comparison sample contains duplicate requirement numbers")
    covered = set().union(*(set(row.get("covered_sections", [])) for row in rows))
    if not TARGET_SECTIONS.issubset(covered):
        errors.append(f"comparison sample misses target sections: {sorted(TARGET_SECTIONS - covered)}")

    recalculated = {
        "RUN-0065": calculate_metrics(rows, "old"),
        "RUN-0066": calculate_metrics(rows, "new"),
    }
    if metrics != recalculated:
        errors.append("stored metrics do not match the row-level sample")
    if metrics != EXPECTED_METRICS:
        errors.append(f"issue acceptance metrics changed: {metrics!r}")

    start = "<!-- issue-353-sample-start -->"
    end = "<!-- issue-353-sample-end -->"
    if start in report and end in report:
        table = report.split(start, 1)[1].split(end, 1)[0]
        table_rows = [line for line in table.splitlines() if line.startswith("| ")][2:]
        if len(table_rows) != len(rows):
            errors.append(f"report table has {len(table_rows)} data rows, expected {len(rows)}")
    else:
        errors.append("report lacks generated sample boundary markers")

    required(
        report,
        (
            "Accuracy_verdict",
            "Accuracy_page",
            "Hallucination_rate",
            "Decomposition_quality",
            "chain-of-thought не публикуется",
            "| H1 |",
            "| H2 |",
            "| H3 |",
            "| H4 |",
            "| H5 |",
            "circuit breaker",
            "Claude Opus 5 / workflow RUN-0066",
            "gpt-5.6-sol",
        ),
        "RCA report",
        errors,
    )
    required(
        contract,
        (
            "не более **12 000 входных токенов**",
            "непосредственно перед каждой эмиссией перечитай frontmatter",
            "[документ, §раздел](путь)",
            "python3 scripts/validate_pagination_shift.py <REPORT>",
        ),
        "citation contract",
        errors,
    )

    evidence_hash = hashlib.sha256(EVIDENCE.read_bytes()).hexdigest()
    if evidence_hash != EVIDENCE_SHA256:
        errors.append(f"redacted trace SHA-256 {evidence_hash}, expected {EVIDENCE_SHA256}")
    required(
        manifest,
        (
            "7c891fbe9c0265c1af81804ef7a01d8d",
            "26d64b219f42ae4b5b4cd53dcb6ae4955924f3dfb5627f6019fb862418af0674",
            EVIDENCE_SHA256,
            "experiments/issue_353/redact_trace.py",
        ),
        "evidence manifest",
        errors,
    )

    checked, citation_errors = validate_report(RUN66, ROOT)
    if checked < 700:
        errors.append(f"RUN-0066 citation gate checked only {checked} citations")
    errors.extend(citation_errors)

    if errors:
        print(f"FAIL: issue #353 validation: {len(errors)} problem(s)")
        print("\n".join(f"- {error}" for error in errors[:40]))
        return 1
    print(
        "OK: issue #353 — 65-row RCA, metrics, evidence, contract, and "
        f"{checked} RUN-0066 citations verified"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
