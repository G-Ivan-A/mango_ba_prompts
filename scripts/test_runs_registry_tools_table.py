#!/usr/bin/env python3
"""Регрессионные тесты таблицы «Локальные инструменты воспроизводимости».

Зачем
-----
Раздел `runs/README.md` перечисляет локальные конвертеры и прогоны, в которых
они применялись. Таблица правится почти в каждом PR с новым прогоном, поэтому
при параллельной работе туда попадали расходящиеся копии одной строки: после
merge-коммитов `6a5debe9` (issue #281) и `1d2c086b` (issue #279) строка для
`scripts/chat_export_to_markdown.py` существовала дважды — в одной копии был
`RUN-0016`, в другой нет. Читатель реестра не мог узнать, какая копия верна.

Списки прогонов здесь не хардкодятся (issue #299): истина наблюдается на диске —
прогон применял инструмент, если ссылается на него хоть одним своим файлом.

Запуск: ``python3 scripts/test_runs_registry_tools_table.py``
"""

from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "runs" / "README.md"

#: Строка таблицы: `| [`путь/к/инструменту.py`](...) | Назначение |`.
TOOL_ROW = re.compile(r"^\|\s*\[`([^`]+\.(?:py|mjs|sh))`\]")
RUN_REF = re.compile(r"RUN-\d{4}")


def tool_rows() -> list[tuple[str, str]]:
    """Пары «путь инструмента → текст строки» из реестра, в порядке файла."""
    rows: list[tuple[str, str]] = []
    for line in REGISTRY.read_text(encoding="utf-8").splitlines():
        match = TOOL_ROW.match(line)
        if match:
            rows.append((match.group(1), line))
    return rows


def runs_referencing(tool: str) -> set[str]:
    """Прогоны, чьи файлы упоминают инструмент по имени."""
    name = Path(tool).name
    found: set[str] = set()
    for run_dir in (ROOT / "runs").glob("*/RUN-*"):
        if not run_dir.is_dir():
            continue
        for path in run_dir.rglob("*.md"):
            if name in path.read_text(encoding="utf-8", errors="ignore"):
                found.add(run_dir.name)
                break
    return found


class ToolsTableTest(unittest.TestCase):
    def test_registry_section_is_present(self) -> None:
        rows = tool_rows()
        self.assertTrue(rows, "в runs/README.md не найдено строк с инструментами")

    def test_each_tool_appears_once(self) -> None:
        """Дубль строки — это две версии истины про один инструмент."""
        seen: dict[str, str] = {}
        for tool, line in tool_rows():
            self.assertNotIn(
                tool,
                seen,
                f"{tool}: строка в таблице инструментов встречается дважды",
            )
            seen[tool] = line

    def test_tool_files_exist(self) -> None:
        for tool, _ in tool_rows():
            self.assertTrue((ROOT / tool).exists(), f"{tool}: файла нет в репозитории")

    def test_listed_runs_actually_use_the_tool(self) -> None:
        """Перечисленный прогон обязан ссылаться на инструмент.

        Обратное направление не проверяется: строка вправе описывать диапазон
        (`RUN-0030`—`RUN-0054`) короче, чем полный список упоминаний.
        """
        for tool, line in tool_rows():
            listed = set(RUN_REF.findall(line))
            if not listed:
                continue
            actual = runs_referencing(tool)
            self.assertEqual(
                listed - actual,
                set(),
                f"{tool}: прогоны перечислены в реестре, но не ссылаются на инструмент",
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
