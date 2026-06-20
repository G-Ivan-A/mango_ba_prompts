#!/usr/bin/env python3
"""Regression check for issue #134 — repository README standard.

The check locks the deliverables requested in issue #134:

- ``standards/readme-standard.md`` exists and describes the four README canons;
- the standard contains the mandatory README structure, prohibitions, ownership
  separation, examples, self-check, and integration references;
- ``templates/readme-template.md`` exists as a reusable five-minute template;
- CHANGELOG and CI mention this validator so the standard does not silently drift.
"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

STANDARD = "standards/readme-standard.md"
TEMPLATE = "templates/readme-template.md"
CHANGELOG = "CHANGELOG.md"
WORKFLOW = ".github/workflows/github-pages.yml"
VALIDATOR = "scripts/validate_issue_134_readme_standard.py"


def read_text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def require_path(path: str) -> list[str]:
    return [] if (ROOT / path).exists() else [f"{path}: missing"]


def require_text(path: str, *needles: str) -> list[str]:
    text = read_text(path)
    return [f"{path}: missing {needle!r}" for needle in needles if needle not in text]


def require_ordered_headings(path: str, headings: tuple[str, ...]) -> list[str]:
    text = read_text(path)
    errors: list[str] = []
    last = -1
    for heading in headings:
        pos = text.find(heading)
        if pos == -1:
            errors.append(f"{path}: missing heading {heading!r}")
        elif pos < last:
            errors.append(f"{path}: heading {heading!r} is out of order")
        last = max(last, pos)
    return errors


def check_standard() -> list[str]:
    errors = require_path(STANDARD)
    if errors:
        return errors

    errors += require_text(
        STANDARD,
        "type: standard",
        "scope: readme",
        "Канон 1: Коммуникация",
        "Канон 2: Инструкция",
        "Канон 3: Сообщество",
        "Канон 4: SEO",
        "Что это за проект/каталог?",
        "Какую проблему он решает?",
        "Чем отличается от других?",
        "## Что это?",
        "## Как использовать?",
        "## Быстрый старт",
        "## Связанные документы",
        "## Как помочь?",
        "README.md",
        "CHANGELOG.md",
        "CONTRACT.md",
        "REGISTRY.md",
        "Не смешивать README",
        "200-300 строк",
        "Пример хорошего README",
        "Пример плохого README",
        "Чек-лист",
        "standards/cascading-context-loading-standard.md",
        "README.executable.md",
        "repository-structure-vision-2026-06.md",
        "standards/runs-contract-standard.md",
        TEMPLATE,
    )

    errors += require_ordered_headings(
        STANDARD,
        (
            "# Стандарт README",
            "## Назначение",
            "## Четыре канона",
            "## Обязательная структура",
            "## Запрещено",
            "## Разделение ответственности",
            "## Интеграция",
            "## Примеры",
            "## Чек-лист",
        ),
    )

    line_count = len(read_text(STANDARD).splitlines())
    if not (80 <= line_count <= 300):
        errors.append(f"{STANDARD}: expected 80..300 lines, found {line_count}")

    return errors


def check_template() -> list[str]:
    errors = require_path(TEMPLATE)
    if errors:
        return errors

    errors += require_text(
        TEMPLATE,
        "# <Название>",
        "Краткое описание",
        "## Что это?",
        "## Как использовать?",
        "## Быстрый старт",
        "## Связанные документы",
        "## Как помочь?",
        STANDARD,
    )

    text = read_text(TEMPLATE)
    if "CHANGELOG" in text or "CONTRACT" in text or "REGISTRY" in text:
        errors.append(f"{TEMPLATE}: template must not include changelog/contract/registry content")

    return errors


def check_changelog_and_ci() -> list[str]:
    errors = require_path(CHANGELOG) + require_path(WORKFLOW)
    if errors:
        return errors

    errors += require_text(
        CHANGELOG,
        "Issue #134",
        STANDARD,
        TEMPLATE,
        VALIDATOR,
    )
    errors += require_text(
        WORKFLOW,
        "Validate issue #134 README standard",
        f"python3 {VALIDATOR}",
    )
    return errors


def main() -> int:
    errors = check_standard() + check_template() + check_changelog_and_ci()

    if errors:
        print("Issue #134 README standard validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    standard_lines = len(read_text(STANDARD).splitlines())
    template_lines = len(read_text(TEMPLATE).splitlines())
    print(
        "Issue #134 README standard validation passed "
        f"({standard_lines} standard lines, {template_lines} template lines)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
