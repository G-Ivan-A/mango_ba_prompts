#!/usr/bin/env python3
"""Regression check for issue #144: KB structure README integrity.

Issue #144 follows the product-docs migration from issue #137 and locks the
documentation boundary for the generic ``kb/`` namespace:

- the root KB README describes ``mango-product-docs/``, ``fragments/``,
  ``practices/`` and taxonomy namespaces;
- ``kb/mango-product-docs/README.md`` exists and owns product-documentation
  sources, generated outputs, and human usage guides;
- ``kb/fragments/`` and ``kb/practices/`` stay as independent KB material, not
  as product-doc source or processed-output directories;
- the git-history audit and changelog record the decision;
- Makefile and the KB workflow run this validator.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = "scripts/validate_issue_144_kb_structure_readmes.py"
MAKEFILE = "Makefile"
KB_WORKFLOW = ".github/workflows/kb.yml"
CHANGELOG = "CHANGELOG.md"
AUDIT = "docs/audit/issue-144-kb-structure.md"


def read_text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def require_path(path: str) -> list[str]:
    return [] if (ROOT / path).exists() else [f"{path}: missing"]


def require_absent(path: str) -> list[str]:
    return [f"{path}: must not exist for issue #144"] if (ROOT / path).exists() else []


def require_text(path: str, *needles: str) -> list[str]:
    text = read_text(path)
    return [f"{path}: missing {needle!r}" for needle in needles if needle not in text]


def check_readmes() -> list[str]:
    errors: list[str] = []
    required = (
        "kb/README.md",
        "kb/mango-product-docs/README.md",
        "kb/mango-product-docs/sources/README.md",
        "kb/mango-product-docs/processed/README.md",
        "kb/fragments/README.md",
        "kb/practices/README.md",
    )
    for path in required:
        errors += require_path(path)
    if errors:
        return errors

    errors += require_text(
        "kb/README.md",
        "kb/mango-product-docs/",
        "kb/fragments/",
        "kb/practices/",
        "kb/industry/",
        "Industry Taxonomy",
        "kb/mango/ (будущий)",
        "kb/mango-product-docs/README.md",
        "USAGE.md",
        "UPLOAD-GUIDE.md",
        "docs/audit/issue-144-kb-structure.md",
        "не переносить в product-docs",
    )
    errors += require_text(
        "kb/mango-product-docs/README.md",
        "База знаний продуктов Mango Office",
        "sources/",
        "processed/",
        "USAGE.md",
        "UPLOAD-GUIDE.md",
        "Git LFS",
        "make kb-source-plan-all",
        "kb/fragments/",
        "kb/practices/",
    )
    errors += require_text(
        "kb/fragments/README.md",
        "не хранит продуктовую документацию",
        "kb/mango-product-docs/processed/",
        "issue #111",
    )
    errors += require_text(
        "kb/practices/README.md",
        "source-backed-analysis.md",
        "не продуктовая документация",
        "kb/mango-product-docs/",
    )
    return errors


def check_audit() -> list[str]:
    errors = require_path(AUDIT)
    if errors:
        return errors
    errors += require_text(
        AUDIT,
        "git log --follow -- kb/fragments/",
        "git log --follow -- kb/practices/",
        "2c766812695a1163b2e7f9cf4c4878dce9a75a1f",
        "37dc51c0c2bb1e89642e841e4962407be02e445b",
        "f361fd5b91cec0493b39a3ed73f3322bb3d7d165",
        "Оставить в kb/",
        "История Git сохранена",
    )
    return errors


def check_changelog_and_ci() -> list[str]:
    errors: list[str] = []
    for path in (CHANGELOG, MAKEFILE, KB_WORKFLOW):
        errors += require_path(path)
    if errors:
        return errors

    errors += require_text(
        CHANGELOG,
        "Issue #144",
        "kb/mango-product-docs/README.md",
        "kb/practices/README.md",
        AUDIT,
        VALIDATOR,
    )
    errors += require_text(
        MAKEFILE,
        VALIDATOR,
    )
    errors += require_text(
        KB_WORKFLOW,
        "Validate issue #144 KB structure README integrity",
        f"python3 {VALIDATOR}",
    )
    return errors


def check_layout_boundaries() -> list[str]:
    errors: list[str] = []
    old_root_paths = (
        "/".join(("kb", "sources")),
        "/".join(("kb", "processed")),
        "/".join(("kb", "USAGE.md")),
        "/".join(("kb", "UPLOAD-GUIDE.md")),
    )
    for path in old_root_paths:
        errors += require_absent(path)
    return errors


def main() -> int:
    errors: list[str] = []
    errors += check_readmes()
    errors += check_audit()
    errors += check_changelog_and_ci()
    errors += check_layout_boundaries()

    if errors:
        print("Issue #144 KB structure README validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Issue #144 KB structure README validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
