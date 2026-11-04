"""Verify additive lessons and preserve every non-BCREQ prompt byte for byte."""
from pathlib import Path
import hashlib
import importlib.util
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('golden_changes', ROOT / 'experiments/issue_391/golden_changes.py')
changes = importlib.util.module_from_spec(spec)
spec.loader.exec_module(changes)
bl156a_spec = importlib.util.spec_from_file_location('bl156a_prompt_changes', ROOT / 'experiments/issue_444/bl156a_prompt_changes.py')
bl156a = importlib.util.module_from_spec(bl156a_spec)
bl156a_spec.loader.exec_module(bl156a)


class LessonTests(unittest.TestCase):
    def test_only_additions_and_untouched_other_prompts(self):
        baseline = json.loads((ROOT / 'experiments/issue_391/prompt-baseline.json').read_text())
        for filename, expected_hash in baseline.items():
            with self.subTest(filename=filename):
                data = (ROOT / filename).read_bytes()
                # Issue 444 (BL-156а): typed gates and pinned runtime links are
                # reverted first; every other byte must still match the baseline.
                data = bl156a.revert_bytes(filename, data)
                # Issue 395 adds a bounded retrieval/fallback block. Its own
                # regression compares the remaining bytes against a new baseline.
                data = re.sub(rb'\n<!-- issue-395: runtime-fallback -->\n.*?<!-- /issue-395: runtime-fallback -->\n', b'', data, flags=re.S)
                addition = changes.ADDITIONS.get(Path(filename).name)
                if addition:
                    encoded = addition[1].encode()
                    self.assertEqual(data.count(encoded), 1, 'source-traced addition must occur exactly once')
                    data = data.replace(encoded, b'', 1)
                # Issue 393 adds catalog metadata only; keep verifying all
                # original fields and the entire approved body byte for byte.
                if Path(filename).name.startswith('bcreq-'):
                    opening, metadata, body = data.split(b'---', 2)
                    metadata = re.sub(rb'^(?:operation|processes):[^\n]*\n', b'', metadata, flags=re.M)
                    data = b'---'.join([opening, metadata, body])
                self.assertEqual(hashlib.sha256(data).hexdigest(), expected_hash)


if __name__ == '__main__':
    unittest.main()
