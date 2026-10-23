"""Разворачивает реплики экспорта чата «Проект: СПЛИТ (БА)» за окно 21–23.10.2026 (issue #384).

Нумерация реплик — индекс в линейной ветке ``linear_chain`` (как в #375).
Окно считается по московскому времени (UTC+3): 2026-10-21 00:00 — 2026-10-23 23:59:59.
Выход — ``experiments/issue_384/turns/`` (в git не попадает, правило #309) и
сводка реплик окна в stdout.

    python3 -I experiments/issue_384_chat_window_dump.py <chat-export.json>
"""

from __future__ import annotations

import datetime
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from chat_export_to_markdown import answer_text, linear_chain  # noqa: E402

MSK = datetime.timezone(datetime.timedelta(hours=3))
WINDOW_START = datetime.datetime(2026, 10, 21, tzinfo=MSK).timestamp()
WINDOW_END = datetime.datetime(2026, 10, 24, tzinfo=MSK).timestamp()


def main() -> int:
    export = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    out = ROOT / "experiments" / "issue_384" / "turns"
    out.mkdir(parents=True, exist_ok=True)
    chain = linear_chain(export)
    print(f"linear chain: {len(chain)} turns")
    for index, message in enumerate(chain):
        stamp = message.get("timestamp") or 0
        if not WINDOW_START <= stamp < WINDOW_END:
            continue
        role = message.get("role")
        text = (message.get("content") or "") if role == "user" else answer_text(message)
        files = [f.get("name") for f in message.get("files") or [] if isinstance(f, dict)]
        when = datetime.datetime.fromtimestamp(stamp, MSK).strftime("%Y-%m-%d %H:%M:%S MSK")
        header = f"### {index} {role} {when} model={message.get('model')} files={files}\n"
        (out / f"{index:03d}.md").write_text(header + text + "\n", encoding="utf-8")
        print(f"{index:4d} {role:9s} {when} chars={len(text):6d} files={files}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
