#!/usr/bin/env python3
"""Разбор выгрузки чата Qwen и подсчёт метрик прогона.

Использован для RUN-0013 (issue #271): нормализация стенограммы и измерение
токенов/латентности по эпизодам.

    python3 experiments/parse_qwen_chat_export.py chat-export.json --metrics
    python3 experiments/parse_qwen_chat_export.py chat-export.json --transcript

Токены считаются через tiktoken cl100k_base — та же кодировка, что указана в
kb/ репозитория (`token_method: tiktoken:cl100k_base`). Для qwen это оценка.
"""
import argparse
import ast
import datetime
import json


def load_branch(path):
    """Возвращает активную ветку диалога: от корня к currentId."""
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    history = data[0]["chat"]["history"]
    messages = history["messages"]
    chain = []
    node = history.get("currentId")
    while node:
        msg = messages[node]
        chain.append(msg)
        node = msg.get("parentId")
    return list(reversed(chain))


def answer_text(msg):
    """Текст ответа модели: только блоки phase == 'answer'."""
    parts = [
        item.get("content", "")
        for item in msg.get("content_list") or []
        if item.get("phase") == "answer"
    ]
    return "\n".join(parts) if parts else msg.get("content", "")


def thinking_text(msg):
    out = []
    for item in msg.get("content_list") or []:
        if item.get("phase") == "thinking_summary":
            extra = item.get("extra") or {}
            if not isinstance(extra, dict):
                extra = ast.literal_eval(extra)
            thought = (extra.get("summary_thought") or {}).get("content", "")
            if isinstance(thought, list):
                thought = "\n".join(str(part) for part in thought)
            out.append(thought)
    return "\n".join(out)


def end_time(msg):
    """extra бывает и dict, и строкой с python-repr."""
    extra = msg.get("extra") or {}
    if not isinstance(extra, dict):
        extra = ast.literal_eval(extra)
    return extra.get("endTime")


def ts(value):
    return datetime.datetime.fromtimestamp(value, datetime.UTC).strftime("%Y-%m-%d %H:%M:%S UTC")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("export")
    ap.add_argument("--metrics", action="store_true")
    ap.add_argument("--transcript", action="store_true")
    args = ap.parse_args()

    chain = load_branch(args.export)

    enc = None
    if args.metrics:
        import tiktoken

        enc = tiktoken.get_encoding("cl100k_base")

    pairs = []
    pending = None
    for msg in chain:
        if msg.get("role") == "user":
            pending = msg
        elif msg.get("role") == "assistant" and pending is not None:
            pairs.append((pending, msg))
            pending = None

    if args.transcript:
        for idx, (user, bot) in enumerate(pairs, 1):
            print(f"## Эпизод {idx}\n")
            print(f"**БА → модель** · {ts(user['timestamp'])}\n")
            print("```text")
            print(user.get("content", "").strip())
            print("```\n")
            print(f"**Модель → БА** · {ts(bot['timestamp'])}\n")
            print(answer_text(bot).strip())
            print("\n---\n")

    if args.metrics:
        tot_in = tot_out = tot_think = 0.0
        tot_lat = 0.0
        print(f"{'ep':>3} {'time':>8} {'in_tok':>7} {'out_tok':>8} {'think':>6} {'lat_s':>7}")
        for idx, (user, bot) in enumerate(pairs, 1):
            n_in = len(enc.encode(user.get("content", "")))
            n_out = len(enc.encode(answer_text(bot)))
            n_think = len(enc.encode(thinking_text(bot)))
            finished = end_time(bot)
            lat = (finished - bot["timestamp"]) if finished else 0.0
            tot_in += n_in
            tot_out += n_out
            tot_think += n_think
            tot_lat += lat
            clock = ts(user["timestamp"]).split()[1]
            print(f"{idx:>3} {clock:>8} {n_in:>7} {n_out:>8} {n_think:>6} {lat:>7.1f}")
        print(
            f"TOTAL in={tot_in:.0f} out={tot_out:.0f} think={tot_think:.0f} "
            f"latency_s={tot_lat:.1f}"
        )
        span = pairs[-1][1]["timestamp"] - pairs[0][0]["timestamp"]
        print(f"wall_clock_s={span:.0f}")


if __name__ == "__main__":
    main()
