#!/usr/bin/env python3
"""Валидация записи прогона RUN-0074 (issue #378, задача 1104, золотой набор ошибок ИИ).

Проверяет:

0. каталог прогона содержит обязательные файлы, в ``inputs/`` нет ничего, кроме
   ``README.md`` (сырой экспорт чата в репозиторий не попадает — правило #309),
   провенанс фиксирует SHA-256 и размер экспорта;
1. порождённые файлы совпадают побайтно с перепорождением
   ``experiments/issue_378_golden_set.py`` из ``stats.json``, ``quote-check.json``
   и разметки ``experiments/issue_378_golden_data.py`` — ручных правок нет;
2. разметка замкнута: категории, происхождение, обнаружение, достоверность,
   продукты, разделы, коды BABOK и ODA, локаторы КБ — из закрытых словарей;
   у реакции БА есть и реплика, и цитата, реплика реакции — реплика БА позже
   дефекта;
3. каждая цитата разметки сверена с экспортом: в ``quote-check.json`` есть
   строка на каждую цитату, расхождений нет;
4. в каждом наборе-кандидате 5–10 кейсов и есть негативный кейс («дефекта
   нет»), идентификаторы кейсов и вхождений уникальны;
5. счётчики ``metadata.yaml`` совпадают с разметкой;
6. в записи и в замерах нет подписанных ссылок CDN на вложения чата;
7. прогон зарегистрирован в ``runs/README.md`` и ``CHANGELOG.md``.
"""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "runs/2026/RUN-0074"
DATA = ROOT / "experiments/issue_378"
GENERATOR = ROOT / "experiments/issue_378_golden_set.py"
EXPORT_SHA = "21b3ac0582bc4c8f28cb99eeb1d687ddf7a0a9685aad669daec39077681dead0"
EXPORT_SIZE = "1950629"
HAND_FILES = (
    "inputs/README.md",
    "logs/experiment-log.md",
    "feedback/review-notes.md",
)
SECRET = re.compile(r"cdn\.qwenlm\.ai|[?&]key=", re.IGNORECASE)
TURN_ROLE = {0: "user"}


def load_generator():
    spec = importlib.util.spec_from_file_location("issue_378_golden_set", GENERATOR)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_files(rendered: dict[str, str], errors: list[str]) -> None:
    for rel in (*rendered, *HAND_FILES):
        if not (RUN / rel).is_file():
            errors.append("нет обязательного файла %s" % rel)
    extra = sorted(p.name for p in (RUN / "inputs").iterdir() if p.name != "README.md")
    if extra:
        errors.append("в inputs/ лишние файлы (сырой экспорт не хранится): %s" % ", ".join(extra))
    provenance = (RUN / "inputs/README.md").read_text(encoding="utf-8")
    for marker in (EXPORT_SHA, EXPORT_SIZE):
        if marker not in provenance:
            errors.append("inputs/README.md: нет %s" % marker)
    for rel, text in rendered.items():
        path = RUN / rel
        if path.is_file() and path.read_text(encoding="utf-8") != text:
            errors.append("%s расходится с перепорождением (запустите experiments/issue_378_golden_set.py)" % rel)


