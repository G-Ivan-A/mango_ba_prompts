#!/usr/bin/env python3
"""Тесты раннера валидаторов (issue #299).

Проверяются гарантии, на которых держится инкрементальный запуск, включая
граничные гипотезы из задачи: повреждённый кэш, исчезнувший файл, новый файл в
каталоге, провал валидатора, параллельный запуск двух раннеров.

Тесты герметичны: собирается временный мини-репозиторий с копией раннера и
синтетическими валидаторами, настоящий репозиторий не затрагивается.

Запуск: ``python3 scripts/test_validate_all.py``
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import threading
import unittest
from pathlib import Path

REAL_ROOT = Path(__file__).resolve().parents[1]

PASSING = """#!/usr/bin/env python3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
data = ROOT / "data"
names = sorted(p.name for p in data.glob("*.txt"))
for name in names:
    (data / name).read_text(encoding="utf-8")
missing = not (ROOT / "optional.txt").exists()
print("checked", len(names), "missing-optional", missing)
sys.exit(0)
"""

FAILING = """#!/usr/bin/env python3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
(ROOT / "data" / "a.txt").read_text(encoding="utf-8")
print("broken on purpose")
sys.exit(1)
"""


class RunnerCase(unittest.TestCase):
    def setUp(self) -> None:
        self.root = Path(tempfile.mkdtemp(prefix="validate-runner-"))
        self.addCleanup(shutil.rmtree, self.root, True)
        (self.root / "scripts").mkdir()
        (self.root / "data").mkdir()
        (self.root / "tools").mkdir()
        for name in ("validate_all.py", "_validator_trace.py"):
            shutil.copy(REAL_ROOT / "scripts" / name, self.root / "scripts" / name)
        (self.root / "data" / "a.txt").write_text("alpha\n", encoding="utf-8")
        (self.root / "data" / "b.txt").write_text("beta\n", encoding="utf-8")
        self.write_validator("validate_issue_001_demo.py", PASSING)

    def write_validator(self, name: str, body: str) -> Path:
        path = self.root / "scripts" / name
        path.write_text(body, encoding="utf-8")
        path.chmod(0o755)
        return path

    def run_runner(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(self.root / "scripts/validate_all.py"), *args],
            cwd=self.root,
            capture_output=True,
            text=True,
        )

    def statuses(self, *args: str) -> dict[str, str]:
        proc = self.run_runner(*args)
        result: dict[str, str] = {}
        for line in proc.stdout.splitlines():
            parts = line.split()
            if len(parts) >= 2 and parts[0] in {"PASS", "CACHED", "FAIL"}:
                result[parts[1]] = parts[0]
        self.last = proc
        return result


class CacheTest(RunnerCase):
    def test_second_run_is_cached(self) -> None:
        self.assertEqual(self.statuses()["validate_issue_001_demo"], "PASS")
        self.assertEqual(self.statuses()["validate_issue_001_demo"], "CACHED")

    def test_changed_dependency_invalidates(self) -> None:
        self.statuses()
        (self.root / "data" / "a.txt").write_text("changed\n", encoding="utf-8")
        self.assertEqual(self.statuses()["validate_issue_001_demo"], "PASS")

    def test_touch_without_content_change_stays_cached(self) -> None:
        """Кэш сравнивает содержимое: `touch` не должен ронять попадание."""

        self.statuses()
        os.utime(self.root / "data" / "a.txt", (0, 0))
        self.assertEqual(self.statuses()["validate_issue_001_demo"], "CACHED")

    def test_new_file_in_scanned_directory_invalidates(self) -> None:
        """Гипотеза: валидатор обходит каталог, а не конкретные файлы."""

        self.statuses()
        (self.root / "data" / "c.txt").write_text("gamma\n", encoding="utf-8")
        self.assertEqual(self.statuses()["validate_issue_001_demo"], "PASS")

    def test_deleted_dependency_invalidates(self) -> None:
        self.statuses()
        (self.root / "data" / "b.txt").unlink()
        self.assertEqual(self.statuses()["validate_issue_001_demo"], "PASS")

    def test_appearing_optional_file_invalidates(self) -> None:
        """Гипотеза: валидатор зависит от *отсутствия* файла."""

        self.statuses()
        (self.root / "optional.txt").write_text("now here\n", encoding="utf-8")
        self.assertEqual(self.statuses()["validate_issue_001_demo"], "PASS")

    def test_changed_validator_source_invalidates(self) -> None:
        self.statuses()
        path = self.root / "scripts" / "validate_issue_001_demo.py"
        path.write_text(PASSING + "\n# правка самого валидатора\n", encoding="utf-8")
        self.assertEqual(self.statuses()["validate_issue_001_demo"], "PASS")

    def test_full_ignores_cache(self) -> None:
        self.statuses()
        self.assertEqual(self.statuses("--full")["validate_issue_001_demo"], "PASS")

    def test_clear_cache_removes_directory(self) -> None:
        self.statuses()
        self.assertTrue((self.root / ".validate-cache").exists())
        self.run_runner("--clear-cache")
        self.assertFalse((self.root / ".validate-cache").exists())


class CorruptCacheTest(RunnerCase):
    def test_garbage_entry_is_treated_as_miss(self) -> None:
        self.statuses()
        entry = self.root / ".validate-cache/entries/validate_issue_001_demo.json"
        entry.write_text("{не json", encoding="utf-8")
        self.assertEqual(self.statuses()["validate_issue_001_demo"], "PASS")
        self.assertEqual(self.statuses()["validate_issue_001_demo"], "CACHED")

    def test_truncated_stat_cache_is_treated_as_miss(self) -> None:
        self.statuses()
        (self.root / ".validate-cache/stat-cache.json").write_text("", encoding="utf-8")
        statuses = self.statuses()
        self.assertIn(statuses["validate_issue_001_demo"], {"PASS", "CACHED"})
        self.assertEqual(self.last.returncode, 0)

    def test_stale_state_with_stale_hash_is_rechecked(self) -> None:
        """Подделанное состояние кэша не должно скрывать реальную поломку."""

        self.statuses()
        entry = self.root / ".validate-cache/entries/validate_issue_001_demo.json"
        payload = json.loads(entry.read_text(encoding="utf-8"))
        payload["state"] = {key: "устаревший" for key in payload["state"]}
        entry.write_text(json.dumps(payload), encoding="utf-8")
        self.assertEqual(self.statuses()["validate_issue_001_demo"], "PASS")


class FailureTest(RunnerCase):
    def test_failure_is_reported_and_not_cached(self) -> None:
        self.write_validator("validate_issue_002_broken.py", FAILING)
        statuses = self.statuses()
        self.assertEqual(statuses["validate_issue_002_broken"], "FAIL")
        self.assertEqual(self.last.returncode, 1)
        self.assertIn("broken on purpose", self.last.stdout)
        # провал обязан воспроизводиться, пока причина не устранена
        self.assertEqual(self.statuses()["validate_issue_002_broken"], "FAIL")

    def test_new_validator_is_discovered_without_registry_edit(self) -> None:
        self.statuses()
        self.write_validator("validate_issue_003_extra.py", PASSING)
        self.assertEqual(self.statuses()["validate_issue_003_extra"], "PASS")


class ParallelTest(RunnerCase):
    def test_two_runners_at_once_leave_usable_cache(self) -> None:
        """Гипотеза: раннер запущен в фоне и вручную одновременно."""

        results: list[subprocess.CompletedProcess] = []
        threads = [
            threading.Thread(target=lambda: results.append(self.run_runner("--full")))
            for _ in range(2)
        ]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        self.assertTrue(all(proc.returncode == 0 for proc in results), results)
        entry = self.root / ".validate-cache/entries/validate_issue_001_demo.json"
        json.loads(entry.read_text(encoding="utf-8"))  # не должен быть повреждён
        self.assertEqual(self.statuses()["validate_issue_001_demo"], "CACHED")
        self.assertFalse(
            list((self.root / ".validate-cache").glob("*.tmp")), "остались временные файлы"
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
