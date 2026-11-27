#!/usr/bin/env python3
"""Issue #495: чистота исполнимых промптов — сторожа стандарта и их мутации.

Проверяет без LLM и без сети (стандарт ``standards/bcreq-prompt-purity.md``):

* ЧП-1…ЧП-3, ЧП-5: аудитор ``scripts/audit_prompt_purity.py`` на рабочем
  дереве — 0 нарушений классов а/б/в во всём контуре (промпты, черновики,
  системный трек, стандарты классов, ССОТ A-IN, данные сайта);
* мутации: в копию контура во временном каталоге вносится одно нарушение —
  аудитор обязан его найти (URL приватного репозитория в промпте и в данных
  сайта, голое имя репозитория, относительная ссылка, ссылка на runtime не по
  закреплённому SHA, голый путь спицы A-SPOKE-PATH (и его исключения: frontmatter,
  архив, пути runtime), кейс-токены CT-01…CT-09, балласт BP-01…BP-13);
* ЧП-4: сборщики ССОТ в режиме ``--check`` и реестр обратимых правок
  ``experiments/issue_495/prompt-edits.json`` актуальны — ручная правка
  сгенерированного файла ловится (мутация: правка черновика роняет ``--check``);
* ЧП-6: версия сайта — patch-серия 2.9.x, не ниже 2.9.0, одинакова в
  генераторе, данных и разметке; мутации 2.10.0 и 2.8.9 падают;
* реестр runtime: ссылки на runtime — только по SHA из ``runtime_sha``;
  справочники И-11/И-12 и задачи РТ-8/РТ-9 заведены, заглушка З-5 активна;
* бэклог: цепочка BL-240 → BL-241 → BL-242 → BL-232 в ``pr-ops/BACKLOG.md``;
* карта базы: группы G принимают только копии нарушений ручных исходников —
  маркер одного сборщика, пустое окно и окно из архива копией не считаются.
"""
import contextlib
import hashlib
import importlib.util
import io
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import audit_prompt_purity as audit  # noqa: E402

POLICY = "standards/bcreq-prompt-purity.json"
REGISTRY = "standards/bcreq-runtime-references.md"
PROMPT = "prompts/bcreq-fr-documentation-stepwise.md"
SITE = "site/data/a-in-kit.json"
ARCHIVE = "prompts/archive/fr-documentation-stepwise.md"
# Кандидат релиза после интеграции #496; patch-серия — только 2.9.x.
MINIMUM = (2, 9, 2)
SERIES = (2, 9)


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def load_module(rel, name):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


PURITY = load_module("scripts/prompt_purity.py", "prompt_purity_495")


def version_errors(version, minimum=MINIMUM, series=SERIES):
    """Нарушения ЧП-6 для строки версии; пусто — версия допустима."""
    match = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", version or "")
    if not match:
        return [f"версия {version!r} не в формате X.Y.Z"]
    parts = tuple(map(int, match.groups()))
    errors = []
    if parts[:2] != series:
        errors.append(f"версия {version} вне patch-серии {series[0]}.{series[1]}.x")
    if parts < minimum:
        errors.append(f"версия {version} ниже минимальной {'.'.join(map(str, minimum))}")
    return errors


class Sandbox:
    """Минимальная копия контура: политика, реестр runtime и выбранные файлы."""

    def __init__(self, files):
        self.dir = tempfile.TemporaryDirectory(prefix="i495-")
        self.root = Path(self.dir.name)
        for rel in [POLICY, REGISTRY, *files]:
            target = self.root / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / rel, target)

    def write(self, rel, text):
        (self.root / rel).write_text(text, encoding="utf-8")

    def run(self):
        return audit.Auditor(self.root).run()

    def close(self):
        self.dir.cleanup()


