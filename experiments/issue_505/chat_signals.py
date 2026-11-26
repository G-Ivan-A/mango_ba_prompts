#!/usr/bin/env python3
"""Счётчики сигналов чата 1143 (issue #505) без публикации текста чата.

Запуск (текст чата не коммитится, путь передаётся аргументом):
    python3 -I experiments/issue_505/chat_signals.py /path/to/1143.txt \
        > runs/2026/RUN-0096/logs/chat-signals.json

Скрипт выводит только счётчики, номера строк и sha256 — без цитат,
поэтому результат можно хранить в репозитории (ТЗ Заказчика не попадает).
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

END_RE = re.compile(r"^КОНЕЦ ((?:AIN-\d\d)|(?:Ш-\d+)) (\d+\.\d+)\s*$")
SIGNALS = {
    "access_to_kb_header": re.compile(r"Доступ к БЗ"),
    "receipt_header": re.compile(r"Проверки \(receipt\)"),
    "step_summary_header": re.compile(r"Итог шага"),
    "ba_approval_header": re.compile(r"На согласование БА"),
    "bcreq_state_header": re.compile(r"Состояние BCREQ"),
    "memory_package_header": re.compile(r"Пакет памяти"),
    "access_gap_token": re.compile(r"ACCESS_GAP"),
    "constitution_receipt_line": re.compile(r"Конституция: прочитана"),
    "future_steps_not_done_line": re.compile(r"[Дд]ействия будущих шагов не выполнялись"),
    "web_tool_denied_line": re.compile(r"(не инициируются|не предоставлен|[Нн]ет веб|No web tools)"),
    "web_search_trace": re.compile(r"^Найдено \d+ веб-страниц"),
    "ui_ai_footer": re.compile(r"Этот ответ сгенерирован AI"),
    "ui_file_limit_notice": re.compile(r"может прочитать максимум"),
    "flattery_absolutely_right": re.compile(r"[Аа]бсолютно прав"),
    "attach_files_request": re.compile(r"прилож(ите|ить) (нужные )?файлы"),
}
CJK_RE = re.compile(r"[一-鿿]")
EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF✅❌⚠]")


def main(path: str) -> dict:
    raw = Path(path).read_bytes()
    text = raw.decode("utf-8").replace("\r\n", "\n")
    lines = text.split("\n")
    ends: list[dict] = []
    for no, line in enumerate(lines, 1):
        m = END_RE.match(line.strip())
        if m:
            ends.append({"line": no, "step": m.group(1), "version": m.group(2)})
    per_step = Counter(e["step"] for e in ends)
    signals = {}
    for key, rx in SIGNALS.items():
        hits = [no for no, line in enumerate(lines, 1) if rx.search(line)]
        signals[key] = {"count": len(hits), "lines": hits[:60]}
    cjk_lines = [no for no, line in enumerate(lines, 1) if CJK_RE.search(line)]
    emoji_lines = [no for no, line in enumerate(lines, 1) if EMOJI_RE.search(line)]
    return {
        "source": {
            "file": "1143.txt (вложение issue #505, не коммитится)",
            "sha256": hashlib.sha256(raw).hexdigest(),
            "bytes": len(raw),
            "lines": len(lines),
            "line_endings": "CRLF" if b"\r\n" in raw else "LF",
        },
        "step_end_markers": {
            "total": len(ends),
            "distinct_steps": len(per_step),
            "repeated_steps": {k: v for k, v in sorted(per_step.items()) if v > 1},
            "markers": ends,
        },
        "signals": signals,
        "language_leaks": {
            "cjk_lines": len(cjk_lines),
            "cjk_line_ranges_sample": cjk_lines[:20],
            "emoji_lines": len(emoji_lines),
        },
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: chat_signals.py <chat.txt>")
    json.dump(main(sys.argv[1]), sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
