#!/usr/bin/env python3
"""Регрессионная проверка постановки задач РТ-1 и РТ-3 для runtime (issue #434).

RFC-RT-001 ``docs/rfc/2026-11-runtime-product-catalog-golden-set.md`` — готовые
к копированию тела задач для ``mango-ba-ai-runtime`` (РТ-1 — каталог продуктов,
РТ-3 — golden set по классам) и Хаба (ХАБ-1), механизм снятия заглушки
таксономии З-1. Проверка фиксирует то, что требует DoD issue #434:

* RFC: frontmatter Хаба, разделы в порядке (обоснование BL-156, РТ-1, РТ-3,
  механизм, следующие шаги), ссылки на #427, #431 и #434;
* тела задач — по шаблону ``docs/task-for-konard-template.md`` (все разделы в
  порядке), только полные URL: задача запускается из runtime;
* явный пункт РТ-1 о фиксации таксономии в runtime и звенья М-1…М-6;
* РТ-3 ссылается на требование #427 и задаёт структуру данных по классам:
  файлы ``golden/cases-<класс>.yaml``, поля ``product_class`` и
  ``atomic_function``;
* числа RFC совпадают с каталогом спицы ``docs/taxonomy/products.json``
  (пересчёт здесь же), прототип ``taxonomy/mango-products.yaml`` — с каталогом;
  функции эталонов runtime, названные в Ф-7, в каталоге отсутствуют;
* ссылки на runtime — только по SHA реестра (ТС-1, ТС-5);
* реестр справочников: строки РТ-1 и РТ-3 ведут в RFC, id заглушек и задач
  прежние; RFC зарегистрирован в реестре RFC, карте артефактов, бэклоге
  (Р-17, BL-163), CHANGELOG;
* относительные ссылки и якоря RFC разрешаются;
* подраздел 3.1 (комментарий владельца к PR #437): происхождение каталога
  из классификации Хаба и связь с индустриальным слоем (``origin``, ``row``)
  пересчитываются по каталогу; ссылки на Хаб — только по SHA; индустриальный
  слой заведён только задачей BL-164 (бэклог, карточка, шаг раздела 11);
* при ``HUB_CLONE=<путь к клону Хаба>`` — классификация не менялась с коммита
  источника каталога, таблицы индустриального слоя — по одной строке на
  Capability с ``row``; без клона проверка пропускается;
* при ``RUNTIME_CLONE=<путь к клону runtime на SHA реестра>`` — факты Ф-1,
  Ф-6, Ф-7 и отсутствие каталога в runtime проверяются на клоне; без клона
  проверка пропускается (CI без сети).

Запуск: ``python3 scripts/validate_issue_434_runtime_tasks.py``.
"""

import collections
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
RFC = ROOT / "docs/rfc/2026-11-runtime-product-catalog-golden-set.md"
REGISTRY = ROOT / "standards/bcreq-runtime-references.md"
CATALOG = ROOT / "docs/taxonomy/products.json"
PROTOTYPE = ROOT / "experiments/issue_434/prototype/mango-products.yaml"
TEMPLATE = ROOT / "docs/task-for-konard-template.md"
RFC_REGISTER = ROOT / "docs/rfc/rfc-register.md"
ARTIFACT_MAP = ROOT / "pr-ops/artifact-map.md"
BACKLOG = ROOT / "pr-ops/BACKLOG.md"
TRACK_B = ROOT / "pr-ops/backlog-ba-model.md"
CHANGELOG = ROOT / "CHANGELOG.md"
HUB = "https://github.com/G-Ivan-A/hybrid-Intelligence-lab"
HUB_SHA = "c06075d0b45da70cb68e2df3851b861b5ec3aed1"
CLASSIFICATION = "research/mango/2026-05-22-classification.md"
# Коммит Хаба, из которого построен каталог спицы (``source_urls``).
CATALOG_HUB_SHA = "cd5d6e4b72700e43ccca6c96119308ab5a6d7379"
HUB_LINK = re.compile(r"github\.com/G-Ivan-A/hybrid-Intelligence-lab/(?:blob|tree)/([^/\s)`]+)/")
# Поля индустриального слоя, которых в узлах каталога быть не должно (Ф-18).
INDUSTRY_KEYS = re.compile(r"tm_?forum|unspsc|okpd|окпд|industry", re.I)