class RepoAuditTest(unittest.TestCase):
    """ЧП-1…ЧП-3, ЧП-5: рабочее дерево чистое."""

    def test_repo_has_zero_findings(self):
        auditor = audit.Auditor(ROOT)
        findings = auditor.run()
        listing = "\n".join(f"{f['file']}:{f['line']} {f['class']} {f['rule']} {f['match']}" for f in findings[:20])
        self.assertEqual(findings, [], f"нарушений: {len(findings)}\n{listing}")
        kinds = set(auditor.files.values())
        self.assertEqual(kinds, {"prompt_texts", "archive_texts", "ssot_texts", "repo_docs_in_prompts", "site_data"})
        # Контур не пустой: промпты, 39 стандартов классов, черновики, данные сайта.
        prompts = [f for f, k in auditor.files.items() if k == "prompt_texts"]
        self.assertGreaterEqual(len([f for f in prompts if f.startswith("standards/bcreq-manual-classes/")]), 39)
        self.assertTrue(any(f.startswith("prompts/drafts/a-in/") for f in prompts))
        self.assertTrue(any(f.startswith("prompts/drafts/system/") for f in prompts))
        self.assertIn("site/data/prompts.json", auditor.files)

    def test_no_private_url_in_site_data_anywhere(self):
        # Сильнее аудитора: ни одной строки с URL спицы в любом JSON сайта.
        rx = re.compile(audit.load_policy(ROOT / POLICY)["links"]["private_link_regex"])
        for path in sorted((ROOT / "site/data").glob("*.json")):
            self.assertIsNone(rx.search(path.read_text(encoding="utf-8")), path.name)

    def test_projection_is_idempotent_on_prompts(self):
        for path in sorted((ROOT / "prompts").glob("*.md")):
            text = path.read_text(encoding="utf-8")
            self.assertEqual(PURITY.project(text), PURITY.project(PURITY.project(text)), path.name)


