#!/usr/bin/env python3
"""Issue #384: read-only metadata scan of prompts/ for the audit report.

Collects, for every file under prompts/: frontmatter fields, line count,
top-level headings (prompt skeleton), naming parse (domain/operation/mode per
standards/prompt-standard.md), presence of output-format section, inbound
references from the process map / README / site, and run evidence (RUN-XXXX
directories that mention the file). Writes experiments/issue_384/inventory.json.

Usage: python3 experiments/issue_384_prompts_inventory.py [--print]
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROMPTS = ROOT / "prompts"
OUT = ROOT / "experiments" / "issue_384" / "inventory.json"
MODES = ("stepwise", "oneshot", "legacy", "executable")
# Text markers of the construction patterns discussed in the report (§3). A flag
# is a lexical hit, not a verdict: the report cites the exact lines.
FLAGS = {
    "role_methodology": r"CBAP|TM Forum|eTOM|ODA|Frameworx|ITIL|сертифицированн|\(cisco\)",
    "old_section_model": r"Раздел[а-я]* [47]|[Уу]ровень 4\.x|\b[47]\.x\b|2\.3\. Задачи|цель, задачи",
    "ban_system_must": r"[Зз]апрет на формулировки «Система должна»|Никаких «Система должна»",
    "self_certification": r"✅|Отчет валидации|Dev Readiness|Контекст валиден|готов к (передаче|формированию)",
    "creative_generation": r"[Кк]реативн|[Мм]айнинг|предложи 1-2 новых термина",
    "english_labels": r"Job Story|Normalized Terms|INVEST|Happy path|Acceptance Criteria",
    "no_invention_rule": r"[Нн]е выдумывай|НЕ придумывай|Не придумывай|Не определено|ТРЕБУЕТСЯ УТОЧНЕНИЕ|Требует проверки",
    "stop_gates": r"СТОП|\(Жди ответа\)|Жди подтверждения",
    "status_field": r"ready \| draft \| needs-clarification",
}
TAXONOMY_OPS = [
    "ingestion", "understanding", "modeling", "documentation", "solution-design",
    "validation", "quality", "risk-analysis", "governance", "release-readiness",
    "reverse-requirements", "impact-analysis", "research",
]


def frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).splitlines():
        mm = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if mm:
            fm[mm.group(1)] = mm.group(2).strip().strip('"')
    return fm


def parse_name(stem):
    parts = stem.split("-")
    mode = parts[-1] if parts[-1] in MODES else None
    rest = parts[:-1] if mode else parts
    op = None
    for k in (2, 1):
        cand = "-".join(rest[-k:]) if len(rest) >= k else None
        if cand in TAXONOMY_OPS:
            op = cand
            rest = rest[:-k]
            break
    return {"domain": "-".join(rest) or None, "operation": op, "mode": mode}


def headings(text):
    body = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.S)
    out, fence = [], False
    for line in body.splitlines():
        if line.startswith("```"):
            fence = not fence
            continue
        m = re.match(r"^(#{1,2})\s+(.*)$", line)
        if m and not fence:
            out.append(m.group(1) + " " + m.group(2).strip())
    return out


def grep_refs(name, paths):
    try:
        res = subprocess.run(
            ["git", "grep", "-l", "-F", name, "--", *paths],
            cwd=ROOT, capture_output=True, text=True, check=False,
        )
    except FileNotFoundError:
        return []
    return sorted(set(res.stdout.split()))


def main():
    rows = []
    for f in sorted(PROMPTS.rglob("*")):
        if not f.is_file():
            continue
        rel = f.relative_to(ROOT).as_posix()
        text = f.read_text(encoding="utf-8")
        fm = frontmatter(text)
        hs = headings(text)
        # README.md is not a unique name: search README files by repo path only.
        needle = rel if f.name.startswith("README") else f.name
        run_refs = grep_refs(needle, ["runs"])
        run_ids = sorted({m.group(0) for p in run_refs for m in [re.search(r"RUN-\d{4}", p)] if m})
        rows.append({
            "path": rel,
            "lines": text.count("\n") + (0 if text.endswith("\n") else 1),
            "archive": "/archive/" in rel,
            "name": parse_name(f.stem),
            "frontmatter": fm,
            "fm_keys": sorted(fm),
            "headings": hs,
            "has_output_format": any(re.search(r"ФОРМАТ (ВЫВОДА|ОТВЕТА)|OUTPUT FORMAT", h, re.I) for h in hs)
                                 or bool(re.search(r"ФОРМАТ (ВЫВОДА|ОТВЕТА)", text)),
            "mentions_bcreq": len(re.findall(r"BCREQ", text)),
            "mentions_section4": bool(re.search(r"раздел[а-я]* 4|Раздел 4", text)),
            "process_map": bool(grep_refs(needle, ["docs/ba-processes/00-index.md"])),
            "readme": bool(grep_refs(needle, ["prompts/README.md"])),
            "site": bool(grep_refs(needle, ["site"])),
            "run_ids": run_ids,
            "flags": sorted(k for k, rx in FLAGS.items() if re.search(rx, text)),
        })
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if "--print" in sys.argv:
        for r in rows:
            fm = r["frontmatter"]
            print(f'{r["path"]:<60} {r["lines"]:>4} st={fm.get("status","-"):<9} v={fm.get("version","-"):<4} '
                  f'upd={fm.get("updated","-"):<10} out={int(r["has_output_format"])} map={int(r["process_map"])} '
                  f'readme={int(r["readme"])} site={int(r["site"])} bcreq={r["mentions_bcreq"]} runs={",".join(r["run_ids"]) or "-"} flags={",".join(r["flags"])}')
    print(f"{len(rows)} files -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
