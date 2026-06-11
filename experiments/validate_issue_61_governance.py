#!/usr/bin/env python3
"""Local regression check for issue #61 governance contracts.

This script is intentionally kept under ignored ./experiments/ because it is a
task-local validation aid, not a repository test harness.
"""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def require(path: str, *needles: str) -> list[str]:
    text = read(path)
    errors = []
    for needle in needles:
        if needle not in text:
            errors.append(f"{path}: missing {needle!r}")
    return errors


def main() -> int:
    errors: list[str] = []

    errors += require(
        "AI_GOVERNANCE.md",
        "Creative",
        "Structured",
        "обоснованный обход",
        "молчание = согласие",
        "комментарий + ручной перезапуск",
    )
    errors += require(
        "AI_QUICK_RULES.md",
        "Structured",
        "Creative",
        "fail-closed",
        "обоснованный обход",
    )
    errors += require(
        "CONTRIBUTING.md",
        "В Creative режиме",
        "scope",
        "молчание = согласие",
        "ручной перезапуск",
    )
    errors += require(
        "docs/rfc-hub-integration.md",
        "рекоменд",
        "не ограничитель",
        "не блокирует локальные решения",
    )

    for path in (
        "docs/task-for-konard-template.md",
        "docs/adr/0003-creative-mode-governance.md",
    ):
        if not (ROOT / path).exists():
            errors.append(f"{path}: file does not exist")

    if (ROOT / "docs/task-for-konard-template.md").exists():
        errors += require(
            "docs/task-for-konard-template.md",
            "Контекст задачи",
            "Решаемая проблема",
            "Story",
            "ФТ",
            "НФТ",
            "Цель",
            "молчание = согласие",
        )

    if (ROOT / "docs/adr/0003-creative-mode-governance.md").exists():
        errors += require(
            "docs/adr/0003-creative-mode-governance.md",
            "PR #57",
            "Было",
            "Стало",
            "обоснованный обход",
            "молчание = согласие",
            "Creative",
        )

    if errors:
        print("issue-61 governance validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("issue-61 governance validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