class MutationTest(unittest.TestCase):
    """Каждая мутация обязана дать нарушение нужного правила."""

    def setUp(self):
        self.box = Sandbox([PROMPT, SITE])
        self.sha = audit.runtime_sha(ROOT)

    def tearDown(self):
        self.box.close()

    def rules(self):
        return {(f["class"], f["rule"], f["file"]) for f in self.box.run()}

    def mutate_prompt(self, line):
        text = read(PROMPT)
        anchor = text.index("\n## ") + 1
        self.box.write(PROMPT, text[:anchor] + line + "\n\n" + text[anchor:])

    def test_baseline_clean(self):
        self.assertEqual(self.box.run(), [])

    def test_private_url_in_prompt(self):
        self.mutate_prompt("См. [контракт](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/x.md).")
        self.assertIn(("a", "A-PRIVATE", PROMPT), self.rules())

    def test_bare_private_name_in_prompt(self):
        self.mutate_prompt("Источник — репозиторий mango_ba_prompts.")
        self.assertIn(("a", "A-PRIVATE-NAME", PROMPT), self.rules())

    def test_relative_link_in_prompt(self):
        self.mutate_prompt("См. [стандарт](../standards/prompt-standard.md).")
        self.assertIn(("a", "A-RELATIVE", PROMPT), self.rules())

    def test_unpinned_runtime_link(self):
        self.mutate_prompt("См. https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/main/golden/x.yaml")
        self.assertIn(("a", "A-RUNTIME-UNPINNED", PROMPT), self.rules())

    def test_pinned_runtime_link_is_allowed(self):
        self.mutate_prompt(f"См. https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/{self.sha}/golden/x.yaml")
        self.assertEqual(self.box.run(), [])

    def test_case_tokens_in_prompt(self):
        for token, rule in [("amoCRM", "CT-01"), ("API-привязка", "CT-02"), ("коннектор", "CT-03"), ("ВАТС", "CT-04"), ("ЛК", "CT-05"),
                            ("HDE", "CT-06"), ("Битрикс24", "CT-07"), ("задача 1075", "CT-08")]:
            with self.subTest(token=token):
                self.mutate_prompt(f"Проверь интеграцию: {token} и смежные данные.")
                self.assertIn(("b", rule, PROMPT), self.rules())

    def test_profile_mapping_vs_minimal_set(self):
        # CT-09 — соответствие «профиль → словари»; универсальный минимальный набор — не кейс.
        for line in ["Словари профиля: оператор связи — D9.", "Словари профиля КЦ: D6, D11."]:
            with self.subTest(line=line):
                self.mutate_prompt(line)
                self.assertIn(("b", "CT-09", PROMPT), self.rules())
        self.mutate_prompt("Возьми минимальный набор D1, D2, D11.")
        self.assertEqual(self.box.run(), [])

    def test_ballast_in_prompt(self):
        for line, rule in [("<!-- Experimental: for BL-156 -->", "BP-01"), ("Решение принято в #427.", "BP-02"),
                           ("См. issue про шаг.", "BP-03"), ("Добавлено по BL-123.", "BP-04"),
                           ("Правка из PR #12.", "BP-05"), ("Редакция по тесту.", "BP-06"),
                           ("Блок собран сборщиком.", "BP-07"), ("Experimental: правило шага.", "BP-08"),
                           ("Правило действует до ADR.", "BP-09"), ("Не внесены правила шага.", "BP-10"),
                           ("История изменений правила — ниже.", "BP-11"), ("Урок из Golden Set (ревизия 3).", "BP-12"),
                           ("Приоритет у принятого RFC-AIN-001.", "BP-13"), ("Решение — ADR-RT-002.", "BP-13"),
                           ("Стандарт промптов (ADR-001).", "BP-13"), ("Приоритет у RFC-A-IN-001.", "BP-13"),
                           # Роль Б, раунд 3, замечание 8: строчная запись и не-ASCII дефисы.
                           ("Приоритет у rfc-ain-001.", "BP-13"), ("Приоритет у RFC\u2011AIN\u2011001.", "BP-13"),
                           ("Решение — ADR\u2010RT\u2010002.", "BP-13"), ("Решение — Adr\u2013001.", "BP-13"),
                           # Роль Б, раунд 4, замечания 2 и 3: длинное тире, мягкий перенос,
                           # публичный RFC через дефис — тоже ID (пишется «RFC 2119»).
                           ("Приоритет у RFC\u2014AIN\u2014001.", "BP-13"),
                           ("Приоритет у RFC\u00adAIN\u00ad001.", "BP-13"), ("Ключевые слова — RFC-2119.", "BP-13"),
                           # Роль Б, раунд 5, замечание 3: тире вплотную перед ID, полноширинный
                           # дефис, буквенно-цифровой сегмент.
                           ("Так решено—ADR-001.", "BP-13"), ("Приоритет у RFC\uff0dAIN1\uff0d001.", "BP-13"),
                           ("-ADR-001", "BP-13"), ("(\u2011ADR-001)", "BP-13"), (" -RFC-AIN-001", "BP-13"),
                           ("RFC\u2015AIN\u2015001", "BP-13"), ("RFC\ufe63AIN\ufe63001", "BP-13")]:
            with self.subTest(line=line):
                self.mutate_prompt(line)
                self.assertIn(("c", rule, PROMPT), self.rules())
        # Слово без номера («RFC-шаблон», «адрес») — не ID: BP-13 не срабатывает.
        self.mutate_prompt("Сохрани адрес и RFC-шаблон ответа; ключевые слова — по RFC 2119; см. PRE-RFC-AIN-001.")
        self.assertNotIn(("c", "BP-13", PROMPT), self.rules())

    def test_spoke_path_in_prompt(self):
        # ЧП-1, A-SPOKE-PATH: снятая ссылка не остаётся голым путём или названием файла спицы.
        for line in ["Правила — в standards/bcreq-sections/NN-*.md.", "Журнал — `pr-ops/session-digests.md`.",
                     "Профили — в стандарте композиции §4.", "Полный текст — README §2.",
                     "Каталог docs/taxonomy и runtime taxonomy/products.yaml.", "Сборка: scripts/build_x.py."]:
            with self.subTest(line=line):
                self.mutate_prompt(line)
                self.assertIn(("a", "A-SPOKE-PATH", PROMPT), self.rules())
        # Пути runtime (docs/kb, docs/guides) — не спица; правило не срабатывает.
        self.mutate_prompt("Справочник runtime — docs/kb/products.md и docs/guides.")
        self.assertEqual(self.box.run(), [])

    def test_spoke_path_outside_live_body_is_not_checked(self):
        # Frontmatter промпта — метаданные карточки (IG-3, IG-9).
        text = read(PROMPT)
        self.box.write(PROMPT, text.replace("---\n", "---\nsource: standards/bcreq-sections/README.md\n", 1))
        self.assertEqual(self.box.run(), [])
        # Архив — история (IG-9): тот же путь в архивном промпте не нарушение.
        box = Sandbox([ARCHIVE])
        try:
            box.write(ARCHIVE, read(ARCHIVE) + "\nПравила — в standards/bcreq-sections/NN-*.md.\n")
            self.assertNotIn("A-SPOKE-PATH", {f["rule"] for f in box.run()})
        finally:
            box.close()

    def test_spoke_path_in_site_prompt_body(self):
        data = json.loads(read(SITE))
        data["steps"][0]["prompt"] += "\nПравила — в standards/bcreq-sections/README.md."
        self.box.write(SITE, json.dumps(data, ensure_ascii=False))
        self.assertIn(("a", "A-SPOKE-PATH", SITE), self.rules())

    def test_private_url_in_site_data(self):
        data = json.loads(read(SITE))
        data["steps"][0]["sourceUrl"] = "https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/" + PROMPT
        self.box.write(SITE, json.dumps(data, ensure_ascii=False))
        self.assertIn(("a", "A-PRIVATE", SITE), self.rules())

    def test_case_token_and_comment_in_site_prompt_body(self):
        data = json.loads(read(SITE))
        data["steps"][0]["prompt"] += "\n<!-- маркер -->\nСверь коннектор с amoCRM."
        self.box.write(SITE, json.dumps(data, ensure_ascii=False))
        found = self.rules()
        for rule in [("c", "BP-01", SITE), ("b", "CT-03", SITE), ("b", "CT-01", SITE)]:
            self.assertIn(rule, found)


