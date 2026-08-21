#!/usr/bin/env python3
"""Валидатор issue #291: структурная миграция корня и скрытый архив.

Проверяет инварианты, а не только факт переноса:

A. **Корень канонический.** В корне нет markdown-файлов вне списка генома HTOM,
   и все обязательные файлы генома на месте.
B. **Архив вынесен и не потерян.** `superseded`-протокол лежит в `.archive/`,
   помечен баннером и ссылается на актуальную версию; в активных каталогах
   `*_old*.md` нет.
C. **Executable-слой handover перенесён в дом промптов** и связан с full-слоем
   в обе стороны.
D. **`runs/` и `kb/` неприкосновенны** (контракт 2): дома на месте.
E. **Замок стоит в CI**, а не только в документации.
F. **Аудит предоставлен** и разбирает причины, а не только перечисляет переносы.

Запуск:

    python3 scripts/validate_issue_291_root_structure.py
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CANONICAL_ROOT_MARKDOWN = {
    "AI_GOVERNANCE.md",
    "AI_QUICK_RULES.md",
    "AI_SESSION_HANDOVER_PROMPT.md",
    "README.md",
    "CONTRIBUTING.md",
    "CHANGELOG.md",
}

MOVED = {
    "AI_SESSION_HANDOVER_PROMPT.executable.md": "prompts/AI_SESSION_HANDOVER_PROMPT.executable.md",
    "ai-rules/agent-onboarding-protocol_old.md": ".archive/ai-rules/agent-onboarding-protocol_old.md",
    "ai-rules/agent-onboarding-protocol_old.executable.md": ".archive/ai-rules/agent-onboarding-protocol_old.executable.md",
}

AUDIT = "docs/audit/2026-08-21-root-structure-audit.md"
STRUCTURE_VALIDATOR = "tools/validate-repository-structure.sh"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def main() -> int:
    errors: list[str] = []

    # --- A. Корень канонический -------------------------------------------
    actual_root = {p.name for p in ROOT.glob("*.md")}
    for extra in sorted(actual_root - CANONICAL_ROOT_MARKDOWN):
        errors.append(f"[A] лишний markdown в корне: {extra}")
    for missing in sorted(CANONICAL_ROOT_MARKDOWN - actual_root):
        errors.append(f"[A] отсутствует обязательный файл генома HTOM: {missing}")

    # --- B/C. Переносы выполнены ------------------------------------------
    for old, new in MOVED.items():
        if (ROOT / old).exists():
            errors.append(f"[B/C] файл остался по старому пути: {old}")
        if not (ROOT / new).exists():
            errors.append(f"[B/C] файл отсутствует по новому пути: {new}")

    stray = [
        p.relative_to(ROOT).as_posix()
        for p in ROOT.rglob("*_old*.md")
        if not p.relative_to(ROOT).as_posix().startswith((".archive/", "runs/", "kb/"))
    ]
    for path in sorted(stray):
        errors.append(f"[B] superseded-артефакт вне .archive/: {path}")

    for archived in (".archive/ai-rules/agent-onboarding-protocol_old.md",
                     ".archive/ai-rules/agent-onboarding-protocol_old.executable.md"):
        if (ROOT / archived).exists():
            text = read(archived)
            if "status: superseded" not in text:
                errors.append(f"[B] архив не помечен superseded: {archived}")
            if "АРХИВ" not in text:
                errors.append(f"[B] в архиве нет баннера «АРХИВ»: {archived}")
            if "ai-rules/agent-onboarding-protocol.md" not in text:
                errors.append(f"[B] архив не ссылается на актуальный протокол: {archived}")

    if not (ROOT / ".archive/README.md").exists():
        errors.append("[B] .archive/README.md отсутствует: правила архива не зафиксированы")

    executable = MOVED["AI_SESSION_HANDOVER_PROMPT.executable.md"]
    if (ROOT / executable).exists():
        if 'full_version: "AI_SESSION_HANDOVER_PROMPT.md"' not in read(executable):
            errors.append(f"[C] executable-слой не связан с full-слоем: {executable}")
    if executable not in read("AI_SESSION_HANDOVER_PROMPT.md"):
        errors.append("[C] full-слой не ссылается на перенесённый executable-слой")

    # --- D. Неприкосновенные дома -----------------------------------------
    for protected in ("runs", "kb"):
        if not (ROOT / protected).is_dir():
            errors.append(f"[D] неприкосновенный каталог отсутствует: {protected}/")

    # --- E. Замок стоит в CI ----------------------------------------------
    if not (ROOT / STRUCTURE_VALIDATOR).exists():
        errors.append(f"[E] отсутствует {STRUCTURE_VALIDATOR}")
    else:
        result = subprocess.run([str(ROOT / STRUCTURE_VALIDATOR)], cwd=ROOT, capture_output=True)
        if result.returncode != 0:
            errors.append(f"[E] {STRUCTURE_VALIDATOR} падает: {result.stderr.decode().strip()}")
    if "validate-structure" not in read("Makefile"):
        errors.append("[E] цель validate-structure не подключена в Makefile")
    if "validate-structure" not in read(".github/workflows/validate.yml"):
        errors.append("[E] validate-structure не запускается в CI")

    # --- F. Аудит ----------------------------------------------------------
    if not (ROOT / AUDIT).exists():
        errors.append(f"[F] отсутствует отчёт аудита: {AUDIT}")
    else:
        audit = read(AUDIT)
        for needle in (
            "жёсткое ограничение",          # разбор посылки задачи
            "Пошаговая реконструкция",      # причины по шагам
            "Явная фиксация решений",       # контракт 3
            "NO CHANGE",                    # что сознательно не тронуто
            "runs/",                        # контракт 2
        ):
            if needle not in audit:
                errors.append(f"[F] в аудите нет обязательного раздела/маркера: {needle!r}")

    if errors:
        print("issue-291 root structure validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("[A] корень канонический: только файлы генома HTOM")
    print(f"[B] архив вынесен в .archive/ и помечен: {len(MOVED) - 1} файла")
    print(f"[C] executable-слой handover перенесён в {executable}")
    print("[D] runs/ и kb/ на месте")
    print("[E] замок на структуру подключён в make validate и CI")
    print(f"[F] аудит предоставлен: {AUDIT}")
    print("\nOK: структура корня исправлена, архив скрыт, регресс закрыт проверкой")
    return 0


if __name__ == "__main__":
    sys.exit(main())
