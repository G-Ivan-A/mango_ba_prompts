"""Remove only reviewed #509 hunks before historical byte comparisons."""
import json
from pathlib import Path

DATA = Path(__file__).with_name("prompt-edits.json")
EDITS = json.loads(DATA.read_text())["files"] if DATA.exists() else {}


def revert(path, text):
    cursor = 0
    for hunk in EDITS.get(str(path), {}).get("hunks", []):
        start = text.index(hunk["after"], cursor)
        text = text[:start] + hunk["before"] + text[start + len(hunk["after"]):]
        cursor = start + len(hunk["before"])
    return text
