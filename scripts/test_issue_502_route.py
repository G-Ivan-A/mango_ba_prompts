#!/usr/bin/env python3
"""CI checks for the BL-230 manual process and its navigation examples."""

from copy import deepcopy
import unittest

import bcreq_manual_route as manual


def state(track, current, *completed, facts=()):
    return {
        "format": track, "current": current, "facts": set(facts),
        "results": dict.fromkeys(completed, "r1"), "accepted": dict.fromkeys(completed, "r1"),
        "scope": dict(zip(manual.SCOPE, ("T-1", "try-1", "0.3", "S-20", "r1"))),
        "decisions": {},
    }


def record(state, step, gate, outcome, *roles):
    state["decisions"][gate] = {
        "step": step, "outcome": outcome, "roles": roles, "explicit": True,
        "revision": state["results"][step], "scope": state["scope"].copy(),
        "date": "2026-11-22", "locator": "chat/42", "report_version": "r1",
    }


class RouteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.route = manual.load()
        cls.source = manual.PROCESS.read_text(encoding="utf-8")

    def go(self, state, target, action="продолжить", **context):
        return manual.navigate(self.route, state, action, target, **context)

    def test_reject_bad_tables(self):
        step = next(line for line in self.source.splitlines() if line.startswith("| 5 | Ш-3 |"))
        cases = [
            ("Ш-3 → Ш-4 → Ш-5", "Ш-3 → Ш-4 → Ш-99", "недоступный шаг"),
            ("Ш-3 → Ш-4 → Ш-5", "Ш-3 → Ш-3 → Ш-5", "повторный шаг"),
            ("Ш-А → Ш-1 → Ш-2", "Ш-А → AIN-02 → Ш-2", "недоступный шаг"),
            ("| Ш-0 | decomposed | продолжить", "| Ш-А | decomposed | продолжить", "недоступный источник"),
            ("| Г-IN/дальше | — | Ш-3 |", "| БА | — | Ш-3 |", "обход"),
            ("| Г-IN/дальше | — | Ш-3 |", "| Г-IN/дальше | — | Ш-4 |", "без обхода"),
            ("| Выпуск/выпуск | пакеты-готовы | BASELINE |", "| БА | пакеты-готовы | BASELINE |", "Обход"),
            ("| AIN-24 | decomposed | выйти в CS |", "| AIN-21 | decomposed | выйти в CS |", "обход проверки"),
            (step, f"{step}\n{step}", "повторная строка"),
            ("[черновик UC](../../prompts/drafts/bcreq-uc-modeling-stepwise.md)",
             "[черновик UC](../../prompts/drafts/bcreq-missing.md)", "Редакция отсутствует"),
            ("`прогон: 2` | разделы 3–6", "`прогон: 1` | разделы 3–6", "параметр прогона UC"),
            ("| A-IN | Ш-1 | AIN-15 |", "| A-IN | Ш-1 | Ш-2 |", "недоступен в decomposed"),
        ]
        for original, mutation, diagnosis in cases:
            with self.subTest(mutation=mutation):
                self.assertIn(original, self.source)
                with self.assertRaisesRegex(ValueError, diagnosis):
                    manual.load(self.source.replace(original, mutation, 1))

    def test_technical_step_and_ba_confirmation(self):
        s = state("system", "Ш-0", facts={"вход-Ш-0", "ввод-промпта"})
        self.assertEqual(self.go(s, "Ш-А")["current"], "Ш-А")
        with self.assertRaisesRegex(ValueError, "недоступная цель"):
            self.go(s, "AIN-01")
        s = state("system", "Ш-А", "Ш-А", facts={"ввод-промпта"})
        s["accepted"].clear()
        with self.assertRaisesRegex(ValueError, "подтверждение БА"):
            self.go(s, "Ш-1")
        s["accepted"]["Ш-А"] = "r1"
        self.assertEqual(self.go(s, "Ш-1")["current"], "Ш-1")

    def test_system_gate_and_sh3_input(self):
        s = state("system", "Ш-2", "Ш-2")
        with self.assertRaisesRegex(ValueError, "Г-IN"):
            self.go(s, "Ш-3")
        record(s, "Ш-2", "Г-IN", "дальше", "БА")
        self.assertEqual(self.go(s, "Ш-3")["current"], "Ш-3")
        with self.assertRaisesRegex(ValueError, "недопустимое действие"):
            self.go(s, "Ш-4")
        s["decisions"]["Г-IN"]["step"] = "AIN-24"
        with self.assertRaisesRegex(ValueError, "Г-IN"):
            self.go(s, "Ш-3")
        s["current"] = "Ш-3"
        s["results"]["Ш-3"] = s["accepted"]["Ш-3"] = "r1"
        with self.assertRaisesRegex(ValueError, "BLOCKED: вход Ш-3"):
            self.go(s, "Ш-4")

    def test_ain21_requires_current_explicit_admission_and_separate_call(self):
        s = state("decomposed", "AIN-21", "AIN-21",
                  facts={"критерии-AIN-21", "отдельный-вызов"})
        record(s, "AIN-21", "AIN-21", "allow", "БА")
        self.assertEqual(self.go(s, "AIN-22")["current"], "AIN-22")
        for field in manual.SCOPE:
            with self.subTest(field=field):
                other = deepcopy(s)
                other["decisions"]["AIN-21"]["scope"][field] = "older"
                with self.assertRaisesRegex(ValueError, "неверная задача"):
                    self.go(other, "AIN-22")
        for changes in ({"roles": ["модель"]}, {"explicit": False}, {"outcome": "доработка"}):
            other = deepcopy(s)
            other["decisions"]["AIN-21"].update(changes)
            with self.assertRaisesRegex(ValueError, "актуальный допуск"):
                self.go(other, "AIN-22")
        s["facts"].remove("отдельный-вызов")
        with self.assertRaisesRegex(ValueError, "отдельный-вызов"):
            self.go(s, "AIN-22")

    def test_ain24_requires_both_gates_and_current_handover(self):
        s = state("decomposed", "AIN-24", "AIN-21", "AIN-24")
        record(s, "AIN-21", "AIN-21", "allow", "БА")
        with self.assertRaisesRegex(ValueError, "Г-IN"):
            self.go(s, "Ш-3")
        record(s, "AIN-24", "Г-IN", "дальше", "БА")
        self.assertEqual(self.go(s, "Ш-3")["current"], "Ш-3")
        other = deepcopy(s)
        other["results"]["AIN-24"] = "updated"
        with self.assertRaisesRegex(ValueError, "подтверждение БА"):
            self.go(other, "Ш-3")
        del s["decisions"]["AIN-21"]
        with self.assertRaisesRegex(ValueError, "AIN-21"):
            self.go(s, "Ш-3")

    def test_return_rechecks_admission_and_invalidates_all_downstream_approvals(self):
        s = state("decomposed", "Ш-7", "AIN-14", "AIN-21", "AIN-24", "Ш-3", "Ш-5",
                  facts={"возврат-БА", "критерии-AIN-21", "отдельный-вызов"})
        record(s, "AIN-21", "AIN-21", "allow", "БА")
        record(s, "AIN-24", "Г-IN", "дальше", "БА")
        record(s, "Ш-5", "Г-С1", "согласование", "Заказчик")
        with self.assertRaisesRegex(ValueError, "нет возврата"):
            self.go(s, "AIN-24", action="вернуться", reason="допуск-AIN")
        other = self.go(s, "AIN-21", action="вернуться", reason="допуск-AIN")
        self.assertEqual(other["stale"], ["AIN-21", "AIN-24", "Ш-3", "Ш-5"])
        self.assertEqual(other["accepted"], {"AIN-14": "r1"})
        self.assertEqual(other["decisions"], {})
        self.assertEqual(other["returns"][-1]["revoked"], s["decisions"])

        other["results"]["AIN-21"] = other["accepted"]["AIN-21"] = "r1"
        other["decisions"]["AIN-21"] = s["decisions"]["AIN-21"].copy()
        with self.assertRaisesRegex(ValueError, "отозван при возврате"):
            self.go(other, "AIN-22")
        other["scope"]["snapshot_version"] = "r2"
        other["results"]["AIN-21"] = other["accepted"]["AIN-21"] = "r2"
        del other["decisions"]["AIN-21"]
        with self.assertRaisesRegex(ValueError, "AIN-21"):
            self.go(other, "AIN-22")
        other["decisions"]["AIN-21"] = s["decisions"]["AIN-21"].copy()
        with self.assertRaisesRegex(ValueError, "AIN-21"):
            self.go(other, "AIN-22")
        record(other, "AIN-21", "AIN-21", "allow", "БА")
        self.assertEqual(self.go(other, "AIN-22")["current"], "AIN-22")

    def test_r19_blocks_even_previously_permitted_actions(self):
        s = state("system", "Ш-2", "Ш-2",
                  facts={"вопрос-модели", "возврат-БА", "запрос-сценариев", "контекст-сценариев"})
        record(s, "Ш-2", "Г-IN", "дальше", "БА")
        for cause in ("BLOCKED", "ACCESS_GAP", "critical_conflict"):
            for action, target in [("продолжить", "Ш-3"), ("вернуться", "Ш-1"),
                                   ("уточнить с моделью", "Ш-2"), ("сценарии по запросу", "Ш-С")]:
                with self.subTest(cause=cause, action=action):
                    for _ in range(2):
                        with self.assertRaisesRegex(ValueError, "^BLOCKED"):
                            self.go({**s, cause: True}, target, action=action, reason="контекст")
        self.assertEqual(self.go(s, "Ш-3")["current"], "Ш-3")

    def test_stage_gates_both_uc_invocations_and_terminal_outcomes(self):
        s = state("system", "Ш-5", "Ш-5", facts={"оценка-от"})
        record(s, "Ш-5", "Г-С1", "согласование", "Заказчик")
        with self.assertRaisesRegex(ValueError, "покрытие-100%"):
            self.go(s, "Ш-6")
        s["facts"].add("покрытие-100%")
        self.assertEqual(self.go(s, "Ш-6")["current"], "Ш-6")
        record(s, "Ш-5", "Г-С1", "отказ", "Заказчик")
        self.assertEqual(self.go(s, "СТОП", "остановить")["current"], "СТОП")

        steps = self.route["steps"]
        self.assertEqual(steps["Ш-5"]["edition"], steps["Ш-8"]["edition"])
        self.assertEqual((steps["Ш-5"]["params"], steps["Ш-8"]["params"]), ("`прогон: 1`", "`прогон: 2`"))
        self.assertEqual(self.go(state("system", "Ш-8", "Ш-8"), "Ш-9")["current"], "Ш-9")
        s = state("system", "Ш-В", "Ш-В")
        record(s, "Ш-В", "Г-W", "согласование", "ПО продукта", "архитектор продукта", "руководитель КК")
        with self.assertRaisesRegex(ValueError, "оценка-согласована"):
            self.go(s, "Ш-Р")
        s["facts"].add("оценка-согласована")
        self.assertEqual(self.go(s, "Ш-Р")["current"], "Ш-Р")
        s = state("system", "Ш-Р", "Ш-Р", facts={"пакеты-готовы"})
        with self.assertRaisesRegex(ValueError, "Выпуск"):
            self.go(s, "BASELINE", "выпустить")
        record(s, "Ш-Р", "Выпуск", "выпуск", "БА")
        end = self.go(s, "BASELINE", "выпустить")
        with self.assertRaisesRegex(ValueError, "нет активного шага"):
            self.go(end, "Ш-Р")

    def test_on_request_and_clarification_preserve_context(self):
        s = state("system", "Ш-6", "Ш-6", facts={"запрос-сценариев", "контекст-сценариев", "вопрос-Заказчику"})
        self.assertEqual(self.go(s, "Ш-6", "уточнить с Заказчиком"), s)
        with self.assertRaisesRegex(ValueError, "запрос-сценариев"):
            self.go({**s, "facts": set()}, "Ш-С", "сценарии по запросу")
        side = self.go(s, "Ш-С", "сценарии по запросу")
        side["results"]["Ш-С"] = side["accepted"]["Ш-С"] = "us-1"
        with self.assertRaisesRegex(ValueError, "неверный исходный контекст"):
            self.go(side, "Ш-7", "вернуться в контекст")
        with self.assertRaisesRegex(ValueError, "неверный исходный контекст"):
            self.go({**side, "format": "decomposed"}, "Ш-6", "вернуться в контекст")
        resumed = self.go(side, "Ш-6", "вернуться в контекст")
        self.assertEqual(resumed["decisions"], s["decisions"])
        self.assertEqual(resumed["current"], "Ш-6")
        self.assertNotIn("origin", resumed)
        ain = state("decomposed", "AIN-16", facts={"вопрос-Заказчику"})
        self.assertEqual(self.go(ain, "AIN-16", "уточнить с Заказчиком"), ain)
        with self.assertRaisesRegex(ValueError, "только через AIN-16"):
            self.go({**ain, "current": "AIN-15"}, "AIN-15", "уточнить с Заказчиком")


if __name__ == "__main__":
    unittest.main(verbosity=2)