REPO = "https://github.com/G-Ivan-A/mango_ba_prompts"
CATALOG_VERSION = "2026-10-28.1"
CATALOG_COMMIT = "7f920e2e967ad1331e027fef885ea68ecef7070f"
RUNTIME_CLASSES = ("contact-center", "voice-ucaas", "analytics-reporting")
LEVELS = ("Domain", "Capability", "Feature", "Atomic Function")

SECTIONS = (
    "## Summary / BLUF",
    "## 0. Тип и дом артефакта",
    "## 1. Проверенное текущее состояние",
    "## 2. Обоснование и связь с BL-156",
    "## 3. ССОТ и разделение ответственности",
    "### 3.1. Происхождение таксономии и индустриальный слой",
    "## 4. Механизм снятия заглушки таксономии (критично)",
    "## 5. РТ-1 — тело задачи для `mango-ba-ai-runtime` (копировать целиком)",
    "## 6. ХАБ-1 — тело задачи для `hybrid-Intelligence-lab` (норма привязки)",
    "## 7. РТ-3 — тело задачи для `mango-ba-ai-runtime` (копировать целиком)",
    "### 7.1. Структура данных по классам",
    "## 8. Связанные задачи спицы и решение владельца",
    "## 9. Риски, допущения, открытые вопросы",
    "## 10. Обоснованные обходы",
    "## 11. Рекомендуемые следующие шаги (после согласования)",
    "## Related Artifacts",
)
# Тела задач: (раздел RFC, заголовок задачи).
BODIES = (
    ("## 5. ", "РТ-1. "),
    ("## 6. ", "ХАБ-1. "),
    ("## 7. ", "РТ-3. "),
)
# Функции, которые эталоны runtime называют в markdown (Ф-7).
GOLDEN_MD_FUNCTIONS = (
    "queue-callback-offer",
    "handling-report-export",
    "callback-offer",
    "queue-capacity-limit",
    "group-report-threshold",
    "after-hours-greeting",
)
RUNTIME_LINK = re.compile(
    r"(?:github\.com/G-Ivan-A/mango-ba-ai-runtime/(?:blob|tree|raw)/"
    r"|raw\.githubusercontent\.com/G-Ivan-A/mango-ba-ai-runtime/)"
    # «<SHA реестра>» в образце текста промпта — шаблон, а не ссылка.
    r"([^/\s)`\"<]+)(/[^\s)`\"]*)?"
)
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


def strip_fences(body):
    """Текст без блоков кода: заголовки тел задач — не заголовки RFC."""
    out, fence = [], None
    for line in body.splitlines():
        mark = re.match(r"^(`{3,}|~{3,})", line)
        if mark and fence is None:
            fence = mark.group(1)
            continue
        if fence is not None:
            if line.startswith(fence) and line.strip() == fence:
                fence = None
            continue
        out.append(line)
    return "\n".join(out)


def slug(heading):
    value = re.sub(r"[`*_]", "", heading.strip().lower())
    value = re.sub(r"[^\w\s-]", "", value)
    return re.sub(r"\s", "-", value)


def anchors(path):
    found = set()
    for heading in re.findall(r"^#{1,6} (.+)$", strip_fences(text(path)), re.M):
        base, n = slug(heading), 1
        candidate = base
        while candidate in found:
            candidate, n = f"{base}-{n}", n + 1
        found.add(candidate)
    return found


def rfc_section(prefix):
    """Раздел RFC (с телами задач) от заголовка с префиксом до следующего «## »."""
    body = text(RFC)
    start = re.search(rf"^{re.escape(prefix)}.*$", body, re.M)
    assert start, prefix
    rest = body[start.end():]
    # Следующий раздел RFC: «## <цифра>.» или «## Related» вне тел задач.
    stop = re.search(r"^## (?:\d+\. |Related Artifacts)", rest, re.M)
    return rest[: stop.start()] if stop else rest


def task_body(section_text):
    match = re.search(r"^````markdown\n(.*?)\n````$", section_text, re.S | re.M)
    assert match, "нет блока ````markdown с телом задачи"
    return match.group(1)


