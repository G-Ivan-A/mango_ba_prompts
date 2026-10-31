#!/usr/bin/env python3
"""Офлайн-приёмка аналитических артефактов issue #409 (аудит аудита репозитория).

Проверяет согласованность, а не содержание решений: решения DEC-01…DEC-10 —
предложение на согласование владельцу. Проверки:

* реестр диспозиции (JSON и Markdown) внутренне согласован, а его итоги
  совпадают с цифрами в аудите, реестре задач и RFC;
* идентификаторы F-xx, DEC-xx, T-xx, H-xx разрешаются в определения;
* относительные ссылки и якоря существуют, ссылки на другие репозитории
  закреплены на коммитах, ссылок на временные ветки форка нет;
* frontmatter проходит валидатор Хаба, поля ``ai-generated`` нет, жаргона из
  ``FORBIDDEN_TERMS`` валидатора #263 нет;
* RFC имеет статус ``proposed`` и зарегистрирован в ``docs/rfc/rfc-register.md``.

История git не читается: CI работает на shallow-клоне, поэтому реестр
сверяется сам с собой и с документами, а не с деревом базового коммита.
"""

import importlib.util
import json
import re
import subprocess
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

AUDIT = ROOT / "docs/audit/2026-10-31-repository-audit.md"
REGISTER = ROOT / "docs/analysis/2026-10-31-file-disposition-register.md"
TASKS = ROOT / "docs/analysis/2026-10-31-follow-up-tasks.md"
EVOLUTION = ROOT / "docs/analysis/2026-10-31-requirements-evolution.md"
STRATEGY = ROOT / "docs/analysis/2026-10-31-strategic-documents-proposal.md"
RFC = ROOT / "docs/rfc/2026-10-repository-modernization.md"
RFC_REGISTER = ROOT / "docs/rfc/rfc-register.md"
DISPOSITION = ROOT / "experiments/issue_409/disposition.json"
GENERATOR = ROOT / "experiments/issue_409/build_disposition.py"

#: Документы, созданные issue #409 (полностью в ответственности этой приёмки).
ARTIFACTS = (AUDIT, REGISTER, TASKS, EVOLUTION, STRATEGY, RFC)
#: Анализы #407, в которых этот PR заменил ссылки на ветку форка.
ANALYSES_407 = tuple(ROOT / "docs/analysis" / name for name in (
    "2026-10-30-repository-current-state.md",
    "2026-10-30-ecosystem-compliance.md",
    "2026-10-30-october-requirements-evolution.md",
))

BASELINE = "6f6cbc477f4b482d3c10bd4d941cbfb481fccf1f"
PINS = {
    "hybrid-Intelligence-lab": "32b5fa524e542af23c1a8e67c919bd66d5f4e399",
    "mango-ba-ai-runtime": "b67410f627801345309281faa15e7219722bfb1a",
    "mango_ba_prompts": BASELINE,
}
DISPOSITIONS = ("current", "update", "relocate", "historical",
                "archive-candidate", "archived", "generated", "statistics")
ACTIONABLE = {"update", "relocate", "archive-candidate"}
FINDINGS = [f"F-{i:02}" for i in range(1, 21)]
DECISIONS = [f"DEC-{i:02}" for i in range(1, 11)]
TASK_IDS = [f"T-{i:02}" for i in range(1, 10)]
APPEALS = [f"H-{i:02}" for i in range(1, 8)]
FORK = "github.com/konard/G-Ivan-A-mango_ba_prompts"
LINK = re.compile(r"\]\(([^\s)]+)\)")


def text(path):
    return path.read_text(encoding="utf-8")


def body(path):
    """Текст без frontmatter."""
    content = text(path)
    if content.startswith("---\n"):
        return content.split("\n---\n", 1)[1]
    return content


def frontmatter(path):
    block = text(path).split("\n---\n", 1)[0]
    fields = {}
    for line in block.splitlines()[1:]:
        match = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if match:
            fields[match.group(1)] = match.group(2).strip().strip('"')
    return fields


