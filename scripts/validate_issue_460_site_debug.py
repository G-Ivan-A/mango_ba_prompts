#!/usr/bin/env python3
"""Регрессионная проверка issue #460: полнота тестового набора, пароль, чтение.

Проверки:

* полнота: ``site/data/test-kit.json`` содержит все шаги таблицы «Порядок шагов»
  комплекта; генератор падает на мутациях комплекта и данных
  (``assertTestKitComplete``); импорт генератора ничего не генерирует;
* вкладка по умолчанию: первая вкладка «Процессов» показывает все шаги;
* чтение: текст редакции через ``textContent``, контейнер с ``max-height: 60vh`` и
  ``overflow-y: auto``, панель с кнопками прилипает;
* пароль: проверка проходит и при отключённом, и при возвращённом пароле, поэтому
  откат не требует правки валидатора. При отключении обязательны комментарий и заметка
  в документе; код входа и запись ``site`` обязательны всегда;
* тексты промптов: тела в данных равны файлам-источникам;
* версия сайта, бэклог BL-169 и постановка задачи.

Браузерная проверка: ``experiments/issue_460/browser-check.cjs``.

Запуск: ``python3 scripts/validate_issue_460_site_debug.py``
"""

from __future__ import annotations

import json
import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GATE_TODO = "// TODO: вернуть пароль после завершения отладки BL-157в"
EXPECTED_CODES = {f"Ш-{n}" for n in range(10)} | {"Ш-В", "Ш-Р", "Ш-С"}

# Мутации настоящего комплекта через настоящий makeTestKit; печатает JSON с итогами.
MUTATION_SCRIPT = r"""
import fs from "node:fs/promises";
const generator = await import(process.argv[1]);
const kitPath = process.argv[2];
const prompts = JSON.parse(await fs.readFile(process.argv[3], "utf8")).prompts;
const markdown = await fs.readFile(kitPath, "utf8");
const outcome = async (text, list = prompts) => {
  try {
    const kit = await generator.makeTestKit(text, list);
    return { ok: true, steps: kit.counts.steps };
  } catch (error) {
    return { ok: false, message: error.message };
  }
};
const lines = markdown.split("\n");
const dropRows = (predicate) => lines.filter((line) => !predicate(line)).join("\n");
const stepRow = (code) => (line) => line.startsWith("|") && line.includes(`| ${code} `) && line.includes("](");
const firstPublished = prompts.find((item) => markdown.includes(item.sourcePath.replace("prompts/", "")) && item.body);
const results = {
  intact: await outcome(markdown),
  rowRemoved: await outcome(dropRows(stepRow("Ш-5"))),
  everythingAboutStepRemoved: await outcome(
    dropRows((line) => line.startsWith("|") && line.includes("UC, прогон 2"))
      .replace(/Ш-8,\s*/g, ""),
  ),
  emptyPublishedBody: await outcome(
    markdown,
    prompts.map((item) => (item.id === firstPublished.id ? { ...item, body: "  \n" } : item)),
  ),
  minimum: generator.TEST_KIT_MIN_STEPS,
};
process.stdout.write(JSON.stringify(results));
"""


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def css_rule(css: str, selector: str) -> str:
    match = re.search(rf"(?m)^\s*{re.escape(selector)} \{{(.*?)\}}", css, re.S)
    if not match:
        raise AssertionError(f"нет правила {selector}")
    return match.group(1)


