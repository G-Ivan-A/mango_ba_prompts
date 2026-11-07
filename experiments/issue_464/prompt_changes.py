"""Обратимые правки промптов issue #464 — верхний слой отката.

Регрессии сохранности (#391, #393, #395, #438, #448, #450) сверяют байты промптов с
эталонами прошлых прогонов. Правка, которой нет в `prompt-edits.json`, остаётся после
отката, и регрессия падает: тихая правка промпта по-прежнему невозможна.

Ш-В не менялся. В его черновике меняется только номер версии профилей в шапке блока:
каталог и строки профилей этого шага прежние.
"""
from __future__ import annotations

import json
import importlib.util
from pathlib import Path

EDITS = json.loads(Path(__file__).with_name("prompt-edits.json").read_text(encoding="utf-8"))["files"]
SHV_DRAFT = "prompts/drafts/bcreq-review-validation-oneshot.md"
PROFILES_REF = "standards/bcreq-prompt-profiles.md) {},"


_spec = importlib.util.spec_from_file_location('prompt474', Path(__file__).parent / '../issue_474/prompt_changes.py')
I474 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(I474)


def revert(path: str, text: str) -> str:
    """Снять правки #464; ханк не нашёлся — исключение, а не молчаливый пропуск."""
    text = I474.revert(path, text)
    if path == SHV_DRAFT:
        return text.replace(PROFILES_REF.format("0.1.2"), PROFILES_REF.format("0.1.1"))
    cursor = 0
    for hunk in EDITS.get(path, []):
        start = text.index(hunk["after"], cursor)
        text = text[:start] + hunk["before"] + text[start + len(hunk["after"]):]
        cursor = start + len(hunk["before"])
    return text
