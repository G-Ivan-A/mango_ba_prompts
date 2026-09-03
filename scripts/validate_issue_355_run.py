#!/usr/bin/env python3
"""Validate the RUN-0067 rework of BCREQ-1074 requested by issue #355.

Checks that the reworked functional-requirements document follows the BCREQ-1025
template, keeps only the delta requirements, lists the eight export fields in the
mandated order, carries no analyst comments inside requirement bodies, and that
RUN-0063 is marked invalid and RUN-0067 is registered.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "runs/2026/RUN-0067"
DOC = RUN / "outputs/functional-requirements-bcreq-1074.md"
OLD_RUN = ROOT / "runs/2026/RUN-0063"

TEMPLATE_SECTIONS = [
    "## 1. Термины и определения",
    "## 2. Проблема, цель, задача",
    "## 3. Описание разрабатываемого решения",
    "## 4. Функциональные требования и сценарии использования",
    "## 5. Нефункциональные требования",
    "## 6. Особенности реализации",
    "## Вопросы владельцу продукта",
]

FIELDS = [
    "Дата/время звонка",
    "Номер, инициировавший звонок",
    "Номер абонента",
    "Название услуги",
    "Оператор связи",
    "Длительность звонка",
    "Сумма в рублях",
    "Номер договора",
]

# Аналитические комментарии не должны оставаться в теле требований — аудит
# прогона RUN-0063 требовал вынести их в раздел вопросов.
COMMENT_MARKERS = [
    "требует решения",
    "требует уточнения",
    "не утвержден",
    "требует проверки",
]

NOT_IMPLEMENTED = [
    "drag-and-drop",
    "видимости колонок",
    "фильтр",
    "ролевой модели",
    "нескольким ЛС",
]


def check(errors: list[str]) -> int:
    if not DOC.exists():
        errors.append(f"{DOC}: missing reworked requirements document")
        return 1
    text = DOC.read_text(encoding="utf-8")

    positions = []
    for heading in TEMPLATE_SECTIONS:
        index = text.find(f"\n{heading}\n")
        if index < 0:
            errors.append(f"{DOC}: missing template section {heading!r}")
        positions.append(index)
    ordered = [p for p in positions if p >= 0]
    if ordered != sorted(ordered):
        errors.append(f"{DOC}: template sections are out of order")

    requirements = re.findall(r"^### 4\.\d+\. Система должна .+$", text, re.M)
    if len(requirements) != 2:
        errors.append(
            f"{DOC}: expected exactly 2 «Система должна» requirements, found {len(requirements)}"
        )

    table = [m.strip() for m in re.findall(r"^\| \d \| (.+?) \|$", text, re.M)]
    if table != FIELDS:
        errors.append(f"{DOC}: export fields {table!r} differ from the mandated order {FIELDS!r}")

    body_end = text.find("\n## 5. Нефункциональные требования\n")
    body = text[:body_end] if body_end > 0 else text
    for marker in COMMENT_MARKERS:
        if marker in body.lower():
            errors.append(f"{DOC}: analyst comment {marker!r} left inside sections 1-4")

    constraints = text[text.find("\n### 6.1. Ограничения\n"):]
    for item in NOT_IMPLEMENTED:
        if item.lower() not in constraints.lower():
            errors.append(f"{DOC}: constraints do not state that {item!r} is out of scope")

    if "как текст" not in text:
        errors.append(f"{DOC}: phone numbers must be stated to be stored as text")
    if "до копеек" not in text:
        errors.append(f"{DOC}: amount must be stated to be exported with kopeck precision")
    for fmt in ("CSV", "XLSX"):
        if fmt not in text:
            errors.append(f"{DOC}: export format {fmt} is not specified")

    old_meta = (OLD_RUN / "metadata.yaml").read_text(encoding="utf-8")
    if "status: invalid" not in old_meta or "superseded_by: RUN-0067" not in old_meta:
        errors.append(f"{OLD_RUN}/metadata.yaml: RUN-0063 is not marked invalid/superseded")
    old_doc = (OLD_RUN / "outputs/functional-requirements-bcreq-1074.md").read_text(encoding="utf-8")
    if "status: invalid" not in old_doc or "Документ невалиден" not in old_doc:
        errors.append(f"{OLD_RUN}: invalid document lacks status and banner")

    registry = (ROOT / "runs/README.md").read_text(encoding="utf-8")
    if not re.search(r"^\| \[`RUN-0067`\]", registry, re.M):
        errors.append("runs/README.md: RUN-0067 registry row is missing")

    return 0


def main() -> int:
    errors: list[str] = []
    check(errors)
    if errors:
        print(f"FAIL: validate_issue_355_run: {len(errors)} problem(s)")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("OK: validate_issue_355_run: RUN-0067 rework matches issue #355 requirements")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
