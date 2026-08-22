#!/usr/bin/env python3
"""Метрики прогона 58093 (issue #281) по эпизодам из выгрузки чата.

Зачем отдельный скрипт: `scripts/chat_export_to_markdown.py` даёт пореплико́вую
таблицу, а для вердиктов по эпизодам нужна агрегация «пара реплик → эпизод»,
активное время (без ночных пауз) и время генерации ответа.

Источник чисел — сам экспорт: `content_list[*].usage` (провайдерский подсчёт
токенов) и `timestamp` реплики/части ответа. Оценок здесь нет.

    python3 experiments/parse_58093_chat_export.py <export.json>
"""
from __future__ import annotations

import argparse
import datetime as dt
import json

# Эпизод = смысловой шаг диалога; границы размечены вручную по транскрипту
# (индексы реплик включительно). См. runs/2026/RUN-0029/outputs/README.md.
EPISODES = [
    (1, 0, 1, "Проверка раздела 2 по документации интеграции"),
    (2, 2, 3, "Промпт eTOM/ODA, первый перечень ФТ 4.1–4.6"),
    (3, 4, 5, "Макет: перенос настройки в ЛК, правка 4.1"),
    (4, 6, 7, "Аудит настроек интеграции, ФТ 4.7–4.13"),
    (5, 8, 9, "Сводный перечень 4.1–4.13"),
    (6, 10, 11, "Иерархическая структура 4.x / 4.x.x"),
    (7, 12, 13, "Отказ от описания текущего функционала"),
    (8, 14, 15, "Разбор избыточного требования 4.2.2"),
    (9, 16, 17, "Редакция без 4.2.2"),
    (10, 18, 19, "Термин «полная карточка сделки»"),
    (11, 20, 21, "Четыре вопроса БА, возврат приоритета «ответственный»"),
    (12, 22, 23, "Перенос 4.3.2 в ограничения"),
    (13, 24, 25, "«Создать контакт и сделку» и тип Клиента"),
    (14, 26, 27, "Формулировки через результат применения настроек"),
    (15, 28, 29, "Подтверждение редакции 4.3"),
    (16, 30, 31, "Рендер раздела 4"),
    (17, 32, 33, "Генерация раздела 6 «Ограничения»"),
    (18, 34, 35, "Фиксация раздела 4 в редакции БА"),
    (19, 36, 37, "Остановка задачи и итоговое резюме"),
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
