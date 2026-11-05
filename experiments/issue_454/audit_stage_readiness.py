#!/usr/bin/env python3
"""Issue #454: read-only audit by stage: A-IN, A-CORE, A-WORK, A-RELEASE -> steps -> operations -> contracts -> gates -> sections.

Run from anywhere: python3 experiments/issue_454/audit_stage_readiness.py
Answers one question per element: what does the BA get on the site, as text, for that element?
"Assigned" means the text the card's main copy button gives: draft body in mode by-test, published body otherwise.
Writes audit_stage_readiness.json (facts) next to itself and prints a table. Exit 1 if a required element is absent.
Reads repository files and site data only; it says nothing about production: see audit_flow_coverage.py.
"""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).with_name("audit_stage_readiness.json")
# docs/contracts/bcreq-stage-gates.md: stage -> steps, sections, gate, criteria.
STAGES = {
    "A-IN": {"steps": ["Ш-1", "Ш-2"], "sections": ["1", "2", "2.5", "8.4"], "gate": "Г-IN", "criteria": 5},
    "A-CORE": {"steps": ["Ш-3", "Ш-4", "Ш-5"], "sections": ["3", "4", "7"], "gate": "Г-С1", "criteria": 5},
    "A-WORK": {"steps": ["Ш-6", "Ш-7", "Ш-8", "Ш-9", "Ш-В"], "sections": ["5", "6", "7", "8"], "gate": "Г-W", "criteria": 5},
    "A-RELEASE": {"steps": ["Ш-Р"], "sections": [], "gate": "Выпуск", "criteria": 0},
}
OUTSIDE = ["Ш-0", "Ш-С"]  # Ш-0 is the constitution without a stage; Ш-С runs on request outside the sequence.
SECTION_FILES = {"1": "01-glossary.md", "2": "02-business-context.md", "3": "03-functional-requirements.md",
                 "4": "04-non-functional-requirements.md", "5": "05-solution-description.md",
                 "6": "06-implementation-constraints.md", "7": "07-use-cases.md", "8": "08-supplementary.md"}
# The operations of each gate cycle in docs/ba-processes/bcreq-manual-process.md: evidence К-20, decision record К-34.
GATE_OPS = ["К-12", "К-13", "К-20", "К-34", "К-39"]
CONTRACT_MARK = "Контракты операций"
# standards/bcreq-prompt-profiles.md: the eight action profiles a step prompt may carry.
ACTION_PROFILES = ["INGEST", "EXTRACT", "ANALYZE", "ELICIT", "GENERATE", "VERIFY", "TRANSFORM", "RECORD"]


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def active_stubs(text):
    """Stub codes the text really carries: the base-standard rule БС-21 only lists them all."""
    return sorted({code for line in text.splitlines() if "БС-21" not in line for code in re.findall(r"З-\d", line)})


def assigned_text(step, by_file):
    """The body behind the card's main button, exactly as the site would copy it."""
    if step["mode"] == "by-test" and step.get("draft"):
        return step["draft"]["body"]
    published = step.get("published")
    item = by_file.get(published["file"]) if published else None
    return item["body"] if item else ""


def section_checklist(path):
    """Number of checklist items under the section standard's validation heading."""
    text = path.read_text(encoding="utf-8")
    part = re.split(r"(?m)^## Чек-лист валидации", text)
    if len(part) < 2:
        return 0
    return len(re.findall(r"(?m)^\s*(?:- \[ \]|- |\d+\. |\| \d)", re.split(r"(?m)^## ", part[1])[0]))


