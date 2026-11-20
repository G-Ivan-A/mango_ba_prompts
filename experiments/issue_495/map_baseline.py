#!/usr/bin/env python3
"""Сведение 100 % нарушений базы к группам реестра (issue #495, ФТ-1, ФТ-2).

Берёт базу задачи (коммит ``BASE``), прогоняет по ней действующий аудитор с
действующей политикой и относит каждое нарушение ровно к одной группе:

* записи реестра замен ``U-xx``/``D-xx``/``A-01`` (``rewrite_cases.py``) — по
  тексту «было», найденному в строке нарушения;
* ``M-xx`` — механическая проекция ``scripts/prompt_purity.project`` (ссылки
  на спицу → подпись, служебные HTML-комментарии → удалены) для ручных
  исходников и архива;
* ``G-xx`` — сгенерированные файлы, которые исправила пересборка из чистых
  источников (сборщики черновиков и сайта).

Нарушение без группы — дефект реестра: скрипт печатает его и выходит с кодом 1.
Второй контроль — аудит текущего дерева: 0 нарушений, то есть каждая группа
действительно закрыта.

    python3 experiments/issue_495/map_baseline.py [--base-root ПУТЬ] [--md out.md] [--json out.json]

Без ``--base-root`` база выгружается во временный каталог через ``git archive``.
Скрипт ничего не меняет в репозитории и не вызывает LLM.
"""
import argparse
import io
import json
import re
import subprocess
import sys
import tarfile
import tempfile
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_prompt_purity as audit  # noqa: E402
import prompt_purity  # noqa: E402
import rewrite_cases  # noqa: E402

BASE = "e051e0fa46e22c43004a6af19e8c53b827ce1b1d"

GROUPS = {
    "M-01": ("а", "Ручные исходники промптов и ССОТ: ссылки на спицу (абсолютные и относительные) → подпись ссылки",
             "experiments/issue_495/clean_sources.py → prompt_purity.project (delink)"),
    "M-02": ("в", "Ручные исходники: служебные HTML-комментарии удалены",
             "experiments/issue_495/clean_sources.py → prompt_purity.project (strip_comments)"),
    "M-03": ("а", "Архив 2.7.0 и прежних редакций: ссылки на спицу → подпись; хэши оригинала — в манифесте архива",
             "clean_sources.py; prompts/archive/a-in-v2.7.0/manifest.json"),
    "M-04": ("а", "Служебные файлы рядом с промптами (README, манифесты, каталог): ссылки на спицу → пути от корня",
             "ручная правка + сборщики манифестов"),
    "M-05": ("а", "Ссылки на спицу, которые строят сами сборщики (REPO_BLOB, AIN_BLOB, SYSTEM_BLOB, ISSUE): "
             "проекция на выходе сборщика → подпись ссылки",
             "prompt_purity.project в build_bcreq_step_prompts, build_bcreq_a_in, build_bcreq_system_track; "
             "сторож test_builders_check"),
    "G-01": ("а, б, в", "Черновики, A-IN и системный трек (`prompts/drafts/**`): только копии нарушений ручных "
             "источников (окно ±15 символов вокруг нарушения есть в ручном исходнике базы); "
             "пересборка из чистых ССОТ",
             "сборщики bcreq_handoff, build_bcreq_a_in, build_bcreq_step_prompts, build_bcreq_system_track (проекция стандартов)"),
    "G-02": ("а", "Данные сайта: поля url/путь → путь от корня, ссылку строит интерфейс",
             "A-01: scripts/generate-pages-data.mjs (repoUrl), site/app.js (repoHref)"),
    "G-03": ("а, б, в", "Данные сайта: тела промптов и поля карточек — только копии нарушений ручных источников "
             "(то же окно ±15 символов)",
             "node scripts/generate-pages-data.mjs"),
}

JSON_VALUE = re.compile(r'^\s*"[\w.]+":\s*"(.*)$')

HAND_PREFIXES = ("prompts/", "standards/bcreq-manual-classes/", "docs/ba-processes/")


def export_base(target):
    data = subprocess.run(["git", "archive", "--format=tar", BASE], cwd=ROOT, capture_output=True, check=True).stdout
    with tarfile.open(fileobj=io.BytesIO(data)) as tar:
        tar.extractall(target, filter="data")


