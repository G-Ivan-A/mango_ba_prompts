#!/usr/bin/env python3
"""Регрессионная проверка решения владельца Р-13 по RFC потока BCREQ (issue #427).

После слияния PR #428 владелец ответил «Р-13 да» (комментарий
https://github.com/G-Ivan-A/mango_ba_prompts/pull/428#issuecomment-6579261813).
«Да» — рекомендация Р-13 из реестра решений бэклога: принять RFC и решения
DEC-427-01…13, RFC → ``accepted``. Решения DEC-427-07 и 08 вынесены в Р-14,
DEC-427-04 и 12 — в Р-15; без ответа по ним они остаются ``proposed``.
Проверка фиксирует:

* RFC: ``status: accepted``, версия 0.3, раздел «Статус принятия (Р-13)»
  со ссылкой на комментарий владельца и статусом каждого из 13 решений;
* реестр RFC: строки RFC-427-DEC с теми же статусами, у принятых — ссылка
  на комментарий; запись в истории изменений;
* бэклог: Р-13 — «принято» со ссылкой; Р-14 и Р-15 — «ждёт»; карточки
  задач, которые открывает Р-13, отмечают решение;
* CHANGELOG описывает принятие в ``Unreleased``.
"""

import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RFC = ROOT / "docs/rfc/2026-11-bcreq-flow-processes-prompts.md"
REGISTER = ROOT / "docs/rfc/rfc-register.md"
BACKLOG = ROOT / "pr-ops/BACKLOG.md"
TRACK_B = ROOT / "pr-ops/backlog-ba-model.md"
CHANGELOG = ROOT / "CHANGELOG.md"

COMMENT = "https://github.com/G-Ivan-A/mango_ba_prompts/pull/428#issuecomment-6579261813"
PENDING = {"04": "Р-15", "07": "Р-14", "08": "Р-14", "12": "Р-15"}
DECISIONS = [f"{n:02d}" for n in range(1, 14)]
ACCEPTED = [n for n in DECISIONS if n not in PENDING]
OPENED_TASKS = ("BL-125", "BL-150", "BL-151", "BL-152", "BL-153", "BL-154", "BL-155")
HEADING = "## Статус принятия (Р-13)"


def text(path):
    return path.read_text(encoding="utf-8")


def frontmatter(body):
    match = re.match(r"^---\n(.*?)\n---\n", body, re.S)
    assert match, "нет frontmatter"
    return dict(
        (k.strip(), v.strip().strip('"'))
        for k, v in (line.split(":", 1) for line in match.group(1).splitlines() if ":" in line and not line.startswith(" "))
    )


def section(body, heading):
    start = body.index(heading + "\n") + len(heading) + 1
    level = len(heading) - len(heading.lstrip("#"))
    stop = re.search(rf"^#{{1,{level}}} ", body[start:], re.M)
    return body[start:start + stop.start()] if stop else body[start:]


def card(body, task):
    return body.split(f"### {task}. ", 1)[1].split("\n### ", 1)[0]


class RfcAccepted(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.body = text(RFC)
        cls.fm = frontmatter(cls.body)

    def test_frontmatter(self):
        self.assertEqual(self.fm.get("status"), "accepted")
        # Редакция 0.3 — принятие Р-13; поправки после приёмки (0.4 — #430,
        # тип гейта) статус не меняют.
        self.assertIn(self.fm.get("version"), ("0.3", "0.4"))

    def test_acceptance_section(self):
        block = section(self.body, HEADING)
        self.assertIn(COMMENT, block)
        self.assertIn("`accepted` (редакция 0.3)", block)
        rows = dict(re.findall(r"^\| DEC-427-(\d\d)\. [^|]+\| `(\w+)` \|", block, re.M))
        self.assertEqual(sorted(rows), DECISIONS)
        for n in DECISIONS:
            with self.subTest(dec=n):
                self.assertEqual(rows[n], "proposed" if n in PENDING else "accepted")
        for n, decision in PENDING.items():
            self.assertRegex(block, rf"(?m)^\| DEC-427-{n}\. .*\| ждёт {decision} \|$")

    def test_summary_points_to_acceptance(self):
        bluf = section(self.body, "## Summary / BLUF")
        self.assertIn("#статус-принятия-р-13", bluf)
        decisions = section(self.body, "## 11. Решения на согласование")
        self.assertIn("#статус-принятия-р-13", decisions)


class RegisterAccepted(unittest.TestCase):
    def test_rows(self):
        body = text(REGISTER)
        for n in DECISIONS:
            with self.subTest(dec=n):
                row = re.search(rf"^\| \[RFC-427-DEC-{n}\].*$", body, re.M)
                self.assertIsNotNone(row)
                cells = [c.strip() for c in row.group(0).strip("|").split(" | ")]
                status = cells[-2]
                if n in PENDING:
                    self.assertEqual(status, "`proposed`")
                else:
                    self.assertEqual(status, f"`accepted` ([Р-13]({COMMENT}))")

    def test_history(self):
        body = text(REGISTER)
        # 0.11 — запись о приёмке RFC #427; поздние версии реестра её сохраняют.
        self.assertGreaterEqual(tuple(map(int, frontmatter(body).get("version").split("."))), (0, 11))
        history = body.split("RFC #427 → `accepted` (v0.3)", 1)
        self.assertEqual(len(history), 2, "нет записи о принятии RFC #427")


class BacklogAccepted(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.backlog = text(BACKLOG)
        cls.track_b = text(TRACK_B)

    def decision_status(self, decision):
        row = re.search(rf"^\| \*\*{decision}\*\* \|.*$", self.backlog, re.M)
        self.assertIsNotNone(row, decision)
        return row.group(0).rstrip(" |").rsplit(" | ", 1)[1]

    def test_r13_accepted(self):
        self.assertEqual(self.decision_status("Р-13"), f"принято ([PR #428]({COMMENT}))")

    def test_r14_r15_pending(self):
        for decision in ("Р-14", "Р-15"):
            with self.subTest(decision=decision):
                self.assertEqual(self.decision_status(decision), "ждёт")

    def test_cards_mark_decision(self):
        for task in OPENED_TASKS:
            with self.subTest(task=task):
                self.assertIn(f"**Решение владельца.** Р-13 — принято ([PR #428]({COMMENT}))", card(self.track_b, task))

    def test_changelog(self):
        unreleased = text(CHANGELOG).split("## Unreleased", 1)[1].split("\n## ", 1)[0]
        self.assertIn("### Changed — Issue #427: решение владельца Р-13", unreleased)
        self.assertIn(COMMENT, unreleased)


if __name__ == "__main__":
    unittest.main(verbosity=1 if "-q" in sys.argv else 2, argv=[sys.argv[0]])
