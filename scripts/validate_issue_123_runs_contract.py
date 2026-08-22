#!/usr/bin/env python3
"""Regression check for issue #123 — unified runs/ execution records.

The check locks the Phase 0 contract from issue #123:

- every run lives under ``runs/YYYY/RUN-XXXX/``;
- each run has ``metadata.yaml`` with the minimal required fields;
- each run contains ``inputs/``, ``outputs/``, ``feedback/`` and ``logs/``;
- existing execution results were moved out of ``docs/ba-process/...``,
  ``prompts/experiments/`` and ``governance/analysis-*`` into run records;
- canonical docs, data generation and CI point at ``runs/``.

Issue #293 extends the contract with explicit run types:

- ``metadata.yaml`` MAY declare ``run_type``; allowed values are ``execution``,
  ``statistics`` and ``legacy``. A missing field is read as ``execution``
  (backward compatibility with runs recorded before issue #293);
- a run MUST NOT reach outside its own directory: every path in ``inputs``,
  ``outputs``, ``logs``, ``feedback`` and ``source_paths`` stays inside
  ``runs/YYYY/RUN-XXXX/`` and never points at ``prompts/``, ``kb/``,
  ``site/data/`` or ``patterns/``;
- the standard and the registry document both rules.
Issue #299 removes the hardcoded ``EXPECTED_RUNS`` registry from this file.
Runs are discovered on disk and validated against two sources of truth that
already live next to the data: the run's own ``metadata.yaml`` (which artifacts
the run declares) and ``runs/README.md`` (the human-facing registry). A new run
therefore touches only its own directory and one registry row, and two runs
recorded in parallel no longer collide inside the validator.
"""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_METADATA_FIELDS = ("run_id", "process", "version", "date", "author", "model", "status")
RUN_ID_PATTERN = re.compile(r"^RUN-\d{4}$")
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")

# issue #293: explicit run types.
ALLOWED_RUN_TYPES = ("execution", "statistics", "legacy")
DEFAULT_RUN_TYPE = "execution"
# Path fields whose values are artifacts of the run itself and therefore
# MUST stay inside runs/YYYY/RUN-XXXX/. ``related_artifacts`` is traceability,
# not an artifact of the run, so it is deliberately excluded.
RUN_PATH_FIELDS = ("inputs", "outputs", "logs", "feedback", "source_paths")
# Working artifacts a run is never allowed to touch.
PROTECTED_DIRS = ("prompts/", "kb/", "site/data/", "patterns/")

#: Пути, откуда результаты были перенесены в runs/ при миграции issue #123.
#: Закрытый список вынесен в данные, чтобы не жить в коде валидатора.
LEGACY_MOVED_PATHS_FILE = "scripts/data/runs-legacy-moved-paths.txt"

YEAR_PATTERN = re.compile(r"^\d{4}$")
RUN_SUBDIRS = ("inputs", "outputs", "feedback", "logs")
REGISTRY = "runs/README.md"
REGISTRY_ROW_RE = re.compile(r"^\| \[`(RUN-\d{4})`\]")


def read_text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def require_path(path: str) -> list[str]:
    return [] if (ROOT / path).exists() else [f"{path}: missing"]


def require_text(path: str, *needles: str) -> list[str]:
    text = read_text(path)
    return [f"{path}: missing {needle!r}" for needle in needles if needle not in text]


def parse_yaml_lists(path: Path) -> dict[str, list[str]]:
    """Collect ``key:`` blocks followed by ``  - value`` items.

    Deliberately minimal: run metadata uses flat scalars and flat lists only.
    """

    data: dict[str, list[str]] = {}
    current: str | None = None
    for line in path.read_text(encoding="utf-8").splitlines():
        key_match = re.match(r"^([A-Za-z0-9_-]+):\s*$", line)
        if key_match:
            current = key_match.group(1)
            data.setdefault(current, [])
            continue
        item_match = re.match(r"^\s+-\s+(.+?)\s*$", line)
        if item_match and current:
            data[current].append(item_match.group(1).strip().strip('"'))
            continue
        if re.match(r"^([A-Za-z0-9_-]+):\s*\S", line):
            current = None
    return data


def effective_run_type(metadata: dict[str, str]) -> str:
    """``run_type`` of a run; runs recorded before issue #293 default to execution."""

    return metadata.get("run_type") or DEFAULT_RUN_TYPE


