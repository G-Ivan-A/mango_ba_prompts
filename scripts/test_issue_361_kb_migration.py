#!/usr/bin/env python3
"""Regression check for the verified processed-KB relocation (issue #361)."""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "kb/processed"
README = PROCESSED / "README.md"
RUNTIME = "https://github.com/G-Ivan-A/mango-ba-ai-runtime/tree/main/docs/kb"


def main() -> int:
    errors = []
    if not README.is_file():
        errors.append("kb/processed/README.md is missing")
    else:
        text = README.read_text(encoding="utf-8")
        if RUNTIME not in text:
            errors.append("README does not link to the runtime KB")
        if not re.search(r"\b[0-9a-f]{40}\b", text):
            errors.append("README does not pin the runtime commit")

    remaining = sorted(p.relative_to(PROCESSED) for p in PROCESSED.rglob("*") if p.is_file() and p != README)
    if remaining:
        errors.append(f"{len(remaining)} processed-KB files remain; first: {remaining[0]}")

    if errors:
        print("issue-361 KB migration validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("issue-361 KB migration validation: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
