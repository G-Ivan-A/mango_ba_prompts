#!/usr/bin/env python3
"""Декомпозиция строк исходника BCREQ-1199 v2 на строки результирующего отчёта (issue #486).

Правила формы отчёта (issue #486):

- строка исходника с заголовком остаётся отдельной строкой «как есть» (`heading`);
- строка исходника с несколькими требованиями раскладывается на фрагменты — отдельные
  строки отчёта со сквозным «№ пп»; значение колонки «№» исходника переносится в каждую;
- обобщающая вводная фраза составного требования — всегда отдельная строка: оценивается,
  если однозначно трактуется как требование верхнего уровня (`req`), иначе фиксируется как
  заголовок комплексного требования (`lead`, не оценивается);
- каждое атомарное требование — отдельная строка (`req`) с собственной оценкой.

Фрагмент — дословная подстрока ячейки (колонки «Требования»; на листе SLA — «Требования»
и «Максимальный срок решения заявки» через перевод строки) без пробелов по краям. Фрагменты
строки идут в порядке текста и покрывают ячейку целиком с точностью до пробельных символов —
это проверяет `check()` здесь и валидатор `scripts/validate_issue_486_run.py`.

Единица разбиения:

- перечень через перевод строки и маркер `-` — каждый пункт перечня (маркер сохраняется),
  текст до первого пункта — вводная фраза;
- сплошной текст — предложения или абзацы с самостоятельным требованием (`SPLIT`);
  определения и пояснения остаются с требованием, к которому относятся;
- Таблица 1 листа SLA — каждая непустая строка ячейки (подпись приоритета — `lead`).

    python3 -I experiments/issue_486/decompose.py

Результат — `fragments.json`: [{fid, rid, sheet, row, num, kind, text, group, sim}], где
`group` — для `heading`/`lead` список fid оцениваемых строк, к которым относится заголовок;
`sim` — сходство фрагмента с пунктами шаблона ТЗ-тендеров-v4 (метрики RUN-0070…RUN-0094).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "issue_484/source_transcription.json"
sys.path.insert(0, str(HERE.parent / "issue_484"))
from atomize import best  # noqa: E402

SHEETS = ("Требования к системе", "SLA")
# Строки исходника без требования — шапка таблицы, название раздела, подписи Таблицы 1 SLA.
HEADINGS = ("Требования к системе!1", "SLA!1", "SLA!17", "SLA!18")
# Сплошной текст с несколькими требованиями: фрагмент начинается с каждого указанного начала.
SPLIT = {
    "Требования к системе!2": ["Сотрудники ВымпелКом работают"],
    "Требования к системе!7": ["Не менее 3-х подтвержденных"],
    "Требования к системе!12": ["Предоставление номеров \"под ключ\"", "Ориентировочный объем",
                                "Также требуется подключить", "(подтверждается лицензией",
                                "Постоянный мониторинг"],
    "Требования к системе!13": ["проведение обучения", "(подтверждается примером"],
    "SLA!2": ["Расчет времени доступности", "Доступность полной функциональности -"],
    "SLA!6": ["Плановые технологические перерывы"],
    "SLA!8": ["Перед релизами"],
    "SLA!11": ["Работникам ВымпелКом направляются", "Поддержка оказывается",
               "За нарушение сроков"],
    "SLA!12": ["Коммуникация с аккаунт-менеджером"],
    "SLA!14": ["При возникновении спорных"],
    "SLA!15": ["Состав отчета:", "В случае выявления"],
}
# Строки Таблицы 1 листа SLA: каждая непустая строка ячейки — отдельный фрагмент.
TABLE = tuple(f"SLA!{n}" for n in range(19, 27))
# Вводные фразы, которые не являются самостоятельным требованием, — заголовок комплексного
# требования (не оцениваются). Остальные вводные фразы оцениваются как требование верхнего
# уровня. Ключ — fid.
LEADS = {
    "Требования к системе!4.1": "условие «подтверждается на презентации» — организация показа, "
                                "сам функционал перечислен в пунктах",
    "Требования к системе!8.1": "этап внедрения и перечень интеграционных работ, сам функционал "
                                "перечислен в пунктах",
    "Требования к системе!9.1": "этап внедрения и перечень настроек и доработок, сам функционал "
                                "перечислен в пунктах",
    "Требования к системе!14.1": "перечень функций админ. панели, сам функционал перечислен в "
                                 "пунктах",
    "SLA!19.1": "подпись приоритета заявки Таблицы 1",
    "SLA!21.1": "подпись приоритета заявки Таблицы 1",
    "SLA!23.1": "подпись приоритета заявки Таблицы 1",
    "SLA!25.1": "подпись типа заявки Таблицы 1",
}
BULLET = re.compile(r"^[-–—•]\s*")
squash = lambda s: re.sub(r"\s+", "", s)


def cell(sheet: str, values: list[str]) -> str:
    """Колонка «Требование» отчёта RUN-0094: «Требования» (+ сроки на листе SLA)."""
    text = values[1] if len(values) > 1 else ""
    tail = values[2] if sheet == "SLA" and len(values) > 2 else ""
    return "\n".join(t for t in (text, tail) if t)


def pieces(rid: str, text: str) -> list[str]:
    """Дословные фрагменты ячейки в порядке текста."""
    if rid in HEADINGS:
        return [text.strip()]
    if rid in TABLE:
        return [line.strip() for line in text.split("\n") if line.strip()]
    if rid in SPLIT:
        cuts = [0]
        for start in SPLIT[rid]:
            pos = text.find(start)
            assert pos > cuts[-1], (rid, start)
            cuts.append(pos)
        return [text[a:b].strip() for a, b in zip(cuts, cuts[1:] + [len(text)])]
    lines = text.split("\n")
    if not any(BULLET.match(line.strip()) for line in lines[1:]):
        return [text.strip()]
    out, buf = [], []
    for line in lines:
        if BULLET.match(line.strip()):
            if buf and "\n".join(buf).strip():
                out.append("\n".join(buf).strip())
            buf = []
            out.append(line.strip())
        else:
            buf.append(line)
    assert not "\n".join(buf).strip(), rid
    return out


def kind_of(rid: str, fid: str, k: int, n: int, text: str) -> str:
    if rid in HEADINGS:
        return "heading"
    if fid in LEADS:
        return "lead"
    return "req"


def continuation(values: list[str]) -> bool:
    """Строка Таблицы 1 с объединённой ячейкой «Тип Заявки» — продолжение предыдущей."""
    return not values[0] and not (values[1] if len(values) > 1 else "")


def build() -> list[dict]:
    src = json.loads(SRC.read_text(encoding="utf-8"))
    out: list[dict] = []
    for sheet in src["sheets"]:
        if sheet["title"] not in SHEETS:
            continue
        for row in sheet["rows"]:
            ri, values = row[0], row[1:]
            if not any(values):
                continue
            rid = f'{sheet["title"]}!{ri}'
            text = cell(sheet["title"], values)
            parts = pieces(rid, text)
            assert squash("".join(parts)) == squash(text), rid
            for k, part in enumerate(parts, start=1):
                fid = f"{rid}.{k}"
                kind = kind_of(rid, fid, k, len(parts), part)
                frag = {"fid": fid, "rid": rid, "sheet": sheet["title"], "row": ri,
                        "num": values[0], "kind": kind, "text": part, "cont": continuation(values)}
                if kind == "req":
                    frag["sim"] = best(BULLET.sub("", part))
                out.append(frag)
    # Состав заголовка: строки той же строки исходника и строк-продолжений Таблицы 1 SLA
    # (для шапки/раздела — все строки до следующего заголовка того же уровня не нужны:
    # шапка и раздел описывают лист целиком).
    for i, frag in enumerate(out):
        if frag["kind"] == "lead":
            group = []
            for nxt in out[i + 1:]:
                if nxt["rid"] != frag["rid"] and not nxt["cont"]:
                    break
                assert nxt["kind"] == "req", nxt["fid"]
                group.append(nxt["fid"])
            frag["group"] = group
            frag["reason"] = LEADS[frag["fid"]]
    for frag in out:
        del frag["cont"]
    return out


def check(frags: list[dict]) -> None:
    fids = [f["fid"] for f in frags]
    assert len(set(fids)) == len(fids)
    assert set(LEADS) <= set(fids), set(LEADS) - set(fids)


if __name__ == "__main__":
    frags = build()
    check(frags)
    (HERE / "fragments.json").write_text(json.dumps(frags, ensure_ascii=False, indent=1) + "\n",
                                         encoding="utf-8")
    by = {}
    for f in frags:
        by.setdefault((f["sheet"], f["kind"]), 0)
        by[(f["sheet"], f["kind"])] += 1
    print(f"fragments: {len(frags)}", by)
    for f in frags:
        if f["kind"] == "req" and f["sim"]["max"] > 0.9:
            s = f["sim"]
            print(f"  >0.9 {f['fid']}: {s['max']} raw {s['raw_item']} core {s['core_item']} "
                  f"dice {s['dice_item']} — {f['text'][:70]}")
