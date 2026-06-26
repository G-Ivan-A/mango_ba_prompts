#!/usr/bin/env python3
"""Validate contract-style RFC documents.

The default scan intentionally targets RFCs generated under
governance/rfc-generation-contract.md. Older RFC-like notes predate that
contract and can be checked explicitly by passing their paths.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_REF = "governance/rfc-generation-contract.md"

DEFAULT_SCAN_GLOBS = (
    "governance/rfc/*.md",
    "governance/rfc-to-hub-*.md",
)

REQUIRED_FRONTMATTER_ORDER = (
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

ALLOWED_STATUSES = {"draft", "review", "canonical", "deprecated"}

REQUIRED_SECTIONS = (
    "## 1. Context and motivation",
    "## 2. Problem",
    "## 3. Proposal",
    "## 4. Alternatives considered",
    "## 5. Rationale",
    "## 6. Impact",
    "## 7. Implementation plan",
    "## 8. Canonical criteria",
)

FORBIDDEN_TOP_LEVEL_YAML_BODY_KEYS = (
    "context:",
    "problems:",
    "alternatives:",
    "rationale:",
)

REQUIRED_MACHINE_READABLE_INSERTS = {
    "proposal traceability": ("proposal_traceability:", "proposal:"),
    "impact": ("impact:",),
    "implementation plan": ("implementation_plan:", "implementation_plan: not_specified"),
    "canonical criteria": ("canonical_criteria:",),
}


@dataclass(frozen=True)
class Fence:
    start: int
    end: int
    lang: str


@dataclass(frozen=True)
class Frontmatter:
    values: dict[str, Any]
    order: list[str]


def repo_path(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def strip_quotes(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def parse_inline_list(value: str) -> list[str] | None:
    if value == "[]":
        return []
    if not (value.startswith("[") and value.endswith("]")):
        return None
    payload = value[1:-1].strip()
    if not payload:
        return []
    return [strip_quotes(item.strip()) for item in payload.split(",")]


def parse_frontmatter_block(block: str) -> tuple[Frontmatter, list[str]]:
    values: dict[str, Any] = {}
    order: list[str] = []
    errors: list[str] = []
    current_key: str | None = None

    for line_number, line in enumerate(block.splitlines(), start=1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue

        if line.startswith((" ", "\t")):
            item = line.strip()
            if current_key and item.startswith("- "):
                existing = values.setdefault(current_key, [])
                if not isinstance(existing, list):
                    errors.append(
                        f"frontmatter line {line_number}: {current_key!r} mixes scalar and list values"
                    )
                    continue
                existing.append(strip_quotes(item[2:].strip()))
                continue
            # Nested maps are not part of the RFC frontmatter contract.
            continue

        match = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):(.*)$", line)
        if not match:
            errors.append(f"frontmatter line {line_number}: expected top-level key")
            current_key = None
            continue

        key, raw_value = match.group(1), match.group(2).strip()
        order.append(key)
        current_key = key

        if raw_value == "":
            values[key] = []
            continue

        inline_list = parse_inline_list(raw_value)
        values[key] = inline_list if inline_list is not None else strip_quotes(raw_value)

    return Frontmatter(values=values, order=order), errors


def split_frontmatter(text: str) -> tuple[str, str, list[str]]:
    match = re.match(r"^---[ \t]*\n(.*?)\n---[ \t]*\n", text, re.DOTALL)
    if not match:
        return "", text, ["missing YAML frontmatter delimited by ---"]
    return match.group(1), text[match.end() :], []


def load_document(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def is_contract_style_rfc(path: Path) -> bool:
    try:
        text = load_document(path)
    except UnicodeDecodeError:
        return False
    frontmatter_text, _body, errors = split_frontmatter(text)
    if errors:
        return False
    frontmatter, _parse_errors = parse_frontmatter_block(frontmatter_text)
    rfc_id = str(frontmatter.values.get("id", ""))
    doc_type = frontmatter.values.get("type")
    related_contracts = frontmatter.values.get("related_contracts", [])
    has_contract = CONTRACT_REF in related_contracts or CONTRACT_REF in text
    return bool(re.fullmatch(r"RFC-[0-9]{3}", rfc_id)) and doc_type == "rfc" and has_contract


def discover_default_paths(validate_all: bool = False) -> list[Path]:
    paths: list[Path] = []
    for pattern in DEFAULT_SCAN_GLOBS:
        for path in sorted(ROOT.glob(pattern)):
            if not path.is_file():
                continue
            if validate_all or is_contract_style_rfc(path):
                paths.append(path)
    return paths


def expand_input_paths(raw_paths: list[str], validate_all: bool = False) -> list[Path | str]:
    if not raw_paths:
        return discover_default_paths(validate_all=validate_all)

    paths: list[Path | str] = []
    for raw_path in raw_paths:
        if raw_path == "-":
            paths.append("-")
            continue
        path = (ROOT / raw_path).resolve() if not Path(raw_path).is_absolute() else Path(raw_path)
        if path.is_dir():
            paths.extend(sorted(child for child in path.rglob("*.md") if child.is_file()))
        else:
            paths.append(path)
    return paths


def fenced_code_blocks(body: str) -> tuple[list[Fence], list[str]]:
    fences: list[Fence] = []
    errors: list[str] = []
    start: int | None = None
    lang = ""

    for index, line in enumerate(body.splitlines(), start=1):
        stripped = line.strip()
        if not stripped.startswith("```"):
            continue
        if start is None:
            start = index
            lang = stripped[3:].strip().lower()
            continue
        fences.append(Fence(start=start, end=index, lang=lang))
        start = None
        lang = ""

    if start is not None:
        errors.append(f"unterminated fenced code block starting at body line {start}")

    return fences, errors


def lines_in_fences(fences: list[Fence], lang: str | None = None) -> set[int]:
    selected: set[int] = set()
    for fence in fences:
        if lang is not None and fence.lang != lang:
            continue
        selected.update(range(fence.start, fence.end + 1))
    return selected


def first_nonblank_line(text: str) -> str:
    for line in text.splitlines():
        if line.strip():
            return line.strip()
    return ""


def section_ranges(body: str) -> tuple[dict[str, str], list[str]]:
    errors: list[str] = []
    positions: list[tuple[str, int]] = []
    previous = -1

    for heading in REQUIRED_SECTIONS:
        position = body.find(heading)
        if position == -1:
            errors.append(f"missing required section {heading!r}")
            continue
        if position < previous:
            errors.append(f"section {heading!r} is out of order")
        previous = max(previous, position)
        positions.append((heading, position))

    sections: dict[str, str] = {}
    sorted_positions = sorted(positions, key=lambda item: item[1])
    for index, (heading, start) in enumerate(sorted_positions):
        end = sorted_positions[index + 1][1] if index + 1 < len(sorted_positions) else len(body)
        sections[heading] = body[start:end]

    return sections, errors


def first_content_after_heading(section: str) -> str:
    lines = section.splitlines()
    for line in lines[1:]:
        stripped = line.strip()
        if stripped:
            return stripped
    return ""


def sequence_errors(label: str, ids: set[str], pattern: re.Pattern[str]) -> list[str]:
    numbers = sorted({int(pattern.fullmatch(identifier).group(1)) for identifier in ids})
    if not numbers:
        return [f"missing {label} IDs"]
    expected = list(range(1, numbers[-1] + 1))
    if numbers != expected:
        return [f"{label} IDs must be sequential without gaps; got {numbers}, expected {expected}"]
    return []


def ids_in_text(rfc_id: str, suffix: str, text: str) -> tuple[set[str], re.Pattern[str]]:
    pattern = re.compile(rf"\b{re.escape(rfc_id)}-{suffix}([0-9]+)\b")
    ids = {match.group(0) for match in pattern.finditer(text)}
    return ids, pattern


def check_frontmatter(path_label: str, frontmatter: Frontmatter) -> list[str]:
    errors: list[str] = []
    values = frontmatter.values

    for key in REQUIRED_FRONTMATTER_ORDER:
        if key not in values:
            errors.append(f"frontmatter missing required field {key!r}")

    actual_order = [key for key in frontmatter.order if key in REQUIRED_FRONTMATTER_ORDER]
    if tuple(actual_order[: len(REQUIRED_FRONTMATTER_ORDER)]) != REQUIRED_FRONTMATTER_ORDER:
        errors.append(
            "frontmatter fields must start in contract order: "
            + ", ".join(REQUIRED_FRONTMATTER_ORDER)
        )

    rfc_id = values.get("id")
    if not isinstance(rfc_id, str) or not re.fullmatch(r"RFC-[0-9]{3}", rfc_id):
        errors.append("frontmatter id must match RFC-NNN")

    status = values.get("status")
    if status not in ALLOWED_STATUSES:
        errors.append(
            "frontmatter status must be one of "
            + ", ".join(sorted(ALLOWED_STATUSES))
        )

    for field in ("created", "updated"):
        value = values.get(field)
        if not isinstance(value, str) or not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value):
            errors.append(f"frontmatter {field} must be YYYY-MM-DD")

    if values.get("layer") != "L3":
        errors.append("frontmatter layer must be L3")
    if values.get("type") != "rfc":
        errors.append("frontmatter type must be rfc")

    for field in ("related_contracts", "target_artifacts"):
        if not isinstance(values.get(field), list):
            errors.append(f"frontmatter {field} must be a YAML list")

    related_contracts = values.get("related_contracts", [])
    if isinstance(related_contracts, list) and CONTRACT_REF not in related_contracts:
        errors.append(f"frontmatter related_contracts must include {CONTRACT_REF}")

    title = values.get("title")
    if not isinstance(title, str) or not title.strip():
        errors.append("frontmatter title must be a non-empty string")
    author = values.get("author")
    if not isinstance(author, str) or not author.strip():
        errors.append("frontmatter author must be a non-empty string")

    return [f"{path_label}: {error}" for error in errors]


def check_markdown_readability(path_label: str, body: str, sections: dict[str, str]) -> list[str]:
    errors: list[str] = []
    body_lines = body.splitlines()
    first_line = first_nonblank_line(body)

    if not first_line.startswith("# "):
        errors.append("body must start with a Markdown H1 after frontmatter")

    fences, fence_errors = fenced_code_blocks(body)
    errors.extend(fence_errors)
    yaml_fences = [fence for fence in fences if fence.lang in {"yaml", "yml"}]
    yaml_line_numbers = lines_in_fences(yaml_fences)
    yaml_ratio = len(yaml_line_numbers) / max(len(body_lines), 1)
    if yaml_ratio > 0.45:
        errors.append(
            f"YAML fences dominate the body ({len(yaml_line_numbers)}/{len(body_lines)} lines)"
        )

    outside_yaml = [
        line.strip()
        for index, line in enumerate(body_lines, start=1)
        if index not in yaml_line_numbers and line.strip()
    ]
    readable_lines = [
        line
        for line in outside_yaml
        if not line.startswith("#") and not line.startswith("---")
    ]
    if len(readable_lines) < 8:
        errors.append("body must contain readable Markdown prose/tables outside YAML fences")

    for heading, section in sections.items():
        first_content = first_content_after_heading(section)
        if not first_content:
            errors.append(f"{heading!r} must have readable content")
        elif first_content in {"```yaml", "```yml"}:
            errors.append(f"{heading!r} must start with readable Markdown, not YAML")

    for key in FORBIDDEN_TOP_LEVEL_YAML_BODY_KEYS:
        pattern = re.compile(rf"```ya?ml\s*\n(?:[ \t]*#.*\n|\s*\n)*{re.escape(key)}")
        if pattern.search(body):
            errors.append(f"body must not encode {key!r} as a top-level YAML block")

    for label, options in REQUIRED_MACHINE_READABLE_INSERTS.items():
        if not any(option in body for option in options):
            errors.append(f"missing machine-readable insert for {label}")

    return [f"{path_label}: {error}" for error in errors]


def check_traceability(path_label: str, rfc_id: str, frontmatter: Frontmatter, sections: dict[str, str]) -> list[str]:
    errors: list[str] = []

    section2 = sections.get(REQUIRED_SECTIONS[1], "")
    section3 = sections.get(REQUIRED_SECTIONS[2], "")
    section4 = sections.get(REQUIRED_SECTIONS[3], "")
    section6 = sections.get(REQUIRED_SECTIONS[5], "")
    section8 = sections.get(REQUIRED_SECTIONS[7], "")

    problem_ids, problem_pattern = ids_in_text(rfc_id, "P", section2)
    proposal_ids, proposal_pattern = ids_in_text(rfc_id, "R", section3)
    alternative_ids, alternative_pattern = ids_in_text(rfc_id, "A", section4)
    criteria_ids, criteria_pattern = ids_in_text(rfc_id, "C", section8)

    errors.extend(sequence_errors("problem", problem_ids, problem_pattern))
    errors.extend(sequence_errors("proposal", proposal_ids, proposal_pattern))
    if alternative_ids:
        errors.extend(sequence_errors("alternative", alternative_ids, alternative_pattern))
    elif not re.search(r"(no viable alternative|no viable alternatives|нет альтернатив)", section4, re.I):
        errors.append("section 4 must contain RFC-NNN-A IDs or explain that no viable alternatives exist")
    errors.extend(sequence_errors("canonical criteria", criteria_ids, criteria_pattern))

    if "source_refs" not in section2 and "Источник" not in section2 and "Source" not in section2:
        errors.append("section 2 must show source traceability for problems")

    known_problem_ids = {match.group(0) for match in re.finditer(rf"\b{re.escape(rfc_id)}-P[0-9]+\b", section2)}
    problem_ref_re = re.compile(rf"\b{re.escape(rfc_id)}-P[0-9]+\b")
    for proposal_id in sorted(proposal_ids):
        linked = False
        for match in re.finditer(re.escape(proposal_id), section3):
            window = section3[match.start() : match.start() + 700]
            refs = {ref.group(0) for ref in problem_ref_re.finditer(window)}
            if refs and refs <= known_problem_ids:
                linked = True
                break
        if not linked:
            errors.append(f"proposal {proposal_id} must link to at least one section 2 problem ID")

    criteria_proposal_refs = {
        match.group(0)
        for match in re.finditer(rf"\b{re.escape(rfc_id)}-R[0-9]+\b", section8)
    }
    missing_criteria = sorted(proposal_ids - criteria_proposal_refs)
    if missing_criteria:
        errors.append(
            "section 8 canonical criteria must verify every proposal ID; missing "
            + ", ".join(missing_criteria)
        )

    for key in ("requires_adr:", "requires_standard:", "target_artifacts:"):
        if key not in section6:
            errors.append(f"section 6 impact must include {key}")

    target_artifacts = frontmatter.values.get("target_artifacts", [])
    if isinstance(target_artifacts, list):
        for target in target_artifacts:
            if target and target not in section6:
                errors.append(
                    f"section 6 target_artifacts must include frontmatter target {target!r}"
                )

    return [f"{path_label}: {error}" for error in errors]


def validate_text(text: str, path_label: str = "<stdin>") -> list[str]:
    frontmatter_text, body, split_errors = split_frontmatter(text)
    if split_errors:
        return [f"{path_label}: {error}" for error in split_errors]

    frontmatter, parse_errors = parse_frontmatter_block(frontmatter_text)
    errors = [f"{path_label}: {error}" for error in parse_errors]
    errors.extend(check_frontmatter(path_label, frontmatter))

    sections, section_errors = section_ranges(body)
    errors.extend(f"{path_label}: {error}" for error in section_errors)
    errors.extend(check_markdown_readability(path_label, body, sections))

    rfc_id = frontmatter.values.get("id")
    if isinstance(rfc_id, str) and re.fullmatch(r"RFC-[0-9]{3}", rfc_id):
        errors.extend(check_traceability(path_label, rfc_id, frontmatter, sections))

    return errors


def validate_path(path: Path | str) -> list[str]:
    if path == "-":
        return validate_text(sys.stdin.read(), "<stdin>")

    assert isinstance(path, Path)
    path_label = repo_path(path)
    if not path.exists():
        return [f"{path_label}: missing file"]
    if not path.is_file():
        return [f"{path_label}: not a file"]
    return validate_text(load_document(path), path_label)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate RFC documents against governance/rfc-generation-contract.md format rules."
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help="RFC file or directory paths. Use '-' to read one RFC from stdin.",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="with no paths, validate every Markdown file in RFC locations instead of contract-style RFCs only",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="list discovered files and exit without validation",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    paths = expand_input_paths(args.paths, validate_all=args.all)

    if args.list:
        for path in paths:
            print(path if isinstance(path, str) else repo_path(path))
        return 0

    if not paths:
        print("RFC format validation failed:")
        print("- no RFC files discovered for validation")
        return 1

    errors: list[str] = []
    for path in paths:
        errors.extend(validate_path(path))

    if errors:
        print("RFC format validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"OK: RFC format validation passed for {len(paths)} file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
