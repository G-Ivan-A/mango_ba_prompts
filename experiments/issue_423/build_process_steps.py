#!/usr/bin/env python3
"""Issue #423: rebuild Part 1.2/1.3 of docs/ba-processes/bcreq-manual-process.md
for the 39 manual BCREQ classes (PR #422).

Source data is read-only: standards/bcreq-manual-classes/catalog.json (inputs,
outputs, stop, checks, phases) and the "Последовательности экземпляров" tables
of standards/bcreq-manual-classes/README.md (order of instances per stage).
Only the process document is written. Run with --check to verify the document
is in sync without writing.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLASSES = ROOT / "standards/bcreq-manual-classes"
DOC = ROOT / "docs/ba-processes/bcreq-manual-process.md"
REPO = "https://github.com/G-Ivan-A/mango_ba_prompts/blob/main"

STAGES = [
    ("a-in", "A-IN", "Г-IN", "БА"),
    ("a-core", "A-CORE", "Г-С1 «Согласование 1»", "Заказчик"),
    ("a-work", "A-WORK", "Г-W", "ПО продукта, архитектор продукта, руководитель КК"),
    ("a-release", "A-RELEASE", "выпуск", "по процессу A-RELEASE"),
]

# Conditions of the README note under the sequences («C16/C17 — альтернативы…»).
CONDITIONS = {
    "C07": "по доступности источника: web",
    "C08": "по доступности источника: PDF и runtime",
    "C09": "по доступности источника: материалы БА",
    "C16": "альтернатива C17: `delta` по решению БА",
    "C17": "альтернатива C16: `new` только по явному решению БА",
    "C22": "по уровню: `L1+L2`",
    "C28": "отдельный чат с ролью критика",
    "C29": "только при изменении кандидата",
    "C30": "только при изменении кандидата",
    "C34": "после фактической реплики человека",
    "C37": "только по запросу БА",
    "C38": "только по запросу БА",
}

GATE = {
    "C20": "Предложение гейта стадии: Г-IN (A-IN) — решает БА; Г-С1 (A-CORE) — решает Заказчик; "
    "Г-W (A-WORK) — решают ПО продукта, архитектор продукта, руководитель КК",
    "C33": "Выпуск — решает человек; C35 фиксирует baseline",
}


def sequences() -> dict[str, list[str]]:
    text = (CLASSES / "README.md").read_text(encoding="utf-8")
    result: dict[str, list[str]] = {}
    for phase, *_ in STAGES:
        block = re.search(rf"^### {phase}\n(.*?)(?=^### |^C16/C17|\Z)", text, re.S | re.M)
        if not block:
            raise SystemExit(f"README: нет последовательности {phase}")
        result[phase] = re.findall(rf"^\| {phase}/(C\d\d) \|", block.group(1), re.M)
    return result


def soft(value: str) -> str:
    """Keep catalog text, but make it one list item (the site splits on '; ')."""
    return value.strip().rstrip(".").replace("; ", ", ").replace("|", "\\|")


def build() -> tuple[str, str]:
    catalog = json.loads((CLASSES / "catalog.json").read_text(encoding="utf-8"))
    classes = {item["id"]: item for item in catalog["classes"]}
    seq = sequences()
    order: list[str] = []
    for phase, *_ in STAGES:
        for class_id in seq[phase]:
            if class_id not in order:
                order.append(class_id)
    if sorted(order) != sorted(classes):
        raise SystemExit(f"последовательности не покрывают 39 классов: {sorted(set(classes) - set(order))}")
    number = {class_id: index + 1 for index, class_id in enumerate(order)}
    stage_label = {phase: label for phase, label, *_ in STAGES}

    rows = [
        "| № | Шаг | Стадия | Промпт | Параметры | Что подготовить | Что делает БА | Результат | Гейт после шага |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for class_id in order:
        item = classes[class_id]
        stages = ", ".join(stage_label[phase] for phase in item["phases"])
        stem = item["file"].removesuffix(".md")
        link = f"[{class_id} {item['slug']}]({REPO}/standards/bcreq-manual-classes/{item['file']})"
        params = [f"`class: {class_id}`", f"`phase: {' / '.join(item['phases'])}`"]
        if class_id == "C36":
            params.append("`input_mode: START` (новый чат — `CONTINUE`)")
        else:
            params.append("`input_mode: CONTINUE`")
        if class_id in CONDITIONS:
            params.append(CONDITIONS[class_id])
        actions = [
            f"Скопировать промпт {class_id} кнопкой ⧉ вместе с контрактом состояния и правилами из C36",
            f"заполнить блок входа: {soft(item['inputs'])}",
            f"если {soft(item['stop'])[0].lower()}{soft(item['stop'])[1:]}",
            f"проверить: {soft(item['checks'])[0].lower()}{soft(item['checks'])[1:]}",
            "сохранить блок BCREQ_OUTPUT и решить, какой класс запустить следующим",
        ]
        rows.append(
            "| "
            + " | ".join(
                [
                    str(number[class_id]),
                    f"Ш-{number[class_id]} {item['name']}",
                    stages,
                    link,
                    "; ".join(params),
                    f"`{item['inputs']}`",
                    "; ".join(actions),
                    f"`{item['outputs']}`",
                    GATE.get(class_id, "—"),
                ]
            )
            + " |"
        )
    steps = "\n".join(rows)

    seq_rows = [
        "| Стадия | Порядок промптов | Гейт стадии | Кто решает |",
        "| --- | --- | --- | --- |",
    ]
    for phase, label, gate, who in STAGES:
        chain = " → ".join(seq[phase])
        seq_rows.append(f"| {label} | {chain} | {gate} | {who} |")
    return steps, "\n".join(seq_rows)


def render(doc: str) -> str:
    steps, seq = build()
    doc = re.sub(
        r"(### 1\.2\. Шаги\n\n.*?\n\n)(\| № \| Шаг \|.*?)(\n\n)",
        lambda m: m.group(1) + steps + m.group(3),
        doc,
        count=1,
        flags=re.S,
    )
    doc = re.sub(
        r"(### 1\.3\. Последовательность по стадиям\n\n.*?\n\n)(\| Стадия \| Порядок промптов \|.*?)(\n\n)",
        lambda m: m.group(1) + seq + m.group(3),
        doc,
        count=1,
        flags=re.S,
    )
    return doc


def main() -> int:
    current = DOC.read_text(encoding="utf-8")
    updated = render(current)
    if "--check" in sys.argv:
        if updated != current:
            print(f"{DOC.relative_to(ROOT)}: шаги не совпадают с catalog.json/README — запустите {Path(__file__).name}")
            return 1
        print("bcreq-manual-process steps: in sync")
        return 0
    DOC.write_text(updated, encoding="utf-8")
    print(f"updated {DOC.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
