"""Разворачивает весь линейный чат экспорта (issue #387) в один файл для поиска.

Нумерация реплик — индекс в ``linear_chain`` (как в #375/#384). Выход вне
репозитория (правило #309): путь задаётся вторым аргументом.

    python3 -I experiments/issue_387_chat_dump.py <chat-export.json> <out.md>
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


def main() -> int:
    export = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    chain = linear_chain(export)
    parts = []
    for index, message in enumerate(chain):
        role = message.get("role")
        text = (message.get("content") or "") if role == "user" else answer_text(message)
        when = datetime.datetime.fromtimestamp(message.get("timestamp") or 0, MSK)
        parts.append(f"\n### {index} {role} {when:%Y-%m-%d %H:%M} MSK\n{text}\n")
    Path(sys.argv[2]).write_text("".join(parts), encoding="utf-8")
    print(f"linear chain: {len(chain)} turns")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
