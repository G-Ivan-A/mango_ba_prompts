#!/usr/bin/env python3
"""Issue #505: прогон 1143, анализ проблем промптов и RFC отладки (BL-193).

Проверяет без LLM, сети и подпроцессов:

* RUN-0096 оформлен по контракту ``runs/README.md``: файлы из ``metadata.yaml``
  существуют, прогон есть в реестре;
* расшифровка чата 1143 не закоммичена (в ней ТЗ Заказчика): в RUN и
  экспериментах нет ``.txt`` и больших файлов, ``chat-signals.json`` хранит
  только числа, номера строк и коды шагов;
* числа замера избыточности в анализе, RFC и ``metadata.yaml`` совпадают с
  ``prompt-redundancy.json``, а сам лог согласован внутри себя;
* анализ содержит ПР-01…ПР-16 и Г-01…Г-08, RFC — правки 2.1–2.12, RG-01…RG-10,
  Р-ОТЛ-1…6 и разделы, которых требует issue (сайт, оба формата, инструкции,
  этап 2);
* RFC зарегистрирован и ссылается на задачу BL-194 (issue #509); бэклог
  показывает BL-193 ``review``, BL-194 ``TODO`` и закрытые BL-230/BL-231.

Лог избыточности — снимок черновиков на момент прогона, поэтому он не
пересчитывается: после правок BL-194 числа изменятся, а история — нет.
"""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "runs/2026/RUN-0096"
ANALYSIS = ROOT / "docs/analysis/2026-11-26-1143-chat-prompt-debugging-analysis.md"
RFC = ROOT / "docs/rfc/2026-11-bcreq-prompt-debugging-1143.md"
SIGNALS = RUN / "logs/chat-signals.json"
REDUNDANCY = RUN / "logs/prompt-redundancy.json"
CHAT_SHA256 = "ecfc81cfff4f50a9d4bdb0a9eaa314e8e9d30fbeeec69a1c010020e1768fb2ac"
ISSUE_509 = "https://github.com/G-Ivan-A/mango_ba_prompts/issues/509"
MAX_FILE_BYTES = 40_000  # расшифровка — 599 651 байт; самый большой файл прогона ~20 КБ


def read(path):
    return Path(path).read_text(encoding="utf-8")


def thousands(n):
    """``17132`` → ``17 132``: так числа записаны в документах."""
    return f"{n:,}".replace(",", " ")


def metadata_list(text, key):
    match = re.search(rf"^{key}:\n((?:  - .+\n)+)", text, re.M)
    return [line[4:].strip() for line in match.group(1).splitlines()] if match else []


