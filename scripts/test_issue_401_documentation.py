"""Offline extraction and completeness regressions for issue 401."""
import json
import hashlib
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'experiments/issue_401'))
import audit
import compare
import build_comparison


class ExtractionTests(unittest.TestCase):
    def test_base_url_and_leading_page_are_not_lost(self):
        row = audit.parse_html('''<base href="../"><nav>Noise</nav>
        <h1>Documentation</h1><div class="dc-doc-leading-page__content">
        <a href="ru/3_produkty-i-prilozheniya/index.html">Products</a></div>''', audit.ROOT_URL)
        self.assertIn(audit.ORIGIN + '/ru/3_produkty-i-prilozheniya/index.html', row['discovered_links'])
        self.assertIn('Products', row['text'])
        self.assertNotIn('Noise', row['text'])

    def test_article_tables_and_cross_references(self):
        row = audit.parse_html('''<base href="../../../"><h1>API</h1>
        <div class="dc-doc-page__body"><p>Limit 10 requests</p>
        <table><tr><th>Method</th><th>Limit</th></tr><tr><td>call</td><td>10</td></tr></table>
        <img src="diagram.png"><a href="ru/5_api-i-razrabotka/index.html#limits">API</a></div>''',
                               audit.ORIGIN + '/ru/3_produkty-i-prilozheniya/p/index.html')
        self.assertEqual(row['tables'][0]['rows'][1], ['call', '10'])
        self.assertFalse(row['is_llm_readable'])
        self.assertEqual(row['content_links'], [audit.ORIGIN + '/ru/5_api-i-razrabotka/index.html'])

    def test_scope_excludes_files_support_archives_and_obsolete_versions(self):
        for path in ['/ru/7_podderzhka/index.html', '/ru/8_archiv/index.html',
                     '/ru/4_integratsii/6_arhiv-integratsii/index.html',
                     '/ru/5_api-i-razrabotka/8_ustarevshie_metody_api/index.html',
                     '/ru/3_produkty-i-prilozheniya/manual.PDF',
                     '/ru/3_produkty-i-prilozheniya/page.html?file=manual.pdf',
                     '/ru/3_produkty-i-prilozheniya/%2e%2e/7_podderzhka/index.html',
                     '/ru/3_produkty-i-prilozheniya/old_versions/index.html']:
            self.assertIsNotNone(audit.exclusion(audit.ORIGIN + path), path)
        self.assertIsNone(audit.exclusion(audit.ROOT_URL))
        self.assertIsNone(audit.exclusion(audit.ORIGIN + '/ru/6_administrirovanie/index.html'))

    def test_binary_response_body_is_never_read(self):
        class Response:
            status, url = 200, audit.ROOT_URL
            headers = {'Content-Type': 'application/pdf'}
            def __enter__(self): return self
            def __exit__(self, *args): pass
            def read(self, *args): raise AssertionError('binary body read')
        with patch.object(audit, 'open_url', return_value=Response()):
            self.assertIn('body not downloaded', audit.request(audit.ROOT_URL)['error'])

    def test_redirect_to_attachment_is_stopped_before_following(self):
        req = audit.Request(audit.ROOT_URL)
        with self.assertRaises(audit.ExcludedRedirect):
            audit.SafeRedirect().redirect_request(req, None, 302, '', {}, audit.ORIGIN + '/manual.pdf')


