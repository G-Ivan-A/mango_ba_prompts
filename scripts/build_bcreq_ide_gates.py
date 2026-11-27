#!/usr/bin/env python3
"""Карта шагов и гейтов этапа 1 для оркестратора IDE (RFC-RT-003, раздел 5).

RFC-RT-003 (#506), раздел 4.2: ``bcreq-ide-gates.json`` — «раздел 5 в
машинном виде», владелец — спица, файл генерируется здесь и приходит в
runtime передачей SSOT (M2, BL-185…BL-188) по пути
``ssot/mango_ba_prompts/docs/ba-processes/bcreq-ide-gates.json`` (Р-RT-6).
Оркестратор ``bcreq-orchestrator`` (BL-192 Э5) берёт следующий шаг и тип
остановки из этого файла, а не из памяти (раздел 6.1, п. 3).

Карта не задаёт новую норму. Всё берётся из действующих источников:

* 24 шага AIN и правила паузы — маршрут ``bcreq-a-in-route.json``;
* 14 технических шагов, гейты, которые техническими не бывают, —
  ``bcreq-a-in-execution.md`` («Технических шагов 14»);
* шаги потока Ш-0…Ш-Р, Ш-С, их стадии и гейты после шага — таблица 0.3,
  типы и роли гейтов — таблицы 0.2 и «Решения гейтов», действия после шага,
  допуски и возвраты — таблицы «Действия после шага» и «Возвраты маршрута»
  ручного процесса ``bcreq-manual-process.md``;
* шаги, которые по Р-09 принимаются при отсутствии возражения БА, — абзац
  Р-09 того же файла.

Типы остановок — раздел 5.1 RFC: ``T`` — технический шаг без остановки,
``P`` — проверка БА (Р-09), ``G`` — шаг, после которого решает гейт,
``B`` — блокировка (Р-19). Тип ``B`` не приписан шагу: он возникает при
``BLOCKED`` на любом шаге.

``--check`` сверяет файл, ничего не записывая. LLM не вызывается.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROCESSES = ROOT / "docs/ba-processes"
ROUTE = PROCESSES / "bcreq-a-in-route.json"
EXECUTION = PROCESSES / "bcreq-a-in-execution.md"
MANUAL = PROCESSES / "bcreq-manual-process.md"
OUT = PROCESSES / "bcreq-ide-gates.json"

#: Стадия артефакта → команда процесса в IDE (RFC-RT-003, раздел 5.3).
COMMANDS = {"A-IN": "/a-in", "A-CORE": "/a-core", "A-WORK": "/a-work", "A-RELEASE": "/a-release"}
#: Сколько технических шагов задаёт норма (исполнение A-IN, issue #490).
TECHNICAL_COUNT = 14

STOP_TYPES = {
    "T": "технический шаг: исполняется без остановки, итог шага пишется в журнал; "
         "по Р-09 ввод следующего промпта и есть принятие",
    "P": "проверка БА (Р-09): остановка, один вопрос «принять и запустить <шаг> / "
         "принять и остановиться / доработать / вернуться» по шагу и редакции",
    "G": "гейт: остановка с вопросом решения гейта, исходами и ролью, которая решает; "
         "для гибрида — рекомендация модели с основанием",
    "B": "блокировка (Р-19): остановка всего процесса до устранения причины; "
         "приоритет над всеми допусками",
}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def table(text: str, header_start: str) -> list[list[str]]:
    """Строки markdown-таблицы, заголовок которой начинается с ``header_start``."""
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith("| " + header_start):
            rows = []
            for row in lines[index + 2:]:
                if not row.startswith("|"):
                    break
                rows.append([cell.strip() for cell in row.strip().strip("|").split("|")])
            return rows
    raise SystemExit(f"таблица «{header_start}» не найдена")


def expand(ids: str) -> list[str]:
    """«AIN-01, 03–10, 12» → AIN-01, AIN-03…AIN-10, AIN-12."""
    out: list[str] = []
    prefix = ""
    for token in (t.strip() for t in ids.split(",")):
        match = re.fullmatch(r"(?:(AIN)-)?(\d{2})(?:[–-](\d{2}))?", token)
        if not match:
            out.append(token)
            continue
        prefix = match[1] or prefix
        first, last = int(match[2]), int(match[3] or match[2])
        out.extend(f"{prefix}-{n:02d}" for n in range(first, last + 1))
    return out


def technical_steps(text: str) -> tuple[list[str], list[str]]:
    block = re.search(r"Технических шагов (\d+):\n\n((?:- .*\n)+)", text)
    if not block:
        raise SystemExit("в исполнении A-IN нет списка «Технических шагов N»")
    steps: list[str] = []
    for item in re.findall(r"^- (.*?);?$", block[2], re.M):
        steps.extend(expand(item.rstrip(";.")))
    if len(steps) != int(block[1]):
        raise SystemExit(f"список технических шагов: {len(steps)}, а заявлено {block[1]}")
    gates = re.search(r"Гейты (.*?) техническими не бывают", text, re.S)
    if not gates:
        raise SystemExit("в исполнении A-IN нет строки «Гейты … техническими не бывают»")
    never = [g.strip() for g in re.split(r",| и ", gates[1].replace("\n", " ")) if g.strip()]
    return steps, never


def accept_unless_objection(text: str) -> list[str]:
    match = re.search(r"Для (AIN-\d{2}(?: и AIN-\d{2})*) успешный результат\s+с «Итогом шага» принимается при отсутствии возражения БА", text)
    if not match:
        raise SystemExit("в Р-09 нет перечня шагов, принимаемых при отсутствии возражения БА")
    return re.findall(r"AIN-\d{2}", match[1])


def flow_steps(text: str) -> list[dict]:
    rows = table(text, "Шаг потока | Процесс | Стадия артефакта")
    steps = []
    for step, process, stage, _prompt, operations, gate in rows:
        code, _, name = step.partition(" ")
        steps.append({
            "id": code,
            "name": name,
            "process": process,
            "stage": stage,
            "operations": [o.strip() for o in operations.split(",")],
            "gate_after": None if gate == "—" else ("Выпуск" if gate.lower() == "выпуск" else gate),
        })
    return steps


def gates(text: str) -> list[dict]:
    flow = {row[0].split(" «")[0]: row for row in table(text, "Гейт потока | Процесс")}
    out = []
    for code, kind, key, checks, who, outcomes, record in table(text, "Код гейта | Тип"):
        row = flow.get(code)
        out.append({
            "code": code,
            "type": kind,
            "key": key == "да",
            "checks": checks,
            "decides": who,
            "outcomes": outcomes,
            "record": record,
            "transition": row[2] if row else None,
            "hybrid": kind == "гибрид",
            "decision_by_model": False,
        })
    return out


def transitions(text: str) -> list[dict]:
    out = []
    for source, fmt, action, when, admission, conditions, target in table(text, "Из шага | Формат действия"):
        gate, _, outcome = admission.partition("/") if "/" in admission else (None, "", "")
        out.append({
            "from": source,
            "format": fmt,
            "action": action,
            "when": when,
            "admission": None if admission == "—" else admission,
            "requires_gate": {"code": gate, "outcome": outcome} if gate else None,
            "requires_ba_acceptance": admission == "БА",
            "conditions": [] if conditions == "—" else [c.strip() for c in conditions.split(",")],
            "target": target,
        })
    return out


def returns(text: str) -> list[dict]:
    out = []
    for reason, when, stage, system, decomposed in table(text, "Причина возврата | Когда"):
        out.append({"reason": reason, "when": when, "stage": stage,
                    "system": None if system == "—" else system,
                    "decomposed": None if decomposed == "—" else decomposed})
    return out


def stop_type(step: str, technical: set[str], gate_after: str | None) -> str:
    if gate_after:
        return "G"
    return "T" if step in technical else "P"


def build() -> dict:
    route = json.loads(ROUTE.read_text(encoding="utf-8"))
    execution = EXECUTION.read_text(encoding="utf-8")
    manual = MANUAL.read_text(encoding="utf-8")
    technical, never_technical = technical_steps(execution)
    lenient = accept_unless_objection(manual)
    gate_list = gates(manual)
    gate_codes = {g["code"] for g in gate_list}
    flow = flow_steps(manual)
    moves = transitions(manual)

    ain_ids = [s["id"] for s in route["steps"]]
    unknown = [s for s in technical if s != "Ш-0" and s not in ain_ids]
    if unknown:
        raise SystemExit(f"технические шаги вне маршрута A-IN: {unknown}")

    # Гейт после шага AIN: AIN-21 — сам гейт, AIN-24 — передача под решение Г-IN
    # (таблица «Действия после шага»: допуск AIN-24 → Г-IN/дальше).
    ain_gate = {}
    for move in moves:
        gate = (move["requires_gate"] or {}).get("code")
        if move["from"].startswith("AIN-") and gate in gate_codes:
            ain_gate.setdefault(move["from"], gate)
    admitted_by = {}
    for move in moves:
        if move["requires_gate"] and move["from"] == move["requires_gate"]["code"]:
            admitted_by[move["target"]] = dict(move["requires_gate"])

    def entry(step_id: str, name: str, gate_after: str | None, **extra) -> dict:
        item = {"id": step_id, "name": name, "type": stop_type(step_id, set(technical), gate_after)}
        if gate_after:
            item["gate_after"] = gate_after
        if step_id in lenient:
            item["accept_unless_objection"] = True
        if step_id in admitted_by:
            item["requires_gate"] = admitted_by[step_id]
            item["separate_call"] = True
        item.update(extra)
        return item

    start = next(s for s in flow if s["id"] == "Ш-0")
    processes = []
    for stage, command in COMMANDS.items():
        seq = [s for s in flow if s["stage"] == stage]
        process = {"stage": stage, "command": command, "formats": {}}
        system = [entry(start["id"], start["name"], None)]
        system += [entry(s["id"], s["name"], s["gate_after"]) for s in seq]
        if stage == "A-IN":
            decomposed = [entry(start["id"], start["name"], None)]
            decomposed += [entry(s["id"], s["name"], ain_gate.get(s["id"])) for s in route["steps"]]
            process["formats"] = {"system": system, "decomposed": decomposed}
        else:
            process["formats"] = {"both": system}
        processes.append(process)
    on_request = [entry(s["id"], s["name"], s["gate_after"]) for s in flow if s["stage"] == "вне последовательности"]

    gate_steps = sorted({s["id"] for p in processes for f in p["formats"].values() for s in f if s["type"] == "G"})
    clash = sorted(set(technical) & set(gate_steps))
    if clash:
        raise SystemExit(f"шаг одновременно технический и гейтовый: {clash}")
    missing = sorted(set(never_technical) - set(gate_steps))
    if missing:
        raise SystemExit(f"гейты из исполнения A-IN без типа G в карте: {missing}")

    return {
        "id": "BCREQ-IDE-GATES",
        "version": "0.1",
        "status": "accepted",
        "rfc": "RFC-RT-003, раздел 5 (issue #506, ADR-020)",
        "generated_by": "scripts/build_bcreq_ide_gates.py",
        "runtime_path": "ssot/mango_ba_prompts/docs/ba-processes/bcreq-ide-gates.json",
        "note": "Карта исполняет норму этапа 1 и не меняет её. Тип шага меняет только процесс спицы (Р-RT-12).",
        "sources": {rel(p): sha256(p) for p in (ROUTE, EXECUTION, MANUAL)},
        "stop_types": STOP_TYPES,
        "interaction": {
            "advance_while_paused": route["interaction"]["advance_while_paused"],
            "resume_requires_ba_instruction": route["interaction"]["resume_requires_ba_instruction"],
            "future_comment_authorizes_execution": route["interaction"]["future_comment_authorizes_execution"],
            "blocked_unavailable": route["startup_rules"]["unavailable"],
        },
        "technical_steps": technical,
        "never_technical": never_technical,
        "accept_unless_objection": lenient,
        "gates": gate_list,
        "processes": processes,
        "on_request": on_request,
        "transitions": moves,
        "returns": returns(manual),
        "decision_log": {
            "path": "work/<ключ>/decisions.jsonl",
            "fields": ["code", "type", "outcome", "who", "when", "locator", "version",
                       "question_id", "model_recommendation", "divergence"],
            "hybrid_only": ["model_recommendation", "divergence"],
        },
    }


def render(data: dict) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("--check", action="store_true", help="сверить файл, не записывая")
    args = parser.parse_args(argv)
    text = render(build())
    if args.check:
        current = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        if current != text:
            print(f"{rel(OUT)} устарел: запустите python3 scripts/build_bcreq_ide_gates.py", file=sys.stderr)
            return 1
        print(f"{rel(OUT)} актуален")
        return 0
    OUT.write_text(text, encoding="utf-8")
    print(f"записан {rel(OUT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
