#!/usr/bin/env python3
"""Выгрузка артефактов из экспорта истории чата (issue #268, прогон RUN-0013).

Запуск:
    python3 experiments/extract_chat_artifacts.py <chat-export.json> <out-dir>

Создаёт в <out-dir>:
  transcript.md      — полная активная ветка диалога (БА ↔ модель);
  user-messages.md   — только реплики БА с индексом и датой (навигация по эпизодам);
  msg-<N>.md         — отдельное сообщение по индексу активной ветки (см. --only).

Метрики прогона считает соседний скрипт analyze_chat_metrics.py.
"""

from __future__ import annotations

import datetime
import json
import pathlib
import sys


def active_chain(chat: dict) -> list[dict]:
    messages = chat["history"]["messages"]
    chain, node = [], chat["history"].get("currentId")
    while node:
        message = messages[node]
        chain.append(message)
        node = message.get("parentId")
    chain.reverse()
    return chain


def body(message: dict) -> str:
    """Текст сообщения: у БА — content, у модели — content_list[phase == answer]."""
    if message.get("content"):
        return message["content"]
    parts = [
        entry["content"]
        for entry in message.get("content_list") or []
        if entry.get("phase") == "answer" and entry.get("content")
    ]
    return "\n\n".join(parts)


def stamp(message: dict) -> str:
    return datetime.datetime.fromtimestamp(
        message.get("timestamp", 0), datetime.timezone.utc
    ).strftime("%Y-%m-%d %H:%M")


def main(src: str, out: str) -> int:
    chain = active_chain(json.load(open(src, encoding="utf-8"))[0]["chat"])
    out_dir = pathlib.Path(out)
    out_dir.mkdir(parents=True, exist_ok=True)

    transcript = "\n\n".join(
        f"########## {m['role']} [{i}] {stamp(m)}\n\n{body(m)}" for i, m in enumerate(chain)
    )
    (out_dir / "transcript.md").write_text(transcript, encoding="utf-8")

    users = "\n\n".join(
        f"########## user [{i}] {stamp(m)}\n\n{body(m)}"
        for i, m in enumerate(chain)
        if m["role"] == "user"
    )
    (out_dir / "user-messages.md").write_text(users, encoding="utf-8")

    print(f"{out_dir}/transcript.md, {out_dir}/user-messages.md: {len(chain)} сообщений")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        raise SystemExit(2)
    raise SystemExit(main(sys.argv[1], sys.argv[2]))
