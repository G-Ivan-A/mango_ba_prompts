#!/usr/bin/env python3
"""Verify the stage-1 catalog projection against its source files."""
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
EXPERIMENT = ROOT / "experiments/issue_500"
sys.path.insert(0, str(EXPERIMENT))
import protected_baseline as protection  # noqa: E402


def read_json(root, relative):
    return json.loads((root / relative).read_text(encoding="utf-8"))


def check_working_editions(root, catalog):
    kit_path = "site/data/test-kit.json"
    route_path = "docs/ba-processes/bcreq-a-in-route.json"
    classes_path = "standards/bcreq-manual-classes/catalog.json"
    editions = catalog.get("workingPrompts", [])
    if not editions:
        raise ValueError("site/data/prompts.json: отсутствуют рабочие редакции этапа 1")
    kit = read_json(root, kit_path)
    route = read_json(root, route_path)
    ain_kit = read_json(root, "site/data/a-in-kit.json")
    classes = read_json(root, classes_path)["classes"]
    expected = {}
    step_classes = {}
    class_steps = {item["id"]: [] for item in classes}

    def add(step, edition, formats, mode, assigned):
        by_path = expected.setdefault(edition["id"], {})
        context = {"step": step, "formats": formats, "mode": mode, "assigned": assigned}
        by_path.setdefault(edition["sourcePath"], []).append(context)

    def link(step, class_id):
        if class_id not in class_steps:
            raise ValueError(f"{step}: {class_id}: неизвестный класс")
        class_steps[class_id].append(step)
        step_classes.setdefault(step, []).append(class_id)

    for step in kit["steps"]:
        code = step["step"].split()[0]
        for key, mode in (("draft", "by-test"), ("published", "published"), ("system", "by-test")):
            if not step[key] or (key == "draft" and step["system"]):
                continue
            formats = ["system"] if step["system"] else ["decomposed", "system"]
            assigned = (key == "system") if step["system"] else step["mode"] == mode
            add(code, step[key], formats, mode, assigned)
    known_sh = {step["step"].split()[0] for step in kit["steps"]}
    for item in classes:
        if item.get("flow_step"):
            if item["flow_step"] not in known_sh:
                raise ValueError(f"{classes_path}: {item['id']}: неизвестный шаг {item['flow_step']}")
            link(item["flow_step"], item["id"])

    ain_projections = {step["id"]: step for step in ain_kit["steps"]}
    for step in route["steps"]:
        code = step["id"]
        projection = ain_projections[code]
        header = projection["prompt"].split("---", 2)[1]
        prompt_id = re.search(r"^id: (\S+)$", header, re.MULTILINE)[1]
        add(code, {"id": prompt_id, "sourcePath": projection["promptPath"]}, ["decomposed"], "by-test", True)
        for class_id in step["operation"].split(", "):
            link(code, class_id)

    seen = set()
    for card in editions:
        prompt_id = card["id"]
        relative = card["sourcePath"]
        label = f"site/data/prompts.json: {prompt_id} ({relative})"
        if prompt_id in seen:
            raise ValueError(f"{label}: повторный ID")
        seen.add(prompt_id)
        paths = expected.get(prompt_id, {})
        if len(paths) != 1 or relative not in paths:
            raise ValueError(f"{label}: неверный или неоднозначный путь редакции")
        try:
            source = (root / relative).read_bytes()
        except FileNotFoundError as error:
            raise ValueError(f"{label}: исходник отсутствует") from error
        header = source.decode().split("---", 2)[1]
        metadata = dict(re.findall(r'^(id|status|version):\s*"?([^"\n]+)"?$', header, re.MULTILINE))
        for field in ("id", "status", "version"):
            if card[field] != metadata[field].strip():
                raise ValueError(f"{label}: неверное поле {field}")
        if card["archived"] or card["contentHash"] != hashlib.sha256(source).hexdigest():
            raise ValueError(f"{label}: неверный архивный признак или SHA")
        if "body" in card or "content" in card:
            raise ValueError(f"{label}: дублирован текст из рабочего комплекта")
        if card["contexts"] != paths[relative]:
            raise ValueError(f"{label}: неверный или неизвестный шаг применения")

    if seen != expected.keys():
        raise ValueError(f"site/data/prompts.json: отсутствуют редакции {sorted(expected.keys() - seen)}")
    if catalog["stepClasses"] != step_classes or catalog["classSteps"] != class_steps:
        raise ValueError(f"site/data/prompts.json: нарушена обратная связь К ↔ шаг ({classes_path}, {route_path})")


