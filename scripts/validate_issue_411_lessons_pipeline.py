#!/usr/bin/env python3
"""Офлайн-приёмка конвейера уроков прогонов BCREQ (issue #411).

Реестр ``standards/bcreq-lessons/lessons.json`` — единый источник (SSOT,
ADR-017). Из него генерируются README реестра, coverage.json, блоки «Уроки
прогонов» в 14 промптах и блоки уроков в 39 классах ручного pipeline. Приёмка
проверяет согласованность цепочки «прогон → урок → промпт → golden set →
сайт», а не качество текста уроков (его проверяет прогон по рубрике):

* схема реестра: последовательные ID, допустимые уровни и статусы, ключи
  промптов, опоры существуют в конституции;
* генерация не устарела: ``build_bcreq_lessons.build(check=True) == 0``, все
  коды ошибок прогонов и пункты инвентаризации сопоставлены урокам;
* правило «розовых слонов»: в правилах, проверках, примерах, блоках промптов,
  golden set и рубрике нет идентификаторов задач, прогонов и чатов;
* golden set по контракту evals: по кейсу на активный урок, негативные кейсы,
  ядро = топ-8 уроков по инцидентам + урок удержания + негативные, вход кейса
  не копирует пример «Не так» из промпта;
* рубрика: бинарные критерии K1–K6 с наблюдаемым признаком и провалом;
* сайт: ``site/data/lessons.json`` совпадает с реестром, шаги процесса
  ссылаются на уроки своих промптов;
* ADR, RFC и аналитический отчёт существуют, RFC зарегистрирован;
* прогон регрессии фиксирует три версии: golden set, рубрики и промпта.
"""

import importlib.util
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LESSONS_DIR = ROOT / "standards/bcreq-lessons"
REGISTRY_PATH = LESSONS_DIR / "lessons.json"
COVERAGE_PATH = LESSONS_DIR / "coverage.json"
GOLDEN = LESSONS_DIR / "golden-set-bcreq-stage1.md"
RUBRIC = LESSONS_DIR / "rubric-bcreq-stage1.md"
CLASSES_DIR = ROOT / "standards/bcreq-manual-classes"
CONSTITUTION = ROOT / "prompts/bcreq-constitution-governance-oneshot.md"
SITE_LESSONS = ROOT / "site/data/lessons.json"
SITE_FLOW = ROOT / "site/data/bcreq-flow.json"
PROCESS_DOC = ROOT / "docs/ba-processes/bcreq-manual-process.md"
REPORT = ROOT / "docs/analysis/2026-10-31-bcreq-pipeline-run-experience-review.md"
RFC_REGISTER = ROOT / "docs/rfc/rfc-register.md"
RUN_DIR = ROOT / "runs/2026/RUN-0079"

LESSON_ID_RE = re.compile(r"^L-(\d{2})$")
LEVELS = {"runtime", "authoring"}
STATUSES = {"active", "proposed"}
#: Число уроков ядра golden set, отбираемых по числу инцидентов.
CORE_TOP = 8
#: Урок удержания правил сессии: всегда в ядре.
CLOSING = "L-32"
VERDICTS = {"дефект", "дефекта нет"}
RUBRIC_CRITERIA = ["K1", "K2", "K3", "K4", "K5", "K6"]


def load_builder():
    spec = importlib.util.spec_from_file_location("build_bcreq_lessons", ROOT / "scripts/build_bcreq_lessons.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BUILDER = load_builder()
REGISTRY = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
COVERAGE = json.loads(COVERAGE_PATH.read_text(encoding="utf-8"))
LESSONS = REGISTRY["lessons"]
ACTIVE = [lesson for lesson in LESSONS if lesson["status"] == "active"]


def frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"---\n(.*?)\n---\n", text, re.S)
    fields = {}
    if match:
        for line in match.group(1).splitlines():
            if ":" in line and not line.startswith((" ", "-")):
                key, value = line.split(":", 1)
                fields[key.strip()] = value.strip().strip('"')
    return fields


def split_row(line: str) -> list[str]:
    return [cell.strip() for cell in re.split(r"(?<!\\)\|", line.strip())[1:-1]]


def tables(path: Path) -> list[tuple[list[str], list[list[str]]]]:
    """Markdown-таблицы файла: (заголовки, строки)."""
    result = []
    lines = path.read_text(encoding="utf-8").splitlines()
    index = 0
    while index < len(lines):
        if lines[index].startswith("|") and index + 1 < len(lines) and re.match(r"^\|\s*-", lines[index + 1]):
            headers = split_row(lines[index])
            rows = []
            index += 2
            while index < len(lines) and lines[index].startswith("|"):
                rows.append(split_row(lines[index]))
                index += 1
            result.append((headers, rows))
        else:
            index += 1
    return result


