#!/usr/bin/env python3
"""Считает статистику ПО ТРЕБОВАНИЯМ ТЗ #319 (не статистику прогонов).

Практика заводится по требованию Заказчика (комментарий к PR #322 от 2026-08-25)
и по образцу первичного исследования
https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/mango/2026-05-22-classification-tz.md
— там классифицируется корпус из 30 ТЗ, здесь единицей наблюдения становится
отдельное требование внутри одного ТЗ.

Источник данных — сгенерированное зеркало формы Заказчика
runs/2026/RUN-0057/outputs/L0-customer-form-with-assessment.md: в нём текст
требований дословно взят из .xls, а оценка — из матрицы L2. Скрипт ничего не
переформулирует, он только считает.

Метрики делятся на два класса, и это разделение принципиально:

* ДЕТЕРМИНИРОВАННЫЕ — считаются по тексту без интерпретации (число строк,
  лексические маркеры модальности, наличие числового порога, состав ответов
  участника, распределение уровней покрытия). Воспроизводимы полностью.
* ЭВРИСТИЧЕСКИЕ — тематический класс требования по словарю ключевых слов.
  Правила напечатаны в отчёте, приоритет применения фиксирован, но точность
  ограничена: требования Заказчика не нормализованы, одна строка часто несёт
  несколько тем. Числа этого блока — материал для выработки методологии, а не
  готовая статистика.

Запуск:

    python3 experiments/issue_319_requirements_statistics.py \
        --mirror runs/2026/RUN-0057/outputs/L0-customer-form-with-assessment.md \
        --out runs/2026/RUN-0057/outputs/L4-requirements-statistics.md
"""

import argparse
import re
from collections import Counter, defaultdict

# Тематические классы второго уровня для требований к голосовому роботу.
# Классификатор корпуса ТЗ (2026-05-22-classification-tz.md) относит все четыре
# приложения к одному классу A8 «Голосовой робот / voice-bot», поэтому для
# статистики ВНУТРИ модуля нужен второй уровень. Правила применяются по порядку:
# срабатывает первое совпадение, поэтому порядок — часть определения классов.
RULES: list[tuple[str, str, tuple[str, ...]]] = [
    ("R10", "Измеримые НФТ (пороги, время, точность)",
     ("не ниже", "не выше", "не более", "не менее", "rtf", "точность", "скорость обработки",
      "время обработки", "секунд", "сек ", "мс ", "%")),
    ("R06", "Интеграции и программный доступ (API, внешние системы)",
     ("api", "интеграц", "webhook", "внешн", "crm", "email", "e-mail", "смс", "sms")),
    ("R03", "Понимание смысла (NLU, интенты, сущности)",
     ("nlu", "интент", "намерен", "классифика", "семантическ", "сущност", "база знаний",
      "базы знаний", "тематик")),
    ("R02", "Синтез речи (TTS)",
     ("синтез", "озвуч", "диктор", "ударени", "интонац", "тембр", "темп речи", "громкост",
      "предзапис", "аудиофайл", "голос робота")),
    ("R01", "Распознавание речи (STT)",
     ("распознав", "транскриб", "asr", "акустическ", "шум", "словар", "лемматиз",
      "стоп-слов", "активационн")),
    ("R05", "Работа с данными диалога (филды, преобразования, переменные)",
     ("филд", "переменн", "преобразован", "реестр", "анкет", "запись номера", "формат записи",
      "верхнему или нижнему регистру", "разделение адреса")),
    ("R04", "Управление диалогом и конструктор сценариев",
     ("сценар", "диалог", "конструктор", "редактор", "граф", "статус", "версион", "перебива",
      "оператор")),
    ("R07", "Обзвон, телефония, списки абонентов",
     ("обзвон", "перезвон", "стоп лист", "стоп-лист", "абонент", "звонк", "вызов")),
    ("R08", "Логи, отчётность, выгрузки",
     ("лог ", "логе", "отчёт", "отчет", "статистик", "выгруз", "журнал")),
    ("R09", "Управляемость и настройка платформы",
     ("настрой", "включ", "отключ", "порог", "режим", "возможность указать")),
]

