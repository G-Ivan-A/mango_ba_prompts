#!/usr/bin/env python3
"""Валидация артефакта прогона RUN-0066 (issue #351).

Проверяет отчёт `runs/2026/RUN-0066/outputs/L0-feasibility-assessment-1099-2.md`:

1. таблица результата содержит ровно 6 колонок в каждой строке;
2. колонка «Оценка» заполняется строго по шкале `Да / Частично / Нет / пусто`;
3. атомарные ссылки имеют вид `[ДОК, §X «Заголовок», с.Y](путь)`
   (без `§X`, если у раздела нет номера в исходном PDF);;
4. каждая ссылка ведёт на существующий раздел `kb/processed/**/sections/*.md`,
   а § и номера страниц совпадают с frontmatter этого раздела.

Пункт 4 закрывает корневую причину дефекта RUN-0065: там номера страниц были
захардкожены в генераторе и разъехались с базой знаний.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "runs/2026/RUN-0066/outputs/L0-feasibility-assessment-1099-2.md"

VERDICTS = {"Да", "Частично", "Нет", ""}
CITATION = re.compile(
    r"\[([^\[\]]+?), (?:§([^\[\]«]+?) )?«([^»]*)», с\.([^\[\]]+?)\]\(([^()]+)\)"
)


def split_row(line: str) -> list[str]:
    return [cell.strip() for cell in re.split(r"(?<!\\)\|", line.strip().strip("|"))]


def frontmatter(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    data: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" in line and not line.startswith((" ", "-")):
            key, _, value = line.partition(":")
            value = value.strip()
            if len(value) > 1 and value[0] == value[-1] and value[0] in "\"'":
                value = value[1:-1]
            data[key.strip()] = value
    return data


def main() -> int:
    errors: list[str] = []
    if not REPORT.exists():
        print("FAIL: отчёт не найден: %s" % REPORT.relative_to(ROOT))
        return 1

    text = REPORT.read_text(encoding="utf-8")
    table = [line for line in text.splitlines() if line.startswith("|")]
    if len(table) < 3:
        print("FAIL: таблица результата не найдена")
        return 1

    for offset, line in enumerate(table, start=1):
        cells = split_row(line)
        if len(cells) != 6:
            errors.append("строка таблицы %d: колонок %d, ожидается 6" % (offset, len(cells)))

    numbers: list[int] = []
    for offset, line in enumerate(table[2:], start=1):
        cells = split_row(line)
        if len(cells) != 6:
            continue
        num, _, _, verdict, reason, audit = cells
        if verdict not in VERDICTS:
            errors.append("строка %d: недопустимая оценка %r" % (offset, verdict))
        if num.isdigit():
            numbers.append(int(num))
            if not verdict:
                errors.append("строка %d: требование №%s осталось без оценки" % (offset, num))
            if not reason.strip() or not audit.strip():
                errors.append("строка %d: требование №%s без обоснования или аудита" % (offset, num))

    if numbers != list(range(1, len(numbers) + 1)):
        errors.append("нумерация требований не сплошная: %d значений, ожидался ряд 1..N" % len(numbers))

    citations = 0
    for doc, section, title, pages, href in CITATION.findall(text):
        section = section or ""
        citations += 1
        target = (REPORT.parent / href).resolve()
        try:
            rel = target.relative_to(ROOT)
        except ValueError:
            errors.append("ссылка ведёт за пределы репозитория: %s" % href)
            continue
        if not target.exists():
            errors.append("ссылка на несуществующий раздел: %s" % rel)
            continue
        meta = frontmatter(target)
        actual_section = meta.get("pdf_section", "")
        if actual_section in ("", "-", "—"):
            actual_section = meta.get("section", "")
        if actual_section in ("", "0", "-", "—"):
            actual_section = ""
        if actual_section != section:
            errors.append("%s: § в ссылке %r, во frontmatter %r" % (rel, section, actual_section))
        if meta.get("pages", "") != pages:
            errors.append("%s: страницы в ссылке %r, во frontmatter %r" % (rel, pages, meta.get("pages", "")))
        if title and meta.get("title", "") != title:
            errors.append("%s: заголовок в ссылке %r, во frontmatter %r" % (rel, title, meta.get("title", "")))
        if doc and meta.get("doc_code", "") != doc:
            errors.append("%s: код документа в ссылке %r, во frontmatter %r" % (rel, doc, meta.get("doc_code", "")))

    if not citations:
        errors.append("в отчёте нет ни одной атомарной ссылки на базу знаний")

    if errors:
        print("FAIL: validate_issue_351_run: найдено проблем: %d" % len(errors))
        for error in errors[:40]:
            print("  - %s" % error)
        if len(errors) > 40:
            print("  ... ещё %d" % (len(errors) - 40))
        return 1

    print("OK: validate_issue_351_run: строк требований %d, атомарных ссылок %d, колонок 6" % (len(numbers), citations))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
