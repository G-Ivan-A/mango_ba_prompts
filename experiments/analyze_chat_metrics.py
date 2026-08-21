#!/usr/bin/env python3
"""Метрики прогона RUN-0013 по экспорту истории чата (issue #268).

Вход — JSON-экспорт чата, приложенный к issue #268:
https://github.com/user-attachments/files/31297233/1059_2-chat-export-1787300919840.json

Запуск:
    python3 experiments/analyze_chat_metrics.py /path/to/1059_2-chat-export.json

Скрипт восстанавливает активную ветку диалога (обход от history.currentId
вверх по parentId) и считает метрики, зафиксированные в
runs/2026/RUN-0013/metadata.yaml и logs/experiment-log.md.
"""

from __future__ import annotations

import collections
import datetime
import json
import re
import sys

# Маркеры явной правки/критики в реплике БА — основа оценки success_rate.
CORRECTION = re.compile(
    r"критичн|критикал|критичсек|критическ|ошибк|не принято|плохо|стоп,|"
    r"запрещен|тупит|тупые|переделать|нарушен|неверно|некорректн",
    re.IGNORECASE,
)


def active_chain(chat: dict) -> list[dict]:
    """Активная ветка диалога: от currentId вверх по parentId, в прямом порядке."""
    messages = chat["history"]["messages"]
    chain, node = [], chat["history"].get("currentId")
    while node:
        message = messages[node]
        chain.append(message)
        node = message.get("parentId")
    chain.reverse()
    return chain


def main(path: str) -> int:
    export = json.load(open(path, encoding="utf-8"))[0]
    chat = export["chat"]
    chain = active_chain(chat)

    users = [m for m in chain if m["role"] == "user"]
    assistants = [m for m in chain if m["role"] == "assistant"]

    models = collections.Counter()
    phases = collections.Counter()
    tokens_in = tokens_out = 0
    for message in assistants:
        if message.get("model"):
            models[message["model"]] += 1
        for entry in message.get("content_list") or []:
            phases[entry.get("phase")] += 1
            usage = entry.get("usage") or {}
            tokens_in += usage.get("input_tokens", 0)
            tokens_out += usage.get("output_tokens", 0)

    days = collections.Counter(
        datetime.datetime.fromtimestamp(
            m.get("timestamp", 0), datetime.timezone.utc
        ).strftime("%Y-%m-%d")
        for m in chain
    )
    corrections = sum(1 for m in users if CORRECTION.search(m.get("content") or ""))

    print(f"chat title:            {export.get('title')}")
    print(f"messages total:        {len(chat['history']['messages'])}")
    print(f"messages active chain: {len(chain)} ({len(users)} user / {len(assistants)} assistant)")
    print(f"models:                {dict(models)}")
    print(f"tool phases:           {dict(phases)}")
    print(f"tokens:                in {tokens_in} / out {tokens_out}")
    print(f"period:                {min(days)} .. {max(days)} ({len(days)} active days)")
    print(f"turns per day:         {dict(sorted(days.items()))}")
    print(
        f"success_rate estimate: {(len(users) - corrections) / len(users):.2f} "
        f"({len(users) - corrections}/{len(users)} без явной правки/критики)"
    )
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        raise SystemExit(2)
    raise SystemExit(main(sys.argv[1]))
