#!/usr/bin/env python3
"""Регрессионная проверка issue #464: корректировки стандартов и стадии A-IN.

Проверки держат решения владельца, а не качество текста:

* антипаттерны первого теста не вернулись: Ш-0 не выводит конституцию и не пишет
  разделы; нет фраз «что мешает, словами Заказчика», «при двух и более продуктах»,
  «Пункты 5.N — по блокам ФТ», «Термины Заказчика и БА переносятся дословно»;
* порядок A-IN: Ш-0 → Ш-А → Ш-1; анкета спрашивает пять показателей и пропускается;
  Ш-1 идёт «сбор → интерпретация → фиксация»;
* стандарты: приоритет словарей, проверка исполнимости, выход в поток CS, виды сущности
  в 2.4, условия работы в 6.2, определение достаточных ФТ, структура раздела 5 по стандарту;
* правило «не выдумывай» есть в каждом промпте маршрута, кроме измеренного Ш-В;
* страница стандартов: блок индустриальных стандартов, внешние ссылки в новом окне;
* выпуск: комплект 0.8, 14 шагов, сайт 2.7.0;
* бэклог: задачи и решение issue #464, движение по цепочке.

Мутации: ``experiments/issue_464/mutations.py``.
Запуск: ``python3 scripts/validate_issue_464_a_in.py``
"""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SECTIONS = "standards/bcreq-sections"
STEP0 = "prompts/bcreq-constitution-governance-oneshot.md"
STEP_A = "prompts/drafts/bcreq-intake-questionnaire-stepwise.md"
STEP1 = "prompts/bcreq-context-understanding-stepwise.md"
SHV = "prompts/bcreq-review-validation-oneshot.md"
ROUTE = (
    "prompts/bcreq-context-understanding-stepwise.md",
    "prompts/bcreq-products-impact-analysis-stepwise.md",
    "prompts/bcreq-fr-documentation-stepwise.md",
    "prompts/bcreq-nfr-documentation-stepwise.md",
    "prompts/bcreq-scenarios-modeling-oneshot.md",
    "prompts/bcreq-uc-modeling-stepwise.md",
    "prompts/bcreq-orr-solution-design-stepwise.md",
    "prompts/bcreq-constraints-documentation-stepwise.md",
    "prompts/bcreq-extra-risk-analysis-stepwise.md",
    "prompts/bcreq-in-understanding-oneshot.md",
    "prompts/bcreq-core-documentation-oneshot.md",
    "prompts/bcreq-work-solution-design-oneshot.md",
)
BANNED = {
    "что мешает, словами Заказчика": (f"{SECTIONS}/02-business-context.md", "site/index.html"),
    "при двух и более продуктах": ("site/index.html",),
    "Пункты 5.N — по блокам ФТ": (f"{SECTIONS}/05-solution-description.md", "site/index.html"),
    "Термины Заказчика и БА переносятся дословно": (f"{SECTIONS}/01-glossary.md", "site/index.html"),
}


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def section(text: str, heading: str) -> str:
    """Текст от заголовка до следующего заголовка того же или старшего уровня."""
    match = re.search(rf"^(#+) {re.escape(heading)}.*$", text, re.M)
    if not match:
        raise AssertionError(f"нет раздела {heading!r}")
    level = len(match.group(1))
    rest = text[match.end():]
    stop = re.search(rf"^#{{1,{level}}} ", rest, re.M)
    return rest[: stop.start()] if stop else rest


class FirstTestAntipatterns(unittest.TestCase):
    def test_banned_wording_is_gone(self):
        for phrase, files in BANNED.items():
            for path in files:
                with self.subTest(phrase=phrase, path=path):
                    self.assertNotIn(phrase, read(path))

    def test_step0_does_not_dump_or_generate(self):
        text = read(STEP0)
        self.assertIn("Не выводи её: БА уже вставил этот промпт в чат.", text)
        banned = re.search(r"\*\*На этом шаге запрещено:\*\*(.*?)Всё это делают следующие шаги", text, re.S)
        self.assertIsNotNone(banned, "нет запрета шага Ш-0")
        for word in ("конституцию", "разделы", "глоссарий", "гипотезы"):
            self.assertIn(word, banned.group(1))
        self.assertIn("Попроси ввести следующий промпт", text)

    def test_constitution_is_not_repeated_later(self):
        self.assertRegex(read(STEP0), r"ЧТ-1 \| Конституция предназначена модели и в чат не выводится\. Исключение: первый этап роадмапа")


