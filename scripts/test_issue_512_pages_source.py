"""Exercise the production Pages source check with simulated API results."""

import os
from pathlib import Path
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]


class PagesSourceTest(unittest.TestCase):
    def check_source(self, result, status=0):
        return subprocess.run(
            [
                "bash", "-c",
                '''
                gh() {
                    if [[ "$1" != api || "$2" != repos/test/project/pages ]]; then
                        return 2
                    fi
                    printf '%s\n' "$MOCK_RESULT"
                    return "$MOCK_STATUS"
                }
                export -f gh
                bash scripts/check-pages-source.sh
                ''',
            ],
            cwd=ROOT,
            env={**os.environ, "GITHUB_REPOSITORY": "test/project",
                 "MOCK_RESULT": result, "MOCK_STATUS": str(status)},
            capture_output=True,
            text=True,
            timeout=5,
        )

    def test_branch_source_is_ready(self):
        result = self.check_source("true")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Pages source is configured", result.stdout)

    def test_wrong_source_has_actionable_error(self):
        result = self.check_source("false")
        self.assertEqual(result.returncode, 1)
        self.assertIn("Unexpected Pages source", result.stdout)
        self.assertIn("gh-pages, /", result.stdout)

    def test_unavailable_pages_has_actionable_error(self):
        result = self.check_source("", status=1)
        self.assertEqual(result.returncode, 1)
        self.assertIn("Settings > Pages", result.stdout)
        self.assertIn("check the plan", result.stdout)


if __name__ == "__main__":
    unittest.main()
