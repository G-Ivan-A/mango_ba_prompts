#!/usr/bin/env python3
"""Регрессионная проверка issue #446: BL-157б (тестовый набор этапа 1), RUN-0082, RUN-0083.

Проверки:

* RUN-0082 (Р-03, BL-156б): метрики трёх повторов A и D пересчитываются из
  оценок слепых судей и ключа X/Y; медианы, решения ``publish_typing`` и
  ``publish_draft`` в ``summary.json`` выводятся из пересчёта по правилу
  пред-регистрации; флаг ``TYPING_APPLIED`` валидатора #438 равен
  ``publish_typing``; черновик Ш-В не опубликован в ``prompts/``;
* RUN-0083 (синтетический прогон A-IN): оценки судьи и ключ X/Y дают итог
  P и T; режим Ш-0, Ш-1, Ш-2 в комплекте прогона равен решению по правилу
  пред-регистрации;
* комплект прогона и сайт: ``site/data/test-kit.json`` повторяет таблицу
  «Порядок шагов» комплекта (номер, шаг, режим, файлы); SHA-256 черновиков
  и опубликованных промптов равны файлам; тело черновика — файл без
  frontmatter; опубликованные id есть в ``site/data/prompts.json``;
* регрессия сборщика: ни один id черновика не несёт двойной суффикс
  ``-by-test-by-test`` и ни один заголовок — двойное «(по тесту)»;
* версия сайта в генераторе, ``index.html`` и данных совпадает: 2.2.0 введена
  issue #446, текущая — 2.3.0 (issue #448, карточки шагов и подстраницы).

Запуск: ``python3 scripts/validate_issue_446_test_kit.py``
"""

import hashlib
import importlib.util
import json
import re
import statistics
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT / "docs/ba-processes/bcreq-run-kit.md"
KIT_DIR = KIT.parent
TEST_KIT = ROOT / "site/data/test-kit.json"
PROMPTS_JSON = ROOT / "site/data/prompts.json"
DRAFTS = ROOT / "prompts/drafts"
RUN_0082 = ROOT / "runs/2026/RUN-0082"
RUN_0083 = ROOT / "runs/2026/RUN-0083"
RUN81 = ROOT / "experiments/issue_444/run0081"
REPLICATES = ("r1", "r2", "r3")
#: База DEC-427-11: RUN-0079, версия A (v0.1), N = 1.
BASELINE_0079 = {"passed": 49, "core": 10, "negatives_false_positive": 0}
#: Текущая версия сайта; 2.2.0 — issue #446, 2.3.0 — issue #448.
SITE_VERSION = "2.3.0"
#: Шаги A-IN, режим которых решает RUN-0083.
A_IN = ("Ш-0 Конституция", "Ш-1 Контекст и глоссарий", "Ш-2 Продукты и стейкхолдеры")


def read(path):
    return path.read_text(encoding="utf-8")


def digest(data):
    return hashlib.sha256(data if isinstance(data, bytes) else data.encode("utf-8")).hexdigest()


def load(name, path):
    sys.path.insert(0, str(path.parent))
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def strip_frontmatter(text):
    return re.sub(r"\A---\n.*?\n---\n?", "", text, count=1, flags=re.S).lstrip("\n")


