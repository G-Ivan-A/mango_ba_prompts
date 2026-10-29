"""Compare every extracted PDF section to both recorded HTML corpora.

Corpus-wide exact 5-token retrieval finds candidates across navigation branches.
Greedy complementary candidates support sections split over several web pages.
The ordered token diff reports lexical changes, not semantic missing features.
Full texts remain ignored; published operations contain offsets and counts.
"""
from collections import defaultdict
from difflib import SequenceMatcher
import hashlib
import json
from pathlib import Path
import audit
import compare
from compare import tokens, text_difference, ssot_decision

BASE = Path(__file__).resolve().parent
OUT = BASE.parents[1] / 'docs/taxonomy'


def grams(ts):
    return {tuple(ts[i:i+5]) for i in range(max(0, len(ts)-4))}


def product_scope(section_id, url):
    chapter = section_id.split('.')[0]
    if chapter == '16':
        return '/8_rechevaya-analitika-i-skoring/' in url or '/4_kontrol-kachestva/8_rechevaya_analitika/' in url
    if chapter == '17':
        return '/6_administrirovanie/1_roli-i-prava/' in url or '/1_virtualnaya-ats-i-lichnyi-kabinet/' in url
    if chapter == '18':
        return '/6_administrirovanie/1_roli-i-prava/' in url or '/3_kontakt-tsentr/' in url
    return '/3_kontakt-tsentr/' in url


def section_window(pdf_tokens, web_tokens):
    blocks = [b for b in SequenceMatcher(None, pdf_tokens, web_tokens, autojunk=False).get_matching_blocks()
              if b.size >= 5]
    if not blocks:
        return 0, len(web_tokens)
    first, last = blocks[0], blocks[-1]
    return (max(0, first.b - first.a),
            min(len(web_tokens), last.b + last.size + len(pdf_tokens) - last.a - last.size))


def load_corpus(source):
    mapping = [json.loads(s) for s in (OUT / ('docs.mango-map.jsonl' if source == 'docs' else 'portal-map.jsonl')).read_text().splitlines()]
    if source == 'docs':
        folder = BASE / 'cache'
    else:
        folder = BASE / 'cache/portal/cache'
        allowed = {r['url'] for r in map(json.loads, (OUT/'portal-comparison-audit.jsonl').read_text().splitlines())}
        mapping = [r for r in mapping if r['url'] in allowed]
    rows = []
    for m in mapping:
        path = folder / (hashlib.sha256(m['url'].encode()).hexdigest() + '.json')
        r = json.loads(path.read_text())
        if r.get('text') and r.get('http_status') == 200:
            rows.append({'url': r['url'], 'title': r['title'], 'text': r['text'],
                         'source_sha256': r.get('source_sha256', r.get('sha256')),
                         'text_sha256': hashlib.sha256(r['text'].encode()).hexdigest()})
    return rows


def compare_corpus(sections, corpus):
    ref_tokens = [tokens(s['text']) for s in sections]
    reference = [grams(ts) for ts in ref_tokens]
    inverse = defaultdict(list)
    for i, gs in enumerate(reference):
        for g in gs:
            inverse[g].append(i)
    hits = [dict() for s in sections]
    all_tokens = []
    for di, doc in enumerate(corpus):
        ts = tokens(doc['text'])
        all_tokens.append(ts)
        matches = defaultdict(set)
        for g in grams(ts):
            for si in inverse.get(g, ()):
                matches[si].add(g)
        for si, gs in matches.items():
            hits[si][di] = gs
    result = []
    for si, section in enumerate(sections):
        candidates = {d: gs for d, gs in hits[si].items() if product_scope(section['id'], corpus[d]['url'])}
        missing = set(reference[si])
        chosen = []
        while candidates:
            di = min(candidates, key=lambda d: (-len(candidates[d] & missing), corpus[d]['url']))
            gain = candidates[di] & missing
            # A weak boilerplate hit is retained as a candidate, never certified coverage.
            if len(gain) < max(3, len(reference[si]) * (0.01 if not chosen else 0.05)):
                break
            chosen.append(di)
            missing.difference_update(gain)
            del candidates[di]
        if not chosen and candidates:
            chosen = [min(candidates, key=lambda d: (-len(candidates[d]), corpus[d]['url']))]
        if not chosen:
            # Short summaries can have no exact five-token match despite an exact title.
            title = tokens(section['title'])
            exact_titles = [di for di, doc in enumerate(corpus)
                            if product_scope(section['id'], doc['url']) and tokens(doc['title']) == title]
            if exact_titles:
                chosen = [min(exact_titles, key=lambda d: corpus[d]['url'])]
        def order(di):
            return SequenceMatcher(None, ref_tokens[si], all_tokens[di], autojunk=False).find_longest_match().a
        chosen.sort(key=lambda d: (order(d), corpus[d]['url']))
        windows = {d: section_window(ref_tokens[si], all_tokens[d]) for d in chosen}
        web_text = '\n'.join(' '.join(all_tokens[d][windows[d][0]:windows[d][1]]) for d in chosen)
        diff = text_difference(section['text'], web_text)
        covered = set().union(*(grams(all_tokens[d]) & reference[si] for d in chosen)) if chosen else set()
        all_covered = set().union(*hits[si].values()) if hits[si] else set()
        pages, offset = [], 0
        for di in chosen:
            start, end = windows[di]
            size = end - start
            pages.append({k:v for k,v in corpus[di].items() if k != 'text'} | {
                'article_token_start': start, 'article_token_end': end,
                'web_token_start': offset, 'web_token_end': offset + size})
            offset += size
        row = {k:v for k,v in section.items() if k != 'text'}
        row.update(pdf_text_sha256=hashlib.sha256(section['text'].encode()).hexdigest(),
                   web_text_sha256=hashlib.sha256(web_text.encode()).hexdigest(),
                   candidate_pages=pages,
                   corpus_fivegram_coverage_pct=100 * len(all_covered) / len(reference[si]) if reference[si] else None,
                   mapping_status='prose-candidate' if covered else 'title-only-candidate' if chosen else 'not-located',
                   **diff)
        result.append(row)
        print(f'section={section["id"]} candidates={len(chosen)} diff={diff["difference_pct"]}', flush=True)
    total_pdf = sum(r['pdf_tokens'] for r in result)
    total_web = sum(r['web_tokens'] for r in result)
    total_match = sum(r['matched_tokens'] for r in result)
    return {'corpus_pages_with_text': len(corpus), 'sections': result,
            'aggregate': {'sections': len(result), 'pdf_tokens': total_pdf, 'web_tokens': total_web,
                          'matched_tokens': total_match,
                          'weighted_difference_pct': 100 * (1 - 2*total_match/(total_pdf+total_web)),
                          'pdf_unmatched_pct': 100 * (1-total_match/total_pdf),
                          'sections_above_5pct': [r['id'] for r in result if r['difference_pct'] is not None and r['difference_pct'] > 5],
                          'sections_not_located': [r['id'] for r in result if r['mapping_status'] == 'not-located']}}


