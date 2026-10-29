#!/usr/bin/env python3
"""Acceptance checks for the manual BCREQ class inventory and replay evidence."""
import json
import re
import unittest
import importlib.util
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLASSES = ROOT / "standards/bcreq-manual-classes"
SPEC = importlib.util.spec_from_file_location("issue_403_replay", ROOT / "experiments/issue_403/check_replay.py")
REPLAY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(REPLAY)


class ManualPipeline(unittest.TestCase):
    def test_one_detailed_standard_per_class(self):
        catalog = json.loads((CLASSES / "catalog.json").read_text())
        self.assertEqual(catalog["phases"], ["a-in", "a-core", "a-work", "a-release"])
        entries = catalog["classes"]
        self.assertEqual(len(entries), 39)
        self.assertEqual(len({x["id"] for x in entries}), len(entries))
        missing = [x["file"] for x in entries if not (CLASSES / x["file"]).is_file()]
        self.assertEqual(missing, [], "Detailed class standards are missing")
        actual = {p.name for p in CLASSES.glob("[0-9][0-9]-*.md")}
        self.assertEqual(actual, {x["file"] for x in entries})
        index = (CLASSES / "README.md").read_text()
        for entry in entries:
            with self.subTest(entry=entry["id"]):
                text = (CLASSES / entry["file"]).read_text()
                for section in ("Назначение", "Вход", "Выход", "Алгоритм", "Circuit breakers", "Контекст", "Проверка", "Паттерн"):
                    self.assertIn("## " + section, text)
                examples = re.findall(r"```json\n(.*?)\n```", text, re.S)
                self.assertEqual(len(examples), 2)
                call, payload = [json.loads(example) for example in examples]
                self.assertEqual(call["class"], entry["id"])
                self.assertIn(call["phase"], entry["phases"])
                self.assertIsInstance(call["class_input"], dict)
                self.assertIsInstance(payload, dict)
                self.assertIn(entry["inputs"], text)
                self.assertIn(entry["outputs"], text)
                self.assertTrue((ROOT / entry["existing"]).is_file())
                for phase in entry["phases"]:
                    self.assertIn(f"{phase}/{entry['id']}", index)

    def test_links_in_new_documents(self):
        files = list(CLASSES.glob("*.md"))
        files += list((ROOT / "docs").glob("**/*bcreq-manual*.md"))
        files += [ROOT / "docs/analysis/2026-10-29-bcreq-checkpoint.md"]
        for path in files:
            for target in re.findall(r"\]\(([^\s)]+)\)", path.read_text()):
                if "://" not in target and not target.startswith("#"):
                    self.assertTrue((path.parent / target.split("#")[0]).exists(), f"{path}: {target}")

    def test_replay_is_a_new_authored_result_with_honest_limits(self):
        run = ROOT / "runs/2026/RUN-0078"
        trace = json.loads((run / "outputs/trace.json").read_text())
        entries = json.loads((CLASSES / "catalog.json").read_text())["classes"]
        self.assertEqual({e["class"] for e in trace["events"]}, {c["id"] for c in entries})
        self.assertEqual({e["phase"] for e in trace["events"]}, {"a-in", "a-core", "a-work", "a-release"})
        self.assertEqual(trace["live_human_approvals"], [])
        self.assertEqual(trace["delivery_status"], "DRAFT_AWAITING_HUMAN")
        doc = (run / "outputs/bcreq-draft.md").read_text()
        self.assertEqual(re.findall(r"^## ([1-8])\.", doc, re.M), list("12345678"))
        self.assertEqual(len(re.findall(r"^\| FR-\d+ \|", doc, re.M)), 16)  # FR table + traceability
        self.assertIn("Если записи не будет, сообщение\nне воспроизводится", doc)
        review = json.loads((run / "outputs/criteria-review.json").read_text())["rows"]
        self.assertEqual({r["id"] for r in review}, {f"SC-{i:02}" for i in range(1, 29)})
        self.assertTrue(all(r["evidence"] for r in review))
        self.assertTrue(any(r["result"] == "not_verified" for r in review))
        self.assertEqual(json.loads((run / "logs/check-results.json").read_text()), REPLAY.counters())
        counts = REPLAY.counters()["baseline"]
        self.assertEqual(counts["incidents_total"], 193)
        self.assertEqual(counts["incidents_confirmed"] + counts["incidents_plausible"], 193)
        handoffs = (run / "outputs/handoffs.md").read_text()
        snapshots = re.findall(r'<BCREQ_OUTPUT [^>]+>\n(.*?)\n</BCREQ_OUTPUT>', handoffs, re.S)
        self.assertEqual(len(snapshots), 4)
        final = json.loads(snapshots[-1])
        self.assertEqual(len([e for e in final["upserts"] if e["kind"] == "draft-section"]), 8)
        self.assertEqual(set(final["payload"]), {"full_snapshot", "entity_register", "unresolved", "superseded", "completeness_receipt"})
        self.assertEqual({q["id"] for q in final["unresolved"]}, {f"Q-{i:02}" for i in range(1, 6)})
        self.assertTrue(all(q["text"] and q["owner"] and q["blocks"] for q in final["unresolved"]))
        self.assertIn("RAW-01", final["receipt"]["live_ids"])
        self.assertTrue({f"A-{i:02}" for i in range(1, 8)} <= set(final["receipt"]["live_ids"]))
        self.assertEqual(final["receipt"]["live_ids"], [e["id"] for e in final["upserts"]])
        for entity in [e for e in final["upserts"] if e["kind"] == "draft-section"]:
            self.assertIn(entity["text"], doc)
            self.assertGreater(len(entity["text"]), 100)
        # Every taxonomy identifier in the new run must exist in the actual snapshot.
        ids = {n["id"] for n in json.loads((ROOT / "docs/taxonomy/products.json").read_text())["nodes"]}
        event = next(e for e in trace["events"] if e["class"] == "C05")
        for field in ("domain", "capability", "feature", "atomic_function"):
            self.assertIn(event["output"][field], ids)


