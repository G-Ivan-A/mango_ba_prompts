#!/usr/bin/env python3
"""Регрессионная проверка issue #448: BL-156б, BL-156в (RUN-0084, Ш-В v0.2) и BL-157в.

Проверки:

* RUN-0084 (Р-03): метрики трёх плеч A0/A1/A2 в трёх повторах
  пересчитываются из оценок слепых судей, ключа X/Y/Z и раскладки кейсов;
  медианы, частоты провала и решение по лестнице пред-регистрации
  выводятся из пересчёта, а не берутся из ``summary.json``; таблица
  медиан отчёта совпадает с пересчётом; регрессия GS-BCREQ-25 (A2 3 из 3,
  A0 0 из 3) записана в BL-156г;
* Ш-В v0.2: ``prompts/bcreq-review-validation-oneshot.md`` равен тексту
  плеча A2 из ``runs/2026/RUN-0084/inputs/`` с заменой двух полей
  frontmatter (``shv_v02_changes.published_text()``); SHA-256 плеч равны
  ``mapping.json``; ``revert()`` возвращает текст A0;
* сайт 2.3.0: тестовый набор — 13 карточек в четырёх группах этапов,
  у каждой карточки инструкция для БА (назначение, подготовка, действия,
  результат), копирование кладёт в первую строку имя промпта и шаг;
* BL-157в: ``coding.json`` проходит схему и проверку обезличивания
  ``bl157v_aggregate.check``; ``aggregate.json`` равен пересчёту из
  ``coding.json``; числа разбора (255, 176/75/4, 19/18, 10 на Ш-6, 50)
  совпадают со сводом; сырых выгрузок чатов в репозитории нет;
* бэклог: Р-03 принято, BL-156б и BL-156в — ``review``, BL-156г —
  ``TODO``, BL-157б — ``DONE``, BL-157в — ``deferred (triggered)`` с
  триггером ``ba_reviewed: true``, BL-167 и BL-168 — ``TODO``, Р-18 — ждёт;
* постановка задачи: WBS W-0…W-9 и ответы владельца 1–6.

Запуск: ``python3 scripts/validate_issue_448_bl156_bl157v.py``
"""

import hashlib
import importlib.util
import json
import re
import statistics
import sys
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "runs/2026/RUN-0084"
EXP = ROOT / "experiments/issue_448"
BL157V = EXP / "bl157v"
ANALYSIS = ROOT / "docs/analysis/2026-11-04-bl-157v-chat-analysis.md"
PROMPT = ROOT / "prompts/bcreq-review-validation-oneshot.md"
TEST_KIT = ROOT / "site/data/test-kit.json"
BACKLOG = ROOT / "pr-ops/BACKLOG.md"
MODEL = ROOT / "pr-ops/backlog-ba-model.md"
TASK = EXP / "task-statement.md"
REPLICATES = ("r1", "r2", "r3")
ARMS = ("A0", "A1", "A2")
LABELS = ("X", "Y", "Z")
CRITERIA = ("K1", "K2", "K3", "K4", "K5", "K6")
METRICS = ("passed", "core", "negatives_false_positive")
#: Итог RUN-0084, закреплённый в отчёте, бэклоге и PR #449.
MEDIANS = {
    "A0": {"passed": 54, "core": 9, "negatives_false_positive": 0},
    "A1": {"passed": 55, "core": 9, "negatives_false_positive": 0},
    "A2": {"passed": 56, "core": 10, "negatives_false_positive": 0},
}


def read(path):
    return path.read_text(encoding="utf-8")


