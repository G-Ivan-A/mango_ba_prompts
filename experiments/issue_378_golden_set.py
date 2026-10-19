#!/usr/bin/env python3
"""Порождение записи RUN-0074 (issue #378): статистика задачи 1104 и золотой набор ошибок ИИ.

Скрипт детерминированно строит из трёх входов:

- ``experiments/issue_378/stats.json`` — вывод
  :mod:`experiments.issue_309_run_stats` по экспорту чата задачи 1104;
- ``experiments/issue_378/quote-check.json`` — вывод
  :mod:`experiments.issue_378_verify_quotes` (сверка цитат с экспортом);
- :mod:`experiments.issue_378_golden_data` — разметка вхождений дефектов,
  позитивных кейсов и критериев успеха.

Порождаются все файлы записи, содержащие числа или цитаты, — их нельзя писать
руками без риска расхождения с разметкой:

- ``metadata.yaml``;
- ``outputs/README.md``, ``outputs/incident-register.md``,
  ``outputs/error-statistics.md``, ``outputs/how-not-to-do-by-product.md``,
  ``outputs/golden-set-candidates.md``, ``outputs/golden-set-candidates.json``,
  ``outputs/rubric-candidates.md``, ``outputs/success-criteria.md``,
  ``outputs/runtime-improvements.md``, ``outputs/prompt-usage.md``;
- ``logs/metrics.md``, ``logs/quote-verification.md``, ``logs/kb-verification.md``.

Провенанс, журнал и ограничения чтения (``inputs/README.md``,
``logs/experiment-log.md``, ``feedback/review-notes.md``) пишутся руками и этим
скриптом не трогаются.

Запуск: ``python3 experiments/issue_378_golden_set.py``
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments"))

import issue_378_golden_data as gd  # noqa: E402

DATA = ROOT / "experiments" / "issue_378"
RUN = ROOT / "runs" / "2026" / "RUN-0074"
RUN_ID = "RUN-0074"
ISSUE = "https://github.com/G-Ivan-A/mango_ba_prompts/issues/378"
ATTACHMENT = "https://github.com/user-attachments/files/33669481/chat-export-1104.json"
RUNTIME_SHA = "91406e430aeb70dabf20548eee0ea95127f42690"
RUNTIME = f"https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/{RUNTIME_SHA}"
UPDATED = "2026-10-19"
GENERATOR = "[`experiments/issue_378_golden_set.py`](../../../../experiments/issue_378_golden_set.py)"
DATA_MODULE = "[`experiments/issue_378_golden_data.py`](../../../../experiments/issue_378_golden_data.py)"

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
    ("ASIS", "Шаг 0: анализ текущего функционала (As-Is) по документации", {"asis", "open"}),
    ("PRB", "Разделы 1–3: глоссарий, проблема, цель, задачи, состав работ", {"1", "2", "3"}),
    ("FR", "Раздел 4: функциональные требования (только доработка)", {"4"}),
    ("LIM", "Раздел 6: ограничения", {"6"}),
    ("DLG", "Ход диалога: статусы, самопроверка, сравнение вариантов", {"dialog"}),
    ("PRM", "Шаблон-промпт генерации раздела", {"prompt"}),
]
MAX_DEFECT_CASES = 8
MIN_CASES = 5
MAX_NEGATIVE_CASES = 2

#: Профиль продукта runtime по продукту задачи (``taxonomy/products.yaml``).
PRODUCT_PROFILE = {
    "vpbx": "P-SETTINGS",
    "cc": "P-SETTINGS",
    "vpbx-api": "P-API",
    "cross": None,
}

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
        row["model"] = turn["model"]
        row["utc"] = turn["utc"]
        row["session"] = session_of(stats, turn["utc"])
        row["section_title"], row["slot"] = gd.SECTIONS[row["sec"]]
        row["babok"] = row.get("babok") or cat["babok"]
        row["oda"] = row.get("oda") or cat["oda"]
        row["primary"] = "BABOK" if row["sec"] in gd.BABOK_SECTIONS else "ODA"
        row["sec345"] = row.get("sec345") or sec345(row)
        row["rule"] = cat["rule"]
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
            "prod": row["prod"], "counter": [row["counter"]], "input": row["quote"],
            "why": row["behaviour"], "uq_turn": row["uq_turn"], "uq": row["uq"],
            "confirmed_by": "user" if row["uq"] else "none",
        })
    for row in gd.SUCCESS_CRITERIA:
        if not row.get("golden"):
            continue
        pool.append({
            "ref": row["id"], "set": row["golden"], "turn": row["turn"], "sec": row["sec"],
            "prod": row["prod"], "counter": row["counters"], "input": row["uq"],
            "why": f"текст БА (реплика {row['turn']}): {row['criterion']}",
            "uq_turn": row["turn"], "uq": row["uq"], "confirmed_by": "user",
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
            cases.append({"case_id": f"GS-378-{code}-{index:02d}", "kind": "negative",
                          "incident": row})
        for offset, row in enumerate(negatives, len(chosen) + 1):
            cases.append({"case_id": f"GS-378-{code}-{offset:02d}", "kind": "positive",
                          "clean": row})
        result.append({"code": code, "title": title, "sections": sorted(sections),
                       "cases": cases, "occurrences": len(members), "counts": counts})
    return result


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


# ---------------------------------------------------------------------------
# Рендер
# ---------------------------------------------------------------------------


def incident_register(rows: list[dict]) -> str:
    out = [
        front_matter("artifact", "mango-only", [
            "related_artifacts:",
            '  - "experiments/issue_378_golden_data.py"',
            '  - "experiments/issue_378_verify_quotes.py"',
        ]),
        f"# Реестр вхождений ошибок ИИ — {RUN_ID}, задача 1104\n\n",
        generated_banner(),
        "Единица учёта — **вхождение**: повтор той же ошибки в новой реплике модели — "
        f"отдельная строка. Всего вхождений: **{len(rows)}**. Сводные распределения — в "
        "[`error-statistics.md`](error-statistics.md).\n\n",
        "## Легенда колонок\n\n",
        "- **Р.** — номер реплики в линейной ветке экспорта (0 — промпт БА; нечётные — ответы модели).\n",
        "- **Сессия** — рабочая сессия (разрыв > 30 мин), см. [`prompt-usage.md`](prompt-usage.md#сессии).\n",
        "- **Раздел → слот** — раздел шаблона ФТ из реплик 0 и 66 и слот скелета "
        f"[mango-ba-ai-runtime]({RUNTIME}/AGENTS.md).\n",
        "- **Кат.** — категория из закрытого словаря (раздел «Категории» ниже).\n",
        "- **Происх.** — " + "; ".join(f"`{k}` — {v}" for k, v in gd.ORIGINS.items()) + ".\n",
        "- **Обнаружение** — `БА, р. N`: БА указал на дефект в реплике N; «при фиксации» — "
        "найдено при сверке с КБ, черновиком и правилами, БА дефект не отметил.\n",
        "- **Задержка** — реплик БА / минут от дефекта до реакции БА.\n",
        "- **Дост.** — " + "; ".join(f"`{k}` — {v}" for k, v in gd.CONFIDENCE.items()) + ".\n",
        "- **Осн.** — основная привязка: BABOK (ФТ — As-Is, разделы 1–3 и 6, вопросы, диалог) "
        "или ODA (функциональный дизайн — раздел 4).\n",
        "- **#345** — вторичная категория классификации "
        "[RUN-0064](../../RUN-0064/reports/error-analysis.md).\n\n",
        "## Категории\n\n",
        "| Код | Категория | BABOK v3 | ODA | Правило runtime |\n| --- | --- | --- | --- | --- |\n",
    ]
    for code, cat in gd.CATEGORIES.items():
        out.append(f"| {code} | {cat['title']} | {babok_ref(cat['babok'])} | "
                   f"{cat['oda']} | {cat['rule']} |\n")
    out.append("\n## Реестр\n\n")
    out.append("| ID | Р. | Модель | Сессия | Раздел → слот | Продукт | Кат. | Происх. | "
               "Обнаружение | Задержка | Дост. | Осн. | BABOK | ODA | #345 | Цитата модели "
               "| Цитата БА / основание |\n")
    out.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- "
               "| --- | --- | --- | --- |\n")
    for row in rows:
        basis = []
        if row["uq"]:
            basis.append(quote(row["uq"]))
        if row["evidence"]:
            basis.append(f"КБ: {cell(row['evidence'])}")
        if row["note"]:
            basis.append(cell(row["note"]))
        out.append(
            f"| {row['id']} | {row['turn']} | {row['model']} | {row['session']} | "
            f"{row['sec']} → {row['slot']} | {row['prod']} | {row['cat']} | {row['origin']} | "
            f"{det_label(row)} | {lag_label(row)} | {row['conf']} | {row['primary']} | "
            f"{babok_ref(row['babok'])} | {row['oda']} | {row['sec345']} | {quote(row['quote'])} | "
            f"{'; '.join(basis) or '—'} |\n"
        )
    return "".join(out)


def crosstab(rows: list[dict], key: str, keys: list[str], titles: dict | None = None) -> list[str]:
    cats = [code for code in gd.CATEGORIES if any(row["cat"] == code for row in rows)]
    out = ["| " + ("Значение" if titles is None else "Значение") + " | Всего | "
           + " | ".join(cats) + " |\n",
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


def first_user_detection(rows: list[dict]) -> dict[str, int]:
    first: dict[str, int] = {}
    for row in rows:
        if row["det_turn"] is not None:
            first[row["cat"]] = min(first.get(row["cat"], 10**6), row["det_turn"])
    return first


def error_statistics(rows: list[dict], stats: dict) -> str:
    total = len(rows)
    answers = answer_turns(stats)
    model_rows = [row for row in rows if row["turn"] > 0]
    by_turn = Counter(row["turn"] for row in model_rows)
    first = first_user_detection(rows)
    out = [
        front_matter("artifact", "mango-only", [
            "related_artifacts:",
            '  - "runs/2026/RUN-0074/outputs/incident-register.md"',
        ]),
        f"# Статистика ошибок ИИ — {RUN_ID}, задача 1104\n\n",
        generated_banner(),
        "Счёт ведётся по вхождениям из [`incident-register.md`](incident-register.md) без "
        "схлопывания повторов (требование issue #378: «Запрещено суммаризировать или "
        "упрощать, важна статистики»).\n\n",
        "## 1. Сводка\n\n",
        "| Показатель | Значение |\n| --- | --- |\n",
        f"| Вхождений всего | {total} |\n",
        f"| В тексте промпта (реплики 0 и 66) | {total - len(model_rows)} |\n",
        f"| В ответах модели | {len(model_rows)} |\n",
        f"| Ответов модели | {len(answers)} |\n",
        f"| Ответов с ≥ 1 вхождением | {len(by_turn)} ({pct(len(by_turn), len(answers))}) |\n",
        f"| Вхождений на ответ модели (среднее) | {len(model_rows) / len(answers):.2f} |\n",
        f"| Максимум вхождений в одном ответе | {max(by_turn.values())} (реплика "
        f"{min(t for t, c in by_turn.items() if c == max(by_turn.values()))}) |\n",
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
    repeats = sum(1 for row in rows if row["cat"] in first and row["turn"] > first[row["cat"]])
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

    out.append("\n## 3. Продукт × категория\n\n")
    out.append("Продуктовая принадлежность — по словарю продуктов задачи; соответствие "
               "классам `taxonomy/products.yaml` runtime — в "
               "[`how-not-to-do-by-product.md`](how-not-to-do-by-product.md).\n\n")
    out.extend(crosstab(rows, "prod", list(gd.PRODUCTS),
                        {k: f"{v['title']} (`{k}`)" for k, v in gd.PRODUCTS.items()}))

    out.append("\n## 4. Раздел шаблона → слот runtime × категория\n\n")
    out.extend(crosstab(rows, "sec", list(gd.SECTIONS),
                        {k: f"{v[0]} → {v[1]}" for k, v in gd.SECTIONS.items()}))

    out.append("\n## 5. Модель × категория\n\n")
    models = ["—"] + list(stats["models"])
    out.extend(crosstab(rows, "model", models,
                        {"—": "промпт БА (реплики 0 и 66)", **{m: m for m in stats["models"]}}))
    out.append("\n| Модель | Ответов | Вхождений | На ответ |\n| --- | --- | --- | --- |\n")
    for model in stats["models"]:
        count = sum(1 for row in answers if row["model"] == model)
        hits = sum(1 for row in rows if row["model"] == model)
        out.append(f"| {model} | {count} | {hits} | {hits / count:.2f} |\n")

    out.append("\n## 6. Сессии\n\n")
    out.append("| Сессия | Ответов модели | Вхождений | На ответ | Категории (вхождений) |\n"
               "| --- | --- | --- | --- | --- |\n")
    for index in range(1, len(stats["session_rows"]) + 1):
        in_session = [row for row in answers if session_of(stats, row["utc"]) == index]
        hits = [row for row in rows if row["session"] == index]
        cats = Counter(row["cat"] for row in hits)
        listing = ", ".join(f"{cat} ×{n}" for cat, n in sorted(cats.items())) or "—"
        per = f"{len(hits) / len(in_session):.2f}" if in_session else "—"
        out.append(f"| {index} | {len(in_session)} | {len(hits)} | {per} | {listing} |\n")

    out.append("\n## 7. Каждый ответ модели\n\n")
    out.append("Перечислены все ответы, включая ответы без вхождений.\n\n")
    out.append("| Р. | Модель | UTC | out_tokens | Вхождений | Категории | ID |\n"
               "| --- | --- | --- | --- | --- | --- | --- |\n")
    for answer in answers:
        hits = [row for row in rows if row["turn"] == answer["index"]]
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

    out.append("\n## 11. Правила mango-ba-ai-runtime\n\n")
    out.append(f"Правила — [`AGENTS.md`]({RUNTIME}/AGENTS.md) runtime на SHA `{RUNTIME_SHA[:7]}`. "
               "«Пробел» — дефект не закрывается текущими правилами; предложения — в "
               "[`runtime-improvements.md`](runtime-improvements.md).\n\n")
    out.append("| Правило | Категории | Вхождений | Есть пробел |\n| --- | --- | --- | --- |\n")
    by_rule: dict[str, list[str]] = {}
    for code, cat in gd.CATEGORIES.items():
        by_rule.setdefault(cat["rule"], []).append(code)
    for rule, codes in by_rule.items():
        count = sum(1 for row in rows if row["cat"] in codes)
        gaps = [code for code in codes if gd.CATEGORIES[code]["gap"]]
        out.append(f"| {rule} | {', '.join(codes)} | {count} | {', '.join(gaps) or 'нет'} |\n")

    out.append("\n## 12. Задержка обнаружения БА\n\n")
    caught = [row for row in rows if row["lag_turns"] is not None]
    out.append("| Задержка | Вхождений | Доля от пойманных БА |\n| --- | --- | --- |\n")
    for title, low, high in LAG_BUCKETS:
        count = sum(1 for row in caught if low <= row["lag_turns"] <= high)
        out.append(f"| {title} | {count} | {pct(count, len(caught))} |\n")
    out.append(f"\nМедиана: {median_of(sorted(r['lag_turns'] for r in caught))} реплик БА, "
               f"{median_of(sorted(r['lag_min'] for r in caught))} мин; максимум: "
               f"{max(r['lag_turns'] for r in caught)} реплик БА.\n")
    return "".join(out)


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


def how_not_to_do(rows: list[dict]) -> str:
    out = [
        front_matter("artifact", "prompts", [
            "related_artifacts:",
            '  - "runs/2026/RUN-0074/outputs/incident-register.md"',
            f'  - "{RUNTIME}/taxonomy/products.yaml"',
        ]),
        f"# Как не надо делать — по продуктам ({RUN_ID}, задача 1104)\n\n",
        generated_banner(),
        "Список — вход для промптов, правил и навыков генерации BCREQ-ФТ по разделам. "
        "Для каждого продукта перечислены категории в порядке частоты; под каждой — "
        "**все** вхождения (без схлопывания), чтобы правило можно было проверить на "
        "реальных формулировках.\n\n",
        "## Продукты задачи и словарь runtime\n\n",
        "| Ключ | Продукт | Класс / профиль `taxonomy/products.yaml` | Вхождений |\n"
        "| --- | --- | --- | --- |\n",
    ]
    for key, product in gd.PRODUCTS.items():
        count = sum(1 for row in rows if row["prod"] == key)
        out.append(f"| `{key}` | {product['title']} | {product['runtime']} | {count} |\n")
    for key, product in gd.PRODUCTS.items():
        subset = [row for row in rows if row["prod"] == key]
        if not subset:
            continue
        out.append(f"\n## {product['title']} (`{key}`) — {len(subset)} вхождений\n")
        counts = Counter(row["cat"] for row in subset)
        for code in sorted(counts, key=lambda c: (-counts[c], c)):
            cat = gd.CATEGORIES[code]
            items = [row for row in subset if row["cat"] == code]
            out.append(f"\n### {code}. {cat['title']} — {len(items)}\n\n")
            out.append(f"- **Не надо:** {cat['antipattern']}.\n")
            out.append(f"- **Надо:** {cat['guard']}.\n")
            out.append(f"- **BABOK:** {babok_ref(cat['babok'])}; **ODA:** {cat['oda']}; "
                       f"**правило runtime:** {cat['rule']}.\n\n")
            out.append("| ID | Р. | Раздел → слот | Цитата | Обнаружение |\n"
                       "| --- | --- | --- | --- | --- |\n")
            for row in items:
                out.append(f"| {row['id']} | {row['turn']} | {row['sec']} → {row['slot']} | "
                           f"{quote(row['quote'])} | {det_label(row)} |\n")
    return "".join(out)


def golden_candidates(sets: list[dict]) -> str:
    out = [
        front_matter("artifact", "prompts", [
            "related_artifacts:",
            '  - "standards/evals-contract-standard.md"',
            '  - "runs/2026/RUN-0074/outputs/rubric-candidates.md"',
            '  - "runs/2026/RUN-0074/outputs/golden-set-candidates.json"',
        ]),
        f"# Кандидаты в золотые наборы генерации BCREQ-ФТ — {RUN_ID}\n\n",
        generated_banner(),
        "## Назначение\n\n",
        "Кандидаты в golden-set по "
        "[`standards/evals-contract-standard.md`](../../../../standards/evals-contract-standard.md): "
        "наборы по **5–10 кейсов**, по одному набору на группу разделов шаблона, — под "
        "посекционную генерацию BCREQ-ФТ. Вход каждого кейса — реальная формулировка "
        "модели или БА из экспорта задачи 1104 (дословно, сверено). Эталонный вердикт "
        "агента-проверяющего: для дефектного кейса — «дефект» с указанным классом, для "
        "негативного кейса — «дефекта нет».\n\n",
        "Это **запись прогона**, а не контракт: стандарт запрещает смешивать эталон и "
        "факт, а контейнер golden-set в этом споке не выбран (см. "
        "[`../feedback/review-notes.md`](../feedback/review-notes.md)). Перенос в "
        "контейнер golden-set — после решения человека и ревью эталона (`draft → reviewed`).\n\n",
        "Правило отбора (детерминированное): в наборе категории упорядочены по числу "
        f"вхождений; для каждой из первых {MAX_DEFECT_CASES} берётся первое подтверждённое "
        "вхождение (если подтверждённых нет — первое вероятное); если категорий меньше "
        f"{MIN_CASES}, добираются следующие вхождения тех же категорий. Негативных кейсов — "
        f"до {MAX_NEGATIVE_CASES}, сначала подтверждённые БА.\n\n",
        "Набор **не покрывает**: смысловую полноту ФТ относительно бизнес-цели, "
        "проверку по продуктам вне задачи 1104, многопродуктовые правила MP-1…MP-4.\n\n",
    ]
    for item in sets:
        out.append(f"## Набор GS-378-{item['code']} — {item['title']}\n\n")
        sections = ", ".join(f"{s} → {gd.SECTIONS[s][1]}" for s in item["sections"])
        out.append(f"Разделы → слоты: {sections}. Вхождений в группе: {item['occurrences']}. "
                   f"Кейсов: {len(item['cases'])}.\n\n")
        out.append("### Кейсы\n\n")
        out.append("| case-id | Вход | Эталонный вердикт | Класс дефекта | Обоснование эталона | "
                   "Контекст | Источник |\n| --- | --- | --- | --- | --- | --- | --- |\n")
        for case in item["cases"]:
            if case["kind"] == "negative":
                row = case["incident"]
                cat = gd.CATEGORIES[row["cat"]]
                reason = [f"реплика {row['turn']}"]
                if row["uq"]:
                    reason.append(f"БА, р. {row['det_turn']}: {quote(row['uq'])}")
                if row["evidence"]:
                    reason.append(f"КБ: {cell(row['evidence'])}")
                if row["note"]:
                    reason.append(cell(row["note"]))
                out.append(
                    f"| {case['case_id']} | {quote(row['quote'])} | дефект | {row['cat']} — "
                    f"{cat['title']} | {'; '.join(reason)} | продукт `{row['prod']}`; раздел "
                    f"{row['sec']} → {row['slot']}; BABOK {babok_ref(row['babok'])}; ODA "
                    f"{row['oda']} | {row['id']}, {row['model']}, {row['conf']} |\n"
                )
            else:
                row = case["clean"]
                reason = [cell(row["why"])]
                if row["uq"] and row["ref"].startswith("N-"):
                    reason.append(f"БА, р. {row['uq_turn']}: {quote(row['uq'])}")
                out.append(
                    f"| {case['case_id']} | {quote(row['input'])} | дефекта нет | — (против "
                    f"{', '.join(row['counter'])}) | {'; '.join(reason)} | продукт "
                    f"`{row['prod']}`; раздел {row['sec']} → {gd.SECTIONS[row['sec']][1]} | "
                    f"{row['ref']}, реплика {row['turn']}, confirmed_by: {row['confirmed_by']} |\n"
                )
        covered = sorted({c["incident"]["cat"] for c in item["cases"] if c["kind"] == "negative"})
        missed = sorted(set(item["counts"]) - set(covered))
        out.append("\n### Покрытие\n\n")
        out.append(f"- Покрыты категории: {', '.join(covered)}.\n")
        out.append("- Есть в группе, но вне набора (лимит "
                   f"{MAX_DEFECT_CASES} категорий): {', '.join(missed) or 'нет'}.\n")
        out.append("- Сознательно не покрыты: категории без вхождений в этой группе.\n\n")
    out.append("## Related Artifacts\n\n")
    out.append("- Рубрика: [`rubric-candidates.md`](rubric-candidates.md).\n")
    out.append("- Машиночитаемая форма (структура `golden/cases.yaml` runtime): "
               "[`golden-set-candidates.json`](golden-set-candidates.json).\n")
    out.append("- Реестр вхождений: [`incident-register.md`](incident-register.md).\n")
    out.append(f"- Скелет и правила: [`AGENTS.md`]({RUNTIME}/AGENTS.md), "
               f"[`golden/cases.yaml`]({RUNTIME}/golden/cases.yaml).\n")
    return "".join(out)


def golden_json(sets: list[dict]) -> str:
    payload = {
        "golden_set": "run-0074-bcreq-fr-sections",
        "version": "0.1",
        "status": "draft",
        "source": ISSUE,
        "runtime_compat": f"golden/cases.yaml @ {RUNTIME_SHA}",
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
                    "product": row["prod"],
                    "product_profile": PRODUCT_PROFILE[row["prod"]],
                    "section": row["sec"],
                    "slot": row["slot"],
                    "input": row["quote"],
                    "source": {"incident": row["id"], "turn": row["turn"], "model": row["model"]},
                    "babok": row["babok"],
                    "oda": row["oda"],
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
                    "product": row["prod"],
                    "product_profile": PRODUCT_PROFILE[row["prod"]],
                    "section": row["sec"],
                    "slot": gd.SECTIONS[row["sec"]][1],
                    "input": row["input"],
                    "source": {"ref": row["ref"], "turn": row["turn"]},
                    "expect": {"outcome": "completed", "no_defect_of": row["counter"]},
                })
        payload["sets"].append({"id": f"GS-378-{item['code']}", "title": item["title"],
                                "sections": item["sections"], "cases": cases})
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def rubric(rows: list[dict]) -> str:
    out = [
        front_matter("artifact", "prompts", [
            "related_artifacts:",
            '  - "standards/evals-contract-standard.md"',
            '  - "runs/2026/RUN-0074/outputs/golden-set-candidates.md"',
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
        "| Код | Критерий | Наблюдаемый признак | Провал = | Вхождений в прогоне | Правило runtime |\n"
        "| --- | --- | --- | --- | --- | --- |\n",
    ]
    counts = Counter(row["cat"] for row in rows)
    for code, cat in gd.CATEGORIES.items():
        if not counts[code]:
            continue
        out.append(f"| R-{code} | {cat['title']} отсутствует | {cat['guard']} | "
                   f"{cat['antipattern']} | {counts[code]} | {cat['rule']} |\n")
    return "".join(out)


def success_criteria(rows: list[dict]) -> str:
    out = [
        front_matter("artifact", "prompts", [
            "related_artifacts:",
            '  - "runs/2026/RUN-0074/outputs/golden-set-candidates.md"',
        ]),
        f"# Золотой набор критериев успеха — {RUN_ID}, задача 1104\n\n",
        generated_banner(),
        "Критерий успеха — правило, которое БА сформулировал в диалоге, или текст, который "
        "БА принял в своей редакции (реплика 116). У каждого критерия — дословная цитата БА, "
        "привязка к продукту, разделу → слоту, BABOK / ODA и категории дефектов, которые он "
        "предотвращает, с числом вхождений этих категорий в прогоне.\n\n",
        "## 1. Критерии успеха\n\n",
        "| ID | Р. | Продукт | Раздел → слот | Критерий | Цитата БА | Против категорий "
        "(вхождений) | BABOK | ODA |\n| --- | --- | --- | --- | --- | --- | --- | --- | --- |\n",
    ]
    counts = Counter(row["cat"] for row in rows)
    for row in gd.SUCCESS_CRITERIA:
        title, slot = gd.SECTIONS[row["sec"]]
        against = ", ".join(f"{c} ({counts[c]})" for c in row["counters"])
        babok = sorted({b for c in row["counters"] for b in gd.CATEGORIES[c]["babok"]},
                       key=version_key)
        oda = sorted({gd.CATEGORIES[c]["oda"] for c in row["counters"]})
        out.append(f"| {row['id']} | {row['turn']} | `{row['prod']}` | {row['sec']} → {slot} | "
                   f"{row['criterion']} | {quote(row['uq'])} | {against} | "
                   f"{babok_ref(babok)} | {', '.join(oda)} |\n")
    out.append("\n## 2. Позитивные кейсы поведения модели\n\n")
    out.append("Ответы модели, где дефекта нет и поведение соответствует правилам (часть — "
               "с подтверждением БА). Используются как негативные кейсы золотых наборов.\n\n")
    out.append("| ID | Р. | Набор | Продукт | Раздел → слот | Цитата модели | Поведение | "
               "Против | Подтверждение БА |\n| --- | --- | --- | --- | --- | --- | --- | --- | --- |\n")
    for index, row in enumerate(gd.NEGATIVES, 1):
        slot = gd.SECTIONS[row["sec"]][1]
        confirm = f"р. {row['uq_turn']}: {quote(row['uq'])}" if row["uq"] else "—"
        out.append(f"| N-{index:02d} | {row['turn']} | GS-378-{row['set']} | `{row['prod']}` | "
                   f"{row['sec']} → {slot} | {quote(row['quote'])} | {row['behaviour']} | "
                   f"{row['counter']} | {confirm} |\n")
    return "".join(out)


def runtime_improvements(rows: list[dict]) -> str:
    counts = Counter(row["cat"] for row in rows)
    prod = Counter(row["prod"] for row in rows)
    kb_rows = [row for row in rows if row["cat"] in ("C01", "C10", "C11")]
    out = [
        front_matter("artifact", "prompts", [
            "related_artifacts:",
            f'  - "{RUNTIME}/AGENTS.md"',
            f'  - "{RUNTIME}/taxonomy/products.yaml"',
            f'  - "{RUNTIME}/golden/cases.yaml"',
        ]),
        f"# Предложения для mango-ba-ai-runtime и промптов — {RUN_ID}\n\n",
        generated_banner(),
        "Ненормативно: runtime этим репозиторием не правится (правило 13 "
        f"[`AGENTS.md`]({RUNTIME}/AGENTS.md)). Каждое предложение опирается на число "
        "вхождений из [`error-statistics.md`](error-statistics.md).\n\n",
        "## 1. Пробелы правил AGENTS.md\n\n",
        "| Категория | Вхождений | Действующее правило | Пробел | Предлагаемая формулировка |\n"
        "| --- | --- | --- | --- | --- |\n",
    ]
    for code, cat in gd.CATEGORIES.items():
        if cat["gap"]:
            out.append(f"| {code} {cat['title']} | {counts[code]} | {cat['rule']} | {cat['gap']} | "
                       f"{cat['guard']} |\n")
    out.append("\n## 2. Словарь продуктов `taxonomy/products.yaml`\n\n")
    out.append(
        f"- ВАТС / ЛК ВАТС (`vpbx`, {prod['vpbx']} вхождений) относится к `voice-ucaas`, "
        "который отмечен `in_slice: false`: золотые кейсы карточки Группы и отчётов ЛК сейчас "
        "вне среза runtime. Предложение: включить `voice-ucaas` в срез или завести профиль "
        "настроек ВАТС.\n"
        f"- Контакт-центр (`cc`, {prod['cc']} вхождений) — `contact-center`, в срезе; "
        "большинство выдуманных атрибутов (столбец «Статус автоперезвона», «Заказы ЗОЗ») "
        "перенесены моделью из ЛК ВАТС в КЦ — нужна маршрутизация «один продукт — одно "
        "руководство».\n"
        f"- VPBX API (`vpbx-api`, {prod['vpbx-api']} вхождений) — профиль `P-API`; в задаче "
        "API вне границ, вхождения — домыслы вопреки запрету БА.\n\n"
    )
    out.append("## 3. Золотые кейсы `golden/cases.yaml`\n\n")
    out.append(
        "Сейчас набор runtime синтетический (`origin: synthetic`, `structural_only: true`). "
        "Предложение: принять кейсы "
        "[`golden-set-candidates.json`](golden-set-candidates.json) со значением "
        "`origin: run-observed`, где `confirmed_by: user` — реакция БА в диалоге; "
        "`expect.outcome: refused` с `defect_class` для дефектных кейсов и "
        "`expect.outcome: completed` для негативных.\n\n"
    )
    out.append("## 4. Маршрутизация в КБ для внешних API\n\n")
    out.append(
        f"{len(kb_rows)} вхождений категорий C01/C10/C11 — утверждения о текущем функционале "
        "без дословной опоры на КБ. Предложение: для слота S-ASIS каждое утверждение выводить "
        "парой «цитата + локатор (руководство, пункт, страница)» и сверять цитату с КБ до "
        "вывода (журнал — "
        "[`../logs/kb-verification.md`](../logs/kb-verification.md)).\n\n"
    )
    out.append("## 5. Шаблон-промпт (реплики 0 и 66)\n\n")
    out.append("Каждая строка — дословный фрагмент промпта и его следствие в прогоне.\n\n")
    out.append("| ID | Фрагмент | Следствие | Обнаружение |\n| --- | --- | --- | --- |\n")
    for row in rows:
        if row["origin"] == "prompt":
            out.append(f"| {row['id']} | {quote(row['quote'])} | {cell(row['note'])} | "
                       f"{det_label(row)} |\n")
    return "".join(out)


def prompt_usage(stats: dict) -> str:
    user_turns = stats["user_turns"]
    out = [
        front_matter("artifact", "prompts", [
            "related_artifacts:",
            '  - "experiments/issue_378_golden_set.py"',
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
            '  - "experiments/issue_378_verify_quotes.py"',
        ]),
        f"# Журнал сверки цитат прогона {RUN_ID}\n\n",
        f"> Файл **порождён** скриптом {GENERATOR} из вывода "
        "[`experiments/issue_378_verify_quotes.py`](../../../../experiments/issue_378_verify_quotes.py)"
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


def kb_verification(rows: list[dict]) -> str:
    out = [
        front_matter("log", "mango-only", [
            "related_artifacts:",
            f'  - "{RUNTIME}/docs/kb"',
        ]),
        f"# Журнал сверки с базой знаний — {RUN_ID}\n\n",
        generated_banner(),
        f"База знаний — `docs/kb` mango-ba-ai-runtime на SHA `{RUNTIME_SHA}`. Локатор — "
        "код документа, раздел и файл раздела КБ.\n\n",
        "## Локаторы\n\n",
        "| Локатор | Файл раздела КБ |\n| --- | --- |\n",
    ]
    for key, path in gd.KB.items():
        file_path = path.split(" (")[0]
        out.append(f"| {key} | [`{path}`]({RUNTIME}/{file_path}) |\n")
    out.append("\n## Вхождения, сверенные с КБ\n\n")
    out.append("| ID | Р. | Кат. | Продукт | Цитата модели | Локатор | Что показывает КБ |\n"
               "| --- | --- | --- | --- | --- | --- | --- |\n")
    for row in rows:
        if row["evidence"] and row["evidence"] in gd.KB:
            out.append(f"| {row['id']} | {row['turn']} | {row['cat']} | `{row['prod']}` | "
                       f"{quote(row['quote'])} | {row['evidence']} | {cell(row['note']) or '—'} |\n")
    return "".join(out)


def outputs_readme(rows: list[dict], stats: dict, sets: list[dict]) -> str:
    cases = sum(len(item["cases"]) for item in sets)
    counts = Counter(row["cat"] for row in rows)
    top = ", ".join(f"{cat} ({n})" for cat, n in counts.most_common(5))
    caught = sum(1 for row in rows if row["det"] != "run")
    out = [
        front_matter("index", "mango-only"),
        f"# Результаты прогона {RUN_ID} — задача 1104, золотой набор ошибок ИИ\n\n",
        generated_banner(),
        "Прогон фиксирует диалог генерации BCREQ-ФТ «Ручной режим обработки пропущенных "
        "вызовов (задание ЗОЗ) в карточке Группы операторов ЛК ВАТС» (задача 1104) ради статистики ошибок ИИ. Результат — не артефакт "
        "требований, а размеченный по вхождениям реестр ошибок с привязкой к продуктам, "
        "BABOK / TM Forum ODA и слотам mango-ba-ai-runtime, кандидаты в золотые наборы и "
        "критерии успеха для промптов, правил и навыков посекционной генерации ФТ.\n\n",
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
        f"| Наборов-кандидатов / кейсов | {len(sets)} / {cases} |\n",
        f"| Критериев успеха / позитивных кейсов | {len(gd.SUCCESS_CRITERIA)} / {len(gd.NEGATIVES)} |\n",
        "\n## Состав записи\n\n",
        "| Файл | Что содержит |\n| --- | --- |\n",
        "| [`incident-register.md`](incident-register.md) | реестр всех вхождений с цитатами и привязками |\n",
        "| [`error-statistics.md`](error-statistics.md) | распределения: категории, продукты, разделы, модели, сессии, ответы, BABOK, ODA, правила runtime, задержка |\n",
        "| [`how-not-to-do-by-product.md`](how-not-to-do-by-product.md) | «как не надо делать» по продуктам — все вхождения |\n",
        "| [`golden-set-candidates.md`](golden-set-candidates.md) | кандидаты в золотые наборы по группам разделов (5–10 кейсов) |\n",
        "| [`golden-set-candidates.json`](golden-set-candidates.json) | те же кейсы в структуре `golden/cases.yaml` runtime |\n",
        "| [`rubric-candidates.md`](rubric-candidates.md) | бинарная рубрика: базовые критерии и стражи по категориям |\n",
        "| [`success-criteria.md`](success-criteria.md) | золотой набор критериев успеха и позитивных кейсов |\n",
        "| [`runtime-improvements.md`](runtime-improvements.md) | предложения для runtime и шаблона-промпта |\n",
        "| [`prompt-usage.md`](prompt-usage.md) | распределение операций БА, сессии, вложения |\n",
        "| [`../logs/metrics.md`](../logs/metrics.md) | метрики по каждой реплике |\n",
        "| [`../logs/quote-verification.md`](../logs/quote-verification.md) | сверка каждой цитаты с экспортом |\n",
        "| [`../logs/kb-verification.md`](../logs/kb-verification.md) | сверка утверждений модели с КБ runtime |\n",
        "| [`../logs/experiment-log.md`](../logs/experiment-log.md) | как получена запись |\n",
        "| [`../inputs/README.md`](../inputs/README.md) | провенанс исходного экспорта |\n",
        "| [`../feedback/review-notes.md`](../feedback/review-notes.md) | ограничения чтения и открытые вопросы |\n",
    ]
    return "".join(out)


def metadata(rows: list[dict], stats: dict, sets: list[dict], check: dict) -> str:
    counts = Counter(row["cat"] for row in rows)
    det = Counter(row["det"] for row in rows)
    conf = Counter(row["conf"] for row in rows)
    prod = Counter(row["prod"] for row in rows)
    first = first_user_detection(rows)
    repeats = sum(1 for row in rows if row["cat"] in first and row["turn"] > first[row["cat"]])
    lines = [
        f"run_id: {RUN_ID}",
        "process: task-1104-bcreq-fr-vpbx-missed-calls-callback-error-golden-set",
        'version: "0.1"',
        f"date: {UPDATED}",
        'author: "BA-IH + LLM (фиксация прогона: AI issue solver)"',
        f'model: "{", ".join(stats["models"])}"',
        "status: draft",
        "run_type: statistics",
        "source_paths:",
        f"  - {ISSUE}",
        f"  - {ATTACHMENT}",
        f"  - https://github.com/G-Ivan-A/mango-ba-ai-runtime/tree/{RUNTIME_SHA}",
        "inputs:",
        "  - inputs/README.md",
        "outputs:",
        "  - outputs/README.md",
        "  - outputs/incident-register.md",
        "  - outputs/error-statistics.md",
        "  - outputs/how-not-to-do-by-product.md",
        "  - outputs/golden-set-candidates.md",
        "  - outputs/golden-set-candidates.json",
        "  - outputs/rubric-candidates.md",
        "  - outputs/success-criteria.md",
        "  - outputs/runtime-improvements.md",
        "  - outputs/prompt-usage.md",
        "logs:",
        "  - logs/experiment-log.md",
        "  - logs/metrics.md",
        "  - logs/quote-verification.md",
        "  - logs/kb-verification.md",
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
        f"  incidents_after_first_ba_remark: {repeats}",
        f"  answers_with_incidents: {len({row['turn'] for row in rows if row['turn'] > 0})}",
        f"  categories_observed: {len(counts)}",
        "  incidents_by_category:",
    ]
    for code in gd.CATEGORIES:
        lines.append(f"    {code}: {counts.get(code, 0)}")
    lines.append("  incidents_by_product:")
    for key in gd.PRODUCTS:
        lines.append(f"    {key}: {prod.get(key, 0)}")
    lines.extend([
        f"  golden_sets: {len(sets)}",
        f"  golden_cases: {sum(len(item['cases']) for item in sets)}",
        f"  success_criteria: {len(gd.SUCCESS_CRITERIA)}",
        f"  positive_cases: {len(gd.NEGATIVES)}",
        f"  quotes_checked: {check['checked']}",
        f"  quote_mismatches: {check['missing']}",
        '  eval: "Прогон зафиксирован ради статистики ошибок ИИ при генерации BCREQ-ФТ по '
        'разделам: вхождения размечены по категориям, продуктам, BABOK / ODA и слотам runtime, '
        'каждая цитата сверена с экспортом. Итоговая редакция БА — реплика 116 (без '
        'явной приёмки), success_rate не задан — оснований в данных нет."',
        "related_issues:",
        f"  - {ISSUE}",
        "  - https://github.com/G-Ivan-A/mango_ba_prompts/issues/345",
        "related_runs:",
        "  - RUN-0064",
        "  - RUN-0073",
        "related_artifacts:",
        "  - standards/runs-contract-standard.md",
        "  - standards/evals-contract-standard.md",
        "  - experiments/issue_309_run_stats.py",
        "  - experiments/issue_378_golden_data.py",
        "  - experiments/issue_378_verify_quotes.py",
        "  - experiments/issue_378_golden_set.py",
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
        "outputs/how-not-to-do-by-product.md": how_not_to_do(rows),
        "outputs/golden-set-candidates.md": golden_candidates(sets),
        "outputs/golden-set-candidates.json": golden_json(sets),
        "outputs/rubric-candidates.md": rubric(rows),
        "outputs/success-criteria.md": success_criteria(rows),
        "outputs/runtime-improvements.md": runtime_improvements(rows),
        "outputs/prompt-usage.md": prompt_usage(stats),
        "logs/metrics.md": metrics(stats),
        "logs/quote-verification.md": quote_verification(check),
        "logs/kb-verification.md": kb_verification(rows),
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
