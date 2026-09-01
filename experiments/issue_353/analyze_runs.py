#!/usr/bin/env python3
"""Build the reproducible RUN-0065/RUN-0066 comparison sample for issue #353.

RUN-0066 is the issue-mandated reference.  RUN-0065 is read from the historical
commit named by the issue, rather than from its later corrected working-tree
artifact.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[2]
OLD_COMMIT = "acb6c7bc"
OLD_PATH = "runs/2026/RUN-0065/outputs/L0-customer-form-with-assessment.md"
NEW_PATH = ROOT / "runs/2026/RUN-0066/outputs/L0-feasibility-assessment-1099-2.md"
TARGET_SECTIONS = {"4.5.3.4", "4.5.11.2.2", "4.5.19", "4.6.3.5", "5"}
LINK = re.compile(r"\[([^\[\]]+)\]\(([^()\s]+)\)")
CITATION = re.compile(
    r"^(?P<doc>[^,]+),\s*§(?P<section>[^,\s«]+)"
    r"(?:\s+«(?P<title>.*)»)?"
    r"(?:,\s*с\.(?P<pages>.+))?$"
)


@dataclass(frozen=True)
class Citation:
    section: str
    pages: str
    fact_section: str
    fact_pages: str
    page_delta: int | None


def frontmatter(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        return {}
    result: dict[str, str] = {}
    for line in lines[1:]:
        if line == "---":
            break
        if ":" not in line or line.startswith((" ", "-")):
            continue
        key, _, value = line.partition(":")
        result[key.strip()] = value.strip().strip("\"'")
    return result


def parse_pages(value: str) -> tuple[int, int] | None:
    numbers = [int(item) for item in re.findall(r"\d+", value)]
    if not numbers:
        return None
    return numbers[0], numbers[-1]


def page_delta(cited: str, fact: str) -> int | None:
    cited_range, fact_range = parse_pages(cited), parse_pages(fact)
    if cited_range is None or fact_range is None:
        return None
    return max(abs(cited_range[0] - fact_range[0]), abs(cited_range[1] - fact_range[1]))


def citations(cell: str, report_dir: Path) -> list[Citation]:
    result: list[Citation] = []
    for label, href in LINK.findall(cell):
        match = CITATION.match(label.strip())
        if not match:
            continue
        target = (report_dir / unquote(href)).resolve()
        try:
            target.relative_to((ROOT / "kb/processed").resolve())
        except ValueError:
            continue
        if "sections" not in target.parts or not target.is_file():
            continue
        meta = frontmatter(target)
        fact_section = meta.get("pdf_section", "") or meta.get("section", "")
        if fact_section in {"0", "-", "—"}:
            fact_section = ""
        pages = match.group("pages") or ""
        fact_pages = meta.get("pages", "")
        result.append(
            Citation(
                match.group("section"),
                pages,
                fact_section,
                fact_pages,
                page_delta(pages, fact_pages),
            )
        )
    return result


def split_rows(text: str) -> list[list[str]]:
    table = [
        [cell.strip() for cell in re.split(r"(?<!\\)\|", line.strip().strip("|"))]
        for line in text.splitlines()
        if line.startswith("|")
    ]
    return table[2:]


def normalized(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("<br>", " ")).strip().lower()


def verdict(value: str) -> str:
    return re.sub(r"[*._]", "", value).strip()


def citation_summary(items: list[Citation], *, fact: bool = False) -> str:
    values = []
    for item in items:
        section = item.fact_section if fact else item.section
        pages = item.fact_pages if fact else item.pages
        value = f"§{section or '—'}"
        if pages:
            value += f"@{pages.replace('–', '-').replace('—', '-')}"
        if value not in values:
            values.append(value)
    return "; ".join(values) or "—"


def page_state(items: list[Citation]) -> tuple[bool, bool]:
    """Return (accurate within two pages, hallucinated by more than two)."""
    if not items or any(item.page_delta is None for item in items):
        return False, False
    return all(item.page_delta <= 2 for item in items), any(item.page_delta > 2 for item in items)


def load_old() -> str:
    return subprocess.run(
        ["git", "show", f"{OLD_COMMIT}:{OLD_PATH}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout


def build_sample() -> tuple[list[dict[str, object]], dict[str, dict[str, float | int]]]:
    old_rows = {
        normalized(row[0]): row
        for row in split_rows(load_old())
        if len(row) == 6
    }
    new_rows = {
        normalized(row[1]): row
        for row in split_rows(NEW_PATH.read_text(encoding="utf-8"))
        if len(row) == 6 and row[0].isdigit()
    }
    old_report_dir = ROOT / Path(OLD_PATH).parent
    sample: list[dict[str, object]] = []

    for key, new_row in new_rows.items():
        old_row = old_rows.get(key)
        if old_row is None:
            continue
        old_cites = citations(old_row[4], old_report_dir)
        new_cites = citations(new_row[4], NEW_PATH.parent)
        covered = TARGET_SECTIONS.intersection(
            {cite.section for cite in old_cites + new_cites}
        )
        if not covered:
            continue
        old_page_ok, old_hallucinated = page_state(old_cites)
        new_page_ok, new_hallucinated = page_state(new_cites)
        old_pairs = {(cite.fact_section, cite.fact_pages) for cite in old_cites}
        new_pairs = {(cite.fact_section, cite.fact_pages) for cite in new_cites}
        old_verdict, new_verdict = verdict(old_row[3]), verdict(new_row[3])
        old_atomic = bool(
            old_verdict == new_verdict
            and old_page_ok
            and old_pairs
            and old_pairs.intersection(new_pairs)
        )
        sample.append(
            {
                "number": int(new_row[0]),
                "requirement": re.sub(r"\s+", " ", new_row[1].replace("<br>", " ")).strip(),
                "covered_sections": sorted(covered),
                "old_verdict": old_verdict or "пусто",
                "new_verdict": new_verdict or "пусто",
                "fact_verdict": new_verdict or "пусто",
                "old_citations": citation_summary(old_cites),
                "new_citations": citation_summary(new_cites),
                "fact_citations": citation_summary(new_cites, fact=True),
                "old_page_ok": old_page_ok,
                "new_page_ok": new_page_ok,
                "old_page_eligible": bool(old_cites),
                "new_page_eligible": bool(new_cites),
                "old_hallucinated": old_hallucinated,
                "new_hallucinated": new_hallucinated,
                "old_decomposition": "атомарно" if old_atomic else "грубо",
                "new_decomposition": "атомарно",
            }
        )

    if len(sample) < 50 or TARGET_SECTIONS != set().union(
        *(set(row["covered_sections"]) for row in sample)
    ):
        raise RuntimeError("representative sample is too small or misses a target section")

    def metrics(prefix: str) -> dict[str, float | int]:
        total = len(sample)
        verdict_hits = sum(row[f"{prefix}_verdict"] == row["fact_verdict"] for row in sample)
        page_eligible = sum(bool(row[f"{prefix}_page_eligible"]) for row in sample)
        page_hits = sum(bool(row[f"{prefix}_page_ok"]) for row in sample)
        hallucinations = sum(bool(row[f"{prefix}_hallucinated"]) for row in sample)
        atomic = sum(row[f"{prefix}_decomposition"] == "атомарно" for row in sample)
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

    return sample, {"RUN-0065": metrics("old"), "RUN-0066": metrics("new")}


def markdown(sample: list[dict[str, object]]) -> str:
    lines = [
        "| № | Требование (сокращено) | RUN-0065: вердикт; §@стр. | RUN-0066: вердикт; §@стр. | Факт: вердикт; §@стр. | Декомпозиция 65/66 |",
        "| ---: | --- | --- | --- | --- | --- |",
    ]
    for row in sample:
        requirement = str(row["requirement"])
        if len(requirement) > 90:
            requirement = requirement[:87].rstrip() + "…"
        cells = (
            str(row["number"]),
            requirement.replace("|", "\\|"),
            f'{row["old_verdict"]}; {row["old_citations"]}',
            f'{row["new_verdict"]}; {row["new_citations"]}',
            f'{row["fact_verdict"]}; {row["fact_citations"]}',
            f'{row["old_decomposition"]}/{row["new_decomposition"]}',
        )
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", type=Path, help="write sample and metrics as JSON")
    parser.add_argument("--markdown", type=Path, help="write the report table as Markdown")
    args = parser.parse_args()
    sample, metrics = build_sample()
    payload = {"method": "RUN-0066 is the issue-mandated reference", "metrics": metrics, "rows": sample}
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.markdown:
        args.markdown.parent.mkdir(parents=True, exist_ok=True)
        args.markdown.write_text(markdown(sample), encoding="utf-8")
    if not args.json and not args.markdown:
        print(json.dumps(metrics, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
