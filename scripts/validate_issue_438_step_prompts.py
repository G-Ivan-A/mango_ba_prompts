#!/usr/bin/env python3
"""Регрессионная проверка BL-157 и BL-156: комплект прогона и промпты шагов «по тесту» (issue #438).

Проверка закрепляет результат задачи:

* сборщик ``scripts/build_bcreq_step_prompts.py`` детерминирован: его выход
  совпадает с ``prompts/drafts/`` байт в байт, лишних файлов нет (то же, что
  ``--check``); манифест покрывает 13 шагов маршрута в 12 файлах;
* каждый черновик несёт текст v0.1 без изменений; после BL-156а (issue
  #444) ссылки на runtime в v0.1 уже закреплены по SHA реестра, замен
  ``blob/main`` → ``blob/<SHA>`` ноль; ``based_on_sha256`` равен хэшу
  текущего v0.1 — правка v0.1 без пересборки ломает проверку;
* профили Ш-В — из таблицы «Шаги и профили» стандарта профилей, а не из
  таблицы 9.2 RFC (ответ владельца в #438); блоки уроков не применены
  (ждут ADR-017);
* RUN-0080 и RUN-0081: метрики A и D пересчитываются из оценок судьи,
  ключа и golden set и совпадают с ``metrics.json``; флаги
  ``publication.not_worse`` — тоже. RUN-0080 — история (правки
  ``post-run-deltas.json`` разобраны), текущие тексты A и D измерены
  RUN-0081: их хэши равны ``prompt_sha256`` RUN-0081 байт в байт (любая
  правка v0.1 Ш-В или черновика Ш-В требует нового прогона);
* комплект прогона ссылается на существующий черновик каждого шага; у
  каждой таблицы комплекта число колонок строк равно заголовку;
* ``R15_ACCEPTED = False`` (проверка готовности 2026-11-04, комментарий
  владельца в PR #439): RFC #427 — версия 0.5.1, поправка 0.6 — проект,
  DEC-427-04 и DEC-427-12 ``proposed``; Р-15 «ждёт»; ``PENDING`` валидатора
  #427 (Р-13) содержит 04 и 12; ``BL156_STARTED = True`` (BL-156а,
  issue #444): ссылки на runtime в ``prompts/`` закреплены по SHA;
  ``TYPING_APPLIED = False``: ``prompt-typing.json`` не применена к 14
  подстановкам — RUN-0081 измерил A с ней, ядро 9/11 против 10/11 RUN-0079,
  правка перенесена в BL-156б (строки ``before`` на месте, ``after`` нет);
  ``SHV_V02_PUBLISHED = True`` (issue #448): подстановка Ш-В применена в
  v0.2 по RUN-0084 вместе с правилом «правка без добавлений»; тексты A и D
  RUN-0081 восстанавливаются из v0.2 откатом ``shv_v02_changes.revert()``;
* бэклог: BL-157 — ``review`` (BL-157а ``DONE``, BL-157б ``review`` в
  PR #447 — набор на сайте и A-IN ``by-test`` по RUN-0083, BL-157в ждёт
  входа от владельца), BL-156 — ``deferred (triggered)`` (BL-156а ``DONE``,
  BL-156б и BL-156в ждут Р-03 и бюджета); карточки — история «Заготовка
  (до старта)», «Исполнение» BL-156а и BL-157б; входы BL-158;
  ``R16_ACCEPTED = False`` в валидаторе #433 до BL-162;
* отчёт BL-156, анализ Р-16 и разбор готовности BL-156 / BL-157: разделы
  стандарта анализа, вопрос владельцу AS-IS / TODO; цитаты анализа Р-16 и
  разбора готовности сверяются с исходными документами.

Запуск: ``python3 scripts/validate_issue_438_step_prompts.py``
"""

