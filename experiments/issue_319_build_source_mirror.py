#!/usr/bin/env python3
"""Строит зеркало исходных приложений ТЗ (#319) с добавленной колонкой анализа.

Требование Заказчика (комментарий к PR #322 от 2026-08-25): один из результирующих
артефактов обязан дословно воспроизвести структуру исходных .xls-приложений
(допустим один файл с разделением на таблицы) и добавить единственную колонку с
комментарием по результатам анализа исполнимости каждого требования.

Скрипт исключает ручной перенос: текст требований и ответы участника берутся
напрямую из .xls, а комментарий анализа — из уже согласованной матрицы
runs/2026/RUN-0057/outputs/L2-feasibility-matrix.md (сопоставление по дословному
тексту требования). Любая несопоставленная строка печатается в stderr и
попадает в вывод с явным маркером — молчаливых пропусков нет.

Запуск:

    pip install xlrd
    python3 experiments/issue_319_build_source_mirror.py \
        --xls 1._STT.xls 2._TTS.xls 3._NLU.xls 4._Dialogue.Manager.xls \
        --matrix runs/2026/RUN-0057/outputs/L2-feasibility-matrix.md \
        --out runs/2026/RUN-0057/outputs/L0-customer-form-with-assessment.md
"""

import argparse
import hashlib
import re
import sys
import unicodedata

import xlrd

GAP = "> ⚠️ **НЕДОСТАТОЧНО ДАННЫХ / ТРЕБУЕТСЯ УТОЧНЕНИЕ**"


def norm(text: str) -> str:
    """Ключ сопоставления: текст без пробелов, регистра и разделителей строк.

    NFC обязателен: в исходных .xls часть букв «й» записана как «и» + combining
    breve (U+0438 U+0306), тогда как в матрице стоит предсоставленный U+0439.
    """
    text = unicodedata.normalize("NFC", text.replace("<br>", " "))
    return re.sub(r"[\s ]+", "", text).lower()


def split_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def parse_matrix(path: str) -> dict[tuple[int, str], dict[str, str]]:
    """Читает L2-матрицу: (номер приложения, нормализованный текст) -> оценка."""
    result: dict[tuple[int, str], dict[str, str]] = {}
    appendix = 0
    for line in open(path, encoding="utf-8"):
        heading = re.match(r"^## Приложение № (\d)", line)
        if heading:
            appendix = int(heading.group(1))
            continue
        if appendix and line.startswith("|") and not line.startswith("| ---"):
            cells = split_row(line)
            if len(cells) != 6 or cells[0] in {"№", ""}:
                continue
            result[(appendix, norm(cells[1]))] = {
                "num": cells[0],
                "level": cells[3],
                "source": cells[4],
                "verdict": cells[5],
            }
    return result


def cell_to_md(value: str) -> str:
    """Дословный текст ячейки в markdown: переносы строк -> <br>, экранирование |."""
    value = value.replace("|", "\\|")
    return "<br>".join(part.strip() for part in value.splitlines()).strip()


def assessment(entry: dict[str, str] | None) -> str:
    if entry is None:
        return (
            f"{GAP}: строка не имеет оценки в матрице исполнимости "
            "(`L2-feasibility-matrix.md`) — требуется отдельный разбор"
        )
    level = entry["level"].replace("**", "").strip() or "—"
    parts = [f"**Уровень покрытия: {level}.**"]
    if entry["source"] and entry["source"] != "—":
        parts.append(f"Подтверждение: {entry['source']}.")
    parts.append(entry["verdict"])
    return " ".join(parts)


def is_group_header(requirement: str, comment: str) -> bool:
    return requirement.rstrip().endswith(":") and not comment.strip()


def render(xls_paths: list[str], matrix: dict, out) -> int:
    unmatched = 0
    for index, path in enumerate(xls_paths, start=1):
        data = open(path, "rb").read()
        book = xlrd.open_workbook(path)
        for sheet in book.sheets():
            rows = [
                [str(sheet.cell_value(r, c)).strip() for c in range(sheet.ncols)]
                for r in range(sheet.nrows)
            ]
            # шапка листа: строки до строки с заголовком таблицы «№ | Требование | ...»
            header_row = next(
                (i for i, row in enumerate(rows) if "№" in row), None
            )
            if header_row is None:
                print(f"нет строки заголовка таблицы в {path}", file=sys.stderr)
                return -1
            title_lines = [
                " ".join(c for c in row if c) for row in rows[:header_row]
            ]
            title_lines = [line for line in title_lines if line]
            print(f"\n## Лист «{sheet.name.strip()}» — файл `{path.split('/')[-1]}`\n", file=out)
            print(
                f"Контрольные суммы файла: `md5:{hashlib.md5(data).hexdigest()}`, "
                f"`sha256:{hashlib.sha256(data).hexdigest()}`.\n",
                file=out,
            )
            print("Шапка листа (дословно):\n", file=out)
            for line in title_lines:
                print(f"> {line}", file=out)
                print(">", file=out)
            header = [c for c in rows[header_row] if c]
            print("", file=out)
            print("| " + " | ".join(header + ["Комментарий по результатам анализа (RUN-0057)"]) + " |", file=out)
            print("| " + " | ".join(["---"] * (len(header) + 1)) + " |", file=out)
            for row in rows[header_row + 1:]:
                cells = [c for c in row if c] if any(row) else []
                if not cells:
                    continue
                # выравнивание по ширине шапки: пустые ячейки исходника сохраняются
                values = [c for c in row[1:1 + len(header)]]
                num, requirement = values[0], values[1]
                comment = values[2] if len(values) > 2 else ""
                if is_group_header(requirement, comment):
                    note = "Заголовок группы требований исходной формы — самостоятельной оценке не подлежит."
                else:
                    entry = matrix.get((index, norm(requirement)))
                    if entry is None:
                        unmatched += 1
                        print(
                            f"НЕ СОПОСТАВЛЕНО: приложение {index}, № {num}: {requirement[:60]!r}",
                            file=sys.stderr,
                        )
                    note = assessment(entry)
                print(
                    "| "
                    + " | ".join(
                        [cell_to_md(num), cell_to_md(requirement), cell_to_md(comment), note]
                    )
                    + " |",
                    file=out,
                )
    return unmatched


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--xls", nargs="+", required=True)
    parser.add_argument("--matrix", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument(
        "--preamble",
        help="файл с шапкой итогового документа (frontmatter и пояснения); "
             "содержимое копируется в начало без изменений",
    )
    args = parser.parse_args()

    matrix = parse_matrix(args.matrix)
    print(f"строк оценки в матрице: {len(matrix)}", file=sys.stderr)
    with open(args.out, "w", encoding="utf-8") as out:
        if args.preamble:
            out.write(open(args.preamble, encoding="utf-8").read())
        unmatched = render(args.xls, matrix, out)
    print(f"несопоставленных строк: {unmatched}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
