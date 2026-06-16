#!/usr/bin/env python3
"""Local regression check for issue #99: GitHub Pages optimization.

Locks the requirements of the multi-page redesign so future edits keep working:
- ФТ-1 multi-page: top nav with five sections + client-side hash router;
- ФТ-2 card optimization: file path / hash removed, version + tests + share added;
- ФТ-3 dashboard: per-process checks, tests coverage and activity (top-5);
- ФТ-4 UX: search suggestions, sort, status filter, export, process modal, theme;
- ФТ-5 data generation: processes.json + patterns.json + enriched checks.json;
- ФТ-6 docs: README + CHANGELOG mention the change;
- NFT: no hardcoded process list (counts derived from generated data), client
  bundle free of secrets, generation does not break.
"""

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

NAV_LABELS = ["Каталог", "Дашборд", "Roadmap", "Процессы", "Паттерны"]
NAV_PAGES = ["catalog", "dashboard", "roadmap", "processes", "patterns"]

SECRET_MARKERS = [
    "api.github.com",
    "Authorization",
    "GITHUB_TOKEN",
    "ghp_",
    "github_pat_",
    "Personal Access Token",
]


def read_text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def read_json(path: str) -> dict:
    return json.loads(read_text(path))


def require(text: str, path: str, *needles: str) -> list[str]:
    return [f"{path}: missing {needle!r}" for needle in needles if needle not in text]


