#!/usr/bin/env python3
"""Проверка заземления сносок [[N]] в экспорте чата задачи 1020 (RUN-0023).

Зачем: в прогоне 1020 модель сопроводила ключевые утверждения сносками вида
`[[1]]`, `[[2]]`, которые отсылают к результатам встроенных веб-инструментов
(`web_search`, `web_extractor`). Ответ модели читается как «со ссылкой на
документацию», но сам текст источника в диалоге не показан. Скрипт извлекает
сырые результаты инструментов и считает в них вхождения проверяемых терминов,
чтобы утверждение «источник это подтверждает» можно было проверить, а не
принять на веру.

Скрипт — локальный инструмент воспроизводимости, а не артефакт прогона:
запускается вручную, из CI не вызывается, зависимостей вне stdlib не имеет.

Использование:
    python3 experiments/okdesk_citation_grounding_probe.py \
        runs/2026/RUN-0023/inputs/1020-chat-export-1787301522802.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

# Термины, которыми модель обосновала ограничение модели данных OkDesk,
# и контрольные термины, заведомо присутствующие в извлечённых страницах.
CHECKED_TERMS = (
    "incoming",
    "outgoing",
    "call_record",
    "телефонн",
    "разговор",
    "звонк",
    "direction",
    "Лид",
    "лид",
    "company",
)


def tool_results(message: dict) -> list[tuple[int, str, str]]:
    """(индекс части, фаза, сериализованный результат инструмента)."""

    found: list[tuple[int, str, str]] = []
    for index, part in enumerate(message.get("content_list") or []):
        extra = part.get("extra")
        if isinstance(extra, dict) and extra.get("tool_result"):
            found.append(
                (index, part.get("phase", "?"), json.dumps(extra["tool_result"], ensure_ascii=False))
            )
    return found


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("export", type=Path)
    args = parser.parse_args()

    export = json.loads(args.export.read_text(encoding="utf-8"))
    messages = export[0]["chat"]["history"]["messages"]

    combined = ""
    for message in messages.values():
        if message.get("role") != "assistant":
            continue
        for index, phase, payload in tool_results(message):
            print(f"tool call: part {index}, phase={phase}, result_chars={len(payload)}")
            combined += payload

    print(f"\nсуммарный объём результатов инструментов: {len(combined)} символов")
    print("\n| Термин | Вхождений в источниках |")
    print("| --- | --- |")
    for term in CHECKED_TERMS:
        print(f"| `{term}` | {combined.count(term)} |")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
