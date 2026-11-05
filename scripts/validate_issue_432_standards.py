#!/usr/bin/env python3
"""Регрессионная проверка решения Р-14, базового стандарта и профилей (issue #432).

Проверка фиксирует контракт:

* словарь потока: цель раздела 3.4 отнесена к этапам 3–4; раздел 3.7 —
  тип каждого гейта на этапах 1–4, на этапе 1 гейта `код` нет, цель на
  этапе 1 недостижима; раздел 3.8 — виды валидаторов В-1 и В-2,
  вероятность В-2 на каждом этапе, задача BL-160;
* базовый стандарт ``standards/bcreq-prompt-base-standard.md`` (BL-151):
  редакция «по тесту», правила БС-01…БС-NN подряд и у каждого источник;
  каждый фрагмент «КС» дословно есть во всех 39 стандартах классов;
  уроки существуют; реестр runtime подключён ссылкой, SHA в файле нет;
  каждый гейт имеет тип, гейта `код` на этапе 1 нет; доля общей части
  совпадает с измерением;
* профили ``standards/bcreq-prompt-profiles.md`` (BL-152): восемь
  профилей; каждая из 39 операций ровно в одном профиле, название и шаг —
  как в каталоге, отнесение — как в гипотезе #425; у каждого профиля свои
  правила с источником; фрагмент «КС К-NN» дословно есть в стандарте
  операции К-NN, и К-NN относится к этому профилю; таблица «шаги и
  профили» выводится из каталога; таблица триггера B сходится со счётом;
* записи: поправка 0.5 RFC с расхождением таблицы 9.2, реестр runtime
  ссылается на базовый стандарт, бэклог (BL-151, BL-152 — `review` в
  PR #435; BL-160 с карточкой), карта артефактов, README стандартов,
  CHANGELOG.

Запуск: ``python3 scripts/validate_issue_432_standards.py``
"""

import collections
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GLOSSARY = ROOT / "standards/bcreq-flow-glossary.md"
BASE = ROOT / "standards/bcreq-prompt-base-standard.md"
PROFILES = ROOT / "standards/bcreq-prompt-profiles.md"
REFERENCES = ROOT / "standards/bcreq-runtime-references.md"
CLASSES = ROOT / "standards/bcreq-manual-classes"
CATALOG = CLASSES / "catalog.json"
LESSONS = ROOT / "standards/bcreq-lessons/lessons.json"
ARCHETYPES = ROOT / "experiments/issue_425/archetypes.json"
RFC = ROOT / "docs/rfc/2026-11-bcreq-flow-processes-prompts.md"
BACKLOG = ROOT / "pr-ops/BACKLOG.md"
TRACK_B = ROOT / "pr-ops/backlog-ba-model.md"
ARTIFACT_MAP = ROOT / "pr-ops/artifact-map.md"
STANDARDS_README = ROOT / "standards/README.md"
CHANGELOG = ROOT / "CHANGELOG.md"

HEADER = "**Редакция по тесту (#427): действует до ADR обратного согласования.**"
PROFILE_NAMES = ("INGEST", "EXTRACT", "ANALYZE", "ELICIT", "GENERATE", "VERIFY", "TRANSFORM", "RECORD")
GATES = ("Г-IN", "Г-С1", "Г-W", "Выпуск", "G-self", "G-mach")
TYPES = ("`человек`", "`гибрид`", "`llm`", "`код`")
STAGES = ("Этап 1: чат", "Этап 2: агентный клиент", "Этап 3: n8n", "Этап 4: Python-исполнитель")
PR = "[PR #435](https://github.com/G-Ivan-A/mango_ba_prompts/pull/435)"
ISSUE = "[#432](https://github.com/G-Ivan-A/mango_ba_prompts/issues/432)"
CLASS_QUOTE = re.compile(r"КС «([^»]+)»: «([^»]+)»")
OPERATION_QUOTE = re.compile(r"КС (К-\d\d): «([^»]+)»")
LESSON = re.compile(r"\bL-\d\d\b")
SHA = re.compile(r"\b[0-9a-f]{40}\b")


def text(path):
    return path.read_text(encoding="utf-8")


def frontmatter(body):
    block = body.split("---\n", 2)[1]
    return dict(line.split(": ", 1) for line in block.splitlines() if re.match(r"^[a-z-]+: ", line))


def section(body, heading):
    level = len(heading) - len(heading.lstrip("#"))
    rest = body[body.index(heading + "\n") + len(heading) + 1:]
    stop = re.search(rf"^#{{1,{level}}} ", rest, re.M)
    return rest[: stop.start()] if stop else rest


