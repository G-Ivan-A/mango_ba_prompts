#!/usr/bin/env python3
"""RUN-0079: подготовка слепой оценки по рубрике K1–K6 (issue #411).

Для каждого кейса два выхода (A и B) получают метки X/Y в случайном порядке
(seed 7979). Судья не знает, какая метка какой версии промпта соответствует.
Ключ хранится в judge-key.json и судье не передаётся.

Использование:
    python3 experiments/issue_411/run0079/judge_prepare.py WORKDIR
"""
from __future__ import annotations

import json
import random
import re
import sys
from pathlib import Path

from prepare import ROOT, load_validator

SEED = 7979
# Версия B ссылается на ID уроков из своего блока. Чтобы ссылка не выдавала
# версию судье, ID уроков в выходах маскируются (содержание нарушения
# сохраняется).
LESSON_REF_RE = re.compile(r"\(?\bL-\d+\b\)?[:,;]?\s*")
BATCHES = 2


def load_outputs(work: Path, version: str) -> dict:
    result = {}
    for path in sorted((work / "out").glob(f"{version}-batch*.json")):
        for item in json.loads(path.read_text(encoding="utf-8")):
            result[item["case"]] = item
    return result


def render(item: dict | None) -> str:
    if item is None:
        return "_(выход отсутствует)_"
    return "\n".join(
        f"- **{key}:** {LESSON_REF_RE.sub('', str(item.get(key, '')))}" for key in ("verdict", "violation", "quote", "fix")
    )


def main() -> int:
    work = Path(sys.argv[1]).resolve()
    (work / "judge").mkdir(exist_ok=True)
    meta = json.loads((work / "mapping.json").read_text(encoding="utf-8"))
    validator = load_validator()
    cases = {case["case-id"]: case for case in validator.golden_cases()}
    lessons = {lesson["id"]: lesson for lesson in json.loads((ROOT / "standards/bcreq-lessons/lessons.json").read_text(encoding="utf-8"))["lessons"]}
    outputs = {"A": load_outputs(work, "A"), "B": load_outputs(work, "B")}
    rng = random.Random(SEED)
    key = {}
    tids = sorted(meta["mapping"])
    size = (len(tids) + BATCHES - 1) // BATCHES
    for batch in range(BATCHES):
        lines = [f"# Слепая оценка, пакет {batch + 1}", ""]
        for tid in tids[batch * size:(batch + 1) * size]:
            case = cases[meta["mapping"][tid]]
            match = re.search(r"L-\d+", case["Урок"])
            lesson = lessons.get(match.group(0), {}) if match else {}
            labels = ["A", "B"]
            rng.shuffle(labels)
            key[tid] = {"X": labels[0], "Y": labels[1]}
            negative = case["Эталонный вердикт"] == "дефекта нет"
            lines += [
                f"## {tid}",
                "",
                f"**Вход:** {case['Вход']}",
                "",
                f"**Контекст:** {case['Контекст']}",
                "",
                f"**Эталонный вердикт:** {case['Эталонный вердикт']}",
                "",
                f"**Тип кейса:** {'негативный (K2 не применяется)' if negative else 'дефектный'}",
                "",
                f"**Правило урока:** {lesson.get('rule', '—')}",
                "",
                f"**Обоснование эталона:** {case['Обоснование эталона']}",
                "",
                "### Выход X",
                "",
                render(outputs[labels[0]].get(tid)),
                "",
                "### Выход Y",
                "",
                render(outputs[labels[1]].get(tid)),
                "",
            ]
        (work / f"judge/judge-batch{batch + 1}.md").write_text("\n".join(lines), encoding="utf-8")
    (work / "judge-key.json").write_text(json.dumps(key, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"cases={len(tids)} A={len(outputs['A'])} B={len(outputs['B'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
