#!/usr/bin/env python3
"""Нагрузочный стенд валидаторов (issue #299): сколько стоит проверка при N прогонах.

Копирует репозиторий во временный каталог, размножает эталонный прогон до
N записей (metadata.yaml + строка реестра) и замеряет три сценария:

* ``full``   — полная проверка без кэша (цель задачи: ≤15 с при 1000 прогонах);
* ``fast``   — повторный запуск, всё из кэша;
* ``edit``   — правка одного файла прогона и инкрементальный запуск (цель: ≤1 с).

Запуск::

    python3 experiments/bench_validators.py --runs 1000
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TEMPLATE_RUN = "RUN-0002"


def build_fixture(destination: Path, total_runs: int) -> Path:
    shutil.copytree(
        REPO,
        destination,
        ignore=shutil.ignore_patterns(".git", ".validate-cache", "__pycache__", "*.pyc"),
    )
    runs_dir = destination / "runs/2026"
    template = runs_dir / TEMPLATE_RUN
    registry = destination / "runs/README.md"
    text = registry.read_text(encoding="utf-8")
    template_row = next(
        line for line in text.splitlines() if line.startswith(f"| [`{TEMPLATE_RUN}`]")
    )

    existing = len([p for p in runs_dir.glob("RUN-*") if p.is_dir()])
    rows: list[str] = []
    for index in range(existing + 1, total_runs + 1):
        run_id = f"RUN-{index:04d}"
        target = runs_dir / run_id
        if target.exists():
            continue
        shutil.copytree(template, target)
        meta = target / "metadata.yaml"
        meta.write_text(
            meta.read_text(encoding="utf-8").replace(TEMPLATE_RUN, run_id), encoding="utf-8"
        )
        rows.append(template_row.replace(TEMPLATE_RUN, run_id).replace(f"2026/{TEMPLATE_RUN}/", f"2026/{run_id}/"))
    if rows:
        registry.write_text(text.replace(template_row, template_row + "\n" + "\n".join(rows)), encoding="utf-8")
    return destination


def measure(label: str, root: Path, *args: str) -> float:
    started = time.perf_counter()
    proc = subprocess.run(
        [sys.executable, str(root / "scripts/validate_all.py"), *args],
        cwd=root,
        capture_output=True,
        text=True,
    )
    elapsed = time.perf_counter() - started
    summary = proc.stdout.strip().splitlines()[-1] if proc.stdout.strip() else ""
    status = "OK" if proc.returncode == 0 else f"FAIL(rc={proc.returncode})"
    print(f"{label:24s} {elapsed:6.2f}s  {status}  {summary}")
    if proc.returncode != 0:
        for line in proc.stdout.splitlines():
            if line.startswith(("FAIL", "       |")):
                print("   ", line)
    return elapsed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs", type=int, default=1000)
    parser.add_argument("--keep", action="store_true", help="не удалять стенд")
    args = parser.parse_args()

    workdir = Path("/tmp") / f"validators-bench-{args.runs}"
    shutil.rmtree(workdir, ignore_errors=True)
    print(f"стенд: {workdir} ({args.runs} прогонов)")
    build_fixture(workdir, args.runs)
    actual = len([p for p in (workdir / "runs/2026").glob("RUN-*") if p.is_dir()])
    print(f"прогонов в стенде: {actual}\n")

    measure("full (холодный кэш)", workdir, "--full")
    measure("fast (всё из кэша)", workdir)
    victim = workdir / f"runs/2026/RUN-{actual:04d}/outputs"
    target = next(iter(sorted(victim.rglob("*.md"))))
    target.write_text(target.read_text(encoding="utf-8") + "\n<!-- bench -->\n", encoding="utf-8")
    measure("fast (правка прогона)", workdir)

    if not args.keep:
        shutil.rmtree(workdir, ignore_errors=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
