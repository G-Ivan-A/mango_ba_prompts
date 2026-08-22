#!/usr/bin/env python3
"""Миграция issue #291 (шаг 2): управляющие контракты из корня в канонические дома.

Контекст. Первая итерация issue #291 оставила `AI_GOVERNANCE.md`,
`AI_QUICK_RULES.md` и `AI_SESSION_HANDOVER_PROMPT.md` в корне: геном HTOM Хаба
требовал их именно там. RFC #532 (принят в Хабе, PR #538) снял это ограничение —
теперь контракт нормируется по **наличию**, а не по размещению, и канонической
раскладкой объявлены `ai-governance/` + `ai-rules/`. Одновременно введён запрет
на два дома одного контракта: дубликат = два SSOT = ошибка валидации.

Что делает скрипт:

1. Освобождает канонический слот генома `ai-governance/ai-governance.md`.
   Его занимала рабочая копия стандарта Хаба (синк issue #265, `sync_policy:
   no local edits`) — другой артефакт с другим source of truth. Копия переезжает
   в `ai-governance/hub-ai-governance.md`, слот отдаётся контракту спицы.
2. Переносит три управляющих контракта из корня в канонические дома.
3. Переписывает входящие и исходящие внутренние ссылки во всех текстовых файлах репозитория,
   пересчитывая относительный путь от каталога каждого файла. В markdown
   переписываются только цели ссылок `](...)`; голые упоминания имени в прозе
   не трогаются автоматически, потому что то же имя может означать файл Хаба,
   а не спицы, — такие места правятся руками и осмысленно.

Границы (контракт 2 issue #291): `runs/` и `kb/` исключены из обхода на уровне
кода — они не читаются и не пишутся. `.archive/` тоже исключён: архив хранит
снимок документа на момент архивации, переписывать его ссылки — фальсификация.

Запуск (идемпотентен, повторный прогон ничего не делает):

    python3 experiments/restructure_governance_to_canonical_homes.py [--dry-run]
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Слот генома освобождается до переноса контракта — иначе git mv затрёт копию Хаба.
FREE_SLOT = ("ai-governance/ai-governance.md", "ai-governance/hub-ai-governance.md")

MOVES = [
    ("AI_GOVERNANCE.md", "ai-governance/ai-governance.md"),
    ("AI_QUICK_RULES.md", "ai-rules/ai-quick-rules.md"),
    ("AI_SESSION_HANDOVER_PROMPT.md", "ai-rules/AI_SESSION_HANDOVER_PROMPT.md"),
]

# Каталоги, которые скрипт не читает и не изменяет.
SKIP_DIRS = {".git", ".validate-cache", "runs", "kb", ".archive"}

TEXT_SUFFIXES = {".md", ".py", ".sh", ".json", ".yml", ".yaml", ".txt", ".html", ".js", ".css"}

# Файлы, которые ведут таблицу переносов сами и потому не переписываются:
# миграционные скрипты (включая этот) и валидаторы структуры — их таблицы
# путей правятся руками и осмысленно, а не регуляркой. `.hub-profile.json`
# исключён потому, что sync_history — журнал путей на момент синка: переписать
# его значит подделать историю (вместо этого ведётся раздел path_migrations).
SKIP_FILES = {
    ".hub-profile.json",
    "experiments/restructure_governance_dirs.py",
    "experiments/restructure_governance_to_canonical_homes.py",
    "experiments/restructure_root_and_archive.py",
    "scripts/validate_issue_291_root_structure.py",
    "tools/validate-repository-structure.sh",
}


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout


def iter_text_files():
    for path in sorted(ROOT.rglob("*")):
        rel = path.relative_to(ROOT)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        if rel.as_posix() in SKIP_FILES:
            continue
        if path.is_file() and path.suffix in TEXT_SUFFIXES:
            yield path


def rewrite_links(mapping: dict[str, str], dry_run: bool) -> list[str]:
    """Переписывает ссылки на перенесённые файлы. Возвращает список изменённых файлов."""
    changed: list[str] = []
    for path in iter_text_files():
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        original = text
        base = path.parent

        for old, new in mapping.items():
            old_name = Path(old).name
            if old_name not in text:
                continue

            # Относительный путь от каталога текущего файла к новому месту.
            def rel_to(target: str) -> str:
                import os

                return os.path.relpath((ROOT / target).as_posix(), base.as_posix())

            new_rel = rel_to(new)

            # 1. Markdown-ссылки: ](<любой путь>/AI_X.md) и ссылочные определения.
            #    Совпадение только по точному имени файла, поэтому
            #    AI_SESSION_HANDOVER_PROMPT.executable.md не задевается.
            text = re.sub(
                r"\]\((?:\./|\.\./)*(?:[\w./-]*/)?" + re.escape(old_name) + r"((?:#[\w.-]+)?)\)",
                lambda m: f"]({new_rel}{m.group(1)})",
                text,
            )

            # 2. Пути внутри кода и конфигов: root-relative строковые литералы.
            #    Только не-markdown — в прозе такое же имя может означать файл
            #    Хаба, а не спицы (например «хабовый AI_GOVERNANCE.md» в
            #    docs/audit/audit-hub-2026-06-17.md). Проза правится руками.
            if path.suffix != ".md":
                text = re.sub(
                    r"(?<![\w./-])(?:\./)?" + re.escape(old_name) + r"(?![\w.-])",
                    new,
                    text,
                )

        if text != original:
            changed.append(path.relative_to(ROOT).as_posix())
            if not dry_run:
                path.write_text(text, encoding="utf-8")
    return changed


def fix_outgoing_links(new_path: str, dry_run: bool) -> bool:
    """Чинит исходящие ссылки внутри переехавшего файла.

    Документ лежал в корне, поэтому его ссылки были root-relative (`](docs/...)`)
    и совпадали с путём от корня. После переезда на уровень вглубь такие цели
    больше не разрешаются: их нужно пересчитать от нового каталога.
    """
    import os

    path = ROOT / new_path
    text = path.read_text(encoding="utf-8")
    base = path.parent

    def repl(match: re.Match[str]) -> str:
        target, anchor = match.group(1), match.group(2)
        if target.startswith(("http", "#", "mailto:", "../", "./")):
            return match.group(0)
        # Root-relative цель распознаётся по тому, что она разрешается от корня,
        # но не разрешается от каталога файла. Иначе это уже корректная ссылка.
        if (ROOT / target).exists() and not (base / target).exists():
            return f"]({os.path.relpath((ROOT / target).as_posix(), base.as_posix())}{anchor})"
        return match.group(0)

    updated = re.sub(r"\]\(([^)#\s]+)((?:#[^)\s]*)?)\)", repl, text)
    if updated == text:
        return False
    if not dry_run:
        path.write_text(updated, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    moved: dict[str, str] = {}

    old, new = FREE_SLOT
    if (ROOT / old).exists() and not (ROOT / new).exists():
        print(f"free slot: {old} -> {new}")
        if not args.dry_run:
            git("mv", old, new)
        moved[old] = new

    for old, new in MOVES:
        if not (ROOT / old).exists():
            print(f"skip (уже перенесён): {old}")
            continue
        # В --dry-run слот ещё физически занят: учитываем, что он уже освобождён выше.
        if (ROOT / new).exists() and new not in moved:
            print(f"ERROR: цель занята: {new}", file=sys.stderr)
            return 1
        print(f"move: {old} -> {new}")
        if not args.dry_run:
            git("mv", old, new)
        moved[old] = new

    if not moved:
        print("нечего переносить — структура уже канонична")
        return 0

    # Ссылки на рабочую копию Хаба переписываются отдельно: имя файла совпадает
    # с целевым слотом, поэтому общий проход дал бы ложные срабатывания.
    link_map = {old: new for old, new in moved.items() if old != FREE_SLOT[0]}
    changed = rewrite_links(link_map, args.dry_run)

    # Входящие ссылки починены выше, исходящие — здесь: переехавший файл сам
    # ссылался на репозиторий от корня, и после переезда эти цели разъехались.
    if not args.dry_run:
        for target in moved.values():
            if target.endswith(".md") and fix_outgoing_links(target, args.dry_run):
                print(f"исходящие ссылки пересчитаны: {target}")
    print(f"\nобновлено ссылок в {len(changed)} файлах:")
    for name in changed:
        print(f"  {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
