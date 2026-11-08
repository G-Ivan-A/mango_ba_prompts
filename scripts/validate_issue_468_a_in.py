#!/usr/bin/env python3
"""Small RFC/site regression checks; no model calls or product reassessment."""
import importlib.util
import json
import re
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT/'experiments/issue_468'
def module(name, path):
    spec=importlib.util.spec_from_file_location(name, path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
class AINAcceptance(unittest.TestCase):
    def setUp(self):
        self.route=json.loads((ROOT/'docs/ba-processes/bcreq-a-in-route.json').read_text())
        self.rfc=(ROOT/'docs/rfc/2026-11-a-in-decomposition.md').read_text()
    def test_contracts_and_reachable_returns(self):
        steps=self.route['steps'];ids={s['id'] for s in steps}
        self.assertEqual(len(steps),24);self.assertEqual(len(ids),24)
        self.assertEqual(self.route['status'],'accepted');self.assertFalse(self.route['runtime'])
        classes={x['id'] for x in json.loads((ROOT/'standards/bcreq-manual-classes/catalog.json').read_text())['classes']}
        for i,s in enumerate(steps,1):
            self.assertEqual(s['id'],f'AIN-{i:02}')
            for field in ('input','output','why','checks','granularity','forbidden','review'):
                self.assertTrue(s[field],(s['id'],field))
            self.assertTrue(set(s['operation'].split(', ')) <= classes)
            self.assertTrue(set(s['returns']+[s['failure']]) <= ids)
            self.assertIn('БА CBAP (ИТ/телеком)',s['review'])
        self.assertEqual(steps[20]['next'],'AIN-22')
        self.assertIn('AIN-07',steps[9]['returns'])
        self.assertIn('AIN-06',steps[18]['returns'])
        self.assertTrue(self.route['receipt']['required_every_step'])
        self.assertFalse(self.route['navigation']['visible'])
        self.assertTrue(self.route['navigation']['loop_aware'])
        startup=self.route['startup_rules']
        self.assertTrue(startup['must_read_before_intake'])
        self.assertEqual(startup['unavailable'],'blocked')
        self.assertEqual(startup['application_sources_steps'],['AIN-08','AIN-09'])
        self.assertIn('blocked до AIN-02',steps[0]['checks'])
        self.assertEqual(steps[-1]['next'],'A-CORE или CS по решению БА')
        self.assertNotIn('A-ARCH',steps[-1]['why'])
    def test_rfc_table_and_links(self):
        table=module('ain_table',HERE/'route_table.py').table()
        self.assertIn(table,self.rfc)
        self.assertLess(self.rfc.index(table),self.rfc.index('## 1.'))
        for target in re.findall(r'\]\(([^ )]+)\)',self.rfc):
            if '://' not in target and not target.startswith('#'):
                self.assertTrue((ROOT/'docs/rfc'/target.split('#')[0]).exists(),target)
        for token in ('40–58','70–98','102–138','Р-AIN-1','Р-AIN-2','CBAP','Self-RAG','W3C','IREB'):
            self.assertIn(token,self.rfc)
    def test_gate_counterexamples(self):
        check=module('ain_contract_check',HERE/'contract_check.py').violations
        cases=json.loads((HERE/'gate-cases.json').read_text())
        self.assertEqual(len(cases),16)
        for case in cases:
            with self.subTest(case=case['id']):
                self.assertEqual(check(case['state']),case['expected'])
        # Reported old behaviour must fail the admission check, independently
        # of how a future prompt chooses to implement it.
        self.assertTrue(check(cases[1]['state']))
    def test_draft_panel_and_reproducible_overlay(self):
        overlay=module('ain_site',HERE/'site_a_in.py')
        html=(ROOT/'site/index.html').read_text()
        self.assertEqual(html.count('id="a-in-proposal"'),1)
        self.assertNotIn('data-ain-step=', html)
        self.assertEqual(html.count('class="process-help"'), 1)
        self.assertEqual(overlay.apply(html),html)
        stripped=html[:html.index(overlay.START)]+html[html.index(overlay.END)+len(overlay.END)+1:]
        self.assertEqual(overlay.apply(stripped),html)
        panel=overlay.panel()
        self.assertNotIn('<table',panel);self.assertNotIn('data-ain-copy=',panel)
        self.assertNotIn('<details',panel)
        self.assertLess(html.index('id="process-help"'), html.index('id="a-in-proposal"'))
        self.assertIn('промпты draft, эффективность не измерена',panel)
        for id in ('process-help','process-tabs','standards-bcreq','standards-ttz','standards-industry'):
            self.assertIn(f'id="{id}"',html)
    def test_source_privacy_and_release(self):
        records=json.loads((HERE/'source-manifest.json').read_text())
        for record in records:
            self.assertRegex(record['sha256'],r'^[0-9a-f]{64}$')
            self.assertFalse(record['raw_committed'])
        self.assertFalse(list(HERE.glob('*.pdf')))
        self.assertFalse((HERE/'issue.json').exists())
        self.assertEqual(json.loads((ROOT/'site/data/stats.json').read_text())['siteVersion']['version'],'2.8.4')
        self.assertIn('BL-179',(ROOT/'pr-ops/BACKLOG.md').read_text())
        self.assertIn('BL-180',(ROOT/'pr-ops/backlog-ba-model.md').read_text())
if __name__=='__main__':
    unittest.main()
