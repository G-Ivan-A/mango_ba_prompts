#!/usr/bin/env python3
"""Regression check for issue #193: AI document approval contract."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

CONTRACT = "governance/contracts/approval-contract.md"
TEST_EVIDENCE = "docs/analysis/approval-contract-test-industry-rfc.md"
VALIDATOR = "scripts/validate_issue_193_approval_contract.py"

REQUIRED_CONTRACT_TEXT = (
    "id: approval-contract",
    "type: contract",
    "executable: true",
    "## 1. Подготовка к согласованию",
    "## 2. Итеративное согласование по разделам",
    "## 3. Принципы согласования",
    "## 4. Обработка отсутствующей конкретики",
    "## 5. Завершение согласования",
    "## 6. Особые случаи",
    "## 7. Роль AI в согласовании",
    "## 8. Применение правил",
    "Запусти процесс согласования для файла",
    "Согласуй документ по контракту",
    "Проведи атомарное согласование",
    "В разделе конкретных предложений НЕТ",
    "НЕ переходить к следующему разделу",
    "AI не принимает решения",
    "RFC",
    "ADR",
    "Standards",
    "Research documents",
    "Analysis documents",
)

REQUIRED_TEST_TEXT = (
    CONTRACT,
    "docs/analysis/rfc-industry-taxonomy-improvement.md",
    "## 1. Тестовый запуск",
    "## 2. Проверка структуры документа",
    "## 3. Пакет согласования для раздела 1",
    "## 4. Результат проверки контракта",
    "Стоп-условие атомарности",
    "В разделе конкретных предложений НЕТ",
    "standards/industry-taxonomy-standard.md",
    "docs/analysis/taxonomy-convergence-test.md",
    "docs/analysis/mango-taxonomy-convergence-test.md",
)

REQUIRED_PROJECT_TEXT = {
    "CHANGELOG.md": ("Issue #193", CONTRACT, TEST_EVIDENCE, VALIDATOR),
    "README.md": (CONTRACT,),
    "governance/artifact-map.md": ("`/governance/contracts/`", CONTRACT),
    ".github/workflows/github-pages.yml": (
        "Validate issue #193 approval contract",
        VALIDATOR,
    ),
}


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


def check_contract_order() -> list[str]:
    errors = require_path(CONTRACT)
    if errors:
        return errors

    text = read_text(CONTRACT)
    positions = []
    for section_number in range(1, 9):
        marker = f"## {section_number}. "
        position = text.find(marker)
        if position == -1:
            errors.append(f"{CONTRACT}: missing section marker {marker!r}")
        else:
            positions.append(position)

    if positions != sorted(positions):
        errors.append(f"{CONTRACT}: founder-rule sections must preserve order 1..8")
    return errors


def check_project_wiring() -> list[str]:
    errors: list[str] = []
    for path, needles in REQUIRED_PROJECT_TEXT.items():
        errors += require_text(path, *needles)
    return errors


def main() -> int:
    errors: list[str] = []
    errors += require_text(CONTRACT, *REQUIRED_CONTRACT_TEXT)
    errors += check_contract_order()
    errors += require_text(TEST_EVIDENCE, *REQUIRED_TEST_TEXT)
    errors += check_project_wiring()

    if errors:
        print("Issue #193 approval contract validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Issue #193 approval contract validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
