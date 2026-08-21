#!/usr/bin/env python3
"""Метрики прогона по нативным usage-полям выгрузки чата (OpenWebUI-подобный JSON).

Зачем: в выгрузках чата Qwen провайдер уже сообщает расход токенов
(`content_list[*].usage`), поэтому пересчёт сторонним токенизатором (tiktoken,
как в `parse_qwen_chat_export.py` для RUN-0018) даёт лишь оценку. Здесь берутся
измеренные значения провайдера — `input_tokens`, `output_tokens`,
`output_tokens_details.reasoning_tokens`.

Использован для RUN-0022 (issue #275).

    python3 experiments/chat_export_usage_metrics.py <export.json>

Только stdlib.
"""
from __future__ import annotations

import argparse
import ast
import datetime as dt
import json
from pathlib import Path


def load_branch(path: Path) -> list[dict]:
    """Активная ветка диалога: от корня к currentId."""
    data = json.loads(path.read_text(encoding="utf-8"))
    chat = data[0]
    messages = chat["chat"]["history"]["messages"]
    chain: list[dict] = []
    node = chat.get("currentId") or chat["chat"]["history"].get("currentId")
    seen: set[str] = set()
    while node and node not in seen:
        seen.add(node)
        chain.append(messages[node])
        node = messages[node].get("parentId")
    return list(reversed(chain))


def answer_usage(msg: dict) -> dict:
    """usage последнего блока phase == 'answer' (итоговый расход реплики)."""
    for item in reversed(msg.get("content_list") or []):
        if item.get("phase") == "answer" and item.get("usage"):
            return item["usage"]
    return {}


def end_time(msg: dict) -> float | None:
    extra = msg.get("extra") or {}
    if not isinstance(extra, dict):
        extra = ast.literal_eval(extra)
    return extra.get("endTime")


def utc(value: float | None) -> str:
    if not value:
        return "—"
    return dt.datetime.fromtimestamp(value, dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


def episodes(chain: list[dict]) -> list[tuple[dict, dict]]:
    pairs: list[tuple[dict, dict]] = []
    pending: dict | None = None
    for msg in chain:
        if msg.get("role") == "user":
            pending = msg
        elif msg.get("role") == "assistant" and pending is not None:
            pairs.append((pending, msg))
            pending = None
    return pairs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("export", type=Path)
    args = parser.parse_args()

    chain = load_branch(args.export)
    pairs = episodes(chain)

    print("| Эпизод | Начало (UTC) | Вход, ток. | Выход, ток. | «Мышление», ток. | Латентность, с |")
    print("| --- | --- | ---: | ---: | ---: | ---: |")
    total_in = total_out = total_think = 0
    total_latency = 0.0
    for index, (user, bot) in enumerate(pairs, 1):
        use = answer_usage(bot)
        n_in = use.get("input_tokens", 0)
        n_out = use.get("output_tokens", 0)
        n_think = (use.get("output_tokens_details") or {}).get("reasoning_tokens", 0)
        finished = end_time(bot)
        latency = (finished - bot["timestamp"]) if finished else 0.0
        total_in += n_in
        total_out += n_out
        total_think += n_think
        total_latency += latency
        print(
            f"| {index} | {utc(user.get('timestamp'))} | {n_in} | {n_out} | {n_think} | {latency:.1f} |"
        )
    print(f"| **Итого** | | **{total_in}** | **{total_out}** | **{total_think}** | **{total_latency:.1f}** |")

    wall = (chain[-1].get("timestamp") or 0) - (chain[0].get("timestamp") or 0)
    # активное время: сумма непрерывных сессий, разрыв между эпизодами > 1 часа
    active = 0.0
    session_start = pairs[0][0]["timestamp"]
    previous_end = end_time(pairs[0][1]) or pairs[0][1]["timestamp"]
    for user, bot in pairs[1:]:
        if user["timestamp"] - previous_end > 3600:
            active += previous_end - session_start
            session_start = user["timestamp"]
        previous_end = end_time(bot) or bot["timestamp"]
    active += previous_end - session_start

    print()
    print(f"- episodes: {len(pairs)}")
    print(f"- tokens_input: {total_in}")
    print(f"- tokens_output: {total_out}")
    print(f"- tokens_thinking: {total_think}")
    print(f"- tokens_dialog_total: {total_in + total_out}")
    print(f"- duration_generation_s: {total_latency:.1f}")
    print(f"- duration_active_s: {active:.0f}")
    print(f"- duration_wall_clock_s: {wall} (~{wall / 3600:.1f} ч)")
    print(f"- window: {utc(chain[0].get('timestamp'))} — {utc(end_time(pairs[-1][1]))} UTC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
