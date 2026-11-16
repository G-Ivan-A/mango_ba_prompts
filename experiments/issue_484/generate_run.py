#!/usr/bin/env python3
"""Генератор отчёта RUN-0094 — L0-оценка исполнимости ТЗ BCREQ-1199 v2 (issue #484).

Отчёт строится детерминированно: колонки 1–2 берутся из эталонной транскрипции
`source_transcription.json` (openpyxl; независимая сверка — `check_source.py` на stdlib),
колонки 3–5 — из исследовательских карточек `research/*.json`, проверенных
`verify_quotes.py` (каждая цитата дословно присутствует в источнике ссылки).

Строки-заголовки (шапка таблицы, название раздела, подпись таблицы) оцениваются
автоматически: пустая оценка, «вне функционального контура».

    MANGO_BA_RUNTIME_MAIN=/tmp/runtime python3 -I experiments/issue_484/generate_run.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ssot  # noqa: E402

RUN = ssot.ROOT / "runs/2026/RUN-0094"
REPORT = RUN / "outputs/L0-feasibility-assessment-1199-2.md"

NO_DATA = "Нет данных"
OK = "Архитектурных противоречий не выявлено, трассировка подтверждена."
OUT = "вне функционального контура"
VERDICTS = ("Да", "Частично", "Нет", "")
HEADER = (
    "| № | Требование | Оценка | Обоснование и ссылка | Цитата источника и технический аудит | Комментарий БА |\n"
    "| --- | --- | --- | --- | --- | --- |\n"
)
# Листы исходника с требованиями; скрытый служебный лист «Лист1» (словарь выпадающего
# списка «Реализован / Частично реализован / Не реализован») требованиями не является.
SHEETS = ("Требования к системе", "SLA")
SHEET_TITLES = {
    "Требования к системе": "Требования к системе",
    "SLA": "SLA (требования к системе и к технической поддержке)",
}
# Строки без требования: шапка таблицы листа 1, название раздела и подписи таблицы листа SLA.
HEADINGS = ("Требования к системе!1", "SLA!1", "SLA!17", "SLA!18")


def esc(text: str) -> str:
    return text.replace("|", "\\|")


def row_text(sheet: str, values: list[str]) -> str:
    """Колонка 2: непустые значения колонок требования исходника, склеенные переводом строки.

    Лист «Требования к системе» — колонка «Требования»; лист «SLA» — «Требования» и
    «Максимальный срок решения заявки» (у строк Таблицы 1 ячейка «Тип Заявки» объединена
    на две строки, поэтому у второй строки пары заполнена только колонка сроков).
    """
    text = values[1] if len(values) > 1 else ""
    tail = values[2] if sheet == "SLA" and len(values) > 2 else ""
    return "\n".join(t for t in (text, tail) if t)


def auto(rid: str) -> dict:
    """Оценка строки без ручного разбора — строка-заголовок исходника."""
    assert rid in HEADINGS, rid
    return {
        "kind": "heading", "verdict": "", "refs": [], "quotes": [],
        "why": f"Шапка таблицы либо название раздела исходника — не требование, {OUT}; "
               f"строки раздела оценены построчно.",
        "audit": OK,
    }


def cells(entry: dict) -> tuple[str, str, str]:
    """(колонка 4, колонка 5, оценка) с подстановкой ссылок после сносок."""
    verdict, why, refs, quotes = entry["verdict"], entry["why"], entry["refs"], entry["quotes"]
    assert verdict in VERDICTS, verdict
    assert len(refs) == len(quotes), entry
    for i, ref in enumerate(refs, start=1):
        marker = f"[{i}]"
        assert why.count(marker) == 1, (marker, why)
        why = why.replace(marker, f"{marker} {ssot.link(ref)}")
    assert not re.search(r"\[\d+\](?! \[)", why), why
    quote = " ".join(f"[{i}] «{q}»" for i, q in enumerate(quotes, start=1))
    if verdict == "":
        assert OUT in why, why
        quote = " ".join(filter(None, [OUT[0].upper() + OUT[1:] + ".", quote]))
    elif verdict == "Нет" and (NO_DATA in why or not quotes):
        quote = " ".join(filter(None, [NO_DATA + ".", quote]))
    if verdict in ("Да", "Частично"):
        assert refs, entry
    audit = entry["audit"].strip()
    audit = OK if audit == "OK" else audit
    return esc(why), esc(f"{quote}<br>Аудит: {audit}"), verdict


def evaluate() -> tuple[dict, list]:
    """(source, [(sheet, row_no, №, требование, entry)]) — оценка каждой строки исходника."""
    src = json.loads((HERE / "source_transcription.json").read_text(encoding="utf-8"))
    data = ssot.research()
    out, seen = [], set()
    for sheet in src["sheets"]:
        if sheet["title"] not in SHEETS:
            continue
        for row in sheet["rows"]:
            ri, values = row[0], row[1:]
            if not any(values):
                continue
            rid = f'{sheet["title"]}!{ri}'
            seen.add(rid)
            entry = dict(data[rid], kind="research") if rid in data else auto(rid)
            out.append((sheet["title"], ri, values[0], row_text(sheet["title"], values), entry))
    unknown = set(data) - seen
    assert not unknown, f"карточки без строк исходника: {unknown}"
    return src, out


def blockers(src: dict, pairs: list) -> str:
    """Сводка по требованиям с пометкой «Блок фактор» в колонке C листа 1."""
    sheet = next(s for s in src["sheets"] if s["title"] == "Требования к системе")
    marked = {row[1] for row in sheet["rows"][1:] if len(row) > 3 and row[3] == "Блок фактор"}
    items = [f"п. {number} — `{entry['verdict'] or 'пусто'}`"
             for name, _ri, number, _vis, entry in pairs
             if name == "Требования к системе" and number in marked]
    return f"{len(items)} ({', '.join(items)})"


def service_table(src: dict) -> str:
    """Служебные колонки листа 1 (C–F), которые контракт шести колонок не переносит."""
    sheet = next(s for s in src["sheets"] if s["title"] == "Требования к системе")
    head = sheet["rows"][0][1:]
    lines = [f"| {' | '.join(esc(h) for h in [head[0]] + list(head[2:]))} |",
             "| " + " | ".join(["---"] * 5) + " |"]
    for row in sheet["rows"][1:]:
        values = row[1:]
        if not any(values):
            continue
        cells_ = [values[0]] + list(values[2:])
        lines.append("| " + " | ".join(esc(c).replace("\n", "<br>") for c in cells_) + " |")
    return "\n".join(lines)


def plural(n: int) -> str:
    if n % 10 == 1 and n % 100 != 11:
        return "строка"
    return "строки" if 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14 else "строк"


def stats(pairs: list) -> dict[str, int]:
    c = {k: 0 for k in ("rows", "Да", "Частично", "Нет", "nodata", "пусто",
                        "heading", "out", "over90", "refs")}
    for *_row, entry in pairs:
        c["rows"] += 1
        v = entry["verdict"]
        c[v or "пусто"] += 1
        c["refs"] += len(entry["refs"])
        if v == "Нет" and (NO_DATA in entry["why"] or not entry["quotes"]):
            c["nodata"] += 1
        if not v:
            c["heading" if entry["kind"] == "heading" else "out"] += 1
        if "Не требует обоснования" in entry["why"]:
            c["over90"] += 1
    return c


def summary(c: dict[str, int]) -> str:
    rated = c["rows"] - c["пусто"]
    pct = lambda n: f"{n / rated * 100:.1f}".replace(".", ",") + " %" if rated else "—"
    return (f"{c['rows']} {plural(c['rows'])}: пусто — {c['пусто']} (заголовки — {c['heading']}, "
            f"вне функционального контура — {c['out']}); оценено — {rated}: "
            f"`Да` — {c['Да']} ({pct(c['Да'])}), `Частично` — {c['Частично']} ({pct(c['Частично'])}), "
            f"`Нет` — {c['Нет']} ({pct(c['Нет'])}, из них «Нет данных» — {c['nodata']})")


def build() -> str:
    src, pairs = evaluate()
    total = stats(pairs)
    parts, totals = [], []
    for i, sheet in enumerate(SHEETS, start=1):
        mine = [p for p in pairs if p[0] == sheet]
        rows = []
        for _sheet, _ri, number, visible, entry in mine:
            why, quote, verdict = cells(entry)
            rows.append(f"| {esc(number)} | {esc(visible).replace(chr(10), '<br>')} | "
                        f"Оценка: <br>{verdict} \\| \\|  | {why} | {quote} |  |")
        s = summary(stats(mine))
        totals.append(f"Лист {i} из 2 «{sheet}» — {s}")
        parts.append(f"### Лист {i} из 2: «{SHEET_TITLES[sheet]}»\n\nИтог: {s}.\n\n"
                     + HEADER + "\n".join(rows) + "\n")
    total_lines = "\n".join(f"- {t};" for t in totals)
    source = src["source"]
    service = service_table(src)
    block = blockers(src, pairs)
    size = f"{source['size']:,}".replace(",", " ")
    atoms = len(json.loads((HERE / "atom_similarity.json").read_text(encoding="utf-8")))
    return f"""---
