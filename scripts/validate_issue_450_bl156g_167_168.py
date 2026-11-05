#!/usr/bin/env python3
"""Issue #450: пересчёт RUN-0085…0087 из записей, публикация, сайт 2.4.0, бэклог.

Числа пересчитываются из оценок судей и ключей в runs/, а не читаются из отчётов.
Обратимость текстов держит ``experiments/issue_450/prompt_changes.py``.
"""
import json, re, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "runs/2026"
REPS = ("r1", "r2", "r3")
PUBLISHED = {
    "prompts/bcreq-review-validation-oneshot.md": "0.3",
    "prompts/bcreq-constitution-governance-oneshot.md": "0.2",
    "prompts/bcreq-context-understanding-stepwise.md": "0.2",
    "prompts/bcreq-fr-documentation-stepwise.md": "0.2",
    "prompts/bcreq-orr-solution-design-stepwise.md": "0.2",
}

def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def recount(n, group=None):
    """{arm: [сдано по повторам]} из judge-scores и judge-key (кейс сдан: нет ни одного false)."""
    res = {}
    for rep in REPS:
        out = RUNS / f"RUN-00{n}/outputs/{rep}"
        key = json.loads((out / "judge-key.json").read_text(encoding="utf-8"))
        for f in sorted(out.glob("judge-scores-*.json")):
            if group and not f.name.endswith(f"-{group}.json"):
                continue
            rows = json.loads(f.read_text(encoding="utf-8"))
            for row in rows:
                for arm, label in key[row["case"]].items():
                    res.setdefault(arm, {}).setdefault(rep, 0)
                    res[arm][rep] += not any(v is False for c, v in row[label].items() if c != "note")
    return {a: [r.get(x, 0) for x in REPS] for a, r in res.items()}


class Published(unittest.TestCase):
    def test_versions(self):
        for path, version in PUBLISHED.items():
            self.assertRegex(read(path), rf"(?m)^version: {re.escape(version)}$", path)

    def test_arm_b_equals_published_body(self):
        strip = lambda t: re.sub(r"\A---\n.*?\n---\n", "", t, count=1, flags=re.S)  # noqa: E731
        for label, path in (("S1", "prompts/bcreq-context-understanding-stepwise.md"),
                            ("S3", "prompts/bcreq-fr-documentation-stepwise.md"),
                            ("S6", "prompts/bcreq-orr-solution-design-stepwise.md")):
            arm = (RUNS / f"RUN-0086/inputs/prompt-{label}-B.md").read_text(encoding="utf-8")
            self.assertEqual(strip(read(path)), strip(arm), path)
        arm = (RUNS / "RUN-0085/inputs/prompt-A3.md").read_text(encoding="utf-8")
        self.assertEqual(strip(read("prompts/bcreq-review-validation-oneshot.md")), strip(arm))
        arm = (RUNS / "RUN-0087/inputs/prompt-B.md").read_text(encoding="utf-8")
        self.assertEqual(strip(read("prompts/bcreq-constitution-governance-oneshot.md")), strip(arm))