def golden_cases() -> list[dict]:
    cases = []
    for headers, rows in tables(GOLDEN):
        if headers and headers[0] == "case-id":
            for row in rows:
                cases.append(dict(zip(headers, row)))
    return cases


#: ID кейсов golden set — собственные идентификаторы набора, не ссылки на задачи.
GOLDEN_ID_RE = re.compile(r"\bGS-BCREQ-N?\d+\b")


def task_ids(text: str) -> list[str]:
    """Идентификаторы задач, прогонов и чатов в тексте (правило «розовых слонов»)."""
    return BUILDER.TASK_ID_RE.findall(GOLDEN_ID_RE.sub("", text))


def anchor_present(anchor: str, text: str) -> bool:
    return re.search(rf"(?<![\w-]){re.escape(anchor)}(?![\w])(?!-\d)", text) is not None


def quoted_fragments(text: str, minimum: int = 20) -> list[str]:
    return [fragment for fragment in re.findall(r"«([^«»]+)»", text) if len(fragment) >= minimum]


class RegistryTests(unittest.TestCase):
    def test_ids_are_sequential_and_unique(self):
        numbers = [int(LESSON_ID_RE.match(lesson["id"]).group(1)) for lesson in LESSONS]
        self.assertEqual(numbers, list(range(1, len(LESSONS) + 1)))

    def test_lesson_fields(self):
        keys = set(REGISTRY["prompt_keys"]) | {"all"}
        for lesson in LESSONS:
            with self.subTest(lesson=lesson["id"]):
                self.assertIn(lesson["level"], LEVELS)
                self.assertIn(lesson["status"], STATUSES)
                for field in ("title", "rule", "check", "bad", "good"):
                    self.assertTrue(lesson[field].strip(), field)
                self.assertLessEqual(set(lesson["prompts"]), keys)
                if lesson["status"] == "active":
                    self.assertTrue(lesson["check"].rstrip().endswith("?"), "проверка — вопрос")
                    self.assertTrue(lesson["anchors"])
                    if lesson["level"] == "runtime":
                        self.assertTrue(lesson["prompts"], "активный урок адресован промптам")
                    self.assertEqual(lesson["golden"], [f"GS-BCREQ-{lesson['id'][2:]}"])
                else:
                    # Предложенный урок ждёт решения владельца: в промпты не встроен.
                    self.assertEqual(lesson["prompts"], [])
                    self.assertEqual(lesson["golden"], [])

    def test_prompt_keys_resolve(self):
        for key, rel in REGISTRY["prompt_keys"].items():
            with self.subTest(key=key):
                self.assertTrue((ROOT / rel).is_file(), rel)
        self.assertEqual(len(REGISTRY["prompt_keys"]), 14)

    def test_anchors_exist_in_constitution(self):
        text = BUILDER.PROMPT_BLOCK_RE.sub("\n", CONSTITUTION.read_text(encoding="utf-8"))
        for lesson in LESSONS:
            for anchor in lesson["anchors"]:
                with self.subTest(lesson=lesson["id"], anchor=anchor):
                    self.assertTrue(anchor_present(anchor, text), anchor)

    def test_registry_paths_resolve(self):
        for field in ("adr", "rfc", "golden_set", "rubric"):
            with self.subTest(field=field):
                self.assertTrue((ROOT / REGISTRY[field]).is_file(), REGISTRY[field])

    def test_no_task_ids_in_lesson_text(self):
        for lesson in LESSONS:
            for field in ("title", "rule", "check", "bad", "good"):
                with self.subTest(lesson=lesson["id"], field=field):
                    self.assertEqual(task_ids(lesson[field]), [])


