"""Обратимые правки промптов issue #450 — верхний слой отката.

Регрессии сохранности (#391, #393, #395, #438, #448) сверяют байты промптов с
эталонами прошлых прогонов. Каждая новая правка должна сниматься здесь точно,
иначе регрессия падает: тихая правка промпта невозможна.

Слой РТ-7 — закрепление runtime на срезе слияния PR #23 и маршрут
`sections_toc` (задача-спица РТ-7, раздел 8 тела PR #23). Поведение в тексте
меняется только в одном месте — порядок чтения базы знаний.
"""
from __future__ import annotations

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


def revert(path: str, text: str) -> str:
    return revert_pin(text)
