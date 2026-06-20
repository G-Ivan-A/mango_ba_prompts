#!/usr/bin/env python3
"""Regression check for issue #137: product-docs KB lives under kb/mango-product-docs.

The migration is intentionally path-only. It must preserve the existing KB
pipeline behavior while moving product documentation inputs and generated
outputs away from the generic ``kb/`` root:

- ``kb/sources`` -> ``kb/mango-product-docs/sources``;
- ``kb/processed`` -> ``kb/mango-product-docs/processed``;
- human guides ``USAGE.md`` and ``UPLOAD-GUIDE.md`` move with the product docs;
- scripts, workflow, Makefile, docs, and generated trace metadata use the new
  stable paths.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "kb"))

from process_sources import PROCESSED_ROOT, SOURCES_ROOT, build_plan, iter_source_dirs  # noqa: E402

PRODUCT_DOCS_ROOT = ROOT / "kb" / "mango-product-docs"
SOURCES = PRODUCT_DOCS_ROOT / "sources"
PROCESSED = PRODUCT_DOCS_ROOT / "processed"

OLD_PATH_TOKENS = ("kb/sources", "kb/processed", "kb/USAGE.md", "kb/UPLOAD-GUIDE.md")
TEXT_SUFFIXES = {
    "",
    ".css",
    ".html",
    ".js",
    ".json",
    ".md",
    ".py",
    ".txt",
    ".yml",
    ".yaml",
}
SKIP_DIRS = {".git", "__pycache__"}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def require_path(path: Path) -> list[str]:
    return [] if path.exists() else [f"{rel(path)}: missing"]


def require_absent(path: Path) -> list[str]:
    return [f"{rel(path)}: old product-docs path must be removed"] if path.exists() else []


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def require_text(path: Path, *needles: str) -> list[str]:
    text = read_text(path)
    return [f"{rel(path)}: missing {needle!r}" for needle in needles if needle not in text]


def iter_text_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.is_file() and path.suffix in TEXT_SUFFIXES:
            files.append(path)
    return sorted(files)


def check_layout() -> list[str]:
    errors: list[str] = []
    for path in (
        PRODUCT_DOCS_ROOT,
        SOURCES,
        PROCESSED,
        SOURCES / "README.md",
        PROCESSED / "README.md",
        PRODUCT_DOCS_ROOT / "USAGE.md",
        PRODUCT_DOCS_ROOT / "UPLOAD-GUIDE.md",
    ):
        errors += require_path(path)
    errors += require_absent(ROOT / "kb" / "sources")
    errors += require_absent(ROOT / "kb" / "processed")
    errors += require_absent(ROOT / "kb" / "USAGE.md")
    errors += require_absent(ROOT / "kb" / "UPLOAD-GUIDE.md")
    return errors


def check_runner_roots() -> list[str]:
    errors: list[str] = []
    if SOURCES_ROOT != SOURCES:
        errors.append(f"scripts/kb/process_sources.py: SOURCES_ROOT is {rel(SOURCES_ROOT)}, expected {rel(SOURCES)}")
    if PROCESSED_ROOT != PROCESSED:
        errors.append(
            f"scripts/kb/process_sources.py: PROCESSED_ROOT is {rel(PROCESSED_ROOT)}, expected {rel(PROCESSED)}"
        )
    source_dirs = iter_source_dirs()
    if not source_dirs:
        errors.append(f"{rel(SOURCES)}: no source manifests found")
    for source_dir in source_dirs:
        try:
            source_dir.relative_to(SOURCES)
        except ValueError:
            errors.append(f"{rel(source_dir)}: source manifest is outside {rel(SOURCES)}")
        plan = build_plan(source_dir)
        try:
            plan.output_dir.relative_to(PROCESSED)
        except ValueError:
            errors.append(f"{rel(source_dir / 'meta.json')}: output is outside {rel(PROCESSED)}")
    return errors


def check_wiring() -> list[str]:
    errors: list[str] = []
    workflow = ROOT / ".github" / "workflows" / "kb.yml"
    makefile = ROOT / "Makefile"
    for path in (workflow, makefile):
        errors += require_path(path)
    if errors:
        return errors
    new_sources = "kb/mango-product-docs/sources"
    new_processed = "kb/mango-product-docs/processed"
    errors += require_text(
        workflow,
        "scripts/validate_issue_137_kb_product_docs_migration.py",
        f"{new_sources}/**",
        f"path: {new_processed}/",
        f"git add {new_processed}",
    )
    errors += require_text(
        makefile,
        "scripts/validate_issue_137_kb_product_docs_migration.py",
        f"SOURCE_DIR ?= {new_sources}/mango-cc-manual",
        "$(PYTHON) scripts/kb/process_sources.py --all",
    )
    return errors


def check_no_stale_path_literals() -> list[str]:
    errors: list[str] = []
    own_file = Path(__file__).resolve()
    for path in iter_text_files():
        if path.resolve() == own_file:
            continue
        text = read_text(path)
        for token in OLD_PATH_TOKENS:
            if token in text:
                errors.append(f"{rel(path)}: stale path literal {token!r}")
    return errors


def main() -> int:
    errors: list[str] = []
    errors += check_layout()
    errors += check_runner_roots()
    errors += check_wiring()
    errors += check_no_stale_path_literals()
    if errors:
        print("Issue #137 KB product-docs migration validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Issue #137 KB product-docs migration validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
