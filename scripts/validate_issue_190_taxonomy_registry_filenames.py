#!/usr/bin/env python3
"""Regression check for issue #190: unified taxonomy registry filenames."""

from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

EXPECTED_FILES = (
    Path("kb/industry-taxonomy/README.md"),
    Path("kb/industry-taxonomy/registry.json"),
    Path("kb/industry-taxonomy/registry.schema.json"),
    Path("kb/mango-taxonomy/README.md"),
    Path("kb/mango-taxonomy/registry.json"),
    Path("kb/mango-taxonomy/registry.schema.json"),
)

RETIRED_FILES = (
    Path("kb/industry-taxonomy/reference-taxonomy.json"),
    Path("kb/industry-taxonomy/reference-taxonomy.schema.json"),
    Path("kb/mango-taxonomy/mango-registry.json"),
    Path("kb/mango-taxonomy/mango-registry.schema.json"),
)

RETIRED_TEXT = (
    "reference-taxonomy.json",
    "reference-taxonomy.schema.json",
    "kb/industry-taxonomy/reference-taxonomy.json",
    "kb/industry-taxonomy/reference-taxonomy.schema.json",
    "mango-registry.json",
    "mango-registry.schema.json",
    "kb/mango-taxonomy/mango-registry.json",
    "kb/mango-taxonomy/mango-registry.schema.json",
)

REQUIRED_TEXT = {
    "CHANGELOG.md": ("Issue #190",),
    "Makefile": ("scripts/validate_issue_190_taxonomy_registry_filenames.py",),
    ".github/workflows/kb.yml": (
        "Validate issue #190 taxonomy registry filenames",
        "scripts/validate_issue_190_taxonomy_registry_filenames.py",
    ),
    "kb/industry-taxonomy/README.md": (
        "kb/industry-taxonomy/registry.json",
        "kb/industry-taxonomy/registry.schema.json",
    ),
    "kb/mango-taxonomy/README.md": (
        "registry.json",
        "registry.schema.json",
        "kb/industry-taxonomy/registry.json",
    ),
}

ALLOWED_RETIRED_TEXT_PATHS = {
    Path("scripts/validate_issue_190_taxonomy_registry_filenames.py"),
    Path("experiments/issue-160-generate-mango-registry.py"),
}

SKIP_SUFFIXES = {
    ".gif",
    ".jpeg",
    ".jpg",
    ".pdf",
    ".png",
    ".webp",
}


def tracked_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
    )
    return [Path(raw.decode("utf-8")) for raw in result.stdout.split(b"\0") if raw]


def read_text(path: Path) -> str | None:
    if path.suffix.lower() in SKIP_SUFFIXES:
        return None
    try:
        return (ROOT / path).read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return None


def check_layout() -> list[str]:
    errors: list[str] = []
    for path in EXPECTED_FILES:
        if not (ROOT / path).exists():
            errors.append(f"{path}: missing")
    for path in RETIRED_FILES:
        if (ROOT / path).exists():
            errors.append(f"{path}: retired filename must not exist")
    return errors


def check_no_retired_text() -> list[str]:
    errors: list[str] = []
    for path in tracked_files():
        if path in ALLOWED_RETIRED_TEXT_PATHS:
            continue
        text = read_text(path)
        if text is None:
            continue
        for retired in RETIRED_TEXT:
            if retired in text:
                errors.append(f"{path}: contains retired taxonomy filename {retired!r}")
    return errors


def check_required_text() -> list[str]:
    errors: list[str] = []
    for path, needles in REQUIRED_TEXT.items():
        file_path = ROOT / path
        if not file_path.exists():
            errors.append(f"{path}: missing")
            continue
        text = file_path.read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text:
                errors.append(f"{path}: missing {needle!r}")
    return errors


def main() -> int:
    errors: list[str] = []
    errors += check_layout()
    errors += check_no_retired_text()
    errors += check_required_text()

    if errors:
        print("Issue #190 taxonomy registry filename validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Issue #190 taxonomy registry filename validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
