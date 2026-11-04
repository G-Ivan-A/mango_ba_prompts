#!/usr/bin/env python3
"""Проверка готовности BL-163 на клоне runtime (issue #442).

Запуск::

    python3 -I experiments/issue_442/runtime_readiness.py <клон runtime> [SHA]

Что проверяется (всё — фактами клона и спицы, без сети):

1. HEAD клона равен SHA-кандидату нового среза реестра.
2. Все пути раздела 2 реестра ``standards/bcreq-runtime-references.md`` и
   каталог ``taxonomy/mango-products.yaml`` существуют на SHA (ТС-2).
3. Поля версии справочников (ТС-3).
4. Что изменилось в runtime между старым срезом реестра и кандидатом
   (``git diff --stat``): факты столбца «Есть в runtime» вне каталога не
   меняются, если файлы не менялись.
5. Каталог runtime против каталога спицы:
   * ``closed: true``, число узлов, ``source_sha256`` против
     ``git show <source_commit>:docs/taxonomy/products.json``;
   * id, уровень, родители — против текущего ``docs/taxonomy/products.json``;
   * расхождение lifecycle/status (PR #440) — печатается отдельно, не ошибка.

Код выхода 0 — все обязательные проверки прошли.
"""

import collections
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "standards/bcreq-runtime-references.md"
CATALOG = ROOT / "docs/taxonomy/products.json"
OLD_SHA = "5d8c201511fd730a596c9f9b4588470a7b01edc9"
LEVEL = {"Domain": "domain", "Capability": "capability", "Feature": "feature", "Atomic Function": "function"}
NODE = re.compile(r"^  - \{id: \"([^\"]+)\", level: (\w+), .*?parents: \[([^\]]*)\], classes: \[([^\]]*)\], lifecycle: ([\w-]+)")
LINK = re.compile(r"mango-ba-ai-runtime/(?:blob|tree)/[0-9a-f]{40}/([^)`\s]+)")

failures = []


def check(ok, message):
    print(("OK   " if ok else "FAIL ") + message)
    if not ok:
        failures.append(message)


def git(clone, *args):
    return subprocess.run(["git", "-C", str(clone), *args], capture_output=True, text=True, check=True).stdout


def section2_paths():
    body = REGISTRY.read_text(encoding="utf-8")
    part = body.split("## 2. Перечень", 1)[1].split("\n## 3.", 1)[0]
    return sorted(set(LINK.findall(part)))


