"""Обратимая публикация Ш-В v0.2 (BL-156б+в, issue #448, RUN-0084).

RUN-0084 (пред-регистрация `experiments/issue_448/run0084/preregistration.md`)
измерил три плеча Ш-В с одновременным контролем (Р-03). A2 не хуже A0 по
медианам сданных, ядра и ложных дефектов — по лестнице в `prompts/` идёт A2:

- подстановка типа гейта Ш-В из `experiments/issue_438/prompt-typing.json`
  (BL-156б; остальные 14 подстановок не мерились и не применены);
- правило «правка без добавлений» (`run0084/no_additions.py`, BL-156в);
- во frontmatter `version: 0.2` и `updated: 2026-11-04`.

Тело опубликованного файла равно A2 RUN-0084 байт в байт; отличаются только
два поля frontmatter. `published_text()` собирает его из A0, `revert()` —
обратная операция для регрессий сохранности промптов (#391, #393, #395):
они вызывают `revert()` через `bl156a_prompt_changes.revert()` и сверяют
оставшиеся байты со своими эталонами.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PATH = "prompts/bcreq-review-validation-oneshot.md"
RUN = ROOT / "runs/2026/RUN-0084"
TYPING = ROOT / "experiments/issue_438/prompt-typing.json"
FRONTMATTER = (("version: 0.1\n", "version: 0.2\n"), ("updated: 2026-10-24\n", "updated: 2026-11-04\n"))
SHA = {
    "A0": "56dee0cc777870cb33ddf5db18fd2577103bc7611f8d36f5a9b27e46a16e0f9e",
    "A1": "adf826634b2e8190da4d0f4ef307a59104a6f8fa3da6ef5a48a3c923ada90581",
    "A2": "158c743e03db5529db44d1cbafd82541d05935c2cb427259c19c620409f11551",
}


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


RULE = _load("no_additions_v02", ROOT / "experiments/issue_448/run0084/no_additions.py").RULE


def substitutions():
    """Подстановки типа гейта Ш-В (одна строка — отказ fallback)."""
    items = json.loads(TYPING.read_text(encoding="utf-8"))["substitutions"]
    return [s for s in items if s["path"] == PATH]


def measured(arm):
    """Текст плеча RUN-0084 из `runs/2026/RUN-0084/inputs/` (SHA сверяется)."""
    import hashlib

    text = (RUN / f"inputs/prompt-{arm}.md").read_text(encoding="utf-8")
    assert hashlib.sha256(text.encode("utf-8")).hexdigest() == SHA[arm], arm
    return text


def to_published(a2):
    """A2 → опубликованный текст: меняются только `version` и `updated`."""
    for before, after in FRONTMATTER:
        assert a2.count(before) == 1, before
        a2 = a2.replace(before, after)
    return a2


def published_text():
    return to_published(measured("A2"))


def revert(path, text):
    """Опубликованный v0.2 → v0.1 (A0). Другие файлы возвращаются как есть.

    Каждый фрагмент v0.2 обязан встретиться ровно один раз, иначе
    AssertionError: публикация неполна или текст изменён после RUN-0084.
    """
    if path != PATH:
        return text
    for before, after in FRONTMATTER:
        assert text.count(after) == 1, after
        text = text.replace(after, before)
    assert text.count(RULE) == 1, "правило «правка без добавлений»"
    text = text.replace(RULE, "")
    for sub in substitutions():
        assert text.count(sub["after"]) == 1, sub["line"]
        text = text.replace(sub["after"], sub["before"])
    return text
