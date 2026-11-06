#!/usr/bin/env python3
"""Small, synthetic export regressions and evidence-preservation checks."""
import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / 'experiments/issue_468'
spec = importlib.util.spec_from_file_location('dialogue', HERE / 'extract_dialogue.py')
dialogue = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dialogue)


def exported(texts):
    messages = []
    for i, text in enumerate(texts):
        messages.append({'id': str(i), 'parentId': str(i - 1) if i else None,
                         'role': 'user', 'content': text})
    return [{'chat': {'messages': messages, 'history': {
        'currentId': messages[-1]['id'],
        'messages': {m['id']: m for m in messages}}}}]


class ExportComparison(unittest.TestCase):
    def load(self, data):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'fixture.json'
            path.write_text(json.dumps(data))
            return dialogue.load_export(path)

    def test_append_and_metadata_only_change(self):
        old = exported(['first', 'second'])
        new = exported(['first', 'second', 'third'])
        new[0]['chat']['messages'][0]['timestamp'] = 99
        report = dialogue.compare(self.load(old), self.load(new))
        self.assertEqual(report['common_visible_prefix'], 2)
        self.assertEqual(report['added_indices'], [2])
        self.assertEqual(report['changed_indices'], [])
        self.assertNotIn('third', json.dumps(report))

    def test_edit_inside_shared_prefix_is_not_lost(self):
        old = self.load(exported(['first', 'second']))
        new = self.load(exported(['edited', 'second', 'third']))
        report = dialogue.compare(old, new)
        self.assertEqual(report['common_visible_prefix'], 0)
        self.assertEqual(report['changed_indices'], [{'before': 0, 'after': 0}])
        self.assertEqual([entry['index'] for entry in report['delta']], [0, 2])

    def test_removal_and_reordering(self):
        old = self.load(exported(['a', 'b', 'c']))
        new = exported(['c', 'a'])
        messages = new[0]['chat']['messages']
        messages[0].update(id='2', parentId=None)
        messages[1].update(id='0', parentId='2')
        new[0]['chat']['history'] = {
            'currentId': '0', 'messages': {m['id']: m for m in messages}}
        report = dialogue.compare(old, self.load(new))
        self.assertEqual(report['removed_indices'], [1])
        self.assertEqual(report['moved_indices'],
                         [{'before': 2, 'after': 0}, {'before': 0, 'after': 1}])

    def test_hidden_reasoning_and_inactive_branches_are_excluded(self):
        data = exported(['visible'])
        message = data[0]['chat']['messages'][0]
        message.update(role='assistant', content='PRIVATE REASONING', content_list=[
            {'phase': 'thinking', 'content': 'PRIVATE REASONING'},
            {'phase': 'answer', 'content': 'visible'}])
        data[0]['chat']['history']['messages']['inactive'] = {
            'role': 'assistant', 'content': 'INACTIVE TEXT'}
        loaded = self.load(data)
        self.assertEqual(loaded['texts'], ['visible'])
        self.assertEqual(loaded['inactive_history_count'], 1)
        message.pop('content_list')
        self.assertEqual(self.load(data)['texts'], [''])

    def test_invalid_active_branch_is_rejected(self):
        valid = exported(['a', 'b'])
        variants = []
        for change in ('duplicate', 'parent', 'current', 'history'):
            data = copy.deepcopy(valid)
            chat = data[0]['chat']
            if change == 'duplicate':
                chat['messages'][1]['id'] = '0'
            elif change == 'parent':
                chat['messages'][1]['parentId'] = None
            elif change == 'current':
                chat['history']['currentId'] = '0'
            else:
                chat['history']['messages'].pop('1')
            variants.append(data)
        for data in variants:
            with self.subTest(data=data), self.assertRaises(ValueError):
                self.load(data)

    def test_cli_refuses_public_extraction(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'source.json'
            source.write_text(json.dumps(exported(['synthetic confidential text'])))
            report = Path(directory) / 'report.json'
            public = Path(directory) / 'public'
            result = subprocess.run(
                [sys.executable, str(HERE / 'extract_dialogue.py'), str(source), str(source),
                 '--report', str(report), '--private-output', str(public)],
                capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertIn('ignored issue_468/private', result.stderr)
            self.assertFalse(public.exists())
            self.assertFalse(report.exists())


class PracticePreservation(unittest.TestCase):
    def test_review_counterexamples(self):
        spec = importlib.util.spec_from_file_location('review', HERE / 'contract_check.py')
        review = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(review)
        cases = json.loads((HERE / 'review-cases.json').read_text())
        self.assertEqual({c['id'].split('-')[0] for c in cases},
                         {f'S{i:02}' for i in range(17, 28)})
        self.assertEqual(len({c['id'] for c in cases}), len(cases))
        for case in cases:
            with self.subTest(case=case['id']):
                self.assertEqual(review.review_violations(case['state']), case['expected'])

    def test_stop_and_critical_review_are_explicit_contracts(self):
        route = json.loads((ROOT / 'docs/ba-processes/bcreq-a-in-route.json').read_text())
        interaction = route['interaction']
        self.assertFalse(interaction['advance_while_paused'])
        self.assertFalse(interaction['future_comment_authorizes_execution'])
        self.assertTrue(interaction['reuse_accepted_inputs'])
        self.assertEqual(interaction['review_outcomes'], ['accept', 'partial', 'reject'])
        self.assertEqual(interaction['public_transition_sentences'], 2)
        self.assertTrue(route['documentation_handover']['constitution_before_agreement'])
        self.assertFalse(route['documentation_handover']['checklist_is_all_functional'])
        self.assertFalse(route['documentation_handover']['functional_item_heading'])
        self.assertFalse(route['analysis_preservation']['silent_removal'])

    def test_delta_coverage_and_traceability(self):
        report = json.loads((HERE / 'dialogue-delta.json').read_text())
        ledger = json.loads((HERE / 'practice-ledger.json').read_text())
        self.assertEqual(report['common_visible_prefix'], 28)
        self.assertEqual(report['sources']['after']['active_count'], 66)
        self.assertEqual(report['added_indices'], list(range(28, 66)))
        self.assertFalse(report['changed_indices'] + report['removed_indices'])
        self.assertEqual(report['sources']['after']['sha256'], ledger['source_sha256'])
        practices = ledger['practices']
        ids = {p['id'] for p in practices}
        self.assertEqual(len(ids), len(practices))
        self.assertEqual({i for p in practices for i in p['messages']}, set(range(28, 66)))
        route = json.loads((ROOT / 'docs/ba-processes/bcreq-a-in-route.json').read_text())
        steps = {step['id']: step for step in route['steps']}
        for practice in practices:
            for field in ('observation', 'rule', 'risk', 'assessment', 'verification'):
                self.assertTrue(practice[field], (practice['id'], field))
            self.assertTrue(practice['steps'])
            for step in practice['steps']:
                self.assertIn(practice['id'], steps[step]['practice_ids'])
        self.assertEqual({c for p in practices for c in p['categories']},
                         {'interaction', 'documentation', 'risk', 'agreement'})
        rfc = (ROOT / 'docs/rfc/2026-11-a-in-decomposition.md').read_text()
        for practice in practices:
            self.assertIn(practice['id'], rfc)
        for label in ('Т-11', 'Т-12', 'Т-13', 'Framework Method', '2.6.'):
            self.assertIn(label, rfc)

    def test_existing_contracts_and_regressions_are_preserved(self):
        baseline = json.loads((HERE / 'preservation-baseline.json').read_text())
        route = json.loads((ROOT / 'docs/ba-processes/bcreq-a-in-route.json').read_text())
        self.assertEqual(len(route['steps']), len(baseline['steps']))
        for original, current in zip(baseline['steps'], route['steps']):
            for field, value in original.items():
                if field in ('checks', 'forbidden'):
                    self.assertTrue(current[field].startswith(value), (current['id'], field))
                else:
                    self.assertEqual(current[field], value, (current['id'], field))
        for field, value in baseline['common'].items():
            self.assertEqual(route[field], value, field)
        cases = (HERE / 'gate-cases.json').read_bytes()
        self.assertEqual(dialogue.digest(cases), baseline['gate_cases_sha256'])
        rfc = (ROOT / 'docs/rfc/2026-11-a-in-decomposition.md').read_text()
        for practice in baseline['legacy_practices']:
            self.assertIn(practice, rfc)
        for index in range(1, 17):
            self.assertIn(f'| S{index:02} ', rfc)


if __name__ == '__main__':
    unittest.main()
