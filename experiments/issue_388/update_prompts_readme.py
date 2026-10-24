#!/usr/bin/env python3
"""Issue #388: prompts/README.md — маршрутизация BCREQ, матрица BCREQ,
перенос 18 устаревших строк в раздел «Архив»."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / "prompts/README.md"
B = "https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/"
ARCH = (ROOT / "experiments/issue_388/archived-prompts.txt").read_text().split()

def link(name):
    return f"[`{name}.md`]({B}{name}.md)"

t = P.read_text(encoding="utf-8")

# 1. Быстрый выбор
quick_new = f"""| Если задача | Начните с |
| --- | --- |
| Нужно создать спецификацию бизнес-требований и дизайна решения (BCREQ) | {link('bcreq-constitution-governance-oneshot')} (Промпт 0), затем шаги по разделу [«BCREQ: маршрутизация»](#bcreq-маршрутизация) |
| Нужно собрать контекст, глоссарий и вопросы заказчику | {link('bcreq-context-understanding-stepwise')} или {link('bcreq-in-understanding-oneshot')} |
| Нужно определить затронутые продукты и команды | {link('bcreq-products-impact-analysis-stepwise')} |
| Нужно сформировать User Story или Use Case | {link('bcreq-scenarios-modeling-oneshot')} (`тип: US \\| UC`) или {link('bcreq-uc-modeling-stepwise')} |
| Нужно написать функциональные требования | {link('bcreq-fr-documentation-stepwise')} или {link('bcreq-core-documentation-oneshot')} |
| Нужно написать нефункциональные требования | {link('bcreq-nfr-documentation-stepwise')} |
| Нужно проверить черновик требований | {link('bcreq-review-validation-oneshot')} |
| Нужно оформить ограничения и границы скоупа | {link('bcreq-constraints-documentation-stepwise')} |
| Нужно описать решение (ОРР) для разработки | {link('bcreq-orr-solution-design-stepwise')} или {link('bcreq-work-solution-design-oneshot')} |
| Нужно собрать риски, зависимости и план приёмки | {link('bcreq-extra-risk-analysis-stepwise')} |
"""
start = t.index("| Если задача | Начните с |")
end = t.index("| Нужно обработать ASR-расшифровку |")
t = t[:start] + quick_new + t[end:]

# 2. Маршрутизация BCREQ — перед матрицей
routing = f"""## BCREQ: маршрутизация

Набор BCREQ (issue #388) создаёт спецификацию бизнес-требований и дизайна
решения по мета-стандартам Задачи 2:
[архитектура промптов](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-architecture.md),
[композиция документа](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-composition-standard.md),
[контракт гейтов](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/contracts/bcreq-stage-gates.md).
Каждый промпт начинается блоком «Конституция и позиция»: **пройдено / текущий /
рекомендуемый следующий** — и заканчивается блоком «Состояние BCREQ», который
БА вставляет в следующий вызов.

Два маршрута:

- **Ручной (stepwise)** — БА ведёт шаги сам, по одному чату на шаг; промпт
  ждёт ответа после каждого подшага («Стоп-гейт»). Пошаговая инструкция —
  на сайте, вкладка «Процессы».
- **Агентный (oneshot)** — ИИ-агент выполняет стадию A-IN, A-CORE или A-WORK
  одним вызовом, копит вопросы в 8.4 и заканчивает отчётом по гейту. Гейт
  агент не пересекает: его решают люди.

| Шаг | Разделы BCREQ | Ручной маршрут (stepwise) | Агентный маршрут (oneshot) | Гейт после шага |
| --- | --- | --- | --- | --- |
| Ш-0 | Каркас, параметры, конституция | {link('bcreq-constitution-governance-oneshot')} | {link('bcreq-constitution-governance-oneshot')} | — |
| Ш-1 | 1 Глоссарий, 2 Бизнес-контекст | {link('bcreq-context-understanding-stepwise')} | {link('bcreq-in-understanding-oneshot')} (стадия A-IN = Ш-1 + Ш-2) | — |
| Ш-2 | ＋2.5 Продукты и стейкхолдеры | {link('bcreq-products-impact-analysis-stepwise')} | A-IN | Г-IN (решает БА) |
| Ш-3 | 3 Функциональные требования | {link('bcreq-fr-documentation-stepwise')} | {link('bcreq-core-documentation-oneshot')} (стадия A-CORE = Ш-3…Ш-5) | — |
| Ш-4 | 4 Нефункциональные требования | {link('bcreq-nfr-documentation-stepwise')} | A-CORE | — |
| Ш-5 | 7 UC, прогон 1 | {link('bcreq-uc-modeling-stepwise')} (`прогон: 1`) | A-CORE | Г-С1 «Согласование 1» (решает Заказчик) |
| Ш-6 | 5 Описание решения (ОРР) | {link('bcreq-orr-solution-design-stepwise')} | {link('bcreq-work-solution-design-oneshot')} (стадия A-WORK = Ш-6…Ш-9) | — |
| Ш-7 | 6 Особенности и ограничения | {link('bcreq-constraints-documentation-stepwise')} | A-WORK | — |
| Ш-8 | 7 UC, прогон 2 | {link('bcreq-uc-modeling-stepwise')} (`прогон: 2`) | A-WORK | — |
| Ш-9 | 8 Риски, зависимости, приёмка | {link('bcreq-extra-risk-analysis-stepwise')} | A-WORK | — |
| Ш-В | Валидация документа второй ролью | {link('bcreq-review-validation-oneshot')} | {link('bcreq-review-validation-oneshot')} | Г-W (решают ПО продукта, архитектор, руководитель КК) |
| Ш-С | US или UC вне документа (2.12 / 2.13) | {link('bcreq-scenarios-modeling-oneshot')} (`тип: US \\| UC`) | {link('bcreq-scenarios-modeling-oneshot')} | — |

Возвраты: если критерий гейта не выполнен, промпт рекомендует возврат в
формате «стадия · шаг · причина»; решение о возврате принимает БА.

"""
t = t.replace("## Матрица промптов\n", routing + "## Матрица промптов\n", 1)

# 3. Удалить строки устаревших промптов из активных таблиц, собрать их
rows = {}
lines = t.split("\n")
kept = []
for line in lines:
    m = re.match(r"\| \[`([\w.-]+)\.md`\]\(" + re.escape(B) + r"archive/", line)
    if m and m.group(1) in ARCH:
        rows[m.group(1)] = line
        continue
    kept.append(line)
t = "\n".join(kept)
assert len(rows) == 18, sorted(set(ARCH) - set(rows))

def archived(line):
    cells = line.split(" | ")
    # Статус — 6-я колонка (индекс 5)
    cells[5] = "`archived`"
    return " | ".join(cells)

desc = {
    "bcreq-constitution-governance-oneshot": ("BCREQ Ш-0: конституция", "Промпт 0: задаёт структуру BCREQ из 8 разделов, стили, правила Р1–Р7, защиты АД-1…АД-7, параметры задачи и каркас документа со статусами.", "oneshot", "governance", "Формирование ФТ/ТЗ"),
    "bcreq-context-understanding-stepwise": ("BCREQ Ш-1: глоссарий и контекст", "Ш-1: пошагово формирует раздел 1 «Глоссарий» и раздел 2 «Бизнес-контекст» (проблема, цель, границы) из материалов Заказчика; вопросы — в 8.4.", "stepwise", "understanding", "Формирование ФТ/ТЗ; Анализ тендерных ТЗ; Формирование UC/US; Помощь ПО/ПМ"),
    "bcreq-products-impact-analysis-stepwise": ("BCREQ Ш-2: продукты и команды", "Ш-2: пошагово формирует пункт ＋2.5 — затронутые продукты по таксономии, продуктовые команды, согласующих и стыки; готовит отчёт к гейту Г-IN.", "stepwise", "impact_analysis", "Формирование ФТ/ТЗ; Impact Analysis"),
    "bcreq-fr-documentation-stepwise": ("BCREQ Ш-3: функциональные требования", "Ш-3: пошагово формирует раздел 3 «Функциональные требования» (вариант delta или new) с фильтрами Ф1–Ф4, условиями EARS и трассой к 2.4.1.", "stepwise", "documentation", "Формирование ФТ/ТЗ"),
    "bcreq-nfr-documentation-stepwise": ("BCREQ Ш-4: нефункциональные требования", "Ш-4: пошагово формирует раздел 4 «Нефункциональные требования» по ISO/IEC 25010:2023 — характеристика, метрика, порог, условие, источник; без выдуманных НФТ.", "stepwise", "documentation", "Формирование ФТ/ТЗ"),
    "bcreq-uc-modeling-stepwise": ("BCREQ Ш-5/Ш-8: UC", "Ш-5 и Ш-8: пошагово формирует раздел 7 Use Case — прогон 1 подтверждает ФТ сценариями (покрытие 100 %), прогон 2 добавляет граничные кейсы и ошибки.", "stepwise", "modeling", "Формирование ФТ/ТЗ; Формирование UC/US"),
    "bcreq-orr-solution-design-stepwise": ("BCREQ Ш-6 (2.6+2.7): ОРР", "Ш-6: пошагово формирует раздел 5 «Описание решения» — L1 ФДР и контекст C4, при `уровень: L1+L2` — L2 ТС, дельта API, данные; трассировка ФТ ↔ ОРР.", "stepwise", "solution_design", "Формирование ФТ/ТЗ; Impact Analysis"),
    "bcreq-constraints-documentation-stepwise": ("BCREQ Ш-7 (2.8): ограничения", "Ш-7: пошагово формирует раздел 6 «Особенности реализации и ограничения» — особенность со ссылкой на раздел 5, ограничение с источником и последствием.", "stepwise", "documentation", "Формирование ФТ/ТЗ; Risk Analysis"),
    "bcreq-extra-risk-analysis-stepwise": ("BCREQ Ш-9 (2.14): риски, приёмка", "Ш-9: пошагово формирует раздел 8 — риски с мерой и владельцем, зависимости, план приёмки «Дано / Когда / Тогда», сводит 8.4 и 8.5; готовит данные к Г-W.", "stepwise", "risk_analysis", "Формирование ФТ/ТЗ; Risk Analysis"),
    "bcreq-review-validation-oneshot": ("BCREQ Ш-В: валидация документа", "Ш-В: проверяет документ BCREQ второй ролью по чек-листам разделов — «пункт → проблема → вариант»; не объявляет готовность, готовит отчёт к гейту Г-W.", "oneshot", "validation", "Валидация ФТ/ТЗ; Формирование ФТ/ТЗ; Анализ тендерных ТЗ; Impact Analysis; Risk Analysis"),
    "bcreq-scenarios-modeling-oneshot": ("BCREQ Ш-С (2.12/2.13): US, UC", "Ш-С: формирует User Story с критериями приёмки или Use Case (`тип: US | UC`) вне документа BCREQ на основе контекста Ш-1; трассирует сценарии к ФТ.", "oneshot", "modeling", "Формирование UC/US; Формирование ФТ/ТЗ"),
    "bcreq-in-understanding-oneshot": ("BCREQ A-IN: контекст, продукты", "Стадия A-IN для ИИ-агента: Ш-1 и Ш-2 одним вызовом — разделы 1, 2 и ＋2.5, словари и расхождения терминов; заканчивается отчётом по гейту Г-IN.", "oneshot", "understanding", "Формирование ФТ/ТЗ; Анализ тендерных ТЗ; Помощь ПО/ПМ"),
    "bcreq-core-documentation-oneshot": ("BCREQ A-CORE: ФТ, НФТ, UC", "Стадия A-CORE для ИИ-агента: Ш-3…Ш-5 одним вызовом — разделы 3, 4 и 7 (прогон 1); заканчивается отчётом по гейту Г-С1 «Согласование 1» для Заказчика.", "oneshot", "documentation", "Формирование ФТ/ТЗ"),
    "bcreq-work-solution-design-oneshot": ("BCREQ A-WORK: решение, риски", "Стадия A-WORK для ИИ-агента: Ш-6…Ш-9 одним вызовом — разделы 5, 6, 7 (прогон 2) и 8; заканчивается предварительным отчётом по гейту Г-W.", "oneshot", "solution_design", "Формирование ФТ/ТЗ; Impact Analysis; Risk Analysis"),
}
hdr = "| Файл | Название | Токен | Назначение | Режим | Статус | Версия | Когнитивная операция | Процесс БА |\n| --- | --- | --- | --- | --- | --- | --- | --- | --- |\n"
bcreq_rows = "".join(
    f"| {link(n)} | {ti} | `mango-{n}` | {d} | `{mo}` | `draft` | `0.1` | `{op}` | {pr} |\n"
    for n, (ti, d, mo, op, pr) in desc.items()
)
bcreq_sec = (
    "### 0. BCREQ: спецификация бизнes-требований и дизайна решения\n\n"
    "Новые промпты issue #388. Порядок вызова — в разделе\n"
    "[«BCREQ: маршрутизация»](#bcreq-маршрутизация).\n\n" + hdr + bcreq_rows + "\n"
).replace("бизнes", "бизнес")
t = t.replace("### 1. Формирование ФТ/ТЗ\n", bcreq_sec + "### 1. Формирование ФТ/ТЗ\n", 1)

# архивная таблица
arch_rows = "".join(archived(rows[n]) + "\n" for n in ARCH)
anchor = "\nПроцессы «Визуализация UML/BPMN»"
arch_sec = (
    "\n### 7. Архив: промпты, заменённые набором BCREQ (issue #388)\n\n"
    "Файлы перенесены в `prompts/archive/` и не удалены: на них ссылаются\n"
    "записанные прогоны в `runs/`. Замена указана баннером в начале каждого файла.\n\n"
    + hdr + arch_rows
)
i = t.index(anchor)
t = t[:i] + arch_sec + t[i:]

# 4. Счётчики и устаревшая фраза
t = t.replace(
    "В активной библиотеке сейчас 24 файла в `prompts/`. В архиве дополнительно\nсохранены 6 legacy-файлов в `prompts/archive/` для истории, сравнения и аудита.",
    "В активной библиотеке сейчас 20 файлов в `prompts/`: 14 промптов BCREQ и 6\nсопутствующих. В архиве сохранены 24 файла в `prompts/archive/` для истории,\nсравнения, аудита и ссылок из записанных прогонов.",
)
t = t.replace(
    "Процессы «Визуализация UML/BPMN», «Impact Analysis» и «Risk Analysis» пока не\nимеют активных рекомендуемых промптов.",
    "Процесс «Визуализация UML/BPMN» пока не имеет активного рекомендуемого промпта;\n«Impact Analysis» и «Risk Analysis» опираются на шаги BCREQ Ш-2, Ш-6, Ш-9 и Ш-В.",
)
t = t.replace("updated: 2026-06-12", "updated: 2026-10-24", 1)
P.write_text(t, encoding="utf-8")
print("ok")
