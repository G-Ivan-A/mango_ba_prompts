#!/usr/bin/env python3
"""Offline acceptance of the IDE-client research; does not execute BA workflows."""
import argparse
import importlib.util
import json
import re
import unittest
from pathlib import Path
from copy import deepcopy
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "experiments/issue_405"
DOCS = ROOT / "docs/analysis/ide-clients-stage-2"


def read_json(path):
    return json.loads(path.read_text())


class Facts(unittest.TestCase):
    def test_sources_have_successful_bounded_observations(self):
        rows = read_json(DATA / "source-observations.json")
        self.assertEqual(len(rows), len({row["id"] for row in rows}))
        self.assertGreaterEqual(len(rows), 30)
        allowed = {"goose-docs.ai", "opencode.ai", "docs.cline.bot"}
        registry = (DOCS / "2026-10-30-sources.md").read_text()
        for row in rows:
            with self.subTest(source=row["id"]):
                self.assertEqual(row["status"], 200)
                self.assertNotIn("error", row)
                self.assertIn(urlparse(row["url"]).hostname, allowed)
                self.assertIn(urlparse(row["resolved_url"]).hostname, allowed)
                self.assertTrue(row["accessed_at"].startswith("2026-10-30T"))
                self.assertRegex(row["sha256"], r"^[a-f0-9]{64}$")
                self.assertTrue(100 < row["bytes"] <= 2_000_000)
                self.assertIn(row["url"], registry)
                self.assertIn("| " + row["id"] + " |", registry)

    def test_comparison_covers_every_client_and_dimension(self):
        rows = read_json(DATA / "comparison.json")
        expected = {(client, dimension)
                    for client in ("goose", "opencode-v1", "cline")
                    for dimension in ("rules", "skills", "memory", "filesystem",
                                      "permissions", "procedures", "debugging", "perimeter")}
        self.assertEqual({(r["client"], r["dimension"]) for r in rows}, expected)
        self.assertEqual(len(rows), len(expected))
        sources = {r["id"] for r in read_json(DATA / "source-observations.json")}
        comparison = (DOCS / "2026-10-30-comparison.md").read_text()
        for row in rows:
            self.assertEqual(row["level"], "documented")
            self.assertTrue(row["sources"])
            self.assertLessEqual(set(row["sources"]), sources)
            for source in row["sources"]:
                self.assertIn(source, comparison)

    def test_cited_sources_resolve(self):
        ids = {r["id"] for r in read_json(DATA / "source-observations.json")}
        for path in DOCS.glob("*.md"):
            cited = set(re.findall(r"\b[GOL]\d{2}\b", path.read_text()))
            self.assertLessEqual(cited, ids, str(path))

    def test_links_exist(self):
        paths = list(DOCS.glob("*.md")) + list(DATA.glob("*.md"))
        paths += list((DATA / "examples").glob("*.md"))
        paths += [ROOT / "docs/analysis/2026-10-30-ide-clients-stage-2.md"]
        adr = ROOT / "docs/adr/2026-10-adr-016-ide-client-process.md"
        if adr.exists():
            paths.append(adr)
        for path in paths:
            for target in re.findall(r"\]\(([^\s)]+)\)", path.read_text()):
                if "://" in target or target.startswith("#"):
                    continue
                self.assertTrue((path.parent / target.split("#")[0]).exists(), f"{path}: {target}")


