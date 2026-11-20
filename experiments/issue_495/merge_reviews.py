#!/usr/bin/env python3
"""Сводка раундов двухролевой проверки (issue #495, дополнение 1).

Каждый раунд роли — отдельный файл ``review/role-<a|b>.r<N>.md`` с таблицей
``| ID | Вердикт | Основание |``. Запись с вердиктом «не принято» возвращается
на шаг 1 (исправление) и проверяется в следующем раунде заново. Сводка берёт по
каждой записи вердикт последнего раунда, в котором роль её проверяла, и пишет:

- ``review/role-a.md``, ``review/role-b.md`` — итоговые вердикты с номером раунда;
- ``review/iterations.json`` — число раундов по записи (максимум по двум ролям).

    python3 experiments/issue_495/merge_reviews.py [--check]

Скрипт не вызывает LLM и ничего не меняет вне ``review/``.
"""
import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REVIEW = HERE / "review"
ROW = re.compile(r"^\|\s*\**([UDAMG]-\d+b?)\**\s*\|\s*([^|]+?)\s*\|\s*(.+?)\s*\|\s*$")
TITLES = {"a": "Роль А — инженер ИИ-промптов", "b": "Роль Б — ИИ-архитектор контрактов и данных"}


def rounds(role):
    files = sorted(REVIEW.glob(f"role-{role}.r*.md"), key=lambda p: int(re.search(r"\.r(\d+)\.md$", p.name)[1]))
    out = []
    for path in files:
        text = path.read_text(encoding="utf-8")
        model = re.search(r"[Мм]одель:?\s*\**\s*([^;\n]+)", text)
        rows = {}
        for line in text.splitlines():
            m = ROW.match(line)
            if m and not set(m[2]) <= set("-: ") and not m[2].lower().startswith("вердикт"):
                rows[m[1]] = (m[2].strip("* ").lower(), m[3])
        out.append((int(re.search(r"\.r(\d+)\.md$", path.name)[1]), path.name,
                    model[1].strip(" *`.") if model else "не указана", rows))
    return out


def merge(role):
    data = rounds(role)
    final, seen = {}, {}
    for no, name, _model, rows in data:
        for gid, (verdict, basis) in rows.items():
            final[gid] = (verdict, basis, no)
            seen.setdefault(gid, []).append(no)
    models = "; ".join(f"раунд {no} — {model} (`{name}`)" for no, name, model, _ in data)
    lines = [f"# {TITLES[role]}: итог по раундам", "",
             f"Модель: {models}; сессия: сводка раундов {', '.join(str(no) for no, *_ in data)}", "",
             "Вердикт — последнего раунда, в котором роль проверяла запись. «Не принято» "
             "возвращает запись на исправление и следующий раунд.", "",
             "| ID | Вердикт | Основание (раунд; история вердиктов) |", "| --- | --- | --- |"]
    for gid in sorted(final, key=order):
        verdict, basis, no = final[gid]
        history = " → ".join(next(r[3][gid][0] for r in data if r[0] == n) for n in seen[gid])
        lines.append(f"| {gid} | {verdict} | раунд {no} ({history}): {basis} |")
    return "\n".join(lines) + "\n", seen


def order(gid):
    kind, num = gid.split("-")
    return ("UDAMG".index(kind), int(num.rstrip("b")), num.endswith("b"))


def build():
    texts, iterations = {}, {}
    for role in "ab":
        text, seen = merge(role)
        texts[REVIEW / f"role-{role}.md"] = text
        for gid, nos in seen.items():
            iterations[gid] = max(iterations.get(gid, 0), len(nos))
    texts[REVIEW / "iterations.json"] = json.dumps(dict(sorted(iterations.items(), key=lambda kv: order(kv[0]))),
                                                   ensure_ascii=False, indent=1) + "\n"
    return texts


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    texts = build()
    stale = [p.name for p, t in texts.items() if not p.exists() or p.read_text(encoding="utf-8") != t]
    if args.check:
        print("OK: сводка актуальна" if not stale else f"ERROR: устарело {stale}")
        return 1 if stale else 0
    for path, text in texts.items():
        path.write_text(text, encoding="utf-8")
    print("записано:", ", ".join(p.name for p in texts))
    return 0


if __name__ == "__main__":
    sys.exit(main())
