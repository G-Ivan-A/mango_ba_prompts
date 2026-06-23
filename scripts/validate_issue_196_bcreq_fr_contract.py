#!/usr/bin/env python3
"""Regression check for issue #196: BCREQ-FR generation contract."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

CONTRACT = "governance/bcreq-fr-generation-contract.md"
VALIDATOR = "scripts/validate_issue_196_bcreq_fr_contract.py"
ISSUE_208_VALIDATOR = "scripts/validate_issue_208_bcreq_fr_l3_boundary.py"

REQUIRED_CONTRACT_TEXT = (
    "id: bcreq-fr-generation-contract",
    "status: active",
    "version: 0.3",
    "type: contract",
    "executable: true",
    "machine_readable: true",
    "https://github.com/G-Ivan-A/mango_ba_prompts/issues/196",
    "https://github.com/G-Ivan-A/mango_ba_prompts/issues/208",
    'comment: "Вложения из PR #202"',
    'status: "temporary"',
    'trace: "https://github.com/G-Ivan-A/mango_ba_prompts/pull/202"',
    "Правила RFC-184 встроены в §3 (BCREQ-FR-GEN-SCOPE-01/02)",
    "kb/industry-taxonomy/registry.json",
    "kb/mango-taxonomy/registry.json",
    "RFC-184-S1",
    "RFC-184-S2",
    "BCREQ-FR-GEN-SCOPE-01",
    "BCREQ-FR-GEN-SCOPE-02",
    "BCREQ-FR-SECTION-01",
    "BCREQ-FR-SECTION-02",
    "BCREQ-FR-SECTION-03",
    "BCREQ-FR-SECTION-04",
    "BCREQ-FR-SECTION-05-STUB",
    "BCREQ-FR-SECTION-06",
    "BCREQ-FR-SECTION-07-STUB",
    "BCREQ-FR-VALIDATION-SUMMARY",
    "generation_enabled: false",
    "Раздел 5",
    "Раздел 7",
    "FR-01",
    "4.x.x",
    "4.x.x.x",
    '"Система должна предоставлять"',
    '"Комментарии: резюме тестирования и валидации"',
    ISSUE_208_VALIDATOR,
)

FORBIDDEN_CONTRACT_TEXT = (
    "github.com/user-attachments",
    "`rfc_184`",
    "governance/rfc/bcreq-ft-scope-formation-rules-proposal.md",
    "standards/industry-taxonomy-standard.md",
    "standards/mango-taxonomy-standard.md",
)

REQUIRED_SECTION_MARKERS = (
    "## 1. Назначение",
    "## 2. Входные данные",
    "## 3. Machine-readable index",
    "## 4. Процесс генерации",
    "## 5. Правила разделов результата",
    "## 6. Правила стиля и трассируемости",
    "## 7. Валидация",
    "## 8. Формат результата",
    "## Источники",
)

REQUIRED_PROJECT_TEXT = {
    "CHANGELOG.md": ("Issue #196", CONTRACT, VALIDATOR),
    "README.md": (CONTRACT,),
    "governance/artifact-map.md": (CONTRACT,),
    ".github/workflows/github-pages.yml": (
        "Validate issue #196 BCREQ-FR generation contract",
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


def reject_text(path: str, *needles: str) -> list[str]:
    errors = require_path(path)
    if errors:
        return errors
    text = read_text(path)
    return [f"{path}: forbidden text {needle!r}" for needle in needles if needle in text]


def check_contract_order() -> list[str]:
    errors = require_path(CONTRACT)
    if errors:
        return errors

    text = read_text(CONTRACT)
    positions = []
    for marker in REQUIRED_SECTION_MARKERS:
        position = text.find(marker)
        if position == -1:
            errors.append(f"{CONTRACT}: missing section marker {marker!r}")
        else:
            positions.append(position)

    if positions != sorted(positions):
        errors.append(f"{CONTRACT}: sections must preserve contract order")
    return errors


def check_project_wiring() -> list[str]:
    errors: list[str] = []
    for path, needles in REQUIRED_PROJECT_TEXT.items():
        errors += require_text(path, *needles)
    return errors


def main() -> int:
    errors: list[str] = []
    errors += require_text(CONTRACT, *REQUIRED_CONTRACT_TEXT)
    errors += reject_text(CONTRACT, *FORBIDDEN_CONTRACT_TEXT)
    errors += check_contract_order()
    errors += check_project_wiring()

    if errors:
        print("Issue #196 BCREQ-FR contract validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Issue #196 BCREQ-FR contract validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
