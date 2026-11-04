"""BL-157в: свод кодировки правок БА по шести выгрузкам чатов (issue #448).

Вход — три файла кодировки (подагенты A, B, C; каждый — свои выгрузки),
выход — обезличенные данные для репозитория:

* ``coding.json`` — все записи, проверенные по схеме и на обезличивание;
* ``aggregate.json`` — счётчики: категория × актуальность, шаг, урок,
  выгрузка; запросы отраслевой практики; кандидаты в новые кейсы.

Сырой текст чатов в репозиторий не попадает: выгрузки лежат вне репозитория,
в записи — пересказ до 200 знаков.

Запуск (вход — недоверенные данные, поэтому ``-I``)::

    python3 -I experiments/issue_448/bl157v_aggregate.py \\
        /tmp/chats448-work/coded-A.json /tmp/chats448-work/coded-B.json \\
        /tmp/chats448-work/coded-C.json --out experiments/issue_448/bl157v
"""

from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from pathlib import Path

EXPORTS = ("1069", "1074", "1101", "1106", "1110", "1128")
CATEGORIES = (
    "добавление без источника",
    "пропуск содержимого",
    "не тот объект/контекст",
    "домен продукта неверно",
    "структура/формат",
    "лишний объём",
    "термины",
    "практика не предложена",
    "неатомарность",
    "потеря ограничителя/условия",
    "дублирование",
    "самосертификация",
    "иное",
)
RELEVANCE = ("закрыто", "частично", "не закрыто")
FIELDS = (
    "export",
    "turn",
    "step",
    "category",
    "lesson",
    "summary",
    "relevance",
    "where",
    "industry_analogue",
    "new_case_candidate",
)
SUMMARY_LIMIT = 200

#: Признаки данных, которых не должно быть в обезличенной записи.
LEAKS = {
    "email": re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"),
    "url": re.compile(r"https?://|www\."),
    "phone": re.compile(r"(?:\+7|8)[\s(-]*\d{3}[\s)-]*\d{3}[\s-]*\d{2}[\s-]*\d{2}"),
    "jira": re.compile(r"\b(?!GS-|RUN-|BL-|CB-|DEC-|AD-|AIP-|ISO-|RFC-|UC-|US-|L-|BCREQ-)[A-Z]{2,10}-\d{2,6}\b"),
    "long_number": re.compile(r"\b\d{6,}\b"),
}


PRACTICE_WORDS = re.compile(r"практик|отраслев|аналог|best practice|лучш\w* практ", re.IGNORECASE)


def leaks(text: str) -> list[str]:
    return [name for name, pattern in LEAKS.items() if pattern.search(text)]


def check(record: dict, origin: str) -> list[str]:
    problems = []
    where = f"{origin}: {record.get('export')} t{record.get('turn')}"
    if tuple(sorted(record)) != tuple(sorted(FIELDS)):
        problems.append(f"{where}: поля {sorted(record)}")
        return problems
    if record["export"] not in EXPORTS:
        problems.append(f"{where}: неизвестная выгрузка")
    if not isinstance(record["turn"], int):
        problems.append(f"{where}: turn не число")
    if record["category"] not in CATEGORIES:
        problems.append(f"{where}: категория {record['category']!r}")
    if record["relevance"] not in RELEVANCE:
        problems.append(f"{where}: актуальность {record['relevance']!r}")
    if not isinstance(record["new_case_candidate"], bool):
        problems.append(f"{where}: new_case_candidate не bool")
    if len(record["summary"]) > SUMMARY_LIMIT:
        problems.append(f"{where}: пересказ длиннее {SUMMARY_LIMIT} знаков")
    for field in ("summary", "where", "industry_analogue", "step", "lesson"):
        found = leaks(str(record[field]))
        if found:
            problems.append(f"{where}: {field}: признаки {found}")
    return problems


def step_code(step: str) -> str:
    match = re.match(r"(Ш-[0-9ВРС]+)", step.strip())
    return match.group(1) if match else (step.strip() or "—")


