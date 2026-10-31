#!/usr/bin/env python3
"""Regression check for issue #413: a prompt holds patterns, classes and principles.

The owner decided in #413 that the questions, values and decisions of a single
task do not belong in a prompt. They go to the process golden set or the task
journal. The standard is `standards/prompt-standard.md`, section
«Обобщение содержимого промпта (issue #413)», rules G1–G5.

Rule G3 can be checked mechanically. The body of an active prompt must not
contain identifiers of a particular task or run:

- question IDs (`Q-2.1`);
- task IDs (`BCREQ-123`);
- run IDs (`RUN-0075`);
- scenario IDs (`SC-65`);
- issue references (`#391`, `.../issues/391`).

Rule G5 makes this a ratchet. Prompt bodies are not edited by the project
track (#413). Existing violations are listed in `ALLOWLIST` with exact counts
and are handed to the prompt track (#411). A count may only go down: a higher
count fails as a new violation, a lower count fails until the allowlist is
lowered too, so the allowlist cannot keep stale slack.
"""

from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROMPTS = ROOT / "prompts"
STANDARD = ROOT / "standards" / "prompt-standard.md"

# Active prompts follow `[domain]-[operation]-[mode].md` (ADR-006). README and
# `*.executable.md` files in prompts/ are indexes, not prompts.
PROMPT_NAME = re.compile(r"^[a-z0-9-]+-(stepwise|oneshot|legacy)\.md$")

PATTERNS: dict[str, re.Pattern[str]] = {
    "question-id": re.compile(r"\bQ-\d+(?:\.\d+)+\b"),
    "task-id": re.compile(r"\bBCREQ-\d+\b"),
    "run-id": re.compile(r"\bRUN-\d{3,}\b"),
    "scenario-id": re.compile(r"\bSC-\d+\b"),
    "issue-ref": re.compile(r"(?<![\w&/#])#\d{2,}\b|/issues/\d+"),
}

# Violations that existed when the rule was introduced (2026-10-31). Fixing
# them is a prompt-content change, tracked in #411.
ALLOWLIST: dict[str, dict[str, int]] = {
    "bcreq-constitution-governance-oneshot.md": {
        "run-id": 6,
        "scenario-id": 1,
        "issue-ref": 1,
    },
}

STANDARD_ANCHOR = "обобщение-содержимого-промпта-issue-413"
STANDARD_HEADING = "## Обобщение содержимого промпта (issue #413)"
STANDARD_RULES = ("**G1.**", "**G2.**", "**G3.**", "**G4.**", "**G5.**")

# Documents that cite the rule by anchor.
ANCHOR_CONSUMERS = ("docs/concept.md", "docs/architecture.md")


def body(text: str) -> str:
    """Return the prompt text without the YAML frontmatter."""
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            return text[end + 5 :]
    return text


def count_identifiers(text: str) -> dict[str, int]:
    return {
        kind: len(pattern.findall(text))
        for kind, pattern in PATTERNS.items()
        if pattern.findall(text)
    }


def active_prompts() -> list[Path]:
    return sorted(p for p in PROMPTS.glob("*.md") if PROMPT_NAME.match(p.name))


def check_prompts() -> list[str]:
    errors: list[str] = []
    seen: set[str] = set()
    for path in active_prompts():
        seen.add(path.name)
        found = count_identifiers(body(path.read_text(encoding="utf-8")))
        allowed = ALLOWLIST.get(path.name, {})
        for kind in sorted(set(found) | set(allowed)):
            have, limit = found.get(kind, 0), allowed.get(kind, 0)
            if have > limit:
                errors.append(
                    f"prompts/{path.name}: {kind} — {have} вхождений при "
                    f"допуске {limit}. Промпт содержит паттерны, классы и "
                    "принципы; кейс задачи переносится в golden set или журнал "
                    "задачи (standards/prompt-standard.md, G2–G3)"
                )
            elif have < limit:
                errors.append(
                    f"prompts/{path.name}: {kind} — {have} вхождений, а в "
                    f"ALLOWLIST {limit}. Уменьши ALLOWLIST (правило G5)"
                )
    for name in sorted(set(ALLOWLIST) - seen):
        errors.append(f"ALLOWLIST: prompts/{name} не найден — удали запись")
    return errors


def check_standard() -> list[str]:
    text = STANDARD.read_text(encoding="utf-8")
    errors = []
    if STANDARD_HEADING not in text:
        errors.append(f"{STANDARD.relative_to(ROOT)}: нет раздела {STANDARD_HEADING!r}")
    errors += [
        f"{STANDARD.relative_to(ROOT)}: нет правила {rule}"
        for rule in STANDARD_RULES
        if rule not in text
    ]
    if "validate_issue_413_prompt_generalization.py" not in text:
        errors.append(f"{STANDARD.relative_to(ROOT)}: нет ссылки на валидатор")
    return errors


def check_consumers() -> list[str]:
    needle = f"prompt-standard.md#{STANDARD_ANCHOR}"
    return [
        f"{path}: нет ссылки на правило обобщения ({needle})"
        for path in ANCHOR_CONSUMERS
        if needle not in (ROOT / path).read_text(encoding="utf-8")
    ]


def check_changelog() -> list[str]:
    text = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    return [] if "Issue #413" in text else ["CHANGELOG.md: нет записи об Issue #413"]


class DetectorTests(unittest.TestCase):
    def test_detects_each_identifier_class(self) -> None:
        sample = (
            "Вопрос Q-2.7 из BCREQ-1024, прогон RUN-0075, сценарий SC-65, "
            "см. #391 и https://github.com/o/r/issues/411"
        )
        self.assertEqual(
            count_identifiers(sample),
            {
                "question-id": 1,
                "task-id": 1,
                "run-id": 1,
                "scenario-id": 1,
                "issue-ref": 2,
            },
        )

    def test_ignores_principles_and_markdown(self) -> None:
        sample = (
            "#### Раздел\n### 4.4. Защиты АД-1…АД-7, шаг 8.4, CB-0.6, "
            "цвет &#123; и якорь [x](#4-stage), Q-шаблон, RUN-id"
        )
        self.assertEqual(count_identifiers(sample), {})

    def test_frontmatter_is_not_body(self) -> None:
        text = "---\nid: mango-x\nnote: RUN-0001\n---\nТекст без идентификаторов\n"
        self.assertEqual(count_identifiers(body(text)), {})

    def test_scope_is_active_prompts(self) -> None:
        names = {p.name for p in active_prompts()}
        self.assertIn("bcreq-constitution-governance-oneshot.md", names)
        self.assertNotIn("README.md", names)
        self.assertNotIn("README.executable.md", names)


def main() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(DetectorTests)
    if not unittest.TextTestRunner(verbosity=0).run(suite).wasSuccessful():
        return 1
    errors = check_prompts() + check_standard() + check_consumers() + check_changelog()
    if errors:
        print("Issue #413 prompt generalization validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    total = sum(sum(v.values()) for v in ALLOWLIST.values())
    print("Issue #413 prompt generalization validation passed.")
    print(f"- проверено промптов: {len(active_prompts())}")
    print(f"- известных нарушений в allowlist (трек #411): {total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
