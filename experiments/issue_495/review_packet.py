#!/usr/bin/env python3
"""Пакет для двухролевой проверки реестра (issue #495, дополнение 1).

Для каждой записи реестра (U/D/A — точечные правки, M — механическая проекция,
G — пересборка) собирает то, что рецензенту нужно для вердикта без цепочки
рассуждений исполнителя: класс, «было», «стало», куда перенесено, локаторы
нарушений базы и машинную сверку «было отсутствует / стало присутствует» в
текущем дереве. Рецензенты получают пакет, правила (постановку, комментарии
владельца, стандарт чистоты) и доступ к обоим деревьям.

    python3 experiments/issue_495/review_packet.py [--base-root ПУТЬ] [--out packet.md]

Скрипт ничего не меняет в репозитории и не вызывает LLM.
"""
import argparse
import json
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import map_baseline as mb  # noqa: E402

ROOT = mb.ROOT
SAMPLES = 8


def check_presence(entry_files, old, new):
    """Сверка текущего дерева: «было» ушло, «стало» на месте (по фрагментам).

    Сборщик держит «было» левой частью пары замены (словарь CASE_EDITS или
    кортеж на одной строке с «стало»): такой текст в собранный промпт не идёт и
    считается отдельно.
    """
    rows = []
    for spec in entry_files:
        rel = spec.split(" (")[0]
        path = ROOT / rel
        if "*" in rel or not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        old_pieces, new_pieces = pieces(old), pieces(new)
        rest = text
        if "CASE_EDITS = {" in text:
            start = text.index("CASE_EDITS = {")
            rest = text.replace(text[start:text.index("\n}\n", start)], "")
        old_left = [p for p in old_pieces
                    if any(p in ln and not any(n in ln for n in new_pieces) for ln in rest.splitlines())]
        pairs = [p for p in old_pieces if p in text and p not in old_left]
        new_found = [p for p in new_pieces if p in text]
        note = f" (только левая часть пары замены сборщика: {len(pairs)})" if pairs else ""
        rows.append(f"- `{rel}`: «было» в тексте — {'да: ' + '; '.join(old_left[:2]) if old_left else 'нет' + note}; "
                    f"«стало» — {f'{len(new_found)}/{len(new_pieces)} фрагментов' if new_pieces else 'удаление'}")
    return rows


def pieces(text):
    """Фрагменты сверки: «…» и перенос строки делят запись на куски."""
    out = [p.strip().strip('"') for chunk in text.split("…") for p in chunk.split("\n")]
    return [p for p in out if len(p) >= 8 and not p.startswith("—") and p.strip("|-: ")]


def generated_texts():
    """Собранные черновики и данные сайта; архивные карточки prompts.json — отдельно.

    Архив 2.7.0 чистит только проекция (решение владельца, п.14): кейс-лексика
    в нём остаётся как история и проверяется контуром archive_texts.
    """
    live, archive = {}, {}
    for path in sorted((ROOT / "prompts/drafts").rglob("*.md")):
        live[path.relative_to(ROOT).as_posix()] = path.read_text(encoding="utf-8")
    for path in sorted((ROOT / "site/data").glob("*.json")):
        rel = path.relative_to(ROOT).as_posix()
        data = json.loads(path.read_text(encoding="utf-8"))
        if rel.endswith("prompts.json"):
            for card in data["prompts"]:
                bucket = archive if card.get("archived") else live
                bucket[f"{rel}#{card['id']}"] = json.dumps(card, ensure_ascii=False)
            data = {k: v for k, v in data.items() if k != "prompts"}
        live[rel] = json.dumps(data, ensure_ascii=False)
    return live, archive


LIVE, ARCHIVE = generated_texts()


