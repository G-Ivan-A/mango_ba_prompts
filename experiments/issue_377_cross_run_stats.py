#!/usr/bin/env python3
"""Сводная статистика RUN-0073…RUN-0076 по группам разделов BCREQ-ФТ (issue #377).

Дополнительное задание из комментария к PR #380 (2026-10-20 20:08): изучить
прогоны RUN-0073, RUN-0074, RUN-0075 и сформулировать три итоговых промпта
генерации разделов — а) 1, 2; б) 3, 5; в) 4, 6. Скрипт даёт для этого числа:

- вхождения дефектов «раздел × категория» из таблицы §4
  ``outputs/error-statistics.md`` каждого прогона — как есть (сырые коды) и в
  едином словаре категорий ``U01``…``U26`` (сопоставление — :data:`UNIFY`);
- критерии успеха ``outputs/success-criteria.md`` по разделам;
- сводку по группам разделов (:func:`group_of`).

RUN-0076 (этот же PR, задача 1110) учитывается как четвёртый прогон: он
построен по тому же словарю C01–C19, что RUN-0073/0074.

Источник чисел — только файлы записей ``runs/2026/RUN-NNNN``; итоги сверяются с
``metadata.yaml`` (``incidents_by_category``), расхождение — ошибка.

Правила трёх итоговых промптов (:data:`RULES`) заданы здесь же: скрипт проверяет,
что каждая категория с вхождениями в группе покрыта правилом промпта этой группы
(или общей частью), и что каждый процитированный критерий успеха существует.

Запуск: ``python3 experiments/issue_377_cross_run_stats.py``
(пишет ``experiments/issue_377/cross-run-stats.json``);
``--write-doc`` — дополнительно обновляет таблицы между маркерами
``<!-- cross-run-stats:NAME -->`` в :data:`DOC`; ``--check-doc`` — только сверяет.
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "experiments" / "issue_377" / "cross-run-stats.json"
DOC = ROOT / "docs" / "analysis" / "2026-10-20-bcreq-fr-section-prompts.md"

RUNS = {
    "RUN-0073": "1123",
    "RUN-0074": "1106",
    "RUN-0075": "1104",
    "RUN-0076": "1110",
}

# Единый словарь. U01–U19 = общий словарь C01–C19 RUN-0073/0074/0076.
UNIFIED = {
    "U01": "Архитектура и реализация в ФТ / функциональном дизайне",
    "U02": "Декларация методологии (TM Forum, ODA, OpenAPI, BABOK) в тексте документа",
    "U03": "Непрошенные функции «по индустриальной практике», диктовка процесса Заказчику",
    "U04": "Расширение границ (scope creep)",
    "U05": "Несанкционированное удаление, переименование или слияние",
    "U06": "Регресс относительно согласованного решения, возврат отклонённого",
    "U07": "Избыточный вопрос, проигнорированный контекст, выход за роль",
    "U08": "Несоответствие адресату",
    "U09": "Непроверенное утверждение, выдуманное число / функция / локатор",
    "U10": "Угодничество, самосертификация, ложное утверждение о диалоге",
    "U11": "Нарушение порядка и структуры (в т. ч. содержание не в своём разделе)",
    "U12": "Неатомарная, двусмысленная формулировка, жаргон",
    "U13": "Пропуск обязательного содержания",
    "U14": "Ложная апелляция или ложный конфликт",
    "U15": "Ошибочное доменное представление, сверхобобщение факта",
    "U16": "Предвзятая аргументация в пользу варианта",
    "U17": "Непрошенный полный вывод документа",
    "U18": "Упущение из предоставленной документации / базы знаний",
    "U19": "Дефект промпта (шаблона)",
    "U20": "Подмена запроса или пересмотр решения БА",
    "U21": "Нарушение формы и структуры, заданной БА",
    "U22": "Утечка чужого контекста (память, другие диалоги)",
    "U23": "Нерелевантные факты",
    "U24": "Не-требование в ФТ: штатный функционал оформлен как доработка",
    "U25": "Избыточная декомпозиция ФТ",
    "U26": "Фиксация несуществующей проблемы («розовый слон»)",
}

_COMMON = {f"C{i:02d}": f"U{i:02d}" for i in range(1, 20)}
# Сопоставление — интерпретация автора анализа по названиям категорий словарей
# прогонов (§2 error-statistics.md); сырые коды сохраняются рядом.
UNIFY = {
    "RUN-0073": dict(_COMMON),
    "RUN-0074": {**_COMMON, "C20": "U20", "C21": "U21", "C22": "U22", "C23": "U23", "C24": "U24", "C25": "U25"},
    "RUN-0075": {
        "C01": "U09",  # выдуманная функция, элемент интерфейса, значение или цитата
        "C02": "U03",  # «индустриальная практика» и диктовка процесса Заказчику
        "C03": "U07",  # отсылка в техподдержку вместо анализа
        "C04": "U10",  # угодничество
        "C05": "U10",  # самосертификация готовности
        "C06": "U01",  # реализационные детали и API-домыслы
        "C07": "U24",  # штатный функционал оформлен как доработка
        "C08": "U11",  # ограничения не в своём разделе
        "C09": "U06",  # возврат отклонённого пункта
        "C10": "U15",  # сверхобобщение задокументированного факта
        "C11": "U09",  # неверный, чужой или непроверяемый локатор
        "C12": "U12",  # неясная формулировка, нарушение стиля
        "C13": "U10",  # ложное утверждение о диалоге, правках, памяти
        "C14": "U07",  # некорректный вопрос, выход за роль
        "C15": "U19",  # дефект промпта
    },
    "RUN-0076": {**_COMMON, "C20": "U26"},
}

GROUPS = {
    "a": "Промпт а) — разделы 1, 2",
    "asis": "Шаг 0 As-Is (вход промпта а), только RUN-0075)",
    "b": "Промпт б) — разделы 3, 5",
    "c": "Промпт в) — разделы 4, 6 (+4.1, 7 RUN-0073)",
    "open": "Реестр открытых вопросов (общая часть промптов)",
    "dialog": "Ход диалога вне документа (общая часть промптов)",
    "prompt": "Шаблон-промпт целиком (дефекты самого промпта)",
}


# Правила итоговых промптов: ID → промпт, покрываемые категории, источники.
# Промпт: common — общая часть, a / b / c — промпты групп, design — конструкция
# промптов (исправление дефектов шаблонов, категория U19).
# Источники по прогонам (проверяются :func:`check_source`):
#   SC-NN      — критерий успеха outputs/success-criteria.md;
#   Rx.y       — правило outputs/section-prompts.md (RUN-0074);
#   I-NNN      — вхождение дефекта промпта outputs/incident-register.md;
#   §N CNN     — строка категории в разделе N outputs/prompt-improvements.md (RUN-0076);
#   промпт N   — промпт N outputs/section-prompts.md (RUN-0073).
RULES: dict[str, dict] = {
    "О1": {"prompt": "common", "covers": ["U09", "U15", "U18", "U22"], "sources": {
        "RUN-0073": ["SC-02"], "RUN-0074": ["SC-01", "SC-02", "SC-08", "R2.3"], "RUN-0075": ["SC-04"],
        "RUN-0076": ["SC-21", "SC-38", "SC-39", "SC-55", "SC-58"]}},
    "О2": {"prompt": "common", "covers": ["U23"], "sources": {"RUN-0074": ["SC-04", "R2.2"]}},
    "О3": {"prompt": "common", "covers": ["U06", "U20"], "sources": {
        "RUN-0073": ["SC-21"], "RUN-0074": ["SC-23", "R4.4"], "RUN-0076": ["SC-24", "§1 C06"]}},
    "О4": {"prompt": "common", "covers": ["U16"], "sources": {"RUN-0074": ["SC-13", "R4.4"], "RUN-0076": ["§1 C16"]}},
    "О5": {"prompt": "common", "covers": ["U14", "U26"], "sources": {"RUN-0076": ["SC-65", "§1 C14", "§1 C20"]}},
    "О6": {"prompt": "common", "covers": ["U17"], "sources": {"RUN-0073": ["SC-03"], "RUN-0076": ["SC-54", "§1 C17"]}},
    "О7": {"prompt": "common", "covers": ["U05", "U11", "U21"], "sources": {
        "RUN-0073": ["SC-05", "SC-16"], "RUN-0074": ["SC-03", "SC-20", "SC-23", "RX.3", "RX.4"],
        "RUN-0076": ["SC-20", "SC-34"]}},
    "О8": {"prompt": "common", "covers": ["U03", "U04"], "sources": {"RUN-0075": ["SC-05"], "RUN-0076": ["SC-12", "§2 C03"]}},
    "О9": {"prompt": "common", "covers": ["U12"], "sources": {"RUN-0073": ["SC-09", "SC-22"], "RUN-0076": ["SC-22"]}},
    "О10": {"prompt": "common", "covers": ["U02"], "sources": {
        "RUN-0073": ["SC-06"], "RUN-0074": ["RX.2"], "RUN-0076": ["§1 C02"]}},
    "О11": {"prompt": "common", "covers": ["U08"], "sources": {"RUN-0073": ["SC-11"], "RUN-0076": ["§1 C08"]}},
    "О12": {"prompt": "common", "covers": ["U07"], "sources": {
        "RUN-0073": ["SC-12"], "RUN-0075": ["SC-08"], "RUN-0076": ["SC-13", "§1 C07"]}},
    "О13": {"prompt": "common", "covers": ["U10"], "sources": {"RUN-0073": ["SC-04"], "RUN-0074": ["RX.5"], "RUN-0076": ["§1 C10"]}},
    "О14": {"prompt": "common", "covers": ["U10", "U13"], "sources": {
        "RUN-0074": ["SC-26", "SC-27", "RX.1"], "RUN-0076": ["SC-61"]}},
    "А0.1": {"prompt": "a", "covers": ["U01", "U09", "U23"], "sources": {
        "RUN-0074": ["SC-04", "R2.2"], "RUN-0075": ["SC-01", "SC-04", "SC-06"]}},
    "А0.2": {"prompt": "a", "covers": ["U09", "U15"], "sources": {"RUN-0075": ["SC-02", "SC-07"]}},
    "А0.3": {"prompt": "a", "covers": ["U15"], "sources": {"RUN-0075": ["SC-03", "SC-07"]}},
    "А0.4": {"prompt": "a", "covers": ["U18"], "sources": {"RUN-0076": ["§1 C18"]}},
    "А1.1": {"prompt": "a", "covers": ["U06", "U12"], "sources": {"RUN-0074": ["R1.1"], "RUN-0076": ["SC-07"]}},
    "А1.2": {"prompt": "a", "covers": ["U12"], "sources": {"RUN-0074": ["R1.2", "R1.3", "R1.4"], "RUN-0076": ["SC-42", "SC-47"]}},
    "А1.3": {"prompt": "a", "covers": ["U03", "U04"], "sources": {
        "RUN-0073": ["SC-13"], "RUN-0076": ["SC-07", "SC-35", "I-005"]}},
    "А1.4": {"prompt": "a", "covers": ["U15"], "sources": {"RUN-0076": ["SC-47"]}},
    "А2.1": {"prompt": "a", "covers": ["U01", "U09", "U26"], "sources": {
        "RUN-0074": ["R2.1"], "RUN-0076": ["SC-08", "SC-09", "SC-48", "I-004"]}},
    "А2.2": {"prompt": "a", "covers": ["U09"], "sources": {"RUN-0074": ["R2.4"], "RUN-0076": ["I-008"]}},
    "А2.3": {"prompt": "a", "covers": ["U04", "U13", "U24"], "sources": {
        "RUN-0073": ["SC-14"], "RUN-0074": ["R2.5"], "RUN-0076": ["SC-10", "SC-11", "I-003"]}},
    "А2.4": {"prompt": "a", "covers": ["U01", "U11"], "sources": {"RUN-0074": ["SC-05"], "RUN-0075": ["SC-09", "SC-11"]}},
    "А2.5": {"prompt": "a", "covers": ["U03", "U04"], "sources": {
        "RUN-0075": ["SC-10"], "RUN-0076": ["SC-01", "SC-56", "SC-60", "SC-62", "SC-64"]}},
    "Б3.1": {"prompt": "b", "covers": ["U24"], "sources": {
        "RUN-0074": ["SC-07", "R3.1"], "RUN-0075": ["SC-13", "SC-16"], "RUN-0076": ["SC-03"]}},
    "Б3.2": {"prompt": "b", "covers": ["U03", "U04", "U20", "U24"], "sources": {
        "RUN-0074": ["SC-10", "SC-16", "SC-21", "SC-25", "R3.2"], "RUN-0076": ["SC-52", "SC-63"]}},
    "Б3.3": {"prompt": "b", "covers": ["U24"], "sources": {"RUN-0074": ["SC-06", "R3.3"]}},
    "Б3.4": {"prompt": "b", "covers": ["U12"], "sources": {
        "RUN-0074": ["R3.6"], "RUN-0076": ["SC-18", "SC-19", "SC-25", "I-002", "I-006"]}},
    "Б3.5": {"prompt": "b", "covers": ["U12", "U25"], "sources": {
        "RUN-0074": ["SC-14", "SC-15", "SC-28", "R3.4"], "RUN-0075": ["SC-14", "SC-15", "SC-17"],
        "RUN-0076": ["SC-04"]}},
    "Б3.6": {"prompt": "b", "covers": ["U01", "U02"], "sources": {
        "RUN-0074": ["SC-09", "R3.5", "R3.8"], "RUN-0076": ["SC-06", "SC-16"]}},
    "Б3.7": {"prompt": "b", "covers": ["U05", "U11"], "sources": {
        "RUN-0073": ["SC-15", "I-013"], "RUN-0074": ["R3.7"], "RUN-0076": ["SC-14", "SC-15", "SC-17", "SC-23"]}},
    "Б3.8": {"prompt": "b", "covers": ["U13", "U15"], "sources": {"RUN-0074": ["SC-19"], "RUN-0073": ["промпт 2"]}},
    "Б3.9": {"prompt": "b", "covers": ["U13"], "sources": {"RUN-0073": ["промпт 2"], "RUN-0076": ["SC-49"]}},
    "Б5.1": {"prompt": "b", "covers": ["U09"], "sources": {
        "RUN-0073": ["промпт 2", "I-011"], "RUN-0074": ["R3.5"], "RUN-0076": ["SC-02"]}},
    "Б5.2": {"prompt": "b", "covers": ["U11"], "sources": {"RUN-0073": ["промпт 2"]}},
    "В4.1": {"prompt": "c", "covers": ["U01", "U02"], "sources": {
        "RUN-0073": ["SC-01", "SC-07", "I-005", "I-006", "I-007"], "RUN-0074": ["SC-17", "R4.1"],
        "RUN-0076": ["SC-28", "SC-31", "SC-50"]}},
    "В4.2": {"prompt": "c", "covers": ["U11", "U13"], "sources": {"RUN-0074": ["SC-21", "R4.2"], "RUN-0076": ["SC-05"]}},
    "В4.3": {"prompt": "c", "covers": ["U11", "U13"], "sources": {
        "RUN-0073": ["SC-10", "SC-17", "SC-20"], "RUN-0074": ["SC-12", "SC-22", "R4.3", "R4.8"],
        "RUN-0075": ["SC-18", "SC-19"], "RUN-0076": ["SC-37"]}},
    "В4.4": {"prompt": "c", "covers": ["U06", "U24"], "sources": {
        "RUN-0074": ["R4.7"], "RUN-0075": ["SC-16"], "RUN-0076": ["SC-03", "SC-60"]}},
    "В4.5": {"prompt": "c", "covers": ["U09", "U15", "U18"], "sources": {
        "RUN-0073": ["SC-18", "SC-19"],
        "RUN-0076": ["SC-21", "SC-26", "SC-27", "SC-29", "SC-30", "SC-38", "SC-40", "SC-41", "SC-57"]}},
    "В4.6": {"prompt": "c", "covers": ["U12", "U15"], "sources": {"RUN-0076": ["SC-32", "SC-33", "SC-44", "SC-45"]}},
    "В4.7": {"prompt": "c", "covers": ["U03", "U16", "U20"], "sources": {
        "RUN-0074": ["SC-11", "SC-13", "R4.4", "R4.5"], "RUN-0076": ["SC-36"]}},
    "В4.8": {"prompt": "c", "covers": ["U03", "U04"], "sources": {"RUN-0074": ["SC-18", "R4.6", "R4.8"]}},
    "В4.9": {"prompt": "c", "covers": ["U05", "U12", "U21"], "sources": {
        "RUN-0073": ["SC-08"], "RUN-0076": ["SC-43", "SC-46"]}},
    "В6.1": {"prompt": "c", "covers": ["U11", "U13"], "sources": {
        "RUN-0073": ["промпт 3"], "RUN-0074": ["SC-24", "R6.1"], "RUN-0075": ["SC-11", "SC-21"]}},
    "В6.2": {"prompt": "c", "covers": ["U24"], "sources": {"RUN-0075": ["SC-22"]}},
    "В6.3": {"prompt": "c", "covers": ["U09"], "sources": {"RUN-0073": ["промпт 3", "I-012"]}},
    "П1": {"prompt": "design", "covers": ["U02", "U03", "U19"], "sources": {
        "RUN-0073": ["I-001", "I-002", "I-003", "I-004"], "RUN-0075": ["I-001", "I-002", "I-113", "I-114"],
        "RUN-0076": ["I-001"]}},
    "П2": {"prompt": "design", "covers": ["U04", "U09", "U19"], "sources": {
        "RUN-0073": ["I-011", "I-012"], "RUN-0075": ["I-005"], "RUN-0076": ["I-004", "I-005", "I-008"]}},
    "П3": {"prompt": "design", "covers": ["U11", "U13", "U19"], "sources": {
        "RUN-0073": ["I-017"], "RUN-0075": ["I-003"], "RUN-0076": ["SC-02", "I-002", "I-003"]}},
    "П4": {"prompt": "design", "covers": ["U03", "U05", "U19", "U20"], "sources": {
        "RUN-0073": ["I-013", "I-018"], "RUN-0076": ["SC-14"]}},
    "П5": {"prompt": "design", "covers": ["U12", "U19"], "sources": {
        "RUN-0073": ["I-008", "I-009", "I-010"], "RUN-0076": ["I-006"]}},
    "П6": {"prompt": "design", "covers": ["U08", "U10", "U14", "U19"], "sources": {
        "RUN-0073": ["I-014", "I-015", "I-016"], "RUN-0075": ["I-004"], "RUN-0076": ["I-007"]}},
    "П7": {"prompt": "design", "covers": ["U04", "U19"], "sources": {"RUN-0074": ["SC-25"], "RUN-0076": ["SC-51", "SC-53"]}},
}

# Какие правила применяются к вхождениям группы.
GROUP_PROMPTS = {
    "a": {"common", "a", "design"},
    "asis": {"common", "a", "design"},
    "b": {"common", "b", "design"},
    "c": {"common", "c", "design"},
    "open": {"common", "a", "b", "c", "design"},
    "dialog": {"common", "a", "b", "c", "design"},
    "prompt": {"common", "design"},
}


def group_of(run: str, label: str) -> str:
    """Группа промпта по метке раздела из §4 или из success-criteria.

    RUN-0075 (задача 1104) нумеровал «Функциональные требования (доработка)»
    разделом 4 со слотом S-SOLUTION; по содержанию это ФТ, поэтому группа б).
    """
    text = label.strip().strip("`")
    low = text.lower()
    if low.startswith(("шаг 0", "asis")):
        return "asis"
    if low.startswith(("реестр открытых", "open")):
        return "open"
    if low.startswith(("ход диалога", "dialog")):
        return "dialog"
    if low.startswith(("шаблон-промпт", "промпты генерации", "prompt")):
        return "prompt"
    num = re.match(r"(\d+)", text)
    if not num:
        raise ValueError(f"{run}: неизвестный раздел {label!r}")
    sec = num.group(1)
    if sec in {"1", "2"}:
        return "a"
    if sec in {"3", "5"}:
        return "b"
    if sec == "4" and run == "RUN-0075":
        return "b"
    if sec in {"4", "6", "7"}:
        return "c"
    raise ValueError(f"{run}: раздел {sec} вне групп")


def cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def section_table(run: str) -> tuple[list[str], list[tuple[str, int, dict[str, int]]]]:
    text = (ROOT / "runs" / "2026" / run / "outputs" / "error-statistics.md").read_text(encoding="utf-8")
    block = re.search(r"^## 4\..*?$(.*?)^## 5\.", text, re.S | re.M)
    if not block:
        raise ValueError(f"{run}: нет §4 в error-statistics.md")
    lines = [ln for ln in block.group(1).splitlines() if ln.startswith("|")]
    head = cells(lines[0])
    codes = head[2:]
    rows = []
    for ln in lines[2:]:
        c = cells(ln)
        if c[0].startswith("**"):
            continue
        counts = {code: int(v) for code, v in zip(codes, c[2:]) if v}
        rows.append((c[0], int(c[1]), counts))
    return codes, rows


def metadata_value(run: str, key: str) -> str:
    text = (ROOT / "runs" / "2026" / run / "metadata.yaml").read_text(encoding="utf-8")
    m = re.search(rf"^\s*{key}: (.+)$", text, re.M)
    if not m:
        raise ValueError(f"{run}: нет {key} в metadata.yaml")
    return m.group(1).strip().strip('"')


def metadata_categories(run: str) -> dict[str, int]:
    text = (ROOT / "runs" / "2026" / run / "metadata.yaml").read_text(encoding="utf-8")
    block = re.search(r"incidents_by_category:\n((?:\s{4}C\d\d: \d+\n)+)", text)
    if not block:
        raise ValueError(f"{run}: нет incidents_by_category")
    return {k: int(v) for k, v in re.findall(r"(C\d\d): (\d+)", block.group(1))}


def success_criteria(run: str) -> list[dict[str, str]]:
    text = (ROOT / "runs" / "2026" / run / "outputs" / "success-criteria.md").read_text(encoding="utf-8")
    out = []
    current = ""
    for ln in text.splitlines():
        if ln.startswith("### "):
            m = re.search(r"\(`([^`]+)`\)\s*$", ln)
            current = m.group(1) if m else ""
        if not ln.startswith("| SC-"):
            continue
        c = cells(ln)
        if run == "RUN-0076":
            section, criterion, quote = current, c[2], c[3]
        else:
            section, criterion, quote = c[3].split("→")[0].strip(), c[4], c[5]
        out.append(
            {
                "id": c[0],
                "turn": c[1],
                "section": section,
                "group": group_of(run, section),
                "criterion": criterion,
                "quote": quote,
            }
        )
    return out


def build() -> dict:
    result: dict = {"unified_categories": UNIFIED, "groups": GROUPS, "mapping": UNIFY, "runs": {}}
    group_unified: dict[str, Counter] = defaultdict(Counter)
    group_raw_total: Counter = Counter()
    unified_by_run: dict[str, Counter] = {}
    sc_by_group: Counter = Counter()
    for run, task in RUNS.items():
        codes, rows = section_table(run)
        meta = metadata_categories(run)
        col_totals: Counter = Counter()
        sections = []
        run_unified: Counter = Counter()
        run_groups: dict[str, Counter] = defaultdict(Counter)
        for label, total, counts in rows:
            if sum(counts.values()) != total:
                raise ValueError(f"{run}: строка {label!r}: сумма {sum(counts.values())} ≠ {total}")
            grp = group_of(run, label)
            uni: Counter = Counter()
            for code, n in counts.items():
                uni[UNIFY[run][code]] += n
            col_totals.update(counts)
            run_unified.update(uni)
            run_groups[grp].update(uni)
            group_unified[grp].update(uni)
            group_raw_total[grp] += total
            sections.append({"section": label, "group": grp, "total": total, "raw": counts, "unified": dict(sorted(uni.items()))})
        nonzero_meta = {k: v for k, v in meta.items() if v}
        if dict(col_totals) != nonzero_meta:
            raise ValueError(f"{run}: §4 {dict(col_totals)} ≠ metadata {nonzero_meta}")
        crit = success_criteria(run)
        sc_by_group.update(c["group"] for c in crit)
        unified_by_run[run] = run_unified
        result["runs"][run] = {
            "task": task,
            "incidents": sum(col_totals.values()),
            "raw_categories": meta,
            "unified_categories": dict(sorted(run_unified.items())),
            "sections": sections,
            "groups": {g: {"total": sum(c.values()), "unified": dict(sorted(c.items()))} for g, c in run_groups.items()},
            "success_criteria": crit,
            "success_criteria_by_group": dict(Counter(c["group"] for c in crit)),
        }
    total = Counter()
    for c in unified_by_run.values():
        total.update(c)
    result["total"] = {
        "incidents": sum(total.values()),
        "unified_categories": {
            u: {"total": total[u], **{run: unified_by_run[run][u] for run in RUNS}, "runs_with_hits": sum(1 for run in RUNS if unified_by_run[run][u])}
            for u in UNIFIED
        },
        "groups": {
            g: {
                "total": group_raw_total[g],
                "unified": dict(sorted(group_unified[g].items())),
                "by_run": {run: result["runs"][run]["groups"].get(g, {"total": 0})["total"] for run in RUNS},
                "success_criteria": sc_by_group[g],
            }
            for g in GROUPS
        },
        "success_criteria": sum(sc_by_group.values()),
    }
    return result


PROMPT_DEFECT = {"RUN-0073": "C19", "RUN-0074": "C19", "RUN-0075": "C15", "RUN-0076": "C19"}


def run_text(run: str, name: str) -> str:
    path = ROOT / "runs" / "2026" / run / "outputs" / name
    return path.read_text(encoding="utf-8") if path.exists() else ""


def check_source(run: str, ref: str, sc_ids: set[str]) -> str | None:
    """Ошибка, если ссылка на источник правила не находится в файлах прогона."""
    if ref.startswith("SC-"):
        return None if ref in sc_ids else f"{run}: нет критерия {ref}"
    if re.fullmatch(r"R[0-9X]+\.\d+", ref):
        ok = re.search(rf"^\| {re.escape(ref)} \|", run_text(run, "section-prompts.md"), re.M)
        return None if ok else f"{run}: нет правила {ref} в section-prompts.md"
    if re.fullmatch(r"I-\d{3}", ref):
        row = re.search(rf"^\| {ref} \|.*$", run_text(run, "incident-register.md"), re.M)
        if not row:
            return f"{run}: нет вхождения {ref}"
        return None if f"| {PROMPT_DEFECT[run]} |" in row.group(0) else f"{run}: {ref} — не дефект промпта"
    m = re.fullmatch(r"§(\d) (C\d\d)", ref)
    if m:
        text = run_text(run, "prompt-improvements.md")
        part = re.search(rf"^## {m.group(1)}\..*?(?=^## |\Z)", text, re.S | re.M)
        ok = part and re.search(rf"^\| {m.group(2)} ", part.group(0), re.M)
        return None if ok else f"{run}: нет {m.group(2)} в §{m.group(1)} prompt-improvements.md"
    m = re.fullmatch(r"промпт (\d)", ref)
    if m:
        ok = re.search(rf"^### 2\.{m.group(1)}\. Промпт {m.group(1)} ", run_text(run, "section-prompts.md"), re.M)
        return None if ok else f"{run}: нет промпта {m.group(1)} в section-prompts.md"
    return f"{run}: неизвестная ссылка {ref!r}"


def check_rules(data: dict) -> dict:
    """Покрытие категорий правилами и существование источников; ошибка — исключение."""
    errors = []
    sc_ids = {run: {c["id"] for c in data["runs"][run]["success_criteria"]} for run in RUNS}
    cited: dict[str, set[str]] = {run: set() for run in RUNS}
    for rid, rule in RULES.items():
        if rule["prompt"] not in {"common", "a", "b", "c", "design"}:
            errors.append(f"{rid}: неизвестный промпт {rule['prompt']}")
        if not any(rule["sources"].values()):
            errors.append(f"{rid}: нет источников")
        for u in rule["covers"]:
            if u not in UNIFIED:
                errors.append(f"{rid}: неизвестная категория {u}")
        for run, refs in rule["sources"].items():
            for ref in refs:
                err = check_source(run, ref, sc_ids[run])
                if err:
                    errors.append(f"{rid}: {err}")
                if ref.startswith("SC-"):
                    cited[run].add(ref)
    coverage = {}
    for g in GROUPS:
        coverage[g] = {}
        for u, n in data["total"]["groups"][g]["unified"].items():
            rules = [rid for rid, r in RULES.items() if u in r["covers"] and r["prompt"] in GROUP_PROMPTS[g]]
            if not rules:
                errors.append(f"группа {g}: {u} ({n}) не покрыта правилом")
            coverage[g][u] = {"incidents": n, "rules": rules}
    for u, v in data["total"]["unified_categories"].items():
        if v["total"] and not any(u in r["covers"] for r in RULES.values()):
            errors.append(f"{u}: нет правила")
    if errors:
        raise ValueError("правила промптов:\n  " + "\n  ".join(errors))
    uncited = [
        {"run": run, "id": c["id"], "section": c["section"], "group": c["group"], "criterion": c["criterion"]}
        for run in RUNS
        for c in data["runs"][run]["success_criteria"]
        if c["id"] not in cited[run]
    ]
    return {
        "coverage": coverage,
        "cited_success_criteria": {run: sorted(v) for run, v in cited.items()},
        "uncited_success_criteria": uncited,
    }


# --- Таблицы аналитического файла -------------------------------------------

GROUP_ORDER = list(GROUPS)


def _table(head: list[str], rows: list[list], align: list[str] | None = None) -> str:
    align = align or ["---"] * len(head)
    out = ["| " + " | ".join(head) + " |", "| " + " | ".join(align) + " |"]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


def _pct(n: int, total: int) -> str:
    return f"{100 * n / total:.1f}" if total else "0.0"


def render_tables(data: dict) -> dict[str, str]:
    t = data["total"]
    runs = list(RUNS)
    num = ["---"] + ["---:"] * 20
    tables: dict[str, str] = {}

    rows = []
    for run in runs:
        rows.append([
            f"[`{run}`](../../runs/2026/{run}/metadata.yaml)",
            RUNS[run],
            metadata_value(run, "model"),
            metadata_value(run, "turns"),
            metadata_value(run, "answers_with_incidents"),
            data["runs"][run]["incidents"],
            metadata_value(run, "success_criteria"),
            f"{metadata_value(run, 'golden_sets')} / {metadata_value(run, 'golden_cases')}",
            metadata_value(run, "positive_cases"),
            f"{metadata_value(run, 'quotes_checked')} / {metadata_value(run, 'quote_mismatches')}",
        ])
    rows.append(["**Итого**", "", "", sum(int(metadata_value(r, "turns")) for r in runs),
                 sum(int(metadata_value(r, "answers_with_incidents")) for r in runs), t["incidents"],
                 t["success_criteria"],
                 f"{sum(int(metadata_value(r, 'golden_sets')) for r in runs)} / "
                 f"{sum(int(metadata_value(r, 'golden_cases')) for r in runs)}",
                 sum(int(metadata_value(r, "positive_cases")) for r in runs),
                 f"{sum(int(metadata_value(r, 'quotes_checked')) for r in runs)} / "
                 f"{sum(int(metadata_value(r, 'quote_mismatches')) for r in runs)}"])
    tables["runs"] = _table(
        ["Прогон", "Задача", "Модель", "Реплик", "Ответов с вхождениями", "Вхождений", "Критериев успеха",
         "Golden set / кейсов", "Позитивных кейсов", "Цитат проверено / расхождений"],
        rows, ["---", "---", "---", "---:", "---:", "---:", "---:", "---", "---:", "---"])

    rows = []
    for u, name in UNIFIED.items():
        v = t["unified_categories"][u]
        cells_ = []
        for run in runs:
            raw = [f"{c}: {n}" for c, n in data["runs"][run]["raw_categories"].items() if n and UNIFY[run].get(c) == u]
            cells_.append(f"{v[run]} ({' + '.join(raw)})" if raw else "—")
        rows.append([u, name, *cells_, v["total"], _pct(v["total"], t["incidents"]), v["runs_with_hits"]])
    rows.append(["**Итого**", "", *[data["runs"][r]["incidents"] for r in runs], t["incidents"], "100.0", ""])
    tables["categories"] = _table(["Код", "Категория", *runs, "Всего", "%", "Прогонов"], rows,
                                  ["---", "---", "---", "---", "---", "---", "---:", "---:", "---:"])

    rows = []
    for run in runs:
        for sec in data["runs"][run]["sections"]:
            uni = ", ".join(f"{u}: {n}" for u, n in sorted(sec["unified"].items(), key=lambda kv: (-kv[1], kv[0])))
            rows.append([run, sec["section"], sec["group"], sec["total"], uni])
    tables["sections"] = _table(["Прогон", "Раздел (§4 error-statistics.md)", "Группа", "Вхождений", "Категории U"],
                                rows, ["---", "---", "---", "---:", "---"])

    rows = []
    for g in GROUP_ORDER:
        v = t["groups"][g]
        sc = [data["runs"][r]["success_criteria_by_group"].get(g, 0) for r in runs]
        rows.append([f"`{g}`", GROUPS[g], *[v["by_run"][r] for r in runs], v["total"], _pct(v["total"], t["incidents"]),
                     *sc, v["success_criteria"]])
    rows.append(["**Итого**", "", *[data["runs"][r]["incidents"] for r in runs], t["incidents"], "100.0",
                 *[len(data["runs"][r]["success_criteria"]) for r in runs], t["success_criteria"]])
    tables["groups"] = _table(
        ["Группа", "Назначение", *[f"{r} вх." for r in runs], "Вхождений", "%", *[f"{r} SC" for r in runs], "SC"],
        rows, ["---", "---"] + ["---:"] * 11)

    rows = []
    for u in UNIFIED:
        counts = [t["groups"][g]["unified"].get(u, 0) for g in GROUP_ORDER]
        if not sum(counts):
            continue
        rows.append([u, *[c or "" for c in counts], sum(counts)])
    rows.append(["**Итого**", *[t["groups"][g]["total"] for g in GROUP_ORDER], t["incidents"]])
    tables["matrix"] = _table(["Код", *[f"`{g}`" for g in GROUP_ORDER], "Всего"], rows, num[: len(GROUP_ORDER) + 2])

    rows = []
    for g in GROUP_ORDER:
        top = sorted(t["groups"][g]["unified"].items(), key=lambda kv: (-kv[1], kv[0]))
        total = t["groups"][g]["total"]
        acc, head_ = 0, []
        for u, n in top:
            head_.append(f"{u} {n} ({_pct(n, total)} %)")
            acc += n
            if acc * 100 >= total * 80:
                break
        rows.append([f"`{g}`", total, len(top), len(head_), "; ".join(head_)])
    tables["pareto"] = _table(["Группа", "Вхождений", "Категорий", "Категорий до 80 %", "Категории (по убыванию)"],
                              rows, ["---", "---:", "---:", "---:", "---"])

    rows = []
    for rid, r in RULES.items():
        src = "; ".join(f"{run[-4:]}: {', '.join(refs)}" for run, refs in r["sources"].items())
        hits = sum(t["unified_categories"][u]["total"] for u in r["covers"])
        rows.append([rid, r["prompt"], ", ".join(r["covers"]), hits, src])
    tables["rules"] = _table(["Правило", "Промпт", "Категории", "Вхождений категорий (все группы)", "Источники"],
                             rows, ["---", "---", "---", "---:", "---"])

    rows = []
    for g in GROUP_ORDER:
        for u, v in sorted(data["rules"]["coverage"][g].items()):
            rows.append([f"`{g}`", u, v["incidents"], ", ".join(v["rules"])])
    tables["coverage"] = _table(["Группа", "Категория", "Вхождений", "Правила промпта группы"], rows,
                                ["---", "---", "---:", "---"])

    cited = data["rules"]["cited_success_criteria"]
    rows = [[run, len(data["runs"][run]["success_criteria"]), len(cited[run]),
             len(data["runs"][run]["success_criteria"]) - len(cited[run])] for run in runs]
    rows.append(["**Итого**", t["success_criteria"], sum(len(v) for v in cited.values()),
                 len(data["rules"]["uncited_success_criteria"])])
    summary = _table(["Прогон", "Критериев успеха", "Процитировано правилами", "Не процитировано"], rows,
                     ["---", "---:", "---:", "---:"])
    rows = [[u["run"], u["id"], u["section"], f"`{u['group']}`", u["criterion"]]
            for u in data["rules"]["uncited_success_criteria"]]
    tables["uncited"] = summary + "\n\n" + _table(["Прогон", "SC", "Раздел", "Группа", "Критерий"], rows)
    return tables


MARK = re.compile(r"(<!-- cross-run-stats:(\w+) -->\n)(.*?)(<!-- /cross-run-stats:\2 -->)", re.S)


def apply_doc(text: str, tables: dict[str, str]) -> tuple[str, list[str]]:
    """Подставляет таблицы в блоки-маркеры; возвращает текст и список отсутствующих блоков."""
    seen = set()

    def repl(m: re.Match) -> str:
        seen.add(m.group(2))
        if m.group(2) not in tables:
            raise ValueError(f"неизвестный блок {m.group(2)}")
        return m.group(1) + tables[m.group(2)].rstrip("\n") + "\n" + m.group(4)

    new = MARK.sub(repl, text)
    return new, sorted(set(tables) - seen)


def build_all() -> tuple[dict, dict[str, str]]:
    data = build()
    data["rules"] = check_rules(data)
    data["rule_definitions"] = RULES
    data["group_prompts"] = {g: sorted(v) for g, v in GROUP_PROMPTS.items()}
    return data, render_tables(data)


def main(argv: list[str]) -> int:
    data, tables = build_all()
    if "--check-doc" in argv:
        text = DOC.read_text(encoding="utf-8")
        new, missing = apply_doc(text, tables)
        if missing or new != text:
            print(f"{DOC.relative_to(ROOT)}: таблицы устарели или нет блоков {missing}; "
                  "запустите python3 experiments/issue_377_cross_run_stats.py --write-doc")
            return 1
        print(f"{DOC.relative_to(ROOT)}: таблицы актуальны")
        return 0
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if "--write-doc" in argv:
        new, missing = apply_doc(DOC.read_text(encoding="utf-8"), tables)
        if missing:
            print(f"нет блоков: {missing}")
            return 1
        DOC.write_text(new, encoding="utf-8")
        print(f"wrote {DOC.relative_to(ROOT)}")
    t = data["total"]
    print(f"incidents: {t['incidents']}, success criteria: {t['success_criteria']}")
    for g, v in t["groups"].items():
        top = sorted(v["unified"].items(), key=lambda kv: -kv[1])[:6]
        print(f"  {g:7} {v['total']:4} {v['by_run']} SC={v['success_criteria']} top={top}")
    for u, v in t["unified_categories"].items():
        print(f"  {u} {v['total']:4} runs={v['runs_with_hits']} {UNIFIED[u][:60]}")
    print(f"uncited success criteria: {len(data['rules']['uncited_success_criteria'])}")
    print(f"wrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
