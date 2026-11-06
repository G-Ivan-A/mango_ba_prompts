#!/usr/bin/env python3
"""Issue #454: read-only audit of what the kit assigns per stage, gate, operation contract and section.

Run: python3 experiments/issue_454/audit_stage_contracts.py [RUNTIME_CLONE]
Answers the owner's question from PR #455: are prompts (steps, gates, contracts) created for
A-IN, A-CORE, A-WORK. "Assigned" is the text the main copy button of a kit card gives the BA.
Writes experiments/issue_454/audit_stage_contracts.json. Exits 1 on a structural hole:
a missing gate criterion, a missing contract or section standard, a broken link, a section
without a producing step. A contract code absent from an assigned text is a reported fact, not a hole:
the v0.1/v0.2 texts carry the rules without the К-NN codes, see the "contract_codes" fields.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).with_name("audit_stage_contracts.json")
STAGES = {
    "старт": ["Ш-0"],
    "A-IN": ["Ш-1", "Ш-2"],
    "A-CORE": ["Ш-3", "Ш-4", "Ш-5"],
    "A-WORK": ["Ш-6", "Ш-7", "Ш-8", "Ш-9", "Ш-В"],
    "A-RELEASE": ["Ш-Р"],
    "вне последовательности": ["Ш-С"],
}
GATES = {
    "Г-IN": {"closing_step": "Ш-2", "criteria": 5, "decides": "БА", "type": "гибрид"},
    "Г-С1": {"closing_step": "Ш-5", "criteria": 5, "decides": "Заказчик", "type": "человек"},
    "Г-W": {"closing_step": "Ш-В", "criteria": 5, "decides": "команда", "type": "человек"},
    "Выпуск": {"closing_step": "Ш-Р", "criteria": 0, "decides": "человек", "type": "человек"},
}
SECTIONS = {
    1: ("01-glossary.md", ["Ш-1"]),
    2: ("02-business-context.md", ["Ш-1", "Ш-2"]),
    3: ("03-functional-requirements.md", ["Ш-3"]),
    4: ("04-non-functional-requirements.md", ["Ш-4"]),
    5: ("05-solution-description.md", ["Ш-6"]),
    6: ("06-implementation-constraints.md", ["Ш-7"]),
    7: ("07-use-cases.md", ["Ш-5", "Ш-8"]),
    8: ("08-supplementary.md", ["Ш-9"]),
}
REPO_LINK = re.compile(r"github\.com/G-Ivan-A/mango_ba_prompts/(?:blob|tree)/main/([^\s)#?\"'>]+)")
RUNTIME_LINK = re.compile(r"github\.com/G-Ivan-A/mango-ba-ai-runtime/(?:blob|tree)/([0-9a-f]{7,40})/([^\s)#?\"'>]+)")


def load():
    kit = json.loads((ROOT / "site/data/test-kit.json").read_text(encoding="utf-8"))
    prompts = json.loads((ROOT / "site/data/prompts.json").read_text(encoding="utf-8"))["prompts"]
    catalog = json.loads((ROOT / "standards/bcreq-manual-classes/catalog.json").read_text(encoding="utf-8"))
    return kit, {p["id"]: p for p in prompts}, catalog["classes"]


def assigned_text(step, by_id):
    """The body the main copy button serves: site/app.js, copyTestKitPrompt."""
    if step["mode"] == "by-test":
        return step["draft"], step["draft"]["body"]
    return step["published"], by_id[step["published"]["id"]]["body"]


def main():
    runtime = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    kit, by_id, classes = load()
    holes = []
    steps = {s["step"].split()[0]: s for s in kit["steps"]}
    texts, rows = {}, []
    for code, step in steps.items():
        variant, body = assigned_text(step, by_id)
        draft = (step.get("draft") or {}).get("body", "")
        ops = sorted(c["id"] for c in classes if c["flow_step"] == code)
        texts[code] = body
        broken = sorted({m for m in REPO_LINK.findall(body) if not (ROOT / m).exists()})
        runtime_refs = sorted(set(RUNTIME_LINK.findall(body)))
        broken_runtime = sorted(p for _, p in runtime_refs if runtime and not (runtime / p).exists())
        rows.append({
            "step": code,
            "stage": next(k for k, v in STAGES.items() if code in v),
            "mode": step["mode"],
            "assigned_file": variant["file"],
            "assigned_version": variant.get("version") or "по тесту",
            "assigned_bytes": len(body.encode()),
            "operations": ops,
            "contract_codes_in_assigned": [o for o in ops if o in body],
            "contract_codes_in_draft": [o for o in ops if o in draft],
            "state_block": "Состояние BCREQ" in body,
            "fallback_rule": "Режим fallback" in body,
            "repo_links": len(set(REPO_LINK.findall(body))),
            "broken_repo_links": broken,
            "runtime_links": len(runtime_refs),
            "broken_runtime_links": broken_runtime if runtime else "не проверялось",
        })
        holes += [f"{code}: битая ссылка {b}" for b in broken + broken_runtime]
        if not ops:
            holes.append(f"{code}: нет операций в каталоге")
    missing_ops = [c["id"] for c in classes if c["flow_step"] not in steps]
    holes += [f"{o}: операция вне шагов" for o in missing_ops]
    missing_files = [c["id"] for c in classes if not (ROOT / "standards/bcreq-manual-classes" / c["file"]).exists() and not (ROOT / c["file"]).exists()]
    holes += [f"{o}: нет файла контракта" for o in missing_files]

    run_kit = (ROOT / "docs/ba-processes/bcreq-run-kit.md").read_text(encoding="utf-8")
    journal = {f: f in run_kit for f in ("gate_id", "gate_type", "model_recommendation", "divergence")}
    holes += [f"журнал гейтов: нет поля {k}" for k, v in journal.items() if not v]
    gates = {}
    for gate, spec in GATES.items():
        code = spec["closing_step"]
        body, card = texts[code], steps[code]
        draft = (card.get("draft") or {}).get("body", "")
        criteria = [f"{gate}.{n}" for n in range(1, spec["criteria"] + 1)]
        in_assigned = [c for c in criteria if c in body]
        gates[gate] = {
            **spec,
            "criteria_in_assigned": in_assigned,
            "criteria_in_draft": [c for c in criteria if c in draft],
            "report_block_in_assigned": bool(re.search(rf"Отч[её]т по гейту {re.escape(gate)}", body)) or gate == "Выпуск" and "Выпуск" in body,
            "card_gate": card.get("gate"),
            "card_hint": bool(card.get("gateHint")),
            "journal_form_in_kit": all(journal.values()),
            "separate_gate_prompt": False,
        }
        if in_assigned != criteria:
            holes.append(f"{gate}: в назначенном тексте {code} нет {sorted(set(criteria) - set(in_assigned))}")
        if not card.get("gate", "—").startswith(gate):
            holes.append(f"{gate}: на карточке {code} нет метки гейта")

    sections = {}
    for number, (name, producers) in SECTIONS.items():
        path = ROOT / "standards/bcreq-sections" / name
        text = path.read_text(encoding="utf-8") if path.exists() else ""
        checklist = text.split("## Чек-лист валидации", 1)[-1].split("\n## ", 1)[0] if "## Чек-лист валидации" in text else ""
        items = len(re.findall(r"(?m)^- \[ \]", checklist))
        linked = [p for p in producers if name[:2] in re.findall(r"bcreq-sections/(\d\d)", texts[p])]
        sections[number] = {"standard": name, "producers": producers, "linked_from_assigned": linked, "checklist_items": items}
        if not items or not linked:
            holes.append(f"раздел {number}: чек-лист {items}, ссылка из промптов {linked}")

    summary = {}
    for stage, codes in STAGES.items():
        stage_rows = [r for r in rows if r["step"] in codes]
        ops = sum(len(r["operations"]) for r in stage_rows)
        summary[stage] = {
            "steps": len(codes),
            "texts_assigned": sum(1 for r in stage_rows if r["assigned_bytes"]),
            "operations": ops,
            "contract_codes_in_assigned": sum(len(r["contract_codes_in_assigned"]) for r in stage_rows),
            "contract_codes_in_draft": sum(len(r["contract_codes_in_draft"]) for r in stage_rows),
            "modes": sorted({r["mode"] for r in stage_rows}),
        }
    facts = {"kit": kit["kit"]["version"], "summary": summary, "gates": gates, "sections": sections, "steps": rows, "journal_fields": journal, "holes": holes}
    OUT.write_text(json.dumps(facts, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("stage | steps | texts | ops | К-NN in assigned | К-NN in draft | modes")
    for stage, s in summary.items():
        print(stage, s["steps"], s["texts_assigned"], s["operations"], s["contract_codes_in_assigned"], s["contract_codes_in_draft"], ",".join(s["modes"]), sep=" | ")
    print("gate | step | criteria assigned | report block | card")
    for gate, g in gates.items():
        print(gate, g["closing_step"], f"{len(g['criteria_in_assigned'])}/{g['criteria']}", g["report_block_in_assigned"], g["card_gate"], sep=" | ")
    print("section | standard | producers | linked | checklist")
    for number, s in sections.items():
        print(number, s["standard"], ",".join(s["producers"]), ",".join(s["linked_from_assigned"]), s["checklist_items"], sep=" | ")
    print("step | assigned | repo links | runtime links | broken")
    for r in rows:
        print(r["step"], r["assigned_version"], r["repo_links"], r["runtime_links"], (r["broken_repo_links"], r["broken_runtime_links"]), sep=" | ")
    print("holes:", holes or "none")
    return 1 if holes else 0


if __name__ == "__main__":
    raise SystemExit(main())
