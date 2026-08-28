#!/usr/bin/env python3
"""Аудит сносок отчёта L4 на пригодность для human review (issue #335).

Зачем
-----
Комментарий к issue #335 показал на примере сноски `^1` раздела 6.3: ссылка
формально ведёт в раздел Webhook API, но описанной в сноске структуры
`WebhookPayloadChatMessageCreated` на открывшейся странице человек не находит.
Прогон [RUN-0061](../runs/2026/RUN-0061/outputs/link-reference-contract-draft.md)
сформулировал причину в общем виде: требование «указывать раздел» держится
только тогда, когда оно проверяется машинно.

Скрипт делает такую проверку для отчёта
`runs/2026/RUN-0060/outputs/L4-combined-gap-report.md`:

1. разбирает все таблицы «Источники» и вытаскивает каждую сноску;
2. извлекает из сноски упомянутые идентификаторы (operationId, `METHOD /path`,
   имена схем, имена полей и параметров);
3. сверяет каждый идентификатор с закреплённой по SHA-256 OpenAPI-спецификацией
   hh.ru: существует ли операция, существует ли схема, есть ли у схемы такое
   поле, объявлен ли такой параметр у операции;
4. отдельно вычисляет **отображаемое имя** схемы: Redoc печатает `title`, а не
   имя схемы, поэтому сноска, называющая схему по имени из спецификации, может
   быть непроверяемой глазами даже при верной ссылке;
5. проверяет якорь ссылки: соответствует ли `#tag/<slug>/operation/<id>` тому
   разделу и той операции, которые названы в сноске.

Только стандартная библиотека Python 3. В CI не запускается: сетевой доступ и
1.2 МБ спецификации — не для валидатора. Регрессию по итогам аудита стережёт
`scripts/validate_issue_335_integration_artifacts.py`.

Использование:
    python3 experiments/issue_335_footnote_audit.py --download --json /tmp/audit.json
    python3 experiments/issue_335_footnote_audit.py --spec /tmp/hh-openapi.yaml
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import urllib.request
from pathlib import Path

SPEC_URL = "https://api.hh.ru/openapi/specification/public"
PINNED_SHA256 = "8ea1380bf87d7351cf2f977f9918bbdd03a26a6b9c9e95eb50f3d4ae080a7576"
REPORT = Path("runs/2026/RUN-0060/outputs/L4-combined-gap-report.md")

HTTP_METHODS = ("get", "put", "post", "delete", "patch", "head", "options")

_BACKTICKED = re.compile(r"`([^`]+)`")
_METHOD_PATH = re.compile(r"^(GET|PUT|POST|DELETE|PATCH|HEAD|OPTIONS)\s+(/\S*)$")
_ANCHOR = re.compile(r"#tag/([^/\s>]+)(?:/operation/([^/\s>]+))?")
_SCHEMA_NAME = re.compile(r"^[A-Z][A-Za-z0-9]+$")
_SECTION = re.compile(r"^### (\d+\.\d+)\.\s+Источники\s*$")
_FT_HEADING = re.compile(r"^## (\d+)\.\s+(.+)$")
_STATUS = re.compile(r"^[1-5][0-9X]{2}$")

# Ключевые слова OpenAPI и имена элементов спецификации, которые в сноске
# уместны как навигационная подсказка, а не как поле объекта.
SPEC_KEYWORDS = {
    "callbacks", "onData", "security: null", "maxItems: 1", "oneOf", "enum",
    "properties", "requestBody", "responses", "parameters", "schema",
}


# --------------------------------------------------------------------------
# Спецификация: точечный индекс вместо полноценного YAML-парсера.
# Спецификация hh.ru сериализована с постоянным отступом в 2 пробела, поэтому
# индексация по отступу однозначна (тот же приём, что в issue_333_*.py).
# --------------------------------------------------------------------------


def load_spec_text(spec_path: str | None, download: bool) -> str:
    if download or spec_path is None:
        with urllib.request.urlopen(SPEC_URL, timeout=180) as response:
            return response.read().decode("utf-8")
    return Path(spec_path).read_text(encoding="utf-8")


def index_block_names(spec_text: str, key: str) -> set[str]:
    """Имена верхнего уровня в `components.<key>` (например, examples)."""
    names: set[str] = set()
    inside = False
    for raw in spec_text.splitlines():
        if not inside:
            if raw == f"  {key}:":
                inside = True
            continue
        if raw and not raw.startswith("   "):
            break
        if len(raw) - len(raw.lstrip(" ")) == 4 and raw.strip().endswith(":"):
            names.add(raw.strip()[:-1].strip().strip("'\""))
    return names


def index_schemas(spec_text: str) -> dict[str, dict]:
    """`components.schemas` -> {имя: {title, properties, enum, line}}.

    В `properties` попадают имена свойств **любой глубины вложенности**: сноски
    отчёта ссылаются в том числе на вложенные поля (`chat_states.write_message_state`),
    и «поле не найдено» должно означать именно отсутствие, а не мелкость индекса.
    """
    schemas: dict[str, dict] = {}
    inside = False
    current: str | None = None
    # стек ключей по отступам: нужен, чтобы отличать `properties:` от `enum:`
    stack: dict[int, str] = {}
    for number, raw in enumerate(spec_text.splitlines(), start=1):
        if not inside:
            if raw == "  schemas:":
                inside = True
            continue
        if raw and not raw.startswith("   "):  # следующий ключ components.*
            break
        stripped = raw.strip()
        if not stripped:
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        if indent == 4 and stripped.endswith(":"):
            current = stripped[:-1].strip().strip("'\"")
            schemas[current] = {"title": None, "properties": {}, "enum": [], "line": number}
            stack = {}
            continue
        if current is None:
            continue
        if stripped.startswith("- "):
            parent = stack.get(max((key for key in stack if key < indent), default=-1))
            if parent == "enum":
                schemas[current]["enum"].append(stripped[2:].strip().strip("'\""))
            continue
        key = stripped.split(":", 1)[0].strip().strip("'\"")
        for level in [level for level in stack if level >= indent]:
            del stack[level]
        stack[indent] = key
        parent = stack.get(max((level for level in stack if level < indent), default=-1))
        if key == "title" and indent == 6:
            schemas[current]["title"] = stripped.split(":", 1)[1].strip().strip("'\"")
        elif parent == "properties":
            schemas[current]["properties"].setdefault(key, number)
    return schemas


def index_all_enum_values(spec_text: str) -> set[str]:
    """Все значения `enum:` документа, включая объявленные у параметров."""
    values: set[str] = set()
    enum_indent: int | None = None
    for raw in spec_text.splitlines():
        stripped = raw.strip()
        if not stripped:
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        if enum_indent is not None:
            if stripped.startswith("- ") and indent > enum_indent:
                values.add(stripped[2:].strip().strip("'\""))
                continue
            enum_indent = None
        if stripped == "enum:":
            enum_indent = indent
    return values


def index_parameters(spec_text: str) -> set[str]:
    """Имена параметров и заголовков из `components.parameters`."""
    names: set[str] = set()
    inside = False
    for raw in spec_text.splitlines():
        if not inside:
            if raw == "  parameters:":
                inside = True
            continue
        if raw and not raw.startswith("   "):
            break
        stripped = raw.strip()
        if stripped.startswith("name:"):
            names.add(stripped.split(":", 1)[1].strip().strip("'\""))
    return names


def index_operations(spec_text: str) -> dict[str, dict]:
    """`paths` -> {operationId: {path, method, tags, parameters, line}}."""
    operations: dict[str, dict] = {}
    inside = False
    path = method = operation_id = None
    tags: list[str] = []
    parameters: list[str] = []
    in_tags = False
    line_no = 0

    def flush() -> None:
        if path and method and operation_id:
            operations[operation_id] = {
                "path": path,
                "method": method.upper(),
                "tags": list(tags),
                "parameters": sorted(set(parameters)),
                "line": line_no,
            }

    for number, raw in enumerate(spec_text.splitlines(), start=1):
        if not inside:
            if raw.startswith("paths:"):
                inside = True
            continue
        if raw and not raw.startswith(" "):
            break
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        if indent == 2 and stripped.endswith(":"):
            flush()
            path = stripped[:-1].strip().strip("'\"")
            method = operation_id = None
            tags, parameters, in_tags = [], [], False
            continue
        if indent == 4:
            key = stripped.split(":", 1)[0].strip().strip("'\"")
            if key in HTTP_METHODS:
                flush()
                method, operation_id, line_no = key, None, number
                tags, parameters, in_tags = [], [], False
            in_tags = False
            continue
        if indent == 6 and method:
            in_tags = False
            if stripped.startswith("operationId:"):
                operation_id = stripped.split(":", 1)[1].strip().strip("'\"")
            elif stripped == "tags:":
                in_tags = True
            continue
        if in_tags and stripped.startswith("- "):
            tags.append(stripped[2:].strip().strip("'\""))
            continue
        # имена параметров объявлены как `- name: <...>` внутри parameters
        if method and stripped.startswith("- name:"):
            parameters.append(stripped.split(":", 1)[1].strip().strip("'\""))
        elif method and stripped.startswith("name:"):
            parameters.append(stripped.split(":", 1)[1].strip().strip("'\""))
    flush()
    return operations


# --------------------------------------------------------------------------
# Разбор отчёта
# --------------------------------------------------------------------------


def parse_footnotes(report_text: str) -> list[dict]:
    rows: list[dict] = []
    section = ft_title = None
    in_table = False
    for number, raw in enumerate(report_text.splitlines(), start=1):
        heading = _FT_HEADING.match(raw)
        if heading:
            ft_title = raw[3:].strip()
        match = _SECTION.match(raw)
        if match:
            section, in_table = match.group(1), True
            continue
        if raw.startswith("## "):
            in_table = False
        if not in_table or not raw.startswith("|"):
            continue
        cells = [cell.strip() for cell in raw.strip().strip("|").split("|")]
        if len(cells) < 4 or cells[0].startswith("---") or cells[0] == "Сноска":
            continue
        rows.append(
            {
                "section": section,
                "ft": ft_title,
                "line": number,
                "marker": cells[0].strip("`").lstrip("^"),
                "doc_section": cells[1],
                "description": cells[2],
                "url": cells[-1].strip("<>"),
            }
        )
    return rows


def classify_tokens(row: dict, spec: dict) -> dict:
    """Раскладывает backtick-токены сноски по видам и сверяет со спецификацией."""
    schemas, operations, examples = spec["schemas"], spec["operations"], spec["examples"]
    found = {
        "operations": [],
        "endpoints": [],
        "schemas": [],
        "examples": [],
        "notation": [],
        "enums": [],
        "fields": [],
        "unresolved": [],
    }
    for token in _BACKTICKED.findall(row["description"]):
        token = token.strip()
        if _METHOD_PATH.match(token):
            found["endpoints"].append(token)
            continue
        if token in operations:
            found["operations"].append(token)
            continue
        base = token.split(".", 1)[0]
        if base in schemas:
            found["schemas"].append(token)
            continue
        if token in examples:
            found["examples"].append(token)
            continue
        if any(char in token for char in '{}"') or ": " in token:
            found["notation"].append(token)
            continue
        if token in SPEC_KEYWORDS or _STATUS.match(token):
            found["notation"].append(token)
            continue
        if token in spec["enum_values"]:
            found["enums"].append(token)
            continue
        if re.fullmatch(r"[A-Z][A-Z0-9_]*", token):
            found["enums"].append(token)
            continue
        if _SCHEMA_NAME.match(token):
            found["unresolved"].append(token)
            continue
        found["fields"].append(token)
    return found


def resolve(row: dict, spec: dict) -> dict:
    schemas, operations = spec["schemas"], spec["operations"]
    tokens = classify_tokens(row, spec)
    problems: list[str] = []

    anchor = _ANCHOR.search(row["url"])
    anchor_tag = anchor.group(1) if anchor else None
    anchor_op = anchor.group(2) if anchor else None

    # 1. Ссылка ведёт на существующую операцию?
    if anchor_op is None:
        problems.append("anchor-not-operation")
    elif anchor_op not in operations:
        problems.append("anchor-unknown-operation")

    # 2. Схемы: существуют ли и как они подписаны в Redoc.
    schema_titles: dict[str, str | None] = {}
    for token in tokens["schemas"]:
        name = token.split(".", 1)[0]
        schema_titles[name] = schemas[name]["title"]
        tail = token.split(".")[1:]
        if tail and tail[0] not in schemas[name]["properties"]:
            problems.append(f"unknown-field:{token}")
    for token in tokens["unresolved"]:
        problems.append(f"unknown-identifier:{token}")

    # 3. Сноска описывает схему, а ссылка ведёт на операцию: чтобы увидеть
    #    схему, человеку нужен дополнительный переход внутри страницы.
    if tokens["schemas"] and not tokens["operations"] and not tokens["endpoints"]:
        problems.append("schema-only-footnote")

    # 4. Имя схемы не совпадает с тем, что печатает Redoc (`title`): человек
    #    ищет на странице строку, которой там нет.
    for name, title in schema_titles.items():
        if title and title != name:
            problems.append(f"title-differs:{name}->{title}")

    # 5. Enum-значения: существуют ли они хоть в одной схеме спецификации.
    all_enums = spec["enum_values"]
    for value in tokens["enums"]:
        if value not in all_enums:
            problems.append(f"enum-not-found:{value}")

    # 6. Поля сноски. Известными считаем свойства названных схем и параметры
    #    названной (или связанной якорем) операции. Если поле есть в
    #    спецификации, но не у названного объекта, читателю негде его искать.
    known_props: set[str] = set()
    for name in schema_titles:
        known_props |= set(schemas[name]["properties"])
    known_params: set[str] = set()
    for operation_id in tokens["operations"]:
        known_params |= set(operations[operation_id]["parameters"])
    if anchor_op in operations:
        known_params |= set(operations[anchor_op]["parameters"])
    known_params |= spec["parameters"]
    everywhere = {prop for item in schemas.values() for prop in item["properties"]}
    for field in tokens["fields"]:
        head = field.split(".", 1)[0].split("[", 1)[0]
        tail = field.replace("[]", "").split(".")[-1]
        if head in known_props or head in known_params:
            continue
        if head in known_props | known_params or tail in known_props:
            continue
        if head in everywhere:
            problems.append(f"field-not-located:{field}")
            continue
        if f"`{head}`" in spec["text"] or f"{head}:" in spec["text"]:
            problems.append(f"only-in-description:{field}")
            continue
        problems.append(f"field-not-found:{field}")

    return {
        **row,
        "tokens": tokens,
        "schema_titles": schema_titles,
        "anchor_tag": anchor_tag,
        "anchor_operation": anchor_op,
        "problems": problems,
    }


def build_index(spec_text: str) -> dict:
    """Собирает индекс спецификации: схемы, операции, примеры, параметры, enum."""
    spec = {
        "schemas": index_schemas(spec_text),
        "operations": index_operations(spec_text),
        "examples": index_block_names(spec_text, "examples"),
        "parameters": index_parameters(spec_text),
    }
    spec["enum_values"] = index_all_enum_values(spec_text)
    spec["text"] = spec_text
    return spec


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", help="локальная копия спецификации (YAML)")
    parser.add_argument("--download", action="store_true", help="скачать спецификацию")
    parser.add_argument("--report", default=str(REPORT), help="путь к отчёту L4")
    parser.add_argument("--json", help="файл для машинного результата")
    args = parser.parse_args(argv)

    spec_text = load_spec_text(args.spec, args.download)
    digest = hashlib.sha256(spec_text.encode("utf-8")).hexdigest()
    spec = build_index(spec_text)
    schemas, operations = spec["schemas"], spec["operations"]
    rows = parse_footnotes(Path(args.report).read_text(encoding="utf-8"))
    resolved = [resolve(row, spec) for row in rows]

    payload = {
        "spec_url": SPEC_URL,
        "sha256": digest,
        "sha256_matches_pinned": digest == PINNED_SHA256,
        "schemas_indexed": len(schemas),
        "operations_indexed": len(operations),
        "footnotes": len(resolved),
        "footnotes_with_problems": sum(1 for row in resolved if row["problems"]),
        "rows": resolved,
    }
    if args.json:
        Path(args.json).write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

    print(f"спецификация: sha256={digest} (совпадает с закреплённой: {payload['sha256_matches_pinned']})")
    print(f"схем в индексе: {len(schemas)}, операций: {len(operations)}")
    print(f"сносок: {len(resolved)}, из них с замечаниями: {payload['footnotes_with_problems']}")
    for row in resolved:
        if row["problems"]:
            print(f"  {row['section']} ^{row['marker']}: {'; '.join(row['problems'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
