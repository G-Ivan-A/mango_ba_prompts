#!/usr/bin/env python3
"""Регрессионная проверка анализа промптов, классов и стандартов (issue #425).

DoD #425 — один аналитический артефакт с успехами и проблемами как база для
RFC. Проверка фиксирует контракт постановки, а не качество текста:

* артефакт ``docs/analysis/2026-11-02-bcreq-prompts-classes-standards-check.md``
  проходит валидатор frontmatter Хаба, профиль ``recommendation``, без поля
  ``ai-generated``, ``based_on`` — дерево ``main`` на полном SHA;
* обязательные разделы стандарта анализа и разделы постановки по шаблону
  задачи (контекст, проблема, Story, ФТ, НФТ, цель, режим, специфика,
  обходы) на месте;
* ответы на три пункта задачи: вердикты У-1…У-4, Г-1, Г-2; применимость;
  терминология; варианты A–D; успехи; проблемы; рекомендации REC-425-NN;
* число классов в каталоге совпадает с числом файлов стандартов и с
  числами в артефакте; ``archetypes.json`` относит каждый класс ровно к
  одному архетипу;
* ``metrics.json`` актуален: пересчёт ``measure_classes.py`` в памяти даёт
  те же ключевые числа, что записаны в артефакте;
* относительные ссылки и якоря артефакта разрешаются;
* стандарты классов, промпты, сайт и прогоны этим PR не меняются.
"""

import importlib.util
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "docs/analysis/2026-11-02-bcreq-prompts-classes-standards-check.md"
CLASSES = ROOT / "standards/bcreq-manual-classes"
EXP = ROOT / "experiments/issue_425"
METRICS = EXP / "metrics.json"
ARCHETYPES = EXP / "archetypes.json"
BACKLOG = ROOT / "pr-ops/backlog-ba-model.md"

REQUIRED_SECTIONS = (
    "Summary / BLUF",
    "Context / Scope",
    "Постановка задачи",
    "Findings / Options",
    "Recommendations",
    "Ограничения",
    "Related Artifacts",
)
TASK_SECTIONS = (
    "Контекст задачи",
    "Решаемая проблема",
    "Story",
    "ФТ",
    "НФТ",
    "Цель",
    "Operating Mode",
    "Специфика работы с Конардом",
    "Обоснованные обходы",
)
FINDING_SECTIONS = (
    "1. Утверждения и гипотезы",
    "2. Есть ли промпты и можно ли их применять",
    "3. Терминология",
    "4. Индустриальная практика",
    "5. Успехи",
    "6. Проблемы",
)
VERDICT_ROWS = ("У-1", "У-2", "У-3", "У-4", "Г-1", "Г-2")
REFERENCES = (
    "issues/403",
    "issues/425",
    "pull/424",
    "BL-134",
    "DEC-411-07",
    "RUN-0078",
    "RUN-0079",
    "ADR-015",
    "metrics.json",
    "archetypes.json",
    "arXiv:2302.11382",
    "dspy.ai",
)
PROTECTED = ("standards/bcreq-manual-classes", "prompts", "site", "runs")
# Слияние PR #426 (issue #425) в main.
MERGE_425 = "1bd48293"
LINK_RE = re.compile(r"\]\(([^)\s]+)\)")


def run(*cmd):
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)


def frontmatter(text):
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        return {}
    data = {}
    for line in match.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip().strip('"')
    return data


def slug(heading):
    text = re.sub(r"[`*_]", "", heading.strip().lower())
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"\s", "-", text)


def anchors(path):
    found = set()
    for heading in re.findall(r"^#{1,6} (.+)$", path.read_text(encoding="utf-8"), re.M):
        base = slug(heading)
        candidate, n = base, 1
        while candidate in found:
            candidate, n = f"{base}-{n}", n + 1
        found.add(candidate)
    return found