import hashlib
import importlib.util
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DRAFTS = ROOT / "prompts/drafts"
MANIFEST = DRAFTS / "manifest.json"
KIT = ROOT / "docs/ba-processes/bcreq-run-kit.md"
RFC = ROOT / "docs/rfc/2026-11-bcreq-flow-processes-prompts.md"
BACKLOG = ROOT / "pr-ops/BACKLOG.md"
TRACK_B = ROOT / "pr-ops/backlog-ba-model.md"
PROFILES = ROOT / "standards/bcreq-prompt-profiles.md"
REPORT = ROOT / "docs/analysis/2026-11-03-bl-156-step-prompts-report.md"
R16 = ROOT / "docs/analysis/2026-11-03-silence-consent-gates-r16.md"
CHANGELOG = ROOT / "CHANGELOG.md"
RUN = ROOT / "runs/2026/RUN-0080"
RUN_0081 = ROOT / "runs/2026/RUN-0081"
RUN_0079 = ROOT / "runs/2026/RUN-0079/outputs/metrics.json"
POST_RUN_DELTAS = ROOT / "experiments/issue_438/run0080/post-run-deltas.json"
PROMPT_TYPING = ROOT / "experiments/issue_438/prompt-typing.json"
READINESS = ROOT / "docs/analysis/2026-11-04-bl-156-157-readiness-check.md"

#: Р-15 принято владельцем явно: «Р-15 да. … П-П: BL-157 сначала (через
#: BL-157а). Р-16 да (А+).» (комментарий к PR #439). Поправка 0.6 RFC
#: принята, RFC v0.6, DEC-427-04 и DEC-427-12 ``accepted``.
R15_ACCEPTED = True
OWNER_COMMENT = "https://github.com/G-Ivan-A/mango_ba_prompts/pull/439#issuecomment-6630337995"
#: BL-156 стартовала: этап BL-156а (issue #444, PR #445) закрепил ссылки на
#: runtime в ``prompts/`` по SHA.
BL156_STARTED = True
#: Типизация гейтов (``prompt-typing.json``) в ``prompts/`` не применена:
#: RUN-0081 — ядро A 9/11 против 10/11 RUN-0079 (DEC-427-11), правка
#: перенесена в BL-156б. True — только с прогоном, где A не хуже RUN-0079.
TYPING_APPLIED = False
#: Issue #448 (BL-156б+в): Ш-В опубликован как v0.2 по RUN-0084 (Р-03,
#: одновременный контроль): подстановка типа гейта Ш-В и правило «правка
#: без добавлений». Остальные 14 подстановок — по ``TYPING_APPLIED``.
SHV_V02_PUBLISHED = True

CRITERIA = ("K1", "K2", "K3", "K4", "K5", "K6")
ANALYSIS_SECTIONS = ("## Summary / BLUF", "## Context / Scope", "## Findings / Options",
                     "## Recommendations", "## Related Artifacts")

#: Цитаты анализа Р-16 → файл-источник. Цитата должна дословно (с точностью
#: до переносов строк) стоять и в анализе, и в источнике.
R16_QUOTES = {
    "docs/adr/0003-creative-mode-governance.md": "Пользователь молчит + мержит PR → молчание = согласие",
    "pr-ops/session-digests.md": "Переход Draft → Canonical требует ЯВНОГО подтверждения Пользователя.",
    "standards/prompt-debugging-process.md": "Молчание ≠ согласие на правку промпта",
    "docs/adr/003-ba-ontology.md": "Переходы через **human gate** требуют подтверждения Пользователя",
    "standards/bcreq-flow-glossary.md": "**Молчание — не согласие.** Решение `человек` и `гибрид` — явный ответ человека",
    "standards/bcreq-process-standard.md": "относится к приёмке изменений репозитория и к решению на гейте не применяется",
    "docs/ba-processes/bcreq-manual-process.md": "Шаг, повтор, пропуск, возврат и гейт выбирает БА или согласующий; молчание не согласие.",
    "docs/contracts/bcreq-manual-state.md": "Рекомендация модели и учебная симуляция не являются человеческим решением. Молчание не согласие.",
    "docs/ba-processes/bcreq-run-kit.md": "неявный (следующий промпт запущен без записи)",
    "prompts/bcreq-context-understanding-stepwise.md": "Если дополнение не передано, по умолчанию — без БЗ",
}

#: Цитаты разбора готовности BL-156 / BL-157 → файл-источник.
READINESS_QUOTES = {
    "pr-ops/backlog-instruction.md": "Задача стартует, когда зависимости `DONE` и решения приняты.",
    "pr-ops/backlog-instruction.md#done": "Результат слит или принят; есть ссылка на доказательство.",
    "docs/rfc/2026-11-runtime-product-catalog-golden-set.md": "Почему: тогда BL-156 выйдет без заглушек З-1 и З-3.",
    "docs/rfc/2026-11-bcreq-flow-processes-prompts.md": "| 4 | Промпты и комплект прогона | BL-156, BL-157 |",
}


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BUILDER = load("bcreq_step_builder", ROOT / "scripts/build_bcreq_step_prompts.py")
BL156A = load("bl156a_for_438", ROOT / "experiments/issue_444/bl156a_prompt_changes.py")
SHV_V02 = BL156A.SHV_V02
SHV = "prompts/bcreq-review-validation-oneshot.md"
SHV_DRAFT = "prompts/drafts/bcreq-review-validation-oneshot.md"


