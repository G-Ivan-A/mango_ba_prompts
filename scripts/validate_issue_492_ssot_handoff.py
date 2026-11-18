#!/usr/bin/env python3
"""Issue #492: аудит зависимостей от runtime и манифест передачи SSOT этапа 1.

Проверяет без LLM, без сети и без клона runtime:

* ФТ-1, ФТ-2: выходы аудита и классификации на месте, сводки сходятся
  с таблицами, у каждой ссылки класса (б) есть решение;
* ФТ-3: манифест ``docs/contracts/ssot-stage1-handoff-manifest.json`` —
  sha256, размер и git-блоб каждого артефакта равны байтам файла на
  ``source_commit``; нет путей с клиентскими данными (``runs/``, ``kb/``,
  ``inputs/``, ``attachments/``); 24 контракта AIN; статусы цепочки
  сходятся со сводкой; MD-рендер совпадает с JSON;
* ФТ-4: каждая цель (б), которой нет в runtime, и заглушка З-2 закрыты
  карточкой BL-184…BL-190, карточка есть в модели бэклога и в таблице
  ``pr-ops/BACKLOG.md``;
* тексты промптов не менялись: ``prompts/`` совпадает с базой ``main``.

Дрейф артефактов относительно рабочего дерева — информация, а не ошибка:
манифест закреплён на ``source_commit``, обновление — новой передачей.
"""
import hashlib
import json
import os
import re
import subprocess
import sys
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXP = ROOT / "experiments/issue_492"
sys.path.insert(0, str(EXP))

import build_ssot_manifest  # noqa: E402

MANIFEST_JSON = ROOT / "docs/contracts/ssot-stage1-handoff-manifest.json"
MANIFEST_MD = ROOT / "docs/contracts/ssot-stage1-handoff-manifest.md"
DEPS_JSON = EXP / "runtime-deps.json"
LINKS_JSON = EXP / "prompt-links.json"
AUDIT = ROOT / "docs/audit/2026-11-18-runtime-dependencies-ssot-handoff.md"
BACKLOG = ROOT / "pr-ops/BACKLOG.md"
MODEL = ROOT / "pr-ops/backlog-ba-model.md"

CARDS = [f"BL-{n}" for n in range(184, 191)]
TRANSFER_CARDS = {"BL-185", "BL-186", "BL-187", "BL-188"}
CHAIN = {"действует", "архив", "заменён"}
SHA = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load(path: Path) -> dict:
    return json.loads(read(path))


def git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True)


def blobs_at(commit: str, paths: list[str]) -> dict[str, bytes | None]:
    """Байты файлов на коммите одним ``git cat-file --batch``."""
    request = "".join(f"{commit}:{p}\n" for p in paths).encode()
    out = subprocess.run(["git", "cat-file", "--batch"], cwd=ROOT, input=request,
                         capture_output=True, check=True).stdout
    result, pos = {}, 0
    for path in paths:
        end = out.index(b"\n", pos)
        header = out[pos:end].split()
        pos = end + 1
        if header[-1] == b"missing":
            result[path] = None
            continue
        size = int(header[2])
        result[path] = out[pos:pos + size]
        pos += size + 1
    return result


