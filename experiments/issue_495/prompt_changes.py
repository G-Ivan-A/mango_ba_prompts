"""Обратимые правки промптов issue #495 — верхний слой цепочки откатов.

``revert(path, text)`` снимает ровно правки из ``prompt-edits.json`` (собирает
``build_prompt_edits.py``) и возвращает текст на базе задачи. Ханк не найден —
исключение, а не молчаливый пропуск: правка вне реестра ломает старые
регрессии сохранности, как и раньше.
"""
import json
from pathlib import Path

_DATA = Path(__file__).with_name("prompt-edits.json")
EDITS = json.loads(_DATA.read_text(encoding="utf-8"))["files"] if _DATA.exists() else {}


def apply_hunks(text, hunks):
    cursor = 0
    for hunk in hunks:
        start = text.index(hunk["after"], cursor)
        text = text[:start] + hunk["before"] + text[start + len(hunk["after"]):]
        cursor = start + len(hunk["before"])
    return text


def revert(path, text):
    """Текст файла ``path`` (от корня репо) без правок #495."""
    entry = EDITS.get(str(path))
    return apply_hunks(text, entry["hunks"]) if entry else text