def slug(heading):
    """Якорь заголовка в стиле GitHub."""
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


def table_rows(markdown, header):
    """Строки Markdown-таблицы, идущей после строки, начинающейся с header."""
    lines = markdown.split(header, 1)[1].splitlines()[2:]
    rows = []
    for line in lines:
        if not line.startswith("|"):
            break
        rows.append([cell.strip() for cell in line.strip().strip("|").split("|")])
    return rows


def load():
    return json.loads(text(DISPOSITION))


class Disposition(unittest.TestCase):
    def setUp(self):
        self.data = load()
        self.entries = self.data["entries"]

    def test_header_and_counts_are_consistent(self):
        data = self.data
        self.assertEqual(data["baseline_sha"], BASELINE)
        self.assertEqual(data["generator"], GENERATOR.relative_to(ROOT).as_posix())
        self.assertTrue(GENERATOR.exists())
        self.assertEqual(data["file_count"], 1615)
        self.assertEqual(len(self.entries), data["file_count"])
        paths = [e["path"] for e in self.entries]
        self.assertEqual(len(paths), len(set(paths)))
        self.assertEqual(paths, sorted(paths))
        self.assertEqual(tuple(data["dispositions"]), DISPOSITIONS)
        self.assertEqual(dict(Counter(e["disposition"] for e in self.entries)), data["counts"])
        self.assertEqual(sum(data["counts"].values()), data["file_count"])

    def test_runs_are_frozen_statistics(self):
        for entry in self.entries:
            with self.subTest(path=entry["path"]):
                in_runs = entry["path"].startswith("runs/")
                self.assertEqual(entry["disposition"] == "statistics", in_runs)
                if in_runs:
                    self.assertEqual(entry["task"], "")

    def test_every_actionable_file_has_exactly_one_known_task(self):
        self.assertEqual(sorted(self.data["tasks"]), TASK_IDS)
        for entry in self.entries:
            with self.subTest(path=entry["path"]):
                if entry["disposition"] in ACTIONABLE:
                    self.assertIn(entry["task"], TASK_IDS)
                else:
                    self.assertEqual(entry["task"], "")
        actionable = sum(self.data["counts"][d] for d in ACTIONABLE)
        self.assertEqual(actionable, 155)

    def test_archive_never_receives_statistics_or_kb(self):
        for entry in self.entries:
            if entry["path"].startswith(("runs/", "kb/")):
                self.assertNotEqual(entry["disposition"], "archived", entry["path"])

    def test_ai_generated_list_matches_entries(self):
        flagged = sorted(e["path"] for e in self.entries if e["ai_generated"])
        self.assertEqual(sorted(self.data["ai_generated_files"]), flagged)
        self.assertEqual(len(flagged), 741)
        self.assertEqual(sum(not p.startswith("runs/") for p in flagged), 113)


