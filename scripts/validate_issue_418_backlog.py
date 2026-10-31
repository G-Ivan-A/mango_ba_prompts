#!/usr/bin/env python3
"""Регрессионная проверка бэклога проекта (issue #418).

Бэклог — один входной документ ``pr-ops/BACKLOG.md`` и три спутника:
карточки трека Б (модель БА: процессы и промпты), карточки трека А
(репозиторий) и инструкция ведения. Проверка фиксирует контракт
постановки, а не качество текста:

* frontmatter всех четырёх файлов проходит валидатор Хаба, поля
  ``ai-generated`` нет;
* входной документ начинается с логики и порядка на одной странице, затем
  реестр решений владельца, ответ по мета-модели БА Хаба, спринты;
  разделы «5. Открытые вопросы» и «6. Технический долг» сохранены, потому
  что на их якоря ссылаются README, CONTRIBUTING и валидаторы;
* каждая задача ``BL-NNN`` из таблиц спринтов имеет ровно одну карточку, а
  каждая карточка — строку в таблице спринта; у карточки есть «Почему»,
  «Что меняется», «Источники» и «Готово, когда»;
  префикс ``BL`` отличает задачи от ``B-NNN`` бэклога Хаба;
* каждый источник карточки — ссылка, раздел и цитата до 100 символов;
  цитата из файла репозитория дословно находится в разделе, на который
  указывает якорь ссылки (после нормализации пробелов и разметки);
* каждое решение ``Р-NN`` реестра упомянуто хотя бы в одной задаче, и
  каждое упомянутое решение есть в реестре;
* относительные ссылки и якоря разрешаются; подписи mermaid в кавычках;
  внутреннего жаргона нет;
* бэклог не меняет репозиторий: ``runs/``, ``prompts/``, ``site/``,
  канонические документы, ADR и RFC совпадают с ``main``.

Внешние цитаты (Хаб, issue, PR) проверяются только по длине; дословность
проверяет ``experiments/issue_418/check_external_quotes.py`` через ``gh``.
"""

import re
import subprocess
import sys
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENTRY = ROOT / "pr-ops/BACKLOG.md"
TRACK_B = ROOT / "pr-ops/backlog-ba-model.md"
TRACK_A = ROOT / "pr-ops/backlog-repository.md"
INSTRUCTION = ROOT / "pr-ops/backlog-instruction.md"
FILES = (ENTRY, TRACK_B, TRACK_A, INSTRUCTION)
CARD_FILES = (TRACK_B, TRACK_A)

QUOTE_LIMIT = 100
QUOTE_RE = re.compile(r"“([^”]+)”")
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
TASK_ID_RE = re.compile(r"\bBL-\d{3}\b")
DECISION_RE = re.compile(r"\bР-\d{2}\b")
CARD_HEADING_RE = re.compile(r"^### (BL-\d{3})\. ", re.M)
CARD_FIELDS = ("**Почему.**", "**Что меняется.**", "**Источники.**", "**Готово, когда.**")

ENTRY_SECTIONS = (
    "## Как читать за две минуты",
    "## 1. Логика и порядок на одной странице",
    "## 2. Решения владельца",
    "## 3. Мета-модель БА Хаба на этом шаге",
    "## 4. Спринты",
    "## 5. Открытые вопросы",
    "## 6. Технический долг соответствия стандартам Хаба (issue #267)",
    "## 7. Архив",
)
SPRINT_HEADER = (
    "| ID | Название | Приоритет | Зависимости | Статус | Issue | Источник "
    "| Краткое содержание | Режим запуска |"
)
STATUSES = re.compile(
    r"^(TODO|in-progress|review|DONE|ЧАСТИЧНО|CANCELLED|"
    r"deferred \((triggered|regular|icebox)\))$"
)
PRIORITIES = {"P0", "P1", "P2", "P3", "—"}
MODES = {"Structured", "Hybrid", "Creative", "—"}

# Строки, которых требуют другие валидаторы (issue #263, issue #72).
REQUIRED_ELSEWHERE = (
    "evals и golden-set отсутствуют",
    "инструментарий веб-ресурса (app)",
    "Пользовател",
)
# Поле frontmatter, запрещённое стандартом Хаба. В тексте оно встречается
# законно: строка долга S-003 раздела 6 называет его.
FORBIDDEN_FIELDS = ("ai-generated",)
FORBIDDEN = (
    "Фаундер",
    "фаундер",
    "Иосполнитель",
    "Конард",
    "Proof of Execution",
    "Learning loop",
    "S1-S5",
    "S1–S5",
)
# Бэклог — согласовательный шаг: эти пути он не меняет.
PROTECTED = (
    "runs",
    "prompts",
    "site",
    "standards",
    "docs/vision.md",
    "docs/concept.md",
    "docs/architecture.md",
    "docs/roadmap.md",
    "docs/adr",
    "docs/rfc",
    "README.md",
)
# Коммиты этого бэклога помечены «(issue-418)» в теме: docs(issue-418): …
OWN_COMMIT = re.compile(r"\(issue-418\)")


