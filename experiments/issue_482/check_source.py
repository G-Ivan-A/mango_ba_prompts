#!/usr/bin/env python3
"""Независимая сверка `source_transcription.json` с PDF BCREQ-1140 (issue #482).

Транскрипция строится pymupdf (`make_transcription.py`); здесь тот же PDF разбирается
другой библиотекой — pdfplumber (pdfminer.six) — и проверяется тремя способами:

1. **SHA-256** файла совпадает с записанным в транскрипции.
2. **Полнота без выдумок**: мультимножество непробельных символов всех страниц
   (x < 405 плюс выноска на поле) равно мультимножеству символов транскрипции —
   номера + колонка 2 (без `~~`, `<br>`) + «Требуемое значение» + исключённые строки
   (глоссарий, шапки, титул, маркеры, выноска). Ни один символ не потерян и не добавлен.
3. **Порядок и границы строк**: для таблицы (с.4–31) из pdfplumber вырезается полоса
   колонки «Требование» (127,2 < x < 345,5), для «Общих требований» (с.4) и вложенного
   ТЗ (с.32–33) — вся ширина; непробельный текст каждой строки транскрипции обязан
   идти в этом потоке подряд, а между строками допустимы только номера / маркеры /
   титул ТЗ-2 (шапка таблицы отбрасывается по строке «№ п/п»); поток колонки «№ п/п»
   равен колонке 1 транскрипции по порядку.
4. **Правки рецензирования**: символ считается удалённым, если его середину пересекает
   тонкий горизонтальный прямоугольник/линия цвета правки (pdfplumber `rects`+`lines`,
   non_stroking/stroking color). Мультимножество удалённых символов обязано совпасть с
   содержимым `~~…~~` транскрипции (колонки 1, 2, 3 и титул).

    python3 -I experiments/issue_482/check_source.py /path/to/tz-1140.pdf
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

import pdfplumber

HERE = Path(__file__).resolve().parent
MARGIN_X = 405.0
EDIT_RGB = ((0.71, 0.031, 0.18), (0.18, 0.592, 0.827))
SYMBOL_MAP = {"": "−"}
COL2 = (127.2, 345.5)


def nonspace(text: str) -> str:
    return "".join(SYMBOL_MAP.get(c, c) for c in text if not c.isspace())


def plain(cell: str) -> str:
    return nonspace(cell.replace("~~", "").replace("<br>", ""))


def struck(cell: str) -> str:
    return nonspace("".join(re.findall(r"~~(.+?)~~", cell)))


def is_edit_color(color) -> bool:
    if not color or len(color) != 3:
        return False
    return any(all(abs(a - b) < 0.02 for a, b in zip(color, rgb)) for rgb in EDIT_RGB)


def edit_marks(page) -> list[tuple[float, float, float]]:
    marks = []
    for obj in list(page.rects) + list(page.lines):
        h = abs(obj["bottom"] - obj["top"])
        w = obj["x1"] - obj["x0"]
        if h < 2 and w > 1 and (is_edit_color(obj.get("non_stroking_color"))
                                or is_edit_color(obj.get("stroking_color"))):
            marks.append((obj["x0"], obj["x1"], (obj["top"] + obj["bottom"]) / 2))
    return marks


def is_struck(ch, marks) -> bool:
    h = ch["bottom"] - ch["top"]
    cx = (ch["x0"] + ch["x1"]) / 2
    for x0, x1, y in marks:
        if x0 - 0.5 <= cx <= x1 + 0.5 and 0.3 <= (y - ch["top"]) / h < 0.65:
            return True
    return False


def main() -> int:
    pdf_path = Path(sys.argv[1])
    data = json.loads((HERE / "source_transcription.json").read_text(encoding="utf-8"))
    raw = pdf_path.read_bytes()
    bad = 0
    if hashlib.sha256(raw).hexdigest() != data["sha256"] or len(raw) != data["size"]:
        print("SHA256/SIZE MISMATCH")
        bad += 1

    rows = data["rows"]
    pdf = pdfplumber.open(pdf_path)
    if len(pdf.pages) != data["pages"]:
        print("PAGE COUNT MISMATCH")
        bad += 1

    # 2. полнота
    pdf_all, pdf_struck = Counter(), Counter()
    for page in pdf.pages:
        marks = edit_marks(page)
        for ch in page.chars:
            t = nonspace(ch["text"])
            if not t:
                continue
            pdf_all[t] += 1
            if is_struck(ch, marks):
                pdf_struck[t] += 1
    tr_all, tr_struck = Counter(), Counter()
    for _rid, num, req, _p, _acc, value, _doc in rows:
        for cell in (num, req, value):
            tr_all.update(plain(cell))
            tr_struck.update(struck(cell))
    for ex in data["excluded"]:
        tr_all.update(plain(ex["text"]))
        tr_struck.update(struck(ex["text"]))
    if pdf_all != tr_all:
        bad += 1
        print("CHARSET MISMATCH: только в PDF", dict(pdf_all - tr_all), "только в транскрипции", dict(tr_all - pdf_all))
    if pdf_struck != tr_struck:
        bad += 1
        print("STRUCK MISMATCH: только в PDF", dict(pdf_struck - tr_struck), "только в транскрипции", dict(tr_struck - pdf_struck))

    # 3. порядок: поток колонки 2 таблицы и поток всей ширины для общих требований / ТЗ-2
    def word_top(page, text):
        return [w["top"] for w in page.extract_words() if w["text"] == text]

    def stream(pages, crop):
        out = []
        for page in pages:
            # строка шапки таблицы («№ п/п | Требование | Требуемое значение») — не текст строк
            head = word_top(page, "п/п")
            words = page.crop(crop(page)).extract_words(keep_blank_chars=False, use_text_flow=False)
            words = [w for w in words if not any(abs(w["top"] - t) < 6 for t in head)]
            # построчная сортировка: сверху вниз, слева направо (с допуском 3 pt по y)
            words.sort(key=lambda w: (round(w["bottom"] / 3), w["x0"]))
            out.append(nonspace("".join(w["text"] for w in words if w["x0"] < MARGIN_X)))
        return "".join(out)

    p4 = pdf.pages[3]
    table_top = word_top(p4, "Функциональные")[0]
    col2 = stream(pdf.pages[3:31], lambda p: (COL2[0], table_top + 10 if p is p4 else 0, COL2[1], p.height))
    wide = (stream([p4], lambda p: (0, 0, MARGIN_X, table_top - 1))
            + stream(pdf.pages[31:33], lambda p: (0, 0, MARGIN_X, p.height)))
    title = plain("".join(e["text"] for e in data["excluded"] if e["reason"].startswith("титул")))
    # между строками допустимы только номера пунктов, маркеры «o» / U+F0B7 / «−» и титул ТЗ-2
    allowed_gap = re.compile(r"^[\d.o−]*$")
    pos = {"col2": 0, "wide": 0}
    checked = 0
    for rid, num, req, _p, _acc, value, doc in rows:
        text = plain(req)
        key, src = ("col2", col2) if (doc == 1 and rid > "R005") else ("wide", wide)
        if not text:
            continue
        i = src.find(text, pos[key])
        if i < 0:
            bad += 1
            print("ORDER/TEXT MISMATCH", rid, num, text[:80])
            continue
        gap = src[pos[key]:i]
        if pos[key] and not (allowed_gap.match(gap) or allowed_gap.match(gap.replace(title, "", 1))):
            bad += 1
            print("UNEXPECTED GAP before", rid, repr(gap[:120]))
        pos[key] = i + len(text)
        checked += 1
    for key, src in (("col2", col2), ("wide", wide)):
        if not allowed_gap.match(src[pos[key]:]):
            bad += 1
            print("UNCOVERED TAIL", key, repr(src[pos[key]:][:120]))
    # колонка «№ п/п» таблицы: поток номеров (без невидимых маркеров) = колонка 1 по порядку
    col1 = stream(pdf.pages[3:31], lambda p: (0, table_top + 10 if p is p4 else 0, COL2[0], p.height))
    col1 = col1.replace("", "")
    want = "".join(plain(num) for rid, num, *_r, doc in rows if doc == 1 and rid > "R005")
    if col1 != want:
        bad += 1
        print("COL1 MISMATCH", col1[:200], "!=", want[:200])
    print(f"rows: {len(rows)}; ordered rows matched: {checked}; chars PDF={sum(pdf_all.values())} "
          f"transcription={sum(tr_all.values())}; struck PDF={sum(pdf_struck.values())} "
          f"transcription={sum(tr_struck.values())}; mismatches: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
