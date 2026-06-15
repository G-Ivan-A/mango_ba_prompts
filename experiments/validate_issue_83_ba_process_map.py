#!/usr/bin/env python3
"""Local regression check for issue #83 BA process map."""

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROCESS_MAP = "docs/ba-processes/00-index.md"

OPERATIONS = (
    "ingestion",
    "understanding",
    "validation",
    "modeling",
    "solution_design",
    "documentation",
    "quality",
    "research",
    "governance",
    "impact_analysis",
    "reverse_requirements",
    "risk_analysis",
    "release_readiness",
)

PROCESSES = (
    "Формирование ФТ/ТЗ",
    "Валидация ФТ/ТЗ",
    "Анализ тендерных ТЗ",
    "Формирование UC/US",
    "Визуализация UML/BPMN",
    "Помощь ПО/ПМ",
    "Статистика",
    "Impact Analysis",
    "Risk Analysis",
)

REQUIRED_PROMPTS = (
    "asr-ingestion-oneshot.md",
    "asr-ingestion-legacy.md",
    "glossary-context-understanding-stepwise.md",
    "glossary-context-understanding-oneshot.md",
    "questions-customer-understanding-stepwise.md",
    "questions-customer-understanding-legacy.md",
    "fr-documentation-stepwise.md",
    "fr-documentation-oneshot.md",
    "constraints-documentation-stepwise.md",
    "constraints-documentation-oneshot.md",
    "technical-details-solution-design-stepwise.md",
    "technical-details-solution-design-oneshot.md",
    "technical-details-solution-design-legacy.md",
    "fr-validation-stepwise.md",
    "fr-validation-oneshot.md",
    "fr-validation-legacy.md",
    "uc-modeling-stepwise.md",
    "uc-modeling-oneshot.md",
    "us-modeling-stepwise.md",
    "us-modeling-oneshot.md",
    "meeting-customer-documentation-stepwise.md",
    "meeting-team-documentation-stepwise.md",
    "letter-customer-documentation-legacy.md",
    "session-debug-documentation-oneshot.md",
    "archive/tz-stats-generator-legacy.md",
    "archive/tz-stats-generator-simple-legacy.md",
    "archive/usecase-stepwise-generator-legacy.md",
    "archive/usecase-stepwise-generator-simple-legacy.md",
    "archive/user-story-generator-legacy.md",
    "archive/user-story-generator-simple-legacy.md",
)

REQUIRED_TRACEABILITY_URLS = (
    "https://github.com/G-Ivan-A/mango_ba_prompts/issues/83",
    "https://github.com/G-Ivan-A/mango_ba_prompts/pull/60",
    "https://github.com/G-Ivan-A/mango_ba_prompts/pull/67",
    "https://github.com/G-Ivan-A/mango_ba_prompts/pull/69",
    "https://github.com/G-Ivan-A/mango_ba_prompts/pull/79",
    "https://github.com/G-Ivan-A/hybrid-Intelligence-lab",
    "https://github.com/G-Ivan-A/clarify-engine-ai",
    "https://github.com/G-Ivan-A/open-ai.ru",
    "https://github.com/G-Ivan-A/mango_ba_prompts",
    "https://g-ivan-a.github.io/mango_ba_prompts/",
)


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def require_file(path: str) -> list[str]:
    if not (ROOT / path).exists():
        return [f"{path}: file does not exist"]
    return []


def require(text: str, path: str, *needles: str) -> list[str]:
    return [f"{path}: missing {needle!r}" for needle in needles if needle not in text]


def require_count(text: str, path: str, needle: str, minimum: int) -> list[str]:
    count = text.count(needle)
    if count < minimum:
        return [f"{path}: expected at least {minimum} occurrences of {needle!r}, found {count}"]
    return []


def require_regex(text: str, path: str, pattern: str, description: str) -> list[str]:
    if not re.search(pattern, text, re.MULTILINE | re.DOTALL):
        return [f"{path}: missing {description}"]
    return []


def markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"\[([^\]]+)]\(([^)]+)\)", text)


def main() -> int:
    errors: list[str] = []
    errors += require_file(PROCESS_MAP)
    if errors:
        print("issue-83 BA process map validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    text = read(PROCESS_MAP)

    errors += require(
        text,
        PROCESS_MAP,
        "related_issues:",
        "https://github.com/G-Ivan-A/mango_ba_prompts/issues/83",
        "## Быстрый выбор маршрута",
        "## Режимы запуска промптов",
        "## Детальная карта 9 процессов",
        "## Known gaps",
        "## Примеры запуска",
        "## Навигация и traceability",
    )

    for operation in OPERATIONS:
        errors += require(text, PROCESS_MAP, f"`{operation}`")

    for process in PROCESSES:
        errors += require_regex(
            text,
            PROCESS_MAP,
            rf"^### [0-9]+\. {re.escape(process)}$",
            f"process section for {process}",
        )
        process_section = re.search(
            rf"^### [0-9]+\. {re.escape(process)}$(.*?)(?=^### [0-9]+\. |\Z)",
            text,
            re.MULTILINE | re.DOTALL,
        )
        if not process_section:
            continue
        section = process_section.group(1)
        errors += require(section, f"{PROCESS_MAP}#{process}", "**Цель.**", "**Входы.**", "**Выходы.**")
        for header in ("| Шаг | Операция | Что получить | Промпты | Gate / gap |",):
            errors += require(section, f"{PROCESS_MAP}#{process}", header)

    for prompt in REQUIRED_PROMPTS:
        path = ROOT / "prompts" / prompt
        if not path.exists():
            errors.append(f"prompts/{prompt}: expected prompt file to exist")
        errors += require(text, PROCESS_MAP, f"../../prompts/{prompt}")

    for url in REQUIRED_TRACEABILITY_URLS:
        errors += require(text, PROCESS_MAP, url)

    errors += require_count(text, PROCESS_MAP, "```mermaid", 4)
    errors += require_count(text, PROCESS_MAP, "Требуется разработка промпта", 5)
    errors += require_count(text, PROCESS_MAP, "Выполняется вручную", 3)
    errors += require_count(text, PROCESS_MAP, "Product Layer", 3)
    errors += require_count(text, PROCESS_MAP, "Commercial Layer", 3)

    for scenario in ("Клиентский заказ", "Внутренняя доработка продукта", "Тендерное предложение"):
        errors += require(text, PROCESS_MAP, scenario)

    for label, target in markdown_links(text):
        if target.startswith(("http://", "https://", "#", "mailto:")):
            continue
        if " " in target:
            target = target.split(" ", 1)[0]
        target = target.split("#", 1)[0]
        if not target:
            continue
        resolved = (ROOT / PROCESS_MAP).parent / target
        if not resolved.resolve().exists():
            errors.append(f"{PROCESS_MAP}: broken relative link {target!r} from label {label!r}")

    changelog = read("CHANGELOG.md")
    errors += require(changelog, "CHANGELOG.md", "Issue #83", "карта процессов БА")

    if errors:
        print("issue-83 BA process map validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("issue-83 BA process map validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
