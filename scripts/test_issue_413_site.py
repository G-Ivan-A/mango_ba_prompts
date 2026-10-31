"""Stage 1 launch on the site: four stages, launch steps, next steps (issue #413).

The site section «Дорожная карта» and the dashboard stage lane are a projection
of `docs/roadmap.md` (standards/pages-ux-standard.md, rules U10–U12). These
tests parse the Markdown source independently of the generator and compare it
with the committed `site/data/*.json`, so a stale or hand-edited data file fails.
"""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "docs/roadmap.md"
SITE = "https://g-ivan-a.github.io/mango_ba_prompts/"
BLOB = "/G-Ivan-A/mango_ba_prompts/blob/main/"
ISSUES = "https://github.com/G-Ivan-A/mango_ba_prompts/issues/"


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def strip_inline(value):
    value = re.sub(r"\[([^\]]+)]\([^)]+\)", r"\1", value)
    value = re.sub(r"`([^`]+)`", r"\1", value)
    return re.sub(r"\*\*([^*]+)\*\*", r"\1", value).strip()


def table(markdown, first, second):
    lines = markdown.splitlines()
    for index, line in enumerate(lines):
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if line.startswith("|") and cells[:2] == [first, second]:
            rows = []
            for row in lines[index + 2:]:
                if not row.startswith("|"):
                    break
                rows.append([c.strip() for c in row.strip().strip("|").split("|")])
            return rows
    raise AssertionError(f"{SOURCE}: no table «{first} | {second}»")


def split_number(title):
    match = re.match(r"^(\d+)\.\s*(.+)$", strip_inline(title))
    return int(match.group(1)), match.group(2)


class LinkCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.nav = {}
        self.current_nav = None
        self.hrefs = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "data-nav" in attrs:
            self.current_nav = attrs["data-nav"]
            self.nav[self.current_nav] = ""
        if tag == "a" and "href" in attrs:
            self.hrefs.append(attrs["href"])

    def handle_data(self, data):
        if self.current_nav:
            self.nav[self.current_nav] += data.strip()

    def handle_endtag(self, tag):
        if tag == "a":
            self.current_nav = None


def site_pages():
    match = re.search(r"const PAGES = \[([^\]]+)]", read("site/app.js"))
    return re.findall(r'"([a-z-]+)"', match.group(1))


class RoadmapSiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.markdown = read(SOURCE)
        cls.roadmap = json.loads(read("site/data/roadmap.json"))
        cls.stats = json.loads(read("site/data/stats.json"))
        html = read("site/index.html")
        cls.section = re.search(r'<section\b[^>]*\bid="roadmap".*?</section>', html, re.S).group()

    def assert_link_resolves(self, url):
        parts = urlsplit(url)
        if url.startswith(SITE):
            page = parts.fragment
            self.assertTrue(page == "" or page in site_pages(),
                            f"{url}: #{page} is not a site page; the router would show the catalog")
        elif parts.netloc == "github.com" and parts.path.startswith(BLOB):
            relative = unquote(parts.path[len(BLOB):]).rstrip("/")
            self.assertTrue((ROOT / relative).exists(), url)
        else:
            self.assertTrue(url.startswith("https://"), url)

    def test_generator_reads_roadmap_source(self):
        generator = read("scripts/generate-pages-data.mjs")
        self.assertIn('roadmap: "docs/roadmap.md"', generator)
        self.assertIn("parseRoadmap(roadmapMarkdown)", generator)
        self.assertEqual(self.roadmap["sourceFiles"][0]["path"], SOURCE)
        for source in self.roadmap["sourceFiles"]:
            self.assert_link_resolves(source["url"])

    def test_four_stages_match_source_with_entry_and_exit(self):
        rows = table(self.markdown, "Этап", "Как работает")
        self.assertEqual(len(rows), 4)
        levels = self.roadmap["levels"]
        self.assertEqual([level["id"] for level in levels], ["stage-1", "stage-2", "stage-3", "stage-4"])
        for row, level in zip(rows, levels):
            with self.subTest(stage=level["id"]):
                number, title = split_number(row[0])
                self.assertEqual((level["number"], level["title"]), (number, title))
                self.assertEqual(level["howItWorks"], strip_inline(row[1]))
                self.assertEqual(level["baRole"], strip_inline(row[2]))
                self.assertEqual(level["entry"], strip_inline(row[3]))
                self.assertEqual(level["exitCriteria"], strip_inline(row[4]))
                self.assertEqual(level["status"], row[5])
                for link in level["links"]:
                    self.assert_link_resolves(link["url"])
        self.assertEqual([level["status"] for level in levels],
                         ["current", "planned", "planned", "planned"])
        self.assertIn("n8n", levels[2]["title"])

    def test_launch_steps_match_source_and_links_resolve(self):
        rows = table(self.markdown, "Шаг запуска", "Что сделать")
        launch = self.roadmap["launch"]
        self.assertEqual(len(launch), len(rows))
        self.assertGreaterEqual(len(launch), 5)
        for row, step in zip(rows, launch):
            with self.subTest(step=step["number"]):
                self.assertEqual((step["number"], step["step"]), split_number(row[0]))
                self.assertEqual(step["action"], strip_inline(row[1]))
                self.assertEqual(step["result"], strip_inline(row[3]))
                for link in step["links"]:
                    self.assert_link_resolves(link["url"])
        urls = [link["url"] for step in launch for link in step["links"]]
        self.assertIn(SITE + "#processes", urls)
        self.assertIn(ISSUES + "new/choose", urls)

    def test_launch_names_existing_issue_templates(self):
        templates = "\n".join(p.read_text(encoding="utf-8")
                              for p in (ROOT / ".github/ISSUE_TEMPLATE").glob("*.yml"))
        actions = " ".join(step["action"] for step in self.roadmap["launch"])
        for name in re.findall(r"«([^»]+)»", actions):
            if name.startswith(("Прогон", "Фидбек")):
                with self.subTest(template=name):
                    self.assertIn(name, templates)

    def test_next_steps_match_source(self):
        rows = table(self.markdown, "Следующий шаг", "Почему важен")
        gaps = self.roadmap["gaps"]
        self.assertEqual([gap["gap"] for gap in gaps], [strip_inline(row[0]) for row in rows])
        for gap in gaps:
            for link in gap["links"]:
                self.assert_link_resolves(link["url"])

    def test_dashboard_stage_lane_has_four_stages_from_roadmap(self):
        phases = self.stats["phases"]
        self.assertEqual([p["id"] for p in phases], ["prompts", "agents", "n8n", "server"])
        titles = [level["title"] for level in self.roadmap["levels"]]
        self.assertEqual([p["title"] for p in phases], titles)
        self.assertEqual([p["status"] for p in phases],
                         [level["status"] for level in self.roadmap["levels"]])
        for phase in phases[1:]:
            with self.subTest(phase=phase["id"]):
                metrics = {m["label"]: m["value"] for m in phase["metrics"]}
                # The process does not change between stages; a person decides at gates.
                self.assertEqual(metrics.get("гейты"), "человек")
                self.assertNotIn("human gates", metrics)
        app = read("site/app.js")
        self.assertNotIn('"multiagents"', app)
        self.assertIn("repeat(4, minmax(0, 1fr))", re.search(r"\.phase-lane \{[^}]+\}", read("site/styles.css")).group())

    def test_navigation_and_section_markup(self):
        parser = LinkCollector()
        parser.feed(read("site/index.html"))
        self.assertEqual(parser.nav.get("roadmap"), "Дорожная карта")
        self.assertIn("roadmap", site_pages())
        for needle in ('id="roadmap-levels"', 'id="roadmap-launch-steps"', 'id="roadmap-gaps"',
                       "Четыре этапа автоматизации процессов БА", "Запуск этапа 1"):
            self.assertIn(needle, self.section)
        hrefs = re.findall(r'href="([^"]+)"', self.section)
        for document in (SOURCE, "docs/adr/2026-10-adr-017-four-stages-n8n-orchestration.md",
                         "docs/vision.md", "docs/concept.md", "docs/architecture.md",
                         "docs/report/2026-10-31-repository-action-plan.md"):
            with self.subTest(document=document):
                self.assertIn(f"https://github.com{BLOB}{document}", hrefs)
        for href in hrefs:
            self.assert_link_resolves(href)
        self.assertNotIn("ba-ecosystem.md", self.section)

    def test_renderer_shows_role_entry_exit_and_launch(self):
        app = read("site/app.js")
        body = re.search(r"function renderRoadmap\(\) \{.*?^}", app, re.S | re.M).group()
        for needle in ("level.baRole", "level.entry", "level.exitCriteria",
                       "state.roadmap.launch", "state.roadmap.gaps", "nodes.roadmapLaunch"):
            self.assertIn(needle, body)
        self.assertIn('querySelector("#roadmap-launch-steps")', app)


if __name__ == "__main__":
    unittest.main()
