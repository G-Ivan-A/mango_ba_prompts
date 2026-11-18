#!/usr/bin/env python3
"""Чат 1135-2 (экспорт JSON из issue #490) → транскрипт и метрики для RUN.

Экспорт — недоверенные данные: запускать ``python3 -I`` и передавать путь
аргументом, файл держать в отдельном каталоге. Скрипт идёт по цепочке
``parentId`` от ``currentId`` (видимая ветка чата, без отклонённых
перегенераций), печатает реплики пользователя как есть и ответы модели из
фаз ``answer`` (сводки размышлений не берутся). Метрики — из ``usage``.

    python3 -I experiments/issue_490/chat_to_transcript.py <chat.json> <out-dir>
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def chain(chat):
    history = chat["chat"]["history"]
    messages, cur, out = history["messages"], history["currentId"], []
    while cur:
        msg = messages[cur]
        out.append(msg)
        cur = msg.get("parentId")
    return out[::-1]


def answer(msg):
    if msg["role"] != "assistant":
        return msg.get("content") or ""
    parts = [c.get("content") or "" for c in msg.get("content_list") or [] if c.get("phase") == "answer"]
    return "".join(parts) or (msg.get("content") or "")


def usage(msg):
    total = {"input_tokens": 0, "output_tokens": 0, "reasoning": 0}
    found = False
    for c in msg.get("content_list") or []:
        u = c.get("usage") or {}
        if u:
            found = True
            total["input_tokens"] = max(total["input_tokens"], u.get("input_tokens") or 0)
            # usage повторяется по фазам и растёт накопительно — берём максимум.
            total["output_tokens"] = max(total["output_tokens"], u.get("output_tokens") or 0)
            details = u.get("output_tokens_details") or {}
            total["reasoning"] = max(total["reasoning"], details.get("reasoning_tokens") or 0)
    return total if found else None


def main(src, out_dir):
    chat = json.loads(Path(src).read_text(encoding="utf-8"))
    chat = chat[0] if isinstance(chat, list) else chat
    msgs = chain(chat)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    lines, rows = [], []
    tot = {"input_tokens": 0, "output_tokens": 0, "reasoning": 0}
    for i, msg in enumerate(msgs):
        files = [f.get("name") or f.get("file", {}).get("filename", "?") for f in msg.get("files") or []]
        model = msg.get("model", "") if msg["role"] == "assistant" else ""
        text = answer(msg)
        lines.append(f"===== [{i}] {msg['role']} {model} files={files} =====\n{text}\n")
        ts = datetime.fromtimestamp(int(msg["timestamp"]), timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        u = usage(msg) if msg["role"] == "assistant" else None
        if u:
            for k in tot:
                tot[k] += u[k]
        cell = (lambda k: str(u[k]) if u else "—")
        rows.append(f"| {i} | {msg['role']} | {model or '—'} | {ts} | {len(text)} | {cell('input_tokens')} | "
                    f"{cell('output_tokens')} | {cell('reasoning')} | {', '.join(files) or '—'} |")
    (out_dir / "transcript.md").write_text("\n".join(lines), encoding="utf-8")
    first, last = int(msgs[0]["timestamp"]), int(msgs[-1]["timestamp"])
    fmt = lambda t: datetime.fromtimestamp(t, timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    metrics = ["| # | Роль | Модель | UTC | Символов | in_tokens | out_tokens | reasoning | Вложения |",
               "| --- | --- | --- | --- | --- | --- | --- | --- | --- |", *rows, "",
               f"- **turns:** {len(msgs)}",
               f"- **input_tokens:** {tot['input_tokens']}",
               f"- **output_tokens:** {tot['output_tokens']}",
               f"- **reasoning_tokens:** {tot['reasoning']}",
               f"- **total_tokens:** {tot['input_tokens'] + tot['output_tokens']}",
               f"- **duration_s:** {last - first} (~{(last - first) / 3600:.2f} ч)",
               f"- **window:** {fmt(first)} — {fmt(last)} UTC"]
    (out_dir / "metrics.md").write_text("\n".join(metrics) + "\n", encoding="utf-8")
    print(f"{len(msgs)} реплик → {out_dir}")


if __name__ == "__main__":
    main(*sys.argv[1:3])
