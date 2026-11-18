#!/usr/bin/env python3
"""Issue #490: цель шага, «Итог шага» и два формата шагов BCREQ.

Проверяет без LLM и без подпроцессов (сборщики импортируются, поэтому
``validate_all`` видит зависимости и кэширует проверку):

* SSOT ``docs/ba-processes/bcreq-step-handoff.md`` → ``site/data/step-handoff.json``;
* черновики Ш-ХХ, AIN-01…24 и системный формат совпадают с выходом сборщиков
  и заканчиваются блоком «Итог шага» (кроме измеренной истории Ш-В/Ш-С);
* в блоке есть обе формы п. 1.2 issue: «БА — проверить» и «Шаг технический…»;
* выбор stepwise/oneshot у БА не запрашивается: Ш-0 принимает «Формат шагов»;
* сайт: «Цель» вместо «Что делает БА», строка проверки, переключатель формата,
  фасет каталога «Формат шагов» вместо stepwise/oneshot.
"""
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import bcreq_handoff  # noqa: E402
import build_bcreq_a_in  # noqa: E402
import build_bcreq_step_prompts  # noqa: E402
import build_bcreq_system_track  # noqa: E402

BEGIN, END = bcreq_handoff.BEGIN, bcreq_handoff.END
DATA = ROOT / "site/data"


def read(path):
    return Path(path).read_text(encoding="utf-8")


def stale(outputs):
    return [str(p.relative_to(ROOT)) for p, text in outputs.items()
            if not p.exists() or read(p) != text]


class SsotTest(unittest.TestCase):
    def setUp(self):
        self.data = bcreq_handoff.load()

    def test_site_data_matches_ssot(self):
        self.assertEqual(read(bcreq_handoff.OUT), bcreq_handoff.dump(self.data))

    def test_every_step_has_goal_and_check(self):
        steps = self.data["steps"]
        self.assertEqual(len(steps), 38)
        for sid, step in steps.items():
            self.assertGreater(len(step["goal"]), 20, f"{sid}: «Цель» пуста или слишком коротка")
            self.assertTrue(step["check"], f"{sid}: нет «Что проверить»")
            self.assertNotRegex(step["goal"], r"(?i)stepwise|oneshot", f"{sid}: цель упоминает режим")

    def test_both_forms_of_issue_item_1_2(self):
        kinds = {s["checkKind"] for s in self.data["steps"].values()}
        self.assertEqual(kinds, {"required", "technical"})
        required = next(s for s in self.data["steps"].values() if s["checkKind"] == "required")
        technical = next(s for s in self.data["steps"].values() if s["checkKind"] == "technical")
        for step, phrase in [(required, "БА — проверить:"), (technical, "Шаг технический, можно проверить")]:
            block = bcreq_handoff.render([step["id"]], self.data)
            self.assertIn(f"Выполнен промпт {step['id']}", block)
            self.assertIn(phrase, block)
            self.assertIn("На согласование БА", block)
        self.assertIn("без обязательного согласования БА выполненных действий",
                      bcreq_handoff.render([technical["id"]], self.data))

    def test_gates_are_never_technical(self):
        for sid in bcreq_handoff.NEVER_TECHNICAL:
            self.assertEqual(self.data["steps"][sid]["checkKind"], "required", sid)