def digest(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def shv_v01():
    """v0.1 Ш-В (A0 RUN-0084): текущий файл с откатом публикации v0.2."""
    text = read(ROOT / SHV)
    return SHV_V02.revert(SHV, text) if SHV_V02_PUBLISHED else text


def measured_a():
    """A RUN-0081: v0.1 Ш-В с подстановками типа гейта (BL-156б)."""
    text = shv_v01()
    return text if TYPING_APPLIED else BL156A.apply_typing(SHV, text)


def measured_d():
    """D RUN-0081: черновик Ш-В, собранный из ``measured_a()``.

    Черновик встраивает текст шага v0.1 и хранит его хэш в
    ``based_on_sha256``; без типизации отличаются только эти места.
    """
    text = read(ROOT / SHV_DRAFT)
    if TYPING_APPLIED:
        return text
    base = digest(read(ROOT / SHV))
    assert text.count(f"based_on_sha256: {base}") == 1, SHV_DRAFT
    text = text.replace(f"based_on_sha256: {base}", f"based_on_sha256: {digest(measured_a())}")
    if SHV_V02_PUBLISHED:
        # Черновик собран из v0.2: правило и версия — откат, тип гейта уже стоит.
        assert text.count(SHV_V02.RULE) == 1, SHV_DRAFT
        text = text.replace(SHV_V02.RULE, "")
        assert text.count("\nversion: 0.2\n") == 1, SHV_DRAFT
        return text.replace("\nversion: 0.2\n", "\nversion: 0.1\n", 1)
    for sub in BL156A.substitutions(SHV):
        assert text.count(sub["before"]) == 1, (SHV_DRAFT, sub["line"])
        text = text.replace(sub["before"], sub["after"])
    return text


def read(path):
    return path.read_text(encoding="utf-8")


def flat(text):
    return re.sub(r"\s+", " ", text)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def table_rows(text):
    """Таблицы Markdown: список (номер строки заголовка, заголовок, строки)."""
    tables, lines, index = [], text.splitlines(), 0
    in_code = False
    while index < len(lines):
        line = lines[index]
        if line.startswith("```"):
            in_code = not in_code
        if (not in_code and line.startswith("|") and index + 1 < len(lines)
                and re.match(r"^\|(\s*:?-{3,}:?\s*\|)+$", lines[index + 1])):
            header, rows, index = line, [], index + 2
            while index < len(lines) and lines[index].startswith("|"):
                rows.append(lines[index])
                index += 1
            tables.append((header, rows))
            continue
        index += 1
    return tables


def columns(line):
    return len(re.split(r"(?<!\\)\|", line.strip().strip("|")))


class BuildTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.outputs = BUILDER.build_all()
        cls.manifest = json.loads(read(MANIFEST))

    def test_drafts_match_builder(self):
        for path, text in self.outputs.items():
            self.assertTrue(path.exists(), path)
            self.assertEqual(read(path), text, f"{path.relative_to(ROOT)}: пересоберите сборщиком")
        extra = sorted(p.name for p in DRAFTS.iterdir() if p.is_file() and p not in self.outputs)
        self.assertEqual(extra, [], "лишние файлы в prompts/drafts/")

    def test_manifest_covers_route(self):
        drafts = self.manifest["drafts"]
        self.assertEqual(len(drafts), 12)
        steps = [s for d in drafts for s in d["steps"]]
        self.assertEqual(sorted(steps), sorted(BUILDER.ROUTE))
        self.assertEqual(self.manifest["source_issue"], "https://github.com/G-Ivan-A/mango_ba_prompts/issues/438")
        self.assertIn("ADR-017", self.manifest["lessons_blocks"])

    def test_draft_markers(self):
        for item in self.manifest["drafts"]:
            text = read(ROOT / item["file"])
            self.assertIn(BUILDER.EXPERIMENTAL, text, item["file"])
            self.assertIn(BUILDER.MODE_LINE, text, item["file"])
            fm = re.match(r"^---\n(.*?)\n---\n", text, re.S).group(1)
            self.assertRegex(fm, r"(?m)^id: \S+-by-test$", item["file"])
            self.assertRegex(fm, r"(?m)^mode: by-test$", item["file"])
            self.assertRegex(fm, rf"(?m)^runtime_sha: {self.manifest['runtime_sha']}$", item["file"])

    def test_v01_text_embedded_unchanged(self):
        sha = self.manifest["runtime_sha"]
        pinned = BUILDER.RUNTIME_MAIN.replace("/main/", f"/{sha}/")
        for item in self.manifest["drafts"]:
            if item["based_on"] is None:
                self.assertEqual(item["steps"], ["Ш-Р"], "без v0.1 — только заглушка Ш-Р")
                continue
            source = ROOT / item["based_on"]
            self.assertEqual(sha256(source), item["based_on_sha256"], f"{item['based_on']} изменён без пересборки")
            _, body = BUILDER.split_frontmatter(read(source))
            draft = read(ROOT / item["file"])
            self.assertEqual(body.count(BUILDER.RUNTIME_MAIN), item["runtime_main_to_sha"], item["file"])
            # BL-156а: v0.1 ссылается на runtime по SHA реестра, а не на main.
            self.assertEqual(item["runtime_main_to_sha"], 0 if BL156_STARTED else item["runtime_main_to_sha"], item["file"])
            if BL156_STARTED:
                self.assertGreater(body.count(pinned), 0, item["file"])
            # Текст шага встроен байт в байт; ссылки на main (до BL-156а)
            # сборщик закрепляет по SHA.
            self.assertIn(body.replace(BUILDER.RUNTIME_MAIN, pinned).rstrip("\n"), draft, item["file"])

    def test_review_profiles_from_steps_table(self):
        _, _, steps = BUILDER.load_profiles()
        review = next(d for d in self.manifest["drafts"] if d["steps"] == ["Ш-В"])
        self.assertEqual(review["profiles"], steps["Ш-В"]["profiles"])
        self.assertIn("ANALYZE", review["profiles"], "Ш-В: профили из таблицы «Шаги и профили», а не 9.2 RFC")
        self.assertIn("Шаги и профили", read(PROFILES))


class RunScoring:
    """Пересчёт метрик прогона из оценок судьи, ключа и golden set."""
    RUN_DIR = RUN

    @classmethod
    def setUpClass(cls):
        run = cls.RUN_DIR
        cls.metrics = json.loads(read(run / "outputs/metrics.json"))
        cls.mapping = json.loads(read(run / "inputs/mapping.json"))
        cls.key = json.loads(read(run / "outputs/judge-key.json"))
        cls.scores = json.loads(read(run / "outputs/judge-scores.json"))
        v411 = load("v411_for_438", ROOT / "scripts/validate_issue_411_lessons_pipeline.py")
        cls.cases = {c["case-id"]: c for c in v411.golden_cases()}

    def score(self, version):
        by_case = {}
        for item in self.scores:
            for label in ("X", "Y"):
                if self.key[item["case"]][label] == version:
                    by_case[item["case"]] = item[label]
        passed = core = core_total = neg = fp = 0
        per = {c: [0, 0] for c in CRITERIA}
        for tid, case_id in self.mapping["mapping"].items():
            case, score = self.cases[case_id], by_case[tid]
            negative = case["Эталонный вердикт"] == "дефекта нет"
            ok = True
            for criterion in CRITERIA:
                if negative and criterion == "K2":
                    continue
                per[criterion][1] += 1
                per[criterion][0] += bool(score.get(criterion))
                ok &= bool(score.get(criterion))
            if negative:
                neg += 1
                fp += not score.get("K1")
            if case["Ядро"] == "да":
                core_total += 1
                core += ok
            passed += ok
        return {"passed": passed, "core": f"{core}/{core_total}", "negatives_false_positive": f"{fp}/{neg}",
                "criteria": {c: f"{v[0]}/{v[1]}" for c, v in per.items()}}

    @staticmethod
    def not_worse(candidate, reference):
        def first(text):
            return int(text.split("/")[0])

        return (candidate["passed"] >= reference["passed"] and first(candidate["core"]) >= first(reference["core"])
                and first(candidate["negatives_false_positive"]) <= first(reference["negatives_false_positive"]))


class Run0080Test(RunScoring, unittest.TestCase):
    def test_metrics_recomputed(self):
        self.assertEqual(len(self.mapping["mapping"]), 62)
        for version in ("A", "D"):
            got = self.score(version)
            for field, value in got.items():
                self.assertEqual(self.metrics[version][field], value, f"{version}.{field}")
        self.assertEqual(self.metrics["A"]["passed"], 55)
        self.assertEqual(self.metrics["D"]["passed"], 55)

    def test_publication_flags(self):
        baseline = json.loads(read(RUN_0079))["A"]
        for name, ref in (("vs_RUN_0079", baseline), ("vs_A_same_judge", self.metrics["A"])):
            self.assertEqual(self.metrics["publication"][name]["not_worse"],
                             self.not_worse(self.metrics["D"], ref), name)
        self.assertTrue(self.metrics["publication"]["not_worse"])

    def test_measured_texts_are_history(self):
        # RUN-0080 — история: тексты A и D после него менялись (BL-156а,
        # issue #444) и измерены заново RUN-0081 (Run0081Test).
        meta = read(RUN / "metadata.yaml")
        draft = ROOT / "prompts/drafts/bcreq-review-validation-oneshot.md"
        v01 = ROOT / "prompts/bcreq-review-validation-oneshot.md"
        # Правки черновика после замера (post-run-deltas.json) — только
        # строки ссылок, поведение none или reverted-to-v0.1.
        deltas = json.loads(read(POST_RUN_DELTAS))
        self.assertEqual(ROOT / deltas["file"], draft)
        for delta in deltas["deltas"]:
            self.assertIn(delta["behavior"], ("none", "reverted-to-v0.1"))
        # A RUN-0080 — v0.1 с типом гейта и ссылками на main. BL-156а
        # закрепила ссылки по SHA, тип гейта не применён: подстановки и
        # откат закрепления дают измеренный A.
        sha = json.loads(read(MANIFEST))["runtime_sha"]
        pinned = BUILDER.RUNTIME_MAIN.replace("/main/", f"/{sha}/")
        self.assertEqual(ROOT / SHV, v01)
        text = measured_a()
        self.assertGreater(text.count(pinned), 0)
        text = text.replace(pinned, BUILDER.RUNTIME_MAIN)
        self.assertEqual(digest(text), self.metrics["A"]["prompt_sha256"],
                         "v0.1 Ш-В: правка сверх закрепления ссылок BL-156а")
        self.assertIn(self.metrics["D"]["prompt_sha256"], meta)
        self.assertIn(self.metrics["A"]["prompt_sha256"], meta)
        previous = json.loads(read(RUN_0081 / "outputs/metrics.json"))["previous_RUN_0080"]
        for version in ("A", "D"):
            self.assertEqual(previous[version]["prompt_sha256"], self.metrics[version]["prompt_sha256"], version)
            self.assertEqual(previous[version]["passed"], self.metrics[version]["passed"], version)

    def test_report_records_decision(self):
        report = flat(read(RUN / "outputs/golden-set-report.md"))
        self.assertIn("«П-Ш-В»", report)
        self.assertIn("в `prompts/` в этом PR не переносится", report)


class Run0081Test(RunScoring, unittest.TestCase):
    """RUN-0081 (BL-156а, issue #444): текущие A и D, тот же golden set и раскладка, что RUN-0079."""
    RUN_DIR = RUN_0081

    def test_metrics_recomputed(self):
        self.assertEqual(len(self.mapping["mapping"]), 62)
        self.assertEqual(self.mapping["mapping"], json.loads(read(ROOT / "runs/2026/RUN-0079/inputs/mapping.json"))["mapping"])
        for version in ("A", "D"):
            got = self.score(version)
            for field, value in got.items():
                self.assertEqual(self.metrics[version][field], value, f"{version}.{field}")

    def test_publication_flags(self):
        # DEC-427-11: правка prompts/ (A) и черновик (D) не хуже базы RUN-0079.
        baseline = json.loads(read(RUN_0079))["A"]
        publication = self.metrics["publication"]
        for name, ref in (("vs_RUN_0079", baseline), ("vs_A_same_judge", self.metrics["A"])):
            self.assertEqual(publication[name]["not_worse"], self.not_worse(self.metrics["D"], ref), name)
        self.assertEqual(self.metrics["A_vs_RUN_0079"]["not_worse"], self.not_worse(self.metrics["A"], baseline))
        # A (v0.1 с типом гейта) хуже RUN-0079 по ядру: типизацию не
        # публиковать. TYPING_APPLIED = True без такого прогона ломает проверку.
        self.assertEqual(TYPING_APPLIED, self.metrics["A_vs_RUN_0079"]["not_worse"],
                         "TYPING_APPLIED расходится с A_vs_RUN_0079 RUN-0081")
        self.assertFalse(publication["not_worse"], "D хуже — черновики остаются в prompts/drafts/")

    def test_measured_texts_are_current(self):
        # Текущие Ш-В и черновик Ш-В — измеренные A и D: v0.2 (RUN-0084)
        # откатывается к v0.1 (shv_v02_changes.revert), к нему добавляются
        # подстановки типа гейта; любая другая правка требует нового прогона.
        meta = read(RUN_0081 / "metadata.yaml")
        for version, text in (("A", measured_a()), ("D", measured_d())):
            self.assertEqual(digest(text), self.metrics[version]["prompt_sha256"],
                             f"{version}: Ш-В изменён после RUN-0081 — нужен новый прогон")
            self.assertIn(self.metrics[version]["prompt_sha256"], meta)


class KitTest(unittest.TestCase):
    def test_draft_column_links_exist(self):
        text = read(KIT)
        manifest = {d["file"] for d in json.loads(read(MANIFEST))["drafts"]}
        header, rows = next(t for t in table_rows(text) if "Черновик «по тесту» (BL-156)" in t[0])
        self.assertEqual(len(rows), 13)
        index = [c.strip() for c in header.strip().strip("|").split("|")].index("Черновик «по тесту» (BL-156)")
        for row in rows:
            cell = row.strip().strip("|").split("|")[index]
            link = re.search(r"\]\(\.\./\.\./(prompts/drafts/[a-z0-9-]+\.md)\)", cell)
            self.assertIsNotNone(link, row)
            self.assertIn(link.group(1), manifest, row)
        self.assertIn("prompt_set.mode: by-test", text)

    def test_tables_have_consistent_columns(self):
        for header, rows in table_rows(read(KIT)):
            for row in rows:
                self.assertEqual(columns(row), columns(header), f"{header[:40]}… / {row[:60]}")


class DecisionsTest(unittest.TestCase):
    def test_rfc_amendment_06(self):
        text = read(RFC)
        self.assertTrue(R15_ACCEPTED)
        self.assertRegex(text, r"(?m)^version: 0\.6$")
        self.assertIn("### Поправка 0.6: промпты шагов (принята Р-15; issue #438)", text)
        self.assertIn("**Статус поправки: принята.**", text)
        self.assertIn(OWNER_COMMENT, text)
        for dec in ("DEC-427-04", "DEC-427-12"):
            self.assertRegex(text, rf"(?m)^\| {dec}\. [^|]+\| `accepted` \| Р-15 \(\[PR #439\]\({re.escape(OWNER_COMMENT)}\)\) \|$")

    def test_r13_validator_pending(self):
        v427 = load("v427_for_438", ROOT / "scripts/validate_issue_427_r13_acceptance.py")
        pending = {n for n, d in v427.PENDING.items() if d == "Р-15"}
        self.assertEqual(set(v427.R15), {"04", "12"})
        self.assertEqual(pending, set() if R15_ACCEPTED else {"04", "12"})

    def test_published_prompts_typed(self):
        typing = json.loads(read(PROMPT_TYPING))
        prefix = "применена" if TYPING_APPLIED else ("частично применена" if SHV_V02_PUBLISHED else "не применена")
        self.assertTrue(typing["status"].startswith(prefix), typing["status"])
        if not TYPING_APPLIED:
            for marker in ("RUN-0081", "RUN-0082", "BL-156б"):
                self.assertIn(marker, typing["status"])
            if SHV_V02_PUBLISHED:
                self.assertIn("RUN-0084", typing["status"])
        self.assertEqual(len({s["path"] for s in typing["substitutions"]}), 14)
        applied = [s for s in typing["substitutions"] if s.get("applied")]
        self.assertEqual([s["path"] for s in applied], [SHV] if SHV_V02_PUBLISHED else [])
        for sub in typing["substitutions"]:
            text = read(ROOT / sub["path"])
            expected, absent = ("after", "before") if TYPING_APPLIED or sub.get("applied") else ("before", "after")
            self.assertEqual(text.count(sub[expected]), 1, f"{sub['path']} {sub['line']}")
            self.assertEqual(text.count(sub[absent]), 0, f"{sub['path']} {sub['line']}")

    def test_backlog_rows(self):
        text = read(BACKLOG)
        r15 = re.search(r"(?m)^\| \*\*Р-15\*\* \|.*\| (\S+)[^|]* \|$", text).group(1)
        self.assertEqual(r15 != "ждёт", R15_ACCEPTED, "Р-15 и R15_ACCEPTED расходятся")
        self.assertIn(OWNER_COMMENT, re.search(r"(?m)^\| \*\*Р-15\*\* \|.*$", text).group(0))
        r16 = re.search(r"(?m)^\| \*\*Р-16\*\* \|.*$", text).group(0)
        self.assertIn("принято, вариант А+", r16)
        rows = {t: [c.strip() for c in re.search(rf"(?m)^\| {t} \|.*$", text).group(0).strip("|").split("|")]
                for t in ("BL-150", "BL-151", "BL-152", "BL-153", "BL-154", "BL-155", "BL-159",
                          "BL-156", "BL-157", "BL-162")}
        for t in ("BL-150", "BL-151", "BL-152", "BL-153", "BL-154", "BL-155", "BL-159"):
            self.assertEqual(rows[t][4], "DONE", t)
        # П-П: BL-157 сначала (через BL-157а) — один номер, два этапа в карточке.
        # PR #439 слит: BL-157а — DONE; BL-157б — review в PR #447 (RUN-0083, issue #446);
        # первый прогон BL-111 выделен в BL-157в и ждёт входа от владельца.
        self.assertEqual(rows["BL-157"][4], "review")
        for pr in ("PR #439", "PR #447"):
            self.assertIn(pr, rows["BL-157"][5])
        for marker in ("BL-157а — `DONE` (PR #439)", "BL-157б — `review` (PR #447)", "RUN-0083",
                       "BL-157в — `deferred (triggered)`", READINESS.name):
            self.assertIn(marker, rows["BL-157"][7])
        # PR #445 слит: BL-156а — DONE; BL-156б и BL-156в ждут Р-03 и бюджета (RUN-0082, issue #446).
        self.assertEqual(rows["BL-156"][4], "TODO" if not BL156_STARTED else "deferred (triggered)")
        self.assertIn("BL-157 (этап BL-157а)", rows["BL-156"][3])
        self.assertIn(READINESS.name, rows["BL-156"][7])
        if BL156_STARTED:
            self.assertIn("PR #445", rows["BL-156"][5])
            self.assertIn("PR #447", rows["BL-156"][5])
            for marker in ("BL-156а — `DONE` (PR #445)", "RUN-0081", "BL-156б — `deferred (triggered)`",
                           "RUN-0082", "BL-156в — `deferred (triggered)`"):
                self.assertIn(marker, rows["BL-156"][7])
        self.assertEqual(rows["BL-162"][4], "TODO")
        # Р-16 принято, но поправку 0.2 ADR-003 применяет BL-162: флаг #433 меняется вместе с ней.
        v433 = load("v433_for_438", ROOT / "scripts/validate_issue_433_gate_types.py")
        self.assertFalse(v433.R16_ACCEPTED, "R16_ACCEPTED = True — только с исполнением BL-162")

    def test_cards(self):
        text = read(TRACK_B)
        for task in ("BL-156", "BL-157"):
            card = re.search(rf"(?ms)^### {task}\..*?(?=^#### |^### )", text).group(0)
            self.assertIn("**Заготовка (до старта).** Issue #438, PR #439 — ", card, task)
            self.assertIn(READINESS.name, card, task)
            self.assertIn(OWNER_COMMENT, card, task)
            if task == "BL-156" and BL156_STARTED:
                self.assertIn("**Исполнение.** Issue #444, PR #445 (2026-11-04) — этап BL-156а.", card)
            else:
                self.assertIn("**Исполнение.** Issue #446, PR #447 (2026-11-04) — этап BL-157б.", card)
        if BL156_STARTED:
            for stage in ("#### BL-156а. ", "#### BL-156б. ", "#### BL-156в. "):
                self.assertIn(stage, text)
            bl156b = re.search(r"(?ms)^#### BL-156б\..*?(?=^#{3,4} )", text).group(0)
            self.assertIn("prompt-typing.json", bl156b)
            self.assertIn("RUN-0082", bl156b)
        card = re.search(r"(?ms)^#### BL-157а\..*?(?=^#{3,4} )", text).group(0)
        self.assertIn("**Исполнение.** Issue #438, PR #439.", card)
        for stage in ("#### BL-157б. Комплект прогона: промпты по тесту", "#### BL-157в. Первый прогон BL-111 с комплектом"):
            self.assertIn(stage, text)
        bl157b = re.search(r"(?ms)^#### BL-157б\..*?(?=^#{3,4} )", text).group(0)
        self.assertIn("RUN-0083", bl157b)
        kit = read(KIT)
        self.assertIn("**Статус: действует; A-IN — по тесту (BL-157б).**", kit)
        self.assertNotIn("не применять", kit)
        self.assertIn("`prompt_set.mode: by-test`", kit)
        bl158 = re.search(r"(?ms)^### BL-158\..*?(?=^### )", text).group(0)
        self.assertIn("**Входы из BL-156**", bl158)
        for rule in sorted(BUILDER.EXCLUDED_BASE):
            self.assertIn(rule, bl158)
        self.assertIn("L-21", bl158)

    def test_changelog(self):
        self.assertIn("### Added — Issue #438:", read(CHANGELOG))


class AnalysisTest(unittest.TestCase):
    def check_analysis(self, path, subtype):
        text = read(path)
        self.assertRegex(text, rf"(?m)^analysis-subtype: {subtype}$", path.name)
        self.assertRegex(text, r'(?m)^source: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/438"$')
        self.assertNotIn("ai-generated", text.split("\n---\n", 1)[0])
        positions = [text.index(s) for s in ANALYSIS_SECTIONS]
        self.assertEqual(positions, sorted(positions), path.name)
        for link in re.findall(r"\]\(([^)#]+\.md)(?:#[^)]*)?\)", text):
            if not link.startswith("http"):
                self.assertTrue((path.parent / link).resolve().exists(), f"{path.name}: {link}")
        return text

    def test_bl156_report(self):
        text = self.check_analysis(REPORT, "recommendation")
        for heading in ("### 1. Порядок исполнения", "### 2. Сборка", "### 3. Расхождения",
                        "### 4. Golden set", "### 5. Публикация", "### 6. Обоснованные обходы"):
            self.assertIn(heading, text)
        for option in ("П1", "П2", "П3"):
            self.assertIn(option, text)
        self.assertIn(R16.name, text)

    def test_r16_analysis(self):
        text = self.check_analysis(R16, "options")
        flat_text = flat(text)
        for marker in ("**AS-IS.**", "**TODO (рекомендация).**", "**Почему.**", "«Р-16 да (А+)»",
                       "BL-162 заблокирован", "`R16_ACCEPTED = False`"):
            self.assertIn(marker, flat_text)
        for number in range(1, 8):
            self.assertIn(f"| П{number} |", text)
        for path, quote in R16_QUOTES.items():
            self.assertIn(flat(quote), flat_text, f"цитата {path} пропала из анализа")
            self.assertIn(flat(quote), flat(read(ROOT / path)), f"цитата не найдена в {path}")

    def test_readiness_check(self):
        text = self.check_analysis(READINESS, "recommendation")
        flat_text = flat(text.replace("\\|", "|"))
        for marker in ("**Гипотеза 1: «BL-156 запущена раньше срока».** Подтверждена.",
                       "**Гипотеза 2: «предусловия BL-157 не готовы».** Подтверждена.",
                       "| **Б (выбран)** |", "«Р-15 да»", "«П-П: BL-157 сначала»",
                       "`R16_ACCEPTED = False`", "2db0ef5"):
            self.assertIn(flat(marker), flat_text)
        for number in range(1, 6):
            self.assertIn(f"| О-{number} |", text)
        for key, quote in READINESS_QUOTES.items():
            self.assertIn(flat(quote), flat_text, f"цитата {key} пропала из разбора")
            self.assertIn(flat(quote), flat(read(ROOT / key.split("#")[0])), f"цитата не найдена в {key}")
        for path in (REPORT, RFC, KIT, TRACK_B, BACKLOG):
            self.assertIn(READINESS.name, read(path), f"{path.name} не ссылается на разбор готовности")


if __name__ == "__main__":
    sys.exit(0 if unittest.main(exit=False, verbosity=1).result.wasSuccessful() else 1)
