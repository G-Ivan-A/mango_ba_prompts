#!/usr/bin/env python3
"""Issue #495: чистота исполнимых промптов — сторожа стандарта и их мутации.

Проверяет без LLM и без сети (стандарт ``standards/bcreq-prompt-purity.md``):

* ЧП-1…ЧП-3, ЧП-5: аудитор ``scripts/audit_prompt_purity.py`` на рабочем
  дереве — 0 нарушений классов а/б/в во всём контуре (промпты, черновики,
  системный трек, стандарты классов, ССОТ A-IN, данные сайта);
* мутации: в копию контура во временном каталоге вносится одно нарушение —
  аудитор обязан его найти (URL приватного репозитория в промпте и в данных
  сайта, голое имя репозитория, относительная ссылка, ссылка на runtime не по
  закреплённому SHA, кейс-токены, HTML-комментарий, отсылка к BL/issue);
* ЧП-4: сборщики ССОТ в режиме ``--check`` и реестр обратимых правок
  ``experiments/issue_495/prompt-edits.json`` актуальны — ручная правка
  сгенерированного файла ловится;
* ЧП-6: версия сайта — patch-серия 2.9.x, не ниже 2.9.0, одинакова в
  генераторе, данных и разметке; мутации 2.10.0 и 2.8.9 падают;
* реестр runtime: ссылки на runtime — только по SHA из ``runtime_sha``;
  справочники И-11/И-12 и задачи РТ-8/РТ-9 заведены, заглушка З-5 активна;
* бэклог: цепочка BL-240 → BL-241 → BL-242 → BL-232 в ``pr-ops/BACKLOG.md``.
"""
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import audit_prompt_purity as audit  # noqa: E402

POLICY = "standards/bcreq-prompt-purity.json"
REGISTRY = "standards/bcreq-runtime-references.md"
PROMPT = "prompts/bcreq-fr-documentation-stepwise.md"
SITE = "site/data/a-in-kit.json"
#: Опубликованная версия сайта на начало задачи; patch-серия — только 2.9.x.
PUBLISHED = (2, 9, 0)
SERIES = (2, 9)


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def load_module(rel, name):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


PURITY = load_module("scripts/prompt_purity.py", "prompt_purity_495")


def version_errors(version, published=PUBLISHED, series=SERIES):
    """Нарушения ЧП-6 для строки версии; пусто — версия допустима."""
    match = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", version or "")
    if not match:
        return [f"версия {version!r} не в формате X.Y.Z"]
    parts = tuple(map(int, match.groups()))
    errors = []
    if parts[:2] != series:
        errors.append(f"версия {version} вне patch-серии {series[0]}.{series[1]}.x")
    if parts < published:
        errors.append(f"версия {version} ниже опубликованной {'.'.join(map(str, published))}")
    return errors


class Sandbox:
    """Минимальная копия контура: политика, реестр runtime и выбранные файлы."""

    def __init__(self, files):
        self.dir = tempfile.TemporaryDirectory(prefix="i495-")
        self.root = Path(self.dir.name)
        for rel in [POLICY, REGISTRY, *files]:
            target = self.root / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / rel, target)

    def write(self, rel, text):
        (self.root / rel).write_text(text, encoding="utf-8")

    def run(self):
        return audit.Auditor(self.root).run()

    def close(self):
        self.dir.cleanup()


