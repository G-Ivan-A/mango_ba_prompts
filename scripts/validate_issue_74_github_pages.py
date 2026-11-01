#!/usr/bin/env python3
"""Local regression check for issue #74 GitHub Pages prompt interface."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def read_json(path: str) -> dict:
    return json.loads(read_text(path))


def require_file(path: str) -> list[str]:
    if not (ROOT / path).exists():
        return [f"{path}: file does not exist"]
    return []


def require(text: str, path: str, *needles: str) -> list[str]:
    return [f"{path}: missing {needle!r}" for needle in needles if needle not in text]


def reject(text: str, path: str, *needles: str) -> list[str]:
    return [f"{path}: contains forbidden {needle!r}" for needle in needles if needle in text]


def active_prompt_paths() -> list[Path]:
    # Issue #423: the catalog publishes the 39 BCREQ manual prompt classes (PR #422).
    return sorted((ROOT / "standards" / "bcreq-manual-classes").glob("[0-9][0-9]-*.md"))


def archived_prompt_paths() -> list[Path]:
    # Issue #423: the 14 stage-1 prompts (issue #391 set) move to the catalog archive.
    return sorted((ROOT / "prompts").glob("bcreq-*.md"))


def main() -> int:
    errors: list[str] = []

    required_files = (
        "scripts/generate-pages-data.mjs",
        "site/index.html",
        "site/styles.css",
        "site/app.js",
        "site/data/prompts.json",
        "site/data/stats.json",
        "site/data/roadmap.json",
        ".github/workflows/github-pages.yml",
    )
    for path in required_files:
        errors += require_file(path)

    if errors:
        print("issue-74 github pages validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    active_paths = active_prompt_paths()
    archived_paths = archived_prompt_paths()
    prompt_paths = active_paths + archived_paths
    prompt_path_names = {str(path.relative_to(ROOT)) for path in prompt_paths}

    prompts_data = read_json("site/data/prompts.json")
    stats_data = read_json("site/data/stats.json")
    roadmap_data = read_json("site/data/roadmap.json")
    prompts = prompts_data.get("prompts", [])

    if len(prompts) != len(prompt_paths):
        errors.append(f"site/data/prompts.json: expected {len(prompt_paths)} prompts, found {len(prompts)}")

    prompts_by_path = {prompt.get("sourcePath"): prompt for prompt in prompts}
    missing_paths = sorted(prompt_path_names - set(prompts_by_path))
    extra_paths = sorted(set(prompts_by_path) - prompt_path_names)
    for path in missing_paths:
        errors.append(f"site/data/prompts.json: missing prompt {path}")
    for path in extra_paths:
        errors.append(f"site/data/prompts.json: unexpected prompt {path}")

    for path in prompt_paths:
        relative = str(path.relative_to(ROOT))
        prompt = prompts_by_path.get(relative)
        if not prompt:
            continue
        content = path.read_text(encoding="utf-8")
        if prompt.get("content") != content:
            errors.append(f"site/data/prompts.json: content mismatch for {relative}")
        for key in ("id", "file", "mode", "status", "version", "operation", "processes", "description"):
            if not prompt.get(key):
                errors.append(f"site/data/prompts.json: {relative} missing {key}")

    active_generated = [prompt for prompt in prompts if not prompt.get("archived")]
    archived_generated = [prompt for prompt in prompts if prompt.get("archived")]
    if len(active_paths) != 39:
        errors.append(f"standards/bcreq-manual-classes: expected 39 classes, found {len(active_paths)}")
    if len(archived_paths) != 14:
        errors.append(f"prompts/bcreq-*.md: expected 14 archived prompts, found {len(archived_paths)}")
    if sorted(p.get("sourcePath") for p in active_generated) != sorted(str(p.relative_to(ROOT)) for p in active_paths):
        errors.append(f"site/data/prompts.json: active prompts must be the {len(active_paths)} classes, found {len(active_generated)}")
    if sorted(p.get("sourcePath") for p in archived_generated) != sorted(str(p.relative_to(ROOT)) for p in archived_paths):
        errors.append(f"site/data/prompts.json: archived prompts must be the {len(archived_paths)} prompts/bcreq-*.md, found {len(archived_generated)}")

    filters = prompts_data.get("filters", {})
    if len(filters.get("operations", [])) != 13:
        errors.append("site/data/prompts.json: expected 13 cognitive operations in filters")
    if len(filters.get("processes", [])) != 4:
        errors.append("site/data/prompts.json: expected 4 BCREQ stages A-IN…A-RELEASE in filters (issue #423)")
    for mode in {prompt["mode"] for prompt in prompts}:
        if mode not in filters.get("modes", []):
            errors.append(f"site/data/prompts.json: filters.modes missing {mode}")

    totals = stats_data.get("totals", {})
    expected_totals = {
        "allPrompts": len(prompts),
        "activePrompts": len(active_paths),
        "archivedPrompts": len(archived_paths),
        "testsPassed": sum(p["status"] == "canonical" for p in active_generated),
        "inWork": sum(p["status"] == "draft" for p in active_generated),
        "deferred": len(archived_paths),
    }
    for key, expected in expected_totals.items():
        if totals.get(key) != expected:
            errors.append(f"site/data/stats.json: totals.{key} expected {expected}, found {totals.get(key)!r}")

    phase_ids = [phase.get("id") for phase in stats_data.get("phases", [])]
    for phase_id in ("prompts", "agents", "multiagents"):
        if phase_id not in phase_ids:
            errors.append(f"site/data/stats.json: phases missing {phase_id}")

    if len(roadmap_data.get("levels", [])) < 4:
        errors.append("site/data/roadmap.json: expected at least 4 maturity levels from docs/ba-ecosystem.md")
    if len(roadmap_data.get("gaps", [])) < 6:
        errors.append("site/data/roadmap.json: expected roadmap known gaps from docs/ba-ecosystem.md")

    app_js = read_text("site/app.js")
    index_html = read_text("site/index.html")
    styles_css = read_text("site/styles.css")
    workflow = read_text(".github/workflows/github-pages.yml")
    client_bundle = "\n".join((app_js, index_html, styles_css))

    errors += require(
        app_js,
        "site/app.js",
        "data/prompts.json",
        "data/stats.json",
        "data/roadmap.json",
        "navigator.clipboard.writeText",
        "selectedFilters",
    )
    errors += require(
        index_html,
        "site/index.html",
        "catalog",
        "dashboard",
        "roadmap",
        "viewport",
    )
    errors += reject(
        client_bundle,
        "site client assets",
        "api.github.com",
        "Authorization",
        "GITHUB_TOKEN",
        "ghp_",
        "github_pat_",
        "Personal Access Token",
    )
    errors += require(
        workflow,
        ".github/workflows/github-pages.yml",
        "node scripts/generate-pages-data.mjs",
        "python3 scripts/validate_issue_74_github_pages.py",
        "gh-pages",
        "GITHUB_TOKEN",
    )

    changelog = read_text("CHANGELOG.md")
    errors += require(changelog, "CHANGELOG.md", "Issue #74", "GitHub Pages")

    if errors:
        print("issue-74 github pages validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("issue-74 github pages validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
