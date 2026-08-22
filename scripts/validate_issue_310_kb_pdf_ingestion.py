#!/usr/bin/env python3
"""Regression check for issue #310 — четыре PDF в БЗ + защита от галлюцинаций.

Stdlib-only, как остальные ``validate_issue_*``: запускается локально
(``make kb-validate``) и в лёгком шаге CI, без pip и без исходных PDF.

Фиксирует деливераблы issue #310:

- устаревший каталог ``kb/processed/contact-center-manual-sample`` удалён и на
  него не осталось живых ссылок в действующих файлах БЗ и Makefile;
- для каждого из четырёх документов задачи есть свой раздел БЗ:
  ``index.md`` + ``meta.json`` + ``verification.md``;
- ``index.md`` каждого раздела несёт frontmatter прослеживаемости
  (``source_document``, ``extraction_date``, ``model_used``,
  ``confidence_level``, ``pages_covered``);
- ``meta.json`` несёт блок ``verification`` перекрёстной проверки;
- каждый маркер неоднозначности (``ТРЕБУЕТСЯ ПРОВЕРКА`` / ``ПРОБЕЛ
  ИЗВЛЕЧЕНИЯ``) содержит имя PDF и номер страницы — иначе локальная сверка
  невозможна, ведь PDF в репозитории не хранятся;
- исходные PDF не закоммичены (кроме синтетических ``*.fixture.pdf``) и Git LFS
  не используется;
- инструменты проверки и negative-тест на месте, CHANGELOG упоминает задачу.

Run: ``python3 scripts/validate_issue_310_kb_pdf_ingestion.py`` (exit 0 = PASS).
"""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

STALE_DOC = "kb/processed/contact-center-manual-sample"
VERIFIER = "scripts/kb/verify_extraction.py"
NEGATIVE_TEST = "experiments/kb-verify-detects-hallucination.py"

# Один PDF задачи = один раздел БЗ.
DOCS = {
    "kb/processed/integration-1c": "Integratsiya_virtualnoy_ats_Pryamaya_integraciya_s_1C.pdf",
    "kb/processed/vpbx-api": "MangoOffice_VPBX_API_v1.9.pdf",
    "kb/processed/lk-vats-sso": "MANGO_OFFICE_LK_VATS_Auth_SSO.pdf",
    "kb/processed/rolevaya-model-vats": "Rolevaya-model-VATS_1_26_08.pdf",
}

TRACEABILITY_KEYS = (
    "source_document",
    "extraction_date",
    "model_used",
    "confidence_level",
    "pages_covered",
)
CONFIDENCE_VALUES = {"high", "medium", "requires_review"}

# Реальный маркер — жирный, с двоеточием: «> ⚠️ **ПРОБЕЛ ИЗВЛЕЧЕНИЯ**: …».
# Упоминание названий маркеров в легенде индекса под это не подпадает.
MARKER_RE = re.compile(r"\*\*(?:ТРЕБУЕТСЯ ПРОВЕРКА|ПРОБЕЛ ИЗВЛЕЧЕНИЯ)\*\*\s*:")

# Файлы, где упоминание удалённого каталога — историческая запись, а не ссылка.
STALE_MENTION_ALLOWED = {
    "CHANGELOG.md",
    "docs/kb-experiment-report.md",
    "kb/processed/README.md",
    "kb/sources/contact-center-manual/source.md",
    "kb/USAGE.md",
    "scripts/validate_issue_310_kb_pdf_ingestion.py",
}


def read_text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def parse_frontmatter(text: str) -> dict:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    data = {}
    for line in text[3:end].splitlines():
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if match:
            data[match.group(1)] = match.group(2).strip().strip('"')
    return data


def check_stale_removed() -> list:
    """Каталог удалён, и на него не осталось живых ссылок."""
    errors = []
    if (ROOT / STALE_DOC).exists():
        errors.append(f"{STALE_DOC}: stale sample KB must be deleted (issue #310)")
    live_refs = (
        STALE_DOC,                                   # kb/processed/<slug>
        "](contact-center-manual-sample/",           # ссылка изнутри kb/processed/
        "](processed/contact-center-manual-sample/",  # ссылка изнутри kb/
    )
    candidates = sorted((ROOT / "kb").rglob("*.md")) + [ROOT / "Makefile"]
    for path in candidates:
        rel = str(path.relative_to(ROOT))
        if rel in STALE_MENTION_ALLOWED:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for needle in live_refs:
            if needle in text:
                errors.append(f"{rel}: still references the deleted {STALE_DOC}")
                break
    return errors