class RepoAuditTest(unittest.TestCase):
    """ЧП-1…ЧП-3, ЧП-5: рабочее дерево чистое."""

    def test_repo_has_zero_findings(self):
        auditor = audit.Auditor(ROOT)
        findings = auditor.run()
        listing = "\n".join(f"{f['file']}:{f['line']} {f['class']} {f['rule']} {f['match']}" for f in findings[:20])
        self.assertEqual(findings, [], f"нарушений: {len(findings)}\n{listing}")
        kinds = set(auditor.files.values())
        self.assertEqual(kinds, {"prompt_texts", "archive_texts", "ssot_texts", "repo_docs_in_prompts", "site_data"})
        # Контур не пустой: промпты, 39 стандартов классов, черновики, данные сайта.
        prompts = [f for f, k in auditor.files.items() if k == "prompt_texts"]
        self.assertGreaterEqual(len([f for f in prompts if f.startswith("standards/bcreq-manual-classes/")]), 39)
        self.assertTrue(any(f.startswith("prompts/drafts/a-in/") for f in prompts))
        self.assertTrue(any(f.startswith("prompts/drafts/system/") for f in prompts))
        self.assertIn("site/data/prompts.json", auditor.files)

    def test_no_private_url_in_site_data_anywhere(self):
        # Сильнее аудитора: ни одной строки с URL спицы в любом JSON сайта.
        rx = re.compile(audit.load_policy(ROOT / POLICY)["links"]["private_link_regex"])
        for path in sorted((ROOT / "site/data").glob("*.json")):
            self.assertIsNone(rx.search(path.read_text(encoding="utf-8")), path.name)

    def test_projection_is_idempotent_on_prompts(self):
        for path in sorted((ROOT / "prompts").glob("*.md")):
            text = path.read_text(encoding="utf-8")
            self.assertEqual(PURITY.project(text), PURITY.project(PURITY.project(text)), path.name)


class MutationTest(unittest.TestCase):
    """Каждая мутация обязана дать нарушение нужного правила."""

    def setUp(self):
        self.box = Sandbox([PROMPT, SITE])
        self.sha = audit.runtime_sha(ROOT)

    def tearDown(self):
        self.box.close()

    def rules(self):
        return {(f["class"], f["rule"], f["file"]) for f in self.box.run()}

    def mutate_prompt(self, line):
        text = read(PROMPT)
        anchor = text.index("\n## ") + 1
        self.box.write(PROMPT, text[:anchor] + line + "\n\n" + text[anchor:])

    def test_baseline_clean(self):
        self.assertEqual(self.box.run(), [])

    def test_private_url_in_prompt(self):
        self.mutate_prompt("См. [контракт](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/x.md).")
        self.assertIn(("a", "A-PRIVATE", PROMPT), self.rules())

    def test_bare_private_name_in_prompt(self):
        self.mutate_prompt("Источник — репозиторий mango_ba_prompts.")
        self.assertIn(("a", "A-PRIVATE-NAME", PROMPT), self.rules())

    def test_relative_link_in_prompt(self):
        self.mutate_prompt("См. [стандарт](../standards/prompt-standard.md).")
        self.assertIn(("a", "A-RELATIVE", PROMPT), self.rules())

    def test_unpinned_runtime_link(self):
        self.mutate_prompt("См. https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/main/golden/x.yaml")
        self.assertIn(("a", "A-RUNTIME-UNPINNED", PROMPT), self.rules())

    def test_pinned_runtime_link_is_allowed(self):
        self.mutate_prompt(f"См. https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/{self.sha}/golden/x.yaml")
        self.assertEqual(self.box.run(), [])

    def test_case_tokens_in_prompt(self):
        for token, rule in [("amoCRM", "CT-01"), ("коннектор", "CT-03"), ("ВАТС", "CT-04"), ("ЛК", "CT-05"),
                            ("HDE", "CT-06"), ("Битрикс24", "CT-07"), ("задача 1075", "CT-08")]:
            with self.subTest(token=token):
                self.mutate_prompt(f"Проверь интеграцию: {token} и смежные данные.")
                self.assertIn(("b", rule, PROMPT), self.rules())

    def test_ballast_in_prompt(self):
        for line, rule in [("<!-- Experimental: for BL-156 -->", "BP-01"), ("Добавлено по BL-123.", "BP-04"),
                           ("Редакция по тесту.", "BP-06"), ("См. issue про шаг.", "BP-03")]:
            with self.subTest(line=line):
                self.mutate_prompt(line)
                self.assertIn(("c", rule, PROMPT), self.rules())

    def test_private_url_in_site_data(self):
        data = json.loads(read(SITE))
        data["steps"][0]["sourceUrl"] = "https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/" + PROMPT
        self.box.write(SITE, json.dumps(data, ensure_ascii=False))
        self.assertIn(("a", "A-PRIVATE", SITE), self.rules())

    def test_case_token_and_comment_in_site_prompt_body(self):
        data = json.loads(read(SITE))
        data["steps"][0]["prompt"] += "\n<!-- маркер -->\nСверь коннектор с amoCRM."
        self.box.write(SITE, json.dumps(data, ensure_ascii=False))
        found = self.rules()
        for rule in [("c", "BP-01", SITE), ("b", "CT-03", SITE), ("b", "CT-01", SITE)]:
            self.assertIn(rule, found)