def catalog_stats():
    """Пересчёт чисел раздела 1 RFC по каталогу спицы."""
    data = json.loads(text(CATALOG))
    nodes = {n["id"]: n for n in data["nodes"]}
    compat = data["runtime_compatibility"]
    domain_to_class = {compat[c]: c for c in RUNTIME_CLASSES}
    memo = {}

    def domains(node_id):
        if node_id not in memo:
            node = nodes[node_id]
            if node["level"] == "Domain":
                memo[node_id] = {node_id}
            else:
                found = set()
                for parent in node["parent_ids"]:
                    found |= domains(parent)
                memo[node_id] = found
        return memo[node_id]

    per_class = {c: collections.Counter() for c in RUNTIME_CLASSES}
    lifecycle = {c: collections.Counter() for c in RUNTIME_CLASSES}
    outside = collections.Counter()
    multi = 0
    for node in nodes.values():
        classes = {domain_to_class[d] for d in domains(node["id"]) if d in domain_to_class}
        if not classes:
            outside[node["level"]] += 1
        if node["level"] == "Atomic Function" and len(classes) == 3:
            multi += 1
        for c in classes:
            per_class[c][node["level"]] += 1
            if node["level"] == "Atomic Function":
                lifecycle[c][node["lifecycle"]] += 1
    return {
        "data": data,
        "nodes": nodes,
        "per_level": collections.Counter(n["level"] for n in nodes.values()),
        "per_class": per_class,
        "lifecycle": lifecycle,
        "outside": outside,
        "af_in_three_classes": multi,
        "compat": compat,
    }


def registry_sha():
    return frontmatter(text(REGISTRY))["runtime_sha"]


