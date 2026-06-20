#!/usr/bin/env python3
"""Regression check for issue #129 — KB pipeline processes every source.

Issue #129 reported a successful KB workflow that still left 12 newly uploaded
source folders absent from ``kb/processed``. The failure mode was orchestration:
manual dispatch defaulted to one hardcoded source, while the repository already
had enough manifest data to plan every ``kb/sources/*/meta.json``.

This check stays stdlib-only for CI and verifies:

- the issue's processable ``meta.json`` sources exist with PDF payloads;
- every issue source expands to a top-level processed output directory;
- workflow_dispatch defaults to all manifests and invokes ``process_sources.py --all``;
- Makefile validation includes this regression.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "kb"))

from process_sources import ManifestError, build_plan, iter_source_dirs  # noqa: E402

WORKFLOW = ".github/workflows/kb.yml"
MAKEFILE = "Makefile"

ISSUE_129_SOURCES = {
    "Rolevaya-model-vats": {"mode": "single", "jobs": 1},
    "integration-bitrix24": {"mode": "single", "jobs": 1},
    "integration_1c": {"mode": "single", "jobs": 1},
    "integration_amocrm": {"mode": "single", "jobs": 1},
    "lk-vats-sso": {"mode": "single", "jobs": 1},
    "mdialogi-api": {"mode": "single", "jobs": 1},
    "quality-managment": {"mode": "single", "jobs": 1},
    "sip-trunk": {"mode": "single", "jobs": 1},
    "speech-analytics": {"mode": "multi_document", "jobs": 4},
    "vpbx-api": {"mode": "single", "jobs": 1},
    "wallboard": {"mode": "single", "jobs": 1},
}


def read_text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def require_text(text: str, path: str, *needles: str) -> list[str]:
    return [f"{path}: missing {needle!r}" for needle in needles if needle not in text]


def check_source_plans() -> list[str]:
    errors: list[str] = []
    planned = {path.name: path for path in iter_source_dirs()}
    missing = sorted(set(ISSUE_129_SOURCES) - set(planned))
    for slug in missing:
        errors.append(f"kb/sources/{slug}/meta.json: missing")

    for slug, expected in sorted(ISSUE_129_SOURCES.items()):
        source_dir = planned.get(slug)
        if source_dir is None:
            continue
        try:
            plan = build_plan(source_dir)
        except ManifestError as exc:
            errors.append(str(exc))
            continue
        if plan.mode != expected["mode"]:
            errors.append(f"kb/sources/{slug}/meta.json: mode {plan.mode!r}, expected {expected['mode']!r}")
        if len(plan.jobs) != expected["jobs"]:
            errors.append(f"kb/sources/{slug}/meta.json: {len(plan.jobs)} jobs, expected {expected['jobs']}")
        if plan.output_dir != ROOT / "kb" / "processed" / slug:
            errors.append(f"kb/sources/{slug}/meta.json: output must be kb/processed/{slug}")
        for job in plan.jobs:
            if not job.pdf_paths:
                errors.append(f"kb/sources/{slug}/meta.json: job {job.source_document} has no PDFs")
            for pdf_path in job.pdf_paths:
                if pdf_path.suffix.lower() != ".pdf":
                    errors.append(f"{pdf_path.relative_to(ROOT)}: expected PDF source")
                if not pdf_path.exists():
                    errors.append(f"{pdf_path.relative_to(ROOT)}: missing")
    return errors


def check_workflow_all_dispatch() -> list[str]:
    text = read_text(WORKFLOW)
    errors = require_text(
        text,
        WORKFLOW,
        'default: "all"',
        'if [ "$SOURCE_DIR" = "all" ]; then',
        "python3 scripts/kb/process_sources.py --all",
        "path: kb/processed/",
        "scripts/validate_issue_129_kb_all_sources.py",
    )
    if 'default: "kb/sources/mango-cc-manual"' in text:
        errors.append(f"{WORKFLOW}: workflow_dispatch must not default to one hardcoded source")
    return errors


def check_makefile_targets() -> list[str]:
    text = read_text(MAKEFILE)
    return require_text(
        text,
        MAKEFILE,
        "kb-source-plan-all",
        "kb-source-extract-all",
        "$(PYTHON) scripts/kb/process_sources.py --all --dry-run",
        "$(PYTHON) scripts/kb/process_sources.py --all",
        "scripts/validate_issue_129_kb_all_sources.py",
    )


def main() -> int:
    errors: list[str] = []
    errors += check_source_plans()
    errors += check_workflow_all_dispatch()
    errors += check_makefile_targets()
    if errors:
        print("Issue #129 validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Issue #129 validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
