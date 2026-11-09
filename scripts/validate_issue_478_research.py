#!/usr/bin/env python3
"""Offline provenance integrity and deploy-candidate preservation for #478.

Checks evidence structure and attribution, not the truth or future freshness
of a remote page. No network, LLM, build, or third-party dependency.
"""
import hashlib
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / 'experiments/issue_478'


def normalized(data):
    if isinstance(data, dict):
        return {k: normalized(v) for k, v in data.items() if k != 'generatedAt'}
    if isinstance(data, list):
        return [normalized(v) for v in data]
    return data


class Research(unittest.TestCase):
    def test_each_assertion_has_auditable_provenance(self):
        evidence = json.loads((HERE / 'evidence.json').read_text())
        sources = evidence['sources']
        by_id = {s['id']: s for s in sources}
        self.assertEqual(len(by_id), len(sources))
        self.assertRegex(evidence['baseline']['sha'], r'^[0-9a-f]{40}$')
        for s in sources:
            with self.subTest(source=s['id']):
                for key in ('url', 'publisher', 'title', 'locator', 'quote', 'claim', 'limits', 'origin'):
                    self.assertTrue(s[key], key)
                self.assertTrue(s['url'].startswith('https://'))
                self.assertIn(s['status'], ('VERIFIED', 'PARTIAL', 'CONFLICT'))
                self.assertIn('published_at', s)
                self.assertIn('event_date', s)
                # Missing dates remain unknown; do not substitute retrieval time.
                if s['published_at']:
                    self.assertRegex(s['published_at'], r'^\d{4}-\d{2}-\d{2}$')
        people = evidence['people']
        self.assertEqual(len(people), 10)
        self.assertEqual(sum(p['name_status'] == 'VERIFIED' for p in people), 9)
        for p in people:
            with self.subTest(person=p['id']):
                source = by_id[p['name_source']]
                self.assertIn(p['name'], source['quote'])
                if p['name_status'] == 'VERIFIED':
                    self.assertIn(source['access'], ('full_text', 'pdf_text'))
                    self.assertEqual(source['status'], 'VERIFIED')
                self.assertEqual(p['authority'], 'unknown')
                for ref in p['role_sources'] + p['mentions']:
                    self.assertIn(ref, by_id)
        self.assertEqual(by_id['N03']['access'], 'search_index')
        self.assertEqual(by_id['N03']['status'], 'CONFLICT')
        self.assertEqual(by_id['N12']['origin'], 'advertorial')
        self.assertEqual(by_id['N15']['event_date'], '2023-09')
        self.assertIsNone(by_id['N15']['published_at'])
        self.assertEqual({by_id[n]['status'] for n in ('N08', 'N09')}, {'CONFLICT'})
        # No copied personal contact fields; URLs are the only @-free contact data.
        self.assertFalse(re.search(r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}', json.dumps(evidence)))

    def test_prepared_site_preserves_merged_baseline(self):
        audit = json.loads((HERE / 'site-audit.json').read_text())
        self.assertEqual(audit['baseline_semantic_changes'], [])
        self.assertEqual(audit['live_version']['version'], '2.7.0')
        self.assertEqual(audit['candidate_version']['version'], '2.8.5')
        self.assertTrue(audit['catalogue_ids_preserved'])
        for name, record in audit['assets'].items():
            path = ROOT / name
            self.assertTrue(path.is_relative_to(ROOT / 'site'))
            body = path.read_bytes()
            # Generator timestamps are variable, content must remain byte-equivalent
            # after dropping that field, as during manifest generation.
            if path.suffix == '.json':
                content = json.dumps(normalized(json.loads(body)), ensure_ascii=False,
                                     sort_keys=True, separators=(',', ':')).encode()
                self.assertEqual(hashlib.sha256(content).hexdigest(), record['normalized_sha256'], name)
            else:
                self.assertEqual(hashlib.sha256(body).hexdigest(), record['sha256'], name)
        stats = json.loads((ROOT / 'site/data/stats.json').read_text())
        self.assertEqual(stats['siteVersion'], audit['candidate_version'])
        kit = json.loads((ROOT / 'site/data/a-in-kit.json').read_text())
        self.assertEqual(len(kit['steps']), 24)
        self.assertFalse(kit['measured'])
        self.assertFalse((ROOT / 'site/reports/run-0060').exists())


if __name__ == '__main__':
    unittest.main()
