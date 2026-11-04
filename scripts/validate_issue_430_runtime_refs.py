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
* блок заглушки совпадает с разделом 8.4 RFC; заглушки З-2…З-4 и задачи для
  runtime РТ-1…РТ-4, РТ-6 связаны; З-1 — в таблице снятых (BL-163, issue #442);
  строка ТС-6 для промпта есть;
* И-2 — «Да»: каталог ``taxonomy/mango-products.yaml`` по SHA раздела 1;
* карточки BL-114, BL-154, BL-155 ссылаются на реестр; реестр есть в
  ``standards/README.md`` и ``pr-ops/artifact-map.md``;
* относительные ссылки и якоря реестра разрешаются;
* при ``RUNTIME_CLONE=<путь к клону runtime на SHA>`` — пути «Да»/«Частично»
  существуют (ТС-2); каталог runtime сверен с каталогом спицы (раздел 2.1
  реестра): ``closed: true``, 353 узла, id, уровни и родители совпадают,
  ``source_sha256`` = sha256 каталога спицы на ``source_commit``, иное
  расхождение ``lifecycle``, кроме ``added-for-review`` → ``accepted``
  (Р-17, до РТ-6), — ошибка; без клона проверка пропускается (CI без сети).
"""

import hashlib
import json
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
CATALOG = ROOT / "docs/taxonomy/products.json"
RUNTIME_CATALOG = "taxonomy/mango-products.yaml"
# Уровни каталога спицы → уровни копии runtime.
LEVELS = {"Domain": "domain", "Capability": "capability", "Feature": "feature", "Atomic Function": "function"}
# Узел копии runtime: одна строка — один узел (РТ-1, НФТ).
RUNTIME_NODE = re.compile(
    r'^  - \{id: "([^"]+)", level: (\w+), .*?parents: \[([^\]]*)\], .*?lifecycle: ([\w-]+)'
)
# Допустимое расхождение копии со спицей до РТ-6 (раздел 2.1 реестра).
ALLOWED_LIFECYCLE_DRIFT = {("added-for-review", "accepted")}

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
        active, _, retired = stubs.partition("Снятые заглушки.")
        self.assertEqual(table_ids(active, "З"), ["З-2", "З-3", "З-4"])
        # Снятая заглушка остаётся строкой: id не переиспользуется (BL-163).
        self.assertEqual(table_ids(retired, "З"), ["З-1"])
        self.assertRegex(retired, r"(?m)^\| З-1 \| И-2 .*BL-163")
        tasks = table_ids(section(self.body, "## 6. Задачи для репозитория runtime"), "РТ")
        self.assertEqual(tasks, ["РТ-1", "РТ-2", "РТ-3", "РТ-4", "РТ-6"])
        for row in re.findall(r"^\| З-\d .*$", active, re.M):
            with self.subTest(row=row[:12]):
                self.assertRegex(row, r"\| РТ-\d \|$")

    def test_taxonomy_catalog_reference(self):
        # BL-163: И-2 — «Да», ссылка на каталог по SHA раздела 1, без заглушки.
        row = re.search(r"^\| И-2 \|.*$", section(self.body, "## 2. Перечень"), re.M).group(0)
        self.assertIn(
            f"mango-ba-ai-runtime/blob/{self.sha}/{RUNTIME_CATALOG}", row, "И-2 ведёт на каталог"
        )
        self.assertIn("| Да: закрытый каталог (`closed: true`), 353 узла", row)
        self.assertNotRegex(row, r"[Зз]аглушка З-")
        rt1 = re.search(r"^\| РТ-1 \|.*$", self.body, re.M).group(0)
        self.assertIn("mango-ba-ai-runtime/pull/16", rt1, "РТ-1 ведёт на PR runtime")
        self.assertIn("### 2.1. Каталог продуктов: копия и сверка со спицей", self.body)

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


def runtime_catalog(path):
    """Шапка и узлы копии каталога runtime (одна строка — один узел)."""
    head, nodes = {}, {}
    for line in text(path).splitlines():
        match = RUNTIME_NODE.match(line)
        if match:
            node_id, level, parents, lifecycle = match.groups()
            nodes[node_id] = {
                "level": level,
                "parents": sorted(x.strip().strip('"') for x in parents.split(",") if x.strip()),
                "lifecycle": lifecycle,
            }
        elif re.match(r"^[a-z_0-9]+: ", line):
            key, value = line.split(": ", 1)
            head[key] = value.strip().strip('"')
    return head, nodes


@unittest.skipUnless(os.environ.get("RUNTIME_CLONE"), "нет RUNTIME_CLONE")
class RuntimeCatalog(unittest.TestCase):
    """Сверка копии каталога runtime со спицей (реестр, раздел 2.1; BL-163)."""

    @classmethod
    def setUpClass(cls):
        clone = Path(os.environ["RUNTIME_CLONE"])
        sha = frontmatter(text(REGISTRY)).get("runtime_sha", "")
        head = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=clone, capture_output=True, text=True
        ).stdout.strip()
        if head != sha:
            raise unittest.SkipTest(f"клон на {head}, реестр на {sha}")
        cls.raw = text(clone / RUNTIME_CATALOG)
        cls.head, cls.nodes = runtime_catalog(clone / RUNTIME_CATALOG)
        cls.spoke = {n["id"]: n for n in json.loads(text(CATALOG))["nodes"]}

    def test_closed_and_complete(self):
        self.assertRegex(self.raw, r"(?m)^closed: true$")
        self.assertEqual(self.raw.count("\n  - {id: "), len(self.nodes), "строка узла не разобрана")
        self.assertEqual(len(self.nodes), len(self.spoke))
        self.assertEqual(set(self.nodes), set(self.spoke))

    def test_levels_and_parents(self):
        for node_id, node in self.spoke.items():
            with self.subTest(node=node_id):
                self.assertEqual(self.nodes[node_id]["level"], LEVELS[node["level"]])
                self.assertEqual(self.nodes[node_id]["parents"], sorted(node["parent_ids"]))

    def test_source_sha256(self):
        commit = self.head["source_commit"]
        blob = subprocess.run(
            ["git", "show", f"{commit}:docs/taxonomy/products.json"], cwd=ROOT, capture_output=True
        )
        if blob.returncode != 0:
            self.skipTest(f"коммит {commit[:7]} недоступен (неглубокий клон)")
        self.assertEqual(hashlib.sha256(blob.stdout).hexdigest(), self.head["source_sha256"])

    def test_lifecycle_drift_allowed(self):
        for node_id, node in self.spoke.items():
            pair = (self.nodes[node_id]["lifecycle"], node["lifecycle"])
            if pair[0] != pair[1]:
                with self.subTest(node=node_id):
                    self.assertIn(pair, ALLOWED_LIFECYCLE_DRIFT, "расхождение вне раздела 2.1")
                    self.assertEqual(node.get("origin"), "portal-update")


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
