#!/usr/bin/env python3
"""Offline contract probes and counters for authored RUN-0078 results.

This does not call an LLM, route BA work, infer semantics, authenticate a user,
or approve delivery. It demonstrates the declared state invariants on finite
fixtures. The prose/trace and SC judgments are independently authored inputs.
"""
from copy import deepcopy
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / "runs/2026/RUN-0078"


def assemble(base, slices):
    """Reference check of a finite snapshot chain, not a production engine."""
    state = deepcopy(base)
    entities = state["entities"]
    known_sources = {s["id"] for s in state["sources"]}
    retired = set(state.get("retired_ids", []))
    seen_revisions = {state["revision"]}
    for patch in slices:
        if patch["task"] != state["task"] or patch["parent"] != state["revision"]:
            raise ValueError("task/revision chain mismatch")
        if patch["revision"] in seen_revisions:
            raise ValueError("revision must advance")
        seen_revisions.add(patch["revision"])
        ids = [x["id"] for x in patch["upserts"]]
        if len(ids) != len(set(ids)):
            raise ValueError("duplicate upsert")
        for removal in patch["tombstones"]:
            key = removal["id"]
            if key not in entities or not removal.get("reason") or not removal.get("authorized_by"):
                raise ValueError("unexplained deletion")
            if key in ids:
                raise ValueError("delete and upsert same entity")
            del entities[key]
            retired.add(key)
        for entity in patch["upserts"]:
            if entity["id"] in retired or not entity.get("text"):
                raise ValueError("reused ID or incomplete entity")
            if not set(entity["source_ids"]) <= known_sources:
                raise ValueError("unknown source")
            entities[entity["id"]] = deepcopy(entity)
        state["revision"] = patch["revision"]
    for entity in entities.values():
        if not set(entity["dependencies"]) <= set(entities):
            raise ValueError("dangling dependency")
    state["retired_ids"] = sorted(retired)
    return state


def release_allowed(candidate, approval, required_actor, required_scope):
    """Trusted fixture identities only; does not implement authentication."""
    return bool(
        approval
        and approval.get("decision") == "approve"
        and approval.get("actor") == required_actor
        and approval.get("actor_kind") == "human"
        and approval.get("authority") == "verified-in-fixture"
        and approval.get("revision") == candidate["revision"]
        and approval.get("scope") == required_scope
        and approval.get("message_locator")
        and not candidate.get("blocking")
        and not candidate.get("stale_ids")
    )


def disputed_command_allowed(disputed, command_id, revision, objection_time, factors):
    if not disputed:
        return True
    if len(factors) != 2:
        return False
    first, second = factors
    return bool(
        first["message_id"] != second["message_id"]
        and first["command_id"] == second["command_id"] == command_id
        and first["revision"] == second["revision"] == revision
        and first["actor"] == second["actor"]
        and first["kind"] == "understand_consequence"
        and second["kind"] == "choose_disputed_option"
        and objection_time < first["time"] < second["time"]
    )


def fixture():
    seed = json.loads((RUN / "inputs/seed.json").read_text())
    entities = {a["id"]: dict(a, conditions=[], dependencies=[]) for a in seed["atoms"]}
    base = dict(task=seed["task"], revision="r0", entities=entities, sources=seed["source_register"])
    fr = dict(id="FR-03", text="Notice only if enabled and actual recording applies.",
              conditions=["notice enabled", "actual recording applies"],
              source_ids=["S-142"], dependencies=["A-03"])
    patches = [
        dict(task=base["task"], parent="r0", revision="r1", upserts=[fr], tombstones=[]),
        dict(task=base["task"], parent="r1", revision="r2", upserts=[dict(fr, text=fr["text"] + " No recording means no notice.")], tombstones=[]),
    ]
    return base, patches


def counters():
    trace = json.loads((RUN / "outputs/trace.json").read_text())
    review = json.loads((RUN / "outputs/criteria-review.json").read_text())
    baseline = (ROOT / "runs/2026/RUN-0074/metadata.yaml").read_text()
    def baseline_int(key):
        return int(re.search(rf"^  {key}: (\d+)$", baseline, re.M)[1])
    counts = {status: sum(row["result"] == status for row in review["rows"])
              for status in ("observed", "not_verified")}
    return {
        "baseline": {key: baseline_int(key) for key in (
            "turns", "iterations", "sessions", "incidents_total", "incidents_prompt",
            "incidents_confirmed", "incidents_plausible", "answers_with_incidents",
            "success_criteria", "golden_cases")},
        "simulation": {"events": len(trace["events"]),
                       "classes_accounted_for": len({e["class"] for e in trace["events"]}),
                       "criteria": counts, "live_human_approvals": len(trace["live_human_approvals"]),
                       "delivery_status": trace["delivery_status"]},
        "comparison_limit": "Author judgments and structural probes; no comparable defect-rate or latency estimate",
    }