class OverCleaningTest(unittest.TestCase):
    """Защита от сверхчистки (комментарий 2 владельца, раздел 3; стандарт, раздел 4).

    Защищённые маркеры (ID правил, ``[ТРЕБУЕТСЯ УТОЧНЕНИЕ]``, ACCESS_GAP,
    «Состояние BCREQ», «Итог шага», «На согласование БА», receipt, стоп-краны…)
    в каждом промпте и черновике — не меньше, чем в базе (снимок
    ``experiments/issue_495/audit/protected-baseline.json``).
    """

    SNAPSHOT = "experiments/issue_495/audit/protected-baseline.json"

    @classmethod
    def setUpClass(cls):
        cls.policy = audit.load_policy(ROOT / POLICY)["protected_markers"]
        rel, key = cls.policy["exempt_ids_from"].split("#")
        cls.exempt = sorted(json.loads(read(rel))[key])
        cls.base = json.loads(read(cls.SNAPSHOT))
        cls.debugging = load_module("experiments/issue_509/prompt_changes.py", "prompt_followup_495")

    def drops(self, texts):
        out = []
        for rel, before in self.base["files"].items():
            if rel not in texts:
                out.append(f"{rel}: файл удалён")
                continue
            after = PURITY.protected_counts(texts[rel], self.policy["patterns"], self.exempt)
            out += [f"{rel}: {kind} {n} → {after[kind]}" for kind, n in before.items() if after[kind] < n]
        return out

    def current(self):
        return {rel: self.debugging.revert_followup(rel, read(rel))
                for rel in self.base["files"] if (ROOT / rel).exists()}

    def test_no_protected_marker_lost(self):
        self.assertEqual(self.base["exempt_ids"], self.exempt, "снимок снят с другим перечнем исключений")
        self.assertGreaterEqual(len(self.base["files"]), 60)
        self.assertEqual(self.drops(self.current()), [])

    def test_exempt_ids_keep_their_home(self):
        # Исключённые правила не исчезают: ID и причина — в манифесте, текст — в базовом стандарте.
        reasons = json.loads(read(self.policy["exempt_ids_from"].split("#")[0]))["excluded_base_rules"]
        standard = read("standards/bcreq-prompt-base-standard.md")
        for rid in self.exempt:
            self.assertTrue(reasons[rid].strip(), rid)
            self.assertRegex(standard, rf"\b{rid}\b", rid)

    def test_mutations_fail(self):
        texts = self.current()
        rel = "prompts/drafts/bcreq-fr-documentation-stepwise.md"
        for marker in ["[ТРЕБУЕТСЯ УТОЧНЕНИЕ]", "Итог шага", "АД-8", "ACCESS_GAP"]:
            with self.subTest(marker=marker):
                self.assertIn(marker, texts[rel])
                mutated = dict(texts, **{rel: texts[rel].replace(marker, "…")})
                self.assertTrue(set(self.drops(mutated)) - set(self.drops(texts)), marker)
        self.assertTrue(self.drops({k: v for k, v in texts.items() if k != rel}))


