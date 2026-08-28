#!/usr/bin/env python3
"""Регрессионная проверка issue #335: стандарт артефактов и веб-отчёт RUN-0060.

Фиксирует три части задачи, чтобы последующие правки их не сломали:
- ADR-011: уровни детализации, обязательная структура L4, требование
  читаемости ссылок для Human Review, процесс запуска и quality gates;
- RFC таксономии задач: типы T1…T5 с профилем артефактов;
- веб-представление отчёта: индекс отчётов, парольная страница, отчёт с
  номером задачи 765, инлайновые SVG вместо Mermaid, кнопка копирования в
  Confluence, отсутствие пароля в открытом виде и внешних загрузок;
- артефакты human review: чек-лист всех 53 сносок и документ методики.
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ADR = "docs/adr/2026-08-adr-011-integration-task-artifacts.md"
RFC = "docs/rfc/2026-08-task-taxonomy.md"
ANALYSIS = "docs/analysis/2026-08-28-human-review-accessibility.md"
CHECKLIST = "runs/2026/RUN-0060/outputs/human-review-checklist.md"
REPORT = "site/reports/run-0060/detailed-gap-report.html"
GATE = "site/reports/run-0060/index.html"
INDEX = "site/reports/index.html"
HASHES = "site/password-hashes.json"

FOOTNOTES_TOTAL = 53


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def require(text: str, path: str, *needles: str) -> list[str]:
    return [f"{path}: нет фрагмента {needle!r}" for needle in needles if needle not in text]


def main() -> int:
    errors: list[str] = []

    # --- часть 1: ADR ---------------------------------------------------------
    adr = read(ADR)
    errors += require(
        adr, ADR,
        "L1", "L4", "Business Gap Summary", "Источники",
        "Human Review", "Чего этот прогон не делает",
        "Инкрементальность", "Quality gates", "Human Gate",
        "L4-combined-gap-report.md",
    )

    # --- часть 2: RFC ---------------------------------------------------------
    rfc = read(RFC)
    errors += require(rfc, RFC, "T1", "T2", "T3", "T4", "T5", "SSOT", "Quality gates")

    # --- комментарий к задаче: human review ссылок ----------------------------
    analysis = read(ANALYSIS)
    errors += require(analysis, ANALYSIS, "Тип A", "Тип B", "Тип C", "Тип D", "Правило 1")

    checklist = read(CHECKLIST)
    rows = [line for line in checklist.splitlines() if re.match(r"^\|\s*\d+\s*\|", line)]
    if len(rows) != FOOTNOTES_TOTAL:
        errors.append(f"{CHECKLIST}: строк проверки {len(rows)}, ожидалось {FOOTNOTES_TOTAL}")

    report_md = read("runs/2026/RUN-0060/outputs/L4-combined-gap-report.md")
    errors += require(report_md, "L4-combined-gap-report.md",
                      "Где смотреть", "Цитата из спецификации")

    # --- часть 3: веб-представление -------------------------------------------
    report = read(REPORT)
    gate = read(GATE)
    index = read(INDEX)
    hashes = json.loads(read(HASHES))

    errors += require(report, REPORT,
                      "765", "Интеграция КЦ Mango Office", "Актуализировано: 2026-08-27",
                      "Скопировать для Конфы", "История изменений",
                      "Сводный вердикт", "RUN-0056", "RUN-0058", "RUN-0059", "RUN-0060")
    if "```mermaid" in report or "<pre><code>graph" in report:
        errors.append(f"{REPORT}: диаграммы должны быть отрисованы в SVG, а не в виде кода")
    if report.count("<svg") < 11:
        errors.append(f"{REPORT}: инлайновых SVG {report.count('<svg')}, ожидалось не менее 11")
    for external in ("<script src=", "<link ", "cdn.jsdelivr", "unpkg.com"):
        if external in report:
            errors.append(f"{REPORT}: внешняя загрузка {external!r} ломает офлайн-копирование")

    errors += require(gate, GATE, "SHA-256", "localStorage", "detailed-gap-report.html")
    errors += require(index, INDEX, "run-0060/", "Отчёты")
    errors += require(read("site/index.html"), "site/index.html", "reports/index.html")

    entry = hashes.get("run-0060", {})
    if not re.fullmatch(r"[0-9a-f]{64}", entry.get("hash", "")):
        errors.append(f"{HASHES}: hash должен быть 64 hex-символами SHA-256")
    if not re.fullmatch(r"[0-9a-f]{16}", entry.get("salt", "")):
        errors.append(f"{HASHES}: salt должен быть 16 hex-символами")
    if set(entry) - {"algorithm", "salt", "hash"}:
        errors.append(f"{HASHES}: допустимы только поля algorithm, salt и hash — "
                      "сам пароль в репозитории не хранится")

    errors += require(read("CHANGELOG.md"), "CHANGELOG.md", "#335")

    if errors:
        print("issue-335 report-site validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("issue-335 report-site validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
