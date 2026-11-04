#!/usr/bin/env python3
"""BL-157в: детерминированное извлечение реплик БА из экспортов чатов (issue #448).

Экспорты — недоверенные данные владельца (шесть чатов на старых промптах).
Скрипт их только читает (``python3 -I``), в репозиторий сырой текст не
пишет: полный дамп реплик идёт во внешний каталог ``--dump`` для ручного
кодирования, в репозиторий — только обезличенная статистика ``--json``.

Что считается:
- линейная ветка диалога (как ``scripts/chat_export_to_markdown.py``);
- реплика БА — «вставка промпта», если в ней есть фронтматтер, маркер
  ``<!-- … -->`` или имя промпта ``bcreq-*``; иначе — «реплика»;
- в репликах размечаются поправки БА по словарю ``CORRECTION`` (эвристика,
  объявлена как эвристика) и упомянутые промпты ``bcreq-*``.

Использование:
    python3 -I experiments/issue_448/bl157v_chat_extract.py EXPORT... \
        --dump /tmp/chats448-work --json experiments/issue_448/bl157v/stats.json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from chat_export_to_markdown import answer_text, linear_chain, usage  # noqa: E402

PROMPT_ID = re.compile(r"\bbcreq-[a-z0-9-]+")
PASTE = re.compile(r"^---\s*$|<!--|^#\s+.*(промпт|prompt|Роль|РОЛЬ)", re.M | re.I)
CORRECTION = {
    "ошибка": r"ошиб|неправильн|неверн|не так\b|некорректн",
    "пропуск": r"забыл|пропустил|не учел|не учёл|упустил|нет\s+раздел|не хватает|отсутству",
    "добавление": r"выдума|придума|откуда|нет в (исходн|документ|стенограм)|не было",
    "переделка": r"переделай|перепиши|исправ|доработ|замени|убери|удали",
    "формат": r"формат|таблиц|шаблон|структур|нумерац",
    "уточнение": r"уточн|почему|зачем|объясни",
    "практика": r"best practice|лучш\w+ практик|стандарт|BABOK|ISO|IEEE|INVEST|BPMN|UML",
}


def kinds(text: str) -> list[str]:
    low = text.lower()
    return [k for k, p in CORRECTION.items() if re.search(p, low, re.I)]


def collect(path: Path) -> tuple[dict, list[dict]]:
    export = json.loads(path.read_text(encoding="utf-8"))
    chain = linear_chain(export)
    turns, models = [], {}
    for i, m in enumerate(chain):
        if m.get("role") == "assistant":
            name = m.get("model") or m.get("modelName") or "?"
            models[name] = models.get(name, 0) + 1
            continue
        if m.get("role") != "user":
            continue
        text = m.get("content") or ""
        paste = bool(PASTE.search(text)) and len(text) > 1500
        turns.append({
            "i": i, "chars": len(text), "paste": paste,
            "prompts": sorted(set(PROMPT_ID.findall(text))),
            "kinds": [] if paste else kinds(text), "text": text,
        })
    answers = [m for m in chain if m.get("role") == "assistant"]
    stat = {
        "export": path.name,
        "messages": len(chain),
        "ba_turns": len(turns),
        "prompt_pastes": sum(t["paste"] for t in turns),
        "ba_replies": sum(not t["paste"] for t in turns),
        "models": models,
        "prompts_named": sorted({p for t in turns for p in t["prompts"]}),
        "correction_kinds": {k: sum(k in t["kinds"] for t in turns) for k in CORRECTION},
        "input_tokens": sum(usage(m).get("input_tokens", 0) for m in answers),
        "output_tokens": sum(usage(m).get("output_tokens", 0) for m in answers),
        "answer_chars": sum(len(answer_text(m)) for m in answers),
    }
    return stat, turns


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("exports", nargs="+", type=Path)
    ap.add_argument("--dump", type=Path, required=True)
    ap.add_argument("--json", type=Path, required=True)
    a = ap.parse_args()
    a.dump.mkdir(parents=True, exist_ok=True)
    stats = []
    for path in sorted(a.exports):
        stat, turns = collect(path)
        stats.append(stat)
        with (a.dump / f"{path.stem}.txt").open("w", encoding="utf-8") as out:
            for t in turns:
                flag = "PASTE" if t["paste"] else "REPLY"
                out.write(f"\n===== turn {t['i']} {flag} chars={t['chars']} prompts={t['prompts']} kinds={t['kinds']}\n")
                out.write(t["text"][:400] if t["paste"] else t["text"][:3000])
                out.write("\n")
    total = {k: sum(s[k] for s in stats) for k in ("messages", "ba_turns", "prompt_pastes", "ba_replies", "input_tokens", "output_tokens")}
    a.json.parent.mkdir(parents=True, exist_ok=True)
    a.json.write_text(json.dumps({"exports": stats, "total": total}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(total, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
