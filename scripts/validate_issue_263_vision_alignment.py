#!/usr/bin/env python3
"""Regression check for issue #263 — корректировка видения и концепции проекта.

Проверка фиксирует контракт концептуальных документов спока:

- принцип «качество системы исполнения > стоимость» объявлен в конституции и
  продублирован ссылкой в README;
- ДОД требует механизм проверки операции (чек-лист / evals / human gate), а
  формулировка «операция без процесса проверки не завершена» присутствует;
- роль проекта и инфраструктурная модель описаны без серверной инфраструктуры
  и мультиагентной системы;
- связь с `ai-ba-playbooks` описана как односторонний неавтоматический поток;
- решения Хаба (ADR-009 v0.3, онтология процессов БА, анализ готовности)
  зарегистрированы якорями в едином мосте, а не скопированы;
- в концептуальных документах нет прямых hub-относительных ссылок;
- в концептуальных документах нет внутренних терминов («фаундер», имя
  AI-исполнителя) и концептов проекта БИЛД (Proof of Execution, Learning loop,
  S1–S5);
- статус механизмов проверки зафиксирован честно: evals и golden-set в
  репозитории отсутствуют, и это отражено в документах и в бэклоге;
- зафиксированы варианты инструментария веб-ресурса после приватизации;
- frontmatter концептуальных документов содержит status/version/updated/owner.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CONCEPT_DOCS = (
    "README.md",
    "AI_GOVERNANCE.md",
    "docs/ba-ecosystem.md",
    "docs/rfc-hub-integration.md",
    "docs/hub-research-dependencies.md",
    "pr-ops/artifact-map.md",
)

REQUIRED_FRONTMATTER = ("status:", "version:", "updated:", "owner:")

NEW_HUB_ANCHORS = (
    "adr-009-repo-split",
    "ba-process-ontology",
    "separation-readiness",
)

# Прямые hub-относительные ссылки запрещены: мост один — реестр зависимостей.
FORBIDDEN_LINK = re.compile(r"\]\(\.\./\.\./(standards|research|docs)/")

# Внутренний жаргон и концепты проекта БИЛД в концептуальных документах спока.
FORBIDDEN_TERMS = (
    "фаундер",
    "Фаундер",
    "Конард",
    "Proof of Execution",
    "Learning loop",
    "S1-S5",
    "S1–S5",
)

# Варианты инструментария веб-ресурса после приватизации (блокер Q1).
WEB_RESOURCE_VARIANTS = (
    "open-ai.ru",
    "Поэтапная миграция",
    "Кастомное решение через `ai-ba-playbooks`",
)

# Пробел evals фиксируется честно, а не маскируется.
EVALS_GAP_MARKERS = {
    "AI_GOVERNANCE.md": (
        "Статус механизмов проверки на сегодня",
        "нет каталога `evals/` и нет golden-set",
    ),
    "pr-ops/BACKLOG.md": (
        "evals и golden-set отсутствуют",
        "инструментарий веб-ресурса (app)",
    ),
}

REQUIRED_TEXT = {
    "AI_GOVERNANCE.md": (
        "качество системы исполнения > стоимость",
        "Операция без процесса проверки считается незавершённой",
        "чек-лист",
        "evals-метрика",
        "human-in-the-loop gate",
        "GitHub — единственная платформа",
        "AI-исполнитель",
        "Подготовка к приватизации",
        "Статус механизмов проверки на сегодня",
        "Веб-ресурс (app) после приватизации",
        "ai-ba-playbooks",
    ),
    "README.md": (
        "качество системы исполнения > стоимость",
        "Операция без процесса проверки считается незавершённой",
        "Private",
        "ai-ba-playbooks",
        "телеком",
        "evals и golden-set отсутствуют",
    ),
    "docs/ba-ecosystem.md": (
        "ДОД операции: процесс проверки обязателен",
        "ai-ba-playbooks",
    ),
    "docs/rfc-hub-integration.md": (
        "Два адресата исходящего потока",
        "строго односторонний",
        "неавтоматическая",
        "ai-ba-playbooks",
        "Универсальные и специализированные плейбуки",
        "Отбор Пользователем",
        "конструктору",
    ),
    "pr-ops/artifact-map.md": (
        "ADR-009",
        "ai-ba-playbooks",
    ),
}


def read_text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def frontmatter(text: str) -> str:
    if not text.startswith("---\n"):
        return ""
    end = text.find("\n---\n", 4)
    return text[4:end] if end != -1 else ""


def check_frontmatter() -> list[str]:
    errors: list[str] = []
    for path in CONCEPT_DOCS:
        block = frontmatter(read_text(path))
        if not block:
            errors.append(f"{path}: frontmatter-блок не найден")
            continue
        for field in REQUIRED_FRONTMATTER:
            if field not in block:
                errors.append(f"{path}: во frontmatter нет поля {field!r}")
    return errors


def check_required_text() -> list[str]:
    errors: list[str] = []
    for path, needles in REQUIRED_TEXT.items():
        text = read_text(path)
        for needle in needles:
            if needle not in text:
                errors.append(f"{path}: отсутствует формулировка {needle!r}")
    return errors


def check_hub_bridge() -> list[str]:
    errors: list[str] = []
    registry = read_text("docs/hub-research-dependencies.md")
    for anchor in NEW_HUB_ANCHORS:
        if f'<a id="{anchor}"></a>' not in registry:
            errors.append(
                f"docs/hub-research-dependencies.md: нет якоря #{anchor}"
            )
        if f"#{anchor}" not in registry:
            errors.append(
                f"docs/hub-research-dependencies.md: якорь #{anchor} не в сводной таблице"
            )

    consumers = {
        "adr-009-repo-split": ("README.md", "AI_GOVERNANCE.md"),
        "ba-process-ontology": ("AI_GOVERNANCE.md", "docs/ba-ecosystem.md"),
        "separation-readiness": ("AI_GOVERNANCE.md",),
    }
    for anchor, paths in consumers.items():
        for path in paths:
            if f"hub-research-dependencies.md#{anchor}" not in read_text(path):
                errors.append(f"{path}: нет ссылки на якорь #{anchor}")
    return errors


def check_forbidden_terms() -> list[str]:
    """Концептуальные документы должны читаться независимым читателем."""
    errors: list[str] = []
    for path in CONCEPT_DOCS:
        for number, line in enumerate(read_text(path).splitlines(), start=1):
            for term in FORBIDDEN_TERMS:
                if term in line:
                    errors.append(
                        f"{path}:{number}: запрещённый термин {term!r} "
                        "в концептуальном документе"
                    )
    return errors


def check_evals_status() -> list[str]:
    """Отсутствие evals фиксируется честно, а не подразумевается."""
    errors: list[str] = []
    if (ROOT / "evals").exists():
        errors.append(
            "evals/: каталог появился — обнови «Статус механизмов проверки "
            "на сегодня» в AI_GOVERNANCE.md и запись в pr-ops/BACKLOG.md"
        )
    for path, needles in EVALS_GAP_MARKERS.items():
        text = read_text(path)
        for needle in needles:
            if needle not in text:
                errors.append(f"{path}: отсутствует фиксация пробела {needle!r}")
    return errors


def check_web_resource_variants() -> list[str]:
    """Блокер Q1: канал публикации веб-ресурса после перевода в Private."""
    text = read_text("AI_GOVERNANCE.md")
    errors = [
        f"AI_GOVERNANCE.md: не зафиксирован вариант веб-ресурса {variant!r}"
        for variant in WEB_RESOURCE_VARIANTS
        if variant not in text
    ]
    if "GitHub Pages не работает для приватных репозиториев" not in text:
        errors.append(
            "AI_GOVERNANCE.md: не зафиксировано ограничение GitHub Pages "
            "для приватных репозиториев"
        )
    return errors


def check_no_direct_hub_links() -> list[str]:
    errors: list[str] = []
    for path in CONCEPT_DOCS:
        for number, line in enumerate(read_text(path).splitlines(), start=1):
            if FORBIDDEN_LINK.search(line):
                errors.append(
                    f"{path}:{number}: прямая hub-относительная ссылка запрещена"
                )
    return errors


def check_ci_wiring() -> list[str]:
    workflow = read_text(".github/workflows/github-pages.yml")
    needle = "python3 scripts/validate_issue_263_vision_alignment.py"
    return [] if needle in workflow else [
        f".github/workflows/github-pages.yml: не подключён шаг {needle!r}"
    ]


def check_changelog() -> list[str]:
    changelog = read_text("CHANGELOG.md")
    return [] if "Issue #263" in changelog else [
        "CHANGELOG.md: нет записи об issue #263 в `## Unreleased`"
    ]


def main() -> int:
    errors = (
        check_frontmatter()
        + check_required_text()
        + check_forbidden_terms()
        + check_evals_status()
        + check_web_resource_variants()
        + check_hub_bridge()
        + check_no_direct_hub_links()
        + check_ci_wiring()
        + check_changelog()
    )
    if errors:
        print("Issue #263 vision alignment validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Issue #263 vision alignment validation passed.")
    for path in CONCEPT_DOCS:
        print(f"- {path}: концептуальный контракт соблюдён")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
