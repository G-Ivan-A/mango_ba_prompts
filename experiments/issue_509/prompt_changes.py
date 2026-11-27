"""Remove reviewed #509 changes and its follow-up before historical byte comparisons."""
from functools import lru_cache
import json
from pathlib import Path
import subprocess

DATA = Path(__file__).with_name("prompt-edits.json")
EDITS = json.loads(DATA.read_text())["files"] if DATA.exists() else {}
FOLLOWUP = json.loads(DATA.with_name("prompt-editions-0.5.json").read_text())
ROOT = DATA.parents[2]


@lru_cache(maxsize=None)
def git_text(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT).decode("utf-8")


def revert_followup(path, text):
    blob = FOLLOWUP["files"].get(str(path))
    if blob is None:
        return text
    reviewed = git_text("cat-file", "blob", blob)
    if reviewed not in text:
        raise ValueError(f"{path}: draft differs from the reviewed 0.5 edition")
    before = git_text("show", f"{FOLLOWUP['base']}:{path}")
    return text.replace(reviewed, before, 1)


def revert(path, text):
    text = revert_followup(path, text)
    cursor = 0
    for hunk in EDITS.get(str(path), {}).get("hunks", []):
        start = text.index(hunk["after"], cursor)
        text = text[:start] + hunk["before"] + text[start + len(hunk["after"]):]
        cursor = start + len(hunk["before"])
    return text
