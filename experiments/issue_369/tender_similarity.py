#!/usr/bin/env python3
"""Правило >90%: сходство строк ТЗ BCREQ-1116 (оба блока) с пунктами «Шаблона ТЗ для тендеров v4».

Метрики и пункты шаблона — как в RUN-0070 (`experiments/issue_367/tender_similarity.py`):
raw (difflib по полному тексту), core (difflib после снятия модальных зачинов), dice
(коэффициент Дайса по 5-символьным основам слов). Строка таблицы сравнивается по тексту ячеек
через пробел. Шаблон v4 тот же (SHA-256 612e5e09…), индекс — `experiments/issue_367/tender_index.json`.
"""
import difflib, json, re, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
items = []
for n, (_page, text) in json.loads((HERE.parent / "issue_367/tender_index.json").read_text(encoding="utf-8")).items():
    t = re.sub(r"\s+наличие\b.*$", "", text, flags=re.S).strip()
    if t:
        items.append((n, t))
low = lambda s: re.sub(r"\s+", " ", s.replace("<br>", " ").replace("<sup>1</sup>", "")).lower().strip(" .;:")
LEAD = re.compile(r"^(в )?(систем[аеы]|платформ[аеы]|приложени[ея])?\s*(должн[аоы]?|должен)?\s*"
                  r"(иметь|предоставлять|позволять|обеспечивать)?\s*(возможность|возможности)?\s*"
                  r"(использования|использовать|осуществлять|для)?\s*", re.I)
core = lambda s: LEAD.sub("", low(s)).strip()
STOP = {"возмо", "должн", "долже", "систе", "иметь", "предо", "обесп", "позво", "налич"}
stems = lambda s: {w[:5] for w in re.findall(r"[а-яёa-z0-9]+", low(s)) if len(w) > 2} - STOP
def dice(a, b):
    a, b = stems(a), stems(b)
    return 2 * len(a & b) / (len(a) + len(b)) if a and b else 0.0
best = {}
for blk in json.loads((HERE / "source_transcription.json").read_text(encoding="utf-8"))["blocks"]:
    for rid, num, req, _ in blk["rows"]:
        r, n = max((difflib.SequenceMatcher(None, low(req), low(t[:len(req) + 40])).ratio(), n) for n, t in items)
        c, cn = max((difflib.SequenceMatcher(None, core(req), core(t)).ratio(), n) for n, t in items)
        d, dn = max((dice(req, t), n) for n, t in items)
        best[rid] = (round(r, 3), n, round(c, 3), cn, round(d, 3), dn)
        print(f"{rid} raw {r:.3f} п/п {n:10} core {c:.3f} п/п {cn:10} dice {d:.3f} п/п {dn:10}: {low(req)[:60]}")
print("items:", len(items), "raw>0.9:", [(k, v[1]) for k, v in best.items() if v[0] > 0.9],
      "core>0.9:", [(k, v[3]) for k, v in best.items() if v[2] > 0.9],
      "dice>0.9:", [(k, v[5]) for k, v in best.items() if v[4] > 0.9])
(HERE / "tender_similarity.json").write_text(json.dumps(best, ensure_ascii=False, indent=0) + "\n", encoding="utf-8")
