#!/usr/bin/env python3
"""RUN-0080: подготовка слепой оценки по рубрике K1–K6 (issue #438).

Для каждого кейса выходы A и D получают метки X/Y в случайном порядке
(seed 8080). Ключ хранится в judge-key.json и судье не передаётся.

D собран из базового стандарта и профилей. Его выход может ссылаться на
ID, которых нет в v0.1: правила БС-NN, операции К-NN, процессы ПБ-N,
справочники И-N, заглушки З-N, профили (ANALYZE, VERIFY, …), receipt.
Такие ссылки выдали бы версию судье, поэтому они маскируются в обоих
выходах одинаково (содержание нарушения сохраняется). Номера уроков L-NN
маскируются, как в RUN-0079.

Использование:
    python3 experiments/issue_438/run0080/judge_prepare.py WORKDIR
"""
from __future__ import annotations

import json
import random
import re
import sys
from pathlib import Path

from prepare import ROOT, load_validator

SEED = 8080
BATCHES = 2
VERSIONS = ("A", "D")
ID_RE = re.compile(r"\b(?:L|БС|К|ПБ|И|З|ТС|ПР)-(?:\d+|NN)(?:\.\d+)*\b")
WORD_RE = re.compile(
    r"\b(?:INGEST|EXTRACT|ANALYZE|ELICIT|GENERATE|VERIFY|TRANSFORM|RECORD|receipt|G-self|G-mach|semantic_diff|UNKNOWN|WAITING|BLOCKED|INCOMPLETE)\b",
    re.I,
)
#: Следы маскировки: пустые скобки, висящие «/», запятые и двоеточия.
CLEANUP = (
    (re.compile(r"/(?=[\s:,;)/]|$)"), ""),
    (re.compile(r"(?<=[\s(/])/"), ""),
    (re.compile(r"\(\s*[,;/]?\s*\)"), ""),
    (re.compile(r"(?:,\s*){2,}"), ", "),
    (re.compile(r"\(\s*,\s*"), "("),
    (re.compile(r",\s*\)"), ")"),
    (re.compile(r"^(?:\s*[,:;])+\s*"), ""),
    (re.compile(r"\s+([,:;.)])"), r"\1"),
    (re.compile(r"([,:;])(?:\s*[,:;])+"), r"\1"),
    (re.compile(r" {2,}"), " "),
)
#: Что не должно остаться в файлах судьи после маскировки.
LEAK_RE = re.compile(r"\b(?:L|БС|К|ПБ|И|З|ТС|ПР)-\d+|\b(?:INGEST|EXTRACT|ANALYZE|ELICIT|GENERATE|VERIFY|TRANSFORM|RECORD|receipt|G-self|G-mach)\b", re.I)


def mask(value: str) -> str:
    value = WORD_RE.sub("", ID_RE.sub("", value))
    for pattern, replacement in CLEANUP:
        value = pattern.sub(replacement, value)
    return value.strip()


def load_outputs(work: Path, version: str) -> dict:
    result = {}
    for path in sorted((work / "out").glob(f"{version}-batch*.json")):
        for item in json.loads(path.read_text(encoding="utf-8")):
            result[item["case"]] = item
    return result


def render(item: dict | None) -> str:
    if item is None:
        return "_(выход отсутствует)_"
    return "\n".join(f"- **{key}:** {mask(str(item.get(key, '')))}" for key in ("verdict", "violation", "quote", "fix"))


def main() -> int:
    work = Path(sys.argv[1]).resolve()
    (work / "judge").mkdir(exist_ok=True)
    meta = json.loads((work / "mapping.json").read_text(encoding="utf-8"))
    cases = {case["case-id"]: case for case in load_validator().golden_cases()}
    lessons = {lesson["id"]: lesson for lesson in json.loads((ROOT / "standards/bcreq-lessons/lessons.json").read_text(encoding="utf-8"))["lessons"]}
    outputs = {version: load_outputs(work, version) for version in VERSIONS}
    rng = random.Random(SEED)
    key = {}
    tids = sorted(meta["mapping"])
    size = (len(tids) + BATCHES - 1) // BATCHES
    leaks = []
    for batch in range(BATCHES):
        lines = [f"# Слепая оценка, пакет {batch + 1}", ""]
        for tid in tids[batch * size:(batch + 1) * size]:
            case = cases[meta["mapping"][tid]]
            match = re.search(r"L-\d+", case["Урок"])
            lesson = lessons.get(match.group(0), {}) if match else {}
            labels = list(VERSIONS)
            rng.shuffle(labels)
            key[tid] = {"X": labels[0], "Y": labels[1]}
            negative = case["Эталонный вердикт"] == "дефекта нет"
            x, y = render(outputs[labels[0]].get(tid)), render(outputs[labels[1]].get(tid))
            leaks += [f"{tid}: {m}" for m in LEAK_RE.findall(x + y)]
            lines += [
                f"## {tid}", "",
                f"**Вход:** {case['Вход']}", "",
                f"**Контекст:** {case['Контекст']}", "",
                f"**Эталонный вердикт:** {case['Эталонный вердикт']}", "",
                f"**Тип кейса:** {'негативный (K2 не применяется)' if negative else 'дефектный'}", "",
                f"**Правило урока:** {lesson.get('rule', '—')}", "",
                f"**Обоснование эталона:** {case['Обоснование эталона']}", "",
                "### Выход X", "", x, "",
                "### Выход Y", "", y, "",
            ]
        (work / f"judge/judge-batch{batch + 1}.md").write_text("\n".join(lines), encoding="utf-8")
    (work / "judge-key.json").write_text(json.dumps(key, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    rules = (ROOT / "runs/2026/RUN-0079/logs/judge-rules.md").read_text(encoding="utf-8")
    (work / "judge/rules.md").write_text(rules.split("---\n", 2)[2].lstrip("\n"), encoding="utf-8")
    print(f"cases={len(tids)} " + " ".join(f"{v}={len(outputs[v])}" for v in VERSIONS) + f" leaks={len(leaks)}")
    for leak in leaks:
        print("LEAK", leak)
    return 1 if leaks or any(len(outputs[v]) != len(tids) for v in VERSIONS) else 0


if __name__ == "__main__":
    raise SystemExit(main())
