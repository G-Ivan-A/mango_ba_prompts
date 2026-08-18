#!/usr/bin/env python3
"""Реструктуризация `governance/` под базовую структуру Хаба (issue #265, ревью PR #266).

Скрипт воспроизводит перенос один-в-один:

1. `git mv` каждого файла по карте MOVES (ai-rules/, pr-ops/, docs/rfc/,
   docs/audit/, standards/);
2. переписывание ссылок вида `governance/<файл>` во всём репозитории на новый
   путь. **Ссылки в permalink'ах Хаба не трогаются**: у Хаба на закреплённых SHA
   был свой каталог `governance/`, и подмена такой ссылки на локальный путь
   сломала бы traceability (тот же дефект «некритично скопированный контекст»,
   ради которого заведён валидатор issue #265);
3. пересчёт относительных ссылок внутри перенесённых файлов: файл сменил
   глубину вложенности, поэтому `../AI_GOVERNANCE.md` из `governance/`
   становится `../../AI_GOVERNANCE.md` из `docs/audit/`.

Запуск (из корня репозитория, до переноса):

    python3 experiments/restructure_governance_dirs.py
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

MOVES = {
    # Операционные записи процесса PR → pr-ops/ (как в Хабе).
    "governance/artifact-map.md": "pr-ops/artifact-map.md",
    "governance/BACKLOG.md": "pr-ops/BACKLOG.md",
    "governance/session-digests.md": "pr-ops/session-digests.md",
    "governance/migration-manifest.md": "pr-ops/migration-manifest.md",
    "governance/migration-issues-registry.md": "pr-ops/migration-issues-registry.md",
    "governance/migration-phase1-issues.md": "pr-ops/migration-phase1-issues.md",
    "governance/sync-matrix-2026-06-17.md": "pr-ops/sync-matrix-2026-06-17.md",
    "governance/prompt-feedback.json": "pr-ops/prompt-feedback.json",
    # Локальная адаптация onboarding-протокола → ai-rules/ с суффиксом _old.
    "governance/agent-onboarding-protocol.md": "ai-rules/agent-onboarding-protocol_old.md",
    "governance/agent-onboarding-protocol.executable.md": "ai-rules/agent-onboarding-protocol_old.executable.md",
    # RFC и их материалы → docs/rfc/ (как в Хабе).
    "governance/rfc-process.md": "docs/rfc/rfc-process.md",
    "governance/rfc-register.md": "docs/rfc/rfc-register.md",
    "governance/rfc-to-hub-001-knowledge-transfer.md": "docs/rfc/rfc-to-hub-001-knowledge-transfer.md",
    "governance/rfc-to-hub-002-prompt-debugging-process.md": "docs/rfc/rfc-to-hub-002-prompt-debugging-process.md",
    "governance/rfc/prompt-improvement-bcreq-1025-proposal.md": "docs/rfc/prompt-improvement-bcreq-1025-proposal.md",
    "governance/rfc/prompt-improvement-multichannel-proposal.md": "docs/rfc/prompt-improvement-multichannel-proposal.md",
    "governance/knowledge-transfer-to-hub": "docs/rfc/knowledge-transfer-to-hub",
    # Аудиты → docs/audit/ (каталог уже есть локально и в Хабе).
    "governance/audit-contracts-2026-06-17.md": "docs/audit/audit-contracts-2026-06-17.md",
    "governance/audit-contracts-mango-2026-06-17.md": "docs/audit/audit-contracts-mango-2026-06-17.md",
    "governance/audit-hub-2026-06-17.md": "docs/audit/audit-hub-2026-06-17.md",
    "governance/audit-research-1027.md": "docs/audit/audit-research-1027.md",
    # Процессный стандарт спицы → standards/.
    "governance/prompt-debugging-process.md": "standards/prompt-debugging-process.md",
}

TEXT_SUFFIXES = {".md", ".py", ".json", ".yml", ".yaml", ".js", ".mjs", ".txt", ".sh", ".html"}

# Ссылка на Хаб: `hybrid-Intelligence-lab/blob|tree/<sha>/...` — не переписывается.
HUB_PREFIX_RE = re.compile(r"hybrid-Intelligence-lab/(?:blob|tree)/[0-9a-f]{7,40}/$")


def run(*args: str) -> None:
    subprocess.run(args, cwd=REPO, check=True)


def do_moves() -> None:
    for old, new in MOVES.items():
        (REPO / new).parent.mkdir(parents=True, exist_ok=True)
        run("git", "mv", old, new)
    for leftover in sorted((REPO / "governance").rglob("*"), reverse=True):
        if leftover.is_dir():
            leftover.rmdir()
    (REPO / "governance").rmdir()


def rewrite_paths() -> int:
    keys = sorted((k[len("governance/"):] for k in MOVES), key=len, reverse=True)
    mapping = {k[len("governance/"):]: v for k, v in MOVES.items()}
    # `rfc/` — каталог: ссылки на него встречаются и без имени файла.
    mapping["rfc/"] = "docs/rfc/"
    keys.append("rfc/")
    keys.sort(key=len, reverse=True)
    pattern = re.compile(r"(?<![-\w])governance/(" + "|".join(re.escape(k) for k in keys) + r")")
    changed = 0
    for rel in tracked_files():
        path = REPO / rel
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        text = path.read_text()

        def replace(match: re.Match[str]) -> str:
            if HUB_PREFIX_RE.search(text[: match.start()]):
                return match.group(0)  # permalink Хаба — у Хаба свой governance/
            return mapping[match.group(1)]

        new_text = pattern.sub(replace, text)
        if new_text != text:
            path.write_text(new_text)
            changed += 1
    return changed


def tracked_files() -> list[str]:
    out = subprocess.check_output(["git", "ls-files"], cwd=REPO, text=True)
    return [line for line in out.splitlines() if line]


def fix_relative_links() -> int:
    """Пересчитать относительные ссылки внутри перенесённых файлов."""
    from validate_issue_265_hub_sync import EXTERNAL_RE, PLACEHOLDER_RE, strip_code

    link_re = re.compile(r"(!?)\[([^\]]*)\]\(([^)\s]+)(\s+\"[^\"]*\")?\)")
    moved: dict[str, str] = {}
    for old, new in MOVES.items():
        old_path, new_path = REPO / old, REPO / new
        if new_path.is_dir():
            for file in sorted(new_path.rglob("*.md")):
                rel = file.relative_to(new_path).as_posix()
                moved[f"{new}/{rel}"] = f"{old}/{rel}"
        else:
            moved[new] = old
    reverse = {v: k for k, v in moved.items()}

    fixed = 0
    for new, old in moved.items():
        if not new.endswith(".md"):
            continue
        old_dir, new_dir = os.path.dirname(old), os.path.dirname(new)
        if old_dir == new_dir:
            continue
        path = REPO / new
        text = path.read_text()
        masked = strip_code(text).splitlines()
        lines = text.splitlines(True)
        out: list[str] = []
        for index, line in enumerate(lines):
            mask = masked[index] if index < len(masked) else ""

            def replace(match: re.Match[str]) -> str:
                nonlocal fixed
                target = match.group(3)
                if mask[match.start(3): match.end(3)] != target:
                    return match.group(0)  # ссылка внутри кода — синтаксический пример
                if EXTERNAL_RE.match(target) or PLACEHOLDER_RE.search(target):
                    return match.group(0)
                body = target.split("#")[0].split("?")[0]
                anchor = target[len(body):]
                if not body or (REPO / os.path.normpath(os.path.join(new_dir, body))).exists():
                    return match.group(0)
                old_target = os.path.normpath(os.path.join(old_dir, body))
                old_target = reverse.get(old_target, MOVES.get(old_target, old_target))
                if not (REPO / old_target).exists():
                    return match.group(0)
                rel = os.path.relpath(old_target, new_dir or ".")
                if body.endswith("/"):
                    rel += "/"
                fixed += 1
                return f"{match.group(1)}[{match.group(2)}]({rel}{anchor}{match.group(4) or ''})"

            out.append(link_re.sub(replace, line))
        new_text = "".join(out)
        if new_text != text:
            path.write_text(new_text)
    return fixed


def main() -> int:
    do_moves()
    print(f"перенесено путей: {len(MOVES)}")
    print(f"файлов с переписанными путями: {rewrite_paths()}")
    print(f"пересчитано относительных ссылок: {fix_relative_links()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
