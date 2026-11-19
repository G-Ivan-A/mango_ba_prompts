#!/usr/bin/env python3
"""Runtime issue #25: RFC-RT-002 «Универсальный агентный контекст runtime».

Задача — в G-Ivan-A/mango-ba-ai-runtime, RFC и бэклог — в спице. Проверяет
без LLM, без сети и без клона runtime:

* RFC: frontmatter (``status: proposed``, ``type: rfc``, ``rfc-scope``),
  гипотезы Г1–Г3 с вердиктом, обязательные разделы DoD и решения
  Р-RT-1…Р-RT-N без пропусков и повторов;
* реестр RFC: строка RFC-RT-002 и запись журнала;
* бэклог: BL-184 ``DONE`` в карточке и в таблице, карточки BL-191 и BL-192
  в модели и в ``pr-ops/BACKLOG.md``, движение по цепочке runtime #25;
* тексты промптов не менялись: коммиты задачи (``runtime-25`` в
  сообщении) не трогают ``prompts/``.
"""
import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RFC = ROOT / "docs/rfc/2026-11-runtime-universal-agent-context.md"
REGISTRY = ROOT / "docs/rfc/rfc-registry.md"
BACKLOG = ROOT / "pr-ops/BACKLOG.md"
MODEL = ROOT / "pr-ops/backlog-ba-model.md"

RUNTIME_ISSUE = "https://github.com/G-Ivan-A/mango-ba-ai-runtime/issues/25"
CARDS = {
    "BL-191": "RFC универсального агентного контекста runtime",
    "BL-192": "Производство универсального агентного контекста runtime",
}
# Разделы, которых требует DoD runtime #25.
SECTIONS = [
    "## Summary / BLUF",
    "## 2. Аудит As-Is (ФТ-1)",
    "## 3. Индустриальные источники и матрица совместимости клиентов",
    "## 4. Целевая архитектура (ФТ-2)",
    "## 5. Приём SSOT этапа 1 (ФТ-3)",
    "## 6. Обратная совместимость (ФТ-4)",
    "## 7. Вывод legacy из эксплуатации (ФТ-5)",
    "## 8. Миграция, валидация и откат (ФТ-6)",
    "## 9. Решения на согласование",
    "## 10. Движение по бэклогу",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not match:
        return {}
    fields = {}
    for line in match.group(1).splitlines():
        key, sep, value = line.partition(":")
        if sep and not line.startswith(" "):
            fields[key.strip()] = value.strip().strip('"')
    return fields


class RfcTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = read(RFC)
        cls.meta = frontmatter(cls.text)

    def test_frontmatter(self):
        self.assertEqual(self.meta.get("status"), "proposed")
        self.assertEqual(self.meta.get("type"), "rfc")
        self.assertEqual(self.meta.get("rfc-scope"), "multi")
        self.assertEqual(self.meta.get("source"), RUNTIME_ISSUE)
        self.assertIn("issues/492", self.meta.get("related_issues", ""))

    def test_title(self):
        self.assertRegex(self.text, r"(?m)^# RFC-RT-002: ")

    def test_sections(self):
        for section in SECTIONS:
            with self.subTest(section=section):
                self.assertIn(section, self.text)

    def test_hypotheses_have_verdicts(self):
        for hypothesis in ("Г1", "Г2", "Г3"):
            with self.subTest(hypothesis=hypothesis):
                self.assertRegex(self.text, rf"(?m)^\| {hypothesis}\. .*\| \*\*Подтверждена")

    def test_decisions_are_numbered_without_gaps(self):
        table = self.text.split("## 9. Решения на согласование", 1)[1].split("\n## ", 1)[0]
        numbers = [int(n) for n in re.findall(r"(?m)^\| Р-RT-(\d+) \|", table)]
        self.assertTrue(numbers, "нет решений Р-RT")
        self.assertEqual(numbers, list(range(1, len(numbers) + 1)))
        for number in set(int(n) for n in re.findall(r"Р-RT-(\d+)", self.text)):
            self.assertLessEqual(number, len(numbers), f"ссылка на несуществующее Р-RT-{number}")

    def test_estimates_are_hypotheses(self):
        section = self.text.split("## 8. Миграция", 1)[1].split("\n## ", 1)[0]
        self.assertIn("Оценка (гипотеза)", section)
        self.assertIn("Откат", section)

    def test_unverified_sources_are_marked(self):
        self.assertIn("ACCESS_GAP", self.text)
        self.assertIn("UNVERIFIED", self.text)


class RegistryTest(unittest.TestCase):
    def test_row_and_journal(self):
        text = read(REGISTRY)
        self.assertRegex(
            text, r"(?m)^\| \[RFC-RT-002\]\(2026-11-runtime-universal-agent-context\.md\) \|.*\| proposed \|"
        )
        self.assertRegex(text, r"(?m)^- \*\*2026-11-19\*\* — runtime issue #25 .*RFC-RT-002")
        self.assertIn("docs/rfc/2026-11-runtime-universal-agent-context.md", text.split("---", 2)[1])


class BacklogTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = read(MODEL)
        cls.backlog = read(BACKLOG)

    def test_cards(self):
        for card, title in CARDS.items():
            with self.subTest(card=card):
                self.assertIn(f"### {card}. {title}", self.model)
                self.assertRegex(self.backlog, rf"(?m)^\| {card} \| \[{re.escape(title)}\]")

    def test_previous_step_is_done(self):
        card = self.model.split("### BL-184.", 1)[1].split("\n### ", 1)[0]
        self.assertIn("**Статус.** `DONE`", card)
        self.assertRegex(self.backlog, r"(?m)^\| BL-184 \| .*\| BL-183 \| DONE \|")

    def test_chain(self):
        self.assertIn("**Движение по цепочке (runtime #25).**", self.backlog)
        chain = self.backlog.split("**Движение по цепочке (runtime #25).**", 1)[1].split("\n\n", 1)[0]
        for card in ("BL-184", "BL-191", "BL-192", "BL-185", "BL-131", "BL-132"):
            with self.subTest(card=card):
                self.assertIn(card, chain)
        self.assertIn("Миграция защищённых путей", chain)

    def test_statuses(self):
        self.assertRegex(self.backlog, r"(?m)^\| BL-191 \| .*\| review \|")
        self.assertRegex(self.backlog, r"(?m)^\| BL-192 \| .*\| deferred \(triggered\) \|")


class PromptsUnchangedTest(unittest.TestCase):
    """Раздел 5 runtime #25: тексты промптов и навыков не производятся."""

    def test_issue_commits_do_not_touch_prompts(self):
        res = subprocess.run(
            ["git", "log", "--no-merges", "--format=%h %s", "--grep=runtime-25", "--", "prompts/"],
            cwd=ROOT, capture_output=True, text=True,
        )
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertEqual(res.stdout.strip(), "", "коммиты runtime #25 меняют тексты промптов")


if __name__ == "__main__":
    unittest.main(verbosity=1)
