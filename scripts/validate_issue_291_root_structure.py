#!/usr/bin/env python3
"""Валидатор issue #291: структурная миграция корня и скрытый архив.

Проверяет инварианты, а не только факт переноса:

A. **Корень канонический.** В корне нет markdown-файлов вне списка генома HTOM,
   а управляющие контракты лежат в канонических домах `ai-governance/` +
   `ai-rules/` и ровно в одном доме каждый (RFC #532 Хаба: два дома = два SSOT).
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
    "README.md",
    "CONTRIBUTING.md",
    "CHANGELOG.md",
}

MOVED = {
    "AI_SESSION_HANDOVER_PROMPT.executable.md": "prompts/AI_SESSION_HANDOVER_PROMPT.executable.md",
    "ai-rules/agent-onboarding-protocol_old.md": ".archive/ai-rules/agent-onboarding-protocol_old.md",
    "ai-rules/agent-onboarding-protocol_old.executable.md": ".archive/ai-rules/agent-onboarding-protocol_old.executable.md",
    "AI_GOVERNANCE.md": "ai-governance/ai-governance.md",
    "AI_QUICK_RULES.md": "ai-rules/ai-quick-rules.md",
    "AI_SESSION_HANDOVER_PROMPT.md": "ai-rules/AI_SESSION_HANDOVER_PROMPT.md",
}

# Дом контракта — ровно один. Первый кандидат канонический, остальные —
# переходные (governance/) и легаси (корень): их наличие означает второй SSOT.
CONTRACT_HOMES = {
    "governance contract": (
        "ai-governance/ai-governance.md",
        "governance/AI_GOVERNANCE.md",
        "AI_GOVERNANCE.md",
    ),
    "quick rules": (
        "ai-rules/ai-quick-rules.md",
        "governance/AI_QUICK_RULES.md",
        "AI_QUICK_RULES.md",
    ),
    "handover prompt": (
        "ai-rules/AI_SESSION_HANDOVER_PROMPT.md",
        "governance/AI_SESSION_HANDOVER_PROMPT.md",
        "AI_SESSION_HANDOVER_PROMPT.md",
    ),
}

HANDOVER = "ai-rules/AI_SESSION_HANDOVER_PROMPT.md"

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

    for label, homes in CONTRACT_HOMES.items():
        present = [home for home in homes if (ROOT / home).exists()]
        if not present:
            errors.append(f"[A] контракт не найден ни в одном доме: {label} ({', '.join(homes)})")
        elif len(present) > 1:
            errors.append(f"[A] контракт в двух домах сразу (два SSOT): {label} — {', '.join(present)}")
        elif present[0] != homes[0]:
            errors.append(f"[A] контракт вне канонического дома: {label} лежит в {present[0]}, ожидался {homes[0]}")

    # Каталог governance/ признан переходным (limbo state) и не должен быть
    # конечным пунктом миграции — RFC #532, ответ Q-2.
    if (ROOT / "governance").is_dir():
        errors.append("[A] governance/ — переходный дом (limbo state), а не конечный: перенеси содержимое в ai-governance/ + ai-rules/")

    # Каждый каталог верхнего уровня вне генома обязан быть задекларирован
    # с непустой причиной — иначе это остаток реструктуризации.
    import json

    profile = json.loads(read(".hub-profile.json"))
    declared = {
        (entry.get("path") or "").strip("/")
        for entry in profile.get("project_specific_directories", []) or []
        if isinstance(entry, dict) and (entry.get("reason") or "").strip()
    }
    canonical_dirs = {".git", ".github", "docs", "tools", "ai-governance", "ai-rules", ".archive"}
    for path in sorted(ROOT.iterdir()):
        if not path.is_dir() or path.name in canonical_dirs or path.name in declared:
            continue
        if subprocess.run(["git", "check-ignore", "-q", path.name], cwd=ROOT).returncode == 0:
            continue
        errors.append(f"[A] недекларированный каталог верхнего уровня: {path.name}/ — задекларируй в .hub-profile.json (path + reason)")

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
        if f'full_version: "{HANDOVER}"' not in read(executable):
            errors.append(f"[C] executable-слой не связан с full-слоем: {executable}")
    if executable not in read(HANDOVER):
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
            "RFC #532",                     # снятие блокера и второй шаг миграции
        ):
            if needle not in audit:
                errors.append(f"[F] в аудите нет обязательного раздела/маркера: {needle!r}")

    if errors:
        print("issue-291 root structure validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("[A] корень канонический; контракты — в ai-governance/ + ai-rules/, по одному дому")
    print(f"[B] архив вынесен в .archive/ и помечен: {len(MOVED) - 1} файла")
    print(f"[C] executable-слой handover перенесён в {executable}")
    print("[D] runs/ и kb/ на месте")
    print("[E] замок на структуру подключён в make validate и CI")
    print(f"[F] аудит предоставлен: {AUDIT}")
    print("\nOK: структура корня исправлена, архив скрыт, регресс закрыт проверкой")
    return 0


if __name__ == "__main__":
    sys.exit(main())
