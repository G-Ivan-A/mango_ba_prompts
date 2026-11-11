#!/usr/bin/env python3
"""Проверка цитат RUN-0093 (issue #482).

Каждая цитата [i] колонки 5 встречается дословно в источнике ссылки [i] колонки 4: тело
раздела БЗ без frontmatter (`kb:`), текст пункта шаблона ТЗ-тендеров-v4 (`tv4:`). Проверяются
и ручные оценки (`research/*.json`), и автоматические строки правила > 90 %. Ссылки портала
(`portal:`) офлайн не проверяются и выводятся списком. Сравнение без учёта пробельных
символов, переводов строк `<br>` в ячейках таблиц БЗ, маркеров списка и разметки `**`; `…` разделяет фрагменты одной ссылки.
Для ручных оценок дополнительно: длина цитаты 30–250 символов, в цитате нет «», `|` и
`<br>`; длина `why` и `audit` ≤ 300; каждой ссылке соответствует ровно одна сноска.

    MANGO_BA_RUNTIME_MAIN=/tmp/rt-main python3 -I experiments/issue_482/verify_quotes.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import generate_run as g  # noqa: E402


def norm(s: str) -> str:
    s = s.replace("<br>", " ")
    s = s.replace(" ", " ").replace("**", "").replace("", " ").replace("•", " ")
    return re.sub(r"\s+", " ", s).strip()


def body(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    return text.split("\n---\n", 1)[1] if text.startswith("---\n") else text


bad = quotes = 0
portal = []
_src, pairs = g.evaluate()
for (rid, *_row), entry in pairs:
    manual = entry["kind"] == "research"
    if manual:
        for field in ("why", "audit"):
            if len(entry[field]) > 300:
                bad += 1
                print(f"{rid}: {field} длиннее 300 символов ({len(entry[field])})")
        if "|" in entry["why"] + entry["audit"]:
            bad += 1
            print(f"{rid}: символ | в why/audit")
        markers = sorted(int(m) for m in re.findall(r"\[(\d+)\]", entry["why"]))
        if markers != list(range(1, len(entry["refs"]) + 1)):
            bad += 1
            print(f"{rid}: сноски {markers} не соответствуют ссылкам ({len(entry['refs'])})")
    for ref, quote in zip(entry["refs"], entry["quotes"]):
        quotes += 1
        if manual and (not 30 <= len(quote) <= 250 or any(ch in quote for ch in "«»|") or "<br>" in quote):
            bad += 1
            print(f"{rid} {ref}: недопустимая цитата (длина {len(quote)} или символы «»|<br>)")
        kind, _, value = ref.partition(":")
        if kind == "portal":
            portal.append(f"{rid}: {value}")
            continue
        corpus = norm(body(g.kb_path(value)) if kind == "kb" else g.tender_text(value))
        for frag in quote.split("…"):
            frag = norm(frag.strip(" .•;"))
            if len(frag) > 8 and frag not in corpus:
                bad += 1
                print(f"{rid} {ref}: NOT FOUND: {frag[:100]}")
for line in portal:
    print("portal (не проверяется офлайн):", line)
print(f"rows: {len(pairs)}; quotes: {quotes}; portal: {len(portal)}; mismatches: {bad}")
sys.exit(1 if bad else 0)
