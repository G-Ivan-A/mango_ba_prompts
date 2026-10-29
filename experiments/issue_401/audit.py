"""Bounded HTML-only audit of the alternative documentation; stdlib only.

Reuses issue 399's HTML tree and table/readability logic. Cached full text stays
local. Redirects and response MIME types are checked before any body is read.
"""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import re
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urljoin, urlsplit, urlunsplit
from urllib.request import build_opener, HTTPRedirectHandler, Request

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[1]
OUT = ROOT / 'docs/taxonomy'
ORIGIN = 'https://docs.mango-office.ru'
ROOT_URL = ORIGIN + '/ru/index.html'
PREFIXES = ('1_nachat-zdes', '3_produkty-i-prilozheniya', '4_integratsii',
            '5_api-i-razrabotka', '6_administrirovanie')
MAX_BYTES = 4 * 1024 * 1024
SPEC = importlib.util.spec_from_file_location('issue399_html', ROOT / 'experiments/issue_399/audit.py')
legacy = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(legacy)
clean = legacy.clean


def normalize(url, base=ROOT_URL):
    p = urlsplit(urljoin(base, url))
    return urlunsplit((p.scheme, p.netloc.lower(), p.path, p.query, ''))


def exclusion(url):
    p = urlsplit(url)
    path = unquote(unquote(p.path)).lower()
    if p.scheme != 'https' or p.netloc != 'docs.mango-office.ru':
        return 'external'
    if p.query:
        return 'query-endpoint'
    if re.search(r'/(?:\.\.?)(?:/|$)', path):
        return 'path-traversal'
    if any(s in path for s in ('arhiv', 'archiv', 'ustarevsh', 'deprecated', 'obsolete',
                                'old_version', '/download', '/skachat', '/ticket', '/7_podderzhka/')):
        return 'archive-obsolete-download-or-support'
    if path == '/ru/index.html':
        return None
    if not any(path.startswith('/ru/' + s + '/') for s in PREFIXES):
        return 'outside-requested-sections'
    if not path.endswith('.html'):
        return 'non-html-file-or-endpoint'
    return None


def parse_html(html, url):
    parser = legacy.Parser()
    parser.feed(html)
    nodes = list(parser.root.walk())
    base = next((urljoin(url, n.attrs['href']) for n in nodes if n.tag == 'base' and n.attrs.get('href')), url)
    bodies = [n for n in nodes if 'dc-doc-page__body' in n.attrs.get('class', '').split()]
    leading = [n for n in nodes if 'dc-doc-leading-page__content' in n.attrs.get('class', '').split()]
    # The alternative site's root uses a leading-page layout, not article body.
    if not leading:
        leading = [n for n in nodes if 'dc-doc-leading-page__main' in n.attrs.get('class', '').split()]
    body = (bodies or leading or [legacy.Node()])[0]
    # Feed a synthetic article wrapper to the already tested table/image parser.
    row = legacy.parse_html(html, url)
    content = list(body.walk())
    row.update(text=clean(body.text()), body_found=bool(bodies or leading))
    row['text_chars'] = len(row['text'])
    row['template'] = 'article' if bodies else 'leading' if leading else 'unrecognized'
    def links(items):
        return sorted({normalize(n.attrs['href'], base) for n in items if n.tag == 'a'
                       and n.attrs.get('href') and not n.attrs['href'].startswith(('#', 'javascript:', 'mailto:', 'tel:'))})
    row['content_links'] = links(content)
    row['discovered_links'] = links(nodes)
    row['images'] = [{**im, 'url': normalize(n.attrs.get('src') or n.attrs.get('data-src', ''), base)}
                     for im, n in zip(row['images'], (n for n in content if n.tag == 'img'))]
    row['base_url'] = base
    row['title'] = next((clean(n.text()) for n in nodes if n.tag == 'h1'), row['title'])
    return {**row, **legacy.assess_readability(row)}


class ExcludedRedirect(URLError):
    def __init__(self, target, code):
        super().__init__('excluded redirect: ' + target)
        self.target, self.code = target, code


class SafeRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        target = normalize(newurl, req.full_url)
        if exclusion(target):
            raise ExcludedRedirect(target, code)
        return super().redirect_request(req, fp, code, msg, headers, target)


def open_url(url):
    return build_opener(SafeRedirect()).open(Request(url, headers={
        'User-Agent': 'Mango-BA-documentation-audit/1.0 (HTML metadata only)'}))


def request(url):
    if reason := exclusion(url):
        raise ValueError('Excluded URL: ' + reason)
    row = {'url': url, 'observed_at': datetime.now(timezone.utc).isoformat(),
           'http_status': None, 'final_url': url}
    try:
        with open_url(url) as response:
            row.update(http_status=response.status, final_url=response.url,
                       headers={k.lower(): v for k, v in response.headers.items()})
            if 'text/html' not in response.headers.get('Content-Type', ''):
                row['error'] = 'non-HTML response: body not downloaded'
            else:
                raw = response.read(MAX_BYTES + 1)
                if len(raw) > MAX_BYTES:
                    row['error'] = 'bounded response size exceeded'
                else:
                    row.update(source_sha256=hashlib.sha256(raw).hexdigest(), bytes=len(raw))
                    row.update(parse_html(raw.decode('utf-8', errors='replace'), response.url))
    except ExcludedRedirect as exc:
        row.update(http_status=exc.code, redirect_target=exc.target, error=str(exc))
    except HTTPError as exc:
        row.update(http_status=exc.code, error=str(exc), headers=dict(exc.headers))
    except (URLError, OSError) as exc:
        row['error'] = str(exc)
    return row