class VersionTest(unittest.TestCase):
    """ЧП-6: только 2.9.x, не ниже опубликованной 2.9.0."""

    def test_site_version_consistent_and_allowed(self):
        version = json.loads(read("site/data/prompts.json"))["siteVersion"]["version"]
        self.assertEqual(version_errors(version), [])
        self.assertEqual(json.loads(read("site/data/stats.json"))["siteVersion"]["version"], version)
        self.assertIn(f'version: "{version}"', read("scripts/generate-pages-data.mjs"))
        html = read("site/index.html")
        self.assertIn(f">v{version}<", html)
        self.assertEqual(set(re.findall(r">v(\d+\.\d+\.\d+)<", html)), {version})
        self.assertIn(f"Версия сайта {version}", read("CHANGELOG.md"))

    def test_version_mutations_fail(self):
        for bad in ["2.10.0", "2.8.9", "3.0.0", "2.9", "v2.9.1"]:
            with self.subTest(version=bad):
                self.assertNotEqual(version_errors(bad), [])
        for good in ["2.9.0", "2.9.1", "2.9.17"]:
            with self.subTest(version=good):
                self.assertEqual(version_errors(good), [])


class SsotTest(unittest.TestCase):
    """ЧП-4: сгенерированное совпадает с выходом сборщиков."""

    def check(self, *cmd):
        proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, f"{' '.join(cmd)}\n{proc.stdout}\n{proc.stderr}")

    def test_builders_check(self):
        for script in ["scripts/bcreq_handoff.py", "scripts/build_bcreq_a_in.py",
                       "scripts/build_bcreq_step_prompts.py", "scripts/build_bcreq_system_track.py"]:
            with self.subTest(script=script):
                self.check(sys.executable, script, "--check")

    def test_prompt_edits_registry_current(self):
        self.check(sys.executable, "experiments/issue_495/build_prompt_edits.py", "--check")


class RegistryAndBacklogTest(unittest.TestCase):
    def test_runtime_registry_rows(self):
        text = read(REGISTRY)
        self.assertRegex(text, r'(?m)^runtime_sha:\s*"?[0-9a-f]{40}"?')
        for marker in ["И-11", "И-12", "З-5", "РТ-8", "РТ-9", "taxonomy/product-profiles.yaml",
                       "golden/prompt-regressions.yaml"]:
            self.assertIn(marker, text)
        sha = audit.runtime_sha(ROOT)
        # Ссылки на коммит runtime в действующих разделах 1–6 — только на
        # закреплённый SHA (шаблон «<SHA>» в инструкции — не ссылка; раздел 7 —
        # история закрытого долга со старыми путями на main).
        live = text.split("\n## 7. ", 1)[0]
        for match in re.finditer(r"mango-ba-ai-runtime/(?:blob|tree)/([^/\s)]+)", live):
            if not match.group(1).startswith("<"):
                self.assertEqual(match.group(1), sha, match.group(0))

    def test_case_register_traces_to_runtime(self):
        policy = audit.load_policy(ROOT / POLICY)
        ids = [c["id"] for c in policy["case_register"]]
        self.assertTrue(ids)
        self.assertEqual(len(ids), len(set(ids)))
        for case in policy["case_register"]:
            self.assertIn("golden/prompt-regressions.yaml", json.dumps(case, ensure_ascii=False), case["id"])

    def test_backlog_chain(self):
        backlog = read("pr-ops/BACKLOG.md")
        cards = read("pr-ops/backlog-repository.md")
        for card in ["BL-240", "BL-241", "BL-242", "BL-232"]:
            self.assertRegex(backlog, rf"(?m)^\|\s*{card}\s*\|", card)
            self.assertRegex(cards, rf"(?m)^### {card}\. ", f"карточка {card}")
        for card, follow in [("BL-240", "BL-241"), ("BL-241", "BL-242"), ("BL-242", "BL-232")]:
            row = re.search(rf"(?m)^\|\s*{card}\s*\|.*$", backlog).group(0)
            self.assertIn(follow, row, f"{card} → {follow}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