class Recount(unittest.TestCase):
    def test_run86_and_87_medians_recomputed(self):
        s = json.loads((RUNS / "RUN-0087/outputs/summary.json").read_text(encoding="utf-8"))
        got = recount("87")
        for arm in ("C", "B"):
            self.assertEqual(got[arm], s["median"][arm]["replicates_passed"], arm)
        s = json.loads((RUNS / "RUN-0086/outputs/summary.json").read_text(encoding="utf-8"))
        for g in ("S1", "S3", "S6"):
            got = recount("86", g)
            for arm in ("C", "B"):
                self.assertEqual(got[arm], s[g]["median"][arm]["replicates_passed"], (g, arm))

    def test_decisions(self):
        s = json.loads((RUNS / "RUN-0085/outputs/summary.json").read_text(encoding="utf-8"))
        self.assertEqual((s["median"]["A3"]["passed"], s["median"]["A3"]["core"]), (59, 11))
        self.assertGreaterEqual(s["median"]["A3"]["passed"], s["median"]["A2"]["passed"])
        self.assertEqual(s["fail_frequency"]["A3"].get("GS-BCREQ-25", 0), 0)
        s86 = json.loads((RUNS / "RUN-0086/outputs/summary.json").read_text(encoding="utf-8"))
        for g in ("S1", "S3", "S6"):
            self.assertEqual(s86[g]["guardrail_R18"], [], g)
            self.assertTrue(s86[g]["publish"], g)
        self.assertEqual(json.loads((RUNS / "RUN-0087/outputs/summary.json").read_text(encoding="utf-8"))["guardrail_R18"], [])

    def test_shv_check_clean(self):
        out = RUNS / "RUN-0086/outputs/shv-check"
        expected = json.loads((out / "expected.json").read_text(encoding="utf-8"))
        for rep in REPS:
            got = json.loads((out / f"{rep}.json").read_text(encoding="utf-8"))
            self.assertEqual({k: v["defect"] for k, v in got.items()}, expected, rep)
        fragments = (out / "fragments.md").read_text(encoding="utf-8")
        self.assertNotRegex(fragments, r"(?m)^#.*(дефект|нарушен|ожидани)", "загрязнённая подача")


class Records(unittest.TestCase):
    def test_metadata_honest(self):
        for n in ("85", "86", "87"):
            meta = (RUNS / f"RUN-00{n}/metadata.yaml").read_text(encoding="utf-8")
            self.assertIn("ba_reviewed: false", meta, n)
            for line in re.findall(r"(?m)^  - ((?:inputs|outputs|logs|feedback)/\S+)$", meta):
                self.assertTrue((RUNS / f"RUN-00{n}" / line).is_file(), line)
            self.assertIn(f"RUN-00{n}`", read("runs/README.md"))

    def test_deviation_logged(self):
        log = (RUNS / "RUN-0086/logs/experiment-log.md").read_text(encoding="utf-8")
        self.assertIn("загрязнённая подача", log)
        self.assertIn("check-discarded", (ROOT / "experiments/issue_450/run0086/tokens.tsv").read_text(encoding="utf-8"))

    def test_budgets(self):
        tok = json.loads(read("experiments/issue_450/tokens-summary.json"))
        for n, limit in (("85", 700_000), ("86", 1_050_000), ("87", 500_000)):
            self.assertLessEqual(tok[n]["total"], limit, n)


class Backlog(unittest.TestCase):
    def setUp(self):
        self.backlog = read("pr-ops/BACKLOG.md")

    def test_chain(self):
        self.assertIn("**Движение по цепочке (на 2026-11-05, issue #450).**", self.backlog)
        for code in ("BL-167", "BL-168"):
            self.assertRegex(self.backlog, rf"(?m)^\| {code} \|.*\| DONE \|")  # PR #451 слит, issue #454
        self.assertIn("BL-156г — `DONE` (PR #451 слит", self.backlog)
        self.assertRegex(self.backlog, r"(?m)^\| BL-157 \|.*\| deferred \(triggered\) \|")

    def test_r18_accepted(self):
        self.assertIn("принято", re.search(r"(?m)^\| \*\*Р-18\*\* \|.*$", self.backlog).group(0))

    def test_rfc(self):
        rfc = read("docs/rfc/2026-11-runtime-product-catalog-golden-set.md")
        self.assertRegex(rfc, r"(?m)^version: 0\.8$")
        self.assertIn("Пробел Р-1 раздела 14.2 снят", rfc)


class Site(unittest.TestCase):
    def test_version_everywhere(self):
        self.assertIn('version: "2.6.0"', read("scripts/generate-pages-data.mjs"))
        self.assertEqual(read("site/index.html").count("v2.6.0"), 2)
        self.assertNotIn("v2.3.0", read("site/index.html"))

    def test_kit_serves_published_prompts(self):
        kit = json.loads(read("site/data/test-kit.json"))
        blob = json.dumps(kit, ensure_ascii=False)
        self.assertIn("Отраслевая практика — на решение БА", blob)
        self.assertNotIn("Индустриально значимые — на решение БА", blob)
        self.assertIn("sections_toc", blob)


if __name__ == "__main__":
    unittest.main(verbosity=1)
