#!/usr/bin/env python3
"""Сторож среза А (issue #456): поле ``ai-generated`` не возвращается в очищенные файлы.

Список — ``experiments/issue_456/slice-a-files.txt``. Файл, которого больше нет на
месте (перенос или архив по BL-222, BL-223), не считается нарушением; проверяется
только то, что лежит по записанному пути. Остальной долг поля учтён в S-003.
"""

import re
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLICE = ROOT / "experiments" / "issue_456" / "slice-a-files.txt"
#: Размер списка на момент исполнения; уменьшение незаметно ослабило бы сторож.
SLICE_SIZE = 65
FRONTMATTER = re.compile(r"---\n.*?\n---\n", re.S)
FIELD = re.compile(r"^ai-generated:", re.M)


def has_field(path: Path) -> bool:
    match = FRONTMATTER.match(path.read_text(encoding="utf-8"))
    return bool(match and FIELD.search(match.group(0)))


class SliceA(unittest.TestCase):
    def test_list_is_not_weakened(self):
        self.assertEqual(len(set(SLICE.read_text(encoding="utf-8").split())), SLICE_SIZE)

    def test_field_does_not_return(self):
        files = (ROOT / name for name in SLICE.read_text(encoding="utf-8").split())
        self.assertEqual([str(p.relative_to(ROOT)) for p in files if p.exists() and has_field(p)], [])

    def test_guard_detects_field_only_in_frontmatter(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "doc.md"
            path.write_text("---\nstatus: draft\nai-generated: true\n---\n", encoding="utf-8")
            self.assertTrue(has_field(path))
            path.write_text("---\nstatus: draft\n---\n\nai-generated: пример в тексте\n", encoding="utf-8")
            self.assertFalse(has_field(path))


if __name__ == "__main__":
    unittest.main()
