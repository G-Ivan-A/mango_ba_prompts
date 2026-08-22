#!/usr/bin/env python3
"""Метрики прогона 765 (issue #276) по эпизодам из выгрузки чата.

Зачем отдельный скрипт: `scripts/chat_export_to_markdown.py` даёт пореплико́вую
таблицу, а для вердиктов по эпизодам нужна агрегация «пара реплик → эпизод»,
активное время (без ночных пауз) и время генерации ответа.

Источник чисел — сам экспорт: `content_list[*].usage` (провайдерский подсчёт
токенов) и `timestamp` реплики/части ответа. Оценок здесь нет.

    python3 experiments/parse_765_chat_export.py <export.json>
"""
from __future__ import annotations

import argparse
import datetime as dt
import json

# Эпизод = смысловой шаг диалога; границы размечены вручную по транскрипту
# (индексы реплик включительно). См. runs/2026/RUN-0022/outputs/README.md.
EPISODES = [
    (1, 0, 1, "Инициализация промпта, Шаг 1"),
    (2, 2, 3, "Подача глоссария и черновика ФТ"),
    (3, 4, 5, "Гибридная стратегия, Шаг 2 (отчёт аудитора)"),
    (4, 6, 7, "Решения БА по отчёту, перегенерация v1.1"),
    (5, 8, 9, "Правка FR-02, новые FR-03 и FR-09, v1.2"),
    (6, 10, 11, "Пересортировка FR"),
    (7, 12, 13, "«Предоставлять возможность» vs «обеспечивать»"),
    (8, 14, 15, "Аудит версии БА на однозначность, v1.3"),
    (9, 16, 17, "Авторизация как отдельный FR-01, раздел 3.1 v1.4"),
    (10, 18, 19, "Термин «Сессия», микротюнинг FR-05"),
    (11, 20, 21, "Рендер раздела 4 v1.4"),
    (12, 22, 23, "Сверка с «Версией 2025»"),
    (13, 24, 25, "Формулировка п. 4.5.7"),
]

# Пауза между репликами больше порога считается перерывом в работе, а не
# активным временем БА.
ACTIVE_GAP_LIMIT_S = 1800


def chain(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    history = data[0]["chat"]["history"]
    messages = history["messages"]
    node = data[0].get("currentId") or history.get("currentId")
    out: list[dict] = []
    while node:
        message = messages[node]
        out.append(message)
        node = message.get("parentId")
    out.reverse()
    return out


def usage(message: dict) -> dict:
    for part in reversed(message.get("content_list") or []):
        if part.get("usage"):
            return part["usage"]
    return {}


def generation_s(message: dict) -> int:
    """Время от постановки реплики до последней части ответа."""
    parts = [p.get("timestamp") for p in (message.get("content_list") or []) if p.get("timestamp")]
    if not parts or not message.get("timestamp"):
        return 0
    return max(parts) - message["timestamp"]


def utc(ts: int) -> str:
    return dt.datetime.fromtimestamp(ts, dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("export")
    args = parser.parse_args()
    turns = chain(args.export)

    print("| Эпизод | Реплики | Тема | out_tokens | reasoning | context_in | generation_s |")
    print("| --- | --- | --- | --- | --- | --- | --- |")
    totals = {"out": 0, "reason": 0, "gen": 0, "chars": 0}
    for number, start, end, title in EPISODES:
        out = reason = gen = 0
        context_in = 0
        for turn in turns[start : end + 1]:
            use = usage(turn)
            out += use.get("output_tokens", 0)
            reason += (use.get("output_tokens_details") or {}).get("reasoning_tokens", 0)
            context_in = max(context_in, use.get("input_tokens", 0))
            gen += generation_s(turn)
            totals["chars"] += len(turn.get("content") or "")
        totals["out"] += out
        totals["reason"] += reason
        totals["gen"] += gen
        print(f"| E{number} | {start}–{end} | {title} | {out} | {reason} | {context_in} | {gen} |")

    stamps = [t["timestamp"] for t in turns if t.get("timestamp")]
    gaps = [b - a for a, b in zip(stamps, stamps[1:])]
    active = sum(g for g in gaps if g <= ACTIVE_GAP_LIMIT_S)
    print()
    print(f"- turns: {len(turns)}")
    print(f"- output_tokens: {totals['out']}")
    print(f"- reasoning_tokens (входят в output): {totals['reason']}")
    print(f"- context_in_max: {max(usage(t).get('input_tokens', 0) for t in turns)}")
    print(f"- context_in_sum (переподача контекста): {sum(usage(t).get('input_tokens', 0) for t in turns)}")
    print(f"- generation_s: {totals['gen']}")
    print(f"- duration_wall_clock_s: {stamps[-1] - stamps[0]}")
    print(f"- duration_active_s (паузы > {ACTIVE_GAP_LIMIT_S} c исключены): {active}")
    print(f"- window_utc: {utc(stamps[0])} — {utc(stamps[-1])}")


if __name__ == "__main__":
    main()
