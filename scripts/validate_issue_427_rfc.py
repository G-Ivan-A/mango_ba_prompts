#!/usr/bin/env python3
"""Регрессионная проверка RFC потока BCREQ и Спринта 9 (issue #427).

DoD #427 — RFC на изменения и спринт в бэклоге. Проверка фиксирует контракт
постановки, а не качество текста:

* RFC ``docs/rfc/2026-11-bcreq-flow-processes-prompts.md`` проходит
  валидатор frontmatter Хаба, статус ``proposed`` (ждёт рассмотрения владельцем), без поля
  ``ai-generated``, ``source`` — issue #427;
* разделы RFC на месте: постановка по шаблону задачи, термин «Поток»,
  мета-модель, процессы, промпт/контракт/стандарт, стандарты, исключения
  runtime, промпты, раздел «Процессы», решения DEC-427-01…13, план, риски,
  альтернативы, самовопросы, «что не сделано»;
* редакция 0.2 по ревью владельца PR #428: цепочка «Поток → Процесс →
  Операция → Артефакт» из четырёх элементов; шаг, гейт и стадия — не
  уровни цепочки; отклонённая иерархия «поток → этап с гейтом → процесс →
  шаг → операция» упоминается только как отклонённая; точное определение
  операции; уровни таксономии операций — техдолг S-010 → BL-125;
* девять процессов ПБ-0…ПБ-7 и ПБ-С; последовательность 12 шагов этапа 1
  и шаг Ш-С вне последовательности; каждый промпт шага существует в
  ``prompts/``; состав — 11 файлов промптов;
* исключения И-1…И-10 и требования ТС-1…ТС-7; блок заглушки; ссылки на
  mango-ba-ai-runtime закреплены полным SHA;
* Спринт 9 в ``pr-ops/BACKLOG.md``: задачи BL-150…BL-158, BL-230, BL-231 с
  карточками, ссылающимися на RFC; решения Р-13…Р-15; долг S-009 → BL-158;
  задача BL-125 в Спринте 6 и долг S-010 → BL-125;
* реестр RFC содержит RFC-427-DEC-01…13 со ссылками на существующие якоря;
* CHANGELOG описывает #427 в ``Unreleased``;
* относительные ссылки и якоря RFC разрешаются;
* промпты, стандарты, процесс BCREQ, сайт и прогоны этим PR не меняются —
  их правка идёт задачами Спринта 9.
"""

import re
import subprocess
import sys
import unittest
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
RFC = ROOT / "docs/rfc/2026-11-bcreq-flow-processes-prompts.md"
REGISTER = ROOT / "docs/rfc/rfc-register.md"
BACKLOG = ROOT / "pr-ops/BACKLOG.md"
TRACK_B = ROOT / "pr-ops/backlog-ba-model.md"
TRACK_A = ROOT / "pr-ops/backlog-repository.md"
CHANGELOG = ROOT / "CHANGELOG.md"
ARTIFACT_MAP = ROOT / "pr-ops/artifact-map.md"
PROMPTS = ROOT / "prompts"

