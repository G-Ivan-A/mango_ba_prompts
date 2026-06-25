#!/usr/bin/env python3
"""Regression check for issue #212: executable contract standard."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STANDARD = "standards/executable-contract-standard.md"
CONTRACTS_REGISTRY = "governance/contracts-registry.md"
CHANGELOG = "CHANGELOG.md"
README = "README.md"
WORKFLOW = ".github/workflows/github-pages.yml"
VALIDATOR = "scripts/validate_issue_212_executable_contract_standard.py"

REQUIRED_HEADINGS = (
    "# Стандарт создания исполнимых контрактов",
    "## 1. Введение",
    "## 2. Самостоятельная классификация артефактов",
    "## 3. Нормативный формат по уровням и YAML-шаблон L1",
    "## 4. Применение шаблона к существующим контрактам",
    "## 5. Экспертная проверка",
    "## 6. DoD стандарта",
)

REQUIRED_TEXT = (
    "Issue #212",
    "docs/analysis/2026-06-23-executable-contracts-and-rfc-problems.md",
    "standards/prompt-standard.md",
    "standards/cascading-context-loading-standard.md",
    "governance/rfc-process.md",
    "governance/bcreq-fr-generation-contract.md",
    "kb/golden-examples/CONTRACT.md",
    "governance/contracts-registry.md",
    "classification_criteria",
    "classification_inventory",
    "layer_format_matrix",
    "format_rules",
    "contract_template",
    "provenance_rules",
    "placement_rules",
    "input_invariant",
    "validation_examples",
    "expert_review",
    "L1-only input test",
    "layer: L1|L2|L3",
    "loading_layer: executable",
    "100% YAML",
    "Markdown-проза запрещена",
    "Markdown with YAML frontmatter",
    "contract_registry_id",
    "source/provenance",
    "rationale",
    "CONTRACT-GEN-SCOPE-01",
    "RUN-REC-META-01",
    "PROMPT-STD-FM-01",
    "Архитектор контрактов",
    "BA-эксперт",
    "AI-инженер",
)

REQUIRED_INVENTORY_PATHS = (
    "standards/artifact-naming-standard.md",
    "standards/ba-ontology.executable.md",
    "standards/ba-ontology.md",
    "standards/cascading-context-loading-standard.md",
    "standards/industry-standards-standard.md",
    "standards/industry-taxonomy-standard.md",
    "standards/kb-standard.md",
    "standards/mango-taxonomy-standard.md",
    "standards/pattern-standard.md",
    "standards/product-classification-contract.md",
    "standards/prompt-standard.md",
    "standards/readme-standard.md",
    "standards/runs-contract-standard.md",
    "standards/GLOSSARY.md",
    "standards/team-directory.md",
    "governance/approval-contract.md",
    "governance/bcreq-fr-generation-contract.md",
    "governance/contracts-registry.md",
    "governance/rfc-process.md",
    "governance/rfc-register.md",
    "governance/rfc/bcreq-ft-scope-formation-rules-proposal.md",
    "prompts/README.executable.md",
    "prompts/README.md",
    "prompts/fr-documentation-stepwise.md",
    "prompts/questions-customer-understanding-stepwise.md",
    "prompts/session-debug-documentation-oneshot.md",
    "prompts/archive/tz-stats-generator-legacy.md",
    "runs/CONTRACT.md",
    "kb/golden-examples/CONTRACT.md",
    "runs/README.md",
    "runs/REGISTRY.md",
    "runs/stats/by-type.md",
)

REQUIRED_PROJECT_TEXT = {
    CHANGELOG: ("Issue #212", STANDARD, CONTRACTS_REGISTRY, VALIDATOR),
    README: (STANDARD, CONTRACTS_REGISTRY, "Стандарт создания исполнимых контрактов"),
    WORKFLOW: ("Validate issue #212 executable contract standard", VALIDATOR),
    CONTRACTS_REGISTRY: (
        "# Реестр исполнимых контрактов",
        "contracts:",
        "id: bcreq-fr-generation-contract",
        "path: \"governance/bcreq-fr-generation-contract.md\"",
        "governance/bcreq-fr-generation-contract.md",
        "source/provenance",
    ),
}

RULE_ID_RE = re.compile(r"^[A-Z]+(?:-[A-Z0-9]+)*-[0-9]{2}$")


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


def require_ordered(path: str, markers: tuple[str, ...]) -> list[str]:
    errors = require_path(path)
    if errors:
        return errors

    text = read_text(path)
    last = -1
    for marker in markers:
        pos = text.find(marker)
        if pos == -1:
            errors.append(f"{path}: missing ordered marker {marker!r}")
        elif pos < last:
            errors.append(f"{path}: marker {marker!r} is out of order")
        last = max(last, pos)
    return errors


def strip_yaml_comments(block: str) -> str:
    return "\n".join(
        line for line in block.splitlines() if not line.lstrip().startswith("#")
    ).strip()


def extract_yaml_json_blocks(text: str) -> list[dict[str, Any]]:
    blocks: list[dict[str, Any]] = []
    pattern = re.compile(r"```yaml\n(.*?)\n```", re.DOTALL)
    for match in pattern.finditer(text):
        payload = strip_yaml_comments(match.group(1))
        if not payload.startswith("{"):
            continue
        blocks.append(json.loads(payload))
    return blocks


def find_standard_payload(text: str) -> dict[str, Any] | None:
    for block in extract_yaml_json_blocks(text):
        payload = block.get("executable_contract_standard")
        if isinstance(payload, dict):
            return payload
    return None


def check_machine_readable_payload() -> list[str]:
    errors = require_path(STANDARD)
    if errors:
        return errors

    text = read_text(STANDARD)
    try:
        payload = find_standard_payload(text)
    except json.JSONDecodeError as exc:
        return [f"{STANDARD}: YAML/JSON-compatible block does not parse: {exc}"]

    if payload is None:
        return [f"{STANDARD}: missing executable_contract_standard YAML payload"]

    if payload.get("standard_id") != "executable-contract-standard":
        errors.append(f"{STANDARD}: standard_id must be executable-contract-standard")
    if payload.get("layer") != "L3":
        errors.append(f"{STANDARD}: standard layer must be L3")
    if payload.get("rule_class") != "management":
        errors.append(f"{STANDARD}: standard rule_class must be management")

    criteria = payload.get("classification_criteria", {})
    layers = criteria.get("layer", {})
    for key in ("L1", "L2", "L3"):
        if key not in layers:
            errors.append(f"{STANDARD}: classification_criteria.layer missing {key}")
        elif "rationale" not in layers[key]:
            errors.append(f"{STANDARD}: layer {key} missing rationale")

    rule_classes = criteria.get("rule_class", {})
    for key in ("combat", "management"):
        if key not in rule_classes:
            errors.append(f"{STANDARD}: classification_criteria.rule_class missing {key}")
        elif "rationale" not in rule_classes[key]:
            errors.append(f"{STANDARD}: rule_class {key} missing rationale")

    inventory = payload.get("classification_inventory", [])
    inventory_paths = {
        row.get("path") for row in inventory if isinstance(row, dict) and row.get("path")
    }
    for path in REQUIRED_INVENTORY_PATHS:
        if path not in inventory_paths:
            errors.append(f"{STANDARD}: classification_inventory missing {path}")

    for required in (
        "layer_format_matrix",
        "format_rules",
        "contract_template",
        "provenance_rules",
        "placement_rules",
        "input_invariant",
    ):
        if required not in payload:
            errors.append(f"{STANDARD}: payload missing {required}")

    matrix = payload.get("layer_format_matrix", {})
    expected_layer_formats = {
        "L1": "100% YAML",
        "L2": "YAML/JSON for structured data; Markdown for textual knowledge",
        "L3": "Markdown with YAML frontmatter",
    }
    for layer, expected in expected_layer_formats.items():
        actual = matrix.get(layer, {}).get("format")
        if actual != expected:
            errors.append(
                f"{STANDARD}: layer_format_matrix.{layer}.format must be {expected!r}"
            )

    format_rules = payload.get("format_rules", [])
    if len(format_rules) < 5:
        errors.append(f"{STANDARD}: expected at least 5 format_rules")
    format_values = {
        row.get("format") for row in format_rules if isinstance(row, dict)
    }
    for expected in expected_layer_formats.values():
        if expected not in format_values:
            errors.append(f"{STANDARD}: format_rules missing format {expected!r}")

    provenance = payload.get("provenance_rules", {})
    if provenance.get("registry_path") != CONTRACTS_REGISTRY:
        errors.append(f"{STANDARD}: provenance_rules.registry_path must be {CONTRACTS_REGISTRY}")
    if provenance.get("l1_contract_field") != "contract_registry_id":
        errors.append(f"{STANDARD}: provenance_rules.l1_contract_field must be contract_registry_id")
    forbidden_l1_fields = set(provenance.get("forbidden_l1_fields", []))
    for field in ("source_hub", "source_sha", "governance_sources", "related_artifacts", "depends_on", "L3 hyperlinks"):
        if field not in forbidden_l1_fields:
            errors.append(f"{STANDARD}: provenance_rules.forbidden_l1_fields missing {field}")

    template = payload.get("contract_template", {})
    if template.get("format") != "100% YAML":
        errors.append(f"{STANDARD}: contract_template.format must be 100% YAML")
    if template.get("markdown_prose") != "forbidden":
        errors.append(f"{STANDARD}: contract_template.markdown_prose must be forbidden")
    for forbidden in ("frontmatter", "markdown_sections", "machine_readable_index", "governance_sources"):
        if forbidden in template:
            errors.append(f"{STANDARD}: contract_template must not contain {forbidden}")

    fields = template.get("top_level_fields", {})
    for key in (
        "status",
        "version",
        "type",
        "executable",
        "layer",
        "rule_class",
        "contract_registry_id",
        "created",
        "updated",
        "owner",
        "runtime_inputs",
        "outputs",
        "rules",
        "validation",
    ):
        if key not in fields:
            errors.append(f"{STANDARD}: contract_template.top_level_fields missing {key}")

    example_rules = fields.get("rules", {}).get("example", [])
    for rule in example_rules:
        rule_id = rule.get("id", "")
        if not RULE_ID_RE.match(rule_id):
            errors.append(f"{STANDARD}: rule id {rule_id!r} does not match {RULE_ID_RE.pattern}")
        if "rationale" not in rule:
            errors.append(f"{STANDARD}: rule {rule_id!r} missing rationale")

    invariant = payload.get("input_invariant", {})
    if invariant.get("rule") != "L1 runtime inputs MUST NOT require L3 artifacts":
        errors.append(f"{STANDARD}: input_invariant.rule has unexpected value")
    if "validation" not in invariant or "rationale" not in invariant:
        errors.append(f"{STANDARD}: input_invariant must include validation and rationale")

    examples = payload.get("validation_examples", [])
    if len(examples) != 3:
        errors.append(f"{STANDARD}: expected exactly 3 validation_examples")
    for example in examples:
        if "rationale" not in example:
            errors.append(f"{STANDARD}: validation example missing rationale")

    return errors


def check_standard_document() -> list[str]:
    errors: list[str] = []
    errors += require_path(STANDARD)
    if errors:
        return errors
    errors += require_ordered(STANDARD, REQUIRED_HEADINGS)
    errors += require_text(STANDARD, *REQUIRED_TEXT, *REQUIRED_INVENTORY_PATHS)
    return errors


def check_project_wiring() -> list[str]:
    errors: list[str] = []
    for path, needles in REQUIRED_PROJECT_TEXT.items():
        errors += require_text(path, *needles)
    return errors


def main() -> int:
    errors = check_standard_document() + check_machine_readable_payload() + check_project_wiring()

    if errors:
        print("Issue #212 executable contract standard validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    inventory_count = len(find_standard_payload(read_text(STANDARD))["classification_inventory"])
    print(
        "Issue #212 executable contract standard validation passed "
        f"({inventory_count} classified artifacts)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
