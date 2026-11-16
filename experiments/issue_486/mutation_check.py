#!/usr/bin/env python3
"""Мутационная проверка валидаторов RUN-0094 v2.0 (issues #484, #486): каждая правка отчёта
даёт FAIL хотя бы одного из `scripts/validate_issue_484_run.py` и
`scripts/validate_issue_486_run.py`. Отчёт временно изменяется и восстанавливается побайтно.

    MANGO_BA_RUNTIME_MAIN=/tmp/runtime python3 experiments/issue_486/mutation_check.py
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / "runs/2026/RUN-0094/outputs/L0-feasibility-assessment-1199-2.md"
VALIDATORS = [ROOT / "scripts/validate_issue_484_run.py", ROOT / "scripts/validate_issue_486_run.py"]


def row(text: str, pp: int) -> int:
    """Индекс строки таблицы отчёта с «№ пп» = pp (таблицы листов — после «### Лист»)."""
    lines = text.split("\n")
    start = next(i for i, line in enumerate(lines) if line.startswith("### Лист 1 из 2"))
    for i in range(start, len(lines)):
        if lines[i].startswith(f"| {pp} | "):
            return i
    raise SystemExit(f"строка № пп {pp} не найдена")


def edit(pp: int, old: str, new: str, count: int = 1):
    def mutate(text: str) -> str:
        lines = text.split("\n")
        i = row(text, pp)
        assert old in lines[i], (pp, old)
        lines[i] = lines[i].replace(old, new, count)
        return "\n".join(lines)
    return mutate


def drop(pp: int):
    def mutate(text: str) -> str:
        lines = text.split("\n")
        del lines[row(text, pp)]
        return "\n".join(lines)
    return mutate


def swap(a: int, b: int):
    def mutate(text: str) -> str:
        lines = text.split("\n")
        i, j = row(text, a), row(text, b)
        lines[i], lines[j] = lines[j], lines[i]
        return "\n".join(lines)
    return mutate


def merge(pp: int):
    """Склеить строку pp со следующей (два пункта перечня в одной строке), «№ пп» далее
    перенумеровать, чтобы мутация не ловилась одной лишь проверкой сквозной нумерации."""
    def mutate(text: str) -> str:
        lines = text.split("\n")
        i = row(text, pp)
        nxt = lines[i + 1].split(" | ")[2]
        cells = lines[i].split(" | ")
        cells[2] = cells[2] + "<br>" + nxt
        lines[i] = " | ".join(cells)
        del lines[i + 1]
        for k in range(i + 1, len(lines)):
            lines[k] = re.sub(r"^\| (\d+) \| ", lambda m: f"| {int(m.group(1)) - 1} | ", lines[k])
        return "\n".join(lines)
    return mutate


def ba(pp: int):
    """Заполнить колонку «Комментарий БА» (последняя ячейка строки)."""
    def mutate(text: str) -> str:
        lines = text.split("\n")
        i = row(text, pp)
        assert lines[i].endswith("|  |"), lines[i][-10:]
        lines[i] = lines[i][:-4] + "| согласовано |"
        return "\n".join(lines)
    return mutate


MUTATIONS = {
    "пропуск в «№ пп» (№ пп 3 → 30)": edit(3, "| 3 | ", "| 30 | "),
    "«№» исходника не повторён во фрагменте (№ пп 3)": edit(3, "| 3 | 1 | ", "| 3 |  | "),
    "«№» исходника изменён (№ пп 6: 3 → 4)": edit(6, "| 6 | 3 | ", "| 6 | 4 | "),
    "текст фрагмента изменён (№ пп 2)": edit(2, "Компания участник", "Компания-участник"),
    "строка-фрагмент удалена (№ пп 7)": drop(7),
    "строки переставлены (№ пп 6 и 7)": swap(6, 7),
    "два пункта перечня в одной строке (№ пп 6 + 7)": merge(6),
    "заголовок комплексного требования с оценкой (№ пп 5)":
        edit(5, "Оценка: <br> \\|", "Оценка: <br>Да \\|"),
    "диапазон заголовка сдвинут (№ пп 5: 6–12 → 6–11)": edit(5, "№ пп 6–12", "№ пп 6–11"),
    "строка-заголовок исходника с оценкой (№ пп 1)": edit(1, "Оценка: <br> \\|", "Оценка: <br>Да \\|"),
    "строка таблицы из 6 колонок (№ пп 2)": edit(2, "| 2 | 1 | ", "| 2 | "),
    "вердикт вне шкалы (№ пп 2)": edit(2, "<br>Да \\|", "<br>Возможно \\|"),
    "непустая средняя часть оценки (№ пп 2)": edit(2, "<br>Да \\| \\|", "<br>Да \\| Реализован \\|"),
    "непустая колонка «Комментарий БА» (№ пп 2)": ba(2),
    "сноска без парной цитаты (№ пп 3)": edit(3, " [2] [", " [7] ["),
    "удалён разделитель «Лист 2 из 2»": lambda t: t.replace("### Лист 2 из 2", "### Лист 2", 1),
}

def run() -> list[int]:
    return [subprocess.run([sys.executable, str(v)], capture_output=True, text=True).returncode
            for v in VALIDATORS]


if any(run()):
    raise SystemExit("исходный отчёт не проходит валидаторы — мутационная проверка не имеет смысла")
original = REPORT.read_bytes()
failed = 0
try:
    for name, mutate in MUTATIONS.items():
        mutated = mutate(original.decode("utf-8"))
        assert mutated != original.decode("utf-8"), name
        REPORT.write_text(mutated, encoding="utf-8")
        codes = run()
        caught = any(codes)
        failed += not caught
        print("%-55s %s %s" % (name, "FAIL (ожидаемо)" if caught else "PASS (валидаторы пропустили!)",
                               codes))
finally:
    REPORT.write_bytes(original)
print("мутаций: %d; пропущено валидаторами: %d" % (len(MUTATIONS), failed))
sys.exit(1 if failed else 0)