def strip_inline(cell):
    return re.sub(r"[`*]", "", re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", cell)).strip()


def kit_steps(text):
    """Строки таблицы «Порядок шагов» комплекта: словари «заголовок → ячейка»."""
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith("| № |") and "Режим в тесте" in line:
            header = [c.strip() for c in line.strip().strip("|").split("|")]
            rows = []
            for row in lines[index + 2:]:
                if not row.startswith("|"):
                    break
                rows.append(dict(zip(header, [c.strip() for c in row.strip().strip("|").split("|")])))
            return header, rows
    raise AssertionError("комплект: нет таблицы с колонкой «Режим в тесте»")


def link_target(cell):
    match = re.search(r"\]\(([^)#]+)[^)]*\)", cell)
    return (KIT_DIR / match.group(1)).resolve().relative_to(ROOT).as_posix() if match else ""


def median(values):
    return int(statistics.median(values))


class Run0082Test(unittest.TestCase):
    """RUN-0082: решение пересчитывается из оценок судей, а не берётся из отчёта."""

    @classmethod
    def setUpClass(cls):
        cls.score = load("score81_for_446", RUN81 / "score.py")
        cls.cases = {c["case-id"]: c for c in cls.score.load_validator().golden_cases()}
        cls.meta = json.loads(read(RUN_0082 / "inputs/mapping.json"))
        cls.summary = json.loads(read(RUN_0082 / "outputs/summary.json"))
        cls.per = {}
        for rep in REPLICATES:
            out = RUN_0082 / "outputs" / rep
            key = json.loads(read(out / "judge-key.json"))
            scores = {}
            for item in json.loads(read(out / "judge-scores.json")):
                for label in ("X", "Y"):
                    scores[(item["case"], key[item["case"]][label])] = item[label]
            cls.per[rep] = {v: cls.score.score_version(v, cls.meta, cls.cases, scores) for v in ("A", "D")}

    def test_replicate_metrics_match_scores(self):
        for rep in REPLICATES:
            stored = json.loads(read(RUN_0082 / "outputs" / rep / "metrics.json"))
            for version in ("A", "D"):
                for field in ("passed", "core", "negatives_false_positive", "criteria", "prompt_sha256"):
                    self.assertEqual(self.per[rep][version][field], stored[version][field], f"{rep} {version} {field}")

    def recomputed(self):
        ratio = self.score.ratio
        medians = {}
        for version in ("A", "D"):
            rows = {rep: {"passed": self.per[rep][version]["passed"],
                          "core": ratio(self.per[rep][version]["core"])[0],
                          "negatives_false_positive": ratio(self.per[rep][version]["negatives_false_positive"])[0]}
                    for rep in REPLICATES}
            medians[version] = {k: median([rows[r][k] for r in REPLICATES]) for k in BASELINE_0079}
        return medians

    def test_medians_and_decision(self):
        medians = self.recomputed()
        self.assertEqual(medians, self.summary["median"])
        not_worse = lambda c, r: (c["passed"] >= r["passed"] and c["core"] >= r["core"]
                                  and c["negatives_false_positive"] <= r["negatives_false_positive"])
        typing = not_worse(medians["A"], BASELINE_0079)
        draft = not_worse(medians["D"], BASELINE_0079) and not_worse(medians["D"], medians["A"])
        self.assertEqual(self.summary["decision"]["publish_typing"], typing)
        self.assertEqual(self.summary["decision"]["publish_draft"], draft)
        # Итог прогона, закреплённый в отчёте и бэклоге: оба решения — «нет».
        self.assertEqual((typing, draft), (False, False))
        self.assertEqual(medians, {"A": {"passed": 53, "core": 8, "negatives_false_positive": 0},
                                   "D": {"passed": 54, "core": 9, "negatives_false_positive": 0}})

    def test_typing_flag_follows_run(self):
        v438 = load("v438_for_446", ROOT / "scripts/validate_issue_438_step_prompts.py")
        self.assertEqual(v438.TYPING_APPLIED, self.summary["decision"]["publish_typing"])

    def test_draft_not_published(self):
        # Ш-В v0.1 в prompts/ — не текст черновика D.
        published = read(ROOT / "prompts/bcreq-review-validation-oneshot.md")
        self.assertNotEqual(digest(published), self.meta["prompt_D"]["sha256"])
        self.assertNotIn("by-test", re.search(r"(?m)^id: .*$", published).group(0))

    def test_core_fail_frequency(self):
        # Автоматическое второе чтение GS-BCREQ-12 и GS-BCREQ-01 (пункт 3 issue #446).
        freq = self.summary["fail_frequency"]
        for version in ("A", "D"):
            counted = {}
            for rep in REPLICATES:
                for item in self.per[rep][version]["failed"]:
                    counted[item["case"]] = counted.get(item["case"], 0) + 1
            self.assertEqual(counted, freq[version], version)
            self.assertEqual(counted.get("GS-BCREQ-12"), 3, version)
        self.assertEqual((freq["A"]["GS-BCREQ-01"], freq["D"]["GS-BCREQ-01"]), (2, 1))

    def test_report_numbers(self):
        report = read(RUN_0082 / "outputs/golden-set-report.md")
        for marker in ("| Сдано из 62 | 47 | 53 | 54 | **53** | 51 | 56 | 54 | **54** | 49 |",
                       "| Ядро из 11 | 6 | 8 | 10 | **8** | 10 | 8 | 9 | **9** | 10 |",
                       "**Тип гейта в `prompts/` не публикуется**"):
            self.assertIn(marker, report)


class TestKitTest(unittest.TestCase):
    """Сайт: тестовый набор этапа 1 повторяет комплект прогона."""

    @classmethod
    def setUpClass(cls):
        cls.kit_text = read(KIT)
        cls.header, cls.rows = kit_steps(cls.kit_text)
        cls.data = json.loads(read(TEST_KIT))
        cls.prompts = {p["id"]: p for p in json.loads(read(PROMPTS_JSON))["prompts"]}

    def test_rows_match_kit(self):
        self.assertEqual(len(self.rows), 13)
        self.assertEqual(len(self.data["steps"]), len(self.rows))
        version = re.search(r"(?m)^version: (\S+)$", self.kit_text).group(1)
        self.assertEqual(self.data["kit"]["version"], version)
        draft_col = next(h for h in self.header if h.startswith("Черновик"))
        for row, step in zip(self.rows, self.data["steps"]):
            self.assertEqual(step["number"], row["№"])
            self.assertEqual(step["step"], strip_inline(row["Шаг"]))
            self.assertEqual(step["mode"], strip_inline(row["Режим в тесте"]).split()[0])
            published = link_target(row["Промпт для копирования"])
            self.assertEqual((step["published"] or {}).get("file", ""), Path(published).name if published else "")
            self.assertEqual(step["draft"]["sourcePath"], link_target(row[draft_col]), step["step"])
        counts = self.data["counts"]
        self.assertEqual(counts["steps"], 13)
        self.assertEqual(counts["byTest"] + counts["published"], 13)
        self.assertEqual(counts["byTest"], sum(s["mode"] == "by-test" for s in self.data["steps"]))

    def test_texts_match_files(self):
        for step in self.data["steps"]:
            draft = step["draft"]
            content = (ROOT / draft["sourcePath"]).read_bytes()
            self.assertEqual(draft["sha256"], digest(content), draft["file"])
            self.assertEqual(draft["body"], strip_frontmatter(content.decode("utf-8")), draft["file"])
            self.assertTrue(draft["id"].endswith("-by-test"), draft["id"])
            if step["mode"] == "by-test":
                self.assertTrue(draft["body"].strip(), step["step"])
            published = step["published"]
            if published:
                prompt = self.prompts[published["id"]]
                self.assertEqual(published["sha256"], prompt["contentHash"])
                self.assertEqual(published["sha256"], digest((ROOT / prompt["sourcePath"]).read_bytes()))
                self.assertTrue(prompt["body"].strip())
            else:
                self.assertEqual(step["mode"], "by-test", f"{step['step']}: нет v0.1 — только by-test")

    def test_a_in_mode_from_run_0083(self):
        modes = {s["step"]: s["mode"] for s in self.data["steps"]}
        expected = "by-test" if Run0083Test.decision()["by_test"] else "published"
        for step in A_IN:
            self.assertEqual(modes[step], expected, step)
        others = {s: m for s, m in modes.items() if s not in A_IN and not s.startswith("Ш-Р")}
        self.assertEqual(set(others.values()), {"published"}, "вне A-IN режим by-test не измерен")

    def test_no_double_suffix(self):
        # Регрессия: заглушка Ш-Р несла id «…-by-test-by-test» (сборщик до issue #446).
        for path in sorted(DRAFTS.glob("*.md")):
            text = read(path)
            ident = re.search(r"(?m)^id: (.*)$", text)
            if ident:
                self.assertNotIn("-by-test-by-test", ident.group(1), path.name)
            title = re.search(r"(?m)^title: (.*)$", text)
            if title:
                self.assertLessEqual(title.group(1).count("(по тесту)"), 1, path.name)

    def test_site_version(self):
        gen = read(ROOT / "scripts/generate-pages-data.mjs")
        self.assertRegex(gen, rf'version: "{re.escape(SITE_VERSION)}"')
        self.assertIn("runKit:", gen)
        html = read(ROOT / "site/index.html")
        for marker in (f"v{SITE_VERSION}", 'id="bcreq-testkit"', 'id="bcreq-testkit-steps"'):
            self.assertIn(marker, html)
        self.assertEqual(json.loads(read(PROMPTS_JSON))["siteVersion"]["version"], SITE_VERSION)
        app = read(ROOT / "site/app.js")
        for marker in ("data/test-kit.json", "renderTestKit", "copyTestKitPrompt"):
            self.assertIn(marker, app)


class Run0083Test(unittest.TestCase):
    """RUN-0083: синтетический прогон A-IN, P (v0.1) против T (черновики «по тесту»)."""

    @staticmethod
    def decision():
        summary = json.loads(read(RUN_0083 / "outputs/summary.json"))
        return summary["decision"]

    @classmethod
    def setUpClass(cls):
        cls.summary = json.loads(read(RUN_0083 / "outputs/summary.json"))
        cls.key = json.loads(read(RUN_0083 / "outputs/judge-key.json"))
        cls.scores = json.loads(read(RUN_0083 / "outputs/judge-scores.json"))

    def test_decision_from_scores(self):
        arms = {self.key["X"]: "X", self.key["Y"]: "Y"}
        self.assertEqual(set(arms), {"P", "T"})
        criteria = [f"J{n:02d}" for n in range(1, 13)]
        passed = {arm: 0 for arm in arms}
        fails = {arm: [] for arm in arms}
        for arm, label in arms.items():
            self.assertEqual(sorted(self.scores[label]), criteria, label)
            for criterion in criteria:
                verdict = self.scores[label][criterion]["verdict"]
                self.assertIn(verdict, ("pass", "fail"))
                if verdict == "pass":
                    passed[arm] += 1
                else:
                    fails[arm].append(criterion)
        critical = set(self.summary["rule"]["critical"])
        self.assertEqual(critical, {"J03", "J07", "J11"})
        by_test = passed["T"] >= passed["P"] and not critical & set(fails["T"])
        self.assertEqual(self.summary["passed"], passed)
        self.assertEqual(sorted(self.summary["failed"]["T"]), sorted(fails["T"]))
        self.assertEqual(self.summary["decision"]["by_test"], by_test)

    def test_every_t_fail_handled(self):
        handled = self.summary["t_fail_handling"]
        self.assertEqual(sorted(handled), sorted(self.summary["failed"]["T"]))
        for criterion, action in handled.items():
            self.assertRegex(action, r"^(исправлено в черновике|BL-\d+)", criterion)

    def test_artifacts(self):
        for rel in ("metadata.yaml", "inputs/README.md", "outputs/README.md", "outputs/P-transcript.md",
                    "outputs/T-transcript.md", "outputs/report.md", "logs/experiment-log.md",
                    "feedback/review-notes.md"):
            self.assertTrue((RUN_0083 / rel).is_file(), rel)
        meta = read(RUN_0083 / "metadata.yaml")
        self.assertIn("synthetic", meta)
        self.assertIn("ba_reviewed: false", meta)


if __name__ == "__main__":
    unittest.main(verbosity=2)
