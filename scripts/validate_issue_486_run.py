#!/usr/bin/env python3
"""Валидация формы отчёта RUN-0094 v2.0 (issue #486, доработка RUN-0094 issue #484).

Содержательные правила оценки issue #484 (шкала, «Нет данных», «вне функционального контура»,
правило > 90 %, сноски и цитаты, ссылки на SSOT, файлы прогона) проверяет
`scripts/validate_issue_484_run.py`. Здесь — форма issue #486 независимо от генератора
(эталон — транскрипция исходника `experiments/issue_484/source_transcription.json`):

1. колонка «№ пп» — сквозной порядковый номер строки отчёта 1…N по обоим листам, без пропусков
   и повторов;
2. строки отчёта идут группами по строкам исходника в порядке исходника: колонка «Требование»
   каждой строки — дословная подстрока ячейки исходника (переводы строк — `<br>`), фрагменты
   группы идут в порядке текста без перекрытий и вместе покрывают ячейку целиком (с точностью
   до пробельных символов); пропуски, добавления и перестановки — ошибка;
3. колонка «№» каждой строки группы равна литеральному значению «№» строки исходника
   (значение повторяется — дубликаты допустимы);
4. строка исходника с заголовком (шапка таблицы, название раздела, подписи Таблицы 1) — одна
   строка отчёта с пустой оценкой;
5. строка исходника с несколькими требованиями разложена: ни одна строка отчёта не содержит
   больше одного пункта перечня `-` и больше одной строки Таблицы 1 листа SLA; обобщающая
   вводная фраза перечня — отдельная строка;
6. заголовок комплексного требования (пустая оценка, «Заголовок комплексного требования»)
   ссылается на непрерывный диапазон «№ пп», который начинается со следующей строки и
   состоит из строк той же строки исходника (и строк-продолжений объединённой ячейки);
7. строки отчёта совпадают с декомпозицией `experiments/issue_486/fragments.json`, итог
   «всего — N строк отчёта» и метрики `metadata.yaml` (число строк, заголовков комплексных
   требований и вердиктов) согласованы с таблицей, frontmatter
   отчёта — версия 2.0 со ссылкой на issue #486.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import validate_issue_484_run as v484  # noqa: E402

RUN = ROOT / "runs/2026/RUN-0094"
REPORT = v484.REPORT
SOURCE = v484.SOURCE
FRAGMENTS = ROOT / "experiments/issue_486/fragments.json"
SHEETS = v484.SHEETS
HEADINGS = ("Требования к системе!1", "SLA!1", "SLA!17", "SLA!18")
TABLE = tuple(f"SLA!{n}" for n in range(19, 27))
LEAD = "Заголовок комплексного требования"
SPAN = re.compile(r"строках № пп (\d+)(?:–(\d+))?")
BULLET = re.compile(r"(?:^|\n)\s*[-–—•]\s")
ISSUE = "https://github.com/G-Ivan-A/mango_ba_prompts/issues/486"


def squash(text: str) -> str:
    return re.sub(r"\s+", "", text)


def source_rows(source: dict) -> list[tuple[str, int, str, str, bool]]:
    """[(лист, строка XLSX, №, ячейка «Требование», продолжение объединённой ячейки)]."""
    out = []
    for sheet in SHEETS:
        data = next(s for s in source["sheets"] if s["title"] == sheet)
        for row in data["rows"]:
            ri, values = row[0], row[1:]
            if not any(values):
                continue
            text = values[1] if len(values) > 1 else ""
            tail = values[2] if sheet == "SLA" and len(values) > 2 else ""
            out.append((sheet, ri, values[0], "\n".join(t for t in (text, tail) if t),
                        not values[0] and not text))
    return out


def report_rows(text: str, errors: list[str]) -> list[dict]:
    rows = []
    for index, (_head, table) in enumerate(v484.blocks(text)):
        for line in table[2:]:
            cells = [c.strip() for c in v484.split_row(line)]
            if len(cells) != 7:
                errors.append("строка отчёта: колонок %d, ожидается 7: %s" % (len(cells), line[:60]))
                continue
            match = v484.VERDICT.match(cells[3])
            rows.append({"sheet": SHEETS[index] if index < len(SHEETS) else "?",
                         "pp": cells[0], "num": cells[1].replace("\\|", "|"),
                         "text": cells[2].replace("\\|", "|").replace("<br>", "\n"),
                         "verdict": match.group(1) if match else None, "why": cells[4]})
    return rows


def match_groups(rows: list[dict], source: dict, errors: list[str]) -> None:
    """Пп. 2–5: жадное сопоставление строк отчёта ячейкам исходника."""
    i = 0
    for sheet, ri, num, cell, cont in source_rows(source):
        rid = f"{sheet}!{ri}"
        where = f"{sheet}, строка XLSX {ri} (№ {num or '—'})"
        target, pos, acc, group = squash(cell), 0, "", []
        while i < len(rows) and len(acc) < len(target):
            row = rows[i]
            if row["sheet"] != sheet:
                break
            frag = row["text"]
            found = cell.find(frag, pos) if frag else -1
            if found < 0 or cell[pos:found].strip():
                errors.append(f"{where}: № пп {row['pp']} — не дословный фрагмент ячейки в порядке "
                              f"текста: {frag[:60]!r}")
                return
            pos, acc = found + len(frag), acc + squash(frag)
            group.append(row)
            i += 1
        if acc != target:
            errors.append(f"{where}: фрагменты не покрывают ячейку исходника целиком")
            return
        for row in group:
            row["rid"], row["cont"] = rid, cont
            if row["num"] != num:
                errors.append(f"№ пп {row['pp']}: «№» {row['num']!r}, в исходнике {num!r}")
        if rid in HEADINGS:
            if len(group) != 1:
                errors.append(f"{where}: строка-заголовок разложена на {len(group)} строк")
            elif group[0]["verdict"] != "":
                errors.append(f"{where}: строка-заголовок с оценкой {group[0]['verdict']!r}")
            continue
        for row in group:
            if len(BULLET.findall("\n" + row["text"])) > 1 or (
                    BULLET.search(row["text"][1:]) and not row["text"].lstrip().startswith("-")):
                errors.append(f"№ пп {row['pp']}: несколько пунктов перечня в одной строке")
            if rid in TABLE and "\n" in row["text"]:
                errors.append(f"№ пп {row['pp']}: несколько строк Таблицы 1 в одной строке отчёта")
    if i != len(rows):
        errors.append(f"строки отчёта без строки исходника: с № пп {rows[i]['pp']}")


def check_leads(rows: list[dict], errors: list[str]) -> int:
    """П. 6: заголовок комплексного требования ссылается на свои атомарные строки."""
    leads = 0
    for k, row in enumerate(rows):
        if LEAD not in row["why"]:
            continue
        leads += 1
        span = SPAN.search(row["why"])
        if row["verdict"] != "" or not span:
            errors.append(f"№ пп {row['pp']}: заголовок комплексного требования с оценкой "
                          f"{row['verdict']!r} или без диапазона «№ пп»")
            continue
        start, end = int(span.group(1)), int(span.group(2) or span.group(1))
        if start != k + 2 or end > len(rows) or end < start:
            errors.append(f"№ пп {row['pp']}: диапазон {start}–{end} не начинается со следующей строки")
            continue
        for sub in rows[start - 1:end]:
            if sub.get("rid") != row.get("rid") and not sub.get("cont"):
                errors.append(f"№ пп {row['pp']}: строка № пп {sub['pp']} диапазона — из другой "
                              f"строки исходника")
            if LEAD in sub["why"]:
                errors.append(f"№ пп {row['pp']}: в диапазон входит другой заголовок № пп {sub['pp']}")
        nxt = rows[end] if end < len(rows) else None
        if nxt and nxt.get("rid") == row.get("rid"):
            errors.append(f"№ пп {row['pp']}: диапазон не включает строку № пп {nxt['pp']}")
    return leads


def main() -> int:
    errors: list[str] = []
    if not REPORT.exists():
        print("FAIL: отчёт не найден: %s" % REPORT.relative_to(ROOT))
        return 1
    text = REPORT.read_text(encoding="utf-8")
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    rows = report_rows(text, errors)
    pps = [r["pp"] for r in rows]
    if pps != [str(n) for n in range(1, len(rows) + 1)]:
        bad = next((p for n, p in enumerate(pps, start=1) if p != str(n)), None)
        errors.append(f"«№ пп» не сквозной 1…{len(rows)}: первое расхождение {bad!r}")
    match_groups(rows, source, errors)
    leads = check_leads(rows, errors)

    frags = json.loads(FRAGMENTS.read_text(encoding="utf-8"))
    if [f["text"] for f in frags] != [r["text"] for r in rows]:
        errors.append("строки отчёта расходятся с декомпозицией experiments/issue_486/fragments.json")
    else:
        for f, r in zip(frags, rows):
            if (f["kind"] == "lead") != (LEAD in r["why"]):
                errors.append(f"№ пп {r['pp']}: вид строки {f['kind']!r} не совпадает с отчётом")

    meta = v484.frontmatter(REPORT)
    if meta.get("version") != "2.0" or ISSUE not in text.split("\n---", 1)[0]:
        errors.append("frontmatter отчёта: ожидается version 2.0 и ссылка на issue #486")
    total = re.search(r"^- всего — (\d+) строк", text, re.M)
    if not total or int(total.group(1)) != len(rows):
        errors.append(f"итог «всего — N строк» не равен числу строк таблицы {len(rows)}")
    metadata = (RUN / "metadata.yaml").read_text(encoding="utf-8")
    counts = {"report_rows": len(rows), "complex_headings": leads,
              "verdicts_yes": sum(r["verdict"] == "Да" for r in rows),
              "verdicts_partial": sum(r["verdict"] == "Частично" for r in rows),
              "verdicts_no": sum(r["verdict"] == "Нет" for r in rows),
              "verdicts_no_data": sum(r["verdict"] == "Нет" and "Нет данных" in r["why"] for r in rows),
              "verdicts_empty": sum(r["verdict"] == "" for r in rows)}
    for key, value in counts.items():
        if not re.search(rf"^  {key}: {value}\b", metadata, re.M):
            errors.append(f"metadata.yaml: метрика {key} должна быть {value}")

    if errors:
        print("FAIL: validate_issue_486_run: найдено проблем: %d" % len(errors))
        for error in errors[:40]:
            print("  - %s" % error)
        return 1
    print("OK: validate_issue_486_run: строк отчёта %d (№ пп 1…%d) из %d строк исходника, "
          "заголовков комплексных требований %d" % (len(rows), len(rows), len(source_rows(source)), leads))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