class VersionTest(unittest.TestCase):
    """ЧП-6: только 2.9.x, начиная с кандидата 2.9.2."""

    def test_site_version_consistent_and_allowed(self):
        version = json.loads(read("site/data/prompts.json"))["siteVersion"]["version"]
        self.assertEqual(version_errors(version), [])
        self.assertEqual(json.loads(read("site/data/stats.json"))["siteVersion"]["version"], version)
        self.assertIn(f'version: "{version}"', read("scripts/generate-pages-data.mjs"))
        html = read("site/index.html")
        self.assertIn(f">v{version}<", html)
        self.assertEqual(set(re.findall(r">v(\d+\.\d+\.\d+)<", html)), {version})
        self.assertIn(f"Версия сайта {version}", read("CHANGELOG.md"))

    def test_version_mutations_fail(self):
        for bad in ["2.10.0", "2.8.9", "2.9.0", "2.9.1", "3.0.0", "2.9", "v2.9.2"]:
            with self.subTest(version=bad):
                self.assertNotEqual(version_errors(bad), [])
        for good in ["2.9.2", "2.9.17"]:
            with self.subTest(version=good):
                self.assertEqual(version_errors(good), [])


class SsotTest(unittest.TestCase):
    """ЧП-4: сгенерированное совпадает с выходом сборщиков."""

    def check(self, *cmd):
        proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, f"{' '.join(cmd)}\n{proc.stdout}\n{proc.stderr}")

    def test_builders_check(self):
        for script in ["scripts/bcreq_handoff.py", "scripts/build_bcreq_a_in.py",
                       "scripts/build_bcreq_step_prompts.py", "scripts/build_bcreq_system_track.py"]:
            with self.subTest(script=script):
                self.check(sys.executable, script, "--check")

    def test_hand_edited_draft_fails_check(self):
        # Мутация ЧП-4: ручная правка черновика (в обход ССОТ) роняет --check сборщика.
        builder = load_module("scripts/build_bcreq_step_prompts.py", "build_steps_495")
        target = sorted(builder.DRAFTS.glob("*.md"))[0]
        original = builder.read
        builder.read = lambda path: original(path) + ("\nРучная правка.\n" if path == target else "")
        with contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(builder.main(["--check"]), 1)
        self.assertIn(target.name, out.getvalue())

    def test_prompt_edits_registry_current(self):
        self.check(sys.executable, "experiments/issue_495/build_prompt_edits.py", "--check")

    def test_rollback_preserves_unrelated_edits_and_rejects_corrupt_hunks(self):
        rollback = load_module("experiments/issue_495/prompt_changes.py", "prompt_rollback_495")
        path = "prompts/bcreq-constitution-governance-oneshot.md"
        text = read(path)
        purity = rollback.EDITS[path]
        original = rollback.revert(path, text)
        self.assertEqual(hashlib.sha256(original.encode()).hexdigest(), purity["sha256_before"])
        extra = "\nПосторонняя правка.\n"
        self.assertEqual(rollback.revert(path, text + extra), original + extra)
        for hunk in (rollback.RELEASE.EDITS[path][0], purity["hunks"][0]):
            with self.subTest(hunk=hunk["after"][:60]):
                self.assertIn(hunk["after"], text)
                corrupted = text.replace(hunk["after"], extra, 1)
                with self.assertRaises(ValueError):
                    rollback.revert(path, corrupted)


