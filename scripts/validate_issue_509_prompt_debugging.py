#!/usr/bin/env python3
"""BL-194: assembly and regression contracts; this does not execute an LLM."""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import bcreq_fragments as fragments
import bcreq_handoff
import build_bcreq_a_in as ain
import build_bcreq_step_prompts as steps
import build_bcreq_system_track as system
from prompt_purity import project


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def contract_gaps(text):
    rules = {
        "decisions": "Реестр решений БА",
        "explicit_admission": "Допускаю <шаг/гейт>",
        "integration_roles": "секрет нужен инициатору",
        "short_receipt": "не больше трёх строк",
        "output_rules": "## Правила вывода для БА",
        "unknown_metadata": "<не задано>",
    }
    return [key for key, rule in rules.items() if rule not in text]


class Debugging(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.kit = json.loads(read("site/data/a-in-kit.json"))

    def test_real_before_and_after_regression(self):
        before = subprocess.check_output([
            "git", "show", "b0caecd30968fb7e62678e78fffc43a4031d3f3f:"
            "prompts/drafts/a-in/bcreq-ain-01-understanding-stepwise.md",
        ], cwd=ROOT).decode()
        self.assertEqual(len(contract_gaps(before)), 6)
        for step in self.kit["steps"]:
            self.assertEqual(contract_gaps(step["prompt"]), [], step["id"])

    def test_builders_and_site_are_in_sync(self):
        outputs = {**ain.build(), **steps.build_all(), **system.build()}
        for path, text in outputs.items():
            self.assertEqual(path.read_text(), text, str(path))
        self.assertEqual(read("site/data/step-handoff.json"), bcreq_handoff.dump())

    def test_forms_share_exact_step_content_and_valid_hashes(self):
        common = fragments.common()
        for step in self.kit["steps"]:
            full, compact = step["prompt"], step["compactPrompt"]
            suffix = full.split("## Только текущий контракт:", 1)[1]
            self.assertEqual(compact.split("## Только текущий контракт:", 1)[1], suffix)
            self.assertIn(common, full)
            self.assertNotIn(common, compact)
            self.assertIn("Контракт отсутствует, другой версии или утрачен — blocked", compact)
            self.assertIn("шаг не выполняй", compact)
            for text, key in [(full, "promptSha256"), (compact, "compactPromptSha256")]:
                self.assertEqual(hashlib.sha256(text.encode()).hexdigest(), step[key])
                self.assertIn(f"КОНЕЦ {step['id']} {fragments.VERSION}", text)
                self.assertNotIn("КОНЕЦ " + step["id"] + " <версия результата>", text)
        contract = self.kit["contract"]
        self.assertEqual(contract["prompt"], f"# Контракт A-IN {fragments.VERSION}\n\n{common}\n")
        self.assertEqual(hashlib.sha256(contract["prompt"].encode()).hexdigest(), contract["promptSha256"])
        self.assertEqual(self.kit["defaultForm"], "full")

    def test_shared_fragments_in_both_formats(self):
        texts = [s["prompt"] for s in self.kit["steps"]]
        texts += list(system.build().values())
        texts += [t for p, t in steps.build_all().items()
                  if p.suffix == ".md" and p.stem not in steps.HANDOFF_SKIP]
        for text in texts:
            self.assertIn(project(fragments.access()), text)
            self.assertIn(project(fragments.output()), text)
            self.assertIn(fragments.response_order(), text)

    def test_decisions_arrive_at_requirements_and_gates(self):
        for name in ("fr-documentation", "nfr-documentation", "uc-modeling"):
            text = read(f"prompts/drafts/bcreq-{name}-stepwise.md")
            self.assertIn(fragments.decisions(), text)
            for token in ("обязательный вход", "со ссылкой на решение БА", "отзови с причиной"):
                self.assertIn(token, text)
        shape = json.loads(read("docs/ba-processes/bcreq-a-in-instructions.json"))
        for sid in ("AIN-03", "AIN-04"):
            self.assertIn("только заполненные поля", shape[sid]["shape"])
        for token in ("границы поставки", "не входит", "термин — определение", "Реестром решений БА"):
            self.assertIn(token, shape["AIN-22"]["action"])
        fr = read("prompts/drafts/bcreq-fr-documentation-stepwise.md")
        for text in (fr, self.kit["steps"][-1]["prompt"]):
            self.assertIn("ФТ-NN. Система должна…", text)
            self.assertIn("заголовки групп без нумерации", text)
        self.assertNotIn("3.1 Система должна", fr)
        for n in (12, 14, 18, 20):
            self.assertIn("LE-21", self.kit["steps"][n-1]["prompt"])

    def test_review_uses_silence_only_for_the_two_approved_technical_steps(self):
        data = bcreq_handoff.load()
        self.assertEqual({sid for sid, step in data["steps"].items() if step.get("acceptOnSilence")},
                         {"AIN-06", "AIN-22"})
        for sid in ("AIN-06", "AIN-22"):
            handoff = bcreq_handoff.render([sid], data)
            self.assertIn("При отсутствии возражений БА текущая версия принята", handoff)
            self.assertIn("отдельный вызов БА", handoff)
            self.assertIn("Итог шага", handoff)
        self.assertEqual({sid for sid, step in data["steps"].items() if step.get("approvalOnce")}, {"AIN-18"})
        handoff = bcreq_handoff.render(["AIN-18"], data)
        self.assertEqual(handoff.count("запроси решение один раз"), 1)
        self.assertNotIn("БА — проверить:", handoff)

    def test_access_contract_replaces_legacy_rules_in_working_editions(self):
        policy = fragments.access()
        for token in ("конфигурация клиента", "оркестратор до шага предзагружает", "в кэше текущей сессии",
                      "На AIN-07…12", "при смене доступа", "поиска нет"):
            self.assertIn(token, policy)
        for token in ("стабильный ID П-n", "пробел П-n открыт", "Не требуй приложить файл",
                      "`[ACCESS_GAP: П-n — <тема>]` выдай только в строке «Отклонения» receipt",
                      "Г-IN, допуск AIN-21, Г-С1"):
            self.assertIn(token, policy)
        self.assertNotIn("ACCESS_GAP", bcreq_handoff.load()["approveTechnical"])
        self.assertIn("Обычный пробел БЗ на согласование не выноси", bcreq_handoff.load()["approveTechnical"])
        legacy = "Перед каждым вызовом явно выдай «Доступ к БЗ»"
        for step in self.kit["steps"]:
            self.assertNotIn(legacy, step["prompt"], step["id"])
        for prompt in system.build().values():
            self.assertLess(prompt.index("ниже заменяют правила доступа и пробелов"), prompt.index(policy))

    def test_regression_inventory_and_stage_two_inputs(self):
        cases = json.loads(read("experiments/issue_509/regressions.json"))
        self.assertEqual([c["id"] for c in cases], [f"RG-{i:02}" for i in range(1, 11)])
        for case in cases:
            self.assertNotRegex(json.dumps(case, ensure_ascii=False), r"1143|SFTP|RUN-0096")
            if case["status"] != "rule":
                self.assertTrue(case["dependency"])
        backlog = read("pr-ops/backlog-ba-model.md")
        entry = backlog.split("### BL-131.", 1)[1].split("### BL-132.", 1)[0]
        for token in ("bcreq-evidence-normalization.md", "bcreq-ba-output.md", "regressions.json", "RG-01…RG-10"):
            self.assertIn(token, entry)

    def test_actual_contract_text_saves_at_least_sixty_percent(self):
        spec = importlib.util.spec_from_file_location("redundancy509", ROOT / "experiments/issue_505/prompt_redundancy.py")
        measurement = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(measurement)
        measured = measurement.main()
        self.assertEqual(measured["ain_files"], 24)
        self.assertGreaterEqual(measured["route_saving_share"], .6)
        # RFC §3 sets the target for contract characters per chat. Count the
        # anchors too, rather than confusing that with the entire route size.
        full_contracts = len(fragments.common()) * len(self.kit["steps"])
        anchors = sum(len(s["compactPrompt"].split("## Якорь контракта", 1)[1]
                          .split("## Только текущий контракт:", 1)[0])
                      + len("## Якорь контракта") for s in self.kit["steps"])
        actual_contract = len(self.kit["contract"]["prompt"]) + anchors
        self.assertLessEqual(actual_contract / full_contracts, .4)
        actual_route = (sum(measured["route_other_prompts_chars"].values())
                        + len(self.kit["contract"]["prompt"])
                        + sum(len(s["compactPrompt"]) for s in self.kit["steps"]))
        self.assertLessEqual(actual_route / measured["route_total_chars_as_pasted"], .4)

    def test_site_behavior(self):
        result = subprocess.run(["node", "--test", "experiments/issue_509/site.test.cjs"], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_reviewed_changes_preserve_historical_bytes_and_detect_drift(self):
        spec = importlib.util.spec_from_file_location("changes509", ROOT / "experiments/issue_509/prompt_changes.py")
        changes = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(changes)
        registry = json.loads(read("experiments/issue_509/prompt-edits.json"))
        followup = changes.FOLLOWUP
        paths = subprocess.check_output([
            "git", "diff", "--name-only", followup["base"], "--", "prompts/drafts",
        ], cwd=ROOT).decode().splitlines()
        self.assertEqual(set(followup["files"]), set(paths))
        for path in paths:
            current = read(path)
            prior = changes.git_text("show", f"{followup['base']}:{path}")
            self.assertEqual(changes.revert_followup(path, current), prior)
            self.assertEqual(changes.revert_followup(path, current + "\nUnreviewed drift"), prior + "\nUnreviewed drift")
            with self.assertRaisesRegex(ValueError, "reviewed 0.5 edition"):
                changes.revert_followup(path, current.replace("Итог шага", "Changed", 1))
        for path, entry in registry["files"].items():
            current = read(path)
            old = changes.revert_followup(path, current)
            self.assertEqual(hashlib.sha256(old.encode()).hexdigest(), entry["sha256_after"])
            before = subprocess.check_output(["git", "show", f"{registry['base']}:{path}"], cwd=ROOT).decode()
            self.assertEqual(changes.revert(path, current), before)
            self.assertEqual(changes.revert(path, current + "\nUnreviewed drift"), before + "\nUnreviewed drift")
        subprocess.run([sys.executable, "experiments/issue_509/build_prompt_edits.py", "--check"], cwd=ROOT, check=True)


if __name__ == "__main__":
    unittest.main()
