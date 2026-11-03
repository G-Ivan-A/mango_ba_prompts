#!/usr/bin/env python3
"""Регрессионная проверка реестра справочников runtime (issue #430, BL-154, BL-155).

Реестр ``standards/bcreq-runtime-references.md`` — носитель раздела 8 RFC #427
(DEC-427-09, DEC-427-10) до базового стандарта BL-151 (поправка 0.4 RFC).
Проверка фиксирует контракт реестра:

* закреплённый срез: 40-символьный SHA во frontmatter (``runtime_sha``) и в
  таблице раздела 1 совпадают — одна точка обновления (ТС-5);
* перечень И-1…И-10 и требования ТС-1…ТС-7 в порядке, как в разделе 8 RFC;
* ссылки на mango-ba-ai-runtime в реестре, словаре потока, процессе BCREQ,
  контрактах и промптах — только по закреплённому SHA (ТС-1, ТС-5);
* известный долг ТС-1 — ссылки ``blob/main`` в текущих ``prompts/`` — не
  растёт: каждая такая ссылка есть в замороженном списке раздела 7;
* блок заглушки совпадает с разделом 8.4 RFC; заглушки З-1…З-4 и задачи для
  runtime РТ-1…РТ-4 связаны; строка ТС-6 для промпта есть;
* карточки BL-114, BL-154, BL-155 ссылаются на реестр; реестр есть в
  ``standards/README.md`` и ``pr-ops/artifact-map.md``;
* относительные ссылки и якоря реестра разрешаются;
* при ``RUNTIME_CLONE=<путь к клону runtime на SHA>`` — пути «Да»/«Частично»
  существуют (ТС-2); без клона проверка пропускается (CI без сети).
"""

import os
import re
import subprocess
import sys
import unittest
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "standards/bcreq-runtime-references.md"
RFC = ROOT / "docs/rfc/2026-11-bcreq-flow-processes-prompts.md"
TRACK_B = ROOT / "pr-ops/backlog-ba-model.md"
STANDARDS_README = ROOT / "standards/README.md"
ARTIFACT_MAP = ROOT / "pr-ops/artifact-map.md"
GLOSSARY = ROOT / "standards/bcreq-flow-glossary.md"

RUNTIME_LINK = re.compile(
    r"(?:github\.com/G-Ivan-A/mango-ba-ai-runtime/(?:blob|tree|raw)/"
    r"|raw\.githubusercontent\.com/G-Ivan-A/mango-ba-ai-runtime/)"
    # Шаблон «<SHA>» в тексте требования ТС-1 — не ссылка.
    r"([^/\s)`\"<]+)(/[^\s)`\"]*)?"
)
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
# Где действует ТС-5: набор промптов потока и его нормативные документы.
# Прогоны, анализы и kb/ фиксируют срез на свою дату и сюда не входят.
SCOPE = ("prompts", "standards", "docs/ba-processes", "docs/contracts")
# Долг ТС-1 на 2026-11-02 (раздел 7 реестра): 14 промптов × 3 ссылки на main.
MAIN_DEBT_URLS = {
    "/docs/kb/README.md",
    "/docs/kb/MAP.json",
    "/taxonomy/products.yaml",
}
MAIN_DEBT_FILES = {
    f"prompts/bcreq-{name}.md"
    for name in (
        "constitution-governance-oneshot",
        "constraints-documentation-stepwise",
        "context-understanding-stepwise",
        "core-documentation-oneshot",
        "extra-risk-analysis-stepwise",
        "fr-documentation-stepwise",
        "in-understanding-oneshot",
        "nfr-documentation-stepwise",
        "orr-solution-design-stepwise",
        "products-impact-analysis-stepwise",
        "review-validation-oneshot",
        "scenarios-modeling-oneshot",
        "uc-modeling-stepwise",
        "work-solution-design-oneshot",
    )
}
STUB_HEAD = "[СПРАВОЧНИК ОТСУТСТВУЕТ: <имя>; задача BL-155]"
LINK_RE = re.compile(r"\]\(([^)\s]+)\)")