def run_source(source, sections):
    corpus = load_corpus('docs' if source == 'docs' else 'portal')
    fingerprint = hashlib.sha256(json.dumps([Path(__file__).read_text(), Path(compare.__file__).read_text(), sections,
                                           [{k:v for k,v in r.items() if k != 'text'} for r in corpus]],
                                           ensure_ascii=False).encode()).hexdigest()
    cache = BASE / 'raw' / (source + '-comparison.json')
    if cache.exists():
        recorded = json.loads(cache.read_text())
        if recorded['fingerprint'] == fingerprint:
            return recorded['result']
    result = compare_corpus(sections, corpus)
    audit.write_json(cache, {'fingerprint': fingerprint, 'result': result})
    return result


def main():
    sections = json.loads((BASE / 'raw/pdf-sections.json').read_text())
    sources = {}
    for source in ['docs', 'portal399']:
        print('source', source, flush=True)
        sources[source] = run_source(source, sections)
    data = {'pdf_manifest_url': 'https://github.com/konard/G-Ivan-A-mango_ba_prompts/blob/issue-401-be292b53210f/docs/taxonomy/cc-pdf-manifest.json',
            'threshold_pct': 5,
            'normalization': 'NFKC, lower-case, е/ё, soft-hyphen removal, line-break dehyphenation, alphanumeric tokens; numbers and negation retained',
            'retrieval': 'Exact 5-token shingles; product-scoped greedy complementary pages with >=5% marginal shingle gain (first >=1%); exact-title fallback for short summaries; candidates, not semantic matches',
            'section_alignment': 'Ordered matching blocks of >=5 tokens locate article windows. Window extends by unmatched PDF prefix/suffix lengths; external article text excluded. Without an anchor the whole candidate is retained.',
            'product_scopes': {'1-15,19-24': 'Contact Center desktop', '16': 'speech analytics including Quality Control embedded speech analytics', '17': 'role administration and PBX account', '18': 'role administration and Contact Center desktop'},
            'difference_formula': '100 * (1 - 2 * ordered_matched_tokens / (pdf_tokens + web_tokens)); SequenceMatcher autojunk=False',
            'aggregation': 'Sum token counts and matches over every exclusive PDF section, then apply formula; website text reused by sections is counted per alignment',
            'change_offsets': 'Zero-based normalized-token half-open intervals within PDF section and concatenated candidate article windows; article_token_start/end locate windows in original normalized article bodies',
            'limitations': ['Lexical difference includes heading/caption/table order and web additions within inferred section windows; it is not a semantic absence percentage.',
                           'Fivegram overlap and article candidates are retrieval evidence, not a statement of complete feature coverage.',
                           'Image-only text is not OCRed; visual completeness is unverified.',
                           'The issue 399 map is pinned; its article text is refreshed, not reconstructed historically.'],
            'sources': sources,
            'decision': ssot_decision([s['aggregate']['weighted_difference_pct'] for s in sources.values()])}
    audit.write_json(OUT / 'cc-source-comparison.json', data)
    print('summary', json.dumps({k:v['aggregate'] for k,v in sources.items()}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
