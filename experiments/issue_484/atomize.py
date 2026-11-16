#!/usr/bin/env python3
"""Атомарная декомпозиция строк исходника BCREQ-1199 v2 и сходство с шаблоном v4.

Требования исходника — составные (вводная фраза + перечень через `\n- `), поэтому
для оценки «Частично» (контракт issue #484, §2) каждая строка разбирается на атомарные
части: вводная фраза и каждый пункт перечня отдельно. Для каждой части считается
сходство с пунктами «Шаблона ТЗ для тендеров v4» по метрикам RUN-0070…RUN-0093
(raw / core / dice, `experiments/issue_482/tender_similarity.py`).

    python3 experiments/issue_484/atomize.py

Результат — `atoms.json` (части строк) и `atom_similarity.json` (лучшие п/п шаблона).
"""
import difflib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "issue_482"))
from tender_similarity import PAGE, core, dice, items, low  # noqa: E402

SHEETS = ("Требования к системе", "SLA")


def atoms(text):
    """Строка ТЗ -> атомарные части: вводная фраза и каждый пункт перечня."""
    parts, buf = [], []
    for line in text.split("\n"):
        stripped = line.strip().lstrip(" ").strip()
        if re.match(r"^[-–—•]\s*", stripped):
            if buf:
                parts.append("\n".join(buf).strip())
                buf = []
            parts.append(re.sub(r"^[-–—•]\s*", "", stripped))
        else:
            buf.append(line)
    if buf and "\n".join(buf).strip():
        parts.append("\n".join(buf).strip())
    return [p for p in parts if p]


def best(text):
    r, n = max((difflib.SequenceMatcher(None, low(text), low(t[:len(text) + 40])).ratio(), n)
               for n, t in items)
    c, cn = max((difflib.SequenceMatcher(None, core(text), core(t)).ratio(), n) for n, t in items)
    d, dn = max((dice(text, t), n) for n, t in items)
    return {"raw": round(r, 3), "raw_item": n, "core": round(c, 3), "core_item": cn,
            "dice": round(d, 3), "dice_item": dn, "max": round(max(r, c, d), 3)}


def main():
    src = json.loads((HERE / "source_transcription.json").read_text(encoding="utf-8"))
    out, sim = [], {}
    for sheet in src["sheets"]:
        if sheet["title"] not in SHEETS:
            continue
        for row in sheet["rows"]:
            ri, values = row[0], row[1:]
            if not any(values):
                continue
            num = values[0]
            text = values[1] if len(values) > 1 else ""
            tail = values[2] if sheet["title"] == "SLA" and len(values) > 2 else ""
            full = "\n".join(t for t in (text, tail) if t)
            rid = f'{sheet["title"]}!{ri}'
            parts = atoms(full)
            out.append({"rid": rid, "sheet": sheet["title"], "row": ri, "num": num,
                        "text": text, "tail": tail, "atoms": parts})
            for i, p in enumerate(parts, 1):
                sim[f"{rid}#{i}"] = {"text": p, **best(p)}
    (HERE / "atoms.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n",
                                     encoding="utf-8")
    (HERE / "atom_similarity.json").write_text(json.dumps(sim, ensure_ascii=False, indent=1) + "\n",
                                               encoding="utf-8")
    over = [k for k, v in sim.items() if v["max"] > 0.9]
    print(f"rows: {len(out)}; atoms: {len(sim)}; max>0.9: {len(over)}")
    for k, v in sim.items():
        flag = "*" if v["max"] > 0.9 else " "
        page = PAGE.get(v[f'{max(("raw","core","dice"), key=lambda m: v[m])}_item'], "-")
        print(f'{flag}{k:28} max {v["max"]:.3f} raw {v["raw"]:.3f}/{v["raw_item"]:8} '
              f'core {v["core"]:.3f}/{v["core_item"]:8} dice {v["dice"]:.3f}/{v["dice_item"]:8} '
              f'с.{page}: {v["text"][:70]}')


if __name__ == "__main__":
    main()
