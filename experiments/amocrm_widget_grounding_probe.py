#!/usr/bin/env python3
"""Проверка заземления сносок [[N]] в экспорте чата задачи 1007 (RUN-0026).

Зачем: в прогоне 1007 модель заявила, что «результаты проверки документации
подтверждают» локацию настройки (виджет в amoCRM, а не ЛК MANGO OFFICE), и
сопроводила вывод сносками `[[30]]`, `[[40]]`, `[[49]]`. Списка источников в
ответе нет, поэтому читатель не может проверить ни номер сноски, ни то, была ли
страница вообще прочитана.

Скрипт разбирает `content_list[*].extra.tool_result` экспорта и печатает:

- сквозную нумерацию документов `web_search` — по ней сноска `[[N]]`
  сопоставляется с конкретным URL и сниппетом;
- статус извлечения страниц `web_extractor` (`tool_call_metrics.extract_page_success`)
  — 0 означает, что текст страницы не получен;
- вхождения контрольных терминов во всех результатах инструментов.

Скрипт — локальный инструмент воспроизводимости, а не артефакт прогона:
запускается вручную, из CI не вызывается, зависимостей вне stdlib не имеет.

Использование:
    python3 experiments/amocrm_widget_grounding_probe.py \
        runs/2026/RUN-0026/inputs/1007-chat-export-1787301730570.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

# Термины, которыми модель обосновала локацию настройки и метку поля.
CHECKED_TERMS = (
    "стр. 127",
    "127",
    "удавшег",
    "недозвон",
    "Перенести в воронку",
    "digital-воронк",
    "виджет",
    "Личн",
    "автоперезвон",
    "идемпотент",
)


def linear_chain(export: list) -> list[dict]:
    """Линейная ветка диалога: от currentId вверх по parentId (см. scripts/chat_export_to_markdown.py)."""

    chat = export[0]
    history = chat["chat"]["history"]
    messages = history["messages"]
    chain: list[dict] = []
    message_id = chat.get("currentId") or history.get("currentId")
    seen: set[str] = set()
    while message_id and message_id not in seen:
        seen.add(message_id)
        chain.append(messages[message_id])
        message_id = messages[message_id].get("parentId")
    chain.reverse()
    return chain


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("export", type=Path)
    args = parser.parse_args()

    chain = linear_chain(json.loads(args.export.read_text(encoding="utf-8")))

    combined = ""
    doc_number = 0
    for index, message in enumerate(chain):
        for part in message.get("content_list") or []:
            extra = part.get("extra") or {}
            result = extra.get("tool_result")
            if not result:
                continue
            phase = part.get("phase", "?")
            payload = json.dumps(result, ensure_ascii=False)
            combined += payload
            print(f"\n## реплика [{index}] · {phase} · {len(payload)} символов результата")
            if phase == "web_search":
                for doc in result.get("docs", []):
                    doc_number += 1
                    print(f"[[{doc_number}]] {doc.get('url')}")
                    print(f"      {(doc.get('snippet') or '').strip()[:160]}")
            if phase == "web_extractor":
                metrics = result.get("tool_call_metrics", {})
                print(f"extract_page_success: {metrics.get('extract_page_success')}")
                print(f"cache_hit: {metrics.get('cache_hit')}")
                observation = result.get("tool_observation", "")
                print(f"страниц с текстом: {observation.count('Evidence in page') - observation.count('could not be accessed')}")

    print(f"\nсуммарный объём результатов инструментов: {len(combined)} символов")
    print(f"документов в выдаче поиска: {doc_number}")
    print("\n| Термин | Вхождений в источниках |")
    print("| --- | --- |")
    for term in CHECKED_TERMS:
        print(f"| `{term}` | {combined.count(term)} |")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
