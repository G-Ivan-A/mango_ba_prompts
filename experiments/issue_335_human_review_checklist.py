#!/usr/bin/env python3
"""Генерация чек-листа Human Review по сноскам отчёта L4 (issue #335).

Скрипт детерминирован: вход — JSON аудита сносок
(``experiments/issue_335_footnote_audit.py --json``) и та же спецификация
hh.ru, закреплённая по SHA-256. Выход — markdown-чек-лист со
классификацией проблем A/B/C/D из комментария к issue #335.

Запуск:
    python3 experiments/issue_335_footnote_audit.py --spec /tmp/hh-openapi.yaml \
        --json /tmp/audit.json
    python3 experiments/issue_335_human_review_checklist.py --audit /tmp/audit.json \
        --spec /tmp/hh-openapi.yaml \
        --out runs/2026/RUN-0060/outputs/human-review-checklist.md
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import issue_335_footnote_audit as audit

TYPE_TITLES = {
    "A": "Тип A — ссылка ведёт на неверный объект",
    "B": "Тип B — ссылка верна, но объект требует дополнительной навигации",
    "C": "Тип C — объект найден, но описан недостаточно",
    "D": "Тип D — объект не найден в документации (GAP SSOT)",
    "OK": "Без замечаний — ссылка ведёт прямо на описанный объект",
}

# Приоритет классификации: чем меньше индекс, тем «тяжелее» проблема.
ORDER = ["A", "D", "C", "B", "OK"]


def classify(problems: list[str]) -> str:
    kinds = set()
    for problem in problems:
        head = problem.split(":", 1)[0]
        if head in {"anchor-not-operation", "anchor-unknown-operation"}:
            kinds.add("A")
        elif head in {"field-not-found", "unknown-identifier", "unknown-field"}:
            kinds.add("D")
        elif head in {"only-in-description", "field-not-located", "enum-not-found"}:
            kinds.add("C")
        elif head in {"schema-only-footnote", "title-differs"}:
            kinds.add("B")
    for kind in ORDER:
        if kind in kinds:
            return kind
    return "OK"


def explain(row: dict, spec: dict) -> tuple[str, str]:
    """Возвращает (что видит человек по ссылке, рекомендуемое исправление)."""
    problems = row["problems"]
    titles = row.get("schema_titles") or {}
    tag = row.get("anchor_tag") or "—"
    operation = row.get("anchor_operation")

    renamed = [
        f"`{name}` отображается как «{title}»"
        for name, title in sorted(titles.items())
        if title and title != name
    ]
    missing_fields = [
        problem.split(":", 1)[1]
        for problem in problems
        if problem.startswith(("field-not-located:", "field-not-found:", "only-in-description:"))
    ]

    seen: list[str] = []
    if any(problem == "schema-only-footnote" for problem in problems):
        seen.append(
            "на странице операции нет заголовка с именем схемы: схема раскрывается "
            "только внутри блока Callbacks/Responses"
        )
    if renamed:
        seen.append("Redoc печатает `title` схемы, а не её имя: " + "; ".join(renamed))
    if missing_fields:
        seen.append(
            "сноска не называет схему-владельца для "
            + ", ".join(f"`{field}`" for field in sorted(set(missing_fields)))
            + ": на странице операции поле приходится искать вручную"
        )
    if any(problem == "anchor-not-operation" for problem in problems):
        seen.append("якорь указывает на подраздел тега, а не на операцию")
    if not seen:
        seen.append("описанный объект виден на странице ссылки без дополнительных шагов")

    fix: list[str] = []
    if any(problem == "anchor-not-operation" for problem in problems):
        fix.append("заменить якорь на `#tag/<tag>/operation/<operationId>`")
    if renamed or any(problem == "schema-only-footnote" for problem in problems):
        path = f"раздел «{tag}»" + (f" → операция `{operation}`" if operation else "")
        labels = ", ".join(f"«{title}»" for title in sorted(set(titles.values())) if title)
        fix.append(
            "правило 3: указать путь навигации — "
            + path
            + (f" → блок с заголовком {labels}" if labels else "")
        )
    for field in sorted(set(missing_fields)):
        leaf = field.rstrip("]").split(".")[-1].split("[")[0]
        owners = sorted(
            name for name, item in spec["schemas"].items() if leaf in item["properties"]
        )
        if len(owners) == 1:
            owner = owners[0]
            line = spec["schemas"][owner]["line"]
            fix.append(
                f"поле `{field}` объявлено только в `components.schemas.{owner}` "
                f"(строка {line} спецификации) — процитировать эту схему"
            )
        elif owners:
            fix.append(
                f"поле `{field}` объявлено в {len(owners)} схемах спецификации и ни "
                "в одной из названных в сноске — указать схему-владельца явно"
            )
        else:
            fix.append(
                f"поле `{field}` отсутствует в структурах спецификации — "
                "пометить как GAP SSOT"
            )
    if not fix:
        fix.append("исправление не требуется")
    return "; ".join(seen), "; ".join(fix)


def render(data: dict, spec: dict) -> str:
    rows = data["rows"]
    for row in rows:
        row["type"] = classify(row["problems"])
        row["seen"], row["fix"] = explain(row, spec)

    counts = {kind: sum(1 for row in rows if row["type"] == kind) for kind in ORDER}
    lines: list[str] = []
    add = lines.append

    add("---")
    add("status: draft")
    add("version: 0.1")
    add("updated: 2026-08-28")
    add("ai-generated: true")
    add("type: artifact")
    add("scope: mango-only")
    add("related_issues:")
    add('  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/335"')
    add("related_artifacts:")
    add('  - "runs/2026/RUN-0060/outputs/L4-combined-gap-report.md"')
    add('  - "docs/analysis/2026-08-28-human-review-accessibility.md"')
    add('  - "experiments/issue_335_footnote_audit.py"')
    add('  - "experiments/issue_335_human_review_checklist.py"')
    add("---")
    add("")
    add("# Чек-лист Human Review: проверка сносок отчёта L4 (RUN-0060)")
    add("")
    add(
        "Проверочный вопрос для каждой сноски: **увидит ли человек, перешедший "
        "по ссылке без дополнительных знаний об API, именно тот объект, который "
        "описан в сноске?**"
    )
    add("")
    add("## 1. Условия проверки")
    add("")
    add(f"- Спецификация: <{data['spec_url']}>")
    add(f"- SHA-256: `{data['sha256']}`")
    add(
        "- Совпадает с SHA-256, закреплённым в отчёте L4: "
        + ("**да**" if data["sha256_matches_pinned"] else "**нет**")
    )
    add(f"- Проиндексировано схем: {data['schemas_indexed']}, операций: {data['operations_indexed']}")
    add(f"- Проверено сносок: **{data['footnotes']}**")
    add("- Инструмент: `experiments/issue_335_footnote_audit.py` (только stdlib)")
    add("")
    add("Воспроизведение:")
    add("")
    add("```bash")
    add("python3 experiments/issue_335_footnote_audit.py --download --json /tmp/audit.json")
    add("python3 experiments/issue_335_human_review_checklist.py --audit /tmp/audit.json \\")
    add("    --out runs/2026/RUN-0060/outputs/human-review-checklist.md")
    add("```")
    add("")
    add("## 2. Итог по классам проблем")
    add("")
    add("| Класс | Определение | Сносок |")
    add("| --- | --- | --- |")
    for kind in ORDER:
        add(f"| {kind} | {TYPE_TITLES[kind]} | {counts[kind]} |")
    add(f"| **Итого** | | **{len(rows)}** |")
    add("")
    add(
        "Ключевой механический факт, объясняющий большинство замечаний класса B: "
        "Redoc выводит в заголовке блока значение `title` схемы, а не её имя в "
        "`components.schemas`. Спецификация hh.ru объявляет `x-tagGroups`, поэтому "
        "раздел Schemas в Redoc не отображается и якорей на схемы не существует — "
        "правило «якорь на дочерний элемент» технически недостижимо, применяется "
        "правило 3 (явный путь навигации) плюс цитата из спецификации, "
        "закреплённой по SHA-256."
    )
    add("")
    add("## 3. Полный чек-лист (53 сноски)")
    add("")
    add("| № | Раздел | Сноска | Что описывает сноска | Что видно по ссылке | Класс | Рекомендация |")
    add("| --- | --- | --- | --- | --- | --- | --- |")
    for index, row in enumerate(rows, start=1):
        description = row["description"].replace("|", "\\|")
        add(
            f"| {index} | {row['section']} | `^{row['marker']}` | {description} | "
            f"{row['seen']} | {row['type']} | {row['fix']} |"
        )
    add("")
    add("## 4. Выводы для стандарта")
    add("")
    add(
        "1. Ссылка на операцию Redoc проверяема машинно: `operationId` обязан "
        "присутствовать в спецификации с зафиксированным SHA-256."
    )
    add(
        "2. Ссылка на схему в Redoc непроверяема и человеку не помогает: у схем нет "
        "якорей. Сноска, описывающая схему, обязана содержать путь навигации и "
        "цитату `components.schemas.<Имя>` со строкой спецификации."
    )
    add(
        "3. Имя схемы нельзя использовать как ориентир для человека: в интерфейсе "
        "видно `title`. Сноска обязана приводить отображаемый заголовок."
    )
    add(
        "4. Поле, отсутствующее в структурах спецификации (например "
        "`X-Manager-Account-Id`, упомянутый только в текстовых описаниях), "
        "фиксируется как GAP SSOT, а не как проверенный факт."
    )
    add("")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit", default="/tmp/audit.json")
    parser.add_argument("--spec", default="/tmp/hh-openapi.yaml")
    parser.add_argument("--out", default="runs/2026/RUN-0060/outputs/human-review-checklist.md")
    args = parser.parse_args()

    data = json.loads(Path(args.audit).read_text(encoding="utf-8"))
    spec = audit.build_index(Path(args.spec).read_text(encoding="utf-8"))
    Path(args.out).write_text(render(data, spec), encoding="utf-8")
    print(f"записано: {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
