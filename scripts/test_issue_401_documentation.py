"""Offline extraction and completeness regressions for issue 401."""
import importlib.util
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'experiments/issue_401'))
import audit
import compare


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


if __name__ == '__main__':
    unittest.main()
