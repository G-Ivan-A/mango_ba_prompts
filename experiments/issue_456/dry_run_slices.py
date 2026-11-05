#!/usr/bin/env python3
"""Сухой прогон среза техдолга в одноразовой копии: меняются ли данные сайта и валидаторы.

Запуск: python3 experiments/issue_456/dry_run_slices.py <worktree> <срез>
Срезы (каталоги, откуда убирается запрещённое поле ai-generated): см. SLICES.
В основной рабочей копии ничего не меняется. Данные сайта сравниваются без generatedAt.
"""
import json, pathlib, re, subprocess, sys, hashlib
SLICES = {"base": [], "docs-etc": ["docs", "pr-ops", "patterns", "kb"], "standards": ["standards"], "prompts": ["prompts"]}
wt = pathlib.Path(sys.argv[1]); name = sys.argv[2]

def norm(o):
    if isinstance(o, dict):
        return {k: norm(v) for k, v in o.items() if k not in ("generatedAt", "generated_at")}
    return [norm(v) for v in o] if isinstance(o, list) else o

def site_hash():
    subprocess.run(["node", "scripts/generate-pages-data.mjs"], cwd=wt, check=True, capture_output=True)
    return {p.name: hashlib.sha256(json.dumps(norm(json.loads(p.read_text())), sort_keys=True).encode()).hexdigest()[:12]
            for p in sorted((wt / "site/data").glob("*.json"))}

subprocess.run(["git", "checkout", "-q", "."], cwd=wt, check=True)
before = site_hash()
print("повтор генерации стабилен:", before == site_hash())
changed = 0
for top in SLICES[name]:
    for f in subprocess.run(["git", "ls-files", top], cwd=wt, capture_output=True, text=True).stdout.split("\n"):
        if not f.endswith(".md"): continue
        p = wt / f; t = p.read_text(encoding="utf-8")
        m = re.match(r"---\n.*?\n---\n", t, re.S)
        if m and re.search(r"^ai-generated:.*\n", m.group(0), re.M):
            p.write_text(re.sub(r"^ai-generated:.*\n", "", m.group(0), flags=re.M) + t[m.end():], encoding="utf-8"); changed += 1
print("срез", name, "файлов изменено:", changed)
after = site_hash()
print("данные сайта изменились:", [k for k in before if before[k] != after.get(k)])
subprocess.run(["git", "checkout", "-q", "site/data"], cwd=wt, check=True)
r = subprocess.run(["python3", "scripts/validate_all.py", "--full", "--jobs", "2"], cwd=wt, capture_output=True, text=True)
out = r.stdout + r.stderr
(pathlib.Path(sys.argv[3]) if len(sys.argv) > 3 else pathlib.Path("/dev/null")).write_text(out)
print("validate_all rc:", r.returncode); print(out.strip().splitlines()[-1] if out.strip() else "")
print("упали:", re.findall(r"^.*(?:FAIL|ПРОВАЛ).*$", out, re.M)[:15])
subprocess.run(["git", "checkout", "-q", "."], cwd=wt, check=True)
