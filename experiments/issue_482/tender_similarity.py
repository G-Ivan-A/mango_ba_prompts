#!/usr/bin/env python3
"""Правило >90%: сходство строк ТЗ BCREQ-1140 (issue #482) с пунктами «Шаблона ТЗ для тендеров v4».

Метрики и индекс шаблона — как в RUN-0070…RUN-0077 (`experiments/issue_367`, `issue_371`, `issue_382`):
raw (difflib по полному тексту), core (difflib после снятия модальных зачинов), dice
(коэффициент Дайса по 5-символьным основам слов). Шаблон v4 тот же (SHA-256 612e5e09…),
индекс п/п — `experiments/issue_367/tender_index.json`; ненумерованный раздел с.5
«2. Общие требования к оказанию услуг Исполнителем» добавлен абзацами как `p5:N`.

Сравнивается текст после принятия правок рецензирования (`accepted`); полностью
удалённые строки (accepted пуст) не сравниваются.

    python3 -I experiments/issue_482/tender_similarity.py
"""
import difflib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
P5 = (
    "Работоспособность сервиса осуществляется 24 часа в сутки, ежедневно, без перерывов, за исключением "
    "проведения необходимых ремонтных и профилактических работ.",
    "Квартальная доступность Услуг должна быть не менее 99,9%.",
    "Технологические перерывы при оказании Услуг в объеме не более 4 (четырех) часов в месяц, "
    "не включаются в показатели доступности Услуг.",
    "Записи о программном обеспечении поставщика («Виртуальная АТС», «Центр обработки вызовов», «Голосовой "
    "робот»), применяемого для предоставления сервисов в рамках настоящего технического задания, должны быть "
    "включены в реестр российского программного обеспечения.",
)
# Текст пункта индекса заканчивается колонкой «наличие»; в ряде пунктов индекс склеил следующий
# подпункт (2.14.8 -> 2.14.8.1, 2.14.8.2) или заголовок раздела («… наличие 3. Требования к
# отчетности»). Режем по «наличие», за которым идёт конец текста или номер, — слово «наличие»
# внутри формулировки (2.18.21 «наличие и количество перебиваний», 10.1.3) не обрезается.
END = re.compile(r"\s+наличие(?=\s*$|\s+\d+(?:\.\d+)*\.?\s)")
HEAD = re.compile(r"^(\d+(?:\.\d+)*)\.?\s+(.+)$", re.S)


def tender_items(index):
    out = []
    for n, (_page, text) in index.items():
        for k, part in enumerate(END.split(text)):
            part = part.strip()
            if not part:
                continue
            m = HEAD.match(part) if k else None
            out.append((m.group(1), m.group(2).strip()) if m else (n, part))
    return out


TENDER_INDEX = json.loads((HERE.parent / "issue_367/tender_index.json").read_text(encoding="utf-8"))
items = [(f"p5:{i}", t) for i, t in enumerate(P5, start=1)] + tender_items(TENDER_INDEX)
ITEM = dict(items)
# маркер списка U+F0B7 шаблона — оформление, не текст
low = lambda s: re.sub(r"\s+", " ", s.replace("<br>", " ").replace("\uf0b7", " ")).lower().strip(" .;:")
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
for rid, num, _vis, _page, acc, _value, _doc in json.loads((HERE / "source_transcription.json").read_text(encoding="utf-8"))["rows"]:
    if not acc:
        continue
    num = re.sub(r"~~.*?~~", "", num).strip()
    r, n = max((difflib.SequenceMatcher(None, low(acc), low(t[:len(acc) + 40])).ratio(), n) for n, t in items)
    c, cn = max((difflib.SequenceMatcher(None, core(acc), core(t)).ratio(), n) for n, t in items)
    d, dn = max((dice(acc, t), n) for n, t in items)
    # пункт шаблона с тем же номером (если есть): при равном сходстве ссылаемся на него
    same = num.rstrip(".")
    if same in ITEM:
        sr = difflib.SequenceMatcher(None, low(acc), low(ITEM[same])).ratio()
        sd = dice(acc, ITEM[same])
        if max(sr, sd) >= max(r, c, d) - 1e-9 or max(sr, sd) > 0.9:
            r, n, c, cn, d, dn = sr, same, difflib.SequenceMatcher(None, core(acc), core(ITEM[same])).ratio(), same, sd, same
    best[rid] = (round(r, 3), n, round(c, 3), cn, round(d, 3), dn)
    print(f"{rid} {num:10} raw {r:.3f} п/п {n:10} core {c:.3f} п/п {cn:10} dice {d:.3f} п/п {dn:10}: {low(acc)[:60]}")
over = {k: v for k, v in best.items() if max(v[0], v[2], v[4]) > 0.9}
print("items:", len(items), "rows:", len(best), "max>0.9:", len(over))
(HERE / "tender_similarity.json").write_text(json.dumps(best, ensure_ascii=False, indent=0) + "\n", encoding="utf-8")