def check_run_type(location: str, metadata: dict[str, str]) -> list[str]:
    declared = metadata.get("run_type")
    if declared is None:
        return []
    if declared not in ALLOWED_RUN_TYPES:
        return [
            f"{location}: run_type {declared!r} not in {list(ALLOWED_RUN_TYPES)}"
        ]
    return []


def check_run_boundaries(location: str, run_prefix: str, path: Path) -> list[str]:
    """Issue #293: run artifacts MUST stay inside runs/YYYY/RUN-XXXX/."""

    errors: list[str] = []
    lists = parse_yaml_lists(path)
    for field in RUN_PATH_FIELDS:
        for value in lists.get(field, []):
            if value.startswith(PROTECTED_DIRS):
                errors.append(
                    f"{location}: {field} points at protected working artifact {value!r}"
                )
                continue
            normalized = value if value.startswith("runs/") else f"{run_prefix}/{value}"
            if not normalized.startswith(f"{run_prefix}/"):
                errors.append(
                    f"{location}: {field} path {value!r} escapes {run_prefix}/"
                )
    return errors


def parse_simple_yaml(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.+?)\s*$", line)
        if match:
            data[match.group(1)] = match.group(2).strip().strip('"')
    return data


def discover_runs() -> list[tuple[str, str]]:
    """Найти прогоны на диске: список пар (год, run_id), отсортированный.

    Единственный источник состава прогонов — файловая система. Раньше здесь был
    словарь ``EXPECTED_RUNS``, который приходилось править в каждом PR с новым
    прогоном; именно он давал конфликты слияния при параллельной работе.
    """

    runs_root = ROOT / "runs"
    if not runs_root.is_dir():
        return []
    found: list[tuple[str, str]] = []
    for year_dir in sorted(runs_root.iterdir()):
        if not year_dir.is_dir() or not YEAR_PATTERN.match(year_dir.name):
            continue
        for run_dir in sorted(year_dir.iterdir()):
            if run_dir.is_dir() and run_dir.name.startswith("RUN-"):
                found.append((year_dir.name, run_dir.name))
    return found


def legacy_moved_paths() -> list[str]:
    path = ROOT / LEGACY_MOVED_PATHS_FILE
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8").splitlines()
    return [line.strip() for line in lines if line.strip() and not line.startswith("#")]


def check_declared_artifacts(location: str, run_prefix: str, run_dir: Path, path: Path) -> list[str]:
    """Каждый артефакт, объявленный в metadata.yaml, существует на диске.

    Это динамическая замена хардкодных списков ``files``: состав прогона
    описывается в самом прогоне, поэтому проверка полноты не требует правки
    валидатора и не конфликтует между параллельными PR.
    """

    errors: list[str] = []
    lists = parse_yaml_lists(path)
    for field in ("inputs", "outputs", "logs", "feedback"):
        for value in lists.get(field, []):
            if value.startswith(("http://", "https://")):
                continue
            target = ROOT / value if value.startswith("runs/") else run_dir / value
            if not target.exists():
                errors.append(f"{location}: {field} declares missing artifact {value!r}")
    return errors


def check_run(year: str, run_id: str) -> list[str]:
    errors: list[str] = []
    run_dir = ROOT / "runs" / year / run_id
    location = f"runs/{year}/{run_id}/metadata.yaml"

    if not RUN_ID_PATTERN.match(run_id):
        errors.append(f"runs/{year}/{run_id}: directory name is not RUN-XXXX")

    for subdir in RUN_SUBDIRS:
        if not (run_dir / subdir).is_dir():
            errors.append(f"runs/{year}/{run_id}/{subdir}: missing required subdirectory")

    outputs = run_dir / "outputs"
    if outputs.is_dir() and not any(item.is_file() for item in outputs.rglob("*")):
        errors.append(f"runs/{year}/{run_id}/outputs: run records no result artifact")

    metadata_path = run_dir / "metadata.yaml"
    if not metadata_path.exists():
        errors.append(f"{location}: missing")
        return errors

    metadata = parse_simple_yaml(metadata_path)
    for field in REQUIRED_METADATA_FIELDS:
        if not metadata.get(field):
            errors.append(f"{location}: missing {field!r}")
    if metadata.get("run_id") != run_id:
        errors.append(f"{location}: run_id {metadata.get('run_id')!r} != {run_id!r}")
    if metadata.get("date") and not DATE_PATTERN.match(metadata["date"]):
        errors.append(f"{location}: invalid date format")

    errors += check_run_type(location, metadata)
    errors += check_run_boundaries(location, f"runs/{year}/{run_id}", metadata_path)
    errors += check_declared_artifacts(location, f"runs/{year}/{run_id}", run_dir, metadata_path)
    return errors


