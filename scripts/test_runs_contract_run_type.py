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
    EXPECTED_RUNS,
    ROOT,
    check_run_boundaries,
    check_run_type,
    effective_run_type,
    parse_simple_yaml,
    parse_yaml_lists,
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
    """Run type follows the goal stated in the issue, not the artifacts produced.

    Criterion agreed in the review of PR #294: «зафиксировать прогон / собрать
    эмпирические данные» → ``statistics``; «выполнить процесс / получить
    артефакт» → ``execution``.
    """

    #: run_id -> run_type, justified in
    #: docs/analysis/2026-08-21-runs-type-gap-analysis.md (Ф-5).
    EXPECTED_CLASSIFICATION = {
        "RUN-0001": "execution",
        "RUN-0002": "execution",
        "RUN-0003": "execution",
        "RUN-0004": "statistics",
        "RUN-0005": "statistics",
        "RUN-0006": "execution",
        "RUN-0007": "execution",
        "RUN-0008": "statistics",
        "RUN-0009": "statistics",
        "RUN-0010": "statistics",
        "RUN-0011": "execution",
        "RUN-0012": "execution",
        "RUN-0013": "statistics",
        "RUN-0014": "statistics",
        "RUN-0017": "statistics",
        "RUN-0018": "statistics",
        "RUN-0020": "statistics",
        "RUN-0022": "statistics",
    }

    def test_metadata_matches_agreed_classification(self) -> None:
        for run_id, expected in self.EXPECTED_CLASSIFICATION.items():
            spec = EXPECTED_RUNS[run_id]
            path = ROOT / "runs" / str(spec["year"]) / run_id / "metadata.yaml"
            metadata = parse_simple_yaml(path)
            self.assertEqual(effective_run_type(metadata), expected, run_id)

    def test_validator_registry_matches_agreed_classification(self) -> None:
        self.assertEqual(
            {run_id: spec["run_type"] for run_id, spec in EXPECTED_RUNS.items()},
            self.EXPECTED_CLASSIFICATION,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
