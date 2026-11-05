#!/usr/bin/env python3
"""Регрессионная проверка issue #462: отчёт RUN-0060 не входит в сайт (вариант А).

Клиентский пароль не защищает файлы на статическом хостинге, поэтому проверяется
физическое отсутствие отчёта и его следов в ``site/``, а не наличие входа.
"""

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
GENERATOR = ROOT / "scripts" / "generate-pages-data.mjs"
EXCLUDED = "reports/run-0060"
#: Следы отчёта: идентификатор, файл, номер задачи и внешняя система интеграции.
MARKERS = ("run-0060", "detailed-gap-report", "задача 765", "hh.ru")
TEXT_SUFFIXES = {".html", ".js", ".json", ".css", ".svg", ".txt", ".xml"}


class ReportExclusion(unittest.TestCase):
    def test_report_is_physically_absent(self):
        self.assertFalse((SITE / EXCLUDED).exists())

    def test_no_report_traces_in_site(self):
        leaks = []
        for path in SITE.rglob("*"):
            if path.is_file() and path.suffix in TEXT_SUFFIXES:
                text = path.read_text(encoding="utf-8").lower()
                leaks += [f"{path.relative_to(ROOT)}: {m}" for m in MARKERS if m in text]
        self.assertEqual(leaks, [])

    def test_no_password_entry_for_report(self):
        hashes = json.loads((SITE / "password-hashes.json").read_text(encoding="utf-8"))
        self.assertEqual(set(hashes), {"site"})

    def test_generator_removes_report_planted_in_site(self):
        with tempfile.TemporaryDirectory() as tmp:
            site = Path(tmp) / "site"
            planted = site / EXCLUDED / "diagrams" / "diagram-00.svg"
            kept = site / "reports" / "index.html"
            planted.parent.mkdir(parents=True)
            planted.write_text("secret", encoding="utf-8")
            kept.write_text("index", encoding="utf-8")
            code = (
                f"const m = await import({json.dumps(GENERATOR.as_uri())});"
                f"await m.enforcePublicSiteExclusions({json.dumps(str(site))});"
            )
            subprocess.run(["node", "--input-type=module", "-e", code], check=True, timeout=60)
            self.assertFalse((site / EXCLUDED).exists())
            self.assertTrue(kept.exists())

    def test_generator_applies_exclusion_on_every_run(self):
        text = GENERATOR.read_text(encoding="utf-8")
        main = text[text.index("async function main()"):]
        self.assertIn("await enforcePublicSiteExclusions();", main[:200])
        self.assertIn(f'"{EXCLUDED}"', text)

    def test_report_builder_writes_outside_site(self):
        builder = (ROOT / "experiments/issue_335_build_report_site.py").read_text(encoding="utf-8")
        self.assertIn('ROOT / ".private-reports"', builder)
        self.assertNotIn('ROOT / "site"', builder)


if __name__ == "__main__":
    unittest.main()
