#!/usr/bin/env python3
"""Issue #454: the roadmap in RFC-PUB-001 cannot drift from the backlog and the site data.

The RFC is a dated snapshot: when a status or a kit step changes, this check fails and asks
to update the roadmap. Read-only, no network: the production value is the stored audit.
"""
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RFC = "docs/rfc/2026-11-bcreq-prompts-publication-roadmap.md"
UPDATE = f"обновите срез в {RFC}"
LINK = re.compile(r"\[(BL-\d+[а-я]?|Р-\d+)\]\(([^)#]+)#([^)]+)\)")


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def cells(line):
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def table(text, name):
    block = text.split(f"<!-- {name}:start -->")[1].split(f"<!-- {name}:end -->")[0]
    return [cells(line) for line in block.strip().splitlines()[2:]]


def slug(title):
    title = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", title).lower()
    return re.sub(r"[^\w\- ]", "", title).replace(" ", "-")


class Roadmap(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rfc = read(RFC)
        cls.backlog = read("pr-ops/BACKLOG.md")
        cls.kit = json.loads(read("site/data/test-kit.json"))
        cls.rows = {cells(line)[0]: cells(line) for line in cls.backlog.splitlines() if re.match(r"\| BL-\d+", line)}

    def status_of(self, code):
        stage = re.fullmatch(r"(BL-\d+)([а-я])", code)
        if not stage:
            if code.startswith("Р-"):
                row = next(line for line in self.backlog.splitlines() if line.startswith(f"| **{code}** |"))
                return cells(row)[-1]
            return self.rows[code][4]
        found = re.search(rf"{code} — `([^`]+)`", self.backlog)
        self.assertTrue(found, f"{code}: статус этапа не найден в BACKLOG.md")
        return found.group(1)

    def test_every_row_is_a_task_or_a_named_gap(self):
        rows = table(self.rfc, "roadmap")
        self.assertGreaterEqual(len(rows), 10)
        for row in rows:
            with self.subTest(stage=row[0], result=row[1][:40]):
                self.assertEqual(len(row), 7)
                self.assertTrue(LINK.search(row[2]) or "Пробел П-" in row[2] or "Порядок BL-232" in row[2],
                                "строка роадмэпа без задачи и без названного пробела")

    def test_statuses_match_the_backlog(self):
        checked = 0
        for row in table(self.rfc, "roadmap"):
            codes = [code for code, _, _ in LINK.findall(row[2])]
            if not codes:
                self.assertEqual(row[3], "—", row[1])
                continue
            statuses = row[3].split(", ")
            self.assertEqual(len(statuses), len(codes), row[1])
            for code, status in zip(codes, statuses):
                with self.subTest(code=code):
                    self.assertEqual(status, self.status_of(code), f"{code} разошёлся с BACKLOG.md: {UPDATE}")
                    checked += 1
        self.assertGreaterEqual(checked, 10)

    def test_links_resolve(self):
        for code, target, anchor in LINK.findall(self.rfc):
            with self.subTest(code=code):
                text = (ROOT / "docs/rfc" / target).resolve().read_text(encoding="utf-8")
                self.assertIn(anchor, {slug(m) for m in re.findall(r"(?m)^#{1,6} (.+)$", text)})

    def test_coverage_matches_the_kit(self):
        rows = {row[0]: row for row in table(self.rfc, "coverage")}
        self.assertEqual(len(table(self.rfc, "coverage")), len(rows), "шаг указан дважды")
        steps = {step["step"].split()[0]: step for step in self.kit["steps"]}
        self.assertEqual(set(rows), set(steps), f"состав шагов изменился: {UPDATE}")
        self.assertEqual(self.kit["counts"]["steps"], len(rows))
        for code, step in steps.items():
            with self.subTest(step=code):
                published = step.get("published")
                self.assertEqual(rows[code][1], f"`{Path((published or step['draft'])['file']).stem}`")
                self.assertEqual(rows[code][2], step["mode"], UPDATE)
                self.assertEqual(rows[code][3], published["version"] if published else "нет", UPDATE)
                self.assertIn("BL-232", rows[code][7])
        self.assertIn("BL-174", rows["Ш-Р"][7])

    def test_measured_runs_exist(self):
        for row in table(self.rfc, "coverage"):
            for run in re.findall(r"RUN-\d{4}", row[5]):
                self.assertTrue((ROOT / "runs/2026" / run).is_dir(), run)

    def test_audit_backs_the_stated_value(self):
        facts = json.loads(read("experiments/issue_454/audit_flow_coverage.json"))
        self.assertEqual(facts["prod"]["steps_total"], len(self.kit["steps"]))
        current = facts["prod"]["steps_current"]
        self.assertIn(f"**{current} из {facts['prod']['steps_total']}**", self.rfc, UPDATE)
        run = subprocess.run([sys.executable, str(ROOT / "experiments/issue_454/audit_flow_coverage.py"), "--offline"],
                             capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stdout)
        self.assertIn("integrity problems: none", run.stdout)

    def test_plan_covers_the_window(self):
        plan = self.rfc.split("## 6. План на 5–7 ноября")[1].split("## 7. ")[0]
        for day in ("5.11", "6.11", "7.11"):
            self.assertIn(f"| {day} |", plan)
        self.assertIn("(BL-232)", plan, "в плане нет деплоя, который закрывает цель")

    def test_decisions(self):
        decisions = self.rfc.split("## 7. Решения на согласование")[1].split("## 8. ")[0]
        for number in range(1, 5):
            self.assertIn(f"| DEC-454-0{number} |", decisions)
        self.assertRegex(self.rfc, r"(?m)^status: (proposed|in-review|accepted|implemented|rejected)$")


class OwnerConfirmation(unittest.TestCase):
    """Owner comment on PR #455: stages, 8 sections, closure plan, parallel track, readiness verdict."""

    @classmethod
    def setUpClass(cls):
        cls.rfc = read(RFC)
        cls.stages = json.loads(read("experiments/issue_454/audit_stage_contracts.json"))
        cls.backlog = read("pr-ops/BACKLOG.md")

    def section(self, number):
        return self.rfc.split(f"\n## {number}. ")[1].split("\n## ")[0]

    def test_stages_and_sections_are_confirmed(self):
        text = self.section(13)
        for stage in ("A-IN", "A-CORE", "A-WORK", "A-RELEASE"):
            self.assertIn(f"| {stage} |", text)
        for gate in ("Г-IN", "Г-С1", "Г-W", "Выпуск"):
            self.assertIn(gate, text)
        for number in range(1, 9):
            self.assertRegex(text, rf"(?m)^\| {number} \S")
        self.assertIn("Отдельных промптов гейтов нет", text)
        totals = next(line for line in text.splitlines() if line.startswith("| **Итого** |"))
        self.assertEqual(cells(totals)[2], "**41**")

    def test_section_rows_add_up(self):
        rows = [cells(l) for l in self.section(13).splitlines() if re.match(r"\| [1-8] \S", l)]
        self.assertEqual(sum(int(r[2]) for r in rows), 41)
        totals = next(cells(l) for l in self.section(13).splitlines() if l.startswith("| **Итого** |"))
        self.assertEqual(f"**{sum(int(r[5]) for r in rows)}**", totals[5])
        self.assertEqual(f"**{sum(int(r[6]) for r in rows)}**", totals[6])

    def test_gaps_keep_their_tasks(self):
        self.assertIn("У гейта «Выпуск» нет критериев", self.section(5))
        for code in ("BL-233", "BL-234", "BL-173"):
            self.assertIn(code, self.section(14))
            row = next(line for line in self.backlog.splitlines() if line.startswith(f"| {code} |"))
            if code != "BL-233":
                self.assertIn("Р-20", cells(row)[3], f"{code}: Р-20 должно быть в зависимостях")
        self.assertTrue(any(line.startswith("| **Р-20** |") for line in self.backlog.splitlines()))

    def test_decisions_of_the_second_round(self):
        decisions = self.section(7)
        for number in range(5, 10):
            self.assertIn(f"| DEC-454-0{number} |", decisions)

    def test_parallel_track_is_measured(self):
        text = self.section(12)
        self.assertIn("parallel_track_blast_radius", text)
        self.assertIn("Сайт сам не движется", text)

    def test_verdict_follows_run0092_rules(self):
        """Section 15 repeats the preregistered rules: a failed R3' may not read as ready packets."""
        summary = json.loads(read("runs/2026/RUN-0092/outputs/summary.json"))
        rows = [line for line in self.section(15).splitlines() if line.startswith("|")]
        packets = next(row for row in rows if row.startswith("| Пакеты готовы к отправке"))
        if not summary["R3"]["passed"]:
            self.assertIn("**не доказано: BL-174, пакеты правит БА**", packets, UPDATE)
            self.assertIn("пакеты читает и правит БА", self.rfc.replace("\n", " ").replace("**", ""), UPDATE)
        confirmed = next(row for row in rows if row.startswith("| Ш-В получает конституцию"))
        if all(summary[rule]["passed"] for rule in ("R4", "R5", "R6")):
            self.assertIn("доказано с ограничением", confirmed, UPDATE)
        else:
            self.assertIn("не доказано", confirmed, UPDATE)

    def test_verdict_does_not_claim_readiness_without_ba(self):
        text = self.section(15)
        self.assertIn("Однозначной готовности нет", text)
        self.assertIn("**заблокировано: нужен БА**", text)
        ba_runs = [p for p in (ROOT / "runs/2026").glob("RUN-*/metadata.yaml")
                   if re.search(r"(?m)^ba_reviewed: true", p.read_text(encoding="utf-8"))]
        self.assertEqual([], [p.parent.name for p in ba_runs if p.parent.name >= "RUN-0089"],
                         f"появился прогон с ba_reviewed: true, пересмотрите вердикт: {UPDATE}")


class MachineBase(unittest.TestCase):
    """PR #459 went in first: the plan and the verdict must stay consistent with it."""

    @classmethod
    def setUpClass(cls):
        cls.rfc = read(RFC)
        cls.base_rfc = read("docs/rfc/2026-11-bcreq-machine-run-baseline.md")
        cls.backlog = read("pr-ops/BACKLOG.md")
        cls.compare = json.loads(read("experiments/issue_454/kit_vs_machine_base.json"))

    def section(self, number):
        return self.rfc.split(f"\n## {number}. ")[1].split("\n## ")[0]

    def test_stated_difference_matches_the_comparison(self):
        """The number in the text comes from hashes pinned in the runs, not from memory."""
        total, different = self.compare["steps_in_base"], len(self.compare["different"])
        self.assertEqual(self.compare["prod_kit"], "0.6", UPDATE)
        self.assertEqual(len(self.compare["prod_same"]), total, "прод ушёл от текстов базы: " + UPDATE)
        for text in (self.rfc, self.base_rfc):
            self.assertIn(f"{different} шагах из {total}", text.replace("\n", " "), UPDATE)
        self.assertIn(f"{different} шагов из {total}", self.section(5), UPDATE)
        self.assertIn(f"различаются [{different} из {total}]", self.rfc.split("\n## 1. ")[0], UPDATE)

    def test_machine_base_is_not_acceptance(self):
        rows = [line for line in self.section(15).splitlines() if line.startswith("|")]
        real = next(row for row in rows if row.startswith("| Реальные задачи проходят поток"))
        self.assertIn("`partial-success`", real)
        self.assertIn("не приёмка", real)
        kit = next(row for row in rows if row.startswith("| Комплект 0.7 работает на реальных задачах"))
        self.assertIn("**не доказано: BL-157в**", kit)
        for code in ("RUN-0090", "RUN-0091"):
            self.assertIn(f"{code}]", real)
            self.assertTrue((ROOT / f"runs/2026/{code}/outputs/report.md").exists())

    def test_the_decision_and_the_ba_rule_are_written_down(self):
        self.assertIn("| DEC-454-09 |", self.section(7))
        self.assertIn("не читая RUN-0090 и RUN-0091", self.section(6))
        self.assertIn("не считается независимым", self.section(10))
        self.assertIn("DEC-454-05…09", self.backlog)
        self.assertIn("**не читая** RUN-0090", self.base_rfc, "защита от якоря задана в RFC-MR-001")

    def test_classes_are_not_overstated(self):
        self.assertIn("`contact-center` не проверен", self.section(15))
        self.assertIn("**не доказано: BL-173, BL-170**", self.section(15))
        self.assertIn("| DEC-454-08 |", self.section(7))
        self.assertIn("Р-МР-3", self.section(7))

    def test_candidates_wait_for_ba_data(self):
        self.assertIn("Р-МР-4", self.section(12))
        self.assertIn("Кандидаты BL-171 сюда не входят", next(
            line for line in self.backlog.splitlines() if line.startswith("| BL-233 |")))

    def test_chain_shows_the_merged_step_and_its_next_one(self):
        chain = self.backlog.split("**Движение по цепочке (на 2026-11-05, issue #454).**")[1].split("### ")[0]
        for code in ("BL-157г", "BL-170", "BL-171"):
            self.assertIn(code, chain)
        self.assertIn("`review` → `DONE` (PR #459 слит)", chain)
        self.assertIn("создаёт владелец, Р-МР-2", chain)


class Chain(unittest.TestCase):
    """Issue postcondition: previous step, current step, what it opens; statuses reflected."""

    @classmethod
    def setUpClass(cls):
        cls.backlog = read("pr-ops/BACKLOG.md")

    def row(self, prefix):
        return next(line for line in self.backlog.splitlines() if line.startswith(prefix))

    def test_chain_table(self):
        chain = re.split(r"\*\*Движение по цепочке|### Как дать решение", self.backlog.split("**Движение по цепочке (на 2026-11-05, issue #454).**")[1])[0]
        for label in ("Предшествующий (полнота)", "Текущий — закрывается", "Открывает", "Ждёт триггера"):
            self.assertIn(f"| {label}", chain)
        for code in ("BL-156г", "BL-167", "BL-168", "BL-156", "BL-232", "Р-19", "BL-230", "BL-231", "BL-157в", "BL-174"):
            self.assertIn(code, chain)

    def test_previous_step_statuses(self):
        for code in ("BL-167", "BL-168"):
            self.assertIn("| DONE |", self.row(f"| {code} |"), code)
        self.assertIn("| ЧАСТИЧНО |", self.row("| BL-156 |"))
        self.assertIn("BL-156г — `DONE` (PR #451 слит", self.row("| BL-156 |"))

    def test_opened_tasks(self):
        deploy = self.row("| BL-232 |")
        self.assertIn("| P0 | — | TODO |", deploy, "деплой не должен ждать Р-19")
        self.assertIn("| deferred (triggered) |", self.row("| BL-174 |"))
        self.assertTrue(self.row("| **Р-19** |").rstrip().endswith("| ждёт |") or "принято" in self.row("| **Р-19** |"))
        for code in ("BL-157", "BL-174", "BL-230", "BL-231"):
            self.assertIn("Р-19", cells(self.row(f"| {code} |"))[3], f"{code}: Р-19 должно быть в зависимостях")
        self.assertIn("BL-232", cells(self.row("| BL-157 |"))[3], "этап BL-157в ждёт деплоя")

    def test_closure_criterion(self):
        closure = self.backlog.split("**Критерий закрытия.** BL-150…BL-157")[1].split("\n\n")[0]
        self.assertIn("BL-232", closure)
        self.assertIn("BL-174", closure)


class Registration(unittest.TestCase):
    def test_rfc_is_registered_and_linked(self):
        name = Path(RFC).name
        self.assertIn(f"| [RFC-PUB-001]({name}) |", read("docs/rfc/rfc-register.md"))
        self.assertIn(f"`/{RFC}`", read("pr-ops/artifact-map.md"))
        self.assertIn(f"rfc/{name}", read("docs/roadmap.md"))
        amended = read("docs/rfc/2026-11-runtime-product-catalog-golden-set.md")
        self.assertRegex(amended, r"(?m)^## 17\. Поправка 0\.8")
        self.assertIn(f"]({name})", amended)
        self.assertIn("Issue #454", read("CHANGELOG.md"))

    def test_task_statement(self):
        self.assertIn("## DoD", read("experiments/issue_454/task-statement.md"))


if __name__ == "__main__":
    unittest.main(verbosity=1)
