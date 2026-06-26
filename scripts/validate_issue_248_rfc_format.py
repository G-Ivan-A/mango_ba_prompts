#!/usr/bin/env python3
"""Regression check for issue #248: reusable RFC format validator."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from validate_rfc_format import ROOT, discover_default_paths, validate_text


RFC_243 = Path("governance/rfc/ba-processes-observability-implementation-proposal.md")
BROKEN_RFC_243_REF = "cc3b3996"
VALIDATOR = Path("scripts/validate_rfc_format.py")
ISSUE_VALIDATOR = Path("scripts/validate_issue_248_rfc_format.py")
DOC = Path("docs/rfc-format-validator.md")
CHANGELOG = Path("CHANGELOG.md")
README = Path("README.md")
WORKFLOW = Path(".github/workflows/github-pages.yml")


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    sys.exit(1)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def read_text(path: Path) -> str:
    full_path = ROOT / path
    require(full_path.exists(), f"missing file: {path}")
    return full_path.read_text(encoding="utf-8")


def require_text(path: Path, *needles: str) -> None:
    text = read_text(path)
    for needle in needles:
        require(needle in text, f"{path}: missing {needle!r}")


def git_show(path: Path, ref: str) -> str:
    result = subprocess.run(
        ["git", "show", f"{ref}:{path.as_posix()}"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    require(
        result.returncode == 0,
        f"cannot read historical RFC fixture {ref}:{path}: {(result.stderr or result.stdout).strip()}",
    )
    return result.stdout


def validate_current_rfc_243() -> None:
    text = read_text(RFC_243)
    errors = validate_text(text, RFC_243.as_posix())
    require(not errors, "current RFC-243 must pass reusable validator:\n" + "\n".join(errors))


def validate_broken_rfc_243_is_rejected() -> None:
    text = git_show(RFC_243, BROKEN_RFC_243_REF)
    errors = validate_text(text, f"{BROKEN_RFC_243_REF}:{RFC_243.as_posix()}")
    require(errors, "historical YAML-heavy RFC-243 must fail reusable validator")

    joined = "\n".join(errors)
    expected_signals = (
        "YAML fences dominate the body",
        "must start with readable Markdown, not YAML",
        "body must not encode 'context:' as a top-level YAML block",
        "body must not encode 'problems:' as a top-level YAML block",
    )
    require(
        any(signal in joined for signal in expected_signals),
        "historical RFC-243 failed for the wrong reason:\n" + joined,
    )


def validate_default_discovery() -> None:
    discovered = {path.relative_to(ROOT).as_posix() for path in discover_default_paths()}
    require(RFC_243.as_posix() in discovered, f"default discovery must include {RFC_243}")


def validate_project_hooks() -> None:
    require_text(
        DOC,
        "Issue #248",
        VALIDATOR.as_posix(),
        ISSUE_VALIDATOR.as_posix(),
        RFC_243.as_posix(),
        BROKEN_RFC_243_REF,
        "Markdown + YAML frontmatter",
    )
    require_text(README, DOC.as_posix(), VALIDATOR.as_posix())
    require_text(
        CHANGELOG,
        "Issue #248",
        VALIDATOR.as_posix(),
        ISSUE_VALIDATOR.as_posix(),
        DOC.as_posix(),
    )
    require_text(
        WORKFLOW,
        "Validate RFC format",
        VALIDATOR.as_posix(),
        "Validate issue #248 RFC format validator",
        ISSUE_VALIDATOR.as_posix(),
    )


def main() -> None:
    validate_current_rfc_243()
    validate_broken_rfc_243_is_rejected()
    validate_default_discovery()
    validate_project_hooks()
    print("OK: issue #248 RFC format validator validated")


if __name__ == "__main__":
    main()
