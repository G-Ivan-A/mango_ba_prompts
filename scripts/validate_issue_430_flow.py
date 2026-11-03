#!/usr/bin/env python3
"""Регрессионная проверка словаря потока, типов гейтов и каталога операций (issue #430).

BL-150, BL-153 и поправка 0.4 RFC #427. Проверка фиксирует контракт:

* словарь потока ``standards/bcreq-flow-glossary.md``: цепочка
  Поток → Процесс → Операция → Артефакт, четыре типа гейта (`человек`,
  `гибрид`, `llm`, `код`), ключевые гейты КГ-1…КГ-4, проверка гипотезы
  #430 (Г-1…Г-5 с вердиктом), таблица гейтов потока с типом и ключевостью,
  префиксы ``К-`` (операция) и ``C`` (код ошибки);
* часть 0 процесса BCREQ: процессы ПБ-0…ПБ-7, ПБ-С с источником, четыре
  гейта стадий с типом и ключевостью, шаги потока Ш-0…Ш-Р, Ш-С; операции
  шагов совпадают с полем ``flow_step`` каталога, все 39 операций покрыты;
* контракт гейтов: у каждого гейта стадии есть тип;
* каталог ``catalog.json`` v0.2 (BL-153): ID ``К-01…К-39`` (кириллическая
  К), ``flow_step`` по таблице 9.2 RFC #427, прежний ID в
  ``history.previous_id``; стандарты классов, реестр классов, контракт
  состояния, процесс и генератор сайта используют новые ID; ID промптов на
  сайте прежние (по ``previous_id``), ``classId`` и ``flowStep`` — новые;
* поправка 0.4 в RFC #427 и реестре RFC; задача BL-159 с чек-листом
  документов в карточке и строкой в BACKLOG; критерий закрытия спринта
  включает BL-159.

Запуск: ``python3 scripts/validate_issue_430_flow.py``
"""

import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GLOSSARY = ROOT / "standards/bcreq-flow-glossary.md"
PROCESS = ROOT / "docs/ba-processes/bcreq-manual-process.md"
GATES = ROOT / "docs/contracts/bcreq-stage-gates.md"
STATE = ROOT / "docs/contracts/bcreq-manual-state.md"
RFC = ROOT / "docs/rfc/2026-11-bcreq-flow-processes-prompts.md"
REGISTER = ROOT / "docs/rfc/rfc-register.md"
CLASSES = ROOT / "standards/bcreq-manual-classes"
CATALOG = CLASSES / "catalog.json"
GENERATOR = ROOT / "scripts/generate-pages-data.mjs"
PROMPTS_JSON = ROOT / "site/data/prompts.json"
TRACK_B = ROOT / "pr-ops/backlog-ba-model.md"
BACKLOG = ROOT / "pr-ops/BACKLOG.md"

TYPES = ("`человек`", "`гибрид`", "`llm`", "`код`")
STAGE_GATES = ("Г-IN", "Г-С1", "Г-W", "Выпуск")
PROCESSES = ("ПБ-0", "ПБ-1", "ПБ-2", "ПБ-3", "ПБ-4", "ПБ-5", "ПБ-6", "ПБ-7", "ПБ-С")
FLOW_STEPS = ("Ш-0", "Ш-1", "Ш-2", "Ш-3", "Ш-4", "Ш-5", "Ш-6", "Ш-7", "Ш-8", "Ш-9", "Ш-В", "Ш-Р", "Ш-С")
GATE_OPERATIONS = ("К-12", "К-13", "К-20", "К-34", "К-39")
OPERATION = re.compile(r"К-\d\d")
LEGACY_OPERATION = re.compile(r"\bC\d\d\b")


def text(path):
    return path.read_text(encoding="utf-8")


def section(body, heading):
    level = len(heading) - len(heading.lstrip("#"))
    rest = body[body.index(heading + "\n") + len(heading) + 1:]
    stop = re.search(rf"^#{{1,{level}}} ", rest, re.M)
    return rest[: stop.start()] if stop else rest


def rows(block):
    """Строки таблиц Markdown без заголовка и разделителя."""
    result = []
    for line in block.splitlines():
        if not line.startswith("| ") or re.match(r"^\| -", line):
            continue
        result.append([cell.strip() for cell in line.strip().strip("|").split(" | ")])
    return result


def table(block, first):
    """Строки таблицы, у которой первая ячейка заголовка — ``first``."""
    data = rows(block)
    for index, row in enumerate(data):
        if row[0] == first:
            header, body = row, []
            for item in data[index + 1:]:
                if len(item) != len(header):
                    break
                body.append(dict(zip(header, item)))
            return body
    raise AssertionError(f"нет таблицы с колонкой «{first}»")


def catalog():
    return json.loads(text(CATALOG))


def rfc_flow_steps():
    """Операция (прежний ID) → шаг потока по таблице 9.2 RFC #427."""
    result = {}
    for row in table(section(text(RFC), "### 9.2. Состав"), "Шаг"):
        for op in re.findall(r"C\d\d", row["Операции (контракты)"]):
            result[op] = row["Шаг"]
    return result