def load_measure():
    spec = importlib.util.spec_from_file_location("measure_425", EXP / "measure_classes.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Issue425Check(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = ARTIFACT.read_text(encoding="utf-8")
        cls.fm = frontmatter(cls.text)
        cls.catalog = json.loads((CLASSES / "catalog.json").read_text(encoding="utf-8"))
        cls.metrics = json.loads(METRICS.read_text(encoding="utf-8"))

    def test_frontmatter(self):
        self.assertEqual(self.fm.get("status"), "draft")
        self.assertEqual(self.fm.get("analysis-subtype"), "recommendation")
        self.assertIn("issues/425", self.fm.get("source", ""))
        self.assertRegex(self.fm.get("based_on", ""), r"/tree/[0-9a-f]{40}$")
        self.assertNotIn("ai-generated", self.fm)
        proc = run("./tools/validate-frontmatter.sh", str(ARTIFACT))
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_sections(self):
        h2 = re.findall(r"^## (.+)$", self.text, re.M)
        self.assertEqual(h2[0], "Summary / BLUF")
        for name in REQUIRED_SECTIONS:
            self.assertIn(name, h2)
        h3 = re.findall(r"^### (.+)$", self.text, re.M)
        for name in TASK_SECTIONS + FINDING_SECTIONS:
            self.assertIn(name, h3)

    def test_verdicts_and_recommendations(self):
        for row in VERDICT_ROWS:
            self.assertIsNotNone(re.search(rf"^\| {row} \|", self.text, re.M), row)
        recs = re.findall(r"^\| (REC-425-\d\d) \|", self.text, re.M)
        self.assertGreaterEqual(len(recs), 5)
        self.assertEqual(len(recs), len(set(recs)))
        problems = re.findall(r"^\| (П-\d\d) \|", self.text, re.M)
        self.assertGreaterEqual(len(problems), 5)
        for option in ("A. Как есть", "B. Универсальный промпт", "C. Сигнатуры + архетипы", "D. Пилот"):
            self.assertIn(option, self.text)
        for ref in REFERENCES:
            self.assertIn(ref, self.text)

    def test_catalog_matches_files(self):
        files = sorted(p.name for p in CLASSES.glob("[0-9][0-9]-*.md"))
        ids = [c["id"] for c in self.catalog["classes"]]
        self.assertEqual(len(files), len(ids))
        self.assertEqual(sorted(c["file"] for c in self.catalog["classes"]), files)
        self.assertIn(f"| Операции (в репозитории — «классы») | {len(ids)} |", self.text)

    def test_archetypes_cover_catalog_once(self):
        data = json.loads(ARCHETYPES.read_text(encoding="utf-8"))
        assigned = [c for a in data["archetypes"].values() for c in a["classes"]]
        # archetypes.json — снимок #425 в нотации C01…C39; после BL-153
        # (issue #430) старый ID хранится в history.previous_id каталога.
        ids = [c.get("history", {}).get("previous_id", c["id"]) for c in self.catalog["classes"]]
        self.assertEqual(sorted(assigned), sorted(ids))
        for name, item in data["archetypes"].items():
            self.assertIn(f"{name} {len(item['classes'])}", self.text)

    def test_metrics_fresh_and_quoted(self):
        module = load_measure()
        # Замер читает файлы закреплённого среза (SNAPSHOT_REF) через git show.
        # В неглубоком клоне среза нет: это пропуск с явной причиной, а не
        # ошибка (CI берёт полную историю, issue #432).
        if run("git", "cat-file", "-e", f"{module.SNAPSHOT_REF}^{{commit}}").returncode != 0:
            self.skipTest(f"нет коммита среза замера #425 {module.SNAPSHOT_REF} (неглубокий клон)")
        catalog = module.load_catalog()
        inst = module.instances()
        fresh_b = module.boilerplate(catalog)
        fresh_p = module.paste_volume(catalog, inst)
        stored = self.metrics
        self.assertEqual(inst["total"], stored["instances"]["total"])
        self.assertEqual(inst["per_phase"], stored["instances"]["per_phase"])
        self.assertEqual(fresh_b["shared_share"], stored["boilerplate"]["shared_share"])
        self.assertEqual(
            fresh_p["manual_classes_without_release_chars"],
            stored["paste_volume"]["manual_classes_without_release_chars"],
        )

        def ru(n):
            return f"{n:,}".replace(",", " ")

        def pct(x):
            return f"{x * 100:.1f}".replace(".", ",") + "%"

        def ratio(x):
            return f"{x:.2f}".replace(".", ",")

        p = stored["paste_volume"]
        self.assertIn(f"| {inst['total']} |", self.text)
        self.assertIn(pct(stored["boilerplate"]["shared_share"]), self.text)
        self.assertIn(pct(stored["boilerplate"]["catalog_specific_share_avg"]), self.text)
        self.assertIn(ru(p["manual_classes_without_release_chars"]), self.text)
        self.assertIn(ru(p["manual_classes_without_release_lower_bound_chars"]), self.text)
        self.assertIn(ru(p["stepwise_route_chars"]), self.text)
        self.assertIn(ratio(p["ratio_lower_bound_to_stepwise"]), self.text)
        self.assertIn(ratio(p["ratio_classes_to_stepwise"]), self.text)
        self.assertEqual(stored["executable_prompt_files_for_classes"], 0)
        self.assertEqual(
            stored["old_prompts"]["prompts_without_class_successor"],
            ["bcreq-work-solution-design-oneshot.md"],
        )

    def test_links_resolve(self):
        for target in LINK_RE.findall(self.text):
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            path_part, _, anchor = target.partition("#")
            path = (ARTIFACT.parent / unquote(path_part)).resolve() if path_part else ARTIFACT
            with self.subTest(link=target):
                self.assertTrue(path.exists(), target)
                if anchor and path.suffix == ".md":
                    self.assertIn(unquote(anchor), anchors(path))

    def test_backlog_note(self):
        card = BACKLOG.read_text(encoding="utf-8").split("### BL-134.", 1)[1].split("\n### ", 1)[0]
        self.assertIn("Пометка #425", card)
        self.assertIn("2026-11-02-bcreq-prompts-classes-standards-check.md", card)

    def test_protected_unchanged(self):
        # Проверка относится к самому PR #426 (issue #425): его слияние сравнивается
        # с main до слияния. Последующие PR (BL-153, issue #430) меняют классы и
        # сайт законно, поэтому сравнение с текущим HEAD здесь неверно.
        if run("git", "cat-file", "-e", f"{MERGE_425}^1").returncode != 0:
            self.skipTest("нет git-истории слияния PR #426")
        proc = run("git", "diff", "--name-only", f"{MERGE_425}^1", MERGE_425, "--", *PROTECTED)
        self.assertEqual(proc.stdout.strip(), "", "PR #425 не меняет классы, промпты, сайт и прогоны")


if __name__ == "__main__":
    unittest.main(verbosity=1 if "-q" in sys.argv else 2, argv=[sys.argv[0]])
