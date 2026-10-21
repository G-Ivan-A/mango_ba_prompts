#!/usr/bin/env python3
"""Итоговые промпты разделов BCREQ-ФТ по RUN-0073…RUN-0076 (issue #377, PR #380).

Зачем
-----
Дополнительное задание к PR #380: по прогонам RUN-0073…RUN-0076 сформулировать
три промпта генерации разделов (а) 1, 2; б) 3, 5; в) 4, 6) и промпт GitHub issue
на сбор golden set. Результат — `docs/analysis/2026-10-20-bcreq-fr-section-prompts.md`.
Валидатор проверяет, что файл не разошёлся с данными и с собственными правилами:

1. контракт Analysis (`standards/analysis-standard.md`): frontmatter `status`,
   `version`, `updated`, `temperature`, `source`, `scope`, `analysis-subtype` из
   словаря стандарта, без `ai-generated`; имя файла `YYYY-MM-DD-*.md`; секции
   Summary / BLUF, Context / Scope, Findings, Recommendations, Related Artifacts;
2. блоки `<!-- section-prompts:common|a|b|c|issue -->` есть, в каждом ровно
   один блок кода;
3. общая часть входит в промпты а), б), в) дословно;
4. каждое правило `RULES` скрипта статистики есть в своём промпте (или в таблице
   правил П), и в промптах нет меток правил, которых нет в `RULES`;
5. в роли промптов нет названий методологий (правило П1);
6. таблицы статистики в файле совпадают с выводом
   `experiments/issue_377_cross_run_stats.py`, а `cross-run-stats.json` — с данными
   (скрипт сам проверяет ссылки правил на источники и покрытие категорий).

Запуск: ``python3 scripts/validate_issue_377_section_prompts.py``
"""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATS = ROOT / "experiments" / "issue_377_cross_run_stats.py"
BLOCKS = ("common", "a", "b", "c", "issue")
PROMPTS = ("a", "b", "c")
BLOCK = re.compile(r"<!-- section-prompts:(\w+) -->\n(.*?)<!-- /section-prompts:\1 -->", re.S)
FENCE = re.compile(r"^```(\w*)\n(.*?)^```$", re.S | re.M)
RULE_LABEL = re.compile(r"^([ОАБВ]\d+(?:\.\d+)?)\. ", re.M)
SUBTYPES = ("inventory", "matrix", "options", "recommendation")
SECTIONS = ("Summary / BLUF", "Context / Scope", "Findings", "Recommendations", "Related Artifacts")
METHODOLOGIES = ("TM Forum", "eTOM", "ODA", "BABOK", "OpenAPI", "архитектор")


def load_stats():
    spec = importlib.util.spec_from_file_location("issue_377_cross_run_stats", STATS)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def frontmatter(text: str) -> dict[str, str]:
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    return dict(re.findall(r"^([\w-]+):\s*(.*)$", m.group(1), re.M))


def check_frontmatter(doc: Path, text: str) -> list[str]:
    errors = []
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}-[a-z0-9-]+\.md", doc.name):
        errors.append(f"{doc.name}: имя не по шаблону YYYY-MM-DD-name.md")
    fm = frontmatter(text)
    for key in ("status", "version", "updated", "temperature", "source", "scope", "analysis-subtype"):
        if not fm.get(key):
            errors.append(f"frontmatter: нет поля {key}")
    if fm.get("analysis-subtype") and fm["analysis-subtype"] not in SUBTYPES:
        errors.append(f"frontmatter: analysis-subtype={fm['analysis-subtype']!r} вне словаря {SUBTYPES}")
    if "ai-generated" in fm:
        errors.append("frontmatter: ai-generated запрещён стандартом Analysis")
    headings = re.findall(r"^## (.+)$", text, re.M)
    for section in SECTIONS:
        if not any(section in h for h in headings):
            errors.append(f"нет секции «{section}» (standards/analysis-standard.md)")
    if headings and "Summary / BLUF" not in headings[0]:
        errors.append("первая секция — не Summary / BLUF")
    return errors