class Completeness(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.kit = json.loads(read("site/data/test-kit.json"))
        cls.markdown = read("docs/ba-processes/bcreq-run-kit.md")

    def test_every_step_of_the_kit_table_is_in_the_data(self):
        section = self.markdown.split("## 1.", 1)[1].split("\n## ", 1)[0]
        # Первая таблица раздела — «Порядок шагов»; ниже идут таблицы карточек и этапов.
        lines = section.splitlines()
        start = next(index for index, line in enumerate(lines) if line.startswith("|"))
        table = []
        for line in lines[start:]:
            if not line.startswith("|"):
                break
            table.append(line)
        rows = [line for line in table if re.match(r"\|\s*(\d+|—)\s*\|", line)]
        table_codes = [row.split("|")[2].split()[0] for row in rows]
        self.assertGreaterEqual(len(table_codes), 13)
        self.assertEqual(table_codes, [step["step"].split()[0] for step in self.kit["steps"]])
        self.assertEqual(self.kit["counts"]["steps"], len(table_codes))

    def test_known_steps_are_present(self):
        self.assertTrue(EXPECTED_CODES <= {step["step"].split()[0] for step in self.kit["steps"]})

    def test_groups_cover_all_steps(self):
        self.assertEqual(sum(group["count"] for group in self.kit["groups"]), self.kit["counts"]["steps"])

    def test_generator_fails_closed(self):
        result = subprocess.run(
            [
                "node", "--input-type=module", "-e", MUTATION_SCRIPT,
                (ROOT / "scripts/generate-pages-data.mjs").as_uri(),
                str(ROOT / "docs/ba-processes/bcreq-run-kit.md"),
                str(ROOT / "site/data/prompts.json"),
            ],
            capture_output=True, text=True, timeout=60, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("Generated", result.stdout, "импорт генератора запустил генерацию")
        outcome = json.loads(result.stdout)
        self.assertEqual(outcome["intact"], {"ok": True, "steps": self.kit["counts"]["steps"]})
        self.assertEqual(outcome["minimum"], 13)
        self.assertFalse(outcome["rowRemoved"]["ok"])
        self.assertIn("неполон", outcome["rowRemoved"]["message"])
        self.assertIn("Ш-5", outcome["rowRemoved"]["message"])
        self.assertFalse(outcome["everythingAboutStepRemoved"]["ok"])
        self.assertIn("минимум 13", outcome["everythingAboutStepRemoved"]["message"])
        self.assertFalse(outcome["emptyPublishedBody"]["ok"])
        self.assertIn("нет текста промпта", outcome["emptyPublishedBody"]["message"])


class AllStepsView(unittest.TestCase):
    def test_all_steps_is_the_default_view(self):
        app = read("site/app.js")
        views = app[app.index("function processViews()"):]
        self.assertLess(views.index("TEST_KIT_ALL_VIEW"), views.index("...groups.map"))
        self.assertIn(
            "group.hidden = current.id !== TEST_KIT_ALL_VIEW && group.dataset.group !== current.id;", app
        )


class Reader(unittest.TestCase):
    def test_text_is_shown_verbatim(self):
        app = read("site/app.js")
        self.assertIn("text.textContent = testKitBody(step, kind)", app)
        start = app.index("function testKitReader(")
        end = app.index("function renderTestKit()")
        self.assertNotIn("innerHTML", app[start:end])

    def test_container_scrolls_and_toolbar_sticks(self):
        css = read("site/styles.css")
        text = css_rule(css, ".testkit-prompt-text")
        self.assertIn("max-height: 60vh;", text)
        self.assertIn("overflow-y: auto;", text)
        bar = css_rule(css, ".testkit-reader-bar")
        self.assertIn("position: sticky;", bar)
        self.assertIn("top: var(--topbar-height", bar)

    def test_controls_exist(self):
        app = read("site/app.js")
        self.assertIn('"⧉ Копировать"', app)
        self.assertIn("data-testkit-edition", app)
        self.assertIn('"aria-pressed"', app)

    def test_first_line_of_copy_is_kept(self):
        self.assertIn("await copyText(`<!-- ${variant.id} · ${step.step} -->\\n\\n${body}`);", read("site/app.js"))


class PromptTexts(unittest.TestCase):
    """Текст на экране равен источнику: данные повторяют файлы промптов."""

    @staticmethod
    def source_body(relative: str) -> str:
        content = read(relative)
        if content.startswith("---\n"):
            content = content[content.index("\n---", 4) + 4:]
        return re.sub(r"^\s*<!--\s*EXPERIMENTAL[^>]*-->\s*\n", "", content, count=1, flags=re.M).strip()

    def test_bodies_equal_sources(self):
        kit = json.loads(read("site/data/test-kit.json"))
        catalog = {item["id"]: item for item in json.loads(read("site/data/prompts.json"))["prompts"]}
        for step in kit["steps"]:
            if step["draft"]:
                self.assertEqual(step["draft"]["body"].strip(), self.source_body(step["draft"]["sourcePath"]))
            if step["published"]:
                prompt = catalog[step["published"]["id"]]
                self.assertEqual(prompt["body"].strip(), self.source_body(prompt["sourcePath"]))


class Gate(unittest.TestCase):
    """Проходит в обоих состояниях: откат пароля не требует правки валидатора."""

    def test_login_code_is_kept_in_any_state(self):
        gate = read("site/gate.js")
        for needle in ("entry.salt + input.value", "crypto.subtle.digest", "sessionStorage", 'const ENTRY = "site"'):
            self.assertIn(needle, gate)
        self.assertIn('id="login-form"', read("site/login.html"))
        entry = json.loads(read("site/password-hashes.json"))["site"]
        self.assertRegex(entry["salt"], r"^[a-f0-9]{16}$")
        self.assertRegex(entry["hash"], r"^[a-f0-9]{64}$")

    def test_disabled_gate_is_documented(self):
        gate = read("site/gate.js")
        if "const GATE_DISABLED = true;" not in gate:
            self.assertNotIn(GATE_TODO, gate, "пароль возвращён, напоминание нужно снять")
            return
        self.assertLess(gate.index(GATE_TODO), gate.index("const GATE_DISABLED = true;"))
        self.assertIn("if (GATE_DISABLED) {", gate)
        self.assertIn("GATE_DISABLED = true", read("docs/site-access.md"))


class Project(unittest.TestCase):
    def test_site_version(self):
        self.assertIn('version: "2.5.1"', read("scripts/generate-pages-data.mjs"))
        self.assertEqual(read("site/index.html").count("v2.5.1"), 2)
        self.assertEqual(json.loads(read("site/data/stats.json"))["siteVersion"]["version"], "2.5.1")

    def test_backlog(self):
        self.assertRegex(read("pr-ops/BACKLOG.md"), r"\| BL-169 \|.*\| deferred \(triggered\) \|")
        self.assertIn("### BL-169. Вернуть пароль сайта", read("pr-ops/backlog-ba-model.md"))

    def test_task_statement(self):
        statement = read("experiments/issue_460/task-statement.md")
        for section in ("## Проверка гипотез постановки", "## Граничные случаи", "## WBS", "## Definition of Done"):
            self.assertIn(section, statement)


if __name__ == "__main__":
    unittest.main()
