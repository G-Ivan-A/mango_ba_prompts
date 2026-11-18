#!/usr/bin/env python3
"""Сигналы проблем в расшифровке чата 1135-2 (issue #490).

Запуск: ``python3 -I experiments/issue_490/chat_signals.py <transcript.md>``
(расшифровку строит ``scripts/chat_export_to_markdown.py`` из выгрузки чата).

Считает по ответам модели простые текстовые признаки — без LLM, только
регулярные выражения. Это счётчики для аналитического артефакта, а не оценка
качества: каждый признак сверен вручную на цитатах (см. анализ #490).

* ``sycophancy`` — «абсолютно прав/точна/справедлива», «безупречн»;
* ``table_rows`` — строки Markdown-таблиц (жалоба БА, ход 18);
* ``next_prompt`` — явный призыв «Введите следующий промпт»/«следующий шаг»;
* ``ask_ba`` — вопросы «Правильно понимаю…?» к БА вместо вопросов Заказчику;
* ``mode_choice`` — упоминание выбора stepwise/oneshot.
"""
import json
import re
import sys

HEADER = re.compile(r"^===== \[(\d+)\] (\w+)\b.*=====$", re.M)
SIGNALS = {
    "sycophancy": re.compile(r"(?i)абсолютно (?:прав|точн|справедлив|верн)|безупречн"),
    "table_rows": re.compile(r"^\s*\|.*\|\s*$", re.M),
    "next_prompt": re.compile(r"(?i)введите следующий промпт|следующий шаг|рекомендуемый следующий"),
    "ask_ba": re.compile(r"(?i)правильно понимаю"),
    "mode_choice": re.compile(r"(?i)stepwise|oneshot"),
}


def turns(text):
    marks = list(HEADER.finditer(text))
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        yield int(m.group(1)), m.group(2), text[m.end():end]


def main(path):
    text = open(path, encoding="utf-8").read()
    per_turn, totals, with_signal = {}, dict.fromkeys(SIGNALS, 0), dict.fromkeys(SIGNALS, 0)
    answers = 0
    for idx, role, body in turns(text):
        if role != "assistant" or not body.strip():
            continue
        answers += 1
        counts = {k: len(rx.findall(body)) for k, rx in SIGNALS.items()}
        per_turn[idx] = {k: v for k, v in counts.items() if v}
        for k, v in counts.items():
            totals[k] += v
            with_signal[k] += bool(v)
    print(json.dumps({"assistant_answers": answers, "totals": totals,
                      "answers_with_signal": with_signal,
                      "per_turn": {k: v for k, v in per_turn.items() if v}},
                     ensure_ascii=False, indent=1))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
