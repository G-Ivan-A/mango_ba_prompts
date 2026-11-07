#!/usr/bin/env python3
"""Draft A-IN regression contracts, provenance counterexamples and copy parity.

No LLM calls. A passing test cannot certify tone, judgement or model obedience.
"""
import importlib.util
import json
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def module(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT/path)
    result = importlib.util.module_from_spec(spec); spec.loader.exec_module(result)
    return result

class Execution(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.oracle = module('admission474', 'experiments/issue_474/admission.py')
        cls.kit = json.loads((ROOT/'site/data/a-in-kit.json').read_text())
        cls.route = json.loads((ROOT/'docs/ba-processes/bcreq-a-in-route.json').read_text())

    def valid(self):
        state = json.loads((ROOT/'experiments/issue_468/gate-cases.json').read_text())[0]['state']
        state.update(task_id='T', attempt='a1', route_version='0.3', snapshot_id='S', snapshot_version='r7',
                     current_step='AIN-22', execute_current=True, question_states=[])
        state['gate21'] = {k:state[k] for k in self.oracle.KEYS}
        state['gate21'].update(gate='AIN-21', decision='allow', actor_role='BA', actor='Reviewer',
                               date='2026-11-07', locator='chat/message-21', report_version='r1')
        return state

    def test_explicit_gate_and_separate_call_regression(self):
        state=self.valid(); self.assertEqual(self.oracle.violations(state), [])
        # #468's general eligibility check passed this case without an actual
        # gate decision. The new writing contract must refuse it.
        del state['gate21']
        self.assertEqual(self.oracle.legacy.violations(state), [])
        self.assertIn('explicit_ba_gate_missing', self.oracle.violations(state))
        for field in self.oracle.KEYS:
            state=self.valid();state['gate21'][field]='older'
            with self.subTest(field=field):
                self.assertIn('gate_version_mismatch', self.oracle.violations(state))
        for patch, expected in [({'execute_current':False},'separate_call_missing'),
                                ({'current_step':'AIN-21'},'separate_call_missing'),
                                ({'paused':True},'paused_execution'),
                                ({'question_states':['rework']},'questions_pending')]:
            state=self.valid();state.update(patch);self.assertIn(expected,self.oracle.violations(state))
        for decision in ('yes','pending','stop',''):
            state=self.valid();state['gate21']['decision']=decision
            self.assertIn('explicit_ba_gate_missing',self.oracle.violations(state))
        state=self.valid();state['gate21']['actor_role']='LLM'
        self.assertIn('explicit_ba_gate_missing',self.oracle.violations(state))

    def test_original_gate_counterexamples_still_block(self):
        cases=json.loads((ROOT/'experiments/issue_468/gate-cases.json').read_text())
        for case in cases:
            state=self.valid();state.update(case['state'])
            with self.subTest(case=case['id']):
                for expected in case['expected']:
                    self.assertIn(expected,self.oracle.violations(state))
                if not case['expected']:self.assertEqual(self.oracle.violations(state),[])

    def test_provenance_does_not_collapse_feasibility(self):
        # A verified negative source is compatible with 'no'; verification of
        # the quote alone cannot establish either positive or negative scope.
        base=dict(evidence_status='VERIFIED',feasibility='no',exact_scope=True,
                  evidence_ids=['E-1'],access='read',freshness='current',origin='knowledge')
        self.assertEqual(self.oracle.evidence_violations(base),[])
        for patch in ({'evidence_status':'CONFLICT'}, {'evidence_status':'PARTIAL'},
                      {'access':'empty'}, {'access':'access_gap'}, {'exact_scope':False},
                      {'freshness':'stale'}, {'evidence_ids':[]}):
            state={**base,**patch}
            self.assertIn('unsupported_feasibility',self.oracle.evidence_violations(state))
            state['feasibility']='unknown'
            self.assertEqual(self.oracle.evidence_violations(state),[])
        state={**base,'origin':'ba_hypothesis'}
        self.assertIn('hypothesis_as_fact',self.oracle.evidence_violations(state))

    def test_loss_aware_status_examples(self):
        for system,status,sufficient,expected in [
                ('gra','VERIFIED',True,'VERIFIED'),('gra','VERIFIED',False,'UNKNOWN'),
                ('gra','PARTIAL',True,'PARTIAL'),('gra','CONFLICT',True,'CONFLICT'),
                ('orbis','OBSERVED',False,'UNKNOWN'),('orbis','OBSERVED',True,'VERIFIED'),
                ('orbis','NOT_OBSERVED',True,'UNKNOWN'),('orbis','UNCERTAIN',True,'UNKNOWN'),
                ('orbis','CONTRADICTED',True,'CONFLICT'),('orbis','new-state',True,'UNKNOWN')]:
            result=self.oracle.example_import_status(system,status,sufficient)
            self.assertEqual(result['evidence_status'],expected)
            self.assertEqual(result['original_status'],status)
            self.assertNotIn('feasibility',result)

    def test_complete_prompts_and_byte_equal_copy_source(self):
        build=module('build474','scripts/build_bcreq_a_in.py').build()
        self.assertEqual(len(self.kit['steps']),24)
        self.assertFalse(self.kit['measured']);self.assertEqual(self.kit['routeVersion'],self.route['version'])
        self.assertEqual(set(build)-{ROOT/'site/data/a-in-kit.json'},
                         set((ROOT/'prompts/drafts/a-in').glob('*.md')))
        for path,body in build.items():self.assertEqual(path.read_text(),body,str(path))
        for step in self.kit['steps']:
            text=(ROOT/step['promptPath']).read_text();self.assertEqual(text,step['prompt'])
            for token in (step['id'],step['checks'],step['forbidden'],'AIN-21','AIN-22','Заказчику',
                          'task_id','attempt','snapshot_id','retrieved_at','CONFLICT',
                          'КОНЕЦ','не имитируй инструменты'.capitalize(),'Проверки (receipt)'):
                self.assertIn(token,text)
            self.assertIn('### Выполни',text);self.assertIn('### Форма результата',text)
        text=self.kit['steps'][15]['prompt']
        self.assertIn('нумерованным списком, без таблицы',text)
        self.assertIn('проверено и пусто',text)
        for n in range(1,21):
            self.assertTrue(any(f'LE-{n:02}' in s['prompt'] for s in self.kit['steps']),f'LE-{n:02}')

    def test_all_legacy_entries_are_guarded(self):
        names=('constitution-governance-oneshot','context-understanding-stepwise',
               'products-impact-analysis-stepwise','fr-documentation-stepwise',
               'in-understanding-oneshot','core-documentation-oneshot')
        paths=[ROOT/f'prompts/bcreq-{name}.md' for name in names]
        paths.append(ROOT/'prompts/drafts/bcreq-intake-questionnaire-stepwise.md')
        for path in paths:
            text=path.read_text();guard=text.split('<!-- issue-474:entry -->')[1].split('<!-- /issue-474:entry -->')[0]
            self.assertIn('AIN-21',guard);self.assertIn('AIN-16',guard)
            self.assertIn('Заказчику',guard)
        state=(ROOT/'docs/contracts/bcreq-manual-state.md').read_text()
        self.assertIn('в том числе при вызове отдельного класса',state)
        self.assertIn('allow AIN-21',self.kit['steps'][21]['prompt'])

    def test_sources_and_coverage_are_auditable(self):
        sources=json.loads((ROOT/'experiments/issue_474/sources.json').read_text())
        self.assertEqual({s['repo'] for s in sources},{'aether-orbis','aether-orbis-gra'})
        for source in sources:self.assertRegex(source['sha'],r'^[a-f0-9]{40}$')
        coverage=(ROOT/'experiments/issue_474/coverage.md').read_text()
        for prefix,count in [('P',20),('S',27),('LE-',20)]:
            for n in range(1,count+1):self.assertIn(f'| {prefix}{n:02} |',coverage)
        registry=(ROOT/'docs/rfc/rfc-registry.md').read_text()
        self.assertIn('RFC-PROV-001',registry);self.assertIn('`accepted` (#474)',registry)

if __name__=='__main__':unittest.main()