MODALITY = [
    ("обязательное («должна/должен/должны»)", r"должн"),
    ("декларативное («наличие», «возможность»)", r"наличие|возможност"),
    ("запрос информации у вендора («вендор должен указать»)", r"вендор должен указать"),
]

ANSWER_BUCKETS = [
    ("Да (безусловно)", lambda a: a.lower().rstrip(". ") in {"да"}),
    ("Да с оговоркой", lambda a: a.lower().startswith("да") and a.lower().rstrip(". ") not in {"да"}),
    ("Нет", lambda a: a.lower().startswith("нет")),
    ("На уточнении", lambda a: "уточнени" in a.lower()),
    ("Свободный ответ (не да/нет)", lambda a: True),
]

LEVELS = ["У1", "У1ч", "У2 (twin)", "У3 (РА)", "—"]


def parse_mirror(path: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    appendix = 0
    for line in open(path, encoding="utf-8"):
        if line.startswith("## Лист «"):
            appendix += 1
            continue
        if not line.startswith("| ") or line.startswith("| ---") or line.startswith("| № "):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 4:
            continue
        rows.append(
            {
                "appendix": appendix,
                "num": cells[0],
                "text": cells[1],
                "answer": cells[2],
                "note": cells[3],
                "is_group": cells[3].startswith("Заголовок группы"),
            }
        )
    return rows


def level_of(note: str) -> str:
    match = re.search(r"\*\*Уровень покрытия: (.+?)\.\*\*", note)
    if not match:
        return "—"
    value = match.group(1)
    # порядок важен: «У1ч» проверяется раньше «У1», иначе поглощается префиксом
    for level in ["У1ч", "У1", "У2", "У3"]:
        if value.startswith(level):
            return "У2 (twin)" if level == "У2" else ("У3 (РА)" if level == "У3" else level)
    return "—"


def classify(text: str) -> tuple[str, str]:
    lowered = text.lower()
    for code, title, keys in RULES:
        if any(key in lowered for key in keys):
            return code, title
    return "R00", "Не классифицировано правилами"


def answer_bucket(answer: str) -> str:
    for title, test in ANSWER_BUCKETS:
        if test(answer):
            return title
    return "Свободный ответ (не да/нет)"


def table(out, header: list[str], body: list[list[str]]) -> None:
    print("| " + " | ".join(header) + " |", file=out)
    print("| " + " | ".join(["---"] * len(header)) + " |", file=out)
    for row in body:
        print("| " + " | ".join(str(cell) for cell in row) + " |", file=out)
    print("", file=out)


APPENDIX_TITLES = {
    1: "№ 1 STT",
    2: "№ 2 TTS",
    3: "№ 3 NLU",
    4: "№ 4 Dialogue Manager",
}


def report(rows: list[dict], out) -> None:
    reqs = [r for r in rows if not r["is_group"]]
    groups = [r for r in rows if r["is_group"]]

    print("## 1. Объём наблюдений\n", file=out)
    body = []
    for appendix in sorted(APPENDIX_TITLES):
        total = [r for r in rows if r["appendix"] == appendix]
        req = [r for r in total if not r["is_group"]]
        composite = [r for r in req if "<br>" in r["text"]]
        body.append(
            [
                APPENDIX_TITLES[appendix],
                len(total),
                len(total) - len(req),
                len(req),
                len(composite),
                round(sum(len(r["text"]) for r in req) / len(req)) if req else 0,
            ]
        )
    body.append(
        [
            "**Итого**",
            f"**{len(rows)}**",
            f"**{len(groups)}**",
            f"**{len(reqs)}**",
            f"**{len([r for r in reqs if '<br>' in r['text']])}**",
            f"**{round(sum(len(r['text']) for r in reqs) / len(reqs))}**",
        ]
    )
    table(
        out,
        ["Приложение", "Строк формы", "Заголовков групп", "Требований", "Многосоставных*", "Средняя длина, симв."],
        body,
    )
    print(
        "\\* Многосоставное — строка формы, внутри которой Заказчик перечислил несколько "
        "положений через перенос строки. Такая строка учитывается как одно требование, "
        "хотя содержит несколько проверяемых утверждений.\n",
        file=out,
    )

    print("## 2. Модальность формулировок (детерминированно)\n", file=out)
    body = []
    for title, pattern in MODALITY:
        hit = [r for r in reqs if re.search(pattern, r["text"], re.IGNORECASE)]
        body.append([title, len(hit), f"{round(100 * len(hit) / len(reqs))} %"])
    numeric = [r for r in reqs if re.search(r"\d+\s?(%|сек|мин|кгц|кбит|мс)", r["text"], re.IGNORECASE)]
    body.append(["содержит числовой порог или единицу измерения", len(numeric), f"{round(100 * len(numeric) / len(reqs))} %"])
    table(out, ["Признак формулировки", "Требований", "Доля"], body)

    print("## 3. Ответы участника в исходной форме (детерминированно)\n", file=out)
    buckets = Counter(answer_bucket(r["answer"]) for r in reqs if r["answer"])
    empty = len([r for r in reqs if not r["answer"]])
    body = [[title, buckets.get(title, 0), f"{round(100 * buckets.get(title, 0) / len(reqs))} %"] for title, _ in ANSWER_BUCKETS]
    if empty:
        body.append(["Ответ не заполнен", empty, f"{round(100 * empty / len(reqs))} %"])
    table(out, ["Ответ участника", "Требований", "Доля"], body)

    print("## 4. Ответ участника × уровень покрытия по итогам анализа\n", file=out)
    cross: dict[str, Counter] = defaultdict(Counter)
    for r in reqs:
        cross[answer_bucket(r["answer"]) if r["answer"] else "Ответ не заполнен"][level_of(r["note"])] += 1
    body = []
    for title in [t for t, _ in ANSWER_BUCKETS] + (["Ответ не заполнен"] if empty else []):
        counts = cross.get(title)
        if not counts:
            continue
        body.append([title] + [counts.get(level, 0) for level in LEVELS] + [sum(counts.values())])
    totals = Counter(level_of(r["note"]) for r in reqs)
    body.append(["**Итого**"] + [f"**{totals.get(level, 0)}**" for level in LEVELS] + [f"**{len(reqs)}**"])
    table(out, ["Ответ участника"] + LEVELS + ["Всего"], body)

    print("## 5. Тематические классы второго уровня (эвристика)\n", file=out)
    print(
        "Правила классификации (первое совпадение выигрывает, порядок значим):\n",
        file=out,
    )
    table(
        out,
        ["Код", "Класс", "Ключевые слова правила"],
        [[code, title, ", ".join(f"`{k.strip()}`" for k in keys)] for code, title, keys in RULES],
    )
    by_class: dict[str, Counter] = defaultdict(Counter)
    for r in reqs:
        code, _ = classify(r["text"])
        by_class[code][r["appendix"]] += 1
    titles = {code: title for code, title, _ in RULES}
    titles["R00"] = "Не классифицировано правилами"
    body = []
    for code in sorted(by_class, key=lambda c: -sum(by_class[c].values())):
        counts = by_class[code]
        body.append(
            [code, titles[code]]
            + [counts.get(a, 0) for a in sorted(APPENDIX_TITLES)]
            + [sum(counts.values())]
        )
    table(out, ["Код", "Класс"] + [APPENDIX_TITLES[a] for a in sorted(APPENDIX_TITLES)] + ["Всего"], body)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mirror", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--preamble")
    parser.add_argument("--epilogue")
    args = parser.parse_args()
    rows = parse_mirror(args.mirror)
    with open(args.out, "w", encoding="utf-8") as out:
        if args.preamble:
            out.write(open(args.preamble, encoding="utf-8").read())
        report(rows, out)
        if args.epilogue:
            out.write(open(args.epilogue, encoding="utf-8").read())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
