#!/usr/bin/env python3
"""Preserve replaced 2.7.0 prompts; verify Git sources against served bodies."""
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = '7152e499bac5d73c08f4ac59a0a714c577597e7e'
PUBLICATION = '268aee900e04e8888364c003d7a602cf573a148d'
OUT = ROOT / 'prompts/archive/a-in-v2.7.0'


def main():
    kit = json.loads((ROOT/'experiments/issue_476/private/test-kit.json').read_text())
    catalog = json.loads((ROOT/'experiments/issue_476/private/prompts.json').read_text())
    assert catalog['siteVersion']['version'] == '2.7.0'
    entries = []
    for step in kit['steps']:
        code = step['step'].split()[0]
        if code not in ('Ш-А', 'Ш-1', 'Ш-2'):
            continue
        draft = step['draft']
        entries.append((draft['sourcePath'], draft['body'], code,
                        {'Ш-А':['AIN-02'], 'Ш-1':[f'AIN-{i:02}' for i in range(1,25)],
                         'Ш-2':[f'AIN-{i:02}' for i in range(6,14)]+['AIN-22']}[code]))
    old = next(p for p in catalog['prompts'] if p['file']=='bcreq-in-understanding-oneshot.md')
    entries.append((old['sourcePath'], old['body'], 'A-IN one-shot',
                    [f'AIN-{i:02}' for i in range(1,25)]))
    manifest = {'siteVersion':'2.7.0', 'observedAt':'2026-11-08',
                'sourceCommit':SOURCE, 'publicationCommit':PUBLICATION,
                'url':'https://g-ivan-a.github.io/mango_ba_prompts/', 'entries':[]}
    OUT.mkdir(parents=True, exist_ok=True)
    for original, served_body, step, replacements in entries:
        content = subprocess.check_output(['git','show',f'{SOURCE}:{original}'], cwd=ROOT).decode()
        body = content.split('---',2)[2].lstrip('\r\n')
        assert body == served_body, f'Production body differs from {SOURCE}:{original}'
        target = OUT / Path(original).name
        target.write_text(content)
        manifest['entries'].append({'sourcePath':original, 'archivePath':str(target.relative_to(ROOT)),
            'step':step, 'replacedBy':replacements,
            'sha256':hashlib.sha256(content.encode()).hexdigest(),
            'bodySha256':hashlib.sha256(body.encode()).hexdigest()})
    (OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    print('4 full original files match the bodies served by production 2.7.0')


if __name__ == '__main__':
    main()