def check_runs() -> list[str]:
    errors: list[str] = []
    runs = discover_runs()
    if not runs:
        return ["runs/: no run records discovered"]

    seen: dict[str, str] = {}
    for year, run_id in runs:
        if run_id in seen:
            errors.append(f"runs/{year}/{run_id}: duplicate run_id, also in runs/{seen[run_id]}/")
        seen[run_id] = year
        errors += check_run(year, run_id)

    for old_path in legacy_moved_paths():
        if (ROOT / old_path).exists():
            errors.append(f"{old_path}: moved execution result still exists at old path")
    return errors


def registry_rows() -> dict[str, str]:
    """run_id -> строка реестра runs/README.md."""

    rows: dict[str, str] = {}
    for line in read_text(REGISTRY).splitlines():
        match = REGISTRY_ROW_RE.match(line)
        if match:
            rows[match.group(1)] = line
    return rows


def check_registry() -> list[str]:
    """Реестр и диск описывают один и тот же состав прогонов.

    Реестр — SSOT для человека, ``metadata.yaml`` — для машины; расхождение
    между ними означает, что прогон записан наполовину.
    """

    errors: list[str] = []
    rows = registry_rows()
    for year, run_id in discover_runs():
        row = rows.pop(run_id, None)
        if row is None:
            errors.append(f"{REGISTRY}: no registry row for {run_id}")
            continue
        metadata_path = ROOT / "runs" / year / run_id / "metadata.yaml"
        if not metadata_path.exists():
            continue
        expected = effective_run_type(parse_simple_yaml(metadata_path))
        if f"`{expected}`" not in row:
            errors.append(f"{REGISTRY}: {run_id} row missing run_type `{expected}`")
    for orphan in sorted(rows):
        errors.append(f"{REGISTRY}: registry row {orphan} has no run directory")
    return errors

def check_docs_and_ci() -> list[str]:
    errors: list[str] = []
    for path in (
        "runs/README.md",
        "standards/runs-contract-standard.md",
        "docs/ba-process/README.md",
        "docs/ba-processes/README.md",
        "README.md",
        "CHANGELOG.md",
        ".github/workflows/github-pages.yml",
        "scripts/generate-pages-data.mjs",
    ):
        errors += require_path(path)
    if errors:
        return errors

    errors += require_text(
        "runs/README.md",
        "run_id",
        "process",
        "version",
        "date",
        "author",
        "model",
        "status",
        "RUN-XXXX",
        "run_type",
        "execution",
        "statistics",
        "## Типы прогонов",
        "## Границы прогона",
    )
    errors += require_text(
        "standards/runs-contract-standard.md",
        "runs/YYYY/RUN-XXXX/",
        "metadata.yaml",
        "scripts/validate_issue_123_runs_contract.py",
        "run_type",
        "## Типы прогонов",
        "## Границы прогона",
        "`prompts/`, `kb/`, `site/data/`, `patterns/`",
    )
    errors += require_text("README.md", "runs/", "Единый каталог результатов")
    errors += require_text("docs/ba-process/README.md", "runs/")
    errors += require_text("docs/ba-processes/README.md", "runs/")
    errors += require_text("CHANGELOG.md", "Issue #123", "runs/", "Issue #293", "run_type")
    errors += require_path("docs/analysis/2026-08-21-runs-type-gap-analysis.md")
    errors += require_text(
        ".github/workflows/github-pages.yml",
        "Validate issue #123 runs contract",
        "scripts/validate_issue_123_runs_contract.py",
    )
    errors += require_text("scripts/generate-pages-data.mjs", "RUNS_DIR", "loadExperiments")
    return errors


def main() -> int:
    errors = []
    errors += check_runs()
    errors += check_docs_and_ci()
    errors += check_registry()

    if errors:
        print("issue-123 runs contract validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("issue-123 runs contract validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