def text(path):
    return Path(path).read_text(encoding="utf-8")


def rel(path):
    return Path(path).relative_to(ROOT).as_posix()


def slug(heading):
    """Якорь заголовка в стиле GitHub (как в validate_issue_409)."""
    heading = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", heading).strip().lower()
    return re.sub(r"[^\w\- ]", "", heading).replace(" ", "-")


def headings(path):
    """Заголовки вне блоков кода: (номер строки, уровень, якорь)."""
    found, seen, fenced = [], Counter(), False
    for number, line in enumerate(text(path).splitlines()):
        if line.startswith("```"):
            fenced = not fenced
            continue
        match = None if fenced else re.match(r"^(#{1,6})\s+(.*?)\s*#*\s*$", line)
        if match:
            base = slug(match.group(2))
            anchor = base if not seen[base] else f"{base}-{seen[base]}"
            seen[base] += 1
            found.append((number, len(match.group(1)), anchor))
    return found


def anchors(path):
    found = {anchor for _, _, anchor in headings(path)}
    found.update(re.findall(r'<a id="([^"]+)"', text(path)))
    return found


def section(path, anchor):
    """Текст раздела по якорю; для <a id> и пустого якоря — весь файл."""
    lines = text(path).splitlines()
    marks = headings(path)
    for index, (start, level, name) in enumerate(marks):
        if name != anchor:
            continue
        end = len(lines)
        for later, later_level, _ in marks[index + 1 :]:
            if later_level <= level:
                end = later
                break
        return "\n".join(lines[start:end])
    return text(path)


def normalize(value):
    """Цитата сравнивается без разметки и с одинарными пробелами."""
    value = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", value)
    value = value.replace("*", "").replace("`", "").replace("\\|", "|")
    value = value.replace("&nbsp;", " ").replace(" ", " ")
    return re.sub(r"\s+", " ", value).strip()


def locate_quote(path, quote):
    """Якоря разделов, где дословно встречается цитата (для отладки)."""
    needle = normalize(quote)
    hits = [anchor for _, _, anchor in headings(path) if needle in normalize(section(path, anchor))]
    # Самый вложенный раздел — последний в списке совпадений.
    return hits[-1:] if hits else []


def resolve(source, target):
    """Путь и якорь относительной ссылки; None для внешних ссылок."""
    if re.match(r"^[a-z]+:", target):
        return None
    path, _, anchor = target.partition("#")
    resolved = (source.parent / path).resolve() if path else source
    return resolved, anchor


def cards(path):
    """Карточки задач: ID -> текст карточки."""
    body = text(path)
    found = {}
    marks = list(CARD_HEADING_RE.finditer(body))
    for index, match in enumerate(marks):
        end = marks[index + 1].start() if index + 1 < len(marks) else len(body)
        chunk = body[match.start() : end]
        chunk = re.split(r"^## ", chunk, maxsplit=1, flags=re.M)[0]
        found.setdefault(match.group(1), []).append(chunk)
    return found


def source_lines(card):
    """Строки блока «Источники» карточки."""
    block = card.split("**Источники.**", 1)[1]
    block = re.split(r"^\*\*[^*]+\.\*\*", block, maxsplit=1, flags=re.M)[0]
    items, current = [], None
    for line in block.splitlines():
        if line.startswith("- "):
            current = [line[2:]]
            items.append(current)
        elif current is not None and line.startswith("  "):
            current.append(line.strip())
    return [" ".join(item) for item in items]


def sprint_rows(path):
    """Строки таблиц спринтов: (заголовок спринта, ячейки)."""
    rows, sprint, inside = [], None, False
    for line in text(path).splitlines():
        if line.startswith("### Спринт "):
            sprint, inside = line, False
        if line.startswith(SPRINT_HEADER):
            inside = True
            continue
        if inside:
            if not line.startswith("|"):
                inside = False
                continue
            if line.startswith("| ---") or line.startswith("|---"):
                continue
            rows.append((sprint, [cell.strip() for cell in line.strip().strip("|").split("|")]))
    return rows


def frontmatter(path):
    match = re.match(r"^---\n(.*?)\n---\n", text(path), re.S)
    return match.group(1) if match else ""


