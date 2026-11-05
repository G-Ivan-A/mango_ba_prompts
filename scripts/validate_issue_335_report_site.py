#!/usr/bin/env python3
"""Регрессионная проверка issue #335: стандарт артефактов и веб-отчёт RUN-0060.

Фиксирует три части задачи, чтобы последующие правки их не сломали:
- ADR-011: уровни детализации, обязательная структура L4, требование
  читаемости ссылок для Human Review, процесс запуска и quality gates;
- RFC таксономии задач: типы T1…T5 с профилем артефактов;
- индекс отчётов на сайте; сам веб-отчёт снят с публикации в issue #462;
- артефакты human review: чек-лист всех 53 сносок и документ методики.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ADR = "docs/adr/2026-08-adr-011-integration-task-artifacts.md"
RFC = "docs/rfc/2026-08-task-taxonomy.md"
ANALYSIS = "docs/analysis/2026-08-28-human-review-accessibility.md"
CHECKLIST = "runs/2026/RUN-0060/outputs/human-review-checklist.md"
INDEX = "site/reports/index.html"

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

    # --- часть 3: веб-представление снято с публикации (issue #462) -----------
    # Запрет публикации проверяет scripts/validate_issue_462_report_exclusion.py.
    errors += require(read(INDEX), INDEX, "Отчёты", '<script src="../gate.js" data-base="../"></script>')

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
