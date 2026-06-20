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

    python3 scripts/kb/extract.py <source.pdf> --out kb/mango-product-docs/processed/<slug> \\
        --doc-code CC --doc-title "Контакт-центр MANGO OFFICE" --doc-version 1.26.23

Вывод детерминирован (pdfplumber + tiktoken + фиксированный порядок).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
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


def rel_link(target: Path, base_dir: Path) -> str:
    return Path(os.path.relpath(target, base_dir)).as_posix()


# --- Детект заголовков ------------------------------------------------------
_NUM_RE = re.compile(r"^(\d+(?:\.\d+)*)\.?\s+(.+)$")
_SECTION_RE = re.compile(r"^Раздел\s+(\d+(?:\.\d+)*)\.?\s+(.+)$", re.IGNORECASE)


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
    text = text.strip()
    match = _SECTION_RE.match(text)
    if match:
        return match.group(1), match.group(2).strip()
    match = _NUM_RE.match(text)
    if not match:
        return None, text
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
    stack: dict[int, dict] = {}
    for level, raw_title, page_no in toc:
        raw_title = raw_title.strip()
        number, title = parse_numbered_title(raw_title)
        for existing_level in list(stack):
            if existing_level >= level:
                del stack[existing_level]
        parent_number = None
        for parent_level in range(level - 1, 0, -1):
            parent_number = stack.get(parent_level, {}).get("trace_number")
            if parent_number:
                break
        trace_number = number or parent_number
        stack[level] = {"number": number, "title": title, "trace_number": trace_number}
        if page_no < 1:
            continue
        entries.append({
            "level": level,
            "raw_title": raw_title,
            "number": number,
            "trace_number": trace_number,
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
        text.isdigit()
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
            "trace_number": marker.get("trace_number") or marker.get("number"),
            "title": marker["title"],
            "pdf_heading": marker.get("raw_title") or marker["title"],
            "level": marker.get("level", 1),
            "blocks": [],
            "start_page": marker["page"],
            "end_page": marker["page"],
            "subheadings": [],
            "source_refs": [],
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
            "trace_number": None,
            "title": "Титульная часть",
            "pdf_heading": "Титульная часть",
            "level": 1,
            "blocks": [],
            "start_page": 1,
            "end_page": 1,
            "subheadings": [],
            "source_refs": [],
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
    front = {
        "number": None, "trace_number": None, "title": "Титульная часть",
        "pdf_heading": "Титульная часть", "level": 1, "blocks": [],
        "start_page": 1, "end_page": 1, "subheadings": [], "source_refs": [],
        "n_tables": 0, "n_images": 0,
    }
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
                    "number": el["number"], "trace_number": el["number"],
                    "title": el["text"], "pdf_heading": f'{el["number"]} {el["text"]}',
                    "level": 1,
                    "blocks": [], "start_page": page_no, "end_page": page_no,
                    "subheadings": [], "source_refs": [], "n_tables": 0, "n_images": 0,
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


def format_pages(start: int, end: int) -> str:
    return f"{start}-{end}" if start != end else f"{start}"


def rel_to_root(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return path.name


def yaml_string(value) -> str:
    return json.dumps(str(value), ensure_ascii=False)


def source_refs_json(section: dict) -> str:
    return json.dumps(section.get("source_refs", []), ensure_ascii=False, separators=(",", ":"))


def trace_number(section: dict) -> str:
    return section.get("trace_number") or section.get("number") or "—"


def source_parts(section: dict) -> str:
    parts = [str(ref["part"]) for ref in section.get("source_refs", [])]
    return ",".join(dict.fromkeys(parts)) or "1"


def source_pages(section: dict) -> str:
    refs = section.get("source_refs", [])
    if not refs:
        return section.get("_pages", "")
    return "; ".join(f'ч.{ref["part"]}: {ref["pages"]}' for ref in refs)


def source_refs_summary(section: dict, include_file: bool = False) -> str:
    refs = section.get("source_refs", [])
    if not refs:
        return "—"
    parts = []
    for ref in refs:
        if include_file:
            file_label = f' `{ref["source_pdf"]}`'
        else:
            file_label = ""
        parts.append(f'ч.{ref["part"]}{file_label} с.{ref["pages"]}')
    return "; ".join(parts)


def merge_continuation_section(target: dict, continuation: dict) -> None:
    target["blocks"].extend(continuation.get("blocks", []))
    target["end_page"] = max(target["end_page"], continuation["end_page"])
    target["subheadings"].extend(continuation.get("subheadings", []))
    target["source_refs"].extend(continuation.get("source_refs", []))
    target["n_tables"] += continuation.get("n_tables", 0)
    target["n_images"] += continuation.get("n_images", 0)


def annotate_source_trace(sections: list[dict], source: dict, page_offset: int) -> None:
    for section in sections:
        local_start = section["start_page"]
        local_end = section["end_page"]
        global_start = page_offset + local_start
        global_end = page_offset + local_end
        adjusted_blocks = []
        for block in section["blocks"]:
            if block[0] == "image":
                adjusted_blocks.append(("image", block[1], page_offset + block[2]))
            else:
                adjusted_blocks.append(block)
        section["blocks"] = adjusted_blocks
        section["start_page"] = global_start
        section["end_page"] = global_end
        section["source_refs"] = [{
            "source_pdf": source["source_pdf"],
            "part": source["order"],
            "pages": format_pages(local_start, local_end),
            "global_pages": format_pages(global_start, global_end),
        }]


# --- Рендер раздела в Markdown ---------------------------------------------
def render_section_markdown(section, meta, image_paths):
    fm_title = f'{section["number"]}. {section["title"]}' if section["number"] else section["title"]
    pages = format_pages(section["start_page"], section["end_page"])
    lines = ["# " + fm_title, ""]
    lines.append(
        f'> Трассировка: PDF §{trace_number(section)} · сквозные стр. {pages} · '
        f'источники: {source_refs_summary(section, include_file=True)}.'
    )
    lines.append("")
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
    refs_json = source_refs_json(section)
    primary_source = section["source_refs"][0]["source_pdf"] if section.get("source_refs") else meta["source_rel"]

    frontmatter = [
        "---",
        f'id: {section["_id"]}',
        f'doc_code: {meta["doc_code"]}',
        f'doc_title: {yaml_string(meta["doc_title"])}',
        f'doc_version: {yaml_string(meta["doc_version"])}',
        f'section: {yaml_string(section["number"] or "0")}',
        f'pdf_section: {yaml_string(trace_number(section))}',
        f'title: {yaml_string(section["title"])}',
        f'pdf_heading: {yaml_string(section.get("pdf_heading") or fm_title)}',
        f'pages: {yaml_string(pages)}',
        f'source: {primary_source}',
        f'source_part: {yaml_string(source_parts(section))}',
        f'source_pages: {yaml_string(source_pages(section))}',
        f"source_refs: '{refs_json}'",
        f'extracted_by: {yaml_string(meta["extracted_by"])}',
        f'token_method: {yaml_string(meta["token_method"])}',
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
    parser = argparse.ArgumentParser(description="Извлечь PDF в структуру БЗ (issue #111/#117).")
    parser.add_argument("pdf", nargs="+", help="один PDF или несколько частей одного документа")
    parser.add_argument("--out", required=True, help="каталог результата, напр. kb/mango-product-docs/processed/<slug>")
    parser.add_argument("--doc-code", default="DOC", help="короткий код документа для цитат, напр. CC")
    parser.add_argument("--doc-title", default="", help="название документа (иначе из титула)")
    parser.add_argument("--doc-version", default="", help="версия документа")
    parser.add_argument("--note", default="", help="примечание в meta.json")
    parser.add_argument("--source-mode", default="", help="single / multi_part / multi_document child mode")
    parser.add_argument("--source-set", default="", help="slug исходного набора документов")
    parser.add_argument("--source-document", default="", help="slug документа внутри исходного набора")
    args = parser.parse_args(argv)

    import pdfplumber

    pdf_paths = [Path(p).resolve() for p in args.pdf]
    for pdf_path in pdf_paths:
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

    pdf_version = getattr(__import__("pdfplumber"), "__version__", "?")
    sections = []
    source_infos = []
    body_sizes = []
    image_tools = []
    section_sources = []
    page_offset = 0
    combined_sha = hashlib.sha256()

    for order, pdf_path in enumerate(pdf_paths, start=1):
        source_bytes = pdf_path.read_bytes()
        source_sha = hashlib.sha256(source_bytes).hexdigest()
        combined_sha.update(source_sha.encode("ascii"))
        source_rel = rel_to_root(pdf_path)

        pdf = pdfplumber.open(str(pdf_path))
        try:
            part_sections, body_size, image_tool, section_source = build_sections(pdf, pdf_path)
            source_info = {
                "order": order,
                "source_pdf": source_rel,
                "source_sha256": source_sha,
                "page_count": len(pdf.pages),
            }
            annotate_source_trace(part_sections, source_info, page_offset)
            if (
                order > 1
                and sections
                and part_sections
                and part_sections[0]["number"] is None
                and part_sections[0]["title"] == "Титульная часть"
            ):
                merge_continuation_section(sections[-1], part_sections.pop(0))
            sections.extend(part_sections)
            source_infos.append(source_info)
            body_sizes.append(body_size)
            image_tools.append(image_tool or "none")
            section_sources.append(section_source)
            page_offset += len(pdf.pages)
        finally:
            pdf.close()

    doc_slug = slugify(out_dir.name)
    doc_title = args.doc_title or (sections[0]["title"] if sections else out_dir.name)
    doc_version = args.doc_version or "unknown"
    source_rels = [source["source_pdf"] for source in source_infos]
    source_rel = source_rels[0] if len(source_rels) == 1 else "; ".join(source_rels)

    meta = {
        "doc_code": args.doc_code,
        "doc_title": doc_title,
        "doc_version": doc_version,
        "source_rel": source_rel,
        "extracted_by": f"pdfplumber {pdf_version}",
        "token_method": token_util.method(),
        "kb_standard_link": rel_link(ROOT / "standards" / "kb-standard.md", out_dir),
        "kb_adr_link": rel_link(ROOT / "docs" / "adr" / "007-kb-standard.md", out_dir),
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
            "number": trace_number(section),
            "title": section["title"],
            "file": f"sections/{file_name}",
            "pages": section["_pages"],
            "pdf_section": trace_number(section),
            "pdf_heading": section.get("pdf_heading") or section["title"],
            "source_refs": section.get("source_refs", []),
            "source_summary": source_refs_summary(section),
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
        "processing_mode": args.source_mode or ("multi_part" if len(source_infos) > 1 else "single"),
        "source_set": args.source_set,
        "source_document": args.source_document,
        "source_pdf": source_rels[0] if len(source_rels) == 1 else "multi-part",
        "source_pdfs": source_rels,
        "sources": source_infos,
        "part_count": len(source_infos),
        "source_sha256": source_infos[0]["source_sha256"] if len(source_infos) == 1 else combined_sha.hexdigest(),
        "extracted_by": meta["extracted_by"],
        "image_extractor": image_tools[0] if len(set(image_tools)) == 1 else "mixed",
        "image_extractors": image_tools,
        "section_source": (
            section_sources[0]
            if len(set(section_sources)) == 1 and len(source_infos) == 1
            else f"pdf-outline multi-part ({len(source_infos)} PDF parts)"
            if section_sources and all(s.startswith("pdf-outline") for s in section_sources)
            else "; ".join(section_sources)
        ),
        "section_sources": section_sources,
        "token_method": meta["token_method"],
        "page_count": page_offset,
        "section_count": len(sections),
        "image_count": image_total,
        "table_count": table_total,
        "body_font_size": body_sizes[0] if body_sizes else 0,
        "body_font_sizes": body_sizes,
        "tokens_total": tokens_total,
        "tokens_index": index_tokens,
        "sections": [
            {
                "order": r["order"], "number": r["number"], "title": r["title"],
                "file": r["file"], "pages": r["pages"], "pdf_section": r["pdf_section"],
                "pdf_heading": r["pdf_heading"], "source_refs": r["source_refs"],
                "tokens": r["tokens"],
            }
            for r in index_rows
        ],
        "note": args.note,
    }
    (out_dir / "meta.json").write_text(
        json.dumps(meta_json, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
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
        "плюс адрес чанка `kb/mango-product-docs/processed/<doc>/sections/<file>#<якорь>` (ADR-007 R3).",
        "",
        "## Разделы",
        "",
        "| № PDF | Раздел | Файл | Стр. | Источник | Токены | Когда обращаться |",
        "| --- | --- | --- | --- | --- | ---: | --- |",
    ]
    for r in rows:
        lines.append(
            f'| {r["number"]} | {r["title"]} | [{r["file"]}]({r["file"]}) | '
            f'{r["pages"]} | {r["source_summary"]} | {r["tokens"]} | {r["summary"]} |'
        )
    lines.append(f"| | **ИТОГО** | | | | **{tokens_total}** | весь документ |")
    lines.append("")
    lines.append("## Источники")
    lines.append("")
    for idx, source in enumerate(str(meta["source_rel"]).split("; "), start=1):
        lines.append(f"- Источник БЗ, часть {idx}: `{source}`")
    lines.append(
        "- Стандарт цитирования: "
        f'[`standards/kb-standard.md`]({meta["kb_standard_link"]}), '
        f'[ADR-007]({meta["kb_adr_link"]})'
    )
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    raise SystemExit(main())