class GenerationTests(unittest.TestCase):
    def test_generated_artifacts_are_fresh(self):
        self.assertEqual(BUILDER.build(check=True), 0, "запустите python3 scripts/build_bcreq_lessons.py")

    def test_every_run_code_and_inventory_item_is_mapped(self):
        for key in ("unmapped_codes", "unregistered_runs", "stale_mappings", "inventory_unmapped"):
            with self.subTest(key=key):
                self.assertFalse(COVERAGE[key])
        self.assertGreater(COVERAGE["incidents_total"], 0)

    def test_prompts_carry_one_clean_block(self):
        for key, rel in REGISTRY["prompt_keys"].items():
            text = (ROOT / rel).read_text(encoding="utf-8")
            with self.subTest(prompt=key):
                self.assertEqual(text.count(BUILDER.PROMPT_START), 1)
                self.assertEqual(text.count(BUILDER.PROMPT_END), 1)
                block = BUILDER.PROMPT_BLOCK_RE.search(text).group()
                self.assertEqual(task_ids(block), [])
                self.assertEqual(frontmatter(ROOT / rel).get("version"), BUILDER.PROMPT_VERSION)

    def test_every_active_runtime_lesson_reaches_a_prompt(self):
        blocks = "".join(
            BUILDER.PROMPT_BLOCK_RE.search((ROOT / rel).read_text(encoding="utf-8")).group()
            for rel in REGISTRY["prompt_keys"].values()
        )
        for lesson in ACTIVE:
            if lesson["level"] == "runtime":
                with self.subTest(lesson=lesson["id"]):
                    self.assertIn(lesson["rule"], blocks)

    def test_classes_carry_lessons_block(self):
        catalog = json.loads((CLASSES_DIR / "catalog.json").read_text(encoding="utf-8"))
        self.assertEqual(len(catalog["classes"]), 39)
        for entry in catalog["classes"]:
            text = (CLASSES_DIR / entry["file"]).read_text(encoding="utf-8")
            with self.subTest(cls=entry["file"]):
                self.assertEqual(text.count(BUILDER.CLASS_START), 1)
                self.assertEqual(task_ids(BUILDER.CLASS_BLOCK_RE.search(text).group()), [])


class GoldenSetTests(unittest.TestCase):
    cases = golden_cases()
    by_id = {case["case-id"]: case for case in cases}

    def test_case_ids_are_unique(self):
        ids = [case["case-id"] for case in self.cases]
        self.assertEqual(len(ids), len(set(ids)))

    def test_one_defect_case_per_active_lesson(self):
        defect = {case["case-id"] for case in self.cases if case["Эталонный вердикт"] == "дефект"}
        expected = {gid for lesson in ACTIVE for gid in lesson["golden"]}
        self.assertEqual(defect, expected)
        for lesson in ACTIVE:
            case = self.by_id[lesson["golden"][0]]
            with self.subTest(lesson=lesson["id"]):
                self.assertEqual(case["Урок"], lesson["id"])
                self.assertTrue(case["Класс дефекта"].startswith(lesson["id"] + " "))

    def test_case_fields_follow_evals_contract(self):
        for case in self.cases:
            with self.subTest(case=case["case-id"]):
                self.assertIn(case["Эталонный вердикт"], VERDICTS)
                fields = ["Вход", "Контекст", "Обоснование эталона", "Источник"]
                if case["Эталонный вердикт"] == "дефект":
                    fields.append("Класс дефекта")
                for field in fields:
                    self.assertTrue(case.get(field, "").strip(" —"), field)
                self.assertIn(case["Ядро"], {"да", "—"})

    def test_negative_cases_exist_and_reference_lessons(self):
        negatives = [case for case in self.cases if case["Эталонный вердикт"] == "дефекта нет"]
        self.assertGreaterEqual(len(negatives), 5)
        known = {lesson["id"] for lesson in LESSONS}
        for case in negatives:
            with self.subTest(case=case["case-id"]):
                self.assertTrue(case["case-id"].startswith("GS-BCREQ-N"))
                referenced = set(re.findall(r"L-\d{2}", case["Урок"]))
                self.assertTrue(referenced)
                self.assertLessEqual(referenced, known)

    def test_core_is_top_lessons_plus_closing_and_negatives(self):
        runtime = [lesson for lesson in ACTIVE if lesson["level"] == "runtime"]
        ranked = sorted(runtime, key=lambda lesson: (-COVERAGE["lessons"][lesson["id"]]["total"], lesson["id"]))
        expected = {lesson["golden"][0] for lesson in ranked[:CORE_TOP]}
        expected.add(next(lesson for lesson in LESSONS if lesson["id"] == CLOSING)["golden"][0])
        core = {case["case-id"] for case in self.cases if case["Ядро"] == "да"}
        core_defects = {cid for cid in core if not cid.startswith("GS-BCREQ-N")}
        self.assertEqual(core_defects, expected)
        self.assertTrue(any(cid.startswith("GS-BCREQ-N") for cid in core), "в ядре есть негативный кейс")

    def test_inputs_do_not_copy_prompt_examples(self):
        lessons = {lesson["id"]: lesson for lesson in LESSONS}
        for case in self.cases:
            for lesson_id in re.findall(r"L-\d{2}", case["Урок"]):
                for fragment in quoted_fragments(lessons[lesson_id]["bad"]):
                    with self.subTest(case=case["case-id"], fragment=fragment[:30]):
                        self.assertNotIn(fragment, case["Вход"])

    def test_no_task_ids(self):
        for path in (GOLDEN, RUBRIC):
            with self.subTest(path=path.name):
                self.assertEqual(task_ids(path.read_text(encoding="utf-8")), [])

    def test_frontmatter_passes_hub_validator(self):
        proc = subprocess.run(["./tools/validate-frontmatter.sh", str(GOLDEN), str(RUBRIC)], cwd=ROOT,
                              capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)