def text(path):
    return path.read_text(encoding="utf-8")


def frontmatter(body):
    match = re.match(r"^---\n(.*?)\n---\n", body, re.S)
    data = {}
    for line in (match.group(1) if match else "").splitlines():
        if ":" in line and not line.startswith(" "):
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip().strip('"')
    return data


def slug(heading):
    value = re.sub(r"[`*_]", "", heading.strip().lower())
    value = re.sub(r"[^\w\s-]", "", value)
    return re.sub(r"\s", "-", value)


def anchors(path):
    found = set()
    for heading in re.findall(r"^#{1,6} (.+)$", text(path), re.M):
        base, n = slug(heading), 1
        candidate = base
        while candidate in found:
            candidate, n = f"{base}-{n}", n + 1
        found.add(candidate)
    return found


def section(body, heading):
    level = len(heading) - len(heading.lstrip("#"))
    rest = body[body.index(heading + "\n") + len(heading) + 1:]
    stop = re.search(rf"^#{{1,{level}}} ", rest, re.M)
    return rest[: stop.start()] if stop else rest


def code_block(body):
    return re.search(r"```text\n(.*?)\n```", body, re.S).group(1)


def table_ids(block, prefix):
    return re.findall(rf"^\| ({prefix}-\d+) \|", block, re.M)


class Registry(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.body = text(REGISTRY)
        cls.fm = frontmatter(cls.body)
        cls.sha = cls.fm.get("runtime_sha", "")

    def test_frontmatter(self):
        self.assertEqual(self.fm.get("type"), "standard")
        self.assertRegex(self.sha, SHA_RE)
        self.assertEqual(
            self.fm.get("runtime_repo"), "https://github.com/G-Ivan-A/mango-ba-ai-runtime"
        )

    def test_single_sha_point(self):
        block = section(self.body, "## 1. Закреплённый срез")
        self.assertIn(f"| SHA | `{self.sha}` |", block)
        self.assertIn("единственная точка обновления SHA", block)

    def test_inventory_matches_rfc(self):
        rfc_ids = table_ids(section(text(RFC), "### 8.2. Перечень"), "И")
        ids = table_ids(section(self.body, "## 2. Перечень"), "И")
        self.assertEqual(ids, [f"И-{n}" for n in range(1, 11)])
        self.assertEqual(ids, rfc_ids)

    def test_requirements_match_rfc(self):
        rfc_ids = table_ids(section(text(RFC), "### 8.3. Требования к справочникам"), "ТС")
        ids = table_ids(section(self.body, "## 3. Требования к справочникам"), "ТС")
        self.assertEqual(ids, [f"ТС-{n}" for n in range(1, 8)])
        self.assertEqual(ids, rfc_ids)

    def test_registry_links_pinned(self):
        links = RUNTIME_LINK.findall(self.body)
        self.assertGreaterEqual(len(links), 7)
        for ref, _ in links:
            with self.subTest(ref=ref):
                self.assertEqual(ref, self.sha)

    def test_stub_block_matches_rfc(self):
        stubs = section(self.body, "## 4. Заглушки")
        rfc_block = code_block(section(text(RFC), "### 8.4. Заглушка"))
        self.assertEqual(code_block(stubs), rfc_block)
        self.assertTrue(rfc_block.startswith(STUB_HEAD))
        self.assertEqual(table_ids(stubs, "З"), ["З-1", "З-2", "З-3", "З-4"])
        tasks = table_ids(section(self.body, "## 6. Задачи для репозитория runtime"), "РТ")
        self.assertEqual(tasks, ["РТ-1", "РТ-2", "РТ-3", "РТ-4"])
        for row in re.findall(r"^\| З-\d .*$", stubs, re.M):
            with self.subTest(row=row[:12]):
                self.assertRegex(row, r"\| РТ-\d \|$")

    def test_stub_per_missing_reference(self):
        inventory = section(self.body, "## 2. Перечень")
        stubs = section(self.body, "## 4. Заглушки")
        for row in re.findall(r"^\| (И-\d+) \|.*[Зз]аглушка (З-\d)", inventory, re.M):
            ref, stub = row
            with self.subTest(ref=ref):
                self.assertRegex(stubs, rf"(?m)^\| {stub} \| {ref} ")

    def test_prompt_line_ts6(self):
        block = section(self.body, "## 5. Строка для промпта (ТС-6)")
        self.assertIn("попроси БА приложить файл", code_block(block))
        self.assertIn("<SHA из раздела 1>", code_block(block))

    def test_links_resolve(self):
        for target in LINK_RE.findall(self.body):
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            path_part, _, anchor = target.partition("#")
            path = (REGISTRY.parent / unquote(path_part)).resolve() if path_part else REGISTRY
            with self.subTest(link=target):
                self.assertTrue(path.exists(), target)
                if anchor and path.suffix == ".md":
                    self.assertIn(unquote(anchor), anchors(path))

    def test_glossary_stub_anchor(self):
        self.assertIn("bcreq-runtime-references.md#4-заглушки", text(GLOSSARY))
        self.assertIn("4-заглушки", anchors(REGISTRY))

    @unittest.skipUnless(os.environ.get("RUNTIME_CLONE"), "нет RUNTIME_CLONE")
    def test_paths_exist_in_clone(self):
        clone = Path(os.environ["RUNTIME_CLONE"])
        head = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=clone, capture_output=True, text=True
        ).stdout.strip()
        self.assertEqual(head, self.sha, "клон не на закреплённом SHA")
        for _, path in RUNTIME_LINK.findall(self.body):
            with self.subTest(path=path):
                self.assertTrue((clone / path.lstrip("/")).exists(), path)


