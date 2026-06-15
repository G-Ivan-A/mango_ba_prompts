#!/usr/bin/env python3
"""Local regression check for issue #85 patterns-library MVP."""

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]

FIELDS = [
    "purpose",
    "process_stage",
    "context_requirements",
    "prompt_template",
    "quality_gates",
    "examples",
    "output_schema",
    "governance_rules",
]

PATTERNS = {
    "glossary-context-generation": {
        "operation": "understanding",
        "processes": ["Формирование ФТ/ТЗ", "Анализ тендерных ТЗ"],
        "prompts": [
            "glossary-context-understanding-stepwise.md",
            "glossary-context-understanding-oneshot.md",
        ],
    },
    "fr-generation": {
        "operation": "documentation",
        "processes": ["Формирование ФТ/ТЗ"],
        "prompts": ["fr-documentation-stepwise.md", "fr-documentation-oneshot.md"],
    },
    "fr-validation": {
        "operation": "validation",
        "processes": ["Валидация ФТ/ТЗ"],
        "prompts": [
            "fr-validation-stepwise.md",
            "fr-validation-oneshot.md",
            "fr-validation-legacy.md",
        ],
    },
    "user-story-generation": {
        "operation": "modeling",
        "processes": ["Формирование UC/US"],
        "prompts": ["us-modeling-stepwise.md", "us-modeling-oneshot.md"],
    },
    "usecase-generation": {
        "operation": "modeling",
        "processes": ["Формирование UC/US"],
        "prompts": ["uc-modeling-stepwise.md", "uc-modeling-oneshot.md"],
    },
    "asr-ingestion": {
        "operation": "ingestion",
        "processes": ["Формирование ФТ/ТЗ", "Помощь ПО/ПМ"],
        "prompts": ["asr-ingestion-oneshot.md", "asr-ingestion-legacy.md"],
    },
    "meeting-summary-generation": {
        "operation": "documentation",
        "processes": ["Помощь ПО/ПМ"],
        "prompts": [
            "meeting-customer-documentation-stepwise.md",
            "meeting-team-documentation-stepwise.md",
        ],
    },
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def markdown_links(markdown: str) -> list[str]:
    return re.findall(r"\[[^\]]+]\(([^)]+)\)", markdown)


def require_ordered_fields(text: str, relative: str) -> list[str]:
    errors = []
    position = -1
    for field in FIELDS:
        marker = f"## {field}"
        new_position = text.find(marker)
        if new_position == -1:
            errors.append(f"{relative}: missing section {marker}")
        elif new_position <= position:
            errors.append(f"{relative}: section {marker} is out of order")
        position = new_position
    return errors


def require_local_links_exist(text: str, relative: str) -> list[str]:
    errors = []
    for link in markdown_links(text):
        if link.startswith(("http://", "https://", "#", "mailto:")):
            continue
        target = link.split("#", 1)[0]
        if not target:
            continue
        if not (ROOT / relative).parent.joinpath(target).resolve().exists():
            errors.append(f"{relative}: broken local link {link}")
    return errors


def require_pattern_readme(slug: str, metadata: dict[str, object]) -> list[str]:
    errors = []
    directory = ROOT / "patterns" / slug
    readme = directory / "README.md"
    examples_dir = directory / "examples"
    relative = f"patterns/{slug}/README.md"

    if not directory.is_dir():
        return [f"patterns/{slug}: directory does not exist"]
    if not examples_dir.is_dir():
        errors.append(f"patterns/{slug}/examples: directory does not exist")
    if not any(examples_dir.iterdir()):
        errors.append(f"patterns/{slug}/examples: directory is empty")
    if not readme.exists():
        errors.append(f"{relative}: file does not exist")
        return errors

    text = read(readme)
    errors += require_ordered_fields(text, relative)
    errors += require_local_links_exist(text, relative)

    for needle in (
        "status: draft",
        "version: 0.1.0",
        "updated: 2026-06-15",
        "Product Layer",
        "Commercial Layer",
        "Правила адаптации",
        "LLM-агност",
        "source of truth",
        "https://github.com/G-Ivan-A/mango_ba_prompts",
    ):
        if needle not in text:
            errors.append(f"{relative}: missing {needle!r}")

    operation = metadata["operation"]
    if f"`{operation}`" not in text:
        errors.append(f"{relative}: missing operation `{operation}`")
    for process in metadata["processes"]:
        if process not in text:
            errors.append(f"{relative}: missing process {process!r}")
    for prompt in metadata["prompts"]:
        if prompt not in text:
            errors.append(f"{relative}: missing prompt {prompt}")
        if not (ROOT / "prompts" / prompt).exists():
            errors.append(f"prompts/{prompt}: referenced prompt does not exist")

    return errors


def require_patterns_index() -> list[str]:
    path = ROOT / "patterns" / "README.md"
    relative = "patterns/README.md"
    if not path.exists():
        return [f"{relative}: file does not exist"]
    text = read(path)
    errors = require_local_links_exist(text, relative)
    for slug, metadata in PATTERNS.items():
        for needle in (
            f"patterns/{slug}/",
            f"[`{slug}`]({slug}/)",
            metadata["operation"],
        ):
            if needle not in text:
                errors.append(f"{relative}: missing {needle!r}")
        for prompt in metadata["prompts"]:
            if prompt not in text:
                errors.append(f"{relative}: missing prompt {prompt}")
    for needle in (
        "Навигация по MVP-паттернам",
        "Матрица: паттерн ↔ процесс ↔ операция ↔ промпты",
        "Пример использования",
        "docs/taxonomy.md",
        "docs/ba-processes/00-index.md",
        "prompts/README.md",
        "docs/ba-ecosystem.md",
        "https://github.com/G-Ivan-A/mango_ba_prompts/pull/70",
        "https://github.com/G-Ivan-A/mango_ba_prompts/pull/67",
        "https://github.com/G-Ivan-A/mango_ba_prompts/pull/69",
        "https://github.com/G-Ivan-A/mango_ba_prompts/pull/60",
        "https://github.com/G-Ivan-A/hybrid-Intelligence-lab",
    ):
        if needle not in text:
            errors.append(f"{relative}: missing {needle!r}")
    return errors


def require_process_registry() -> list[str]:
    path = ROOT / "docs/ba-processes/00-index.md"
    relative = "docs/ba-processes/00-index.md"
    if not path.exists():
        return [f"{relative}: file does not exist"]
    text = read(path)
    errors = require_local_links_exist(text, relative)
    for slug, metadata in PATTERNS.items():
        if f"../../patterns/{slug}/" not in text:
            errors.append(f"{relative}: missing central registry link for {slug}")
        for prompt in metadata["prompts"]:
            if f"../../prompts/{prompt}" not in text:
                errors.append(f"{relative}: missing prompt registry link for {prompt}")
    return errors


def require_changelog() -> list[str]:
    text = read(ROOT / "CHANGELOG.md")
    errors = []
    for needle in ("Issue #85", "patterns/README.md", "validate_issue_85_patterns_library.py"):
        if needle not in text:
            errors.append(f"CHANGELOG.md: missing {needle!r}")
    return errors


def main() -> int:
    errors = []
    for slug, metadata in PATTERNS.items():
        errors += require_pattern_readme(slug, metadata)
    errors += require_patterns_index()
    errors += require_process_registry()
    errors += require_changelog()

    if errors:
        print("issue-85 patterns library validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("issue-85 patterns library validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
