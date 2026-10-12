#!/usr/bin/env python3
"""Валидация артефакта прогона RUN-0072 (issue #371, ТЗ 2026 по BCREQ-1116, задача 1117).

Проверяет отчёт `runs/2026/RUN-0072/outputs/L0-feasibility-assessment-1117.md`:

0. отчёт состоит из двух разделов: `## Отчёт 1: оценка исполнимости «имя файла»`
   (таблица оценки ТЗ 2026) и `## Отчёт 2: анализ дельты ТЗ 2026 к ТЗ 2025`
   (аналитическая записка с таблицей дельты); до Отчёта 1 таблиц нет;
1. таблица Отчёта 1 содержит ровно 6 колонок в каждой строке;
2. колонки 1–2 (№ и текст требования) посимвольно совпадают с транскрипцией
   исходника `experiments/issue_371/source_transcription.json` — в том же
   порядке, без пропусков, добавлений и правок (ячейка отделена от `|` ровно
   одним пробелом);
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
7. таблица дельты Отчёта 2 содержит 7 колонок, вид изменения — `Изменено /
   Добавлено / Исключено`, ссылки на строки Отчёта 1 существуют, а оценка в них
   совпадает с колонкой 3 Отчёта 1; у изменённых пунктов заполнены «Было» и «Стало»;
8. каталог прогона содержит обязательные файлы, контрольные суммы ТЗ 2026, ТЗ 2025
   и шаблона v4 зафиксированы в `inputs/README.md`, исходники в `inputs/` не хранятся.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "runs/2026/RUN-0072"
REPORT = RUN / "outputs/L0-feasibility-assessment-1117.md"
SOURCE = ROOT / "experiments/issue_371/source_transcription.json"
TENDER = ROOT / "experiments/issue_367/tender_index.json"
TENDER_SHA = "612e5e0938b9d4edad8e341f7fb03ba8498f7ec12dea0fe88f71e6817169d4cc"
RUN_FILES = (
    "metadata.yaml",
    "inputs/README.md",
    "outputs/README.md",
    "outputs/L0-feasibility-assessment-1117.md",
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
REPORT1 = "## Отчёт 1: оценка исполнимости «%s»"
REPORT2 = "## Отчёт 2: анализ дельты ТЗ 2026 к ТЗ 2025"
TZ2025_SHA = "0659eeae961a36c302f9b92dc66c3cf5bd2041cedf17b29175d40d1df4602191"
DELTA_ROW = re.compile(r"^строка (\d+) \(п\. [^()]+\) — (Да|Частично|Нет|пусто)$")
BLOB = re.compile(r"^https://github\.com/G-Ivan-A/mango-ba-ai-runtime/blob/([0-9a-f]{40})/(docs/kb/.+\.md)$")


def unpad(cell: str) -> str:
    """Снять ровно один пробел-отступ с каждой стороны ячейки."""
    cell = cell[1:] if cell.startswith(" ") else cell
    return cell[:-1] if cell.endswith(" ") else cell


def split_row(line: str) -> list[str]:
    return [unpad(cell) for cell in re.split(r"(?<!\\)\|", line[1:-1])]


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
        for digest in (json.loads(SOURCE.read_text(encoding="utf-8"))["sha256"], TZ2025_SHA, TENDER_SHA):
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


def tables(text: str) -> tuple[list[str], list[str], str]:
    """(строки таблицы Отчёта 1, строки таблицы Отчёта 2, текст до Отчёта 1)."""
    title = json.loads(SOURCE.read_text(encoding="utf-8"))["title"]
    head1, head2 = REPORT1 % title, REPORT2
    lines = text.splitlines()
    if head1 not in lines or head2 not in lines or lines.index(head1) > lines.index(head2):
        return [], [], text
    i1, i2 = lines.index(head1), lines.index(head2)
    pick = lambda part: [line for line in part if line.startswith("|")]  # noqa: E731
    return pick(lines[i1:i2]), pick(lines[i2:]), "\n".join(lines[:i1])


def check_delta(table: list[str], verdicts: list[str], errors: list[str]) -> int:
    if len(table) < 3:
        errors.append("Отчёт 2: нет таблицы дельты")
        return 0
    for offset, line in enumerate(table[2:], start=1):
        cells = [cell.strip() for cell in split_row(line)]
        if len(cells) != 7:
            errors.append("Отчёт 2: строка %d: колонок %d, ожидается 7" % (offset, len(cells)))
            continue
        number, kind, _p2025, targets, was, now, impact = cells
        if number != str(offset):
            errors.append("Отчёт 2: строка %d: № %r" % (offset, number))
        if kind not in ("Изменено", "Добавлено", "Исключено"):
            errors.append("Отчёт 2: строка %d: вид изменения %r" % (offset, kind))
        if not impact:
            errors.append("Отчёт 2: строка %d: не указано влияние на оценку" % offset)
        if (was == "—") != (kind == "Добавлено") or (now == "—") != (kind == "Исключено"):
            errors.append("Отчёт 2: строка %d: «Было»/«Стало» не соответствуют виду %r" % (offset, kind))
        if kind == "Исключено":
            continue
        for target in targets.split("<br>"):
            match = DELTA_ROW.match(target)
            if not match:
                errors.append("Отчёт 2: строка %d: ссылка на строку Отчёта 1 не по формату: %r" % (offset, target))
                continue
            row, verdict = int(match.group(1)), match.group(2)
            if not 1 <= row <= len(verdicts):
                errors.append("Отчёт 2: строка %d: нет строки Отчёта 1 №%d" % (offset, row))
            elif (verdicts[row - 1] or "пусто") != verdict:
                errors.append("Отчёт 2: строка %d: оценка строки %d %r, в Отчёте 1 %r" % (offset, row, verdict, verdicts[row - 1]))
    return len(table) - 2


def main() -> int:
    errors: list[str] = []
    if not REPORT.exists():
        print("FAIL: отчёт не найден: %s" % REPORT.relative_to(ROOT))
        return 1

    text = REPORT.read_text(encoding="utf-8")
    table, delta, before = tables(text)
    if not table:
        errors.append("нет разделов «Отчёт 1» и «Отчёт 2» в нужном порядке")
    if any(line.startswith("|") for line in before.splitlines()):
        errors.append("таблица до раздела «Отчёт 1»")
    for offset, line in enumerate(table, start=1):
        if len(split_row(line)) != 6:
            errors.append("строка таблицы %d: колонок %d, ожидается 6" % (offset, len(split_row(line))))
    rows = [split_row(line) for line in table[2:]]
    expected = json.loads(SOURCE.read_text(encoding="utf-8"))["rows"]
    if len(rows) != len(expected):
        errors.append("строк требований %d, в транскрипции исходника %d" % (len(rows), len(expected)))
    verdicts: list[str] = []
    for offset, (cells, (_rid, num, req, _page)) in enumerate(zip(rows, expected), start=1):
        if len(cells) != 6:
            verdicts.append("?")
            continue
        where = "строка %d (№%s)" % (offset, num)
        if cells[0] != num:
            errors.append("%s: № %r, в исходнике %r" % (where, cells[0], num))
        if cells[1].replace("\\|", "|") != req:
            errors.append("%s: текст требования расходится с исходником" % where)
        cells = [cell.strip() for cell in cells]
        match = VERDICT.match(cells[2])
        if not match:
            errors.append("%s: колонка «Оценка» не по формату/шкале: %r" % (where, cells[2]))
            verdicts.append("?")
            continue
        verdict = match.group(1)
        verdicts.append(verdict)
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

    changes = check_delta(delta, verdicts, errors) if table else 0
    citations = check_citations(text, errors)
    if not citations:
        errors.append("в отчёте нет ни одной атомарной ссылки на SSOT")
    check_run(errors)

    if errors:
        print("FAIL: validate_issue_371_run: найдено проблем: %d" % len(errors))
        for error in errors[:40]:
            print("  - %s" % error)
        return 1

    print("OK: validate_issue_371_run: строк требований %d, атомарных ссылок %d, колонок 6, изменений в дельте %d"
          % (len(rows), citations, changes))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