class Glossary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.body = text(GLOSSARY)

    def test_sections(self):
        for heading in (
            "## 1. Цепочка элементов",
            "## 2. Термины",
            "### 3.3. Типы гейта",
            "### 3.4. Ключевые гейты",
            "### 3.5. Проверка гипотезы #430",
            "### 3.6. Гейты потока BCREQ",
            "## 4. Два пространства номеров «Ш-»",
            "## 5. Идентификаторы",
        ):
            with self.subTest(heading=heading):
                self.assertIn(heading + "\n", self.body)
        self.assertIn("**Поток → Процесс (подпроцессы) → Операция → Артефакт**", self.body)

    def test_gate_types(self):
        types = [row["Тип"].split(" ")[0] for row in table(section(self.body, "### 3.3. Типы гейта"), "Тип")]
        self.assertEqual(types, list(TYPES))

    def test_key_gates_and_hypothesis(self):
        key = table(section(self.body, "### 3.4. Ключевые гейты"), "№")
        self.assertEqual([r["№"] for r in key], ["КГ-1", "КГ-2", "КГ-3", "КГ-4"])
        hypothesis = table(section(self.body, "### 3.5. Проверка гипотезы #430"), "№")
        self.assertEqual([r["№"] for r in hypothesis], [f"Г-{n}" for n in range(1, 6)])
        for row in hypothesis:
            with self.subTest(claim=row["№"]):
                self.assertTrue(row["Вердикт"].startswith("Подтверждено"), row["Вердикт"])
                self.assertTrue(row["Доказательство"])
        self.assertIn("**Вердикт: гипотеза подтверждена", self.body)

    def test_flow_gates_typed(self):
        gates = table(section(self.body, "### 3.6. Гейты потока BCREQ"), "Гейт")
        stage = [r for r in gates if r["Гейт"].startswith(STAGE_GATES)]
        self.assertEqual(len(stage), 4)
        for row in gates:
            with self.subTest(gate=row["Гейт"][:12]):
                self.assertTrue(any(t in row["Тип сейчас"] for t in TYPES), row["Тип сейчас"])
                self.assertRegex(row["Ключевой"], r"^(да|нет)")
        for row in stage:
            with self.subTest(gate=row["Гейт"][:12]):
                self.assertTrue(row["Ключевой"].startswith("да"), "ключевые сейчас все четыре гейта стадий")

    def test_identifiers(self):
        block = section(self.body, "## 5. Идентификаторы")
        prefixes = [r["Префикс"] for r in table(block, "Префикс")]
        for prefix in ("`ПБ-`", "`Ш-`", "`Г-`", "`К-`", "`C`", "`И-`", "`ТС-`"):
            with self.subTest(prefix=prefix):
                self.assertIn(prefix, prefixes)
        self.assertIn("`К` — кириллическая буква (U+041A)", block)