def main():
    kit = json.loads((ROOT / "site/data/test-kit.json").read_text(encoding="utf-8"))
    site = json.loads((ROOT / "site/data/prompts.json").read_text(encoding="utf-8"))
    by_file = {Path(p["sourcePath"]).name: p for p in site["prompts"] if p.get("sourcePath")}
    catalog = json.loads((ROOT / "standards/bcreq-manual-classes/catalog.json").read_text(encoding="utf-8"))
    cards = {s["step"].split()[0]: s for s in kit["steps"]}
    ops = {c["id"]: c for c in catalog["classes"]}
    by_step = {}
    for op in catalog["classes"]:
        by_step.setdefault(op["flow_step"], []).append(op["id"])
    problems = []
    steps = {}
    for code, card in cards.items():
        text = assigned_text(card, by_file)
        draft = (card.get("draft") or {}).get("body", "")
        if not text:
            problems.append(f"{code}: no assigned text on the site")
        step_ops = by_step.get(code, [])
        for op in step_ops:
            if not (ROOT / "standards/bcreq-manual-classes" / ops[op]["file"]).is_file():
                problems.append(f"{op}: contract file {ops[op]['file']} missing")
        steps[code] = {
            "title": card["step"], "mode": card["mode"], "file": (card.get("published") or card.get("draft"))["file"],
            "size_kb": round(len(text.encode("utf-8")) / 1024, 1), "sha256": sha(text),
            "operations": step_ops,
            "contract_files_exist": all((ROOT / "standards/bcreq-manual-classes" / ops[o]["file"]).is_file() for o in step_ops),
            "contracts_in_assigned_text": CONTRACT_MARK in text,
            "contracts_in_comparison_draft": CONTRACT_MARK in draft,
            "ops_named_in_assigned_text": [o for o in step_ops if o in text],
            "ops_named_in_draft": [o for o in step_ops if o in draft],
            "stubs_in_assigned_text": active_stubs(text),
            "stubs_in_draft": active_stubs(draft),
            "section_standard_links": len(re.findall(r"bcreq-sections", text)),
            "card_gate": card["gate"], "card_has_actions": bool(card["actions"]), "card_has_prepare": bool(card["prepare"]),
            "card_has_result": bool(card["result"]),
        }
    stages = {}
    assigned = {c: assigned_text(cards[c], by_file) for c in cards}
    for name, stage in STAGES.items():
        gate = stage["gate"]
        criteria = {}
        for number in range(1, stage["criteria"] + 1):
            mark = f"{gate}.{number}"
            criteria[mark] = [c for c in cards if mark in assigned[c]]
            if not criteria[mark]:
                problems.append(f"{mark}: no assigned text reports this criterion")
        gate_owner = [c for c in cards if cards[c]["gate"] != "—" and cards[c]["gate"].startswith(gate)]
        if not gate_owner:
            problems.append(f"{gate}: no site card names this gate")
        stages[name] = {
            "steps": {c: steps[c]["title"] for c in stage["steps"]},
            "sections": stage["sections"], "gate": gate, "gate_card": gate_owner,
            "gate_decision_recorded_by": "БА/согласующий в журнале гейтов (logs/gate-journal.md), модель только советует",
            "criteria_reported_in": criteria,
            "operations": sum((steps[c]["operations"] for c in stage["steps"]), []),
            "all_contract_files_exist": all(steps[c]["contract_files_exist"] for c in stage["steps"]),
            "steps_with_contracts_in_assigned_text": [c for c in stage["steps"] if steps[c]["contracts_in_assigned_text"]],
            "steps_with_contracts_in_draft": [c for c in stage["steps"] if steps[c]["contracts_in_comparison_draft"]],
        }
    sections = {}
    for number, file_name in SECTION_FILES.items():
        path = ROOT / "standards/bcreq-sections" / file_name
        if not path.is_file():
            problems.append(f"section {number}: standard missing")
            continue
        sections[number] = {
            "standard": f"standards/bcreq-sections/{file_name}",
            "checklist_items": section_checklist(path),
            "assigned_texts_linking_standard": [c for c in cards if file_name in assigned[c]],
        }
    gate_ops = {op: {"file_exists": (ROOT / "standards/bcreq-manual-classes" / ops[op]["file"]).is_file(),
                     "flow_step": ops[op]["flow_step"],
                     "named_in_assigned": [c for c in cards if op in assigned[c]]} for op in GATE_OPS}
    profiles = {name: {"in_assigned": [c for c in cards if name in assigned[c]]}
                for name in ACTION_PROFILES}
    for name, item in profiles.items():
        if not item["in_assigned"]:
            problems.append(f"profile {name}: no assigned text carries it")
    fact_terms = {c: len(re.findall(r"(?<![А-Яа-яЁё])ТЗ(?![А-Яа-яЁё])", assigned[c])) for c in cards}
    facts = {
        "kit_version": kit["kit"]["version"], "operations_total": len(ops),
        "operations_with_contract_file": sum((ROOT / "standards/bcreq-manual-classes" / o["file"]).is_file() for o in ops.values()),
        "assigned_total_kb": round(sum(s["size_kb"] for s in steps.values()), 1),
        "stages": stages, "outside_stages": OUTSIDE, "steps": steps, "sections": sections, "gate_cycle_operations": gate_ops,
        "action_profiles": profiles,
        "tz_term_in_assigned_texts": fact_terms,
        "tz_assembly_on_site": any(fact_terms.values()) or any("ТЗ" in " ".join(c["actions"]) + c["prepare"] + c["result"] for c in cards.values()),
        "problems": problems,
    }
    OUT.write_text(json.dumps(facts, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"kit {facts['kit_version']}; operations {facts['operations_with_contract_file']}/{facts['operations_total']} with contract file; assigned {facts['assigned_total_kb']} KB")
    print("stage | step | mode | KB | ops | contract files | contracts in assigned | contracts in draft | stubs assigned | stubs draft")
    for name, stage in STAGES.items():
        for code in stage["steps"]:
            s = steps[code]
            print(" | ".join(str(x) for x in (name, code, s["mode"], s["size_kb"], ",".join(s["operations"]), s["contract_files_exist"],
                                              s["contracts_in_assigned_text"], s["contracts_in_comparison_draft"],
                                              ",".join(s["stubs_in_assigned_text"]) or "-", ",".join(s["stubs_in_draft"]) or "-")))
    for code in OUTSIDE:
        s = steps[code]
        print(" | ".join(str(x) for x in ("вне стадии", code, s["mode"], s["size_kb"], ",".join(s["operations"]), s["contract_files_exist"],
                                          s["contracts_in_assigned_text"], s["contracts_in_comparison_draft"],
                                          ",".join(s["stubs_in_assigned_text"]) or "-", ",".join(s["stubs_in_draft"]) or "-")))
    print("gate criteria reported in:")
    for name, stage in stages.items():
        print(" ", name, stage["gate"], "cards:", stage["gate_card"], {k: v for k, v in stage["criteria_reported_in"].items()})
    print("gate cycle operations:", {k: v["named_in_assigned"] for k, v in gate_ops.items()})
    print("sections:", {k: (v["checklist_items"], v["assigned_texts_linking_standard"]) for k, v in sections.items()})
    print("action profiles:", {k: v["in_assigned"] for k, v in profiles.items()})
    print("ТЗ in assigned texts:", {k: v for k, v in fact_terms.items() if v} or "none", "| assembly on site:", facts["tz_assembly_on_site"])
    print("problems:", problems or "none")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
