#!/usr/bin/env python3
"""Исключения контура аудита чистоты (issue #495, проблема A).

Не путать с трассировкой игнорирования прежних требований (issue, раздел 2):
та отвечает, почему прежнее требование не исполнялось, и живёт в описании PR;
здесь — механизмы, которыми аудитор сознательно не считает совпадение
нарушением.

Для каждого механизма, которым аудитор не считает совпадение нарушением,
снимает ровно это исключение и считает, сколько совпадений оно гасит. Так
каждое «не нарушение» объяснено механизмом и решением, а не потеряно молча.

    python3 experiments/issue_495/ignore_trace.py [--root ПУТЬ] [--md out.md]

``--root`` — проверяемое дерево (по умолчанию — репозиторий); политика и
аудитор берутся из текущего репозитория. Скрипт ничего не меняет и не
вызывает LLM.
"""
import argparse
import copy
import fnmatch
import glob
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import audit_prompt_purity as audit  # noqa: E402

# Механизм → (что снимаем, основание). Порядок — порядок строк таблицы.
MECHANISMS = [
    ("IG-1", "Архив 2.7.0 и прежних редакций: классы б и в (кроме HTML-комментариев) не применяются",
     "Постановка, проблема A: приватные ссылки убираются из всех промптов, включая архив, — класс а применяется и снят проекцией; удаление текста архива — только по команде (БС-12), поэтому классы б и в в архиве не применяются (стандарт, раздел 5). Статус архива 2.7.0 как исторической сущности — комментарий 2, п.14"),
    ("IG-2", "Карточки архивных промптов в данных сайта (`archive_source_globs`): классы б и в, кроме BP-01, и правило A-SPOKE-PATH",
     "То же основание, что IG-1: карточка сайта — копия архивного текста; BP-01 (HTML-комментарий) снят проекцией"),
    ("IG-3", "Frontmatter промптов: классы б и в и правила A-PRIVATE-NAME/A-RELATIVE/A-SPOKE-PATH",
     "Frontmatter — метаданные карточки, в исполнимый текст не копируется (сборщики и сайт отрезают его)"),
    ("IG-4", "Служебные файлы рядом с промптами (`repo_docs_in_prompts`): только класс а",
     "Это не исполнимые промпты (README, манифесты, каталог); приватные ссылки в них всё равно запрещены"),
    ("IG-5", "ССОТ A-IN (`ssot_texts`): класс в не применяется",
     "ССОТ — источник сборки, его служебная разметка отрезается сборщиком; балласт проверяется в собранных черновиках"),
    ("IG-6", "Данные сайта вне тел промптов: класс в и класс б вне карточек",
     "Поля интерфейса (заголовки, описания процессов, счётчики) не исполняются моделью; тела промптов проверяются полностью"),
    ("IG-7", "Публичный адрес сайта `g-ivan-a.github.io/mango_ba_prompts` не считается голым именем репозитория",
     "Публичный адрес доступен исполнителю и не ведёт в приватный репозиторий (политика, `private_name_note`)"),
    ("IG-8", "Разметка сайта (`site/index.html`, `site/app.js`, `site/*.css`) вне контура",
     "Интерфейс, а не промпт: ссылку «исходник на GitHub» строит интерфейс (стандарт, раздел 5; ЧП-5)"),
    ("IG-9", "Правило A-SPOKE-PATH (голый путь спицы) — только тело действующего промпта: архив, карточки архива, "
     "frontmatter, ССОТ, служебные файлы и поля сайта вне тел не проверяются",
     "Архив — история (п.14, БС-12); в ССОТ, служебных файлах, frontmatter и полях интерфейса путь спицы адресован "
     "сопровождающему, а не исполнителю промпта (стандарт, ЧП-1, правило A-SPOKE-PATH)"),
    ("IG-10", "Пути runtime `docs/kb`, `docs/guides` не считаются путями спицы",
     "Это каталоги runtime, доступные исполнителю по SHA реестра справочников; путь спицы — `docs/` всего остального "
     "(политика, `spoke_path_note`)"),
]


