#!/usr/bin/env python3
"""Проверка карточек фрагментов RUN-0094 v2.0 (issue #486).

Проверки карточек issue #484 (`experiments/issue_484/verify_quotes.py`: шкала, сноски, длины,
каждая цитата дословно в источнике ссылки) применяются к `experiments/issue_486/research/*.json`;
дополнительно — каждая карточка относится к оцениваемому фрагменту (`kind == "req"`
в `fragments.json`), каждый оцениваемый фрагмент имеет карточку ровно одну, фрагмент со
сходством > 90 % с пунктом шаблона содержит «Не требует обоснования» и ссылку на этот пункт.

    MANGO_BA_RUNTIME_MAIN=/tmp/runtime python3 -I experiments/issue_486/verify_cards.py [BATCH]

С аргументом BATCH проверяются только карточки этого батча (полнота — по его `_rows.txt`).
"""
from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "issue_484"))
import ssot  # noqa: E402

# Модуль проверки issue #484 — по пути: `ssot` добавляет в sys.path каталоги других issue,
# где есть одноимённые `verify_quotes.py`.
_spec = importlib.util.spec_from_file_location("verify_quotes_484",
                                               HERE.parent / "issue_484/verify_quotes.py")
verify_quotes = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(verify_quotes)

OVER = "Не требует обоснования"


def cards(only: str | None = None) -> dict[str, dict]:
    """Объединение `research/*.json` issue #486; пересечение ключей запрещено."""
    out: dict[str, dict] = {}
    for path in sorted((HERE / "research").glob("*.json")):
        if only and path.stem != only:
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        overlap = set(out) & set(data)
        assert not overlap, f"{path.name}: повтор фрагментов {overlap}"
        for fid, entry in data.items():
            entry["batch"] = path.stem
            out[fid] = entry
    return out


def main(only: str | None = None) -> int:
    frags = {f["fid"]: f for f in json.loads((HERE / "fragments.json").read_text(encoding="utf-8"))}
    data = cards(only)
    bad = 0
    if only:
        rows = (HERE / "research" / f"{only}_rows.txt").read_text(encoding="utf-8")
        need = set(re.findall(r"^### (.+?!\d+\.\d+) \[req", rows, re.M))
    else:
        need = {fid for fid, f in frags.items() if f["kind"] == "req"}
    for fid in sorted(need - set(data)):
        bad += 1
        print(f"{fid}: нет карточки")
    for fid in sorted(set(data) - need):
        bad += 1
        print(f"{fid}: карточка не оцениваемого фрагмента")
    for fid, entry in data.items():
        missing = {"verdict", "why", "refs", "quotes", "audit"} - set(entry)
        if missing:
            bad += 1
            print(f"{fid}: нет полей {missing}")
            entry.update({k: [] if k in ("refs", "quotes") else "" for k in missing})
        frag = frags.get(fid)
        if frag and frag["kind"] == "req" and frag["sim"]["max"] > 0.9:
            s = frag["sim"]
            items = {s["raw_item"], s["core_item"], s["dice_item"]}
            if OVER not in entry["why"] or not any(f"tv4:{n}" in entry["refs"] for n in items):
                bad += 1
                print(f"{fid}: сходство {s['max']} > 0,9 с п/п {items} — нужна формулировка "
                      f"«{OVER}» и ссылка на пункт")
    ssot.research = lambda: data
    bad += verify_quotes.main()
    print(f"фрагментов к оценке: {len(need)}; карточек: {len(data)}; ошибок полноты/правил: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))
