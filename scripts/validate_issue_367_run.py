#!/usr/bin/env python3
"""Валидация артефакта прогона RUN-0070 (issue #367, ТЗ BCREQ-1115).

Проверяет отчёт `runs/2026/RUN-0070/outputs/L0-feasibility-assessment-1115.md`:

1. таблица результата содержит ровно 6 колонок в каждой строке;
2. колонки 1–2 (№ и текст требования) посимвольно совпадают с транскрипцией
   исходника `experiments/issue_367/source_transcription.json` — в том же
   порядке, без пропусков, добавлений и «исправлений» опечаток;
3. колонка 3 имеет формат `Оценка: <br>[оценка] | [ ] | [ ]`, оценка — строго
   по шкале `Да / Частично / Нет / пусто`;
4. колонки 4–5 заполнены, колонка 5 содержит технический аудит, колонка 6 пуста;
   «Нет данных» в колонке 5 только при оценке `Нет`, «вне функционального
   контура» — только при пустой оценке;
5. атомарные ссылки `[ДОК, §X «Заголовок», с.Y](url)` указывают на runtime-БЗ
   на зафиксированном commit; если runtime на этом commit доступен локально
   (`MANGO_BA_RUNTIME_MAIN`), § / заголовок / страницы сверяются с frontmatter;
6. ссылки `[ТЗ-тендеров-v4, п/п X, с.Y]` указывают на существующий пункт шаблона
   и его страницу (`experiments/issue_367/tender_index.json`);
7. каталог прогона содержит обязательные файлы, контрольные суммы исходников
   зафиксированы в `inputs/README.md`, исходники в `inputs/` не хранятся.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "runs/2026/RUN-0070"
REPORT = RUN / "outputs/L0-feasibility-assessment-1115.md"
SOURCE = ROOT / "experiments/issue_367/source_transcription.json"
TENDER = ROOT / "experiments/issue_367/tender_index.json"
TENDER_SHA = "612e5e0938b9d4edad8e341f7fb03ba8498f7ec12dea0fe88f71e6817169d4cc"
RUN_FILES = (
    "metadata.yaml",
    "inputs/README.md",
    "outputs/README.md",
    "outputs/L0-feasibility-assessment-1115.md",
    "logs/experiment-log.md",
    "logs/technical-audit.md",
    "feedback/review-notes.md",
)

VERDICT = re.compile(r"^Оценка: <br>(Да|Частично|Нет|) ?\\\| \\\|$")
AUDIT = "Аудит: "
CITATION = re.compile(
    r"\[([^\[\]]+?), (?:§([^\[\]«]+?) )?«((?:[^«»]|«[^«»]*»)*)», с\.([^\[\]]+?)\]\(([^()]+)\)"
)
TENDER_CITATION = re.compile(r"\[ТЗ-тендеров-v4, п/п ([0-9.]+), с\.(\d+)\]\(([^()]+)\)")
BLOB = re.compile(r"^https://github\.com/G-Ivan-A/mango-ba-ai-runtime/blob/([0-9a-f]{40})/(docs/kb/.+\.md)$")


def split_row(line: str) -> list[str]:
    return [cell.strip() for cell in re.split(r"(?<!\\)\|", line.strip()[1:-1])]


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


def check_run(errors: list[str]) -> None:
    for name in RUN_FILES:
        if not (RUN / name).exists():
            errors.append("нет файла прогона: %s" % name)
    inputs = RUN / "inputs"
    if inputs.exists():
        stored = [p.name for p in inputs.iterdir() if p.name != "README.md"]
        if stored:
            errors.append("в inputs/ хранятся исходные файлы: %s" % ", ".join(sorted(stored)))
        readme = (inputs / "README.md").read_text(encoding="utf-8") if (inputs / "README.md").exists() else ""
        sha = json.loads(SOURCE.read_text(encoding="utf-8"))["sha256"]
        for digest in (sha, TENDER_SHA):
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
    for item, page, _href in TENDER_CITATION.findall(text):
        citations += 1
        if item not in tender:
            errors.append("ссылка на несуществующий п/п шаблона ТЗ-тендеров-v4: %s" % item)
        elif str(tender[item][0]) != page:
            errors.append("п/п %s шаблона: страница %s в ссылке, в шаблоне %s" % (item, page, tender[item][0]))
    return citations


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
    for offset, (cells, (_rid, num, req, _para)) in enumerate(zip(rows, expected), start=1):
        if len(cells) != 6:
            continue
        if cells[0] != num:
            errors.append("строка %d: № %r, в исходнике %r" % (offset, cells[0], num))
        if cells[1].replace("\\|", "|") != req:
            errors.append("строка %d (№%s): текст требования расходится с исходником" % (offset, num))
        match = VERDICT.match(cells[2])
        if not match:
            errors.append("строка %d: колонка «Оценка» не по формату/шкале: %r" % (offset, cells[2]))
            continue
        verdict = match.group(1)
        if not cells[3] or not cells[4]:
            errors.append("строка %d (№%s): пустое обоснование или цитата" % (offset, num))
        if AUDIT not in cells[4]:
            errors.append("строка %d (№%s): в колонке 5 нет технического аудита" % (offset, num))
        if cells[5]:
            errors.append("строка %d (№%s): колонка 6 (комментарий БА) должна быть пустой" % (offset, num))
        if cells[4].startswith("Нет данных") and verdict != "Нет":
            errors.append("строка %d (№%s): «Нет данных» при оценке %r" % (offset, num, verdict))
        if cells[4].lower().startswith("вне функционального контура") and verdict:
            errors.append("строка %d (№%s): «вне функционального контура» при оценке %r" % (offset, num, verdict))
        if verdict and "](" not in cells[3] and "Нет данных" not in cells[3]:
            errors.append("строка %d (№%s): оценка без ссылки на SSOT и без «Нет данных»" % (offset, num))

    citations = check_citations(text, errors)
    if not citations:
        errors.append("в отчёте нет ни одной атомарной ссылки на SSOT")
    check_run(errors)

    if errors:
        print("FAIL: validate_issue_367_run: найдено проблем: %d" % len(errors))
        for error in errors[:40]:
            print("  - %s" % error)
        return 1

    print("OK: validate_issue_367_run: строк требований %d, атомарных ссылок %d, колонок 6" % (len(rows), citations))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