def rows(block):
    result = []
    for line in block.splitlines():
        if not line.startswith("| ") or re.match(r"^\| -", line):
            continue
        result.append([cell.strip() for cell in line.strip().strip("|").split(" | ")])
    return result


def table(block, first, column=None):
    """Строки таблицы, у которой первая ячейка заголовка — ``first`` (и есть колонка ``column``)."""
    data = rows(block)
    for index, row in enumerate(data):
        if row[0] == first and (column is None or column in row):
            header, body = row, []
            for item in data[index + 1:]:
                if len(item) != len(header):
                    break
                body.append(dict(zip(header, item)))
            return body
    raise AssertionError(f"нет таблицы с колонкой «{first}»")


def normalize(value):
    return re.sub(r"\s+", " ", value)


def catalog():
    return {item["id"]: item for item in json.loads(text(CATALOG))["classes"]}


def class_texts():
    result = {}
    for op, item in catalog().items():
        number = op.split("-")[1]
        result[op] = normalize(text(CLASSES / f"{number}-{item['slug']}.md"))
    return result


def lesson_ids():
    data = json.loads(text(LESSONS))
    items = data if isinstance(data, list) else data["lessons"]
    return {item["id"] for item in items}


def expand(cell):
    """«К-14…К-19, К-21» → множество ID."""
    result = set()
    for start, end in re.findall(r"К-(\d\d)…К-(\d\d)", cell):
        result.update(f"К-{n:02d}" for n in range(int(start), int(end) + 1))
    result.update(re.findall(r"К-\d\d", re.sub(r"К-\d\d…К-\d\d", "", cell)))
    return result


def common_share():
    """Доля строк, общих для всех 39 стандартов классов (как в experiments/issue_432)."""
    files = sorted(CLASSES.glob("[0-9][0-9]-*.md"))
    per_file = [[line.rstrip() for line in text(path).splitlines() if line.strip()] for path in files]
    count = collections.Counter(line for lines in per_file for line in set(lines))
    total = sum(len(lines) for lines in per_file)
    shared = sum(1 for lines in per_file for line in lines if count[line] == len(files))
    return shared / total * 100


class Glossary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.body = text(GLOSSARY)

    def test_version(self):
        self.assertEqual(frontmatter(self.body)["version"], "0.2.1")

    def test_goal_is_stages_3_4(self):
        block = section(self.body, "### 3.4. Ключевые гейты")
        self.assertIn("**на этапах 3–4 дорожной карты** все гейты, кроме ключевых", block)
        self.assertIn("#37-типы-гейтов-по-этапам-дорожной-карты", block)

    def test_gate_types_by_stage(self):
        block = section(self.body, "### 3.7. Типы гейтов по этапам дорожной карты")
        data = {row["Гейт"].split(" ")[0]: row for row in table(block, "Гейт")}
        for gate in GATES:
            with self.subTest(gate=gate):
                self.assertIn(gate, data)
                for stage in STAGES:
                    self.assertTrue(any(kind in data[gate][stage] for kind in TYPES), (gate, stage))
                # На этапе 1 гейт `код` исполнить некому (правило 1 раздела 3.7).
                self.assertNotIn("`код`", data[gate]["Этап 1: чат"])
        goal = {row["Этап"]: row for row in table(block, "Этап", "Цель «все неключевые гейты — машинные»")}
        self.assertIn("Недостижима", goal["1"]["Цель «все неключевые гейты — машинные»"])
        self.assertIn("Достижима", goal["4"]["Цель «все неключевые гейты — машинные»"])

    def test_validators_by_stage(self):
        block = section(self.body, "### 3.8. Валидаторы (`.py`) по этапам дорожной карты")
        kinds = [row["Вид"] for row in table(block, "Вид")]
        self.assertTrue(kinds[0].startswith("В-1.") and kinds[1].startswith("В-2."), kinds)
        stages = table(block, "Этап")
        self.assertEqual([row["Этап"][0] for row in stages], ["1", "2", "3", "4"])
        for row in stages:
            with self.subTest(stage=row["Этап"]):
                self.assertRegex(row["Вероятность В-2"], r"\d+ %")
        self.assertIn("**≈0 %**", stages[0]["Вероятность В-2"])
        self.assertIn("BL-160", block)
        self.assertIn("**В-2 пишется как чистая функция.**", block)


