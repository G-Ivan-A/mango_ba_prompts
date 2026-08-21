#!/usr/bin/env python3
"""Исправление структуры корня и сбор архива в скрытый каталог (issue #291).

Скрипт воспроизводит миграцию один-в-один и является исполнимым приложением к
аудиту `docs/audit/2026-08-21-root-structure-audit.md`:

1. `git mv` каждого файла по карте MOVES;
2. пересчёт markdown-ссылок **внутри** перенесённых файлов: файл сменил каталог,
   поэтому цель разрешается относительно старого каталога и заново выражается
   относительно нового (`(agent-onboarding-protocol.md)` из `ai-rules/`
   становится `(../../ai-rules/agent-onboarding-protocol.md)` из
   `.archive/ai-rules/`);
3. переписывание ссылок и упоминаний пути **на** перенесённые файлы во всём
   репозитории — и в markdown, и в коде валидаторов;
4. точечная нормализация frontmatter-значений, где путь записан
   repo-relative (NORMALIZE).

Ссылки в permalink'ах Хаба (`https://github.com/...`) не трогаются: они ведут в
структуру Хаба на закреплённом SHA (тот же принцип, что в
`experiments/restructure_governance_dirs.py`, issue #265).

Каталоги `runs/` и `kb/` исключены из обхода полностью — жёсткий запрет issue #291.

Запуск (из корня репозитория, до переноса):

    python3 experiments/restructure_root_and_archive.py
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath

REPO = Path(__file__).resolve().parent.parent

# Неприкосновенные каталоги (контракт 2 issue #291) и служебные пути.
FROZEN = {"runs", "kb", ".git"}

MOVES = {
    # Executable-слой handover prompt — локальная надстройка спицы (issue #125),
    # которой нет в геноме Хаба templates/htom/. Место артефакта-промпта — prompts/.
    "AI_SESSION_HANDOVER_PROMPT.executable.md": "prompts/AI_SESSION_HANDOVER_PROMPT.executable.md",
    # Superseded-протокол v1.2 — архив для traceability, не точка входа (issue #267).
    # Соседство с активным v1.5 в ai-rules/ и есть та «свалка», которую убирает issue #291.
    "ai-rules/agent-onboarding-protocol_old.md": ".archive/ai-rules/agent-onboarding-protocol_old.md",
    "ai-rules/agent-onboarding-protocol_old.executable.md": ".archive/ai-rules/agent-onboarding-protocol_old.executable.md",
}

# Frontmatter-значения, где путь записан относительно файла, а не корня:
# приводим к repo-relative виду, как в остальных executable-слоях спицы.
NORMALIZE = {
    ".archive/ai-rules/agent-onboarding-protocol_old.executable.md": [
        (
            'related_standard: "../standards/cascading-context-loading-standard.md"',
            'related_standard: "standards/cascading-context-loading-standard.md"',
        ),
    ],
}

TEXT_SUFFIXES = {".md", ".py", ".mjs", ".json", ".sh", ".yml", ".yaml", ".txt", ".html", ".js"}

# Исторические записи: фиксируют путь, каким он был на момент события.
# Переписывание превратило бы журнал в неверный (тот же класс дефекта, что
# «некритично скопированный контекст», issue #265).
FROZEN_HISTORY = {
    ".hub-profile.json",
    "experiments/restructure_governance_dirs.py",
    # Сам скрипт: карта MOVES обязана хранить исходные пути.
    "experiments/restructure_root_and_archive.py",
}


def run(*args: str) -> None:
    subprocess.run(args, cwd=REPO, check=True)


def rewrite_internal_links(text: str, old_path: str, new_path: str) -> str:
    """Пересчитать markdown-ссылки внутри перенесённого файла."""
    old_dir = PurePosixPath(old_path).parent
    new_dir = PurePosixPath(new_path).parent
    if old_dir == new_dir:
        return text

    def fix(match: re.Match[str]) -> str:
        target = match.group(1)
        head, sep, tail = target.partition("#")
        # Внешние URL, чистые якоря и абсолютные пути остаются как есть.
        if not head or head.startswith("/") or re.match(r"^[a-z][a-z0-9+.-]*:", head):
            return match.group(0)
        resolved = os.path.normpath(str(old_dir / head))
        rebased = PurePosixPath(os.path.relpath(resolved, str(new_dir))).as_posix()
        return f"]({rebased}{sep}{tail})"

    return re.sub(r"\]\(([^)\s]+)\)", fix, text)


def iter_text_files() -> list[Path]:
    files: list[Path] = []
    for path in REPO.rglob("*"):
        rel = path.relative_to(REPO)
        if rel.parts and rel.parts[0] in FROZEN:
            continue
        if path.is_file() and path.suffix in TEXT_SUFFIXES:
            files.append(path)
    return files


def main() -> int:
    missing = [src for src in MOVES if not (REPO / src).exists()]
    if missing:
        print(f"нечего переносить, файлы отсутствуют: {missing}")
        return 0

    for src, dst in MOVES.items():
        (REPO / dst).parent.mkdir(parents=True, exist_ok=True)
        run("git", "mv", src, dst)
        target = REPO / dst
        target.write_text(
            rewrite_internal_links(target.read_text(encoding="utf-8"), src, dst),
            encoding="utf-8",
        )
        print(f"moved: {src} -> {dst}")

    # Ссылки НА перенесённые файлы: и относительные, и repo-relative упоминания.
    for path in iter_text_files():
        rel = path.relative_to(REPO).as_posix()
        if rel in FROZEN_HISTORY:
            continue
        text = original = path.read_text(encoding="utf-8")
        for src, dst in MOVES.items():
            here = "/".join([".."] * (len(path.relative_to(REPO).parts) - 1) + [dst]) or dst
            text = re.sub(r"\]\((?:\.\./)*" + re.escape(src) + r"([)#])", f"]({here}" + r"\1", text)
            # Голое упоминание пути: код валидаторов, таблицы README, frontmatter.
            text = re.sub(r"(?<![\w/.-])" + re.escape(src), dst, text)
        for needle, replacement in NORMALIZE.get(rel, []):
            text = text.replace(needle, replacement)
        if text != original:
            path.write_text(text, encoding="utf-8")
            print(f"links updated: {rel}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
