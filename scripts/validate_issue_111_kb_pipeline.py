#!/usr/bin/env python3
"""Local/CI regression check for issue #111 — the KB ingestion pipeline.

Stdlib-only (no pdfplumber/tiktoken), so it runs in CI exactly like the other
``validate_issue_*`` checks. It locks the issue-#111 deliverables so later edits
cannot silently break them:

- the **ingestion scripts** exist (``scripts/kb/{extract,tokens,make_sample_pdf}.py``,
  ``requirements.txt``, ``README.md``);
- the **neutral KB layout** (ФТ-4) exists with the mandatory **manual-input
  directory** and its human guide: ``kb/mango-product-docs/sources/README.md`` (ФТ-7),
  ``kb/mango-product-docs/processed/README.md``, ``kb/fragments/README.md``, the document manifest
  and ``kb/mango-product-docs/sources/web-links/README.md``; the forbidden name ``mango-kc`` is not
  used as a path;
- the **extracted sample** is internally consistent: every ``kb/mango-product-docs/processed/*/``
  has ``index.md`` + ``meta.json``; ``section_count`` matches the section files;
  per-section token counts sum to ``tokens_total``; each section's frontmatter
  ``tokens`` matches ``meta.json``; the index links every section; referenced
  images exist;
- the **prompt examples** (ФТ-6) and the **experiment report** (ФТ-8) exist and
  carry the mandatory points: the five examples, the ``[CC, §…, с.…]`` citation,
  the whole-doc-vs-section token comparison, the tool comparison
  (marker/nougat/MinerU/pdfplumber), and the explicit "evolutionary step to a
  vector KB and RAG" statement;
- the checks are **wired**: CHANGELOG mentions issue #111 and the KB workflow
  runs this validator.

Run: ``python3 scripts/validate_issue_111_kb_pipeline.py`` (exit 0 = PASS).
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR_REF = "scripts/validate_issue_111_kb_pipeline.py"
KB_WORKFLOW = ".github/workflows/kb.yml"
REPORT = "docs/kb-experiment-report.md"
SAMPLE = "kb/mango-product-docs/processed/contact-center-manual-sample"

# Files that must exist (infrastructure + docs).
REQUIRED_FILES = (
    "scripts/kb/extract.py",
    "scripts/kb/tokens.py",
    "scripts/kb/make_sample_pdf.py",
    "scripts/kb/requirements.txt",
    "scripts/kb/README.md",
    "kb/mango-product-docs/sources/README.md",
    "kb/mango-product-docs/sources/contact-center-manual/source.md",
    "kb/mango-product-docs/sources/web-links/README.md",
    "kb/mango-product-docs/processed/README.md",
    "kb/fragments/README.md",
    "kb/mango-product-docs/USAGE.md",
    REPORT,
    KB_WORKFLOW,
    "Makefile",
)

# meta.json keys every extracted document must carry.
META_KEYS = (
    "doc_code", "extracted_by", "token_method", "page_count",
    "section_count", "tokens_total", "source_sha256", "sections",
)
# Section-file frontmatter keys every chunk must carry.
SECTION_FM_KEYS = ("id", "doc_code", "section", "pages", "source", "tokens", "status")

MAKE_TARGETS = ("kb-sample", "kb-extract", "kb-validate", "kb-tokens", "kb-clean")


def read_text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def require_file(path: str) -> list:
    return [] if (ROOT / path).exists() else [f"{path}: file does not exist"]


def require(text: str, path: str, *needles: str) -> list:
    return [f"{path}: missing {needle!r}" for needle in needles if needle not in text]


def parse_frontmatter(text: str) -> dict:
    """Tiny YAML-frontmatter reader (key: value), stdlib only."""
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    block = text[3:end]
    data = {}
    for line in block.splitlines():
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if m:
            value = m.group(2).strip().strip('"')
            data[m.group(1)] = value
    return data


def check_required_files() -> list:
    errors = []
    for path in REQUIRED_FILES:
        errors += require_file(path)
    return errors


def check_neutral_name() -> list:
    """ФТ-4 hard constraint: the forbidden name 'mango-kc' is not used as a path."""
    errors = []
    for path in ROOT.rglob("*"):
        if ".git/" in str(path):
            continue
        if "mango-kc" in path.name:
            rel = path.relative_to(ROOT)
            errors.append(f"{rel}: forbidden KB name 'mango-kc' used as a path (ФТ-4)")
    return errors


def check_manual_input_dir() -> list:
    """ФТ-4/ФТ-7: manual-input dir exists with a human replenishment guide."""
    errors = require_file("kb/mango-product-docs/sources/README.md")
    if errors:
        return errors
    text = read_text("kb/mango-product-docs/sources/README.md")
    # The guide must cover the ФТ-7 steps (add file, run, verify, update, web link).
    errors += require(
        text, "kb/mango-product-docs/sources/README.md",
        "Как добавить новый файл", "Как запустить обработку",
        "Как проверить результат", "Как обновить документ", "веб-ресурс",
    )
    return errors


def _section_files(doc_dir: Path) -> list:
    sections = doc_dir / "sections"
    if not sections.is_dir():
        return []
    return sorted(p for p in sections.glob("*.md"))


def check_extracted_doc(doc_rel: str) -> list:
    """Internal consistency of one kb/mango-product-docs/processed/<doc>/ artifact."""
    errors = []
    doc_dir = ROOT / doc_rel
    index_path = doc_dir / "index.md"
    meta_path = doc_dir / "meta.json"
    if not index_path.exists():
        errors.append(f"{doc_rel}/index.md: missing")
    if not meta_path.exists():
        errors.append(f"{doc_rel}/meta.json: missing")
    if errors:
        return errors

    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{doc_rel}/meta.json: invalid JSON ({exc})"]

    for key in META_KEYS:
        if key not in meta:
            errors.append(f"{doc_rel}/meta.json: missing key {key!r}")
    if errors:
        return errors

    index_text = index_path.read_text(encoding="utf-8")
    files = _section_files(doc_dir)

    # section_count == files on disk == entries in meta.sections.
    if meta["section_count"] != len(files):
        errors.append(
            f"{doc_rel}: section_count {meta['section_count']} != "
            f"{len(files)} files in sections/"
        )
    if len(meta["sections"]) != len(files):
        errors.append(
            f"{doc_rel}: meta.sections {len(meta['sections'])} != "
            f"{len(files)} files in sections/"
        )

    # Per-section consistency + token arithmetic.
    token_sum = 0
    for entry in meta["sections"]:
        rel_file = entry.get("file", "")
        sec_path = doc_dir / rel_file
        if not sec_path.exists():
            errors.append(f"{doc_rel}: meta lists missing section file {rel_file!r}")
            continue
        if rel_file not in index_text:
            errors.append(f"{doc_rel}/index.md: does not link section {rel_file!r}")
        fm = parse_frontmatter(sec_path.read_text(encoding="utf-8"))
        for key in SECTION_FM_KEYS:
            if key not in fm:
                errors.append(f"{doc_rel}/{rel_file}: frontmatter missing {key!r}")
        # Frontmatter tokens must match meta entry.
        meta_tokens = entry.get("tokens")
        token_sum += meta_tokens if isinstance(meta_tokens, int) else 0
        try:
            if int(fm.get("tokens", -1)) != meta_tokens:
                errors.append(
                    f"{doc_rel}/{rel_file}: frontmatter tokens {fm.get('tokens')} "
                    f"!= meta {meta_tokens}"
                )
        except ValueError:
            errors.append(f"{doc_rel}/{rel_file}: non-integer tokens frontmatter")

    if token_sum != meta["tokens_total"]:
        errors.append(
            f"{doc_rel}/meta.json: tokens_total {meta['tokens_total']} != "
            f"sum of section tokens {token_sum}"
        )

    # Every referenced image exists.
    for sec_path in files:
        text = sec_path.read_text(encoding="utf-8")
        for rel_img in re.findall(r"!\[[^\]]*\]\(\.\./(images/[^)]+)\)", text):
            if not (doc_dir / rel_img).exists():
                errors.append(
                    f"{doc_rel}/{sec_path.name}: references missing image {rel_img!r}"
                )
    return errors


def iter_processed_doc_dirs(processed: Path) -> list[Path]:
    """Return extracted KB document dirs, skipping collection-level meta.json files."""
    doc_dirs = []
    for meta_path in sorted(processed.rglob("meta.json")):
        doc_dir = meta_path.parent
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            doc_dirs.append(doc_dir)
            continue
        if meta.get("collection_type") == "multi_document":
            continue
        doc_dirs.append(doc_dir)
    return doc_dirs


def check_processed() -> list:
    """The sample must exist; every kb/mango-product-docs/processed/<doc>/ must be consistent."""
    errors = require_file(f"{SAMPLE}/index.md") + require_file(f"{SAMPLE}/meta.json")
    processed = ROOT / "kb" / "mango-product-docs" / "processed"
    found_any = False
    for doc_dir in iter_processed_doc_dirs(processed):
        found_any = True
        errors += check_extracted_doc(str(doc_dir.relative_to(ROOT)))
    if not found_any:
        errors.append("kb/mango-product-docs/processed/: no extracted document with meta.json found")
    return errors


def check_usage_examples() -> list:
    """ФТ-6: five concrete prompt examples + citation + token comparison."""
    path = "kb/mango-product-docs/USAGE.md"
    errors = require_file(path)
    if errors:
        return errors
    text = read_text(path)
    errors += require(text, path, "Пример 1", "Пример 2", "Пример 3",
                      "Пример 4", "Пример 5")
    # Concrete citation in project format and a token comparison.
    if not re.search(r"\[CC,\s*§[\d.]+,\s*с\.\d+\]", text):
        errors.append(f"{path}: missing concrete citation like '[CC, §4.2, с.5]' (ФТ-6 пример 4)")
    errors += require(text, path, "Весь документ", "1587")
    return errors


def check_report() -> list:
    """ФТ-8: report carries the mandatory points."""
    errors = require_file(REPORT)
    if errors:
        return errors
    text = read_text(REPORT)
    # Tool comparison (ФТ-2) must name the alternatives and the chosen tool.
    errors += require(text, REPORT, "marker", "nougat", "MinerU", "pdfplumber")
    # Quality priority + extraction-quality evaluation.
    errors += require(text, REPORT, "качество")
    # Section splitting scripts-vs-LLM (ФТ-3).
    if not re.search(r"LLM", text):
        errors.append(f"{REPORT}: must discuss scripts-vs-LLM splitting (ФТ-3)")
    # Mandatory: explicit evolutionary step to vector KB and RAG.
    if not (re.search(r"эволюционн", text) and "RAG" in text and re.search(r"вектор", text)):
        errors.append(f"{REPORT}: must explicitly state KB is an evolutionary step to a vector KB and RAG")
    return errors


def check_wiring() -> list:
    """Checks actually run: CHANGELOG mentions #111; KB workflow runs the validator."""
    errors = require_file("CHANGELOG.md") + require_file(KB_WORKFLOW) + require_file("Makefile")
    if errors:
        return errors
    errors += require(read_text("CHANGELOG.md"), "CHANGELOG.md", "Issue #111")
    errors += require(read_text(KB_WORKFLOW), KB_WORKFLOW, VALIDATOR_REF)
    errors += require(read_text("Makefile"), "Makefile", *MAKE_TARGETS)
    return errors


def main() -> int:
    errors = []
    errors += check_required_files()
    errors += check_neutral_name()
    errors += check_manual_input_dir()
    errors += check_processed()
    errors += check_usage_examples()
    errors += check_report()
    errors += check_wiring()

    if errors:
        print("issue-111 KB pipeline validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("issue-111 KB pipeline validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
