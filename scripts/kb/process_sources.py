#!/usr/bin/env python3
"""Manifest-driven KB source processor (issue #121).

The low-level extractor intentionally knows only how to turn one logical
document (one PDF or several PDF parts) into one processed KB directory. This
runner adds the source-folder contract on top:

- ``single``: one source file -> one processed KB;
- ``multi_part``: several physical files -> one logical document and one KB;
- ``multi_document``: one product/documentation set -> a collection with one
  nested KB per independent document.

The manifest is ``kb/sources/<slug>/meta.json``. Existing source folders remain
backward-compatible: if ``processing_mode`` is absent, the runner infers it from
``documents``/``parts``/PDF count, but new sources should set the mode explicitly.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCES_ROOT = ROOT / "kb" / "sources"
PROCESSED_ROOT = ROOT / "kb" / "processed"
EXTRACTOR = ROOT / "scripts" / "kb" / "extract.py"

VALID_MODES = {"single", "multi_part", "multi_document"}
LFS_POINTER_PREFIX = b"version https://git-lfs.github.com/spec/v1\n"


class ManifestError(ValueError):
    """Source manifest is missing required data or points to invalid files."""


@dataclass(frozen=True)
class ExtractJob:
    source_dir: Path
    output_dir: Path
    pdf_paths: tuple[Path, ...]
    doc_code: str
    doc_title: str
    doc_version: str
    note: str
    source_mode: str
    source_set: str
    source_document: str

    @property
    def output_slug(self) -> str:
        return self.output_dir.name


@dataclass(frozen=True)
class SourcePlan:
    source_dir: Path
    mode: str
    name: str
    version: str
    output_dir: Path
    jobs: tuple[ExtractJob, ...]
    manifest: dict

    @property
    def collection(self) -> bool:
        return self.mode == "multi_document"


def rel_to_root(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def slugify(text: str, max_len: int = 56) -> str:
    slug = text.lower()
    translit = {
        "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "e",
        "ж": "zh", "з": "z", "и": "i", "й": "y", "к": "k", "л": "l", "м": "m",
        "н": "n", "о": "o", "п": "p", "р": "r", "с": "s", "т": "t", "у": "u",
        "ф": "f", "х": "h", "ц": "c", "ч": "ch", "ш": "sh", "щ": "sch", "ъ": "",
        "ы": "y", "ь": "", "э": "e", "ю": "yu", "я": "ya",
    }
    slug = "".join(translit.get(ch, ch) for ch in slug)
    slug = re.sub(r"[^a-z0-9]+", "-", slug).strip("-")
    return slug[:max_len].strip("-") or "document"


def natural_key(path: Path) -> list[object]:
    parts = re.split(r"(\d+)", path.name.lower())
    return [int(part) if part.isdigit() else part for part in parts]


def load_manifest(source_dir: Path) -> dict:
    manifest_path = source_dir / "meta.json"
    if not manifest_path.exists():
        raise ManifestError(f"{rel_to_root(manifest_path)}: missing source manifest")
    try:
        return json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ManifestError(f"{rel_to_root(manifest_path)}: invalid JSON ({exc})") from exc


def infer_mode(source_dir: Path, manifest: dict) -> str:
    explicit = manifest.get("processing_mode")
    if explicit:
        if explicit not in VALID_MODES:
            raise ManifestError(
                f"{rel_to_root(source_dir / 'meta.json')}: processing_mode must be one of "
                f"{', '.join(sorted(VALID_MODES))}"
            )
        return explicit
    if manifest.get("documents"):
        return "multi_document"
    if int(manifest.get("parts") or 0) > 1:
        return "multi_part"
    files = manifest.get("source_files")
    if isinstance(files, list) and len(files) > 1:
        return "multi_part"
    return "single"


def resolve_files(
    source_dir: Path,
    files: object,
    context: str,
    require_sources: bool = True,
) -> tuple[Path, ...]:
    if files is None:
        discovered = sorted(source_dir.glob("*.pdf"), key=natural_key)
        if not discovered:
            raise ManifestError(f"{context}: no PDF files found")
        return tuple(discovered)
    if not isinstance(files, list) or not files:
        raise ManifestError(f"{context}: source_files must be a non-empty list")

    resolved: list[Path] = []
    for item in files:
        if not isinstance(item, str) or not item.strip():
            raise ManifestError(f"{context}: source_files entries must be non-empty strings")
        path = (source_dir / item).resolve()
        try:
            path.relative_to(source_dir.resolve())
        except ValueError as exc:
            raise ManifestError(f"{context}: source file {item!r} escapes source directory") from exc
        if require_sources and not path.exists():
            raise ManifestError(f"{context}: source file {item!r} does not exist")
        resolved.append(path)
    return tuple(resolved)


def doc_code_default(source_slug: str) -> str:
    letters = re.sub(r"[^A-Za-z0-9]", "", source_slug.upper())
    return (letters[:12] or "DOC")


def ensure_pdf_payload(path: Path) -> None:
    with path.open("rb") as handle:
        head = handle.read(len(LFS_POINTER_PREFIX))
    if head == LFS_POINTER_PREFIX:
        raise ManifestError(
            f"{rel_to_root(path)}: Git LFS pointer checked out instead of PDF bytes; "
            "install Git LFS and run 'git lfs pull', or run the KB workflow with lfs: true"
        )
    if not head.startswith(b"%PDF"):
        raise ManifestError(f"{rel_to_root(path)}: not a PDF payload")


def make_job(
    source_dir: Path,
    output_dir: Path,
    pdf_paths: tuple[Path, ...],
    manifest: dict,
    mode: str,
    source_set: str,
    source_document: str,
    doc_meta: dict | None = None,
) -> ExtractJob:
    doc_meta = doc_meta or {}
    source_slug = source_dir.name
    title = str(doc_meta.get("title") or manifest.get("name") or source_slug)
    version = str(doc_meta.get("version") or manifest.get("version") or "unknown")
    code = str(doc_meta.get("doc_code") or manifest.get("doc_code") or doc_code_default(output_dir.name))
    note = str(doc_meta.get("description") or manifest.get("description") or "")
    return ExtractJob(
        source_dir=source_dir,
        output_dir=output_dir,
        pdf_paths=pdf_paths,
        doc_code=code,
        doc_title=title,
        doc_version=version,
        note=note,
        source_mode=mode,
        source_set=source_set,
        source_document=source_document,
    )


def build_plan(
    source_dir: Path,
    processed_root: Path = PROCESSED_ROOT,
    require_sources: bool = True,
) -> SourcePlan:
    source_dir = source_dir.resolve()
    manifest = load_manifest(source_dir)
    mode = infer_mode(source_dir, manifest)
    source_slug = source_dir.name
    name = str(manifest.get("name") or source_slug)
    version = str(manifest.get("version") or "unknown")
    collection_slug = str(manifest.get("output_slug") or source_slug)
    collection_dir = (processed_root / collection_slug).resolve()

    if mode in {"single", "multi_part"}:
        files = resolve_files(
            source_dir,
            manifest.get("source_files"),
            rel_to_root(source_dir / "meta.json"),
            require_sources=require_sources,
        )
        if mode == "single" and len(files) != 1:
            raise ManifestError(f"{rel_to_root(source_dir / 'meta.json')}: single mode requires exactly one PDF")
        if mode == "multi_part" and len(files) < 2:
            raise ManifestError(f"{rel_to_root(source_dir / 'meta.json')}: multi_part mode requires 2+ PDFs")
        job = make_job(
            source_dir=source_dir,
            output_dir=collection_dir,
            pdf_paths=files,
            manifest=manifest,
            mode=mode,
            source_set=collection_slug,
            source_document=collection_slug,
        )
        return SourcePlan(source_dir, mode, name, version, collection_dir, (job,), manifest)

    documents = manifest.get("documents")
    if not isinstance(documents, list) or not documents:
        raise ManifestError(f"{rel_to_root(source_dir / 'meta.json')}: documents must be a non-empty list")

    jobs: list[ExtractJob] = []
    seen_slugs: set[str] = set()
    for index, doc in enumerate(documents, start=1):
        if not isinstance(doc, dict):
            raise ManifestError(f"{rel_to_root(source_dir / 'meta.json')}: documents[{index}] must be an object")
        files = doc.get("source_files")
        if files is None and doc.get("file_name"):
            files = [doc["file_name"]]
        context = f"{rel_to_root(source_dir / 'meta.json')}: documents[{index}]"
        pdf_paths = resolve_files(source_dir, files, context, require_sources=require_sources)
        doc_slug = str(doc.get("output_slug") or slugify(doc.get("title") or pdf_paths[0].stem))
        if doc_slug in seen_slugs:
            raise ManifestError(f"{context}: duplicate output_slug {doc_slug!r}")
        seen_slugs.add(doc_slug)
        doc_mode = "multi_part" if len(pdf_paths) > 1 else "single"
        jobs.append(
            make_job(
                source_dir=source_dir,
                output_dir=collection_dir / doc_slug,
                pdf_paths=pdf_paths,
                manifest=manifest,
                mode=doc_mode,
                source_set=collection_slug,
                source_document=doc_slug,
                doc_meta=doc,
            )
        )
    return SourcePlan(source_dir, mode, name, version, collection_dir, tuple(jobs), manifest)


def job_command(job: ExtractJob, python_bin: str, extractor: Path) -> list[str]:
    return [
        python_bin,
        str(extractor),
        *[str(path) for path in job.pdf_paths],
        "--out",
        str(job.output_dir),
        "--doc-code",
        job.doc_code,
        "--doc-title",
        job.doc_title,
        "--doc-version",
        job.doc_version,
        "--note",
        job.note,
        "--source-mode",
        job.source_mode,
        "--source-set",
        job.source_set,
        "--source-document",
        job.source_document,
    ]


def print_plan(plan: SourcePlan, as_json: bool = False) -> None:
    data = {
        "source_dir": rel_to_root(plan.source_dir),
        "processing_mode": plan.mode,
        "name": plan.name,
        "version": plan.version,
        "output_dir": rel_to_root(plan.output_dir),
        "jobs": [
            {
                "output_dir": rel_to_root(job.output_dir),
                "doc_code": job.doc_code,
                "doc_title": job.doc_title,
                "doc_version": job.doc_version,
                "source_mode": job.source_mode,
                "source_document": job.source_document,
                "source_files": [rel_to_root(path) for path in job.pdf_paths],
            }
            for job in plan.jobs
        ],
    }
    if as_json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return
    print(f"{rel_to_root(plan.source_dir)}: {plan.mode} -> {rel_to_root(plan.output_dir)}")
    for job in plan.jobs:
        sources = ", ".join(rel_to_root(path) for path in job.pdf_paths)
        print(f"- {job.source_document}: {sources} -> {rel_to_root(job.output_dir)}")


def clean_stale_collection_docs(plan: SourcePlan) -> None:
    if not plan.collection or not plan.output_dir.exists():
        return
    expected = {job.output_dir.name for job in plan.jobs}
    for child in sorted(plan.output_dir.iterdir()):
        if not child.is_dir() or child.name in expected:
            continue
        if (child / "meta.json").exists():
            shutil.rmtree(child)


def read_child_meta(job: ExtractJob) -> dict:
    meta_path = job.output_dir / "meta.json"
    if not meta_path.exists():
        return {}
    return json.loads(meta_path.read_text(encoding="utf-8"))


def write_collection_index(plan: SourcePlan) -> None:
    plan.output_dir.mkdir(parents=True, exist_ok=True)
    documents = []
    for job in plan.jobs:
        child_meta = read_child_meta(job)
        documents.append({
            "slug": job.output_dir.name,
            "title": job.doc_title,
            "doc_code": job.doc_code,
            "version": job.doc_version,
            "source_files": [rel_to_root(path) for path in job.pdf_paths],
            "output": rel_to_root(job.output_dir),
            "index": f"{job.output_dir.name}/index.md",
            "meta": f"{job.output_dir.name}/meta.json",
            "page_count": child_meta.get("page_count"),
            "section_count": child_meta.get("section_count"),
            "tokens_total": child_meta.get("tokens_total"),
        })

    collection_meta = {
        "collection_type": "multi_document",
        "processing_mode": "multi_document",
        "name": plan.name,
        "version": plan.version,
        "product": plan.manifest.get("product"),
        "language": plan.manifest.get("language"),
        "source_dir": rel_to_root(plan.source_dir),
        "document_count": len(documents),
        "documents": documents,
        "total_pages": sum(d["page_count"] or 0 for d in documents),
        "tokens_total": sum(d["tokens_total"] or 0 for d in documents),
        "generated_by": rel_to_root(Path(__file__)),
    }
    (plan.output_dir / "meta.json").write_text(
        json.dumps(collection_meta, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    lines = [
        "---",
        "type: kb-multi-document-index",
        "status: extracted",
        "ai-generated: true",
        "---",
        "",
        f"# {plan.name} — комплект документации",
        "",
        f"> Источник: `{rel_to_root(plan.source_dir)}` · документов: {len(documents)}.",
        "",
        "| Документ | Код | Версия | Файл БЗ | Страницы | Разделы | Токены |",
        "| --- | --- | --- | --- | ---: | ---: | ---: |",
    ]
    for doc in documents:
        lines.append(
            f'| {doc["title"]} | {doc["doc_code"]} | {doc["version"]} | '
            f'[{doc["index"]}]({doc["index"]}) | {doc["page_count"] or 0} | '
            f'{doc["section_count"] or 0} | {doc["tokens_total"] or 0} |'
        )
    lines.append("")
    (plan.output_dir / "index.md").write_text("\n".join(lines), encoding="utf-8")


def execute_plan(plan: SourcePlan, python_bin: str, extractor: Path, dry_run: bool = False) -> None:
    print_plan(plan)
    if dry_run:
        return
    for job in plan.jobs:
        for pdf_path in job.pdf_paths:
            ensure_pdf_payload(pdf_path)
    clean_stale_collection_docs(plan)
    for job in plan.jobs:
        subprocess.run(job_command(job, python_bin, extractor), check=True)
    if plan.collection:
        write_collection_index(plan)


def iter_source_dirs() -> list[Path]:
    return sorted(path.parent for path in SOURCES_ROOT.glob("*/meta.json"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Process kb/sources/<slug>/meta.json manifests.")
    parser.add_argument("source_dir", nargs="?", help="source directory with meta.json")
    parser.add_argument("--all", action="store_true", help="process every kb/sources/*/meta.json")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="validate the manifest and print the extraction plan without reading PDF payloads",
    )
    parser.add_argument("--json", action="store_true", help="print dry-run plan as JSON")
    parser.add_argument("--python", default=sys.executable, help="Python executable for extract.py")
    parser.add_argument("--extractor", default=str(EXTRACTOR), help="path to scripts/kb/extract.py")
    parser.add_argument("--processed-root", default=str(PROCESSED_ROOT), help="processed KB root")
    args = parser.parse_args(argv)

    if args.all == bool(args.source_dir):
        parser.error("pass either source_dir or --all")

    source_dirs = iter_source_dirs() if args.all else [Path(args.source_dir)]
    try:
        processed_root = Path(args.processed_root).resolve()
        plans = [
            build_plan(path, processed_root, require_sources=not args.dry_run)
            for path in source_dirs
        ]
        for plan in plans:
            if args.json:
                print_plan(plan, as_json=True)
                if not args.dry_run:
                    raise ManifestError("--json is only supported with --dry-run")
            else:
                execute_plan(plan, args.python, Path(args.extractor).resolve(), dry_run=args.dry_run)
        return 0
    except ManifestError as exc:
        print(f"KB source manifest error: {exc}", file=sys.stderr)
        return 2
    except subprocess.CalledProcessError as exc:
        print(f"KB extraction failed with exit code {exc.returncode}", file=sys.stderr)
        return exc.returncode or 1


if __name__ == "__main__":
    raise SystemExit(main())
