"""Точная замена с защитой: каждая замена срабатывает ровно столько раз, сколько ждали.

Общий помощник одноразовых правок issue #464. Несовпадение — ошибка, а не молчаливый пропуск.
"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]


def edit(path, pairs):
    file = ROOT / path
    text = file.read_text(encoding="utf-8")
    for pair in pairs:
        old, new = pair[0], pair[1]
        expected = pair[2] if len(pair) > 2 else 1
        found = text.count(old)
        if found != expected:
            raise SystemExit(f"{path}: ждали {expected}, нашли {found}: {old[:70]!r}")
        text = text.replace(old, new)
    file.write_text(text, encoding="utf-8")
    print(f"правка: {path} ({len(pairs)})")