class Mapping(unittest.TestCase):
    def test_all_classes_preserve_canonical_contracts_and_three_adapters(self):
        canonical = read_json(ROOT / "standards/bcreq-manual-classes/catalog.json")
        mapping = read_json(DATA / "class-mapping.json")
        self.assertEqual(mapping["catalog_version"], canonical["version"])
        self.assertEqual(len(mapping["classes"]), 39)
        self.assertEqual([c["id"] for c in mapping["classes"]],
                         [c["id"] for c in canonical["classes"]])
        report = (DOCS / "2026-10-30-mapping.md").read_text()
        for original, mapped in zip(canonical["classes"], mapping["classes"]):
            with self.subTest(class_id=original["id"]):
                for field, value in original.items():
                    self.assertEqual(mapped[field], value, field)
                self.assertIn("[" + mapped["id"] + " —", report)
                self.assertEqual(set(mapped["adapters"]), {"goose", "opencode-v1", "cline"})
                for client, folder in (("goose", ".agents"), ("opencode-v1", ".opencode"), ("cline", ".cline")):
                    adapter = mapped["adapters"][client]
                    self.assertEqual(adapter["profile"], mapped["profile"])
                    self.assertEqual(adapter["skill_path"],
                                     f"{folder}/skills/bcreq-{mapped['id'].lower()}/SKILL.md")
                    self.assertTrue((ROOT / adapter["body_source"]).is_file())

    def test_example_policies_do_not_grant_execution(self):
        examples = DATA / "examples"
        recipe = read_json(examples / "goose-review.json")
        self.assertEqual(recipe["extensions"], [])
        self.assertNotIn("retry", recipe)
        self.assertNotIn("sub_recipes", recipe)
        config = read_json(examples / "opencode-v1.json")
        for tool in ("bash", "task", "external_directory", "webfetch", "websearch"):
            self.assertEqual(config["permission"][tool], "deny")
        self.assertEqual(config["permission"]["edit"], "ask")
        self.assertEqual(config["agent"]["bcreq-review"]["permission"]["edit"], "deny")
        self.assertFalse(config["autoupdate"])
        self.assertEqual(config["plugin"], [])
        self.assertEqual(config["mcp"], {})
        self.assertFalse(any(p.suffix in {".sh", ".py", ".js", ".ps1"}
                             for p in examples.rglob("*")))
        self.assertFalse(list(DATA.rglob("SKILL.md")), "Examples must stay inactive")

    def test_protections_and_breakers_remain_distinct(self):
        report = (DOCS / "2026-10-30-mapping.md").read_text()
        for number in range(1, 6):
            self.assertEqual(len(re.findall(rf"^\| З{number} —", report, re.M)), 1)
        for number in range(1, 8):
            self.assertIn(f"CB-0.{number}", report)
        self.assertIn("Чужой контекст, CB-0.7", report)
        self.assertIn("Сохранение, З2/C39", report)


class ContractExamples(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location(
            "issue405_reference", ROOT / "experiments/issue_403/check_replay.py")
        cls.reference = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.reference)

    def setUp(self):
        self.data = read_json(DATA / "examples/contract-fixture.json")

    def test_example_full_matches_all_live_bodies(self):
        actual = self.reference.assemble(self.data["base"], self.data["slices"])
        self.assertEqual(actual, self.data["expected_full"])
        self.assertEqual(set(actual["entities"]), {"A-01", "FR-01"})

    def test_missing_parent_foreign_task_and_unapproved_deletion_fail(self):
        for defect in ("parent", "task", "delete", "body"):
            patches = deepcopy(self.data["slices"])
            if defect == "parent":
                patches[0]["parent"] = "missing"
            elif defect == "task":
                patches[0]["task"] = "TASK-B"
            elif defect == "delete":
                patches[0]["tombstones"] = [dict(id="A-01", reason="remove", authorized_by=None)]
            else:
                patches[0]["upserts"][0]["text"] = ""
            with self.subTest(defect=defect), self.assertRaises(ValueError):
                self.reference.assemble(self.data["base"], patches)

    def test_only_current_human_record_allows_fixture_release(self):
        candidate, approval = self.data["candidate"], self.data["approval"]
        allowed = lambda c, a: self.reference.release_allowed(c, a, "BA-fixture", "TASK-A/release")
        self.assertTrue(allowed(candidate, approval))
        self.assertFalse(allowed(candidate, None))
        for field, value in (("revision", "r000"), ("scope", "TASK-B/release"),
                             ("actor_kind", "model"), ("message_locator", None)):
            with self.subTest(field=field):
                self.assertFalse(allowed(candidate, dict(approval, **{field: value})))
        for field in ("blocking", "stale_ids"):
            self.assertFalse(allowed(dict(candidate, **{field: ["FR-01"]}), approval))

    def test_two_factors_require_distinct_ordered_current_messages(self):
        factors = self.data["factors"]
        allowed = lambda f: self.reference.disputed_command_allowed(True, "D-01", "r001", 1, f)
        self.assertTrue(allowed(factors))
        self.assertFalse(allowed(factors[:1]))
        self.assertTrue(self.reference.disputed_command_allowed(False, "D-01", "r001", 1, []))
        for field, value in (("message_id", "M1"), ("revision", "r000"),
                             ("command_id", "D-02"), ("time", 0), ("actor", "other")):
            with self.subTest(field=field):
                self.assertFalse(allowed([factors[0], dict(factors[1], **{field: value})]))

    def test_structural_check_does_not_certify_semantic_preservation(self):
        patches = deepcopy(self.data["slices"])
        patches[0]["upserts"][0]["text"] = "Export even without confirmation."
        actual = self.reference.assemble(self.data["base"], patches)
        # A deliberate negative semantic control: valid structure accepts reversed meaning.
        self.assertNotEqual(actual, self.data["expected_full"])
        self.assertEqual(actual["entities"]["FR-01"]["text"], "Export even without confirmation.")