H2 = (
    "Summary / BLUF",
    "Навигация и обязательные результаты",
    "1. Постановка задачи",
    "2. SSOT и источники",
    "3. Термин «Поток»: сверка с практикой",
    "4. Цепочка «Поток — Процесс — Операция — Артефакт» и совместимость с мета-моделью БА",
    "5. Процессы потока BCREQ",
    "6. Промпт, контракт, стандарт",
    "7. Полный набор стандартов",
    "8. Исключения: ссылки промптов на mango-ba-ai-runtime",
    "9. Полный набор промптов по процессам",
    "10. Раздел «Процессы» сайта",
    "11. Решения на согласование",
    "12. План реализации",
    "13. Риски",
    "14. Альтернативы",
    "15. Самовопросы",
    "16. Что не сделано в этом PR и почему",
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
    "Специфика работы",
    "Обоснованные обходы",
)
PROCESSES = tuple(f"ПБ-{n}" for n in range(8)) + ("ПБ-С",)
STEPS = ("Ш-0", "Ш-1", "Ш-2", "Ш-3", "Ш-4", "Ш-5", "Ш-6", "Ш-7", "Ш-8", "Ш-9", "Ш-В", "Ш-Р")
EXCEPTIONS = tuple(f"И-{n}" for n in range(1, 11))
REQUIREMENTS = tuple(f"ТС-{n}" for n in range(1, 8))
TRACK_B_TASKS = tuple(f"BL-{n}" for n in range(150, 159))
TRACK_A_TASKS = ("BL-230", "BL-231")
DECISIONS = ("Р-13", "Р-14", "Р-15")
SPRINT = "### Спринт 9: Поток BCREQ: стандарты и промпты по тесту"
SPRINT_ANCHOR = "спринт-9-поток-bcreq-стандарты-и-промпты-по-тесту"
H2_CHAIN = "## 4. Цепочка «Поток — Процесс — Операция — Артефакт» и совместимость с мета-моделью БА"
PROTECTED = ("prompts", "standards", "docs/ba-processes", "site", "runs")
LINK_RE = re.compile(r"\]\(([^)\s]+)\)")
RUNTIME_RE = re.compile(r"https://github\.com/G-Ivan-A/mango-ba-ai-runtime/(?:tree|blob)/([^/)\s>]+)")


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


def section(text, heading):
    """Текст от заголовка до следующего заголовка того же или верхнего уровня."""
    level = len(heading) - len(heading.lstrip("#"))
    start = text.index(heading + "\n")
    rest = text[start + len(heading) + 1:]
    stop = re.search(rf"^#{{1,{level}}} ", rest, re.M)
    return rest[: stop.start()] if stop else rest


def rows(text, first_cell):
    return re.findall(rf"^\| ({first_cell}) \|(.*)$", text, re.M)


