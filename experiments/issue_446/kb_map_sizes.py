#!/usr/bin/env python3
"""Размер карт разделов БЗ runtime и компактного оглавления (RFC-RT-001, раздел 14, РТ-7).

RUN-0083 показал: исполнитель читает карту `docs/kb/maps/<документ>.json`
частично, если она больше лимита одного чтения. Скрипт меряет карты на
клоне runtime и оценивает компактное оглавление «раздел | название | путь»
без `hint`, `pages`, `tokens` и `id`.

Использование:
    python3 -I experiments/issue_446/kb_map_sizes.py /tmp/rt446 > experiments/issue_446/kb-map-sizes.log
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

# Порог одного чтения карты — ориентир РТ-7 (около 32 КБ ≈ 8–10 тыс. токенов).
LIMIT = 32 * 1024


def toc(sections) -> str:
    # Путь пишется относительно каталога документа: префикс повторяется в каждой строке.
    return "".join(f"{s['section']}\t{s['title']}\t{Path(s['path']).name}\n" for s in sections)


def main() -> int:
    clone = Path(sys.argv[1]).resolve()
    sha = subprocess.run(["git", "-C", str(clone), "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
    maps = sorted((clone / "docs/kb/maps").glob("*.json"), key=lambda p: -p.stat().st_size)
    print(f"runtime {sha}; карт: {len(maps)}; MAP.json: {(clone / 'docs/kb/MAP.json').stat().st_size} Б; порог {LIMIT} Б")
    print("документ\tкарта, Б\tразделов\tоглавление, Б\tкарта > порога\tоглавление > порога")
    over_map = over_toc = 0
    for path in maps:
        data = json.loads(path.read_text(encoding="utf-8"))
        sections = data["sections"]
        size = path.stat().st_size
        compact = len(toc(sections).encode("utf-8"))
        over_map += size > LIMIT
        over_toc += compact > LIMIT
        print(f"{path.stem}\t{size}\t{len(sections)}\t{compact}\t{'да' if size > LIMIT else 'нет'}\t{'да' if compact > LIMIT else 'нет'}")
    print(f"итого: карт больше порога — {over_map}, оглавлений больше порога — {over_toc}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
