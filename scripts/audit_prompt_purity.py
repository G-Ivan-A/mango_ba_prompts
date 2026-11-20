#!/usr/bin/env python3
"""Аудит чистоты исполнимых промптов: три класса нарушений.

Классы (стандарт ``standards/bcreq-prompt-purity.md``):

* ``a`` — ссылки: URL приватного репозитория (в теле промпта — и голое имя
  репозитория), относительная ссылка на файл
  репозитория из текста промпта (у исполнителя промпта её нет), ссылка на
  runtime не по SHA из реестра справочников runtime;
* ``b`` — кейс-специфика: токены словаря ``case_tokens`` вне разрешённых
  справочных секций;
* ``c`` — неисполнимый балласт: шаблоны ``ballast_patterns`` в теле промпта
  (frontmatter — метаданные карточки, в тело не копируется и не проверяется).

Контур, словарь и шаблоны — в ``standards/bcreq-prompt-purity.json``. Архив
прежних редакций (контур ``archive_texts`` и карточки сайта из
``archive_source_globs``) — историческая сущность: для него проверяются только
ссылки (класс a) и служебные HTML-комментарии.
Скрипт ничего не меняет и не вызывает LLM.

    python3 scripts/audit_prompt_purity.py                 # сводка, код 1 при нарушениях
    python3 scripts/audit_prompt_purity.py --json out.json --md out.md
"""
import argparse
import fnmatch
import glob
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "standards/bcreq-prompt-purity.json"
CLASS_NAMES = {"a": "приватные/незакреплённые ссылки", "b": "кейс-специфика", "c": "неисполнимый балласт"}


def load_policy(path=POLICY):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def runtime_sha(root=ROOT, policy=None):
    policy = policy or load_policy()
    text = (root / policy["links"]["runtime_sha_registry"]).read_text(encoding="utf-8")
    match = re.search(r'(?m)^runtime_sha:\s*"?([0-9a-f]{40})"?', text)
    if not match:
        raise SystemExit("реестр справочников runtime: нет runtime_sha во frontmatter")
    return match.group(1)


def expand(root, spec):
    files = []
    for pattern in spec["globs"]:
        for name in sorted(glob.glob(str(root / pattern))):
            rel = Path(name).relative_to(root).as_posix()
            if any(fnmatch.fnmatch(rel, ex) for ex in spec.get("exclude", [])):
                continue
            files.append(rel)
    return files


def split_frontmatter(text):
    """Вернуть (число строк frontmatter, тело). Frontmatter — с первой строки."""
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            head = text[: end + 5]
            return head.count("\n"), text[end + 5:]
    return 0, text


class Auditor:
    def __init__(self, root=ROOT, policy=None):
        self.root = Path(root)
        self.policy = policy or load_policy(self.root / "standards/bcreq-prompt-purity.json")
        links = self.policy["links"]
        self.private = links["private_repo"]
        self.private_re = re.compile(links["private_link_regex"])
        self.public_site_re = re.compile(links["public_site_regex"])
        self.sha = runtime_sha(self.root, self.policy)
        self.runtime_re = re.compile(links["runtime_link_regex"])
        self.relative_re = re.compile(links["relative_repo_link_regex"])
        self.tokens = [(t["id"], re.compile(t["regex"]), t) for t in self.policy["case_tokens"]]
        self.ballast = [(b["id"], re.compile(b["regex"]), b) for b in self.policy["ballast_patterns"]]
        self.allowed = self.policy.get("allowed_sections", [])
        self.archive_sources = self.policy["contour"]["site_data"].get("archive_source_globs", [])
        self.findings = []

    # --- правила по строке -------------------------------------------------
    def check_links(self, line, *, prompt_text):
        out = []
        for match in self.private_re.finditer(line):
            out.append(("a", "A-PRIVATE", match.group(0)))
        if prompt_text and not out and self.private in self.public_site_re.sub("", line):
            out.append(("a", "A-PRIVATE-NAME", self.private))
        for match in self.runtime_re.finditer(line):
            if match.group(1) != self.sha:
                out.append(("a", "A-RUNTIME-UNPINNED", match.group(0)))
        if prompt_text:
            for match in self.relative_re.finditer(line):
                target = match.group(1)
                if target.startswith(("http", "#")):
                    continue
                out.append(("a", "A-RELATIVE", target))
        return out

    def check_tokens(self, line):
        return [("b", tid, m.group(0)) for tid, rx, _ in self.tokens for m in rx.finditer(line)]

    def check_ballast(self, line, ids=None):
        return [("c", bid, m.group(0)) for bid, rx, _ in self.ballast
                if ids is None or bid in ids for m in rx.finditer(line)]

    def is_allowed(self, rel, heading, rule_id):
        for item in self.allowed:
            if fnmatch.fnmatch(rel, item["file"]) and rule_id in item["tokens"] \
                    and heading and re.search(item["heading"], heading):
                return True
        return False

    def add(self, rel, line_no, cls, rule, match, line, where):
        snippet = line.strip()
        if len(snippet) > 160:
            pos = snippet.find(match)
            start = max(0, pos - 60)
            snippet = ("…" if start else "") + snippet[start:start + 150] + "…"
        self.findings.append({"class": cls, "rule": rule, "file": rel, "line": line_no,
                              "match": match, "where": where, "snippet": snippet})

    # --- файлы -------------------------------------------------------------
    def audit_text_file(self, rel, classes, *, prompt_text, ballast_ids=None):
        text = (self.root / rel).read_text(encoding="utf-8")
        fm_lines, _ = split_frontmatter(text) if rel.endswith(".md") else (0, text)
        heading = ""
        for no, line in enumerate(text.splitlines(), 1):
            in_body = no > fm_lines
            if in_body and line.startswith("#"):
                heading = line
            found = []
            if "a" in classes:
                found += self.check_links(line, prompt_text=prompt_text and in_body)
            if in_body and "b" in classes:
                found += [f for f in self.check_tokens(line) if not self.is_allowed(rel, heading, f[1])]
            if in_body and "c" in classes:
                found += self.check_ballast(line, ballast_ids)
            for cls, rule, match in found:
                self.add(rel, no, cls, rule, match, line, "frontmatter" if not in_body else "body")

    def audit_site_file(self, rel, classes, body_fields, card):
        data = json.loads((self.root / rel).read_text(encoding="utf-8"))
        for path, value, archived in walk(data, archive=self.is_archive_card):
            is_body = any(field_match(path, f) for f in body_fields)
            for no, line in enumerate(value.splitlines() or [value], 1):
                found = self.check_links(line, prompt_text=is_body) if "a" in classes else []
                if "b" in classes and (card or is_body) and not archived:
                    found += self.check_tokens(line)
                if is_body:
                    found += self.check_ballast(line, {"BP-01"} if archived else None)
                for cls, rule, match in found:
                    self.add(rel, no, cls, rule, match, line, path)

    def is_archive_card(self, node):
        source = node.get("sourcePath") or node.get("relativePath") or ""
        return isinstance(source, str) and any(fnmatch.fnmatch(source, g) for g in self.archive_sources)

    def run(self):
        contour = self.policy["contour"]
        self.files = {}
        for name in ("prompt_texts", "archive_texts", "ssot_texts", "repo_docs_in_prompts"):
            spec = contour[name]
            for rel in expand(self.root, spec):
                self.files[rel] = name
                self.audit_text_file(rel, set(spec["classes"]), prompt_text=name in ("prompt_texts", "archive_texts"),
                                     ballast_ids=set(spec["ballast_ids"]) if "ballast_ids" in spec else None)
        site = contour["site_data"]
        for rel in expand(self.root, site):
            self.files[rel] = "site_data"
            self.audit_site_file(rel, set(site["classes"]), site["prompt_body_fields"].get(rel, []),
                                 rel in site["card_files"])
        for i, item in enumerate(self.findings, 1):
            item["id"] = f"V-{i:04d}"
        return self.findings


