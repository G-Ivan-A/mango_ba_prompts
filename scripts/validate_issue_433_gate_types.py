#!/usr/bin/env python3
"""Регрессионная проверка типа гейта во всех документах проекта (issue #433, BL-159).

Проверка закрепляет результат сквозной актуализации терминологии гейтов:

* поиск «human gate», «G-human», «человеческий гейт», «решение человека»,
  «подтверждение человека», «human-in-the-loop» в активных документах
  находит гейт без типа только в местах из списка ``ALLOW`` — у каждого
  места есть категория и причина (A — ждёт Р-16, N — не гейт процесса,
  T — пакет для Хаба, O — идентификатор другого источника, H — история,
  P — промпты, BL-156б: RUN-0081 не подтвердил правку, issue #444). Новое место без типа ломает проверку; исключение,
  которого больше нет в тексте, тоже ломает её — список не устаревает;
* ADR-003 и онтология: поправка 0.2 — проект, ждёт Р-16. Пока
  ``R16_ACCEPTED = False``, ADR-003 остаётся версией 0.1 с пометкой
  «проект»; после ответа владельца (BL-162) константа меняется на
  ``True`` и проверка требует версию 0.2 без пометки;
* решение Р-16 в BACKLOG, задачи BL-162 и BL-161 — строки и карточки;
* журнал К-34: поля ``gate_id``, ``gate_type``, ``model_recommendation``,
  ``divergence`` в стандарте класса, каталоге и правиле Г3 контракта;
* К-20 называется «Подготовка доказательств гейта»;
* строка самопроверки во всех 39 стандартах классов называет гейты с
  решением человека с типом;
* стандарт процесса и ADR-009 не связывают гейт с моделью
  «молчание = согласие» (правило 4 словаря потока);
* карта процессов ``00-index.md``: каждый «Gate» в колонке «Gate / gap»
  несёт тип, равный исполнителю операции строки (С3 онтологии).

Запуск: ``python3 scripts/validate_issue_433_gate_types.py``
"""

import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADR003 = ROOT / "docs/adr/003-ba-ontology.md"
ADR009 = ROOT / "docs/adr/009-bcreq-formation-process.md"
ONTOLOGY = ROOT / "standards/ba-ontology.md"
ONTOLOGY_EXEC = ROOT / "standards/ba-ontology.executable.md"
PROCESS_STANDARD = ROOT / "standards/bcreq-process-standard.md"
GATES = ROOT / "docs/contracts/bcreq-stage-gates.md"
CLASSES = ROOT / "standards/bcreq-manual-classes"
CATALOG = CLASSES / "catalog.json"
INDEX = ROOT / "docs/ba-processes/00-index.md"
BACKLOG = ROOT / "pr-ops/BACKLOG.md"
TRACK_B = ROOT / "pr-ops/backlog-ba-model.md"
INVENTORY = ROOT / "docs/analysis/2026-11-03-gate-types-bl-159-inventory.md"

# Р-16 (BL-162): после ответа владельца «Р-16 да» поменять на True вместе с
# применением поправки 0.2 ADR-003 и онтологии.
R16_ACCEPTED = False

GATE_WORDS = re.compile(
    r"human[ -]gate|G-human|человеческ(?:ий|ого|ие|их|ому|им) гейт"
    r"|решени[еяю] человека|подтверждени[яе] человека|human-in-the-loop",
    re.IGNORECASE,
)
TYPED = re.compile(r"`(?:человек|гибрид|llm|код)`|тип гейта|типа? `|ключев", re.IGNORECASE)
HISTORICAL = re.compile(
    r"^(docs/analysis/|docs/audit/|runs/|experiments/|site/data/|prompts/archive/"
    r"|pr-ops/archive/|CHANGELOG|node_modules/)"
)
WINDOW = 2

