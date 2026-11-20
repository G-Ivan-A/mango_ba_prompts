"""Exact reversible #474 migration above the measured #464 prompt layer.

Frozen run inputs are never changed. Unknown edits still fail old byte checks:
only the reviewed, ordered before/after hunks in prompt-edits.json are removed.
"""
import importlib.util
import json
from pathlib import Path
EDITS=json.loads(Path(__file__).with_name('prompt-edits.json').read_text())['files']

# Issue #488: the newer release layer (classification link by SHA) is removed first.
_spec=importlib.util.spec_from_file_location('prompt488', Path(__file__).parent / '../issue_488/prompt_changes.py')
I488=importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(I488)

def revert(path, text):
    text=I488.revert(path, text)
    cursor=0
    for hunk in EDITS.get(path,[]):
        start=text.index(hunk['after'],cursor)
        text=text[:start]+hunk['before']+text[start+len(hunk['after']):]
        cursor=start+len(hunk['before'])
    return text
