#!/usr/bin/env python3
"""Проверка заземления сносок прогона 978 (подписи email) на результаты веб-поиска.

Зачем: в реплике 5 диалога модель валидирует НФТ-001…НФТ-003 и ставит сноски
вида `[[10]]`. Утверждение «сноска подтверждена» проверяемо только если
контрольный термин утверждения встречается в тексте, который инструмент реально
вернул модели (`content_list[*].extra.tool_result.tool_observation`).

Скрипт детерминированно достаёт результаты `web_search` / `web_extractor` из
выгрузки чата и считает вхождения контрольных терминов. Только stdlib.

Использование:
    python3 experiments/signature_citation_grounding_probe.py <export.json>
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

# Контрольные термины: что должно найтись в выдаче инструмента, если утверждение
# модели заземлено на источник, а не на память.
PROBES: dict[str, tuple[str, ...]] = {
    "НФТ-001 Gmail clipping 102 КБ": ("102KB", "102 KB", "102kB"),
    "НФТ-002 Outlook signature 30 000 символов": ("30,000 characters",),
    "НФТ-002 «30 000 символов ≈ 30 КБ»": ("approximately **30 KB**", "approximately 30 KB"),
    "НФТ-002 лимит включает Base64-изображения": ("embedded images", "Base64 enco"),
    "НФТ-003 Outlook 20–35 МБ": ("20-34MB", "20-34 MB", "35 MB"),
    "НФТ-003 Gmail 25 МБ": ("25MB", "25 MB"),
    "Body.setSignatureAsync как источник лимита": ("setSignatureAsync",),
    "Рекомендация «целевой лимит ≤80 КБ» + минификация": ("below 80KB",),
    "Base64 увеличивает размер (качественно)": ("Base64 encoding increases", "increases the image size"),
    "Base64 увеличивает размер ровно на ~33 % (число)": ("33%", "33 %", "one-third"),
    "«200 КБ» как лимит файла изображения": ("200KB", "200 KB"),
}


def linear_chain(export: list) -> list[dict]:
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


def tool_outputs(chain: list[dict]) -> list[tuple[int, str, str]]:
    """(индекс реплики, фаза, текст выдачи инструмента)."""

    found: list[tuple[int, str, str]] = []
    for index, message in enumerate(chain):
        for part in message.get("content_list") or []:
            result = (part.get("extra") or {}).get("tool_result")
            if not isinstance(result, dict):
                continue
            observation = result.get("tool_observation")
            if isinstance(observation, str) and observation:
                found.append((index, part.get("phase", "?"), observation))
    return found


def sources(chain: list[dict]) -> list[str]:
    urls: list[str] = []
    for message in chain:
        for part in message.get("content_list") or []:
            for item in (part.get("extra") or {}).get("web_search_info") or []:
                url = item.get("url")
                if url and url not in urls:
                    urls.append(url)
    return urls


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("export", type=Path)
    args = parser.parse_args()

    chain = linear_chain(json.loads(args.export.read_text(encoding="utf-8")))
    outputs = tool_outputs(chain)
    corpus = "\n".join(text for _, _, text in outputs)

    print(f"реплик в ветке: {len(chain)}")
    print(f"вызовов инструментов с выдачей: {len(outputs)}")
    for index, phase, text in outputs:
        print(f"  реплика {index}: {phase}, {len(text)} символов")
    print(f"уникальных источников в web_search_info: {len(sources(chain))}")
    print()
    print("| Проверяемое утверждение | Вхождений | Заземлено |")
    print("| --- | ---: | --- |")
    for label, terms in PROBES.items():
        hits = sum(len(re.findall(re.escape(term), corpus)) for term in terms)
        print(f"| {label} | {hits} | {'да' if hits else 'НЕТ'} |")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
