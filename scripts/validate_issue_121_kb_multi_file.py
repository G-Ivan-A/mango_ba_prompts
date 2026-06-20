#!/usr/bin/env python3
"""Regression check for issue #121 — KB multi-file source scenarios.

The heavy PDF extraction remains a manual/dispatch workflow. This stdlib-only
validator locks the source manifest contract and update semantics that decide
which extraction jobs must run:

- ``single``: one file becomes one KB;
- ``multi_part``: N files are one logical document and one KB;
- ``multi_document``: N independent documents become a product collection with
  one nested KB per document;
- update cases keep stable output directories while changing source files, and
  stale generated multi-document children are removed when the manifest removes
  or renames a document.
"""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "kb"))

from process_sources import (  # noqa: E402
    ManifestError,
    build_plan,
    clean_stale_collection_docs,
    infer_mode,
)

RUNNER = "scripts/kb/process_sources.py"
WORKFLOW = ".github/workflows/kb.yml"
MAKEFILE = "Makefile"
SOURCES_README = "kb/sources/README.md"
KB_README = "scripts/kb/README.md"

CC_SOURCES = [
    "CC_manual_1.26.23-part-1.pdf",
    "CC_manual_1.26.23-part-2.pdf",
    "CC_manual_1.26.23-part-3.pdf",
    "CC_manual_1.26.23-part-4.pdf",
    "CC_manual_1.26.23-part-5.pdf",
    "CC_manual_1.26.23-part-6.pdf",
]
LK_SOURCES = [
    "LK_manual_v-121часть-1.pdf",
    "LK_manual_v-121часть-2.pdf",
    "LK_manual_v-121часть-3.pdf",
    "LK_manual_v-121часть-4.pdf",
    "LK_manual_v-121часть-5.pdf",
]
MTALKER_DOCS = {
    "quick-start": "mTalker_Quick_start.pdf",
    "windows-mac-working": "mTalker_User_Guide_ch1_Working.pdf",
    "windows-mac-settings": "mTalker_User_Guide_ch2_Settings.pdf",
    "windows-mac-admin": "mTalker_User_Guide_ch3_Admin_Guide.pdf",
    "android-user-guide": "UserGuide_mTalker_4Mobile.pdf",
}


def read_text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def require_path(path: str) -> list[str]:
    return [] if (ROOT / path).exists() else [f"{path}: missing"]


def require_text(text: str, path: str, *needles: str) -> list[str]:
    return [f"{path}: missing {needle!r}" for needle in needles if needle not in text]


def load_json(path: str, errors: list[str]) -> dict:
    full = ROOT / path
    if not full.exists():
        errors.append(f"{path}: missing")
        return {}
    try:
        return json.loads(full.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"{path}: invalid JSON ({exc})")
        return {}


def rel_paths(paths: tuple[Path, ...], source_dir: Path) -> list[str]:
    return [str(path.relative_to(source_dir)) for path in paths]


