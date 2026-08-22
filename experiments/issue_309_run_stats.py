#!/usr/bin/env python3
"""Статистика по экспорту чата → JSON (issue #309).

Зачем: задача #309 требует зафиксировать 25 экспортов чатов как прогоны с
``run_type: statistics`` — то есть накопить **статистику применения промптов и
операций процесса БА**, а не сложить в репозиторий сырые данные. Этот скрипт
считает такую статистику детерминированно: на вход — экспорт чата, на выход —
JSON с объёмом диалога, токенами (из полей ``usage`` самого экспорта),
календарём сессий, вложениями и эвристической разметкой типов запросов БА.

Разбор структуры экспорта переиспользуется из
``scripts/chat_export_to_markdown.py`` (линейная ветка диалога по ``parentId``,
текст ответа из ``content_list[*].phase == "answer"``, токены из ``usage``).

Статус: локальный инструмент воспроизводимости, из CI не вызывается.

Использование:
    python3 experiments/issue_309_run_stats.py <export.json> [--json out.json]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from chat_export_to_markdown import answer_text, linear_chain, usage, utc  # noqa: E402

# Разрыв между сообщениями, с которого начинается новая рабочая сессия.
SESSION_GAP_SECONDS = 30 * 60

#: Эвристическая разметка операций процесса БА по тексту реплики БА.
#: Метки не взаимоисключающие: одна реплика может нести несколько операций.
#: Эвристика намеренно грубая и объявлена как эвристика в самих артефактах.
REQUEST_KINDS: list[tuple[str, str]] = [
    ("prompt-engineering", r"промпт|prompt|инструкц|системн\w* сообщени"),
    ("artifact-generation", r"сформируй|составь|напиши|подготовь|сгенерир|выведи|оформи|сделай"),
    ("validation", r"проверь|провер\w+|валидир|оцени|соответств|критик|ошибк|замечани"),
    ("elicitation", r"уточн|вопрос|непонятн|что именно|какие данные"),
    ("iteration", r"исправ|доработ|перепиши|переделай|учти|измени|дополни|добавь"),
    ("context-load", r"приложен|во вложени|прикрепл|документ ниже|стенограмм|транскрип"),
]


def classify(text: str) -> list[str]:
    lowered = text.lower()
    return [kind for kind, pattern in REQUEST_KINDS if re.search(pattern, lowered)]


def collect(export_path: Path) -> dict:
    export = json.loads(export_path.read_text(encoding="utf-8"))
    chat = export[0]
    chain = linear_chain(export)

    user = [m for m in chain if m.get("role") == "user"]
    assistant = [m for m in chain if m.get("role") == "assistant"]
    stamps = [m["timestamp"] for m in chain if m.get("timestamp")]

    sessions: list[list[int]] = []
    for value in stamps:
        if sessions and value - sessions[-1][-1] <= SESSION_GAP_SECONDS:
            sessions[-1].append(value)
        else:
            sessions.append([value])

    inputs = [usage(m).get("input_tokens", 0) for m in assistant]
    kinds: dict[str, int] = {kind: 0 for kind, _ in REQUEST_KINDS}
    unclassified = 0
    for message in user:
        found = classify(message.get("content") or "")
        if not found:
            unclassified += 1
        for kind in found:
            kinds[kind] += 1

    attachments: dict[str, int] = {}
    for message in chain:
        for file in message.get("files") or []:
            name = file.get("name") or "—"
            attachments[name] = attachments.get(name, 0) + 1

    models = sorted({m.get("model") for m in assistant if m.get("model")})

    return {
        "source": export_path.name,
        "title": chat.get("title") or "—",
        "models": models,
        "turns": len(chain),
        "user_turns": len(user),
        "assistant_turns": len(assistant),
        "chars_user": sum(len(m.get("content") or "") for m in user),
        "chars_assistant": sum(len(answer_text(m)) for m in assistant),
        "tokens_input_sum": sum(inputs),
        "tokens_input_max": max(inputs or [0]),
        "tokens_output": sum(usage(m).get("output_tokens", 0) for m in assistant),
        "tokens_reasoning": sum(
            (usage(m).get("output_tokens_details") or {}).get("reasoning_tokens", 0)
            for m in assistant
        ),
        "start_utc": utc(stamps[0]) if stamps else "",
        "end_utc": utc(stamps[-1]) if stamps else "",
        "calendar_days": round((stamps[-1] - stamps[0]) / 86400, 1) if stamps else 0,
        "sessions": len(sessions),
        "active_minutes": round(sum(s[-1] - s[0] for s in sessions) / 60),
        "session_rows": [
            {
                "start_utc": utc(s[0]),
                "end_utc": utc(s[-1]),
                "messages": len(s),
                "minutes": round((s[-1] - s[0]) / 60),
            }
            for s in sessions
        ],
        "request_kinds": kinds,
        "requests_unclassified": unclassified,
        "attachments": attachments,
        "turn_rows": [
            {
                "index": index,
                "role": message.get("role"),
                "model": message.get("model") or "—",
                "utc": utc(message.get("timestamp")),
                "chars": len(answer_text(message))
                if message.get("role") == "assistant"
                else len(message.get("content") or ""),
                "input_tokens": usage(message).get("input_tokens", 0),
                "output_tokens": usage(message).get("output_tokens", 0),
                "reasoning_tokens": (usage(message).get("output_tokens_details") or {}).get(
                    "reasoning_tokens", 0
                ),
                "files": [f.get("name", "") for f in (message.get("files") or [])],
            }
            for index, message in enumerate(chain)
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("export", type=Path)
    parser.add_argument("--json", type=Path, help="куда записать статистику")
    args = parser.parse_args()

    stats = collect(args.export)
    text = json.dumps(stats, ensure_ascii=False, indent=2) + "\n"
    if args.json:
        args.json.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
