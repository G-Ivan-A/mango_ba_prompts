#!/usr/bin/env python3
"""Issue #506, M2: подготовка приёма SSOT этапа 1 в runtime (BL-246, PR #515).

Ответ на комментарий владельца к PR #514 (7225787518): блокер
«BL-185…BL-188: приём SSOT этапа 1» не снят; спица готовит передачу, задача
выставлена в runtime. Проверяет без LLM, без сети и без клона runtime:

* манифест 0.2: заменяет 0.1, ``source_commit`` есть в истории, 135
  артефактов по четырём карточкам; ``git_blob``, режим ``100644`` и sha256
  каждого артефакта совпадают с ``source_commit``; имена ASCII; файлов
  инструкций клиента (``AGENTS.md``, ``CLAUDE.md``, ``CONTEXT.md``,
  ``SKILL.md``) в передаче нет; карта гейтов IDE — в BL-188, её ``sources``
  совпадают с манифестом, ``runtime_path`` — внутри каталога копии;
  правило 5 политики синхронизации — Р-RT-7, вариант 7а;
* карта ссылок: тот же ``source_commit`` и каталог; ссылки только
  ``outside`` от артефактов передачи на цели вне передачи; permalink
  закреплён на ``source_commit``; счётчики ``summary`` сходятся с
  перечнями; кандидаты передачи №2 — нормативные цели;
* журнал пробной передачи: ``ИТОГ: OK``, 135 из 135, тест карты гейтов не
  пропущен, 0 совпадений шаблонов перед публикацией;
* RFC-RT-003, раздел 12: подразделы 12.1…12.N без пропусков, ≥ 20 граничных
  кейсов без пропусков, Р-RT-22 и варианты А…Г, предусловия П-0…П-2,
  sha256 файла манифеста, ссылка на комментарий владельца и задачу runtime;
* бэклог: BL-185…BL-188 ``DONE`` со ссылками на задачу, PR runtime и Р-RT-22,
  BL-246 ``DONE``, для BL-190 зафиксирован триггер, блок
  «Движение по цепочке (#506, M2)»: предыдущий, текущий и открываемый шаг;
* заглушки номера задачи runtime не осталось.
"""
import hashlib
import json
import re
import subprocess
import sys
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs/contracts/ssot-stage1-handoff-manifest.json"
MANIFEST_MD = ROOT / "docs/contracts/ssot-stage1-handoff-manifest.md"
LINK_MAP = ROOT / "docs/contracts/ssot-stage1-link-map.json"
DRY_RUN = ROOT / "experiments/issue_506/m2-transfer-dry-run.log"
RFC = ROOT / "docs/rfc/2026-11-runtime-ide-orchestrator.md"
BACKLOG = ROOT / "pr-ops/BACKLOG.md"
MODEL = ROOT / "pr-ops/backlog-ba-model.md"
REPOSITORY = ROOT / "pr-ops/backlog-repository.md"

OWNER_COMMENT = "https://github.com/G-Ivan-A/mango_ba_prompts/pull/514#issuecomment-7225787518"
PR = "https://github.com/G-Ivan-A/mango_ba_prompts/pull/515"
RUNTIME_ISSUE = re.compile(r"https://github\.com/G-Ivan-A/mango-ba-ai-runtime/issues/(\d+)")
RUNTIME_PR = "https://github.com/G-Ivan-A/mango-ba-ai-runtime/pull/32"
PUBLICATION_DECISION = "https://github.com/G-Ivan-A/mango-ba-ai-runtime/issues/31#issuecomment-7226978319"
GATE_MAP = "docs/ba-processes/bcreq-ide-gates.json"
CARDS = {"BL-185": 38, "BL-186": 31, "BL-187": 62, "BL-188": 4}
ARTIFACTS = sum(CARDS.values())
CLIENT_INSTRUCTIONS = {"AGENTS.md", "CLAUDE.md", "CONTEXT.md", "SKILL.md"}
SECTION_12 = "## 12. Постановка M2: приём SSOT этапа 1 (задача runtime)"
PLACEHOLDER = "RTISSUE"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True)


def section(text: str, heading: str) -> str:
    """Текст раздела от заголовка до следующего заголовка того же уровня."""
    level = heading.split(" ", 1)[0]
    start = text.index(heading + "\n")
    rest = text[start + len(heading):]
    match = re.search(rf"^{level} ", rest, re.M)
    return rest[: match.start()] if match else rest


def card(text: str, code: str) -> str:
    return text.split(f"### {code}. ", 1)[1].split("\n### ", 1)[0]


def row(text: str, code: str) -> str:
    return next(line for line in text.splitlines() if line.startswith(f"| {code} | "))


class ManifestTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m = json.loads(read(MANIFEST))
        cls.commit = cls.m["source_commit"]
        cls.by_path = {a["path"]: a for a in cls.m["artifacts"]}

    def test_header(self):
        self.assertEqual(self.m["version"], "0.2")
        self.assertEqual(self.m["supersedes"]["version"], "0.1")
        self.assertRegex(self.commit, r"^[0-9a-f]{40}$")
        self.assertEqual(self.m["summary"]["artifacts"], ARTIFACTS)
        self.assertEqual(self.m["summary"]["transfer_cards"], CARDS)
        self.assertEqual(Counter(a["transfer_card"] for a in self.m["artifacts"]), Counter(CARDS))
        self.assertEqual(len(self.by_path), ARTIFACTS, "пути артефактов повторяются")
        self.assertTrue(all(a["source_commit"] == self.commit for a in self.m["artifacts"]))
        self.assertEqual(self.m["transfer"]["cards"], list(CARDS))
        self.assertIn("раздел 12", self.m["transfer"]["statement"])

    def test_bytes_match_source_commit(self):
        """Побайтная копия: blob, режим и sha256 каждого артефакта — с source_commit."""
        res = git("ls-tree", "-r", self.commit)
        self.assertEqual(res.returncode, 0, f"нет коммита {self.commit}: нужна полная история")
        tree = {}
        for line in res.stdout.decode().splitlines():
            meta, path = line.split("\t", 1)
            mode, _, blob = meta.split()
            tree[path] = (mode, blob)
        batch = subprocess.run(
            ["git", "cat-file", "--batch"], cwd=ROOT, capture_output=True,
            input="".join(f"{self.commit}:{p}\n" for p in self.by_path).encode(),
        ).stdout
        pos = 0
        for path, art in self.by_path.items():
            with self.subTest(path=path):
                self.assertIn(path, tree)
                self.assertEqual(tree[path], ("100644", art["git_blob"]))
                header_end = batch.index(b"\n", pos)
                size = int(batch[pos:header_end].split()[2])
                data = batch[header_end + 1: header_end + 1 + size]
                pos = header_end + 1 + size + 1
                self.assertEqual(hashlib.sha256(data).hexdigest(), art["sha256"])
                self.assertEqual(len(data), art["bytes"])
                self.assertTrue(path.isascii())
                self.assertNotIn(Path(path).name, CLIENT_INSTRUCTIONS)

    def test_gate_map_in_transfer(self):
        self.assertEqual(self.by_path[GATE_MAP]["transfer_card"], "BL-188")
        gates = json.loads(git("show", f"{self.commit}:{GATE_MAP}").stdout)
        self.assertTrue(gates["runtime_path"].startswith(self.m["transfer"]["target_dir"]))
        for path, digest in gates["sources"].items():
            with self.subTest(source=path):
                self.assertEqual(self.by_path[path]["sha256"], digest)

    def test_rule_5_is_7a(self):
        rules = self.m["sync_policy"]["rules"]
        self.assertIn("7а", rules[4])
        self.assertIn("ssot-stage1-link-map.json", rules[4])
        self.assertIn("ACCESS_GAP", rules[4])

    def test_markdown_view(self):
        text = read(MANIFEST_MD)
        self.assertIn(self.commit[:8], text)
        self.assertIn("0.2", text)


class LinkMapTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m = json.loads(read(MANIFEST))
        cls.lm = json.loads(read(LINK_MAP))
        cls.paths = {a["path"] for a in cls.m["artifacts"]}

    def test_header(self):
        self.assertEqual(self.lm["source_commit"], self.m["source_commit"])
        self.assertEqual(self.lm["target_dir"], self.m["transfer"]["target_dir"])
        self.assertEqual(self.lm["manifest"], MANIFEST.relative_to(ROOT).as_posix())
        self.assertEqual(self.m["transfer"]["link_map"], LINK_MAP.relative_to(ROOT).as_posix())
        self.assertIn("7а", self.lm["decision"])

    def test_links(self):
        commit = self.lm["source_commit"]
        for link in self.lm["links"]:
            with self.subTest(link=f'{link["from"]}:{link["line"]}'):
                self.assertEqual(link["class"], "outside")
                self.assertIn(link["from"], self.paths)
                self.assertNotIn(link["target"], self.paths)
                self.assertIn(f"/{commit}/", link["permalink"])

    def test_summary_recount(self):
        s, links, targets = self.lm["summary"], self.lm["links"], self.lm["targets"]
        self.assertEqual(s["links"]["outside"], len(links))
        self.assertEqual(s["files_with_outside_links"], len({link["from"] for link in links}))
        self.assertEqual(s["targets"]["outside"], len(targets))
        self.assertEqual(sum(t["occurrences"] for t in targets), len(links))
        self.assertEqual({t["target"] for t in targets}, {link["target"] for link in links})
        candidates = [t for t in targets if t["next_transfer_candidate"]]
        self.assertEqual(s["next_transfer_candidates"], len(candidates))
        for t in candidates:
            with self.subTest(candidate=t["target"]):
                self.assertTrue(t["normative"])
                self.assertTrue(t["target"].startswith(tuple(self.lm["normative_roots"])))


