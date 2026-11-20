#!/usr/bin/env python3
"""Release parity, immutable history, traceability and actual Catalog filter regression."""
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
BASE = 'f0f5ad56'  # merged PR #475, before publication-only changes


def read(path):
    return (ROOT/path).read_text()


def load(path):
    return json.loads(read(path))


def only_pin_488(path, text, base):
    """Issue #488: файл отличается от BASE только перезакреплённой ссылкой и версией.

    Слой experiments/issue_488/prompt_changes.py снимает ровно эти правки; строку
    based_on_sha256 черновика и манифеста (хеш опубликованного текста) и счётчик
    hub_main_to_metamodel_sha манифеста сверяет --check сборщика.
    """
    spec=importlib.util.spec_from_file_location('i488_for_476',ROOT/'experiments/issue_488/prompt_changes.py')
    layer=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(layer)
    drop=lambda t: re.sub(r'(?m)^ *"?(based_on_sha256|hub_main_to_metamodel_sha)"?: .*\n','',t)  # noqa: E731
    return drop(layer.revert(path,text))==drop(base)


class Readiness(unittest.TestCase):
    def test_four_original_files_and_served_body_hashes(self):
        manifest=load('prompts/archive/a-in-v2.7.0/manifest.json')
        self.assertEqual(manifest['siteVersion'],'2.7.0')
        self.assertEqual(len(manifest['entries']),4)
        catalog=load('site/data/prompts.json')['prompts']
        for entry in manifest['entries']:
            text=read(entry['archivePath'])
            original=subprocess.check_output(['git','show',f"{manifest['sourceCommit']}:{entry['sourcePath']}"],cwd=ROOT).decode()
            self.assertEqual(text,original)
            self.assertEqual(hashlib.sha256(text.encode()).hexdigest(),entry['sha256'])
            body=text.split('---',2)[2].lstrip('\r\n')
            self.assertEqual(hashlib.sha256(body.encode()).hexdigest(),entry['bodySha256'])
            card=next(p for p in catalog if p['sourcePath']==entry['archivePath'])
            self.assertTrue(card['archived'])
            self.assertEqual(card['content'],text)
            self.assertEqual(card['body'],body)
            self.assertEqual(card['archiveInfo']['replacedBy'],entry['replacedBy'])

    def test_full_24_steps_and_cross_references(self):
        route=load('docs/ba-processes/bcreq-a-in-route.json')
        kit=load('site/data/a-in-kit.json')
        self.assertEqual(len(kit['steps']),24)
        self.assertEqual(kit['routeVersion'],route['version'])
        ids={s['id'] for s in route['steps']}
        classes={p['classId'] for p in load('site/data/prompts.json')['prompts'] if p.get('classId')}
        for expected,step in zip(route['steps'],kit['steps']):
            for key,value in expected.items():
                self.assertEqual(step[key],value)
            self.assertEqual(step['prompt'],read(step['promptPath']))
            self.assertEqual(hashlib.sha256(step['prompt'].encode()).hexdigest(),step['promptSha256'])
            self.assertTrue(set(re.findall(r'К-\d{2}',step['operation'])) <= classes)
            self.assertTrue(set(step['returns']+[step['failure']]) <= ids)
            if step['id']!='AIN-24':
                self.assertIn(step['next'],ids)
        for path in re.findall(r'https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/([^"`]+)',read('site/app.js')):
            if '${' not in path:
                self.assertTrue((ROOT/path).exists(),path)

    def test_no_prompt_or_layout_degradation(self):
        paths=subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,'prompts/'],cwd=ROOT).decode().splitlines()
        base={path:subprocess.check_output(['git','show',f'{BASE}:{path}'],cwd=ROOT) for path in paths}
        changed=[path for path in paths if (ROOT/path).read_bytes()!=base[path]
                 and not only_pin_488(path,read(path),base[path].decode())]
        # Issue #490: «Итог шага» и формат шагов меняют только сгенерированные
        # черновики; каждый совпадает с выходом своего сборщика (--check).
        for path in changed:
            self.assertTrue(path.startswith('prompts/drafts/') and '/archive/' not in path, path)
            self.assertIn('Итог шага', read(path), path)
        for builder in ('scripts/build_bcreq_a_in.py','scripts/build_bcreq_step_prompts.py'):
            subprocess.run(['python3',builder,'--check'],cwd=ROOT,check=True,capture_output=True,timeout=60)
        # Новые правила #490 — в site/step-format.css; файлы 2.8.6 не меняются.
        for path in ('site/styles.css','site/v2.css','site/standards.css','site/v2.js'):
            self.assertEqual((ROOT/path).read_bytes(),subprocess.check_output(['git','show',f'{BASE}:{path}'],cwd=ROOT),path)

    def test_release_and_archive_applicability(self):
        data=load('site/data/prompts.json')
        # 2.8.6 — релиз #476/#480; #490 выпускает 2.9.0. Версия не откатывается
        # и одинакова в данных и разметке.
        version=data['siteVersion']['version']
        self.assertGreaterEqual(tuple(map(int,version.split('.'))),(2,8,6))
        self.assertEqual(data['siteVersion'],load('site/data/stats.json')['siteVersion'])
        self.assertIn(f'>v{version}<',read('site/index.html'))
        self.assertIn('архив: 14 промптов этапа 1 и 4 редакции 2.7.0',read('site/index.html'))
        stages={p['label'] for p in data['filters']['processes']}
        ops={p['id'] for p in data['filters']['operations']}
        for p in data['prompts']:
            self.assertTrue(set(p.get('filterProcesses',p['processes'])) <= stages)
            self.assertTrue(p.get('filterProcesses',p['processes']))
            self.assertIn(p['operation']['id'],ops)
        self.assertEqual(len({p['id'] for p in data['prompts']}),57)

    def test_actual_filter_regression(self):
        subprocess.run(['node','--test','experiments/issue_476/catalog.test.cjs'],cwd=ROOT,check=True,timeout=20)


if __name__=='__main__':
    unittest.main()
