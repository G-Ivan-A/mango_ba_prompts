"""Exact reversible #488 release above the #474 prompt layer.

Removes only the reviewed, ordered before/after hunks of `prompt-edits.json`
(classification link pinned to ba-ai-metamodel by SHA, version and date). Any
other edit survives the revert and still fails the old byte checks.
"""
import importlib.util
import json
from pathlib import Path

EDITS = json.loads(Path(__file__).with_name("prompt-edits.json").read_text(encoding="utf-8"))["files"]
spec = importlib.util.spec_from_file_location("debugging509", Path(__file__).parents[1] / "issue_509/prompt_changes.py")
DEBUGGING = importlib.util.module_from_spec(spec)
spec.loader.exec_module(DEBUGGING)


def revert(path, text):
    text = DEBUGGING.revert(path, text)
    cursor = 0
    for hunk in EDITS.get(path, []):
        start = text.index(hunk["after"], cursor)
        text = text[:start] + hunk["before"] + text[start + len(hunk["after"]):]
        cursor = start + len(hunk["before"])
    return text