class AInOrder(unittest.TestCase):
    def test_questionnaire_asks_five_indicators_and_can_be_skipped(self):
        text = read(STEP_A)
        for item in ("продукты Mango Office подключены", "операторов", "номеров Mango ВАТС",
                     "сторонних номеров", "звонков и текстовых коммуникаций в месяц"):
            with self.subTest(item=item):
                self.assertIn(item, text)
        self.assertIn("шаг можно пропустить", text)
        self.assertIn("| Раздел 5, структура ОРР | C4 | TM Forum ODA или другой по ссылке |", text)

    def test_step1_collects_before_sections(self):
        text = read(STEP1)
        self.assertIn("**Порядок: сбор → интерпретация → фиксация.** Разделы 1 и 2 пишутся только", text)
        positions = [text.index(mark) for mark in ("*Сбор*", "*Интерпретация*", "*Фиксация*")]
        self.assertEqual(positions, sorted(positions), "подшаги идут не по порядку")

    def test_kit_order_and_size(self):
        kit = json.loads(read("site/data/test-kit.json"))
        self.assertEqual(kit["kit"]["version"], "0.8")
        steps = [item["step"].split()[0] for item in kit["steps"]]
        self.assertEqual(len(steps), 14)
        self.assertEqual(steps[:3], ["Ш-0", "Ш-А", "Ш-1"])

    def test_step_a_is_not_published_before_measurement(self):
        self.assertFalse((ROOT / "prompts/bcreq-intake-questionnaire-stepwise.md").exists())
        self.assertIn("mode: by-test", read(STEP_A))


class Standards(unittest.TestCase):
    def test_glossary_dictionary_priority(self):
        text = read(f"{SECTIONS}/01-glossary.md")
        order = section(text, "Порядок источников истины")
        positions = [order.index(mark) for mark in ("D0", "IREB CPRE Glossary", "БА")]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("### Пользователь и Оператор", text)

    def test_executability_scale_and_exit(self):
        text = section(read(f"{SECTIONS}/02-business-context.md"), "Проверка исполнимости требования")
        for mark in ("**Да**", "**Частично**", "**Нет**", "UNKNOWN", "Выход из BCREQ", "Система должна"):
            with self.subTest(mark=mark):
                self.assertIn(mark, text)
        self.assertTrue((ROOT / "docs/ba-processes/cs-flow-stub.md").exists())
        self.assertIn("BL-235", read("docs/ba-processes/cs-flow-stub.md"))

    def test_boundaries_by_entity_kinds(self):
        text = section(read(f"{SECTIONS}/02-business-context.md"), "Однозначность границ")
        for mark in ("Сущность", "Интерфейс, компонент, сервис", "исходящий обзвон", "АПП", "ЗОЗ",
                     "Что не входит в 2.4.1 и 2.4.2", "6.2"):
            with self.subTest(mark=mark):
                self.assertIn(mark, text)
        self.assertIn("условия-работы-и-сценарные-исключения", text)
        self.assertIn("## Условия работы и сценарные исключения".split(" ", 1)[1],
                      read(f"{SECTIONS}/06-implementation-constraints.md"))

    def test_stakeholders_stub(self):
        text = section(read(f"{SECTIONS}/02-business-context.md"), "2.5 — заглушка стейкхолдеров")
        self.assertIn("Стейкхолдеры всегда: Заказчик и Продуктовая команда", text)
        self.assertIn("заглушка до документов команд Mango Office", text)

    def test_fr_sufficiency_is_defined(self):
        text = read(f"{SECTIONS}/03-functional-requirements.md")
        self.assertIn("## Необходимые и достаточные ФТ: определение", text)
        self.assertIn("BABOK Guide v3; БА может инициировать смену", text)

    def test_orr_structure_follows_standard_not_fr(self):
        text = read(f"{SECTIONS}/05-solution-description.md")
        self.assertIn("Раздел 5 **не строится** по блокам ФТ", text)
        self.assertIn("5.2. Формулировка заявки (ФТ-01, ФТ-03)", text)
        self.assertIn("Номера пунктов не зависят от номеров ФТ", text)
        self.assertIn("Это не архитектура и не системный анализ", text)

    def test_dont_invent_rule_in_route_prompts(self):
        for path in ROUTE:
            with self.subTest(path=path):
                self.assertIn("Р2: неясное не выдумывай", read(path))

    def test_measured_review_prompt_is_untouched(self):
        self.assertNotIn("неясное не выдумывай", read(SHV))


