"""Точное снятие слоёв #488 → #495 перед проверкой измеренных промптов.

``revert(path, text)`` сначала снимает релиз #488 действующим обратимым слоем,
затем снимает правки чистоты по ханкам, рассчитанным для текста без #488.
Ханк должен присутствовать в точности. Остальные изменения остаются видны
в старых побайтовых сверках.
"""
import importlib.util
import json
from pathlib import Path

_DATA = Path(__file__).with_name("prompt-edits.json")
EDITS = json.loads(_DATA.read_text(encoding="utf-8"))["files"] if _DATA.exists() else {}
_spec = importlib.util.spec_from_file_location(
    "prompt488_for_495", _DATA.parent.parent / "issue_488/prompt_changes.py"
)
RELEASE = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(RELEASE)


def apply_hunks(text, hunks):
    cursor = 0
    for hunk in hunks:
        start = text.index(hunk["after"], cursor)
        text = text[:start] + hunk["before"] + text[start + len(hunk["after"]):]
        cursor = start + len(hunk["before"])
    return text


def revert(path, text):
    """Текст файла (путь от корня репо) без слоёв #488 и #495."""
    path = str(path)
    text = RELEASE.revert(path, text)
    entry = EDITS.get(path)
    return apply_hunks(text, entry["hunks"]) if entry else text