class Register(unittest.TestCase):
    """Markdown-реестр — производная JSON; расхождение значит ручную правку."""

    def setUp(self):
        self.data = load()
        self.markdown = text(REGISTER)

    def test_area_summary_matches_json(self):
        rows = table_rows(self.markdown, "| Область |")
        expected = Counter((e["area"], e["disposition"]) for e in self.data["entries"])
        areas = {e["area"] for e in self.data["entries"]}
        self.assertEqual(len(rows), len(areas))
        for row in rows:
            area = row[0].strip("`")
            with self.subTest(area=area):
                values = [int(cell) for cell in row[1:]]
                self.assertEqual(values[:-1], [expected[(area, d)] for d in DISPOSITIONS])
                self.assertEqual(values[-1], sum(values[:-1]))

    def test_task_summary_matches_json_and_follow_up_register(self):
        per_task = Counter(e["task"] for e in self.data["entries"] if e["task"])
        rows = table_rows(self.markdown, "| Задача | Содержание |")
        self.assertEqual([row[0] for row in rows], TASK_IDS)
        for task_id, title, count in rows:
            self.assertEqual(int(count), per_task[task_id], task_id)
            self.assertEqual(title, self.data["tasks"][task_id])
        follow_up = table_rows(text(TASKS), "| Задача | Зависит от решений |")
        self.assertEqual([row[0] for row in follow_up], TASK_IDS)
        for row in follow_up:
            self.assertEqual(int(row[3].split()[0]), per_task[row[0]], row[0])
        self.assertIn("— 155:", text(TASKS))

    def test_per_file_table_matches_json(self):
        rows = table_rows(self.markdown, "| Путь | status |")
        expected = {e["path"]: e for e in self.data["entries"] if not e["path"].startswith("runs/")}
        self.assertEqual(len(rows), len(expected))
        for row in rows:
            path = row[0].strip("`")
            entry = expected[path]
            self.assertEqual(row[3].strip("`"), entry["disposition"], path)
            self.assertEqual(row[5], entry["task"] or "—", path)

    def test_documents_quote_the_same_totals(self):
        counts = self.data["counts"]
        summary = re.sub(r"\s+", " ", text(AUDIT))
        self.assertIn(f"Каждый из {self.data['file_count']} файлов", summary)
        for phrase in (f"{counts['current']} актуальны", f"{counts['update']} требуют актуализации",
                       f"{counts['relocate']} — переноса", f"{counts['historical']} — исторические",
                       f"{counts['archive-candidate']} — кандидаты в архив",
                       f"{counts['archived']} уже в архиве", f"{counts['generated']} сгенерированы",
                       f"{counts['statistics']} — замороженная"):
            self.assertIn(phrase, summary)
        rfc = re.sub(r"\s+", " ", text(RFC))
        for disposition, count in counts.items():
            self.assertIn(f"`{disposition}` {count}", rfc)


class Identifiers(unittest.TestCase):
    def test_findings_are_contiguous_and_assigned(self):
        rows = table_rows(text(AUDIT), "| ID | S | Находка")
        self.assertEqual([row[0] for row in rows], FINDINGS)
        for path in (RFC, TASKS):
            self.assertIn(f"{FINDINGS[0]}…{FINDINGS[-1]}", text(path), path.name)
        for row in rows:
            self.assertRegex(row[1], r"^S[1-4]$", row[0])
            self.assertRegex(row[-1], r"(DEC|T|H)-\d{2}", row[0])

    def test_decisions_tasks_and_appeals_are_defined(self):
        rfc, tasks = text(RFC), text(TASKS)
        defined = {
            "F": set(FINDINGS),
            "DEC": set(re.findall(r"^#### (DEC-\d{2})\.", rfc, re.M)),
            "T": set(re.findall(r"^### (T-\d{2})\.", tasks, re.M)),
            "H": set(re.findall(r"^### (H-\d{2})\.", tasks, re.M)),
        }
        self.assertEqual(defined["DEC"], set(DECISIONS))
        self.assertEqual(defined["T"], set(TASK_IDS))
        self.assertEqual(defined["H"], set(APPEALS))
        for path in ARTIFACTS:
            content = body(path)
            for kind, ids in defined.items():
                cited = set(re.findall(rf"\b{kind}-\d{{2}}\b", content))
                with self.subTest(path=path.name, kind=kind):
                    self.assertLessEqual(cited, ids)
            # Диапазон «X-01…X-NN» не выходит за определения и не устарел:
            # полный диапазон всегда заканчивается последним определённым ID.
            for kind, ids in defined.items():
                for start, end in re.findall(rf"\b{kind}-(\d{{2}})…{kind}-(\d{{2}})\b", content):
                    with self.subTest(path=path.name, range=f"{kind}-{start}…{end}"):
                        self.assertLess(int(start), int(end))
                        self.assertIn(f"{kind}-{end}", ids)
                        if start == "01" and kind != "F":
                            self.assertEqual(f"{kind}-{end}", max(ids))

    def test_rfc_is_proposed_and_registered(self):
        fields = frontmatter(RFC)
        self.assertEqual(fields["status"], "proposed")
        self.assertEqual(fields["version"], "0.4")
        register = text(RFC_REGISTER)
        rows = re.findall(r"^\| \[RFC-409-(DEC-\d{2})\]\(", register, re.M)
        self.assertEqual(rows, DECISIONS)
        rfc_anchors = anchors(RFC)
        for target in re.findall(r"\]\(2026-10-repository-modernization\.md#([^)]+)\)", register):
            self.assertIn(target, rfc_anchors)