# Место без типа → (категория, причина). Ключ — путь и фрагмент строки
# (не номер строки: номера сдвигаются при правках выше по файлу).
ALLOW = {
    # A — носитель определения «Контрольной точки»; меняется поправкой 0.2 (Р-16 → BL-162).
    ("docs/adr/003-ba-ontology.md", "(human gate)"): ("A", "схема §1, ждёт Р-16"),
    ("docs/adr/003-ba-ontology.md", "требует подтверждения человека"): ("A", "определение §2, ждёт Р-16"),
    ("docs/adr/003-ba-ontology.md", "на модель human-gate из"): ("A", "§3, ждёт Р-16"),
    ("docs/adr/003-ba-ontology.md", "Обязательный human gate"): ("A", "столбец §4, ждёт Р-16"),
    ("docs/adr/003-ba-ontology.md", "Переходы через **human gate**"): ("A", "§6, ждёт Р-16"),
    # N — не гейт процесса BCREQ: механизм проверки операции из DoD Хаба
    # (строку требует валидатор issue #263), приёмка PR/RFC, порог метрики.
    ("README.md", "human-in-the-loop gate."): ("N", "механизм проверки операции, DoD Хаба"),
    ("README.md", "human-in-the-loop gate в репозитории есть"): ("N", "механизм проверки операции"),
    ("ai-governance/ai-governance.md", "чек-лист или human-in-the-loop gate, иначе"): ("N", "DoD Хаба"),
    ("ai-governance/ai-governance.md", "evals-метрика или human-in-the-loop gate); операция"): ("N", "DoD Хаба"),
    ("ai-governance/ai-governance.md", "чек-лист или human-in-the-loop gate; ссылка"): ("N", "DoD Хаба"),
    ("docs/adr/0004-hub-resync-2026-08.md", "Качество системы исполнения"): ("N", "DoD Хаба"),
    ("docs/rfc-hub-integration.md", "evals-метрика или human-in-the-loop gate);"): ("N", "DoD Хаба"),
    ("docs/rfc-hub-integration.md", "чек-лист или human-in-the-loop gate."): ("N", "DoD Хаба"),
    ("ai-rules/agent-onboarding-protocol.md", "без решения человека"): ("N", "структура репозитория, не гейт"),
    ("ai-rules/agent-work-rules.md", "не переопределяет решение человека"): ("N", "полномочия агента"),
    ("docs/rfc/rfc-process.md", "предсказуемый путь до решения человека"): ("N", "приёмка RFC"),
    ("docs/rfc/rfc-process.md", "право даёт только решение человека"): ("N", "приёмка RFC"),
    ("docs/rfc/rfc-process.md", "только по решению человека"): ("N", "статус RFC"),
    ("standards/evals-contract-standard.md", "Порог — решение человека"): ("N", "порог метрики"),
    ("standards/evals-contract-standard.md", "требуют решения человека"): ("N", "границы стандарта evals"),
    ("docs/rfc/2026-10-ba-automation-strategy.md", "продукта или решение человека"): ("N", "вердикт «нет данных»"),
    ("docs/rfc/2026-10-ba-automation-strategy.md", "те же решения человека"): ("N", "детерминированность"),
    # T — пакет передачи знаний в Хаб, заморожен решением #413 (→ BL-122).
    ("docs/rfc/knowledge-transfer-to-hub/README.md", "(human gates)"): ("T", "BL-122"),
    ("docs/rfc/knowledge-transfer-to-hub/bcreq-process.md", "(human gates)"): ("T", "BL-122"),
    ("docs/rfc/knowledge-transfer-to-hub/bcreq-process.md", "human-in-the-loop и без"): ("T", "BL-122"),
    ("docs/rfc/knowledge-transfer-to-hub/bcreq-process.md", "типизированные human gates"): ("T", "BL-122"),
    ("docs/rfc/knowledge-transfer-to-hub/bcreq-process.md", "точками решения человека"): ("T", "BL-122"),
    ("docs/rfc/rfc-to-hub-001-knowledge-transfer.md", "(human gates)"): ("T", "BL-122"),
    ("docs/rfc/rfc-to-hub-001-knowledge-transfer.md", "BCREQ hum"): ("T", "BL-122"),
    # O — идентификатор или термин другого источника.
    ("docs/hub-research-dependencies.md", "`human gate`)"): ("O", "пробелы исследования Хаба"),
    ("standards/bcreq-runtime-references.md", "G-human"): ("O", "файл runtime g-human-checklist.md"),
    ("standards/bcreq-runtime-references.md", "| ТС-3 |"): ("O", "ссылка на g-human-checklist.md"),
    ("docs/rfc/2026-11-bcreq-flow-processes-prompts.md", "g-human-checklist.md"): ("O", "файл runtime"),
    # Черновик Ш-В (BL-156, #438): имя справочника И-8 из реестра runtime, раздел 2;
    # текст черновика меняется только пересборкой (измерен RUN-0080, после BL-156а — RUN-0081).
    ("prompts/drafts/bcreq-review-validation-oneshot.md", "Чек-лист гейта G-human"): ("O", "имя И-8 из реестра runtime"),
    ("standards/bcreq-flow-glossary.md", "G-self → G-mach → G-human"): ("O", "порядок гейтов узла runtime"),
    ("docs/rfc/2026-10-standards-page-rfc.md", "ждёт решения человека на гейтах. | план |"):
        ("O", "порождаемое приложение: источник experiments/issue_420/site-v2/content.py, "
              "валидатор #420 сверяет его с build.py побайтно"),
    # H — история, цитата «было», прежнее имя.
    ("standards/bcreq-flow-glossary.md", "Было в RFC #427"): ("H", "цитата «было»"),
    ("standards/bcreq-manual-classes/catalog.json", '"name": "Подготовка доказательств человеческого гейта"'):
        ("H", "прежнее имя К-20 в history.previous_fields"),
    ("standards/bcreq-manual-classes/catalog.json", 'до исправления и решения человека."'):
        ("H", "прежний stop К-33 в history.previous_fields"),
    ("standards/bcreq-manual-classes/catalog.json", '"behavior": "Записывать только явное решение человека'):
        ("H", "прежний behavior К-34 в history.previous_fields"),
    ("pr-ops/backlog-ba-model.md", "«human gate» или «решение человека» без типа"): ("H", "BL-159, «Почему»"),
    ("pr-ops/backlog-ba-model.md", "поиском «human gate»"): ("H", "BL-159, метод поиска"),
    ("pr-ops/backlog-ba-model.md", "«человеческий гейт», «решение человека»."): ("H", "BL-159, метод поиска"),
    ("pr-ops/backlog-ba-model.md", "«решение человека» — порог метрики"): ("H", "BL-159, итог пункта"),
    ("docs/report/2026-10-31-repository-action-plan.md", "узлом ожидания решения человека"): ("H", "отчёт на дату"),
    ("docs/rfc/2026-08-task-taxonomy.md", "Human Gate"): ("H", "исторический RFC"),
    ("docs/rfc/2026-10-bcreq-manual-pipeline.md", "Человеческие гейты"): ("H", "исторический RFC"),
    ("docs/rfc/2026-10-repository-modernization.md", "решение человека"): ("H", "исторический RFC"),
    ("docs/rfc/2026-10-repository-modernization.md", "узел ожидания решения человека"): ("H", "принятый RFC, требования ADR-017"),
    ("docs/rfc/2026-10-repository-modernization.md", "запись решения человека"): ("H", "принятый RFC"),
    # P — промпты; DEC-427-11 запрещает правку без замера «не хуже» RUN-0079.
    # Заготовка правки — experiments/issue_438/prompt-typing.json (PR #439).
    # RUN-0081 (BL-156а, issue #444) измерил её: ядро 9/11 против 10/11
    # RUN-0079, правка перенесена в BL-156б.
    ("prompts/bcreq-constitution-governance-oneshot.md", "| CB-0.5 |"): ("P", "BL-156б"),
    ("prompts/drafts/bcreq-constitution-governance-oneshot.md", "| CB-0.5 |"): ("P", "BL-156б"),
    ("prompts/", "заменить отсутствующее решение человека"): ("P", "BL-156б"),
}
CATEGORIES = {"A", "N", "T", "O", "H", "P"}

