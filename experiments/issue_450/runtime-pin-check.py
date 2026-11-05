#!/usr/bin/env python3
"""Сверка среза runtime перед закреплением (РТ-7, issue #450).

Запуск: python3 experiments/issue_450/runtime-pin-check.py <клон runtime>
Клон уже на новом SHA; разница с прежним срезом берётся из GitHub compare.
"""
import json, pathlib, re, subprocess, sys

rt = pathlib.Path(sys.argv[1]); OLD = "f31dcde33f0bc120244128faab98fc0162e45701"
sha = subprocess.check_output(["git", "-C", rt, "rev-parse", "HEAD"], text=True).strip()
reg = pathlib.Path("standards/bcreq-runtime-references.md").read_text()
paths = sorted(set(re.findall(rf"blob/{sha}/([^)#\s]+)", reg)))
missing = [p for p in paths if not (rt / p).exists()]
docs = json.loads((rt / "docs/kb/MAP.json").read_text())["documents"]
no_toc = [d.get("id") for d in docs if not d.get("sections_toc") or not (rt / "docs/kb" / d["sections_toc"]).exists() and not (rt / d["sections_toc"]).exists()]
print("sha", sha); print("пути реестра", len(paths), "нет", missing)
print("документов", len(docs), "без оглавления", no_toc)
changed = subprocess.check_output(["gh", "api", f"repos/G-Ivan-A/mango-ba-ai-runtime/compare/{OLD}...{sha}", "--jq", ".files[].filename"], text=True).split()
tops = {}
for c in changed:
    k = "/".join(c.split("/")[:2]); tops[k] = tops.get(k, 0) + 1
print("изменено с прежнего среза", len(changed), tops)
sys.exit(1 if missing or no_toc else 0)
