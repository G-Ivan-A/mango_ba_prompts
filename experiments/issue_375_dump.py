"""Разворачивает экспорт чата задачи 1106 в пронумерованные реплики (issue #375).

Нумерация реплик совпадает с индексом в линейной ветке ``linear_chain`` —
та же, что используется в разметке и сверке цитат. Выход — каталог
``experiments/issue_375/turns/`` (в git не попадает, правило #309).

    python3 -I experiments/issue_375_dump.py <chat-export-1106.json>
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from chat_export_to_markdown import answer_text, linear_chain  # noqa: E402


def main() -> int:
    export = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    out = ROOT / "experiments" / "issue_375" / "turns"
    out.mkdir(parents=True, exist_ok=True)
    for index, message in enumerate(linear_chain(export)):
        role = message.get("role")
        text = message.get("content") or "" if role == "user" else answer_text(message)
        files = [f.get("name") for f in message.get("files") or [] if isinstance(f, dict)]
        header = f"### {index} {role} model={message.get('model')} files={files}\n"
        (out / f"{index:03d}.md").write_text(header + text + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
