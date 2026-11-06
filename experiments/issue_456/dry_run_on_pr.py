#!/usr/bin/env python3
"""Срез А поверх головы другого PR: пересечение файлов, данные сайта, валидаторы до и после.
Список кандидатов строится по ветке issue-456 (текущий каталог), прогон идёт в одноразовой копии.
Запуск: python3 experiments/issue_456/dry_run_on_pr.py <worktree> <файлы PR #451> <чтения генератора> <файлы PR #455> <выход: список среза>"""
import hashlib, json, pathlib, re, subprocess, sys
wt, pr451, reads, pr455, out = sys.argv[1:6]; wt = pathlib.Path(wt)
lines = lambda p: set(open(p).read().split("\n"))
excl = lines(pr451) | lines(reads) | lines(pr455)
chain = re.compile(r"^(docs/roadmap|docs/rfc/2026-11|docs/ba-processes/|docs/analysis/2026-11|docs/site-access)")
FM = re.compile(r"---\n.*?\n---\n", re.S); AI = re.compile(r"^ai-generated:.*\n", re.M)
def has_ai(p):
    m = FM.match(p.read_text(encoding="utf-8")); return bool(m and AI.search(m.group(0)))
ls = subprocess.run(["git", "ls-files", "docs", "pr-ops", "patterns", "kb"], capture_output=True, text=True).stdout.split("\n")
files = [f for f in ls if f.endswith(".md") and has_ai(pathlib.Path(f)) and f not in excl and not chain.match(f)]
pathlib.Path(out).write_text("\n".join(files) + "\n")
print("файлов в срезе:", len(files), "| пересечение с PR #455:", len(set(files) & lines(pr455)))
def norm(o):
    if isinstance(o, dict): return {k: norm(v) for k, v in o.items() if k not in ("generatedAt", "generated_at")}
    return [norm(v) for v in o] if isinstance(o, list) else o
def site():
    subprocess.run(["node", "scripts/generate-pages-data.mjs"], cwd=wt, check=True, capture_output=True)
    h = {p.name: hashlib.sha256(json.dumps(norm(json.loads(p.read_text())), sort_keys=True).encode()).hexdigest()[:12] for p in sorted((wt / "site/data").glob("*.json"))}
    subprocess.run(["git", "checkout", "-q", "site/data"], cwd=wt, check=True); return h
def validate():
    r = subprocess.run(["python3", "scripts/validate_all.py", "--full", "--jobs", "2"], cwd=wt, capture_output=True, text=True)
    o = r.stdout + r.stderr
    return r.returncode, o.strip().splitlines()[-1], re.findall(r"^.*(?:FAIL|ПРОВАЛ).*$", o, re.M)[:15]
a = site(); print("до:", validate())
n = 0
for f in files:
    p = wt / f
    if not p.exists(): print("нет в голове PR:", f); continue
    t = p.read_text(encoding="utf-8"); m = FM.match(t)
    p.write_text(AI.sub("", m.group(0)) + t[m.end():], encoding="utf-8"); n += 1
print("изменено:", n); b = site()
print("данные сайта изменились:", [k for k in a if a[k] != b.get(k)]); print("после:", validate())
subprocess.run(["git", "checkout", "-q", "."], cwd=wt, check=True)
