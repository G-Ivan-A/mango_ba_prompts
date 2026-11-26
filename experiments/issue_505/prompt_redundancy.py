#!/usr/bin/env python3
"""Избыточность текста промптов BCREQ (issue #505, RFC-BCREQ-PROMPT-DEBUG-001).

Считает, сколько символов каждого AIN-промпта приходится на строки, общие
для всех 24 карточек (общий исполняемый контракт), а сколько — на
уникальную часть шага. Дополнительно — размеры остальных черновиков
маршрута BCREQ, которые БА вставляет в тот же чат.

Запуск из корня репозитория:
    python3 -I experiments/issue_505/prompt_redundancy.py \
        > runs/2026/RUN-0096/logs/prompt-redundancy.json

Вывод детерминирован: зависит только от файлов в prompts/drafts/.
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AIN_DIR = ROOT / "prompts" / "drafts" / "a-in"
DRAFTS = ROOT / "prompts" / "drafts"
CHAT_ROUTE = [  # то, что БА вставил в чат 1143, кроме AIN-01…24
    "bcreq-constitution-governance-oneshot.md",
    "bcreq-fr-documentation-stepwise.md",
    "bcreq-nfr-documentation-stepwise.md",
    "bcreq-uc-modeling-stepwise.md",
]
SECTIONS = [  # заголовки разделов общего контракта A-IN
    "## Вход и полномочия",
    "## Границы, вопросы и гейты",
    "## Источники, память и изменения",
    "## Доказательная нормализация и фактический доступ",
    "## Взаимодействие и квитанция каждого ответа",
]


def section_sizes(text: str) -> dict[str, int]:
    """Размер каждого раздела общего контракта в символах (до следующего `## `)."""
    sizes: dict[str, int] = {}
    lines = text.split("\n")
    for head in SECTIONS:
        try:
            start = lines.index(head)
        except ValueError:
            continue
        end = next(
            (i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")),
            len(lines),
        )
        sizes[head[3:]] = len("\n".join(lines[start:end]))
    return sizes


def main() -> dict:
    files = sorted(AIN_DIR.glob("bcreq-ain-*.md"))
    texts = {f.name: f.read_text(encoding="utf-8") for f in files}
    line_sets = {name: set(t.split("\n")) for name, t in texts.items()}
    counts: Counter[str] = Counter()
    for lines in line_sets.values():
        counts.update(lines)
    common = {line for line, n in counts.items() if n == len(files) and line.strip()}

    per_file = []
    for name, text in texts.items():
        lines = text.split("\n")
        shared = sum(len(l) + 1 for l in lines if l in common)
        total = len(text)
        per_file.append(
            {
                "file": name,
                "chars": total,
                "shared_chars": shared,
                "unique_chars": total - shared,
                "unique_share": round((total - shared) / total, 3),
            }
        )

    ain_total = sum(p["chars"] for p in per_file)
    ain_unique = sum(p["unique_chars"] for p in per_file)
    common_block = max(p["shared_chars"] for p in per_file)
    route = {name: len((DRAFTS / name).read_text(encoding="utf-8")) for name in CHAT_ROUTE}
    route_total = ain_total + sum(route.values())
    # Сценарий RFC: общий контракт вставляется один раз, карточки — только уникальная часть.
    once = ain_unique + common_block + sum(route.values())
    return {
        "ain_files": len(files),
        "common_lines": len(common),
        "common_block_chars": common_block,
        "common_sections_chars": section_sizes(next(iter(texts.values()))),
        "ain_total_chars": ain_total,
        "ain_unique_chars": ain_unique,
        "ain_unique_share_min": min(p["unique_share"] for p in per_file),
        "ain_unique_share_max": max(p["unique_share"] for p in per_file),
        "route_other_prompts_chars": route,
        "route_total_chars_as_pasted": route_total,
        "route_total_chars_contract_once": once,
        "route_saving_share": round(1 - once / route_total, 3),
        "per_file": per_file,
    }


if __name__ == "__main__":
    json.dump(main(), sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
