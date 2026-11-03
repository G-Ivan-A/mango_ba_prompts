#!/usr/bin/env python3
"""BL-153 (issue #430): ID операций C01…C39 → К-01…К-39, поле flow_step.

Одноразовое преобразование, сохранено для воспроизводимости. Меняет только
действующие носители ID операций; коды ошибок C01…C25 в уроках, прогонах,
промптах и исторических анализах/RFC не трогает (глоссарий потока, раздел 5).

Запуск: python3 experiments/issue_430/rename_operations.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "standards/bcreq-manual-classes/catalog.json"
OP = re.compile(r"\bC(\d\d)\b")
K = "К"  # U+041A

# RFC #427, раздел 9.2: операция → шаг потока.
FLOW = {
    "Ш-0": "C36 C34 C13",
    "Ш-1": "C01 C02 C03 C04 C09 C14 C15",
    "Ш-2": "C05 C06 C07 C08 C11",
    "Ш-3": "C16 C17",
    "Ш-4": "C18",
    "Ш-5": "C19",
    "Ш-6": "C21 C22",
    "Ш-7": "C23",
    "Ш-8": "C24",
    "Ш-9": "C25 C26 C27",
    "Ш-В": "C28 C10 C29 C30 C20 C39",
    "Ш-Р": "C31 C32 C33 C35 C12",
    "Ш-С": "C37 C38",
}
STEP_OF = {op: step for step, ops in FLOW.items() for op in ops.split()}
assert sorted(STEP_OF) == [f"C{n:02d}" for n in range(1, 40)], "9.2 покрывает не все операции"

# Файлы, где C-NN — только ID операций (проверено вручную, issue #430).
TEXT_FILES = [
    "standards/bcreq-manual-classes/README.md",
    "docs/contracts/bcreq-manual-state.md",
    "docs/ba-processes/bcreq-manual-process.md",
    *[p.relative_to(ROOT).as_posix() for p in sorted((ROOT / "standards/bcreq-manual-classes").glob("[0-9][0-9]-*.md"))],
]


def rename(text):
    return OP.sub(lambda m: f"{K}-{m.group(1)}", text)


def main():
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    if data["classes"][0]["id"].startswith(K):
        raise SystemExit("каталог уже переименован")
    classes = []
    for item in data["classes"]:
        old = item["id"]
        new = {"id": f"{K}-{old[1:]}"}
        for key, value in item.items():
            if key == "id":
                continue
            new[key] = rename(value) if isinstance(value, str) else value
            if key == "phases":
                new["flow_step"] = STEP_OF[old]
        new["history"] = {"previous_id": old, "renamed_in": "BL-153 (issue #430)"}
        classes.append(new)
    out = {
        "version": "0.2",
        "id_prefix": f"{K}-",
        "flow_step_source": "docs/rfc/2026-11-bcreq-flow-processes-prompts.md#92-состав",
        "phases": data["phases"],
        "classes": classes,
    }
    CATALOG.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for rel in TEXT_FILES:
        path = ROOT / rel
        path.write_text(rename(path.read_text(encoding="utf-8")), encoding="utf-8")
    print(f"classes={len(classes)} files={len(TEXT_FILES)}")


if __name__ == "__main__":
    main()
