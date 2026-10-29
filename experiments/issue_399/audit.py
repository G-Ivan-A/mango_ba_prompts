"""Bounded, resumable HTML-only portal audit. Python standard library only.

Raw HTML/text stays in ignored cache/. Public evidence contains metadata only.
No image, PDF, archive, installer or ticket endpoint is requested.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
from datetime import datetime, timezone
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urljoin, urlsplit, urlunsplit
from urllib.request import build_opener, HTTPRedirectHandler, Request

ROOT_URL = 'https://www.mango-office.ru/support/1_nachat-zdes/'
BASE = Path(__file__).resolve().parent
MAX_BYTES = 4 * 1024 * 1024
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}


def normalize(url, base=ROOT_URL):
    p = urlsplit(urljoin(base, url))
    return urlunsplit((p.scheme, p.netloc.lower(), p.path, p.query, ''))


def exclusion(url):
    p = urlsplit(url)
    path = unquote(p.path).lower()
    if p.scheme != 'https' or p.netloc != 'www.mango-office.ru':
        return 'external'
    if not path.startswith('/support/'):
        return 'outside-documentation'
    if any(s in path for s in ('/7_podderzhka/', '/8_archiv/', '/download', '/skachat', '/1_skachat', '/resources/')):
        return 'downloads-tickets-or-assets'
    if re.search(r'\.(pdf|docx?|xlsx?|zip|rar|exe|msi|dmg|png|jpe?g|gif|svg|webp|mp4|json|xml|js|css)(?:$|[?&])', url, re.I):
        return 'file'
    if p.query:
        return 'query-endpoint'
    return None


class Node:
    def __init__(self, tag='', attrs=()):
        self.tag, self.attrs, self.children = tag, dict(attrs), []

    def walk(self):
        yield self
        for c in self.children:
            if isinstance(c, Node):
                yield from c.walk()

    def text(self):
        if self.tag in ('script', 'style', 'svg'):
            return ''
        return ' '.join(c.text() if isinstance(c, Node) else c for c in self.children)


class Parser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node()
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        n = Node(tag, attrs)
        self.stack[-1].children.append(n)
        if tag not in VOID:
            self.stack.append(n)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for i in range(len(self.stack)-1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        self.stack[-1].children.append(data)


def clean(text):
    return re.sub(r'\s+', ' ', text).strip()


def assess_readability(row):
    """Conservative extraction gate, not a measurement of LLM comprehension."""
    tables = row.get('tables', [])
    visual = bool(row.get('images') or row.get('inline_diagrams'))
    ambiguous_table = any(t['merged_cells'] or not t['has_headers'] for t in tables)
    readable = bool(row.get('text_chars')) and not visual and not ambiguous_table
    return {'has_visual_context': bool(visual or tables), 'is_llm_readable': readable,
            'readability': ('text-and-tables' if tables else 'text') if readable else
                           'unreadable-or-unrecognized-template' if not row.get('text_chars') else
                           'visual-review-required' if visual else 'table-review-required'}


def parse_html(html, url):
    parser = Parser()
    parser.feed(html)
    nodes = list(parser.root.walk())
    bodies = [n for n in nodes if 'dc-doc-page__body' in n.attrs.get('class', '').split()]
    body = bodies[0] if bodies else Node()
    content = list(body.walk())
    def links(items):
        return sorted({normalize(n.attrs['href'], url) for n in items
                       if n.tag == 'a' and n.attrs.get('href')
                       and not n.attrs['href'].startswith(('#', 'javascript:', 'mailto:', 'tel:'))})
    text = clean(body.text())
    tables = []
    for table in (n for n in content if n.tag == 'table'):
        rows = [[clean(c.text()) for c in row.children if isinstance(c, Node) and c.tag in ('th', 'td')]
                for row in table.walk() if row.tag == 'tr']
        tables.append({'rows': rows, 'has_headers': any(n.tag == 'th' for n in table.walk()),
                       'merged_cells': any(n.attrs.get('rowspan', '1') != '1' or n.attrs.get('colspan', '1') != '1'
                                           for n in table.walk())})
    images = [{'url': normalize(n.attrs.get('src') or n.attrs.get('data-src', ''), url),
               'alt': n.attrs.get('alt', ''), 'title': n.attrs.get('title', '')}
              for n in content if n.tag == 'img']
    diagrams = sum(n.tag in ('svg', 'canvas') or 'mermaid' in n.attrs.get('class', '') for n in content)
    h1 = next((clean(n.text()) for n in nodes if n.tag == 'h1'), '')
    row = {'title': h1, 'body_found': bool(bodies), 'text': text, 'text_chars': len(text),
            'headings': [{'text': clean(n.text()), 'anchor': n.attrs.get('id')}
                         for n in content if re.fullmatch('h[1-6]', n.tag)],
            'content_links': links(content),
            'discovered_links': [x for x in links(nodes) if urlsplit(x).path.startswith('/support/')],
            'tables': tables, 'images': images, 'inline_diagrams': diagrams}
    return {**row, **assess_readability(row)}


class ExcludedRedirect(URLError):
    def __init__(self, url, code):
        super().__init__('excluded redirect: ' + url)
        self.target, self.code = url, code


class SafeRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if exclusion(normalize(newurl, req.full_url)):
            raise ExcludedRedirect(normalize(newurl, req.full_url), code)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch(url, refresh=False):
    if reason := exclusion(url):
        raise ValueError('Excluded URL: ' + reason)
    cache = BASE / 'cache' / (hashlib.sha256(url.encode()).hexdigest() + '.json')
    previous = None
    if cache.exists():
        row = json.loads(cache.read_text())
        if not refresh:
            return {**row, **assess_readability(row)}
        previous = [{k: v for k, v in row.items() if k not in ('text', 'discovered_links', 'previous_attempts')}]
        previous = row.get('previous_attempts', []) + previous
    row = {'url': url, 'observed_at': datetime.now(timezone.utc).isoformat(),
           'http_status': None, 'final_url': url}
    try:
        request = Request(url, headers={'User-Agent': 'Mango-BA-documentation-audit/1.0 (HTML metadata only)'})
        with build_opener(SafeRedirect()).open(request) as response:
            row.update(http_status=response.status, final_url=response.url,
                       content_type=response.headers.get('Content-Type', ''),
                       last_modified=response.headers.get('Last-Modified'))
            if 'text/html' not in row['content_type']:
                row['error'] = 'non-HTML response: body not downloaded'
            else:
                raw = response.read(MAX_BYTES + 1)
                if len(raw) > MAX_BYTES:
                    row['error'] = 'response exceeds bounded size'
                else:
                    row.update(sha256=hashlib.sha256(raw).hexdigest(), bytes=len(raw))
                    row.update(parse_html(raw.decode('utf-8', errors='replace'), response.url))
    except ExcludedRedirect as exc:
        row.update(http_status=exc.code, redirect_target=exc.target, error=str(exc))
    except HTTPError as exc:
        row.update(http_status=exc.code, error=str(exc))
    except (URLError, OSError) as exc:
        row['error'] = str(exc)
    if previous:
        row['previous_attempts'] = previous
    cache.parent.mkdir(exist_ok=True)
    cache.write_text(json.dumps(row, ensure_ascii=False))
    return {**row, **assess_readability(row)}


def crawl(output, max_pages=10000):
    pending, seen, rows, excluded = {ROOT_URL}, set(), [], {}
    with ThreadPoolExecutor(max_workers=4) as pool:
        jobs = set()
        while pending or jobs:
            while pending and len(jobs) < 4:
                if len(seen) >= max_pages:
                    raise RuntimeError('page bound reached: audit incomplete; increase bound explicitly')
                url = min(pending)
                pending.remove(url)
                seen.add(url)
                jobs.add(pool.submit(fetch, url))
            done, jobs = wait(jobs, return_when=FIRST_COMPLETED)
            for job in done:
                row = job.result()
                rows.append(row)
                for url in row.get('discovered_links', []):
                    why = exclusion(url)
                    if why:
                        excluded[url] = why
                    elif url not in seen:
                        pending.add(url)
                if len(rows) % 40 == 0:
                    print(f'fetched={len(rows)} pending={len(pending)} excluded={len(excluded)}', flush=True)
    public = []
    for r in sorted(rows, key=lambda r: r['url']):
        r = {k: v for k, v in r.items() if k not in ('text', 'discovered_links')}
        for table in r.get('tables', []):
            table['row_count'] = len(table['rows'])
            table['sample_rows'] = table.pop('rows')[:3]
        public.append(r)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(''.join(json.dumps(r, ensure_ascii=False, separators=(',', ':')) + '\n' for r in public))
    summary = {'root_url': ROOT_URL, 'pages': len(public), 'frontier_remaining': len(pending),
               'excluded': [{'url': u, 'reason': r} for u, r in sorted(excluded.items())],
               'errors': [r['url'] for r in rows if r.get('error')],
               'scope': 'all reachable HTML links under /support/; downloads/tickets/file archive excluded; HTML integration archive included'}
    output.with_name('crawl-summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: v for k, v in summary.items() if k != 'excluded'}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--output', type=Path, default=BASE.parents[1] / 'docs/taxonomy/portal-audit.jsonl')
    cli.add_argument('--max-pages', type=int, default=10000)
    cli.add_argument('--retry-errors', action='store_true', help='Retry failed/empty responses once, preserving observations')
    args = cli.parse_args()
    if args.retry_errors:
        failed = [r for r in (json.loads(p.read_text()) for p in (BASE/'cache').glob('*.json'))
                  if r.get('error') or r.get('bytes') == 0]
        with ThreadPoolExecutor(max_workers=4) as pool:
            for row in pool.map(lambda r: fetch(r['url'], refresh=True), failed):
                print('recheck', row['url'], row['http_status'], row.get('error', 'ok'), flush=True)
    crawl(args.output, args.max_pages)