class OutputsTest(unittest.TestCase):
    """ФТ-1 и ФТ-2: выходы скриптов и журналы на месте и согласованы."""

    def test_outputs_and_logs_exist(self):
        for name in ("audit_runtime_deps.py", "runtime-deps.json", "runtime-deps.md",
                     "audit-runtime-deps.log", "classify_prompt_links.py", "prompt-links.json",
                     "prompt-links.md", "classify-prompt-links.log", "build_ssot_manifest.py",
                     "build-ssot-manifest.log"):
            self.assertTrue((EXP / name).is_file(), f"нет experiments/issue_492/{name}")
        self.assertTrue(MANIFEST_JSON.is_file() and MANIFEST_MD.is_file())
        self.assertTrue(AUDIT.is_file(), "нет итогового аудита #492")

    def test_dependency_audit_summary(self):
        deps = load(DEPS_JSON)
        s = deps["summary"]
        self.assertEqual(s["issue"], 492)
        self.assertEqual(len(deps["rows"]), s["table_rows"])
        self.assertEqual(len(deps["paths"]), s["runtime_paths"])
        statuses = Counter(p["status"] for p in deps["paths"])
        self.assertLessEqual(set(statuses), {"защищённый", "защищённый (двойной)", "свободный"})
        for path in deps["paths"]:
            self.assertTrue(path["consumer"] or path["status"] == "свободный",
                            f"{path['runtime_path']}: защищённый путь без потребителя")

    def test_every_link_is_classified(self):
        links = load(LINKS_JSON)
        s = links["summary"]
        occ = links["occurrences"]
        self.assertEqual(len(occ), s["occurrences"])
        self.assertEqual(dict(Counter(o["class"] for o in occ)), s["by_class"])
        rules = {r["id"]: r["class"] for r in links["rules"]}
        for o in occ:
            self.assertIn(o["class"], ("а", "б"))
            self.assertEqual(rules.get(o["rule"]), o["class"],
                             f"{o['prompt']}:{o['line']}: правило {o['rule']} не задаёт класс {o['class']}")
        for t in links["targets"]:
            self.assertTrue(t["decision"], f"{t['target']}: нет решения")
            if "б" in t["classes"]:
                self.assertTrue(t["normative"], f"{t['target']}: цель (б) не помечена нормативной")


class ManifestTest(unittest.TestCase):
    """ФТ-3: манифест закреплён на коммите-источнике и без клиентских данных."""

    @classmethod
    def setUpClass(cls):
        cls.m = load(MANIFEST_JSON)
        cls.commit = cls.m["source_commit"]
        cls.paths = [a["path"] for a in cls.m["artifacts"]]

    def test_header(self):
        m = self.m
        self.assertEqual(m["issue"], 492)
        self.assertEqual(m["source_repository"], "G-Ivan-A/mango_ba_prompts")
        self.assertEqual(m["target_repository"], "G-Ivan-A/mango-ba-ai-runtime")
        for key in ("source_commit", "runtime_registry_sha", "runtime_main_observed"):
            self.assertRegex(m[key], SHA, key)
        self.assertIs(m["runtime_changed"], False)
        self.assertTrue(m["sync_policy"]["rules"], "нет политики синхронизации")
        self.assertTrue(m["evolution"], "нет цепочки эволюции")

    def test_source_commit_is_available(self):
        res = git("cat-file", "-e", f"{self.commit}^{{commit}}")
        self.assertEqual(res.returncode, 0,
                         f"коммит {self.commit[:8]} недоступен: нужен полный клон (fetch-depth: 0)")

    def test_hashes_match_source_commit(self):
        data = blobs_at(self.commit, self.paths)
        for a in self.m["artifacts"]:
            raw = data[a["path"]]
            self.assertIsNotNone(raw, f"{a['path']}: нет на {self.commit[:8]}")
            self.assertRegex(a["sha256"], SHA256)
            self.assertEqual(hashlib.sha256(raw).hexdigest(), a["sha256"], a["path"])
            self.assertEqual(len(raw), a["bytes"], a["path"])
            blob = hashlib.sha1(b"blob %d\0" % len(raw) + raw).hexdigest()
            self.assertEqual(blob, a["git_blob"], a["path"])
            self.assertEqual(a["source_commit"], self.commit, a["path"])

    def test_no_client_data(self):
        self.assertEqual(len(self.paths), len(set(self.paths)), "дубли путей")
        for path in self.paths:
            self.assertFalse(path.startswith(build_ssot_manifest.FORBIDDEN_PREFIXES),
                             f"{path}: клиентские данные в манифесте запрещены")
            self.assertFalse(path.startswith("/") or ".." in Path(path).parts, path)
        for a in self.m["artifacts"]:
            self.assertFalse({"content", "text", "body"} & set(a), f"{a['path']}: содержимое в манифесте")

    def test_contracts(self):
        ids = [c["id"] for c in self.m["contracts"]]
        self.assertEqual(ids, [f"AIN-{n:02d}" for n in range(1, 25)])
        by_path = {a["path"]: a for a in self.m["artifacts"]}
        for c in self.m["contracts"]:
            self.assertIn(c["prompt"], by_path, f"{c['id']}: промпт не в манифесте")
            self.assertEqual(c["prompt_sha256"], by_path[c["prompt"]]["sha256"], c["id"])
            self.assertRegex(c["instruction_sha256"], SHA256, c["id"])

    def test_summary_and_chain(self):
        s = self.m["summary"]
        arts = self.m["artifacts"]
        self.assertEqual(s["artifacts"], len(arts))
        self.assertEqual(s["contracts"], len(self.m["contracts"]))
        self.assertEqual(s["in_runtime"], sum(1 for a in arts if a["in_runtime"]))
        self.assertEqual(s["chain_status"], dict(Counter(a["chain_status"] for a in arts)))
        self.assertEqual(s["transfer_cards"], dict(Counter(a["transfer_card"] for a in arts)))
        for a in arts:
            self.assertIn(a["chain_status"], CHAIN, a["path"])
            self.assertIn(a["transfer_card"], TRANSFER_CARDS, a["path"])
        groups = {g["id"]: g["count"] for g in self.m["groups"]}
        self.assertEqual(groups, dict(Counter(a["group"] for a in arts)))

    def test_markdown_is_rendered_from_json(self):
        self.assertTrue(read(MANIFEST_MD) == build_ssot_manifest.render(self.m),
                         "MD манифеста устарел: перезапустите experiments/issue_492/build_ssot_manifest.py")

    def test_drift_is_informational(self):
        drift = []
        for a in self.m["artifacts"]:
            path = ROOT / a["path"]
            if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest() != a["sha256"]:
                drift.append(a["path"])
        if drift and os.environ.get("ISSUE_492_VERBOSE"):
            print(f"\nдрейф от source_commit (информация, не ошибка): {len(drift)}", *drift, sep="\n  ")


