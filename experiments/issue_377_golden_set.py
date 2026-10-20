#!/usr/bin/env python3
"""Порождение записи RUN-0076 (issue #377): статистика задачи 1110 и золотые наборы.

Скрипт детерминированно строит из трёх входов:

- ``experiments/issue_377/stats.json`` — вывод
  :mod:`experiments.issue_309_run_stats` по экспорту чата задачи 1110;
- ``experiments/issue_377/quote-check.json`` — вывод
  :mod:`experiments.issue_377_verify_quotes` (сверка цитат с экспортом);
- :mod:`experiments.issue_377_golden_data` — разметка вхождений дефектов,
  позитивных кейсов и критериев успеха.

Режим — гибридный, как в запросе БА к RUN-0073 (PR #374): без обращения к
mango-ba-ai-runtime и без продуктовой принадлежности. Основание разметки —
сам диалог: реакции БА, стандарт BCREQ, который БА передал в реплике 10, и
шаблон-промпт реплики 0.

Порождаются все файлы записи, содержащие числа или цитаты:

- ``metadata.yaml``;
- ``outputs/README.md``, ``outputs/incident-register.md``,
  ``outputs/error-statistics.md``, ``outputs/how-not-to-do.md``,
  ``outputs/golden-set-candidates.md``, ``outputs/golden-set-candidates.json``,
  ``outputs/rubric-candidates.md``, ``outputs/success-criteria.md``,
  ``outputs/prompt-improvements.md``, ``outputs/prompt-usage.md``;
- ``logs/metrics.md``, ``logs/quote-verification.md``.

Провенанс, журнал и ограничения чтения (``inputs/README.md``,
``logs/experiment-log.md``, ``feedback/review-notes.md``) пишутся руками.

Запуск: ``python3 experiments/issue_377_golden_set.py``
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments"))

import issue_377_golden_data as gd  # noqa: E402

DATA = ROOT / "experiments" / "issue_377"
RUN = ROOT / "runs" / "2026" / "RUN-0076"
PREVIOUS = ROOT / "runs" / "2026" / "RUN-0073" / "metadata.yaml"
RUN_ID = "RUN-0076"
TASK = "1110"
ISSUE = "https://github.com/G-Ivan-A/mango_ba_prompts/issues/377"
ATTACHMENT = "https://github.com/user-attachments/files/33669255/chat-export-1110.json"
UPDATED = "2026-10-19"
GENERATOR = "[`experiments/issue_377_golden_set.py`](../../../../experiments/issue_377_golden_set.py)"
DATA_MODULE = "[`experiments/issue_377_golden_data.py`](../../../../experiments/issue_377_golden_data.py)"

#: Человекочитаемые названия эвристических меток операций БА.
KIND_TITLES = {
    "prompt-engineering": "работа с промптом / инструкцией (`prompt-engineering`)",
    "artifact-generation": "запрос на генерацию артефакта (`artifact-generation`)",
    "validation": "проверка и критика результата (`validation`)",
    "elicitation": "элицитация, уточняющие вопросы (`elicitation`)",
    "iteration": "доработка предыдущего ответа (`iteration`)",
    "context-load": "передача контекста и вложений (`context-load`)",
}

#: Наборы золотых кейсов: по группам разделов шаблона (генерация ФТ по разделам).
SETS = [
    ("PRB", "Разделы 1–2: глоссарий, проблема, цель, границы", {"1", "2"}),
    ("FR", "Раздел 3: функциональные требования", {"3"}),
    ("SOL", "Разделы 4–6: описание решения, НФТ, ограничения",
     {"4", "5", "6"}),
    ("DLG", "Ход диалога: статусы, самопроверка, вопросы", {"dialog"}),
    ("PRM", "Шаблон-промпт генерации раздела", {"prompt"}),
]
MAX_DEFECT_CASES = 8
MIN_CASES = 5
MAX_NEGATIVE_CASES = 2

LAG_BUCKETS = [
    ("1 реплика БА", 1, 1),
    ("2–5 реплик", 2, 5),
    ("6–20 реплик", 6, 20),
    ("> 20 реплик", 21, 10**6),
]


# ---------------------------------------------------------------------------
# Подготовка данных
# ---------------------------------------------------------------------------


def parse_utc(value: str) -> dt.datetime:
    return dt.datetime.strptime(value, "%Y-%m-%d %H:%M:%S")


def session_of(stats: dict, utc: str) -> int:
    moment = parse_utc(utc)
    for index, row in enumerate(stats["session_rows"], 1):
        if parse_utc(row["start_utc"]) <= moment <= parse_utc(row["end_utc"]):
            return index
    raise ValueError(f"момент {utc} вне сессий")


def sec345(row: dict) -> str:
    if row["origin"] in ("prompt", "prompt-induced"):
        return "Неоднозначность промпта"
    if row["origin"] == "tooling":
        return "Техническое ограничение"
    return gd.CATEGORIES[row["cat"]]["sec345"]


def enrich(stats: dict) -> list[dict]:
    turns = stats["turn_rows"]
    rows = []
    for row in gd.numbered_incidents():
        cat = gd.CATEGORIES[row["cat"]]
        turn = turns[row["turn"]]
        row = dict(row)
        row["model"] = turn["model"] or "—"
        row["utc"] = turn["utc"]
        row["session"] = session_of(stats, turn["utc"])
        row["section_title"] = gd.SECTIONS[row["sec"]]
        row["babok"] = row.get("babok") or cat["babok"]
        row["oda"] = row.get("oda") or cat["oda"]
        row["primary"] = "BABOK" if row["sec"] in gd.BABOK_SECTIONS else "ODA"
        row["sec345"] = row.get("sec345") or sec345(row)
        row["std"] = cat["std"]
        if row["det_turn"] is not None:
            row["lag_turns"] = (row["det_turn"] - row["turn"] + 1) // 2
            delta = parse_utc(turns[row["det_turn"]]["utc"]) - parse_utc(turn["utc"])
            row["lag_min"] = round(delta.total_seconds() / 60)
            row["confirmed_by"] = "user"
        else:
            row["lag_turns"] = None
            row["lag_min"] = None
            row["confirmed_by"] = "none"
        rows.append(row)
    return rows


def negative_pool() -> list[dict]:
    """Позитивные кейсы и критерии успеха, пригодные как негативный вход набора."""
    pool = []
    for index, row in enumerate(gd.NEGATIVES, 1):
        pool.append({
            "ref": f"N-{index:02d}", "set": row["set"], "turn": row["turn"], "sec": row["sec"],
            "counter": [row["counter"]], "input": row["quote"],
            "why": row["behaviour"], "uq_turn": row["uq_turn"], "uq": row["uq"],
            "confirmed_by": "user" if row["uq"] else "none",
        })
    return pool


def select_cases(rows: list[dict]) -> list[dict]:
    """5–10 кейсов на набор: первое подтверждённое вхождение каждой категории."""
    result = []
    pool = negative_pool()
    for code, title, sections in SETS:
        members = [row for row in rows if row["sec"] in sections]
        counts = Counter(row["cat"] for row in members)
        cats = sorted(counts, key=lambda cat: (-counts[cat], cat))
        chosen: list[dict] = []

        def ranked(cat: str) -> list[dict]:
            items = [row for row in members if row["cat"] == cat]
            return sorted(items, key=lambda row: (row["conf"] != "confirmed", row["turn"]))

        for cat in cats[:MAX_DEFECT_CASES]:
            chosen.append(ranked(cat)[0])
        cursor = 1
        while len(chosen) < MIN_CASES and any(len(ranked(cat)) > cursor for cat in cats):
            for cat in cats:
                items = ranked(cat)
                if len(items) > cursor and len(chosen) < MIN_CASES:
                    chosen.append(items[cursor])
            cursor += 1
        negatives = [row for row in pool if row["set"] == code]
        negatives.sort(key=lambda row: (row["confirmed_by"] != "user", row["turn"]))
        negatives = negatives[:MAX_NEGATIVE_CASES]
        cases = []
        for index, row in enumerate(chosen, 1):
            cases.append({"case_id": f"GS-377-{code}-{index:02d}", "kind": "negative",
                          "incident": row})
        for offset, row in enumerate(negatives, len(chosen) + 1):
            cases.append({"case_id": f"GS-377-{code}-{offset:02d}", "kind": "positive",
                          "clean": row})
        result.append({"code": code, "title": title, "sections": sorted(sections),
                       "cases": cases, "occurrences": len(members), "counts": counts})
    return result


def previous_counts() -> dict[str, int]:
    """Вхождения по категориям в RUN-0073 (задача 1123) — для сравнения прогонов."""
    if not PREVIOUS.is_file():
        return {}
    text = PREVIOUS.read_text(encoding="utf-8")
    block = text.split("  incidents_by_category:\n", 1)[1].split("  incidents_by_product:", 1)[0]
    return {code: int(value) for code, value in re.findall(r"^\s+(C\d+): (\d+)$", block, re.M)}


# ---------------------------------------------------------------------------
# Общие элементы разметки
# ---------------------------------------------------------------------------


def front_matter(doc_type: str, scope: str, extra: list[str] | None = None) -> str:
    lines = [
        "---",
        "status: draft",
        "version: 0.1",
        f"updated: {UPDATED}",
        "ai-generated: true",
        f"type: {doc_type}",
        f"scope: {scope}",
        "related_issues:",
        f'  - "{ISSUE}"',
    ]
    lines.extend(extra or [])
    lines.append("---")
    return "\n".join(lines) + "\n\n"


def generated_banner() -> str:
    return (
        f"> Файл **порождён** скриптом {GENERATOR} из разметки {DATA_MODULE} — "
        "не редактируйте вручную. Каждая цитата сверена с экспортом чата "
        "([`../logs/quote-verification.md`](../logs/quote-verification.md)).\n\n"
    )


def cell(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def quote(text: str) -> str:
    return f"«{cell(text)}»"


def pct(part: int, whole: int) -> str:
    return f"{round(100 * part / whole)}%" if whole else "—"


def babok_ref(codes: list[str]) -> str:
    return "; ".join(codes)


def std_ref(codes: list[str]) -> str:
    return ", ".join(codes) or "—"


def det_label(row: dict) -> str:
    if row["det_turn"] is None:
        return "при фиксации"
    return f"БА, р. {row['det_turn']}"


def lag_label(row: dict) -> str:
    if row["lag_turns"] is None:
        return "—"
    return f"{row['lag_turns']} / {row['lag_min']}"


def answer_turns(stats: dict) -> list[dict]:
    return [row for row in stats["turn_rows"] if row["role"] == "assistant"]


def median_of(values: list[int]) -> str:
    if not values:
        return "—"
    middle = len(values) // 2
    if len(values) % 2:
        return str(values[middle])
    value = (values[middle - 1] + values[middle]) / 2
    return str(int(value)) if value == int(value) else f"{value:.1f}"


def version_key(code: str) -> tuple[int, ...]:
    return tuple(int(part) for part in code.split("."))


def first_user_detection(rows: list[dict]) -> dict[str, int]:
    first: dict[str, int] = {}
    for row in rows:
        if row["det_turn"] is not None:
            first[row["cat"]] = min(first.get(row["cat"], 10**6), row["det_turn"])
    return first


def repeats_after_remark(rows: list[dict]) -> int:
    first = first_user_detection(rows)
    return sum(1 for row in rows if row["cat"] in first and row["turn"] > first[row["cat"]])


# ---------------------------------------------------------------------------
# Рендер
# ---------------------------------------------------------------------------


def incident_register(rows: list[dict]) -> str:
    out = [
        front_matter("artifact", "mango-only", [
            "related_artifacts:",
            '  - "experiments/issue_377_golden_data.py"',
            '  - "experiments/issue_377_verify_quotes.py"',
        ]),
        f"# Реестр вхождений ошибок ИИ — {RUN_ID}, задача {TASK}\n\n",
        generated_banner(),
        "Единица учёта — **вхождение**: повтор той же ошибки в новой реплике модели — "
        f"отдельная строка. Всего вхождений: **{len(rows)}**. Сводные распределения — в "
        "[`error-statistics.md`](error-statistics.md).\n\n",
        "## Легенда колонок\n\n",
        "- **Р.** — номер реплики в линейной ветке экспорта (чётные — БА, 0 — шаблон-промпт; "
        "нечётные — ответы модели).\n",
        "- **Сессия** — рабочая сессия (разрыв > 30 мин), см. [`prompt-usage.md`](prompt-usage.md#сессии).\n",
        "- **Раздел** — раздел документа BCREQ-ФТ (`dialog` — ход диалога вне документа, "
        "`prompt` — текст промпта).\n",
        "- **Кат.** — категория из закрытого словаря (раздел «Категории» ниже).\n",
        "- **Происх.** — " + "; ".join(f"`{k}` — {v}" for k, v in gd.ORIGINS.items()) + ".\n",
        "- **Обнаружение** — `БА, р. N`: БА указал на дефект в реплике N; «при фиксации» — "
        "найдено при сверке со стандартом BCREQ (р. 10), шаблоном и решениями БА, "
        "БА дефект не отметил.\n",
        "- **Задержка** — реплик БА / минут от дефекта до реакции БА.\n",
        "- **Дост.** — " + "; ".join(f"`{k}` — {v}" for k, v in gd.CONFIDENCE.items()) + ".\n",
        "- **Осн.** — основная привязка: BABOK (ФТ — разделы 1–3, 5–6, вопросы, диалог) "
        "или ODA (функциональный дизайн — разделы 4, 7).\n",
        "- **Стандарт** — правило стандарта BCREQ из реплики 10, которое нарушено "
        "(словарь — [`error-statistics.md`](error-statistics.md#11-правила-стандарта-bcreq-реплика-10)).\n",
        "- **#345** — вторичная категория классификации "
        "[RUN-0064](../../RUN-0064/reports/error-analysis.md).\n\n",
        "## Категории\n\n",
        "| Код | Категория | BABOK v3 | ODA | Стандарт BCREQ |\n| --- | --- | --- | --- | --- |\n",
    ]
    for code, cat in gd.CATEGORIES.items():
        out.append(f"| {code} | {cat['title']} | {babok_ref(cat['babok'])} | "
                   f"{cat['oda']} | {std_ref(cat['std'])} |\n")
    out.append("\n## Реестр\n\n")
    out.append("| ID | Р. | Сессия | Раздел | Кат. | Происх. | Обнаружение | Задержка | Дост. | "
               "Осн. | BABOK | ODA | Стандарт | #345 | Цитата | Цитата БА / основание |\n")
    out.append("| --- " * 16 + "|\n")
    for row in rows:
        basis = []
        if row["uq"]:
            basis.append(quote(row["uq"]))
        if row["rule_uq"]:
            basis.append(f"нарушено правило БА, р. {row['rule_turn']}: {quote(row['rule_uq'])}")
        if row["note"]:
            basis.append(cell(row["note"]))
        out.append(
            f"| {row['id']} | {row['turn']} | {row['session']} | {row['sec']} | {row['cat']} | "
            f"{row['origin']} | {det_label(row)} | {lag_label(row)} | {row['conf']} | "
            f"{row['primary']} | {babok_ref(row['babok'])} | {row['oda']} | {std_ref(row['std'])} | "
            f"{row['sec345']} | {quote(row['quote'])} | {'; '.join(basis) or '—'} |\n"
        )
    return "".join(out)


def crosstab(rows: list[dict], key: str, keys: list, titles: dict | None = None) -> list[str]:
    cats = [code for code in gd.CATEGORIES if any(row["cat"] == code for row in rows)]
    out = ["| Значение | Всего | " + " | ".join(cats) + " |\n",
           "| --- | --- | " + " | ".join("---" for _ in cats) + " |\n"]
    for value in keys:
        subset = [row for row in rows if row[key] == value]
        if not subset:
            continue
        counts = Counter(row["cat"] for row in subset)
        label = titles[value] if titles else value
        out.append(f"| {label} | {len(subset)} | "
                   + " | ".join(str(counts.get(cat, 0) or "") for cat in cats) + " |\n")
    total = Counter(row["cat"] for row in rows)
    out.append(f"| **Итого** | **{len(rows)}** | "
               + " | ".join(f"**{total[cat]}**" for cat in cats) + " |\n")
    return out


def error_statistics(rows: list[dict], stats: dict) -> str:
    total = len(rows)
    answers = answer_turns(stats)
    model_rows = [row for row in rows if row["origin"] != "prompt"]
    by_turn = Counter(row["turn"] for row in model_rows)
    first = first_user_detection(rows)
    peak = max(by_turn.values())
    out = [
        front_matter("artifact", "mango-only", [
            "related_artifacts:",
            '  - "runs/2026/RUN-0076/outputs/incident-register.md"',
        ]),
        f"# Статистика ошибок ИИ — {RUN_ID}, задача {TASK}\n\n",
        generated_banner(),
        "Счёт ведётся по вхождениям из [`incident-register.md`](incident-register.md) без "
        "схлопывания повторов (требование issue #377: «Запрещено суммаризировать или "
        "упрощать, важна статистики»).\n\n",
        "## 1. Сводка\n\n",
        "| Показатель | Значение |\n| --- | --- |\n",
        f"| Вхождений всего | {total} |\n",
        f"| В текстах промптов БА | {total - len(model_rows)} |\n",
        f"| В ответах модели | {len(model_rows)} |\n",
        f"| Ответов модели | {len(answers)} |\n",
        f"| Ответов с ≥ 1 вхождением | {len(by_turn)} ({pct(len(by_turn), len(answers))}) |\n",
        f"| Вхождений на ответ модели (среднее) | {len(model_rows) / len(answers):.2f} |\n",
        f"| Максимум вхождений в одном ответе | {peak} (реплика "
        f"{min(t for t, c in by_turn.items() if c == peak)}) |\n",
    ]
    for key, title in gd.DETECTORS.items():
        count = sum(1 for row in rows if row["det"] == key)
        out.append(f"| Обнаружено: {title} | {count} ({pct(count, total)}) |\n")
    for key, title in gd.CONFIDENCE.items():
        count = sum(1 for row in rows if row["conf"] == key)
        out.append(f"| Достоверность: {title} | {count} ({pct(count, total)}) |\n")
    for key, title in gd.ORIGINS.items():
        count = sum(1 for row in rows if row["origin"] == key)
        out.append(f"| Происхождение: {title} | {count} ({pct(count, total)}) |\n")
    repeats = repeats_after_remark(rows)
    out.append(f"| Вхождений после первого замечания БА по той же категории | {repeats} "
               f"({pct(repeats, total)}) |\n")

    out.append("\n## 2. По категориям\n\n")
    out.append("«Повторов после замечания» — вхождения категории в репликах позже первой "
               "реплики, где БА указал на дефект этой категории. Задержка — медиана по "
               "вхождениям, пойманным БА.\n\n")
    out.append("| Код | Категория | Всего | Доля | confirmed | plausible | БА сразу | БА позже | "
               "при фиксации | model | prompt-induced | prompt | tooling | Первая р. | "
               "Последняя р. | Первое замечание БА, р. | Повторов после замечания | "
               "Медиана задержки, реплик БА / мин |\n")
    out.append("| --- " * 18 + "|\n")
    for code, cat in gd.CATEGORIES.items():
        subset = [row for row in rows if row["cat"] == code]
        if not subset:
            out.append(f"| {code} | {cat['title']} | 0 | 0% |" + " — |" * 14 + "\n")
            continue
        count = Counter(row["det"] for row in subset)
        conf = Counter(row["conf"] for row in subset)
        origin = Counter(row["origin"] for row in subset)
        lags = sorted(row["lag_turns"] for row in subset if row["lag_turns"] is not None)
        mins = sorted(row["lag_min"] for row in subset if row["lag_min"] is not None)
        median = f"{median_of(lags)} / {median_of(mins)}" if lags else "—"
        rep = sum(1 for row in subset if code in first and row["turn"] > first[code])
        out.append(
            f"| {code} | {cat['title']} | {len(subset)} | {pct(len(subset), total)} | "
            f"{conf['confirmed']} | {conf['plausible']} | {count['user']} | {count['user-later']} | "
            f"{count['run']} | {origin['model']} | {origin['prompt-induced']} | {origin['prompt']} | "
            f"{origin['tooling']} | {min(r['turn'] for r in subset)} | "
            f"{max(r['turn'] for r in subset)} | {first.get(code, '—')} | "
            f"{rep if code in first else '—'} | {median} |\n"
        )

    out.append("\n## 3. Цепочки повторов после замечания БА\n\n")
    out.append("Для каждой категории, на дефект которой БА указал хотя бы раз: реплика "
               "первого замечания и все последующие реплики модели, где категория "
               "повторилась. Длинная цепочка — признак того, что правило из реплики БА "
               "не закрепилось в контексте и его нужно выносить в промпт раздела.\n\n")
    out.append("| Код | Категория | Первое замечание БА, р. | Повторов | Реплики повторов |\n"
               "| --- | --- | --- | --- | --- |\n")
    for code, cat in gd.CATEGORIES.items():
        if code not in first:
            continue
        later = sorted({row["turn"] for row in rows if row["cat"] == code and row["turn"] > first[code]})
        count = sum(1 for row in rows if row["cat"] == code and row["turn"] > first[code])
        out.append(f"| {code} | {cat['title']} | {first[code]} | {count} | "
                   f"{', '.join(map(str, later)) or '—'} |\n")

    out.append("\n## 4. Раздел документа × категория\n\n")
    out.extend(crosstab(rows, "sec", list(gd.SECTIONS),
                        {k: f"{v} (`{k}`)" for k, v in gd.SECTIONS.items()}))

    out.append("\n## 5. Происхождение × категория\n\n")
    out.extend(crosstab(rows, "origin", list(gd.ORIGINS),
                        {k: f"`{k}`" for k in gd.ORIGINS}))

    out.append("\n## 6. Сессии\n\n")
    out.append("| Сессия | Начало, UTC | Ответов модели | Вхождений | На ответ | Категории (вхождений) |\n"
               "| --- | --- | --- | --- | --- | --- |\n")
    for index, session in enumerate(stats["session_rows"], 1):
        in_session = [row for row in answers if session_of(stats, row["utc"]) == index]
        hits = [row for row in rows if row["session"] == index]
        cats = Counter(row["cat"] for row in hits)
        listing = ", ".join(f"{cat} ×{n}" for cat, n in sorted(cats.items())) or "—"
        per = f"{len(hits) / len(in_session):.2f}" if in_session else "—"
        out.append(f"| {index} | {session['start_utc']} | {len(in_session)} | {len(hits)} | "
                   f"{per} | {listing} |\n")

    out.append("\n## 7. Каждый ответ модели\n\n")
    out.append("Перечислены все ответы, включая ответы без вхождений.\n\n")
    out.append("| Р. | Модель | UTC | out_tokens | Вхождений | Категории | ID |\n"
               "| --- | --- | --- | --- | --- | --- | --- |\n")
    for answer in answers:
        hits = [row for row in model_rows if row["turn"] == answer["index"]]
        cats = Counter(row["cat"] for row in hits)
        listing = ", ".join(f"{cat} ×{n}" for cat, n in sorted(cats.items())) or "—"
        ids = ", ".join(row["id"] for row in hits) or "—"
        out.append(f"| {answer['index']} | {answer['model']} | {answer['utc']} | "
                   f"{answer['output_tokens']} | {len(hits)} | {listing} | {ids} |\n")

    out.append("\n## 8. BABOK v3 (ФТ)\n\n")
    out.append("Одно вхождение может относиться к нескольким задачам/техникам, поэтому "
               "сумма больше числа вхождений. «Осн. BABOK» — только вхождения разделов, "
               "для которых BABOK — основная привязка.\n\n")
    out.append("| Код | Задача / техника | Вхождений | Осн. BABOK |\n| --- | --- | --- | --- |\n")
    for code, title in sorted(gd.BABOK.items(), key=lambda item: version_key(item[0])):
        count = sum(1 for row in rows if code in row["babok"])
        primary = sum(1 for row in rows if code in row["babok"] and row["primary"] == "BABOK")
        out.append(f"| {code} | {title} | {count} | {primary} |\n")

    out.append("\n## 9. TM Forum ODA (функциональный дизайн)\n\n")
    out.append("| Сегмент | Описание | Вхождений | Осн. ODA |\n| --- | --- | --- | --- |\n")
    for code, title in gd.ODA.items():
        count = sum(1 for row in rows if row["oda"] == code)
        primary = sum(1 for row in rows if row["oda"] == code and row["primary"] == "ODA")
        out.append(f"| {code} | {title} | {count} | {primary} |\n")

    out.append("\n## 10. Вторичная классификация issue #345\n\n")
    out.append("| Категория #345 | Вхождений | Доля |\n| --- | --- | --- |\n")
    for key, count in Counter(row["sec345"] for row in rows).most_common():
        out.append(f"| {key} | {count} | {pct(count, total)} |\n")

    out.append("\n## 11. Правила стандарта BCREQ (реплика 10)\n\n")
    out.append("Стандарт формирования BCREQ-документации БА передал модели в реплике 10. "
               "Категория считается нарушением правила, если правило прямо запрещает "
               "дефект; «—» — правило в стандарте отсутствует (пробел, см. "
               "[`prompt-improvements.md`](prompt-improvements.md)).\n\n")
    out.append("| Правило | Содержание | Категории | Вхождений |\n| --- | --- | --- | --- |\n")
    for code, title in gd.STANDARD.items():
        codes = [c for c, cat in gd.CATEGORIES.items() if code in cat["std"]]
        count = sum(1 for row in rows if row["cat"] in codes)
        out.append(f"| {code} | {title} | {', '.join(codes) or '—'} | {count} |\n")
    uncovered = [c for c, cat in gd.CATEGORIES.items() if not cat["std"]]
    count = sum(1 for row in rows if row["cat"] in uncovered)
    out.append(f"| — | правила нет | {', '.join(uncovered) or '—'} | {count} |\n")

    out.append("\n## 12. Задержка обнаружения БА\n\n")
    caught = [row for row in rows if row["lag_turns"] is not None]
    out.append("| Задержка | Вхождений | Доля от пойманных БА |\n| --- | --- | --- |\n")
    for title, low, high in LAG_BUCKETS:
        count = sum(1 for row in caught if low <= row["lag_turns"] <= high)
        out.append(f"| {title} | {count} | {pct(count, len(caught))} |\n")
    if caught:
        out.append(f"\nМедиана: {median_of(sorted(r['lag_turns'] for r in caught))} реплик БА, "
                   f"{median_of(sorted(r['lag_min'] for r in caught))} мин; максимум: "
                   f"{max(r['lag_turns'] for r in caught)} реплик БА.\n")

    previous = previous_counts()
    if previous:
        out.append("\n## 13. Сравнение с RUN-0073 (задача 1123)\n\n")
        out.append("Обе записи размечены одним словарём категорий C01–C19, поэтому доли "
                   "сопоставимы; абсолютные числа — нет (разная длина диалогов). Новые "
                   "категории этой записи в RUN-0073 не размечались.\n\n")
        prev_total = sum(previous.values())
        out.append(f"| Код | Категория | {RUN_ID}, вхождений | {RUN_ID}, доля | "
                   "RUN-0073, вхождений | RUN-0073, доля |\n| --- | --- | --- | --- | --- | --- |\n")
        counts = Counter(row["cat"] for row in rows)
        for code, cat in gd.CATEGORIES.items():
            prev = previous.get(code)
            prev_cells = f"{prev} | {pct(prev, prev_total)}" if prev is not None else "— | —"
            out.append(f"| {code} | {cat['title']} | {counts[code]} | {pct(counts[code], total)} | "
                       f"{prev_cells} |\n")
        out.append(f"| | **Итого** | **{total}** | | **{prev_total}** | |\n")
    return "".join(out)


def how_not_to_do(rows: list[dict]) -> str:
    counts = Counter(row["cat"] for row in rows)
    out = [
        front_matter("artifact", "prompts", [
            "related_artifacts:",
            '  - "runs/2026/RUN-0076/outputs/incident-register.md"',
        ]),
        f"# Как не надо делать — общий список ({RUN_ID}, задача {TASK})\n\n",
        generated_banner(),
        "Список — вход для промптов, правил и навыков генерации BCREQ-ФТ по разделам. "
        "Продуктовая принадлежность не определяется (режим, заданный БА в PR #374). "
        "Часть 1 — правила «не надо / надо» по категориям в порядке частоты; часть 2 — "
        "**все** вхождения по разделам документа (без схлопывания), чтобы правило можно "
        "было проверить на реальных формулировках.\n\n",
        "## 1. Правила по категориям\n\n",
        "| # | Код | Не надо | Надо | Вхождений | Разделы | Стандарт BCREQ |\n"
        "| --- | --- | --- | --- | --- | --- | --- |\n",
    ]
    for index, code in enumerate(sorted(counts, key=lambda c: (-counts[c], c)), 1):
        cat = gd.CATEGORIES[code]
        secs = Counter(row["sec"] for row in rows if row["cat"] == code)
        listing = ", ".join(f"{s} ×{n}" for s, n in sorted(secs.items(), key=lambda i: -i[1]))
        out.append(f"| {index} | {code} | {cat['antipattern']} | {cat['guard']} | {counts[code]} | "
                   f"{listing} | {std_ref(cat['std'])} |\n")
    out.append("\n## 2. Вхождения по разделам документа\n")
    for key, title in gd.SECTIONS.items():
        subset = [row for row in rows if row["sec"] == key]
        if not subset:
            continue
        out.append(f"\n### {title} (`{key}`) — {len(subset)} вхождений\n")
        sec_counts = Counter(row["cat"] for row in subset)
        for code in sorted(sec_counts, key=lambda c: (-sec_counts[c], c)):
            cat = gd.CATEGORIES[code]
            items = [row for row in subset if row["cat"] == code]
            out.append(f"\n#### {code}. {cat['title']} — {len(items)}\n\n")
            out.append(f"- **Не надо:** {cat['antipattern']}.\n")
            out.append(f"- **Надо:** {cat['guard']}.\n\n")
            out.append("| ID | Р. | Цитата | Что не так | Обнаружение |\n| --- | --- | --- | --- | --- |\n")
            for row in items:
                out.append(f"| {row['id']} | {row['turn']} | {quote(row['quote'])} | "
                           f"{cell(row['note']) or '—'} | {det_label(row)} |\n")
    return "".join(out)


def golden_candidates(sets: list[dict]) -> str:
    out = [
        front_matter("artifact", "prompts", [
            "related_artifacts:",
            '  - "standards/evals-contract-standard.md"',
            '  - "runs/2026/RUN-0076/outputs/rubric-candidates.md"',
            '  - "runs/2026/RUN-0076/outputs/golden-set-candidates.json"',
        ]),
        f"# Кандидаты в золотые наборы инцидентов генерации BCREQ-ФТ — {RUN_ID}\n\n",
        generated_banner(),
        "## Назначение\n\n",
        "Кандидаты в golden-set по "
        "[`standards/evals-contract-standard.md`](../../../../standards/evals-contract-standard.md): "
        "наборы по **5–10 кейсов**, по одному набору на группу разделов документа, — под "
        f"посекционную генерацию BCREQ-ФТ. Вход каждого кейса — реальная формулировка "
        f"модели или промпта из экспорта задачи {TASK} (дословно, сверено). Эталонный "
        "вердикт агента-проверяющего: для дефектного кейса — «дефект» с указанным классом, "
        "для негативного кейса — «дефекта нет».\n\n",
        "Это **запись прогона**, а не контракт: стандарт запрещает смешивать эталон и "
        "факт, а контейнер golden-set в этом споке не выбран (см. "
        "[`../feedback/review-notes.md`](../feedback/review-notes.md)).\n\n",
        "Правило отбора (детерминированное): в наборе категории упорядочены по числу "
        f"вхождений; для каждой из первых {MAX_DEFECT_CASES} берётся первое подтверждённое "
        "вхождение (если подтверждённых нет — первое вероятное); если категорий меньше "
        f"{MIN_CASES}, добираются следующие вхождения тех же категорий. Негативных кейсов — "
        f"до {MAX_NEGATIVE_CASES}, сначала подтверждённые БА. Полный список вхождений — в "
        "[`how-not-to-do.md`](how-not-to-do.md).\n\n",
    ]
    for item in sets:
        out.append(f"## Набор GS-377-{item['code']} — {item['title']}\n\n")
        out.append(f"Разделы: {', '.join(item['sections'])}. Вхождений в группе: "
                   f"{item['occurrences']}. Кейсов: {len(item['cases'])}.\n\n")
        out.append("| case-id | Вход | Эталонный вердикт | Класс дефекта | Обоснование эталона | "
                   "Контекст | Источник |\n| --- | --- | --- | --- | --- | --- | --- |\n")
        for case in item["cases"]:
            if case["kind"] == "negative":
                row = case["incident"]
                cat = gd.CATEGORIES[row["cat"]]
                reason = [f"реплика {row['turn']}"]
                if row["uq"]:
                    reason.append(f"БА, р. {row['det_turn']}: {quote(row['uq'])}")
                if row["note"]:
                    reason.append(cell(row["note"]))
                out.append(
                    f"| {case['case_id']} | {quote(row['quote'])} | дефект | {row['cat']} — "
                    f"{cat['title']} | {'; '.join(reason)} | раздел {row['sec']}; BABOK "
                    f"{babok_ref(row['babok'])}; ODA {row['oda']} | {row['id']}, {row['conf']} |\n"
                )
            else:
                row = case["clean"]
                reason = [cell(row["why"])]
                if row["uq"]:
                    reason.append(f"БА, р. {row['uq_turn']}: {quote(row['uq'])}")
                out.append(
                    f"| {case['case_id']} | {quote(row['input'])} | дефекта нет | — (против "
                    f"{', '.join(row['counter'])}) | {'; '.join(reason)} | раздел {row['sec']} | "
                    f"{row['ref']}, реплика {row['turn']}, confirmed_by: {row['confirmed_by']} |\n"
                )
        covered = sorted({c["incident"]["cat"] for c in item["cases"] if c["kind"] == "negative"})
        missed = sorted(set(item["counts"]) - set(covered))
        out.append("\n**Покрытие.** Категории в наборе: "
                   f"{', '.join(covered) or 'нет'}. Есть в группе, но вне набора (лимит "
                   f"{MAX_DEFECT_CASES} категорий): {', '.join(missed) or 'нет'}.\n\n")
    return "".join(out)


def golden_json(sets: list[dict]) -> str:
    payload = {
        "golden_set": "run-0074-bcreq-fr-sections",
        "version": "0.1",
        "status": "draft",
        "source": ISSUE,
        "sets": [],
    }
    for item in sets:
        cases = []
        for case in item["cases"]:
            if case["kind"] == "negative":
                row = case["incident"]
                cases.append({
                    "id": case["case_id"],
                    "kind": "negative",
                    "origin": "run-observed",
                    "confirmed_by": row["confirmed_by"],
                    "artifact_class": "A-BCREQ",
                    "section": row["sec"],
                    "input": row["quote"],
                    "source": {"incident": row["id"], "turn": row["turn"], "model": row["model"]},
                    "babok": row["babok"],
                    "oda": row["oda"],
                    "standard": row["std"],
                    "expect": {"outcome": "refused", "defect_class": row["cat"],
                               "reason": gd.CATEGORIES[row["cat"]]["guard"]},
                })
            else:
                row = case["clean"]
                cases.append({
                    "id": case["case_id"],
                    "kind": "positive",
                    "origin": "run-observed",
                    "confirmed_by": row["confirmed_by"],
                    "artifact_class": "A-BCREQ",
                    "section": row["sec"],
                    "input": row["input"],
                    "source": {"ref": row["ref"], "turn": row["turn"]},
                    "expect": {"outcome": "completed", "no_defect_of": row["counter"]},
                })
        payload["sets"].append({"id": f"GS-377-{item['code']}", "title": item["title"],
                                "sections": item["sections"], "cases": cases})
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def rubric(rows: list[dict]) -> str:
    out = [
        front_matter("artifact", "prompts", [
            "related_artifacts:",
            '  - "standards/evals-contract-standard.md"',
            '  - "runs/2026/RUN-0076/outputs/golden-set-candidates.md"',
        ]),
        f"# Кандидат в рубрику приёмки — {RUN_ID}\n\n",
        generated_banner(),
        "Все критерии бинарные (да/нет) по "
        "[`standards/evals-contract-standard.md`](../../../../standards/evals-contract-standard.md#рубрика-приёмки). "
        "Базовые пять критериев сохранены; к ним добавлены критерии-стражи по категориям "
        "дефектов, встреченным в прогоне. Веса не задаются.\n\n",
        "## Базовые критерии\n\n",
        "| Критерий | Наблюдаемый признак | Провал = |\n| --- | --- | --- |\n",
        "| Дефект найден | Для кейса `дефект` агент вернул вердикт «дефект» | Пропуск дефекта (ложный «ок») |\n",
        "| Тип верен | Класс в вердикте совпал с `Класс дефекта` кейса | Неверная категория |\n",
        "| Обоснование корректно | Вердикт ссылается на фрагмент входа кейса | «Галлюцинация» причины |\n",
        "| Нет ложных срабатываний | Для кейса `дефекта нет` агент не вернул «дефект» | Шум / over-flagging |\n",
        "| Формат вердикта | Выход — вердикт по контракту промпта проверки | Невалидная форма |\n",
        "\n## Критерии-стражи по категориям\n\n",
        "Применяются к **сгенерированному разделу** (не только к кейсам набора): каждый "
        "даёт «да», если признака провала в выходе нет.\n\n",
        "| Код | Критерий | Наблюдаемый признак | Провал = | Вхождений в прогоне | Стандарт BCREQ |\n"
        "| --- | --- | --- | --- | --- | --- |\n",
    ]
    counts = Counter(row["cat"] for row in rows)
    for code, cat in gd.CATEGORIES.items():
        if not counts[code]:
            continue
        out.append(f"| R-{code} | {cat['title']} отсутствует | {cat['guard']} | "
                   f"{cat['antipattern']} | {counts[code]} | {std_ref(cat['std'])} |\n")
    return "".join(out)


def success_criteria(rows: list[dict]) -> str:
    counts = Counter(row["cat"] for row in rows)
    out = [
        front_matter("artifact", "prompts", [
            "related_artifacts:",
            '  - "runs/2026/RUN-0076/outputs/golden-set-candidates.md"',
        ]),
        f"# Золотой набор критериев успешного формирования требований — {RUN_ID}, задача {TASK}\n\n",
        generated_banner(),
        "Критерий успеха — правило, которое БА сформулировал в диалоге (замечание, "
        "решение, стандарт BCREQ реплики 10). У каждого критерия — дословная цитата БА, "
        "раздел документа, категории дефектов, которые он предотвращает, с числом "
        "вхождений этих категорий в прогоне (столбец «Нарушений в прогоне» — сколько раз "
        "модель нарушила критерий), BABOK / ODA.\n\n",
        "## 1. Критерии успеха по разделам\n",
    ]
    for key, title in gd.SECTIONS.items():
        items = [row for row in gd.SUCCESS_CRITERIA if row["sec"] == key]
        if not items:
            continue
        out.append(f"\n### {title} (`{key}`)\n\n")
        out.append("| ID | Р. | Критерий | Цитата БА | Против категорий (вхождений) | "
                   "Нарушений в прогоне | BABOK | ODA |\n"
                   "| --- | --- | --- | --- | --- | --- | --- | --- |\n")
        for row in items:
            against = ", ".join(f"{c} ({counts[c]})" for c in row["counters"])
            violations = sum(counts[c] for c in row["counters"])
            babok = sorted({b for c in row["counters"] for b in gd.CATEGORIES[c]["babok"]},
                           key=version_key)
            oda = sorted({gd.CATEGORIES[c]["oda"] for c in row["counters"]})
            out.append(f"| {row['id']} | {row['turn']} | {row['criterion']} | {quote(row['uq'])} | "
                       f"{against} | {violations} | {babok_ref(babok)} | {', '.join(oda)} |\n")
    out.append("\n## 2. Покрытие категорий критериями\n\n")
    out.append("Категория без критерия — кандидат на новое правило промпта.\n\n")
    out.append("| Код | Категория | Вхождений | Критерии |\n| --- | --- | --- | --- |\n")
    for code, cat in gd.CATEGORIES.items():
        ids = [row["id"] for row in gd.SUCCESS_CRITERIA if code in row["counters"]]
        out.append(f"| {code} | {cat['title']} | {counts[code]} | {', '.join(ids) or '**нет**'} |\n")
    out.append("\n## 3. Позитивные кейсы поведения модели\n\n")
    out.append("Ответы модели, где дефекта нет и поведение соответствует правилам (часть — "
               "с подтверждением БА). Используются как негативные кейсы золотых наборов.\n\n")
    out.append("| ID | Р. | Набор | Раздел | Цитата модели | Поведение | Против | Подтверждение БА |\n"
               "| --- | --- | --- | --- | --- | --- | --- | --- |\n")
    for index, row in enumerate(gd.NEGATIVES, 1):
        confirm = f"р. {row['uq_turn']}: {quote(row['uq'])}" if row["uq"] else "—"
        out.append(f"| N-{index:02d} | {row['turn']} | GS-377-{row['set']} | {row['sec']} | "
                   f"{quote(row['quote'])} | {cell(row['behaviour'])} | {row['counter']} | {confirm} |\n")
    return "".join(out)


def prompt_improvements(rows: list[dict]) -> str:
    counts = Counter(row["cat"] for row in rows)
    first = first_user_detection(rows)
    out = [
        front_matter("artifact", "prompts", [
            "related_artifacts:",
            '  - "runs/2026/RUN-0076/outputs/how-not-to-do.md"',
            '  - "runs/2026/RUN-0076/outputs/success-criteria.md"',
        ]),
        f"# Предложения для промптов и стандарта BCREQ — {RUN_ID}\n\n",
        generated_banner(),
        "Ненормативно. Каждое предложение опирается на число вхождений из "
        "[`error-statistics.md`](error-statistics.md). Режим гибридный: "
        "mango-ba-ai-runtime не читался и не правится.\n\n",
        "## 1. Пробелы стандарта BCREQ (реплика 10)\n\n",
        "Категории, для которых в стандарте нет запрещающего правила; «Надо» — "
        "предлагаемая формулировка правила.\n\n",
        "| Категория | Вхождений | Повторов после замечания БА | Предлагаемое правило |\n"
        "| --- | --- | --- | --- |\n",
    ]
    for code, cat in gd.CATEGORIES.items():
        if cat["std"] or not counts[code]:
            continue
        rep = sum(1 for row in rows if row["cat"] == code and code in first and row["turn"] > first[code])
        out.append(f"| {code} {cat['title']} | {counts[code]} | {rep} | {cat['guard']} |\n")
    out.append("\n## 2. Правила, которые есть, но не удержались\n\n")
    out.append("Категории с правилом в стандарте и повторами после замечания БА: правило "
               "нужно дублировать в промпт каждого раздела и в чек-лист самопроверки.\n\n")
    out.append("| Категория | Правило стандарта | Вхождений | Повторов после замечания БА |\n"
               "| --- | --- | --- | --- |\n")
    for code, cat in gd.CATEGORIES.items():
        if not cat["std"] or code not in first:
            continue
        rep = sum(1 for row in rows if row["cat"] == code and row["turn"] > first[code])
        if rep:
            out.append(f"| {code} {cat['title']} | {std_ref(cat['std'])} | {counts[code]} | {rep} |\n")
    out.append("\n## 3. Тексты промптов БА\n\n")
    out.append("Каждая строка — дословный фрагмент промпта (шаблон реплики 0 или промпт, "
               "переданный позже) и его следствие в прогоне.\n\n")
    out.append("| ID | Р. | Фрагмент | Следствие | Обнаружение |\n| --- | --- | --- | --- | --- |\n")
    for row in rows:
        if row["origin"] == "prompt":
            out.append(f"| {row['id']} | {row['turn']} | {quote(row['quote'])} | "
                       f"{cell(row['note'])} | {det_label(row)} |\n")
    out.append("\n## 4. Улучшения отчёта относительно RUN-0073\n\n")
    out.append(
        "- Цепочки повторов после замечания БА по каждой категории "
        "([`error-statistics.md` § 3](error-statistics.md#3-цепочки-повторов-после-замечания-ба)) — "
        "показывают, какие правила не удерживаются в контексте.\n"
        "- Привязка категорий к правилам стандарта BCREQ из диалога вместо правил runtime "
        "([§ 11](error-statistics.md#11-правила-стандарта-bcreq-реплика-10)) и список пробелов "
        "стандарта (раздел 1 выше).\n"
        "- Сравнение долей категорий с RUN-0073 "
        "([§ 13](error-statistics.md#13-сравнение-с-run-0073-задача-1123)).\n"
        "- «Как не надо» — общий список по категориям и по разделам документа (без продуктов) "
        "с пояснением каждого вхождения ([`how-not-to-do.md`](how-not-to-do.md)).\n"
        "- Критерии успеха сгруппированы по разделам и показывают число нарушений и "
        "категории без критерия ([`success-criteria.md`](success-criteria.md)).\n"
    )
    return "".join(out)


def prompt_usage(stats: dict) -> str:
    user_turns = stats["user_turns"]
    out = [
        front_matter("artifact", "prompts", [
            "related_artifacts:",
            '  - "experiments/issue_377_golden_set.py"',
        ]),
        f"# Операции процесса БА в прогоне {RUN_ID}\n\n",
        f"> Файл **порождён** скриптом {GENERATOR} — не редактируйте вручную.\n\n",
        "## Распределение запросов БА\n\n",
        "Разметка **эвристическая**: тип операции определяется по ключевым словам "
        "реплики БА (правила — в "
        "[`experiments/issue_309_run_stats.py`](../../../../experiments/issue_309_run_stats.py), "
        "константа `REQUEST_KINDS`). Метки не взаимоисключающие, поэтому сумма по "
        "столбцу может превышать число реплик.\n\n",
        "| Операция | Реплик БА | Доля от реплик БА |\n| --- | --- | --- |\n",
    ]
    for kind, title in KIND_TITLES.items():
        count = stats["request_kinds"].get(kind, 0)
        out.append(f"| {title} | {count} | {round(100 * count / user_turns)}% |\n")
    unknown = stats["requests_unclassified"]
    out.append(
        f"| _не распознано эвристикой_ | {unknown} | {round(100 * unknown / user_turns)}% |\n"
    )
    out.append("\n## Сессии\n\n")
    out.append("| # | Начало, UTC | Конец, UTC | Реплик | Длительность, мин |\n")
    out.append("| --- | --- | --- | --- | --- |\n")
    for i, row in enumerate(stats["session_rows"], 1):
        out.append(
            f"| {i} | {row['start_utc']} | {row['end_utc']} | "
            f"{row['messages']} | {row['minutes']} |\n"
        )
    out.append("\n## Вложения диалога\n\n")
    out.append("| Файл | Прикреплён к репликам |\n| --- | --- |\n")
    for name, count in sorted(stats["attachments"].items()):
        out.append(f"| `{name}` | {count} |\n")
    return "".join(out)


def metrics(stats: dict) -> str:
    out = [
        front_matter("artifact", "mango-only"),
        f"# Метрики прогона {RUN_ID} (измеренные)\n\n",
        "> Файл **порождён** из экспорта чата — не редактируйте вручную. Все числа "
        "взяты из полей `usage` и `timestamp` самого экспорта и не являются оценкой.\n\n",
        "| # | Роль | Модель | UTC | Символов | in_tokens | out_tokens | reasoning | Вложений |\n",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |\n",
    ]
    for row in stats["turn_rows"]:
        out.append(
            f"| {row['index']} | {row['role']} | {row['model']} | {row['utc']} | "
            f"{row['chars']} | {row['input_tokens']} | {row['output_tokens']} | "
            f"{row['reasoning_tokens']} | {len(row['files'])} |\n"
        )
    out.append(
        f"\n- **turns:** {stats['turns']}\n"
        f"- **input_tokens:** {stats['tokens_input_sum']}\n"
        f"- **output_tokens:** {stats['tokens_output']}\n"
        f"- **reasoning_tokens:** {stats['tokens_reasoning']}\n"
    )
    return "".join(out)


def quote_verification(check: dict) -> str:
    kinds = Counter(row["kind"] for row in check["rows"])
    ambiguous = [row for row in check["rows"] if len(row["found_turns"]) > 1]
    out = [
        front_matter("log", "mango-only", [
            "related_artifacts:",
            '  - "experiments/issue_377_verify_quotes.py"',
        ]),
        f"# Журнал сверки цитат прогона {RUN_ID}\n\n",
        f"> Файл **порождён** скриптом {GENERATOR} из вывода "
        "[`experiments/issue_377_verify_quotes.py`](../../../../experiments/issue_377_verify_quotes.py)"
        " — не редактируйте вручную.\n\n",
        "Каждая цитата разметки искалась в тексте заявленной реплики экспорта после "
        "нормализации (пробелы схлопнуты, `*` и `` ` `` удалены). Текст экспорта в журнал "
        "не копируется: фиксируется SHA-256 нормализованной цитаты.\n\n",
        f"- SHA-256 экспорта: `{check['export_sha256']}`\n",
        f"- Реплик в ветке: {check['messages']}\n",
        f"- Цитат проверено: {check['checked']}; не найдено в заявленной реплике: "
        f"**{check['missing']}**\n",
        f"- Встречаются ещё и в других репликах: {len(ambiguous)} (заявленная реплика "
        "входит в список найденных — привязка однозначна по номеру реплики)\n\n",
        "| Вид цитаты | Проверено |\n| --- | --- |\n",
    ]
    for kind, count in sorted(kinds.items()):
        out.append(f"| `{kind}` | {count} |\n")
    out.append("\n| Ссылка | Вид | Реплика | Найдена | Также в репликах | SHA-256 (нормализованной) |\n"
               "| --- | --- | --- | --- | --- | --- |\n")
    for row in check["rows"]:
        others = [t for t in row["found_turns"] if t != row["turn"]]
        out.append(f"| {row['ref']} | `{row['kind']}` | {row['turn']} | "
                   f"{'да' if row['found'] else '**нет**'} | "
                   f"{', '.join(map(str, others)) or '—'} | `{row['sha256'][:16]}` |\n")
    return "".join(out)


def outputs_readme(rows: list[dict], stats: dict, sets: list[dict]) -> str:
    cases = sum(len(item["cases"]) for item in sets)
    counts = Counter(row["cat"] for row in rows)
    top = ", ".join(f"{cat} ({n})" for cat, n in counts.most_common(5))
    caught = sum(1 for row in rows if row["det"] != "run")
    out = [
        front_matter("index", "mango-only"),
        f"# Результаты прогона {RUN_ID} — задача {TASK}, золотые наборы ошибок ИИ и критериев успеха\n\n",
        generated_banner(),
        f"Прогон фиксирует диалог генерации BCREQ-ФТ по задаче {TASK} (доработка "
        "распределения попытки вызова кампании исходящего обзвона на операторов из "
        "переданного внешней системой списка) ради статистики ошибок ИИ. Результат — не "
        "артефакт требований, а размеченный по вхождениям реестр ошибок с привязкой к "
        "разделам документа, BABOK / TM Forum ODA и стандарту BCREQ из диалога, золотой "
        "набор инцидентов («как не надо») и золотой набор критериев успешного формирования "
        "требований — данные для промптов, правил и навыков посекционной генерации ФТ.\n\n",
        "## Сводка\n\n",
        "| Метрика | Значение |\n| --- | --- |\n",
        f"| Реплик в ветке диалога | {stats['turns']} |\n",
        f"| Реплик БА / ответов модели | {stats['user_turns']} / {stats['assistant_turns']} |\n",
        f"| Модели | {', '.join(stats['models'])} |\n",
        f"| Рабочих сессий (разрыв > 30 мин) | {stats['sessions']} |\n",
        f"| Активное время внутри сессий, мин | {stats['active_minutes']} |\n",
        f"| Календарный интервал, дн. | {stats['calendar_days']} |\n",
        f"| Токенов на входе (с переотправкой контекста) | {stats['tokens_input_sum']} |\n",
        f"| Токенов на выходе / в том числе reasoning | {stats['tokens_output']} / "
        f"{stats['tokens_reasoning']} |\n",
        f"| Вхождений ошибок ИИ | {len(rows)} |\n",
        f"| Категорий с вхождениями | {len(counts)} из {len(gd.CATEGORIES)} |\n",
        f"| Самые частые категории | {top} |\n",
        f"| Поймано БА в диалоге | {caught} ({pct(caught, len(rows))}) |\n",
        f"| Повторов после первого замечания БА | {repeats_after_remark(rows)} |\n",
        f"| Наборов-кандидатов / кейсов | {len(sets)} / {cases} |\n",
        f"| Критериев успеха / позитивных кейсов | {len(gd.SUCCESS_CRITERIA)} / {len(gd.NEGATIVES)} |\n",
        "\n## Состав записи\n\n",
        "| Файл | Что содержит |\n| --- | --- |\n",
        "| [`incident-register.md`](incident-register.md) | реестр всех вхождений с цитатами и привязками |\n",
        "| [`error-statistics.md`](error-statistics.md) | распределения: категории, цепочки повторов, разделы, происхождение, сессии, ответы, BABOK, ODA, стандарт BCREQ, задержка, сравнение с RUN-0073 |\n",
        "| [`how-not-to-do.md`](how-not-to-do.md) | золотой набор инцидентов: общий список «как не надо» — правила по категориям и все вхождения по разделам |\n",
        "| [`golden-set-candidates.md`](golden-set-candidates.md) | кандидаты в золотые наборы по группам разделов (5–10 кейсов) |\n",
        "| [`golden-set-candidates.json`](golden-set-candidates.json) | те же кейсы в машиночитаемом виде |\n",
        "| [`rubric-candidates.md`](rubric-candidates.md) | бинарная рубрика: базовые критерии и стражи по категориям |\n",
        "| [`success-criteria.md`](success-criteria.md) | золотой набор критериев успешного формирования требований и позитивных кейсов |\n",
        "| [`prompt-improvements.md`](prompt-improvements.md) | предложения для промптов и стандарта BCREQ, улучшения отчёта |\n",
        "| [`prompt-usage.md`](prompt-usage.md) | распределение операций БА, сессии, вложения |\n",
        "| [`../logs/metrics.md`](../logs/metrics.md) | метрики по каждой реплике |\n",
        "| [`../logs/quote-verification.md`](../logs/quote-verification.md) | сверка каждой цитаты с экспортом |\n",
        "| [`../logs/experiment-log.md`](../logs/experiment-log.md) | как получена запись |\n",
        "| [`../inputs/README.md`](../inputs/README.md) | провенанс исходного экспорта |\n",
        "| [`../feedback/review-notes.md`](../feedback/review-notes.md) | ограничения чтения и открытые вопросы |\n",
    ]
    return "".join(out)


def metadata(rows: list[dict], stats: dict, sets: list[dict], check: dict) -> str:
    counts = Counter(row["cat"] for row in rows)
    det = Counter(row["det"] for row in rows)
    conf = Counter(row["conf"] for row in rows)
    secs = Counter(row["sec"] for row in rows)
    lines = [
        f"run_id: {RUN_ID}",
        "process: task-1110-bcreq-fr-cc-operator-distribution-error-golden-set",
        'version: "0.1"',
        f"date: {UPDATED}",
        'author: "BA-IH + LLM (фиксация прогона: AI issue solver)"',
        f'model: "{", ".join(stats["models"])}"',
        "status: draft",
        "run_type: statistics",
        "source_paths:",
        f"  - {ISSUE}",
        f"  - {ATTACHMENT}",
        "inputs:",
        "  - inputs/README.md",
        "outputs:",
        "  - outputs/README.md",
        "  - outputs/incident-register.md",
        "  - outputs/error-statistics.md",
        "  - outputs/how-not-to-do.md",
        "  - outputs/golden-set-candidates.md",
        "  - outputs/golden-set-candidates.json",
        "  - outputs/rubric-candidates.md",
        "  - outputs/success-criteria.md",
        "  - outputs/prompt-improvements.md",
        "  - outputs/prompt-usage.md",
        "logs:",
        "  - logs/experiment-log.md",
        "  - logs/metrics.md",
        "  - logs/quote-verification.md",
        "feedback:",
        "  - feedback/review-notes.md",
        "metrics:",
        f"  episodes: {stats['user_turns']}",
        f"  iterations: {stats['assistant_turns']}",
        f"  turns: {stats['turns']}",
        f"  sessions: {stats['sessions']}",
        f"  tokens_input: {stats['tokens_input_sum']}",
        f"  tokens_output: {stats['tokens_output']}",
        f"  tokens_thinking: {stats['tokens_reasoning']}",
        f"  tokens_dialog_total: {stats['tokens_input_sum'] + stats['tokens_output']}",
        f'  token_method: "provider-usage:{",".join(stats["models"])}"',
        f"  duration_active_s: {stats['active_minutes'] * 60}",
        f'  dialog_start_utc: "{stats["start_utc"]}"',
        f'  dialog_end_utc: "{stats["end_utc"]}"',
        f"  calendar_days: {stats['calendar_days']}",
        f"  attachments_distinct: {len(stats['attachments'])}",
        f"  incidents_total: {len(rows)}",
        f"  incidents_prompt: {sum(1 for row in rows if row['origin'] == 'prompt')}",
        f"  incidents_confirmed: {conf['confirmed']}",
        f"  incidents_plausible: {conf['plausible']}",
        f"  incidents_detected_by_ba: {det['user'] + det['user-later']}",
        f"  incidents_detected_next_turn: {det['user']}",
        f"  incidents_detected_at_fixation: {det['run']}",
        f"  incidents_after_first_ba_remark: {repeats_after_remark(rows)}",
        f"  answers_with_incidents: {len({row['turn'] for row in rows if row['origin'] != 'prompt'})}",
        f"  categories_observed: {len(counts)}",
        "  incidents_by_category:",
    ]
    for code in gd.CATEGORIES:
        lines.append(f"    {code}: {counts.get(code, 0)}")
    lines.append("  incidents_by_section:")
    for key in gd.SECTIONS:
        lines.append(f"    {key!r}: {secs.get(key, 0)}".replace("'", '"'))
    lines.extend([
        f"  golden_sets: {len(sets)}",
        f"  golden_cases: {sum(len(item['cases']) for item in sets)}",
        f"  success_criteria: {len(gd.SUCCESS_CRITERIA)}",
        f"  positive_cases: {len(gd.NEGATIVES)}",
        f"  quotes_checked: {check['checked']}",
        f"  quote_mismatches: {check['missing']}",
        '  eval: "Прогон зафиксирован ради статистики ошибок ИИ при генерации BCREQ-ФТ по '
        'разделам (гибридный режим, без продуктовой принадлежности): вхождения размечены по '
        'категориям, разделам, BABOK / ODA и правилам стандарта BCREQ из диалога, каждая '
        'цитата сверена с экспортом. success_rate не задан — оснований в данных нет."',
        "related_issues:",
        f"  - {ISSUE}",
        "  - https://github.com/G-Ivan-A/mango_ba_prompts/issues/373",
        "  - https://github.com/G-Ivan-A/mango_ba_prompts/issues/345",
        "related_runs:",
        "  - RUN-0064",
        "  - RUN-0073",
        "related_artifacts:",
        "  - standards/runs-contract-standard.md",
        "  - standards/evals-contract-standard.md",
        "  - experiments/issue_309_run_stats.py",
        "  - experiments/issue_377_golden_data.py",
        "  - experiments/issue_377_verify_quotes.py",
        "  - experiments/issue_377_golden_set.py",
    ])
    return "\n".join(lines) + "\n"


def render(stats: dict, check: dict) -> dict[str, str]:
    """Все порождаемые файлы: относительный путь в записи → текст."""
    rows = enrich(stats)
    sets = select_cases(rows)
    return {
        "metadata.yaml": metadata(rows, stats, sets, check),
        "outputs/README.md": outputs_readme(rows, stats, sets),
        "outputs/incident-register.md": incident_register(rows),
        "outputs/error-statistics.md": error_statistics(rows, stats),
        "outputs/how-not-to-do.md": how_not_to_do(rows),
        "outputs/golden-set-candidates.md": golden_candidates(sets),
        "outputs/golden-set-candidates.json": golden_json(sets),
        "outputs/rubric-candidates.md": rubric(rows),
        "outputs/success-criteria.md": success_criteria(rows),
        "outputs/prompt-improvements.md": prompt_improvements(rows),
        "outputs/prompt-usage.md": prompt_usage(stats),
        "logs/metrics.md": metrics(stats),
        "logs/quote-verification.md": quote_verification(check),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stats", type=Path, default=DATA / "stats.json")
    parser.add_argument("--quote-check", type=Path, default=DATA / "quote-check.json")
    parser.add_argument("--run-dir", type=Path, default=RUN)
    args = parser.parse_args()
    stats = json.loads(args.stats.read_text(encoding="utf-8"))
    check = json.loads(args.quote_check.read_text(encoding="utf-8"))
    for rel, text in render(stats, check).items():
        path = args.run_dir / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        print(f"written: {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
