#!/usr/bin/env python3
"""Индекс источников hh.ru API для сносок отчёта L4 (issue #333).

Скрипт строит воспроизводимый указатель «operationId -> метод, путь, раздел,
глубокая ссылка в Redoc» по публичной OpenAPI-спецификации hh.ru. Ссылки такого
вида используются в разделе «Источники» каждого блока ФТ-XX отчёта
`runs/2026/RUN-0060/outputs/L4-combined-gap-report.md`, чтобы человек-ревьюер мог
перейти по сноске и сразу увидеть нужный метод.

Схема якоря Redoc (восстановлена по бандлу redoc.standalone.js и проверена на
внутренних ссылках самой спецификации, например
`#tag/Obshie-spravochniki/operation/get-locales`):

    https://api.hh.ru/openapi/redoc#tag/<slug(tag)>/operation/<operationId>

где slug — транслитерация charmap + удаление недопустимых символов +
схлопывание пробелов и дефисов в один дефис (регистр сохраняется).

Только стандартная библиотека Python 3. В CI не запускается.

Использование:
    python3 experiments/issue_333_hh_api_source_index.py --download --out /tmp/index.md
    python3 experiments/issue_333_hh_api_source_index.py --spec /tmp/hh-spec.yaml --json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import urllib.request

SPEC_URL = "https://api.hh.ru/openapi/specification/public"
REDOC_URL = "https://api.hh.ru/openapi/redoc"

# Подмножество charmap из redoc.standalone.js (кириллица + типографика).
CHARMAP = {
    "Ё": "Yo", "Ђ": "DJ", "Є": "Ye", "І": "I", "Ї": "Yi", "Ј": "J", "Љ": "LJ",
    "Њ": "NJ", "Ћ": "C", "Џ": "DZ", "А": "A", "Б": "B", "В": "V", "Г": "G",
    "Д": "D", "Е": "E", "Ж": "Zh", "З": "Z", "И": "I", "Й": "J", "К": "K",
    "Л": "L", "М": "M", "Н": "N", "О": "O", "П": "P", "Р": "R", "С": "S",
    "Т": "T", "У": "U", "Ф": "F", "Х": "H", "Ц": "C", "Ч": "Ch", "Ш": "Sh",
    "Щ": "Sh", "Ъ": "U", "Ы": "Y", "Ь": "", "Э": "E", "Ю": "Yu", "Я": "Ya",
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ж": "zh",
    "з": "z", "и": "i", "й": "j", "к": "k", "л": "l", "м": "m", "н": "n",
    "о": "o", "п": "p", "р": "r", "с": "s", "т": "t", "у": "u", "ф": "f",
    "х": "h", "ц": "c", "ч": "ch", "ш": "sh", "щ": "sh", "ъ": "u", "ы": "y",
    "ь": "", "э": "e", "ю": "yu", "я": "ya", "ё": "yo", "ђ": "dj", "є": "ye",
    "і": "i", "ї": "yi", "ј": "j", "љ": "lj", "њ": "nj", "ћ": "c", "ѝ": "u",
    "џ": "dz", "Ґ": "G", "ґ": "g", "Ғ": "GH", "ғ": "gh", "Қ": "KH", "қ": "kh",
    "Ң": "NG", "ң": "ng", "Ү": "UE", "ү": "ue", "Ұ": "U", "ұ": "u", "Һ": "H",
    "һ": "h", "Ә": "AE", "ә": "ae", "Ө": "OE", "ө": "oe", "’": "'", "…": "...",
}

_REMOVE = re.compile(r"""[^\w\s$*_+~.()'"!\-:@]+""", re.ASCII)
_COLLAPSE = re.compile(r"[\s-]+")

HTTP_METHODS = ("get", "put", "post", "delete", "patch", "head", "options")


def slugify(value: str) -> str:
    """Повторяет slugify из Redoc: charmap -> фильтр символов -> схлопывание."""
    translated = "".join(CHARMAP.get(char, char) for char in value)
    cleaned = _REMOVE.sub("", translated).strip()
    return _COLLAPSE.sub("-", cleaned)


def operation_anchor(tag: str, operation_id: str) -> str:
    return f"{REDOC_URL}#tag/{slugify(tag)}/operation/{operation_id}"


def tag_anchor(tag: str) -> str:
    return f"{REDOC_URL}#tag/{slugify(tag)}"


def load_spec_text(spec_path: str | None, download: bool) -> str:
    if download or spec_path is None:
        with urllib.request.urlopen(SPEC_URL, timeout=120) as response:
            return response.read().decode("utf-8")
    with open(spec_path, encoding="utf-8") as handle:
        return handle.read()


def parse_operations(spec_text: str) -> list[dict]:
    """Построчный разбор блока `paths:` спецификации.

    Спецификация hh.ru сериализована с постоянным отступом (2 пробела на
    уровень), поэтому полноценный YAML-парсер для этой задачи не нужен и
    зависимость от PyYAML не вводится.
    """
    operations: list[dict] = []
    in_paths = False
    path = method = operation_id = summary = None
    tags: list[str] = []
    in_tags = False

    def flush() -> None:
        if path and method and operation_id:
            operations.append(
                {
                    "path": path,
                    "method": method.upper(),
                    "operation_id": operation_id,
                    "summary": summary or "",
                    "tags": list(tags),
                }
            )

    for raw_line in spec_text.splitlines():
        if not in_paths:
            if raw_line.startswith("paths:"):
                in_paths = True
            continue
        if raw_line and not raw_line.startswith(" "):
            break  # блок paths закончился
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))

        if indent == 2 and stripped.endswith(":"):
            flush()
            path = stripped[:-1].strip().strip("'\"")
            method = operation_id = summary = None
            tags, in_tags = [], False
            continue
        if indent == 4:
            key = stripped.split(":", 1)[0].strip().strip("'\"")
            if key in HTTP_METHODS:
                flush()
                method, operation_id, summary = key, None, None
                tags, in_tags = [], False
            in_tags = False
            continue
        if indent == 6 and method:
            in_tags = False
            if stripped.startswith("operationId:"):
                operation_id = stripped.split(":", 1)[1].strip().strip("'\"")
            elif stripped.startswith("summary:"):
                summary = stripped.split(":", 1)[1].strip().strip("'\"")
            elif stripped == "tags:":
                in_tags = True
            continue
        if in_tags and stripped.startswith("- "):
            tags.append(stripped[2:].strip().strip("'\""))
            continue

    flush()
    return operations