class WorkingEditionsTest(unittest.TestCase):
    def test_working_editions(self):
        root = Path(sys.argv[1]) if len(sys.argv) == 2 else ROOT
        check_working_editions(root, read_json(root, "site/data/prompts.json"))

    def test_catalog_mutations(self):
        data = read_json(ROOT, "site/data/prompts.json")
        tests = {
            "draft → archived": ("неверное поле status", lambda catalog, card: card.update(status="archived")),
            "исторический путь для системного Ш-1": ("путь редакции", lambda catalog, card: card.update(
                sourcePath="prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md")),
            "исторический путь с тем же именем": ("путь редакции", lambda catalog, card: next(
                item for item in catalog["workingPrompts"] if item["id"] ==
                "mango-bcreq-constitution-governance-oneshot-by-test").update(
                    sourcePath="prompts/archive/a-in-v2.7.0/bcreq-constitution-governance-oneshot.md")),
            "неизвестный шаг": ("неизвестный шаг применения", lambda catalog, card: card["contexts"][0].update(
                step="Ш-99")),
            "сломана обратная связь К-36": ("обратная связь", lambda catalog, card: catalog["classSteps"]["К-36"].remove(
                "AIN-01")),
            "дублирован ID": ("повторный ID", lambda catalog, card: catalog["workingPrompts"].append(card)),
        }
        for name, (message, mutate) in tests.items():
            with self.subTest(name=name):
                candidate = deepcopy(data)
                card = next(card for card in candidate["workingPrompts"] if card["id"] ==
                            "mango-bcreq-context-understanding-system")
                mutate(candidate, card)
                with self.assertRaisesRegex(ValueError, message):
                    check_working_editions(ROOT, candidate)
                print(f"Мутация отклонена — {name}")

    def test_generator_rejects_invalid_source_links(self):
        subprocess.run(["node", "--test", str(EXPERIMENT / "working-data.test.mjs")], cwd=ROOT, check=True)

    def test_post_497_snapshot(self):
        subprocess.run([sys.executable, str(protection.OUT.with_name("protected_baseline.py")), "--check"],
                       cwd=ROOT, check=True)

    def test_post_497_mutations(self):
        base = read_json(ROOT, protection.OUT.relative_to(ROOT))
        ain_path = "prompts/drafts/a-in/bcreq-ain-01-understanding-stepwise.md"
        source = (ROOT / ain_path).read_text(encoding="utf-8")
        key = "a-in-kit.json:AIN-01"
        self.assertEqual(protection.counts(source), base["projections"][key])
        for marker in ("Проверки (receipt)", "ACCESS_GAP", "Итог шага", "КОНЕЦ AIN-01 <версия результата>",
                       next(iter(protection.RULE.findall(source)))):
            with self.subTest(marker=marker):
                candidate = deepcopy(base)
                replace = "КОНЕЦ AIN-01 v9.9" if marker.startswith("КОНЕЦ") else ""
                candidate["projections"][key] = protection.counts(source.replace(marker, replace, 1))
                self.assertTrue(any(marker in error and key in error
                                    for error in protection.regressions(base, candidate)))
                print(f"Мутация отклонена — {key}: {marker}")
        for rule in ("CT-01", "BP-01"):
            candidate = deepcopy(base)
            candidate["policy_ids"].remove(rule)
            self.assertTrue(any(rule in error for error in protection.regressions(base, candidate)))
            print(f"Мутация отклонена — отсутствует {rule}")
        candidate = deepcopy(base)
        del candidate["projections"][key]
        self.assertTrue(any(key in error for error in protection.regressions(base, candidate)))
        print(f"Мутация отклонена — исчезновение {key}")

    def test_site_json_reproducible(self):
        # Inputs are read from the checkout; all generator writes go to a disposable tree.
        generator = Path("scripts/generate-pages-data.mjs")
        site_data = ROOT / "site/data"
        with tempfile.TemporaryDirectory(prefix="bl231-site-") as tmp:
            target = Path(tmp)
            for directory in ("docs", "patterns", "pr-ops", "prompts", "runs", "standards"):
                (target / directory).symlink_to(ROOT / directory, target_is_directory=True)
            (target / generator.parent).mkdir()
            shutil.copy2(ROOT / generator, target / generator)
            output = target / "site/data"
            output.mkdir(parents=True)
            shutil.copy2(site_data / "step-handoff.json", output)
            generated_at = read_json(ROOT, "site/data/prompts.json")["generatedAt"]
            env = {**os.environ, "SITE_DATA_GENERATED_AT": generated_at}
            subprocess.run(["node", str(target / generator)], cwd=target, env=env, check=True)
            self.assertEqual({path.name for path in site_data.glob("*.json")},
                             {path.name for path in output.glob("*.json")})
            for path in site_data.glob("*.json"):
                self.assertEqual(path.read_bytes(), (output / path.name).read_bytes(), path.name)
            mutated = output / "prompts.json"
            mutated.write_bytes(mutated.read_bytes().replace(b'"family": "working"', b'"family": "legacy"', 1))
            self.assertNotEqual((site_data / "prompts.json").read_bytes(), mutated.read_bytes())
            print("Мутация отклонена — ручная правка site/data/prompts.json")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        result = unittest.TextTestRunner(verbosity=2).run(
            unittest.TestSuite([WorkingEditionsTest("test_working_editions")]))
        sys.exit(not result.wasSuccessful())
    unittest.main(verbosity=2)