def main() -> int:
    errors: list[str] = []

    index_html = read_text("site/index.html")
    app_js = read_text("site/app.js")
    styles_css = read_text("site/styles.css")

    # --- ФТ-1: multi-page nav + hash router ----------------------------------
    errors += require(index_html, "site/index.html", *NAV_LABELS)
    for page in NAV_PAGES:
        if f'data-nav="{page}"' not in index_html:
            errors.append(f"site/index.html: missing nav link data-nav={page!r}")
        if f'data-page="{page}"' not in index_html and page not in {"dashboard"}:
            # dashboard page groups several sections via data-page="dashboard"
            errors.append(f"site/index.html: missing section data-page={page!r}")
    if 'data-page="dashboard"' not in index_html:
        errors.append("site/index.html: missing section data-page='dashboard'")

    # Section id order must stay catalog -> dashboard -> checks -> roadmap
    # (locked by issue #91; the new pages are appended afterwards).
    ids_order = re.findall(r'<section[^>]*\sid="([a-z]+)"', index_html)
    expected_prefix = ["catalog", "dashboard", "checks", "roadmap"]
    if ids_order[: len(expected_prefix)] != expected_prefix:
        errors.append(
            f"site/index.html: section id order {ids_order} must start with {expected_prefix}"
        )
    for required_id in ("processes", "patterns"):
        if required_id not in ids_order:
            errors.append(f"site/index.html: missing <section id={required_id!r}>")

    # Router lives in app.js and reacts to hash changes.
    errors += require(
        app_js,
        "site/app.js",
        "hashchange",
        "applyRoute",
        "data/processes.json",
        "data/patterns.json",
        "data/prompts.json",
        "data/stats.json",
        "data/roadmap.json",
        "data/checks.json",
    )

    # --- ФТ-2: card optimization ---------------------------------------------
    card_match = re.search(
        r"function promptCard\(prompt\)\s*\{(.+?)^}", app_js, re.DOTALL | re.MULTILINE
    )
    if not card_match:
        errors.append("site/app.js: promptCard function not found")
    else:
        card_body = card_match.group(1)
        # File path and content hash must be gone from the card.
        for forbidden in ("sourcePath", "contentHash", "checksum", "prompt-file"):
            if forbidden in card_body:
                errors.append(f"site/app.js: promptCard must not render {forbidden!r}")
        # New card content: long description, version, test count, id, share link.
        errors += require(
            card_body,
            "site/app.js promptCard",
            "descriptionLong",
            "prompt.version",
            "prompt-id",
            "shareId",
        )
        if "testsFor" not in card_body and "тест" not in card_body:
            errors.append("site/app.js: promptCard must show test status")
        # ID HTML comment is copy-only, not rendered in the card (issue #95).
        if "<!-- ${prompt.id} -->" in card_body:
            errors.append("site/app.js: HTML comment must not appear in promptCard")

    # Copy still prepends the prompt id (issue #95 contract preserved).
    if not re.search(
        r"copyText\(`<!-- \$\{prompt\.id\} -->\\n\\n\$\{body\}`\)", app_js
    ):
        errors.append(
            "site/app.js: copyText must keep format `<!-- ${prompt.id} -->\\n\\n${body}`"
        )

    # --- ФТ-3 + ФТ-4: dashboard + UX render hooks ----------------------------
    errors += require(
        app_js,
        "site/app.js",
        "renderChecks",
        "renderProcesses",
        "renderPatterns",
        "byProcess",
        "testsPassed",
        "selectedFilters",
        "selectedValues",
        "availableOperationIds",
        "sortPrompts",
        "exportCatalog",
        "search-suggestions",
        "openProcessModal",
        "closeProcessModal",
        "localStorage",
        "#prompt=",
    )
    # Status filter is a fourth filter group built from the three statuses.
    errors += require(app_js, "site/app.js", "status:${status}", "Статус")
    for status in ("draft", "canonical", "archived"):
        if status not in app_js:
            errors.append(f"site/app.js: status filter missing {status!r}")
    # Export builds a Markdown blob client-side.
    errors += require(app_js, "site/app.js", "Blob", "text/markdown")
    # Theme toggle wiring.
    errors += require(index_html, "site/index.html", "theme-toggle", "sort-select", "export-button")

    # --- ФТ-4 styling: dark theme + new components ---------------------------
    errors += require(
        styles_css,
        "site/styles.css",
        ':root[data-theme="dark"]',
        ".process-grid",
        ".pattern-grid",
        ".byprocess-grid",
        ".modal",
    )

    # --- ФТ-5: generated data -------------------------------------------------
    prompts = read_json("site/data/prompts.json")
    for prompt in prompts.get("prompts", []):
        long_desc = prompt.get("descriptionLong", "")
        if not long_desc:
            errors.append(f"prompts.json: {prompt.get('id')} missing descriptionLong")
        elif len(long_desc) < 150:
            errors.append(
                f"prompts.json: {prompt.get('id')} descriptionLong is {len(long_desc)} chars (<150)"
            )

    checks = read_json("site/data/checks.json")
    for key in ("byProcess", "testsPassed", "totalChecked", "feedback"):
        if key not in checks:
            errors.append(f"checks.json: missing key {key!r}")
    if not isinstance(checks.get("byProcess"), list) or not checks["byProcess"]:
        errors.append("checks.json: byProcess must be a non-empty list")
    else:
        for entry in checks["byProcess"]:
            for field in ("label", "emoji", "checks", "coveredPrompts"):
                if field not in entry:
                    errors.append(f"checks.json: byProcess entry missing {field!r}")
                    break
    tp = checks.get("testsPassed", {})
    for field in ("covered", "total", "percent"):
        if field not in tp:
            errors.append(f"checks.json: testsPassed missing {field!r}")

    processes = read_json("site/data/processes.json")
    proc_list = processes.get("processes", [])
    if not proc_list:
        errors.append("processes.json: processes must be a non-empty list")
    for process in proc_list:
        for field in ("id", "label", "emoji", "description", "prompts", "gaps", "checks"):
            if field not in process:
                errors.append(f"processes.json: process {process.get('id')} missing {field!r}")
                break

    patterns = read_json("site/data/patterns.json")
    pat_list = patterns.get("patterns", [])
    if not pat_list:
        errors.append("patterns.json: patterns must be a non-empty list")
    for pattern in pat_list:
        for field in ("slug", "url", "processes", "operation", "prompts"):
            if field not in pattern:
                errors.append(f"patterns.json: pattern {pattern.get('slug')} missing {field!r}")
                break

    # NFT: no hardcoded process list — the dashboard breakdown is derived from
    # the same taxonomy that drives processes.json, so counts must align.
    if proc_list and checks.get("byProcess"):
        process_labels = {p["label"] for p in proc_list}
        check_labels = {entry["label"] for entry in checks["byProcess"]}
        # Every taxonomy process must appear in the per-process checks block.
        missing = process_labels - check_labels
        if missing:
            errors.append(f"checks.json: byProcess missing taxonomy processes {sorted(missing)}")

    # NFT: client bundle must not leak secrets / tokens.
    for marker in SECRET_MARKERS:
        if marker in app_js:
            errors.append(f"site/app.js: must not contain secret marker {marker!r}")

    # --- ФТ-6: documentation --------------------------------------------------
    errors += require(read_text("CHANGELOG.md"), "CHANGELOG.md", "Issue #99")
    readme = read_text("README.md")
    errors += require(readme, "README.md", "Каталог", "Паттерны")

    if errors:
        print("issue-99 pages-optimization validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("issue-99 pages-optimization validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
