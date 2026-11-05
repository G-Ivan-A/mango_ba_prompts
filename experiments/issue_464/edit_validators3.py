"""Issue #464: версия сайта 2.7.0 и снимок аудита прода. Одноразовая правка."""
from _edit import edit

edit("scripts/validate_issue_427_rfc.py", [("list(range(1, 15)))", "list(range(1, 14)))")])
edit("scripts/validate_issue_448_bl156_bl157v.py", [('self.assertEqual(len(self.data["steps"]), 13)', 'self.assertEqual(len(self.data["steps"]), 14)')])
edit("scripts/validate_issue_450_bl156g_167_168.py", [
    ("""self.assertIn('version: "2.6.0"', read("scripts/generate-pages-data.mjs"))""", """self.assertIn('version: "2.7.0"', read("scripts/generate-pages-data.mjs"))"""),
    ("""self.assertEqual(read("site/index.html").count("v2.6.0"), 2)""", """self.assertEqual(read("site/index.html").count("v2.7.0"), 2)"""),
])
edit("scripts/validate_issue_460_site_debug.py", [
    ("""self.assertIn('version: "2.6.0"', read("scripts/generate-pages-data.mjs"))""", """self.assertIn('version: "2.7.0"', read("scripts/generate-pages-data.mjs"))"""),
    ("""self.assertEqual(read("site/index.html").count("v2.6.0"), 2)""", """self.assertEqual(read("site/index.html").count("v2.7.0"), 2)"""),
    ("""["siteVersion"]["version"], "2.6.0")""", """["siteVersion"]["version"], "2.7.0")"""),
])
edit("scripts/validate_issue_454_publication_roadmap.py", [
    ('        self.assertEqual(facts["prod"]["steps_total"], len(self.kit["steps"]))\n',
     '        # Снимок прода снят на 13 шагах; Ш-А (issue #464) появится на проде с деплоем 2.7.0.\n'
     '        self.assertEqual(facts["prod"]["steps_total"], len([s for s in self.kit["steps"] if not s["step"].startswith("Ш-А")]))\n'),
])
edit("site/index.html", [("v2.6.0", "v2.7.0", 2)])
