#!/usr/bin/env python3
"""Валидатор шаблонов задач категории `runs` (issue #323).

Что проверяется
---------------
1. Оба шаблона существуют и лежат в `.github/ISSUE_TEMPLATE/` с расширением
   `.yml` — GitHub считает Issue Forms только `.yml`/`.yaml`; `.md` в этом
   каталоге трактуется как легаси-шаблон Markdown без полей формы.
2. YAML валиден и содержит обязательные ключи Issue Forms: `name`,
   `description`, `body`; `labels` — предвыбранные метки прогона.
3. Каждый блок `body` имеет разрешённый `type`, поля с вводом — уникальный `id`
   и `attributes.label`; у `dropdown`/`checkboxes` непустой список `options`.
4. У всех `textarea` есть `placeholder` — требование issue #323 (подсказка,
   куда прикладывать файлы и что писать руками).
5. Ключевые поля описания процесса и цели анализа остаются `textarea`, а не
   `dropdown`: таксономия процессов БА не формализована, жёсткие списки
   запрещены постановкой.

Парсер YAML
-----------
В CI (`.github/workflows/validate.yml`) стоит голый `setup-python` без
установки зависимостей, поэтому PyYAML может отсутствовать. Валидатор
разбирает подмножество YAML сам; если PyYAML всё же доступен, результаты
сверяются между собой — расхождение считается ошибкой.

Запуск: ``python3 scripts/validate_issue_323_issue_forms.py``
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = ROOT / ".github" / "ISSUE_TEMPLATE"

ALLOWED_TYPES = {"markdown", "input", "textarea", "dropdown", "checkboxes"}

#: Поля, которые постановка требует держать свободным текстом.
FREEFORM_FIELDS = {"process_description", "analysis_goal"}

#: Шаблон -> обязательные `id` полей (issue #323, «Контракты задачи»).
EXPECTED = {
    "run-execution.yml": {
        "labels": {"runs", "execution"},
        "ids": {"run_title", "process_description", "inputs", "constraints", "labels"},
    },
    "run-statistics.yml": {
        "labels": {"runs", "statistics"},
        "ids": {"run_title", "task_reference", "chat_exports", "analysis_goal", "labels"},
    },
}


# --------------------------------------------------------------------------
# Минимальный разбор YAML: блочные отображения, списки, скаляры и `|`-блоки.
# --------------------------------------------------------------------------


def _scalar(raw: str):
    text = raw.strip()
    if len(text) >= 2 and text[0] == text[-1] and text[0] in "\"'":
        return text[1:-1]
    if text in ("true", "false"):
        return text == "true"
    if text.lstrip("-").isdigit():
        return int(text)
    return text


def _lines(text: str) -> list[tuple[int, int, str]]:
    """(номер строки, отступ, содержимое) без комментариев и пустых строк."""
    out = []
    for number, raw in enumerate(text.splitlines(), start=1):
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        out.append((number, len(raw) - len(raw.lstrip(" ")), stripped))
    return out


def _block_scalar(raw_lines: list[str], start: int, indent: int) -> tuple[str, int]:
    """Читает `|`-блок: все строки с отступом больше `indent`."""
    body, index = [], start
    while index < len(raw_lines):
        line = raw_lines[index]
        if line.strip() and len(line) - len(line.lstrip(" ")) <= indent:
            break
        body.append(line)
        index += 1
    while body and not body[-1].strip():
        body.pop()
    if not body:
        return "", index
    pad = min(len(l) - len(l.lstrip(" ")) for l in body if l.strip())
    return "\n".join(l[pad:] for l in body) + "\n", index


def parse_yaml(text: str):
    raw_lines = text.splitlines()
    items = _lines(text)

    def parse(pos: int, indent: int):
        if items[pos][2].startswith("- "):
            result, index = [], pos
            while index < len(items):
                number, own_indent, content = items[index]
                if own_indent < indent or not content.startswith("- "):
                    break
                rest = content[2:].strip()
                if ":" in rest and not rest.startswith(("|", ">")):
                    # элемент-отображение: разбираем его как блок с виртуальным
                    # отступом на позиции первого ключа
                    inner_indent = own_indent + 2
                    items[index] = (number, inner_indent, rest)
                    value, index = parse(index, inner_indent)
                else:
                    result.append(_scalar(rest))
                    index += 1
                    continue
                result.append(value)
            return result, index

        mapping, index = {}, pos
        while index < len(items):
            number, own_indent, content = items[index]
            if own_indent < indent:
                break
            if own_indent > indent:
                raise ValueError(f"строка {number}: неожиданный отступ")
            if ":" not in content:
                raise ValueError(f"строка {number}: ожидалась пара ключ: значение")
            key, _, rest = content.partition(":")
            key, rest = key.strip().strip("\"'"), rest.strip()
            index += 1
            if rest in ("|", "|-", ">"):
                value, cursor = _block_scalar(raw_lines, number, own_indent)
                if rest == "|-":
                    value = value.rstrip("\n")
                while index < len(items) and items[index][0] <= cursor:
                    index += 1
            elif rest:
                value = _scalar(rest)
            elif index < len(items) and items[index][1] >= own_indent:
                value, index = parse(index, items[index][1])
            else:
                value = None
            mapping[key] = value
        return mapping, index

    if not items:
        return {}
    return parse(0, items[0][1])[0]


# --------------------------------------------------------------------------
# Проверки
# --------------------------------------------------------------------------


def check_template(name: str, spec: dict, errors: list[str]) -> None:
    path = TEMPLATE_DIR / name
    if not path.is_file():
        errors.append(f"{path.relative_to(ROOT)}: файл отсутствует")
        return
    errors.extend(check_text(path.relative_to(ROOT), path.read_text(encoding="utf-8"), spec))


def check_text(where, text: str, spec: dict) -> list[str]:
    """Проверки над содержимым шаблона; вынесены ради тестов на синтетике."""
    errors: list[str] = []
    try:
        data = parse_yaml(text)
    except ValueError as exc:
        errors.append(f"{where}: YAML не разобран — {exc}")
        return errors

    try:  # перекрёстная сверка, когда PyYAML доступен (локально)
        import yaml  # noqa: PLC0415
    except ImportError:
        pass
    else:
        try:
            reference = yaml.safe_load(text)
        except yaml.YAMLError as exc:
            errors.append(f"{where}: PyYAML не разобрал файл — {exc}")
            return errors
        if reference != data:
            errors.append(f"{where}: разбор PyYAML и встроенного парсера расходится")

    if not isinstance(data, dict):
        errors.append(f"{where}: корень должен быть отображением")
        return errors

    for key in ("name", "description", "body"):
        if not data.get(key):
            errors.append(f"{where}: отсутствует обязательный ключ {key!r}")

    labels = set(data.get("labels") or [])
    missing_labels = spec["labels"] - labels
    if missing_labels:
        errors.append(f"{where}: не проставлены метки {sorted(missing_labels)}")

    body = data.get("body")
    if not isinstance(body, list):
        errors.append(f"{where}: 'body' должен быть списком блоков")
        return errors

    seen_ids: set[str] = set()
    for position, block in enumerate(body, start=1):
        label = f"{where}: блок #{position}"
        if not isinstance(block, dict):
            errors.append(f"{label}: должен быть отображением")
            continue
        block_type = block.get("type")
        if block_type not in ALLOWED_TYPES:
            errors.append(f"{label}: недопустимый type={block_type!r}")
            continue
        attributes = block.get("attributes")
        if not isinstance(attributes, dict):
            errors.append(f"{label}: отсутствует 'attributes'")
            continue

        if block_type == "markdown":
            if not attributes.get("value"):
                errors.append(f"{label}: markdown без 'value'")
            continue

        block_id = block.get("id")
        if not block_id:
            errors.append(f"{label}: поле без 'id'")
        elif block_id in seen_ids:
            errors.append(f"{label}: дублирующийся id={block_id!r}")
        else:
            seen_ids.add(block_id)

        if not attributes.get("label"):
            errors.append(f"{label}: поле без 'attributes.label'")

        if block_type == "textarea" and not attributes.get("placeholder"):
            errors.append(f"{label} (id={block_id!r}): textarea без 'placeholder'")

        if block_type in ("dropdown", "checkboxes") and not attributes.get("options"):
            errors.append(f"{label} (id={block_id!r}): {block_type} без 'options'")

        if block_id in FREEFORM_FIELDS and block_type != "textarea":
            errors.append(
                f"{label} (id={block_id!r}): должно быть 'textarea' — жёсткие списки "
                "процессов запрещены до формализации таксономии (issue #323)"
            )

    missing_ids = spec["ids"] - seen_ids
    if missing_ids:
        errors.append(f"{where}: отсутствуют обязательные поля {sorted(missing_ids)}")
    return errors


def main() -> int:
    errors: list[str] = []
    for name, spec in EXPECTED.items():
        check_template(name, spec, errors)

    stray = sorted(p.name for p in TEMPLATE_DIR.glob("run-*.md"))
    if stray:
        errors.append(
            ".github/ISSUE_TEMPLATE: шаблоны прогонов в .md не распознаются как "
            f"Issue Forms: {stray}"
        )

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"Issue forms validation failed with {len(errors)} error(s).", file=sys.stderr)
        return 1

    print("Issue forms validation passed (issue #323).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