def parse_catalog(path):
    head, nodes = {}, {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = NODE.match(line)
        if match:
            node_id, level, parents, classes, lifecycle = match.groups()
            split = lambda s: [x.strip().strip('"') for x in s.split(",") if x.strip()]
            nodes[node_id] = {"level": level, "parents": split(parents), "classes": split(classes), "lifecycle": lifecycle}
        elif re.match(r"^[a-z_0-9]+: ", line):
            key, value = line.split(": ", 1)
            head[key] = value.strip().strip('"')
    return head, nodes


def main():
    clone = Path(sys.argv[1]).resolve()
    sha = sys.argv[2] if len(sys.argv) > 2 else git(clone, "rev-parse", "HEAD").strip()
    head = git(clone, "rev-parse", "HEAD").strip()
    print(f"# runtime clone {clone}\n# HEAD {head}\n# candidate {sha}\n")
    check(head == sha, f"HEAD клона = кандидат {sha}")
    print("\n## commit\n" + git(clone, "log", "-1", "--format=%H %cI %s"))

    print("## 2. пути раздела 2 реестра + каталог (ТС-2)")
    paths = section2_paths() + ["taxonomy/mango-products.yaml"]
    for rel in paths:
        check((clone / rel).exists(), f"путь {rel}")

    print("\n## 3. версии (ТС-3)")
    for rel in ("taxonomy/products.yaml", "taxonomy/domain-glossary.yaml", "golden/cases.yaml",
                "taxonomy/source-tiers.yaml", "evaluation/g-human-checklist.md", "taxonomy/mango-products.yaml"):
        found = re.search(r"(?m)^version: *(.+)$", (clone / rel).read_text(encoding="utf-8"))
        check(bool(found), f"{rel}: version = {found.group(1) if found else '—'}")
    kb_map = json.loads((clone / "docs/kb/MAP.json").read_text(encoding="utf-8"))
    check("schema_version" in kb_map, f"docs/kb/MAP.json: schema_version = {kb_map.get('schema_version')}")

    print(f"\n## 4. изменения runtime {OLD_SHA[:7]}..{sha[:7]}")
    print(git(clone, "diff", "--stat", OLD_SHA, sha))
    changed = set(git(clone, "diff", "--name-only", OLD_SHA, sha).split())
    untouched = [p for p in section2_paths() if not any(c == p or c.startswith(p.rstrip("/") + "/") for c in changed)]
    check(untouched == section2_paths(), "файлы раздела 2 не менялись — факты столбца «Есть в runtime» прежние")

    print("\n## 5. каталог runtime против каталога спицы")
    rt_head, rt_nodes = parse_catalog(clone / "taxonomy/mango-products.yaml")
    text = (clone / "taxonomy/mango-products.yaml").read_text(encoding="utf-8")
    check(re.search(r"(?m)^closed: true$", text) is not None, "closed: true")
    check(text.count("\n  - {id: ") == len(rt_nodes), f"каждая строка узла разобрана ({len(rt_nodes)})")
    source_commit = rt_head["source_commit"]
    blob = subprocess.run(["git", "-C", str(ROOT), "show", f"{source_commit}:docs/taxonomy/products.json"],
                          capture_output=True, check=True).stdout
    digest = hashlib.sha256(blob).hexdigest()
    check(digest == rt_head["source_sha256"], f"source_sha256 {rt_head['source_sha256'][:12]}… = sha256(спица@{source_commit[:7]}) {digest[:12]}…")
    spoke = json.loads(CATALOG.read_text(encoding="utf-8"))
    current = hashlib.sha256(CATALOG.read_bytes()).hexdigest()
    print(f"     sha256 текущего docs/taxonomy/products.json = {current[:12]}… ({'= источник' if current == digest else 'ДРЕЙФ от источника'})")
    sp_nodes = {n["id"]: n for n in spoke["nodes"]}
    check(len(rt_nodes) == len(sp_nodes) == 353, f"узлов: runtime {len(rt_nodes)}, спица {len(sp_nodes)}")
    check(set(rt_nodes) == set(sp_nodes), "множества id совпадают")
    bad = [i for i in sp_nodes if i in rt_nodes and (
        LEVEL[sp_nodes[i]["level"]] != rt_nodes[i]["level"]
        or sorted(sp_nodes[i]["parent_ids"]) != sorted(rt_nodes[i]["parents"]))]
    check(not bad, f"уровень и родители совпадают (расхождений {len(bad)})")
    print("     уровни runtime:", dict(collections.Counter(n["level"] for n in rt_nodes.values())))
    per_class = collections.Counter(c for n in rt_nodes.values() if n["level"] == "function" for c in n["classes"])
    print("     функции по классам runtime:", dict(per_class),
          "без класса:", sum(1 for n in rt_nodes.values() if n["level"] == "function" and not n["classes"]))
    params = text.count("params: []")
    print(f"     функций с params: [] — {params}")
    drift = collections.Counter((rt_nodes[i]["lifecycle"], sp_nodes[i]["lifecycle"]) for i in sp_nodes
                                if i in rt_nodes and rt_nodes[i]["lifecycle"] != sp_nodes[i]["lifecycle"])
    print(f"     catalog_status runtime {rt_head.get('catalog_status')}, status спицы {spoke['status']}")
    print(f"     дрейф lifecycle (runtime → спица): {dict(drift) or 'нет'}")

    print(f"\n# итог: {'готово' if not failures else 'НЕ готово: ' + '; '.join(failures)}")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
