#!/usr/bin/env python3
"""Exercise the actual generator on CRLF archives without writes or a copied repo."""
from pathlib import Path
import os
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]


class Generation(unittest.TestCase):
    def run_node(self, *args, **env):
        return subprocess.run(
            ['node', *args], cwd=ROOT, env={**os.environ, **env},
            capture_output=True, text=True, timeout=30,
        )

    def test_frontmatter_and_copy_boundaries(self):
        result = self.run_node('--test', 'experiments/issue_480/frontmatter.test.mjs')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_full_crlf_generation_preserves_catalog_and_route(self):
        result = self.run_node('experiments/issue_480/probe-line-endings.mjs')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('Generated 57 prompts', result.stdout)

    def test_invalid_operation_still_blocks_with_actionable_diagnostic(self):
        result = self.run_node('experiments/issue_480/probe-line-endings.mjs', MANGO_PROBE_VARIANT='invalid')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('bcreq-context-understanding-stepwise.md', result.stderr)
        self.assertIn('frontmatter.operation', result.stderr)
        self.assertIn('"__invalid__"', result.stderr)


if __name__ == '__main__':
    unittest.main()
