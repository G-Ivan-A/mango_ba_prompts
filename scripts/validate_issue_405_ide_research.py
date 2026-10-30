#!/usr/bin/env python3
"""Offline acceptance of the IDE-client research; does not execute BA workflows."""
import argparse
import json
import re
import unittest
from pathlib import Path
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
        paths = list(DOCS.glob("*.md")) + [DATA / "plan.md"]
        for path in paths:
            for target in re.findall(r"\]\(([^\s)]+)\)", path.read_text()):
                if "://" in target or target.startswith("#"):
                    continue
                self.assertTrue((path.parent / target.split("#")[0]).exists(), f"{path}: {target}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", type=int, choices=(1, 2, 3), default=3)
    args = parser.parse_args()
    suite = unittest.TestSuite()
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(Facts))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(not result.wasSuccessful())
