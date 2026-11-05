"""Обратимые правки промптов issue #450 — верхний слой отката.

Регрессии сохранности (#391, #393, #395, #438, #448) сверяют байты промптов с
эталонами прошлых прогонов. Каждая новая правка должна сниматься здесь точно,
иначе регрессия падает: тихая правка промпта невозможна.

Слой РТ-7 — закрепление runtime на срезе слияния PR #23 и маршрут
`sections_toc` (задача-спица РТ-7, раздел 8 тела PR #23). Поведение в тексте
меняется только в одном месте — порядок чтения базы знаний.

Слой публикации — правки по решениям RUN-0085 (Ш-В v0.3), RUN-0086 (Ш-1, Ш-3, Ш-6
v0.2) и RUN-0087 (Ш-0 v0.2).
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

SHA_OLD = "f31dcde33f0bc120244128faab98fc0162e45701"
SHA_NEW = "68ad8fcffd47439fc3051852d9a2fbbe23815855"
ROUTE_OLD = "`sections_map` → только относящиеся к вопросу разделы. Для нескольких\n"
ROUTE_NEW = (
    "`sections_toc` (оглавление читается за одно обращение; разделы выбирай по\n"
    "`title`) → только относящиеся к вопросу разделы; `sections_map` открывай, только\n"
    "когда нужны `hint`, страницы или токены. Для нескольких\n"
)


REGISTRY_REF = "standards/bcreq-runtime-references.md) {}."


def revert_pin(text: str) -> str:
    """Снять слой РТ-7: новый маршрут и новый SHA → прежние. Прежнего SHA быть не должно."""
    assert SHA_OLD not in text, "прежний SHA рядом с новым"
    text = text.replace(REGISTRY_REF.format("0.5"), REGISTRY_REF.format("0.4"))  # строка черновика
    return text.replace(ROUTE_NEW, ROUTE_OLD).replace(SHA_NEW, SHA_OLD)


def _load(name, rel):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).parent / rel)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


A3 = _load("a3_rule", "run0085/a3_rule.py")
BLOCK = _load("block_rule", "run0086/block_rule.py")
SESSION = _load("session_rules", "run0087/session_rules.py")
SHV = "prompts/bcreq-review-validation-oneshot.md"
UPDATED = "2026-11-05"
FRONT = {  # путь: прежняя версия, новая версия, прежний updated
    SHV: ("0.2", "0.3", "2026-11-04"),
    BLOCK.S1: ("0.1", "0.2", "2026-10-24"),
    BLOCK.S3: ("0.1", "0.2", "2026-10-24"),
    BLOCK.S6: ("0.1", "0.2", "2026-10-24"),
    SESSION.PROMPT: ("0.1", "0.2", "2026-10-24"),
}


def revert_publish(path: str, text: str) -> str:
    """Снять публикацию RUN-0085/86/87. Работает и с черновиками: те содержат текст промпта."""
    text = text.replace(A3.AFTER, A3.BEFORE)
    head = "## 5. Формат вывода\n"
    text = text.replace(BLOCK.RULE + BLOCK.API_RULE + "\n" + head, head)
    text = text.replace(BLOCK.RULE + "\n" + head, head)
    text = text.replace(BLOCK.BLOCK + BLOCK.API_BLOCK, "")
    if path == BLOCK.S3 or BLOCK.S3_STEP_NEW in text:
        text = text.replace(BLOCK.S3_STEP_NEW, BLOCK.S3_STEP).replace(BLOCK.BLOCK, BLOCK.S3_FMT)
    else:
        text = text.replace(BLOCK.BLOCK, "")
    text = text.replace(SESSION.ROWS, "")
    source = path.replace("prompts/drafts/", "prompts/")
    if source in FRONT:
        old_v, new_v, old_u = FRONT[source]
        text = text.replace(f"version: {new_v}\n", f"version: {old_v}\n").replace(f"updated: {UPDATED}\n", f"updated: {old_u}\n")
    return text


def revert(path: str, text: str) -> str:
    return revert_pin(revert_publish(path, text))
