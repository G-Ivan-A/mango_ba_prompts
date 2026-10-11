#!/usr/bin/env python3
"""Извлечение основного текста Word 97-2003 (.doc) по таблице фрагментов (piece table, CLX).

Только olefile + стандартная библиотека: поток WordDocument -> FIB (ccpText, fcClx/lcbClx)
-> поток 0Table/1Table -> Pcdt/PlcPcd -> фрагменты текста (cp1251-«compressed» или UTF-16LE).
Возвращает строку длиной ccpText с управляющими символами Word: \\r — конец абзаца,
\\x07 — конец ячейки/строки таблицы, \\x0b — разрыв строки, \\x0c — разрыв страницы,
\\x13\\x14\\x15 — поля.

    python3 experiments/issue_369/doc_text.py <file.doc>  # печатает repr абзацев
"""
from __future__ import annotations

import struct
import sys

import olefile


def doc_text(path: str) -> str:
    ole = olefile.OleFileIO(path)
    wd = ole.openstream("WordDocument").read()
    assert struct.unpack_from("<H", wd, 0)[0] == 0xA5EC, "не Word 97+ (wIdent)"
    flags = struct.unpack_from("<H", wd, 0x0A)[0]
    table = ole.openstream("1Table" if flags & 0x0200 else "0Table").read()
    ccp_text = struct.unpack_from("<i", wd, 0x4C)[0]
    fc_clx, lcb_clx = struct.unpack_from("<II", wd, 0x1A2)
    clx = table[fc_clx:fc_clx + lcb_clx]
    pos = 0
    while clx[pos] == 0x01:  # Prc (grpprl) — пропускаем
        pos += 3 + struct.unpack_from("<H", clx, pos + 1)[0]
    assert clx[pos] == 0x02, "Pcdt не найден"
    lcb = struct.unpack_from("<I", clx, pos + 1)[0]
    plc = clx[pos + 5:pos + 5 + lcb]
    n = (lcb - 4) // 12
    cps = struct.unpack_from(f"<{n + 1}i", plc, 0)
    out = []
    for i in range(n):
        fc = struct.unpack_from("<I", plc, 4 * (n + 1) + 8 * i + 2)[0]
        count = cps[i + 1] - cps[i]
        if fc & 0x40000000:
            start = (fc & ~0x40000000) // 2
            out.append(wd[start:start + count].decode("cp1251"))
        else:
            out.append(wd[fc:fc + 2 * count].decode("utf-16-le"))
    return "".join(out)[:ccp_text]


if __name__ == "__main__":
    text = doc_text(sys.argv[1])
    for i, para in enumerate(text.split("\r")):
        print(i, repr(para))
