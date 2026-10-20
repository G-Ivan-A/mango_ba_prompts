#!/usr/bin/env python3
"""Независимая сверка колонок 1-2 и оценки исходника с CSV-файлами BCREQ-1125 (issue #382).

Без модуля csv: байты файла декодируются из Windows-1251 и разбираются собственным
автоматом (поле в кавычках может содержать «;» и перевод строки, `""` — экранированная
кавычка). Каждая строка `source_transcription.json` обязана совпасть с очередной записью
файла: КЦ — `№`, `Группа<br>Конкретное требование`, `Оценка Внутр`; ФТ — пустой №,
`Требование`, `Комментарий поставщика`; перевод строки внутри ячейки = `<br>`.
Дополнительно проверяются SHA-256 и отсутствие непокрытых записей.

    python3 -I experiments/issue_382/check_source.py <f1.csv> <f2.csv> <f3.csv> <f4.csv> <f5.csv>
"""
import hashlib
import json
import sys
from pathlib import Path


def records(text: str) -> list[list[str]]:
    out, rec, field, quoted, i = [], [], [], False, 0
    while i < len(text):
        ch = text[i]
        if quoted:
            if ch == '"' and text[i + 1:i + 2] == '"':
                field.append('"')
                i += 1
            elif ch == '"':
                quoted = False
            else:
                field.append(ch)
        elif ch == '"' and not field:
            quoted = True
        elif ch == ";":
            rec.append("".join(field))
            field = []
        elif ch == "\r" and text[i + 1:i + 2] == "\n":
            pass
        elif ch == "\n":
            rec.append("".join(field))
            out.append(rec)
            rec, field = [], []
        else:
            field.append(ch)
        i += 1
    if field or rec:
        rec.append("".join(field))
        out.append(rec)
    return out


def br(value: str) -> str:
    return value.replace("\r\n", "\n").replace("\n", "<br>")


data = json.loads(Path(__file__).with_name("source_transcription.json").read_text(encoding="utf-8"))
bad = total = 0
for block, path in zip(data["blocks"], sys.argv[1:]):
    raw = Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest() != block["sha256"]:
        bad += 1
        print("SHA256 MISMATCH", block["title"])
    body = records(raw.decode(block["encoding"]))[1:]
    if len(body) != len(block["rows"]):
        bad += 1
        print(f"{block['key']}: записей в файле {len(body)}, в транскрипции {len(block['rows'])}")
    for rec, (rid, num, req, own, _line) in zip(body, block["rows"]):
        total += 1
        if block["kind"] == "КЦ":
            want = (rec[0], br(rec[1]) + "<br>" + br(rec[2]), br(rec[3]))
        else:
            want = ("", br(rec[0]), br(rec[1]))
        if (num, req, own) != want:
            bad += 1
            print("MISMATCH", rid, repr((num, req, own)), "!=", repr(want))
print(f"files: {len(data['blocks'])}; rows checked: {total}; mismatches: {bad}")
sys.exit(1 if bad or len(sys.argv) - 1 != len(data["blocks"]) else 0)