class DryRunTest(unittest.TestCase):
    def test_log(self):
        text = read(DRY_RUN)
        m = json.loads(read(MANIFEST))
        self.assertIn(f"манифест {m['version']}: {ARTIFACTS} артефактов, source_commit={m['source_commit']}", text)
        for needle in (
            f"сверка sha256: совпало {ARTIFACTS} из {ARTIFACTS}",
            "лишних: 0; недостающих: 0",
            ": поймана",
            "не совпало с передачей: 0; runtime_path в каталоге копии: True",
            "всего: {'почта': 0, 'телефон': 0, 'секрет': 0, 'внутренний контур': 0}",
            "файлов с CRLF: 0",
            "test_map_matches_the_layer (tests.test_ide_layer.GateMap.test_map_matches_the_layer) ... ok",
            "runtime smoke test passed",
            "все внутри ssot/: True",
        ):
            with self.subTest(needle=needle):
                self.assertIn(needle, text)
        self.assertTrue(text.rstrip().endswith("ИТОГ: OK"))


class RfcTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = read(RFC)
        cls.part = section(cls.text, SECTION_12)

    def test_subsections(self):
        numbers = [int(n) for n in re.findall(r"(?m)^### 12\.(\d+)\. ", self.part)]
        self.assertGreaterEqual(len(numbers), 10)
        self.assertEqual(numbers, list(range(1, len(numbers) + 1)))
        for name in ("Цель", "SSOT", "Предусловия", "Решение на согласование", "Раскладка",
                     "Функциональные требования", "Нефункциональные требования",
                     "Граничные кейсы", "Обоснованные решения", "Готово, когда", "Не входит"):
            with self.subTest(section=name):
                self.assertRegex(self.part, rf"(?m)^### 12\.\d+\. {name}$")

    def test_edge_cases(self):
        cases = re.findall(r"(?m)^\| (\d+) \|", section(self.part, "### 12.8. Граничные кейсы"))
        self.assertGreaterEqual(len(cases), 20)
        self.assertEqual([int(n) for n in cases], list(range(1, len(cases) + 1)))

    def test_publication_decision(self):
        decision = section(self.part, "### 12.4. Решение на согласование")
        self.assertRegex(decision, r"(?m)^\| Р-RT-22 \|")
        for variant in ("А", "Б", "В", "Г"):
            with self.subTest(variant=variant):
                self.assertRegex(decision, rf"(?m)^\| \*\*{variant}\.\*\*")
        for needle in ("П-0", "П-1", "П-2", "PRIVATE", "PUBLIC", "ai-governance"):
            with self.subTest(needle=needle):
                self.assertIn(needle, self.part)

    def test_pointers(self):
        digest = hashlib.sha256(MANIFEST.read_bytes()).hexdigest()
        self.assertIn(digest, self.part, "sha256 файла манифеста в разделе 12 устарел")
        self.assertIn(OWNER_COMMENT, self.part)
        self.assertRegex(self.part, RUNTIME_ISSUE)
        self.assertIn("не снят", self.part)
        self.assertIn(PR, self.text)


class BacklogTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.backlog = read(BACKLOG)
        cls.model = read(MODEL)
        cls.repository = read(REPOSITORY)
        cls.issue = RUNTIME_ISSUE.search(section(read(RFC), SECTION_12)).group(0)

    def test_transfer_cards(self):
        for code in CARDS:
            with self.subTest(card=code):
                line = row(self.backlog, code)
                self.assertIn("| DONE |", line)
                body = card(self.model, code)
                self.assertIn("**Статус.** `DONE`", body)
                for evidence in (self.issue, RUNTIME_PR, PUBLICATION_DECISION):
                    self.assertIn(evidence, line)
                    self.assertIn(evidence, body)

    def test_new_cards(self):
        self.assertIn("| DONE |", row(self.backlog, "BL-246"))
        self.assertIn(PR, row(self.backlog, "BL-246"))
        self.assertIn("**Статус.** `DONE`", card(self.repository, "BL-246"))
        link_card = row(self.backlog, "BL-190")
        self.assertIn(RUNTIME_PR, link_card)
        self.assertNotIn("| deferred (triggered) |", link_card)
        self.assertTrue(row(self.backlog, "BL-247"))
        for code in ("BL-246", "BL-247"):
            body = card(self.repository, code)
            for field in ("**Статус.**", "**Почему.**", "**Что меняется.**", "**Источники.**",
                          "**Зависит от.**", "**Решение владельца.**", "**Готово, когда.**"):
                with self.subTest(card=code, field=field):
                    self.assertIn(field, body)

    def test_chain(self):
        chain = self.backlog.split("**Движение по цепочке (#506, M2).**", 1)[1].split("\n\n", 1)[0]
        for needle in ("Предыдущий шаг", "Текущий шаг", "Открывается", "BL-244", "BL-192",
                       "BL-246", "BL-247", "BL-185", "BL-190", "Р-RT-22",
                       PR, OWNER_COMMENT, self.issue, RUNTIME_PR):
            with self.subTest(needle=needle):
                self.assertIn(needle, chain)

    def test_no_placeholder(self):
        for path in (RFC, BACKLOG, MODEL, REPOSITORY):
            with self.subTest(path=path.name):
                self.assertNotIn(PLACEHOLDER, read(path))


if __name__ == "__main__":
    sys.exit(0 if unittest.main(exit=False, verbosity=1).result.wasSuccessful() else 1)