def lesson_codes(lesson: str) -> list[str]:
    codes = re.findall(r"L-\d+", lesson)
    return codes or ["новый"]


def aggregate(records: list[dict]) -> dict:
    by_relevance = collections.Counter(r["relevance"] for r in records)
    by_category: dict[str, dict[str, int]] = {}
    for category in CATEGORIES:
        rows = [r for r in records if r["category"] == category]
        by_category[category] = {
            "всего": len(rows),
            **{rel: sum(1 for r in rows if r["relevance"] == rel) for rel in RELEVANCE},
        }
    by_step = collections.Counter(step_code(r["step"]) for r in records)
    open_by_step = collections.Counter(
        step_code(r["step"]) for r in records if r["relevance"] != "закрыто"
    )
    by_lesson = collections.Counter(code for r in records for code in lesson_codes(r["lesson"]))
    by_export = {
        export: {
            "записей": sum(1 for r in records if r["export"] == export),
            **{
                rel: sum(1 for r in records if r["export"] == export and r["relevance"] == rel)
                for rel in RELEVANCE
            },
            "практика не предложена": sum(
                1
                for r in records
                if r["export"] == export and r["category"] == "практика не предложена"
            ),
        }
        for export in EXPORTS
    }
    practice = [r for r in records if r["category"] == "практика не предложена"]
    # Записи других категорий, где пересказ говорит об отраслевой практике или
    # аналоге (БА просит или приносит практику сам) — для вопроса владельца.
    mentions = [
        r
        for r in records
        if r["category"] != "практика не предложена" and PRACTICE_WORDS.search(r["summary"])
    ]
    return {
        "records": len(records),
        "by_relevance": {rel: by_relevance.get(rel, 0) for rel in RELEVANCE},
        "by_category": by_category,
        "by_step": dict(sorted(by_step.items())),
        "open_by_step": dict(sorted(open_by_step.items())),
        "by_lesson": dict(sorted(by_lesson.items(), key=lambda item: (-item[1], item[0]))),
        "by_export": by_export,
        "practice_not_offered": {
            "records": len(practice),
            "open": sum(1 for r in practice if r["relevance"] != "закрыто"),
            "by_step": dict(sorted(collections.Counter(step_code(r["step"]) for r in practice).items())),
            "mentioned_in_other_categories": len(mentions),
        },
        "with_industry_analogue": sum(1 for r in records if r["industry_analogue"].strip()),
        "new_case_candidates": [
            {k: r[k] for k in ("export", "turn", "step", "category", "lesson", "relevance", "summary")}
            for r in records
            if r["new_case_candidate"]
        ],
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("coded", nargs="+", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)

    records: list[dict] = []
    problems: list[str] = []
    for path in args.coded:
        data = json.loads(path.read_text(encoding="utf-8"))
        for record in data:
            problems.extend(check(record, path.name))
            records.append(record)
    # Одна реплика БА может нести несколько правок разных категорий: ключ —
    # реплика, категория и пересказ.
    seen = collections.Counter((r["export"], r["turn"], r["category"], r["summary"]) for r in records)
    problems.extend(f"дубль {key}" for key, count in seen.items() if count > 1)
    if problems:
        print("\n".join(problems), file=sys.stderr)
        return 1
    records.sort(key=lambda r: (EXPORTS.index(r["export"]), r["turn"], CATEGORIES.index(r["category"])))

    args.out.mkdir(parents=True, exist_ok=True)
    dump = lambda value: json.dumps(value, ensure_ascii=False, indent=1) + "\n"  # noqa: E731
    (args.out / "coding.json").write_text(dump(records), encoding="utf-8")
    result = aggregate(records)
    (args.out / "aggregate.json").write_text(dump(result), encoding="utf-8")
    print(
        f"OK: {result['records']} записей; актуальность {result['by_relevance']}; "
        f"практика не предложена {result['practice_not_offered']['records']}; "
        f"кандидатов в кейсы {len(result['new_case_candidates'])}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
