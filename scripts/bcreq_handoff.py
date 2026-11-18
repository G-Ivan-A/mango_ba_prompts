#!/usr/bin/env python3
"""Цель шага и блок «Итог шага» для БА из SSOT (issue #490).

Источник — ``docs/ba-processes/bcreq-step-handoff.md``: правила, шаблон блока
и таблица 38 шагов (Ш-0…Ш-С, AIN-01…AIN-24). Модуль:

* разбирает SSOT (``load``) и рендерит блок для одного или нескольких шагов
  одного промпта (``render``) — им пользуются сборщики промптов;
* пишет ``site/data/step-handoff.json`` — цель, проверку и готовый блок для
  карточек сайта и для опубликованных Ш-В и Ш-С, чьи файлы ``prompts/``
  заморожены (сайт добавляет блок к копируемому тексту).

``--check`` сверяет JSON с выходом, ничего не записывая. LLM не вызывается.
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SSOT = ROOT / "docs/ba-processes/bcreq-step-handoff.md"
OUT = ROOT / "site/data/step-handoff.json"
BEGIN = "<!-- issue-490:handoff -->"
END = "<!-- /issue-490:handoff -->"
COLUMNS = ["Шаг", "Название", "Цель", "Выполнено", "Проверка БА", "Что проверить", "Следующий"]
KINDS = {"обязательна": "required", "технический": "technical"}
ROUTE = ["Ш-0", "Ш-А", "Ш-1", "Ш-2", "Ш-3", "Ш-4", "Ш-5", "Ш-6", "Ш-7", "Ш-8", "Ш-9", "Ш-В", "Ш-Р", "Ш-С"]
AIN = [f"AIN-{n:02}" for n in range(1, 25)]
#: Гейты людей не бывают техническими (правило ИШ-4).
NEVER_TECHNICAL = {"Ш-2", "Ш-5", "Ш-В", "Ш-Р", "AIN-21", "AIN-24"}
SINGLE = re.compile(r"^(AIN-\d{2}|Ш-[0-9А-ЯЁ])$")


def _between(text, tag):
    start, end = f"<!-- {tag} -->\n", f"\n<!-- /{tag} -->"
    if text.count(start) != 1 or text.count(end) != 1:
        raise ValueError(f"SSOT: маркер {tag} должен встречаться ровно один раз")
    return text.split(start, 1)[1].split(end, 1)[0]


def _cells(line):
    return [c.strip() for c in line.strip().strip("|").split(" | ")]


def load(path=SSOT):
    text = path.read_text(encoding="utf-8")
    table = text.split("\n## 3. Шаги\n", 1)[1]
    rows = [line for line in table.splitlines() if line.startswith("| ")]
    if _cells(rows[0]) != COLUMNS:
        raise ValueError(f"SSOT: колонки {_cells(rows[0])} вместо {COLUMNS}")
    steps = {}
    for line in rows[2:]:
        cells = _cells(line)
        if len(cells) != len(COLUMNS):
            raise ValueError(f"SSOT: {len(cells)} ячеек в строке {line[:40]}")
        row = dict(zip(["id", "name", "goal", "done", "kind", "check", "next"], cells))
        if row["kind"] not in KINDS:
            raise ValueError(f"SSOT: {row['id']}: проверка БА «{row['kind']}»")
        row["checkKind"] = KINDS[row.pop("kind")]
        if row["id"] in steps:
            raise ValueError(f"SSOT: шаг {row['id']} повторяется")
        steps[row["id"]] = row
    if list(steps) != ROUTE + AIN:
        raise ValueError(f"SSOT: шаги {list(steps)} вместо {ROUTE + AIN}")
    for sid in NEVER_TECHNICAL:
        if steps[sid]["checkKind"] != "required":
            raise ValueError(f"SSOT: гейт {sid} не может быть техническим")
    return {
        "version": re.search(r"^version: (\S+)$", text, re.M).group(1),
        "template": _between(text, "handoff-template"),
        "approveRequired": _between(text, "approve-required"),
        "approveTechnical": _between(text, "approve-technical"),
        "steps": steps,
    }


def _form(step, indent="   "):
    head = f"{indent}- Выполнен промпт {step['id']} «{step['name']}»: {step['done']}."
    nxt = step["next"]
    if step["checkKind"] == "required":
        second = f"{indent}- БА — проверить: {step['check']}. Без решения БА следующий промпт не запускается."
    else:
        target = f"промпта {nxt}" if SINGLE.match(nxt) else f"следующего промпта ({nxt})"
        second = (f"{indent}- Шаг технический, можно проверить ({step['check']}), но не обязательно. "
                  f"ИИ-ассистент ожидает ввода {target} без обязательного согласования БА выполненных действий.")
    return [f"{indent}**Итог шага**", "", head, second, f"{indent}- Следующий промпт: {nxt}."]


def render(step_ids, data=None):
    """Блок «Итог шага» для промпта, исполняющего шаги ``step_ids``."""
    data = data or load()
    steps = [data["steps"][sid] for sid in step_ids]
    required = [s for s in steps if s["checkKind"] == "required"]
    if required:
        check = "; ".join(
            (f"на {s['id']} — {s['check']}" if len(steps) > 1 else s["check"]) for s in required)
        approve = data["approveRequired"].replace("{check}", check)
    else:
        approve = data["approveTechnical"]
    if len(steps) > 1:
        intro = (f"Этот промпт исполняет шаги {' и '.join(s['id'] for s in steps)}: "
                 "выведи итог того шага, который выполняешь.\n\n")
        forms = []
        for s in steps:
            forms += [f"   Для {s['id']}:", ""] + _form(s, "   ") + [""]
    else:
        intro, forms = "", _form(steps[0]) + [""]
    block = (data["template"].replace("{steps_intro}", intro)
             .replace("{approve_rule}", approve)
             .replace("{forms}", "\n".join(forms)))
    assert "{" not in block.replace("`{", ""), block
    assert block.startswith(BEGIN) and block.endswith(END)
    return block + "\n"


def site_data(data=None):
    data = data or load()
    steps = {}
    for sid, s in data["steps"].items():
        steps[sid] = {k: s[k] for k in ("name", "goal", "done", "checkKind", "check", "next")}
        steps[sid]["block"] = render([sid], data)
    return {
        "source": "docs/ba-processes/bcreq-step-handoff.md",
        "version": data["version"],
        "issue": "https://github.com/G-Ivan-A/mango_ba_prompts/issues/490",
        "steps": steps,
    }


def dump(data=None):
    return json.dumps(site_data(data), ensure_ascii=False, indent=2) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("--check", action="store_true", help="сверить site/data/step-handoff.json, не записывая")
    args = parser.parse_args(argv)
    text = dump()
    if args.check:
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != text:
            print(f"устарел или отсутствует: {OUT.relative_to(ROOT)}")
            return 1
        print("OK: site/data/step-handoff.json совпадает с SSOT")
        return 0
    OUT.write_text(text, encoding="utf-8")
    print(f"записано: {OUT.relative_to(ROOT)} (38 шагов)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