def write_handoffs():
    """Serialize the author's complete section bodies, without summarizing."""
    seed = json.loads((RUN / "inputs/seed.json").read_text())
    doc = (RUN / "outputs/bcreq-draft.md").read_text()
    parts = re.split(r"(?=^## [1-8]\.)", doc, flags=re.M)[1:]
    sections = {int(part[3]): part for part in parts}
    blocks = []
    selections = {"a-in":[1,2], "a-core":[1,2,3,4,7],
                  "a-work":list(range(1,9)), "a-release":list(range(1,9))}
    for index, (phase, numbers) in enumerate(selections.items(), 1):
        context_entities = [dict(id="RAW-01", kind="raw-request", text=seed["raw_verbatim"],
                                 conditions=[], source_ids=["S-02"], dependencies=[], status="draft")]
        context_entities += [dict(atom, kind="historical-atom", conditions=[], dependencies=[], status="draft")
                             for atom in seed["atoms"]]
        context_entities += [dict(id=q["id"], kind="question", text=q["text"],
                                  conditions=[], source_ids=q["source_ids"], dependencies=[], status="blocked")
                             for q in seed["open_questions"]]
        context_entities += [dict(conflict, kind="conflict", conditions=[], dependencies=[], status="blocked")
                             for conflict in seed["conflicts"]]
        entities = context_entities + [dict(id=f"SEC-{n}", kind="draft-section", text=sections[n],
                         conditions=["unapproved historical-design projection"],
                         source_ids=[s["id"] for s in seed["source_register"]],
                         dependencies=[], status="draft") for n in numbers]
        completeness = dict(base_revision="authored-r3", slice_revisions=[],
                            live_ids=[e["id"] for e in entities], part_ids=[])
        payload = dict(full_snapshot={"task":seed["task"], "revision":f"handoff-{index}-r3",
                                      "sections":{str(n):sections[n] for n in numbers}},
                       entity_register=[{"id":e["id"],"kind":e["kind"]} for e in entities],
                       unresolved=seed["open_questions"], superseded=[], completeness_receipt=completeness)
        snapshot = dict(task=seed["task"], phase=phase, **{"class":"C12"},
                        revision=f"handoff-{index}-r3", parent_revision="authored-r3",
                        mode="FULL", status="DRAFT", payload=payload,
                        upserts=entities, tombstones=[], preserved_ids=[], stale_ids=[],
                        source_register=seed["source_register"], decisions=[],
                        unresolved=seed["open_questions"],
                        receipt={"base_revision":"authored-r3", "slice_revisions":[],
                                 "live_ids":[e["id"] for e in entities],
                                 "checked_sources":[s["id"] for s in seed["source_register"]],
                                 "unread_sources":["original product manual bodies"],
                                 "checks":["full section body serialization"],
                                 "limitations":["rules must be supplied as full bundle in new chat; source facts unverified"]},
                        recommendation={"next_class":"C13", "reason":"check full bundle and pending prerequisites",
                                        "requires_human":True})
        tag = f'<BCREQ_OUTPUT task="SIM-1106" phase="{phase}" class="C12" revision="handoff-{index}-r3" mode="FULL">'
        blocks.append(tag + "\n" + json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n</BCREQ_OUTPUT>")
    header = "---\nstatus: draft\nversion: 0.1\nupdated: 2026-10-29\ntemperature: 0.1\n---\n\n# Полные проекции handoff из авторского r3\n\nЭто сериализованные тела результата, не четыре дополнительных LLM-вызова.\nДля нового чата дополнительно передать полный bundle правил. Гейты pending.\n\n"
    (RUN / "outputs/handoffs.md").write_text(header + "\n\n".join("```text\n" + b + "\n```" for b in blocks) + "\n")


if __name__ == "__main__":
    result = counters()
    base, patches = fixture()
    full = assemble(base, patches)
    assert len(full["entities"]) == 8
    assert json.loads(json.dumps(full)) == full
    write_handoffs()
    (RUN / "logs/check-results.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))