class BaselineMapTest(unittest.TestCase):
    """Группы G карты базы принимают только копии нарушений ручных исходников.

    Мутации (роль Б, раунд 2): маркер, который пишет только сборщик, пустое окно
    и окно, найденное лишь в архиве, копией не считаются — иначе удаление без
    записи реестра ушло бы в группу G молча.
    """

    def setUp(self):
        self.mb = load_module("experiments/issue_495/map_baseline.py", "map_baseline_495")
        self.dir = tempfile.TemporaryDirectory(prefix="i495-map-")
        root = Path(self.dir.name)
        files = {
            "prompts/hand.md": "Текст шага. <!-- hand-marker: kept --> Правило шага.\n",
            "prompts/archive/old.md": "Архив. <!-- archive-only: zz --> Старый текст.\n",
            "prompts/drafts/step.md": "сборка\n",
            "prompts/hand-link.md": "См. [Ш-А](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/a.md) далее.\n",
            "prompts/drafts/system/bcreq-intake-questionnaire-system.md":
                "Промпт 0;\nИспользуй Промпт 0; затем шаг\n"
                "> **Редакция по тесту (#427): действует до ADR обратного согласования.**\n",
            "prompts/drafts/bcreq-other-stepwise.md":
                "Промпт 0;\n> **Редакция по тесту (#427): действует до ADR обратного согласования.**\n",
        }
        for rel, text in files.items():
            (root / rel).parent.mkdir(parents=True, exist_ok=True)
            (root / rel).write_text(text, encoding="utf-8")
        kinds = {rel: "archive_texts" if "/archive/" in rel else "prompts" for rel in files}
        self.mapper = self.mb.Mapper(root, kinds)

    def tearDown(self):
        self.dir.cleanup()

    def copy(self, snippet, match):
        return self.mapper.is_copy({"snippet": snippet, "match": match})

    def test_copy_of_hand_comment_is_copy(self):
        self.assertTrue(self.copy("Текст шага. <!-- hand-marker: kept --> Правило", "<!-- hand-marker: kept -->"))

    def test_builder_only_marker_is_not_copy(self):
        self.assertFalse(self.copy("<!-- totally-new-marker: zz -->", "<!-- totally-new-marker: zz -->"))

    def test_empty_window_is_not_copy(self):
        self.assertFalse(self.copy("", ""))

    def test_archive_only_window_is_not_copy(self):
        self.assertFalse(self.copy("Архив. <!-- archive-only: zz --> Старый", "<!-- archive-only: zz -->"))

    def test_link_copy_needs_whole_link(self):
        # Окно «[Ш-А](https://…/blob/main/p» есть в ручном исходнике, но ссылка
        # целиком (на черновик системного трека) — нет: это не копия (роль Б, раунд 3).
        url = "https://github.com/G-Ivan-A/mango_ba_prompts"
        same = f"См. [Ш-А]({url}/blob/main/prompts/a.md) далее."
        other = f"См. [Ш-А]({url}/blob/main/prompts/drafts/system/a.md) далее."
        self.assertTrue(self.copy(same, url))
        self.assertFalse(self.copy(other, url))

    def register(self, rel, no, match):
        line = (Path(self.dir.name) / rel).read_text(encoding="utf-8").splitlines()[no - 1]
        return self.mapper.by_register({"file": rel, "line": no, "snippet": line, "match": match}, "prompts")

    def test_short_piece_matches_whole_line_only(self):
        # «Промпт 0;» (A-07) короче 10 символов: относится к записи только строкой целиком.
        intake = "prompts/drafts/system/bcreq-intake-questionnaire-system.md"
        self.assertEqual(self.register(intake, 1, "Промпт 0"), "A-07")
        self.assertNotEqual(self.register(intake, 2, "Промпт 0"), "A-07")

    def test_carriers_split_shared_fragments(self):
        # Носитель решает, чья копия: «Промпт 0;» вне Ш-А — не A-07; общий хвост
        # баннера в черновике шага — D-13, в системном формате — D-22.
        step = "prompts/drafts/bcreq-other-stepwise.md"
        intake = "prompts/drafts/system/bcreq-intake-questionnaire-system.md"
        self.assertNotEqual(self.register(step, 1, "Промпт 0"), "A-07")
        self.assertEqual(self.register(step, 2, "ADR"), "D-13")
        self.assertEqual(self.register(intake, 3, "ADR"), "D-22")

    def test_archive_card_line_goes_to_archive(self):
        # Строка шапки блока «по тесту» на карточке архива 2.7.0 в данных сайта —
        # копия файла архива (M-02, M-03), а не запись сборщика D-14; та же строка
        # в карточке действующего промпта — D-14 (роль Б, раунд 4).
        url = "https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/x.md"
        site = Path(self.dir.name) / "site/data/prompts.json"
        site.parent.mkdir(parents=True)
        site.write_text(json.dumps({"prompts": [{"sourcePath": "prompts/hand.md", "content": "x"}]}), encoding="utf-8")
        for line, match, rule, group in (("<!-- bl-156: by-test -->", "<!-- bl-156: by-test -->", "BP-01", "M-02"),
                                         (f"Источник — [стандарт]({url}).", url, "A-PRIVATE", "M-03")):
            f = {"file": "site/data/prompts.json", "line": 1, "snippet": line, "match": match,
                 "rule": rule, "where": "prompts[].content"}
            self.assertEqual(self.mapper.classify(dict(f, archived=True), "site_data"), group)
            self.assertNotEqual(self.mapper.classify(f, "site_data"), group)
            # Новое текстовое поле карточки архива идёт туда же: маршрут задан
            # исключением (url), а не перечнем полей (роль Б, раунд 5).
            self.assertEqual(self.mapper.classify(dict(f, archived=True, where="prompts[].summary"), "site_data"), group)
        self.assertNotIn(self.mapper.classify(
            {"file": "site/data/prompts.json", "line": 1, "snippet": url, "match": url, "rule": "A-PRIVATE",
             "where": "prompts[].url", "archived": True}, "site_data"), ("M-02", "M-03"))
        self.assertEqual(self.mapper.classify(
            {"file": "site/data/prompts.json", "line": 1, "snippet": "<!-- bl-156: by-test -->",
             "match": "<!-- bl-156: by-test -->", "rule": "BP-01", "where": "prompts[].content"}, "site_data"), "D-14")

    def test_auditor_marks_archive_card_findings(self):
        root = Path(self.dir.name)
        url = "https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/x.md"
        cards = {"prompts": [{"sourcePath": "prompts/archive/old.md", "content": f"[a]({url})"},
                             {"sourcePath": "prompts/hand.md", "content": f"[a]({url})"}]}
        (root / "site/data").mkdir(parents=True, exist_ok=True)
        (root / "standards").mkdir(exist_ok=True)
        shutil.copy(ROOT / "standards/bcreq-runtime-references.md", root / "standards")
        (root / "site/data/prompts.json").write_text(json.dumps(cards), encoding="utf-8")
        auditor = audit.Auditor(root, audit.load_policy())
        auditor.audit_site_file("site/data/prompts.json", {"a"}, ["prompts[].content"], True)
        flags = [bool(f.get("archived")) for f in auditor.findings if f["rule"] == "A-PRIVATE"]
        self.assertEqual(flags, [True, False])


