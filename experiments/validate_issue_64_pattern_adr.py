#!/usr/bin/env python3
"""Local regression check for issue #64 pattern-standard ADR."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ADR = ROOT / "docs/adr/002-pattern-standard.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def require(text: str, path: str, *needles: str) -> list[str]:
    errors = []
    for needle in needles:
        if needle not in text:
            errors.append(f"{path}: missing {needle!r}")
    return errors


def require_existing_links(text: str, path: str) -> list[str]:
    errors = []
    for relative in (
        "patterns/README.md",
        "standards/pattern-standard.md",
        "standards/prompt-standard.md",
        "docs/taxonomy.md",
        "docs/ba-processes/00-index.md",
    ):
        if relative not in text:
            errors.append(f"{path}: missing reference to {relative}")
        if not (ROOT / relative).exists():
            errors.append(f"{relative}: referenced local file does not exist")
    return errors


def main() -> int:
    path = "docs/adr/002-pattern-standard.md"
    errors: list[str] = []

    if not ADR.exists():
        errors.append(f"{path}: file does not exist")
    else:
        text = read(ADR)
        errors += require(
            text,
            path,
            "# ADR",
            "Контекст",
            "Решение",
            "Последствия",
            "Примеры",
            "purpose",
            "process_stage",
            "context_requirements",
            "prompt_template",
            "quality_gates",
            "examples",
            "output_schema",
            "governance_rules",
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
            "Формирование ФТ/ТЗ",
            "Валидация ФТ/ТЗ",
            "Анализ тендерных ТЗ",
            "Формирование UC/US",
            "Визуализация UML/BPMN",
            "Помощь ПО/ПМ",
            "Статистика",
            "Impact Analysis",
            "Risk Analysis",
            "LLM-агност",
            "frontmatter",
            "major",
            "minor",
            "patch",
            "https://github.com/G-Ivan-A/mango_ba_prompts/issues/64",
            "https://github.com/G-Ivan-A/mango_ba_prompts/pull/60",
            "https://github.com/G-Ivan-A/mango_ba_prompts/pull/57",
            "https://github.com/G-Ivan-A/mango_ba_prompts/pull/59",
            "https://github.com/G-Ivan-A/mango_ba_prompts/issues/61",
            "https://github.com/G-Ivan-A/hybrid-Intelligence-lab",
        )
        errors += require_existing_links(text, path)

    if errors:
        print("issue-64 pattern ADR validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("issue-64 pattern ADR validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
