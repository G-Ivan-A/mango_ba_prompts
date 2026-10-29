"""Refresh permitted HTML URLs from the pinned issue 399 map for text comparison.

The historical map has no full text; a fresh corpus is necessary. Original
observation hashes remain in the baseline, and drift is reported, not hidden.
"""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import re
import audit

BASE = Path(__file__).resolve().parent
OUT = BASE.parents[1] / 'docs/taxonomy'


def exclusion(url):
    if reason := audit.legacy.exclusion(url):
        return reason
    if re.search('arhiv|archiv|ustarevsh|deprecated|obsolete|old_version', url, re.I):
        return 'archive-or-obsolete'
    return None


class SafeRedirect(audit.legacy.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        target = audit.legacy.normalize(newurl, req.full_url)
        if exclusion(target):
            raise audit.legacy.ExcludedRedirect(target, code)
        return super().redirect_request(req, fp, code, msg, headers, target)


def main():
    audit.legacy.BASE = BASE / 'cache/portal'
    audit.legacy.BASE.mkdir(parents=True, exist_ok=True)
    audit.legacy.SafeRedirect = SafeRedirect
    rows = [json.loads(s) for s in (OUT / 'portal-map.jsonl').read_text().splitlines()]
    allowed = [r for r in rows if not exclusion(r['url'])]
    observations = []
    def fetch(row):
        r = audit.legacy.fetch(row['url'])
        if r.get('error') or not r.get('text_chars'):
            r = audit.legacy.fetch(row['url'], refresh=True)
        return {'url': r['url'], 'http_status': r.get('http_status'), 'error': r.get('error'),
                'observed_at': r['observed_at'], 'source_sha256': r.get('sha256'),
                'baseline_sha256': row['source_sha256'],
                'matches_baseline_html': r.get('sha256') == row['source_sha256'],
                'text_chars': r.get('text_chars', 0),
                'text_sha256': hashlib.sha256(r.get('text', '').encode()).hexdigest()}
    with ThreadPoolExecutor(max_workers=4) as pool:
        for r in pool.map(fetch, allowed):
            observations.append(r)
            if len(observations) % 100 == 0:
                print(f'pages={len(observations)}/{len(allowed)}', flush=True)
    (OUT / 'portal-comparison-audit.jsonl').write_text(''.join(json.dumps(r, ensure_ascii=False, separators=(',', ':')) + '\n' for r in observations))
    audit.write_json(OUT / 'portal-comparison-summary.json', {
        'baseline_map_url': 'https://github.com/G-Ivan-A/mango_ba_prompts/blob/7feb9be2/docs/taxonomy/portal-map.jsonl',
        'baseline_map_sha256': hashlib.sha256((OUT / 'portal-map.jsonl').read_bytes()).hexdigest(),
        'baseline_rows': len(rows), 'refreshed_rows': len(observations),
        'baseline_html_hash_matches': sum(r['matches_baseline_html'] for r in observations),
        'errors': [r for r in observations if r.get('error')],
        'excluded': [{'url': r['url'], 'reason': exclusion(r['url'])} for r in rows if exclusion(r['url'])],
        'temporal_limit': 'Historical map contains no article texts; prose comparison uses fresh HTML at its permitted URLs. HTML hash drift can include markup changes.'})
    print('complete', len(observations), flush=True)


if __name__ == '__main__':
    main()
