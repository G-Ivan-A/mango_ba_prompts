#!/usr/bin/env python3
"""Regression check for issue #115 — real mango-cc-manual KB extraction.

The bug: KB Pipeline #11 succeeded but only extracted the sample fixture to an
artifact. It did not process ``kb/sources/mango-cc-manual/`` and therefore did
not create ``kb/processed/mango-cc-manual/`` in the repository.

This stdlib-only check locks the fix:

- the real processed KB exists and points to the uploaded PDF;
- it contains index/meta/sections/images with real-manual scale;
- section boundaries come from the PDF outline, not bold numbered list items;
- the GitHub workflow exposes manual inputs and passes them to ``make kb-extract``.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SOURCE = "kb/sources/mango-cc-manual/CC_manual_1.26.23_compressed.pdf"
PROCESSED = "kb/processed/mango-cc-manual"
WORKFLOW = ".github/workflows/kb.yml"
MAKEFILE = "Makefile"


def read_text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def require_path(path: str) -> list[str]:
    return [] if (ROOT / path).exists() else [f"{path}: missing"]


def require_text(text: str, path: str, *needles: str) -> list[str]:
    return [f"{path}: missing {needle!r}" for needle in needles if needle not in text]


def load_meta(errors: list[str]) -> dict:
    meta_path = ROOT / PROCESSED / "meta.json"
    if not meta_path.exists():
        errors.append(f"{PROCESSED}/meta.json: missing")
        return {}
    try:
        return json.loads(meta_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"{PROCESSED}/meta.json: invalid JSON ({exc})")
        return {}


def check_processed_mango() -> list[str]:
    errors: list[str] = []
    errors += require_path(SOURCE)
    errors += require_path(f"{PROCESSED}/index.md")
    errors += require_path(f"{PROCESSED}/sections")
    errors += require_path(f"{PROCESSED}/images")
    meta = load_meta(errors)
    if errors:
        return errors

    sections_dir = ROOT / PROCESSED / "sections"
    images_dir = ROOT / PROCESSED / "images"
    section_files = sorted(sections_dir.glob("*.md"))
    image_files = sorted(p for p in images_dir.iterdir() if p.is_file())

    expected = {
        "doc_code": "CC",
        "doc_version": "1.26.23",
        "source_pdf": SOURCE,
    }
    for key, value in expected.items():
        if meta.get(key) != value:
            errors.append(f"{PROCESSED}/meta.json: {key}={meta.get(key)!r}, expected {value!r}")

    if meta.get("section_source", "").startswith("pdf-outline") is False:
        errors.append(f"{PROCESSED}/meta.json: section_source must use pdf-outline")
    if meta.get("page_count", 0) < 600:
        errors.append(f"{PROCESSED}/meta.json: page_count must reflect the real 600+ page manual")
    if meta.get("section_count") != len(section_files):
        errors.append(
            f"{PROCESSED}/meta.json: section_count {meta.get('section_count')} "
            f"!= {len(section_files)} files"
        )
    if len(meta.get("sections", [])) != len(section_files):
        errors.append(f"{PROCESSED}/meta.json: sections list does not match files on disk")
    if len(section_files) < 200:
        errors.append(f"{PROCESSED}/sections: expected 200+ real-manual sections")
    if not image_files or meta.get("image_count", 0) <= 0:
        errors.append(f"{PROCESSED}/images: expected extracted images")
    if meta.get("table_count", 0) < 100:
        errors.append(f"{PROCESSED}/meta.json: expected 100+ extracted tables")
    if meta.get("tokens_total", 0) < 100_000:
        errors.append(f"{PROCESSED}/meta.json: expected real-manual token volume")

    section_pairs = {(s.get("number"), s.get("title")) for s in meta.get("sections", [])}
    required_sections = {
        ("1", "Начало работы"),
        ("1.1", "Регистрация нового пользователя"),
        ("1.2", "Вход в систему"),
        ("2", "Главное окно программы"),
        ("4", "Обращения"),
        ("25", "Приложение 8. Устранение неполадок"),
    }
    for pair in sorted(required_sections):
        if pair not in section_pairs:
            errors.append(f"{PROCESSED}/meta.json: missing outline section {pair[0]} {pair[1]}")

    false_positive_title = "Направление звонка (входящий или внутренний) – настройка условия направления"
    if any(s.get("title") == false_positive_title for s in meta.get("sections", [])):
        errors.append(
            f"{PROCESSED}/meta.json: list item became a section; expected PDF outline boundaries"
        )

    index = read_text(f"{PROCESSED}/index.md")
    errors += require_text(index, f"{PROCESSED}/index.md", SOURCE, "Регистрация нового пользователя")
    return errors


def check_workflow_inputs() -> list[str]:
    errors = require_path(WORKFLOW)
    if errors:
        return errors
    text = read_text(WORKFLOW)
    errors += require_text(
        text,
        WORKFLOW,
        "workflow_dispatch:",
        "inputs:",
        "source:",
        "out:",
        "doc_code:",
        "doc_title:",
        "doc_version:",
        "commit_result:",
        SOURCE,
        PROCESSED,
        "make kb-extract \\",
        'SRC="${{ inputs.source }}"',
        'OUT="${{ inputs.out }}"',
        "scripts/validate_issue_115_kb_mango_pipeline.py",
    )
    if re.search(r"Build sample fixture and extract|make kb-sample\s+make kb-extract", text):
        errors.append(f"{WORKFLOW}: workflow_dispatch extract job must not hardcode the sample fixture")
    return errors


def check_makefile_parameters() -> list[str]:
    errors = require_path(MAKEFILE)
    if errors:
        return errors
    text = read_text(MAKEFILE)
    return require_text(
        text,
        MAKEFILE,
        "SRC     ?= $(SAMPLE_PDF)",
        "OUT     ?= $(SAMPLE_OUT)",
        "kb-mango:",
        "$(MAKE) kb-extract \\",
        'SRC="$(MANGO_SRC)"',
        'OUT="$(MANGO_OUT)"',
    )


def main() -> int:
    errors: list[str] = []
    errors += check_processed_mango()
    errors += check_workflow_inputs()
    errors += check_makefile_parameters()

    if errors:
        print("issue-115 KB mango pipeline validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("issue-115 KB mango pipeline validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
