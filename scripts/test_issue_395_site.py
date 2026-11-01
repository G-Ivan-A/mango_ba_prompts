"""Standards onboarding acceptance checks and scope preservation (issue 395)."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib
import json
import re
import unittest
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1]
OVERRIDES = 'experiments/issue_413/site-baseline-overrides.json'


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.articles = {}
        self.current = None
        self.targets = []
        self.nav = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'data-nav' in attrs:
            self.nav.append(attrs['data-nav'])
        if 'data-standard-target' in attrs:
            self.targets.append(attrs['data-standard-target'])
        if 'data-bcreq-section' in attrs:
            self.current = attrs['data-bcreq-section']
            self.articles[self.current] = {'criteria': 0, 'links': []}
        if self.current:
            if tag == 'li':
                self.articles[self.current]['criteria'] += 1
            if tag == 'a':
                self.articles[self.current]['links'].append(attrs['href'])

    def handle_endtag(self, tag):
        if tag == 'article':
            self.current = None


class StandardsTests(unittest.TestCase):
    def test_eight_sections_have_checklists_and_absolute_sources(self):
        html = (ROOT / 'site/index.html').read_text()
        parser = PageParser()
        parser.feed(html)
        # Issue #423 publishes the menu of PR #422 (RFC standards page v0.2).
        self.assertEqual(parser.nav, ['about', 'catalog', 'standards', 'processes', 'dashboard', 'glossary'])
        self.assertEqual(set(parser.articles), set('12345678'))
        # Intro (0) and section cards 1–8 are reachable from the standards page.
        self.assertEqual(set(parser.targets), set('012345678'))
        terms = set(re.findall(r'id="term-([^"]+)"', html))
        for number, article in parser.articles.items():
            with self.subTest(section=number):
                self.assertGreaterEqual(article['criteria'], 3)
                self.assertTrue(any(url.startswith('https://') for url in article['links']))
                for url in article['links']:
                    if url.startswith('#glossary?term='):
                        self.assertIn(url.split('=', 1)[1], terms, url)
                    else:
                        self.assertTrue(url.startswith('https://'), url)
        self.assertIn('"standards"', (ROOT / 'site/app.js').read_text())

    def test_terms_and_stage_context_are_present(self):
        html = (ROOT / 'site/index.html').read_text()
        # Issue #423: the page text is the v0.2 template approved in PR #422
        # (docs/rfc/2026-10-standards-page-rfc.md); the RFC drops EARS, «3.N»,
        # «Коротко» and «за одну минуту» from the page.
        terms = ['5±2', 'A-IN', 'A-CORE', 'A-WORK', 'Г-IN', 'Г-С1', 'Г-W',
                 'BABOK', 'IREB', 'ISO/IEC 25010:2023']
        for term in terms:
            with self.subTest(term=term):
                self.assertTrue(term in html, term)
        for phrase in ['EARS', '3.N', 'Коротко', 'за одну минуту']:
            with self.subTest(forbidden=phrase):
                self.assertNotIn(phrase, html)

    def test_existing_sections_gate_and_standards_remain_identical(self):
        baseline = json.loads((ROOT / 'experiments/issue_395/site-baseline.json').read_text())
        # Intentional later changes are pinned by their own issue; the #395
        # baseline itself is historical evidence and stays unchanged.
        overrides = json.loads((ROOT / OVERRIDES).read_text())
        for kind in ('files', 'sections'):
            for name, entry in overrides[kind].items():
                self.assertIn(name, baseline[kind], f'{OVERRIDES}: {name} не из baseline #395')
                self.assertTrue(entry['reason'].startswith('#'), name)
                baseline[kind][name] = entry['sha256']
        for name, digest in baseline['files'].items():
            with self.subTest(file=name):
                self.assertEqual(hashlib.sha256((ROOT / name).read_bytes()).hexdigest(), digest)
        sections = re.findall(r'<section\b.*?</section>', (ROOT / 'site/index.html').read_text(), re.S)
        actual = {re.search(r'\bid="([^"]+)"', part).group(1): part for part in sections}
        for name, digest in baseline['sections'].items():
            self.assertEqual(hashlib.sha256(actual[name].encode()).hexdigest(), digest, name)

    def test_new_page_sources_resolve_to_real_repository_files(self):
        html = (ROOT / 'site/index.html').read_text()
        section = re.search(r'<section class="page-band standards-band".*?</section>', html, re.S).group()
        terms = set(re.findall(r'id="term-([^"]+)"', html))
        for href in re.findall(r'href="([^"]+)"', section):
            if href.startswith('#glossary?term='):
                self.assertIn(href.split('=', 1)[1], terms, href)
                continue
            if href.startswith('#standards?section='):
                self.assertIn(href.split('=', 1)[1], set('012345678'), href)
                continue
            self.assertTrue(href.startswith('https://'), href)
            prefix = '/G-Ivan-A/mango_ba_prompts/blob/main/'
            url = urlsplit(href)
            if url.netloc == 'github.com' and url.path.startswith(prefix):
                self.assertTrue((ROOT / unquote(url.path[len(prefix):])).is_file(), href)


if __name__ == '__main__':
    unittest.main()