def check_markup(gd, stats: dict, errors: list[str]) -> list[dict]:
    rows = gd.numbered_incidents()
    roles = {row["index"]: row["role"] for row in stats["turn_rows"]}
    for row in rows:
        where = "%s (реплика %d)" % (row["id"], row["turn"])
        checks = (
            ("категория", row["cat"], gd.CATEGORIES),
            ("происхождение", row["origin"], gd.ORIGINS),
            ("обнаружение", row["det"], gd.DETECTORS),
            ("достоверность", row["conf"], gd.CONFIDENCE),
            ("продукт", row["prod"], gd.PRODUCTS),
            ("раздел", row["sec"], gd.SECTIONS),
        )
        for label, value, vocabulary in checks:
            if value not in vocabulary:
                errors.append("%s: %s %r вне словаря" % (where, label, value))
        for code in row.get("babok") or []:
            if code not in gd.BABOK:
                errors.append("%s: код BABOK %r вне словаря" % (where, code))
        if row.get("oda") and row["oda"] not in gd.ODA:
            errors.append("%s: сегмент ODA %r вне словаря" % (where, row["oda"]))
        if not row["quote"].strip():
            errors.append("%s: пустая цитата" % where)
        expected_role = "user" if row["origin"] == "prompt" else "assistant"
        if roles.get(row["turn"]) != expected_role:
            errors.append("%s: реплика не %s" % (where, expected_role))
        if (row["det_turn"] is None) != (not row["uq"]):
            errors.append("%s: реакция БА без реплики или без цитаты" % where)
        if row["det_turn"] is not None:
            if row["det_turn"] <= row["turn"] or roles.get(row["det_turn"]) != "user":
                errors.append("%s: реплика реакции %r — не более поздняя реплика БА" % (where, row["det_turn"]))
        if row["det"] == "run" and row["det_turn"] is not None:
            errors.append("%s: «при фиксации», но есть реакция БА" % where)
        if row["evidence"] and row["evidence"] not in gd.KB and not row["evidence"].startswith("VPBXAPI:"):
            errors.append("%s: локатор КБ %r вне словаря" % (where, row["evidence"]))
    for code, cat in gd.CATEGORIES.items():
        for code_babok in cat["babok"]:
            if code_babok not in gd.BABOK:
                errors.append("%s: код BABOK %r вне словаря" % (code, code_babok))
        if cat["oda"] not in gd.ODA:
            errors.append("%s: сегмент ODA %r вне словаря" % (code, cat["oda"]))
        for key in ("title", "antipattern", "guard", "rule", "sec345"):
            if not cat[key]:
                errors.append("%s: пустое поле %s" % (code, key))
    for row in gd.NEGATIVES:
        if roles.get(row["turn"]) != "assistant":
            errors.append("позитивный кейс реплики %d: реплика не ответ модели" % row["turn"])
    ids = [row["id"] for row in gd.SUCCESS_CRITERIA]
    if len(ids) != len(set(ids)):
        errors.append("идентификаторы критериев успеха не уникальны")
    for row in gd.SUCCESS_CRITERIA:
        if roles.get(row["turn"]) != "user":
            errors.append("%s: реплика %d не реплика БА" % (row["id"], row["turn"]))
        for code in row["counters"]:
            if code not in gd.CATEGORIES:
                errors.append("%s: категория %r вне словаря" % (row["id"], code))
    return rows


def check_quotes(gd, rows: list[dict], check: dict, errors: list[str]) -> None:
    if check["missing"]:
        errors.append("quote-check.json: не найдено цитат: %d" % check["missing"])
    if check["export_sha256"] != EXPORT_SHA:
        errors.append("quote-check.json: сверка выполнена не по экспорту задачи 1104")
    refs = Counter((row["ref"], row["kind"]) for row in check["rows"])
    expected = Counter()
    for row in rows:
        expected[(row["id"], "incident")] += 1
        if row["uq"]:
            expected[(row["id"], "incident-uq")] += 1
    for index, row in enumerate(gd.NEGATIVES, 1):
        expected[("N-%02d" % index, "negative")] += 1
        if row["uq"]:
            expected[("N-%02d" % index, "negative-uq")] += 1
    for row in gd.SUCCESS_CRITERIA:
        expected[(row["id"], "success")] += 1
    if refs != expected:
        missing = sorted((expected - refs).elements())[:5]
        extra = sorted((refs - expected).elements())[:5]
        errors.append("quote-check.json не соответствует разметке (перезапустите сверку): нет %s, лишние %s" % (missing, extra))
    if any(not row["found"] for row in check["rows"]):
        errors.append("quote-check.json: есть строки с found=false")