class RubricTests(unittest.TestCase):
    def test_binary_criteria(self):
        rows = next(rows for headers, rows in tables(RUBRIC) if headers[:4] == ["#", "Критерий", "Наблюдаемый признак", "Провал ="])
        self.assertEqual([row[0] for row in rows], RUBRIC_CRITERIA)
        for row in rows:
            with self.subTest(criterion=row[0]):
                self.assertTrue(all(cell.strip() for cell in row))

    def test_threshold_is_a_human_decision(self):
        text = RUBRIC.read_text(encoding="utf-8")
        self.assertIn("решение владельца", text)
        self.assertIn("три версии", text)


class SiteTests(unittest.TestCase):
    site = json.loads(SITE_LESSONS.read_text(encoding="utf-8"))

    def test_site_matches_registry(self):
        site = {lesson["id"]: lesson for lesson in self.site["lessons"]}
        self.assertEqual(set(site), {lesson["id"] for lesson in LESSONS})
        for lesson in LESSONS:
            with self.subTest(lesson=lesson["id"]):
                for field in ("title", "rule", "check", "bad", "good", "golden", "status", "level"):
                    self.assertEqual(site[lesson["id"]][field], lesson[field])
                self.assertEqual(site[lesson["id"]]["total"], COVERAGE["lessons"][lesson["id"]]["total"])
        self.assertEqual(self.site["totals"]["incidents"], COVERAGE["incidents_total"])
        self.assertEqual(self.site["promptCount"], len(REGISTRY["prompt_keys"]))

    def test_site_has_no_run_or_task_ids(self):
        self.assertEqual(task_ids(SITE_LESSONS.read_text(encoding="utf-8")), [])

    def test_steps_point_to_their_prompt_lessons(self):
        flow = json.loads(SITE_FLOW.read_text(encoding="utf-8"))
        site = {lesson["id"]: lesson for lesson in self.site["lessons"]}
        self.assertEqual(len(flow["manual"]["steps"]), 11)
        for step in flow["manual"]["steps"]:
            with self.subTest(step=step["step"]):
                expected = {lid for lid, lesson in site.items() if step["prompt"]["file"] in lesson["prompts"]}
                self.assertTrue(expected)
                self.assertEqual(set(step["lessons"]), expected)

    def test_page_has_lessons_band_and_rules(self):
        html = (ROOT / "site/index.html").read_text(encoding="utf-8")
        self.assertIn('id="bcreq-lessons"', html)
        self.assertIn('href="lessons.css"', html)
        app = (ROOT / "site/app.js").read_text(encoding="utf-8")
        self.assertIn('fetch("data/lessons.json")', app)
        rules = [rule["id"] for rule in json.loads(SITE_FLOW.read_text(encoding="utf-8"))["manual"]["rules"]]
        self.assertEqual(rules, [f"П-{n}" for n in range(1, 11)])
        self.assertIn("### 1.3. Уроки прогонов (этап 1)", PROCESS_DOC.read_text(encoding="utf-8"))


class DecisionTests(unittest.TestCase):
    def test_adr_rfc_and_report_exist(self):
        adr = ROOT / REGISTRY["adr"]
        rfc = ROOT / REGISTRY["rfc"]
        for path in (adr, rfc, REPORT):
            with self.subTest(path=path.name):
                self.assertTrue(path.is_file())
        self.assertTrue(frontmatter(adr).get("decision-type"))
        self.assertTrue(frontmatter(rfc).get("rfc-scope"))
        self.assertIn(rfc.name, RFC_REGISTER.read_text(encoding="utf-8"))

    def test_decision_documents_pass_hub_validator(self):
        paths = [str(ROOT / REGISTRY["adr"]), str(ROOT / REGISTRY["rfc"]), str(REPORT)]
        proc = subprocess.run(["./tools/validate-frontmatter.sh", *paths], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)


class RegressionRunTests(unittest.TestCase):
    def test_run_records_three_versions(self):
        report = RUN_DIR / "outputs/golden-set-report.md"
        self.assertTrue(report.is_file(), report)
        text = report.read_text(encoding="utf-8")
        versions = {
            "golden set": frontmatter(GOLDEN)["version"],
            "рубрика": frontmatter(RUBRIC)["version"],
            "промпт": BUILDER.PROMPT_VERSION,
        }
        for label, version in versions.items():
            with self.subTest(label=label):
                self.assertRegex(text, rf"{label}[^\n]*\b{re.escape(version)}\b")


if __name__ == "__main__":
    unittest.main(verbosity=1 if "-q" in sys.argv else 2, argv=[sys.argv[0]])
