#!/usr/bin/env python3
"""Regression check for issue #226: RFC generation contract and evidence."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

CONTRACT = "governance/rfc-generation-contract.md"
REGISTRY = "governance/contracts-registry.md"
RUN_DIR = "runs/2026/RUN-0015"
RUN_METADATA = f"{RUN_DIR}/metadata.yaml"
RUN_REPORT = f"{RUN_DIR}/outputs/rfc-generation-contract-test-report.md"
RUN_LOG = f"{RUN_DIR}/logs/validation-log.md"
VALIDATOR = "scripts/validate_issue_226_rfc_generation_contract.py"
WORKFLOW = ".github/workflows/github-pages.yml"

REQUIRED_INPUT_KEYS = (
    "analytics_sources",
    "report_sources",
    "research_sources",
    "existing_rfcs",
    "product_docs",
)

REQUIRED_FRONTMATTER_FIELDS = (
    "id",
    "status",
    "title",
    "author",
    "created",
    "updated",
    "layer",
    "type",
    "related_contracts",
    "target_artifacts",
)

REQUIRED_SECTION_TITLES = (
    "Context and motivation",
    "Problem",
    "Proposal",
    "Alternatives considered",
    "Rationale",
    "Impact",
    "Implementation plan",
    "Canonical criteria",
)

REQUIRED_CONTRACT_TEXT = (
    "id: rfc-generation-contract",
    "status: active",
    "version: 0.1",
    "contract_registry_id: rfc-generation-contract",
    "contract_id: rfc-generation-contract",
    "artifact_type: rfc",
    "output_artifact_layer: L3",
    "output_format: \"Markdown with YAML frontmatter\"",
    "analytics_sources:",
    "report_sources:",
    "research_sources:",
    "existing_rfcs:",
    "product_docs:",
    "RFC-NNN-P1",
    "RFC-NNN-R1",
    "requires_adr",
    "requires_standard",
    "target_artifacts",
    "traceability_rules:",
    "style_rules:",
    "validation:",
    "testing_scenarios:",
    "rfc_without_explicit_source",
    "requires_adr_true",
    "requires_standard_true",
)

FORBIDDEN_CONTRACT_TEXT = (
    "```",
    "| Поле |",
    "| ID |",
    "https://github.com/G-Ivan-A/mango_ba_prompts/issues/226",
    "https://github.com/G-Ivan-A/mango_ba_prompts/pull/227",
)

REQUIRED_PROJECT_TEXT = {
    "CHANGELOG.md": (
        "Issue #226",
        CONTRACT,
        RUN_REPORT,
        VALIDATOR,
    ),
    "README.md": (
        CONTRACT,
        REGISTRY,
    ),
    "governance/artifact-map.md": (
        CONTRACT,
        REGISTRY,
    ),
    WORKFLOW: (
        "Validate issue #226 RFC generation contract",
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


def parse_yaml_stream(path: str) -> tuple[list[Any] | None, list[str]]:
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
        "output_artifact_layer",
        "output_format",
        "output_language",
        "normative_keywords",
    )
    actual_first_keys = list(body.keys())[: len(expected_first_keys)]
    if tuple(actual_first_keys) != expected_first_keys:
        errors.append(
            f"{CONTRACT}: body must start with {expected_first_keys!r}, "
            f"got {actual_first_keys!r}"
        )

    metadata_expectations = {
        "id": "rfc-generation-contract",
        "status": "active",
        "type": "contract",
        "scope": "rfc-generation",
        "layer": "L1",
        "rule_class": "combat",
        "contract_registry_id": "rfc-generation-contract",
    }
    for key, expected in metadata_expectations.items():
        if metadata.get(key) != expected:
            errors.append(f"{CONTRACT}: metadata {key!r} must be {expected!r}")
    if metadata.get("executable") is not True or metadata.get("machine_readable") is not True:
        errors.append(f"{CONTRACT}: metadata must mark executable and machine_readable true")

    forbidden_metadata_keys = (
        "issue",
        "issues",
        "pull_request",
        "related_artifacts",
        "source_hub",
        "source_sha",
        "governance_sources",
        "research_sources",
    )
    for key in forbidden_metadata_keys:
        if key in metadata:
            errors.append(f"{CONTRACT}: metadata must not contain provenance key {key!r}")

    for key in (
        "purpose",
        "inputs",
        "source_priority",
        "id_rules",
        "generation_process",
        "frontmatter_schema",
        "sections",
        "traceability_rules",
        "style_rules",
        "validation",
        "testing_scenarios",
        "output_document_template",
        "self_review",
    ):
        if key not in body:
            errors.append(f"{CONTRACT}: body missing top-level key {key!r}")

    inputs = body.get("inputs")
    if not isinstance(inputs, dict):
        errors.append(f"{CONTRACT}: inputs must be a mapping")
    else:
        for key in REQUIRED_INPUT_KEYS:
            if key not in inputs:
                errors.append(f"{CONTRACT}: inputs missing {key!r}")

    frontmatter = body.get("frontmatter_schema", {})
    required_fields = frontmatter.get("required_fields") if isinstance(frontmatter, dict) else None
    if not isinstance(required_fields, dict):
        errors.append(f"{CONTRACT}: frontmatter_schema.required_fields must be a mapping")
    else:
        for key in REQUIRED_FRONTMATTER_FIELDS:
            if key not in required_fields:
                errors.append(f"{CONTRACT}: frontmatter missing field {key!r}")
        if required_fields.get("layer", {}).get("required_value") != "L3":
            errors.append(f"{CONTRACT}: generated RFC layer must be L3")
        if required_fields.get("type", {}).get("required_value") != "rfc":
            errors.append(f"{CONTRACT}: generated RFC type must be rfc")
        expected_statuses = ["draft", "review", "canonical", "deprecated"]
        actual_statuses = required_fields.get("status", {}).get("allowed_values")
        if actual_statuses != expected_statuses:
            errors.append(
                f"{CONTRACT}: frontmatter status values must be {expected_statuses!r}"
            )

    sections = body.get("sections")
    if not isinstance(sections, list) or len(sections) != 8:
        errors.append(f"{CONTRACT}: sections must contain exactly 8 entries")
    elif isinstance(sections, list):
        for index, section in enumerate(sections, start=1):
            if not isinstance(section, dict):
                errors.append(f"{CONTRACT}: section {index} must be a mapping")
                continue
            if section.get("number") != index:
                errors.append(f"{CONTRACT}: section {index} must have number {index}")
            expected_title = REQUIRED_SECTION_TITLES[index - 1]
            if section.get("title") != expected_title:
                errors.append(
                    f"{CONTRACT}: section {index} title must be {expected_title!r}"
                )
            if "machine_readable_shape" not in section:
                errors.append(f"{CONTRACT}: section {index} missing machine_readable_shape")

        impact = sections[5]
        impact_shape = impact.get("machine_readable_shape", {}).get("impact", {})
        for key in ("requires_adr", "requires_standard", "target_artifacts"):
            if key not in impact_shape:
                errors.append(f"{CONTRACT}: impact section missing {key!r}")

    validation = body.get("validation", {})
    checks = validation.get("checks") if isinstance(validation, dict) else None
    if not isinstance(checks, list):
        errors.append(f"{CONTRACT}: validation.checks must be a list")
    else:
        check_ids = {check.get("id") for check in checks if isinstance(check, dict)}
        for number in range(1, 17):
            check_id = f"RFC-GEN-VAL-{number:02d}"
            if check_id not in check_ids:
                errors.append(f"{CONTRACT}: validation missing {check_id}")

    scenarios = body.get("testing_scenarios")
    if not isinstance(scenarios, list):
        errors.append(f"{CONTRACT}: testing_scenarios must be a list")
    else:
        scenario_names = {item.get("name") for item in scenarios if isinstance(item, dict)}
        for name in (
            "real_repository_issue",
            "rfc_without_explicit_source",
            "requires_adr_true",
            "requires_standard_true",
        ):
            if name not in scenario_names:
                errors.append(f"{CONTRACT}: testing_scenarios missing {name!r}")

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

    matching = [item for item in contracts if item.get("id") == "rfc-generation-contract"]
    if len(matching) != 1:
        return [f"{REGISTRY}: expected exactly one rfc-generation-contract entry"]

    entry = matching[0]
    errors = []
    expected_values = {
        "path": CONTRACT,
        "version": 0.1,
        "status": "active",
        "layer": "L1",
        "rule_class": "combat",
    }
    for key, expected in expected_values.items():
        if entry.get(key) != expected:
            errors.append(f"{REGISTRY}: {key!r} must be {expected!r}")
    for key in ("provenance", "approved_decisions", "related_artifacts", "validated_by"):
        if key not in entry:
            errors.append(f"{REGISTRY}: contract entry missing {key!r}")
    if VALIDATOR not in entry.get("validated_by", []):
        errors.append(f"{REGISTRY}: validator not registered")
    if RUN_REPORT not in entry.get("related_artifacts", []):
        errors.append(f"{REGISTRY}: test report not linked")
    return errors


def check_run_artifacts() -> list[str]:
    errors: list[str] = []
    required_paths = (
        RUN_METADATA,
        f"{RUN_DIR}/inputs/issue-226.md",
        f"{RUN_DIR}/inputs/research-sources.md",
        RUN_REPORT,
        RUN_LOG,
        f"{RUN_DIR}/feedback/.gitkeep",
    )
    for path in required_paths:
        errors += require_path(path)
    if errors:
        return errors

    errors += require_text(
        RUN_METADATA,
        "run_id: RUN-0015",
        "process: rfc-generation-contract-validation",
        "run_type: validation",
        "status: success",
        CONTRACT,
        RUN_REPORT.removeprefix(f"{RUN_DIR}/"),
        "logs/validation-log.md",
    )
    errors += require_text(
        RUN_LOG,
        "RUN-0015",
        "validation",
        "Ход выполнения",
        "Итог",
        "success",
    )
    errors += require_text(
        RUN_REPORT,
        "Issue #226",
        "11 existing RFC-like documents",
        "RFC-GEN-TEST-02",
        "RFC-GEN-TEST-03",
        "RFC-GEN-TEST-04",
        "requires_adr: true",
        "requires_standard: true",
    )
    return errors


def check_project_wiring() -> list[str]:
    errors: list[str] = []
    for path, needles in REQUIRED_PROJECT_TEXT.items():
        errors += require_text(path, *needles)
    errors += require_text(
        "runs/REGISTRY.md",
        "RUN-0015",
        "rfc-generation-contract-validation",
        "rfc-generation-contract-test-report.md",
        "logs/validation-log.md",
    )
    errors += require_text(
        "runs/stats/by-date.md",
        "2026-06 | 12",
        "RUN-0015",
        "rfc-generation-contract-validation",
    )
    errors += require_text(
        "runs/stats/by-type.md",
        "Всего: 17 run'ов.",
        "validation` — валидация",
        "Всего: 4.",
        "RUN-0015",
    )
    errors += require_text(
        "runs/stats/by-process.md",
        "Уникальных процессов: 17.",
        "rfc-generation-contract-validation",
        CONTRACT,
    )
    return errors


def main() -> int:
    errors: list[str] = []
    errors += require_text(CONTRACT, *REQUIRED_CONTRACT_TEXT)
    errors += reject_text(CONTRACT, *FORBIDDEN_CONTRACT_TEXT)
    errors += check_contract_yaml_shape()
    errors += check_registry_yaml_shape()
    errors += check_run_artifacts()
    errors += check_project_wiring()

    if errors:
        print("Issue #226 RFC generation contract validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Issue #226 RFC generation contract validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