status: draft
version: "1.0"
updated: 2026-11-13
ai-generated: true
type: analysis
scope: bcreq-1199-v2-only
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/484"
---

# L0 — оценка исполнимости ТЗ BCREQ-1199 (2-я версия)

Исходник Заказчика — «{source['name']}» (sha256 `{source['sha256']}`, {size} байт,
[вложение issue #484]({ssot.SOURCE_URL})); контрольные суммы всех входов — в
[`inputs/README.md`](../inputs/README.md). Оценены оба листа с требованиями, они разделены
заголовками `### Лист N из 2`.

**Статистика** (знаменатель процентов — оценённые строки, без пустых оценок):

- всего — {summary(total)};
{total_lines}
- ссылок на SSOT в колонке 4 — {total['refs']}, столько же дословных цитат в колонке 5;
- строк с формулировкой «Не требует обоснования» по правилу > 90 % — {total['over90']};
- требований с пометкой «Блок фактор» — {block}.

**Методика.**

- Колонки 1–2 перенесены из ячеек XLSX без правок: опечатки исходника («программне
  обеспечение», «аппеляций», «Отсутсвие») сохранены, переводы строк внутри ячейки — `<br>`.
  Колонка 1 — литеральное значение колонки «№ пункта» (лист 1) или «№» (лист SLA); у строк
  без номера колонка 1 пустая. Эталон транскрипции строит
  `experiments/issue_484/make_transcription.py` (openpyxl), независимо сверяет
  `experiments/issue_484/check_source.py` (другая реализация: stdlib `zipfile` +
  `xml.etree` по OOXML): 3 листа, 240 ячеек, 21 632 символа, расхождений 0.
- Исходник — книга из трёх листов; требования содержат два видимых листа («Требования к
  системе» и «SLA»), оба оценены полностью. Третий лист «Лист1» скрыт и содержит пять
  словарей выпадающих списков (строки 1–3 «Реализован / Частично реализован / Не
  реализован»; 5–6; 8–9 «Согласны полностью / Не согласны»; 12–15 «До 2 мес / 2-4 мес /
  более 4 мес / Невозможна реализация»; 22–24 «Готовы предоставить в полном объеме /
  частично / Не готовы предоставить») — требованием не является и в таблицу не включён.
- На листе «SLA» колонка 2 отчёта склеивает через `<br>` непустые значения колонок
  «Требования» и «Максимальный срок решения заявки»: в Таблице 1 ячейка «Тип Заявки»
  объединена на две строки исходника (`B19:B20`, `B21:B22`, `B23:B24`, `B25:B26`), поэтому
  у второй строки каждой пары заполнена только колонка сроков. Строка остаётся отдельной —
  это сохраняет соответствие строк отчёта строкам исходника байт-в-байт.
- Колонка 3 — формат `Оценка: <br>[Оценка Исполнителя] | [ ] | [ ]`; оценка строго по шкале
  `Да / Частично / Нет / пусто`. Колонка исходника «Факт реализации» (её заполняет
  Исполнитель) и колонка «Срок доработки» пусты во всех строках, кроме служебной пометки
  «Не применима к блок-факторам», поэтому средняя часть колонки 3 пустая.
- `Частично` применяется только там, где требование раскладывается на атомарные части и
  часть из них подтверждена SSOT: разбор в `experiments/issue_484/atomize.py`
  ({atoms} атомарных частей в 43 строках). Числовые пороги (5 %, 80 %, 95 %, 98 %, 3 месяца, 15 минут,
  5–15 секунд, 100 операторов) считаются отдельными атомарными частями и подтверждаются
  только прямым утверждением SSOT.
- SSOT: шаблон «ТЗ-тендеров-v4» ([вложение issue #484]({ssot.TENDER_URL}), sha256
  `{ssot.TENDER_SHA}`, высший приоритет и неоспорим) и БЗ
  [`mango-ba-ai-runtime/docs/kb`](https://github.com/G-Ivan-A/mango-ba-ai-runtime/tree/{ssot.COMMIT}/docs/kb)
  на commit `{ssot.COMMIT}`; веб — только домены и поддомены Mango Office. Общие знания
  модели не использовались: каждая оценка `Да` / `Частично` опирается на дословную цитату
  SSOT в колонке 5, которую построчно сверяет `experiments/issue_484/verify_quotes.py`
  (расхождений 0).
- Совпадение > 90 % со «Шаблоном ТЗ для тендеров v4» (`experiments/issue_484/atomize.py`,
  максимум из метрик raw / core / dice, как в RUN-0070…RUN-0093) даёт формулировку
  «Не требует обоснования» со ссылкой на п/п шаблона. Исходник — собственная форма
  Заказчика, а не шаблон: порог превышают только 7 атомарных частей из {atoms}
  (п/п 2.9.1, 2.18.1, 2.18.3, 2.18.9, 2.15.6, 2.15.11, 9.11), поэтому остальные строки
  разобраны по компонентам с цитатами. Строка целиком получает эту формулировку (и
  оценку `Да`) только когда порог превышает всё требование — таких строк 1 (п. 1.4
  листа SLA); в составном требовании формулировка стоит у конкретной атомарной части
  (п. 17 листа 1, «каждые 15 минут» — п/п 2.15.6), а оценка строки выводится из всех
  частей.
- Требования к организации работ Исполнителя (внедрения и презентации, обучение и
  инструкции, аккаунт-менеджер, одно окно, сроки реакции и решения заявок, штрафы, права
  на обновления) функцией продукта не являются — пустая оценка и пометка «{OUT}». Это не
  отказ: такие строки требуют коммерческого и юридического согласования, а не технической
  проверки.
- Правило базового движка («Да (базовая функция Yandex SpeechKit)») не применялось:
  официального источника вендора в разрешённых доменах нет.
- Трактовки неоднозначных формулировок в пользу Mango указаны в аудите колонки 5
  («Трактовка в пользу Mango: …»). Там же — платные опции, лимиты и отдельные продукты:
  оценка `Да` или `Частично` не означает включения функции в базовый тариф.
- Колонка 6 «Комментарий БА» оставлена пустой для бизнес-аналитика.

Сравнение с предыдущей версией ТЗ (RUN-0065) — в
[`outputs/analytical-note-1199-v1-vs-v2.md`](analytical-note-1199-v1-vs-v2.md).

**Служебные колонки исходника.** Контракт шести колонок переносит только «№ пункта» и
«Требования», поэтому остальные колонки листа «Требования к системе» приведены отдельной
таблицей без изменений. Колонки «Факт реализации» и «Срок доработки» заполняет Исполнитель;
в исходнике они пусты (кроме объединённой ячейки `F2:F7` — пометка относится к требованиям
1–6). Значения выпадающих списков задаёт скрытый «Лист1»: «Реализован», «Частично
реализован», «Не реализован» — для «Факта реализации»; «До 2 мес», «2-4 мес», «более 4 мес»,
«Невозможна реализация» — для «Срока доработки».

{service}

## Отчёт: оценка исполнимости «{source['name']}»

""" + "\n".join(parts)


if __name__ == "__main__":
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(build(), encoding="utf-8")
    src, pairs = evaluate()
    c = stats(pairs)
    print(f"written {REPORT.relative_to(ssot.ROOT)} (runtime {ssot.COMMIT})")
    print(summary(c))
