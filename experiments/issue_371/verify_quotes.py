#!/usr/bin/env python3
"""Проверка цитат RUN-0072 (issue #371).

1. Каждая цитата [i] колонки 5 Отчёта 1 встречается дословно в источнике ссылки [i] колонки 4:
   тело раздела БЗ (`kb:`), текст пункта шаблона ТЗ-тендеров-v4 (`tv4:`). Ссылки портала
   (`portal:`) офлайн не проверяются и выводятся списком.
2. Каждый фрагмент «Было» Отчёта 2 встречается в тексте ТЗ 2025 (pymupdf), каждый фрагмент
   «Стало» — в строках ТЗ 2026 из `source_transcription.json`, на которые ссылается запись.
   Сравнение без учёта пробелов и регистра; перенос «-» в конце строки PDF читается и как мягкий, и как дефис.

    MANGO_BA_RUNTIME_MAIN=/tmp/rt-main python3 -I experiments/issue_371/verify_quotes.py /path/to/tz2025.pdf
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import generate_run as g  # noqa: E402


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.replace("\u00a0", " ").replace("**", "")).strip()


def squash(s: str) -> str:
    return re.sub(r"\s+", "", s.replace("\uf02d", "-")).lower()


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

import pymupdf  # noqa: E402

pdf = Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/dl371/tz2025/tz2025.pdf")
text = "\n".join(p.get_text() for p in pymupdf.open(pdf))
# перенос в PDF бывает и мягким («пре-\nдоставление»), и настоящим дефисом («SIP-\nTrunk»): проверяются оба прочтения
old = (squash(re.sub(r"(?<=[А-Яа-яЁёA-Za-z])-\n", "", text)), squash(text))
rows = {rid: f"{num} {req}" for rid, num, req, _ in
        json.loads((g.HERE / "source_transcription.json").read_text(encoding="utf-8"))["rows"]}
delta = json.loads((g.HERE / "delta.json").read_text(encoding="utf-8"))
for n, entry in enumerate(delta, start=1):
    if entry["was"] and not any(squash(entry["was"]) in o for o in old):
        bad += 1
        print(f"delta {n}: «Было» NOT FOUND in ТЗ 2025: {entry['was'][:80]}")
    if entry["now"] and entry["rows"] and squash(entry["now"]) not in squash(" ".join(rows[r] for r in entry["rows"])):
        bad += 1
        print(f"delta {n}: «Стало» NOT FOUND in rows {entry['rows']}: {entry['now'][:80]}")
    if entry["now"] and not entry["rows"]:
        bad += 1
        print(f"delta {n}: «Стало» без строк ТЗ 2026")
print(f"delta entries: {len(delta)}; mismatches:", bad)
sys.exit(1 if bad else 0)
