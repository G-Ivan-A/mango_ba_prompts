#!/usr/bin/env python3
"""Проверка исследовательских карточек BCREQ-1199 v2 (issue #484).

Контроль против додумывания: каждая цитата [i] встречается дословно в источнике ссылки [i] —
в теле раздела БЗ без frontmatter (`kb:`) либо в тексте пункта шаблона ТЗ-тендеров-v4 (`tv4:`).
Сравнение без учёта пробельных символов, `<br>`, маркеров списка и разметки `**`; `…`
разделяет фрагменты одной ссылки. Ссылки портала (`portal:`) офлайн не проверяются и
выводятся списком для ручной сверки.

Дополнительно: вердикт строго по шкале контракта, число ссылок равно числу цитат, каждой
ссылке соответствует ровно одна сноска `[i]` в `why`, длина цитаты 30–250 символов, в цитате
нет «», `|` и `<br>`, длина `why` ≤ 1500 и `audit` ≤ 600 символов, вердикты «Да» и «Частично»
подкреплены хотя бы одной ссылкой.

    MANGO_BA_RUNTIME_MAIN=/tmp/runtime python3 -I experiments/issue_484/verify_quotes.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ssot  # noqa: E402

VERDICTS = ("Да", "Частично", "Нет", "")
LIMITS = {"why": 1500, "audit": 600}


def main() -> int:
    entries = ssot.research()
    bad = quotes = 0
    portal: list[str] = []
    for rid, entry in sorted(entries.items()):
        refs, qs = entry["refs"], entry["quotes"]
        if entry["verdict"] not in VERDICTS:
            bad += 1
            print(f"{rid}: вердикт вне шкалы: {entry['verdict']!r}")
        if len(refs) != len(qs):
            bad += 1
            print(f"{rid}: ссылок {len(refs)}, цитат {len(qs)}")
        if entry["verdict"] in ("Да", "Частично") and not refs:
            bad += 1
            print(f"{rid}: вердикт {entry['verdict']} без ссылок")
        for field, limit in LIMITS.items():
            if len(entry[field]) > limit:
                bad += 1
                print(f"{rid}: {field} длиннее {limit} символов ({len(entry[field])})")
        if "|" in entry["why"] + entry["audit"]:
            bad += 1
            print(f"{rid}: символ | в why/audit")
        markers = sorted(int(m) for m in re.findall(r"\[(\d+)\]", entry["why"]))
        if markers != list(range(1, len(refs) + 1)):
            bad += 1
            print(f"{rid}: сноски {markers} не соответствуют ссылкам ({len(refs)})")
        for ref, quote in zip(refs, qs):
            quotes += 1
            kind, _, value = ref.partition(":")
            if kind == "portal":
                portal.append(f"{rid}: {value}")
                if not 30 <= len(quote) <= 250 or any(ch in quote for ch in "«»|") or "<br>" in quote:
                    bad += 1
                    print(f"{rid} {ref}: недопустимая цитата (длина {len(quote)} либо символы «»|<br>)")
                continue
            try:
                corpus = ssot.norm(ssot.body(ssot.kb_path(value)) if kind == "kb"
                                   else ssot.tender_text(value))
            except (KeyError, FileNotFoundError):
                bad += 1
                print(f"{rid} {ref}: источник не найден")
                continue
            # Цитата короче 30 символов допустима, только если это пункт источника целиком
            # (п/п 9.2 шаблона — «Доступность системы 99,9%»).
            short_ok = ssot.norm(quote) == corpus
            if not (30 <= len(quote) <= 250 or short_ok) or any(ch in quote for ch in "«»|") \
                    or "<br>" in quote:
                bad += 1
                print(f"{rid} {ref}: недопустимая цитата (длина {len(quote)} либо символы «»|<br>)")
            for frag in quote.split("…"):
                frag = ssot.norm(frag.strip(" .•;"))
                if len(frag) > 8 and frag not in corpus:
                    bad += 1
                    print(f"{rid} {ref}: НЕ НАЙДЕНО: {frag[:120]}")
    for line in portal:
        print("portal (офлайн не проверяется):", line)
    print(f"строк: {len(entries)}; цитат: {quotes}; portal: {len(portal)}; расхождений: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
