#!/usr/bin/env python3
"""Проверка готовности среза реестра 0.4 и BL-156 на клоне runtime (issue #444).

Запуск::

    python3 -I experiments/issue_444/runtime_readiness.py <клон runtime> [SHA]

Основа — experiments/issue_442/runtime_readiness.py (BL-163); добавлено то,
что внесла runtime PR #21 (РТ-6, РТ-4, РТ-3, компиляция ХАБ-1):

1. HEAD клона равен SHA-кандидату нового среза.
2. Пути раздела 2 реестра и новые пути И-5, И-6 существуют (ТС-2).
3. Поля версии всех справочников среза (ТС-3).
4. Что изменилось в runtime между срезом 0.3 (``2db0ef51``) и кандидатом.
5. Каталог runtime против каталога спицы: ``source_sha256`` = sha256 спицы на
   ``source_commit``, id/уровни/родители 353 узлов, lifecycle — без дрейфа
   (РТ-6 снимает расхождение раздела 2.1 реестра).
6. Golden set трёх классов (РТ-3): у каждого случая ``atomic_function`` —
   id функции каталога, в ``classes`` которой есть класс набора (строгая форма
   PR #21: без маркеров-исключений); ``declared_function`` — вне каталога или
   чужого класса по ``catalog_check``; ``structural_only`` и ``confirmed_by``
   печатаются — это факт для BL-156 («не хуже» = структурная сверка).
7. Глоссарии РТ-4: словарь не пуст, пары ``confusable_with`` есть (источник
   отрицательных случаев); пара вне словаря печатается как термин-подмена
   (допустимо), узлы ``catalog`` есть в каталоге.

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
OLD_SHA = "2db0ef5106883b01b096fe8c4af50334899e9fe0"
LEVEL = {"Domain": "domain", "Capability": "capability", "Feature": "feature", "Atomic Function": "function"}
NODE = re.compile(r"^  - \{id: \"([^\"]+)\", level: (\w+), .*?parents: \[([^\]]*)\], classes: \[([^\]]*)\], lifecycle: ([\w-]+)")
LINK = re.compile(r"mango-ba-ai-runtime/(?:blob|tree)/[0-9a-f]{40}/([^)`\s]+)")
GOLDEN = {
    "contact-center": "golden/cases.yaml",
    "voice-ucaas": "golden/cases-voice-ucaas.yaml",
    "analytics-reporting": "golden/cases-analytics-reporting.yaml",
}
GLOSSARY = {
    "contact-center": "taxonomy/domain-glossary.yaml",
    "voice-ucaas": "taxonomy/domain-glossary-voice-ucaas.yaml",
    "analytics-reporting": "taxonomy/domain-glossary-analytics-reporting.yaml",
}

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
            head[key] = value.split("#", 1)[0].strip().strip('"')
    return head, nodes


def parse_cases(text):
    """Плоский разбор списка cases: поля верхнего уровня каждого случая."""
    cases, cur = [], None
    for line in text.splitlines():
        start = re.match(r"^  - id: (\S+)", line)
        if start:
            cur = {"id": start.group(1)}
            cases.append(cur)
            continue
        field = re.match(r"^    ([a-z_]+): (.+?)\s*(?:#.*)?$", line)
        if cur is not None and field:
            cur[field.group(1)] = field.group(2).strip().strip('"')
    return cases


def main():
    clone = Path(sys.argv[1]).resolve()
    sha = sys.argv[2] if len(sys.argv) > 2 else git(clone, "rev-parse", "HEAD").strip()
    head = git(clone, "rev-parse", "HEAD").strip()
    print(f"# runtime clone {clone}\n# HEAD {head}\n# candidate {sha}\n")
    check(head == sha, f"HEAD клона = кандидат {sha}")
    print("\n## commit\n" + git(clone, "log", "-1", "--format=%H %cI %s"))

    print("## 2. пути раздела 2 реестра, И-5, И-6 и каталог (ТС-2)")
    paths = sorted(set(section2_paths()) | set(GOLDEN.values()) | set(GLOSSARY.values()) | {"taxonomy/mango-products.yaml"})
    for rel in paths:
        check((clone / rel).exists(), f"путь {rel}")

    print("\n## 3. версии (ТС-3)")
    for rel in ("taxonomy/products.yaml", "taxonomy/mango-products.yaml", "taxonomy/source-tiers.yaml",
                "evaluation/g-human-checklist.md", *GOLDEN.values(), *GLOSSARY.values()):
        found = re.search(r"(?m)^version: *(.+)$", (clone / rel).read_text(encoding="utf-8"))
        check(bool(found), f"{rel}: version = {found.group(1).strip() if found else '—'}")
    kb_map = json.loads((clone / "docs/kb/MAP.json").read_text(encoding="utf-8"))
    check("schema_version" in kb_map, f"docs/kb/MAP.json: schema_version = {kb_map.get('schema_version')}")

    print(f"\n## 4. изменения runtime {OLD_SHA[:7]}..{sha[:7]}")
    print(git(clone, "diff", "--stat", OLD_SHA, sha))
    changed = set(git(clone, "diff", "--name-only", OLD_SHA, sha).split())
    for p in section2_paths():
        hit = any(c == p or c.startswith(p.rstrip("/") + "/") for c in changed)
        print(f"     раздел 2: {p} — {'ИЗМЕНЁН' if hit else 'не менялся'}")
    kb_changed = sorted(c for c in changed if c.startswith("docs/kb/") and "__pycache__" not in c)
    check(not kb_changed, f"база знаний docs/kb не менялась (И-1): {kb_changed or 'нет изменений'}")

    print("\n## 5. каталог runtime против каталога спицы (РТ-6)")
    rt_head, rt_nodes = parse_catalog(clone / "taxonomy/mango-products.yaml")
    text = (clone / "taxonomy/mango-products.yaml").read_text(encoding="utf-8")
    check(re.search(r"(?m)^closed: true$", text) is not None, "closed: true")
    check(text.count("\n  - {id: ") == len(rt_nodes), f"каждая строка узла разобрана ({len(rt_nodes)})")
    source_commit = rt_head["source_commit"]
    blob = subprocess.run(["git", "-C", str(ROOT), "show", f"{source_commit}:docs/taxonomy/products.json"],
                          capture_output=True, check=True).stdout
    digest = hashlib.sha256(blob).hexdigest()
    check(digest == rt_head["source_sha256"], f"source_sha256 {rt_head['source_sha256'][:12]}… = sha256(спица@{source_commit[:7]}) {digest[:12]}…")
    current = hashlib.sha256(CATALOG.read_bytes()).hexdigest()
    check(current == digest, f"текущий docs/taxonomy/products.json {current[:12]}… = источник копии (дрейфа нет)")
    spoke = json.loads(CATALOG.read_text(encoding="utf-8"))
    sp_nodes = {n["id"]: n for n in spoke["nodes"]}
    check(len(rt_nodes) == len(sp_nodes) == 353, f"узлов: runtime {len(rt_nodes)}, спица {len(sp_nodes)}")
    check(set(rt_nodes) == set(sp_nodes), "множества id совпадают")
    bad = [i for i in sp_nodes if i in rt_nodes and (
        LEVEL[sp_nodes[i]["level"]] != rt_nodes[i]["level"]
        or sorted(sp_nodes[i]["parent_ids"]) != sorted(rt_nodes[i]["parents"]))]
    check(not bad, f"уровень и родители совпадают (расхождений {len(bad)})")
    print("     уровни runtime:", dict(collections.Counter(n["level"] for n in rt_nodes.values())))
    drift = collections.Counter((rt_nodes[i]["lifecycle"], sp_nodes[i]["lifecycle"]) for i in sp_nodes
                                if i in rt_nodes and rt_nodes[i]["lifecycle"] != sp_nodes[i]["lifecycle"])
    check(not drift, f"lifecycle без дрейфа (раздел 2.1 реестра снимается): {dict(drift) or 'нет'}")
    check(rt_head.get("catalog_status") == "accepted" and spoke["status"] == "accepted",
          f"catalog_status runtime {rt_head.get('catalog_status')}, status спицы {spoke['status']}")

    print("\n## 6. golden set трёх классов (РТ-3, строгая форма PR #21)")
    functions = {i: n for i, n in rt_nodes.items() if n["level"] == "function"}
    for klass, rel in GOLDEN.items():
        body = (clone / rel).read_text(encoding="utf-8")
        cases = parse_cases(body)
        kinds = collections.Counter(c.get("kind") for c in cases)
        structural = re.search(r"(?m)^structural_only: *(\w+)", body)
        confirmed = collections.Counter(c.get("confirmed_by") for c in cases)
        print(f"     {rel}: {dict(kinds)}; structural_only {structural.group(1) if structural else '—'}; confirmed_by {dict(confirmed)}")
        check(kinds["positive"] >= 2 and kinds["negative"] >= 1, f"{klass}: ≥2 положительных и ≥1 отрицательный")
        for c in cases:
            fn = c.get("atomic_function", "")
            check(c.get("product_class") == klass, f"{c['id']}: product_class = {klass}")
            check(fn in functions and klass in functions[fn]["classes"],
                  f"{c['id']}: atomic_function {fn} — функция каталога класса {klass}")
            if "declared_function" in c:
                decl, kind = c["declared_function"], c.get("catalog_check")
                ok = (kind == "outside-catalog" and decl not in rt_nodes) or (
                    kind == "foreign-class" and decl in functions and klass not in functions[decl]["classes"])
                check(ok, f"{c['id']}: declared_function {decl} — {kind}")

    print("\n## 7. глоссарии (РТ-4)")
    for klass, rel in GLOSSARY.items():
        body = (clone / rel).read_text(encoding="utf-8")
        ids = re.findall(r"(?m)^  - id: (TRM-[A-Z0-9-]+)", body)
        terms = set(re.findall(r"(?m)^    term: (.+?)\s*$", body))
        refs = set(re.findall(r"(?m)^      - term: (.+?)\s*$", body))
        cat = {x.strip().strip('"') for m in re.findall(r"catalog: \[([^\]]*)\]", body) for x in m.split(",") if x.strip()}
        print(f"     {rel}: терминов {len(ids)}, пар confusable_with {len(refs)}, узлов catalog {len(cat)}")
        check(len(ids) > 0, f"{klass}: глоссарий не пуст")
        check(len(refs) > 0, f"{klass}: есть пары confusable_with (источник отрицательных случаев)")
        print(f"     {klass}: пары вне словаря (термин-подмена, допустимо): {sorted(refs - terms) or 'нет'}")
        check(cat <= set(rt_nodes), f"{klass}: узлы catalog есть в каталоге (вне: {sorted(cat - set(rt_nodes)) or 'нет'})")

    print(f"\n# итог: {'готово' if not failures else 'НЕ готово: ' + '; '.join(failures)}")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