class PinnedLinks(unittest.TestCase):
    """ТС-1 и ТС-5 в наборе промптов и нормативных документах потока."""

    @classmethod
    def setUpClass(cls):
        cls.sha = frontmatter(text(REGISTRY))["runtime_sha"]
        cls.links = []
        for top in SCOPE:
            for path in sorted((ROOT / top).rglob("*")):
                if path.suffix not in {".md", ".json", ".yaml", ".yml"} or not path.is_file():
                    continue
                for ref, rest in RUNTIME_LINK.findall(text(path)):
                    cls.links.append((path.relative_to(ROOT).as_posix(), ref, rest))

    def test_one_sha(self):
        for rel, ref, rest in self.links:
            if ref == "main":
                continue
            with self.subTest(file=rel, ref=ref):
                self.assertRegex(ref, SHA_RE, "ТС-1: ссылка на runtime не по полному SHA")
                self.assertEqual(ref, self.sha, "ТС-5: SHA не из реестра справочников")

    def test_main_debt_not_growing(self):
        debt = {(rel, rest) for rel, ref, rest in self.links if ref == "main"}
        for rel, rest in sorted(debt):
            with self.subTest(file=rel, path=rest):
                self.assertIn(rel, MAIN_DEBT_FILES, "ТС-1: новая ссылка на main")
                self.assertIn(rest, MAIN_DEBT_URLS, "ТС-1: новая ссылка на main")


class Backlog(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.track_b = text(TRACK_B)

    def card(self, task):
        return self.track_b.split(f"### {task}. ", 1)[1].split("\n### ", 1)[0]

    def test_cards_link_registry(self):
        for task in ("BL-114", "BL-154", "BL-155"):
            with self.subTest(task=task):
                self.assertIn("standards/bcreq-runtime-references.md", self.card(task))

    def test_registry_registered(self):
        self.assertIn("bcreq-runtime-references.md", text(STANDARDS_README))
        self.assertIn("/standards/bcreq-runtime-references.md", text(ARTIFACT_MAP))


if __name__ == "__main__":
    result = unittest.main(exit=False, verbosity=2).result
    sys.exit(0 if result.wasSuccessful() else 1)