def check_real_manifests() -> list[str]:
    errors: list[str] = []

    cc = load_json("kb/sources/mango-cc-manual/meta.json", errors)
    lk = load_json("kb/sources/mango-lk-manual/meta.json", errors)
    mtalker = load_json("kb/sources/mtalker/meta.json", errors)
    if errors:
        return errors

    if cc.get("processing_mode") != "multi_part":
        errors.append("kb/sources/mango-cc-manual/meta.json: processing_mode must be multi_part")
    if cc.get("source_files") != CC_SOURCES:
        errors.append("kb/sources/mango-cc-manual/meta.json: source_files must list six CC parts")
    if cc.get("output_slug") != "mango-cc-manual" or cc.get("doc_code") != "CC":
        errors.append("kb/sources/mango-cc-manual/meta.json: output_slug/doc_code mismatch")

    if lk.get("processing_mode") != "multi_part":
        errors.append("kb/sources/mango-lk-manual/meta.json: processing_mode must be multi_part")
    if lk.get("source_files") != LK_SOURCES:
        errors.append("kb/sources/mango-lk-manual/meta.json: source_files must list five LK parts")
    if lk.get("output_slug") != "mango-lk-manual" or lk.get("doc_code") != "LK":
        errors.append("kb/sources/mango-lk-manual/meta.json: output_slug/doc_code mismatch")

    if mtalker.get("processing_mode") != "multi_document":
        errors.append("kb/sources/mtalker/meta.json: processing_mode must be multi_document")
    if mtalker.get("output_slug") != "mtalker":
        errors.append("kb/sources/mtalker/meta.json: output_slug must be mtalker")

    documents = mtalker.get("documents", [])
    by_slug = {doc.get("output_slug"): doc for doc in documents if isinstance(doc, dict)}
    if set(by_slug) != set(MTALKER_DOCS):
        errors.append("kb/sources/mtalker/meta.json: documents must define the expected output slugs")
    for slug, file_name in MTALKER_DOCS.items():
        doc = by_slug.get(slug, {})
        if doc.get("file_name") != file_name:
            errors.append(f"kb/sources/mtalker/meta.json: {slug} must point to {file_name}")
        if not doc.get("doc_code"):
            errors.append(f"kb/sources/mtalker/meta.json: {slug} missing doc_code")

    for source_dir in (
        ROOT / "kb/sources/mango-cc-manual",
        ROOT / "kb/sources/mango-lk-manual",
        ROOT / "kb/sources/mtalker",
    ):
        try:
            plan = build_plan(source_dir)
        except ManifestError as exc:
            errors.append(str(exc))
            continue
        if source_dir.name == "mango-cc-manual":
            job = plan.jobs[0]
            if plan.mode != "multi_part" or rel_paths(job.pdf_paths, source_dir) != CC_SOURCES:
                errors.append("mango-cc-manual plan: expected one multi_part job with six files")
        elif source_dir.name == "mango-lk-manual":
            job = plan.jobs[0]
            if plan.mode != "multi_part" or rel_paths(job.pdf_paths, source_dir) != LK_SOURCES:
                errors.append("mango-lk-manual plan: expected one multi_part job with five files")
        elif source_dir.name == "mtalker":
            slugs = [job.output_dir.name for job in plan.jobs]
            if plan.mode != "multi_document" or slugs != list(MTALKER_DOCS):
                errors.append("mtalker plan: expected five nested multi_document jobs in manifest order")
            if any(job.source_mode != "single" for job in plan.jobs):
                errors.append("mtalker plan: every current document must be an independent single-file KB")

    return errors


def write_manifest(source_dir: Path, data: dict) -> None:
    source_dir.mkdir(parents=True, exist_ok=True)
    (source_dir / "meta.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")


def touch_sources(source_dir: Path, *names: str) -> None:
    source_dir.mkdir(parents=True, exist_ok=True)
    for name in names:
        (source_dir / name).write_text("%PDF-1.4\n", encoding="utf-8")


