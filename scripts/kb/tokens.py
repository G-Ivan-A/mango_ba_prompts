#!/usr/bin/env python3
"""Подсчёт токенов для оценки расхода контекста при обращении к БЗ.

Зачем. Один из приоритетов issue #111 — измеримая оптимизация токенов
(весь документ vs только нужный раздел). Чтобы цифры в отчёте и в
``meta.json`` были **реальными, а не выдуманными**, токены считаются здесь
единым способом.

Метод (в порядке приоритета):

1. ``tiktoken`` (кодировщик ``cl100k_base``) — если установлен. Это токенизатор
   семейства GPT-4/3.5; для смешанного RU/EN-текста даёт близкую к реальной
   оценку и воспроизводимый результат.
2. Эвристика ``символы / 3.3`` — fallback без внешних зависимостей. Делитель
   3.3 откалиброван под кириллицу в ``cl100k_base`` (кириллица «дороже»
   латиницы: ~2–3 байта/символ → ~3 символа/токен). Это **оценка сверху-снизу**,
   которой достаточно для сравнения «весь документ vs раздел».

Использованный метод всегда фиксируется (``method()``) и пишется в ``meta.json``
полем ``token_method`` — чтобы цифры были воспроизводимы и честны.

CLI::

    python3 scripts/kb/tokens.py path/to/file.md      # токены файла
    echo "текст" | python3 scripts/kb/tokens.py -     # токены из stdin
"""

from __future__ import annotations

import sys

# Калибровочный делитель эвристики (символов на токен) для кириллицы в cl100k.
_HEURISTIC_CHARS_PER_TOKEN = 3.3

_encoder = None
_method = None


def _load_encoder():
    """Лениво загружает tiktoken; возвращает (encoder|None, method_label)."""
    global _encoder, _method
    if _method is not None:
        return _encoder, _method
    try:
        import tiktoken

        _encoder = tiktoken.get_encoding("cl100k_base")
        _method = "tiktoken:cl100k_base"
    except Exception:
        _encoder = None
        _method = f"heuristic:chars/{_HEURISTIC_CHARS_PER_TOKEN}"
    return _encoder, _method


def count_tokens(text: str) -> int:
    """Возвращает число токенов в ``text`` выбранным методом."""
    if not text:
        return 0
    encoder, _ = _load_encoder()
    if encoder is not None:
        return len(encoder.encode(text))
    return int(round(len(text) / _HEURISTIC_CHARS_PER_TOKEN))


def method() -> str:
    """Метка использованного метода (для ``meta.json`` / отчёта)."""
    _load_encoder()
    return _method


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__)
        return 2
    if argv[1] == "-":
        text = sys.stdin.read()
    else:
        with open(argv[1], "r", encoding="utf-8") as handle:
            text = handle.read()
    print(f"{count_tokens(text)} tokens ({method()})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
