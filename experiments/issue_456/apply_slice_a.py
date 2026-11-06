#!/usr/bin/env python3
"""Применяет срез А к рабочему дереву: убирает `ai-generated` из frontmatter файлов списка.
Сравнивает данные сайта до и после без учёта времени сборки.
Запуск: python3 experiments/issue_456/apply_slice_a.py experiments/issue_456/slice-a-files.txt"""
import hashlib, json, pathlib, re, subprocess, sys
FM = re.compile(r"---\n.*?\n---\n", re.S); AI = re.compile(r"^ai-generated:.*\n", re.M)
def norm(o):
    if isinstance(o, dict): return {k: norm(v) for k, v in o.items() if k not in ("generatedAt", "generated_at")}
    return [norm(v) for v in o] if isinstance(o, list) else o
def site():
    subprocess.run(["node", "scripts/generate-pages-data.mjs"], check=True, capture_output=True)
    h = {p.name: hashlib.sha256(json.dumps(norm(json.loads(p.read_text())), sort_keys=True).encode()).hexdigest()[:12] for p in sorted(pathlib.Path("site/data").glob("*.json"))}
    subprocess.run(["git", "checkout", "-q", "site/data"], check=True); return h
files = pathlib.Path(sys.argv[1]).read_text().split()
a = site(); changed = 0
for f in files:
    p = pathlib.Path(f); t = p.read_bytes().decode("utf-8"); m = FM.match(t)
    new = AI.sub("", m.group(0))
    if new != m.group(0): p.write_bytes((new + t[m.end():]).encode("utf-8")); changed += 1
b = site()
print("файлов в списке:", len(files), "| изменено:", changed)
print("JSON данных сайта:", len(a), "| изменились:", [k for k in a if a[k] != b.get(k)])