class ProcessPartZero(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.body = section(text(PROCESS), "## 0. Поток BCREQ: процессы, шаги, гейты")
        cls.catalog = catalog()

    def test_processes_with_sources(self):
        processes = table(section(self.body, "### 0.1. Процессы потока"), "ID")
        self.assertEqual([r["ID"] for r in processes], list(PROCESSES))
        for row in processes:
            with self.subTest(process=row["ID"]):
                self.assertTrue(row["Источник (L2 мета-модели)"])
        ops = [op for r in processes for op in OPERATION.findall(r["Операции на шагах"])]
        self.assertEqual(len(ops), len(set(ops)), "операция в двух процессах")
        self.assertEqual(sorted(ops + list(GATE_OPERATIONS)), [c["id"] for c in self.catalog["classes"]])

    def test_stage_gates_typed(self):
        gates = table(section(self.body, "### 0.2. Гейты и стадии артефакта"), "Гейт потока")
        self.assertEqual([r["Гейт потока"].split(" ")[0] for r in gates], list(STAGE_GATES))
        for row in gates:
            with self.subTest(gate=row["Гейт потока"][:12]):
                self.assertTrue(any(t in row["Тип гейта"] for t in TYPES), row["Тип гейта"])
                self.assertTrue(row["Ключевой"].startswith("да"), row["Ключевой"])
        self.assertIn("`гибрид`", gates[0]["Тип гейта"], "Г-IN — гибрид (П-5, П-7, Г1)")

    def test_flow_steps_match_catalog(self):
        steps = table(section(self.body, "### 0.3. Шаги потока"), "Шаг потока")
        self.assertEqual([r["Шаг потока"].split(" ")[0] for r in steps], list(FLOW_STEPS))
        expected = {}
        for item in self.catalog["classes"]:
            expected.setdefault(item["flow_step"], set()).add(item["id"])
        for row in steps:
            step = row["Шаг потока"].split(" ")[0]
            with self.subTest(step=step):
                ops = set(OPERATION.findall(row["Операции (поле `flow_step` каталога)"]))
                self.assertEqual(ops, expected.get(step, set()))


class GateContract(unittest.TestCase):
    def test_stage_gates_typed(self):
        block = section(text(GATES), "## 2. Гейты")
        found = 0
        for line in block.splitlines():
            if line.startswith(tuple(f"| {g}" for g in STAGE_GATES[:3])):
                found += 1
                with self.subTest(gate=line[:8]):
                    self.assertTrue(any(t in line.rsplit(" | ", 1)[1] for t in TYPES), line[-80:])
        self.assertEqual(found, 3)


class Catalog(unittest.TestCase):
    """BL-153: префикс К- и поле «шаг потока»."""

    @classmethod
    def setUpClass(cls):
        cls.data = catalog()
        cls.classes = cls.data["classes"]

    def test_ids_history_and_version(self):
        self.assertEqual(self.data["version"], "0.2")
        self.assertEqual(self.data["id_prefix"], "К-")
        self.assertEqual([c["id"] for c in self.classes], [f"К-{n:02d}" for n in range(1, 40)])
        for item in self.classes:
            with self.subTest(op=item["id"]):
                self.assertEqual(item["id"][0], "К")
                self.assertEqual(item["history"]["previous_id"], "C" + item["id"][2:])
                self.assertTrue(item["file"].startswith(item["id"][2:] + "-"))

    def test_flow_step_matches_rfc(self):
        rfc = rfc_flow_steps()
        self.assertEqual(sorted(rfc), [f"C{n:02d}" for n in range(1, 40) if f"C{n:02d}" not in ("C01", "C09")])
        for item in self.classes:
            with self.subTest(op=item["id"]):
                self.assertIn(item["flow_step"], FLOW_STEPS)
                previous = item["history"]["previous_id"]
                # C01 и C09 приходят в Ш-1 из входа БА (RFC #427, раздел 9.2).
                self.assertEqual(item["flow_step"], rfc.get(previous, "Ш-1"))

    def test_no_legacy_ids_in_contract_text(self):
        for item in self.classes:
            for key, value in item.items():
                if isinstance(value, str):
                    with self.subTest(op=item["id"], field=key):
                        self.assertIsNone(LEGACY_OPERATION.search(value))

    def test_class_files_and_registry(self):
        registry = text(CLASSES / "README.md")
        for item in self.classes:
            body = text(CLASSES / item["file"])
            with self.subTest(op=item["id"]):
                self.assertRegex(body, rf"(?m)^# {item['id']}\. ")
                self.assertIn(f'"class": "{item["id"]}"', body)
                self.assertIsNone(LEGACY_OPERATION.search(body))
                self.assertRegex(registry, rf"(?m)^\| {item['id']} \| \[[^]]+\]\({re.escape(item['file'])}\) \| [^|]+ \| {item['flow_step']} \|")
        self.assertIsNone(LEGACY_OPERATION.search(registry))

    def test_active_documents_use_new_ids(self):
        for path in (STATE, PROCESS):
            with self.subTest(file=path.name):
                self.assertIsNone(LEGACY_OPERATION.search(text(path)))
        operations = re.search(r"const CLASS_OPERATIONS = \{(.*?)\};", text(GENERATOR), re.S).group(1)
        keys = re.findall(r'"(К-\d\d)":', operations)
        self.assertEqual(sorted(keys), [c["id"] for c in self.classes])

    def test_site_ids_stable(self):
        prompts = [p for p in json.loads(text(PROMPTS_JSON))["prompts"] if p.get("classId")]
        by_class = {p["classId"]: p for p in prompts}
        self.assertEqual(sorted(by_class), [c["id"] for c in self.classes])
        for item in self.classes:
            prompt = by_class[item["id"]]
            with self.subTest(op=item["id"]):
                self.assertEqual(prompt["id"], f"mango-bcreq-{item['history']['previous_id'].lower()}-{item['slug']}")
                self.assertEqual(prompt["flowStep"], item["flow_step"])


class Records(unittest.TestCase):
    def test_amendment_registered(self):
        self.assertIn("### Поправка 0.4: гейт и его типы (issue #430)", text(RFC))
        self.assertIn("Поправка 0.4", text(REGISTER))

    def test_bl159(self):
        card = text(TRACK_B).split("### BL-159. ", 1)[1].split("\n### ", 1)[0]
        self.assertTrue(card.startswith("Типы гейтов во всех документах проекта"))
        self.assertGreaterEqual(len(re.findall(r"^- \[ \] ", card, re.M)), 8)
        for field in ("**Почему.**", "**Что меняется.**", "**Источники.**", "**Зависит от.**", "**Готово, когда.**"):
            with self.subTest(field=field):
                self.assertIn(field, card)
        backlog = text(BACKLOG)
        self.assertRegex(backlog, r"(?m)^\| BL-159 \| \[Типы гейтов во всех документах проекта\]")
        self.assertRegex(backlog, r"\*\*Критерий закрытия\.\*\* [^\n]*BL-159")


if __name__ == "__main__":
    result = unittest.main(exit=False, verbosity=2).result
    sys.exit(0 if result.wasSuccessful() else 1)