class Links(unittest.TestCase):
    def test_relative_links_and_anchors_resolve(self):
        for path in (*ARTIFACTS, *ANALYSES_407, RFC_REGISTER):
            for target in LINK.findall(body(path)):
                if "://" in target or target.startswith("mailto:"):
                    continue
                file_part, _, anchor = target.partition("#")
                resolved = (path.parent / file_part).resolve() if file_part else path
                with self.subTest(path=path.name, target=target):
                    self.assertTrue(resolved.exists())
                    if anchor and resolved.suffix == ".md":
                        self.assertIn(anchor, anchors(resolved))

    def test_ecosystem_links_are_pinned(self):
        for path in ARTIFACTS:
            for repo, ref in re.findall(
                    r"github\.com/G-Ivan-A/([\w.-]+)/(?:blob|tree)/([^/)\s\"]+)", text(path)):
                with self.subTest(path=path.name, repo=repo):
                    self.assertEqual(ref, PINS[repo])

    def test_no_fork_branch_links(self):
        for path in (*ARTIFACTS, *ANALYSES_407):
            content = text(path)
            # Аудит цитирует шаблон поиска, но не ссылается на форк.
            links = [t for t in LINK.findall(content) if FORK in t]
            self.assertEqual(links, [], path.name)
            if path not in (AUDIT, TASKS):
                self.assertNotIn(FORK, content, path.name)


class Hygiene(unittest.TestCase):
    def test_frontmatter_passes_hub_validator(self):
        paths = [p.relative_to(ROOT).as_posix() for p in (*ARTIFACTS, *ANALYSES_407)]
        proc = subprocess.run(["./tools/validate-frontmatter.sh", *paths], cwd=ROOT,
                              capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_forbidden_fields_and_terms(self):
        # Словарь жаргона — тот же, что валидатор #263 запрещает в концептуальных
        # документах. RFC и предложение по стратегическим документам станут их
        # источником, поэтому проверяются по всему списку; анализ эволюции
        # цитирует сам запрет, поэтому остальным артефактам запрещено только
        # «Фаундер». Анализы #407 — датированные свидетельства, их термины
        # не переписываются.
        spec = importlib.util.spec_from_file_location(
            "vision263", ROOT / "scripts/validate_issue_263_vision_alignment.py")
        vision263 = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(vision263)
        for path in (*ARTIFACTS, *ANALYSES_407):
            with self.subTest(path=path.name):
                self.assertNotIn("ai-generated", frontmatter(path))
                if path in (RFC, STRATEGY):
                    for term in vision263.FORBIDDEN_TERMS:
                        self.assertNotIn(term, text(path))
                elif path in ARTIFACTS:
                    self.assertNotIn("аундер", text(path))
                self.assertEqual(frontmatter(path)["updated"][:7], "2026-10")

    def test_analysis_frontmatter_is_hub_class(self):
        for path in (REGISTER, TASKS, EVOLUTION, STRATEGY):
            fields = frontmatter(path)
            with self.subTest(path=path.name):
                self.assertEqual(fields["source"], "https://github.com/G-Ivan-A/mango_ba_prompts/issues/409")
                self.assertIn("analysis-subtype", fields)


if __name__ == "__main__":
    unittest.main(verbosity=2)
