#!/usr/bin/env python3
"""Валидация артефакта прогона RUN-0093 (issue #482, ТЗ BCREQ-1140).

Проверяет отчёт `runs/2026/RUN-0093/outputs/L0-feasibility-assessment-1140.md`:

0. PDF Заказчика содержит два документа — в отчёте два блока с явными разделителями
   `### Документ 1 из 2: «…»` и `### Документ 2 из 2: «…»`, у каждого своя таблица;
1. таблица результата содержит ровно 6 колонок в каждой строке;
2. колонки 1–2 (№ и текст требования) посимвольно совпадают с транскрипцией исходника
   `experiments/issue_482/source_transcription.json` (видимый текст PDF, зачёркнутое
   правкой — `~~…~~`) — в том же порядке, без пропусков и добавлений;
3. колонка 3 имеет формат `Оценка: <br>[оценка] | [ ] | [ ]`, оценка — строго по шкале
   `Да / Частично / Нет / пусто` (колонки оценки поставщика в исходнике нет — средняя
   часть пустая); строка, целиком зачёркнутая правкой, имеет пустую оценку;
4. колонки 4–5 заполнены, колонка 5 содержит технический аудит, колонка 6 пуста;
   «Нет данных» в колонке 5 только при оценке `Нет`, «вне функционального контура» —
   только при пустой оценке; «Не требует обоснования» — только при `Да` со ссылкой на
   п/п шаблона ТЗ-тендеров-v4;
5. атомарные ссылки `[ДОК, §X «Заголовок», с.Y](url)` указывают на runtime-БЗ на
   зафиксированном commit; если runtime на этом commit доступен локально
   (`MANGO_BA_RUNTIME_MAIN`), § / заголовок / страницы сверяются с frontmatter;
6. ссылки `[ТЗ-тендеров-v4, п/п X, с.Y](url)` указывают на существующий пункт шаблона и его
   страницу (`experiments/issue_367/tender_index.json`; подпункты 2.14.8.1/2.14.8.2 — внутри
   2.14.8) и на вложение шаблона из issue #482;
7. каталог прогона содержит обязательные файлы, контрольные суммы исходника и шаблона
   зафиксированы в `inputs/README.md`, исходники в `inputs/` не хранятся.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "runs/2026/RUN-0093"
REPORT = RUN / "outputs/L0-feasibility-assessment-1140.md"
SOURCE = ROOT / "experiments/issue_482/source_transcription.json"
TENDER = ROOT / "experiments/issue_367/tender_index.json"
TENDER_SHA = "612e5e0938b9d4edad8e341f7fb03ba8498f7ec12dea0fe88f71e6817169d4cc"
TENDER_URL = "https://github.com/user-attachments/files/34651817/-.-v4.pdf"
RUN_FILES = (
    "metadata.yaml",
    "inputs/README.md",
    "outputs/README.md",
    "outputs/L0-feasibility-assessment-1140.md",
    "logs/experiment-log.md",
    "logs/technical-audit.md",
    "feedback/review-notes.md",
)

VERDICT = re.compile(r"^Оценка: <br>(Да|Частично|Нет|) \\\| (.*?) ?\\\|$")
AUDIT = "Аудит: "
CITATION = re.compile(
    r"\[([^\[\]]+?), (?:§([^\[\]«]+?) )?«((?:[^«»]|«[^«»]*»)*)», с\.([^\[\]]+?)\]\(([^()]+)\)"
)
TENDER_CITATION = re.compile(r"\[ТЗ-тендеров-v4, (?:п/п ([0-9.]+)|разд\. «[^«»]+»), с\.(\d+)\]\(([^()]+)\)")
BLOB = re.compile(r"^https://github\.com/G-Ivan-A/mango-ba-ai-runtime/blob/([0-9a-f]{40})/(docs/kb/.+\.md)$")
BLOCK = re.compile(r"^### Документ (\d+) из (\d+): «(.+)»$")


def unpad(cell: str) -> str:
    """Снять ровно один пробел-отступ с каждой стороны ячейки."""
    cell = cell[1:] if cell.startswith(" ") else cell
    return cell[:-1] if cell.endswith(" ") else cell


def split_row(line: str) -> list[str]:
    return [unpad(cell) for cell in re.split(r"(?<!\\)\|", line[1:-1])]


def blocks(text: str) -> list[tuple[str, list[str]]]:
    """[(заголовок-разделитель, строки таблицы блока)] в порядке документа."""
    found: list[tuple[str, list[str]]] = []
    for line in text.splitlines():
        if BLOCK.match(line):
            found.append((line, []))
        elif line.startswith("|") and found:
            found[-1][1].append(line)
    return found


def frontmatter(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines()[1:]:
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


def check_run(source: dict, errors: list[str]) -> None:
    for name in RUN_FILES:
        if not (RUN / name).exists():
            errors.append("нет файла прогона: %s" % name)
    inputs = RUN / "inputs"
    if inputs.exists():
        stored = [p.name for p in inputs.iterdir() if p.name != "README.md"]
        if stored:
            errors.append("в inputs/ хранятся исходные файлы: %s" % ", ".join(sorted(stored)))
        readme = (inputs / "README.md").read_text(encoding="utf-8") if (inputs / "README.md").exists() else ""
        for digest in (source["sha256"], TENDER_SHA):
            if digest not in readme:
                errors.append("inputs/README.md: не зафиксирована контрольная сумма %s" % digest)


def check_citations(text: str, errors: list[str]) -> int:
    citations = 0
    for doc, section, title, pages, href in CITATION.findall(text):
        if doc.startswith("ТЗ-тендеров-v4"):
            continue
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

    tender = json.loads(TENDER.read_text(encoding="utf-8"))
    for item, page, href in TENDER_CITATION.findall(text):
        citations += 1
        if href != TENDER_URL:
            errors.append("ссылка на шаблон v4 не на вложение issue #482: %s" % href)
        if not item:
            if page != "5":
                errors.append("раздел общих требований шаблона v4 — с.5, в ссылке с.%s" % page)
            continue
        key = item if item in tender else item.rsplit(".", 1)[0]
        if key not in tender or (key != item and item not in tender[key][1]):
            errors.append("ссылка на несуществующий п/п шаблона ТЗ-тендеров-v4: %s" % item)
        elif str(tender[key][0]) != page:
            errors.append("п/п %s шаблона: страница %s в ссылке, в шаблоне %s" % (item, page, tender[key][0]))
    return citations


def main() -> int:
    errors: list[str] = []
    if not REPORT.exists():
        print("FAIL: отчёт не найден: %s" % REPORT.relative_to(ROOT))
        return 1

    text = REPORT.read_text(encoding="utf-8")
    if any(line.startswith("|") for line in text.split("\n### Документ ", 1)[0].splitlines()):
        errors.append("таблица до первого разделителя документа")
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    found = blocks(text)
    heads = [BLOCK.match(head).group(1, 2) for head, _ in found]
    if heads != [("1", "2"), ("2", "2")]:
        errors.append("разделители документов %r, ожидаются «Документ 1 из 2», «Документ 2 из 2»" % heads)
    total = 0
    counts = {"Да": 0, "Частично": 0, "Нет": 0, "": 0}
    for doc, (head, table) in enumerate(found, start=1):
        name = "Документ %d" % doc
        for offset, line in enumerate(table, start=1):
            if len(split_row(line)) != 6:
                errors.append("%s: строка таблицы %d: колонок %d, ожидается 6" % (name, offset, len(split_row(line))))
        rows = [split_row(line) for line in table[2:]]
        expected = [row for row in source["rows"] if row[6] == doc]
        total += len(rows)
        if len(rows) != len(expected):
            errors.append("%s: строк требований %d, в транскрипции исходника %d" % (name, len(rows), len(expected)))
        for cells, (rid, num, visible, _page, accepted, _value, _doc) in zip(rows, expected):
            if len(cells) != 6:
                continue
            where = "%s %s (№%s)" % (name, rid, num)
            if cells[0] != num:
                errors.append("%s: № %r, в исходнике %r" % (where, cells[0], num))
            if cells[1].replace("\\|", "|") != visible:
                errors.append("%s: текст требования расходится с исходником" % where)
            cells = [cell.strip() for cell in cells]
            match = VERDICT.match(cells[2])
            if not match:
                errors.append("%s: колонка «Оценка» не по формату/шкале: %r" % (where, cells[2]))
                continue
            verdict = match.group(1)
            counts[verdict] += 1
            if match.group(2):
                errors.append("%s: средняя часть колонки 3 должна быть пустой: %r" % (where, match.group(2)))
            if not accepted and verdict:
                errors.append("%s: строка зачёркнута правкой целиком, но оценена %r" % (where, verdict))
            if not cells[3] or not cells[4]:
                errors.append("%s: пустое обоснование или цитата" % where)
            if AUDIT not in cells[4]:
                errors.append("%s: в колонке 5 нет технического аудита" % where)
            if cells[5]:
                errors.append("%s: колонка 6 (комментарий БА) должна быть пустой" % where)
            if verdict == "Нет" and "Нет данных" in cells[3] and not cells[4].startswith("Нет данных"):
                errors.append("%s: «Нет данных» в обосновании, но не в колонке 5" % where)
            if not verdict and not cells[4].lower().startswith("вне функционального контура"):
                errors.append("%s: пустая оценка без «вне функционального контура»" % where)
            if cells[4].startswith("Нет данных") and verdict != "Нет":
                errors.append("%s: «Нет данных» при оценке %r" % (where, verdict))
            if cells[4].lower().startswith("вне функционального контура") and verdict:
                errors.append("%s: «вне функционального контура» при оценке %r" % (where, verdict))
            if verdict and "](" not in cells[3] and "Нет данных" not in cells[3]:
                errors.append("%s: оценка без ссылки на SSOT и без «Нет данных»" % where)
            if "Не требует обоснования" in cells[3] and (verdict != "Да" or "[ТЗ-тендеров-v4, " not in cells[3]):
                errors.append("%s: «Не требует обоснования» без `Да` или без ссылки на п/п шаблона v4" % where)

    citations = check_citations(text, errors)
    if not citations:
        errors.append("в отчёте нет ни одной атомарной ссылки на SSOT")
    check_run(source, errors)

    if errors:
        print("FAIL: validate_issue_482_run: найдено проблем: %d" % len(errors))
        for error in errors[:40]:
            print("  - %s" % error)
        return 1

    summary = ", ".join("%s %d" % (k or "пусто", v) for k, v in counts.items())
    print("OK: validate_issue_482_run: документов %d, строк требований %d (%s), атомарных ссылок %d, колонок 6"
          % (len(found), total, summary, citations))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
