#!/usr/bin/env python3
"""Генерация записей прогонов `runs/2026/RUN-XXXX/` по экспортам чатов (issue #309).

Задача #309: каждый из 25 приложенных к issue JSON-экспортов чата фиксируется
**отдельной** записью прогона с ``run_type: statistics`` — целью является
накопление статистики применения промптов и операций процесса БА, а не
хранение сырых данных. Поэтому сами JSON в репозиторий не кладутся: в записи
остаются провенанс (URL + SHA-256 + размер), агрегированная статистика и
метрики по репликам — всё это порождается детерминированно.

Вход:
- ``experiments/issue_309_manifest.json`` — соответствие «файл ↔ прогон»,
  контрольные суммы, ссылки на вложения и тематика (курируется вручную);
- каталог со статистикой, полученной из ``experiments/issue_309_run_stats.py``:
  ``python3 experiments/issue_309_run_stats.py <export.json> --json <dir>/<file>.json``.

Использование:
    python3 experiments/issue_309_fixate_runs.py --stats-dir /tmp/stats
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ISSUE = "https://github.com/G-Ivan-A/mango_ba_prompts/issues/309"
FIXATION_DATE = "2026-08-22"
AUTHOR = "BA-IH + LLM (фиксация прогона: AI issue solver)"

KIND_TITLES = {
    "prompt-engineering": "работа с промптом / инструкцией",
    "artifact-generation": "запрос на генерацию артефакта",
    "validation": "проверка и критика результата",
    "elicitation": "элицитация, уточняющие вопросы",
    "iteration": "доработка предыдущего ответа",
    "context-load": "передача контекста и вложений",
}


def frontmatter(doc_type: str, scope: str, extra: list[str] | None = None) -> list[str]:
    lines = [
        "---",
        "status: draft",
        "version: 0.1",
        f"updated: {FIXATION_DATE}",
        "ai-generated: true",
        f"type: {doc_type}",
        f"scope: {scope}",
        "related_issues:",
        f'  - "{ISSUE}"',
    ]
    lines += extra or []
    lines.append("---")
    lines.append("")
    return lines


def yaml_list(name: str, values: list[str]) -> list[str]:
    return [f"{name}:"] + [f"  - {value}" for value in values]


def metadata(entry: dict, stats: dict) -> str:
    models = ", ".join(stats["models"]) or "not-recorded"
    lines = [
        f"run_id: {entry['run_id']}",
        f"process: {entry['process']}",
        'version: "0.1"',
        f"date: {FIXATION_DATE}",
        f'author: "{AUTHOR}"',
        f'model: "{models}"',
        "status: draft",
        "run_type: statistics",
    ]
    lines += yaml_list("source_paths", [ISSUE, entry["url"]])
    lines += yaml_list("inputs", ["inputs/README.md"])
    lines += yaml_list("outputs", ["outputs/README.md", "outputs/prompt-usage.md"])
    lines += yaml_list("logs", ["logs/experiment-log.md", "logs/metrics.md"])
    lines += yaml_list("feedback", ["feedback/review-notes.md"])
    lines += [
        "metrics:",
        f"  episodes: {stats['user_turns']}",
        f"  iterations: {stats['assistant_turns']}",
        f"  turns: {stats['turns']}",
        f"  sessions: {stats['sessions']}",
        f"  tokens_input: {stats['tokens_input_sum']}",
        f"  tokens_output: {stats['tokens_output']}",
        f"  tokens_thinking: {stats['tokens_reasoning']}",
        f"  tokens_dialog_total: {stats['tokens_input_sum'] + stats['tokens_output']}",
        f'  token_method: "provider-usage:{models}"',
        f"  duration_active_s: {stats['active_minutes'] * 60}",
        f'  dialog_start_utc: "{stats["start_utc"]}"',
        f'  dialog_end_utc: "{stats["end_utc"]}"',
        f"  calendar_days: {stats['calendar_days']}",
        f"  attachments_distinct: {len(stats['attachments'])}",
        f'  eval: "Прогон зафиксирован ради статистики: приёмка БА в экспорте не '
        f'выражена, оценка качества артефакта не выставляется. Считываются объём '
        f'диалога, распределение операций БА и расход токенов."',
    ]
    lines += yaml_list("related_issues", [ISSUE])
    lines += yaml_list(
        "related_artifacts",
        [
            "standards/runs-contract-standard.md",
            "experiments/issue_309_run_stats.py",
            "experiments/issue_309_fixate_runs.py",
        ],
    )
    return "\n".join(lines) + "\n"


def inputs_readme(entry: dict, stats: dict) -> str:
    lines = frontmatter("input", "mango-only")
    lines += [
        f"# Вход прогона {entry['run_id']} — провенанс",
        "",
        f"Тема: **{entry['theme']}**. {entry['focus']}",
        "",
        "## Источник",
        "",
        "| Поле | Значение |",
        "| --- | --- |",
        f"| Вложение issue | [`{entry['source_file']}`]({entry['url']}) |",
        f"| Размер, байт | {entry['size_bytes']} |",
        f"| SHA-256 | `{entry['sha256']}` |",
        f"| Заголовок чата в экспорте | `{stats['title'].strip() or '—'}` |",
        f"| Окно диалога, UTC | {stats['start_utc']} — {stats['end_utc']} |",
        "",
        "## Почему исходного JSON нет в репозитории",
        "",
        "Задача [#309]("
        + ISSUE
        + ") требует зафиксировать прогоны как **статистику применения промптов**"
        " и удалить исходные JSON-файлы из репозитория. Поэтому вход прогона"
        " описан провенансом, а не копией сырых данных: файл однозначно"
        " идентифицируется ссылкой и контрольной суммой, а все производные"
        " артефакты прогона порождаются из него детерминированно.",
        "",
        "## Воспроизведение",
        "",
        "```bash",
        f"curl -L -o {entry['source_file']} \\",
        f"  {entry['url']}",
        f"sha256sum {entry['source_file']}",
        f"# ожидается: {entry['sha256']}",
        "",
        f"python3 experiments/issue_309_run_stats.py {entry['source_file']} \\",
        f"  --json /tmp/stats/{Path(entry['source_file']).stem}.json",
        "python3 experiments/issue_309_fixate_runs.py --stats-dir /tmp/stats",
        "```",
        "",
        "## Чего во входе нет",
        "",
        "- нет сырого JSON-экспорта и полной стенограммы: прогон фиксирует"
        " статистику, а не содержимое переписки;",
        "- нет вложений диалога (документы, расшифровки): в записи остаются"
        " только их имена и количество обращений — см."
        " [`../outputs/prompt-usage.md`](../outputs/prompt-usage.md).",
    ]
    return "\n".join(lines) + "\n"


def outputs_readme(entry: dict, stats: dict) -> str:
    lines = frontmatter("index", "mango-only")
    lines += [
        f"# Результаты прогона {entry['run_id']} — {entry['theme']}",
        "",
        entry["focus"],
        "",
        "Прогон имеет `run_type: statistics`: результатом является не артефакт"
        " требований, а замеры по шкале статистики — объём выборки, покрытие"
        " типов запросов БА и расход ресурсов (см."
        " [`standards/runs-contract-standard.md`](../../../../standards/runs-contract-standard.md)).",
        "",
        "## Сводка",
        "",
        "| Метрика | Значение |",
        "| --- | --- |",
        f"| Реплик в ветке диалога | {stats['turns']} |",
        f"| Эпизодов (реплик БА) | {stats['user_turns']} |",
        f"| Ответов модели | {stats['assistant_turns']} |",
        f"| Рабочих сессий (разрыв > 30 мин) | {stats['sessions']} |",
        f"| Активное время внутри сессий, мин | {stats['active_minutes']} |",
        f"| Календарный интервал, дн. | {stats['calendar_days']} |",
        f"| Модели | {', '.join(stats['models']) or '—'} |",
        f"| Токенов на выходе | {stats['tokens_output']} |",
        f"| В том числе reasoning | {stats['tokens_reasoning']} |",
        f"| Токенов на входе (с переотправкой контекста) | {stats['tokens_input_sum']} |",
        f"| Максимум входа за один вызов | {stats['tokens_input_max']} |",
        f"| Символов ввода БА | {stats['chars_user']} |",
        f"| Символов ответов модели | {stats['chars_assistant']} |",
        "",
        "## Состав записи",
        "",
        "| Файл | Что содержит |",
        "| --- | --- |",
        "| [`prompt-usage.md`](prompt-usage.md) | распределение операций процесса БА и вложения |",
        "| [`../logs/metrics.md`](../logs/metrics.md) | метрики по каждой реплике |",
        "| [`../logs/experiment-log.md`](../logs/experiment-log.md) | как получена запись |",
        "| [`../inputs/README.md`](../inputs/README.md) | провенанс исходного экспорта |",
        "| [`../feedback/review-notes.md`](../feedback/review-notes.md) | ограничения чтения |",
    ]
    return "\n".join(lines) + "\n"


def prompt_usage(entry: dict, stats: dict) -> str:
    lines = frontmatter("artifact", "prompts")
    lines += [
        f"# Операции процесса БА в прогоне {entry['run_id']}",
        "",
        "> Файл **порождён** скриптом"
        " [`experiments/issue_309_fixate_runs.py`](../../../../experiments/issue_309_fixate_runs.py)"
        " — не редактируйте вручную.",
        "",
        "## Распределение запросов БА",
        "",
        "Разметка **эвристическая**: тип операции определяется по ключевым словам"
        " реплики БА (правила — в"
        " [`experiments/issue_309_run_stats.py`](../../../../experiments/issue_309_run_stats.py),"
        " константа `REQUEST_KINDS`). Метки не взаимоисключающие, поэтому сумма"
        " по столбцу может превышать число реплик.",
        "",
        "| Операция | Реплик БА | Доля от реплик БА |",
        "| --- | --- | --- |",
    ]
    total = stats["user_turns"] or 1
    for kind, count in stats["request_kinds"].items():
        lines.append(f"| {KIND_TITLES[kind]} (`{kind}`) | {count} | {count / total:.0%} |")
    lines += [
        f"| _не распознано эвристикой_ | {stats['requests_unclassified']} |"
        f" {stats['requests_unclassified'] / total:.0%} |",
        "",
        "## Сессии",
        "",
        "| # | Начало, UTC | Конец, UTC | Реплик | Длительность, мин |",
        "| --- | --- | --- | --- | --- |",
    ]
    for index, row in enumerate(stats["session_rows"], start=1):
        lines.append(
            f"| {index} | {row['start_utc']} | {row['end_utc']} | {row['messages']} |"
            f" {row['minutes']} |"
        )
    lines += ["", "## Вложения диалога", ""]
    if stats["attachments"]:
        lines += ["| Файл | Прикреплён к репликам |", "| --- | --- |"]
        for name, count in sorted(stats["attachments"].items()):
            lines.append(f"| `{name}` | {count} |")
        lines += [
            "",
            "Содержимое вложений в репозиторий не переносится: фиксируется факт"
            " передачи контекста, а не сами данные.",
        ]
    else:
        lines.append("Вложений в диалоге нет.")
    return "\n".join(lines) + "\n"


def metrics(entry: dict, stats: dict) -> str:
    lines = frontmatter("artifact", "mango-only")
    lines += [
        f"# Метрики прогона {entry['run_id']} (измеренные)",
        "",
        "> Файл **порождён** из экспорта чата — не редактируйте вручную. Все числа"
        " взяты из полей `usage` и `timestamp` самого экспорта и не являются оценкой.",
        "",
        "| # | Роль | Модель | UTC | Символов | in_tokens | out_tokens | reasoning | Вложений |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in stats["turn_rows"]:
        lines.append(
            f"| {row['index']} | {row['role']} | {row['model']} | {row['utc']} |"
            f" {row['chars']} | {row['input_tokens']} | {row['output_tokens']} |"
            f" {row['reasoning_tokens']} | {len(row['files'])} |"
        )
    lines += [
        "",
        f"- **turns:** {stats['turns']}",
        f"- **input_tokens:** {stats['tokens_input_sum']}",
        f"- **output_tokens:** {stats['tokens_output']}",
        f"- **reasoning_tokens:** {stats['tokens_reasoning']}",
        f"- **window:** {stats['start_utc']} — {stats['end_utc']} UTC",
        "",
        "> Скачки входных токенов — это переданные в отдельные реплики документы,"
        " а не рост самой переписки.",
    ]
    return "\n".join(lines) + "\n"


def experiment_log(entry: dict, stats: dict) -> str:
    lines = frontmatter(
        "log",
        "mango-only",
        [
            "related_artifacts:",
            '  - "standards/runs-contract-standard.md"',
            '  - "experiments/issue_309_run_stats.py"',
        ],
    )
    lines += [
        f"# Журнал фиксации прогона {entry['run_id']}",
        "",
        "## Цель",
        "",
        "Зафиксировать экспорт чата "
        f"`{entry['source_file']}` отдельной записью прогона с"
        " `run_type: statistics` (issue #309): накопить статистику применения"
        " промптов и операций процесса БА.",
        "",
        "## Шаги",
        "",
        "1. Вложение issue скачано и разобрано как JSON; экспорт читаем, ветка"
        f" диалога восстановлена по `parentId` — {stats['turns']} реплик.",
        "2. Статистика посчитана `experiments/issue_309_run_stats.py`"
        " (объём, токены, сессии, вложения, эвристическая разметка операций).",
        "3. Артефакты записи порождены `experiments/issue_309_fixate_runs.py`.",
        "4. Исходный JSON в репозиторий не добавлялся — по требованию issue #309"
        " исходные файлы в репозитории не остаются; вместо них в"
        " [`../inputs/README.md`](../inputs/README.md) зафиксирован провенанс"
        " (ссылка, размер, SHA-256).",
        "",
        "## Наблюдения",
        "",
        f"- диалог шёл с {stats['start_utc'][:10]} по {stats['end_utc'][:10]}"
        f" ({stats['sessions']} рабочих сессий);",
        f"- моделей задействовано: {len(stats['models'])}"
        f" ({', '.join(stats['models']) or '—'});",
        f"- вложений в диалоге: {len(stats['attachments'])} различных файлов.",
    ]
    return "\n".join(lines) + "\n"


def review_notes(entry: dict, stats: dict) -> str:
    lines = frontmatter(
        "artifact",
        "mango-only",
        ["related_artifacts:", '  - "runs/2026/%s/outputs/prompt-usage.md"' % entry["run_id"]],
    )
    lines += [
        f"# Ограничения чтения прогона {entry['run_id']}",
        "",
        "- **Шкала.** Прогон `statistics`: успех читается по покрытию и"
        " сопоставимости выборки, а не по качеству артефакта. Смешивать с"
        " прогонами `execution` при выводах о промптах нельзя.",
        "- **Приёмка.** В экспорте нет выраженной приёмки БА, поэтому"
        " `status: draft`, а `success_rate` намеренно не выставлен: основания для"
        " него в данных отсутствуют.",
        "- **Разметка операций** эвристическая (ключевые слова), даёт порядок"
        " величин, а не точную классификацию; одна реплика может попасть в"
        " несколько категорий.",
        "- **Токены входа** просуммированы по вызовам и включают переотправку"
        f" контекста: {stats['tokens_input_sum']} при максимуме"
        f" {stats['tokens_input_max']} за один вызов — это не объём переписки.",
        "- **Содержимое диалога** в записи отсутствует: восстановить его можно"
        " только из исходного вложения issue по провенансу в"
        " [`../inputs/README.md`](../inputs/README.md).",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stats-dir", type=Path, required=True)
    parser.add_argument("--runs-dir", type=Path, default=ROOT / "runs" / "2026")
    args = parser.parse_args()

    manifest = json.loads((ROOT / "experiments/issue_309_manifest.json").read_text("utf-8"))
    for entry in manifest:
        stats_path = args.stats_dir / (Path(entry["source_file"]).stem + ".json")
        stats = json.loads(stats_path.read_text("utf-8"))
        run_dir = args.runs_dir / entry["run_id"]
        for subdir in ("inputs", "outputs", "logs", "feedback"):
            (run_dir / subdir).mkdir(parents=True, exist_ok=True)
        files = {
            "metadata.yaml": metadata(entry, stats),
            "inputs/README.md": inputs_readme(entry, stats),
            "outputs/README.md": outputs_readme(entry, stats),
            "outputs/prompt-usage.md": prompt_usage(entry, stats),
            "logs/metrics.md": metrics(entry, stats),
            "logs/experiment-log.md": experiment_log(entry, stats),
            "feedback/review-notes.md": review_notes(entry, stats),
        }
        for name, text in files.items():
            (run_dir / name).write_text(text, encoding="utf-8")
        print(f"{entry['run_id']} ← {entry['source_file']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