def strings(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for key, value in obj.items():
            yield key
            yield from strings(value)
    elif isinstance(obj, list):
        for value in obj:
            yield from strings(value)


class RunRecordTest(unittest.TestCase):
    def setUp(self):
        self.meta = read(RUN / "metadata.yaml")

    def test_required_fields(self):
        for field in ("run_id: RUN-0096", "process:", "version:", "date: 2026-11-26",
                      "author:", "model:", "status:", "run_type: execution"):
            self.assertIn(field, self.meta)

    def test_listed_files_exist(self):
        listed = [p for key in ("inputs", "outputs", "logs", "feedback")
                  for p in metadata_list(self.meta, key)]
        self.assertGreaterEqual(len(listed), 8)
        for rel in listed:
            self.assertTrue((RUN / rel).is_file(), rel)

    def test_related_artifacts_exist(self):
        for rel in metadata_list(self.meta, "related_artifacts"):
            self.assertTrue((ROOT / rel).exists(), rel)

    def test_registered_in_runs_registry(self):
        registry = read(ROOT / "runs/README.md")
        self.assertIn("[`RUN-0096`](2026/RUN-0096/metadata.yaml)", registry)
        for tool in ("experiments/issue_505/chat_signals.py",
                     "experiments/issue_505/prompt_redundancy.py"):
            self.assertIn(f"[`{tool}`]", registry)


class NoTranscriptTest(unittest.TestCase):
    """НФТ-01: в репозиторий попадают только метрики и короткие цитаты."""

    def test_no_text_dumps_or_large_files(self):
        for base in (RUN, ROOT / "experiments/issue_505"):
            for path in base.rglob("*"):
                if not path.is_file():
                    continue
                rel = path.relative_to(ROOT)
                self.assertNotEqual(path.suffix, ".txt", f"{rel}: похоже на расшифровку")
                self.assertLess(path.stat().st_size, MAX_FILE_BYTES, f"{rel}: слишком большой")

    def test_signals_hold_no_chat_text(self):
        data = json.loads(read(SIGNALS))
        self.assertEqual(data["source"]["sha256"], CHAT_SHA256)
        for value in strings(data):
            self.assertLess(len(value), 80, f"строка в логе сигналов: {value[:40]}…")
        for marker in data["step_end_markers"]["markers"]:
            self.assertEqual(set(marker), {"line", "step", "version"})
            self.assertIsInstance(marker["line"], int)
            self.assertRegex(marker["step"], r"^(AIN-\d\d|Ш-\d)$")

    def test_sha_recorded_for_reproduction(self):
        self.assertIn(CHAT_SHA256, read(RUN / "inputs/README.md"))


class MetricsMatchLogsTest(unittest.TestCase):
    def setUp(self):
        self.red = json.loads(read(REDUNDANCY))
        self.sig = json.loads(read(SIGNALS))

    def test_redundancy_log_is_consistent(self):
        files = self.red["per_file"]
        self.assertEqual(len(files), self.red["ain_files"])
        self.assertEqual(self.red["ain_files"], 24)
        self.assertEqual(sum(f["chars"] for f in files), self.red["ain_total_chars"])
        self.assertEqual(sum(f["unique_chars"] for f in files), self.red["ain_unique_chars"])
        self.assertEqual(max(f["shared_chars"] for f in files), self.red["common_block_chars"])
        once = (self.red["ain_unique_chars"] + self.red["common_block_chars"]
                + sum(self.red["route_other_prompts_chars"].values()))
        self.assertEqual(once, self.red["route_total_chars_contract_once"])
        saving = round(1 - once / self.red["route_total_chars_as_pasted"], 3)
        self.assertEqual(saving, self.red["route_saving_share"])

    def test_documents_quote_logged_numbers(self):
        saving = f"−{self.red['route_saving_share'] * 100:.1f}".replace(".", ",") + " %"
        numbers = [thousands(self.red[k]) for k in (
            "common_block_chars", "route_total_chars_as_pasted",
            "route_total_chars_contract_once")]
        for doc in (ANALYSIS, RFC):
            text = read(doc)
            for value in numbers + [saving]:
                self.assertIn(value, text, f"{doc.name}: нет числа {value}")

    def test_metadata_metrics_match_logs(self):
        meta = read(RUN / "metadata.yaml")
        markers = self.sig["step_end_markers"]
        signals = self.sig["signals"]
        expected = {
            "chat_lines": self.sig["source"]["lines"],
            "chat_step_end_markers": markers["total"],
            "chat_distinct_steps": markers["distinct_steps"],
            "chat_repeated_steps": len(markers["repeated_steps"]),
            "chat_access_gap_tokens": signals["access_gap_token"]["count"],
            "chat_web_tool_denied_lines": signals["web_tool_denied_line"]["count"],
            "chat_web_search_traces": signals["web_search_trace"]["count"],
            "chat_memory_packages": signals["memory_package_header"]["count"],
            "chat_sycophancy_lines": signals["flattery_absolutely_right"]["count"],
            "ain_common_block_chars": self.red["common_block_chars"],
            "ain_unique_share_min": self.red["ain_unique_share_min"],
            "ain_unique_share_max": self.red["ain_unique_share_max"],
            "route_chars_as_pasted": self.red["route_total_chars_as_pasted"],
            "route_chars_contract_once": self.red["route_total_chars_contract_once"],
            "route_saving_share": self.red["route_saving_share"],
        }
        for key, value in expected.items():
            self.assertRegex(meta, rf"(?m)^  {key}: {re.escape(str(value))}(\s|$)", key)


class DocumentsTest(unittest.TestCase):
    def test_analysis_lists_problems_and_hypotheses(self):
        text = read(ANALYSIS)
        for n in range(1, 17):
            self.assertIn(f"ПР-{n:02d}", text)
        for n in range(1, 9):
            self.assertIn(f"Г-{n:02d}", text)
        self.assertIn(ISSUE_509, text)

    def test_rfc_covers_issue_requirements(self):
        text = read(RFC)
        self.assertIn("status: proposed", text)
        for heading in ("## 2. Какие промпты правим и как", "## 3. Избыточный контент",
                        "## 4. Как сохраняются оба формата шагов",
                        "## 5. Как обновляются инструкции", "## 6. Предложения по сайту",
                        "## 7. Перенос практики на этап 2 (OpenCode)", "## 9. Проверка",
                        "## 10. Решения владельца"):
            self.assertIn(heading, text)
        for n in range(1, 13):
            self.assertRegex(text, rf"(?m)^\| 2\.{n} \|", f"правка 2.{n}")
        for n in range(1, 11):
            self.assertIn(f"RG-{n:02d}", text)
        for n in range(1, 7):
            self.assertIn(f"Р-ОТЛ-{n}", text)
        self.assertIn(ISSUE_509, text)

    def test_rfc_registered(self):
        registry = read(ROOT / "docs/rfc/rfc-registry.md")
        self.assertIn("[RFC-BCREQ-PROMPT-DEBUG-001](2026-11-bcreq-prompt-debugging-1143.md)", registry)


class BacklogTest(unittest.TestCase):
    def setUp(self):
        self.backlog = read(ROOT / "pr-ops/BACKLOG.md")

    def row(self, bl):
        match = re.search(rf"(?m)^\| {bl} \|.*$", self.backlog)
        self.assertIsNotNone(match, f"нет строки {bl}")
        return [cell.strip() for cell in match.group(0).split("|")[1:-1]]

    def test_chain_statuses(self):
        self.assertEqual(self.row("BL-193")[4], "review")
        self.assertEqual(self.row("BL-194")[4], "TODO")
        self.assertIn(ISSUE_509, self.row("BL-194")[5])
        self.assertEqual(self.row("BL-230")[4], "DONE")
        self.assertEqual(self.row("BL-231")[4], "DONE")

    def test_cards_exist(self):
        model = read(ROOT / "pr-ops/backlog-ba-model.md")
        self.assertIn("### BL-193. Прогон 1143: проблемы промптов и RFC отладки", model)
        self.assertIn("### BL-194. Отладка и оптимизация промптов BCREQ по "
                      "RFC-BCREQ-PROMPT-DEBUG-001", model)


if __name__ == "__main__":
    unittest.main()
