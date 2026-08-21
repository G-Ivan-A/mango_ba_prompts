#!/usr/bin/env python3
"""Рендер экспорта чата (Qwen web UI, JSON) в Markdown-стенограмму и метрики.

Экспорт хранит ответ ассистента не в ``content``, а в ``content_list``: там
лежат фазы ``thinking_summary`` / ``web_search`` / ``web_extractor`` / ``answer``.
Наивное чтение ``content`` даёт пустые ответы — отсюда отдельный рендер.

Запуск:

    python3 experiments/run-0014-chat-export/render_chat_export.py \
        runs/2026/RUN-0014/inputs/chat-export-1075.json \
        --transcript runs/2026/RUN-0014/logs/chat-transcript.md \
        --metrics-json -
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path


def linear_chain(history: dict) -> list[dict]:
    """Активная ветка диалога: от currentId вверх по parentId."""
    messages = history["messages"]
    chain: list[dict] = []
    current = history.get("currentId")
    while current:
        message = messages[current]
        chain.append(message)
        current = message.get("parentId")
    return list(reversed(chain))


def answer_phases(message: dict) -> list[dict]:
    return [part for part in (message.get("content_list") or []) if part.get("phase") == "answer"]


def answer_text(message: dict) -> str:
    return "\n\n".join(part.get("content") or "" for part in answer_phases(message)).strip()


def usage(message: dict) -> dict:
    phases = answer_phases(message)
    return phases[-1].get("usage", {}) if phases else {}


def iso(timestamp: int | None) -> str:
    if not timestamp:
        return ""
    return dt.datetime.fromtimestamp(timestamp, dt.UTC).strftime("%Y-%m-%d %H:%M:%S UTC")


def web_sources(message: dict) -> list[dict]:
    """Источники, реально показанные модели: выдача поиска и извлечённые страницы."""
    found: list[dict] = []
    for part in message.get("content_list") or []:
        extra = part.get("extra") or {}
        for item in extra.get("web_search_info") or []:
            found.append({"kind": "search", "title": item.get("title"), "url": item.get("url")})
        for item in extra.get("web_extract_info") or []:
            found.append({"kind": "extract", "title": item.get("title"), "url": item.get("url")})
    return found


def render(chat: dict, title: str) -> tuple[str, dict]:
    chain = linear_chain(chat["history"])
    lines = [f"# Стенограмма чата «{title}»", ""]
    totals = {"input_tokens": 0, "output_tokens": 0, "reasoning_tokens": 0, "cached_tokens": 0}
    turns = []

    for index, message in enumerate(chain, start=1):
        role = message["role"]
        head = f"## [{index}] {'Пользователь' if role == 'user' else 'Ассистент'}"
        if role == "assistant":
            head += f" ({message.get('modelName') or message.get('model')})"
        lines += [head, "", f"*{iso(message.get('timestamp'))}*", ""]

        if role == "user":
            lines += [message.get("content", "").strip(), ""]
            for attachment in message.get("files") or []:
                lines += [f"**Вложение:** `{attachment.get('name')}`", ""]
            continue

        used = usage(message)
        details = used.get("output_tokens_details", {})
        prompt_details = used.get("prompt_tokens_details", {})
        totals["input_tokens"] += used.get("input_tokens", 0)
        totals["output_tokens"] += used.get("output_tokens", 0)
        totals["reasoning_tokens"] += details.get("reasoning_tokens", 0)
        totals["cached_tokens"] += prompt_details.get("cached_tokens", 0)
        turns.append(
            {
                "index": index,
                "id": message["id"],
                "timestamp": iso(message.get("timestamp")),
                "input_tokens": used.get("input_tokens", 0),
                "output_tokens": used.get("output_tokens", 0),
                "reasoning_tokens": details.get("reasoning_tokens", 0),
                "cached_tokens": prompt_details.get("cached_tokens", 0),
                "web_sources": web_sources(message),
            }
        )

        sources = web_sources(message)
        if sources:
            lines += ["**Веб-источники, показанные модели:**", ""]
            for number, source in enumerate(sources, start=1):
                mark = "извлечена" if source["kind"] == "extract" else "выдача поиска"
                lines.append(f"{number}. [{source['title']}]({source['url']}) — {mark}")
            lines.append("")

        lines += [answer_text(message) or "_(пустой ответ)_", ""]

    timestamps = [message["timestamp"] for message in chain if message.get("timestamp")]
    metrics = {
        "turns": turns,
        "totals": totals,
        "messages": len(chain),
        "started_at": iso(min(timestamps)) if timestamps else "",
        "finished_at": iso(max(timestamps)) if timestamps else "",
        "duration_seconds": (max(timestamps) - min(timestamps)) if timestamps else 0,
    }
    return "\n".join(lines).rstrip() + "\n", metrics


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("export", type=Path, help="JSON-экспорт чата")
    parser.add_argument("--transcript", type=Path, help="куда писать Markdown-стенограмму")
    parser.add_argument("--metrics-json", help="куда писать метрики (путь или '-' для stdout)")
    parser.add_argument("--front-matter", type=Path, help="файл с YAML frontmatter, добавляемым в начало стенограммы")
    args = parser.parse_args()

    payload = json.loads(args.export.read_text(encoding="utf-8"))
    chat_record = payload[0] if isinstance(payload, list) else payload
    transcript, metrics = render(chat_record["chat"], chat_record.get("title") or "chat")

    if args.front_matter:
        transcript = args.front_matter.read_text(encoding="utf-8").rstrip() + "\n\n" + transcript
    if args.transcript:
        args.transcript.write_text(transcript, encoding="utf-8")
    if args.metrics_json == "-":
        print(json.dumps(metrics, ensure_ascii=False, indent=2))
    elif args.metrics_json:
        Path(args.metrics_json).write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
