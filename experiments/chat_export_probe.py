#!/usr/bin/env python3
"""Probe an OpenWebUI-style chat export: linear chain, token usage, attachments.

Статус: локальный разведочный инструмент, запускается вручную
(`python3 experiments/chat_export_probe.py <export.json>`); из CI/GitHub Actions
не вызывается (см. `runs/README.md`, раздел «Локальные инструменты
воспроизводимости»). Зависимостей, кроме стандартной библиотеки, нет.
"""
import json, sys, datetime

path = sys.argv[1]
chat = json.load(open(path, encoding="utf-8"))[0]
hist = chat["chat"]["history"]
msgs = hist["messages"]

chain, mid = [], chat.get("currentId") or hist.get("currentId")
while mid:
    m = msgs[mid]; chain.append(m); mid = m.get("parentId")
chain.reverse()

def answer(m):
    return "\n\n".join(p["content"] for p in (m.get("content_list") or [])
                       if p.get("phase") == "answer" and p.get("content")) or m.get("content", "")

def usage(m):
    for p in reversed(m.get("content_list") or []):
        if p.get("usage"):
            return p["usage"]
    return {}

tot_in = tot_out = tot_reason = 0
for i, m in enumerate(chain):
    u = usage(m)
    tot_in += u.get("input_tokens", 0); tot_out += u.get("output_tokens", 0)
    tot_reason += (u.get("output_tokens_details") or {}).get("reasoning_tokens", 0)
    files = [f.get("name") for f in (m.get("files") or [])]
    print(f"[{i}] {m['role']} model={m.get('model')} ts={m.get('timestamp')} "
          f"len={len(answer(m))} in={u.get('input_tokens')} out={u.get('output_tokens')} files={files}")
dur = chain[-1]["timestamp"] - chain[0]["timestamp"]
print(f"\nturns={len(chain)} input_tokens={tot_in} output_tokens={tot_out} "
      f"reasoning_tokens={tot_reason} total={tot_in+tot_out} duration_s={dur} ({dur/3600:.2f} h)")