# Тип гейта в колонке «Gate / gap» карты процессов = исполнитель операции (С3).
EXECUTOR = {
    "ingestion": "llm", "modeling": "llm", "documentation": "llm",
    "understanding": "гибрид", "validation": "гибрид", "solution_design": "гибрид",
    "quality": "гибрид", "research": "гибрид", "impact_analysis": "гибрид",
    "reverse_requirements": "гибрид",
    "governance": "человек", "risk_analysis": "человек", "release_readiness": "человек",
}


def text(path):
    return path.read_text(encoding="utf-8")


def tracked_files():
    result = subprocess.run(
        ["git", "ls-files", "*.md", "*.json", "*.yaml", "*.yml"],
        cwd=ROOT, capture_output=True, text=True, check=True,
    )
    return [f for f in result.stdout.split() if not HISTORICAL.match(f)]


def untyped_hits(files=None):
    """Места с гейтом без типа в окне ±WINDOW строк: [(путь, номер, строка)]."""
    hits = []
    for name in files if files is not None else tracked_files():
        path = ROOT / name
        if not path.is_file():
            continue
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        for i, line in enumerate(lines):
            if GATE_WORDS.search(line):
                window = "\n".join(lines[max(0, i - WINDOW): i + WINDOW + 1])
                if not TYPED.search(window):
                    hits.append((name, i + 1, line))
    return hits


def allowed(name, line):
    for (prefix, fragment) in ALLOW:
        if (name == prefix or (prefix.endswith("/") and name.startswith(prefix))) and fragment in line:
            return (prefix, fragment)
    return None