def register_entries():
    """(id, файлы, фрагменты «было») из реестра замен; «…» делит фрагменты."""
    out = []
    for eid, files, old, *_ in rewrite_cases.EDITS + rewrite_cases.REGISTER_ONLY:
        pieces = [p.strip() for chunk in old.split("…") for p in chunk.split("\n")]
        # Записи по JSON-ССОТ хранят «было» с ключом и кавычками; в черновиках
        # и на сайте тот же текст стоит без них.
        pieces += [JSON_VALUE.sub(r"\1", p).strip().rstrip('",').strip() for p in pieces if JSON_VALUE.search(p)]
        pieces = [p for p in pieces if len(p) >= 12 and p not in ("| --- | --- | --- | --- |",)]
        paths = [f.split(" (")[0] for f in files]
        out.append((eid, paths, old, pieces))
    out.append(("D-11", ["prompts/archive/*.md"], rewrite_cases.ARCHIVE_BANNER[0], [rewrite_cases.ARCHIVE_BANNER[0]]))
    for rel, old, _ in rewrite_cases.FRONTMATTER_LINKS:
        out.append(("D-12", [rel], old, [old]))
    return out


def line_ranges(text, old):
    """Номера строк (1-based), которые занимает каждое вхождение ``old``."""
    lines, pos = set(), 0
    while True:
        i = text.find(old, pos)
        if i < 0:
            return lines
        start = text.count("\n", 0, i) + 1
        lines.update(range(start, start + old.count("\n") + 1))
        pos = i + 1


def squash(text):
    return re.sub(r"\s+", " ", text)


def window(f, pad=15):
    """Окно ±``pad`` символов вокруг нарушения в его фрагменте (пробелы сжаты)."""
    snippet = squash(f["snippet"]).strip("…")
    i = snippet.find(f["match"])
    if i < 0:
        return snippet[:60].strip()
    return snippet[max(0, i - pad):i + len(f["match"]) + pad].strip("…").strip()


class Mapper:
    def __init__(self, base_root, kinds=None):
        self.root = Path(base_root)
        self.entries = register_entries()
        self.texts = {}
        # Ручные исходники базы (всё в контуре, кроме собранных черновиков и данных
        # сайта): группы G принимают только копии их нарушений. Текст сборщика,
        # которого нет в ручных исходниках, должен иметь свою запись реестра.
        hand = [rel for rel, kind in (kinds or {}).items()
                if kind != "site_data" and not rel.startswith("prompts/drafts/")]
        raw = "\n".join((self.root / rel).read_text(encoding="utf-8") for rel in sorted(hand))
        self.hand = squash(raw) + "\n" + squash(prompt_purity.project(raw))

    def is_copy(self, f):
        w = window(f)
        return w in self.hand or squash(prompt_purity.project(w + "\n")).strip() in self.hand

    def line(self, rel, no):
        if rel not in self.texts:
            self.texts[rel] = (self.root / rel).read_text(encoding="utf-8")
        lines = self.texts[rel].splitlines()
        return lines[no - 1] if 0 < no <= len(lines) else ""

    def by_register(self, f, kind):
        rel = f["file"]
        if kind == "site_data":
            text_line = f["snippet"]
        else:
            text_line = self.line(rel, f["line"])
        for eid, paths, old, pieces in self.entries:
            if rel in paths and kind != "site_data":
                if f["line"] in line_ranges(self.texts[rel], old):
                    return eid
                # «Было» записано после снятия ссылок: ищем его в тексте без
                # ссылок, если снятие не сдвинуло строки.
                delinked = prompt_purity.delink(self.texts[rel])
                if delinked.count("\n") == self.texts[rel].count("\n") \
                        and f["line"] in line_ranges(delinked, old):
                    return eid
        # Копии в сгенерированных файлах и в данных сайта: по фрагменту «было».
        # «Было» в реестре записано после проекции (ссылки уже сняты), поэтому
        # строка сравнивается и в исходном виде, и в проекции.
        candidates = (text_line, prompt_purity.project(text_line + "\n").rstrip("\n"))
        for eid, paths, old, pieces in self.entries:
            for piece in pieces:
                if f["match"] in piece and any(piece in c for c in candidates):
                    return eid
        # Сгенерированные копии: строку, которую целиком сняла запись реестра
        # (например, служебный комментарий D-18), относим к записи по всем правилам.
        if kind == "site_data" or rel.startswith("prompts/drafts/"):
            for eid, paths, old, pieces in self.entries:
                if any(len(p) >= 20 and p in c for p in pieces for c in candidates):
                    return eid
        return None

    def classify(self, f, kind):
        rel, rule = f["file"], f["rule"]
        if kind == "archive_texts" and (rule.startswith("A-") or rule == "BP-01"):
            # Архив чистит только проекция (решение владельца, п.14).
            return "M-03" if rule.startswith("A-") else "M-02"
        eid = self.by_register(f, kind)
        if eid:
            return eid
        if kind == "site_data" and (f["where"].endswith(".url") or f["where"] in ("issue",)):
            return "G-02"
        if kind == "site_data" or rel.startswith("prompts/drafts/"):
            if self.is_copy(f):
                return "G-03" if kind == "site_data" else "G-01"
            return "M-05" if rule.startswith("A-") else None
        if kind == "archive_texts":
            return "M-03" if rule.startswith("A-") else ("M-02" if rule == "BP-01" else None)
        if kind == "repo_docs_in_prompts":
            return "M-04"
        if rel.startswith(HAND_PREFIXES):
            if rule.startswith("A-"):
                return "M-01"
            if rule == "BP-01":
                return "M-02"
        return None


