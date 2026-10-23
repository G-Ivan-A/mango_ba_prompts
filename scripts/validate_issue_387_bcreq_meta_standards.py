#!/usr/bin/env python3
"""Валидатор мета-стандартов разделов BCREQ (issue #387).

Зачем: Задача 2 программы пересборки промптов BCREQ фиксирует восемь
мета-стандартов разделов, правила композиции, контракт стадий и гейтов,
архитектуру промптов, третье мнение и RFC-387-01…07. Задача 3 собирает
промпты по этим документам, поэтому их состав проверяется механически.

Проверки:

1. ``standards/bcreq-sections/``: README и восемь файлов 01–08; в каждом
   разделе есть «Назначение», «Необходимо и достаточно», «Стиль»,
   «Паттерны формулировок», «Circuit breakers», «Чек-лист валидации»,
   «Источники»; чек-лист — 3–7 пунктов; README определяет короткий стиль
   КС1–КС7 для разделов 2, 5 L1, 6 и бюрократический БС1–БС5.
2. Раздел 1 — словари D1–D11 со ссылками и классы расхождения С0–С4;
   раздел 3 — варианты В-Д и В-Н; раздел 5 — уровни L1 и L2.
3. Композиция: правила К1–К7, условия ODA-1…ODA-3, не меньше трёх
   примеров ``### 5.N``.
4. Контракт гейтов: Г-IN (БА), Г-С1 (Заказчик), Г-W (ПО продукта,
   архитектор продукта, руководитель КК), стадии A-IN / A-CORE / A-WORK.
5. Архитектура: Промпт 0, stepwise и oneshot, слияния М1–М4, 14 файлов
   набора, пункты 2.1–2.14 в §6.1.
6. Третье мнение — по стандарту Analysis (frontmatter, секции, без
   ``ai-generated``).
7. RFC-387-01…07: якорь, «Путь отката» в каждом разделе, строка в реестре
   RFC.
8. Ссылки на реестр цитат чата: форма «[р. N, Ч-NN](…#Ln)», номер реплики и
   строки совпадают с реестром; плейсхолдеров ``{{Ч-NN}}`` нет; сверка
   цитат с экспортом пройдена (``chat-quote-check.json``).
9. Относительные ссылки этих файлов и индексов (реестр RFC,
   ``standards/README.md``, реестр источников, карта артефактов) ведут на
   существующие файлы и якоря заголовков (slug как на GitHub).

Запуск: ``python3 scripts/validate_issue_387_bcreq_meta_standards.py``
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SECTIONS_DIR = ROOT / "standards" / "bcreq-sections"
SECTION_FILES = (
    "01-glossary.md", "02-business-context.md", "03-functional-requirements.md",
    "04-non-functional-requirements.md", "05-solution-description.md",
    "06-implementation-constraints.md", "07-use-cases.md", "08-supplementary.md",
)
SECTION_HEADINGS = (
    "Назначение", "Необходимо и достаточно", "Стиль", "Паттерны формулировок",
    "Circuit breakers", "Чек-лист валидации", "Источники",
)
README = SECTIONS_DIR / "README.md"
COMPOSITION = ROOT / "standards" / "bcreq-composition-standard.md"
ARCHITECTURE = ROOT / "standards" / "bcreq-prompt-architecture.md"
GATES = ROOT / "docs" / "contracts" / "bcreq-stage-gates.md"
ANALYSIS = ROOT / "docs" / "analysis" / "2026-10-23-bcreq-standards-third-opinion.md"
ADR = ROOT / "docs" / "adr" / "2026-10-adr-012-bcreq-meta-standards.md"
RFC = ROOT / "docs" / "rfc" / "2026-10-bcreq-meta-standards-rfc.md"
RFC_REGISTER = ROOT / "docs" / "rfc" / "rfc-register.md"
INDEXES = (
    RFC_REGISTER, ROOT / "standards" / "README.md", ROOT / "standards" / "industry-standards-standard.md",
    ROOT / "pr-ops" / "artifact-map.md",
)
REGISTER = ROOT / "experiments" / "issue_387" / "chat-2026-10-22-23-register.md"
QUOTE_CHECK = ROOT / "experiments" / "issue_387" / "chat-quote-check.json"
REGISTER_URL = (
    "https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/"
    "experiments/issue_387/chat-2026-10-22-23-register.md?plain=1#L"
)
SUBTYPES = ("inventory", "matrix", "options", "recommendation")
ANALYSIS_SECTIONS = ("Summary / BLUF", "Context / Scope", "Findings", "Recommendations", "Related Artifacts")
RFC_IDS = tuple(f"RFC-387-0{n}" for n in range(1, 8))


def frontmatter(text: str) -> dict[str, str]:
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    return dict(re.findall(r"^([\w-]+):\s*(.*)$", m.group(1), re.M))


def section(text: str, heading: str) -> str | None:
    """Тело секции ``## heading`` до следующего заголовка второго уровня."""
    m = re.search(rf"^## {re.escape(heading)}\s*\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    return m.group(1) if m else None


def check_sections(texts: dict[Path, str]) -> list[str]:
    errors = []
    for name in SECTION_FILES:
        path = SECTIONS_DIR / name
        text = texts[path]
        for heading in SECTION_HEADINGS:
            if section(text, heading) is None:
                errors.append(f"{name}: нет секции «## {heading}»")
        checklist = section(text, "Чек-лист валидации") or ""
        items = re.findall(r"^- \[ \] ", checklist, re.M)
        if not 3 <= len(items) <= 7:
            errors.append(f"{name}: в чек-листе {len(items)} пунктов, нужно 3–7")
        if not re.search(r"^\| CB-\d\.\d+ \|", text, re.M):
            errors.append(f"{name}: нет таблицы circuit breakers CB-N.M")
        if "необходимо и достаточно" not in text.lower():
            errors.append(f"{name}: нет критерия «необходимо и достаточно»")

    readme = texts[README]
    for rule in [*(f"КС{n}" for n in range(1, 8)), *(f"БС{n}" for n in range(1, 6)),
                 *(f"Р{n}" for n in range(1, 8))]:
        if not re.search(rf"\b{rule}\b", readme):
            errors.append(f"README: нет правила {rule}")
    if not re.search(r"^### 2\.1\. Короткий стиль \(разделы 2, 5 L1, 6\)", readme, re.M):
        errors.append("README: нет определения короткого стиля для разделов 2, 5 L1, 6")
    if not re.search(r"^\| CB-0\.\d+ \|", readme, re.M):
        errors.append("README: нет общих circuit breakers CB-0.x")

    glossary = texts[SECTIONS_DIR / "01-glossary.md"]
    for n in range(1, 12):
        row = re.search(rf"^\| D{n} \| (.*)$", glossary, re.M)
        if row is None:
            errors.append(f"01-glossary: нет словаря D{n}")
        elif not re.search(r"<https://|\]\(", row.group(1)):
            errors.append(f"01-glossary: у словаря D{n} нет ссылки")
    for n in range(5):
        if not re.search(rf"^\s*\| С{n} \|", glossary, re.M):
            errors.append(f"01-glossary: нет класса расхождения С{n}")

    fr = texts[SECTIONS_DIR / "03-functional-requirements.md"]
    for variant in ("В-Д", "В-Н"):
        if variant not in fr:
            errors.append(f"03-functional-requirements: нет варианта {variant}")
    solution = texts[SECTIONS_DIR / "05-solution-description.md"]
    if section(solution, "Уровни L1 и L2") is None:
        errors.append("05-solution-description: нет секции «Уровни L1 и L2»")
    return errors


def check_composition(text: str) -> list[str]:
    errors = []
    for n in range(1, 8):
        if not re.search(rf"^- \*\*К{n}\. ", text, re.M):
            errors.append(f"композиция: нет правила К{n}")
    for n in range(1, 4):
        if not re.search(rf"^\| ODA-{n} \|", text, re.M):
            errors.append(f"композиция: нет условия ODA-{n}")
    if section(text, "3. TM Forum ODA — альтернативный стандарт") is None:
        errors.append("композиция: нет секции о TM Forum ODA как альтернативе")
    examples = re.findall(r"^### 5\.\d+\. ", text, re.M)
    if len(examples) < 3:
        errors.append(f"композиция: примеров комбинаций {len(examples)}, нужно ≥3")
    return errors


def check_gates(text: str) -> list[str]:
    errors = []
    for stage in ("A-IN", "A-CORE", "A-WORK", "A-RELEASE"):
        if stage not in text:
            errors.append(f"контракт гейтов: нет стадии {stage}")
    gates = section(text, "2. Гейты") or ""
    expected = {
        "Г-IN": ("БА",),
        "Г-С1": ("Заказчик",),
        "Г-W": ("ПО продукта", "архитектор продукта", "руководитель КК"),
    }
    for gate, roles in expected.items():
        row = re.search(rf"^\| {re.escape(gate)}\b[^|]*\| [^|]+\| ([^|]+)\|", gates, re.M)
        if row is None:
            errors.append(f"контракт гейтов: нет строки гейта {gate}")
            continue
        for role in roles:
            if role not in row.group(1):
                errors.append(f"контракт гейтов: у {gate} не указана решающая роль «{role}»")
    if section(text, "3. Возвраты") is None:
        errors.append("контракт гейтов: нет правил возврата")
    return errors


def check_architecture(text: str) -> list[str]:
    errors = []
    if section(text, "2. Промпт 0 — конституция") is None:
        errors.append("архитектура: нет секции «Промпт 0 — конституция»")
    if section(text, "4. stepwise и oneshot") is None:
        errors.append("архитектура: нет секции «stepwise и oneshot»")
    for n in range(1, 5):
        if not re.search(rf"^\| М{n} \|", text, re.M):
            errors.append(f"архитектура: нет слияния М{n}")
    files = re.findall(r"^\| `(bcreq-[a-z-]+-(?:stepwise|oneshot)\.md)` \|", text, re.M)
    if len(files) != 14 or len(set(files)) != 14:
        errors.append(f"архитектура: в таблице набора {len(set(files))} уникальных файлов, нужно 14")
    points = section(text, "6. Подтверждение структуры 2.1–2.14") or ""
    covered = {p.strip() for cell in re.findall(r"^\| ([\d., ]+) \|", points, re.M)
               for p in cell.split(",")}
    for item in (f"2.{n}" for n in range(1, 15)):
        if item not in covered:
            errors.append(f"архитектура §6.1: нет строки пункта «{item}»")
    if "Промпт 0" not in points:
        errors.append("архитектура §6.1: не указан добавленный шаг Промпт 0")
    return errors


def check_analysis(text: str) -> list[str]:
    errors = []
    fm = frontmatter(text)
    for key in ("status", "version", "updated", "temperature", "source", "scope", "analysis-subtype"):
        if not fm.get(key):
            errors.append(f"третье мнение: нет поля frontmatter {key}")
    if fm.get("analysis-subtype") and fm["analysis-subtype"] not in SUBTYPES:
        errors.append(f"третье мнение: analysis-subtype={fm['analysis-subtype']!r} вне словаря {SUBTYPES}")
    if "ai-generated" in fm:
        errors.append("третье мнение: ai-generated запрещён стандартом Analysis")
    headings = re.findall(r"^## (.+)$", text, re.M)
    for name in ANALYSIS_SECTIONS:
        if not any(name in h for h in headings):
            errors.append(f"третье мнение: нет секции «{name}» (standards/analysis-standard.md)")
    if headings and "Summary / BLUF" not in headings[0]:
        errors.append("третье мнение: первая секция — не Summary / BLUF")
    return errors


def check_rfc(rfc: str, register: str) -> list[str]:
    errors = []
    if not re.search(r"^## Статус: proposed$", rfc, re.M):
        errors.append("RFC: нет «## Статус: proposed»")
    for rid in RFC_IDS:
        anchor = rid.lower()
        body = re.search(rf'<a id="{anchor}"></a>\n+## {rid}\. (.*?)(?=<a id="rfc-|^## Источники|\Z)',
                         rfc, re.S | re.M)
        if body is None:
            errors.append(f"RFC: нет раздела {rid} с якорем #{anchor}")
            continue
        for part in ("Конфликт", "Предложение", "Обоснование", "Путь отката"):
            if part not in body.group(1):
                errors.append(f"RFC: в {rid} нет части «{part}»")
        if not re.search(rf"^\| \[{rid}\]\(2026-10-bcreq-meta-standards-rfc\.md#{anchor}\) \|", register, re.M):
            errors.append(f"реестр RFC: нет строки {rid}")
    return errors


def register_rows(register: str) -> dict[str, tuple[int, int]]:
    """ID строки реестра → (номер реплики, номер строки файла)."""
    rows = {}
    for number, line in enumerate(register.splitlines(), 1):
        m = re.match(r"^\| (Ч-\d{2}) \| (\d+) \|", line)
        if m:
            rows[m.group(1)] = (int(m.group(2)), number)
    return rows


def check_quotes(texts: dict[Path, str], register: str, quote_check: dict) -> list[str]:
    errors = []
    rows = register_rows(register)
    if not rows:
        return ["реестр цитат: нет строк Ч-NN"]
    total = 0
    for path, text in texts.items():
        rel = path.relative_to(ROOT)
        links = re.findall(rf"\[р\. (\d+), (Ч-\d{{2}})\]\({re.escape(REGISTER_URL)}(\d+)\)", text)
        total += len(links)
        for turn, rid, line in links:
            if rid not in rows:
                errors.append(f"{rel}: ссылка на {rid} — такой строки в реестре нет")
            elif rows[rid] != (int(turn), int(line)):
                errors.append(f"{rel}: «р. {turn}, {rid}» → L{line}; в реестре р. {rows[rid][0]}, L{rows[rid][1]}")
        loose = len(re.findall(r"chat-2026-10-22-23-register\.md\?plain=1#L", text)) - len(links)
        if loose:
            errors.append(f"{rel}: {loose} ссылок на строки реестра не в форме «[р. N, Ч-NN](…#Ln)»")
        if "{{Ч-" in text:
            errors.append(f"{rel}: остались плейсхолдеры {{{{Ч-NN}}}}")
    if not total:
        errors.append("нет ни одной ссылки на реестр цитат чата 21–23.10.2026")

    sha = re.search(r"^\| SHA-256 \| `([0-9a-f]{64})` \|$", register, re.M)
    if not quote_check.get("ok"):
        errors.append("chat-quote-check.json: ok=false — цитаты не сверены с экспортом")
    if sha is None or quote_check.get("export_sha256") != sha.group(1):
        errors.append("chat-quote-check.json: SHA-256 экспорта не совпадает с провенансом реестра")
    checked = [r["id"] for r in quote_check.get("results", [])]
    if sorted(checked) != sorted(rows):
        errors.append(f"chat-quote-check.json: сверено {len(checked)} строк, в реестре {len(rows)}")
    return errors


def slug(heading: str) -> str:
    """Якорь заголовка, как его строит GitHub."""
    heading = re.sub(r"`|\*\*|\[([^\]]*)\]\([^)]*\)", lambda m: m.group(1) or "", heading)
    heading = re.sub(r"[^\w\- ]", "", heading.strip().lower())
    return heading.replace(" ", "-")


def anchors(text: str) -> set[str]:
    found, seen = set(), {}
    for heading in re.findall(r"^#{1,6} (.+?)\s*$", text, re.M):
        base = slug(heading)
        n = seen.get(base, 0)
        found.add(base if n == 0 else f"{base}-{n}")
        seen[base] = n + 1
    found.update(re.findall(r'<a id="([^"]+)"></a>', text))
    return found


def check_links(texts: dict[Path, str]) -> list[str]:
    errors, cache = [], {}
    for path, text in texts.items():
        body = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.S)
        body = re.sub(r"```.*?```", "", body, flags=re.S)
        for target in re.findall(r"\]\(([^)\s]+)\)", body):
            if re.match(r"[a-z]+:", target):
                continue
            file_part, _, anchor = target.partition("#")
            dest = (path.parent / file_part).resolve() if file_part else path
            rel = path.relative_to(ROOT)
            if not dest.exists():
                errors.append(f"{rel}: ссылка {target!r} ведёт на несуществующий файл")
                continue
            if anchor and dest.suffix == ".md" and not anchor.startswith("L"):
                if dest not in cache:
                    cache[dest] = anchors(dest.read_text(encoding="utf-8"))
                if anchor not in cache[dest]:
                    errors.append(f"{rel}: якоря #{anchor} нет в {dest.relative_to(ROOT)}")
    return errors


