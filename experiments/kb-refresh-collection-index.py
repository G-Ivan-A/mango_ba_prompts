#!/usr/bin/env python3
"""Пересобрать index.md/meta.json комплекта kb/processed/<collection>/ без PDF.

Нужен, когда обновилась часть документов комплекта (issue #317: два из пяти
руководств Mango Talker), а исходные PDF остальных уже удалены из рабочего
каталога — сам конвейер в этом случае требует все файлы.
Никакие данные не выдумываются: строки таблицы берутся из meta.json уже
извлечённых документов.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "kb"))

import process_sources as ps  # noqa: E402


def main(argv):
    source_dir = Path(argv[1]) if len(argv) > 1 else ROOT / "kb/sources/mtalker"
    plan = ps.build_plan(source_dir.resolve(), ps.PROCESSED_ROOT, require_sources=False)
    ps.write_collection_index(plan)
    print(f"collection index refreshed: {ps.rel_to_root(plan.output_dir)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
