"""Offline regressions for portal evidence and product routing (issue 399)."""
import importlib.util
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import URLError


def load_route():
    spec = importlib.util.spec_from_file_location('portal_route', ROOT / 'experiments/issue_399/route.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('portal_audit', ROOT / 'experiments/issue_399/audit.py')
audit = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit)


class AuditTests(unittest.TestCase):
    def test_files_tickets_and_downloads_are_never_fetched(self):
        for url in ('https://www.mango-office.ru/x.pdf',
                    'https://www.mango-office.ru/support/8_archiv/',
                    'https://www.mango-office.ru/support/7_podderzhka/',
                    'https://www.mango-office.ru/support/download/setup.exe',
                    'https://example.com/support/page/'):
            self.assertIsNotNone(audit.exclusion(url))
        self.assertIsNone(audit.exclusion('https://www.mango-office.ru/support/5_api-i-razrabotka/'))

    def test_content_extraction_preserves_table_structure_and_flags_visual_blindness(self):
        doc = audit.parse_html('''<nav><img src="logo.png"><a href="/support/noise/">Noise</a></nav>
        <h1>API</h1><div class="dc-doc-page__body"><h2 id="limits">Limits</h2>
        <table><tr><th>Method</th><th>Limit</th></tr><tr><td>call</td><td>10</td></tr></table>
        <img src="/diagram.png" alt=""><a href="/support/real/">Real</a></div>''', audit.ROOT_URL)
        self.assertEqual(doc['tables'][0]['rows'], [['Method', 'Limit'], ['call', '10']])
        self.assertEqual(len(doc['images']), 1)
        self.assertFalse(doc['is_llm_readable'])
        self.assertEqual(doc['readability'], 'visual-review-required')
        self.assertIn('https://www.mango-office.ru/support/real/', doc['content_links'])
        self.assertNotIn('https://www.mango-office.ru/support/noise/', doc['content_links'])

    def test_text_only_content_is_readable_without_javascript(self):
        doc = audit.parse_html('<h1>Text</h1><div class="dc-doc-page__body"><p>Readable instructions.</p></div>', audit.ROOT_URL)
        self.assertTrue(doc['is_llm_readable'])
        self.assertFalse(doc['has_visual_context'])

    def test_fragment_normalization_and_binary_query_exclusion(self):
        self.assertEqual(audit.normalize('/support/a/#x', audit.ROOT_URL),
                         'https://www.mango-office.ru/support/a/')
        self.assertIsNotNone(audit.exclusion('https://www.mango-office.ru/support/a/?file=manual.pdf'))

    def test_table_without_headers_or_with_merged_cells_requires_review(self):
        for table in ('<tr><td>A</td><td>1</td></tr>', '<tr><th colspan="2">A</th></tr>'):
            doc = audit.parse_html('<div class="dc-doc-page__body"><table>'+table+'</table></div>', audit.ROOT_URL)
            self.assertFalse(doc['is_llm_readable'])
            self.assertEqual(doc['readability'], 'table-review-required')

    def test_non_html_body_and_forbidden_redirect_are_not_downloaded(self):
        class Response:
            status, url = 200, 'https://www.mango-office.ru/support/manual/'
            headers = {'Content-Type': 'application/pdf'}

            def __enter__(self):
                return self

            def __exit__(self, *args):
                pass

            def read(self, *args):
                raise AssertionError('Binary response body must not be read')

        with tempfile.TemporaryDirectory() as tmp, patch.object(audit, 'BASE', Path(tmp)), patch.object(audit, 'build_opener') as opener:
            opener.return_value.open.return_value = Response()
            row = audit.fetch(Response.url)
            self.assertIn('body not downloaded', row['error'])
        request = audit.Request(Response.url)
        with self.assertRaises(URLError):
            audit.SafeRedirect().redirect_request(request, None, 302, '', {}, '/support/download/manual.pdf')


class RoutingTests(unittest.TestCase):
    def pages(self):
        # Same symptom spans independent clients and a connector; the wrong
        # connector has a better lexical match and must still be excluded.
        return [dict(url='https://www.mango-office.ru/support/'+str(i)+'/', title=title,
                     portal_product=product, connector_id=connector, http_status=200,
                     taxonomy_matches=[], is_llm_readable=readable)
                for i, (title, product, connector, readable) in enumerate([
                    ('API status session', 'api', None, True),
                    ('WFM рабочее время пунктуальность', 'cc-desktop', None, False),
                    ('Вход и статус web-КЦ', 'cc-web', None, False),
                    ('Права пользователя ЛК', 'pbx-account', None, True),
                    ('Ролевая модель', 'administration', None, True),
                    ('amoCRM настройка', 'integrations', 'amocrm', False),
                    ('BPMSoft WFM статус API session', 'integrations', 'bpmsoft', True)])]

    def test_api_word_does_not_erase_wfm_clients_or_requested_connector(self):
        result = load_route().select_pages(self.pages(), 'WFM статус API amoCRM')
        products = {p['portal_product'] for p in result['pages']}
        self.assertTrue({'cc-desktop', 'cc-web', 'pbx-account', 'api', 'administration', 'integrations'} <= products)
        self.assertFalse(any(p['connector_id'] == 'bpmsoft' for p in result['pages']))
        self.assertEqual(result['evidence_status'], 'locators-only')

    def test_visual_page_requires_targeted_fallback_without_assuming_image_descriptions(self):
        result = load_route().select_pages(self.pages(), 'WFM статус API')
        self.assertTrue(result['fallback_required'])
        self.assertIn('description-not-guaranteed', result['fallback']['image_semantics'])
        self.assertEqual(result['question_owner']['as_is'], 'product-team-or-documentation-owner')

    def test_missing_product_or_connector_is_an_explicit_gap(self):
        result = load_route().select_pages(self.pages()[:1], 'WFM API amoCRM')
        self.assertIn('cc-desktop', result['coverage_gaps'])
        self.assertIn('connector:amocrm', result['coverage_gaps'])

    def test_status_entity_and_multiple_explicit_products_survive_ranking(self):
        rows = self.pages()
        rows += [dict(rows[0], url='https://www.mango-office.ru/support/api-wrong/',
                      title='API Изменить статус индивидуальных правил автосекретаря'),
                 dict(rows[0], url='https://www.mango-office.ru/support/cc-status/',
                      title='Смена статуса пользователя КЦ'),
                 dict(rows[0], url='https://www.mango-office.ru/support/sip/',
                      title='SIP Trunk', portal_product='sip-trunk'),
                 dict(rows[0], url='https://www.mango-office.ru/support/speech/',
                      title='Речевая аналитика', portal_product='speech-analytics')]
        route = load_route()
        result = route.select_pages(rows, 'WFM статус API', limit=1)
        api_page = next(p for p in result['pages'] if p['portal_product'] == 'api')
        self.assertEqual(api_page['title'], 'Смена статуса пользователя КЦ')
        result = route.select_pages(rows, 'SIP Trunk речевая аналитика', limit=2)
        self.assertEqual({p['portal_product'] for p in result['pages']}, {'sip-trunk', 'speech-analytics'})


