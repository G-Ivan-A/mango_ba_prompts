#!/usr/bin/env python3
"""Миграция имён docs/rfc (issue #470): git mv и перенос ссылок.

Не трогает неизменяемые свидетельства: runs/ (инвариант неизменности прогонов),
*.log и снимки pr-body, исторический инвентарь, а также ссылки, закреплённые на
SHA (blob/<sha>/...): по такому адресу файл лежит под старым именем.
Старое имя находится по таблице соответствия в реестре RFC.
Запуск: python3 experiments/issue_470/migrate_rfc_names.py [--apply]
"""
import re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
KT = "docs/rfc/knowledge-transfer-to-hub/"
MAP = {
    "docs/rfc/rfc-register.md": "docs/rfc/rfc-registry.md",
    "docs/rfc/rfc-process.md": "docs/rfc/2026-06-rfc-process.md",
    "docs/rfc/rfc-to-hub-001-knowledge-transfer.md": "docs/rfc/2026-06-rfc-to-hub-001-knowledge-transfer.md",
    "docs/rfc/rfc-to-hub-002-prompt-debugging-process.md": "docs/rfc/2026-06-rfc-to-hub-002-prompt-debugging-process.md",
    "docs/rfc/prompt-improvement-bcreq-1025-proposal.md": "docs/rfc/2026-06-prompt-improvement-bcreq-1025-proposal.md",
    "docs/rfc/prompt-improvement-multichannel-proposal.md": "docs/rfc/2026-06-prompt-improvement-multichannel-proposal.md",
    "docs/rfc/2026-10-bcreq-meta-standards-rfc.md": "docs/rfc/2026-10-bcreq-meta-standards.md",
    "docs/rfc/2026-10-standards-page-rfc.md": "docs/rfc/2026-10-standards-page.md",
    **{f"{KT}{n}.md": f"{KT}2026-06-{n}.md" for n in ("ba-ontology", "bcreq-process", "operations-taxonomy", "pages-ux")},
}
SKIP_DIRS = ("runs/", "site/data/", "node_modules/")
SKIP_FILES = {"docs/analysis/2026-10-30-repository-inventory.md", "docs/analysis/2026-10-31-file-disposition-register.md", "experiments/issue_409/disposition.json", "docs/report/evidence/2026-09-01-run-0065-acb6c7bc-redacted.txt", "experiments/issue_470/migrate_rfc_names.py"}
SKIP_RE = re.compile(r"\.log$|(^|/)pr-body[^/]*\.md$|\.(png|jpe?g|gif|ico|woff2?|pdf|zip|xlsx|docx)$")
PINNED = re.compile(r"blob/[0-9a-f]{7,40}/\S*")
# Голые имена уникальны только у файлов верхнего уровня; ba-ontology.md и т. п.
# заменяются без каталога лишь внутри пакета knowledge-transfer.
GLOBAL = {Path(o).name: Path(n).name for o, n in MAP.items() if not o.startswith(KT)}
KT_LOCAL = {Path(o).name: Path(n).name for o, n in MAP.items() if o.startswith(KT)}
tok = lambda names: re.compile(r"(?<![\w/-])(" + "|".join(map(re.escape, names)) + r")(?![\w-])")
G_RE, KT_RE = tok(GLOBAL), tok(KT_LOCAL)
KT_PATH = re.compile(r"(knowledge-transfer-to-hub/)(" + "|".join(map(re.escape, KT_LOCAL)) + ")")


def rewrite(text, rel):
    def line(s):
        parts, pos = [], 0
        for m in PINNED.finditer(s):
            parts += [conv(s[pos:m.start()]), m.group()]
            pos = m.end()
        return "".join(parts + [conv(s[pos:])])

    def conv(s):
        s = G_RE.sub(lambda m: GLOBAL[m[1]], s)
        s = KT_PATH.sub(lambda m: m[1] + KT_LOCAL[m[2]], s)
        if rel.startswith(KT):
            s = KT_RE.sub(lambda m: KT_LOCAL[m[1]], s)
        return s

    return "".join(line(s) for s in text.splitlines(keepends=True))


def main():
    apply = "--apply" in sys.argv
    if apply:
        for old, new in MAP.items():
            if (ROOT / old).exists():
                subprocess.run(["git", "mv", old, new], cwd=ROOT, check=True)
    files = subprocess.run(["git", "ls-files"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.split("\n")
    changed = 0
    for rel in filter(None, files):
        p = ROOT / rel
        if rel.startswith(SKIP_DIRS) or rel in SKIP_FILES or SKIP_RE.search(rel) or not p.is_file():
            continue
        try:
            text = p.read_text(encoding="utf-8", newline="")
        except UnicodeDecodeError:
            continue
        new = rewrite(text, rel)
        if new != text:
            changed += 1
            print(rel)
            if apply:
                p.write_text(new, encoding="utf-8", newline="")
    print(f"files changed: {changed}")


if __name__ == "__main__":
    main()
