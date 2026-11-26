#!/usr/bin/env python3
"""Issue #506: готовность runtime к этапу 2 (IDE), RFC-RT-003 и ADR-020.

Задача — исследование и RFC без правок runtime. Проверяет без LLM, без сети
и без клона runtime:

* аудит: frontmatter (``type: audit``, вердикт), разделы ФТ-1…ФТ-3,
  указатели sha256 на экспорт диалога и чат прогона 1143, 56 проблем
  П-1143-NN без пропусков, классы A/B/C и счётчики вердикта сходятся с
  таблицей, распределение раздела 4.4 совпадает с классами;
* RFC-RT-003: ``status: proposed``, ``type: rfc``, обязательные разделы ФТ-4,
  карта гейтов этапа 1, решения Р-RT-10…Р-RT-N без пропусков и повторов,
  задача runtime описана, но не создана;
* ADR-020: ``status: proposed`` и разделы ADR;
* реестр RFC: строка RFC-RT-003 и запись журнала;
* бэклог: строка и карточка BL-244 ``review``, BL-192 остаётся
  ``deferred (triggered)``, цепочка #506 с пометкой «в бэклоге задачи нет»;
* клиентские данные не коммитятся: в документах задачи нет длинных цитат
  из чата и e-mail, только sha256 и указатель;
* тексты промптов, SHA реестра runtime и сайт не менялись: коммиты задачи
  (``issue-506`` в сообщении) не трогают ``prompts/``,
  ``standards/bcreq-runtime-references.md`` и ``site/``.
"""
import re
import subprocess
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs/audit/2026-11-26-runtime-stage2-ide-readiness.md"
RFC = ROOT / "docs/rfc/2026-11-runtime-ide-orchestrator.md"
ADR = ROOT / "docs/adr/2026-11-adr-020-ide-orchestrator-runtime.md"
REGISTRY = ROOT / "docs/rfc/rfc-registry.md"
BACKLOG = ROOT / "pr-ops/BACKLOG.md"
REPOSITORY = ROOT / "pr-ops/backlog-repository.md"
MODEL = ROOT / "pr-ops/backlog-ba-model.md"
EXPERIMENT = ROOT / "experiments/issue_506"

ISSUE = "https://github.com/G-Ivan-A/mango_ba_prompts/issues/506"
CARD = "BL-244"
CARD_TITLE = "RFC IDE-слоя runtime для этапа 2: оркестратор, гейты, MCP"
DIALOG_SHA = "07696b3792caace5f8c0ea2d42e2829036d6383ef36cfbe6de2a5991f47df7af"
CHAT_SHA = "ecfc81cfff4f50a9d4bdb0a9eaa314e8e9d30fbeeec69a1c010020e1768fb2ac"
PROBLEMS = 56

AUDIT_SECTIONS = [
    "## Summary / BLUF",
    "## 1. Источники и их приоритет",
    "## 2. Gap'ы runtime под целевую модель (ФТ-1)",
    "## 3. Предшествующие задачи (ФТ-2)",
    "## 4. Прогон 1143 (ФТ-3)",
    "### 4.2. Реестр проблем",
    "### 4.4. Распределение в работу",
    "## 5. Пределы",
]
# ФТ-4 #506: структура, карта шагов и гейтов, контракт, MCP, миграция, Р-RT.
RFC_SECTIONS = [
    "## Summary / BLUF",
    "## 1. Постановка и границы",
    "## 4. Целевая структура runtime (ФТ-4)",
    "## 5. Карта автономных шагов и гейтов (ФТ-4)",
    "## 6. Контракт оркестратора и подтверждений (ФТ-4)",
    "## 7. Топология MCP и разрешений (ФТ-4)",
    "## 8. Миграция и откат (ФТ-4)",
    "## 9. Решения на согласование",
    "## 10. Движение по бэклогу",
    "## 11. Задача runtime (описана, не создана)",
]
ADR_SECTIONS = [
    "## Статус",
    "## Контекст",
    "## Решение",
    "## Что не менялось",
    "## Последствия",
    "## Альтернативы",
]
# Гейты этапа 1 («Решения гейтов» bcreq-manual-process.md) и нормы,
# которые IDE-слой не ослабляет.
GATES = ("AIN-21", "Г-IN", "Г-С1", "Г-W", "Выпуск")
NORMS = ("Р-09", "Р-19", "ACCESS_GAP")
# Технические шаги этапа 1: только они идут автономно.
TECHNICAL = ("Ш-0", "AIN-01", "AIN-03", "AIN-04", "AIN-05", "AIN-06", "AIN-07",
             "AIN-08", "AIN-09", "AIN-10", "AIN-12", "AIN-15", "AIN-19", "AIN-22")
