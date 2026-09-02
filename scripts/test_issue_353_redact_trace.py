#!/usr/bin/env python3
"""Behavior tests for the issue #353 trace redactor."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments/issue_353"))
from redact_trace import redact  # noqa: E402


def main() -> int:
    secrets = (
        "person@example.com",
        "123e4567-e89b-12d3-a456-426614174000",
        "/home/box/project",
        "/tmp/gh-issue-solver-1788292015338/repo",
        "ghp_abcdefghijklmnopqrstuvwxyz123456",
        "github_pat_abcdefghijklmnopqrstuvwxyz123456",
        "sk-abcdefghijklmnopqrstuvwxyz123456",
    )
    near_misses = ("docs@example", "/home/boxes/project", "ghp_short", "sk-short")
    source = "\n".join((*secrets, *near_misses))
    result = redact(source)
    errors = [secret for secret in secrets if secret in result]
    errors.extend(value for value in near_misses if value not in result)
    if errors:
        print(f"FAIL: trace redactor leaked or over-redacted {errors!r}")
        return 1
    expected_markers = (
        "[REDACTED_EMAIL]",
        "[REDACTED_UUID]",
        "[REDACTED_HOME]",
        "[REDACTED_WORKTREE]",
        "[REDACTED_GITHUB_TOKEN]",
        "[REDACTED_API_KEY]",
    )
    missing = [marker for marker in expected_markers if marker not in result]
    if missing:
        print(f"FAIL: trace redactor missed replacement markers {missing!r}")
        return 1
    print("OK: trace redactor covers identifiers, paths, and token formats")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
