#!/usr/bin/env python3
"""Issue #388: перенести устаревшие промпты в prompts/archive/ и переписать ссылки.

Шаги:
1. ``git mv prompts/<f>.md prompts/archive/<f>.md``; ``status: archived``;
   баннер «Архив (issue #388)» со ссылкой на замену из набора BCREQ.
2. Относительные ссылки внутри перенесённых файлов пересчитываются от нового
   места.
3. Во всех текстовых файлах репозитория (кроме .git и site/data — данные
   сайта перегенерируются) ссылки на старый путь — относительные,
   абсолютные URL и упоминания ``prompts/<f>.md`` — ведут в архив.

Повторный запуск безопасен: уже перенесённые файлы пропускаются.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NAMES = (ROOT / "experiments/issue_388/archived-prompts.txt").read_text().split()
BASE = "https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/"

REPLACEMENT = {
    "constraints-documentation": ["bcreq-constraints-documentation-stepwise", "bcreq-work-solution-design-oneshot"],
    "fr-documentation": ["bcreq-fr-documentation-stepwise", "bcreq-core-documentation-oneshot"],
    "fr-validation": ["bcreq-review-validation-oneshot"],
    "glossary-context-understanding": ["bcreq-context-understanding-stepwise", "bcreq-in-understanding-oneshot"],
    "questions-customer-understanding": ["bcreq-context-understanding-stepwise", "bcreq-in-understanding-oneshot"],
    "technical-details-solution-design": ["bcreq-orr-solution-design-stepwise", "bcreq-work-solution-design-oneshot"],
    "uc-modeling": ["bcreq-uc-modeling-stepwise", "bcreq-scenarios-modeling-oneshot"],
    "us-modeling": ["bcreq-scenarios-modeling-oneshot"],
}

TEXT_SUFFIXES = {".md", ".py", ".mjs", ".js", ".json", ".yml", ".yaml", ".html", ".txt", ".sh", ".csv"}
LINK = re.compile(r"(\]\()([^)\s#?]+)([#?][^)\s]*)?(\))")


def family(name: str) -> str:
    return name.rsplit("-", 1)[0]


def banner(name: str) -> str:
    links = ", ".join(f"[{r}]({BASE}{r}.md)" for r in REPLACEMENT[family(name)])
    return (
        "> **Архив (issue #388).** Промпт заменён набором BCREQ: "
        f"{links}. Файл сохранён для ссылок из записанных прогонов.\n\n"
    )


def rel(target: Path, start: Path) -> str:
    return os.path.relpath(target, start).replace(os.sep, "/")


def move(name: str) -> None:
    old = ROOT / "prompts" / f"{name}.md"
    new = ROOT / "prompts" / "archive" / f"{name}.md"
    if new.exists():
        return
    subprocess.run(["git", "mv", str(old), str(new)], cwd=ROOT, check=True)
    text = new.read_text(encoding="utf-8")
    head, sep, body = text.partition("\n---\n")
    head = re.sub(r"^status: .*$", "status: archived", head, count=1, flags=re.M)

    def fix(m: re.Match) -> str:
        url = m.group(2)
        if re.match(r"^[a-z]+:", url) or url.startswith("/"):
            return m.group(0)
        resolved = (old.parent / url).resolve()
        moved_name = resolved.stem if resolved.parent == old.parent else None
        if moved_name in NAMES:
            resolved = new.parent / resolved.name
        return m.group(1) + rel(resolved, new.parent) + (m.group(3) or "") + m.group(4)

    body = LINK.sub(fix, body)
    # баннер — сразу после frontmatter
    new.write_text(head + sep + "\n" + banner(name) + body.lstrip("\n"), encoding="utf-8")


def rewrite_repo() -> int:
    changed = 0
    files = subprocess.run(["git", "ls-files"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.split("\n")
    alt = "|".join(re.escape(n) for n in NAMES)
    abs_re = re.compile(rf"(blob/main/prompts/)({alt})\.md")
    plain_re = re.compile(rf"(?<![\w./-])prompts/({alt})\.md")
    for f in files:
        if not f or f.startswith(("site/data/", "prompts/archive/", "experiments/issue_388/")):
            continue
        p = ROOT / f
        if p.suffix not in TEXT_SUFFIXES or not p.is_file():
            continue
        text = p.read_text(encoding="utf-8", errors="strict")
        orig = text

        def fix(m: re.Match) -> str:
            url = m.group(2)
            if re.match(r"^[a-z]+:", url) or url.startswith("/"):
                return m.group(0)
            resolved = (p.parent / url).resolve()
            if resolved.parent == ROOT / "prompts" and resolved.stem in NAMES and resolved.suffix == ".md":
                target = ROOT / "prompts" / "archive" / resolved.name
                return m.group(1) + rel(target, p.parent) + (m.group(3) or "") + m.group(4)
            return m.group(0)

        if p.suffix == ".md":
            text = LINK.sub(fix, text)
        text = abs_re.sub(r"\1archive/\2.md", text)
        text = plain_re.sub(r"prompts/archive/\1.md", text)
        if text != orig:
            p.write_text(text, encoding="utf-8")
            changed += 1
            print("rewrote", f)
    return changed


def main() -> int:
    for n in NAMES:
        move(n)
    print("files rewritten:", rewrite_repo())
    return 0


if __name__ == "__main__":
    sys.exit(main())