def main() -> int:
    paths = [README, *(SECTIONS_DIR / n for n in SECTION_FILES), COMPOSITION, ARCHITECTURE,
             GATES, ANALYSIS, ADR, RFC]
    for path in (*paths, *INDEXES, REGISTER, QUOTE_CHECK):
        if not path.exists():
            print(f"FAIL: нет {path.relative_to(ROOT)}")
            return 1
    texts = {p: p.read_text(encoding="utf-8") for p in paths}
    indexes = {p: p.read_text(encoding="utf-8") for p in INDEXES}
    errors = check_sections(texts)
    errors += check_composition(texts[COMPOSITION])
    errors += check_gates(texts[GATES])
    errors += check_architecture(texts[ARCHITECTURE])
    errors += check_analysis(texts[ANALYSIS])
    errors += check_rfc(texts[RFC], indexes[RFC_REGISTER])
    errors += check_quotes(texts, REGISTER.read_text(encoding="utf-8"),
                           json.loads(QUOTE_CHECK.read_text(encoding="utf-8")))
    errors += check_links({**texts, **indexes})
    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        return 1
    print(f"OK: мета-стандарты BCREQ (issue #387) — {len(SECTION_FILES)} разделов, композиция, гейты, "
          f"архитектура промптов, третье мнение, {len(RFC_IDS)} RFC и ссылки на реестр цитат согласованы")
    return 0


if __name__ == "__main__":
    sys.exit(main())