def walk(node, path="", archive=lambda node: False, archived=False):
    """Строки JSON: (путь, значение, лежит ли в карточке архивного промпта)."""
    if isinstance(node, dict):
        archived = archived or archive(node)
        for key, value in node.items():
            yield from walk(value, f"{path}.{key}" if path else key, archive, archived)
    elif isinstance(node, list):
        for value in node:
            yield from walk(value, f"{path}[]", archive, archived)
    elif isinstance(node, str):
        yield path, node, archived


def field_match(path, pattern):
    if pattern.endswith(".*"):
        return path.startswith(pattern[:-2] + ".")
    return path == pattern


def summary(findings, files):
    by_class = Counter(f["class"] for f in findings)
    by_rule = Counter((f["class"], f["rule"]) for f in findings)
    by_file = Counter((f["file"], f["class"]) for f in findings)
    lines = [f"Файлов в контуре: {len(files)}; нарушений: {len(findings)}"]
    for cls in "abc":
        lines.append(f"  ({cls}) {CLASS_NAMES[cls]}: {by_class.get(cls, 0)}")
    lines.append("По правилам:")
    for (cls, rule), n in sorted(by_rule.items()):
        lines.append(f"  {cls} {rule}: {n}")
    lines.append("По файлам (a/b/c):")
    for rel in sorted({f for f, _ in by_file}):
        lines.append(f"  {rel}: " + "/".join(str(by_file.get((rel, c), 0)) for c in "abc"))
    return "\n".join(lines)


def to_markdown(findings, files, title):
    out = [f"# {title}", "", "```", summary(findings, files), "```", "",
           "| ID | Класс | Правило | Локатор | Совпадение | Фрагмент |", "| --- | --- | --- | --- | --- | --- |"]
    for f in findings:
        # «](» экранируется: фрагмент — цитата, а не ссылка (проверка ссылок #265).
        snippet = f["snippet"].replace("|", "\\|").replace("](", "]\\(")
        match = f["match"].replace("|", "\\|")
        loc = f"{f['file']}:{f['line']}" + (f" ({f['where']})" if f["where"] not in ("body",) else "")
        out.append(f"| {f['id']} | {f['class']} | {f['rule']} | `{loc}` | `{match}` | {snippet} |")
    return "\n".join(out) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("--root", default=str(ROOT))
    parser.add_argument("--policy", help="файл политики (по умолчанию — из --root)")
    parser.add_argument("--json", help="записать реестр нарушений в JSON")
    parser.add_argument("--md", help="записать реестр нарушений в Markdown")
    parser.add_argument("--title", default="Аудит чистоты промптов")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)
    auditor = Auditor(Path(args.root), load_policy(args.policy) if args.policy else None)
    findings = auditor.run()
    text = summary(findings, auditor.files)
    if args.json:
        Path(args.json).write_text(json.dumps({"runtime_sha": auditor.sha, "files": auditor.files,
                                               "findings": findings}, ensure_ascii=False, indent=1) + "\n",
                                   encoding="utf-8")
    if args.md:
        Path(args.md).write_text(to_markdown(findings, auditor.files, args.title), encoding="utf-8")
    if not args.quiet:
        print(text)
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
