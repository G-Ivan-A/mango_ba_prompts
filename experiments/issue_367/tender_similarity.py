#!/usr/bin/env python3
"""Правило >90%: сходство каждой строки ТЗ BCREQ-1115 с пунктами «Шаблона ТЗ для тендеров v4» (difflib).

raw  — сравнение полного текста (как в RUN-0069);
core — сравнение после снятия модальных зачинов («Система должна иметь возможность», «Возможность»,
       «должен/должны иметь возможность» и т.п.), т.е. по предметной части требования.
dice — коэффициент Дайса по множествам 5-символьных основ слов (порядок слов не важен).
Пункт шаблона очищается от значения колонки «Требуемое значение» («наличие»).
"""
import difflib, json, re, sys
from pathlib import Path
import pymupdf
pdf = sys.argv[1] if len(sys.argv) > 1 else "/tmp/i367/tender.pdf"
raw = "\n".join(p.get_text() for p in pymupdf.open(pdf))
parts = re.split(r"\n\s*(\d+(?:\.\d+)+)\.?\s*\n", "\n" + raw)
clean = lambda t: re.sub(r"\s+наличие\b.*$", "", re.sub(r"\s+", " ", t).strip())
items = [(parts[i], clean(parts[i + 1])) for i in range(1, len(parts) - 1, 2)]
low = lambda s: re.sub(r"\s+", " ", s.replace("<br>", " ")).lower().strip(" .;:")
LEAD = re.compile(r"^(в )?(систем[аеы]|платформ[аеы]|приложени[ея])?\s*(должн[аоы]?|должен)?\s*"
                  r"(иметь|предоставлять|позволять|обеспечивать)?\s*(возможность|возможности)?\s*"
                  r"(использования|использовать|осуществлять|для)?\s*", re.I)
core = lambda s: LEAD.sub("", low(s)).strip()
STOP = {"возмо", "должн", "долже", "систе", "иметь", "предо", "обесп", "позво", "налич"}
stems = lambda s: {w[:5] for w in re.findall(r"[а-яёa-z0-9]+", low(s)) if len(w) > 2} - STOP
def dice(a, b):
    a, b = stems(a), stems(b)
    return 2 * len(a & b) / (len(a) + len(b)) if a and b else 0.0
rows = json.loads(Path(__file__).with_name("source_transcription.json").read_text())["rows"]
best = {}
for rid, num, req, _ in rows:
    r, n, t = max((difflib.SequenceMatcher(None, low(req), low(t[:len(req) + 40])).ratio(), n, t) for n, t in items)
    c, cn, ct = max((difflib.SequenceMatcher(None, core(req), core(t)).ratio(), n, t) for n, t in items)
    d, dn, dt = max((dice(req, t), n, t) for n, t in items)
    best[rid] = (round(r, 3), n, round(c, 3), cn, round(d, 3), dn)
    print(f"{rid} {num:4} raw {r:.3f} п/п {n:10} core {c:.3f} п/п {cn:10} dice {d:.3f} п/п {dn:10}: {dt[:80]}")
print("items:", len(items), "raw>0.9:", [k for k, v in best.items() if v[0] > 0.9],
      "core>0.9:", [(k, v[3]) for k, v in best.items() if v[2] > 0.9],
      "dice>0.9:", [(k, v[5]) for k, v in best.items() if v[4] > 0.9])
Path(__file__).with_name("tender_similarity.json").write_text(json.dumps(best, ensure_ascii=False, indent=0) + "\n")
