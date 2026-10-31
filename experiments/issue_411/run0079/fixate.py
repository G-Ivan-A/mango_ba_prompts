#!/usr/bin/env python3
"""RUN-0079: перенос входов, выходов и логов из рабочего каталога в runs/ (issue #411).

Копирует только данные прогона. Промпты A и B не копируются: они
воспроизводятся из git по ссылкам в mapping.json (см. inputs/README.md).

Использование:
    python3 experiments/issue_411/run0079/fixate.py WORKDIR
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

from prepare import ROOT

RUN = ROOT / "runs/2026/RUN-0079"


FRONTMATTER = "---\nstatus: draft\nversion: 0.1\nupdated: 2026-10-31\ntemperature: 0.1\n---\n\n"


def copy_md(source: Path, target: Path) -> None:
    target.write_text(FRONTMATTER + source.read_text(encoding="utf-8"), encoding="utf-8")


def merged(paths: list[Path]) -> list:
    items: list = []
    for path in paths:
        items.extend(json.loads(path.read_text(encoding="utf-8")))
    return sorted(items, key=lambda item: item["case"])


def dump(path: Path, data) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    work = Path(sys.argv[1]).resolve()
    for sub in ("inputs", "outputs", "logs", "feedback"):
        (RUN / sub).mkdir(parents=True, exist_ok=True)
    for batch in (1, 2):
        copy_md(work / f"exec/cases-batch{batch}.md", RUN / f"inputs/cases-batch{batch}.md")
        copy_md(work / f"judge/judge-batch{batch}.md", RUN / f"logs/judge-input-batch{batch}.md")
    shutil.copyfile(work / "mapping.json", RUN / "inputs/mapping.json")
    copy_md(work / "judge/rules.md", RUN / "logs/judge-rules.md")
    for version in ("A", "B"):
        dump(RUN / f"outputs/executor-{version}.json", merged(sorted((work / "out").glob(f"{version}-batch*.json"))))
    dump(RUN / "outputs/judge-scores.json", merged(sorted((work / "judge").glob("out-batch*.json"))))
    shutil.copyfile(work / "judge-key.json", RUN / "outputs/judge-key.json")
    shutil.copyfile(work / "metrics.json", RUN / "outputs/metrics.json")
    print(f"fixated into {RUN.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