def fetch(url, refresh=False):
    if exclusion(url):
        raise ValueError('Excluded URL: ' + url)
    cache = BASE / 'cache' / (hashlib.sha256(url.encode()).hexdigest() + '.json')
    if cache.exists() and not refresh:
        return json.loads(cache.read_text())
    row = request(url)
    if cache.exists():
        previous = json.loads(cache.read_text())
        row['previous_attempts'] = previous.get('previous_attempts', []) + [
            {k: previous.get(k) for k in ('http_status', 'error', 'observed_at')}]
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_text(json.dumps(row, ensure_ascii=False))
    return row


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def public(row):
    result = {k: v for k, v in row.items() if k not in ('text', 'discovered_links')}
    result['text_sha256'] = hashlib.sha256(row.get('text', '').encode()).hexdigest()
    result['tables'] = [{k: v for k, v in t.items() if k != 'rows'} | {'row_count': len(t['rows'])}
                        for t in row.get('tables', [])]
    return result


def mapping(rows):
    by_url = {r['url']: r for r in rows}
    mapped = []
    for r in rows:
        parts = urlsplit(r['url']).path.split('/')[2:-1]
        hierarchy = [{'url': ROOT_URL, 'title': by_url.get(ROOT_URL, {}).get('title', 'Документация')}]
        for i in range(len(parts)):
            u = ORIGIN + '/ru/' + '/'.join(parts[:i+1]) + '/index.html'
            hierarchy.append({'url': u, 'title': by_url.get(u, {}).get('title', parts[i]),
                              'title_observed': bool(by_url.get(u, {}).get('title'))})
        if hierarchy[-1]['url'] != r['url']:
            hierarchy.append({'url': r['url'], 'title': r.get('title', '')})
        api = '/5_api-i-razrabotka/' in r['url']
        admin = '/6_administrirovanie/' in r['url']
        integrations = '/4_integratsii/' in r['url'] or api
        tag = parts[1] if len(parts) > 1 else parts[0] if parts else 'root'
        mapped.append({**public(r), 'hierarchy': hierarchy,
            'content_type': 'API spec' if api else 'instruction' if admin or '/1_nachat-zdes/' in r['url'] else 'product-documentation',
            'tags': sorted(set([tag] + (['integration'] if integrations else []) + (['administration'] if admin else []))),
            'relevance_for_BA': {'FT': 2 if r.get('text_chars') else 0, 'NFT': 2 if admin or api else 1,
                                 'integrations': 3 if integrations else 1,
                                 'basis': 'editorial 0..3 routing heuristic; not measured relevance'},
            'is_llm_readable': r.get('is_llm_readable', False),
            'has_visual_context': r.get('has_visual_context', False),
            'update_frequency': {'value': 'unknown', 'basis': 'single observation; Last-Modified is not frequency',
                                 'last_modified': r.get('headers', {}).get('last-modified'), 'recheck_days': 30},
            'cross_references': r.get('content_links', []),
            'source_urls': [r['url']]})
    return mapped


def crawl(max_pages=10000, retry_errors=False):
    pending, seen, excluded, rows = {ROOT_URL}, set(), {}, []
    with ThreadPoolExecutor(max_workers=4) as pool:
        while pending:
            batch = sorted(pending)[:4]
            if len(seen) + len(batch) > max_pages:
                raise RuntimeError('page bound reached; audit incomplete')
            pending.difference_update(batch)
            seen.update(batch)
            for r in pool.map(fetch, batch):
                if retry_errors and (r.get('error') or not r.get('text_chars')):
                    r = fetch(r['url'], refresh=True)
                rows.append(r)
                for u in r.get('discovered_links', []):
                    if reason := exclusion(u):
                        excluded[u] = reason
                    elif u not in seen:
                        pending.add(u)
            if len(rows) % 100 < 4:
                print(f'pages={len(rows)} pending={len(pending)} excluded={len(excluded)}', flush=True)
    rows.sort(key=lambda r: r['url'])
    OUT.mkdir(exist_ok=True)
    (OUT / 'docs.mango-map.jsonl').write_text(''.join(json.dumps(r, ensure_ascii=False, separators=(',', ':')) + '\n' for r in mapping(rows)))
    write_json(OUT / 'docs-crawl-summary.json', {
        'root_url': ROOT_URL, 'pages': len(rows), 'frontier_remaining': 0,
        'http_status_counts': dict(Counter(str(r.get('http_status')) for r in rows)),
        'sections': {p: sum('/ru/' + p + '/' in r['url'] for r in rows) for p in PREFIXES},
        'errors': [r['url'] for r in rows if r.get('error')],
        'unrecognized_templates': [r['url'] for r in rows if not r.get('body_found')],
        'excluded': [{'url': u, 'reason': v} for u, v in sorted(excluded.items())],
        'scope': 'All reachable HTML in the five requested branches; archives, obsolete versions, downloads, support and files excluded.'})
    print(f'complete pages={len(rows)} errors={sum(bool(r.get("error")) for r in rows)}', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--max-pages', type=int, default=10000)
    parser.add_argument('--retry-errors', action='store_true')
    args = parser.parse_args()
    crawl(args.max_pages, args.retry_errors)
