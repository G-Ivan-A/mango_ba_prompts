#!/usr/bin/env python3
"""Регрессионная проверка RFC стратегии автоматизации БА (issue #415).

RFC ``docs/rfc/2026-10-ba-automation-strategy.md`` собирает видение,
концепцию, архитектуру и дорожную карту автоматизации бизнес-анализа
команды крупных клиентов в одном документе для руководителей. Проверка
фиксирует контракт постановки, а не качество текста:

* RFC в статусе ``proposed``, frontmatter проходит валидатор Хаба, решения
  DEC-415-01…08 зарегистрированы в ``docs/rfc/rfc-register.md``;
* четыре раздела верхнего уровня, каждый с указанием канонического файла,
  и таблица переноса в ``docs/vision.md``, ``docs/concept.md``,
  ``docs/architecture.md``, ``docs/roadmap.md``;
* область — команда БА крупных клиентов (КК), а не все БА Манго;
* пять этапов: этап 1 — только BCREQ с ручным запуском промптов; этап 2 —
  агентный клиент (OpenCode) и оценка ТЗ заказчика, RUN-0077 — пример;
  этап 5 — масштабирование параллельно этапу 4;
* формат дорожной карты: карточка «что — зачем — как — сколько» у каждого
  этапа, списки «точно войдёт» и «не рассматривалось»;
* относительные ссылки и якоря разрешаются, внутреннего жаргона нет;
* канонические документы, ``runs/`` и сайт этим RFC не меняются.
"""

import re
import subprocess
import sys
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RFC = ROOT / "docs/rfc/2026-10-ba-automation-strategy.md"
RFC_REGISTER = ROOT / "docs/rfc/rfc-register.md"
CHANGELOG = ROOT / "CHANGELOG.md"

SECTIONS = {
    "## 1. Видение": "docs/vision.md",
    "## 2. Концепция": "docs/concept.md",
    "## 3. Архитектура": "docs/architecture.md",
    "## 4. Дорожная карта": "docs/roadmap.md",
}
STAGES = range(1, 6)
CARD_ROWS = ("**Что**", "**Зачем**", "**Как**", "**Сколько**")
DECISIONS = [f"DEC-415-{n:02d}" for n in range(1, 9)]
FORBIDDEN_TERMS = (
    "фаундер", "Фаундер", "Конард", "Proof of Execution", "Learning loop",
    "S1-S5", "S1–S5",
)

LINK = re.compile(r"\]\(([^\s)]+)\)")


def text(path):
    return path.read_text(encoding="utf-8")


def slug(heading):
    heading = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", heading).strip().lower()
    return re.sub(r"[^\w\- ]", "", heading).replace(" ", "-")


def anchors(path):
    found, seen, fenced = set(), Counter(), False
    for line in text(path).splitlines():
        if line.startswith("```"):
            fenced = not fenced
            continue
        found.update(re.findall(r'<a id="([^"]+)"', line))
        match = None if fenced else re.match(r"^#{1,6}\s+(.*?)\s*#*\s*$", line)
        if match:
            base = slug(match.group(1))
            found.add(base if not seen[base] else f"{base}-{seen[base]}")
            seen[base] += 1
    return found


def frontmatter(markdown):
    if not markdown.startswith("---\n"):
        return {}
    block = markdown[4:markdown.index("\n---\n", 4)]
    fields = {}
    for line in block.splitlines():
        if ":" in line and not line.startswith((" ", "-")):
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip().strip('"')
    return fields


def section(markdown, heading):
    """Текст раздела от заголовка до следующего заголовка того же уровня."""
    level = heading.split(" ", 1)[0]
    start = markdown.index(heading + "\n")
    rest = markdown[start + len(heading):]
    match = re.search(rf"^{level} ", rest, re.M)
    return rest[: match.start()] if match else rest


def table_rows(markdown, header):
    lines = markdown.split(header, 1)[1].splitlines()[2:]
    rows = []
    for line in lines:
        if not line.startswith("|"):
            break
        rows.append([cell.strip() for cell in line.strip().strip("|").split("|")])
    return rows


class StrategyRfcTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.md = text(RFC)
        cls.fm = frontmatter(cls.md)
        cls.roadmap = section(cls.md, "## 4. Дорожная карта")

    def test_frontmatter_and_status(self):
        self.assertEqual(self.fm.get("status"), "proposed")
        self.assertEqual(self.fm.get("owner"), "G-Ivan-A")
        self.assertIn("issues/415", self.fm.get("source", ""))
        for issue in ("409", "411", "415"):
            self.assertIn(f"issues/{issue}", self.fm.get("related_issues", ""))
        self.assertNotIn("ai-generated", self.fm)
        proc = subprocess.run(["./tools/validate-frontmatter.sh", str(RFC)], cwd=ROOT,
                              capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_executive_summary_first(self):
        body = self.md.split("\n---\n", 1)[1]
        headings = re.findall(r"^## (.+)$", body, re.M)
        self.assertEqual(headings[:2], ["Кратко для руководителя", "Как читать"])

    def test_four_sections_name_their_canonical_file(self):
        for heading, target in SECTIONS.items():
            with self.subTest(section=heading):
                body = section(self.md, heading)
                note = body.strip().splitlines()[0]
                self.assertTrue(note.startswith("> Переносится в"), note)
                self.assertIn(f"(../{target.split('/', 1)[1]})", note)
                self.assertTrue((ROOT / target).exists())

    def test_transfer_table_covers_all_sections(self):
        rows = table_rows(self.md, "| Раздел RFC | Канонический файл |")
        targets = {re.search(r"`(docs/[^`]+)`", row[1]).group(1) for row in rows}
        self.assertEqual(targets, set(SECTIONS.values()))

    def test_scope_is_large_clients_team(self):
        title = re.search(r"^# (.+)$", self.md, re.M).group(1)
        self.assertIn("команды крупных клиентов", title)
        scope = section(self.md, "### Область")
        self.assertIn("Команда БА крупных клиентов (КК) на этапах 1–4", scope)
        self.assertIn("Другие команды БА Манго — до решения по этапу 5", scope)

    def test_five_stages_with_card(self):
        for n in STAGES:
            with self.subTest(stage=n):
                heading = re.search(rf"^### Этап {n}\. .+$", self.roadmap, re.M)
                self.assertIsNotNone(heading, f"нет карточки этапа {n}")
                card = section(self.roadmap, heading.group(0))
                for row in CARD_ROWS:
                    self.assertIn(f"| {row} |", card)
        summary = table_rows(self.roadmap, "| Этап | Что | Зачем | Как | Сколько (гипотеза) | Статус |")
        self.assertEqual([row[0] for row in summary], [str(n) for n in STAGES])

    def test_stage_1_is_bcreq_only(self):
        card = section(self.roadmap, "### Этап 1. Промпты в чате: только BCREQ")
        self.assertIn("Других процессов на этапе 1 нет", card)
        self.assertNotIn("оценк", card.lower())

    def test_stage_2_agent_client_and_spec_assessment(self):
        card = section(self.roadmap, "### Этап 2. Агентный клиент и оценка ТЗ")
        for needle in ("OpenCode", "оценки ТЗ заказчика", "RUN-0077", "навыки (skills)",
                       "маршрутизатор промптов", "MCP"):
            self.assertIn(needle, card)
        self.assertIn("пример формы и уровня доказательности, а не эталон", self.md)
        self.assertTrue((ROOT / "runs/2026/RUN-0077/outputs/README.md").exists())

    def test_stage_5_parallel_to_stage_4(self):
        card = section(self.roadmap, "### Этап 5. Масштабирование на продуктовые команды и других аналитиков")
        self.assertIn("Идёт параллельно этапу 4", card)
        self.assertIn("Ворота 3: практики этапов 1–3 отработаны", card)
        self.assertIn('S3 -->|"ворота 3: практики отработаны"| S5', self.roadmap)

    def test_in_scope_and_not_considered_lists(self):
        for header in ("### Что точно войдёт в дорожную карту", "### Что не рассматривалось",
                       "### Что рассматривалось и отклонено"):
            with self.subTest(list=header):
                rows = [line for line in section(self.roadmap, header).splitlines()
                        if line.startswith("| ") and not line.startswith("| ---")]
                self.assertGreaterEqual(len(rows) - 1, 5)
        in_scope = section(self.roadmap, "### Что точно войдёт в дорожную карту")
        for stage in STAGES:
            self.assertRegex(in_scope, rf"\| {stage} \|")

    def test_estimates_are_hypotheses(self):
        fmt = section(self.roadmap, "### Формат")
        self.assertIn("гипотеза планирования", fmt)
        self.assertIn("назначает", fmt)

    def test_decisions_anchored_and_registered(self):
        register = text(RFC_REGISTER)
        own = anchors(RFC)
        for dec in DECISIONS:
            with self.subTest(decision=dec):
                anchor = dec.lower()
                self.assertIn(anchor, own)
                self.assertIn(f"| [RFC-415-DEC-{dec[-2:]}](2026-10-ba-automation-strategy.md#{anchor}) |",
                              register)
        self.assertIn('"docs/rfc/2026-10-ba-automation-strategy.md"', register.split("\n---\n", 1)[0])

    def test_links_resolve(self):
        missing = []
        for target in LINK.findall(self.md):
            if target.startswith(("http://", "https://")):
                continue
            path, _, frag = target.partition("#")
            resolved = (RFC.parent / path).resolve() if path else RFC
            if not resolved.exists():
                missing.append(target)
            elif frag and resolved.suffix == ".md" and frag not in anchors(resolved):
                missing.append(target)
        self.assertEqual(missing, [])

    def test_mermaid_labels_quoted(self):
        for block in re.findall(r"```mermaid\n(.*?)```", self.md, re.S):
            for label in re.findall(r"\w+\[([^\]]*)\]", block):
                if not label.startswith("("):
                    self.assertTrue(label.startswith('"'), label)

    def test_no_internal_jargon(self):
        for term in FORBIDDEN_TERMS:
            self.assertNotIn(term, self.md)

    def test_canonical_documents_untouched(self):
        for target in SECTIONS.values():
            fm = frontmatter(text(ROOT / target))
            self.assertEqual(fm.get("version"), "1.0", f"{target}: перенос — отдельной задачей")

    def test_changelog(self):
        self.assertIn("Issue #415", text(CHANGELOG).split("\n## ", 2)[1])


if __name__ == "__main__":
    unittest.main(verbosity=1 if "-q" in sys.argv else 2, argv=[sys.argv[0]])
