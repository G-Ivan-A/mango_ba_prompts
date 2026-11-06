#!/usr/bin/env python3
"""Пересечение кандидатов среза с PR #451/#453, файлами сайта и файлами цепочки #454.
Запуск: python3 experiments/issue_456/slice_overlap.py <список файлов PR #451> <чтения генератора> <лог frontmatter>"""
import collections, re, subprocess, sys
pr451 = set(open(sys.argv[1]).read().split("\n")); reads = set(open(sys.argv[2]).read().split("\n"))
ls = subprocess.run(["git", "ls-files", "docs", "pr-ops", "patterns", "kb"], capture_output=True, text=True).stdout.split("\n")
cand = []
for f in ls:
    if f.endswith(".md"):
        head = open(f, encoding="utf-8").read(1500)
        if head.startswith("---") and re.search(r"^ai-generated:", head.split("\n---")[0], re.M): cand.append(f)
chain = re.compile(r"^(pr-ops/(BACKLOG|backlog-)|docs/roadmap|docs/rfc/2026-11|docs/ba-processes/|docs/analysis/2026-11|docs/site-access)")
safe, ex = [], collections.defaultdict(list)
for f in cand:
    if f in pr451: ex["в PR #451"].append(f)
    elif f in reads: ex["читает генератор сайта"].append(f)
    elif chain.match(f): ex["файлы цепочки #454/бэклога"].append(f)
    else: safe.append(f)
print("кандидатов", len(cand), "безопасных", len(safe))
for k, v in ex.items(): print("исключено:", k, len(v), v)
print("по каталогам:", collections.Counter(f.split("/")[0] for f in safe))
errs = collections.Counter(); kinds = collections.defaultdict(collections.Counter)
for l in open(sys.argv[3], errors="ignore"):
    m = re.match(r"\./([^:]+):\d+: ERROR: (.*)", l)
    if m:
        d = m.group(1).split("/")[0]; errs[d] += 1
        kinds[d][re.sub(r":.*", "", m.group(2))] += 1
for d in ("patterns", "kb", "pr-ops", "docs"): print(d, errs[d], dict(kinds[d]))
