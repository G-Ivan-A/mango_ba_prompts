#!/usr/bin/env python3
"""Таблица протокола двух ролей по 100 % реестра (issue #495, дополнение 1).

Склеивает реестр (``rewrite_cases.py``, группы ``map_baseline.py``), число
нарушений базы по группе (``audit/baseline-map.json``) и вердикты рецензентов
(``review/role-a.md``, ``review/role-b.md`` — таблицы ``| ID | Вердикт | Основание |``
с заголовком «Модель: …; сессия: …»). Запись без вердикта любой роли — дефект
протокола: скрипт печатает её и выходит с кодом 1.

    python3 experiments/issue_495/protocol_table.py [--basis 110] [--out protocol.md]

Скрипт ничего не меняет в репозитории и не вызывает LLM.
"""
import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1] / "scripts"))
import map_baseline as mb  # noqa: E402

REVIEW = HERE / "review"
ROW = re.compile(r"^\|\s*\**([UDAMG]-\d+b?)\**\s*\|\s*([^|]+?)\s*\|\s*(.+?)\s*\|\s*$")
#: Итерации проверки по записи (запись → число раундов). Раунд 1 — у всех.
ITERATIONS = json.loads((REVIEW / "iterations.json").read_text(encoding="utf-8")) \
    if (REVIEW / "iterations.json").exists() else {}

# Сторожа (легенда — в описании PR); все работают под test_repo_has_zero_findings.
GUARDS = {
    "а": "С-а", "б": "С-б", "в": "С-в",
}


def guards(gid, cls, files):
    out = [GUARDS[c.strip()] for c in cls.split(",") if c.strip() in GUARDS]
    joined = " ".join(files)
    if "scripts/build_" in joined or "bcreq_handoff" in joined or gid == "G-01":
        out.append("С-сб")
    if gid in ("A-01", "G-02", "G-03") or "generate-pages-data" in joined or "catalog.json" in joined:
        out.append("С-сайт")
    if gid.startswith("M-"):
        out.append("С-пр")
    if "prompt-regressions" in mb.describe(gid)[2] or gid in ("U-01", "U-01b"):
        out.append("С-рт")
    return ", ".join(dict.fromkeys(out)) or "С-0"


def read_role(path):
    text = path.read_text(encoding="utf-8")
    head = next((ln for ln in text.splitlines() if re.search(r"[Мм]одель|[Mm]odel", ln)), "").strip("#> *")
    verdicts = {}
    for line in text.splitlines():
        m = ROW.match(line)
        if m and not set(m[2]) <= set("-: "):
            verdicts[m[1]] = (m[2].strip("* "), m[3])
    return head, verdicts


def short(text, n):
    text = re.sub(r"\s+", " ", text).replace("|", "\\|")
    return text if len(text) <= n else text[: n - 1].rstrip() + "…"


def entries():
    rc = mb.rewrite_cases
    out = [(eid, files, cls) for eid, files, _o, _n, _c, cls, _w in rc.EDITS + rc.REGISTER_ONLY]
    out += [("D-11", ["prompts/archive/*.md"], "в"),
            ("D-12", [rel for rel, _, _ in rc.FRONTMATTER_LINKS], "а")]
    out += [(gid, [], cls) for gid, (cls, _w, _x) in mb.GROUPS.items()]
    return sorted(out, key=lambda e: mb.order(e[0]))


def build(basis):
    counts = {g: len(v) for g, v in json.loads((HERE / "audit/baseline-map.json").read_text(encoding="utf-8"))["groups"].items()}
    head_a, role_a = read_role(REVIEW / "role-a.md")
    head_b, role_b = read_role(REVIEW / "role-b.md")
    missing = []
    rows = ["| ID | Класс | Локатор до | Исправление (локатор после / куда) | Роль А | Роль Б | Сторож | Итер. | Статус |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for gid, files, cls in entries():
        _, what, where = mb.describe(gid)
        before = (", ".join(f"`{f.split(' (')[0]}`" for f in files[:2]) + (" …" if len(files) > 2 else "")) or short(what, 70)
        a, b = role_a.get(gid), role_b.get(gid)
        if not a or not b:
            missing.append(gid)
        ok = a and b and a[0].lower().startswith("принят") and b[0].lower().startswith("принят")
        cell = lambda v: f"**{v[0]}** — {short(v[1], basis)}" if v else "—"
        rows.append(f"| {gid} | {cls} | {before}; нарушений базы {counts.get(gid, 0)} | {short(where, 90)} | "
                    f"{cell(a)} | {cell(b)} | {guards(gid, cls, files)} | {ITERATIONS.get(gid, 1)} | "
                    f"{'принято' if ok else 'не принято'} |")
    head = [f"Роль А: {head_a}", "", f"Роль Б: {head_b}", ""]
    return "\n".join(head + rows) + "\n", missing, len(rows) - 2


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--basis", type=int, default=110)
    parser.add_argument("--out")
    args = parser.parse_args(argv)
    text, missing, total = build(args.basis)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
    else:
        print(text)
    print(f"записей: {total}; без вердикта: {len(missing)} {missing}", file=sys.stderr)
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
