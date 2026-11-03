#!/usr/bin/env python3
"""Прототип компиляции каталога продуктов спицы в форму runtime (issue #434, РТ-1).

Что делает:

* читает каталог значений спицы ``docs/taxonomy/products.json``;
* считает для каждого узла множество продуктовых классов runtime
  (``contact-center``, ``voice-ucaas``, ``analytics-reporting``) через предков
  уровня Domain и таблицу ``runtime_compatibility`` каталога;
* печатает статистику (уровни, классы, lifecycle, binding_basis) — эти числа
  цитирует RFC ``docs/rfc/2026-11-runtime-catalog-golden-set-tasks.md``;
* пишет черновик файла runtime ``taxonomy/product-catalog.yaml`` в
  ``experiments/issue_434/prototype/`` — образец формы для исполнителя РТ-1.

Прототип живёт в спице: в runtime файлы ``.py`` запрещены
(``tests/runtime-smoke.sh``), а нормативное содержание runtime правится только
компиляцией (правило 13 ``AGENTS.md`` runtime). YAML пишется без зависимостей:
строки в двойных кавычках JSON — допустимый YAML 1.2.

Запуск: ``python3 experiments/issue_434/compile_catalog_prototype.py [--write]``.
"""

import argparse
import collections
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "docs/taxonomy/products.json"
OUT = Path(__file__).resolve().parent / "prototype/product-catalog.yaml"
RUNTIME_CLASSES = ("contact-center", "voice-ucaas", "analytics-reporting")
LEVEL_KEY = {
    "Domain": "domain",
    "Capability": "capability",
    "Feature": "feature",
    "Atomic Function": "function",
}


def q(value):
    return json.dumps(value, ensure_ascii=False)


def source_commit():
    out = subprocess.run(
        ["git", "log", "-1", "--format=%H", "--", str(SOURCE.relative_to(ROOT))],
        cwd=ROOT, capture_output=True, text=True,
    )
    return out.stdout.strip()


def load():
    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    nodes = {n["id"]: n for n in data["nodes"]}
    compat = data["runtime_compatibility"]
    domain_to_class = {compat[c]: c for c in RUNTIME_CLASSES}
    return data, nodes, domain_to_class


def domains_of(node_id, nodes, memo):
    if node_id in memo:
        return memo[node_id]
    node = nodes[node_id]
    if node["level"] == "Domain":
        result = {node_id}
    else:
        result = set()
        for parent in node["parent_ids"]:
            result |= domains_of(parent, nodes, memo)
    memo[node_id] = result
    return result


def stats(data, nodes, domain_to_class):
    memo = {}
    per_level = collections.Counter(n["level"] for n in nodes.values())
    per_class = {c: collections.Counter() for c in RUNTIME_CLASSES}
    af_lifecycle = {c: collections.Counter() for c in RUNTIME_CLASSES}
    no_class = collections.Counter()
    for node in nodes.values():
        classes = sorted(domain_to_class[d] for d in domains_of(node["id"], nodes, memo) if d in domain_to_class)
        node["_classes"] = classes
        if not classes:
            no_class[node["level"]] += 1
        for c in classes:
            per_class[c][node["level"]] += 1
            if node["level"] == "Atomic Function":
                af_lifecycle[c][node["lifecycle"]] += 1
    afs = [n for n in nodes.values() if n["level"] == "Atomic Function"]
    feats = [n for n in nodes.values() if n["level"] == "Feature"]
    caps = [n for n in nodes.values() if n["level"] == "Capability"]
    has_cyr = lambda s: any("а" <= ch.lower() <= "я" or ch.lower() == "ё" for ch in s)
    return {
        "source": str(SOURCE.relative_to(ROOT)),
        "source_commit": source_commit(),
        "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "catalog_version": data["catalog_version"],
        "status": data["status"],
        "nodes_total": len(nodes),
        "per_level": dict(per_level),
        "per_class": {c: dict(v) for c, v in per_class.items()},
        "af_lifecycle_per_class": {c: dict(v) for c, v in af_lifecycle.items()},
        "outside_runtime_classes": dict(no_class),
        "af_lifecycle": dict(collections.Counter(n["lifecycle"] for n in afs)),
        "af_binding_basis": dict(collections.Counter(n.get("binding_basis") for n in afs)),
        "af_parent_count": dict(collections.Counter(len(n["parent_ids"]) for n in afs)),
        "af_multi_class": sum(1 for n in afs if len(n["_classes"]) > 1),
        "af_cyrillic_name": sum(1 for n in afs if has_cyr(n["name"])),
        "feature_cyrillic_name": sum(1 for n in feats if has_cyr(n["name"])),
        "capability_cyrillic_name": sum(1 for n in caps if has_cyr(n["name"])),
        "availability": dict(collections.Counter(n["availability"] for n in nodes.values())),
    }


def render(data, nodes, summary):
    lines = [
        "# Закрытый каталог значений продуктовой таксономии (уровни Domain …",
        "# Atomic Function). Форма уровней — taxonomy/products.yaml; значения",
        "# скопированы из каталога спицы без изменения смысла (манифест: copied).",
        "# Файл — факты (ТС-4 RFC #427): правило привязки atomic_function",
        "# объявлено в contracts/c-in.md, а не здесь. classes — продуктовые",
        "# классы products.yaml, к которым узел относится через предков Domain.",
        "vocabulary: product-catalog",
        "closed: true",
        'version: "1.0"',
        f"catalog_version: {q(data['catalog_version'])}",
        f"catalog_status: {q(data['status'])}",
        "source: https://github.com/G-Ivan-A/mango_ba_prompts/blob/"
        f"{summary['source_commit']}/docs/taxonomy/products.json",
        f"source_commit: {q(summary['source_commit'])}",
        f"source_sha256: {summary['source_sha256']}",
        "class_domains:",
    ]
    compat = data["runtime_compatibility"]
    for c in RUNTIME_CLASSES:
        lines.append(f"  {c}: {compat[c]}")
    lines.append("nodes:")
    order = {"Domain": 0, "Capability": 1, "Feature": 2, "Atomic Function": 3}
    for node in sorted(nodes.values(), key=lambda n: (order[n["level"]], n["id"])):
        parts = [
            f"id: {q(node['id'])}",
            f"level: {LEVEL_KEY[node['level']]}",
            f"name: {q(node['name'])}",
            f"parents: {q(node['parent_ids'])}",
            f"classes: {q(node['_classes'])}",
            f"lifecycle: {node['lifecycle']}",
        ]
        if node.get("params"):
            parts.append(f"params: {q(node['params'])}")
        if node.get("locator"):
            parts.append(f"locator: {q(node['locator'])}")
        if node.get("binding_basis"):
            parts.append(f"binding_basis: {node['binding_basis']}")
        lines.append("  - {" + ", ".join(parts) + "}")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="записать черновик YAML")
    args = parser.parse_args()
    data, nodes, domain_to_class = load()
    summary = stats(data, nodes, domain_to_class)
    body = render(data, nodes, summary)
    summary["prototype_yaml_bytes"] = len(body.encode("utf-8"))
    summary["prototype_yaml_lines"] = body.count("\n")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if args.write:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(body, encoding="utf-8")
        print(f"written: {OUT.relative_to(ROOT)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
