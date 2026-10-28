"""Regression for phased chat exports used by the issue 397 retrospective."""
import importlib.util
import json
from pathlib import Path
import re
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'experiments/issue_397'
REPORT = ROOT / 'docs/analysis/2026-10-28-bcreq-evolution-failure-analysis.md'
spec = importlib.util.spec_from_file_location('issue397_extract', ROOT / 'experiments/issue_397/extract.py')
extractor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(extractor)


class ExportTests(unittest.TestCase):
    def test_answer_phase_is_not_lost_when_content_is_empty(self):
        message = {'content': '', 'content_list': [
            {'phase': 'thinking_summary', 'content': 'not the published answer'},
            {'phase': 'answer', 'content': 'A documented answer.'},
        ]}
        self.assertEqual(extractor.answer_text(message), 'A documented answer.')

    def test_plain_user_content_and_multiple_answer_blocks(self):
        self.assertEqual(extractor.answer_text({'content': None, 'content_list': None}), '')
        self.assertEqual(extractor.answer_text({'content': 'Founder requirement'}), 'Founder requirement')
        self.assertEqual(extractor.answer_text({'content': '', 'content_list': [
            {'phase': 'answer', 'content': 'First'}, {'phase': 'answer', 'content': 'Second'},
        ]}), 'First\n\nSecond')


class SafeguardDesignTests(unittest.TestCase):
    def test_counterfactuals_include_failures_and_permitted_work(self):
        spec = importlib.util.spec_from_file_location('issue397_replay', ROOT / 'experiments/issue_397/replay.py')
        replay = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(replay)
        cases = json.loads((ROOT / 'experiments/issue_397/replay-cases.json').read_text())
        self.assertEqual(len({case['id'] for case in cases}), len(cases))
        self.assertTrue({'continue', 'block_disputed', 'execute_override', 'block_release'} <=
                        {case['expected'] for case in cases})
        for case in cases:
            with self.subTest(case=case['id']):
                self.assertEqual(replay.decide(case['input']), case['expected'])

    def test_every_quote_has_export_provenance_and_report_reference(self):
        evidence = json.loads((ROOT / 'experiments/issue_397/evidence.json').read_text())
        keys = [row['key'] for row in evidence['entries']]
        self.assertEqual(len(set(keys)), len(keys))
        for row in evidence['entries']:
            self.assertIn(row['chat'], evidence['exports'])
            self.assertTrue(row['visible'])
            self.assertTrue(row['quotes'])
            self.assertEqual(len(row['answer_sha256']), 64)
            self.assertIn(f"[{row['key']}][{row['key']}]", REPORT.read_text())

    def test_report_has_complete_requirement_and_source_registers(self):
        report = REPORT.read_text()
        self.assertEqual(set(re.findall(r'^\| (T\d+) \|', report, re.M)),
                         {f'T{n:02d}' for n in range(1, 33)})
        used = set(re.findall(r'\]\[([^\]]+)\]', report))
        refs = dict(re.findall(r'^\[([^\]]+)\]: (\S+)$', report, re.M))
        self.assertEqual(used, set(refs))
        for key, url in refs.items():
            with self.subTest(source=key):
                self.assertTrue(url.startswith('https://'))
                if '/blob/' in url and '/konard/' not in url:
                    self.assertRegex(url, r'/blob/[0-9a-f]{40}/')

    def test_markdown_quotes_match_exact_json_except_trailing_whitespace(self):
        evidence = json.loads((BASE / 'evidence.json').read_text())
        markdown = (BASE / 'evidence.md').read_text()
        expected = []
        for entry in evidence['entries']:
            for quote in entry['quotes']:
                expected.extend('> ' + line.rstrip() if line.rstrip() else '>'
                                for line in quote.splitlines())
        actual = [line for line in markdown.splitlines() if line.startswith('>')]
        self.assertEqual(actual, expected)
        self.assertTrue(all(line == line.rstrip() for line in markdown.splitlines()))

    def test_recorded_replay_results_match_the_reviewed_inputs(self):
        cases = json.loads((BASE / 'replay-cases.json').read_text())
        result = json.loads((BASE / 'replay-results.json').read_text())
        self.assertEqual(len(cases), 23)
        self.assertEqual([r['id'] for r in result['cases']], [c['id'] for c in cases])
        for case, row in zip(cases, result['cases']):
            self.assertEqual(row['actual'], case['expected'])
            self.assertEqual(row['expected'], case['expected'])
            self.assertEqual(row['basis'], case['basis'])
            self.assertEqual(row['hypotheses'], case['hypotheses'])

    def test_run_counts_are_recomputed_from_the_source_artifacts(self):
        from collections import Counter
        inventory = json.loads((BASE / 'run-inventory.json').read_text())
        for row in inventory['runs']:
            outputs = ROOT / 'runs/2026' / row['run'] / 'outputs'
            data = json.loads((outputs / 'golden-set-candidates.json').read_text())
            cases = [c for group in data['sets'] for c in group['cases']]
            criteria = set(re.findall(r'\bSC-\d+\b', (outputs / 'success-criteria.md').read_text()))
            self.assertEqual(row['cases'], len(cases))
            self.assertEqual(row['sets'], len(data['sets']))
            self.assertEqual(row['success_criteria'], len(criteria))
            self.assertEqual(row['status'], data['status'])
            self.assertEqual(row['confirmed_by'], dict(Counter(c['confirmed_by'] for c in cases)))
            self.assertEqual(row['kinds'], dict(Counter(c['kind'] for c in cases)))
        self.assertEqual(inventory['total_cases'], sum(r['cases'] for r in inventory['runs']))
        self.assertEqual(inventory['total_success_criteria'],
                         sum(r['success_criteria'] for r in inventory['runs']))


class PromptProbeTests(unittest.TestCase):
    def test_body_normalization_preserves_substantive_text(self):
        spec = importlib.util.spec_from_file_location('issue397_probe', BASE / 'probe.py')
        probe = importlib.util.module_from_spec(spec)
        with patch.dict(sys.modules, {'extract': extractor}):
            spec.loader.exec_module(probe)
        self.assertEqual(probe.body('<!-- mango-bcreq-test -->\r\n---\r\nversion: 1\r\n---\r\nA  B\r\n'), 'A  B')
        self.assertNotEqual(probe.body('A  B'), probe.body('A B'))
        self.assertNotEqual(probe.body('A\nB'), probe.body('A B'))


if __name__ == '__main__':
    unittest.main()
