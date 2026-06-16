#!/usr/bin/env python3
"""Local regression check for issue #91 GitHub Pages enhancements.

Locks the requirements re-issued after PR #90:
- catalog is rendered before dashboard and roadmap (ФТ-1);
- filter order is Процессы БА -> Операции -> Режимы (ФТ-2);
- cascade + AND/OR filtering helpers exist (ФТ-2, ФТ-3);
- the "Проверки" module and its checks data replace "Мультиагенты" (ФТ-4);
- the prompt-feedback static source exists (ФТ-4).
"""

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


def require_order(text: str, path: str, *needles: str) -> list[str]:
    errors: list[str] = []
    last = -1
    last_needle = ""
    for needle in needles:
        index = text.find(needle)
        if index == -1:
            errors.append(f"{path}: missing {needle!r}")
            continue
        if index < last:
            errors.append(f"{path}: {needle!r} must appear after {last_needle!r}")
        last = index
        last_needle = needle
    return errors


def main() -> int:
    errors: list[str] = []

    required_files = (
        "site/data/checks.json",
        "governance/prompt-feedback.json",
    )
    for path in required_files:
        errors += require_file(path)

    if errors:
        print("issue-91 pages enhancements validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    index_html = read_text("site/index.html")
    app_js = read_text("site/app.js")

    # ФТ-1: каталог отображается первым (раньше дашборда и roadmap).
    errors += require_order(
        index_html,
        "site/index.html",
        'id="catalog"',
        'id="dashboard"',
        'id="checks"',
        'id="roadmap"',
    )
    errors += require(index_html, "site/index.html", "checks-grid", "Проверки")

    # ФТ-2: порядок фильтров Процессы БА -> Операции -> Режимы.
    errors += require_order(
        app_js,
        "site/app.js",
        'renderFilterGroup("Процессы БА"',
        'renderFilterGroup("Операции"',
        'renderFilterGroup("Режимы"',
    )

    # ФТ-2/ФТ-3: каскад и И/ИЛИ-логика фильтров.
    errors += require(
        app_js,
        "site/app.js",
        "availableOperationIds",
        "selectedValues",
        "renderChecks",
        "data/checks.json",
    )

    # ФТ-4: модуль "Проверки" с активностью и обратной связью.
    checks = read_json("site/data/checks.json")
    for key in ("statuses", "tests", "feedback", "activity", "prompts"):
        if key not in checks:
            errors.append(f"site/data/checks.json: missing {key!r}")

    statuses = checks.get("statuses", {})
    status_total = sum(statuses.get(name, 0) for name in ("draft", "canonical", "archived"))
    if status_total != 30:
        errors.append(
            f"site/data/checks.json: statuses must cover all 30 prompts, found {status_total}"
        )

    tests = checks.get("tests", {})
    for key in ("logs", "total", "coveredPrompts"):
        if key not in tests:
            errors.append(f"site/data/checks.json: tests missing {key!r}")
    if tests.get("logs", 0) < 1:
        errors.append("site/data/checks.json: expected at least one experiments log")

    feedback = checks.get("feedback", {})
    if feedback.get("label") != "prompt:feedback":
        errors.append("site/data/checks.json: feedback.label must be 'prompt:feedback'")

    feedback_source = read_json("governance/prompt-feedback.json")
    if not isinstance(feedback_source.get("entries"), list):
        errors.append("governance/prompt-feedback.json: 'entries' must be a list")

    changelog = read_text("CHANGELOG.md")
    errors += require(changelog, "CHANGELOG.md", "Issue #91")

    if errors:
        print("issue-91 pages enhancements validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("issue-91 pages enhancements validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