class Issue427Rfc(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = RFC.read_text(encoding="utf-8")
        cls.fm = frontmatter(cls.text)

    def test_frontmatter(self):
        self.assertEqual(self.fm.get("status"), "proposed")
        self.assertEqual(self.fm.get("type"), "rfc")
        self.assertEqual(self.fm.get("owner"), "G-Ivan-A")
        self.assertIn("issues/427", self.fm.get("source", ""))
        self.assertNotIn("ai-generated", self.fm)
        proc = run("./tools/validate-frontmatter.sh", str(RFC))
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_sections_in_order(self):
        h2 = re.findall(r"^## (.+)$", self.text, re.M)
        self.assertEqual(h2, list(H2))
        task = section(self.text, "## 1. Постановка задачи")
        h3 = re.findall(r"^### (.+)$", task, re.M)
        self.assertEqual(h3, list(TASK_SECTIONS))

    def test_decisions(self):
        block = section(self.text, "## 11. Решения на согласование")
        found = re.findall(r"^### (DEC-427-\d\d)\. ", block, re.M)
        self.assertEqual(found, [f"DEC-427-{n:02d}" for n in range(1, 14)])

    def test_flow_term_verdict(self):
        block = section(self.text, "## 3. Термин «Поток»: сверка с практикой")
        for source in ("ГОСТ Р 56020-2020", "SAFe", "Business Architecture Guild", "APQC"):
            self.assertIn(source, block)
        self.assertIn("### 3.2. Вердикт исполнителя", block)

    def test_chain_of_elements(self):
        """Ревью владельца PR #428: цепочка из четырёх элементов, а не иерархия из пяти уровней."""
        block = section(self.text, H2_CHAIN)
        table = section(block, "### 4.1. Четыре элемента")
        self.assertEqual(
            [cell.strip() for cell in re.findall(r"^\| [1-4] \| ([^|]+)\|", table, re.M)],
            ["Поток", "Процесс (подпроцесс)", "Операция", "Артефакт"],
        )
        not_levels = section(block, "### 4.2. Шаг, гейт и стадия — не уровни")
        for term in ("Шаг", "Гейт", "Стадия"):
            self.assertRegex(not_levels, rf"(?m)^\| {term} ", term)
        self.assertIn("**Поток → Процесс (подпроцессы) → Операция → Артефакт**", self.text)
        for paragraph in re.split(r"\n\s*\n", self.text):
            if re.search(r"этап\S*\s+(?:\(стадия\)\s+)?с\s+гейтом\s+→\s+процесс", paragraph):
                self.assertRegex(paragraph, r"отклонен", "отклонённая иерархия без пометки")

    def test_operation_definition(self):
        block = section(self.text, "### 4.3. Операция: точное определение")
        self.assertIn("**Операция** — атомарное действие процесса", block)
        for row in ("Тип операции (класс, контракт)", "Экземпляр операции", "Исполнение"):
            self.assertRegex(block, rf"(?m)^\| {re.escape(row)} \|", row)
        taxonomy = section(self.text, "### 4.4. Уровни таксономии операций: техдолг S-010")
        for marker in ("ingestion", "C02", "normalize-text", "SK-transcript-normalization", "BL-125"):
            self.assertIn(marker, taxonomy)

    def test_processes(self):
        block = section(self.text, "### 5.3. Процессы")
        self.assertEqual([r[0] for r in rows(block, r"ПБ-[0-9С]")], list(PROCESSES))

    def test_step_sequence(self):
        block = section(self.text, "### 5.4. Последовательность шагов этапа 1")
        numbered = re.findall(r"^\| (\d+) \| (Ш-[0-9ВР]) ", block, re.M)
        self.assertEqual([int(n) for n, _ in numbered], list(range(1, 13)))
        self.assertEqual([s for _, s in numbered], list(STEPS))
        self.assertRegex(block, r"(?m)^\| — \| Ш-С ", "Ш-С вне последовательности")
        header = block.split("\n| --- ", 1)[0]
        for column in ("Зачем шаг", "Варианты дальше"):
            self.assertIn(column, header)

    def test_prompt_set_exists(self):
        block = section(self.text, "### 9.2. Состав")
        table = [r for r in rows(block, r"Ш-[0-9ВРС]")]
        names = {m for _, cells in table for m in re.findall(r"`(bcreq-[a-z-]+)`", cells.split("|")[1])}
        self.assertEqual(len(names), 11, sorted(names))
        for name in names:
            with self.subTest(prompt=name):
                self.assertTrue((PROMPTS / f"{name}.md").exists(), name)
        self.assertEqual([r[0] for r in table], list(STEPS) + ["Ш-С"])

    def test_standards_set(self):
        block = section(self.text, "### 7.1. Состав")
        self.assertIn("1 базовый + 8 профилей", block)
        for archetype in ("INGEST", "EXTRACT", "ANALYZE", "ELICIT", "GENERATE", "VERIFY", "TRANSFORM", "RECORD"):
            self.assertIn(archetype, block)

    def test_runtime_exceptions(self):
        listed = [r[0] for r in rows(section(self.text, "### 8.2. Перечень"), r"И-\d+")]
        self.assertEqual(listed, list(EXCEPTIONS))
        reqs = [r[0] for r in rows(section(self.text, "### 8.3. Требования к справочникам"), r"ТС-\d")]
        self.assertEqual(reqs, list(REQUIREMENTS))
        self.assertIn("[СПРАВОЧНИК ОТСУТСТВУЕТ: <имя>; задача BL-155]", section(self.text, "### 8.4. Заглушка"))

    def test_runtime_links_pinned(self):
        refs = RUNTIME_RE.findall(self.text)
        self.assertTrue(refs)
        for ref in refs:
            with self.subTest(ref=ref):
                self.assertTrue(re.fullmatch(r"[0-9a-f]{40}", ref) or ref.startswith("<SHA"), ref)

    def test_not_done_mapped_to_sprint(self):
        block = section(self.text, "## 16. Что не сделано в этом PR и почему")
        for task in ("BL-151", "BL-155", "BL-156", "BL-158", "BL-230", "BL-231", "BL-125"):
            self.assertIn(task, block)

    def test_links_resolve(self):
        for target in LINK_RE.findall(self.text):
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            path_part, _, anchor = target.partition("#")
            path = (RFC.parent / unquote(path_part)).resolve() if path_part else RFC
            with self.subTest(link=target):
                self.assertTrue(path.exists(), target)
                if anchor and path.suffix == ".md":
                    self.assertIn(unquote(anchor), anchors(path))

    def test_protected_unchanged(self):
        base = None
        for ref in ("upstream/main", "origin/main", "main"):
            proc = run("git", "merge-base", "HEAD", ref)
            if proc.returncode == 0:
                base = proc.stdout.strip()
                break
        if not base:
            self.skipTest("нет git-истории main")
        proc = run("git", "log", "--format=%H", f"{base}..HEAD", "--grep", "(issue-427)")
        own = proc.stdout.split()
        for sha in own:
            changed = run("git", "diff-tree", "--no-commit-id", "--name-only", "-r", sha, "--", *PROTECTED)
            self.assertEqual(changed.stdout.strip(), "", f"{sha}: #427 — только RFC и бэклог")


class Issue427Backlog(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.backlog = BACKLOG.read_text(encoding="utf-8")
        cls.track_b = TRACK_B.read_text(encoding="utf-8")
        cls.track_a = TRACK_A.read_text(encoding="utf-8")

    def test_sprint_rows(self):
        block = section(self.backlog, SPRINT)
        ids = re.findall(r"^\| (BL-\d{3}) \|", block, re.M)
        self.assertEqual(ids, list(TRACK_B_TASKS + TRACK_A_TASKS))
        self.assertIn(SPRINT_ANCHOR, anchors(BACKLOG))
        self.assertIn(f"#{SPRINT_ANCHOR}", RFC.read_text(encoding="utf-8"))

    def test_cards_cite_rfc(self):
        for tasks, text in ((TRACK_B_TASKS, self.track_b), (TRACK_A_TASKS, self.track_a)):
            for task in tasks:
                with self.subTest(task=task):
                    card = text.split(f"### {task}. ", 1)[1].split("\n### ", 1)[0]
                    self.assertIn("2026-11-bcreq-flow-processes-prompts.md", card)
                    self.assertIn("**Решение владельца.** Р-1", card)

    def test_decisions_declared(self):
        block = section(self.backlog, "## 2. Решения владельца")
        for decision in DECISIONS:
            self.assertRegex(block, rf"(?m)^\| \*\*{decision}\*\* \|", decision)
        self.assertIn("«Р-01…Р-15 да»", block)

    def test_tech_debt(self):
        block = section(self.backlog, "## 6. Технический долг соответствия стандартам Хаба (issue #267)")
        self.assertRegex(block, r"(?m)^\| S-009 \| .*RFC #427", "строка долга")
        self.assertRegex(block, r"(?m)^\| S-009 \| BL-158 \|", "связь с задачей")
        self.assertRegex(block, r"(?m)^\| S-010 \| .*RFC #427", "строка долга S-010")
        self.assertRegex(block, r"(?m)^\| S-010 \| BL-125 \|", "связь S-010 с задачей")

    def test_taxonomy_debt_task(self):
        block = section(self.backlog, "### Спринт 6: Ревизия мета-модели после этапа 1")
        self.assertRegex(block, r"(?m)^\| BL-125 \| .*S-010", "строка BL-125 в Спринте 6")
        card = self.track_b.split("### BL-125. ", 1)[1].split("\n### ", 1)[0]
        self.assertIn("2026-11-bcreq-flow-processes-prompts.md", card)
        self.assertIn("**Решение владельца.** Р-1", card)


class Issue427Registers(unittest.TestCase):
    def test_rfc_register(self):
        text = REGISTER.read_text(encoding="utf-8")
        found = re.findall(r"^\| \[RFC-427-DEC-(\d\d)\]\(2026-11-bcreq-flow-processes-prompts\.md#([^)]+)\)", text, re.M)
        self.assertEqual([n for n, _ in found], [f"{n:02d}" for n in range(1, 14)])
        rfc_anchors = anchors(RFC)
        for _, anchor in found:
            self.assertIn(anchor, rfc_anchors)

    def test_changelog_and_map(self):
        unreleased = CHANGELOG.read_text(encoding="utf-8").split("## Unreleased", 1)[1].split("\n## ", 1)[0]
        self.assertIn("### Added — Issue #427", unreleased)
        self.assertIn("`/docs/rfc/2026-11-bcreq-flow-processes-prompts.md`", ARTIFACT_MAP.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main(verbosity=1 if "-q" in sys.argv else 2, argv=[sys.argv[0]])