class Frontmatter(unittest.TestCase):
    def test_hub_validator(self):
        for path in FILES:
            with self.subTest(path=rel(path)):
                self.assertTrue(path.exists(), rel(path))
                result = subprocess.run(
                    ["./tools/validate-frontmatter.sh", rel(path)],
                    cwd=ROOT,
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(result.returncode, 0, result.stderr)

    def test_fields(self):
        for path in FILES:
            with self.subTest(path=rel(path)):
                head = frontmatter(path)
                for field in ("owner: G-Ivan-A", "type: backlog", "issues/418"):
                    self.assertIn(field, head)


class EntryDocument(unittest.TestCase):
    def setUp(self):
        self.body = text(ENTRY)

    def test_sections_in_order(self):
        positions = []
        for heading in ENTRY_SECTIONS:
            self.assertIn("\n" + heading + "\n", self.body, heading)
            positions.append(self.body.index("\n" + heading + "\n"))
        self.assertEqual(positions, sorted(positions), "порядок разделов входного документа")

    def test_open_questions_anchor(self):
        """README, CONTRIBUTING и ai-governance ссылаются на этот якорь."""
        self.assertIn("5-открытые-вопросы", anchors(ENTRY))

    def test_required_by_other_validators(self):
        for needle in REQUIRED_ELSEWHERE:
            self.assertIn(needle, self.body, needle)

    def test_tech_debt_rows(self):
        for number in range(1, 9):
            self.assertIn(f"| S-00{number} |", self.body)

    def test_meta_model_answer(self):
        part = section(ENTRY, "3-мета-модель-ба-хаба-на-этом-шаге")
        for needle in ("не меняем", "Критических предпосылок", "BL-121", "BL-122", "Р-12"):
            self.assertIn(needle, part, needle)

    def test_stage_order(self):
        """Порядок владельца: этап 1 → ревизия мета-модели → этап 2 (OpenCode)."""
        part = section(ENTRY, "1-логика-и-порядок-на-одной-странице")
        first = part.index("Этап 1")
        meta = part.index("мета-модел")
        second = part.index("OpenCode")
        self.assertLess(first, meta)
        self.assertLess(meta, second)

    def test_mermaid_labels_quoted(self):
        for block in re.findall(r"```mermaid\n(.*?)```", self.body, re.S):
            for label in re.findall(r"\w+\[([^\]]*)\]", block):
                self.assertTrue(label.startswith('"') and label.endswith('"'), label)


class Decisions(unittest.TestCase):
    def setUp(self):
        self.register = section(ENTRY, "2-решения-владельца")
        self.declared = re.findall(r"^\| \*\*(Р-\d{2})\*\* \|", self.register, re.M)

    def test_register(self):
        self.assertGreaterEqual(len(self.declared), 10)
        self.assertEqual(len(self.declared), len(set(self.declared)), "дубли Р-NN")
        self.assertIn("Как дать решение", self.register)

    def test_every_decision_used_by_tasks(self):
        used = set()
        for path in CARD_FILES:
            used.update(DECISION_RE.findall(text(path)))
        for _, cells in sprint_rows(ENTRY):
            used.update(DECISION_RE.findall(cells[3]))
        for decision in self.declared:
            self.assertIn(decision, used, f"{decision} не открывает ни одной задачи")
        for decision in used:
            self.assertIn(decision, self.declared, f"{decision} нет в реестре")


class Tasks(unittest.TestCase):
    def setUp(self):
        self.rows = sprint_rows(ENTRY)
        self.cards = {}
        for path in CARD_FILES:
            for task, chunks in cards(path).items():
                self.cards.setdefault(task, []).extend((path, chunk) for chunk in chunks)

    def test_rows(self):
        self.assertGreaterEqual(len(self.rows), 30)
        ids = [cells[0] for _, cells in self.rows]
        self.assertEqual(len(ids), len(set(ids)), "дубли BL-NNN в спринтах")
        known = set(ids) | {f"S-00{n}" for n in range(1, 9)}
        for sprint, cells in self.rows:
            with self.subTest(task=cells[0]):
                self.assertEqual(len(cells), 9, cells)
                self.assertRegex(cells[0], r"^BL-\d{3}$")
                self.assertIn(cells[2], PRIORITIES)
                self.assertRegex(cells[4], STATUSES)
                self.assertIn(cells[8], MODES)
                for dependency in re.findall(r"\b(?:BL|S)-\d{3}\b", cells[3]):
                    self.assertIn(dependency, known, dependency)

    def test_every_row_has_one_card_and_back(self):
        ids = {cells[0] for _, cells in self.rows}
        for task in ids:
            with self.subTest(task=task):
                self.assertEqual(len(self.cards.get(task, [])), 1, f"{task}: карточек")
        for task in self.cards:
            self.assertIn(task, ids, f"{task}: карточка без строки спринта")

    def test_card_fields(self):
        for task, items in self.cards.items():
            for path, card in items:
                with self.subTest(task=task):
                    for field in CARD_FIELDS:
                        self.assertIn(field, card, f"{task}: нет {field}")
                    self.assertGreaterEqual(len(source_lines(card)), 1, task)

    def test_track_split(self):
        for task, items in self.cards.items():
            path = items[0][0]
            expected = TRACK_B if task.startswith("BL-1") else TRACK_A
            self.assertEqual(path, expected, f"{task} в {rel(path)}")

    def test_sources_format_and_quotes(self):
        for task, items in self.cards.items():
            path, card = items[0]
            for line in source_lines(card):
                with self.subTest(task=task, source=line[:60]):
                    links = LINK_RE.findall(line)
                    quotes = QUOTE_RE.findall(line)
                    self.assertTrue(links, "нет ссылки")
                    self.assertIn("раздел «", line, "нет раздела")
                    self.assertEqual(len(quotes), 1, "нужна ровно одна цитата")
                    quote = quotes[0]
                    self.assertLessEqual(len(quote), QUOTE_LIMIT, quote)
                    target = resolve(path, links[0][1])
                    if target is None:
                        continue
                    file, anchor = target
                    self.assertTrue(file.exists(), file)
                    if file.suffix != ".md":
                        self.assertIn(normalize(quote), normalize(text(file)))
                        continue
                    if anchor:
                        self.assertIn(anchor, anchors(file), f"якорь {anchor}")
                    self.assertIn(
                        normalize(quote),
                        normalize(section(file, anchor)),
                        f"цитата не найдена в {rel(file)}#{anchor}",
                    )


class Links(unittest.TestCase):
    def test_relative_links_and_anchors(self):
        for path in FILES:
            body = re.sub(r"```.*?```", "", text(path), flags=re.S)
            for _, target in LINK_RE.findall(body):
                target = target.strip("<>")
                resolved = resolve(path, target)
                if resolved is None:
                    continue
                file, anchor = resolved
                with self.subTest(path=rel(path), target=target):
                    self.assertTrue(file.exists(), file)
                    if anchor and file.suffix == ".md":
                        self.assertIn(anchor, anchors(file))

    def test_forbidden_terms(self):
        for path in FILES:
            for term in FORBIDDEN:
                self.assertNotIn(term, text(path), f"{rel(path)}: {term}")
            for field in FORBIDDEN_FIELDS:
                self.assertNotIn(field, frontmatter(path), f"{rel(path)}: {field}")

    def test_registered_in_artifact_map(self):
        mapping = text(ROOT / "pr-ops/artifact-map.md")
        for path in FILES:
            self.assertIn(f"/{rel(path)}", mapping)

    def test_changelog(self):
        changelog = text(ROOT / "CHANGELOG.md")
        unreleased = changelog.split("\n## ", 2)[1]
        self.assertIn("Issue #418", unreleased)


class NoRepositoryChange(unittest.TestCase):
    """Бэклог — согласовательный этап: защищённые пути не меняются."""

    def test_protected_paths(self):
        base = None
        for ref in ("upstream/main", "origin/main", "main"):
            probe = subprocess.run(
                ["git", "merge-base", "HEAD", ref], cwd=ROOT, capture_output=True, text=True
            )
            if probe.returncode == 0:
                base = probe.stdout.strip()
                break
        if base is None:
            self.skipTest("нет git-истории main")
        result = subprocess.run(
            ["git", "diff", "--name-only", base, "--", *PROTECTED],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        changed = [line for line in result.stdout.splitlines() if line]
        own = self._own_commits(base)
        offenders = [path for path in changed if path in own]
        self.assertEqual(offenders, [], "бэклог изменил защищённые пути")

    @staticmethod
    def _own_commits(base):
        """Файлы, изменённые коммитами issue #418 (а не слиянием main и не другими PR)."""
        log = subprocess.run(
            ["git", "log", "--no-merges", "--format=%H %s", f"{base}..HEAD"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        files = set()
        for line in log.stdout.splitlines():
            sha, _, subject = line.partition(" ")
            if not OWN_COMMIT.search(subject):
                continue
            show = subprocess.run(
                ["git", "show", "--name-only", "--format=", sha],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            files.update(name for name in show.stdout.splitlines() if name)
        return files


if __name__ == "__main__":
    unittest.main(verbosity=1 if "-q" in sys.argv else 2, argv=[sys.argv[0]])
