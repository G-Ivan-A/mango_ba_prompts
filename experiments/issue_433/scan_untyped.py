"""Список мест «гейт человека» без типа в окне ±2 строки (BL-159, issue #433)."""
import re, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
PAT = re.compile(r"human[ -]gate|G-human|человеческ(?:ий|ого|ие|их|ому|им) гейт|решени[еяю] человека|подтверждени[яе] человека|human-in-the-loop", re.I)
TYPE = re.compile(r"`(?:человек|гибрид|llm|код)`|тип гейта|типа? `|ключев", re.I)
EXCL = re.compile(r"^(docs/analysis|runs|experiments|site/data|prompts/archive|CHANGELOG|node_modules|docs/audit|pr-ops/archive)")
files = subprocess.run(["git", "ls-files", "*.md", "*.json", "*.yaml", "*.yml"], cwd=ROOT, capture_output=True, text=True).stdout.split()
for f in files:
    if EXCL.match(f): continue
    lines = (ROOT / f).read_text(errors="ignore").splitlines()
    for i, line in enumerate(lines):
        if PAT.search(line):
            window = "\n".join(lines[max(0, i-2): i+3])
            if not TYPE.search(window):
                print(f"{f}:{i+1}: {line.strip()[:170]}")
