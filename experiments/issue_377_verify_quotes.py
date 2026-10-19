"""Сверка цитат золотого набора RUN-0074 с экспортом чата задачи 1110 (issue #377).

Каждая цитата разметки (:mod:`experiments.issue_377_golden_data`) должна
дословно (после нормализации пробелов и markdown-выделения) встречаться в
тексте заявленной реплики экспорта:

- ``quote`` инцидента — в реплике ``turn``;
- ``uq`` инцидента — в реплике БА ``det_turn``, ``rule_uq`` — в ``rule_turn``;
- цитаты позитивных кейсов и критериев успеха — в своих репликах.

Результат пишется в ``experiments/issue_377/quote-check.json``: номер реплики,
найдено ли, в каких репликах цитата встречается ещё и SHA-256 нормализованной
цитаты. Текст экспорта и ссылки на вложения в файл не попадают.

Запуск (экспорт — недоверенные данные, только с ``-I``)::

    python3 -I experiments/issue_377_verify_quotes.py <chat-export-1110.json>
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
sys.path.insert(0, str(ROOT / "experiments"))

from chat_export_to_markdown import answer_text, linear_chain  # noqa: E402
from issue_377_golden_data import NEGATIVES, SUCCESS_CRITERIA, numbered_incidents  # noqa: E402

OUT = ROOT / "experiments" / "issue_377" / "quote-check.json"


def normalize(text: str) -> str:
    text = text.replace("*", "").replace("`", "").replace(" ", " ")
    return re.sub(r"\s+", " ", text).strip()


def check(texts: list[str], turn: int | None, quote: str, kind: str, ref: str) -> dict:
    needle = normalize(quote)
    found = [index for index, text in enumerate(texts) if needle and needle in text]
    return {
        "ref": ref,
        "kind": kind,
        "turn": turn,
        "found": turn in found,
        "found_turns": found,
        "sha256": hashlib.sha256(needle.encode("utf-8")).hexdigest(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("export", type=Path)
    parser.add_argument("--output", type=Path, default=OUT)
    args = parser.parse_args()

    chain = linear_chain(json.loads(args.export.read_text(encoding="utf-8")))
    texts = [normalize(answer_text(message)) for message in chain]
    rows = []
    for row in numbered_incidents():
        rows.append(check(texts, row["turn"], row["quote"], "incident", row["id"]))
        if row["uq"]:
            rows.append(check(texts, row["det_turn"], row["uq"], "incident-uq", row["id"]))
        if row["rule_uq"]:
            rows.append(check(texts, row["rule_turn"], row["rule_uq"], "incident-rule", row["id"]))
    for index, row in enumerate(NEGATIVES, 1):
        ref = f"N-{index:02d}"
        rows.append(check(texts, row["turn"], row["quote"], "negative", ref))
        if row["uq"]:
            rows.append(check(texts, row["uq_turn"], row["uq"], "negative-uq", ref))
    for row in SUCCESS_CRITERIA:
        rows.append(check(texts, row["turn"], row["uq"], "success", row["id"]))

    missing = [row for row in rows if not row["found"]]
    payload = {
        "export_sha256": hashlib.sha256(args.export.read_bytes()).hexdigest(),
        "messages": len(chain),
        "checked": len(rows),
        "missing": len(missing),
        "rows": rows,
    }
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for row in missing:
        print(f"MISSING {row['ref']} {row['kind']} turn={row['turn']} also={row['found_turns']}")
    print(f"checked={len(rows)} missing={len(missing)} -> {args.output.relative_to(ROOT)}")
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
