#!/usr/bin/env python3
"""Валидация артефакта прогона RUN-0068 (issue #363, ТЗ BCREQ-1114).

Проверяет отчёт `runs/2026/RUN-0068/outputs/L0-feasibility-assessment-1114.md`:

1. таблица результата содержит ровно 6 колонок в каждой строке;
2. колонка «Оценка» заполняется строго по шкале `Да / Частично / Нет / пусто`;
3. колонки 1–2 (№ и текст требования) посимвольно совпадают с транскрипцией
   исходника `experiments/issue_363/source_transcription.json` — в том же
   порядке, без пропусков, добавлений и «исправлений» опечаток;
4. атомарные ссылки `[ДОК, §X «Заголовок», с.Y](url)` указывают на runtime-БЗ
   на зафиксированном commit; если runtime на этом commit доступен локально
   (`MANGO_BA_RUNTIME_MAIN`), § / заголовок / страницы сверяются с frontmatter.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "runs/2026/RUN-0068/outputs/L0-feasibility-assessment-1114.md"
SOURCE = ROOT / "experiments/issue_363/source_transcription.json"

VERDICTS = {"Да", "Частично", "Нет", ""}
CITATION = re.compile(
    r"\[([^\[\]]+?), (?:§([^\[\]«]+?) )?«((?:[^«»]|«[^«»]*»)*)», с\.([^\[\]]+?)\]\(([^()]+)\)"
)
BLOB = re.compile(r"^https://github\.com/G-Ivan-A/mango-ba-ai-runtime/blob/([0-9a-f]{40})/(docs/kb/.+\.md)$")


def split_row(line: str) -> list[str]:
    return [cell.strip() for cell in re.split(r"(?<!\\)\|", line.strip().strip("|"))]


def frontmatter(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    data: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" in line and not line.startswith((" ", "-")):
            key, _, value = line.partition(":")
            data[key.strip()] = value.strip().strip("\"'")
    return data


def local_runtime(commit: str) -> Path | None:
    path = os.environ.get("MANGO_BA_RUNTIME_MAIN")
    if not path:
        return None
    try:
        head = subprocess.check_output(["git", "-C", path, "rev-parse", "HEAD"], text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None
    return Path(path) if head == commit else None


def main() -> int:
    errors: list[str] = []
    if not REPORT.exists():
        print("FAIL: отчёт не найден: %s" % REPORT.relative_to(ROOT))
        return 1

    text = REPORT.read_text(encoding="utf-8")
    table = [line for line in text.splitlines() if line.startswith("|")]
    for offset, line in enumerate(table, start=1):
        if len(split_row(line)) != 6:
            errors.append("строка таблицы %d: колонок %d, ожидается 6" % (offset, len(split_row(line))))

    rows = [split_row(line) for line in table[2:]]
    expected = json.loads(SOURCE.read_text(encoding="utf-8"))["rows"]
    if len(rows) != len(expected):
        errors.append("строк требований %d, в транскрипции исходника %d" % (len(rows), len(expected)))
    for offset, (cells, (num, req, _image)) in enumerate(zip(rows, expected), start=1):
        if len(cells) != 6:
            continue
        if cells[0] != num:
            errors.append("строка %d: № %r, в исходнике %r" % (offset, cells[0], num))
        if cells[1].replace("\\|", "|") != req:
            errors.append("строка %d (№%s): текст требования расходится с исходником" % (offset, num))
        if cells[2] not in VERDICTS:
            errors.append("строка %d: недопустимая оценка %r" % (offset, cells[2]))
        if not cells[3] or not cells[4] or not cells[5]:
            errors.append("строка %d (№%s): пустое обоснование, цитата или аудит" % (offset, num))

    citations = 0
    for doc, section, title, pages, href in CITATION.findall(text):
        citations += 1
        match = BLOB.match(href)
        if not match:
            errors.append("ссылка не на runtime-БЗ с фиксированным commit: %s" % href)
            continue
        runtime = local_runtime(match.group(1))
        if runtime is None:
            continue
        target = runtime / match.group(2)
        if not target.exists():
            errors.append("ссылка на несуществующий раздел: %s" % match.group(2))
            continue
        meta = frontmatter(target)
        actual = meta.get("pdf_section", "")
        if actual in ("", "0", "-", "—"):
            actual = meta.get("section", "")
        if actual in ("", "0", "-", "—"):
            actual = ""
        for label, got, want in (("§", section or "", actual), ("заголовок", title, meta.get("title", "")),
                                 ("страницы", pages, meta.get("pages", "")), ("документ", doc, meta.get("doc_code", ""))):
            if got != want:
                errors.append("%s: %s в ссылке %r, во frontmatter %r" % (match.group(2), label, got, want))

    if not citations:
        errors.append("в отчёте нет ни одной атомарной ссылки на базу знаний")

    if errors:
        print("FAIL: validate_issue_363_run: найдено проблем: %d" % len(errors))
        for error in errors[:40]:
            print("  - %s" % error)
        return 1

    print("OK: validate_issue_363_run: строк требований %d, атомарных ссылок %d, колонок 6" % (len(rows), citations))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
