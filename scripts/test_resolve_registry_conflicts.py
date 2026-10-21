#!/usr/bin/env python3
"""Регрессионные тесты `scripts/resolve_registry_conflicts.py` (issue #377).

Сценарий из комментария к PR #380: два PR открыты одновременно, первый смержен,
второй получает конфликт в `CHANGELOG.md` и `runs/README.md`. Тесты проверяют,
что append-only конфликты разрешаются без потери сторон, а настоящие конфликты
(правка одной строки, коллизия номера прогона) не разрешаются молча.
Интеграционные тесты строят временный git-репозиторий.

Запуск: ``python3 scripts/test_resolve_registry_conflicts.py``
"""

from __future__ import annotations

import io
import contextlib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import resolve_registry_conflicts as rrc  # noqa: E402

M = "<" * 7  # маркер не пишется литералом: его ищет validate_issue_377_merge_hygiene

FRONT = "---\nstatus: draft\nversion: {v}\nupdated: {d}\n---\n\n"


def row(n: int, text: str = "x") -> str:
    return f"| [`RUN-{n:04d}`](2026/RUN-{n:04d}/metadata.yaml) | 2026-10-20 | `statistics` | {text} |"


def registry(rows: list[str], v: str = "1.2", d: str = "2026-10-19", tools: list[str] | None = None) -> str:
    text = FRONT.format(v=v, d=d) + "## Реестр записей\n\n| Run | Дата |\n|---|---|\n"
    text += "".join(r + "\n" for r in rows)
    text += "\n## Локальные инструменты\n\n| Скрипт | Назначение |\n|---|---|\n"
    text += "".join(t + "\n" for t in (tools or []))
    return text


def tool(runs: list[int]) -> str:
    links = [f"[`RUN-{n:04d}`](2026/RUN-{n:04d}/inputs/README.md)" for n in runs]
    used = links[0] if len(links) == 1 else ", ".join(links[:-1]) + " и " + links[-1]
    return f"| [`scripts/conv.py`](../scripts/conv.py) | Конвертер. Используется в {used}. |"


class ResolveTextTest(unittest.TestCase):
    def test_run_rows_from_both_sides_sorted(self) -> None:
        base = registry([row(1)])
        ours = registry([row(1), row(3, "наш")])
        theirs = registry([row(1), row(2, "main")], v="1.3", d="2026-10-20")
        merged = rrc.resolve_text("runs/README.md", ours, base, theirs)
        self.assertNotIn(M, merged)
        self.assertLess(merged.index("RUN-0002"), merged.index("RUN-0003"))
        self.assertIn("version: 1.3", merged)
        self.assertIn("updated: 2026-10-20", merged)

    def test_run_id_collision_is_not_merged(self) -> None:
        base = registry([row(1)])
        with self.assertRaisesRegex(rrc.UnresolvableConflict, "коллизия номера прогона RUN-0002"):
            rrc.resolve_text(
                "runs/README.md", registry([row(1), row(2, "наш")]), base, registry([row(1), row(2, "main")])
            )

    def test_tool_row_run_links_are_united(self) -> None:
        base = registry([row(1)], tools=[tool([1])])
        ours = registry([row(1), row(3)], tools=[tool([1, 3])])
        theirs = registry([row(1), row(2)], tools=[tool([1, 2])])
        merged = rrc.resolve_text("runs/README.md", ours, base, theirs)
        self.assertIn(tool([1, 2, 3]), merged)
        self.assertEqual(merged.count("scripts/conv.py`]"), 1)

    def test_same_line_edited_differently_is_refused(self) -> None:
        base = "# Changelog\n\n## Unreleased\n\nline\n"
        with self.assertRaises(rrc.UnresolvableConflict):
            rrc.resolve_text("CHANGELOG.md", base.replace("line", "ours"), base, base.replace("line", "theirs"))

    def test_changelog_own_entry_on_top(self) -> None:
        base = FRONT.format(v="0.1", d="2026-10-19") + "## Unreleased\n\n### Old\n\n- old\n"
        ours = base.replace("### Old", "### Ours\n\n- ours\n\n### Old")
        theirs = base.replace("### Old", "### Main\n\n- main\n\n### Old")
        merged = rrc.resolve_text("CHANGELOG.md", ours, base, theirs)
        self.assertIn("### Ours\n\n- ours\n\n### Main\n\n- main\n\n### Old", merged)

    def test_files_outside_registries_are_refused(self) -> None:
        with self.assertRaises(rrc.UnresolvableConflict):
            rrc.resolve_text("README.md", "a\n", "", "b\n")