class Operations(unittest.TestCase):
    def test_requirement_inventory_is_complete_and_resolves(self):
        requirements = read_json(DATA / "requirements.json")
        expected = {f"Q{i:02}" for i in range(1, 18)}
        self.assertEqual({r["id"] for r in requirements}, expected)
        self.assertEqual(len(requirements), len(expected))
        main = (ROOT / "docs/analysis/2026-10-30-ide-clients-stage-2.md").read_text()
        for row in requirements:
            self.assertTrue(row["artifacts"])
            self.assertTrue(row["evidence"])
            self.assertTrue(row["verification"])
            self.assertIn("| " + row["id"] + " —", main)
            for artifact in row["artifacts"]:
                self.assertTrue((ROOT / artifact).is_file(), artifact)

    def test_meta_model_preserves_entities_and_covers_every_class_once(self):
        text = (DOCS / "2026-10-30-meta-model.md").read_text()
        entities = set(re.findall(r"^\| ([A-Z][A-Za-z0-9]+) \|", text, re.M))
        self.assertEqual(entities, {"Product", "System", "Artifact", "Operation", "Skill",
                                    "Process", "Route", "Actor", "Gate", "Contract", "Trace", "M0", "M1", "M2"})
        table = text.split("| Группа классов", 1)[1].split("В машинной приёмке", 1)[0]
        classes = re.findall(r"\bC\d{2}\b", "\n".join(
            line.split("|")[1] for line in table.splitlines() if line.startswith("| C")))
        self.assertEqual(len(classes), 39)
        self.assertEqual(set(classes), {f"C{i:02}" for i in range(1, 40)})
        self.assertIn("SB-6", text)

    def test_risks_and_runtime_admission_are_explicit_and_distinct(self):
        text = (DOCS / "2026-10-30-operations.md").read_text()
        risks = re.findall(r"^\| (R\d{2}) —", text, re.M)
        self.assertEqual(risks, [f"R{i:02}" for i in range(1, 13)])
        probes = re.findall(r"^\| (P\d{2}) \|", text, re.M)
        self.assertEqual(probes, [f"P{i:02}" for i in range(1, 9)])
        self.assertIn("runtime здесь не выполнен", text)
        self.assertIn("Telegram исключён из архитектуры", text)

    def test_hub_sources_are_pinned_and_registered(self):
        registry = (ROOT / "docs/hub-research-dependencies.md").read_text()
        section = registry.split('<a id="ide-stage-2"></a>', 1)[1]
        links = re.findall(r"https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/([^\s)]+)", section)
        self.assertEqual(len(links), 7)
        for link in links:
            self.assertTrue(link.startswith("c105323322d7e3a0450199db28071ea21fa9404d/"))
        self.assertIn("10-theory.md", section)
        self.assertFalse((ROOT / "research").exists())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", type=int, choices=(1, 2, 3), default=3)
    args = parser.parse_args()
    suite = unittest.TestSuite()
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(Facts))
    if args.stage >= 2:
        for checks in (Mapping, ContractExamples):
            suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(checks))
    if args.stage >= 3:
        suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(Operations))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(not result.wasSuccessful())
