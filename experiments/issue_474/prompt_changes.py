"""Exact reversible #474 migration above the measured #464 prompt layer.

Frozen run inputs are never changed. Unknown edits still fail old byte checks:
only the reviewed, ordered before/after hunks in prompt-edits.json are removed.
"""
import json
from pathlib import Path
EDITS=json.loads(Path(__file__).with_name('prompt-edits.json').read_text())['files']

def revert(path, text):
    cursor=0
    for hunk in EDITS.get(path,[]):
        start=text.index(hunk['after'],cursor)
        text=text[:start]+hunk['before']+text[start+len(hunk['after']):]
        cursor=start+len(hunk['before'])
    return text
