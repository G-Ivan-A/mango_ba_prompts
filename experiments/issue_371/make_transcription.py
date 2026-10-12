#!/usr/bin/env python3
"""Транскрипция колонок 1–2 ТЗ 2026 (issue #371, задача 1117) -> source_transcription.json.

Исходник — «Телефония ТЗ 0710 1026 года в анализ.pdf» (Word 2013 -> PDF, текстовый слой,
6 страниц). Строки отчёта выделяются из текстового слоя pymupdf по признакам начала абзаца:

- номер пункта «2.1.», «3.17.», «4.» в начале строки — колонка 1 = номер как в исходнике;
- маркер списка — глиф шрифта SymbolMT: U+F02D (Symbol 0x2D, «−», минус) в разд. 1, 3.1,
  3.2, 3.17, 4.1 и U+F0B7 (Symbol 0xB7, «•») в 3.3 и Приложении 2 — колонка 1 = «−» / «•»
  (Unicode-эквивалент глифа, как он виден в документе);
- ненумерованные абзацы («Не оценивается» в разд. 5–7, Приложение 2) — колонка 1 пуста.

Колонка 2 — текст абзаца: строки PDF внутри абзаца — мягкие переносы вёрстки Word, они
склеиваются одним пробелом (хвостовой пробел строки снимается); перенос после дефиса
(«веб-», «дата-», «онлайн-») — часть слова, склеивается без пробела. Опечатки, регистр,
пунктуация и пробелы внутри строки не меняются. Твёрдых разрывов строк внутри абзацев
в исходнике нет, поэтому `<br>` в колонке 2 не используется.

Не переносятся (не требования): титул («ТЕХНИЧЕСКОЕ ЗАДАНИЕ», наименование закупки) и
блок «Термины и определения» (13 определений). Строки «Не оценивается» переносятся как
есть — они часть структуры документа.

Запуск: python3 experiments/issue_371/make_transcription.py /path/to/tz2026.pdf
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

import pymupdf

HERE = Path(__file__).resolve().parent
TITLE = "Телефония ТЗ 0710 1026 года в анализ.pdf"
MARKERS = {"": "−", "": "•"}
NUMBER = re.compile(r"^(\d+\.(?:\d+\.)?)(?:\s+(.*))?$")
EXCLUDED_TITLE = ("ТЕХНИЧЕСКОЕ ЗАДАНИЕ", "Предоставление доступа к программному обеспечению расширенной IP-телефонии")
TERMS_START, TERMS_END = "Термины и определения", "2. Стандарт услуг"


def lines(pdf: Path) -> list[tuple[int, str]]:
    out = []
    for pno, page in enumerate(pymupdf.open(pdf), start=1):
        for raw in page.get_text().split("\n"):
            text = raw.rstrip()
            if text.strip():
                out.append((pno, text.lstrip(" ")))
    return out


def join(prev: str, nxt: str) -> str:
    if re.search(r"[A-Za-zА-Яа-яЁё]-$", prev):
        return prev + nxt
    return prev + " " + nxt


def rows(pdf: Path) -> tuple[list[list], list[str]]:
    result: list[list] = []
    excluded: list[str] = []
    in_terms = False
    for pno, line in lines(pdf):
        if line.strip() in EXCLUDED_TITLE:
            excluded.append(line.strip())
            continue
        if line.strip() == TERMS_START:
            in_terms = True
        if in_terms:
            if line.strip() == TERMS_END:
                in_terms = False
            else:
                excluded.append(line.strip())
                continue
        marker = line[0] if line[0] in MARKERS else None
        number = NUMBER.match(line) if marker is None else None
        if marker:
            result.append([MARKERS[marker], line[1:].strip(), pno])
        elif number:
            result.append([number.group(1), (number.group(2) or "").strip(), pno])
        elif result and not result[-1][1]:
            # номер или маркер стоит отдельной строкой («2.5.», «3.14.», «» в разд. 1)
            result[-1][1] = line.strip()
        elif line.strip() in ("Не оценивается", "Приложение 2 к Техническому заданию") or line.startswith("Исполнитель предоставляет доступ"):
            result.append(["", line.strip(), pno])
        else:
            assert result, line
            result[-1][1] = join(result[-1][1], line.strip())
    return result, excluded


def main() -> None:
    pdf = Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/dl371/tz2026/tz2026.pdf")
    data = pdf.read_bytes()
    found, excluded = rows(pdf)
    out = {
        "title": TITLE,
        "sha256": hashlib.sha256(data).hexdigest(),
        "size": len(data),
        "excluded": excluded,
        "rows": [[f"R{i:03d}", num, req, f"p{page}"] for i, (num, req, page) in enumerate(found, start=1)],
    }
    (HERE / "source_transcription.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"rows: {len(found)}, excluded lines: {len(excluded)}, sha256 {out['sha256']}")


if __name__ == "__main__":
    main()
