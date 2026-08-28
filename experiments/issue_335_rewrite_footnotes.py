#!/usr/bin/env python3
"""Дополнение таблиц «Источники» отчёта L4 колонками читаемости (issue #335).

К каждой сноске добавляются две колонки:

* **Где смотреть** — путь навигации от якоря до описанного объекта с
  отображаемым заголовком (`title`), который человек реально видит в Redoc.
* **Цитата из спецификации** — путь в спецификации (`components.schemas.X` или
  `paths./x.get`) с номером строки в спецификации, закреплённой по SHA-256.

Скрипт идемпотентен: повторный запуск не меняет уже расширенные таблицы.

Запуск:
    python3 experiments/issue_335_footnote_audit.py --spec /tmp/hh-openapi.yaml \
        --json /tmp/audit.json
    python3 experiments/issue_335_rewrite_footnotes.py --audit /tmp/audit.json \
        --spec /tmp/hh-openapi.yaml
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import issue_335_footnote_audit as audit

EXTRA_HEADER = " Где смотреть | Цитата из спецификации |"
EXTRA_SEPARATOR = " --- | --- |"


def navigation(row: dict) -> str:
    section = row["doc_section"].split(" / ")[0]
    steps = [f"раздел «{section}»"]
    operation = row.get("anchor_operation")
    heading = row.get("anchor_heading")
    if operation:
        steps.append(f"операция `{operation}`")
    elif heading:
        steps.append(f"секция «{heading}»")
    titles = [title for title in (row.get("schema_titles") or {}).values() if title]
    if titles:
        if "schema-only-footnote" in row["problems"]:
            steps.append("блок **Callbacks** → `onData`")
        steps.append("блок «" + "», «".join(sorted(set(titles))) + "»")
    return " → ".join(steps)


def citation(row: dict, spec: dict) -> str:
    parts: list[str] = []
    for name in sorted(row.get("schema_titles") or {}):
        item = spec["schemas"].get(name)
        if item:
            parts.append(f"`components.schemas.{name}` (стр. {item['line']})")
    if not parts:
        for operation_id in row["tokens"]["operations"]:
            item = spec["operations"].get(operation_id)
            if item:
                parts.append(
                    f"`paths.{item['path']}.{item['method'].lower()}` (стр. {item['line']})"
                )
    return "; ".join(parts) if parts else "—"


def rewrite(report_text: str, data: dict, spec: dict) -> str:
    by_position = {(row["line"], row["marker"]): row for row in data["rows"]}
    lines = report_text.splitlines()
    output: list[str] = []
    in_sources = False

    for number, line in enumerate(lines, start=1):
        if audit._SECTION.match(line):
            in_sources = True
        elif line.startswith("## "):
            in_sources = False

        if in_sources and line.startswith("| Сноска | Раздел документации |"):
            output.append(line.rstrip() + EXTRA_HEADER if not line.rstrip().endswith(
                "Цитата из спецификации |") else line)
            continue
        if in_sources and set(line.replace("|", "").replace("-", "").strip()) == set():
            if line.strip().startswith("|") and "---" in line:
                output.append(line.rstrip() + EXTRA_SEPARATOR)
                continue
        row = by_position.get((number, line.split("|")[1].strip().strip("`").lstrip("^")
                               if line.startswith("| `^") else None))
        if row is not None:
            output.append(line.rstrip() + f" {navigation(row)} | {citation(row, spec)} |")
            continue
        output.append(line)
    return "\n".join(output) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit", default="/tmp/audit.json")
    parser.add_argument("--spec", default="/tmp/hh-openapi.yaml")
    parser.add_argument("--report", default="runs/2026/RUN-0060/outputs/L4-combined-gap-report.md")
    args = parser.parse_args()

    data = json.loads(Path(args.audit).read_text(encoding="utf-8"))
    spec = audit.build_index(Path(args.spec).read_text(encoding="utf-8"))
    report = Path(args.report)
    text = report.read_text(encoding="utf-8")
    if "Цитата из спецификации" in text:
        print("таблицы уже расширены, изменений нет")
        return 0
    report.write_text(rewrite(text, data, spec), encoding="utf-8")
    print(f"обновлено: {report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