def prompt_blocks(text: str) -> tuple[dict[str, str], list[str]]:
    errors, blocks = [], {}
    found = {}
    for name, body in BLOCK.findall(text):
        if name in found:
            errors.append(f"блок section-prompts:{name} повторяется")
        found[name] = body
    for name in BLOCKS:
        if name not in found:
            errors.append(f"нет блока section-prompts:{name}")
            continue
        fences = FENCE.findall(found[name])
        if len(fences) != 1:
            errors.append(f"блок section-prompts:{name}: блоков кода {len(fences)}, нужен 1")
            continue
        blocks[name] = fences[0][1]
    return blocks, errors


def check_prompts(blocks: dict[str, str], rules: dict[str, dict], text: str) -> list[str]:
    errors = []
    common = blocks.get("common", "")
    for name in PROMPTS:
        if name in blocks and common and common not in blocks[name]:
            errors.append(f"промпт {name}): общая часть не входит дословно")
    design = re.search(r"^### 5\.5\..*?(?=^## )", text, re.S | re.M)
    design = design.group(0) if design else ""
    if not design:
        errors.append("нет раздела «### 5.5.» с правилами П")
    expected = {"common": set(), "a": set(), "b": set(), "c": set()}
    for rid, rule in rules.items():
        if rule["prompt"] == "design":
            if design and not re.search(rf"^\| {re.escape(rid)} \|", design, re.M):
                errors.append(f"правило {rid}: нет строки в таблице правил П (§5.5)")
            continue
        expected[rule["prompt"]].add(rid)
    for name, ids in expected.items():
        if name not in blocks:
            continue
        body = blocks[name]
        if name != "common":
            body = body.replace(common, "")
        labels = RULE_LABEL.findall(body)
        dup = sorted({x for x in labels if labels.count(x) > 1})
        if dup:
            errors.append(f"промпт {name}: метки правил повторяются {dup}")
        missing, extra = sorted(ids - set(labels)), sorted(set(labels) - ids)
        if missing:
            errors.append(f"промпт {name}: нет правил {missing}")
        if extra:
            errors.append(f"промпт {name}: правила вне RULES скрипта {extra}")
    for name in PROMPTS + ("common",):
        role = re.search(r"# РОЛЬ\n(.*?)\n\n", blocks.get(name, "") + "\n\n", re.S)
        if not role:
            errors.append(f"промпт {name}: нет раздела «# РОЛЬ»")
            continue
        named = [m for m in METHODOLOGIES if m in role.group(1)]
        if named:
            errors.append(f"промпт {name}: в роли методология / экспертиза {named} (П1)")
    return errors


def check_stats(stats, text: str) -> list[str]:
    errors = []
    try:
        data, tables = stats.build_all()
    except ValueError as exc:
        return [f"скрипт статистики: {exc}"]
    new, missing = stats.apply_doc(text, tables)
    if missing:
        errors.append(f"нет блоков cross-run-stats: {missing}")
    elif new != text:
        errors.append("таблицы статистики устарели: python3 experiments/issue_377_cross_run_stats.py --write-doc")
    expected = json.loads(json.dumps(data, ensure_ascii=False))
    if not stats.OUT.exists():
        errors.append(f"нет {stats.OUT.relative_to(ROOT)}")
    elif json.loads(stats.OUT.read_text(encoding="utf-8")) != expected:
        errors.append(f"{stats.OUT.relative_to(ROOT)} устарел: python3 experiments/issue_377_cross_run_stats.py")
    return errors


def main() -> int:
    stats = load_stats()
    doc = stats.DOC
    if not doc.exists():
        print(f"FAIL: нет {doc.relative_to(ROOT)}")
        return 1
    text = doc.read_text(encoding="utf-8")
    blocks, errors = prompt_blocks(text)
    errors += check_frontmatter(doc, text)
    errors += check_prompts(blocks, stats.RULES, text)
    errors += check_stats(stats, text)
    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        return 1
    print(f"OK: {doc.relative_to(ROOT)} — промпты а)–в), общая часть, {len(stats.RULES)} правил, "
          "таблицы статистики и cross-run-stats.json согласованы")
    return 0


if __name__ == "__main__":
    sys.exit(main())
