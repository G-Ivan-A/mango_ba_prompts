#!/usr/bin/env python3
"""Lightweight acceptance checks for issue #466; automatically discovered by CI.

No PDFs, product KB lookup, reassessment or external dependencies. Functional
hash routing runs the real JS with a small DOM boundary; browser coverage has
a reusable Playwright MCP script in experiments/issue_466/.
"""
from __future__ import annotations

import json
import importlib.util
import re
import subprocess
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RFC = ROOT / "docs/rfc/2026-11-ttz-feasibility-flow.md"


class Structure(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.ids = {}
        self.parents = {}

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        identity = attrs.get("id")
        if identity:
            if identity in self.ids:
                raise AssertionError(f"duplicate ID: {identity}")
            self.ids[identity] = (tag, attrs)
            self.parents[identity] = [x[1] for x in self.stack]
        if tag not in {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}:
            self.stack.append((tag, identity))

    def handle_endtag(self, tag):
        # HTML uses optional endings elsewhere; retain ancestors up to the tag.
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                del self.stack[index:]
                break


class TTZAcceptance(unittest.TestCase):
    def test_independent_groups_and_preserved_anchors(self):
        tree = Structure()
        tree.feed((ROOT / "site/index.html").read_text())
        groups = {key for key, (tag, attrs) in tree.ids.items()
                  if tag == "details" and "standards-group" in attrs.get("class", "").split()}
        self.assertEqual(groups, {"standards-bcreq", "standards-ttz", "standards-industry"})
        for group in groups:
            self.assertIn("standards", tree.parents[group])
            self.assertFalse(groups.intersection(tree.parents[group]))
        for target in ["standard-intro"] + [f"standard-{i}" for i in range(1, 9)]:
            self.assertIn("standards-bcreq", tree.parents[target])
            self.assertEqual(tree.ids[target][1].get("tabindex"), "-1")
        for group, target in [("standards-ttz", "standard-ttz"), ("standards-industry", "standard-industry")]:
            self.assertIn(group, tree.parents[target])
            self.assertEqual(tree.ids[target][1].get("tabindex"), "-1")

    def test_real_router(self):
        subprocess.run(["node", "experiments/issue_466/route_check.js"], cwd=ROOT, check=True)

    def test_router_port_is_reproducible(self):
        spec = importlib.util.spec_from_file_location(
            "port_466", ROOT / "experiments/issue_423/port_site_v2.py")
        port = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(port)
        current = (ROOT / "site/app.js").read_text()
        reveal_old, reveal_new = port.I466.app_js_patches([])[0]
        previous = current.replace(reveal_new, reveal_old).replace(
            '/^(?:[0-9]|ttz)$/', '/^[0-9]$/').replace(
            ', ttz: "standard-ttz"', '')
        self.assertNotEqual(previous, current)
        self.assertEqual(port.port_app(previous), current)
        self.assertEqual(port.port_app(current), current)

    def test_pdf_manifest_and_eight_run_traceability(self):
        text = RFC.read_text()
        for number in (55, 57, 66, 69, 70, 71, 72, 77):
            self.assertIn(f"runs/2026/RUN-{number:04d}/metadata.yaml", text)
        records = json.loads((ROOT / "experiments/issue_466/pdf-manifest.json").read_text())
        self.assertEqual({x["file"] for x in records}, {f"{i}.pdf" for i in (1114, 1115, 1122, 1125)})
        self.assertEqual(sum(x["pages"] for x in records), 362)
        for record in records:
            self.assertRegex(record["sha256"], r"^[0-9a-f]{64}$")
            self.assertIn(record["sha256"], text)
        self.assertFalse(list((ROOT / "experiments/issue_466").rglob("*.pdf")))

    def test_rfc_local_links_exist(self):
        for target in re.findall(r"\]\(([^ )]+)\)", RFC.read_text()):
            if "://" in target or target.startswith("#"):
                continue
            with self.subTest(target=target):
                self.assertTrue((RFC.parent / target.split("#")[0]).exists())

    def test_registered_proposal_and_release(self):
        self.assertIn("status: proposed", RFC.read_text().split("---", 2)[1])
        for path in ("docs/rfc/rfc-register.md", "pr-ops/artifact-map.md", "standards/README.md"):
            self.assertIn(RFC.name, (ROOT / path).read_text())
        for number in (176, 177, 178):
            for path in ("pr-ops/BACKLOG.md", "pr-ops/backlog-ba-model.md"):
                self.assertIn(f"BL-{number}", (ROOT / path).read_text())
        version = json.loads((ROOT / "site/data/stats.json").read_text())["siteVersion"]
        self.assertGreaterEqual(tuple(map(int, version["version"].split("."))), (2, 8, 0))
        self.assertIn("версия сайта 2.8.0", (ROOT / "CHANGELOG.md").read_text())


if __name__ == "__main__":
    unittest.main()