class StateProbes(unittest.TestCase):
    def setUp(self):
        self.base, self.slices = REPLAY.fixture()

    def test_full_roundtrip_preserves_every_atom_and_condition(self):
        full = REPLAY.assemble(self.base, self.slices)
        for key, entity in self.base["entities"].items():
            self.assertEqual(full["entities"][key], entity)
        self.assertEqual(full, json.loads(json.dumps(full)))
        self.assertIn("No recording means no notice.", full["entities"]["FR-03"]["text"])

    def test_missing_slice_cannot_be_a_full_handoff(self):
        with self.assertRaises(ValueError):
            REPLAY.assemble(self.base, self.slices[1:])

    def test_wrong_task_and_fork_rejected(self):
        for field, value in (("task", "OTHER"), ("parent", "fork"), ("revision", "r0")):
            with self.subTest(field=field):
                patches = deepcopy(self.slices)
                patches[0][field] = value
                with self.assertRaises(ValueError):
                    REPLAY.assemble(self.base, patches)

    def test_incomplete_entity_unknown_source_duplicate_rejected(self):
        for defect in ("text", "source", "duplicate"):
            with self.subTest(defect=defect):
                patches = deepcopy(self.slices)
                if defect == "text":
                    patches[0]["upserts"][0]["text"] = ""
                elif defect == "source":
                    patches[0]["upserts"][0]["source_ids"] = ["not-read"]
                else:
                    patches[0]["upserts"] *= 2
                with self.assertRaises(ValueError):
                    REPLAY.assemble(self.base, patches)

    def test_deletion_requires_authority_and_must_not_break_dependencies(self):
        patches = deepcopy(self.slices)
        patches[1]["tombstones"] = [dict(id="A-03", reason="remove", authorized_by="BA-fixture")]
        with self.assertRaises(ValueError):
            REPLAY.assemble(self.base, patches)  # FR-03 depends on A-03
        patches[1]["tombstones"] = [dict(id="A-07", reason="remove", authorized_by=None)]
        with self.assertRaises(ValueError):
            REPLAY.assemble(self.base, patches)
        patches[1]["tombstones"][0]["authorized_by"] = "BA-fixture"
        full = REPLAY.assemble(self.base, patches)
        self.assertNotIn("A-07", full["entities"])
        self.assertIn("A-07", full["retired_ids"])

    def test_structural_validity_does_not_detect_reversed_meaning(self):
        patches = deepcopy(self.slices)
        patches[1]["upserts"][0]["text"] = "Notice even when no recording applies."
        full = REPLAY.assemble(self.base, patches)
        # Deliberate boundary: structural receipt cannot certify semantics.
        self.assertEqual(full["entities"]["FR-03"]["text"], patches[1]["upserts"][0]["text"])

    def test_human_approval_positive_and_negative_controls(self):
        candidate = dict(revision="r3", blocking=[], stale_ids=[])
        approval = dict(decision="approve", actor="BA-fixture", actor_kind="human",
                        authority="verified-in-fixture", revision="r3", scope="release", message_locator="fixture-only")
        self.assertTrue(REPLAY.release_allowed(candidate, approval, "BA-fixture", "release"))
        for field, value in (("actor_kind", "model"), ("actor", "other"), ("revision", "r2"),
                             ("scope", "another-task"), ("message_locator", None), ("authority", None)):
            with self.subTest(field=field):
                self.assertFalse(REPLAY.release_allowed(candidate, dict(approval, **{field:value}), "BA-fixture", "release"))
        self.assertFalse(REPLAY.release_allowed(dict(candidate, blocking=["Q-01"]), approval, "BA-fixture", "release"))
        self.assertFalse(REPLAY.release_allowed(dict(candidate, stale_ids=["UC-03"]), approval, "BA-fixture", "release"))
        self.assertFalse(REPLAY.release_allowed(candidate, None, "BA-fixture", "release"))

    def test_two_factors_only_for_disputed_command(self):
        factors = [dict(message_id="m1", actor="BA", revision="r3", time=2, kind="understand_consequence"),
                   dict(message_id="m2", actor="BA", revision="r3", time=3, kind="choose_disputed_option")]
        self.assertTrue(REPLAY.disputed_command_allowed(True, "r3", 1, factors))
        self.assertTrue(REPLAY.disputed_command_allowed(False, "r3", 1, []))
        self.assertFalse(REPLAY.disputed_command_allowed(True, "r3", 1, factors[:1]))
        for changes in ({"message_id":"m1"}, {"revision":"r2"}, {"actor":"other"}, {"time":0}):
            altered = [factors[0], dict(factors[1], **changes)]
            self.assertFalse(REPLAY.disputed_command_allowed(True, "r3", 1, altered))


if __name__ == "__main__":
    unittest.main()
