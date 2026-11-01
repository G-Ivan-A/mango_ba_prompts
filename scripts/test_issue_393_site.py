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
ACTIVE_STAGES = [
    "A-IN · Приём задачи",
    "A-CORE · Требования",
    "A-WORK · Решение",
    "A-RELEASE · Выпуск",
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
        # Issue #423: the six issue-393 stages stay on the 14 archived prompts
        # (frontmatter untouched); the catalog filter shows the 4 stages of
        # process v0.2 for the 39 active classes.
        data = json.loads((ROOT / "site/data/prompts.json").read_text())
        self.assertEqual([p["label"] for p in data["filters"]["processes"]], ACTIVE_STAGES)
        self.assertEqual(len(data["filters"]["operations"]), 13)
        archived = [p for p in data["prompts"] if p["archived"]]
        active = [p for p in data["prompts"] if not p["archived"]]
        self.assertEqual(len(archived), 14)
        self.assertEqual(len(active), 39)
        for prompt in archived:
            stem = prompt["file"].removeprefix("bcreq-").removesuffix(".md")
            expected = [stage for stage, group in zip(STAGES, GROUPS) if stem in group]
            self.assertTrue(expected, prompt["file"])
            self.assertEqual(prompt["processes"], expected)
            self.assertEqual(prompt["frontmatter"]["processes"], expected)
            self.assertEqual(prompt["operation"]["id"], prompt["frontmatter"]["operation"])
        for prompt in active:
            self.assertTrue(prompt["processes"] and set(prompt["processes"]) <= set(ACTIVE_STAGES), prompt["id"])
        for process in data["filters"]["processes"]:
            expected = {p["operation"]["id"] for p in active if process["label"] in p["processes"]}
            self.assertEqual(set(process["operations"]), expected)

    def test_actual_catalog_filter_logic(self):
        subprocess.run(["node", "--test", "experiments/issue_393/catalog.test.cjs"], cwd=ROOT, check=True)


if __name__ == "__main__":
    unittest.main()