def check_synthetic_update_scenarios() -> list[str]:
    errors: list[str] = []
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        processed_root = tmp_path / "processed"

        # Single-file baseline: one file -> one stable output.
        single_dir = tmp_path / "sources" / "single-doc"
        touch_sources(single_dir, "manual.pdf")
        write_manifest(single_dir, {
            "name": "Single Doc",
            "version": "1",
            "processing_mode": "single",
            "output_slug": "stable-doc",
            "source_files": ["manual.pdf"],
        })
        single_plan = build_plan(single_dir, processed_root)
        if single_plan.mode != "single" or len(single_plan.jobs[0].pdf_paths) != 1:
            errors.append("synthetic single: expected one source file")
        if single_plan.jobs[0].output_dir != processed_root / "stable-doc":
            errors.append("synthetic single: output directory must stay stable")

        # 1 -> N update: same output, source list changes to multi_part.
        touch_sources(single_dir, "part-1.pdf", "part-2.pdf")
        write_manifest(single_dir, {
            "name": "Single Doc",
            "version": "2",
            "processing_mode": "multi_part",
            "output_slug": "stable-doc",
            "source_files": ["part-1.pdf", "part-2.pdf"],
        })
        split_plan = build_plan(single_dir, processed_root)
        if split_plan.jobs[0].output_dir != single_plan.jobs[0].output_dir:
            errors.append("synthetic 1->N: output directory changed")
        if len(split_plan.jobs[0].pdf_paths) != 2:
            errors.append("synthetic 1->N: expected two source parts")

        # N -> 1 update: same output, mode returns to single.
        write_manifest(single_dir, {
            "name": "Single Doc",
            "version": "3",
            "processing_mode": "single",
            "output_slug": "stable-doc",
            "source_files": ["manual.pdf"],
        })
        joined_plan = build_plan(single_dir, processed_root)
        if joined_plan.jobs[0].output_dir != single_plan.jobs[0].output_dir:
            errors.append("synthetic N->1: output directory changed")

        # Multi-document add/delete: collection keeps expected child dirs and removes stale generated dirs.
        multi_dir = tmp_path / "sources" / "product-docs"
        touch_sources(multi_dir, "a.pdf", "b.pdf")
        write_manifest(multi_dir, {
            "name": "Product Docs",
            "version": "1",
            "processing_mode": "multi_document",
            "output_slug": "product",
            "documents": [
                {"file_name": "a.pdf", "output_slug": "doc-a", "title": "Doc A"},
                {"file_name": "b.pdf", "output_slug": "doc-b", "title": "Doc B"},
            ],
        })
        multi_plan = build_plan(multi_dir, processed_root)
        if [job.output_dir.name for job in multi_plan.jobs] != ["doc-a", "doc-b"]:
            errors.append("synthetic multi_document: expected two child jobs")
        stale = processed_root / "product" / "removed-doc"
        stale.mkdir(parents=True)
        (stale / "meta.json").write_text("{}", encoding="utf-8")
        keep = processed_root / "product" / "doc-a"
        keep.mkdir(parents=True)
        (keep / "meta.json").write_text("{}", encoding="utf-8")
        clean_stale_collection_docs(multi_plan)
        if stale.exists():
            errors.append("synthetic multi_document delete: stale generated child was not removed")
        if not keep.exists():
            errors.append("synthetic multi_document add/delete: expected child was removed")

        # Inference remains backward-compatible for old manifests.
        if infer_mode(multi_dir, {"documents": [{"file_name": "a.pdf"}]}) != "multi_document":
            errors.append("mode inference: documents should imply multi_document")
        if infer_mode(single_dir, {"parts": 2}) != "multi_part":
            errors.append("mode inference: parts > 1 should imply multi_part")

    return errors


def check_docs_and_wiring() -> list[str]:
    errors = []
    for path in (RUNNER, WORKFLOW, MAKEFILE, SOURCES_README, KB_README):
        errors += require_path(path)
    if errors:
        return errors

    runner = read_text(RUNNER)
    errors += require_text(
        runner,
        RUNNER,
        "processing_mode",
        "multi_part",
        "multi_document",
        "Git LFS pointer checked out instead of PDF bytes",
        "clean_stale_collection_docs",
    )

    makefile = read_text(MAKEFILE)
    errors += require_text(
        makefile,
        MAKEFILE,
        "kb-source-plan",
        "kb-source-extract",
        "kb-mtalker",
        "validate_issue_121_kb_multi_file.py",
    )

    workflow = read_text(WORKFLOW)
    errors += require_text(
        workflow,
        WORKFLOW,
        "source_dir:",
        "scripts/kb/process_sources.py",
        "validate_issue_121_kb_multi_file.py",
    )

    sources_readme = read_text(SOURCES_README)
    errors += require_text(
        sources_readme,
        SOURCES_README,
        "processing_mode",
        "single",
        "multi_part",
        "multi_document",
        "Сценарий 1",
        "Сценарий 6",
        "1 → N",
        "N → 1",
        "Troubleshooting",
    )

    kb_readme = read_text(KB_README)
    errors += require_text(kb_readme, KB_README, "process_sources.py", "multi-document")
    return errors


def main() -> int:
    errors: list[str] = []
    errors += check_real_manifests()
    errors += check_synthetic_update_scenarios()
    errors += check_docs_and_wiring()

    if errors:
        print("issue-121 KB multi-file validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("issue-121 KB multi-file validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
