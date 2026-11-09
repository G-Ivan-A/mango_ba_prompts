#!/usr/bin/env python3
"""Verify #477 parity and optionally the downloaded 2.7.0 baseline, offline."""
import hashlib
import json
import re
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
BASE = 'e6a72240ba5f7b121f42e2446d9bd7fa341f753c'


def original(path):
    return subprocess.check_output(['git', 'show', f'{BASE}:{path}'], cwd=ROOT)


def load(path):
    return json.loads((ROOT / path).read_text())


def stable(value):
    if isinstance(value, dict):
        return {k: stable(v) for k, v in value.items() if k not in ('siteVersion', 'generatedAt')}
    if isinstance(value, list):
        return [stable(v) for v in value]
    return value


def main():
    paths = subprocess.check_output([
        'git', 'ls-tree', '-r', '--name-only', BASE, 'prompts/', 'standards/',
        'site/app.js', 'site/styles.css', 'site/v2.css', 'site/v2.js', 'site/standards.css',
    ], cwd=ROOT, text=True).splitlines()
    for path in paths:
        assert (ROOT / path).read_bytes() == original(path), path
    for path in sorted((ROOT / 'site/data').glob('*.json')):
        relative = path.relative_to(ROOT).as_posix()
        assert stable(json.loads(path.read_text())) == stable(json.loads(original(relative))), relative
    assert (ROOT / 'site/index.html').read_bytes().replace(b'v2.8.6', b'v2.8.5') == original('site/index.html')
    report = {'sourceBaseline': BASE, 'unchangedSourceFiles': len(paths),
              'allSiteDataEqualExceptVersionAndTimestamp': True,
              'htmlEqualExceptVersion': True, 'liveBaselineChecked': False}
    private = ROOT / 'experiments/issue_480/private'
    if (private / 'live-prompts.json').exists():
        live = json.loads((private / 'live-prompts.json').read_text())
        kit = json.loads((private / 'live-test-kit.json').read_text())
        assert live['siteVersion']['version'] == '2.7.0'
        current = load('site/data/prompts.json')['prompts']
        assert {p['id'] for p in live['prompts']} <= {p['id'] for p in current}
        manifest = load('prompts/archive/a-in-v2.7.0/manifest.json')
        bodies = {s['draft']['sourcePath']: s['draft']['body'] for s in kit['steps'] if s.get('draft')}
        bodies.update({p['sourcePath']: p['body'] for p in live['prompts']})
        for entry in manifest['entries']:
            assert hashlib.sha256(bodies[entry['sourcePath']].encode()).hexdigest() == entry['bodySha256']
            card = next(p for p in current if p['sourcePath'] == entry['archivePath'])
            assert card['body'] == bodies[entry['sourcePath']]
        old_steps = {s['draft']['sourcePath']: s['draft']['body'] for s in load('site/data/test-kit.json')['steps'] if s.get('draft')}
        preserved = 0
        extended = []
        for step in kit['steps']:
            if step['step'].split()[0] in ('Ш-А', 'Ш-1', 'Ш-2'):
                continue
            old = step['draft']['body']
            new = old_steps[step['draft']['sourcePath']]
            if old == new:
                preserved += 1
            else:
                # #474 deliberately prepended an explicit A-IN guard; require
                # the entire preceding live body to survive after its removal.
                clean, count = re.subn(r'\n<!-- issue-474:entry -->.*?<!-- /issue-474:entry -->\n\n', '', new, flags=re.S)
                assert count == 1 and clean == old, step['step']
                extended.append(step['step'])
        report.update(liveBaselineChecked=True, liveVersion='2.7.0', liveCatalogIdsRetained=len(live['prompts']),
                      archivedLiveBodiesEqual=4, otherLiveStepsUnchanged=preserved, liveStepsWithOnlyAcceptedAINGuard=extended)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