class StandardsPage(unittest.TestCase):
    def setUp(self):
        self.html = read("site/index.html")

    def block(self) -> str:
        match = re.search(r'<section class="standard-card v2-card standards-industry".*?</section>', self.html, re.S)
        self.assertIsNotNone(match, "нет блока индустриальных стандартов")
        return match.group(0)

    def test_industry_block_covers_owner_list(self):
        block = self.block()
        for mark in ("BABOK", "C4", "TM Forum", "ODA"):
            with self.subTest(mark=mark):
                self.assertIn(mark, block)

    def test_external_links_open_in_new_window(self):
        links = re.findall(r"<a\b[^>]*href=\"https?://[^\"]+\"[^>]*>", self.block())
        self.assertGreater(len(links), 0)
        for link in links:
            with self.subTest(link=link):
                self.assertIn('target="_blank"', link)

    def test_navigation_reaches_the_block(self):
        self.assertIn('href="#standards?section=9" data-standard-target="9"', self.html)
        self.assertIn('9: "standard-industry"', read("site/app.js"))

    def test_page_names_verified_ireb_glossary(self):
        self.assertIn("IREB CPRE Glossary", self.html)


class Release(unittest.TestCase):
    def test_site_version(self):
        stats = json.loads(read("site/data/stats.json"))
        self.assertIn("2.7.0", json.dumps(stats, ensure_ascii=False))
        self.assertIn("версия сайта 2.7.0", read("CHANGELOG.md"))

    def test_adr_number_does_not_take_lessons_reservation(self):
        self.assertTrue((ROOT / "docs/adr/2026-11-adr-019-bcreq-a-in-collection.md").exists())
        self.assertFalse((ROOT / "docs/adr/2026-11-adr-018-bcreq-a-in-collection.md").exists())


class Backlog(unittest.TestCase):
    def setUp(self):
        self.entry = read("pr-ops/BACKLOG.md")

    def test_tasks_and_decision_are_registered(self):
        for task, card in (("BL-175", "pr-ops/backlog-ba-model.md"),
                           ("BL-235", "pr-ops/backlog-repository.md"),
                           ("BL-236", "pr-ops/backlog-repository.md")):
            with self.subTest(task=task):
                self.assertRegex(self.entry, rf"(?m)^\| {task} \|.*\| deferred \(triggered\) \|")
                self.assertIn(f"### {task}. ", read(card))
        self.assertIn("| **Р-21** |", self.entry)

    def test_chain_movement_is_recorded(self):
        chain = re.search(r"\*\*Движение по цепочке \(на 2026-11-05, issue #464\)\.\*\*(.*?)\n\n\*\*", self.entry, re.S)
        self.assertIsNotNone(chain)
        for mark in ("| Предшествующий (полнота) |", "| Текущий — закрывается |", "| Открывает |",
                     "BL-232", "BL-235", "BL-236", "BL-175", "Р-21", "BL-157в"):
            with self.subTest(mark=mark):
                self.assertIn(mark, chain.group(1))

    def test_deploy_task_targets_new_build(self):
        self.assertRegex(self.entry, r"(?m)^\| BL-232 \|.*деплой 2\.7\.0")


if __name__ == "__main__":
    unittest.main()
