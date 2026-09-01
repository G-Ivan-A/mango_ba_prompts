#!/usr/bin/env python3
"""Validate local KB citations against the linked section frontmatter.

Page-bearing citations are accepted only when document, section, title, and
pages match the linked ``kb/processed/**/sections/*.md`` file.  A citation may
omit pages as an explicit fallback, but it must still resolve to the declared
document and section.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from urllib.parse import unquote


LINK = re.compile(r"\[([^\[\]]+)\]\(([^()\s]+)\)")
CITATION = re.compile(
    r"^(?P<doc>[^,]+),\s*§(?P<section>[^,\s«]+)"
    r"(?:\s+«(?P<title>[^»]*)»)?"
    r"(?:,\s*с\.(?P<pages>.+))?$"
)


def normalize(value: str) -> str:
    return re.sub(r"\s+", "", value.replace("–", "-").replace("—", "-")).strip()


def frontmatter(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    data: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" not in line or line.startswith((" ", "-")):
            continue
        key, _, value = line.partition(":")
        value = value.strip()
        if len(value) > 1 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        data[key.strip()] = value
    return data


def document_aliases(meta: dict[str, str]) -> set[str]:
    aliases = {meta.get("doc_code", "")}
    source = meta.get("source", "")
    if source:
        aliases.add(Path(source).stem)
    return {alias for alias in aliases if alias}


def validate_report(report: Path, root: Path) -> tuple[int, list[str]]:
    errors: list[str] = []
    checked = 0
    text = report.read_text(encoding="utf-8")
    processed = (root / "kb/processed").resolve()

    for label, href in LINK.findall(text):
        match = CITATION.match(label.strip())
        if not match or href.startswith(("http://", "https://", "mailto:")):
            continue
        target = (report.parent / unquote(href.split("#", 1)[0])).resolve()
        try:
            target.relative_to(processed)
        except ValueError:
            continue
        if "sections" not in target.parts:
            continue
        checked += 1
        try:
            meta = frontmatter(target)
        except OSError as exc:
            errors.append(f"{report}: missing citation target {target}: {exc}")
            continue
        if not meta:
            errors.append(f"{target}: missing YAML frontmatter")
            continue

        cited_doc = match.group("doc").strip()
        aliases = document_aliases(meta)
        if cited_doc not in aliases:
            errors.append(f"{target}: document {cited_doc!r}, frontmatter aliases {sorted(aliases)!r}")

        actual_section = meta.get("pdf_section", "") or meta.get("section", "")
        if actual_section in {"0", "-", "—"}:
            actual_section = ""
        cited_section = match.group("section").strip()
        if cited_section != actual_section:
            errors.append(f"{target}: section {cited_section!r}, frontmatter {actual_section!r}")

        cited_title = match.group("title")
        if cited_title is not None and cited_title.strip() != meta.get("title", ""):
            errors.append(f"{target}: title {cited_title.strip()!r}, frontmatter {meta.get('title', '')!r}")

        cited_pages = match.group("pages")
        if cited_pages is not None:
            expected_pages = normalize(meta.get("pages", ""))
            actual_pages = normalize(cited_pages)
            if actual_pages != expected_pages:
                errors.append(f"{target}: pages {actual_pages!r}, frontmatter {expected_pages!r}")

    if checked == 0:
        errors.append(f"{report}: no local atomic KB citations found")
    return checked, errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("reports", nargs="+", type=Path, help="Markdown report(s) to validate")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()

    root = args.root.resolve()
    total = 0
    errors: list[str] = []
    for report_arg in args.reports:
        report = report_arg if report_arg.is_absolute() else root / report_arg
        try:
            checked, report_errors = validate_report(report.resolve(), root)
        except OSError as exc:
            checked, report_errors = 0, [f"{report}: {exc}"]
        total += checked
        errors.extend(report_errors)

    if errors:
        print(f"FAIL: validate_pagination_shift: {len(errors)} problem(s)")
        for error in errors[:40]:
            print(f"  - {error}")
        return 1
    print(f"OK: validate_pagination_shift: {total} citation(s) match section frontmatter")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
