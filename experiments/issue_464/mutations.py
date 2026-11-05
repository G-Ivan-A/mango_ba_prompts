#!/usr/bin/env python3
"""Мутации: каждая должна ронять валидатор issue #464; файл восстанавливается.

Запуск: python3 experiments/issue_464/mutations.py > experiments/issue_464/mutations.log
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
S0 = "prompts/bcreq-constitution-governance-oneshot.md"
SA = "prompts/drafts/bcreq-intake-questionnaire-stepwise.md"
S1 = "prompts/bcreq-context-understanding-stepwise.md"
S = "standards/bcreq-sections/"
B = "pr-ops/BACKLOG.md"
PAGE = "site/index.html"
KIT = "site/data/test-kit.json"
CATALOG = "standards/bcreq-manual-classes/catalog.json"
M = [
    (SA, "какие 1–2 аналогичных продукта Mango взять опорой", "какой API изучить"),
    (S1, "и не задаёт границу функциональности", "и задаёт границу функциональности"),
    (S + "03-functional-requirements.md", "публичный API не\nзадаёт", "публичный API\nзадаёт"),
    (CATALOG, '"fields_changed_in": "issue #464"', '"fields_changed_in": "issue #000"'),
    (S0, "Не выводи её: БА уже вставил этот промпт в чат.", "Выведи её в чат."),
    (S0, "**На этом шаге запрещено:** выводить конституцию или каркас; писать разделы,", "**На этом шаге запрещено:** ничего;"),
    (S0, "Попроси ввести следующий промпт", "Продолжай без остановки"),
    (S0, "ЧТ-1 | Конституция предназначена модели и в чат не выводится", "ЧТ-1 | Конституцию можно выводить"),
    (SA, "2. Сколько операторов работает?", "2. Как дела?"),
    (SA, "шаг можно пропустить", "шаг обязателен"),
    (SA, "| Раздел 5, структура ОРР | C4 | TM Forum ODA или другой по ссылке |", "| Раздел 5 | C4 | — |"),
    (SA, "mode: by-test", "mode: published"),
    (S1, "**Порядок: сбор → интерпретация → фиксация.**", "**Порядок: сразу разделы.**"),
    (S1, "*Фиксация*", "*Сбор данных*", -1),
    (S1, "Р2: неясное не выдумывай", "Р2: неясное додумай"),
    (S + "01-glossary.md", "### Пользователь и Оператор", "### Роли"),
    (S + "02-business-context.md", "### Проверка исполнимости требования", "### Проверка"),
    (S + "02-business-context.md", "| **Частично** |", "| Частично |"),
    (S + "02-business-context.md", "### Однозначность границ", "### Границы"),
    (S + "02-business-context.md", "**Что не входит в 2.4.1 и 2.4.2.**", "**Прочее.**"),
    (S + "02-business-context.md", "Стейкхолдеры всегда: Заказчик и Продуктовая команда", "Стейкхолдеры при двух продуктах", -1),
    (S + "03-functional-requirements.md", "## Необходимые и достаточные ФТ: определение", "## Состав ФТ"),
    (S + "05-solution-description.md", "Раздел 5 **не строится** по блокам ФТ", "Раздел 5 строится по блокам ФТ"),
    (S + "05-solution-description.md", "Номера пунктов не зависят от номеров ФТ", "Номера пунктов равны номерам ФТ"),
    (S + "05-solution-description.md", "Это не архитектура и не системный анализ", "Это архитектура"),
    (PAGE, 'class="standard-card v2-card standards-industry"', 'class="standard-card v2-card"'),
    (PAGE, 'href="#standards?section=9" data-standard-target="9"', 'href="#standards" data-standard-target="8"', -1),
    (PAGE, "<h3>Как пишем</h3>", "<h3>Термины Заказчика и БА переносятся дословно</h3>"),
    ("site/app.js", '9: "standard-industry"', '9: "standard-8"'),
    (KIT, '"version": "0.8"', '"version": "0.7"'),
    (KIT, '"step": "Ш-А Анкета"', '"step": "Анкета"'),
    ("site/data/stats.json", "2.7.0", "2.6.0"),
    ("CHANGELOG.md", "версия сайта 2.7.0", "версия сайта 2.6.0", -1),
    (B, "| **Р-21** |", "| Р-21 |"),
    (B, "**Движение по цепочке (на 2026-11-05, issue #464).**", "**Цепочка.**"),
    (B, "| BL-235 | [Поток CS", "| BL-999 | [Поток CS"),
    (B, "деплой 2.7.0, повторный аудит", "деплой 2.6.0, повторный аудит"),
    ("pr-ops/backlog-repository.md", "### BL-236. ", "### BL-999. "),
    ("pr-ops/backlog-ba-model.md", "### BL-175. ", "### BL-998. "),
]


def run():
    return subprocess.run(
        [sys.executable, "scripts/validate_issue_464_a_in.py"],
        cwd=ROOT, capture_output=True, text=True, timeout=60,
    )


def main():
    if run().returncode:
        raise SystemExit("база не проходит")
    alive = 0
    for item in M:
        path, old, new = item[0], item[1], item[2]
        count = item[3] if len(item) > 3 else 1
        file = ROOT / path
        source = file.read_bytes()
        text = source.decode("utf-8")
        if old not in text:
            raise SystemExit(f"нет цели мутации: {path}: {old}")
        file.write_text(text.replace(old, new, count), encoding="utf-8")
        try:
            killed = run().returncode != 0
        finally:
            file.write_bytes(source)
        alive += not killed
        print(f"{'убита' if killed else 'ЖИВА '} | {path} | {old[:60]}")
    if run().returncode:
        raise SystemExit("после мутаций база не восстановилась")
    print(f"итого: {len(M)}, живых: {alive}")
    return 1 if alive else 0


if __name__ == "__main__":
    raise SystemExit(main())
