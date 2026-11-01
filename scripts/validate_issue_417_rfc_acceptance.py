#!/usr/bin/env python3
"""Регрессионная проверка принятия RFC стратегии автоматизации БА (issue #417).

Владелец рассмотрел RFC ``docs/rfc/2026-10-ba-automation-strategy.md`` v0.1
(#415) и в #417 поставил две задачи. Проверка фиксирует контракт постановки:

* задача 1 — исправления внесены, статус принятия зафиксирован:
  RFC ``accepted`` v0.2; видение и концепция приняты предварительно,
  архитектура и дорожная карта — с исправлениями; этап 2 — OpenCode;
  этап 3 — потоки n8n на выделенном сервере как испытательный стенд;
  этап 4 — промышленное решение без n8n, код на Python под управлением
  исполнителя процессов, способ разработки — в начале этапа 4; витрина —
  GitHub Pages на этапах 1–3, решение о портале на этапе 3; правило
  пересмотра; 14 промптов — снимок as-is;
* задача 2 — контрольная проверка на соответствие индустриальным
  практикам: отчёт в ``docs/analysis/``, вердикт «критичных отклонений
  нет», рекомендации REC-417-01…06 предложены (``proposed``), а не внесены;
* решения DEC-415-01…12 и рекомендации зарегистрированы в реестре RFC;
* канонические документы ``docs/`` не изменены (перенос — отдельной задачей).
"""

import re
import subprocess
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_issue_415_strategy_rfc import (  # noqa: E402
    LINK, SECTIONS, anchors, frontmatter, section, table_rows, text,
)

ROOT = Path(__file__).resolve().parents[1]
RFC = ROOT / "docs/rfc/2026-10-ba-automation-strategy.md"
REGISTER = ROOT / "docs/rfc/rfc-register.md"
ANALYSIS = ROOT / "docs/analysis/2026-10-31-industry-practice-check.md"
CHANGELOG = ROOT / "CHANGELOG.md"
ISSUE = "https://github.com/G-Ivan-A/mango_ba_prompts/issues/417"

DECISIONS = [f"DEC-415-{n:02d}" for n in range(1, 13)]
NEW_DECISIONS = DECISIONS[8:]
RECOMMENDATIONS = [f"REC-417-{n:02d}" for n in range(1, 7)]
SECTION_STATUS = {
    "1. Видение": "принято предварительно",
    "2. Концепция": "принято предварительно",
    "3. Архитектура": "принято с исправлениями #417",
    "4. Дорожная карта": "принято с исправлениями #417",
}
ACCEPTANCE = "## Статус принятия (#417)"


def card(roadmap, prefix):
    heading = re.search(rf"^### {re.escape(prefix)}.*$", roadmap, re.M)
    assert heading, f"нет карточки «{prefix}»"
    return section(roadmap, heading.group(0))


class RfcAcceptanceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.md = text(RFC)
        cls.fm = frontmatter(cls.md)
        cls.roadmap = section(cls.md, "## 4. Дорожная карта")
        cls.acceptance = section(cls.md, ACCEPTANCE)
        cls.register = text(REGISTER)
        cls.analysis = text(ANALYSIS)

    # --- задача 1: исправления и статус принятия -------------------------

    def test_rfc_accepted_v02(self):
        self.assertEqual(self.fm.get("status"), "accepted")
        self.assertEqual(self.fm.get("version"), "0.2")
        self.assertIn(ISSUE, self.fm.get("related_issues", ""))

    def test_acceptance_section_status_per_section(self):
        rows = table_rows(self.acceptance, "| Раздел | Статус | Что это значит |")
        statuses = {re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", row[0]): row[1] for row in rows}
        self.assertEqual(statuses, SECTION_STATUS)
        self.assertIn("`accepted` (версия 0.2)", self.acceptance)

    def test_stage_2_opencode_chosen(self):
        stage2 = card(self.roadmap, "Этап 2.")
        self.assertIn("OpenCode (решение владельца, #417)", stage2)
        dec07 = next(line for line in self.md.splitlines() if 'id="dec-415-07"' in line)
        self.assertIn("`accepted`: вариант Б", dec07)

    def test_stage_3_n8n_testbed_on_dedicated_server(self):
        stage3 = card(self.roadmap, "Этап 3.")
        self.assertRegex(self.roadmap, r"(?m)^### Этап 3\. .*n8n", "заголовок этапа 3 без n8n")
        for needle in ("выделенном сервере", "испытательный стенд машинной оркестрации",
                       "отлаживаются контракты", "golden set"):
            self.assertIn(needle, stage3)

    def test_stage_4_code_runner_without_n8n(self):
        stage4 = card(self.roadmap, "Этап 4.")
        for needle in ("без n8n", "Python", "исполнителем процессов (runner)",
                       "детерминированное выполнение", "agentic coding",
                       "команда разработки", "в начале этапа 4"):
            self.assertIn(needle, stage4)
        summary = table_rows(self.roadmap, "| Этап | Что | Зачем | Как | Сколько (гипотеза) | Статус |")
        self.assertIn("Промышленное решение", summary[3][1])

    def test_showcase_and_portal(self):
        rows = [line for line in self.md.splitlines() if line.startswith("| Витрина |")]
        self.assertTrue(rows, "нет строки «Витрина» в таблице контейнеров")
        self.assertIn("GitHub Pages", rows[0])
        self.assertIn("портал", rows[0])
        self.assertIn("решение о портале", card(self.roadmap, "Этап 3."))

    def test_revision_rule(self):
        rule = section(self.acceptance, "### Правило пересмотра")
        for needle in ("эксплуатации при переходе на", "по требованию владельца"):
            self.assertIn(needle, rule)

    def test_prompt_count_as_is(self):
        summary = section(self.md, "## Кратко для руководителя")
        self.assertIn("14 промптов", summary)
        self.assertIn("as-is", summary)

    def test_new_decisions_anchored_accepted_and_registered(self):
        own = anchors(RFC)
        for dec in DECISIONS:
            with self.subTest(decision=dec):
                anchor = dec.lower()
                self.assertIn(anchor, own)
                row = next(line for line in self.md.splitlines() if f'id="{anchor}"' in line)
                self.assertIn("`accepted`", row)
                reg = next(line for line in self.register.splitlines()
                           if line.startswith(f"| [RFC-415-DEC-{dec[-2:]}]"))
                self.assertIn(f"(2026-10-ba-automation-strategy.md#{anchor})", reg)
                self.assertIn("`accepted`", reg)

    # --- задача 2: контрольная проверка ---------------------------------

    def test_analysis_frontmatter_valid(self):
        fm = frontmatter(self.analysis)
        self.assertIn("issues/417", fm.get("source", ""))
        self.assertEqual(fm.get("analysis-subtype"), "recommendation")
        proc = subprocess.run(["./tools/validate-frontmatter.sh", str(ANALYSIS)], cwd=ROOT,
                              capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_verdict_no_critical_deviations(self):
        bluf = section(self.analysis, "## Summary / BLUF")
        self.assertIn("Критичных отклонений нет", bluf)
        self.assertIn("Статус согласования RFC подтверждён", bluf)
        self.assertIn("критичных отклонений нет", self.acceptance)
        matrix = table_rows(self.analysis, "| № | Решение проекта | Индустриальная практика | Источник | Вердикт |")
        self.assertGreaterEqual(len(matrix), 10)
        for row in matrix:
            with self.subTest(row=row[0]):
                self.assertRegex(row[3], r"https://", "у практики нет источника")
                self.assertNotIn("отклоняется", row[4])

    def test_recommendations_proposed_not_applied(self):
        for rec in RECOMMENDATIONS:
            with self.subTest(recommendation=rec):
                self.assertIn(f'<a id="{rec.lower()}"></a>{rec}', self.analysis)
                self.assertIn(f"| {rec} |", self.acceptance)
                reg = next(line for line in self.register.splitlines() if line.startswith(f"| [{rec}]"))
                self.assertIn("`proposed`", reg)
                # Рекомендация не внесена в тело RFC: упоминается только в разделе
                # «Статус принятия» и в сводных разделах о самом RFC.
                body = section(self.md, "## Proposal")
                self.assertNotIn(rec, body)
        self.assertRegex(self.acceptance, r"не\s+внесены")

    def test_links_resolve(self):
        for path, md in ((ANALYSIS, self.analysis), (REGISTER, self.register)):
            missing = []
            for target in LINK.findall(md):
                if target.startswith(("http://", "https://")):
                    continue
                file_part, _, frag = target.partition("#")
                resolved = (path.parent / file_part).resolve() if file_part else path
                if not resolved.exists():
                    missing.append(target)
                elif frag and resolved.suffix == ".md" and frag not in anchors(resolved):
                    missing.append(target)
            with self.subTest(file=path.name):
                self.assertEqual(missing, [])

    # --- границы ---------------------------------------------------------

    def test_register_metadata(self):
        head = self.register.split("\n---\n", 1)[0]
        self.assertIn(f'"{ISSUE}"', head)
        self.assertIn('"docs/analysis/2026-10-31-industry-practice-check.md"', head)
        self.assertIn("issue #417", self.register.split("## Журнал изменений реестра", 1)[1])

    def test_canonical_documents_untouched(self):
        for target in SECTIONS.values():
            self.assertEqual(frontmatter(text(ROOT / target)).get("version"), "1.0", target)

    def test_changelog(self):
        unreleased = text(CHANGELOG).split("\n## ", 2)[1]
        self.assertIn("Issue #417", unreleased)
        self.assertIn("Issue #415", unreleased)


if __name__ == "__main__":
    unittest.main(verbosity=1 if "-q" in sys.argv else 2, argv=[sys.argv[0]])
