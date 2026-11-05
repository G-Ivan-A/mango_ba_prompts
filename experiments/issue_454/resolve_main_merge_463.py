"""Разрешение конфликта слияния main (PR #463) в ветку #454.

BL-172 остаётся за main; задача этой ветки о Ш-Р получает BL-174.
Запускается один раз в незавершённом слиянии, из корня репозитория.
"""
import re, subprocess
from pathlib import Path

CONFLICT = re.compile(r"<<<<<<< HEAD\n(.*?)=======\n(.*?)>>>>>>> upstream/main\n", re.S)
NEW = "BL-174"

def renum(t):
    return t.replace("BL-172", NEW).replace("bl-172-", "bl-174-")

def sub(path, fn):
    p = Path(path); t = p.read_text(encoding="utf-8")
    p.write_text(CONFLICT.sub(fn, t), encoding="utf-8")

# Журнал: обе записи, номер этой ветки заменён только в её части.
sub("CHANGELOG.md", lambda m: renum(m[1]) + "\n" + m[2])

# Реестр: строки BL-230/231 этой ветки новее, строка BL-172 — из main.
def table(m):
    ours = renum(m[1]).splitlines(True)
    main172 = [l for l in m[2].splitlines(True) if l.startswith("| BL-172 ")]
    r174 = [l for l in ours if l.startswith("| BL-174 ")]
    rest = [l for l in ours if not l.startswith("| BL-174 ")]
    i = next(i for i, l in enumerate(rest) if l.startswith("| BL-173 ")) + 1
    return "".join(main172 + rest[:i] + r174 + rest[i:])
sub("pr-ops/BACKLOG.md", table)

# Карточки: BL-172 (main), BL-173, BL-174.
def cards(m):
    ours = renum(m[1])
    a, b = ours.split("### BL-173.", 1)
    return m[2].rstrip("\n") + "\n\n### BL-173." + b.rstrip("\n") + "\n\n" + a.rstrip("\n") + "\n"
sub("pr-ops/backlog-ba-model.md", cards)

# Версия: 2.6.0 старше 2.5.1 и включает исключение отчёта.
for f in ("scripts/generate-pages-data.mjs", "scripts/validate_issue_446_test_kit.py",
          "scripts/validate_issue_450_bl156g_167_168.py", "scripts/validate_issue_460_site_debug.py",
          "site/index.html"):
    sub(f, lambda m: m[1])

# Остальные файлы: номер меняется там, где он принадлежит этой ветке.
own = subprocess.run(["git", "grep", "-l", "BL-172", "HEAD", "--"], capture_output=True, text=True).stdout.split()
for name in {x.split(":", 1)[1] for x in own}:
    if name in ("CHANGELOG.md", "pr-ops/BACKLOG.md", "pr-ops/backlog-ba-model.md"):
        continue
    p = Path(name); p.write_text(renum(p.read_text(encoding="utf-8")), encoding="utf-8")