class RfcStructure(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.body = text(RFC)
        cls.outline = strip_fences(cls.body)

    def test_frontmatter(self):
        meta = frontmatter(self.body)
        for key in ("status", "version", "updated", "temperature", "owner", "source", "type"):
            self.assertIn(key, meta, key)
        self.assertEqual(meta["type"], "rfc")
        self.assertIn(meta["status"], ("proposed", "accepted", "rejected", "superseded"))
        self.assertEqual(meta["source"], f"{REPO}/issues/434")
        self.assertNotIn("ai-generated", meta)

    def test_sections_in_order(self):
        headings = re.findall(r"^#{2,3} .+$", self.outline, re.M)
        positions = []
        for heading in SECTIONS:
            with self.subTest(heading=heading):
                self.assertIn(heading, headings)
                positions.append(headings.index(heading))
        self.assertEqual(positions, sorted(positions), "порядок разделов")

    def test_issue_links(self):
        # #431 — источник шага владельца; #427 — требование golden set по классам.
        for target in (f"{REPO}/pull/431", f"{REPO}/issues/427", f"{REPO}/issues/434"):
            with self.subTest(target=target):
                self.assertIn(target, self.outline)
        rt3 = rfc_section("## 7. ")
        self.assertIn(f"]({REPO}/issues/427)", rt3, "РТ-3 ссылается на #427 вне тела")
        self.assertIn(f"{REPO}/issues/427", task_body(rt3), "РТ-3: #427 в теле задачи")

    def test_bl156_rationale(self):
        block = rfc_section("## 2. ")
        self.assertIn("backlog-ba-model.md#bl-156-", block)
        for needle in ("Ш-2", "З-1", "З-3", "golden set"):
            self.assertIn(needle, block, needle)

    def test_next_steps_justified(self):
        block = rfc_section("## 11. ")
        items = re.findall(r"^\d+\. .*?(?=^\d+\. |\Z)", block, re.M | re.S)
        self.assertGreaterEqual(len(items), 5)
        for item in items:
            with self.subTest(item=item[:40]):
                self.assertIn("Почему", item, "у шага нет обоснования")

    def test_type_and_home(self):
        block = rfc_section("## 0. ")
        self.assertIn("**Дом — `docs/rfc/`", block)
        self.assertIn("RFC-RT-001", block)
        # Альтернативы рассмотрены: таблица «Вариант | Почему».
        self.assertGreaterEqual(len(re.findall(r"^\| .+ \| .+ \|$", block, re.M)), 6)


class TaskBodies(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.template = re.findall(r"^## .+$", text(TEMPLATE), re.M)

    def test_template_sections_in_order(self):
        for prefix, title in BODIES:
            with self.subTest(task=title):
                section = rfc_section(prefix)
                self.assertRegex(section, rf"(?m)^Заголовок: `{re.escape(title)}")
                headings = re.findall(r"^## .+$", task_body(section), re.M)
                self.assertEqual(headings, self.template)

    def test_full_urls_only(self):
        # Задача запускается из runtime: относительные пути спицы там не работают.
        for prefix, title in BODIES:
            with self.subTest(task=title):
                body = task_body(rfc_section(prefix))
                self.assertFalse(re.search(r"\]\((?!https?://)", body), "относительная ссылка")
                self.assertIn(f"{REPO}/blob/main/docs/rfc/{RFC.name}", body)
                self.assertNotRegex(body, r"(?<![\w/.-])\.\./")

    def test_rt1_obligation(self):
        body = task_body(rfc_section("## 5. "))
        self.assertIn("taxonomy/mango-products.yaml", body)
        self.assertIn("tests/runtime-smoke.sh", body)
        self.assertIn("closed: true", body)
        self.assertIn(CATALOG_VERSION, body)
        mechanism = rfc_section("## 4. ")
        self.assertIn(
            "Задача РТ-1 обязывает runtime зафиксировать актуальную\nпродуктовую таксономию Mango",
            mechanism,
        )

    def test_rt3_structure(self):
        section = rfc_section("## 7. ")
        body = task_body(section)
        for needle in (
            "golden/cases-<класс>.yaml",
            "golden/cases.yaml",
            "product_class",
            "atomic_function",
            "confirmed_by",
        ):
            self.assertIn(needle, body, needle)
        sample = re.search(r"```yaml\n(.*?)\n```", body, re.S)
        self.assertTrue(sample, "образец случая в YAML")
        self.assertIn("atomic_function:", sample.group(1))
        self.assertIn("product_class:", sample.group(1))
        table = section.split("### 7.1.", 1)[1]
        files = {"contact-center": "golden/cases.yaml"}
        for cls in RUNTIME_CLASSES:
            name = files.get(cls, f"golden/cases-{cls}.yaml")
            self.assertRegex(table, rf"(?m)^\| `{cls}` \| `{re.escape(name)}` \|", cls)


class Mechanism(unittest.TestCase):
    def test_links_m1_to_m6(self):
        block = rfc_section("## 4. ")
        ids = re.findall(r"^\| (М-\d) \|", block, re.M)
        self.assertEqual(ids, [f"М-{n}" for n in range(1, 7)])

    def test_prompt_reading_text(self):
        block = rfc_section("## 4. ")
        sample = re.search(r"```text\n(.*?)\n```", block, re.S).group(1)
        self.assertIn(
            "https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/<SHA реестра>/taxonomy/mango-products.yaml",
            sample,
        )
        self.assertIn("[ТРЕБУЕТСЯ УТОЧНЕНИЕ]", sample)
        self.assertIn("added-for-review", sample)

    def test_smoke_simulation_log(self):
        # М-2 проверено симуляцией: без каталога и с выдуманной функцией — красный.
        log = text(ROOT / "experiments/issue_434/runtime-smoke-sim.log")
        scenarios = dict(re.findall(r"=== scenario (\w+) ===.*?exit: (\d+)", log, re.S))
        self.assertEqual(scenarios, {"missing": "1", "catalog": "0", "invented": "1", "catalogid": "0"})


class CatalogNumbers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.stats = catalog_stats()
        cls.body = text(RFC)
        if cls.stats["data"]["catalog_version"] != CATALOG_VERSION:
            raise unittest.SkipTest(
                f"каталог спицы {cls.stats['data']['catalog_version']} новее {CATALOG_VERSION}: "
                "обновите числа раздела 1 RFC-RT-001 и CATALOG_VERSION"
            )

    def test_levels(self):
        per_level = self.stats["per_level"]
        self.assertEqual(sum(per_level.values()), 353)
        fact = re.search(r"^\| Ф-13 \|.*$", self.body, re.M).group(0)
        self.assertIn(f"{sum(per_level.values())} узла", fact)
        for level in LEVELS:
            self.assertIn(f"{level} {per_level[level]}", fact, level)

    def test_per_class_table(self):
        for cls in RUNTIME_CLASSES:
            with self.subTest(cls=cls):
                counts = self.stats["per_class"][cls]
                life = self.stats["lifecycle"][cls]
                row = (
                    f"| `{cls}` | `{self.stats['compat'][cls]}` | {counts['Capability']} | "
                    f"{counts['Feature']} | {counts['Atomic Function']} | "
                    f"{life['retained']} / {life['added-for-review']} |"
                )
                self.assertIn(row, self.body)
        outside = self.stats["outside"]
        self.assertIn(
            f"| {outside['Capability']} | {outside['Feature']} | {outside['Atomic Function']} | — |",
            self.body,
        )
        self.assertIn(f"{self.stats['af_in_three_classes']} функций относятся сразу к трём классам", self.body)

    def test_golden_md_functions_not_in_catalog(self):
        ids = set(self.stats["nodes"])
        tails = {node_id.rsplit("/", 1)[-1] for node_id in ids}
        fact = re.search(r"^\| Ф-7 \|.*$", self.body, re.M).group(0)
        for name in GOLDEN_MD_FUNCTIONS:
            with self.subTest(function=name):
                self.assertIn(f"`{name}`", fact)
                self.assertNotIn(name, ids)
                self.assertNotIn(name, tails)

    def test_prototype_matches_catalog(self):
        prototype = text(PROTOTYPE)
        nodes = re.findall(r'^  - \{id: "([^"]+)", level: (\w+),', prototype, re.M)
        self.assertEqual(len(nodes), len(self.stats["nodes"]))
        self.assertEqual({i for i, _ in nodes}, set(self.stats["nodes"]))
        self.assertIn("\nclosed: true\n", prototype)
        self.assertIn("\nvocabulary: mango-products\n", prototype)
        self.assertIn(f"source_sha256: {hashlib.sha256(CATALOG.read_bytes()).hexdigest()}", prototype)
        self.assertIn(f'source_commit: "{CATALOG_COMMIT}"', prototype)

    def test_catalog_commit_pinned(self):
        links = re.findall(r"mango_ba_prompts/blob/([0-9a-f]{40})/docs/taxonomy/products\.json", self.body)
        self.assertTrue(links)
        self.assertEqual(set(links), {CATALOG_COMMIT})
        probe = subprocess.run(
            ["git", "cat-file", "-p", f"{CATALOG_COMMIT}:docs/taxonomy/products.json"],
            cwd=ROOT, capture_output=True,
        )
        if probe.returncode != 0:
            self.skipTest("коммит каталога недоступен (неглубокий клон)")
        self.assertEqual(
            json.loads(probe.stdout.decode("utf-8"))["catalog_version"], CATALOG_VERSION
        )


class Links(unittest.TestCase):
    def test_runtime_links_pinned_to_registry(self):
        sha = registry_sha()
        found = RUNTIME_LINK.findall(text(RFC))
        self.assertTrue(found)
        for ref, path in found:
            with self.subTest(link=f"{ref}{path}"):
                self.assertEqual(ref, sha)

    def test_relative_links_and_anchors(self):
        for target in LINK_RE.findall(strip_fences(text(RFC))):
            if re.match(r"^[a-z]+:", target):
                continue
            with self.subTest(target=target):
                path, _, anchor = unquote(target).partition("#")
                resolved = (RFC.parent / path).resolve() if path else RFC
                self.assertTrue(resolved.exists(), resolved)
                if anchor and resolved.suffix == ".md":
                    self.assertIn(anchor, anchors(resolved), f"якорь {anchor}")


class Records(unittest.TestCase):
    def test_registry_rows(self):
        body = text(REGISTRY)
        head = re.match(r"^---\n(.*?)\n---\n", body, re.S).group(1)
        self.assertIn(f'  - "docs/rfc/{RFC.name}"', head, "RFC в related_artifacts реестра")
        rfc_anchors = anchors(RFC)
        for task, prefix in (("РТ-1", "#5-рт-1-"), ("РТ-3", "#7-рт-3-")):
            with self.subTest(task=task):
                row = re.search(rf"^\| {task} \|.*$", body, re.M).group(0)
                links = [t for t in LINK_RE.findall(row) if RFC.name in t]
                self.assertTrue(links, "строка ведёт в RFC-RT-001")
                anchor = links[0].split("#", 1)[1]
                self.assertTrue(f"#{anchor}".startswith(prefix), anchor)
                self.assertIn(anchor, rfc_anchors)
        # Id заглушек и задач не меняются: на них ссылаются карточки и валидатор #430.
        self.assertEqual(re.findall(r"^\| (З-\d) \|", body, re.M), ["З-1", "З-2", "З-3", "З-4"])
        self.assertEqual(re.findall(r"^\| (РТ-\d) \|", body, re.M), ["РТ-1", "РТ-2", "РТ-3", "РТ-4"])

    def test_rfc_register(self):
        body = text(RFC_REGISTER)
        self.assertRegex(body, rf"(?m)^\| \[RFC-RT-001\]\({re.escape(RFC.name)}\) \|.*(?:`proposed`|`accepted`)")
        self.assertIn("issue #434", body)

    def test_artifact_map(self):
        self.assertIn(f"/docs/rfc/{RFC.name}", text(ARTIFACT_MAP))

    def test_backlog(self):
        backlog = text(BACKLOG)
        self.assertRegex(backlog, r"(?m)^\| \*\*Р-17\*\* \|.*\| BL-163 \|")
        self.assertRegex(backlog, r"(?m)^\| BL-163 \| \[Реестр справочников на каталог продуктов runtime\]")
        self.assertRegex(backlog, r"\*\*Критерий закрытия\.\*\* [^\n]*BL-159[\s\S]*?BL-163")
        self.assertIn("| `ХАБ-N` |", backlog)
        card = text(TRACK_B).split("### BL-163. ", 1)[1]
        self.assertIn("**Решение владельца.** Р-17", card)
        self.assertIn(RFC.name, card)

    def test_changelog(self):
        unreleased = text(CHANGELOG).split("\n## ", 2)[1]
        self.assertIn("Issue #434", unreleased)
        self.assertIn("RFC-RT-001", unreleased)


class IndustryTaxonomy(unittest.TestCase):
    """Подраздел 3.1: исток таксономии Mango и индустриальный слой (PR #437)."""

    @classmethod
    def setUpClass(cls):
        cls.body = text(RFC)
        cls.data = json.loads(text(CATALOG))
        cls.section = rfc_section("## 3. ").split("### 3.1. ", 1)[1]

    def test_catalog_lineage(self):
        self.assertIn(f"{HUB}/blob/{CATALOG_HUB_SHA}/{CLASSIFICATION}", self.data["source_urls"])
        origin = collections.Counter(n["origin"] for n in self.data["nodes"])
        self.assertEqual(sum(origin.values()), len(self.data["nodes"]))
        fact = re.search(r"^\| Ф-16 \|.*$", self.body, re.M).group(0)
        self.assertIn(f"{origin['inherited']} узлов `origin: inherited`", fact)
        self.assertIn(f"{origin['portal-update']} — `portal-update`", fact)
        self.assertIn(f"`{CATALOG_HUB_SHA[:8]}`", fact)

    def test_row_bridge(self):
        caps = [n for n in self.data["nodes"] if n["level"] == "Capability"]
        missing = [n["id"] for n in caps if "row" not in n]
        fact = re.search(r"^\| Ф-18 \|.*$", self.body, re.M).group(0)
        self.assertIn(f"{len(caps) - len(missing)} из {len(caps)} Capability", fact)
        for node_id in missing:
            self.assertIn(f"`{node_id}`", fact)
        for node in self.data["nodes"]:
            for key in node:
                with self.subTest(node=node["id"], key=key):
                    self.assertIsNone(INDUSTRY_KEYS.search(key), "поле индустриального слоя в каталоге")

    def test_hub_links_pinned(self):
        refs = HUB_LINK.findall(self.body)
        self.assertTrue(refs)
        for ref in refs:
            with self.subTest(ref=ref):
                self.assertRegex(ref, r"^[0-9a-f]{40}$", "ссылка на Хаб без SHA")
        self.assertIn(f"{HUB}/blob/{HUB_SHA}/{CLASSIFICATION}", self.body)

    def test_section_checks_and_alternatives(self):
        for n in range(1, 7):
            self.assertRegex(self.section, rf"(?m)^\| П-{n} \|")
        self.assertIn("backlog-ba-model.md#bl-164-", self.section)
        self.assertIn(f"{REPO}/pull/437", self.section)
        table = self.section.split("Рассмотренные альтернативы", 1)[1]
        self.assertGreaterEqual(len(re.findall(r"^\| (?!---|Вариант).+ \|$", table, re.M)), 4)
        self.assertEqual(table.count("**Принят**"), 1)

    def test_bl164_only_backlog(self):
        backlog = text(BACKLOG)
        row = re.search(r"^\| BL-164 \|.*$", backlog, re.M).group(0)
        self.assertIn("| deferred (triggered) |", row)
        self.assertIn("BL-133", row)
        self.assertRegex(backlog, r"\*\*Критерий закрытия\.\*\* [^\n]*BL-159[\s\S]*?BL-164")
        card = text(TRACK_B).split("### BL-164. ", 1)[1]
        for needle in ("**Почему.**", "**Источники.**", "**Зависит от.** BL-133", "**Готово, когда.**", RFC.name):
            self.assertIn(needle, card, needle)
        self.assertIn(f"{HUB}/blob/{HUB_SHA}/{CLASSIFICATION}", card)
        # Индустриальный слой не входит в тела задач runtime и Хаба (R-9).
        for prefix, _ in BODIES:
            with self.subTest(body=prefix):
                self.assertNotRegex(task_body(rfc_section(prefix)), r"UNSPSC|ОКПД|BL-164")
        steps = rfc_section("## 11. ")
        self.assertIn("BL-164", steps)
        self.assertIn("docs/hub-research-dependencies.md", steps)


class HubClone(unittest.TestCase):
    """Факты Ф-16, Ф-17 на клоне Хаба (HUB_CLONE), без клона — пропуск."""

    @classmethod
    def setUpClass(cls):
        clone = os.environ.get("HUB_CLONE")
        if not clone:
            raise unittest.SkipTest("HUB_CLONE не задан")
        cls.clone = Path(clone)

    def test_classification_unchanged_since_catalog(self):
        diff = subprocess.run(
            ["git", "-C", str(self.clone), "diff", "--quiet", CATALOG_HUB_SHA, HUB_SHA, "--", CLASSIFICATION]
        )
        self.assertEqual(diff.returncode, 0)

    def test_industry_tables_cover_rows(self):
        body = subprocess.run(
            ["git", "-C", str(self.clone), "show", f"{HUB_SHA}:{CLASSIFICATION}"],
            capture_output=True, text=True, check=True,
        ).stdout
        rows = {int(n) for n in re.findall(r"(?m)^\| *(\d+) *\| ", body.split("## Сравнительная таблица международной классификации", 1)[1].split("\n## ", 1)[0])}
        caps = [n for n in json.loads(text(CATALOG))["nodes"] if n["level"] == "Capability" and "row" in n]
        for node in caps:
            with self.subTest(capability=node["id"]):
                self.assertIn(int(node["row"]), rows)
        self.assertIn("## Рабочая таксономия для входящих требований", body)
        for field in ("TM Forum domain", "UNSPSC code", "ОКПД 2 class", "Russian standards overlay"):
            self.assertIn(f"| {field} |", body)


class RuntimeClone(unittest.TestCase):
    """Факты раздела 1 на клоне runtime (RUNTIME_CLONE), без клона — пропуск."""

    @classmethod
    def setUpClass(cls):
        clone = os.environ.get("RUNTIME_CLONE")
        if not clone:
            raise unittest.SkipTest("RUNTIME_CLONE не задан")
        cls.clone = Path(clone)
        head = subprocess.run(
            ["git", "-C", clone, "rev-parse", "HEAD"], capture_output=True, text=True
        ).stdout.strip()
        if head != registry_sha():
            raise unittest.SkipTest(f"клон на {head}, реестр на {registry_sha()}")

    def test_stub_is_real(self):
        products = text(self.clone / "taxonomy/products.yaml")
        for cls in RUNTIME_CLASSES:
            self.assertIn(cls, products)
        self.assertFalse((self.clone / "taxonomy/mango-products.yaml").exists())

    def test_golden_index(self):
        cases = text(self.clone / "golden/cases.yaml")
        self.assertIn("structural_only: true", cases)
        self.assertIn("product_class: contact-center", cases)
        self.assertNotIn("atomic_function", cases)

    def test_golden_md_functions(self):
        corpus = "".join(text(p) for p in sorted((self.clone / "golden").glob("*.md")))
        for name in GOLDEN_MD_FUNCTIONS:
            with self.subTest(function=name):
                self.assertIn(name, corpus)


if __name__ == "__main__":
    result = unittest.main(argv=[sys.argv[0], "-v"], exit=False).result
    sys.exit(0 if result.wasSuccessful() else 1)
