#!/usr/bin/env python3
"""Issue #458: машинные прогоны RUN-0090, RUN-0091, RFC-MR-001 и цепочка бэклога.

Вердикт пересчитывается из check.json и judge-scores.json по правилу
пред-регистрации, а не читается из карточки.
"""
import hashlib, json, re, subprocess, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS = {"RUN-0090": "1135", "RUN-0091": "1137"}
GATES = ("Г-IN", "Г-С1", "Г-W", "Выпуск")
FAILED = {
    "RUN-0090": {"J01", "J02", "J03", "J07"},
    "RUN-0091": {"J01", "J02", "J03", "J07", "B4", "B5", "B7"},
}
RFC = "docs/rfc/2026-11-bcreq-machine-run-baseline.md"


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def out(run, name):
    return json.loads(read(f"runs/2026/{run}/outputs/{name}"))


def meta(run):
    return read(f"runs/2026/{run}/metadata.yaml")


def verdict(run):
    """Правило пред-регистрации: `success` недоступен, он требует проверки БА."""
    checks = out(run, "check.json")
    criteria = out(run, "judge-scores.json")["criteria"]
    text = meta(run)
    critical = re.search(r"(?m)^  critical: \[(.*)\]$", text).group(1).split(", ")
    steps = int(re.search(r"(?m)^  steps_done: (\d+)$", text).group(1))
    scripted = all(checks[f"C0{i}"]["pass"] for i in range(1, 9))
    critical_ok = all(criteria[c]["verdict"] == "pass" for c in critical)
    return "works-with-edits" if steps == 12 and scripted and critical_ok else "partial-success"


class Runs(unittest.TestCase):
    def test_verdict_recomputed(self):
        for run in RUNS:
            with self.subTest(run=run):
                self.assertEqual(verdict(run), "partial-success")
                self.assertRegex(meta(run), r"(?m)^  verdict: partial-success$")

    def test_scores_match_card(self):
        for run in RUNS:
            with self.subTest(run=run):
                criteria = out(run, "judge-scores.json")["criteria"]
                failed = {k for k, v in criteria.items() if v["verdict"] != "pass"}
                self.assertEqual(failed, FAILED[run])
                text = meta(run)
                self.assertEqual(int(re.search(r"(?m)^  criteria: (\d+)$", text).group(1)), len(criteria))
                self.assertEqual(int(re.search(r"(?m)^  passed: (\d+)$", text).group(1)), len(criteria) - len(failed))
                listed = re.search(r"(?m)^  failed: \[(.*)\]$", text).group(1).split(", ")
                self.assertEqual(set(listed), failed)

    def test_all_scripted_checks_pass(self):
        for run in RUNS:
            with self.subTest(run=run):
                checks = out(run, "check.json")
                self.assertEqual([k for k in checks if k.startswith("C") and not checks[k]["pass"]], [])

    def test_eight_sections(self):
        for run in RUNS:
            with self.subTest(run=run):
                self.assertEqual(out(run, "check.json")["C01"]["missing_sections"], [])
                text = read(f"runs/2026/{run}/outputs/bcreq.md")
                numbers = set(re.findall(r"(?m)^#{1,3} (?:Раздел )?([1-8])[.\s]", text))
                self.assertEqual(numbers, set("12345678"))

    def test_one_task_one_run(self):
        for run, task in RUNS.items():
            with self.subTest(run=run):
                self.assertRegex(meta(run), rf"(?m)^  id: BCREQ-{task}$")
                other = next(t for t in RUNS.values() if t != task)
                self.assertNotIn(f"BCREQ-{other}", read(f"runs/2026/{run}/outputs/bcreq.md"))
                self.assertTrue(out(run, "check.json")["C07"]["pass"])
                self.assertIn(f"[`{run}`](2026/{run}/metadata.yaml)", read("runs/README.md"))

    def test_gates_not_passed_by_model(self):
        for run in RUNS:
            with self.subTest(run=run):
                text = meta(run)
                self.assertRegex(text, r"(?m)^ba_reviewed: false$")
                self.assertEqual(
                    re.search(r"(?m)^  gates_pending: \[(.*)\]$", text).group(1).split(", "), list(GATES)
                )
                rows = [
                    [cell.strip().strip("`") for cell in line.split("|")[1:]]
                    for line in read(f"runs/2026/{run}/logs/gate-journal.md").splitlines()
                    if line.startswith("| ")
                ]
                gate_rows = [row for row in rows if row[0] in GATES]
                self.assertEqual({row[0] for row in gate_rows}, set(GATES))
                self.assertEqual({row[2] for row in gate_rows}, {"pending"})

    def test_not_ready_for_release(self):
        for run in RUNS:
            with self.subTest(run=run):
                self.assertRegex(
                    read(f"runs/2026/{run}/outputs/release-readiness.md"),
                    r"(ready_for_human_release \| \*\*нет\*\*|Готово к выпуску человеком: нет)",
                )

    def test_prompts_match_snapshot(self):
        # Запись прогона — текст на его коммите: черновики идут дальше, снимок не двигается (issue #454).
        for run in RUNS:
            commit = re.search(r"(?m)^  commit: (\S+)$", meta(run)).group(1)
            for path, digest in re.findall(r"path: (\S+), version: \"[^\"]+\", sha256: ([0-9a-f]{64})", meta(run)):
                with self.subTest(run=run, path=path):
                    text = subprocess.run(["git", "show", f"{commit}:{path}"], cwd=ROOT, capture_output=True, check=True).stdout
                    self.assertEqual(hashlib.sha256(text).hexdigest(), digest)

    def test_prompts_count(self):
        for run in RUNS:
            self.assertEqual(len(re.findall(r"(?m)^  - \{step: ", meta(run))), 12)

    def test_preregistration_rule(self):
        text = read("experiments/issue_458/preregistration.md")
        self.assertIn("`success` в этом прогоне **недоступен**", text)
        for run in RUNS:
            self.assertEqual(read(f"runs/2026/{run}/logs/preregistration.md"), text)


