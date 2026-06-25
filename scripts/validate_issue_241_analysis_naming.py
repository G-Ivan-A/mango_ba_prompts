#!/usr/bin/env python3
"""Regression check for issue #241: dated analysis artifact filenames."""

from __future__ import annotations

import re
import subprocess
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

ANALYSIS_DIR = Path("docs/analysis")
STANDARD = Path("standards/artifact-naming-standard.md")
README = Path("README.md")
CHANGELOG = Path("CHANGELOG.md")
WORKFLOW = Path(".github/workflows/github-pages.yml")
VALIDATOR = Path("scripts/validate_issue_241_analysis_naming.py")

DATED_ANALYSIS_RE = re.compile(
    r"^docs/analysis/(?P<date>\d{4}-\d{2}-\d{2})-[a-z0-9]+(?:-[a-z0-9]+)*\.md$"
)
MARKDOWN_LINK_RE = re.compile(
    r"\]\((?!https?://|#|mailto:)(?P<target>[^)#?]+\.md)(?:#[^)]+)?\)"
)

SKIP_SUFFIXES = {
    ".gif",
    ".jpeg",
    ".jpg",
    ".pdf",
    ".png",
    ".webp",
}


def run_git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
        text=True,
    )
    return result.stdout


def tracked_files(*pathspecs: str) -> list[Path]:
    output = run_git("ls-files", "-z", *pathspecs)
    return [Path(raw) for raw in output.split("\0") if raw]


def read_text(path: Path) -> str | None:
    if path.suffix.lower() in SKIP_SUFFIXES:
        return None
    try:
        return (ROOT / path).read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return None


def creation_date_for(path: Path) -> str | None:
    candidates = [path]
    match = DATED_ANALYSIS_RE.match(path.as_posix())
    if match:
        candidates.append(path.with_name(path.name[len(match.group("date")) + 1 :]))

    dates: set[str] = set()
    for candidate in candidates:
        output = run_git(
            "log",
            "--diff-filter=A",
            "--follow",
            "--date=short",
            "--format=%ad",
            "--",
            candidate.as_posix(),
        ).strip()
        if output:
            dates.update(line for line in output.splitlines() if line)
    return min(dates) if dates else None


def check_analysis_filenames() -> list[str]:
    errors: list[str] = []
    analysis_files = tracked_files(f"{ANALYSIS_DIR.as_posix()}/*.md")

    if not analysis_files:
        return [f"{ANALYSIS_DIR}: no tracked Markdown files found"]

    for path in analysis_files:
        path_text = path.as_posix()
        match = DATED_ANALYSIS_RE.match(path_text)
        if not match:
            errors.append(f"{path}: must match docs/analysis/YYYY-MM-DD-kebab-slug.md")
            continue

        prefix = match.group("date")
        try:
            date.fromisoformat(prefix)
        except ValueError:
            errors.append(f"{path}: invalid ISO date prefix {prefix!r}")
            continue

        created = creation_date_for(path)
        if created is None:
            errors.append(f"{path}: cannot determine creation date from git history")
        elif created != prefix:
            errors.append(f"{path}: date prefix {prefix} does not match git creation date {created}")

    return errors


def analysis_rename_pairs() -> dict[str, str]:
    pairs: dict[str, str] = {}
    for path in tracked_files(f"{ANALYSIS_DIR.as_posix()}/*.md"):
        match = DATED_ANALYSIS_RE.match(path.as_posix())
        if not match:
            continue
        old_path = path.with_name(path.name[len(match.group("date")) + 1 :])
        pairs[old_path.as_posix()] = path.as_posix()
    return pairs


def check_no_stale_analysis_paths() -> list[str]:
    errors: list[str] = []
    stale_paths = analysis_rename_pairs()
    if not stale_paths:
        stale_paths = {
            path.as_posix(): path.as_posix()
            for path in tracked_files(f"{ANALYSIS_DIR.as_posix()}/*.md")
        }

    for path in tracked_files():
        text = read_text(path)
        if text is None:
            continue
        for stale, replacement in stale_paths.items():
            if stale in text:
                errors.append(f"{path}: stale analysis path {stale!r}; use {replacement!r}")
    return errors


def check_markdown_links() -> list[str]:
    errors: list[str] = []
    analysis_paths = {path.as_posix() for path in tracked_files(f"{ANALYSIS_DIR.as_posix()}/*.md")}

    for path in tracked_files("*.md", "docs/**/*.md", "kb/**/*.md", "governance/**/*.md", "standards/**/*.md"):
        text = read_text(path)
        if text is None:
            continue
        for match in MARKDOWN_LINK_RE.finditer(text):
            target = match.group("target")
            if target.startswith("/"):
                resolved = ROOT / target.lstrip("/")
            else:
                resolved = (ROOT / path.parent / target).resolve()
            if ROOT not in resolved.parents and resolved != ROOT:
                continue
            relative = resolved.relative_to(ROOT).as_posix()
            if not relative.startswith(f"{ANALYSIS_DIR.as_posix()}/"):
                continue
            if not resolved.exists():
                errors.append(f"{path}: broken Markdown link target {target!r}")
    return errors


def check_required_text() -> list[str]:
    errors: list[str] = []
    required = {
        STANDARD: (
            "YYYY-MM-DD-<kebab-slug>.md",
            "Нативная сортировка",
            "Уникальность",
            "docs/analysis/",
        ),
        README: (
            "docs/analysis/",
            "YYYY-MM-DD-<kebab-slug>.md",
        ),
        CHANGELOG: (
            "Issue #241",
            VALIDATOR.as_posix(),
        ),
        WORKFLOW: (
            "Validate issue #241 analysis artifact naming",
            VALIDATOR.as_posix(),
        ),
    }
    for path, needles in required.items():
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
    errors += check_analysis_filenames()
    errors += check_no_stale_analysis_paths()
    errors += check_markdown_links()
    errors += check_required_text()

    if errors:
        print("Issue #241 analysis artifact naming validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Issue #241 analysis artifact naming validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
