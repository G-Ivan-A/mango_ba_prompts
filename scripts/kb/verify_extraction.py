#!/usr/bin/env python3
"""Перекрёстная проверка извлечённой БЗ вторым движком (issue #310).

Зачем. Конвейер `scripts/kb/extract.py` строит разделы БЗ по одному движку
(pdfplumber). Для функциональных данных — имён параметров API, лимитов,
портов, URL, кодов ошибок — одного движка мало: искажение здесь тиражируется
в downstream-задачи. Этот скрипт независимо перечитывает те же PDF вторым
движком (PyMuPDF) и сверяет **критические токены** каждого раздела с текстом
тех страниц, из которых раздел собран.

Что считается критическим токеном (то, что нельзя «додумывать»):

- ``snake_case``-идентификаторы — имена полей и параметров API;
- URL и HTTP-пути;
- числовые литералы (лимиты, таймауты, порты, версии, коды ответов);
- латинские аббревиатуры и константы в верхнем регистре (SSO, IdP, JSON…);
- латинские термины и имена сущностей длиной от 4 символов (Keycloak, ADFS…).

Токен считается подтверждённым, если он найден в тексте тех же страниц по
версии второго движка (сравнение — по строкам без пробелов, чтобы разная
раскладка переносов и колонок не давала ложных срабатываний). Допуск ±1
страница компенсирует разные границы разбиения на разделы.

Что делает скрипт (никаких «догадок» — только пометки):

1. вписывает в раздел блок-маркер ``❓ ТРЕБУЕТСЯ ПРОВЕРКА`` с точной ссылкой
   «имя PDF + страницы» для неподтверждённых значений;
2. вписывает ``⚠️ ПРОБЕЛ ИЗВЛЕЧЕНИЯ`` для страниц без текстового слоя
   (скан/картинка) — раздел не выдумывается, пробел фиксируется явно;
3. пишет отчёт ``verification.md`` и блок ``verification`` в ``meta.json``;
4. проставляет во frontmatter ``index.md`` поля прослеживаемости
   (``source_document``, ``extraction_date``, ``model_used``,
   ``confidence_level``, ``pages_covered``).

Блоки-маркеры обёрнуты в ``<!-- kb-verify:start -->`` / ``<!-- kb-verify:end -->``
и при повторном прогоне заменяются целиком (идемпотентность).

Запуск::

    python3 scripts/kb/verify_extraction.py kb/processed/<slug> [...] \\
        --extraction-date 2026-08-22

Зависимости: PyMuPDF (см. scripts/kb/requirements.txt). Исходные PDF должны
быть на месте — проверка выполняется ДО их удаления из репозитория.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

MARKER_START = "<!-- kb-verify:start -->"
MARKER_END = "<!-- kb-verify:end -->"

# Порог: сколько неподтверждённых токенов на раздел показывать поимённо.
MAX_TOKENS_IN_MARKER = 40

# Критические токены — то, что запрещено «додумывать».
CRITICAL_PATTERNS = (
    ("url", re.compile(r"https?://[^\s`)\]<>\"']+")),
    ("param", re.compile(r"\b[A-Za-z][A-Za-z0-9]*(?:_[A-Za-z0-9]+)+\b")),
    ("const", re.compile(r"\b[A-Z]{3,}\b")),
    ("number", re.compile(r"\b\d[\d]*(?:[.,]\d+)+\b|\b\d{2,}\b")),
    ("term", re.compile(r"\b[A-Za-z][A-Za-z0-9]{3,}\b")),
)

# Слова-константы, которые встречаются в служебной обвязке самой БЗ, а не в
# исходном PDF: их отсутствие в PDF — не дефект извлечения.
BOILERPLATE = {
    "PDF", "ADR", "JSON", "YAML", "MD", "KB", "URL", "URI",
}


def normalize(text: str) -> str:
    """Строка без пробелов и в нижнем регистре — устойчиво к переносам."""
    return re.sub(r"\s+", "", text).lower()


def load_pymupdf_pages(pdf_path: Path) -> list[str]:
    import fitz  # PyMuPDF

    doc = fitz.open(str(pdf_path))
    try:
        return [page.get_text("text") for page in doc]
    finally:
        doc.close()


def strip_verify_blocks(text: str) -> str:
    pattern = re.compile(
        re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END) + r"\n*",
        re.DOTALL,
    )
    return pattern.sub("", text)


def split_frontmatter(text: str) -> tuple[list[str], str]:
    if not text.startswith("---\n"):
        return [], text
    end = text.find("\n---\n", 3)
    if end == -1:
        return [], text
    fm = text[4:end].splitlines()
    return fm, text[end + 5:]


def body_for_scan(body: str) -> str:
    """Тело раздела без служебной обвязки: трассировки, картинок, ссылок."""
    lines = []
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith(">") or stripped.startswith("<!--"):
            continue
        if stripped.startswith("!["):
            continue
        lines.append(line)
    return "\n".join(lines)


def critical_tokens(text: str) -> list[tuple[str, str]]:
    found: dict[str, str] = {}
    for kind, pattern in CRITICAL_PATTERNS:
        for match in pattern.findall(text):
            token = match.strip(".,;:)]} ")
            if len(token) < 3 or token in BOILERPLATE:
                continue
            found.setdefault(token, kind)
    return sorted(found.items())


def pages_from_refs(refs: list[dict]) -> list[tuple[str, int]]:
    """[(source_pdf, page_number_within_that_pdf), ...] для раздела."""
    pages: list[tuple[str, int]] = []
    for ref in refs:
        pdf = ref.get("source_pdf")
        spec = str(ref.get("pages") or "")
        if not pdf or not spec:
            continue
        for chunk in spec.split(","):
            chunk = chunk.strip()
            if not chunk:
                continue
            if "-" in chunk:
                start, _, end = chunk.partition("-")
                if start.isdigit() and end.isdigit():
                    pages.extend((pdf, n) for n in range(int(start), int(end) + 1))
            elif chunk.isdigit():
                pages.append((pdf, int(chunk)))
    return pages


def reference_text(
    pages: list[tuple[str, int]],
    page_texts: dict[str, list[str]],
    tolerance: int = 1,
) -> str:
    """Нормализованный текст тех же страниц по версии второго движка."""
    wanted: set[tuple[str, int]] = set()
    for pdf, page in pages:
        for shift in range(-tolerance, tolerance + 1):
            wanted.add((pdf, page + shift))
    parts = []
    for pdf, page in sorted(wanted):
        texts = page_texts.get(pdf)
        if not texts or page < 1 or page > len(texts):
            continue
        parts.append(texts[page - 1])
    return normalize("\n".join(parts))


def pages_label(pages: list[tuple[str, int]]) -> str:
    """«MangoOffice_VPBX_API_v1.9.pdf, стр. 8-12» — читаемая ссылка."""
    by_pdf: dict[str, list[int]] = {}
    for pdf, page in pages:
        by_pdf.setdefault(Path(pdf).name, []).append(page)
    parts = []
    for name, nums in by_pdf.items():
        nums = sorted(set(nums))
        span = f"{nums[0]}-{nums[-1]}" if len(nums) > 1 else str(nums[0])
        parts.append(f"`{name}`, стр. {span}")
    return "; ".join(parts)


def empty_pages(pages: list[tuple[str, int]], page_texts: dict[str, list[str]]) -> list[tuple[str, int]]:
    """Страницы, на которых второй движок вообще не видит текста."""
    gaps = []
    for pdf, page in sorted(set(pages)):
        texts = page_texts.get(pdf)
        if not texts or page < 1 or page > len(texts):
            continue
        if not normalize(texts[page - 1]):
            gaps.append((pdf, page))
    return gaps


def build_marker_block(unconfirmed: list[tuple[str, str]], gaps: list[tuple[str, int]],
                       pages: list[tuple[str, int]], engine: str) -> str:
    lines = [MARKER_START, ""]
    if gaps:
        for pdf, page in gaps:
            lines.append(
                f"> ⚠️ **ПРОБЕЛ ИЗВЛЕЧЕНИЯ**: на странице нет текстового слоя "
                f"(скан/изображение) — содержимое не извлечено и не додумано; "
                f"проверить в источнике вручную. (Источник: `{Path(pdf).name}`, стр. {page})"
            )
            lines.append("")
    if unconfirmed:
        shown = unconfirmed[:MAX_TOKENS_IN_MARKER]
        listed = ", ".join(f"`{token}`" for token, _ in shown)
        tail = "" if len(unconfirmed) == len(shown) else f" и ещё {len(unconfirmed) - len(shown)}"
        lines.append(
            f"> ❓ **ТРЕБУЕТСЯ ПРОВЕРКА**: значения {listed}{tail} не подтверждены "
            f"независимым движком извлечения ({engine}) на тех же страницах. "
            f"Значение НЕ достраивалось — сверьте с источником. "
            f"(Источник: {pages_label(pages)})"
        )
        lines.append("")
    lines.append(MARKER_END)
    return "\n".join(lines)


def confidence_for(total: int, unconfirmed: int, gap_pages: int) -> str:
    if gap_pages:
        return "requires_review"
    if total == 0:
        return "requires_review"
    ratio = unconfirmed / total
    if ratio <= 0.02:
        return "high"
    if ratio <= 0.10:
        return "medium"
    return "requires_review"


def upsert_frontmatter(fm: list[str], updates: dict[str, str]) -> list[str]:
    result = list(fm)
    for key, value in updates.items():
        line = f'{key}: "{value}"'
        for index, existing in enumerate(result):
            if re.match(rf"^{re.escape(key)}\s*:", existing):
                result[index] = line
                break
        else:
            result.append(line)
    return result


def verify_doc(doc_dir: Path, extraction_date: str) -> dict:
    meta_path = doc_dir / "meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    source_pdfs = meta.get("source_pdfs") or [meta.get("source_pdf")]

    page_texts: dict[str, list[str]] = {}
    engine = "PyMuPDF"
    missing_sources = []
    for rel in source_pdfs:
        if not rel:
            continue
        path = ROOT / rel
        if not path.exists():
            missing_sources.append(rel)
            continue
        page_texts[rel] = load_pymupdf_pages(path)
    if missing_sources:
        raise SystemExit(
            f"{doc_dir}: исходные PDF недоступны — проверка должна выполняться "
            f"до их удаления: {', '.join(missing_sources)}"
        )
    try:
        import fitz

        engine = f"PyMuPDF {fitz.VersionBind}"
    except Exception:  # pragma: no cover - движок уже использован выше
        pass

    section_reports = []
    total_tokens = 0
    total_unconfirmed = 0
    total_gap_pages = 0

    for section in meta.get("sections", []):
        section_path = doc_dir / section["file"]
        raw = section_path.read_text(encoding="utf-8")
        raw = strip_verify_blocks(raw)
        fm, body = split_frontmatter(raw)

        pages = pages_from_refs(section.get("source_refs") or [])
        reference = reference_text(pages, page_texts)
        tokens = critical_tokens(body_for_scan(body))
        unconfirmed = [
            (token, kind) for token, kind in tokens
            if normalize(token) not in reference
        ]
        gaps = empty_pages(pages, page_texts)

        total_tokens += len(tokens)
        total_unconfirmed += len(unconfirmed)
        total_gap_pages += len(gaps)

        text = raw
        if unconfirmed or gaps:
            block = build_marker_block(unconfirmed, gaps, pages, engine)
            text = raw.rstrip("\n") + "\n\n" + block + "\n"
        if text != section_path.read_text(encoding="utf-8"):
            section_path.write_text(text, encoding="utf-8")

        section_reports.append({
            "file": section["file"],
            "title": section.get("title", ""),
            "pages": section.get("pages", ""),
            "critical_tokens": len(tokens),
            "unconfirmed": [token for token, _ in unconfirmed],
            "gap_pages": [f"{Path(pdf).name}:{page}" for pdf, page in gaps],
        })

    confidence = confidence_for(total_tokens, total_unconfirmed, total_gap_pages)
    pages_covered = f"1-{meta.get('page_count')}" if meta.get("page_count") else "unknown"
    source_document = ", ".join(Path(p).name for p in source_pdfs if p)

    verification = {
        "method": "cross-engine (pdfplumber -> PyMuPDF re-read of the same pages)",
        "verifier_engine": engine,
        "extraction_date": extraction_date,
        "critical_tokens_checked": total_tokens,
        "critical_tokens_unconfirmed": total_unconfirmed,
        "confirmed_ratio": round(1 - (total_unconfirmed / total_tokens), 4) if total_tokens else 0.0,
        "pages_without_text_layer": total_gap_pages,
        "confidence_level": confidence,
        "sections": section_reports,
    }
    meta["verification"] = verification
    meta_path.write_text(
        json.dumps(meta, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    write_report(doc_dir, meta, verification, source_document, pages_covered)
    patch_index(doc_dir, source_document, extraction_date, engine, confidence, pages_covered)
    return verification


def write_report(doc_dir: Path, meta: dict, verification: dict,
                 source_document: str, pages_covered: str) -> None:
    doc_code = meta.get("doc_code", "")
    lines = [
        "---",
        "type: kb-verification-report",
        f'doc_code: {doc_code}',
        f'source_document: "{source_document}"',
        f'extraction_date: "{verification["extraction_date"]}"',
        f'model_used: "{meta.get("extracted_by", "")} + {verification["verifier_engine"]}"',
        f'confidence_level: "{verification["confidence_level"]}"',
        f'pages_covered: "{pages_covered}"',
        "status: verified",
        "ai-generated: true",
        "---",
        "",
        f"# Отчёт перекрёстной проверки — {meta.get('doc_title', doc_code)}",
        "",
        f"Метод: {verification['method']}. Основное извлечение — "
        f"`{meta.get('extracted_by', '')}`; независимая перепроверка — "
        f"`{verification['verifier_engine']}` по тем же страницам источника.",
        "",
        "Критический токен — то, что запрещено «додумывать»: имя параметра "
        "(`snake_case`), URL, числовой литерал (лимит/порт/таймаут/код ответа), "
        "латинская константа или термин. Токен считается подтверждённым, если второй движок "
        "видит его на тех же страницах (допуск ±1 страница).",
        "",
        "## Итог",
        "",
        "| Метрика | Значение |",
        "| --- | ---: |",
        f"| Проверено критических токенов | {verification['critical_tokens_checked']} |",
        f"| Не подтверждено вторым движком | {verification['critical_tokens_unconfirmed']} |",
        f"| Доля подтверждённых | {verification['confirmed_ratio'] * 100:.2f} % |",
        f"| Страниц без текстового слоя | {verification['pages_without_text_layer']} |",
        f"| Уровень доверия | **{verification['confidence_level']}** |",
        "",
        "## Разделы, требующие ручной сверки",
        "",
    ]
    flagged = [s for s in verification["sections"] if s["unconfirmed"] or s["gap_pages"]]
    if not flagged:
        lines.append("Расхождений нет: все критические токены подтверждены вторым движком.")
    else:
        lines.append("| Раздел | Стр. | Не подтверждено | Страницы без текста |")
        lines.append("| --- | --- | ---: | --- |")
        for section in flagged:
            gaps = ", ".join(section["gap_pages"]) or "—"
            lines.append(
                f"| [{section['title']}]({section['file']}) | {section['pages']} "
                f"| {len(section['unconfirmed'])} | {gaps} |"
            )
        lines += [
            "",
            f"Точные значения перечислены в самих разделах внутри блоков "
            f"`{MARKER_START}` … `{MARKER_END}` с указанием имени PDF и страницы: "
            "исходные PDF в репозитории не хранятся, сверка выполняется по "
            "локальной копии документа.",
        ]
    lines.append("")
    (doc_dir / "verification.md").write_text("\n".join(lines), encoding="utf-8")


def patch_index(doc_dir: Path, source_document: str, extraction_date: str,
                engine: str, confidence: str, pages_covered: str) -> None:
    index_path = doc_dir / "index.md"
    text = index_path.read_text(encoding="utf-8")
    fm, body = split_frontmatter(text)
    if not fm:
        return
    meta = json.loads((doc_dir / "meta.json").read_text(encoding="utf-8"))
    fm = upsert_frontmatter(fm, {
        "source_document": source_document,
        "extraction_date": extraction_date,
        "model_used": f"{meta.get('extracted_by', '')} + {engine}",
        "confidence_level": confidence,
        "pages_covered": pages_covered,
    })
    link = (
        "\n> Перекрёстная проверка критических данных: "
        "[`verification.md`](verification.md) — уровень доверия "
        f"**{confidence}**. Неоднозначности помечены в разделах маркерами "
        "`❓ ТРЕБУЕТСЯ ПРОВЕРКА` / `⚠️ ПРОБЕЛ ИЗВЛЕЧЕНИЯ` с точной ссылкой "
        "«PDF + страница».\n"
    )
    body = strip_verify_blocks(body)
    if "verification.md" not in body:
        parts = body.split("\n## ", 1)
        parts[0] = parts[0].rstrip("\n") + "\n" + link
        body = "\n## ".join(parts) if len(parts) > 1 else parts[0]
    index_path.write_text("---\n" + "\n".join(fm) + "\n---\n" + body, encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("doc_dirs", nargs="+", help="каталоги kb/processed/<slug>")
    parser.add_argument("--extraction-date", required=True, help="YYYY-MM-DD")
    args = parser.parse_args(argv)

    for raw in args.doc_dirs:
        doc_dir = Path(raw)
        if not doc_dir.is_absolute():
            doc_dir = ROOT / doc_dir
        report = verify_doc(doc_dir, args.extraction_date)
        print(
            f"{raw}: проверено {report['critical_tokens_checked']} токенов, "
            f"не подтверждено {report['critical_tokens_unconfirmed']}, "
            f"страниц без текста {report['pages_without_text_layer']}, "
            f"доверие {report['confidence_level']}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
