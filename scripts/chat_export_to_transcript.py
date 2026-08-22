#!/usr/bin/env python3
"""Chat export (Open WebUI style JSON) → воспроизводимая стенограмма и метрики.

Используется для фиксации прогонов в ``runs/``: сырой экспорт чата кладётся в
``inputs/``, а читаемая стенограмма и метрики порождаются из него детерминированно,
чтобы фиксация оставалась проверяемой (см. ``standards/runs-contract-standard.md``).

Формат входа: список чатов; берётся первый. Порядок сообщений восстанавливается
по цепочке ``parentId`` от ``currentId`` — это фактическая ветка диалога, а не
все черновики. Текст ответа ассистента лежит не в ``content``, а в элементах
``content_list`` с ``phase == "answer"``; там же — расход токенов.

Пример:

    python3 scripts/chat_export_to_transcript.py \\
        runs/2026/RUN-0019/inputs/chat-export-1064.json \\
        --transcript runs/2026/RUN-0019/inputs/chat-transcript.md \\
        --metrics runs/2026/RUN-0019/logs/metrics.md
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


# Сообщения без gap-cap: перерыв между сессиями (дни) не является работой БА.
SESSION_GAP_SECONDS = 30 * 60


def load_chat(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        if not data:
            raise SystemExit(f"{path}: export is empty")
        return data[0]
    return data


def ordered_messages(chat: dict[str, Any]) -> list[dict[str, Any]]:
    """Ветка диалога от корня до ``currentId`` (порядок — хронологический)."""
    history = chat["chat"]["history"]["messages"]
    current = chat["chat"].get("currentId") or chat.get("currentId")
    chain: list[dict[str, Any]] = []
    seen: set[str] = set()
    while current:
        if current in seen:
            raise SystemExit(f"cycle in parentId chain at {current}")
        seen.add(current)
        message = history[current]
        chain.append(message)
        current = message.get("parentId")
    chain.reverse()
    return chain


def answer_text(message: dict[str, Any]) -> str:
    if message.get("role") != "assistant":
        return (message.get("content") or "").replace("\r\n", "\n").strip()
    parts = [
        (part.get("content") or "").strip()
        for part in (message.get("content_list") or [])
        if part.get("phase") == "answer"
    ]
    text = "\n\n".join(part for part in parts if part)
    return (text or (message.get("content") or "")).replace("\r\n", "\n").strip()


def usage(message: dict[str, Any]) -> dict[str, int]:
    content_list = message.get("content_list") or []
    if not content_list:
        return {}
    return content_list[-1].get("usage") or {}


def stamp(seconds: int | None) -> str:
    if not seconds:
        return "—"
    return datetime.fromtimestamp(seconds, timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def render_transcript(chat: dict[str, Any], messages: list[dict[str, Any]], source: str) -> str:
    title = chat.get("title", "—")
    lines = [
        "---",
        "status: draft",
        "version: 0.1",
        "ai-generated: true",
        "type: input",
        "generator: scripts/chat_export_to_transcript.py",
        f"source: {source}",
        "---",
        "",
        f"# Стенограмма чата «{title}»",
        "",
        "> Файл **порождён** из сырого экспорта — не редактируйте вручную.",
        "> Воспроизведение: `python3 scripts/chat_export_to_transcript.py "
        f"{source} --transcript <этот файл>`.",
        "> Время — UTC, как в экспорте. Реплики ассистента приведены без блоков"
        " размышлений (`thinking_summary`): в экспорте они пусты, кроме служебных"
        " заголовков.",
        "",
        f"- Сообщений в ветке диалога: **{len(messages)}**",
        f"- Модели: **{', '.join(chat['chat'].get('models') or ['—'])}**",
        f"- Первое сообщение: **{stamp(messages[0].get('timestamp'))}**",
        f"- Последнее сообщение: **{stamp(messages[-1].get('timestamp'))}**",
        "",
        "---",
        "",
    ]
    for index, message in enumerate(messages):
        role = message.get("role", "—")
        model = message.get("model") or "—"
        head = f"## [{index}] {role} · {stamp(message.get('timestamp'))}"
        if role == "assistant":
            head += f" · {model}"
        lines += [head, "", answer_text(message) or "_(пустой ответ)_", ""]
    return "\n".join(lines).rstrip() + "\n"


def render_metrics(chat: dict[str, Any], messages: list[dict[str, Any]], source: str) -> str:
    timestamps = [m["timestamp"] for m in messages if m.get("timestamp")]
    assistant = [m for m in messages if m.get("role") == "assistant"]
    user = [m for m in messages if m.get("role") == "user"]

    output_tokens = sum(usage(m).get("output_tokens", 0) for m in assistant)
    reasoning_tokens = sum(
        (usage(m).get("output_tokens_details") or {}).get("reasoning_tokens", 0) for m in assistant
    )
    input_tokens = [usage(m).get("input_tokens", 0) for m in assistant]

    sessions: list[list[int]] = []
    for value in timestamps:
        if sessions and value - sessions[-1][-1] <= SESSION_GAP_SECONDS:
            sessions[-1].append(value)
        else:
            sessions.append([value])
    active_seconds = sum(session[-1] - session[0] for session in sessions)

    lines = [
        "---",
        "status: draft",
        "version: 0.1",
        "ai-generated: true",
        "type: log",
        "generator: scripts/chat_export_to_transcript.py",
        f"source: {source}",
        "---",
        "",
        f"# Метрики прогона по экспорту чата «{chat.get('title', '—')}»",
        "",
        "> Файл **порождён** из сырого экспорта — не редактируйте вручную.",
        "> Все числа взяты из полей `usage` и `timestamp` самого экспорта, не оценочные.",
        "",
        "## Объём диалога",
        "",
        "| Метрика | Значение |",
        "| --- | --- |",
        f"| Сообщений в ветке | {len(messages)} |",
        f"| Реплик пользователя (БА) | {len(user)} |",
        f"| Ответов модели | {len(assistant)} |",
        f"| Модель | {', '.join(chat['chat'].get('models') or ['—'])} |",
        f"| Символов ввода БА | {sum(len(m.get('content') or '') for m in user)} |",
        f"| Символов ответов модели | {sum(len(answer_text(m)) for m in assistant)} |",
        "",
        "## Токены",
        "",
        "| Метрика | Значение |",
        "| --- | --- |",
        f"| Выход модели, суммарно | {output_tokens} |",
        f"| В том числе reasoning | {reasoning_tokens} |",
        f"| Вход (сумма по всем вызовам, с учётом переотправки контекста) | {sum(input_tokens)} |",
        f"| Вход, максимум за один вызов | {max(input_tokens or [0])} |",
        f"| Вход, минимум за один вызов | {min(input_tokens or [0])} |",
        "",
        "## Календарь и длительность",
        "",
        "| Метрика | Значение |",
        "| --- | --- |",
        f"| Начало | {stamp(timestamps[0])} |",
        f"| Конец | {stamp(timestamps[-1])} |",
        f"| Календарный интервал | {(timestamps[-1] - timestamps[0]) / 86400:.1f} дн. |",
        f"| Рабочих сессий (разрыв > {SESSION_GAP_SECONDS // 60} мин) | {len(sessions)} |",
        f"| Активное время внутри сессий | {active_seconds / 60:.0f} мин |",
        "",
        "## По ответам модели",
        "",
        "| # | Время (UTC) | Вход, ток. | Выход, ток. | Reasoning, ток. |",
        "| --- | --- | --- | --- | --- |",
    ]
    for index, message in enumerate(messages):
        if message.get("role") != "assistant":
            continue
        use = usage(message)
        lines.append(
            f"| {index} | {stamp(message.get('timestamp'))} | {use.get('input_tokens', 0)} | "
            f"{use.get('output_tokens', 0)} | "
            f"{(use.get('output_tokens_details') or {}).get('reasoning_tokens', 0)} |"
        )
    lines += [
        "",
        "> Скачки входных токенов (тысячи → сотни тысяч) — это прикреплённые к"
        " отдельным репликам документы (руководства и PDF по интеграциям), а не рост"
        " самой переписки: чистая переписка занимает единицы тысяч токенов.",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("export", type=Path, help="JSON-экспорт чата")
    parser.add_argument("--transcript", type=Path, help="куда записать стенограмму (.md)")
    parser.add_argument("--metrics", type=Path, help="куда записать метрики (.md)")
    parser.add_argument(
        "--source",
        default=None,
        help="путь к экспорту, который подставляется в шапку (по умолчанию — аргумент export)",
    )
    args = parser.parse_args()

    chat = load_chat(args.export)
    messages = ordered_messages(chat)
    source = args.source or args.export.as_posix()

    if not args.transcript and not args.metrics:
        parser.error("укажите --transcript и/или --metrics")

    if args.transcript:
        args.transcript.parent.mkdir(parents=True, exist_ok=True)
        args.transcript.write_text(render_transcript(chat, messages, source), encoding="utf-8")
        print(f"transcript → {args.transcript}")
    if args.metrics:
        args.metrics.parent.mkdir(parents=True, exist_ok=True)
        args.metrics.write_text(render_metrics(chat, messages, source), encoding="utf-8")
        print(f"metrics → {args.metrics}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