class CatalogTests(unittest.TestCase):
    def test_compact_index_selects_exact_snapshot_ranges(self):
        # A stale index silently sends a prompt to another product's records.
        # Verify the published index against the actual snapshot, not the builder.
        folder = ROOT/'docs/taxonomy'
        content = (folder/'portal-map.jsonl').read_bytes()
        rows = [json.loads(line) for line in content.splitlines()]
        index = json.loads((folder/'portal-index.json').read_text())
        self.assertEqual(index['map_sha256'], hashlib.sha256(content).hexdigest())
        covered = []
        for product in index['products']:
            positions = [i for start, end in product['record_ranges_1_based']
                         for i in range(start, end+1)]
            self.assertEqual(len(positions), product['page_count'])
            self.assertEqual({rows[i-1]['portal_product'] for i in positions}, {product['portal_product']})
            self.assertIn(product['entry_url'], {rows[i-1]['url'] for i in positions})
            covered.extend(positions)
        self.assertEqual(sorted(covered), list(range(1, len(rows)+1)))
        catalog = json.loads((folder/'products.json').read_text())
        self.assertEqual({c['id'] for c in index['capabilities']},
                         {n['id'] for n in catalog['nodes'] if n['level'] == 'Capability'})

    def test_four_levels_preserve_historical_inventory_and_valid_paths(self):
        baseline = json.loads((ROOT/'experiments/issue_399/baseline.json').read_text())
        catalog = json.loads((ROOT/'docs/taxonomy/products.json').read_text())
        levels = ['Domain', 'Capability', 'Feature', 'Atomic Function']
        self.assertEqual(catalog['levels'], levels)
        nodes = {n['id']: n for n in catalog['nodes']}
        self.assertEqual(len(nodes), len(catalog['nodes']))
        for node in nodes.values():
            self.assertIn(node['level'], levels)
            for parent in node['parent_ids']:
                self.assertEqual(levels.index(nodes[parent]['level'])+1, levels.index(node['level']))
            self.assertTrue(node['source_urls'])
            if node['level'] != 'Domain':
                self.assertTrue(node['parent_ids'])
        for cap in baseline['capabilities']:
            self.assertIn(cap['id'], nodes)
            for feature in cap['features']:
                self.assertIn(cap['id']+'/feature/'+feature, nodes)
            for function in cap['atomic_functions']:
                node = nodes[cap['id']+'/function/'+function['id']]
                self.assertEqual(node['params'], function['params'])
        for feature in (n for n in nodes.values() if n['level'] == 'Feature'):
            self.assertTrue(any(feature['id'] in n['parent_ids'] for n in nodes.values()), feature['id'])

    def test_complete_snapshot_and_provenance_for_every_curated_operation(self):
        folder = ROOT/'docs/taxonomy'
        summary = json.loads((folder/'crawl-summary.json').read_text())
        audit_rows = [json.loads(s) for s in (folder/'portal-audit.jsonl').read_text().splitlines()]
        mapping = [json.loads(s) for s in (folder/'portal-map.jsonl').read_text().splitlines()]
        by_url = {r['url']: r for r in audit_rows}
        self.assertEqual(summary['frontier_remaining'], 0)
        self.assertEqual(summary['pages'], len(by_url))
        self.assertEqual(set(by_url), {m['url'] for m in mapping})
        for row in mapping:
            self.assertIsNone(audit.exclusion(row['url']))
            self.assertEqual(row['update_frequency']['value'], 'unknown')
            self.assertEqual(row['is_llm_readable'], audit.assess_readability(by_url[row['url']])['is_llm_readable'])
            for link in row['cross_product_links']:
                self.assertIn(link['target_url'], by_url)
                self.assertNotEqual(row['portal_product'], link['target_product'])
        catalog = json.loads((folder/'products.json').read_text())
        for node in catalog['nodes']:
            if node['origin'] == 'portal-update':
                for url in node['source_urls']:
                    self.assertEqual(by_url[url]['http_status'], 200)
                    self.assertTrue(by_url[url]['body_found'])


if __name__ == '__main__':
    unittest.main()