def digest(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def not_worse(candidate, control):
    return (candidate["passed"] >= control["passed"] and candidate["core"] >= control["core"]
            and candidate["negatives_false_positive"] <= control["negatives_false_positive"])


def ladder(medians):
    """Лестница пред-регистрации RUN-0084, п. 3 «Правило решения»."""
    if not_worse(medians["A2"], medians["A0"]):
        return "A2"
    if not_worse(medians["A1"], medians["A0"]):
        return "A1"
    return None


class Run0084Test(unittest.TestCase):
    """RUN-0084: решение пересчитывается из оценок судей, а не берётся из отчёта."""

    @classmethod
    def setUpClass(cls):
        v411 = load("v411_for_448", ROOT / "scripts/validate_issue_411_lessons_pipeline.py")
        cls.cases = {c["case-id"]: c for c in v411.golden_cases()}
        cls.mapping = json.loads(read(RUN / "inputs/mapping.json"))
        cls.summary = json.loads(read(RUN / "outputs/summary.json"))
        cls.per = {rep: cls.score(rep) for rep in REPLICATES}

    @classmethod
    def score(cls, rep):
        out = RUN / "outputs" / rep
        key = json.loads(read(out / "judge-key.json"))
        scores = {}
        for item in json.loads(read(out / "judge-scores.json")):
            for label in LABELS:
                scores[(item["case"], key[item["case"]][label])] = item[label]
        result = {}
        for arm in ARMS:
            passed = core = neg_fp = 0
            per = Counter()
            failed = []
            for tid, case_id in sorted(cls.mapping["mapping"].items()):
                case = cls.cases[case_id]
                score = scores[(tid, arm)]
                negative = case["Эталонный вердикт"] == "дефекта нет"
                applicable = [c for c in CRITERIA if not (negative and c == "K2")]
                ok = all(bool(score.get(c)) for c in applicable)
                per.update(c for c in applicable if score.get(c))
                neg_fp += negative and not score.get("K1")
                core += ok and case["Ядро"] == "да"
                passed += ok
                if not ok:
                    failed.append((case_id, [c for c in applicable if not score.get(c)]))
            result[arm] = {"passed": passed, "core": core, "negatives_false_positive": int(neg_fp),
                           "criteria": {c: per[c] for c in CRITERIA}, "failed": failed}
        return result

    def test_mapping_and_prompts(self):
        self.assertEqual(len(self.mapping["mapping"]), 62)
        for arm in ARMS:
            text = read(RUN / f"inputs/prompt-{arm}.md")
            self.assertEqual(digest(text), self.mapping[f"prompt_{arm}"]["sha256"], arm)
        for rep in REPLICATES:
            key = json.loads(read(RUN / "outputs" / rep / "judge-key.json"))
            self.assertEqual(sorted(key), sorted(self.mapping["mapping"]), rep)
            for tid, labels in key.items():
                self.assertEqual(sorted(labels.values()), list(ARMS), f"{rep} {tid}: метки не слепые")

    def test_replicate_metrics_match_scores(self):
        for rep in REPLICATES:
            stored = json.loads(read(RUN / "outputs" / rep / "metrics.json"))
            for arm in ARMS:
                mine = self.per[rep][arm]
                self.assertEqual(mine["passed"], stored[arm]["passed"], f"{rep} {arm}")
                self.assertEqual(mine["core"], int(stored[arm]["core"].split("/")[0]), f"{rep} {arm}")
                self.assertEqual(mine["negatives_false_positive"],
                                 int(stored[arm]["negatives_false_positive"].split("/")[0]), f"{rep} {arm}")
                self.assertEqual(mine["criteria"], {c: int(v.split("/")[0]) for c, v in stored[arm]["criteria"].items()},
                                 f"{rep} {arm}")
                self.assertEqual([c for c, _ in mine["failed"]], [f["case"] for f in stored[arm]["failed"]])

    def medians(self):
        return {arm: {m: int(statistics.median(self.per[rep][arm][m] for rep in REPLICATES)) for m in METRICS}
                for arm in ARMS}

    def test_medians_and_decision(self):
        medians = self.medians()
        self.assertEqual(medians, self.summary["median"])
        self.assertEqual(medians, MEDIANS)
        publish = ladder(medians)
        self.assertEqual(publish, self.summary["decision"]["publish"])
        self.assertEqual(publish, "A2")

    def test_fail_frequency(self):
        freq = {arm: Counter(case for rep in REPLICATES for case, _ in self.per[rep][arm]["failed"]) for arm in ARMS}
        for arm in ARMS:
            self.assertEqual(dict(freq[arm]), self.summary["fail_frequency"][arm], arm)
        # GS-BCREQ-12 — устойчивый дефект Ш-В v0.1 (RUN-0082): 3 из 3 → 1 из 3 у A2.
        self.assertEqual({arm: freq[arm]["GS-BCREQ-12"] for arm in ARMS}, {"A0": 3, "A1": 3, "A2": 1})
        # Регрессия A2 → BL-156г: 3 из 3 у плеча, 0 из 3 у контроля.
        regress = sorted(c for c, n in freq["A2"].items() if n == 3 and freq["A0"][c] == 0)
        self.assertEqual(regress, ["GS-BCREQ-25"])
        # Провалы по K5 (правка нарушает урок): 17 → 7.
        k5 = {arm: sum("K5" in crit for rep in REPLICATES for _, crit in self.per[rep][arm]["failed"]) for arm in ARMS}
        self.assertEqual((k5["A0"], k5["A2"]), (17, 7))

    def test_report_table(self):
        report = read(RUN / "outputs/golden-set-report.md")
        rows = {"passed": "Сдано из 62", "core": "Ядро из 11", "negatives_false_positive": "Ложный дефект из 10"}
        for metric, title in rows.items():
            cells = []
            for arm in ARMS:
                cells += [str(self.per[rep][arm][metric]) for rep in REPLICATES]
                cells.append(f"**{self.medians()[arm][metric]}**")
            self.assertIn(f"| {title} | " + " | ".join(cells) + " |", report, metric)
        self.assertIn("| A2 не хуже A0 | 56 / 10 / 0 | 54 / 9 / 0 | **да** |", report)

    def test_artifacts(self):
        for rel in ("metadata.yaml", "inputs/README.md", "outputs/README.md", "outputs/golden-set-report.md",
                    "logs/experiment-log.md", "logs/executor-instruction.md", "logs/judge-instruction.md",
                    "feedback/review-notes.md"):
            self.assertTrue((RUN / rel).is_file(), rel)
        self.assertIn("ba_reviewed: false", read(RUN / "metadata.yaml"))
        prereg = read(EXP / "run0084/preregistration.md")
        for marker in ("## Правило решения", "если A2 не хуже A0 — публикуется A2", "N = 3"):
            self.assertIn(marker, prereg)


class ShvV02Test(unittest.TestCase):
    """Ш-В v0.2 в `prompts/` — это измеренное плечо A2, а не новый текст."""

    @classmethod
    def setUpClass(cls):
        cls.changes = load("shv_v02_for_448", EXP / "shv_v02_changes.py")
        cls.text = read(PROMPT)

    def test_published_equals_a2(self):
        self.assertEqual(self.text, self.changes.published_text())
        a2 = read(RUN / "inputs/prompt-A2.md")
        strip = lambda t: re.sub(r"\A---\n.*?\n---\n", "", t, count=1, flags=re.S)  # noqa: E731
        self.assertEqual(strip(self.text), strip(a2))
        self.assertRegex(self.text, r"(?m)^version: 0\.2$")
        self.assertRegex(self.text, r"(?m)^updated: 2026-11-04$")

    def test_revert_gives_control(self):
        self.assertEqual(self.changes.revert(self.changes.PATH, self.text), read(RUN / "inputs/prompt-A0.md"))

    def test_rule_present_once(self):
        self.assertEqual(self.text.count(self.changes.RULE), 1)


class SiteTest(unittest.TestCase):
    """Сайт 2.3.0: карточки шагов — инструкция для БА, группы этапов, имя промпта в копии."""

    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(read(TEST_KIT))

    def test_groups(self):
        groups = self.data["groups"]
        self.assertEqual([g["id"] for g in groups], ["g1", "g2", "g3", "g4"])
        steps = [s["step"].split()[0] for s in self.data["steps"]]
        self.assertEqual([code for g in groups for code in g["steps"]], steps)
        for group in groups:
            self.assertEqual(group["count"], len(group["steps"]))
            self.assertTrue(group["title"] and group["outcome"], group["id"])

    def test_cards_are_instructions(self):
        self.assertEqual(len(self.data["steps"]), 13)
        for step in self.data["steps"]:
            for field in ("purpose", "prepare", "result"):
                self.assertTrue(step[field].strip(), f"{step['step']}: {field}")
                # Инструкция для БА — без кодов шагов и классов.
                self.assertNotRegex(step[field], r"\b(?:Ш-[0-9ВРС]+|C\d{2}|L-\d+|GS-BCREQ-\d+)\b", step["step"])
            self.assertGreaterEqual(len(step["actions"]), 2, step["step"])
            self.assertIn(step["group"], {"g1", "g2", "g3", "g4"})

    def test_copy_header_names_prompt(self):
        app = read(ROOT / "site/app.js")
        self.assertIn("await copyText(`<!-- ${variant.id} · ${step.step} -->\\n\\n${body}`);", app)
        self.assertIn('id="process-tabs"', read(ROOT / "site/index.html"))
        for name in ("after-processes-desktop.png", "after-processes-mobile.png", "after-testkit-desktop.png",
                     "after-testkit-mobile.png", "before-processes-desktop.png", "before-testkit-desktop.png"):
            self.assertTrue((ROOT / "site/screenshots/issue-448" / name).is_file(), name)


class Bl157vTest(unittest.TestCase):
    """BL-157в: кодировка правок БА обезличена, свод пересчитывается, числа разбора совпадают."""

    @classmethod
    def setUpClass(cls):
        cls.agg = load("bl157v_for_448", EXP / "bl157v_aggregate.py")
        cls.records = json.loads(read(BL157V / "coding.json"))
        cls.stored = json.loads(read(BL157V / "aggregate.json"))
        cls.doc = read(ANALYSIS)

    def test_schema_and_leaks(self):
        problems = [p for r in self.records for p in self.agg.check(r, "coding.json")]
        self.assertEqual(problems, [])
        keys = Counter((r["export"], r["turn"], r["category"], r["summary"]) for r in self.records)
        self.assertEqual([k for k, n in keys.items() if n > 1], [])

    def test_aggregate_recomputed(self):
        self.assertEqual(self.agg.aggregate(self.records), self.stored)

    def test_numbers_in_analysis(self):
        total = self.stored["records"]
        rel = self.stored["by_relevance"]
        practice = self.stored["practice_not_offered"]
        self.assertEqual((total, rel["закрыто"], rel["частично"], rel["не закрыто"]), (255, 176, 75, 4))
        self.assertEqual((practice["records"], practice["open"], practice["by_step"]["Ш-6"]), (19, 18, 10))
        self.assertEqual(len(self.stored["new_case_candidates"]), 50)
        pct = lambda n: round(100 * n / total)  # noqa: E731
        for marker in (f"**{total} правок**", f"**{rel['закрыто']} ({pct(rel['закрыто'])} %)**",
                       f"**{rel['частично']} ({pct(rel['частично'])} %)**", f"**{rel['не закрыто']}** не закрыты",
                       f"**{practice['records']} раз**", f"{practice['open']} из этих случаев открыты",
                       f"{practice['by_step']['Ш-6']} приходятся на Ш-6",
                       f"{len(self.stored['new_case_candidates'])} кандидатов в golden set"):
            self.assertIn(marker, self.doc)

    def test_no_raw_chats(self):
        # Шесть выгрузок issue #448 остаются вне репозитория; выгрузки прошлых
        # прогонов (RUN-0014, RUN-0019) — их собственные входы, не этот разбор.
        names = {f"chat-export-{export}.json" for export in self.agg.EXPORTS}
        for base in ("experiments", "docs", "runs", "site", "pr-ops"):
            found = sorted(p.relative_to(ROOT).as_posix() for p in (ROOT / base).rglob("chat-export-*")
                           if p.name in names)
            self.assertEqual(found, [], base)


class BacklogTest(unittest.TestCase):
    """Бэклог: движение по цепочке BL-156, BL-157, BL-167, BL-168, Р-03, Р-18."""

    @classmethod
    def setUpClass(cls):
        cls.backlog = read(BACKLOG)
        cls.model = read(MODEL)

    def row(self, code):
        match = re.search(rf"(?m)^\| {re.escape(code)} \|.*$", self.backlog)
        self.assertIsNotNone(match, code)
        return match.group(0)

    def test_rows(self):
        self.assertIn("| принято |", re.search(r"(?m)^\| \*\*Р-03\*\* \|.*$", self.backlog).group(0))
        self.assertIn("ответ 3", re.search(r"(?m)^\| \*\*Р-03\*\* \|.*$", self.backlog).group(0))
        self.assertIsNotNone(re.search(r"(?m)^\| \*\*Р-18\*\* \|.*$", self.backlog))
        bl156 = self.row("BL-156")
        for marker in ("| review |", "BL-156б и BL-156в — `review` (PR #449)", "RUN-0084", "BL-156г — `TODO`",
                       "GS-BCREQ-25"):
            self.assertIn(marker, bl156)
        bl157 = self.row("BL-157")
        for marker in ("| deferred (triggered) |", "BL-157б — `DONE` (PR #447)", "`ba_reviewed: true`"):
            self.assertIn(marker, bl157)
        for code in ("BL-167", "BL-168"):
            self.assertIn("| TODO |", self.row(code), code)

    def card(self, heading):
        self.assertIn(heading, self.model)
        level = heading.split()[0]
        body = self.model.split(heading, 1)[1]
        return re.split(rf"(?m)^#{{2,{len(level)}}} ", body, maxsplit=1)[0]

    def test_cards(self):
        # Статус карточек ### — в строке таблицы BACKLOG (test_rows); у этапа
        # #### — своя строка «Статус».
        stage = self.card("#### BL-156г. Правило «правка без добавлений» и шаги одного процесса")
        self.assertRegex(stage, r"(?m)^\*\*Статус\.\*\* `TODO`")
        for heading in ("### BL-167. Блок «Отраслевая практика — на решение БА» в шагах Ш-1, Ш-3, Ш-6",
                        "### BL-168. Правила многоходовой сессии правок"):
            self.assertIn("**Готово, когда.**", self.card(heading), heading)
        for heading, status in (("#### BL-156б.", "`review` (PR #449)"), ("#### BL-156в.", "`review` (PR #449)"),
                                ("#### BL-157б.", "`DONE`")):
            line = next(line for line in self.model.splitlines() if line.startswith(heading))
            self.assertIn(status, self.card(line), heading)
        self.assertNotIn("BL-156г — `DONE`", self.backlog)


class TaskStatementTest(unittest.TestCase):
    """Постановка задачи #448: WBS и ответы владельца."""

    def test_task(self):
        text = read(TASK)
        self.assertRegex(text, r"(?m)^scope: issue-448$")
        for n in range(10):
            self.assertRegex(text, rf"(?m)^\| W-{n} \|", f"W-{n}")
        answers = re.search(r"\| № \| Рекомендация PR #447 \|.*?\n\n", text, re.S).group(0)
        self.assertEqual(re.findall(r"(?m)^\| (\d) \|", answers), ["1", "2", "3", "4", "5", "6"])
        self.assertIn("Industry Practice Alert", text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
