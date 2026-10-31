#!/usr/bin/env python3
"""BCREQ stage metadata and actual catalog filtering regressions (issue 393)."""
import json
import hashlib
from pathlib import Path
import subprocess
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
STAGES = [
    "Приём и контекст",
    "Требования и предварительное согласование",
    "Дизайн решения и оценка",
    "Конституция и управление",
    "Валидация второй ролью",
    "Сценарии вне документа",
]
GROUPS = [
    ["context-understanding-stepwise", "products-impact-analysis-stepwise", "in-understanding-oneshot"],
    ["fr-documentation-stepwise", "nfr-documentation-stepwise", "uc-modeling-stepwise", "core-documentation-oneshot"],
    ["orr-solution-design-stepwise", "constraints-documentation-stepwise", "extra-risk-analysis-stepwise", "uc-modeling-stepwise", "work-solution-design-oneshot"],
    ["constitution-governance-oneshot"],
    ["review-validation-oneshot"],
    ["scenarios-modeling-oneshot"],
]


class StageTests(unittest.TestCase):
    def test_prompt_bytes_preserved_except_new_frontmatter_tags(self):
        baseline = json.loads((ROOT / "experiments/issue_393/prompt-baseline.json").read_text())
        self.assertEqual(set(baseline), {p.name for p in (ROOT / "prompts").glob("bcreq-*.md")})
        for filename, expected in baseline.items():
            text = (ROOT / "prompts" / filename).read_text()
            # Preserve the original metadata/body assertion across the additive
            # issue 395 retrieval contract, verified independently byte for byte.
            text = re.sub(r'\n<!-- issue-395: runtime-fallback -->\n.*?<!-- /issue-395: runtime-fallback -->\n', '', text, flags=re.S)
            opening, meta, body = text.split("---", 2)
            original_meta = re.sub(r"^(?:operation|processes):[^\n]*\n", "", meta, flags=re.M)
            original = "---".join([opening, original_meta, body])
            self.assertEqual(hashlib.sha256(original.encode()).hexdigest(), expected, filename)

    def test_six_stages_and_every_prompt_mapping(self):
        data = json.loads((ROOT / "site/data/prompts.json").read_text())
        self.assertEqual([p["label"] for p in data["filters"]["processes"]], STAGES)
        self.assertEqual(len(data["filters"]["operations"]), 13)
        self.assertEqual(len(data["prompts"]), 14)
        for prompt in data["prompts"]:
            stem = prompt["file"].removeprefix("bcreq-").removesuffix(".md")
            expected = [stage for stage, group in zip(STAGES, GROUPS) if stem in group]
            self.assertTrue(expected, prompt["file"])
            self.assertEqual(prompt["processes"], expected)
            self.assertEqual(prompt["frontmatter"]["processes"], expected)
            self.assertEqual(prompt["operation"]["id"], prompt["frontmatter"]["operation"])
        for process in data["filters"]["processes"]:
            expected = {p["operation"]["id"] for p in data["prompts"] if process["label"] in p["processes"]}
            self.assertEqual(set(process["operations"]), expected)

    def test_actual_catalog_filter_logic(self):
        subprocess.run(["node", "--test", "experiments/issue_393/catalog.test.cjs"], cwd=ROOT, check=True)


if __name__ == "__main__":
    unittest.main()