class Rfc(unittest.TestCase):
    def test_status_proposed(self):
        self.assertRegex(read(RFC), r"(?m)^status: proposed$")
        self.assertRegex(read("docs/rfc/rfc-registry.md"), r"(?m)^\| \[RFC-MR-001\]\(.*\| proposed \| \[PR #459\]")

    def test_baseline_is_not_acceptance(self):
        text = read(RFC)
        self.assertIn("**не читая** RUN-0090 и RUN-0091", text)
        self.assertIn("Приёмку\n   даёт только прогон БА (BL-157в)", text)

    def test_decisions_have_recommendation(self):
        text = read(RFC)
        for code in ("Р-МР-1", "Р-МР-2", "Р-МР-3", "Р-МР-4"):
            self.assertRegex(text, rf"(?m)^\| {code} \| .* \| \*\*")

    def test_base_rfc_linked_and_unchanged_status(self):
        text = read("docs/rfc/2026-11-runtime-product-catalog-golden-set.md")
        self.assertRegex(text, r"(?m)^status: accepted$")
        self.assertIn("(2026-11-bcreq-machine-run-baseline.md)", text)


class Backlog(unittest.TestCase):
    def setUp(self):
        self.backlog = read("pr-ops/BACKLOG.md")
        self.model = read("pr-ops/backlog-ba-model.md")

    def status(self, code):
        return re.search(rf"(?m)^\| {code} \|(?:[^|]*\|){{3}} ([^|]+) \|", self.backlog).group(1)

    def test_previous_step_complete(self):
        self.assertIn("BL-156г — `DONE` (PR #451 слит", self.backlog)
        self.assertEqual(self.status("BL-167"), "DONE")
        self.assertEqual(self.status("BL-168"), "DONE")
        self.assertEqual(self.status("BL-156"), "ЧАСТИЧНО")

    def test_current_step(self):
        self.assertIn("BL-157г — `DONE` ([PR #459]", self.backlog)  # PR #459 слит, issue #454
        card = self.model.split("#### BL-157г.", 1)[1].split("\n### ", 1)[0]
        self.assertIn("**Статус.** `DONE` (PR #459 слит, issue #454).", card)

    def test_opened_steps(self):
        self.assertEqual(self.status("BL-157"), "deferred (triggered)")
        self.assertEqual(self.status("BL-170"), "TODO")
        self.assertEqual(self.status("BL-171"), "deferred (triggered)")
        self.assertIn("задачи 1135 и 1137", re.search(r"(?m)^\| BL-157 \|.*$", self.backlog).group(0))

    def test_chain_table(self):
        chain = self.backlog.split("**Движение по цепочке (на 2026-11-05, issue #458).**", 1)[1].split("\n\n", 2)[1]
        for step in ("Предшествующий (полнота)", "Текущий — закрывается", "Открывает"):
            self.assertIn(f"| {step} |", chain)
        for code in ("BL-156г", "BL-167", "BL-168", "BL-157г", "BL-157в", "BL-170", "BL-171"):
            self.assertIn(code, chain)
        self.assertIn("машинный прогон её не закрывает", chain)


if __name__ == "__main__":
    unittest.main(verbosity=2)
