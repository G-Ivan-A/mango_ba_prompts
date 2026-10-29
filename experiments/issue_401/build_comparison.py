"""Compare every extracted PDF section to both recorded HTML corpora.

Corpus-wide exact 5-token retrieval finds candidates across navigation branches.
Greedy complementary candidates support sections split over several web pages.
The ordered token diff reports lexical changes, not semantic missing features.
Full texts remain ignored; published operations contain offsets and counts.
"""
from collections import Counter, defaultdict
from difflib import SequenceMatcher
import hashlib
import json
from pathlib import Path
import audit
from compare import tokens, text_difference, ssot_decision

BASE = Path(__file__).resolve().parent
OUT = BASE.parents[1] / 'docs/taxonomy'


def grams(ts):
    return {tuple(ts[i:i+5]) for i in range(max(0, len(ts)-4))}


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
        candidates = hits[si]
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
        def order(di):
            return SequenceMatcher(None, ref_tokens[si], all_tokens[di], autojunk=False).find_longest_match().a
        chosen.sort(key=lambda d: (order(d), corpus[d]['url']))
        # Whole articles are compared: extra web navigation/captions count as additions.
        web_text = '\n'.join(corpus[d]['text'] for d in chosen)
        diff = text_difference(section['text'], web_text)
        covered = set().union(*(grams(all_tokens[d]) & reference[si] for d in chosen)) if chosen else set()
        all_covered = set().union(*(gs for gs in hits[si].values()), covered)
        # hits was consumed during greedy selection; union with chosen restores the whole corpus union.
        row = {k:v for k,v in section.items() if k != 'text'}
        row.update(pdf_text_sha256=hashlib.sha256(section['text'].encode()).hexdigest(),
                   web_text_sha256=hashlib.sha256(web_text.encode()).hexdigest(),
                   candidate_pages=[{k:v for k,v in corpus[d].items() if k != 'text'} for d in chosen],
                   corpus_fivegram_coverage_pct=100 * len(all_covered) / len(reference[si]) if reference[si] else None,
                   mapping_status='candidate-located' if covered else 'not-located',
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


def main():
    sections = json.loads((BASE / 'raw/pdf-sections.json').read_text())
    sources = {}
    for source in ['docs', 'portal399']:
        print('source', source, flush=True)
        sources[source] = compare_corpus(sections, load_corpus('docs' if source == 'docs' else 'portal'))
    data = {'pdf_manifest_url': 'https://github.com/konard/G-Ivan-A-mango_ba_prompts/blob/issue-401-be292b53210f/docs/taxonomy/cc-pdf-manifest.json',
            'threshold_pct': 5,
            'normalization': 'NFKC, lower-case, е/ё, soft-hyphen removal, line-break dehyphenation, alphanumeric tokens; numbers and negation retained',
            'retrieval': 'Exact 5-token shingles over all permitted text pages; greedy complementary pages with >=5% marginal shingle gain (first >=1%); candidates, not semantic matches',
            'difference_formula': '100 * (1 - 2 * ordered_matched_tokens / (pdf_tokens + web_tokens)); SequenceMatcher autojunk=False',
            'aggregation': 'Sum token counts and matches over every exclusive PDF section, then apply formula; website text reused by sections is counted per alignment',
            'change_offsets': 'Zero-based normalized-token half-open intervals within PDF section and ordered concatenation of candidate_pages; full article bodies, excluding titles/navigation',
            'limitations': ['Lexical difference includes heading/caption/table order and web additions; it is not a semantic absence percentage.',
                           'Fivegram overlap and article candidates are retrieval evidence, not a statement of complete feature coverage.',
                           'Image-only text is not OCRed; visual completeness is unverified.',
                           'The issue 399 map is pinned; its article text is refreshed, not reconstructed historically.'],
            'sources': sources,
            'decision': ssot_decision([s['aggregate']['weighted_difference_pct'] for s in sources.values()])}
    audit.write_json(OUT / 'cc-source-comparison.json', data)
    print('summary', json.dumps({k:v['aggregate'] for k,v in sources.items()}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
