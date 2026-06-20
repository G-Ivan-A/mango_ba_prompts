#!/usr/bin/env python3
"""Regression check for issue #117 — KB section traceability and multi-part PDF.

This check is intentionally stdlib-only so it can run in the lightweight CI job.
It locks the issue-#117 requirements:

- generated sections carry machine-readable trace metadata;
- section files include a human-readable trace line;
- the split LK manual is processed as one document from five PDF parts;
- global page numbers remain continuous across parts while each source reference
  still points back to the exact PDF part and local pages.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PROCESSED_ROOT = ROOT / "kb" / "mango-product-docs" / "processed"
LK_DOC = "kb/mango-product-docs/processed/mango-lk-manual"
LK_SOURCES = [
    "kb/mango-product-docs/sources/mango-lk-manual/LK_manual_v-121часть-1.pdf",
    "kb/mango-product-docs/sources/mango-lk-manual/LK_manual_v-121часть-2.pdf",
    "kb/mango-product-docs/sources/mango-lk-manual/LK_manual_v-121часть-3.pdf",
    "kb/mango-product-docs/sources/mango-lk-manual/LK_manual_v-121часть-4.pdf",
    "kb/mango-product-docs/sources/mango-lk-manual/LK_manual_v-121часть-5.pdf",
]
LK_PAGE_COUNTS = [101, 101, 101, 101, 164]

REQUIRED_SECTION_META = (
    "file",
    "number",
    "title",
    "pages",
    "pdf_section",
    "pdf_heading",
    "source_refs",
)
REQUIRED_REF_KEYS = ("source_pdf", "part", "pages", "global_pages")
REQUIRED_FM_KEYS = ("pdf_section", "pdf_heading", "pages", "source", "source_refs")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_json(path: Path, errors: list[str]) -> dict:
    if not path.exists():
        errors.append(f"{path.relative_to(ROOT)}: missing")
        return {}
    try:
        return json.loads(read_text(path))
    except json.JSONDecodeError as exc:
        errors.append(f"{path.relative_to(ROOT)}: invalid JSON ({exc})")
        return {}


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}
    data: dict[str, str] = {}
    for line in text[4:end].splitlines():
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if not match:
            continue
        value = match.group(2).strip()
        if (value.startswith('"') and value.endswith('"')) or (
            value.startswith("'") and value.endswith("'")
        ):
            value = value[1:-1]
        data[match.group(1)] = value
    return data


def parse_source_refs(raw, context: str, errors: list[str]) -> list[dict]:
    if isinstance(raw, list):
        refs = raw
    elif isinstance(raw, str):
        try:
            refs = json.loads(raw)
        except json.JSONDecodeError as exc:
            errors.append(f"{context}: source_refs is not JSON ({exc})")
            return []
    else:
        errors.append(f"{context}: source_refs must be a list or JSON string")
        return []

    if not refs:
        errors.append(f"{context}: source_refs is empty")
        return []
    for ref in refs:
        if not isinstance(ref, dict):
            errors.append(f"{context}: source_refs entry is not an object")
            continue
        for key in REQUIRED_REF_KEYS:
            if key not in ref:
                errors.append(f"{context}: source_refs entry missing {key!r}")
    return refs


def page_start(pages: str) -> int | None:
    match = re.match(r"^(\d+)(?:-\d+)?$", str(pages))
    return int(match.group(1)) if match else None


def check_doc_traceability(doc_dir: Path) -> list[str]:
    errors: list[str] = []
    rel_doc = str(doc_dir.relative_to(ROOT))
    meta = load_json(doc_dir / "meta.json", errors)
    if not meta:
        return errors

    sources = meta.get("sources")
    if not isinstance(sources, list) or not sources:
        errors.append(f"{rel_doc}/meta.json: sources must be a non-empty list")
    else:
        for source in sources:
            for key in ("order", "source_pdf", "page_count", "source_sha256"):
                if key not in source:
                    errors.append(f"{rel_doc}/meta.json: source entry missing {key!r}")

    if meta.get("part_count") != len(sources or []):
        errors.append(f"{rel_doc}/meta.json: part_count does not match sources")

    sections = meta.get("sections", [])
    if not isinstance(sections, list) or not sections:
        errors.append(f"{rel_doc}/meta.json: sections must be a non-empty list")
        return errors

    for entry in sections:
        context = f"{rel_doc}/meta.json section {entry.get('order', '?')}"
        for key in REQUIRED_SECTION_META:
            if key not in entry:
                errors.append(f"{context}: missing {key!r}")
        refs = parse_source_refs(entry.get("source_refs"), context, errors)
        if refs and entry.get("pages") != refs[0].get("global_pages") and len(refs) == 1:
            errors.append(f"{context}: pages must match source_refs[0].global_pages")

        section_path = doc_dir / str(entry.get("file", ""))
        if not section_path.exists():
            errors.append(f"{context}: file {entry.get('file')!r} missing")
            continue
        text = read_text(section_path)
        fm = parse_frontmatter(text)
        for key in REQUIRED_FM_KEYS:
            if key not in fm:
                errors.append(f"{section_path.relative_to(ROOT)}: frontmatter missing {key!r}")
        parse_source_refs(fm.get("source_refs"), str(section_path.relative_to(ROOT)), errors)
        if "> Трассировка:" not in text:
            errors.append(f"{section_path.relative_to(ROOT)}: missing human trace line")

    return errors


def check_lk_manual() -> list[str]:
    errors: list[str] = []
    doc_dir = ROOT / LK_DOC
    if not doc_dir.exists():
        return [f"{LK_DOC}: missing processed multi-part LK manual"]

    meta = load_json(doc_dir / "meta.json", errors)
    if not meta:
        return errors

    if meta.get("doc_code") != "LK":
        errors.append(f"{LK_DOC}/meta.json: doc_code must be LK")
    if meta.get("page_count") != sum(LK_PAGE_COUNTS):
        errors.append(f"{LK_DOC}/meta.json: page_count must be 568")
    if meta.get("part_count") != 5:
        errors.append(f"{LK_DOC}/meta.json: part_count must be 5")
    if meta.get("source_pdfs") != LK_SOURCES:
        errors.append(f"{LK_DOC}/meta.json: source_pdfs must list all five LK parts in order")

    sources = meta.get("sources", [])
    if [s.get("page_count") for s in sources] != LK_PAGE_COUNTS:
        errors.append(f"{LK_DOC}/meta.json: sources page_count must be {LK_PAGE_COUNTS}")

    sections = meta.get("sections", [])
    if len(sections) < 300:
        errors.append(f"{LK_DOC}/meta.json: expected 300+ LK sections from the five parts")
    if sum(1 for s in sections if s.get("title") == "Титульная часть") > 1:
        errors.append(f"{LK_DOC}/meta.json: continuation pages created extra title sections")

    part2_section = next((s for s in sections if s.get("pdf_section") == "4.4.1.3"), None)
    if not part2_section:
        errors.append(f"{LK_DOC}/meta.json: missing section 4.4.1.3 from part 2")
    else:
        if page_start(part2_section.get("pages", "")) != 102:
            errors.append(f"{LK_DOC}/meta.json: section 4.4.1.3 must start on global page 102")
        refs = parse_source_refs(part2_section.get("source_refs"), "LK section 4.4.1.3", errors)
        if refs and refs[0].get("part") != 2:
            errors.append(f"{LK_DOC}/meta.json: section 4.4.1.3 must point to source part 2")

    final_section = next(
        (
            s for s in sections
            if s.get("pdf_section") == "6" and s.get("title") == "Роли и права доступа ЛК ВАТС"
        ),
        None,
    )
    if not final_section:
        errors.append(f"{LK_DOC}/meta.json: missing final section 6")
    else:
        if final_section.get("pages") != "568":
            errors.append(f"{LK_DOC}/meta.json: section 6 must point to global page 568")
        refs = parse_source_refs(final_section.get("source_refs"), "LK section 6", errors)
        if refs and refs[0].get("part") != 5:
            errors.append(f"{LK_DOC}/meta.json: section 6 must point to source part 5")

    return errors


def iter_processed_doc_dirs() -> list[Path]:
    doc_dirs: list[Path] = []
    for meta_path in sorted(PROCESSED_ROOT.rglob("meta.json")):
        try:
            meta = json.loads(read_text(meta_path))
        except json.JSONDecodeError:
            doc_dirs.append(meta_path.parent)
            continue
        if meta.get("collection_type") == "multi_document":
            continue
        doc_dirs.append(meta_path.parent)
    return doc_dirs


def main() -> int:
    errors: list[str] = []
    for doc_dir in iter_processed_doc_dirs():
        errors += check_doc_traceability(doc_dir)
    errors += check_lk_manual()

    if errors:
        print("issue-117 KB traceability validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("issue-117 KB traceability validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
