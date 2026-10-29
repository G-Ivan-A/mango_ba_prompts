"""Publish source provenance, representative extraction checks and section index."""
from collections import Counter
import hashlib
import json
from pathlib import Path
from urllib.parse import urlsplit
import audit

BASE = Path(__file__).resolve().parent
OUT = BASE.parents[1] / 'docs/taxonomy'
PUBLIC = 'https://github.com/konard/G-Ivan-A-mango_ba_prompts/blob/issue-401-be292b53210f/'


def main():
    rows = [json.loads(s) for s in (OUT/'docs.mango-map.jsonl').read_text().splitlines()]
    by_url = {r['url']: r for r in rows}
    prior = json.loads((OUT/'readability-checks.json').read_text())
    areas = []
    for area in prior['areas']:
        path = urlsplit(area['source_url']).path.removeprefix('/support/').rstrip('/')
        candidates = [audit.ORIGIN+'/ru/'+path+suffix for suffix in ('.html', '/index.html')]
        url = next(u for u in candidates if u in by_url)
        r = by_url[url]
        areas.append({'area': area['area'], 'source_url': url, 'title': r['title'],
                      'observed_at': r['observed_at'], 'source_sha256': r['source_sha256'],
                      'http_status': r['http_status'], 'article_text_chars': r['text_chars'],
                      'headings': r['headings'], 'tables': r['tables'],
                      'image_count': len(r['images']), 'readability': r['readability']})
    start = by_url[audit.ORIGIN+'/ru/1_nachat-zdes/index.html']
    checks = {'method': 'Static article extraction, table structure and image metadata; browser evidence is separate. No LLM accuracy evaluation or image download.',
              'areas': areas,
              'start_work': {'source_url': start['url']+'#nachat-rabotu',
                             'headings': start['headings'], 'http_status': start['http_status'],
                             'finding': 'Start work is an in-page heading, not a separately reachable page.'},
              'totals': {'pages': len(rows), 'readability': dict(Counter(r['readability'] for r in rows)),
                         'llm_readable': sum(r['is_llm_readable'] for r in rows),
                         'visual_context': sum(r['has_visual_context'] for r in rows),
                         'tables': sum(len(r['tables']) for r in rows),
                         'images': sum(len(r['images']) for r in rows)},
              'observation_range': {'first': min(r['observed_at'] for r in rows),
                                    'last': max(r['observed_at'] for r in rows)},
              'visual_limit': 'Image/SVG/canvas metadata may include decorative controls. Screenshot, diagram and image-only semantics remain unverified.'}
    audit.write_json(OUT/'docs-readability-checks.json', checks)
    pdf = json.loads((OUT/'cc-pdf-manifest.json').read_text())
    audit.write_json(OUT/'documentation-sources.json', {
        'issue_url': 'https://github.com/G-Ivan-A/mango_ba_prompts/issues/401',
        'parent_issue_url': 'https://github.com/G-Ivan-A/mango_ba_prompts/issues/399',
        'pdf': {k:pdf[k] for k in ['source_url', 'version', 'sha256', 'bytes', 'pages', 'extractor']},
        'historical_context': {'source_url': 'https://github.com/user-attachments/files/34130447/4.txt',
                               'sha256': hashlib.sha256((BASE/'raw/context.txt').read_bytes()).hexdigest(),
                               'use': 'Context only; not a product fact source; text is not republished.'},
        'baseline': json.loads((OUT/'portal-comparison-summary.json').read_text())['baseline_map_url'],
        'download_boundary': 'Only the explicit GitHub reference inputs are downloaded. Mango-hosted PDF, images, downloads, support, archives and obsolete versions are excluded before body reads.',
        'public_text_policy': 'Publish hashes, metadata, locators and token operations. Extracted full article/PDF text and inputs remain in ignored local cache/raw directories.'})
    comparison = json.loads((OUT/'cc-source-comparison.json').read_text())
    notes = [
        ('2.4.1', 'text-and-table-order', 'Performance descriptions differ in placement and amount; ordered text cannot certify parameter/cell equivalence.'),
        ('16.4', 'structural-and-wording', 'PDF lists three recording ingestion tabs; web lists settings including general settings. Exact title only; not evidence that ingestion was removed.'),
        ('16.6', 'baseline-map-gap-and-text-change', 'Embedded speech analytics page is in docs but not the pinned portal399 map. Web adds a prerequisite about configuring text analytics. Portal outside-map availability was not tested.'),
        ('17.1', 'matrix-alignment-unverified', 'Long PDF rights matrix has column-broken words; selected web report page is a partial candidate. Full role/cell equivalence is not established.'),
        ('17.6', 'unlocated-matrix', 'Version-switch navigation exists, but no reliable match for this PDF role matrix was located. Not a claim that the product feature is absent.'),
        ('17.7', 'unlocated-matrix', 'Widget pages exist, but no reliable match for this PDF role matrix was located. Not a claim that the product feature is absent.'),
        ('18', 'matrix-alignment-unverified', 'PDF covers more operations than selected report-page candidate. Word splitting and table order inflate lexical difference; semantic loss is not quantified.')]
    reviews = []
    for identifier, kind, observation in notes:
        evidence = {}
        for source, corpus in comparison['sources'].items():
            r = next(r for r in corpus['sections'] if r['id'] == identifier)
            evidence[source] = {'difference_pct': r['difference_pct'], 'mapping_status': r['mapping_status'],
                                'candidate_urls': [p['url'] for p in r['candidate_pages']]}
        r = next(r for r in comparison['sources']['docs']['sections'] if r['id'] == identifier)
        related = []
        if identifier in ('17.6', '17.7'):
            needle = 'смена версии' if identifier == '17.6' else 'виджеты'
            for row in rows:
                if not '/1_virtualnaya-ats-i-lichnyi-kabinet/' in row['url']:
                    continue
                cache = BASE/'cache'/(hashlib.sha256(row['url'].encode()).hexdigest()+'.json')
                if needle in json.loads(cache.read_text())['text'].lower():
                    related.append(row['url'])
        reviews.append({'pdf_id': identifier, 'pdf_url': r['source_url'],
                        'pdf_pages': [r['page_start'], r['page_end']], 'classification': kind,
                        'observation': observation, 'sources': evidence,
                        'related_docs_urls_not_equivalent_to_matrix': related,
                        'semantic_completeness_certified': False})
    audit.write_json(OUT/'cc-difference-checks.json', {
        'method': 'Manual review of bounded token-difference contexts and source structure; inspect_differences.py reproduces contexts locally.',
        'all_operations_url': PUBLIC+'docs/taxonomy/cc-source-comparison.json',
        'checks': reviews,
        'limit': 'Representative classifications do not replace the exhaustive lexical operation ledger; no image OCR or exhaustive role-matrix equivalence certification.'})
    other = {r['id']: r for r in comparison['sources']['portal399']['sections']}
    lines = ['---', 'status: review', 'version: 1.0', 'updated: 2026-10-29', 'temperature: 0.1', '---', '',
             '# КЦ: все разделы PDF и расхождения с двумя веб-источниками', '',
             'Метод и ограничения: '+PUBLIC+'docs/taxonomy/documentation-audit.md', '',
             'Машинные операции, хэши, интервалы токенов и страницы-кандидаты: '+PUBLIC+'docs/taxonomy/cc-source-comparison.json', '',
             'Каждый процент — лексическое расхождение. Кандидат и низкий процент не удостоверяют семантическую полноту. '
             '`not-located` означает отсутствие надёжного сопоставления в разрешённом снимке. '
             'Полнота изображений и матриц прав не подтверждена. Числа округлены только в этой таблице.', '',
             '| PDF: раздел, страницы, заголовок | docs, % | портал #399, % | docs: кандидаты | портал: кандидаты |',
             '| --- | ---: | ---: | --- | --- |']
    for r in comparison['sources']['docs']['sections']:
        p = other[r['id']]
        title = r['title'].replace('|', '\\|')
        def links(row):
            return '<br>'.join(f'[{i+1}]({c["url"]})' for i,c in enumerate(row['candidate_pages'])) or 'not-located'
        lines.append(f'| [{r["id"]}: стр. {r["page_start"]}–{r["page_end"]}, {title}]({r["source_url"]}) '
                     f'| {r["difference_pct"]:.2f} | {p["difference_pct"]:.2f} | {links(r)} | {links(p)} |')
    (OUT/'cc-section-differences.md').write_text('\n'.join(lines)+'\n')
    print('published checks, provenance and', len(other), 'section rows')


if __name__ == '__main__':
    main()