def section(body, heading):
    start = body.index(heading)
    nxt = re.search(r"^#{2,3} ", body[start + len(heading):], re.MULTILINE)
    return body[start: start + len(heading) + nxt.start()] if nxt else body[start:]


class UntypedGateTest(unittest.TestCase):
    def test_every_untyped_place_is_allowed(self):
        rogue = [f"{n}:{i}: {line.strip()[:160]}" for n, i, line in untyped_hits() if not allowed(n, line)]
        self.assertEqual(rogue, [], "гейт без типа — назовите тип (`человек`, `гибрид`, `llm`, `код`) "
                                   "или добавьте место в ALLOW с категорией и причиной")

    def test_allow_list_has_no_stale_entries(self):
        used = {allowed(n, line) for n, _, line in untyped_hits()}
        stale = [key for key in ALLOW if key not in used]
        self.assertEqual(stale, [], "исключение больше не нужно — удалите его из ALLOW")

    def test_allow_list_categories_and_reasons(self):
        for key, (category, reason) in ALLOW.items():
            self.assertIn(category, CATEGORIES, key)
            self.assertTrue(reason.strip(), key)

    def test_detector_catches_new_untyped_gate(self):
        sample = ROOT / "experiments/issue_433/fixture_untyped_gate.md"
        self.assertTrue(sample.is_file(), "нужен файл-образец гейта без типа")
        hits = untyped_hits(["experiments/issue_433/fixture_untyped_gate.md"])
        self.assertEqual([i for _, i, _ in hits], [3], hits)


class OntologyR16Test(unittest.TestCase):
    def test_adr003_amendment_prepared(self):
        body = text(ADR003)
        self.assertIn("## Поправка 0.2: тип гейта", body)
        amendment = section(body, "## Поправка 0.2: тип гейта")
        for needle in ("Р-16 да", "**Варианты Р-16:**", "Было (0.1)", "Станет (0.2)", "`код`",
                       "молчание — не согласие", "ADR-0003"):
            self.assertIn(needle, amendment)

    def test_adr003_state_matches_r16(self):
        body = text(ADR003)
        version = re.search(r"^version: (\S+)$", body, re.MULTILINE).group(1)
        if R16_ACCEPTED:
            self.assertEqual(version, "0.2")
            self.assertNotIn("проект, ждёт Р-16", body)
            self.assertNotIn("подготовлена, не принята", body)
        else:
            self.assertEqual(version, "0.1", "ADR-003 0.2 — только после «Р-16 да» (BL-162)")
            self.assertIn("## Поправка 0.2: тип гейта (проект, ждёт Р-16)", body)
            self.assertIn("**Поправка 0.2 подготовлена, не принята (BL-159, issue #433).**", body)

    def test_ontology_points_to_glossary(self):
        for path in (ONTOLOGY, ONTOLOGY_EXEC):
            body = text(path)
            self.assertIn("bcreq-flow-glossary.md", body, path.name)
            for t in ("`человек`", "`гибрид`", "`llm`", "`код`"):
                self.assertIn(t, body, path.name)
        if not R16_ACCEPTED:
            self.assertIn("только решением владельца Р-16", text(ONTOLOGY))

    def test_backlog_r16_and_tasks(self):
        backlog = text(BACKLOG)
        self.assertIn("| **Р-16** |", backlog)
        # Р-16 входит в общий диапазон решений; следующие PR могут продлить его (Р-17 — PR #437).
        self.assertRegex(backlog, r"Р-01…Р-(1[6-9]|[2-9]\d)")
        for task in ("BL-159", "BL-161", "BL-162"):
            self.assertRegex(backlog, re.compile(rf"^\| {task} \| \[", re.MULTILINE), task)
        track = text(TRACK_B)
        self.assertIn("### BL-162. Поправка 0.2 ADR-003: тип гейта в онтологии", track)
        self.assertIn("### BL-161. Журнал К-34 по Г-IN и решение о типе гейта", track)
        self.assertIn("R16_ACCEPTED", section(track, "### BL-162."))

    def test_bl159_checklist_closed_or_moved(self):
        card = section(text(TRACK_B), "### BL-159.")
        items = re.findall(r"^- \[([ x])\] ", card, re.MULTILINE)
        self.assertGreaterEqual(len(items), 8)
        self.assertNotIn(" ", items, "каждый пункт BL-159 отмечен или перенесён в карточку-владельца")
        for moved in ("BL-161", "BL-162", "BL-156", "BL-122"):
            self.assertIn(moved, card)
        self.assertIn("2026-11-03-gate-types-bl-159-inventory.md", card)
        self.assertTrue(INVENTORY.is_file())


