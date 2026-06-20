#!/usr/bin/env python3
"""Regression check for issue #127 — BA ontology sync with Hub RFCs.

The check locks the three requested sync points:

- C1: requirement level is an orthogonal tag axis, not a replacement for the
  existing Domain -> Capability -> Feature -> Atomic Function classification;
- C2: business-rule is an explicit artifact type with the five Wiegers
  categories;
- C3: a crosswalk links Wiegers processes to mango operations and BCREQ
  subprocesses.

Run: ``python3 scripts/validate_issue_127_hub_rfc_sync.py``.
"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

WIEGERS_RFC = "requirements-engineering-ai-era-2026.md"
AI_RFC = "ai-classifications-formalization-2026-06.md"
CROSSWALK = "docs/requirements-engineering-crosswalk.md"
VALIDATOR = "scripts/validate_issue_127_hub_rfc_sync.py"


def read_text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def require_path(path: str) -> list[str]:
    return [] if (ROOT / path).exists() else [f"{path}: missing"]


def require_text(path: str, *needles: str) -> list[str]:
    errors = require_path(path)
    if errors:
        return errors
    text = read_text(path)
    return [f"{path}: missing {needle!r}" for needle in needles if needle not in text]


def check_ontology_standard() -> list[str]:
    path = "standards/ba-ontology.md"
    errors = require_text(
        path,
        "requirement_level",
        "`business`",
        "`user`",
        "`functional`",
        "`non-functional`",
        "Domain→Capability→Feature→Atomic Function",
        "R13",
        "| A31 | `business-rule`",
        "Факты",
        "Ограничения",
        "Активаторы операций",
        "Выводы",
        "Вычисления",
        WIEGERS_RFC,
        AI_RFC,
        VALIDATOR,
    )
    if errors:
        return errors

    text = read_text(path)
    if text.find("requirement_level") > text.find("| A31 | `business-rule`"):
        errors.append(
            f"{path}: requirement_level axis must be described before the "
            "business-rule artifact registry row"
        )
    return errors


def check_executable_companion() -> list[str]:
    return require_text(
        "standards/ba-ontology.executable.md",
        "requirement_level",
        "`business`",
        "`user`",
        "`functional`",
        "`non-functional`",
        "R13",
        "A31 business-rule",
    )


def check_crosswalk() -> list[str]:
    path = CROSSWALK
    errors = require_text(
        path,
        "Вигерс",
        "mango",
        "BCREQ",
        WIEGERS_RFC,
        AI_RFC,
        "Выявление / Elicitation",
        "Анализ / Analysis",
        "Спецификация / Specification",
        "Проверка / Validation",
        "Управление / Management",
        "`ingestion`",
        "`understanding`",
        "`modeling`",
        "`research`",
        "`impact_analysis`",
        "`reverse_requirements`",
        "`documentation`",
        "`solution_design`",
        "`validation`",
        "`quality`",
        "`governance`",
        "`release_readiness`",
        "`risk_analysis`",
        "П1",
        "П2",
        "П3",
        "П4",
        "П5",
        "П6",
    )
    if errors:
        return errors

    text = read_text(path)
    for forbidden in ("Prompt engineering", "Инжиниринг промптов", "Настройка RAG"):
        if forbidden in text:
            errors.append(
                f"{path}: out-of-scope AI subprocess {forbidden!r} must not be "
                "introduced by issue #127"
            )
    return errors


def check_decision_docs() -> list[str]:
    errors: list[str] = []
    errors += require_text(
        "docs/adr/003-ba-ontology.md",
        "requirement_level",
        "`business-rule`",
        "Бизнес-правило",
        WIEGERS_RFC,
        AI_RFC,
    )
    errors += require_text(
        "docs/adr/004-operations-taxonomy.md",
        CROSSWALK,
        "Вигерс",
        "C3",
        WIEGERS_RFC,
        AI_RFC,
    )
    errors += require_text(
        "docs/taxonomy.md",
        CROSSWALK,
        "Вигерс",
        WIEGERS_RFC,
        AI_RFC,
    )
    return errors


def check_project_wiring() -> list[str]:
    errors: list[str] = []
    errors += require_text(
        "README.md",
        "requirement_level",
        "business-rule",
        CROSSWALK,
        WIEGERS_RFC,
        AI_RFC,
    )
    errors += require_text(
        "docs/hub-research-dependencies.md",
        "requirements-engineering-ai-era",
        "ai-classifications-formalization",
        WIEGERS_RFC,
        AI_RFC,
    )
    errors += require_text("CHANGELOG.md", "Issue #127", "C1", "C2", "C3", VALIDATOR)
    errors += require_text(
        ".github/workflows/github-pages.yml",
        "Validate issue #127 Hub RFC sync",
        VALIDATOR,
    )
    return errors


def main() -> int:
    errors: list[str] = []
    errors += check_ontology_standard()
    errors += check_executable_companion()
    errors += check_crosswalk()
    errors += check_decision_docs()
    errors += check_project_wiring()

    if errors:
        print("Issue #127 Hub RFC sync validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Issue #127 Hub RFC sync validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
