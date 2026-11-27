#!/usr/bin/env python3
"""Runtime issue #27: BL-192 «Производство универсального агентного контекста runtime».

Производство — в G-Ivan-A/mango-ba-ai-runtime (PR runtime #29), движение
бэклога — в спице. Проверяет без LLM и без сети:

* движение по цепочке: BL-191 ``DONE`` (PR runtime #26 и PR #494 слиты,
  решение владельца по Р-RT-2…Р-RT-4 и Р-RT-6), BL-192 ``DONE`` со ссылками
  на runtime #27 и PR runtime #29 — в таблице, в карточках и в блоке
  «Движение по цепочке (runtime #27)»;
* соседние задачи не сдвинуты без основания: BL-132 ``deferred (triggered)``,
  BL-185 ``TODO``; RFC-RT-002 остаётся ``proposed`` (решения в разделе 9
  записывает владелец);
* тексты промптов не менялись: коммиты задачи (``runtime-27`` в сообщении)
  не трогают ``prompts/``;
* при ``RUNTIME_RT27_CLONE=<клон runtime с PR #29>`` — результат в runtime:
  зеркало ``.agents/skills/<имя>/SKILL.md`` побайтно равно ``skills/<имя>.md``
  и ничего больше в ``.agents`` нет, ``AGENTS.md`` знает ``ACCESS_GAP`` и
  маршрут ``MAP.json`` → ``sections_toc``, есть smoke OpenCode.
"""
import hashlib
import os
import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKLOG = ROOT / "pr-ops/BACKLOG.md"
MODEL = ROOT / "pr-ops/backlog-ba-model.md"
RFC = ROOT / "docs/rfc/2026-11-runtime-universal-agent-context.md"

RT = "https://github.com/G-Ivan-A/mango-ba-ai-runtime"
ISSUE = f"{RT}/issues/27"
PR = f"{RT}/pull/29"
OWNER_DECISION = f"{RT}/pull/26#issuecomment-7020333876"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def card(model: str, bl: str) -> str:
    return model.split(f"### {bl}.", 1)[1].split("\n### ", 1)[0]


def row(backlog: str, bl: str) -> str:
    match = re.search(rf"(?m)^\| {bl} \|.*$", backlog)
    return match.group(0) if match else ""


class ChainTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.backlog = read(BACKLOG)
        cls.model = read(MODEL)

    def test_bl191_done(self):
        self.assertRegex(row(self.backlog, "BL-191"), r"\| BL-184 \| DONE \|")
        text = card(self.model, "BL-191")
        self.assertIn("**Статус.** `DONE`", text)
        for evidence in (f"{RT}/pull/26", "pull/494", "16c11e55", "e051e0fa", OWNER_DECISION):
            self.assertIn(evidence, text)

    def test_bl192_done(self):
        line = row(self.backlog, "BL-192")
        self.assertRegex(line, r"\| DONE \|")
        self.assertIn(ISSUE, line)
        self.assertIn(PR, line)
        text = card(self.model, "BL-192")
        self.assertIn("**Статус.** `DONE`", text)
        for evidence in (ISSUE, PR, ".agents/skills/<имя>/SKILL.md", "ACCESS_GAP", "tests/opencode_smoke.py",
                         "Ранее — `deferred (triggered)` → `review`", "bee5f9ba", OWNER_DECISION):
            self.assertIn(evidence, text)

    def test_chain_block(self):
        block = self.backlog.split("**Движение по цепочке (runtime #27).**", 1)
        self.assertEqual(len(block), 2, "нет блока движения по цепочке runtime #27")
        text = block[1].split("\n\n", 1)[0]
        for step in ("BL-191 `review` → `DONE`", "BL-192 `deferred (triggered)` →\n`review` → `DONE`", "bee5f9ba", "Р-RT-7",
                     "BL-185…BL-188", "BL-132", OWNER_DECISION, ISSUE, PR):
            self.assertIn(step, text)

    def test_neighbours_unchanged(self):
        self.assertRegex(row(self.backlog, "BL-132"), r"\| deferred \(triggered\) \|")
        self.assertRegex(row(self.backlog, "BL-185"), r"\| TODO \|")
        self.assertRegex(read(RFC), r"(?m)^status: proposed$")


class PromptsUnchangedTest(unittest.TestCase):
    def test_issue_commits_do_not_touch_prompts(self):
        res = subprocess.run(
            ["git", "log", "--no-merges", "--format=%h %s", "--grep=runtime-27", "--", "prompts/"],
            cwd=ROOT, capture_output=True, text=True,
        )
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertEqual(res.stdout.strip(), "", "коммиты runtime #27 меняют тексты промптов")


@unittest.skipUnless(os.environ.get("RUNTIME_RT27_CLONE"), "нет RUNTIME_RT27_CLONE")
class RuntimeResultTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.clone = Path(os.environ["RUNTIME_RT27_CLONE"])

    def test_mirror(self):
        skills = sorted((self.clone / "skills").glob("*.md"))
        self.assertEqual(len(skills), 11)
        want = {f".agents/skills/{s.stem}/SKILL.md" for s in skills}
        have = {p.relative_to(self.clone).as_posix() for p in (self.clone / ".agents").rglob("*") if not p.is_dir()}
        self.assertEqual(have, want)
        for src in skills:
            mirror = self.clone / ".agents/skills" / src.stem / "SKILL.md"
            self.assertFalse(mirror.is_symlink(), mirror)
            self.assertEqual(hashlib.sha256(mirror.read_bytes()).hexdigest(),
                             hashlib.sha256(src.read_bytes()).hexdigest(), src.name)

    def test_agents_md(self):
        text = read(self.clone / "AGENTS.md")
        for marker in ("ACCESS_GAP: <что> — <почему>", "unverified", "docs/kb/MAP.json", "sections_toc",
                       "retrieval_if_insufficient", ".agents/skills/<имя>/SKILL.md"):
            self.assertIn(marker, text)
        self.assertLessEqual(len(text.encode()), 32 * 1024)

    def test_smoke_present(self):
        for path in ("tests/build_skills_mirror.py", "tests/test_skills_mirror.py", "tests/opencode_smoke.py"):
            self.assertTrue((self.clone / path).is_file(), path)


if __name__ == "__main__":
    unittest.main(verbosity=1)