RT_DECISION = re.compile(r"^\| Р-RT-(\d+) \|", re.M)
MIGRATION_STEP = re.compile(r"^\| \*\*(M\d)\*\* \|", re.M)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not match:
        return {}
    fields = {}
    for line in match.group(1).splitlines():
        key, sep, value = line.partition(":")
        if sep and not line.startswith(" "):
            fields[key.strip()] = value.strip().strip('"')
    return fields


def section(text: str, heading: str) -> str:
    """Текст раздела от заголовка до следующего заголовка того же уровня."""
    level = heading.split(" ", 1)[0]
    start = text.index(heading + "\n")
    rest = text[start + len(heading) :]
    match = re.search(rf"^{level} ", rest, re.M)
    return rest[: match.start()] if match else rest


def cells(line: str) -> list[str]:
    return [cell.strip().strip("*").strip() for cell in line.strip().strip("|").split("|")]


def problems(text: str) -> list[tuple[str, str, str]]:
    """Строки реестра 4.2: (номер, класс, элементы IDE); критичные — жирным."""
    rows = []
    for line in text.splitlines():
        if re.match(r"^\| \**П-1143-\d{2}\** \|", line):
            row = cells(line)
            rows.append((row[0].removeprefix("П-1143-"), row[4], row[5]))
    return rows


def steps(cell: str) -> list[str]:
    """Коды шагов в ячейке; диапазон «AIN-03…AIN-10» раскрывается."""
    found = []
    for first, last in re.findall(r"AIN-(\d{2})…AIN-(\d{2})", cell):
        found += [f"AIN-{n:02d}" for n in range(int(first), int(last) + 1)]
    cell = re.sub(r"AIN-\d{2}…AIN-\d{2}", "", cell)
    return found + re.findall(r"Ш-0|AIN-\d{2}", cell)


class AuditTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = read(AUDIT)
        cls.meta = frontmatter(cls.text)
        cls.rows = problems(cls.text)

    def test_frontmatter(self):
        self.assertEqual(self.meta.get("type"), "audit")
        self.assertEqual(self.meta.get("source"), ISSUE)
        for key in ("status", "version", "updated", "owner", "verdict", "evidence_model"):
            self.assertIn(key, self.meta, key)

    def test_sections(self):
        for heading in AUDIT_SECTIONS:
            with self.subTest(heading=heading):
                self.assertRegex(self.text, rf"(?m)^{re.escape(heading)}$")

    def test_sha256_pointers(self):
        """Экспорт диалога и чат 1143 — только sha256 и указатель."""
        self.assertIn(DIALOG_SHA, self.text)
        self.assertIn(CHAT_SHA, self.text)
        self.assertRegex(self.text, r"issues/506#issuecomment-\d{6,}")

    def test_gaps_have_locators(self):
        gaps = section(self.text, "## 2. Gap'ы runtime под целевую модель (ФТ-1)")
        ids = re.findall(r"^\| (RT-\d{2}) \|", gaps, re.M)
        self.assertGreaterEqual(len(ids), 10)
        self.assertEqual(len(ids), len(set(ids)), "дубли RT-NN")
        self.assertEqual(ids, [f"RT-{n:02d}" for n in range(1, len(ids) + 1)])

    def test_problems_numbered_without_gaps(self):
        numbers = [int(number) for number, _, _ in self.rows]
        self.assertEqual(numbers, list(range(1, PROBLEMS + 1)))
        for _, cls, _ in self.rows:
            self.assertIn(cls, ("A", "B", "C"))

    def test_critical_gate_problems(self):
        """П-1143-38 и П-1143-44 — ложный допуск на гейтах AIN-21 и Г-IN."""
        for number, gate in (("38", "AIN-21"), ("44", "Г-IN")):
            with self.subTest(problem=number):
                line = re.search(rf"(?m)^\| \*\*П-1143-{number}\*\* \|.*$", self.text)
                self.assertIsNotNone(line)
                self.assertIn(gate, line.group(0))
                self.assertIn("Критично", line.group(0))

    def test_verdict_counts_match_table(self):
        classes = Counter(cls for _, cls, _ in self.rows)
        config = classes["A"] + classes["C"]
        prompt = classes["B"] + classes["C"]
        verdict = self.meta["verdict"]
        self.assertIn(f"{config} из {PROBLEMS}", verdict)
        self.assertIn(f"{prompt} требуют правки промптов", verdict)
        self.assertIn(f"{classes['C']} — и то и другое", verdict)

    def test_distribution_matches_classes(self):
        part = section(self.text, "### 4.4. Распределение в работу")
        by_class = {
            cls: sorted(number for number, row_cls, _ in self.rows if row_cls == cls)
            for cls in "ABC"
        }
        for line in part.splitlines():
            match = re.match(r"^\| .*?\| ([ABC]) \((\d+)\) \| ([\d, ]+) \|", line)
            if not match:
                continue
            cls, count, listed = match.groups()
            listed = sorted(item.strip() for item in listed.split(","))
            with self.subTest(cls=cls):
                self.assertEqual(int(count), len(by_class[cls]))
                self.assertEqual(listed, by_class[cls])
        self.assertIn("#505", part)

    def test_ide_elements_known(self):
        for number, _, elements in self.rows:
            with self.subTest(problem=number):
                found = re.findall(r"E\d", elements)
                self.assertTrue(found)
                self.assertTrue(set(found) <= {f"E{n}" for n in range(1, 7)}, elements)


class RfcTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = read(RFC)
        cls.meta = frontmatter(cls.text)

    def test_frontmatter(self):
        self.assertEqual(self.meta.get("status"), "proposed")
        self.assertEqual(self.meta.get("type"), "rfc")
        self.assertEqual(self.meta.get("source"), ISSUE)
        self.assertIn("rfc-scope", self.meta)

    def test_title(self):
        self.assertIn("# RFC-RT-003: ", self.text)

    def test_sections(self):
        for heading in RFC_SECTIONS:
            with self.subTest(heading=heading):
                self.assertRegex(self.text, rf"(?m)^{re.escape(heading)}$")

    def test_gate_map_keeps_stage1_norms(self):
        part = section(self.text, "## 5. Карта автономных шагов и гейтов (ФТ-4)")
        for needle in GATES + NORMS:
            with self.subTest(needle=needle):
                self.assertIn(needle, part)

    def test_only_technical_steps_are_autonomous(self):
        """Карта 5.2: тип T ровно у 14 технических шагов, AIN-01…24 все на месте."""
        table = section(self.text, "### 5.2. A-IN (24 шага)")
        autonomous, seen = set(), set()
        for line in table.splitlines():
            if not line.startswith("| ") or line.startswith("| Шаг") or line.startswith("| ---"):
                continue
            row = cells(line)
            codes = steps(row[0])
            seen.update(codes)
            if row[1].startswith("T"):
                autonomous.update(codes)
        self.assertEqual(autonomous, set(TECHNICAL))
        self.assertEqual(seen, {"Ш-0"} | {f"AIN-{n:02d}" for n in range(1, 25)})
        contract = section(self.text, "## 6. Контракт оркестратора и подтверждений (ФТ-4)")
        for needle in ("decisions.jsonl", "LE-04", "Продолжаем?"):
            with self.subTest(needle=needle):
                self.assertIn(needle, contract)

    def test_mcp_read_only(self):
        part = section(self.text, "## 7. Топология MCP и разрешений (ФТ-4)")
        for needle in ("deny", "disabled", "ACCESS_GAP"):
            with self.subTest(needle=needle):
                self.assertIn(needle, part)

    def test_migration_has_rollback(self):
        part = section(self.text, "## 8. Миграция и откат (ФТ-4)")
        stages = MIGRATION_STEP.findall(part)
        self.assertEqual(stages, [f"M{n}" for n in range(len(stages))])
        self.assertGreaterEqual(len(stages), 6)
        self.assertIn("| Откат |", part)

    def test_decisions_numbered_without_gaps(self):
        numbers = [int(number) for number in RT_DECISION.findall(self.text)]
        self.assertGreaterEqual(len(numbers), 5)
        self.assertEqual(numbers, list(range(10, 10 + len(numbers))))

    def test_runtime_task_described_not_created(self):
        part = section(self.text, "## 11. Задача runtime (описана, не создана)")
        self.assertIn("BL-192 Э5", part)
        self.assertIn("**Готово, когда.**", part)
        self.assertNotRegex(part, r"mango-ba-ai-runtime/issues/(?!25\b|27\b)\d+")

    def test_backlog_chain(self):
        part = section(self.text, "## 10. Движение по бэклогу")
        for needle in (CARD, "BL-192", "BL-185", "BL-242", "BL-243", "ADR-020",
                       "BL-194", "issues/509"):
            with self.subTest(needle=needle):
                self.assertIn(needle, part)
        # Постусловие #506: прогоны M6 — «в бэклоге задачи нет, будет создана».
        self.assertIn("Задачи в бэклоге нет, будет создана", part)


class AdrTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = read(ADR)
        cls.meta = frontmatter(cls.text)

    def test_frontmatter(self):
        self.assertEqual(self.meta.get("status"), "proposed")
        self.assertIn("decision-type", self.meta)

    def test_title_and_sections(self):
        self.assertIn("# ADR-020: ", self.text)
        for heading in ADR_SECTIONS:
            with self.subTest(heading=heading):
                self.assertRegex(self.text, rf"(?m)^{re.escape(heading)}$")

    def test_links_rfc_and_audit(self):
        self.assertIn("../rfc/2026-11-runtime-ide-orchestrator.md", self.text)
        self.assertIn("../audit/2026-11-26-runtime-stage2-ide-readiness.md", self.text)


class RegistryTest(unittest.TestCase):
    def test_row_and_journal(self):
        text = read(REGISTRY)
        self.assertRegex(text, r"(?m)^\| \[RFC-RT-003\]\(2026-11-runtime-ide-orchestrator\.md\) \|.*`proposed`")
        self.assertIn("2026-11-runtime-ide-orchestrator.md", text)
        self.assertRegex(text, r"(?m)^- \*\*2026-11-26\*\* — issue #506")


class BacklogTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.backlog = read(BACKLOG)
        cls.repository = read(REPOSITORY)
        cls.model = read(MODEL)

    def test_card_and_row(self):
        self.assertIn(f"### {CARD}. {CARD_TITLE}", self.repository)
        self.assertRegex(
            self.backlog, rf"(?m)^\| {CARD} \| \[{re.escape(CARD_TITLE)}\]\(backlog-repository\.md#"
        )
        self.assertRegex(self.backlog, rf"(?m)^\| {CARD} \| .*\| review \|")

    def test_bl192_status_unchanged(self):
        self.assertRegex(self.backlog, r"(?m)^\| BL-192 \| .*\| deferred \(triggered\) \|")
        card = self.model.split("### BL-192.", 1)[1].split("\n### ", 1)[0]
        self.assertIn("ADR-020", card)

    def test_chain(self):
        chain = self.backlog.split("**Движение по цепочке (#506).**", 1)[1].split("\n## ", 1)[0]
        for needle in (CARD, "ADR-020", "BL-192", "BL-242", "BL-243", "#505", "BL-194", "#509"):
            with self.subTest(needle=needle):
                self.assertIn(needle, chain)
        # Постусловие #506: «в бэклоге задачи нет, будет создана».
        self.assertIn("в бэклоге задачи нет, будет создана", re.sub(r"\s+", " ", chain))


class ClientDataTest(unittest.TestCase):
    """#506, раздел 6: клиентские данные не коммитятся."""

    FILES = (AUDIT, RFC, ADR)
    EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
    PHONE = re.compile(r"\+7[\s(-]*\d{3}[\s)-]*\d{3}[\s-]*\d{2}[\s-]*\d{2}")

    def files(self):
        yield from self.FILES
        yield from sorted(EXPERIMENT.glob("*"))

    def test_no_personal_data(self):
        for path in self.files():
            text = read(path)
            with self.subTest(path=path.name):
                self.assertIsNone(self.EMAIL.search(text))
                self.assertIsNone(self.PHONE.search(text))

    def test_no_raw_chat_copies(self):
        """Чат и экспорт не лежат в спице: нет больших текстовых файлов задачи."""
        for path in EXPERIMENT.glob("*"):
            with self.subTest(path=path.name):
                self.assertLess(path.stat().st_size, 200_000)
                self.assertNotRegex(path.name, r"(?i)chat|dialog|export|\.zip$")


class ProtectedPathsTest(unittest.TestCase):
    """#506, раздел 6: runtime, тексты промптов и SHA реестра не меняются."""

    def test_issue_commits_do_not_touch_protected_paths(self):
        res = subprocess.run(
            ["git", "log", "--no-merges", "--format=%h %s", "--grep=issue-506", "--",
             "prompts/", "standards/bcreq-runtime-references.md", "site/"],
            cwd=ROOT, capture_output=True, text=True,
        )
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertEqual(res.stdout.strip(), "", "коммиты #506 меняют защищённые пути")


if __name__ == "__main__":
    unittest.main(verbosity=1)
