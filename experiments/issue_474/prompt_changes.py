"""Exact reversible #474 migration above the measured #464 prompt layer.

Frozen run inputs are never changed. Unknown edits still fail old byte checks:
only the reviewed, ordered before/after hunks in prompt-edits.json are removed.
"""
import importlib.util
import json
from pathlib import Path
EDITS=json.loads(Path(__file__).with_name('prompt-edits.json').read_text())['files']

# Issue #495: снять #488, затем #495, до отката #474.
_spec=importlib.util.spec_from_file_location('prompt495', Path(__file__).parent/'../issue_495/prompt_changes.py')
I495=importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(I495)

def revert(path, text):
    text=I495.revert(path, text)
    cursor=0
    for hunk in EDITS.get(path,[]):
        start=text.index(hunk['after'],cursor)
        text=text[:start]+hunk['before']+text[start+len(hunk['after']):]
        cursor=start+len(hunk['before'])
    return text