class BacklogTest(unittest.TestCase):
    """ФТ-4: каждый пробел закрыт карточкой, карточки и статусы — в бэклоге."""

    @classmethod
    def setUpClass(cls):
        cls.links = load(LINKS_JSON)
        cls.model = read(MODEL)
        cls.backlog = read(BACKLOG)

    def test_cards_exist_in_model_and_sprint_table(self):
        for card in CARDS:
            self.assertTrue(re.search(rf"(?m)^### {card}\. ", self.model), f"{card}: нет карточки в модели бэклога")
            self.assertTrue(re.search(rf"(?m)^\| {card} \| \[", self.backlog), f"{card}: нет строки в BACKLOG.md")
        self.assertTrue("Движение по цепочке (#492)" in self.backlog, "нет движения по цепочке")

    def test_missing_normative_targets_have_transfer_cards(self):
        missing = [t for t in self.links["targets"] if t["normative"] and not t["runtime"]]
        self.assertEqual(len(missing), 24)
        for t in missing:
            self.assertIn(t["card"], TRANSFER_CARDS, f"{t['target']}: нет карточки переноса")
        manifest_paths = {a["path"] for a in load(MANIFEST_JSON)["artifacts"]}
        for t in missing:
            self.assertIn(t["target"], manifest_paths, f"{t['target']}: цель (б) не в манифесте")

    def test_stubs_have_cards(self):
        for stub in self.links["stubs"]:
            self.assertIn(stub["card"], CARDS, f"{stub['id']}: нет карточки")
        self.assertEqual([s["id"] for s in self.links["stubs"]], ["З-2"])

    def test_card_registry_matches_backlog(self):
        for card, title in self.links["cards"].items():
            self.assertTrue(f"### {card}. {title}" in self.model, f"{card}: заголовок карточки расходится")


class PromptsUnchangedTest(unittest.TestCase):
    """НФТ: тексты промптов в этой задаче не редактируются.

    Проверяются коммиты задачи (``issue-492`` в сообщении), а не разница с
    ``main``: последующие задачи вправе менять промпты, и проверка #492 не
    должна им мешать.
    """

    def test_issue_commits_do_not_touch_prompts(self):
        res = git("log", "--no-merges", "--format=%h %s", "--grep=issue-492", "--", "prompts/")
        self.assertEqual(res.returncode, 0, res.stderr.decode())
        self.assertEqual(res.stdout.decode().strip(), "", "коммиты #492 меняют тексты промптов")


if __name__ == "__main__":
    unittest.main(verbosity=1)
