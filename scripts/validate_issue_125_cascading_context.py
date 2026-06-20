#!/usr/bin/env python3
"""Regression check for issue #125 — cascading context loading.

The check locks the implementation contract:

- critical full documents have adjacent ``.executable.md`` companions;
- every companion declares its full version and deterministic escalation triggers;
- every full document warns LLM agents to start from the executable layer;
- the prompt that references an optimized index points at the executable layer;
- token measurements prove the executable layer is smaller than the full layer.
"""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.kb.tokens import count_tokens, method  # noqa: E402

EXPECTED_PAIRS = (
    ("AI_SESSION_HANDOVER_PROMPT.md", "AI_SESSION_HANDOVER_PROMPT.executable.md"),
    (
        "governance/agent-onboarding-protocol.md",
        "governance/agent-onboarding-protocol.executable.md",
    ),
    ("prompts/README.md", "prompts/README.executable.md"),
    ("docs/ba-processes/00-index.md", "docs/ba-processes/00-index.executable.md"),
    ("standards/ba-ontology.md", "standards/ba-ontology.executable.md"),
)

FULL_WARNING = "LLM Loading Contract"
EXECUTABLE_MARKERS = (
    "layer: executable",
    "full_version:",
    "## Escalation triggers",
    "TRIGGER-1",
    "TRIGGER-2",
    "TRIGGER-3",
)


def read_text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def require_path(path: str) -> list[str]:
    return [] if (ROOT / path).exists() else [f"{path}: missing"]


def require_text(path: str, *needles: str) -> list[str]:
    text = read_text(path)
    return [f"{path}: missing {needle!r}" for needle in needles if needle not in text]


def check_pairs() -> list[str]:
    errors: list[str] = []

    for full_path, executable_path in EXPECTED_PAIRS:
        path_errors = require_path(full_path) + require_path(executable_path)
        errors += path_errors
        if path_errors:
            continue

        full_text = read_text(full_path)
        executable_text = read_text(executable_path)

        if FULL_WARNING not in full_text:
            errors.append(f"{full_path}: missing full-layer LLM warning")
        if executable_path not in full_text:
            errors.append(f"{full_path}: warning does not link {executable_path}")

        for marker in EXECUTABLE_MARKERS:
            if marker not in executable_text:
                errors.append(f"{executable_path}: missing {marker!r}")
        if full_path not in executable_text:
            errors.append(f"{executable_path}: does not name full version {full_path}")

        full_tokens = count_tokens(full_text)
        executable_tokens = count_tokens(executable_text)
        if executable_tokens >= full_tokens:
            errors.append(
                f"{executable_path}: executable layer is not smaller "
                f"({executable_tokens} >= {full_tokens} tokens)"
            )

    return errors


def check_contract_documents() -> list[str]:
    errors: list[str] = []
    for path in (
        "standards/cascading-context-loading-standard.md",
        "CHANGELOG.md",
        "prompts/session-debug-documentation-oneshot.md",
        ".github/workflows/github-pages.yml",
    ):
        errors += require_path(path)
    if errors:
        return errors

    errors += require_text(
        "standards/cascading-context-loading-standard.md",
        "Cascading Context Loading",
        ".executable.md",
        "Escalation triggers",
        "LLM Loading Contract",
    )
    errors += require_text(
        "prompts/session-debug-documentation-oneshot.md",
        "prompts/README.executable.md",
    )
    errors += require_text(
        "CHANGELOG.md",
        "Issue #125",
        "cascading context loading",
        "validate_issue_125_cascading_context.py",
    )
    errors += require_text(
        ".github/workflows/github-pages.yml",
        "Validate issue #125 cascading context loading",
        "python3 scripts/validate_issue_125_cascading_context.py",
    )
    return errors


def main() -> int:
    errors = check_pairs() + check_contract_documents()
    if errors:
        print("Issue #125 cascading context validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Issue #125 cascading context validation passed ({method()}).")
    for full_path, executable_path in EXPECTED_PAIRS:
        full_tokens = count_tokens(read_text(full_path))
        executable_tokens = count_tokens(read_text(executable_path))
        savings = full_tokens - executable_tokens
        ratio = full_tokens / max(executable_tokens, 1)
        print(
            f"- {executable_path}: {executable_tokens}/{full_tokens} tokens, "
            f"saves {savings}, full/executable {ratio:.1f}:1"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