class PromptsTest(unittest.TestCase):
    def test_builders_are_in_sync(self):
        for name, outputs in [("Ш-ХХ", build_bcreq_step_prompts.build_all()),
                              ("AIN", build_bcreq_a_in.build()),
                              ("системный формат", build_bcreq_system_track.build())]:
            self.assertEqual(stale(outputs), [], f"{name}: перезапустите сборщик")

    def test_drafts_end_with_handoff(self):
        skip = build_bcreq_step_prompts.HANDOFF_SKIP
        paths = [p for p in sorted((ROOT / "prompts/drafts").glob("bcreq-*.md")) if p.stem not in skip]
        paths += sorted((ROOT / "prompts/drafts/a-in").glob("*.md"))
        paths += sorted((ROOT / "prompts/drafts/system").glob("*.md"))
        self.assertEqual(len(paths), 11 + 24 + 3)
        for path in paths:
            text = read(path)
            self.assertIn(BEGIN, text, path.name)
            self.assertIn(END, text, path.name)
            self.assertIn("**Итог шага**", text, path.name)
            if "/a-in/" not in str(path):
                self.assertTrue(text.rstrip().endswith(END), f"{path.name}: блок не в конце")

    def test_system_track_keeps_archive_text(self):
        for path in sorted((ROOT / "prompts/drafts/system").glob("*.md")):
            text = read(path)
            self.assertIn("track: system", text)
            source = re.search(r"^based_on: (\S+)$", text, re.M).group(1)
            self.assertTrue(source.startswith("prompts/archive/a-in-v2.7.0/"), source)
            # Правила из чата 1135-2 (анализ #490, П-12, П-13, П-15).
            block = text.split(build_bcreq_system_track.BEGIN, 1)[1].split(build_bcreq_system_track.END, 1)[0]
            for rule in ("Темп задаёт БА", "одно бизнес-решение на пункт",
                         "сленг в требования не переноси"):
                self.assertIn(rule, block, path.name)

    def test_fr_step_keeps_what_not_how(self):
        fr = read(ROOT / "prompts/drafts/bcreq-fr-documentation-stepwise.md")
        self.assertIn("сленг в ФТ не переноси", fr)

    def test_starter_takes_format_not_mode_choice(self):
        starter = read(ROOT / "prompts/drafts/bcreq-constitution-governance-oneshot.md")
        self.assertIn("Формат шагов", starter)
        # Граничный случай E-02: «stepwise»/«oneshot» от БА формат не меняют.
        self.assertIn("а не формат шагов: формат не меняй и не переспрашивай", starter)
        self.assertNotRegex(starter, r"(?i)выбери(те)? режим|режим stepwise или oneshot")


class SiteTest(unittest.TestCase):
    def setUp(self):
        self.app = read(ROOT / "site/app.js")
        self.index = read(ROOT / "site/index.html")
        self.kit = json.loads(read(DATA / "test-kit.json"))
        self.prompts = json.loads(read(DATA / "prompts.json"))

    def test_step_card_has_goal_and_check(self):
        body = self.app.split("function testKitStep", 1)[1].split("\nfunction ", 1)[0]
        self.assertIn('bcreqField("Цель"', body)
        self.assertIn("БА — проверить", body)
        self.assertIn("Шаг технический", body)
        # Метка поля больше не выводится (упоминание в комментарии — история).
        self.assertNotRegex(body, r"[\"'`]Что делает БА")
        self.assertNotIn("<strong>Что делает БА", self.index)

    def test_test_kit_data(self):
        steps = self.kit["steps"]
        self.assertEqual(self.kit["counts"]["system"], 3)
        for step in steps:
            for key in ("goal", "checkKind", "check"):
                self.assertTrue(step.get(key), f"{step['step']}: нет {key}")
            self.assertNotIn("actions", step)
        system = [s for s in steps if s.get("system")]
        self.assertEqual([s["step"].split()[0] for s in system], ["Ш-А", "Ш-1", "Ш-2"])
        for step in system:
            self.assertIn("**Итог шага**", step["system"]["body"])
        for step in steps:
            if step["mode"] == "published":
                self.assertIn(BEGIN, step["handoffBlock"])

    def test_format_switch_and_facet(self):
        self.assertIn('id="step-format-switch"', self.index)
        self.assertIn('href="step-format.css"', self.index)
        for token in ("STEP_FORMATS", "composeSystemTestKit", "Формат шагов: ", 'renderFilterGroup("Формат шагов"'):
            self.assertIn(token, self.app)
        self.assertNotIn('renderFilterGroup("Режимы"', self.app)
        formats = {f["id"]: f for f in self.prompts["filters"]["formats"]}
        self.assertEqual(set(formats), {"system", "decomposed"})
        self.assertEqual(formats["system"]["label"], "Системные (комплексные шаги)")
        self.assertEqual(formats["decomposed"]["label"], "Декомпозированные шаги")
        items = self.prompts["prompts"]
        self.assertTrue(all(p.get("format") in formats for p in items))
        self.assertEqual(sum(f["count"] for f in formats.values()), len(items))


if __name__ == "__main__":
    unittest.main(verbosity=1)
