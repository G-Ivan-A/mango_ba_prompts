#!/usr/bin/env python3
"""Регрессионная проверка BL-157 и BL-156: комплект прогона и промпты шагов «по тесту» (issue #438).

Проверка закрепляет результат задачи:

* сборщик ``scripts/build_bcreq_step_prompts.py`` детерминирован: его выход
  совпадает с ``prompts/drafts/`` байт в байт, лишних файлов нет (то же, что
  ``--check``); манифест покрывает 13 шагов маршрута в 12 файлах;
* каждый черновик несёт текст v0.1 без изменений, кроме ссылок на runtime
  ``blob/main`` → ``blob/<SHA реестра>``; ``based_on_sha256`` равен хэшу
  текущего v0.1 — правка v0.1 без пересборки ломает проверку;
* профили Ш-В — из таблицы «Шаги и профили» стандарта профилей, а не из
  таблицы 9.2 RFC (ответ владельца в #438); блоки уроков не применены
  (ждут ADR-017);
* RUN-0080: метрики A и D пересчитываются из оценок судьи, ключа и golden
  set и совпадают с ``metrics.json``; флаги ``publication.not_worse`` —
  тоже; хэш черновика Ш-В равен измеренному (черновик меняется только
  новым прогоном);
* комплект прогона ссылается на существующий черновик каждого шага; у
  каждой таблицы комплекта число колонок строк равно заголовку;
* RFC #427 — версия 0.6, Р-15 принято, DEC-427-04 и DEC-427-12 ``accepted``;
* бэклог: BL-156 и BL-157 — ``review`` с остатком, входы BL-158;
  Р-16 ждёт, и тогда ``R16_ACCEPTED = False`` в валидаторе #433;
* отчёт BL-156 и анализ Р-16: разделы стандарта анализа, вопрос владельцу
  AS-IS / TODO; цитаты анализа Р-16 сверяются с исходными документами.

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
RUN_0079 = ROOT / "runs/2026/RUN-0079/outputs/metrics.json"

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


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BUILDER = load("bcreq_step_builder", ROOT / "scripts/build_bcreq_step_prompts.py")


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
            self.assertGreater(item["runtime_main_to_sha"], 0, item["file"])
            self.assertIn(body.replace(BUILDER.RUNTIME_MAIN, pinned).rstrip("\n"), draft, item["file"])
            self.assertIn(body.rstrip("\n"), draft.replace(pinned, BUILDER.RUNTIME_MAIN), item["file"])

    def test_review_profiles_from_steps_table(self):
        _, _, steps = BUILDER.load_profiles()
        review = next(d for d in self.manifest["drafts"] if d["steps"] == ["Ш-В"])
        self.assertEqual(review["profiles"], steps["Ш-В"]["profiles"])
        self.assertIn("ANALYZE", review["profiles"], "Ш-В: профили из таблицы «Шаги и профили», а не 9.2 RFC")
        self.assertIn("Шаги и профили", read(PROFILES))


class Run0080Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.metrics = json.loads(read(RUN / "outputs/metrics.json"))
        cls.mapping = json.loads(read(RUN / "inputs/mapping.json"))
        cls.key = json.loads(read(RUN / "outputs/judge-key.json"))
        cls.scores = json.loads(read(RUN / "outputs/judge-scores.json"))
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
        d = self.metrics["D"]

        def first(text):
            return int(text.split("/")[0])

        for name, ref in (("vs_RUN_0079", baseline), ("vs_A_same_judge", self.metrics["A"])):
            expect = (d["passed"] >= ref["passed"] and first(d["core"]) >= first(ref["core"])
                      and first(d["negatives_false_positive"]) <= first(ref["negatives_false_positive"]))
            self.assertEqual(self.metrics["publication"][name]["not_worse"], expect, name)
        self.assertTrue(self.metrics["publication"]["not_worse"])

    def test_measured_texts_are_current(self):
        meta = read(RUN / "metadata.yaml")
        draft = ROOT / "prompts/drafts/bcreq-review-validation-oneshot.md"
        v01 = ROOT / "prompts/bcreq-review-validation-oneshot.md"
        self.assertEqual(sha256(draft), self.metrics["D"]["prompt_sha256"], "черновик Ш-В изменён после RUN-0080")
        self.assertEqual(sha256(v01), self.metrics["A"]["prompt_sha256"], "v0.1 Ш-В изменён после RUN-0080")
        self.assertIn(self.metrics["D"]["prompt_sha256"], meta)
        self.assertIn(self.metrics["A"]["prompt_sha256"], meta)

    def test_report_records_decision(self):
        report = flat(read(RUN / "outputs/golden-set-report.md"))
        self.assertIn("«П-Ш-В»", report)
        self.assertIn("в `prompts/` в этом PR не переносится", report)


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
        self.assertRegex(text, r"(?m)^version: 0\.6$")
        self.assertIn("### Поправка 0.6: решение Р-15 и промпты шагов (issue #438)", text)
        for dec in ("DEC-427-04", "DEC-427-12"):
            self.assertRegex(text, rf"(?m)^\| {dec}\. [^|]+\| `accepted` \| Р-15 \(\[#438\]")

    def test_backlog_rows(self):
        text = read(BACKLOG)
        self.assertRegex(text, r"(?m)^\| \*\*Р-15\*\* \|.*\| принято \(\[issue #438\]")
        r16 = re.search(r"(?m)^\| \*\*Р-16\*\* \|.*\| (\S+) \|$", text).group(1)
        for task in ("BL-156", "BL-157"):
            row = re.search(rf"(?m)^\| {task} \|.*$", text).group(0)
            cells = [c.strip() for c in row.strip("|").split("|")]
            self.assertEqual(cells[4], "review", task)
            self.assertIn("PR #439", cells[5], task)
            self.assertIn("остаток", cells[7], task)
        v433 = load("v433_for_438", ROOT / "scripts/validate_issue_433_gate_types.py")
        self.assertEqual(v433.R16_ACCEPTED, r16 != "ждёт", "Р-16 и R16_ACCEPTED расходятся")

    def test_cards(self):
        text = read(TRACK_B)
        for task in ("BL-156", "BL-157"):
            card = re.search(rf"(?ms)^### {task}\..*?(?=^### )", text).group(0)
            self.assertIn("**Исполнение.** Issue #438, PR #439", card, task)
            self.assertIn("Остаток:", card, task)
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


if __name__ == "__main__":
    sys.exit(0 if unittest.main(exit=False, verbosity=1).result.wasSuccessful() else 1)