def check_documents() -> list:
    errors = []
    for doc, pdf_name in DOCS.items():
        doc_dir = ROOT / doc
        for name in ("index.md", "meta.json", "verification.md"):
            if not (doc_dir / name).exists():
                errors.append(f"{doc}/{name}: missing (issue #310 deliverable)")
        if errors and not (doc_dir / "meta.json").exists():
            continue

        index_fm = parse_frontmatter((doc_dir / "index.md").read_text(encoding="utf-8"))
        for key in TRACEABILITY_KEYS:
            if not index_fm.get(key):
                errors.append(f"{doc}/index.md: frontmatter is missing {key!r}")
        confidence = index_fm.get("confidence_level")
        if confidence and confidence not in CONFIDENCE_VALUES:
            errors.append(
                f"{doc}/index.md: confidence_level={confidence!r} is not one of "
                f"{sorted(CONFIDENCE_VALUES)}"
            )
        if index_fm.get("source_document") and pdf_name not in index_fm["source_document"]:
            errors.append(
                f"{doc}/index.md: source_document must name {pdf_name!r} "
                f"(got {index_fm['source_document']!r})"
            )

        meta = json.loads((doc_dir / "meta.json").read_text(encoding="utf-8"))
        verification = meta.get("verification")
        if not isinstance(verification, dict):
            errors.append(f"{doc}/meta.json: missing 'verification' block")
            continue
        for key in ("method", "verifier_engine", "critical_tokens_checked",
                    "critical_tokens_unconfirmed", "confidence_level"):
            if key not in verification:
                errors.append(f"{doc}/meta.json: verification.{key} is missing")
        if verification.get("confidence_level") != confidence:
            errors.append(
                f"{doc}: confidence_level differs between index.md "
                f"({confidence!r}) and meta.json ({verification.get('confidence_level')!r})"
            )
    return errors


def check_markers_traceable() -> list:
    """Каждый маркер неоднозначности обязан нести «имя PDF + страница»."""
    errors = []
    page_ref = re.compile(r"стр\.\s*\d")
    for doc in DOCS:
        for path in sorted((ROOT / doc).rglob("*.md")):
            rel = str(path.relative_to(ROOT))
            for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if not MARKER_RE.search(line):
                    continue
                if "Источник:" not in line or not page_ref.search(line):
                    errors.append(
                        f"{rel}:{number}: ambiguity marker without an exact "
                        "'Источник: <файл.pdf>, стр. N' reference"
                    )
                elif ".pdf" not in line:
                    errors.append(f"{rel}:{number}: ambiguity marker without a PDF file name")
    return errors


def check_no_pdfs_committed() -> list:
    """PDF не хранятся в репозитории; Git LFS не используется.

    Проверяется список файлов под контролем версий: исходные PDF лежат у
    пользователя локально и попадают под ``.gitignore``, поэтому наличие файла
    в рабочем каталоге нарушением не является — нарушением является коммит.
    """
    errors = []
    try:
        tracked = subprocess.run(
            ["git", "-C", str(ROOT), "ls-files", "-z", "*.pdf"],
            capture_output=True, text=True, check=True,
        ).stdout.split("\0")
    except (OSError, subprocess.CalledProcessError):
        tracked = [
            str(path.relative_to(ROOT))
            for path in ROOT.rglob("*.pdf")
            if ".git/" not in str(path)
        ]
    for rel in tracked:
        if not rel or rel.endswith(".fixture.pdf"):
            continue
        errors.append(f"{rel}: source PDF must not be stored in the repository (issue #310)")

    gitattributes = ROOT / ".gitattributes"
    if gitattributes.exists() and "lfs" in gitattributes.read_text(encoding="utf-8"):
        errors.append(".gitattributes: Git LFS is forbidden for PDFs (issue #310)")
    for workflow in sorted((ROOT / ".github" / "workflows").glob("*.yml")):
        if "lfs: true" in workflow.read_text(encoding="utf-8"):
            errors.append(
                f"{workflow.relative_to(ROOT)}: LFS checkout left over — Git LFS is not used"
            )
    gitignore = read_text(".gitignore")
    if "kb/sources/**/*.pdf" not in gitignore:
        errors.append(".gitignore: source PDFs must stay untracked (kb/sources/**/*.pdf)")
    return errors


def check_tooling_and_wiring() -> list:
    errors = []
    for path in (VERIFIER, NEGATIVE_TEST):
        if not (ROOT / path).exists():
            errors.append(f"{path}: file does not exist")
    if not errors:
        verifier = read_text(VERIFIER)
        for needle in ("ТРЕБУЕТСЯ ПРОВЕРКА", "ПРОБЕЛ ИЗВЛЕЧЕНИЯ", "PyMuPDF"):
            if needle not in verifier:
                errors.append(f"{VERIFIER}: missing {needle!r}")
    makefile = read_text("Makefile")
    if "validate_issue_310_kb_pdf_ingestion.py" not in makefile:
        errors.append("Makefile: kb-validate must run scripts/validate_issue_310_kb_pdf_ingestion.py")
    if "Issue #310" not in read_text("CHANGELOG.md"):
        errors.append("CHANGELOG.md: missing 'Issue #310' entry")
    return errors


def main() -> int:
    errors: list = []
    errors += check_stale_removed()
    errors += check_documents()
    errors += check_markers_traceable()
    errors += check_no_pdfs_committed()
    errors += check_tooling_and_wiring()

    if errors:
        print("issue-310 KB PDF ingestion validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("issue-310 KB PDF ingestion validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
