#!/usr/bin/env python3
"""Мутационная проверка валидатора RUN-0094 (issue #484): каждая правка отчёта даёт FAIL.

Отчёт временно изменяется и восстанавливается побайтно.

    MANGO_BA_RUNTIME_MAIN=/tmp/runtime python3 experiments/issue_484/mutation_check.py
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / "runs/2026/RUN-0094/outputs/L0-feasibility-assessment-1199-2.md"
VALIDATOR = ROOT / "scripts/validate_issue_484_run.py"


def mutate_row(text: str, prefix: str, old: str, new: str) -> str:
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if line.startswith(prefix) and old in line:
            lines[i] = line.replace(old, new, 1)
            return "\n".join(lines)
    raise SystemExit("строка не найдена: %r" % prefix)


ROW1 = "| 1 | Компания участник конкурса"
SLA12 = "| 1.2. | Система должна обеспечивать на своей стороне"

MUTATIONS = {
    "текст требования п. 1": lambda t: mutate_row(t, ROW1, "Компания участник", "Компания-участник"),
    "вердикт вне шкалы (п. 1)": lambda t: mutate_row(t, ROW1, "<br>Да \\|", "<br>Возможно \\|"),
    "непустая средняя часть колонки 3 (п. 1)":
        lambda t: mutate_row(t, ROW1, "<br>Да \\| \\|", "<br>Да \\| Реализован \\|"),
    "удалён разделитель «Лист 2 из 2»": lambda t: t.replace("### Лист 2 из 2", "### Лист 2", 1),
    "непустая колонка 6 (п. 1)": lambda t: mutate_row(t, ROW1, "(п. 9.6). |  |", "(п. 9.6). | x |"),
    "снята пометка «Нет данных» (SLA п. 1.2)":
        lambda t: mutate_row(t, SLA12, "| Нет данных.<br>Аудит:", "| Аудит:"),
    "сноска без парной цитаты (п. 1)": lambda t: mutate_row(t, ROW1, " [1] «", " [9] «"),
}

original = REPORT.read_bytes()
failed = 0
try:
    for name, mutate in MUTATIONS.items():
        mutated = mutate(original.decode("utf-8"))
        assert mutated != original.decode("utf-8"), name
        REPORT.write_text(mutated, encoding="utf-8")
        result = subprocess.run([sys.executable, str(VALIDATOR)], capture_output=True, text=True)
        verdict = "FAIL (ожидаемо)" if result.returncode else "PASS (валидатор пропустил!)"
        failed += result.returncode == 0
        print("%-45s %s" % (name, verdict))
finally:
    REPORT.write_bytes(original)
print("мутаций: %d; пропущено валидатором: %d" % (len(MUTATIONS), failed))
sys.exit(1 if failed else 0)
