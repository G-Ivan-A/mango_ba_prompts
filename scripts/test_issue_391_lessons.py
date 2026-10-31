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


class LessonTests(unittest.TestCase):
    def test_only_additions_and_untouched_other_prompts(self):
        baseline = json.loads((ROOT / 'experiments/issue_391/prompt-baseline.json').read_text())
        for filename, expected_hash in baseline.items():
            with self.subTest(filename=filename):
                data = (ROOT / filename).read_bytes()
                # Issue 395 adds a bounded retrieval/fallback block. Its own
                # regression compares the remaining bytes against a new baseline.
                data = re.sub(rb'\n<!-- issue-395: runtime-fallback -->\n.*?<!-- /issue-395: runtime-fallback -->\n', b'', data, flags=re.S)
                # Issue 411 appends a generated run-lessons block and bumps version.
                data = re.sub(rb'\n<!-- issue-411: run-lessons -->\n.*?<!-- /issue-411: run-lessons -->\n', b'', data, flags=re.S)
                if Path(filename).name.startswith('bcreq-'):
                    data = data.replace(b'version: 0.2\nupdated: 2026-10-31\n', b'version: 0.1\nupdated: 2026-10-24\n', 1)
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
