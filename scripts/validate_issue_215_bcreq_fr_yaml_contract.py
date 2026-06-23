#!/usr/bin/env python3
"""Regression check for issue #215: BCREQ-FR contract is a pure YAML contract."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

CONTRACT = "governance/bcreq-fr-generation-contract.md"
REGISTRY = "governance/contracts-registry.md"
VALIDATOR = "scripts/validate_issue_215_bcreq_fr_yaml_contract.py"

REQUIRED_CONTRACT_TEXT = (
    "id: bcreq-fr-generation-contract",
    "status: active",
    "version: 0.4",
    "contract_registry_id: bcreq-fr-generation-contract",
    "contract_id: bcreq-fr-generation-contract",
    "artifact_type: bcreq-fr",
    "output_language: ru",
    "normative_keywords:",
    "source_priority:",
    "BCREQ-FR-GEN-SCOPE-01",
    "BCREQ-FR-GEN-SCOPE-02",
    "BCREQ-FR-SECTION-01",
    "BCREQ-FR-SECTION-07-STUB",
    "generation_process:",
    "section_rules:",
    "style_rules:",
    "traceability:",
    "validation:",
    "output_format:",
    "self_review:",
)

FORBIDDEN_CONTRACT_TEXT = (
    "```",
    "| Вход | Обязательность | Правило чтения |",
    "| Подраздел | Правило |",
    "| ID | Проверка | Условие pass |",
    "## 1. Назначение",
    "## 2. Входные данные",
    "## 3. Machine-readable index",
    "## 4. Процесс генерации",
    "## 5. Правила разделов результата",
    "## 6. Правила стиля и трассируемости",
    "## 7. Валидация",
    "## 8. Формат результата",
    "## Источники и происхождение контракта",
    "https://github.com/G-Ivan-A/mango_ba_prompts/issues/196",
    "https://github.com/G-Ivan-A/mango_ba_prompts/issues/208",
    "https://github.com/G-Ivan-A/mango_ba_prompts/issues/211",
    "https://github.com/G-Ivan-A/mango_ba_prompts/pull/202",
)

REQUIRED_REGISTRY_TEXT = (
    "# Реестр исполнимых контрактов",
    "contracts:",
    "id: bcreq-fr-generation-contract",
    "version: 0.4",
    "status: active",
    "layer: L1",
    "rule_class: combat",
    "provenance:",
    "https://github.com/G-Ivan-A/mango_ba_prompts/issues/196",
    "https://github.com/G-Ivan-A/mango_ba_prompts/issues/208",
    "https://github.com/G-Ivan-A/mango_ba_prompts/issues/211",
    "https://github.com/G-Ivan-A/mango_ba_prompts/pull/202",
    "kb/industry-taxonomy/registry.json",
    "kb/mango-taxonomy/registry.json",
    "scripts/validate_issue_196_bcreq_fr_contract.py",
    "scripts/validate_issue_208_bcreq_fr_l3_boundary.py",
    VALIDATOR,
)

REQUIRED_PROJECT_TEXT = {
    "CHANGELOG.md": ("Issue #215", CONTRACT, REGISTRY, VALIDATOR),
    "README.md": (CONTRACT, REGISTRY),
    "governance/artifact-map.md": (CONTRACT, REGISTRY),
    ".github/workflows/github-pages.yml": (
        "Validate issue #215 BCREQ-FR YAML contract",
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


def parse_yaml_stream(path: str) -> tuple[list[object] | None, list[str]]:
    """Parse a YAML stream via Ruby Psych, available on GitHub-hosted Ubuntu."""

    errors = require_path(path)
    if errors:
        return None, errors

    command = (
        "require 'yaml';"
        "require 'json';"
        "docs = YAML.load_stream(File.read(ARGV[0]));"
        "puts JSON.generate(docs)"
    )
    result = subprocess.run(
        ["ruby", "-e", command, str(ROOT / path)],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip().splitlines()
        message = detail[-1] if detail else "unknown parser error"
        return None, [f"{path}: must parse as YAML stream: {message}"]

    return json.loads(result.stdout), []


def check_contract_yaml_shape() -> list[str]:
    docs, errors = parse_yaml_stream(CONTRACT)
    if errors:
        return errors

    if not isinstance(docs, list) or len(docs) != 2:
        return [f"{CONTRACT}: expected two YAML documents: metadata and contract body"]

    metadata, body = docs
    if not isinstance(metadata, dict):
        errors.append(f"{CONTRACT}: first YAML document must be metadata mapping")
    if not isinstance(body, dict):
        errors.append(f"{CONTRACT}: second YAML document must be contract body mapping")
        return errors

    expected_first_keys = (
        "contract_id",
        "artifact_type",
        "output_language",
        "normative_keywords",
    )
    actual_first_keys = list(body.keys())[: len(expected_first_keys)]
    if tuple(actual_first_keys) != expected_first_keys:
        errors.append(
            f"{CONTRACT}: body must start with YAML rule index keys "
            f"{expected_first_keys!r}, got {actual_first_keys!r}"
        )

    if metadata.get("contract_registry_id") != "bcreq-fr-generation-contract":
        errors.append(f"{CONTRACT}: metadata must use contract_registry_id only")
    if "issue" in metadata or "source_attachments" in metadata:
        errors.append(f"{CONTRACT}: provenance/runtime source fields must move out of metadata")

    for key in (
        "scope_rules",
        "inputs",
        "source_priority",
        "sections",
        "generation_process",
        "section_rules",
        "style_rules",
        "traceability",
        "validation",
        "output_format",
    ):
        if key not in body:
            errors.append(f"{CONTRACT}: body missing top-level key {key!r}")

    return errors


def check_registry_yaml_shape() -> list[str]:
    docs, errors = parse_yaml_stream(REGISTRY)
    if errors:
        return errors

    if not isinstance(docs, list) or len(docs) != 1 or not isinstance(docs[0], dict):
        return [f"{REGISTRY}: expected one YAML mapping document"]

    contracts = docs[0].get("contracts")
    if not isinstance(contracts, list):
        return [f"{REGISTRY}: missing contracts list"]

    matching = [item for item in contracts if item.get("id") == "bcreq-fr-generation-contract"]
    if len(matching) != 1:
        return [f"{REGISTRY}: expected exactly one bcreq-fr-generation-contract entry"]

    entry = matching[0]
    errors = []
    for key in ("provenance", "integrates", "related_artifacts", "validated_by"):
        if key not in entry:
            errors.append(f"{REGISTRY}: contract entry missing {key!r}")
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
    errors += require_text(REGISTRY, *REQUIRED_REGISTRY_TEXT)
    errors += check_contract_yaml_shape()
    errors += check_registry_yaml_shape()
    errors += check_project_wiring()

    if errors:
        print("Issue #215 BCREQ-FR YAML contract validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Issue #215 BCREQ-FR YAML contract validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
