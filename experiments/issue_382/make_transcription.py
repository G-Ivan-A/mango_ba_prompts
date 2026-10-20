#!/usr/bin/env python3
"""Транскрипция пяти CSV-исходников BCREQ-1125 (issue #382) -> source_transcription.json.

Исходники — выгрузки листов Excel в CSV (разделитель «;», кодировка Windows-1251, CRLF).
Файлы читаются модулем csv; строка-шапка (названия колонок) требованием не является.

КЦ-файлы (колонки «№;Группа;Конкретное требование;Оценка Внутр»):
  колонка 1 = «№»; колонка 2 = «Группа» и «Конкретное требование», сцепленные через `<br>`
  (условие issue #382 для файлов «КЦ»); оценка исходника = «Оценка Внутр».
ФТ-файлы (колонки «Требование;Комментарий поставщика (…)»):
  номера требований нет — колонка 1 пустая; колонка 2 = «Требование»; оценка исходника =
  «Комментарий поставщика».
Переносы строк внутри ячейки -> `<br>`; остальной текст (опечатки, пробелы, в т.ч. хвостовые)
не меняется.

Строка JSON: [rid, №, требование, оценка исходника, номер строки CSV].

    python3 experiments/issue_382/make_transcription.py <f1.csv> <f2.csv> <f3.csv> <f4.csv> <f5.csv>
"""
import csv
import hashlib
import io
import json
import sys
from pathlib import Path

ENCODING = "cp1251"
# Порядок и имена файлов — как в issue #382 (раздел «Исходники ТЗ»).
BLOCKS = (
    ("KC1", "КЦ", "КЦ Требования к коннектору.csv", "https://github.com/user-attachments/files/33717835/default.csv"),
    ("KC2", "КЦ", "КЦ Требования КЦ.csv", "https://github.com/user-attachments/files/33717836/default.csv"),
    ("FT1", "ФТ", "ФТ - Расшифровка отчетность.csv", "https://github.com/user-attachments/files/33717837/-.csv"),
    ("FT2", "ФТ", "ФТ - Расшифровки оценка звонков.csv", "https://github.com/user-attachments/files/33717838/-.csv"),
    ("FT3", "ФТ", "ФТ - Функциональные критерии.csv", "https://github.com/user-attachments/files/33717839/-.csv"),
)


def cell(value: str) -> str:
    return value.replace("\r\n", "\n").replace("\n", "<br>")


def transcribe(key: str, kind: str, raw: bytes) -> tuple[list[str], list[list]]:
    records = list(csv.reader(io.StringIO(raw.decode(ENCODING), newline=""), delimiter=";"))
    header, body = records[0], records[1:]
    rows = []
    for line, rec in enumerate(body, start=2):
        if kind == "КЦ":
            assert len(rec) == 4, (key, line, rec)
            num, group, req, own = rec
            rows.append([f"{key}-{len(rows) + 1:03d}", num, f"{cell(group)}<br>{cell(req)}", cell(own), line])
        else:
            assert len(rec) == 2, (key, line, rec)
            req, own = rec
            rows.append([f"{key}-{len(rows) + 1:03d}", "", cell(req), cell(own), line])
    return header, rows


def main(paths: list[str]) -> None:
    assert len(paths) == len(BLOCKS), "нужно 5 файлов в порядке issue #382"
    blocks = []
    for (key, kind, title, url), path in zip(BLOCKS, paths):
        raw = Path(path).read_bytes()
        header, rows = transcribe(key, kind, raw)
        blocks.append({
            "key": key, "kind": kind, "title": title, "url": url, "encoding": ENCODING,
            "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw),
            "header": header, "rows": rows,
        })
        print(f"{key} {title}: {len(rows)} rows, sha256 {blocks[-1]['sha256']}")
    out = Path(__file__).with_name("source_transcription.json")
    out.write_text(json.dumps({"blocks": blocks}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main(sys.argv[1:])
