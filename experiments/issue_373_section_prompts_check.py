"""Сверка цитат ``outputs/section-prompts.md`` RUN-0073 с экспортом чата задачи 1123 (issue #373).

Каждая цитата вида ``р. N: «…»`` должна дословно (после нормализации пробелов и
markdown-выделения) встречаться в реплике N линейной ветки экспорта. Результат —
``experiments/issue_373/section-prompts-check.json`` (номер реплики, найдено ли,
SHA-256 нормализованной цитаты); текст экспорта в файл не попадает.

Запуск (экспорт — недоверенные данные, только с ``-I``)::

    python3 -I experiments/issue_373_section_prompts_check.py <chat-export-1123.json>
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from chat_export_to_markdown import answer_text, linear_chain  # noqa: E402

DOC = ROOT / "runs/2026/RUN-0073/outputs/section-prompts.md"
OUT = ROOT / "experiments" / "issue_373" / "section-prompts-check.json"
QUOTE = re.compile(r"р\. (\d+)\]?: «([^»]+)»")


def normalize(text: str) -> str:
    text = text.replace("*", "").replace("`", "").replace(" ", " ")
    return re.sub(r"\s+", " ", text).strip()


def quotes(text: str) -> list[tuple[int, str]]:
    return [(int(turn), quote) for turn, quote in QUOTE.findall(text)]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("export", type=Path)
    parser.add_argument("--output", type=Path, default=OUT)
    args = parser.parse_args()

    chain = linear_chain(json.loads(args.export.read_text(encoding="utf-8")))
    texts = [normalize(answer_text(message)) for message in chain]
    rows = []
    for turn, quote in quotes(DOC.read_text(encoding="utf-8")):
        needle = normalize(quote)
        rows.append({
            "turn": turn,
            "found": turn < len(texts) and needle in texts[turn],
            "sha256": hashlib.sha256(needle.encode("utf-8")).hexdigest(),
        })
    payload = {
        "export_sha256": hashlib.sha256(args.export.read_bytes()).hexdigest(),
        "quotes": len(rows),
        "missing": sum(not row["found"] for row in rows),
        "rows": rows,
    }
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"quotes={payload['quotes']} missing={payload['missing']}")
    return 1 if payload["missing"] else 0


if __name__ == "__main__":
    sys.exit(main())
