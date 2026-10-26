"""Standards onboarding acceptance checks and scope preservation (issue 395)."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib
import json
import re
import unittest
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1]


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
        self.assertEqual(parser.nav, ['catalog', 'standards', 'dashboard', 'processes'])
        self.assertEqual(set(parser.articles), set('12345678'))
        self.assertEqual(parser.targets, list('12345678'))
        for number, article in parser.articles.items():
            with self.subTest(section=number):
                self.assertGreaterEqual(article['criteria'], 3)
                self.assertTrue(article['links'])
                self.assertTrue(all(url.startswith('https://') for url in article['links']))
        self.assertIn('"standards"', (ROOT / 'site/app.js').read_text())

    def test_terms_and_stage_context_are_present(self):
        html = (ROOT / 'site/index.html').read_text()
        terms = ['Измеримая цель', 'Включено', 'Не включено', 'Дельта',
                 'Необходимо и достаточно', '5±2', 'EARS', 'ФТ ↔ ОРР ↔ UC',
                 '100%', 'L1 ФДР', 'L2 ТС', 'Характеристики качества',
                 'A-IN', 'A-CORE', 'A-WORK', 'Г-IN', 'Г-С1', 'Г-W',
                 'BABOK', 'IREB', 'ISO/IEC 25010:2023', 'arc42']
        for term in terms:
            with self.subTest(term=term):
                self.assertTrue(term in html, term)

    def test_existing_sections_gate_and_standards_remain_identical(self):
        baseline = json.loads((ROOT / 'experiments/issue_395/site-baseline.json').read_text())
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
        for href in re.findall(r'href="([^"]+)"', section):
            self.assertTrue(href.startswith('https://'), href)
            prefix = '/G-Ivan-A/mango_ba_prompts/blob/main/'
            url = urlsplit(href)
            if url.netloc == 'github.com' and url.path.startswith(prefix):
                self.assertTrue((ROOT / unquote(url.path[len(prefix):])).is_file(), href)


if __name__ == '__main__':
    unittest.main()
