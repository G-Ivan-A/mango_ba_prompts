#!/usr/bin/env python3
"""Regression contract for the BCREQ-only publication boundary (issue 391)."""
import json
from pathlib import Path
import re
import unittest
import subprocess
import hashlib

ROOT = Path(__file__).resolve().parents[1]


class PublicationTests(unittest.TestCase):
    def test_catalog_contains_all_and_only_bcreq_sources(self):
        data = json.loads((ROOT / 'site/data/prompts.json').read_text())
        expected = {str(p.relative_to(ROOT)) for p in (ROOT / 'prompts').glob('bcreq-*.md')}
        actual = {p['sourcePath'] for p in data['prompts']}
        self.assertEqual(actual, expected)
        self.assertEqual(len(data['prompts']), len(expected))
        self.assertTrue(all(p['family'] == 'bcreq' and not p['archived'] for p in data['prompts']))
        self.assertEqual({f['id'] for f in data['filters']['families']}, {'bcreq'})
        for prompt in data['prompts']:
            self.assertEqual(prompt['content'], (ROOT / prompt['sourcePath']).read_text())

    def test_process_route_has_exactly_two_blocks(self):
        html = (ROOT / 'site/index.html').read_text()
        sections = re.findall(r'<section\b[^>]*data-page="processes"[^>]*>', html)
        self.assertEqual(len(sections), 2)

    def test_login_is_a_separate_page(self):
        self.assertTrue((ROOT / 'site/login.html').exists())

    def test_password_hash_preserves_case_and_whitespace(self):
        sample = 'Case-Sensitive'
        script = """import { hashPassword } from './scripts/set-site-password.mjs';
console.log(JSON.stringify(['Case-Sensitive', 'case-sensitive', ' Case-Sensitive', 'Case-Sensitive '].map(p => hashPassword('example-salt', p))));"""
        result = subprocess.run(['node', '--input-type=module', '-e', script], cwd=ROOT, check=True, capture_output=True, text=True)
        hashes = json.loads(result.stdout)
        self.assertEqual(hashes[0], hashlib.sha256(('example-salt' + sample).encode()).hexdigest())
        self.assertEqual(len(set(hashes)), 4)
        gate = (ROOT / 'site/gate.js').read_text()
        self.assertNotIn('.toUpperCase()', gate)
        self.assertNotIn('.trim()', gate)
        self.assertIn('entry.salt + input.value', gate)
        self.assertIn('https://g-ivan-a.github.io/mango_ba_prompts/', gate)
        self.assertIn('sessionStorage', gate)

    def test_login_has_only_one_password_input(self):
        html = (ROOT / 'site/login.html').read_text()
        self.assertEqual(len(re.findall(r'<input\b', html)), 1)
        self.assertIn('type="password"', html)


if __name__ == '__main__':
    unittest.main()