class RegistryAndBacklogTest(unittest.TestCase):
    def test_runtime_registry_rows(self):
        text = read(REGISTRY)
        self.assertRegex(text, r'(?m)^runtime_sha:\s*"?[0-9a-f]{40}"?')
        for marker in ["И-11", "И-12", "З-5", "РТ-8", "РТ-9", "taxonomy/product-profiles.yaml",
                       "golden/prompt-regressions.yaml"]:
            self.assertIn(marker, text)
        sha = audit.runtime_sha(ROOT)
        # Ссылки на коммит runtime в действующих разделах 1–6 — только на
        # закреплённый SHA (шаблон «<SHA>» в инструкции — не ссылка; раздел 7 —
        # история закрытого долга со старыми путями на main).
        live = text.split("\n## 7. ", 1)[0]
        for match in re.finditer(r"mango-ba-ai-runtime/(?:blob|tree)/([^/\s)]+)", live):
            if not match.group(1).startswith("<"):
                self.assertEqual(match.group(1), sha, match.group(0))

    def test_case_register_traces_to_runtime(self):
        policy = audit.load_policy(ROOT / POLICY)
        ids = [c["id"] for c in policy["case_register"]]
        self.assertTrue(ids)
        self.assertEqual(len(ids), len(set(ids)))
        for case in policy["case_register"]:
            self.assertIn("golden/prompt-regressions.yaml", json.dumps(case, ensure_ascii=False), case["id"])

    def test_backlog_chain(self):
        backlog = read("pr-ops/BACKLOG.md")
        cards = read("pr-ops/backlog-repository.md")
        for card in ["BL-240", "BL-241", "BL-242", "BL-232"]:
            self.assertRegex(backlog, rf"(?m)^\|\s*{card}\s*\|", card)
            self.assertRegex(cards, rf"(?m)^### {card}\. ", f"карточка {card}")
        for card, follow in [("BL-240", "BL-241"), ("BL-241", "BL-242"), ("BL-242", "BL-232")]:
            row = re.search(rf"(?m)^\|\s*{card}\s*\|.*$", backlog).group(0)
            self.assertIn(follow, row, f"{card} → {follow}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