def render_markdown(operations: list[dict], digest: str, size: int) -> str:
    lines = [
        "# Индекс источников hh.ru API (сноски отчёта L4)",
        "",
        f"- Спецификация: <{SPEC_URL}>",
        f"- SHA-256 спецификации: `{digest}`",
        f"- Размер: {size} байт",
        f"- Операций в выборке: {len(operations)}",
        "",
        "| Раздел (tag) | Метод | Путь | operationId | Ссылка для проверки |",
        "| --- | --- | --- | --- | --- |",
    ]
    for operation in sorted(
        operations, key=lambda item: (item["tags"][:1] or [""], item["path"])
    ):
        tag = operation["tags"][0] if operation["tags"] else ""
        anchor = operation_anchor(tag, operation["operation_id"]) if tag else ""
        lines.append(
            f"| {tag} | `{operation['method']}` | `{operation['path']}` | "
            f"`{operation['operation_id']}` | [{operation['summary'] or operation['operation_id']}]({anchor}) |"
        )
    return "\n".join(lines) + "\n"


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", help="путь к локальной копии спецификации (YAML)")
    parser.add_argument("--download", action="store_true", help="скачать спецификацию с api.hh.ru")
    parser.add_argument("--tag", action="append", help="оставить только указанные разделы (можно повторять)")
    parser.add_argument("--json", action="store_true", help="вывести JSON вместо Markdown")
    parser.add_argument("--out", help="файл для результата (по умолчанию stdout)")
    args = parser.parse_args(argv)

    spec_text = load_spec_text(args.spec, args.download)
    digest = hashlib.sha256(spec_text.encode("utf-8")).hexdigest()
    operations = parse_operations(spec_text)
    if args.tag:
        wanted = set(args.tag)
        operations = [op for op in operations if wanted & set(op["tags"])]

    if args.json:
        payload = {
            "spec_url": SPEC_URL,
            "sha256": digest,
            "size_bytes": len(spec_text.encode("utf-8")),
            "operations": [
                dict(op, anchor=operation_anchor(op["tags"][0], op["operation_id"]) if op["tags"] else "")
                for op in operations
            ],
        }
        text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    else:
        text = render_markdown(operations, digest, len(spec_text.encode("utf-8")))

    if args.out:
        with open(args.out, "w", encoding="utf-8") as handle:
            handle.write(text)
        print(f"written: {args.out} ({len(operations)} операций)", file=sys.stderr)
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
