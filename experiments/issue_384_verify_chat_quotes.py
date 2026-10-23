"""Сверка реестра цитат чата «Проект: СПЛИТ (БА)» с экспортом (issue #384).

Каждая строка реестра ``experiments/issue_384/chat-2026-10-22-23-register.md``
должна дословно (после нормализации пробелов и markdown-выделения) встречаться
в тексте заявленной реплики линейной ветки экспорта, а реплика — попадать в
окно задачи 21–23.10.2026 (МСК). Роль и время UTC строки реестра сверяются с
репликой. SHA-256 и размер экспорта сверяются с провенансом реестра.

Результат пишется в ``experiments/issue_384/chat-quote-check.json``: ID строки,
номер реплики, найдено ли, в каких репликах окна цитата встречается ещё и
SHA-256 нормализованной цитаты. Текст экспорта в файл не попадает.

Запуск (экспорт — недоверенные данные, только с ``-I``)::

    python3 -I experiments/issue_384_verify_chat_quotes.py <chat-export.json>
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from chat_export_to_markdown import answer_text, linear_chain  # noqa: E402

REGISTER = ROOT / "experiments" / "issue_384" / "chat-2026-10-22-23-register.md"
OUT = ROOT / "experiments" / "issue_384" / "chat-quote-check.json"
MSK = datetime.timezone(datetime.timedelta(hours=3))
WINDOW = (
    datetime.datetime(2026, 10, 21, tzinfo=MSK).timestamp(),
    datetime.datetime(2026, 10, 24, tzinfo=MSK).timestamp(),
)
ROLES = {"БА": "user", "модель": "assistant"}
ROW = re.compile(
    r"^\| (?P<id>Ч-\d{2}) \| (?P<turn>\d+) \| (?P<utc>[\d-]+ [\d:]+) \| (?P<role>[^|]+?) "
    r"\| (?P<quote>[^|]+?) \| [^|]+ \|$"
)
SHA = re.compile(r"^\| SHA-256 \| `([0-9a-f]{64})` \|$", re.M)
SIZE = re.compile(r"^\| Размер \| (\d+) байт \|$", re.M)


def normalize(text: str) -> str:
    text = text.replace("*", "").replace("`", "").replace(" ", " ")
    return re.sub(r"\s+", " ", text).strip()


def register_rows(text: str) -> list[dict]:
    rows = []
    for number, line in enumerate(text.splitlines(), 1):
        match = ROW.match(line)
        if match:
            rows.append({**match.groupdict(), "turn": int(match["turn"]), "line": number})
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("export", type=Path)
    parser.add_argument("--register", type=Path, default=REGISTER)
    parser.add_argument("--output", type=Path, default=OUT)
    args = parser.parse_args()

    raw = args.export.read_bytes()
    register = args.register.read_text(encoding="utf-8")
    sha = hashlib.sha256(raw).hexdigest()
    errors = []
    if SHA.search(register) is None or SHA.search(register)[1] != sha:
        errors.append(f"SHA-256 экспорта {sha} не совпадает с провенансом реестра")
    if SIZE.search(register) is None or int(SIZE.search(register)[1]) != len(raw):
        errors.append(f"размер экспорта {len(raw)} не совпадает с провенансом реестра")

    chain = linear_chain(json.loads(raw.decode("utf-8")))
    window = [i for i, m in enumerate(chain) if WINDOW[0] <= (m.get("timestamp") or 0) < WINDOW[1]]
    texts = {i: normalize(answer_text(chain[i])) for i in window}
    rows = register_rows(register)
    if not rows:
        errors.append("в реестре нет строк Ч-NN")
    results = []
    for row in rows:
        needle = normalize(row["quote"])
        turn = row["turn"]
        message = chain[turn] if turn < len(chain) else {}
        utc = datetime.datetime.fromtimestamp(message.get("timestamp") or 0, datetime.timezone.utc)
        checks = {
            "in_window": turn in texts,
            "role": ROLES.get(row["role"]) == message.get("role"),
            "utc": utc.strftime("%Y-%m-%d %H:%M:%S") == row["utc"],
            "quote": turn in texts and needle in texts[turn],
        }
        results.append({
            "id": row["id"],
            "line": row["line"],
            "turn": turn,
            **checks,
            "found_turns": [i for i in window if needle in texts[i]],
            "sha256": hashlib.sha256(needle.encode("utf-8")).hexdigest(),
        })
        failed = [name for name, ok in checks.items() if not ok]
        if failed:
            errors.append(f"{row['id']} (р. {turn}, L{row['line']}): не прошло {', '.join(failed)}")
    ids = [row["id"] for row in rows]
    if len(ids) != len(set(ids)):
        errors.append("ID строк реестра повторяются")

    report = {
        "export_sha256": sha,
        "export_bytes": len(raw),
        "chain_turns": len(chain),
        "window_turns": [window[0], window[-1]] if window else [],
        "window_count": len(window),
        "rows": len(results),
        "ok": not errors,
        "results": results,
    }
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    print(f"rows={len(results)} window={report['window_turns']} ok={report['ok']}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
