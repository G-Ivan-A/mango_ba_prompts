#!/usr/bin/env python3
"""Юнит-тесты двух нетривиальных функций синка (issue #265).

Проверяются ровно те места, где ручной перенос ошибался:
* `rewrite_link` — куда ведёт ссылка Хаба после переноса в спицу;
* `strip_code` — что валидатор не принимает синтаксический пример за адрес.

Запуск: `python3 experiments/test_sync_link_rewrite.py`
"""

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from sync_from_hub import SyncError, rewrite_link  # noqa: E402
from validate_issue_265_hub_sync import strip_code  # noqa: E402

SHA = "3bfa4103c9efbbd59bc951814884920e406982e2"
HUB_DIR = REPO_ROOT  # для этих кейсов важны только существование/отсутствие цели


class RewriteLinkTest(unittest.TestCase):
    def test_synced_target_becomes_local_relative_path(self):
        # glossary.md -> standards/GLOSSARY.md, цель ai-rules/ тоже перенесена
        self.assertEqual(
            rewrite_link("standards/glossary.md", "../ai-rules/agent-work-rules.md", SHA, HUB_DIR),
            "../ai-rules/agent-work-rules.md",
        )

    def test_synced_target_keeps_anchor(self):
        self.assertEqual(
            rewrite_link("ai-rules/README.md", "../standards/glossary.md#термины", SHA, HUB_DIR),
            "../standards/GLOSSARY.md#термины",
        )

    def test_hub_only_file_becomes_pinned_blob_permalink(self):
        # README.md существует в корне и не входит в манифест -> permalink на SHA
        self.assertEqual(
            rewrite_link("standards/glossary.md", "../README.md", SHA, HUB_DIR),
            f"https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/{SHA}/README.md",
        )

    def test_hub_only_directory_becomes_tree_permalink(self):
        self.assertEqual(
            rewrite_link("standards/glossary.md", "../patterns/", SHA, HUB_DIR),
            f"https://github.com/G-Ivan-A/hybrid-Intelligence-lab/tree/{SHA}/patterns",
        )

    def test_target_missing_in_hub_stops_the_sync(self):
        # Именно этот класс дефекта дал 23 битые ссылки в скопированном глоссарии.
        with self.assertRaises(SyncError):
            rewrite_link("standards/glossary.md", "../CONCEPT.md", SHA, HUB_DIR)

    def test_pure_anchor_is_left_untouched(self):
        self.assertEqual(rewrite_link("ai-rules/README.md", "#граница", SHA, HUB_DIR), "#граница")


class StripCodeTest(unittest.TestCase):
    def test_inline_code_is_masked_and_line_numbers_kept(self):
        text = "первая\nформат: `[KB: <s>](kb/<path>)` — пример\nтретья"
        out = strip_code(text)
        self.assertEqual(len(out.splitlines()), 3)
        self.assertNotIn("kb/<path>", out)
        self.assertIn("формат:", out)

    def test_fenced_block_is_masked(self):
        text = "до\n```markdown\n[Глоссарий](standards/GLOSSARY.md)\n```\nпосле"
        out = strip_code(text)
        self.assertNotIn("standards/GLOSSARY.md", out)
        self.assertEqual(len(out.splitlines()), 5)

    def test_real_link_survives(self):
        text = "см. [карту](pr-ops/artifact-map.md)"
        self.assertIn("pr-ops/artifact-map.md", strip_code(text))


if __name__ == "__main__":
    unittest.main(verbosity=2)
