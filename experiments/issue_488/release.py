#!/usr/bin/env python3
"""Issue #488: prompt release that pins the Hub classification link by SHA.

The BA meta-model left the Hub (`G-Ivan-A/hybrid-Intelligence-lab`) for
`G-Ivan-A/ba-ai-metamodel`; the Hub deletes `research/mango/`, so the floating
link `blob/main/research/mango/2026-05-22-classification.md` in the published
prompts stops resolving. The same file lives in ba-ai-metamodel at the E6
acceptance commit under the same path.

For every published prompt `prompts/bcreq-*.md` that still carries the floating
link this script

* replaces the link with the pinned one (the object stays the same file);
* raises `version` by one minor step and sets `updated` to the release date.

Nothing else in the prompt changes. Then it rebuilds the step drafts with
`scripts/build_bcreq_step_prompts.py` (the builder pins the same link and dates
the drafts `PIN_DATE`). Each edit of a published prompt and of a draft is
recorded as an ordered before/after hunk in `prompt-edits.json`;
`prompt_changes.revert` removes exactly these hunks, so the byte-level
preservation checks of earlier issues keep comparing the measured text. In a
draft the `based_on_sha256` line is not a hunk: it is the hash of the current
published prompt and the checks recompute it themselves, as for earlier layers. Archive `prompts/archive/` and measured run inputs
are historical records and are not touched (issue #488, item 2).

Usage::

    python3 experiments/issue_488/release.py           # apply once on the pre-release tree
    python3 experiments/issue_488/release.py --check   # prompts and drafts match prompt-edits.json
"""
import argparse
import difflib
import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EDITS = Path(__file__).with_name("prompt-edits.json")
DATE = "2026-11-20"
FLOATING = ("https://github.com/G-Ivan-A/hybrid-Intelligence-lab" + "/blob/main/"
            "research/mango/2026-05-22-classification.md")
PINNED = ("https://github.com/G-Ivan-A/ba-ai-metamodel/blob/"
          "e1f67e267beb73809e1edb26313691a5c769c92a/research/mango/2026-05-22-classification.md")


def bump(version):
    major, minor = version.split(".")
    return f"{major}.{int(minor) + 1}"


def plan(text):
    """Ordered (before, after) hunks of the #488 release for one prompt."""
    version = re.search(r"(?m)^version: (\d+\.\d+)$", text).group(1)
    updated = re.search(r"(?m)^updated: (\S+)$", text).group(1)
    hunks = [(f"version: {version}\nupdated: {updated}\n", f"version: {bump(version)}\nupdated: {DATE}\n")]
    for line in text.splitlines(keepends=True):
        if FLOATING in line:
            hunks.append((line, line.replace(FLOATING, PINNED)))
    return hunks


def draft_hunks(old, new):
    """Line hunks old → new draft; the based_on_sha256 line is left to the checks."""
    a, b = old.splitlines(keepends=True), new.splitlines(keepends=True)
    hunks = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag == "equal":
            continue
        before, after = "".join(a[i1:i2]), "".join(b[j1:j2])
        if tag == "replace" and i2 - i1 == j2 - j1 == 1 and before.startswith("based_on_sha256: "):
            continue
        if tag != "replace":
            raise SystemExit(f"#488: unexpected {tag} in a draft: {before!r} → {after!r}")
        hunks.append((before, after))
    return hunks


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def apply(text, hunks):
    cursor = 0
    for before, after in hunks:
        start = text.index(before, cursor)
        text = text[:start] + after + text[start + len(before):]
        cursor = start + len(after)
    return text


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    if args.check:
        layer = load("p488", Path(__file__).with_name("prompt_changes.py"))
        files = json.loads(EDITS.read_text(encoding="utf-8"))["files"]
        for rel in files:
            text = (ROOT / rel).read_text(encoding="utf-8")
            if FLOATING in text or apply(layer.revert(rel, text), [(h["before"], h["after"]) for h in files[rel]]) != text:
                raise SystemExit(f"#488: {rel} differs from prompt-edits.json")
        print(f"#488 release: OK ({len(files)} prompt(s) and draft(s) match prompt-edits.json)")
        return 0
    files = {}
    for path in sorted((ROOT / "prompts").glob("bcreq-*.md")):
        text = path.read_text(encoding="utf-8")
        if FLOATING not in text:
            continue
        hunks = plan(text)
        path.write_text(apply(text, hunks), encoding="utf-8")
        files[path.relative_to(ROOT).as_posix()] = [{"before": b, "after": a} for b, a in hunks]
    builder = load("step_builder_488", ROOT / "scripts/build_bcreq_step_prompts.py")
    for path, new in builder.build_all().items():
        old = path.read_text(encoding="utf-8")
        if path.suffix == ".md" and old != new:
            hunks = draft_hunks(old, new)
            if hunks:
                files[path.relative_to(ROOT).as_posix()] = [{"before": b, "after": a} for b, a in hunks]
        path.write_text(new, encoding="utf-8")
    EDITS.write_text(json.dumps({
        "issue": "https://github.com/G-Ivan-A/mango_ba_prompts/issues/488",
        "date": DATE,
        "floating": FLOATING,
        "pinned": PINNED,
        "files": files,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"#488 release: {len(files)} prompt(s) pinned")
    return 0


if __name__ == "__main__":
    sys.exit(main())