def check_generated(old, new):
    """Сверка собранных черновиков и данных сайта: копии «было» ушли, «стало» пришло."""
    new_pieces = pieces(new)
    old_pieces = [p for p in pieces(old) if not any(p in n for n in new_pieces)]
    old_live = sorted({p for p in old_pieces for t in LIVE.values() if p in t})
    old_arch = {key for p in old_pieces for key, t in ARCHIVE.items() if p in t}
    new_files = {key for p in new_pieces for key, t in LIVE.items() if p in t}
    return (f"- Собранные черновики и данные сайта ({len(LIVE)} единиц): фрагментов «было» — {len(old_live)}"
            f"{': ' + '; '.join(old_live[:2]) if old_live else ''}; единиц с «стало» — {len(new_files)}; "
            f"архивных карточек 2.7.0 с «было» (только проекция, п.14) — {len(old_arch)}")


def sample_lines(items):
    out = []
    for f in items[:SAMPLES]:
        snippet = f["snippet"].replace("`", "'")[:160]
        out.append(f"- {f['id']} `{f['file']}:{f['line']}` ({f['where']}) {f['rule']} «{f['match']}» — `{snippet}`")
    if len(items) > SAMPLES:
        out.append(f"- … ещё {len(items) - SAMPLES} (полный список — `audit/baseline-map.json`)")
    return out


def after_state(items, head):
    """Для групп M/G: файлы группы, удалённые файлы и нарушения в их текущих версиях."""
    files = sorted({f["file"] for f in items})
    gone = [rel for rel in files if not (ROOT / rel).exists()]
    left = [f for f in head if f["file"] in files]
    return left, files, gone


def build(base_root):
    findings, groups, unmapped, head = mb.build(base_root)
    entries = {e[0]: e for e in rewrite_entries()}
    out = ["# Пакет двухролевой проверки реестра issue #495", "",
           f"База `{mb.BASE[:8]}`: нарушений {len(findings)}, без группы {len(unmapped)}; "
           f"текущее дерево: нарушений {len(head)}.", ""]
    ids = set(groups) | set(entries) | set(mb.GROUPS)
    for gid in sorted(ids, key=mb.order):
        items = groups.get(gid, [])
        cls, what, where = mb.describe(gid)
        out += [f"## {gid}", "", f"- Класс: {cls}", f"- Что: {what}", f"- Исправление / куда перенесено: {where}",
                f"- Нарушений базы в группе: {len(items)}", ""]
        if gid in entries:
            _, files, old, new = entries[gid]
            out += ["Файлы: " + ", ".join(f"`{f}`" for f in files), "", "Было:", "```text", old.rstrip("\n"), "```",
                    "Стало:", "```text", (new.rstrip("\n") or "— (удалено)"), "```", ""]
            presence = check_presence(files, old, new) + [check_generated(old, new)]
            out += ["Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — "
                    "проверять вручную):", *presence, ""]
        if items:
            out += ["Локаторы базы (выборка):", *sample_lines(items), ""]
            if gid[0] in "MG":
                left, files, gone = after_state(items, head)
                out.append(f"Файлов группы: {len(files)}; удалено из дерева: {len(gone)}; "
                           f"нарушений в текущих версиях этих файлов: {len(left)}.")
                out.append("")
    return "\n".join(line.rstrip() for block in out for line in block.split("\n")).rstrip("\n") + "\n"


def rewrite_entries():
    rc = mb.rewrite_cases
    out = [(eid, files, old, new) for eid, files, old, new, *_ in rc.EDITS + rc.REGISTER_ONLY]
    out.append(("D-11", ["prompts/archive/*.md"], *rc.ARCHIVE_BANNER))
    out.append(("D-12", [rel for rel, _, _ in rc.FRONTMATTER_LINKS],
                "\n".join(o for _, o, _ in rc.FRONTMATTER_LINKS), "\n".join(n for _, _, n in rc.FRONTMATTER_LINKS)))
    return out


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-root")
    parser.add_argument("--out")
    args = parser.parse_args(argv)
    with tempfile.TemporaryDirectory() as tmp:
        base_root = Path(args.base_root) if args.base_root else Path(tmp)
        if not args.base_root:
            mb.export_base(base_root)
        text = build(base_root)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
    else:
        print(text)


if __name__ == "__main__":
    main()
