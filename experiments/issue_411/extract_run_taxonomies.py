#!/usr/bin/env python3
"""Extract run-local defect taxonomies (code -> name, total, confirmed) from
runs/**/outputs/error-statistics.md and RUN-0064 reports/error-analysis.md.

Issue #411 finding: every statistics run defines its own C-code list, so the
same code means different defects in different runs (RUN-0075 C01 is
"выдуманная функция", RUN-0074 C01 is "архитектура в ФТ"). The output is the
raw input for standards/bcreq-lessons/lessons.json `run_taxonomies`.

Usage: python3 experiments/issue_411/extract_run_taxonomies.py > experiments/issue_411/run_taxonomies.json
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def parse_stats(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    sec = text.split("## 2. По категориям", 1)[1].split("\n## ", 1)[0]
    header = None
    out = []
    for line in sec.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells[0] == "Код":
            header = cells
            continue
        if not re.fullmatch(r"C\d{2}", cells[0]) or header is None:
            continue
        row = dict(zip(header, cells))
        def num(key):
            v = row.get(key, "")
            return int(v) if v.isdigit() else 0
        out.append({
            "code": cells[0],
            "name": cells[1],
            "total": num("Всего"),
            "confirmed": num("confirmed"),
            "plausible": num("plausible"),
        })
    return out


def parse_run0064(path: Path) -> list[dict]:
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\| (ERR-\d{2}) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \|$", line)
        if m:
            out.append({"code": m.group(1), "name": m.group(2)[:160], "category": m.group(3),
                        "total": 1, "confirmed": 1, "plausible": 0, "rule": m.group(5)})
    return out


def main() -> int:
    data = {}
    for p in sorted(ROOT.glob("runs/*/RUN-*/outputs/error-statistics.md")):
        data[p.parts[-3]] = {"source": str(p.relative_to(ROOT)), "categories": parse_stats(p)}
    p = ROOT / "runs/2026/RUN-0064/reports/error-analysis.md"
    data["RUN-0064"] = {"source": str(p.relative_to(ROOT)), "categories": parse_run0064(p)}
    json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
