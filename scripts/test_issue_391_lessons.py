"""Verify additive lessons and preserve every non-BCREQ prompt byte for byte."""
from pathlib import Path
import hashlib
import importlib.util
import json
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
                addition = changes.ADDITIONS.get(Path(filename).name)
                if addition:
                    encoded = addition[1].encode()
                    self.assertEqual(data.count(encoded), 1, 'source-traced addition must occur exactly once')
                    data = data.replace(encoded, b'', 1)
                self.assertEqual(hashlib.sha256(data).hexdigest(), expected_hash)


if __name__ == '__main__':
    unittest.main()
