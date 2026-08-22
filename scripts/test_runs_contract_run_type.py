#!/usr/bin/env python3
"""Regression tests for issue #293 — run types and run boundaries.

The repository validator (``validate_issue_123_runs_contract.py``) checks the
real runs. These tests check the *rules* on synthetic metadata, so the two
guarantees of issue #293 stay covered even when every real run is well-formed:

- backward compatibility: ``metadata.yaml`` without ``run_type`` is valid and
  reads as ``execution``;
- classification: runs recorded by a "зафиксировать прогон" issue are
  ``statistics``, runs recorded by a "получить артефакт" issue are ``execution``
  (issue #293 review criterion);
- boundaries: a run that points at ``prompts/``, ``kb/``, ``site/data/`` or
  ``patterns/``, or otherwise escapes its own directory, fails.

Run: ``python3 scripts/test_runs_contract_run_type.py``
"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from validate_issue_123_runs_contract import (  # noqa: E402
    ROOT,
    check_run_boundaries,
    check_run_type,
    discover_runs,
    effective_run_type,
    parse_simple_yaml,
    parse_yaml_lists,
    registry_rows,
)

RUN_PREFIX = "runs/2026/RUN-9999"


def write_metadata(body: str) -> Path:
    tmp = Path(tempfile.mkdtemp()) / "metadata.yaml"
    tmp.write_text(body, encoding="utf-8")
    return tmp


class RunTypeTest(unittest.TestCase):
    def test_missing_run_type_defaults_to_execution(self) -> None:
        path = write_metadata("run_id: RUN-9999\nstatus: success\n")
        metadata = parse_simple_yaml(path)
        self.assertEqual(check_run_type(RUN_PREFIX, metadata), [])
        self.assertEqual(effective_run_type(metadata), "execution")

    def test_allowed_values(self) -> None:
        for value in ("execution", "statistics", "legacy"):
            metadata = parse_simple_yaml(write_metadata(f"run_type: {value}\n"))
            self.assertEqual(check_run_type(RUN_PREFIX, metadata), [])
            self.assertEqual(effective_run_type(metadata), value)

    def test_unknown_value_rejected(self) -> None:
        metadata = parse_simple_yaml(write_metadata("run_type: experiment\n"))
        errors = check_run_type(RUN_PREFIX, metadata)
        self.assertEqual(len(errors), 1)
        self.assertIn("run_type 'experiment'", errors[0])


class BoundariesTest(unittest.TestCase):
    def test_paths_inside_run_are_accepted(self) -> None:
        path = write_metadata(
            "outputs:\n"
            "  - outputs/final-artifact.md\n"
            f"source_paths:\n  - {RUN_PREFIX}/outputs/final-artifact.md\n"
            "related_artifacts:\n  - prompts/fr-documentation-stepwise.md\n"
        )
        self.assertEqual(check_run_boundaries(RUN_PREFIX, RUN_PREFIX, path), [])

    def test_protected_directories_rejected(self) -> None:
        for protected in (
            "prompts/fr-documentation-stepwise.md",
            "kb/processed/mango-cc-manual/index.json",
            "site/data/runs.json",
            "patterns/agent-workload.md",
        ):
            path = write_metadata(f"outputs:\n  - {protected}\n")
            errors = check_run_boundaries(RUN_PREFIX, RUN_PREFIX, path)
            self.assertEqual(len(errors), 1, protected)
            self.assertIn("protected working artifact", errors[0])

    def test_other_run_directory_rejected(self) -> None:
        path = write_metadata("logs:\n  - runs/2026/RUN-0001/logs/experiment-log.md\n")
        errors = check_run_boundaries(RUN_PREFIX, RUN_PREFIX, path)
        self.assertEqual(len(errors), 1)
        self.assertIn("escapes", errors[0])

    def test_list_parser_stops_at_next_scalar(self) -> None:
        path = write_metadata(
            "outputs:\n  - outputs/a.md\nstatus: success\nlogs:\n  - logs/b.md\n"
        )
        lists = parse_yaml_lists(path)
        self.assertEqual(lists["outputs"], ["outputs/a.md"])
        self.assertEqual(lists["logs"], ["logs/b.md"])


class ClassificationTest(unittest.TestCase):
    """Тип прогона следует цели, заявленной в задаче, а не составу артефактов.

    Критерий согласован в ревью PR #294: «зафиксировать прогон / собрать
    эмпирические данные» → ``statistics``; «выполнить процесс / получить
    артефакт» → ``execution``.

    Согласованная классификация больше не дублируется в коде (issue #299): её
    держит реестр ``runs/README.md``, а тест проверяет, что реестр и
    ``metadata.yaml`` каждого обнаруженного прогона говорят одно и то же.
    Раньше здесь был словарь ``EXPECTED_RUNS``, требовавший правки в каждом PR
    с новым прогоном.
    """

    def test_every_run_declares_a_known_type(self) -> None:
        runs = discover_runs()
        self.assertTrue(runs, "прогоны не обнаружены")
        for year, run_id in runs:
            metadata = parse_simple_yaml(ROOT / "runs" / year / run_id / "metadata.yaml")
            self.assertEqual(check_run_type(run_id, metadata), [], run_id)

    def test_registry_and_metadata_agree(self) -> None:
        rows = registry_rows()
        for year, run_id in discover_runs():
            metadata = parse_simple_yaml(ROOT / "runs" / year / run_id / "metadata.yaml")
            self.assertIn(run_id, rows, f"{run_id}: нет строки в runs/README.md")
            self.assertIn(f"`{effective_run_type(metadata)}`", rows[run_id], run_id)


class DiscoveryTest(unittest.TestCase):
    """Обнаружение прогонов на диске — замена хардкодного реестра."""

    def test_discovered_runs_match_directory_listing(self) -> None:
        discovered = {run_id for _, run_id in discover_runs()}
        on_disk = {
            path.name
            for path in (ROOT / "runs").glob("*/RUN-*")
            if path.is_dir()
        }
        self.assertEqual(discovered, on_disk)

    def test_run_ids_are_unique_across_years(self) -> None:
        run_ids = [run_id for _, run_id in discover_runs()]
        self.assertEqual(len(run_ids), len(set(run_ids)))


if __name__ == "__main__":
    unittest.main(verbosity=2)