class JournalAndClassesTest(unittest.TestCase):
    FIELDS = ("gate_id", "gate_type", "model_recommendation", "divergence")

    def test_k34_fields(self):
        for path in (CLASSES / "34-human-record.md", CATALOG, GATES):
            body = text(path)
            for field in self.FIELDS:
                self.assertIn(field, body, f"{path.name}: {field}")
        gates = text(GATES)
        rule = gates[gates.index("**Правило Г3 (журнал).**"):]
        rule = rule[: rule.index("\n- **", 1) if "\n- **" in rule else len(rule)]
        for field in self.FIELDS:
            self.assertIn(f"`{field}`", rule, f"правило Г3: {field}")

    def test_k34_gate_sentence_once(self):
        # Регрессия: повторный прогон experiments/issue_433/apply_class_gate_types.py
        # дописывал фразу журнала гейта в стандарт К-34 второй раз.
        sentence = "Для решения гейта записать gate_id и gate_type"
        self.assertEqual(text(CLASSES / "34-human-record.md").count(sentence), 1)
        catalog = json.loads(text(CATALOG))
        classes = catalog["classes"] if isinstance(catalog, dict) else catalog
        k34 = next(c for c in classes if c.get("id") == "К-34")
        self.assertEqual(k34["behavior"].count(sentence), 1)
        # Базовый стандарт и профили (#432) цитируют новые строки классов.
        self.assertIn("не проходит гейты с решением человека (тип `человек` или `гибрид`",
                      text(ROOT / "standards/bcreq-prompt-base-standard.md"))
        self.assertIn("| К-20 | Подготовка доказательств гейта |",
                      text(ROOT / "standards/bcreq-prompt-profiles.md"))

    def test_k20_name(self):
        catalog = json.loads(text(CATALOG))
        classes = catalog["classes"] if isinstance(catalog, dict) else catalog
        k20 = [c for c in classes if c.get("id") == "К-20"]
        self.assertEqual(len(k20), 1)
        self.assertEqual(k20[0]["name"], "Подготовка доказательств гейта")
        self.assertIn("Подготовка доказательств гейта", text(CLASSES / "20-gate-evidence.md"))
        history = k20[0]["history"]
        self.assertEqual(history["previous_fields"]["name"], "Подготовка доказательств человеческого гейта")
        self.assertEqual(history["fields_changed_in"], "BL-159 (issue #433)")
        changed = {c["id"] for c in classes if "previous_fields" in c.get("history", {})}
        self.assertEqual(changed, {"К-20", "К-33", "К-34"}, "прежние значения полей — в history.previous_fields")

    def test_self_check_line_typed_in_all_classes(self):
        files = sorted(CLASSES.glob("[0-3][0-9]-*.md"))
        self.assertEqual(len(files), 39)
        for path in files:
            flat = " ".join(text(path).split())
            self.assertIn("Самопроверка не меняет полномочия и не проходит гейты с решением человека "
                          "(тип `человек` или `гибрид`, в том числе ключевые).", flat, path.name)
            self.assertNotIn("не проходит человеческие гейты", flat, path.name)


class SilenceRuleTest(unittest.TestCase):
    def test_gates_not_tied_to_silence_consent(self):
        for path in (PROCESS_STANDARD, ADR009):
            flat = " ".join(text(path).split())
            self.assertIn("Молчание — не согласие", flat, path.name)
            self.assertIn("к решению на гейте не применяется", flat, path.name)
            self.assertNotRegex(flat, r"(?i)gate[^.]{0,80}\(модель «молчание = согласие»", path.name)


class ProcessIndexTest(unittest.TestCase):
    def test_gate_column_typed_by_executor(self):
        body = text(INDEX)
        self.assertIn("Колонка «Gate / gap»: тип гейта", body)
        rows = 0
        for line in body.splitlines():
            if not line.startswith("| ") or "Gate / gap" in line:
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) != 5:
                continue
            op = re.fullmatch(r"`([a-z_]+)`", cells[1])
            gate = cells[4]
            if not op or not gate.startswith("Gate"):
                continue
            rows += 1
            m = re.match(r"Gate \(`([^`]+)`\):", gate)
            self.assertIsNotNone(m, f"гейт без типа: {line[:120]}")
            self.assertEqual(m.group(1), EXECUTOR[op.group(1)], f"тип ≠ исполнитель {op.group(1)}")
        self.assertGreaterEqual(rows, 20)


if __name__ == "__main__":
    sys.exit(0 if unittest.main(exit=False, verbosity=1).result.wasSuccessful() else 1)
