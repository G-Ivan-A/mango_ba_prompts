#!/usr/bin/env python3
"""Валидация артефакта прогона RUN-0094 (issue #484, ТЗ BCREQ-1199, 2-я версия).

Правила оценки issue #484 для отчёта `runs/2026/RUN-0094/outputs/L0-feasibility-assessment-1199-2.md`
в форме v2.0 (issue #486): слева добавлена колонка «№ пп», составные требования разложены на
атомарные строки. Форму (сквозной «№ пп», колонки «№» и «Требование» против транскрипции
исходника, заголовки комплексных требований) проверяет `scripts/validate_issue_486_run.py`;
здесь — содержательные правила issue #484 для каждой строки отчёта:

0. исходник содержит два листа с требованиями — в отчёте два блока с явными разделителями
   `### Лист 1 из 2: «…»` и `### Лист 2 из 2: «…»`, у каждого своя таблица;
1. таблица результата содержит ровно 7 колонок в каждой строке, шапка — по контракту;
2. строк отчёта не меньше, чем непустых строк исходника на листе (транскрипция
   `experiments/issue_484/source_transcription.json`);
3. колонка «Оценка» имеет формат `Оценка: <br>[оценка] | [ ] | [ ]`, оценка — строго по шкале
   `Да / Частично / Нет / пусто`; колонки исходника «Факт реализации» и «Срок доработки»
   пустые, поэтому средняя часть колонки пустая;
4. колонки «Обоснование» и «Цитата» заполнены, вторая содержит технический аудит,
   «Комментарий БА» пуст; «Нет данных» в колонке цитат только при оценке `Нет`, «вне функционального контура» —
   только при пустой оценке; «Не требует обоснования» — только при `Да` со ссылкой на
   п/п шаблона ТЗ-тендеров-v4 (для строки целиком — только при `Да`, для отдельной
   атомарной части внутри обоснования); оценка `Да` / `Частично`
   — только со ссылкой на SSOT;
5. атомарные ссылки `[ДОК, §X «Заголовок», с.Y](url)` указывают на runtime-БЗ на
   зафиксированном commit; если runtime на этом commit доступен локально
   (`MANGO_BA_RUNTIME_MAIN`), § / заголовок / страницы сверяются с frontmatter;
6. ссылки `[ТЗ-тендеров-v4, п/п X, с.Y](url)` указывают на существующий пункт шаблона и его
   страницу (`experiments/issue_367/tender_index.json`) и на вложение шаблона из issue #484;
   веб-ссылки — только на домены Mango Office;
7. число сносок `[n]` обоснования равно числу цитат `[n] «…»` в каждой строке;
8. каталог прогона содержит обязательные файлы, контрольные суммы исходника и шаблона
   зафиксированы в `inputs/README.md`, исходники в `inputs/` не хранятся (только `*.md`);
9. аналитическая записка со сравнением версий ТЗ присутствует и ссылается на обе версии.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "runs/2026/RUN-0094"
REPORT = RUN / "outputs/L0-feasibility-assessment-1199-2.md"
NOTE = RUN / "outputs/analytical-note-1199-v1-vs-v2.md"
SOURCE = ROOT / "experiments/issue_484/source_transcription.json"
TENDER = ROOT / "experiments/issue_367/tender_index.json"
TENDER_SHA = "612e5e0938b9d4edad8e341f7fb03ba8498f7ec12dea0fe88f71e6817169d4cc"
TENDER_URL = "https://github.com/user-attachments/files/34787757/-.-v4.pdf"
V1_SHA = "4806288a13f03b4e972b726e92e267c4c627cab42ad4ade3929607c0fd4287ba"
# Листы исходника с требованиями; скрытый «Лист1» — словари выпадающих списков.
SHEETS = ("Требования к системе", "SLA")
RUN_FILES = (
    "metadata.yaml",
    "inputs/README.md",
    "inputs/task-statement-486.md",
    "outputs/README.md",
    "outputs/L0-feasibility-assessment-1199-2.md",
    "outputs/analytical-note-1199-v1-vs-v2.md",
    "logs/experiment-log.md",
    "logs/technical-audit.md",
    "feedback/review-notes.md",
)
# Эскалация в интернет разрешена только на домены Манго Офис.
ALLOWED_HOSTS = ("github.com", "www.mango-office.ru", "mango-office.ru")

VERDICT = re.compile(r"^Оценка: <br>(Да|Частично|Нет|) \\\| (.*?) ?\\\|$")
AUDIT = "Аудит: "
COLUMNS = ("№ пп", "№", "Требование", "Оценка", "Обоснование и ссылка",
           "Цитата источника и технический аудит", "Комментарий БА")
NO_DATA = "Нет данных"
OUT = "вне функционального контура"
CITATION = re.compile(
    r"\[([^\[\]]+?), (?:§([^\[\]«]+?) )?«((?:[^«»]|«[^«»]*»)*)», с\.([^\[\]]+?)\]\(([^()]+)\)"
)
TENDER_CITATION = re.compile(r"\[ТЗ-тендеров-v4, (?:п/п ([0-9.]+)|«[^«»]+»), с\.(\d+)\]\(([^()]+)\)")
BLOB = re.compile(r"^https://github\.com/G-Ivan-A/mango-ba-ai-runtime/blob/([0-9a-f]{40})/(docs/kb/.+\.md)$")
BLOCK = re.compile(r"^### Лист (\d+) из (\d+): «(.+)»$")
URL = re.compile(r"\]\((https?://[^()\s]+)\)")
FOOTNOTE = re.compile(r"\[(\d+)\] \[")
QUOTE = re.compile(r"\[(\d+)\] «")


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


def expected_rows(source: dict, sheet: str) -> list[tuple[str, str]]:
    """[(№, видимый текст требования)] листа исходника — строки без значений пропускаются."""
    data = next(s for s in source["sheets"] if s["title"] == sheet)
    rows = []
    for row in data["rows"]:
        values = row[1:]
        if not any(values):
            continue
        text = values[1] if len(values) > 1 else ""
        tail = values[2] if sheet == "SLA" and len(values) > 2 else ""
        rows.append((values[0], "\n".join(t for t in (text, tail) if t)))
    return rows


def frontmatter(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines()[1:]:
        if line.strip() == "---":
            break
        if ":" in line and not line.startswith((" ", "-")):
            key, _, value = line.partition(":")
            value = value.strip()
            if len(value) > 1 and value[0] == value[-1] and value[0] in "\"'":
                value = value[1:-1]  # только внешняя пара кавычек YAML-скаляра
            data[key.strip()] = value
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
        # Описания (README, постановка задачи) — markdown; исходники Заказчика не хранятся.
        stored = [p.name for p in inputs.iterdir() if p.suffix != ".md"]
        if stored:
            errors.append("в inputs/ хранятся исходные файлы: %s" % ", ".join(sorted(stored)))
        readme = (inputs / "README.md").read_text(encoding="utf-8") if (inputs / "README.md").exists() else ""
        for digest in (source["source"]["sha256"], TENDER_SHA, V1_SHA):
            if digest not in readme:
                errors.append("inputs/README.md: не зафиксирована контрольная сумма %s" % digest)


def check_note(errors: list[str]) -> None:
    """Аналитическая записка: сравнение новой версии ТЗ с предыдущей (RUN-0065)."""
    if not NOTE.exists():
        errors.append("нет аналитической записки: %s" % NOTE.relative_to(ROOT))
        return
    text = NOTE.read_text(encoding="utf-8")
    for needle in ("RUN-0065", "SoC_внешний 29-10.xlsx", V1_SHA):
        if needle not in text:
            errors.append("аналитическая записка: нет упоминания %r" % needle)
    for url in URL.findall(text):
        host = urlsplit(url).hostname or ""
        if host not in ALLOWED_HOSTS:
            errors.append("аналитическая записка: ссылка вне разрешённых доменов: %s" % url)


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
                                 ("страницы", pages, meta.get("pages", "")),
                                 ("документ", doc, meta.get("doc_code", ""))):
            if got != want:
                errors.append("%s: %s в ссылке %r, во frontmatter %r" % (match.group(2), label, got, want))

    tender = json.loads(TENDER.read_text(encoding="utf-8"))
    for item, page, href in TENDER_CITATION.findall(text):
        citations += 1
        if href != TENDER_URL:
            errors.append("ссылка на шаблон v4 не на вложение issue #484: %s" % href)
        if not item:
            if page != "5":
                errors.append("раздел общих требований шаблона v4 — с.5, в ссылке с.%s" % page)
            continue
        key = item if item in tender else item.rsplit(".", 1)[0]
        if key not in tender or (key != item and item not in tender[key][1]):
            errors.append("ссылка на несуществующий п/п шаблона ТЗ-тендеров-v4: %s" % item)
        elif str(tender[key][0]) != page:
            errors.append("п/п %s шаблона: страница %s в ссылке, в шаблоне %s" % (item, page, tender[key][0]))

    for url in URL.findall(text):
        host = urlsplit(url).hostname or ""
        if host not in ALLOWED_HOSTS:
            errors.append("ссылка вне разрешённых доменов (SSOT и домены Mango Office): %s" % url)
    return citations


def main() -> int:
    errors: list[str] = []
    if not REPORT.exists():
        print("FAIL: отчёт не найден: %s" % REPORT.relative_to(ROOT))
        return 1

    text = REPORT.read_text(encoding="utf-8")
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    found = blocks(text)
    heads = [BLOCK.match(head).group(1, 2) for head, _ in found]
    if heads != [("1", "2"), ("2", "2")]:
        errors.append("разделители листов %r, ожидаются «Лист 1 из 2», «Лист 2 из 2»" % heads)
    total = 0
    counts = {"Да": 0, "Частично": 0, "Нет": 0, "": 0}
    for index, (_head, table) in enumerate(found):
        sheet = SHEETS[index] if index < len(SHEETS) else "?"
        name = "Лист %d" % (index + 1)
        if not table or split_row(table[0]) != list(COLUMNS):
            errors.append("%s: шапка таблицы %r, ожидается %r"
                          % (name, split_row(table[0]) if table else None, list(COLUMNS)))
        for offset, line in enumerate(table, start=1):
            if len(split_row(line)) != len(COLUMNS):
                errors.append("%s: строка таблицы %d: колонок %d, ожидается %d"
                              % (name, offset, len(split_row(line)), len(COLUMNS)))
        rows = [split_row(line) for line in table[2:]]
        expected = expected_rows(source, sheet) if sheet in SHEETS else []
        total += len(rows)
        if len(rows) < len(expected):
            errors.append("%s: строк отчёта %d, непустых строк исходника %d"
                          % (name, len(rows), len(expected)))
        for position, cells in enumerate(rows, start=1):
            if len(cells) != len(COLUMNS):
                continue
            where = "%s строка %d (№ пп %s)" % (name, position, cells[0] or "—")
            cells = [cell.strip() for cell in cells[2:]]
            match = VERDICT.match(cells[1])
            if not match:
                errors.append("%s: колонка «Оценка» не по формату/шкале: %r" % (where, cells[1]))
                continue
            verdict = match.group(1)
            counts[verdict] += 1
            if match.group(2):
                errors.append("%s: средняя часть колонки «Оценка» должна быть пустой: %r" % (where, match.group(2)))
            if not cells[2] or not cells[3]:
                errors.append("%s: пустое обоснование или цитата" % where)
            if AUDIT not in cells[3]:
                errors.append("%s: в колонке цитат нет технического аудита" % where)
            if cells[4]:
                errors.append("%s: колонка «Комментарий БА» должна быть пустой" % where)
            if verdict == "Нет" and NO_DATA in cells[2] and not cells[3].startswith(NO_DATA):
                errors.append("%s: «Нет данных» в обосновании, но не в колонке цитат" % where)
            if not verdict and OUT not in cells[2]:
                errors.append("%s: пустая оценка без «вне функционального контура»" % where)
            if cells[3].startswith(NO_DATA) and verdict != "Нет":
                errors.append("%s: «Нет данных» при оценке %r" % (where, verdict))
            if cells[3].lower().startswith(OUT) and verdict:
                errors.append("%s: «вне функционального контура» при оценке %r" % (where, verdict))
            if verdict in ("Да", "Частично") and "](" not in cells[2]:
                errors.append("%s: оценка %r без ссылки на SSOT" % (where, verdict))
            if "Не требует обоснования" in cells[2] and "[ТЗ-тендеров-v4, " not in cells[2]:
                errors.append("%s: «Не требует обоснования» без ссылки на п/п шаблона v4" % where)
            if cells[2].startswith("Не требует обоснования") and verdict != "Да":
                errors.append("%s: «Не требует обоснования» для строки целиком при оценке %r" % (where, verdict))
            notes = [int(n) for n in FOOTNOTE.findall(cells[2])]
            quotes = [int(n) for n in QUOTE.findall(cells[3])]
            if notes != list(range(1, len(notes) + 1)) or notes != quotes:
                errors.append("%s: сноски обоснования %r не соответствуют цитатам %r"
                              % (where, notes, quotes))

    citations = check_citations(text, errors)
    if not citations:
        errors.append("в отчёте нет ни одной атомарной ссылки на SSOT")
    check_note(errors)
    check_run(source, errors)

    if errors:
        print("FAIL: validate_issue_484_run: найдено проблем: %d" % len(errors))
        for error in errors[:40]:
            print("  - %s" % error)
        return 1

    summary = ", ".join("%s %d" % (k or "пусто", v) for k, v in counts.items())
    print("OK: validate_issue_484_run: листов %d, строк отчёта %d (%s), ссылок на БЗ и шаблон v4 %d, колонок 7"
          % (len(found), total, summary, citations))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