class Relaxed(audit.Auditor):
    """Аудитор с флагами снятия исключений IG-3, IG-6 и IG-9."""

    no_frontmatter = False
    all_site_fields = False
    spoke_everywhere = False

    def check_links(self, line, *, prompt_text, live=False):
        return super().check_links(line, prompt_text=prompt_text, live=live or self.spoke_everywhere)

    def run(self):
        """IG-3: frontmatter считается телом — и в файлах, и в телах промптов данных сайта."""
        if not self.no_frontmatter:
            return super().run()
        saved = audit.split_frontmatter
        audit.split_frontmatter = lambda text: (0, text)
        try:
            return super().run()
        finally:
            audit.split_frontmatter = saved

    def audit_site_file(self, rel, classes, body_fields, card):
        if not self.all_site_fields:
            return super().audit_site_file(rel, classes, body_fields, card)
        data = json.loads((self.root / rel).read_text(encoding="utf-8"))
        for path, value, archived in audit.walk(data, archive=self.is_archive_card):
            is_body = any(audit.field_match(path, f) for f in body_fields)
            front = audit.split_frontmatter(value)[0] if is_body else 0
            for no, line in enumerate(value.splitlines() or [value], 1):
                found = self.check_links(line, prompt_text=is_body, live=is_body and not archived and no > front)
                if not archived:
                    found += self.check_tokens(line)
                found += self.check_ballast(line, {"BP-01"} if archived else None)
                for cls, rule, match in found:
                    self.add(rel, no, cls, rule, match, line, path)


def run(root, policy, **flags):
    auditor = Relaxed(root, policy)
    for key, value in flags.items():
        setattr(auditor, key, value)
    return auditor.run()


def variant(policy, mech):
    p = copy.deepcopy(policy)
    flags = {}
    if mech == "IG-1":
        p["contour"]["archive_texts"]["classes"] = ["a", "b", "c"]
        p["contour"]["archive_texts"].pop("ballast_ids", None)
    elif mech == "IG-2":
        p["contour"]["site_data"]["archive_source_globs"] = []
    elif mech == "IG-3":
        flags["no_frontmatter"] = True
    elif mech == "IG-4":
        p["contour"]["repo_docs_in_prompts"]["classes"] = ["a", "b", "c"]
    elif mech == "IG-5":
        p["contour"]["ssot_texts"]["classes"] = ["a", "b", "c"]
    elif mech == "IG-6":
        flags["all_site_fields"] = True
    elif mech == "IG-7":
        p["links"]["public_site_regex"] = r"(?!)"
    elif mech == "IG-9":
        flags["spoke_everywhere"] = True
    elif mech == "IG-10":
        p["links"]["spoke_path_regex"] = p["links"]["spoke_path_regex"].replace(r"docs/(?!kb\b|guides\b)", "docs/")
        assert p["links"]["spoke_path_regex"] != policy["links"]["spoke_path_regex"]
    return p, flags


def markup_hits(root, policy):
    rx = re.compile(policy["links"]["private_link_regex"])
    hits = Counter()
    for pattern in ("site/*.html", "site/*.js", "site/*.css"):
        for name in sorted(glob.glob(str(Path(root) / pattern))):
            rel = Path(name).relative_to(root).as_posix()
            n = len(rx.findall(Path(name).read_text(encoding="utf-8")))
            if n:
                hits[rel] = n
    return hits


def trace(root):
    policy = audit.load_policy()
    base = run(root, policy)
    base_count = Counter((f["file"], f["rule"]) for f in base)
    rows = []
    for mech, what, why in MECHANISMS:
        if mech == "IG-8":
            hits = markup_hits(root, policy)
            rows.append((mech, what, why, sum(hits.values()), {f"{k} A-PRIVATE": v for k, v in hits.items()}))
            continue
        p, flags = variant(policy, mech)
        relaxed = Counter((f["file"], f["rule"]) for f in run(root, p, **flags))
        extra = relaxed - base_count
        by_rule = Counter()
        for (rel, rule), n in extra.items():
            by_rule[rule] += n
        rows.append((mech, what, why, sum(extra.values()), dict(sorted(by_rule.items()))))
    return len(base), rows


def to_markdown(root, total, rows):
    out = [f"Дерево: `{root}`; нарушений по действующей политике: {total}", "",
           "| ID | Что не считается нарушением | Основание | Погашено совпадений | По правилам |",
           "| --- | --- | --- | --- | --- |"]
    for mech, what, why, n, detail in rows:
        rules = ", ".join(f"{k}: {v}" for k, v in detail.items()) or "—"
        out.append(f"| {mech} | {what} | {why} | {n} | {rules} |")
    return "\n".join(out) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(ROOT))
    parser.add_argument("--md")
    args = parser.parse_args(argv)
    total, rows = trace(Path(args.root))
    md = to_markdown(Path(args.root).name if Path(args.root) != ROOT else ".", total, rows)
    if args.md:
        Path(args.md).write_text(md, encoding="utf-8")
    print(md)


if __name__ == "__main__":
    main()