class BaseStandard(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.body = text(BASE)
        cls.rules = [row for row in rows(section(cls.body, "## 3. Правила")) if row[0].startswith("БС-")]

    def test_frontmatter_and_header(self):
        fm = frontmatter(self.body)
        self.assertEqual(fm["status"], "draft")
        self.assertEqual(fm["type"], "standard")
        self.assertIn(HEADER, self.body.split("\n## ", 1)[0])

    def test_rules_numbered_with_source(self):
        self.assertEqual([row[0] for row in self.rules], [f"БС-{n:02d}" for n in range(1, len(self.rules) + 1)])
        self.assertGreaterEqual(len(self.rules), 36)
        for row in self.rules:
            with self.subTest(rule=row[0]):
                self.assertEqual(len(row), 3)
                self.assertTrue(row[1] and row[2])
                self.assertTrue(
                    CLASS_QUOTE.search(row[2]) or LESSON.search(row[2]) or "](" in row[2],
                    "источник: строка стандарта класса, урок или контракт",
                )

    def test_class_quotes_in_all_39(self):
        quotes = CLASS_QUOTE.findall(self.body)
        self.assertGreaterEqual(len(quotes), 20)
        texts = class_texts()
        self.assertEqual(len(texts), 39)
        for part, quote in quotes:
            for op, body in texts.items():
                with self.subTest(quote=quote[:40], op=op):
                    self.assertIn(normalize(quote), body)
                    self.assertIn(f"## {part}", body)

    def test_lessons_exist(self):
        known = lesson_ids()
        for lesson in set(LESSON.findall(self.body)):
            with self.subTest(lesson=lesson):
                self.assertIn(lesson, known)

    def test_runtime_registry_by_link(self):
        block = section(self.body, "### 3.4. Источники, цитаты и справочники runtime")
        self.assertIn("(bcreq-runtime-references.md#2-перечень)", block)
        for code in ("И-7", "ТС-1", "ТС-5", "ТС-6", "ТС-7", "только З-2"):
            self.assertIn(code, block)
        self.assertIsNone(SHA.search(self.body), "SHA — только в разделе 1 реестра (ТС-5)")

    def test_stage_one_has_no_code_gate(self):
        rule = {row[0]: row[1] for row in self.rules}
        self.assertIn("Промпт этапа 1 **НЕ ДОЛЖЕН** опираться на гейт `код`", rule["БС-30"])
        self.assertIn("с типом (`человек`, `гибрид`, `llm`, `код`)", rule["БС-29"])
        gates = table(section(self.body, "## 4. Типы гейтов базового стандарта"), "Гейт")
        self.assertEqual(sorted(row["Гейт"] for row in gates), sorted(GATES))
        for row in gates:
            with self.subTest(gate=row["Гейт"]):
                self.assertTrue(any(kind in row["Тип (этап 1)"] for kind in TYPES[:3]))
                self.assertNotIn("`код`", row["Тип (этап 1)"])

    def test_common_part_measured(self):
        stated = re.search(r"\*\*(\d+),(\d) %\*\* непустых строк", self.body)
        self.assertIsNotNone(stated)
        # Допуск: правки стандартов классов (BL-159) сдвигают долю, но не смысл.
        self.assertAlmostEqual(float(f"{stated.group(1)}.{stated.group(2)}"), common_share(), delta=3.0)


class Profiles(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.body = text(PROFILES)
        cls.catalog = catalog()
        block = section(cls.body, "## 3. Операции и профили")
        cls.assignment = table(block, "Операция")
        cls.steps = table(block, "Шаг")
        cls.profile_of = {row["Операция"]: row["Профиль"] for row in cls.assignment}
        cls.sections = {}
        for index, name in enumerate(PROFILE_NAMES, 1):
            heading = next(line for line in cls.body.splitlines() if line.startswith(f"### 2.{index}. {name} "))
            cls.sections[name] = section(cls.body, heading)

    def test_frontmatter_and_header(self):
        self.assertEqual(frontmatter(self.body)["status"], "draft")
        self.assertIn(HEADER, self.body.split("\n## ", 1)[0])
        self.assertIn("(bcreq-prompt-base-standard.md)", self.body.split("\n## ", 1)[0])

    def test_each_operation_in_one_profile(self):
        ops = [row["Операция"] for row in self.assignment]
        self.assertEqual(sorted(ops), sorted(self.catalog))
        self.assertEqual(len(ops), len(set(ops)))
        for row in self.assignment:
            with self.subTest(op=row["Операция"]):
                item = self.catalog[row["Операция"]]
                self.assertIn(row["Профиль"], PROFILE_NAMES)
                self.assertEqual(row["Название"], item["name"])
                self.assertEqual(row["Шаг"], item["flow_step"])

    def test_profile_sections_match_table(self):
        for name, block in self.sections.items():
            with self.subTest(profile=name):
                listed = expand(re.search(r"^Операции: ([^.]+)\.", block, re.M).group(1))
                self.assertEqual(listed, {op for op, profile in self.profile_of.items() if profile == name})

    def test_hypothesis_425(self):
        archetypes = json.loads(text(ARCHETYPES))["archetypes"]
        self.assertEqual(sorted(archetypes), sorted(PROFILE_NAMES))
        previous = {item["history"]["previous_id"]: op for op, item in self.catalog.items()}
        for name, data in archetypes.items():
            with self.subTest(profile=name):
                self.assertEqual(
                    {previous[c] for c in data["classes"]},
                    {op for op, profile in self.profile_of.items() if profile == name},
                )

    def test_own_rules_with_sources(self):
        texts = class_texts()
        known = lesson_ids()
        seen = set()
        for name, block in self.sections.items():
            rules = table(block, "№")
            with self.subTest(profile=name):
                self.assertGreaterEqual(len(rules), 1, "триггер B: профиль без своих правил сливается")
            for rule in rules:
                with self.subTest(rule=rule["№"]):
                    self.assertNotIn(rule["№"], seen)
                    seen.add(rule["№"])
                    source = rule["Источник"]
                    self.assertTrue(OPERATION_QUOTE.search(source) or "](" in source, "нет источника")
                    for op, quote in OPERATION_QUOTE.findall(source):
                        self.assertEqual(self.profile_of[op], name, f"{op} не из профиля {name}")
                        self.assertIn(normalize(quote), texts[op])
                    for lesson in LESSON.findall(source):
                        self.assertIn(lesson, known)

    def test_steps_derived_from_catalog(self):
        expected = collections.defaultdict(set)
        ops = collections.defaultdict(set)
        for op, item in self.catalog.items():
            expected[item["flow_step"]].add(self.profile_of[op])
            ops[item["flow_step"]].add(op)
        self.assertEqual({row["Шаг"] for row in self.steps}, set(expected))
        for row in self.steps:
            with self.subTest(step=row["Шаг"]):
                self.assertEqual(set(row["Профили"].split(", ")), expected[row["Шаг"]])
                self.assertEqual(set(row["Операции"].split(", ")), ops[row["Шаг"]])

    def test_trigger_b(self):
        verdicts = {row["Профиль"]: row for row in table(section(self.body, "## 4. Проверка триггера B"), "Профиль")}
        self.assertEqual(list(verdicts), list(PROFILE_NAMES))
        for name, row in verdicts.items():
            with self.subTest(profile=name):
                self.assertEqual(int(row["Операций"]), sum(1 for p in self.profile_of.values() if p == name))
                self.assertEqual(int(row["Своих правил"]), len(table(self.sections[name], "№")))
                self.assertTrue(row["Вердикт"].startswith("Отдельный"))


class Records(unittest.TestCase):
    def test_rfc_amendment(self):
        block = section(text(RFC), "### Поправка 0.5: решение Р-14 и гейты по этапам (issue #432)")
        self.assertIn("**Расхождение в разделе 9.2 (найдено в BL-152).**", block)
        self.assertIn("bcreq-prompt-profiles.md#3-операции-и-профили", block)

    def test_registry_links_base_standard(self):
        body = text(REFERENCES)
        self.assertIn("(bcreq-prompt-base-standard.md#34-источники-цитаты-и-справочники-runtime)", body)
        self.assertNotIn("ждёт решения Р-14", body)

    def test_backlog(self):
        backlog = text(BACKLOG)
        for task in ("BL-151", "BL-152"):
            with self.subTest(task=task):
                row = re.search(rf"^\| {task} \|.*$", backlog, re.M).group(0)
                self.assertRegex(row, rf"\| (review|DONE) \| {re.escape(ISSUE)}, {re.escape(PR)} \|")  # DONE — PR #439, «закрыть слитые»
                card = text(TRACK_B).split(f"### {task}. ", 1)[1].split("\n### ", 1)[0]
                self.assertIn("**Исполнение.** Issue #432, PR #435", card)
        self.assertRegex(backlog, r"(?m)^\| BL-160 \| \[Валидаторы процесса: чистые функции для гейта `код`\]")
        self.assertIn("### BL-160. Валидаторы процесса: чистые функции для гейта `код`", text(TRACK_B))

    def test_registered(self):
        for path in (BASE, PROFILES):
            name = path.relative_to(ROOT).as_posix()
            with self.subTest(path=name):
                self.assertIn(f"| `/{name}` |", text(ARTIFACT_MAP))
                self.assertIn(f"[`{path.name}`]({path.name})", text(STANDARDS_README))

    def test_changelog(self):
        unreleased = text(CHANGELOG).split("## Unreleased", 1)[1].split("\n## ", 1)[0]
        self.assertIn("### Added — Issue #432:", unreleased)


if __name__ == "__main__":
    result = unittest.main(exit=False, verbosity=2).result
    sys.exit(0 if result.wasSuccessful() else 1)
