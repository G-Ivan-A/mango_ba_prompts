#!/usr/bin/env python3
"""Проверка: каждая цитата [i] колонки 5 встречается дословно в источнике ссылки [i] колонки 4.

Источник — тело раздела БЗ (`kb:`), текст пункта шаблона ТЗ-тендеров-v4 (`tv4:`).
Ссылки портала (`portal:`) не проверяются офлайн и выводятся списком.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import generate_run as g  # noqa: E402


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.replace(" ", " ").replace("**", "")).strip()


bad = 0
for rid, entry in sorted(g.load().items()):
    for ref, quote in zip(entry["refs"], entry["quotes"]):
        kind, _, value = ref.partition(":")
        if kind == "portal":
            print(f"{rid}: portal (не проверяется офлайн): {value}")
            continue
        corpus = norm(g.kb_path(value).read_text(encoding="utf-8") if kind == "kb" else g.tender_text(value))
        for frag in quote.split("…"):
            frag = norm(frag.strip(" .•;"))
            if len(frag) > 8 and frag not in corpus:
                bad += 1
                print(f"{rid} {ref}: NOT FOUND: {frag[:100]}")
print("mismatches:", bad)
sys.exit(1 if bad else 0)
