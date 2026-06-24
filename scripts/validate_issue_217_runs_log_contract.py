#!/usr/bin/env python3
"""Regression check for issue #217: mandatory Markdown logs for every run."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

CONTRACT = "runs/CONTRACT.md"
STANDARD = "standards/runs-contract-standard.md"
REGISTRY = "runs/REGISTRY.md"
ANALYSIS = "docs/analysis/runs-contract-log-policy-audit.md"
CHANGELOG = "CHANGELOG.md"
WORKFLOW = ".github/workflows/github-pages.yml"
VALIDATOR = "scripts/validate_issue_217_runs_log_contract.py"

RUN_ID_PATTERN = re.compile(r"^RUN-\d{4}$")
CANONICAL_LOG_BY_RUN_TYPE = {
    "experiment": "logs/experiment-log.md",
    "generation": "logs/generation-log.md",
    "validation": "logs/validation-log.md",
    "documentation": "logs/documentation-log.md",
    "business-task": "logs/business-task-log.md",
}


def read_text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def require_path(path: str) -> list[str]:
    return [] if (ROOT / path).exists() else [f"{path}: missing"]


def require_text(path: str, *needles: str) -> list[str]:
    errors = require_path(path)
    if errors:
        return errors
    text = read_text(path)
    return [f"{path}: missing {needle!r}" for needle in needles if needle not in text]


def parse_simple_yaml(path: Path) -> dict[str, object]:
    data: dict[str, object] = {}
    current_list: str | None = None

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue

        list_item = re.match(r"^\s+-\s+(.+?)\s*$", raw_line)
        if list_item and current_list:
            data.setdefault(current_list, [])
            assert isinstance(data[current_list], list)
            data[current_list].append(list_item.group(1).strip().strip('"'))
            continue

        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*?)\s*$", raw_line)
        if not match:
            continue

        key = match.group(1)
        value = match.group(2).strip()
        if value:
            data[key] = value.strip('"')
            current_list = None
        else:
            data[key] = []
            current_list = key

    return data


def iter_run_dirs() -> list[Path]:
    runs_root = ROOT / "runs"
    return sorted(
        path
        for year_dir in runs_root.iterdir()
        if year_dir.is_dir() and re.fullmatch(r"\d{4}", year_dir.name)
        for path in year_dir.iterdir()
        if path.is_dir() and RUN_ID_PATTERN.match(path.name)
    )


def check_run_logs() -> list[str]:
    errors: list[str] = []

    for run_dir in iter_run_dirs():
        relative_run_dir = run_dir.relative_to(ROOT)
        metadata_path = run_dir / "metadata.yaml"
        if not metadata_path.exists():
            errors.append(f"{relative_run_dir}/metadata.yaml: missing")
            continue

        metadata = parse_simple_yaml(metadata_path)
        run_id = str(metadata.get("run_id", ""))
        run_type = str(metadata.get("run_type", ""))
        if run_id != run_dir.name:
            errors.append(f"{metadata_path.relative_to(ROOT)}: run_id must match directory name")
        canonical_log = CANONICAL_LOG_BY_RUN_TYPE.get(run_type)
        if not canonical_log:
            errors.append(f"{metadata_path.relative_to(ROOT)}: unsupported run_type {run_type!r}")
            continue

        log_path = run_dir / canonical_log
        if not log_path.exists():
            errors.append(f"{log_path.relative_to(ROOT)}: missing required Markdown log")
        elif log_path.suffix != ".md":
            errors.append(f"{log_path.relative_to(ROOT)}: required log must be Markdown")
        elif not log_path.read_text(encoding="utf-8").strip():
            errors.append(f"{log_path.relative_to(ROOT)}: required log must not be empty")
        else:
            log_text = log_path.read_text(encoding="utf-8")
            for needle in (run_id, run_type, "Ход выполнения", "Итог"):
                if needle not in log_text:
                    errors.append(f"{log_path.relative_to(ROOT)}: missing {needle!r}")

        metadata_logs = metadata.get("logs")
        if not isinstance(metadata_logs, list):
            errors.append(f"{metadata_path.relative_to(ROOT)}: missing logs list")
        elif canonical_log not in metadata_logs:
            errors.append(
                f"{metadata_path.relative_to(ROOT)}: logs must include {canonical_log!r}"
            )

        if (run_dir / "logs" / ".gitkeep").exists() and not any(
            path.suffix == ".md" for path in (run_dir / "logs").glob("*.md")
        ):
            errors.append(f"{relative_run_dir}/logs/.gitkeep: .gitkeep is not a run log")

    return errors


def check_docs() -> list[str]:
    errors: list[str] = []
    errors += require_text(
        CONTRACT,
        "contract_id: runs-contract",
        "# runs-contract",
        "## Типы run'ов (`run_type`)",
        "| `run_type` | Назначение | Канонический Markdown-лог | Примеры |",
        "Markdown-лог обязателен для каждого факта прохода",
        "успешного, неуспешного или частично успешного",
        "`.gitkeep` не считается логом",
    )
    errors += require_text(
        STANDARD,
        "`run_type` | MUST",
        "Markdown-лог",
        "logs/experiment-log.md",
        "logs/business-task-log.md",
    )
    errors += require_text(
        REGISTRY,
        "| Run | Дата | Тип | Процесс | Основной результат | Лог |",
    )
    for run_dir in iter_run_dirs():
        metadata = parse_simple_yaml(run_dir / "metadata.yaml")
        canonical_log = CANONICAL_LOG_BY_RUN_TYPE.get(str(metadata.get("run_type", "")))
        if canonical_log:
            errors += require_text(REGISTRY, run_dir.name, canonical_log)
    errors += require_text(
        ANALYSIS,
        "Issue #217",
        "RUN-0001..RUN-0010",
        "RUN-0013",
        "Markdown-лог",
        "docs/analysis/",
    )
    errors += require_text(CHANGELOG, "Issue #217", VALIDATOR, ANALYSIS)
    errors += require_text(WORKFLOW, "Validate issue #217 runs log contract", VALIDATOR)
    return errors


def main() -> int:
    errors = check_run_logs() + check_docs()
    if errors:
        print("Issue #217 runs log contract validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Issue #217 runs log contract validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