def check_sets(rendered: dict[str, str], errors: list[str]) -> int:
    payload = json.loads(rendered["outputs/golden-set-candidates.json"])
    seen: set[str] = set()
    total = 0
    for item in payload["sets"]:
        cases = item["cases"]
        total += len(cases)
        if not 5 <= len(cases) <= 10:
            errors.append("%s: кейсов %d, ожидается 5–10" % (item["id"], len(cases)))
        if not any(case["kind"] == "positive" for case in cases):
            errors.append("%s: нет негативного кейса («дефекта нет»)" % item["id"])
        for case in cases:
            if case["id"] in seen:
                errors.append("повтор case-id %s" % case["id"])
            seen.add(case["id"])
            outcome = case["expect"]["outcome"]
            if (case["kind"] == "negative") != (outcome == "refused"):
                errors.append("%s: вид кейса и ожидаемый исход не согласованы" % case["id"])
    return total


def check_metadata(gd, rows: list[dict], check: dict, errors: list[str]) -> None:
    text = (RUN / "metadata.yaml").read_text(encoding="utf-8")
    counts = Counter(row["cat"] for row in rows)
    expected = {
        "incidents_total": len(rows),
        "incidents_confirmed": sum(1 for row in rows if row["conf"] == "confirmed"),
        "success_criteria": len(gd.SUCCESS_CRITERIA),
        "positive_cases": len(gd.NEGATIVES),
        "quotes_checked": check["checked"],
        "quote_mismatches": 0,
        **{code: counts.get(code, 0) for code in gd.CATEGORIES},
    }
    for key, value in expected.items():
        if not re.search(r"^\s+%s: %d$" % (re.escape(key), value), text, re.M):
            errors.append("metadata.yaml: %s ≠ %d" % (key, value))
    for key in ("run_type: statistics", "run_id: RUN-0074", "status: draft"):
        if key not in text:
            errors.append("metadata.yaml: нет «%s»" % key)


def check_secrets(errors: list[str]) -> None:
    paths = [p for p in RUN.rglob("*") if p.is_file()]
    paths += [DATA / "stats.json", DATA / "quote-check.json"]
    for path in paths:
        if SECRET.search(path.read_text(encoding="utf-8")):
            errors.append("%s: подписанная ссылка CDN на вложение" % path.relative_to(ROOT))


def check_registry(errors: list[str]) -> None:
    registry = (ROOT / "runs/README.md").read_text(encoding="utf-8")
    if "[`RUN-0074`](2026/RUN-0074/metadata.yaml)" not in registry:
        errors.append("runs/README.md: RUN-0074 не зарегистрирован")
    if "experiments/issue_378_golden_set.py" not in registry:
        errors.append("runs/README.md: генератор RUN-0074 не описан в инструментах")
    if "Issue #378" not in (ROOT / "CHANGELOG.md").read_text(encoding="utf-8"):
        errors.append("CHANGELOG.md: нет записи Issue #378")


def main() -> int:
    errors: list[str] = []
    sys.path.insert(0, str(ROOT / "experiments"))
    generator = load_generator()
    gd = generator.gd
    stats = json.loads((DATA / "stats.json").read_text(encoding="utf-8"))
    check = json.loads((DATA / "quote-check.json").read_text(encoding="utf-8"))
    rendered = generator.render(stats, check)

    check_files(rendered, errors)
    rows = check_markup(gd, stats, errors)
    ids = [row["id"] for row in rows]
    if len(ids) != len(set(ids)):
        errors.append("идентификаторы вхождений не уникальны")
    check_quotes(gd, rows, check, errors)
    cases = check_sets(rendered, errors)
    check_metadata(gd, rows, check, errors)
    check_secrets(errors)
    check_registry(errors)

    if errors:
        print("FAIL: validate_issue_378_run: найдено проблем: %d" % len(errors))
        for error in errors[:40]:
            print("  - %s" % error)
        return 1

    print("OK: validate_issue_378_run: вхождений %d, категорий %d, кейсов %d, цитат сверено %d"
          % (len(rows), len(set(row["cat"] for row in rows)), cases, check["checked"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
