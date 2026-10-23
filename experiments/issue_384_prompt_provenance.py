#!/usr/bin/env python3
"""Issue #384: which prompts/ files the BA templates of RUN-0073..RUN-0077 came from.

Read-only. For every incident with origin ``prompt`` (a defect of the BA's
template prompt) in ``runs/2026/RUN-007[3-7]/outputs/incident-register.md``,
takes the model/template quote and searches it verbatim (whitespace and
Markdown emphasis normalized) in every ``prompts/**/*.md`` body.

Usage:
    python3 experiments/issue_384_prompt_provenance.py          # JSON summary
    python3 experiments/issue_384_prompt_provenance.py --print  # table

Writes ``experiments/issue_384/prompt-provenance.json``.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS = [f"RUN-{n:04d}" for n in range(73, 78)]
OUT = ROOT / "experiments" / "issue_384" / "prompt-provenance.json"
MODEL_DRAFTED: dict[str, int] = {}
QUOTE = re.compile(r"«(.+?)»(?!»)")


def norm(text: str) -> str:
    text = text.replace("**", "").replace("`", "")
    text = re.sub(r"[.…]+$", "", text.strip())
    return re.sub(r"\s+", " ", text).strip().lower()


def body(path: Path) -> str:
    lines = path.read_text(encoding="utf-8").splitlines()
    if lines and lines[0] == "---":
        end = lines.index("---", 1)
        lines = lines[end + 1:]
    return norm("\n".join(lines))


def incidents(run: str):
    path = ROOT / "runs" / "2026" / run / "outputs" / "incident-register.md"
    if not path.exists():
        return
    header = None
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.startswith("| "):
            header = None if not line.strip() else header
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells and cells[0] == "ID":
            header = cells
            continue
        if header is None or not re.fullmatch(r"I-\d{3}", cells[0]):
            continue
        row = dict(zip(header, cells))
        if row.get("Раздел") == "prompt" and row.get("Происх.") != "prompt":
            # Defect inside a prompt the model itself drafted in the dialog
            # (RUN-0076 sessions 9..16), not inside the BA's template.
            MODEL_DRAFTED[run] = MODEL_DRAFTED.get(run, 0) + 1
        if row.get("Происх.") != "prompt":
            continue
        quote_cell = row.get("Цитата модели") or row.get("Цитата") or ""
        quotes = QUOTE.findall(quote_cell)
        yield {
            "run": run,
            "id": cells[0],
            "line": lineno,
            "category": row.get("Кат."),
            "detection": row.get("Обнаружение"),
            "quote": quotes[0] if quotes else quote_cell,
            "ba_quote": row.get("Цитата БА / основание", "")[:300],
        }


def main() -> int:
    prompts = {
        str(p.relative_to(ROOT)): body(p)
        for p in sorted((ROOT / "prompts").rglob("*.md"))
    }
    rows = []
    for run in RUNS:
        for inc in incidents(run):
            needle = norm(inc["quote"])
            inc["matches"] = [
                name for name, text in prompts.items() if len(needle) >= 12 and needle in text
            ]
            rows.append(inc)
    by_prompt: dict[str, list[str]] = {}
    for inc in rows:
        for name in inc["matches"]:
            by_prompt.setdefault(name, []).append(f'{inc["run"]} {inc["id"]}')
    summary = {
        "prompt_incidents": len(rows),
        "matched_incidents": sum(1 for r in rows if r["matches"]),
        "by_run": {
            run: {
                "prompt_incidents": sum(1 for r in rows if r["run"] == run),
                "matched": sum(1 for r in rows if r["run"] == run and r["matches"]),
            }
            for run in RUNS
        },
        "model_drafted_prompt_rows": MODEL_DRAFTED,
        "by_prompt": by_prompt,
        "incidents": rows,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if "--print" in sys.argv:
        for r in rows:
            print(f'{r["run"]} {r["id"]} L{r["line"]} {r["category"]} | {",".join(r["matches"]) or "—"} | «{r["quote"][:90]}»')
        print(json.dumps({k: v for k, v in summary.items() if k != "incidents"}, ensure_ascii=False, indent=2))
    else:
        print(json.dumps({k: v for k, v in summary.items() if k != "incidents"}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