def build(base_root):
    policy = audit.load_policy()
    auditor = audit.Auditor(base_root, policy)
    findings = auditor.run()
    mapper = Mapper(base_root, auditor.files)
    groups, unmapped = defaultdict(list), []
    for f in findings:
        g = mapper.classify(f, auditor.files[f["file"]])
        (groups[g] if g else unmapped).append(f)
    head = audit.Auditor(ROOT, policy).run()
    return findings, groups, unmapped, head


def describe(gid):
    if gid in GROUPS:
        return GROUPS[gid]
    for eid, files, old, new, _, cls, where in rewrite_cases.EDITS + rewrite_cases.REGISTER_ONLY:
        if eid == gid:
            return cls, f"{', '.join(files)}: «{old.splitlines()[0][:90]}»", where
    if gid == "D-11":
        return "в", "Баннер архива «(issue #388)» в 18 из 24 файлов архива (`prompts/archive/*.md`)", "> **Архив.** Промпт заменён; номер решения — prompts/README.md (строки 50, 107, 169)"
    if gid == "D-12":
        return "а", "Ссылки на issue во frontmatter служебных файлов", "номер issue вместо URL"
    return "?", gid, ""


def order(gid):
    kind, _, num = gid.partition("-")
    return ("UDAMG".index(kind[0]) if kind[0] in "UDAMG" else 9, int("".join(c for c in num if c.isdigit()) or 0), num)


def to_markdown(findings, groups, unmapped, head):
    out = [f"База `{BASE[:8]}`, действующая политика: нарушений {len(findings)}; "
           f"отнесено к группам {sum(map(len, groups.values()))}; без группы {len(unmapped)}; "
           f"нарушений в текущем дереве {len(head)}.", "",
           "| Группа | Класс | Что | Исправление / куда перенесено | Нарушений базы | Файлов | По правилам |",
           "| --- | --- | --- | --- | --- | --- | --- |"]
    ids = set(groups) | {e[0] for e in rewrite_cases.EDITS + rewrite_cases.REGISTER_ONLY} | {"D-11", "D-12"}
    for gid in sorted(ids, key=order):
        items = groups.get(gid, [])
        cls, what, where = describe(gid)
        rules = Counter(f["rule"] for f in items)
        files = {f["file"] for f in items}
        cell = lambda s: s.replace("|", "\\|").replace("\n", " ")
        out.append(f"| {gid} | {cls} | {cell(what)} | {cell(where)} | {len(items)} | {len(files)} | "
                   + ", ".join(f"{r}: {n}" for r, n in sorted(rules.items())) + " |")
    return "\n".join(out) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-root")
    parser.add_argument("--md")
    parser.add_argument("--json")
    args = parser.parse_args(argv)
    with tempfile.TemporaryDirectory() as tmp:
        base_root = Path(args.base_root) if args.base_root else Path(tmp)
        if not args.base_root:
            export_base(base_root)
        findings, groups, unmapped, head = build(base_root)
    md = to_markdown(findings, groups, unmapped, head)
    print(md)
    if args.md:
        Path(args.md).write_text(md, encoding="utf-8")
    if args.json:
        Path(args.json).write_text(json.dumps(
            {"base": BASE, "total": len(findings), "head_findings": len(head),
             "groups": {g: [f["id"] for f in items] for g, items in sorted(groups.items(), key=lambda x: order(x[0]))},
             "unmapped": unmapped}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    for f in unmapped[:60]:
        print("БЕЗ ГРУППЫ:", f["id"], f["rule"], f"{f['file']}:{f['line']}", f["where"], f["snippet"][:110], file=sys.stderr)
    return 1 if unmapped or head else 0


if __name__ == "__main__":
    sys.exit(main())
