#!/usr/bin/env python3
"""Валидатор issue #265: ре-синк методологии Хаба и целостность ссылок.

Проверки
--------
A. **Ссылки.** Ни одна относительная Markdown-ссылка репозитория не ведёт в
   несуществующую цель. Это регрессионный тест дефекта §4.2 анализа готовности
   Хаба («некритично скопированный контекст»): документ уверенно ссылается на
   цели, которых в споке нет, — поведенчески это неотличимо от галлюцинации.
   Инлайн-код и fenced-блоки не проверяются: там ссылка — синтаксический пример
   (`[KB: <slug>](kb/<path>#<anchor>)`), а не адрес.
B. **Рабочие копии Хаба.** Каждый файл из манифеста `scripts/sync_from_hub.py`
   существует и несёт `source_sha`, равный `last_sync.hub_sha` в
   `.hub-profile.json` (единая точка синка, без «частично обновлённых» копий).
C. **Нет hub-относительных путей.** В споке запрещены ссылки, выходящие за
   корень репозитория (`../../CONCEPT.md`): цель Хаба адресуется полным URL с
   закреплённым SHA, иначе ссылка ломается при любом изменении структуры Хаба.

Запуск (stdlib-only, без сети):

    python3 scripts/validate_issue_265_hub_sync.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sync_from_hub import MANIFEST  # noqa: E402  (локальный модуль рядом)

REPO_ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", "node_modules", "site/data"}

LINK_RE = re.compile(r"(?<!\!)\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
EXTERNAL_RE = re.compile(r"^(https?:|mailto:|tel:|#|data:)")

# Плейсхолдеры-шаблоны: цель содержит метапеременную и не является адресом.
PLACEHOLDER_RE = re.compile(r"[<>]")


def iter_markdown() -> list[Path]:
    files: list[Path] = []
    for path in sorted(REPO_ROOT.rglob("*.md")):
        rel = path.relative_to(REPO_ROOT).as_posix()
        if any(rel == d or rel.startswith(f"{d}/") for d in SKIP_DIRS):
            continue
        files.append(path)
    return files


def strip_code(text: str) -> str:
    """Заменить содержимое fenced-блоков и инлайн-кода пробелами.

    Позиции строк сохраняются: номера строк в отчёте остаются настоящими.
    """
    out: list[str] = []
    in_fence = False
    fence = ""
    for line in text.splitlines():
        stripped = line.lstrip()
        if in_fence:
            if stripped.startswith(fence):
                in_fence = False
            out.append("")
            continue
        match = re.match(r"(`{3,}|~{3,})", stripped)
        if match:
            in_fence = True
            fence = match.group(1)[:3]
            out.append("")
            continue
        out.append(re.sub(r"`[^`]*`", lambda m: " " * len(m.group(0)), line))
    return "\n".join(out)


def check_links() -> list[str]:
    errors: list[str] = []
    checked = 0
    for path in iter_markdown():
        rel_file = path.relative_to(REPO_ROOT).as_posix()
        body = strip_code(path.read_text(encoding="utf-8"))
        for lineno, line in enumerate(body.splitlines(), start=1):
            targets = [(m.group(2)) for m in LINK_RE.finditer(line)]
            targets += [(m.group(2)) for m in IMAGE_RE.finditer(line)]
            for target in targets:
                if EXTERNAL_RE.match(target) or PLACEHOLDER_RE.search(target):
                    continue
                clean = target.split("#", 1)[0].split("?", 1)[0]
                if not clean:
                    continue
                checked += 1
                resolved = (path.parent / clean).resolve()
                try:
                    resolved.relative_to(REPO_ROOT)
                except ValueError:
                    errors.append(
                        f"{rel_file}:{lineno}: ссылка `{target}` выходит за корень "
                        "репозитория; цель в Хабе адресуется полным URL с SHA"
                    )
                    continue
                if not resolved.exists():
                    errors.append(f"{rel_file}:{lineno}: битая ссылка `{target}`")
    print(f"[A/C] проверено относительных ссылок: {checked}")
    return errors


def check_working_copies() -> list[str]:
    errors: list[str] = []
    profile = json.loads((REPO_ROOT / ".hub-profile.json").read_text(encoding="utf-8"))
    sha = profile["last_sync"]["hub_sha"]
    synced = set(profile["last_sync"].get("synced_paths", []))
    for local_file in sorted(MANIFEST.values()):
        path = REPO_ROOT / local_file
        if not path.exists():
            errors.append(f"{local_file}: рабочая копия Хаба отсутствует")
            continue
        head = path.read_text(encoding="utf-8")[:4000]
        if f'source_sha: "{sha}"' not in head:
            errors.append(
                f"{local_file}: source_sha не равен last_sync.hub_sha ({sha[:7]}); "
                "выполните `python3 scripts/sync_from_hub.py --hub-dir <клон Хаба>`"
            )
        if local_file not in synced:
            errors.append(f"{local_file}: путь не заявлен в .hub-profile.json synced_paths")
    print(f"[B] проверено рабочих копий Хаба: {len(MANIFEST)} @ {sha[:7]}")
    return errors


def main() -> int:
    errors = check_links() + check_working_copies()
    if errors:
        print(f"\nFAIL: {len(errors)} проблем:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1
    print("\nOK: ссылки целостны, рабочие копии Хаба на одном SHA")
    return 0


if __name__ == "__main__":
    sys.exit(main())
