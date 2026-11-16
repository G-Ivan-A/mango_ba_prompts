#!/usr/bin/env python3
"""Нарезка оцениваемых фрагментов (`fragments.json`) на батчи исследования (issue #486).

Для каждого батча пишется `research/<BATCH>_rows.txt`: блок на фрагмент — fid, номер пункта
исходника, вид (`req`; вводная фраза, оцениваемая как требование верхнего уровня, помечена
`top`), дословный текст фрагмента, подсказка о ближайшем пункте шаблона ТЗ-тендеров-v4 (при
сходстве > 0,6) и — один раз на строку исходника — карточка RUN-0094 v1.0 (issue #484) этой
строки как исходный материал: её ссылки и цитаты уже сверены `verify_quotes.py` и
переиспользуются для фрагментов.

    python3 -I experiments/issue_486/make_batches.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "issue_484"))
import ssot  # noqa: E402

T = "Требования к системе!"
BATCHES: dict[str, list[str]] = {
    "A_general_dialing": [T + n for n in ("2", "3", "4", "7", "12", "13")],
    "B_admin_skillaz": [T + n for n in ("5", "6", "8")],
    "C_routing_reports": [T + n for n in ("9", "10", "11", "14", "19")],
    "D_quality_speech": [T + n for n in ("15", "16")],
    "E_robots_wfm": [T + n for n in ("17", "18")],
    "F_sla": [f"SLA!{n}" for n in range(2, 27)],
}


def main() -> None:
    frags = json.loads((HERE / "fragments.json").read_text(encoding="utf-8"))
    prior = ssot.research()
    rows = {f["rid"] for f in frags if f["kind"] == "req"}
    covered = {rid for rids in BATCHES.values() for rid in rids}
    assert rows <= covered, rows - covered
    total = 0
    for batch, rids in BATCHES.items():
        out = [f"# Батч {batch} (issue #486): оценка атомарных фрагментов\n"]
        for rid in rids:
            mine = [f for f in frags if f["rid"] == rid]
            if not any(f["kind"] == "req" for f in mine):
                continue
            out.append(f"## Строка исходника {rid} (№ {mine[0]['num'] or '—'})\n")
            for f in mine:
                if f["kind"] != "req":
                    out.append(f"- {f['fid']} — НЕ ОЦЕНИВАТЬ ({f['kind']}): {f['text']}")
                    continue
                total += 1
                top = " top" if len([g for g in mine if g['kind'] == 'req']) > 1 and \
                    f["fid"].endswith(".1") and f["text"].rstrip().endswith(":") else ""
                s = f["sim"]
                hint = (f" | v4: п/п {s['raw_item'] if s['raw'] == s['max'] else s['core_item'] if s['core'] == s['max'] else s['dice_item']} ({s['max']})"
                        if s["max"] > 0.6 else "")
                out.append(f"### {f['fid']} [req{top}]{hint}\n{f['text']}\n")
            card = prior.get(rid)
            if card:
                card = {k: card[k] for k in ("verdict", "why", "refs", "quotes", "audit")}
                out.append("Карточка RUN-0094 v1.0 этой строки (материал, не ответ):\n```json\n"
                           + json.dumps(card, ensure_ascii=False, indent=1) + "\n```\n")
        (HERE / "research" / f"{batch}_rows.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"batches: {len(BATCHES)}; fragments to assess: {total}")


if __name__ == "__main__":
    main()
