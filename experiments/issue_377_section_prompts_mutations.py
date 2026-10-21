#!/usr/bin/env python3
"""Мутационная проверка scripts/validate_issue_377_section_prompts.py (issue #377).

Каждая порча аналитического файла должна дать FAIL с ожидаемым сообщением; файл
восстанавливается после каждой мутации. Запуск:
``python3 experiments/issue_377_section_prompts_mutations.py``
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/analysis/2026-10-20-bcreq-fr-section-prompts.md"
ROLE = "Ты — бизнес-аналитик. Готовишь"
COMMON_RULE = "Перед ответом текст сверяется с ЖУРНАЛОМ РЕШЕНИЙ БА."

# (название, что заменить, на что, какое вхождение: 0 — первое, -1 — последнее, None — все, ожидаемый фрагмент FAIL)
MUTATIONS = [
    ("удалено правило Б3.5", "Б3.5. Одно ФТ", "Одно ФТ", 0, "нет правил ['Б3.5']"),
    ("общая часть в промпте в) изменена", COMMON_RULE, "Перед ответом текст сверяется.", -1,
     "c): общая часть не входит дословно"),
    ("лишнее правило В4.10", "В4.9. Новый пункт", "В4.10. Лишнее.\nВ4.9. Новый пункт", 0,
     "правила вне RULES скрипта ['В4.10']"),
    ("методология в роли всех промптов", ROLE, "Ты — бизнес-аналитик (BABOK). Готовишь", None,
     "в роли методология / экспертиза ['BABOK']"),
    ("таблица статистики изменена руками", "| **Итого** |  |  | 594 |", "| **Итого** |  |  | 595 |", 0,
     "таблицы статистики устарели"),
    ("нет строки П7 в §5.5", "| П7 |", "| П-7 |", -1, "правило П7: нет строки"),
    ("нет блока issue", "<!-- section-prompts:issue -->", "<!-- section-prompts:isue -->", 0,
     "нет блока section-prompts:issue"),
    ("нет analysis-subtype", "analysis-subtype: options\n", "", 0, "нет поля analysis-subtype"),
    ("подтип вне словаря стандарта", "analysis-subtype: options", "analysis-subtype: problem", 0,
     "вне словаря"),
    ("нет секции Recommendations", "## 8. Recommendations", "## 8. Рекомендации", 0,
     "нет секции «Recommendations»"),
]


def mutate(text: str, old: str, new: str, which) -> str:
    assert old in text, old
    if which is None:
        return text.replace(old, new)
    i = text.index(old) if which == 0 else text.rindex(old)
    return text[:i] + new + text[i + len(old):]


def main() -> int:
    original = DOC.read_text(encoding="utf-8")
    missed = 0
    try:
        for name, old, new, which, expected in MUTATIONS:
            DOC.write_text(mutate(original, old, new, which), encoding="utf-8")
            r = subprocess.run([sys.executable, "scripts/validate_issue_377_section_prompts.py"],
                               cwd=ROOT, capture_output=True, text=True)
            ok = r.returncode == 1 and expected in r.stdout
            missed += not ok
            print(f"{'caught' if ok else 'MISSED'}: {name}")
            if not ok:
                print(r.stdout)
    finally:
        DOC.write_text(original, encoding="utf-8")
    return 1 if missed else 0


if __name__ == "__main__":
    sys.exit(main())
