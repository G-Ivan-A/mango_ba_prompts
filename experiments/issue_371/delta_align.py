#!/usr/bin/env python3
"""Отчёт 2 (issue #371): выравнивание строк ТЗ 2026 с абзацами ТЗ 2025 — доказательная база дельты.

ТЗ 2025 («Телефония ТЗ 2307 2025 года в анализ.pdf») не оценивается, а только сравнивается.
Тело (с. 1–6, разделы 1–4) режется на абзацы по номеру пункта («2.6.», «3.11.»), маркеру «-» и
глифу SymbolMT U+F02D; Приложение 1 (с. 7–9, таблица) — на строки, перенос «-» внутри
слова и висячие строки склеиваются со следующей. Для каждой строки ТЗ 2026 ищется лучший
абзац ТЗ 2025 (difflib ratio по нормализованному тексту). Классы:
- `same`    — ratio ≥ 0,95: формулировка не изменилась (игнорируется в Отчёте 2);
- `changed` — 0,55 ≤ ratio < 0,95: есть правка — разбирается вручную в `delta.json`;
- `new`     — ratio < 0,55: пункта в ТЗ 2025 нет.
Обратный проход печатает абзацы ТЗ 2025 без пары в ТЗ 2026 (ratio < 0,55) — кандидаты в «исключено».
Пороги эмпирические; финальное решение «влияет / не влияет на оценку» принимается вручную
(`delta.json`), скрипт лишь гарантирует, что ни одна правка не пропущена.

    python3 -I experiments/issue_371/delta_align.py /path/to/tz2025.pdf
"""
from __future__ import annotations

import difflib
import hashlib
import json
import re
import sys
from pathlib import Path

import pymupdf

HERE = Path(__file__).resolve().parent
NUMBER = re.compile(r"^\d+\.(?:\d+\.?)?(?:\s|$)")


def paragraphs(pdf: Path) -> list[tuple[str, str]]:
    body, appendix = [], []
    for pno, page in enumerate(pymupdf.open(pdf), start=1):
        for raw in page.get_text().split("\n"):
            line = raw.strip()
            if line:
                (body if pno <= 6 else appendix).append(line)
    out: list[list[str]] = []
    for line in body:
        if NUMBER.match(line) or line.startswith("-") or line == "":
            out.append(["b", "" if line == "" else line.lstrip("-").strip()])
        elif out:
            sep = "" if re.search(r"[A-Za-zА-Яа-яЁё]-$", out[-1][1]) or not out[-1][1] else " "
            out[-1][1] += sep + line
    for line in appendix:
        if out and out[-1][0] == "a" and (re.search(r"[-,]$", out[-1][1]) or line[:1].islower()):
            sep = "" if re.search(r"[A-Za-zА-Яа-яЁё]-$", out[-1][1]) else " "
            out[-1][1] += sep + line
        else:
            out.append(["a", line])
    return [(kind, text) for kind, text in out if len(text) > 3]


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).lower().strip(" .;:")


def main() -> None:
    pdf = Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/dl371/tz2025/tz2025.pdf")
    old = paragraphs(pdf)
    rows = json.loads((HERE / "source_transcription.json").read_text(encoding="utf-8"))["rows"]
    ratio = lambda a, b: difflib.SequenceMatcher(None, norm(a), norm(b)).ratio()  # noqa: E731
    result, used = {}, set()
    for rid, num, req, _ in rows:
        text = f"{num} {req}" if NUMBER.match(num + " ") else req
        score, idx = max((ratio(text, t), i) for i, (_k, t) in enumerate(old))
        cls = "same" if score >= 0.95 else "changed" if score >= 0.55 else "new"
        if cls != "new":
            used.add(idx)
        result[rid] = {"class": cls, "ratio": round(score, 3), "tz2025": old[idx][1] if cls != "new" else ""}
        print(f"{rid} {cls:7} {score:.3f} {num:5} {req[:50]!r} <- {old[idx][1][:50]!r}")
    removed = [t for i, (_k, t) in enumerate(old) if i not in used
               and max(ratio(t, (f'{n} {r}' if NUMBER.match(n + ' ') else r)) for _rid, n, r, _ in rows) < 0.55]
    for t in removed:
        print("REMOVED?", repr(t[:110]))
    counts = {c: sum(v["class"] == c for v in result.values()) for c in ("same", "changed", "new")}
    print(counts, "removed candidates:", len(removed))
    out = {"tz2025_sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(), "counts": counts,
           "rows": result, "removed_candidates": removed}
    (HERE / "delta_alignment.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
