#!/usr/bin/env python3
"""Regression check for issue #133 — runs/ README split and classification."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

RUN_TYPES = {
    "RUN-0001": "experiment",
    "RUN-0002": "generation",
    "RUN-0003": "generation",
    "RUN-0004": "validation",
    "RUN-0005": "validation",
    "RUN-0006": "documentation",
    "RUN-0007": "generation",
    "RUN-0008": "validation",
    "RUN-0009": "experiment",
    "RUN-0010": "business-task",
    "RUN-0011": "business-task",
    "RUN-0012": "business-task",
    "RUN-0013": "business-task",
    "RUN-0014": "business-task",
    "RUN-0015": "validation",
}

TYPE_LABELS = {
    "experiment": "эксперимент",
    "generation": "генерация",
    "validation": "валидация",
    "documentation": "документирование",
    "business-task": "бизнес-задача",
}


def read_text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def parse_simple_yaml(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.+?)\s*$", line)
        if match:
            data[match.group(1)] = match.group(2).strip().strip('"')
    return data


def require_path(path: str) -> list[str]:
    return [] if (ROOT / path).exists() else [f"{path}: missing"]


def require_text(path: str, *needles: str) -> list[str]:
    text = read_text(path)
    return [f"{path}: missing {needle!r}" for needle in needles if needle not in text]


def check_metadata() -> list[str]:
    errors: list[str] = []
    allowed = set(TYPE_LABELS)
    for run_id, expected_type in RUN_TYPES.items():
        path = ROOT / "runs" / "2026" / run_id / "metadata.yaml"
        metadata = parse_simple_yaml(path)
        actual_type = metadata.get("run_type")
        if actual_type != expected_type:
            errors.append(f"{path.relative_to(ROOT)}: run_type {actual_type!r} != {expected_type!r}")
        if actual_type and actual_type not in allowed:
            errors.append(f"{path.relative_to(ROOT)}: unsupported run_type {actual_type!r}")
    return errors


def check_docs() -> list[str]:
    errors: list[str] = []
    required_docs = (
        "runs/README.md",
        "runs/CONTRACT.md",
        "runs/REGISTRY.md",
        "runs/stats/by-type.md",
        "runs/stats/by-date.md",
        "runs/stats/by-process.md",
    )
    for path in required_docs:
        errors += require_path(path)
    if errors:
        return errors

    errors += require_text(
        "runs/README.md",
        "Что это",
        "Быстрый старт",
        "CONTRACT.md",
        "REGISTRY.md",
        "stats/by-type.md",
    )
    errors += require_text("runs/CONTRACT.md", "run_type", "runs/YYYY/RUN-XXXX/", "metadata.yaml")
    errors += require_text("runs/REGISTRY.md", "| Run | Дата | Тип | Процесс | Основной результат | Лог |")
    for run_id, run_type in RUN_TYPES.items():
        errors += require_text("runs/REGISTRY.md", run_id, run_type)
    for run_type, label in TYPE_LABELS.items():
        errors += require_text("runs/stats/by-type.md", run_type, label)
    for run_id in RUN_TYPES:
        errors += require_text("runs/stats/by-type.md", run_id)
        errors += require_text("runs/stats/by-date.md", run_id)
        errors += require_text("runs/stats/by-process.md", run_id)
    errors += require_text("runs/stats/by-type.md", "Всего: 15")
    errors += require_text("runs/stats/by-date.md", "2026-05", "2026-06", "Тренд")
    errors += require_text("runs/stats/by-process.md", "Уникальных процессов: 15")
    errors += require_text(".github/workflows/github-pages.yml", "Validate issue #133 runs restructure")
    return errors


def main() -> int:
    errors = check_metadata() + check_docs()
    if errors:
        print("issue-133 runs restructure validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("issue-133 runs restructure validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
