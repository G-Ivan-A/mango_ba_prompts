#!/usr/bin/env python3
"""Reproducible, bounded snapshot of the public site and prepared assets.

Run after generate-pages-data.mjs. Network reads only GitHub Pages; Academy
evidence is reviewed separately. --refresh-live explicitly replaces snapshots.
"""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
BASE = 'e6a72240ba5f7b121f42e2446d9bd7fa341f753c'
LIVE = 'https://g-ivan-a.github.io/mango_ba_prompts/'
LIVE_FILES = ('index.html', 'data/stats.json', 'data/prompts.json', 'data/test-kit.json')


def normalized(data):
    if isinstance(data, dict):
        return {k: normalized(v) for k, v in data.items() if k != 'generatedAt'}
    if isinstance(data, list):
        return [normalized(v) for v in data]
    return data


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--refresh-live', action='store_true')
    args = parser.parse_args()
    cache = HERE / 'source-snapshots' / 'live'
    cache.mkdir(parents=True, exist_ok=True)
    live_hashes = {}
    for name in LIVE_FILES:
        path = cache / name
        path.parent.mkdir(parents=True, exist_ok=True)
        if args.refresh_live or not path.exists():
            with urlopen(LIVE + name, timeout=30) as response:
                body = response.read(4 * 1024 * 1024 + 1)
                assert len(body) <= 4 * 1024 * 1024, name
                path.write_bytes(body)
        live_hashes[name] = digest(path.read_bytes())
    assets = {}
    changed = []
    for path in sorted((ROOT / 'site').rglob('*')):
        if not path.is_file() or 'screenshots' in path.parts:
            continue
        name = path.relative_to(ROOT).as_posix()
        body = path.read_bytes()
        record = {'sha256': digest(body), 'bytes': len(body)}
        if path.suffix == '.json':
            record['normalized_sha256'] = digest(json.dumps(normalized(json.loads(body)),
                ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode())
        assets[name] = record
        old = subprocess.run(['git', 'show', BASE + ':' + name], cwd=ROOT,
                             capture_output=True, check=False)
        same = old.returncode == 0 and old.stdout == body
        if not same and path.suffix == '.json' and old.returncode == 0:
            same = normalized(json.loads(body)) == normalized(json.loads(old.stdout))
        if not same:
            changed.append(name)
    live_stats = json.loads((cache / 'data/stats.json').read_text())
    local_stats = json.loads((ROOT / 'site/data/stats.json').read_text())
    live_prompts = json.loads((cache / 'data/prompts.json').read_text())
    local_prompts = json.loads((ROOT / 'site/data/prompts.json').read_text())
    old_ids = {p['id'] for p in live_prompts['prompts']}
    new_ids = {p['id'] for p in local_prompts['prompts']}
    assert old_ids <= new_ids, 'Public catalogue entries removed'
    assert changed == [], 'Prepared site diverged from merged baseline: ' + str(changed)
    result = {
        'accessed_at': '2026-11-09', 'baseline_sha': BASE,
        'live_url': LIVE, 'live_version': live_stats['siteVersion'],
        'candidate_version': local_stats['siteVersion'],
        'live_totals': live_stats['totals'], 'candidate_totals': local_stats['totals'],
        'live_sha256': live_hashes, 'catalogue_ids_preserved': sorted(old_ids),
        'catalogue_ids_added': sorted(new_ids - old_ids),
        'baseline_semantic_changes': changed,
        'normalization': 'Ignore generatedAt only; screenshots excluded from deploy-content hash comparison.',
        'assets': assets,
    }
    (HERE / 'site-audit.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ('live_version', 'candidate_version',
          'live_totals', 'candidate_totals', 'baseline_semantic_changes')}, ensure_ascii=False, indent=2))
    print(f'{len(assets)} asset hashes; {len(old_ids)} public catalogue IDs preserved')


if __name__ == '__main__':
    main()
