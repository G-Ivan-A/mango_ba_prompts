#!/usr/bin/env python3
"""Regression check for issue #172: taxonomy directory path refactor.

Issue #172 renames the two machine-readable taxonomy namespaces to explicit
``*-taxonomy`` paths and requires every exact reference to the retired directory
names to be updated without touching unrelated KB namespaces.
"""

from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

OLD_INDUSTRY_DIR = Path("kb") / "industry"
OLD_MANGO_DIR = Path("kb") / "mango"
INDUSTRY_DIR = Path("kb") / "industry-taxonomy"
MANGO_DIR = Path("kb") / "mango-taxonomy"

OLD_TEXT_REFERENCES = (
    "kb/" + "industry/",
    "kb/" + "mango/",
)

EXPECTED_FILES = (
    INDUSTRY_DIR / "README.md",
    INDUSTRY_DIR / "registry.json",
    INDUSTRY_DIR / "registry.schema.json",
    MANGO_DIR / "README.md",
    MANGO_DIR / "registry.json",
    MANGO_DIR / "registry.schema.json",
)

REQUIRED_TEXT = {
    "CHANGELOG.md": ("Issue #172",),
    "Makefile": ("scripts/validate_issue_172_taxonomy_path_refactor.py",),
    ".github/workflows/kb.yml": (
        "Validate issue #172 taxonomy path refactor",
        "scripts/validate_issue_172_taxonomy_path_refactor.py",
        "kb/industry-taxonomy/**",
        "kb/mango-taxonomy/**",
    ),
    "kb/README.md": (
        "kb/industry-taxonomy/",
        "kb/mango-taxonomy/",
    ),
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
    try:
        result = subprocess.run(
            ["git", "ls-files", "-z"],
            cwd=ROOT,
            check=True,
            stdout=subprocess.PIPE,
        )
    except (OSError, subprocess.CalledProcessError):
        return [
            path.relative_to(ROOT)
            for path in ROOT.rglob("*")
            if path.is_file() and ".git" not in path.relative_to(ROOT).parts
        ]

    return [
        Path(raw.decode("utf-8"))
        for raw in result.stdout.split(b"\0")
        if raw
    ]


def read_text(path: Path) -> str | None:
    if path.suffix.lower() in SKIP_SUFFIXES:
        return None
    try:
        return (ROOT / path).read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return None


def require_path(path: Path) -> list[str]:
    return [] if (ROOT / path).exists() else [f"{path}: missing"]


def require_absent(path: Path) -> list[str]:
    return [f"{path}: retired directory must not exist"] if (ROOT / path).exists() else []


def check_layout() -> list[str]:
    errors: list[str] = []
    errors += require_absent(OLD_INDUSTRY_DIR)
    errors += require_absent(OLD_MANGO_DIR)
    for path in EXPECTED_FILES:
        errors += require_path(path)
    return errors


def check_no_retired_references() -> list[str]:
    errors: list[str] = []
    for path in tracked_files():
        text = read_text(path)
        if text is None:
            continue
        for retired in OLD_TEXT_REFERENCES:
            if retired in text:
                errors.append(f"{path}: contains retired taxonomy path {retired!r}")
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
    errors += check_no_retired_references()
    errors += check_required_text()

    if errors:
        print("Issue #172 taxonomy path refactor validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Issue #172 taxonomy path refactor validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
