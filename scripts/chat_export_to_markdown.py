#!/usr/bin/env python3
"""Конвертер экспорта чата (OpenWebUI-подобный JSON) в транскрипт и метрики прогона.

Зачем: истории чатов приходят в задачи `runs: <id>` как приложенный JSON. Ручное
чтение такого файла не воспроизводимо, поэтому вход прогона разворачивается в
markdown детерминированным скриптом (только stdlib).

Особенности формата:
- сообщения лежат в `[0].chat.history.messages` как словарь по id с `parentId`;
  линейная ветка восстанавливается обходом от `currentId` вверх по `parentId`;
- текст ответа ассистента находится не в `content`, а в элементах `content_list`
  с `phase == "answer"` (есть также `thinking_summary`);
- метрики токенов — в `content_list[*].usage`.

Статус: локальный инструмент воспроизводимости, а не артефакт прогона. Запускается
вручную, из CI/GitHub Actions не вызывается (см. `runs/README.md`, раздел
«Локальные инструменты воспроизводимости»).

Использование:
    python3 scripts/chat_export_to_markdown.py <export.json> \
        [--transcript transcript.md] [--metrics turn-metrics.md]
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path


def linear_chain(export: list) -> list[dict]:
    chat = export[0]
    history = chat["chat"]["history"]
    messages = history["messages"]
    chain: list[dict] = []
    message_id = chat.get("currentId") or history.get("currentId")
    seen: set[str] = set()
    while message_id and message_id not in seen:
        seen.add(message_id)
        message = messages[message_id]
        chain.append(message)
        message_id = message.get("parentId")
    chain.reverse()
    return chain


def answer_text(message: dict) -> str:
    parts = [
        part["content"]
        for part in (message.get("content_list") or [])
        if part.get("phase") == "answer" and part.get("content")
    ]
    return "\n\n".join(parts) or message.get("content", "")


def usage(message: dict) -> dict:
    for part in reversed(message.get("content_list") or []):
        if part.get("usage"):
            return part["usage"]
    return {}


def utc(timestamp: int | None) -> str:
    if not timestamp:
        return ""
    return dt.datetime.fromtimestamp(timestamp, dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


def render_transcript(chain: list[dict]) -> str:
    blocks = []
    for index, message in enumerate(chain):
        files = [file.get("name") for file in (message.get("files") or [])]
        header = f"===== [{index}] {message['role']} {message.get('model') or ''} files={files} ====="
        blocks.append(f"{header}\n{answer_text(message)}")
    return "\n\n".join(blocks) + "\n"


def render_metrics(chain: list[dict]) -> str:
    rows = ["| # | Роль | Модель | UTC | Символов | in_tokens | out_tokens | reasoning | Вложения |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    total_in = total_out = total_reasoning = 0
    for index, message in enumerate(chain):
        use = usage(message)
        total_in += use.get("input_tokens", 0)
        total_out += use.get("output_tokens", 0)
        total_reasoning += (use.get("output_tokens_details") or {}).get("reasoning_tokens", 0)
        files = ", ".join(file.get("name", "") for file in (message.get("files") or [])) or "—"
        rows.append(
            f"| {index} | {message['role']} | {message.get('model') or '—'} | {utc(message.get('timestamp'))} "
            f"| {len(answer_text(message))} | {use.get('input_tokens', '—')} | {use.get('output_tokens', '—')} "
            f"| {(use.get('output_tokens_details') or {}).get('reasoning_tokens', '—')} | {files} |"
        )
    duration = (chain[-1].get("timestamp") or 0) - (chain[0].get("timestamp") or 0)
    summary = [
        "",
        f"- **turns:** {len(chain)}",
        f"- **input_tokens:** {total_in}",
        f"- **output_tokens:** {total_out}",
        f"- **reasoning_tokens:** {total_reasoning}",
        f"- **total_tokens:** {total_in + total_out}",
        f"- **duration_s:** {duration} (~{duration / 3600:.2f} ч)",
        f"- **window:** {utc(chain[0].get('timestamp'))} — {utc(chain[-1].get('timestamp'))} UTC",
    ]
    return "\n".join(rows + summary) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("export", type=Path)
    parser.add_argument("--transcript", type=Path)
    parser.add_argument("--metrics", type=Path)
    args = parser.parse_args()

    export = json.loads(args.export.read_text(encoding="utf-8"))
    chain = linear_chain(export)

    if args.transcript:
        args.transcript.write_text(render_transcript(chain), encoding="utf-8")
    if args.metrics:
        args.metrics.write_text(render_metrics(chain), encoding="utf-8")
    if not args.transcript and not args.metrics:
        print(render_metrics(chain))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
