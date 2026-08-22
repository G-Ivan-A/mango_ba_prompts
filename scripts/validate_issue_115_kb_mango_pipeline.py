#!/usr/bin/env python3
"""Regression check for issue #115/#119 — real mango-cc-manual KB extraction.

The bug: KB Pipeline #11 succeeded but only extracted the sample fixture to an
artifact. It did not process ``kb/sources/mango-cc-manual/`` and therefore did
not create ``kb/processed/mango-cc-manual/`` in the repository.

Issue #119 extended the regression: the CC manual is now six LFS-backed PDF
parts, not one ``*_compressed.pdf`` file. The processed KB and workflow must
handle those parts as one document with continuous page numbering.

This stdlib-only check locks the fix:

- the real processed KB exists and points to all expected PDF parts;
- it contains index/meta/sections/images with real-manual scale;
- section boundaries come from the PDF outline, not bold numbered list items;
- the GitHub workflow passes multi-part inputs to ``make kb-extract``.

After the LFS cleanup in issue #259, the lightweight CI validator must not
require the PDF payload bytes to be present in the repository. Extraction still
requires real PDF files; this check validates the generated KB snapshot and its
source provenance. Issue #310 went further and forbade Git LFS for PDFs
altogether, so the workflow must no longer request an LFS checkout.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CC_SOURCES = [
    "kb/sources/mango-cc-manual/CC_manual_1.26.23-part-1.pdf",
    "kb/sources/mango-cc-manual/CC_manual_1.26.23-part-2.pdf",
    "kb/sources/mango-cc-manual/CC_manual_1.26.23-part-3.pdf",
    "kb/sources/mango-cc-manual/CC_manual_1.26.23-part-4.pdf",
    "kb/sources/mango-cc-manual/CC_manual_1.26.23-part-5.pdf",
    "kb/sources/mango-cc-manual/CC_manual_1.26.23-part-6.pdf",
]
CC_PAGE_COUNT = 614
REMOVED_CC_SOURCE = "kb/sources/mango-cc-manual/CC_manual_1.26.23_compressed.pdf"
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


def page_range_end(pages: str) -> int | None:
    match = re.match(r"^\d+(?:-(\d+))?$", str(pages))
    if not match:
        return None
    return int(match.group(1) or str(pages).split("-", 1)[0])


def all_source_refs(sections: list[dict]) -> list[dict]:
    refs = []
    for section in sections:
        for ref in section.get("source_refs", []):
            if isinstance(ref, dict):
                refs.append(ref)
    return refs


def check_processed_mango() -> list[str]:
    errors: list[str] = []
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
    }
    for key, value in expected.items():
        if meta.get(key) != value:
            errors.append(f"{PROCESSED}/meta.json: {key}={meta.get(key)!r}, expected {value!r}")

    if meta.get("source_pdf") != "multi-part":
        errors.append(f"{PROCESSED}/meta.json: source_pdf must be 'multi-part'")
    if meta.get("source_pdfs") != CC_SOURCES:
        errors.append(f"{PROCESSED}/meta.json: source_pdfs must list all six CC parts in order")
    if meta.get("part_count") != len(CC_SOURCES):
        errors.append(f"{PROCESSED}/meta.json: part_count must be {len(CC_SOURCES)}")
    if meta.get("section_source", "").startswith("pdf-outline multi-part") is False:
        errors.append(f"{PROCESSED}/meta.json: section_source must use pdf-outline multi-part")
    if meta.get("page_count") != CC_PAGE_COUNT:
        errors.append(f"{PROCESSED}/meta.json: page_count must be {CC_PAGE_COUNT}")
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

    sources = meta.get("sources", [])
    if not isinstance(sources, list) or len(sources) != len(CC_SOURCES):
        errors.append(f"{PROCESSED}/meta.json: sources must contain all six source parts")
    else:
        source_paths = [source.get("source_pdf") for source in sources]
        if source_paths != CC_SOURCES:
            errors.append(f"{PROCESSED}/meta.json: sources are not in CC part order")
        source_pages = [source.get("page_count") for source in sources]
        if not all(isinstance(page_count, int) and page_count > 0 for page_count in source_pages):
            errors.append(f"{PROCESSED}/meta.json: every source must have positive page_count")
        elif sum(source_pages) != CC_PAGE_COUNT:
            errors.append(f"{PROCESSED}/meta.json: source page_count sum must be {CC_PAGE_COUNT}")
        for index, source in enumerate(sources, start=1):
            if source.get("order") != index:
                errors.append(f"{PROCESSED}/meta.json: source part {index} has wrong order")
            if not source.get("source_sha256"):
                errors.append(f"{PROCESSED}/meta.json: source part {index} missing source_sha256")

    refs = all_source_refs(meta.get("sections", []))
    parts_seen = sorted({ref.get("part") for ref in refs})
    if parts_seen != list(range(1, len(CC_SOURCES) + 1)):
        errors.append(f"{PROCESSED}/meta.json: source_refs must cover CC parts 1-6")
    if any(ref.get("source_pdf") == REMOVED_CC_SOURCE for ref in refs):
        errors.append(f"{PROCESSED}/meta.json: source_refs still point to removed compressed PDF")
    max_global_page = max(
        (end for end in (page_range_end(ref.get("global_pages", "")) for ref in refs) if end),
        default=0,
    )
    if max_global_page != CC_PAGE_COUNT:
        errors.append(f"{PROCESSED}/meta.json: source_refs must reach global page {CC_PAGE_COUNT}")

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
    errors += require_text(
        index,
        f"{PROCESSED}/index.md",
        *CC_SOURCES,
        "Регистрация нового пользователя",
    )
    if REMOVED_CC_SOURCE in index:
        errors.append(f"{PROCESSED}/index.md: still points to removed compressed PDF")
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
        "actions/checkout@v7",
        "actions/setup-python@v6",
        "actions/upload-artifact@v7",
        PROCESSED,
        "make kb-extract \\",
        'SRCS="${{ inputs.source }}"',
        'OUT="${{ inputs.out }}"',
        "scripts/validate_issue_115_kb_mango_pipeline.py",
    )
    errors += require_text(text, WORKFLOW, *CC_SOURCES)
    if "lfs" in text:
        errors.append(f"{WORKFLOW}: Git LFS is not used for PDFs anymore (issue #310)")
    if REMOVED_CC_SOURCE in text:
        errors.append(f"{WORKFLOW}: default source still points to removed compressed PDF")
    if re.search(r"Build sample fixture and extract|make kb-sample\s+make kb-extract", text):
        errors.append(f"{WORKFLOW}: workflow_dispatch extract job must not hardcode the sample fixture")
    return errors


def check_makefile_parameters() -> list[str]:
    errors = require_path(MAKEFILE)
    if errors:
        return errors
    text = read_text(MAKEFILE)
    errors += require_text(
        text,
        MAKEFILE,
        "SRC     ?= $(SAMPLE_PDF)",
        "OUT     ?= $(SAMPLE_OUT)",
        "MANGO_SRCS",
        "kb-mango:",
        "$(MAKE) kb-extract \\",
        'SRCS="$(MANGO_SRCS)"',
        'OUT="$(MANGO_OUT)"',
    )
    errors += require_text(text, MAKEFILE, *CC_SOURCES)
    if REMOVED_CC_SOURCE in text:
        errors.append(f"{MAKEFILE}: MANGO source still points to removed compressed PDF")
    return errors


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