class ComparisonTests(unittest.TestCase):
    def test_other_products_cannot_supply_contact_center_evidence(self):
        section = {'id': '2', 'title': 'Users', 'text': 'Users may not delete other users without approval.'}
        foreign = {'url': audit.ORIGIN + '/ru/3_produkty-i-prilozheniya/10_sip-trunk/roles.html',
                   'title': 'Users', 'text': section['text'], 'source_sha256': 'x', 'text_sha256': 'x'}
        result = build_comparison.compare_corpus([section], [foreign])
        self.assertEqual(result['sections'][0]['candidate_pages'], [])

    def test_section_embedded_in_long_article_has_bounded_alignment(self):
        pdf = compare.tokens('The supervisor may inspect calls and change schedules after approval')
        web = compare.tokens('Unrelated navigation words ' * 20) + pdf + compare.tokens('Other report contents ' * 20)
        start, end = build_comparison.section_window(pdf, web)
        self.assertEqual(web[start:end], pdf)

    def test_changed_numbers_and_deleted_negation_are_differences(self):
        diff = compare.text_difference('Limit 10 requests. Do not delete users.',
                                       'Limit 100 requests. Do delete users.')
        self.assertGreater(diff['difference_pct'], 5)
        self.assertEqual(sum(o['pdf_tokens'] for o in diff['changes']), 2)

    def test_layout_normalization_only(self):
        self.assertEqual(compare.tokens('теле-\nфония Ёлка\u00ad'), compare.tokens('телефония елка'))
        self.assertNotEqual(compare.tokens('нет доступа'), compare.tokens('доступа'))

    def test_empty_and_unobserved_content_cannot_pass(self):
        self.assertIsNone(compare.text_difference('', '')['difference_pct'])
        self.assertEqual(compare.ssot_decision([None, 0]), 'combined-required-unverified')
        self.assertEqual(compare.ssot_decision([5, 5]), 'web-eligible-for-reference-product')
        self.assertEqual(compare.ssot_decision([5.00001, 0]), 'combined-required')

    def test_missing_web_section_keeps_a_traceable_deletion(self):
        diff = compare.text_difference('Role may not access settings', '')
        self.assertEqual(diff['difference_pct'], 100)
        self.assertEqual(sum(o['pdf_tokens'] for o in diff['changes']), diff['pdf_tokens'])


class PublishedEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.folder = ROOT/'docs/taxonomy'
        cls.rows = [json.loads(s) for s in (cls.folder/'docs.mango-map.jsonl').read_text().splitlines()]
        cls.mapping = {r['url']: r for r in cls.rows}
        cls.comparison = json.loads((cls.folder/'cc-source-comparison.json').read_text())
        cls.manifest = json.loads((cls.folder/'cc-pdf-manifest.json').read_text())

    def test_crawl_closes_frontier_and_preserves_metadata_contract(self):
        summary = json.loads((self.folder/'docs-crawl-summary.json').read_text())
        self.assertEqual(summary['pages'], len(self.mapping))
        self.assertEqual(len(self.rows), len(self.mapping))
        self.assertEqual(summary['frontier_remaining'], 0)
        self.assertEqual(summary['errors'], [])
        self.assertEqual(summary['unrecognized_templates'], [])
        self.assertEqual(sum(summary['sections'].values())+1, len(self.rows))
        for row in self.rows:
            self.assertIsNone(audit.exclusion(row['url']))
            self.assertEqual(row['http_status'], 200)
            self.assertTrue(row['body_found'])
            self.assertEqual(row['hierarchy'][-1]['url'], row['url'])
            self.assertTrue(all(p['url'].startswith(audit.ORIGIN+'/ru/') for p in row['hierarchy']))
            self.assertIn(row['content_type'], ['API spec', 'instruction', 'product-documentation'])
            self.assertTrue(row['tags'])
            self.assertTrue(all(k in row['relevance_for_BA'] for k in ['FT', 'NFT', 'integrations']))
            self.assertIsInstance(row['is_llm_readable'], bool)
            self.assertIsInstance(row['has_visual_context'], bool)
            self.assertEqual(row['update_frequency']['value'], 'unknown')
            self.assertTrue(all(u.startswith(('https://', 'http://')) for u in row['cross_references']))

    def test_every_pdf_page_toc_entry_and_section_is_accounted_for(self):
        m = self.manifest
        self.assertEqual(m['pages'], 590)
        self.assertEqual([p['page'] for p in m['page_extraction']], list(range(1, 591)))
        identifiers = {s['id'] for s in m['sections']}
        self.assertEqual(len(identifiers), len(m['sections']))
        self.assertEqual(len(identifiers), 194)
        self.assertTrue({s['id'] for s in m['toc']} <= identifiers)
        for source in self.comparison['sources'].values():
            self.assertEqual({r['id'] for r in source['sections']}, identifiers)
        self.assertTrue(all(p['text_chars'] > 0 for p in m['page_extraction']))

    def test_all_changes_balance_and_recompute_the_decision(self):
        differences = []
        for source in self.comparison['sources'].values():
            rows = source['sections']
            a = source['aggregate']
            for field in ['pdf_tokens', 'web_tokens', 'matched_tokens']:
                self.assertEqual(sum(r[field] for r in rows), a[field])
            for row in rows:
                for side in ['pdf', 'web']:
                    changed = sum(o[side+'_tokens'] for o in row['changes'])
                    self.assertEqual(row[side+'_tokens']-changed, row['matched_tokens'])
                    for operation in row['changes']:
                        self.assertTrue(0 <= operation[side+'_start'] <= operation[side+'_end'] <= row[side+'_tokens'])
                self.assertAlmostEqual(row['difference_pct'], 100*(1-2*row['matched_tokens']/(row['pdf_tokens']+row['web_tokens'])))
                self.assertEqual(sum(p['article_token_end']-p['article_token_start'] for p in row['candidate_pages']), row['web_tokens'])
            difference = 100*(1-2*a['matched_tokens']/(a['pdf_tokens']+a['web_tokens']))
            self.assertAlmostEqual(difference, a['weighted_difference_pct'])
            self.assertEqual(a['sections_above_5pct'], [r['id'] for r in rows if r['difference_pct'] > 5])
            differences.append(difference)
        self.assertEqual(compare.ssot_decision(differences), self.comparison['decision'])
        self.assertEqual(self.comparison['decision'], 'combined-required')

    def test_candidates_retain_source_hashes_and_product_boundaries(self):
        portal = {r['url']: r for r in map(json.loads, (self.folder/'portal-comparison-audit.jsonl').read_text().splitlines())}
        manifest = {r['id']:r for r in self.manifest['sections']}
        for name, source in self.comparison['sources'].items():
            mapping = self.mapping if name == 'docs' else portal
            for row in source['sections']:
                self.assertEqual(row['pdf_text_sha256'], manifest[row['id']]['text_sha256'])
                self.assertEqual(row['source_url'], manifest[row['id']]['source_url'])
                for candidate in row['candidate_pages']:
                    observed = mapping[candidate['url']]
                    self.assertEqual(candidate['source_sha256'], observed['source_sha256'])
                    self.assertEqual(candidate['text_sha256'], observed['text_sha256'])
                    self.assertTrue(build_comparison.product_scope(row['id'], candidate['url']))
        summary = json.loads((self.folder/'portal-comparison-summary.json').read_text())
        self.assertEqual(summary['baseline_map_sha256'], hashlib.sha256((self.folder/'portal-map.jsonl').read_bytes()).hexdigest())

    def test_browser_probe_and_section_index_cover_required_inputs(self):
        browser = json.loads((self.folder/'docs-browser-checks.json').read_text())
        self.assertTrue(browser['javascript_disabled'])
        self.assertTrue(browser['asset_requests_blocked'])
        self.assertEqual(len(browser['pages']), 6)
        self.assertTrue(all(p['status'] == 200 and p['body_found'] for p in browser['pages']))
        self.assertEqual(browser['cross_origin_fetch']['type'], 'cors')
        index = (self.folder/'cc-section-differences.md').read_text()
        for section in self.manifest['sections']:
            self.assertIn('| ['+section['id']+': стр.', index)
        checks = json.loads((self.folder/'docs-readability-checks.json').read_text())
        self.assertTrue(checks['start_work']['source_url'].endswith('#nachat-rabotu'))
        self.assertEqual(checks['totals']['pages'], len(self.rows))


if __name__ == '__main__':
    unittest.main()
