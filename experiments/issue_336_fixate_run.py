#!/usr/bin/env python3
"""Порождение механических артефактов записи RUN-0061 (issue #336).

Скрипт детерминированно строит из двух JSON-замеров:

- ``experiments/issue_336/stats.json`` — вывод
  :mod:`experiments.issue_309_run_stats` по экспорту чата задачи 1090;
- ``experiments/issue_336/link-audit.json`` — вывод
  :mod:`experiments.issue_336_link_audit` по отчёту RUN-0057 и стенограмме.

Порождаются файлы прогона, которые нельзя писать руками без риска расхождения
с замерами:

- ``outputs/prompt-usage.md`` — распределение операций БА, сессии, вложения;
- ``logs/metrics.md`` — метрики по каждой реплике;
- ``logs/link-verification.md`` — журнал проверки ссылок (диалог + отчёт).

Аналитические тексты записи (``outputs/link-review-statistics.md`` и др.)
пишутся руками и этим скриптом не трогаются.

Запуск: ``python3 experiments/issue_336_fixate_run.py``
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "experiments" / "issue_336"
RUN = ROOT / "runs" / "2026" / "RUN-0061"
ISSUE = "https://github.com/G-Ivan-A/mango_ba_prompts/issues/336"
UPDATED = "2026-08-28"

#: Человекочитаемые названия эвристических меток операций БА.
KIND_TITLES = {
    "prompt-engineering": "работа с промптом / инструкцией (`prompt-engineering`)",
    "artifact-generation": "запрос на генерацию артефакта (`artifact-generation`)",
    "validation": "проверка и критика результата (`validation`)",
    "elicitation": "элицитация, уточняющие вопросы (`elicitation`)",
    "iteration": "доработка предыдущего ответа (`iteration`)",
    "context-load": "передача контекста и вложений (`context-load`)",
}

#: Что означает каждый исход сопоставления «раздел из ответа → заголовок страницы».
RESOLUTION_TITLES = {
    "anchor-available": "заголовок найден, якорь существует",
    "page-title-only": "названо заглавие страницы, а не раздел",
    "text-only": "формулировка есть в тексте, но не заголовком",
    "not-found-on-page": "на странице не найдено",
    "no-section-claimed": "раздел не указан",
}


def front_matter(doc_type: str, scope: str, extra: list[str] | None = None) -> str:
    lines = [
        "---",
        "status: draft",
        "version: 0.1",
        f"updated: {UPDATED}",
        "ai-generated: true",
        f"type: {doc_type}",
        f"scope: {scope}",
        "related_issues:",
        f'  - "{ISSUE}"',
    ]
    lines.extend(extra or [])
    lines.append("---")
    return "\n".join(lines) + "\n\n"


def prompt_usage(stats: dict) -> str:
    user_turns = stats["user_turns"]
    out = [
        front_matter(
            "artifact",
            "prompts",
            [
                "related_artifacts:",
                '  - "experiments/issue_336_fixate_run.py"',
            ],
        ),
        "# Операции процесса БА в прогоне RUN-0061\n\n",
        "> Файл **порождён** скриптом "
        "[`experiments/issue_336_fixate_run.py`](../../../../experiments/issue_336_fixate_run.py)"
        " — не редактируйте вручную.\n\n",
        "## Распределение запросов БА\n\n",
        "Разметка **эвристическая**: тип операции определяется по ключевым словам "
        "реплики БА (правила — в "
        "[`experiments/issue_309_run_stats.py`](../../../../experiments/issue_309_run_stats.py), "
        "константа `REQUEST_KINDS`). Метки не взаимоисключающие, поэтому сумма по "
        "столбцу может превышать число реплик.\n\n",
        "| Операция | Реплик БА | Доля от реплик БА |\n| --- | --- | --- |\n",
    ]
    for kind, title in KIND_TITLES.items():
        count = stats["request_kinds"].get(kind, 0)
        out.append(f"| {title} | {count} | {round(100 * count / user_turns)}% |\n")
    unknown = stats["requests_unclassified"]
    out.append(
        f"| _не распознано эвристикой_ | {unknown} | {round(100 * unknown / user_turns)}% |\n"
    )

    out.append("\n## Сессии\n\n")
    out.append("| # | Начало, UTC | Конец, UTC | Реплик | Длительность, мин |\n")
    out.append("| --- | --- | --- | --- | --- |\n")
    for i, row in enumerate(stats["session_rows"], 1):
        out.append(
            f"| {i} | {row['start_utc']} | {row['end_utc']} | "
            f"{row['messages']} | {row['minutes']} |\n"
        )

    out.append("\n## Вложения диалога\n\n")
    out.append("| Файл | Прикреплён к репликам |\n| --- | --- |\n")
    for name, count in sorted(stats["attachments"].items()):
        out.append(f"| `{name}` | {count} |\n")
    return "".join(out)


def metrics(stats: dict) -> str:
    out = [
        front_matter("artifact", "mango-only"),
        "# Метрики прогона RUN-0061 (измеренные)\n\n",
        "> Файл **порождён** из экспорта чата — не редактируйте вручную. Все числа "
        "взяты из полей `usage` и `timestamp` самого экспорта и не являются оценкой.\n\n",
        "| # | Роль | Модель | UTC | Символов | in_tokens | out_tokens | reasoning | Вложений |\n",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |\n",
    ]
    for row in stats["turn_rows"]:
        out.append(
            f"| {row['index']} | {row['role']} | {row['model']} | {row['utc']} | "
            f"{row['chars']} | {row['input_tokens']} | {row['output_tokens']} | "
            f"{row['reasoning_tokens']} | {len(row['files'])} |\n"
        )
    out.append(
        f"\n- **turns:** {stats['turns']}\n"
        f"- **input_tokens:** {stats['tokens_input_sum']}\n"
        f"- **output_tokens:** {stats['tokens_output']}\n"
        f"- **reasoning_tokens:** {stats['tokens_reasoning']}\n"
    )
    return "".join(out)


def link_verification(audit: dict) -> str:
    report = audit["report"]
    dialog = audit["dialog"]
    checks = dialog["link_checks"]
    pages = report["pages"]
    with_headings = [p for p in pages if p["headings"] > 0]

    out = [
        front_matter(
            "log",
            "mango-only",
            [
                "related_artifacts:",
                '  - "experiments/issue_336_link_audit.py"',
                '  - "runs/2026/RUN-0057/outputs/L0-customer-form-with-assessment.md"',
            ],
        ),
        "# Журнал проверки ссылок прогона RUN-0061\n\n",
        "> Файл **порождён** скриптом "
        "[`experiments/issue_336_fixate_run.py`](../../../../experiments/issue_336_fixate_run.py)"
        " из замеров "
        "[`experiments/issue_336_link_audit.py`](../../../../experiments/issue_336_link_audit.py)"
        " — не редактируйте вручную.\n\n",
        "## 1. Ссылки, выданные моделью в диалоге\n\n",
        f"Проверена {len(checks)} ссылка(и) из ответов модели: HTTP-статус страницы, "
        "число заголовков с якорями и сопоставление заявленного раздела "
        "(«Раздел на странице: …») с реальными заголовками страницы.\n\n",
        "| Реплика | URL | HTTP | Заголовков | Заявленный раздел | Исход | Возможный якорь |\n",
        "| --- | --- | --- | --- | --- | --- | --- |\n",
    ]
    for check in checks:
        section = check["section_claimed"] or "—"
        anchor = f"`#{check['anchor']}`" if check["anchor"] else "—"
        out.append(
            f"| {check['turn']} | <{check['url']}> | {check['http']} | "
            f"{check['headings']} | {section} | "
            f"{RESOLUTION_TITLES[check['resolution']]} | {anchor} |\n"
        )

    out.append("\nИтог по исходам:\n\n")
    out.append("| Исход | Ссылок |\n| --- | --- |\n")
    for key, title in RESOLUTION_TITLES.items():
        count = sum(1 for c in checks if c["resolution"] == key)
        if count:
            out.append(f"| {title} | {count} |\n")

    out.append("\n## 2. Страницы вики, процитированные отчётом RUN-0057\n\n")
    out.append(
        f"Проверены все {len(pages)} различных страниц, названных токенами "
        f"`[twin: …]` в "
        "[`../../RUN-0057/outputs/L0-customer-form-with-assessment.md`]"
        "(../../RUN-0057/outputs/L0-customer-form-with-assessment.md). "
        f"Доступны (HTTP 200): {sum(1 for p in pages if p['http'] == 200)}. "
        f"Публикуют якоря заголовков: {len(with_headings)} "
        f"(всего {sum(p['headings'] for p in pages)} заголовков).\n\n"
    )
    out.append("| Страница | HTTP | Заголовков | Заглавие |\n| --- | --- | --- | --- |\n")
    for page in sorted(pages, key=lambda p: p["page"]):
        out.append(
            f"| [`{page['page']}`]({page['url']}) | {page['http']} | "
            f"{page['headings']} | {page['title']} |\n"
        )
    return "".join(out)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stats", type=Path, default=DATA / "stats.json")
    parser.add_argument("--audit", type=Path, default=DATA / "link-audit.json")
    parser.add_argument("--run-dir", type=Path, default=RUN)
    args = parser.parse_args()

    stats = json.loads(args.stats.read_text(encoding="utf-8"))
    audit = json.loads(args.audit.read_text(encoding="utf-8"))

    written = {
        args.run_dir / "outputs" / "prompt-usage.md": prompt_usage(stats),
        args.run_dir / "logs" / "metrics.md": metrics(stats),
        args.run_dir / "logs" / "link-verification.md": link_verification(audit),
    }
    for path, text in written.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        print(f"written: {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