def sh(cwd: Path, *args: str) -> str:
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True, check=False).stdout


class GitIntegrationTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        self.old_root = rrc.ROOT
        rrc.ROOT = self.repo
        sh(self.repo, "git", "init", "-q", "-b", "main")
        sh(self.repo, "git", "config", "user.email", "t@example.com")
        sh(self.repo, "git", "config", "user.name", "t")
        self.write("runs/README.md", registry([row(1)], tools=[tool([1])]))
        self.write("CHANGELOG.md", "## Unreleased\n\n### Old\n")
        self.write("runs/2026/RUN-0001/metadata.yaml", "run_id: RUN-0001\n")
        self.commit("init")

    def tearDown(self) -> None:
        rrc.ROOT = self.old_root
        self.tmp.cleanup()

    def write(self, rel: str, text: str) -> None:
        path = self.repo / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def commit(self, msg: str) -> None:
        sh(self.repo, "git", "add", "-A")
        sh(self.repo, "git", "commit", "-q", "-m", msg)

    def add_run(self, n: int, who: str) -> None:
        self.write("runs/README.md", registry([row(1), row(n, who)], tools=[tool([1, n])]))
        self.write("CHANGELOG.md", f"## Unreleased\n\n### {who} RUN-{n:04d}\n\n### Old\n")
        self.write(f"runs/2026/RUN-{n:04d}/metadata.yaml", f"run_id: RUN-{n:04d}\nwho: {who}\n")
        self.commit(f"{who}: RUN-{n:04d}")

    def quiet(self, fn, *args):
        with contextlib.redirect_stdout(io.StringIO()) as out:
            code = fn(*args)
        return code, out.getvalue()

    def test_parallel_pr_conflict_resolved_automatically(self) -> None:
        sh(self.repo, "git", "checkout", "-q", "-b", "pr")
        self.add_run(3, "pr")
        sh(self.repo, "git", "checkout", "-q", "main")
        self.add_run(2, "main")
        sh(self.repo, "git", "checkout", "-q", "pr")
        sh(self.repo, "git", "merge", "-q", "main")
        self.assertIn(M, (self.repo / "runs/README.md").read_text(encoding="utf-8"))
        code, out = self.quiet(rrc.resolve_in_progress_merge)
        self.assertEqual(code, 0, out)
        text = (self.repo / "runs/README.md").read_text(encoding="utf-8")
        self.assertNotIn(M, text)
        self.assertIn(tool([1, 2, 3]), text)
        self.assertLess(text.index("RUN-0002"), text.index("RUN-0003"))
        self.assertEqual(sh(self.repo, "git", "diff", "--name-only", "--diff-filter=U"), "")

    def test_run_number_collision_then_renumber(self) -> None:
        sh(self.repo, "git", "checkout", "-q", "-b", "pr")
        self.add_run(2, "pr")
        sh(self.repo, "git", "checkout", "-q", "main")
        self.add_run(2, "main")
        sh(self.repo, "git", "checkout", "-q", "pr")
        sh(self.repo, "git", "merge", "-q", "main")
        code, out = self.quiet(rrc.resolve_in_progress_merge)
        self.assertEqual(code, 1)
        self.assertIn("--renumber RUN-0002", out)
        sh(self.repo, "git", "merge", "--abort")
        code, _ = self.quiet(rrc.renumber, "RUN-0002", "RUN-0003", "main")
        self.assertEqual(code, 0)
        self.commit("renumber")
        meta = (self.repo / "runs/2026/RUN-0003/metadata.yaml").read_text(encoding="utf-8")
        self.assertIn("run_id: RUN-0003", meta)
        self.assertFalse((self.repo / "runs/2026/RUN-0002").exists())
        sh(self.repo, "git", "merge", "-q", "main")
        code, out = self.quiet(rrc.resolve_in_progress_merge)
        self.assertEqual(code, 0, out)
        text = (self.repo / "runs/README.md").read_text(encoding="utf-8")
        self.assertIn(row(2, "main"), text)
        self.assertIn(row(3, "pr"), text)
        changelog = (self.repo / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertIn("### pr RUN-0003", changelog)
        self.assertIn("### main RUN-0002", changelog)
        self.assertIn("who: main", (self.repo / "runs/2026/RUN-0002/metadata.yaml").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
