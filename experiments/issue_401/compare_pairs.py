"""Compare fresh static prose at corresponding routes on both web sources."""
import json
from pathlib import Path
from urllib.parse import urlsplit
import audit

OUT = Path(__file__).resolve().parents[2] / 'docs/taxonomy'


def main():
    docs = [json.loads(s) for s in (OUT/'docs.mango-map.jsonl').read_text().splitlines()]
    portal = {r['url']:r for r in map(json.loads, (OUT/'portal-comparison-audit.jsonl').read_text().splitlines())}
    pairs, mismatches, outside = 0, [], []
    exact = 0
    for d in docs:
        path = urlsplit(d['url']).path.removeprefix('/ru/')
        path = path[:-10] if path.endswith('index.html') else path[:-5] + '/'
        u = 'https://www.mango-office.ru/support/' + path
        if u not in portal:
            outside.append({'docs_url': d['url'], 'expected_portal_url': u})
            continue
        pairs += 1
        p = portal[u]
        if d['text_sha256'] == p['text_sha256']:
            exact += 1
        else:
            mismatches.append({'docs_url': d['url'], 'portal_url': u,
                               'docs_text_sha256': d['text_sha256'], 'portal_text_sha256': p['text_sha256'],
                               'docs_status': d['http_status'], 'portal_status': p['http_status']})
    audit.write_json(OUT/'web-source-pairs.json', {'route_pairs': pairs, 'identical_extracted_text': exact,
        'text_mismatches': mismatches, 'not_in_permitted_portal399_map': outside,
        'method': 'Transform /ru/path/index.html to /support/path/ and /ru/path/page.html to /support/path/page/; compare extracted text SHA-256. Unpaired legacy URLs are not equated.',
        'limit': 'Single-time observation, not evidence of independent publishing pipelines or long-term uptime.'})
    print('pairs',pairs,'exact',exact,'mismatches',len(mismatches),'unpaired',len(outside))


if __name__ == '__main__':
    main()
