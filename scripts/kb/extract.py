#!/usr/bin/env python3
"""Извлечение PDF-источника в структурированную БЗ (issue #111).

Конвейер (детерминированный, без ML, дружелюбный к git и CI):

    PDF → текст с сохранением структуры разделов
        → деление на разделы по нумерованным заголовкам (ФТ-3)
        → таблицы → Markdown-таблицы
        → растровые изображения → файлы + ссылки
        → index.md (карта разделов для агента, замена retrieval-шага)
        → meta.json (метаданные + статистика токенов, воспроизводимость)

Инструменты (ФТ-2):
  • ``pdfplumber`` — текст, координаты, размер шрифта (детект заголовков),
    таблицы. Детерминирован, без GPU, ставится в CI одной строкой.
  • ``PyMuPDF`` (опционально) — байты встроенных растровых изображений.
  • ``scripts/kb/tokens.py`` — подсчёт токенов (tiktoken или эвристика).
Сравнение с marker/nougat/MinerU — в ``docs/kb-experiment-report.md`` (они дают
выше качество на сложной вёрстке/формулах, но требуют GPU и недетерминированы —
поэтому для git-конвейера выбран pdfplumber, а ML — опциональный fallback).

Деление на разделы (ФТ-3): по заголовкам **скриптом**, без LLM. Заголовок —
строка с кеглем больше основного текста ИЛИ короткая жирная строка с нумерацией
``N`` / ``N.M`` / ``N.M.K``. Уровень берётся из глубины нумерации. LLM нужен
только для документов БЕЗ структуры заголовков (скан, свободная вёрстка) —
гибридный режим описан в отчёте.

Запуск::

    python3 scripts/kb/extract.py <source.pdf> --out kb/processed/<slug> \\
        --doc-code CC --doc-title "Контакт-центр MANGO OFFICE" --doc-version 1.26.23

Вывод детерминирован (pdfplumber + tiktoken + фиксированный порядок).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import tokens as token_util  # noqa: E402  (локальный модуль scripts/kb/tokens.py)

# --- Транслитерация RU → латиница для ASCII-имён файлов/якорей --------------
# Имена разделов кириллические; пути держим ASCII (портируемость, URL, chunk-id).
_TRANSLIT = {
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "e",
    "ж": "zh", "з": "z", "и": "i", "й": "y", "к": "k", "л": "l", "м": "m",
    "н": "n", "о": "o", "п": "p", "р": "r", "с": "s", "т": "t", "у": "u",
    "ф": "f", "х": "h", "ц": "c", "ч": "ch", "ш": "sh", "щ": "sch", "ъ": "",
    "ы": "y", "ь": "", "э": "e", "ю": "yu", "я": "ya",
}


def transliterate(text: str) -> str:
    out = []
    for ch in text.lower():
        out.append(_TRANSLIT.get(ch, ch))
    return "".join(out)


def slugify(text: str, max_len: int = 40) -> str:
    slug = transliterate(text)
    slug = re.sub(r"[^a-z0-9]+", "-", slug).strip("-")
    return slug[:max_len].strip("-") or "section"


# --- Детект заголовков ------------------------------------------------------
_NUM_RE = re.compile(r"^(\d+(?:\.\d+)*)\.?\s+(.+)$")


def line_size(line: dict) -> float:
    sizes = [round(c.get("size", 0), 1) for c in line.get("chars", []) if c.get("size")]
    return max(sizes) if sizes else 0.0


def line_is_bold(line: dict) -> bool:
    return any("bold" in (c.get("fontname", "") or "").lower() for c in line.get("chars", []))


def body_font_size(pages) -> float:
    """Самый частый размер шрифта по документу = размер основного текста."""
    counter: dict[float, int] = {}
    for page in pages:
        for line in page.extract_text_lines(layout=False):
            for c in line.get("chars", []):
                size = round(c.get("size", 0), 1)
                if size:
                    counter[size] = counter.get(size, 0) + 1
    if not counter:
        return 10.0
    return max(counter.items(), key=lambda kv: kv[1])[0]


def classify_line(line: dict, body_size: float):
    """Возвращает (kind, number, level, title).

    kind ∈ {"heading", "subheading", "text"}.
    """
    text = (line.get("text") or "").strip()
    if not text:
        return ("text", None, 0, text)
    size = line_size(line)
    bold = line_is_bold(line)
    big = size >= body_size + 1.0
    match = _NUM_RE.match(text)
    numbered_heading = bool(match) and len(text) <= 90 and (big or bold)
    if not (big or numbered_heading):
        return ("text", None, 0, text)
    if match:
        number = match.group(1)
        title = match.group(2).strip()
        level = number.count(".") + 1
        return ("heading" if level == 1 else "subheading", number, level, title)
    # Заголовок без нумерации (напр., титульная страница) — выделим, но не делим.
    return ("text", None, 0, text)


# --- Рендер таблиц в Markdown ----------------------------------------------
def render_table(rows) -> str:
    def cell(value):
        value = "" if value is None else str(value)
        return value.replace("\n", "<br>").replace("|", "\\|").strip()

    clean = [[cell(c) for c in row] for row in rows if any(c is not None for c in row)]
    if not clean:
        return ""
    width = max(len(r) for r in clean)
    clean = [r + [""] * (width - len(r)) for r in clean]
    header = clean[0]
    out = ["| " + " | ".join(header) + " |", "| " + " | ".join(["---"] * width) + " |"]
    for row in clean[1:]:
        out.append("| " + " | ".join(row) + " |")
    return "\n".join(out)


# --- Извлечение изображений (PyMuPDF) --------------------------------------
def load_image_bytes(pdf_path: Path):
    """Возвращает {page_index: [ {bytes, ext}, ... ]} или {} если PyMuPDF нет."""
    try:
        import fitz  # PyMuPDF
    except Exception:
        return {}, None
    images: dict[int, list[dict]] = {}
    doc = fitz.open(str(pdf_path))
    version = f"pymupdf {fitz.VersionBind}"
    for page_index in range(len(doc)):
        page = doc[page_index]
        page_images = []
        for info in page.get_images(full=True):
            xref = info[0]
            try:
                extracted = doc.extract_image(xref)
            except Exception:
                continue
            page_images.append({"bytes": extracted["image"], "ext": extracted.get("ext", "png")})
        if page_images:
            images[page_index] = page_images
    doc.close()
    return images, version


# --- Сбор элементов страницы в порядке чтения ------------------------------
def page_elements(page, body_size, page_images):
    """Элементы страницы, отсортированные по вертикали (reading order)."""
    elements = []
    tables = page.find_tables()
    table_bboxes = [t.bbox for t in tables]

    def in_table(top, bottom):
        mid = (top + bottom) / 2
        for x0, t0, x1, t1 in table_bboxes:
            if t0 <= mid <= t1:
                return True
        return False

    for line in page.extract_text_lines(layout=False):
        if in_table(line["top"], line["bottom"]):
            continue  # текст внутри таблицы рендерим только как таблицу
        kind, number, level, title = classify_line(line, body_size)
        elements.append(
            {"type": kind, "top": line["top"], "number": number, "level": level, "text": title}
        )

    for table in tables:
        elements.append({"type": "table", "top": table.bbox[1], "data": table.extract()})

    # Изображения: позиция из pdfplumber (та же система координат), байты из PyMuPDF.
    pdfplumber_imgs = sorted(page.images, key=lambda im: im["top"])
    byte_list = page_images or []
    for idx, img in enumerate(pdfplumber_imgs):
        payload = byte_list[idx] if idx < len(byte_list) else None
        elements.append({"type": "image", "top": img["top"], "payload": payload})
    # Если PyMuPDF дал больше картинок, чем нашёл pdfplumber — добьём в конец.
    for idx in range(len(pdfplumber_imgs), len(byte_list)):
        elements.append({"type": "image", "top": 10 ** 6 + idx, "payload": byte_list[idx]})

    elements.sort(key=lambda e: e["top"])
    return elements


def normalize_heading(text: str) -> str:
    """Нормализация заголовков для сопоставления с PDF outline."""
    text = text.replace("\u00a0", " ").replace("ё", "е").replace("Ё", "Е")
    text = re.sub(r"\s+", " ", text).strip()
    return text.rstrip(".")


def parse_numbered_title(text: str):
    match = _NUM_RE.match(text.strip())
    if not match:
        return None, text.strip()
    return match.group(1), match.group(2).strip()


def load_pdf_outline(pdf_path: Path) -> tuple[list[dict], str | None]:
    """Возвращает outline/bookmarks PDF, если он есть.

    Для больших руководств встроенное оглавление надежнее эвристики по жирным
    нумерованным строкам: списки внутри раздела не становятся отдельными чанками.
    """
    try:
        import fitz  # PyMuPDF
    except Exception:
        return [], None

    doc = fitz.open(str(pdf_path))
    try:
        toc = doc.get_toc(simple=True)
        version = f"pymupdf {fitz.VersionBind}"
    finally:
        doc.close()

    entries = []
    for level, raw_title, page_no in toc:
        if page_no < 1:
            continue
        number, title = parse_numbered_title(raw_title)
        entries.append({
            "level": level,
            "raw_title": raw_title.strip(),
            "number": number,
            "title": title,
            "page": page_no,
        })
    return entries, version


def heading_matches(line_text: str, outline_title: str) -> bool:
    line = normalize_heading(line_text)
    wanted = normalize_heading(outline_title)
    if line == wanted:
        return True
    # Длинные заголовки иногда переносятся: первая строка должна совпадать
    # с началом outline-заголовка, но короткие случайные совпадения отбрасываем.
    return len(line) >= 12 and wanted.startswith(line + " ")


def resolve_outline_positions(pdf, outline_entries: list[dict]) -> list[dict]:
    """Находит вертикальную позицию каждого outline-заголовка на странице."""
    lines_by_page: dict[int, list[dict]] = {}
    last_top_by_page: dict[int, float] = {}
    resolved = []

    for entry in outline_entries:
        page_index = entry["page"] - 1
        if page_index < 0 or page_index >= len(pdf.pages):
            continue
        if page_index not in lines_by_page:
            lines_by_page[page_index] = pdf.pages[page_index].extract_text_lines(layout=False)

        last_top = last_top_by_page.get(page_index, -1.0)
        candidates = [
            line["top"]
            for line in lines_by_page[page_index]
            if heading_matches(line.get("text") or "", entry["raw_title"])
        ]
        top = None
        for candidate in sorted(candidates):
            if candidate > last_top + 0.5:
                top = candidate
                break
        if top is None and candidates:
            top = sorted(candidates)[0]
        if top is None:
            # Fail-open: если координату не нашли, все равно используем outline
            # как границу страницы. Малый сдвиг сохраняет порядок на одной странице.
            top = max(last_top + 0.01, 0.0)

        marker = dict(entry)
        marker["page_index"] = page_index
        marker["top"] = top
        resolved.append(marker)
        last_top_by_page[page_index] = top

    return resolved


def page_number_footer(line: dict, page) -> bool:
    text = (line.get("text") or "").strip()
    return (
        text == str(getattr(page, "page_number", ""))
        and line.get("top", 0) > getattr(page, "height", 0) - 80
    )


def page_elements_plain(page, page_images):
    """Элементы страницы без детекта заголовков; границы берет PDF outline."""
    elements = []
    tables = page.find_tables()
    table_bboxes = [t.bbox for t in tables]

    def in_table(top, bottom):
        mid = (top + bottom) / 2
        for x0, t0, x1, t1 in table_bboxes:
            if t0 <= mid <= t1:
                return True
        return False

    for line in page.extract_text_lines(layout=False):
        if page_number_footer(line, page) or in_table(line["top"], line["bottom"]):
            continue
        text = (line.get("text") or "").strip()
        if text:
            elements.append({"type": "text", "top": line["top"], "text": text})

    for table in tables:
        elements.append({"type": "table", "top": table.bbox[1], "data": table.extract()})

    pdfplumber_imgs = sorted(page.images, key=lambda im: im["top"])
    byte_list = page_images or []
    for idx, img in enumerate(pdfplumber_imgs):
        payload = byte_list[idx] if idx < len(byte_list) else None
        elements.append({"type": "image", "top": img["top"], "payload": payload})
    for idx in range(len(pdfplumber_imgs), len(byte_list)):
        elements.append({"type": "image", "top": 10 ** 6 + idx, "payload": byte_list[idx]})

    elements.sort(key=lambda e: e["top"])
    return elements


def append_plain_element(section: dict, el: dict, page_no: int):
    section["end_page"] = page_no
    if el["type"] == "text":
        if el["text"].strip():
            section["blocks"].append(("text", el["text"].strip()))
    elif el["type"] == "table":
        md = render_table(el["data"])
        if md:
            section["blocks"].append(("table", md))
            section["n_tables"] += 1
    elif el["type"] == "image":
        section["blocks"].append(("image", el.get("payload"), page_no))
        section["n_images"] += 1


def build_sections_from_outline(pdf, outline_entries, image_map):
    markers = resolve_outline_positions(pdf, outline_entries)
    if not markers:
        return []

    sections = []

    def new_section(marker):
        return {
            "number": marker.get("number"),
            "title": marker["title"],
            "level": marker.get("level", 1),
            "blocks": [],
            "start_page": marker["page"],
            "end_page": marker["page"],
            "subheadings": [],
            "n_tables": 0,
            "n_images": 0,
        }

    def collect(section, start_page_index, start_top, end_marker):
        end_page_index = end_marker["page_index"] if end_marker else len(pdf.pages) - 1
        for page_index in range(start_page_index, end_page_index + 1):
            page = pdf.pages[page_index]
            lower = start_top if page_index == start_page_index else -1.0
            upper = (
                end_marker["top"]
                if end_marker and page_index == end_marker["page_index"]
                else float("inf")
            )
            for el in page_elements_plain(page, image_map.get(page_index)):
                top = el["top"]
                if page_index == start_page_index and top <= lower + 0.5:
                    continue
                if page_index == end_page_index and top >= upper - 0.5:
                    continue
                append_plain_element(section, el, page_index + 1)

    # Титульные страницы и оглавление до первого outline-раздела сохраняем.
    first = markers[0]
    if first["page_index"] > 0 or first["top"] > 0:
        front = {
            "number": None,
            "title": "Титульная часть",
            "level": 1,
            "blocks": [],
            "start_page": 1,
            "end_page": 1,
            "subheadings": [],
            "n_tables": 0,
            "n_images": 0,
        }
        collect(front, 0, -1.0, first)
        if front["blocks"]:
            sections.append(front)

    for idx, marker in enumerate(markers):
        section = new_section(marker)
        next_marker = markers[idx + 1] if idx + 1 < len(markers) else None
        collect(section, marker["page_index"], marker["top"], next_marker)
        sections.append(section)

    return sections


# --- Сборка разделов --------------------------------------------------------
def build_sections(pdf, pdf_path):
    body_size = body_font_size(pdf.pages)
    image_map, image_tool = load_image_bytes(Path(pdf_path))
    outline, outline_tool = load_pdf_outline(Path(pdf_path))
    if outline:
        sections = build_sections_from_outline(pdf, outline, image_map)
        if sections:
            return sections, body_size, image_tool, f"pdf-outline ({outline_tool})"

    sections = []
    front = {"number": None, "title": "Титульная часть", "level": 1, "blocks": [],
             "start_page": 1, "end_page": 1, "subheadings": [], "n_tables": 0, "n_images": 0}
    current = front

    for page_index, page in enumerate(pdf.pages):
        page_no = page_index + 1
        for el in page_elements(page, body_size, image_map.get(page_index)):
            if el["type"] == "heading":  # новый раздел верхнего уровня
                if current is front and (front["blocks"] or front["subheadings"]):
                    sections.append(front)
                elif current is not front:
                    sections.append(current)
                current = {
                    "number": el["number"], "title": el["text"], "level": 1,
                    "blocks": [], "start_page": page_no, "end_page": page_no,
                    "subheadings": [], "n_tables": 0, "n_images": 0,
                }
                continue
            current["end_page"] = page_no
            if el["type"] == "subheading":
                current["subheadings"].append((el["number"], el["text"]))
                current["blocks"].append(("subheading", el["number"], el["text"]))
            elif el["type"] == "text":
                if el["text"].strip():
                    current["blocks"].append(("text", el["text"].strip()))
            elif el["type"] == "table":
                md = render_table(el["data"])
                if md:
                    current["blocks"].append(("table", md))
                    current["n_tables"] += 1
            elif el["type"] == "image":
                current["blocks"].append(("image", el.get("payload"), page_no))
                current["n_images"] += 1

    if current is front:
        if front["blocks"] or front["subheadings"]:
            sections.append(front)
    else:
        sections.append(current)
    return sections, body_size, image_tool, "layout-heuristic"


# --- Рендер раздела в Markdown ---------------------------------------------
def render_section_markdown(section, meta, image_paths):
    fm_title = f'{section["number"]}. {section["title"]}' if section["number"] else section["title"]
    pages = (
        f'{section["start_page"]}-{section["end_page"]}'
        if section["start_page"] != section["end_page"]
        else f'{section["start_page"]}'
    )
    lines = ["# " + fm_title, ""]
    image_idx = 0
    paragraph = []

    def flush_paragraph():
        nonlocal paragraph
        if paragraph:
            lines.append(" ".join(paragraph).strip())
            lines.append("")
            paragraph = []

    for block in section["blocks"]:
        if block[0] == "subheading":
            flush_paragraph()
            lines.append(f"## {block[1]} {block[2]}")
            lines.append("")
        elif block[0] == "text":
            paragraph.append(block[1])
        elif block[0] == "table":
            flush_paragraph()
            lines.append(block[1])
            lines.append("")
        elif block[0] == "image":
            flush_paragraph()
            rel = image_paths[image_idx] if image_idx < len(image_paths) else None
            page_no = block[2]
            if rel:
                lines.append(f"![Изображение, стр. {page_no}](../{rel})")
            else:
                lines.append(f"<!-- изображение на стр. {page_no}: байты не извлечены (PyMuPDF недоступен) -->")
            lines.append("")
            image_idx += 1
    flush_paragraph()

    body = "\n".join(lines).rstrip() + "\n"
    tok = token_util.count_tokens(body)
    section["_tokens"] = tok
    section["_pages"] = pages

    frontmatter = [
        "---",
        f'id: {section["_id"]}',
        f'doc_code: {meta["doc_code"]}',
        f'doc_title: "{meta["doc_title"]}"',
        f'doc_version: "{meta["doc_version"]}"',
        f'section: "{section["number"] or "0"}"',
        f'title: "{section["title"]}"',
        f"pages: \"{pages}\"",
        f'source: {meta["source_rel"]}',
        f'extracted_by: "{meta["extracted_by"]}"',
        f'token_method: "{meta["token_method"]}"',
        f"tokens: {tok}",
        "status: extracted",
        "ai-generated: true",
        "---",
        "",
    ]
    return "\n".join(frontmatter) + body


def section_summary(section) -> str:
    """Короткое «когда обращаться» для индекса — из подзаголовков/первой фразы."""
    if section["subheadings"]:
        titles = [t for _, t in section["subheadings"]]
        return "; ".join(titles[:4])
    for block in section["blocks"]:
        if block[0] == "text":
            sentence = re.split(r"(?<=[.!?])\s", block[1])[0]
            return sentence[:120]
    return "—"


# --- main -------------------------------------------------------------------
def main(argv=None):
    parser = argparse.ArgumentParser(description="Извлечь PDF в структуру БЗ (issue #111).")
    parser.add_argument("pdf", help="путь к исходному PDF")
    parser.add_argument("--out", required=True, help="каталог результата, напр. kb/processed/<slug>")
    parser.add_argument("--doc-code", default="DOC", help="короткий код документа для цитат, напр. CC")
    parser.add_argument("--doc-title", default="", help="название документа (иначе из титула)")
    parser.add_argument("--doc-version", default="", help="версия документа")
    parser.add_argument("--note", default="", help="примечание в meta.json")
    args = parser.parse_args(argv)

    import pdfplumber

    pdf_path = Path(args.pdf).resolve()
    if not pdf_path.exists():
        parser.error(f"PDF не найден: {pdf_path}")
    out_dir = Path(args.out).resolve()
    sections_dir = out_dir / "sections"
    images_dir = out_dir / "images"
    for d in (sections_dir, images_dir):
        d.mkdir(parents=True, exist_ok=True)
    # Чистим прошлый прогон (детерминированный полный ререндер).
    for old in list(sections_dir.glob("*.md")) + list(images_dir.glob("*")):
        old.unlink()

    source_sha = hashlib.sha256(pdf_path.read_bytes()).hexdigest()
    try:
        source_rel = str(pdf_path.relative_to(ROOT))
    except ValueError:
        source_rel = pdf_path.name

    pdf = pdfplumber.open(str(pdf_path))
    pdf_version = getattr(__import__("pdfplumber"), "__version__", "?")
    sections, body_size, image_tool, section_source = build_sections(pdf, pdf_path)

    doc_slug = slugify(out_dir.name)
    doc_title = args.doc_title or (sections[0]["title"] if sections else out_dir.name)
    doc_version = args.doc_version or "unknown"

    meta = {
        "doc_code": args.doc_code,
        "doc_title": doc_title,
        "doc_version": doc_version,
        "source_rel": source_rel,
        "extracted_by": f"pdfplumber {pdf_version}",
        "token_method": token_util.method(),
    }

    # Присваиваем стабильные id и сохраняем секции/изображения.
    index_rows = []
    tokens_total = 0
    image_total = 0
    table_total = 0
    for order, section in enumerate(sections):
        num = section["number"] or "00"
        slug = slugify(section["title"])
        prefix = f"{order:02d}"
        section["_id"] = f"{doc_slug}-{prefix}-{slug}"
        file_name = f"{prefix}-{slug}.md"

        # Сохранить изображения раздела.
        image_paths = []
        img_n = 0
        for block in section["blocks"]:
            if block[0] == "image" and block[1] is not None:
                img_n += 1
                ext = block[1].get("ext", "png")
                img_name = f"{prefix}-{slug}-{img_n}.{ext}"
                (images_dir / img_name).write_bytes(block[1]["bytes"])
                image_paths.append(f"images/{img_name}")
        image_total += img_n

        md = render_section_markdown(section, meta, image_paths)
        (sections_dir / file_name).write_text(md, encoding="utf-8")
        tokens_total += section["_tokens"]
        table_total += section["n_tables"]

        index_rows.append({
            "order": prefix,
            "number": section["number"] or "—",
            "title": section["title"],
            "file": f"sections/{file_name}",
            "pages": section["_pages"],
            "tokens": section["_tokens"],
            "summary": section_summary(section),
        })

    # index.md — карта разделов (замена retrieval-шага, ADR-007 R2).
    index_md = build_index(meta, index_rows, tokens_total)
    index_tokens = token_util.count_tokens(index_md)
    (out_dir / "index.md").write_text(index_md, encoding="utf-8")

    meta_json = {
        "doc_code": meta["doc_code"],
        "doc_title": meta["doc_title"],
        "doc_version": meta["doc_version"],
        "source_pdf": source_rel,
        "source_sha256": source_sha,
        "extracted_by": meta["extracted_by"],
        "image_extractor": image_tool or "none",
        "section_source": section_source,
        "token_method": meta["token_method"],
        "page_count": len(pdf.pages),
        "section_count": len(sections),
        "image_count": image_total,
        "table_count": table_total,
        "body_font_size": body_size,
        "tokens_total": tokens_total,
        "tokens_index": index_tokens,
        "sections": [
            {
                "order": r["order"], "number": r["number"], "title": r["title"],
                "file": r["file"], "pages": r["pages"], "tokens": r["tokens"],
            }
            for r in index_rows
        ],
        "note": args.note,
    }
    (out_dir / "meta.json").write_text(
        json.dumps(meta_json, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    pdf.close()

    print(f"OK: {len(sections)} разделов, {image_total} изобр., {table_total} табл., "
          f"{tokens_total} токенов → {out_dir.relative_to(ROOT) if str(out_dir).startswith(str(ROOT)) else out_dir}")
    return 0


def build_index(meta, rows, tokens_total) -> str:
    lines = [
        "---",
        "type: kb-source-index",
        f'doc_code: {meta["doc_code"]}',
        f'doc_title: "{meta["doc_title"]}"',
        f'doc_version: "{meta["doc_version"]}"',
        "status: extracted",
        "ai-generated: true",
        "---",
        "",
        f'# {meta["doc_title"]} — индекс БЗ (карта разделов)',
        "",
        f'> Источник: `{meta["source_rel"]}` · извлечено: {meta["extracted_by"]} ·',
        f'> токены: {meta["token_method"]}. Это **карта поиска** для агента (замена',
        "> retrieval-шага до RAG, ADR-007 R2): найди раздел по колонке «Когда",
        "> обращаться», открой только его файл, процитируй стабильным адресом.",
        "",
        "## Как цитировать",
        "",
        f'`[{meta["doc_code"]}, §<номер>, с.<страница>]` — формат проекта (issue #109);',
        "плюс адрес чанка `kb/processed/<doc>/sections/<file>#<якорь>` (ADR-007 R3).",
        "",
        "## Разделы",
        "",
        "| № | Раздел | Файл | Стр. | Токены | Когда обращаться |",
        "| --- | --- | --- | --- | ---: | --- |",
    ]
    for r in rows:
        lines.append(
            f'| {r["number"]} | {r["title"]} | [{r["file"]}]({r["file"]}) | '
            f'{r["pages"]} | {r["tokens"]} | {r["summary"]} |'
        )
    lines.append(f"| | **ИТОГО** | | | **{tokens_total}** | весь документ |")
    lines.append("")
    lines.append("## Источники")
    lines.append("")
    lines.append(f'- Источник БЗ: `{meta["source_rel"]}`')
    lines.append("- Стандарт цитирования: [`standards/kb-standard.md`](../../../standards/kb-standard.md), "
                 "[ADR-007](../../../docs/adr/007-kb-standard.md)")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    raise SystemExit(main())
