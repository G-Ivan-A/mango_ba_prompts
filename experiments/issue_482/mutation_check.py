#!/usr/bin/env python3
"""Мутационная проверка валидатора RUN-0093 (issue #482): каждая правка отчёта даёт FAIL.

Отчёт временно изменяется и восстанавливается побайтно.

    MANGO_BA_RUNTIME_MAIN=/tmp/rt-main python3 experiments/issue_482/mutation_check.py
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / "runs/2026/RUN-0093/outputs/L0-feasibility-assessment-1140.md"
VALIDATOR = ROOT / "scripts/validate_issue_482_run.py"


def mutate_row(text: str, prefix: str, old: str, new: str) -> str:
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if line.startswith(prefix) and old in line:
            lines[i] = line.replace(old, new, 1)
            return "\n".join(lines)
    raise SystemExit("строка не найдена: %r" % prefix)


MUTATIONS = {
    "текст требования 1.4 ТЗ-2": lambda t: mutate_row(t, "| 1.4 | Голосовое", "3-4 раз", "3–4 раз"),
    "вердикт вне шкалы (1.4 ТЗ-2)": lambda t: mutate_row(t, "| 1.4 | Голосовое", "<br>Частично \\|", "<br>Возможно \\|"),
    "оценка у зачёркнутого 2.14.5": lambda t: mutate_row(t, "| ~~2.14.5.~~", "Оценка: <br> \\|", "Оценка: <br>Да \\|"),
    "удалён разделитель «Документ 2 из 2»": lambda t: t.replace("### Документ 2 из 2", "### Документ 2", 1),
    "непустая колонка 6 (4.2 ТЗ-2)": lambda t: mutate_row(t, "| 4.2 |", "подтверждена. |  |", "подтверждена. | x |"),
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
        print("%-40s %s" % (name, verdict))
finally:
    REPORT.write_bytes(original)
print("мутаций: %d; пропущено валидатором: %d" % (len(MUTATIONS), failed))
sys.exit(1 if failed else 0)
