#!/usr/bin/env python3
"""Генератор отчёта RUN-0094 v2.0 — L0-оценка исполнимости атомарных требований BCREQ-1199 v2
(issue #486, доработка формы RUN-0094 issue #484).

Форма отчёта (issue #486): слева колонка «№ пп» — сквозной порядковый номер строки отчёта;
строка исходника с заголовком — одна строка; строка исходника с несколькими требованиями
разложена на строки по фрагментам (`fragments.json`, `decompose.py`), значение колонки «№»
исходника перенесено в каждую. Обобщающая вводная фраза — всегда отдельная строка: оценивается
как требование верхнего уровня либо фиксируется как заголовок комплексного требования.

Колонки «№ пп», «№», «Требование» строятся из `fragments.json`; колонки «Оценка» —
«Цитата источника и технический аудит» — из карточек `research/*.json`, проверенных
`verify_cards.py` (правила и сверка цитат issue #484). Строки-заголовки и заголовки
комплексных требований заполняются автоматически (пустая оценка).

    MANGO_BA_RUNTIME_MAIN=/tmp/runtime python3 -I experiments/issue_486/generate_run.py
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
I484 = HERE.parent / "issue_484"
sys.path.insert(0, str(I484))
import ssot  # noqa: E402


def _load(name: str, path: Path):
    """Модуль issue #484 по пути: в sys.path есть одноимённые модули других issue."""
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


g484 = _load("generate_run_484", I484 / "generate_run.py")
verify_cards = _load("verify_cards_486", HERE / "verify_cards.py")

RUN = ssot.ROOT / "runs/2026/RUN-0094"
REPORT = RUN / "outputs/L0-feasibility-assessment-1199-2.md"
OUT, OK, NO_DATA = g484.OUT, g484.OK, g484.NO_DATA
OVER = "Не требует обоснования"
SHEETS, SHEET_TITLES = g484.SHEETS, g484.SHEET_TITLES
HEADER = (
    "| № пп | № | Требование | Оценка | Обоснование и ссылка "
    "| Цитата источника и технический аудит | Комментарий БА |\n"
    "| --- | --- | --- | --- | --- | --- | --- |\n"
)
esc = g484.esc


def heading(frag: dict) -> dict:
    """Строка-заголовок исходника (шапка таблицы, название раздела, подпись таблицы)."""
    return {"verdict": "", "refs": [], "quotes": [], "audit": OK,
            "why": f"Шапка таблицы либо название раздела исходника — не требование, {OUT}; "
                   f"строки раздела оценены построчно."}


def lead(frag: dict, pp: dict[str, int]) -> dict:
    """Заголовок комплексного требования — не оценивается, ссылается на свои строки."""
    nums = [pp[fid] for fid in frag["group"]]
    assert nums and nums == list(range(nums[0], nums[-1] + 1)), frag["fid"]
    where = f"п. {frag['num']}" if frag["num"] else f"«{frag['text']}»"
    span = f"{nums[0]}–{nums[-1]}" if len(nums) > 1 else f"{nums[0]}"
    return {"verdict": "", "refs": [], "quotes": [], "audit": OK,
            "why": f"Заголовок комплексного требования {where} ({frag['reason']}) — не "
                   f"самостоятельное требование, {OUT}; атомарные требования оценены в "
                   f"строках № пп {span}."}


def evaluate() -> tuple[dict, list[dict]]:
    """(source, [фрагмент + pp + entry]) в порядке отчёта."""
    src = json.loads((I484 / "source_transcription.json").read_text(encoding="utf-8"))
    frags = json.loads((HERE / "fragments.json").read_text(encoding="utf-8"))
    data = verify_cards.cards()
    pp = {f["fid"]: i for i, f in enumerate(frags, start=1)}
    need = {f["fid"] for f in frags if f["kind"] == "req"}
    assert set(data) == need, (sorted(need - set(data))[:5], sorted(set(data) - need)[:5])
    out = []
    for f in frags:
        if f["kind"] == "heading":
            entry = heading(f)
        elif f["kind"] == "lead":
            entry = lead(f, pp)
        else:
            entry = data[f["fid"]]
        out.append(dict(f, pp=pp[f["fid"]], entry=entry))
    return src, out


def stats(rows: list[dict]) -> dict[str, int]:
    c = {k: 0 for k in ("rows", "src", "Да", "Частично", "Нет", "nodata", "пусто",
                        "heading", "lead", "top", "out", "over90", "refs")}
    c["src"] = len({r["rid"] for r in rows})
    for r in rows:
        e = r["entry"]
        c["rows"] += 1
        v = e["verdict"]
        c[v or "пусто"] += 1
        c["refs"] += len(e["refs"])
        if v == "Нет" and (NO_DATA in e["why"] or not e["quotes"]):
            c["nodata"] += 1
        if r["kind"] in ("heading", "lead"):
            c[r["kind"]] += 1
        elif not v:
            c["out"] += 1
        if OVER in e["why"]:
            c["over90"] += 1
        if r["kind"] == "req" and top(r, rows):
            c["top"] += 1
    return c


def top(r: dict, rows: list[dict]) -> bool:
    """Обобщающая вводная фраза, оценённая как требование верхнего уровня."""
    same = [x for x in rows if x["rid"] == r["rid"]]
    return (r["kind"] == "req" and len(same) > 1 and same[0]["fid"] == r["fid"]
            and r["text"].rstrip().endswith(":"))


def plural(n: int) -> str:
    return g484.plural(n)


def summary(c: dict[str, int]) -> str:
    rated = c["rows"] - c["пусто"]
    pct = lambda n: f"{n / rated * 100:.1f}".replace(".", ",") + " %" if rated else "—"
    return (f"{c['rows']} {plural(c['rows'])} отчёта из {c['src']} {g484.plural(c['src'])} "
            f"исходника: пусто — {c['пусто']} (заголовки — {c['heading']}, заголовки "
            f"комплексных требований — {c['lead']}, вне функционального контура — {c['out']}); "
            f"оценено — {rated}: `Да` — {c['Да']} ({pct(c['Да'])}), `Частично` — "
            f"{c['Частично']} ({pct(c['Частично'])}), `Нет` — {c['Нет']} ({pct(c['Нет'])}, "
            f"из них «Нет данных» — {c['nodata']})")


def blockers(src: dict, rows: list[dict]) -> str:
    """Сводка по требованиям с пометкой «Блок фактор» — оценки их строк отчёта."""
    sheet = next(s for s in src["sheets"] if s["title"] == "Требования к системе")
    marked = [row[1] for row in sheet["rows"][1:] if len(row) > 3 and row[3] == "Блок фактор"]
    items = []
    for number in marked:
        mine = [r for r in rows if r["sheet"] == "Требования к системе" and r["num"] == number]
        verdicts = [r["entry"]["verdict"] or "пусто" for r in mine]
        span = f"{mine[0]['pp']}–{mine[-1]['pp']}" if len(mine) > 1 else f"{mine[0]['pp']}"
        counts = ", ".join(f"`{v}` — {verdicts.count(v)}"
                           for v in ("Да", "Частично", "Нет", "пусто") if verdicts.count(v))
        items.append(f"п. {number} (№ пп {span}: {counts})")
    return f"{len(items)}: " + "; ".join(items)


def mapping(rows: list[dict]) -> str:
    """Соответствие строк исходника строкам отчёта (трассировка разбиения)."""
    lines = ["| Лист | Строка XLSX | № | № пп | Строк отчёта | Да | Частично | Нет | пусто |",
             "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    order: list[str] = []
    for r in rows:
        if r["rid"] not in order:
            order.append(r["rid"])
    for rid in order:
        mine = [r for r in rows if r["rid"] == rid]
        v = [r["entry"]["verdict"] or "пусто" for r in mine]
        span = f"{mine[0]['pp']}–{mine[-1]['pp']}" if len(mine) > 1 else f"{mine[0]['pp']}"
        sheet = SHEETS.index(mine[0]["sheet"]) + 1
        lines.append(f"| {sheet} | {mine[0]['row']} | {esc(mine[0]['num'])} | {span} | "
                     f"{len(mine)} | {v.count('Да')} | {v.count('Частично')} | {v.count('Нет')} "
                     f"| {v.count('пусто')} |")
    return "\n".join(lines)


def over90(rows: list[dict]) -> str:
    items = []
    for r in rows:
        if r["kind"] == "req" and r["sim"]["max"] > 0.9:
            s = r["sim"]
            item = next(s[f"{m}_item"] for m in ("raw", "core", "dice") if s[m] == s["max"])
            items.append(f"№ пп {r['pp']} — п/п {item}")
    return f"{len(items)} ({', '.join(items)})"


def build() -> str:
    src, rows = evaluate()
    total = stats(rows)
    parts, totals = [], []
    for i, sheet in enumerate(SHEETS, start=1):
        mine = [r for r in rows if r["sheet"] == sheet]
        lines = []
        for r in mine:
            why, quote, verdict = g484.cells(r["entry"])
            lines.append(f"| {r['pp']} | {esc(r['num'])} | {esc(r['text']).replace(chr(10), '<br>')} | "
                         f"Оценка: <br>{verdict} \\| \\|  | {why} | {quote} |  |")
        s = summary(stats(mine))
        totals.append(f"Лист {i} из 2 «{sheet}» — {s}")
        parts.append(f"### Лист {i} из 2: «{SHEET_TITLES[sheet]}»\n\nИтог: {s}.\n\n"
                     + HEADER + "\n".join(lines) + "\n")
    total_lines = "\n".join(f"- {t};" for t in totals)
    source = src["source"]
    size = f"{source['size']:,}".replace(",", " ")
    return f"""---
status: draft
version: "2.0"
updated: 2026-11-16
ai-generated: true
type: analysis
scope: bcreq-1199-v2-only
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/484"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/486"
---

# L0 — оценка исполнимости ТЗ BCREQ-1199 (2-я версия)

Исходник Заказчика — «{source['name']}» (sha256 `{source['sha256']}`, {size} байт,
[вложение issue #484]({ssot.SOURCE_URL})); контрольные суммы всех входов — в
[`inputs/README.md`](../inputs/README.md). Оценены оба листа с требованиями, они разделены
заголовками `### Лист N из 2`. Версия 2.0 (issue #486): составные требования разложены на
атомарные строки со сквозной нумерацией «№ пп», каждая строка оценена отдельно.

**Статистика** (знаменатель процентов — оценённые строки отчёта, без пустых оценок):

- всего — {summary(total)};
{total_lines}
- обобщающих вводных фраз, оценённых как требование верхнего уровня, — {total['top']};
- ссылок на SSOT в колонке 5 — {total['refs']}, столько же дословных цитат в колонке 6;
- строк с формулировкой «Не требует обоснования» по правилу > 90 % — {over90(rows)};
- требований с пометкой «Блок фактор» — {blockers(src, rows)}.

**Форма отчёта (issue #486).**

- Колонка 1 «№ пп» — сквозной порядковый номер строки отчёта (1…{total['rows']}, оба листа,
  без пропусков); на него ссылаются заголовки комплексных требований и сводки.
- Колонка 2 «№» — литеральное значение колонки «№ пункта» (лист 1) или «№» (лист SLA)
  строки исходника; оно повторяется во всех строках отчёта, полученных из одной строки
  исходника (дубликаты допустимы). У строк исходника без номера колонка пустая.
- Колонка 3 «Требование» — дословный фрагмент ячейки исходника (переводы строк — `<br>`).
  Фрагменты одной строки исходника идут в порядке текста и вместе покрывают ячейку целиком
  (с точностью до пробельных символов на границах) — это проверяет валидатор.
- Строка исходника с заголовком (шапка таблицы листа 1, название раздела и подписи Таблицы 1
  листа SLA) остаётся одной строкой отчёта — пустая оценка.
- Строка исходника с несколькими требованиями разложена на строки
  (`experiments/issue_486/decompose.py`):
  - перечень с маркером `-` — каждый пункт перечня отдельной строкой (маркер сохранён),
    текст до первого пункта — обобщающая вводная фраза;
  - сплошной текст — по предложениям или абзацам, содержащим самостоятельное требование;
    определения и пояснения (например, формула расчёта, состав отчёта) остаются в строке
    требования, к которому относятся, если сами не являются требованием;
  - Таблица 1 листа SLA — каждая непустая строка ячейки (подпись приоритета, время реакции,
    время решения) отдельной строкой.
- Обобщающая вводная фраза — всегда отдельная строка:
  - если она однозначно трактуется как требование верхнего уровня (например, «Система
    должна предоставить функционал …:»), она оценена как самостоятельное требование — по
    собственной формулировке (наличие функции/продукта и её собственные условия), без
    повторения оценок подпунктов;
  - иначе (условие показа на презентации, этап внедрения как перечень работ, перечень функций
    админ. панели, подписи приоритетов Таблицы 1) она зафиксирована как заголовок комплексного
    требования: пустая оценка, «{OUT}», ссылка на диапазон «№ пп» его атомарных требований.
- Сквозное соответствие строк исходника строкам отчёта — в таблице «Трассировка разбиения»
  ниже.

**Методика оценки** (правила issue #484 без изменений, применены к каждой атомарной строке).

- Колонки исходника перенесены без правок: опечатки («программне обеспечение»,
  «аппеляций», «Отсутсвие») сохранены. Эталон транскрипции строит
  `experiments/issue_484/make_transcription.py` (openpyxl), независимо сверяет
  `experiments/issue_484/check_source.py` (stdlib `zipfile` + `xml.etree` по OOXML):
  3 листа, 240 ячеек, 21 632 символа, расхождений 0.
- Исходник — книга из трёх листов; требования содержат два видимых листа («Требования к
  системе» и «SLA»), оба оценены полностью. Третий лист «Лист1» скрыт и содержит пять
  словарей выпадающих списков — требованием не является и в таблицу не включён.
- На листе «SLA» ячейка «Требование» склеивает непустые значения колонок «Требования» и
  «Максимальный срок решения заявки»: в Таблице 1 ячейка «Тип Заявки» объединена на две
  строки исходника (`B19:B20`, `B21:B22`, `B23:B24`, `B25:B26`), поэтому у второй строки пары
  заполнена только колонка сроков; её фрагменты относятся к заголовку из строки выше.
- Колонка 4 — формат `Оценка: <br>[Оценка Исполнителя] | [ ] | [ ]`; оценка строго по шкале
  `Да / Частично / Нет / пусто`. Колонки исходника «Факт реализации» и «Срок доработки»
  пусты во всех строках (кроме служебной пометки «Не применима к блок-факторам»), поэтому
  средняя часть колонки 4 пустая.
- `Частично` — только если собственная формулировка строки раскладывается на атомарные
  части (несколько функций, функция и числовой порог) и подтверждена лишь часть из них;
  в колонке 5 названы подтверждённые и неподтверждённые части. Строка с одной атомарной
  частью получает `Да`, `Нет` или пустую оценку. Числовые пороги (5 %, 80 %, 95 %, 98 %,
  3 месяца, 15 минут, 5–15 секунд, 100 операторов) подтверждаются только прямым
  утверждением SSOT.
- `Нет` — функция не подтверждена SSOT или требует доработки; «Нет данных» — в SSOT нет
  сведений для проверки.
- SSOT: шаблон «ТЗ-тендеров-v4» ([вложение issue #484]({ssot.TENDER_URL}), sha256
  `{ssot.TENDER_SHA}`, высший приоритет и неоспорим) и БЗ
  [`mango-ba-ai-runtime/docs/kb`](https://github.com/G-Ivan-A/mango-ba-ai-runtime/tree/{ssot.COMMIT}/docs/kb)
  на commit `{ssot.COMMIT}`; веб — только домены и поддомены Mango Office. Общие знания
  модели не использовались: каждая оценка `Да` / `Частично` опирается на дословную цитату
  SSOT в колонке 6; цитаты всех строк сверяют `experiments/issue_486/verify_cards.py` и
  `experiments/issue_484/verify_quotes.py` (расхождений 0).
- Совпадение > 90 % с пунктом «Шаблона ТЗ для тендеров v4» (максимум из метрик raw / core /
  dice `experiments/issue_484/atomize.py`, как в RUN-0070…RUN-0093) считается для каждой
  атомарной строки и даёт оценку `Да` с формулировкой «{OVER}» и ссылкой на п/п
  шаблона; отличия формулировки (более строгие условия Заказчика) — в аудите.
- Требования к организации работ Исполнителя (внедрения и презентации, обучение и
  инструкции, лицензии и подтверждающие документы, аккаунт-менеджер, одно окно, сроки
  реакции и решения заявок, отчётность, штрафы) функцией продукта не являются — пустая
  оценка и пометка «{OUT}». Это не отказ: такие строки требуют коммерческого и
  юридического согласования, а не технической проверки.
- Правило базового движка («Да (базовая функция Yandex SpeechKit)») не применялось:
  официального источника вендора в разрешённых доменах нет.
- Трактовки неоднозначных формулировок в пользу Mango указаны в аудите колонки 6
  («Трактовка в пользу Mango: …»). Там же — платные опции, лимиты и отдельные продукты:
  оценка `Да` или `Частично` не означает включения функции в базовый тариф.
- Колонка 7 «Комментарий БА» оставлена пустой для бизнес-аналитика.

Сравнение с предыдущей версией ТЗ (RUN-0065) — в
[`outputs/analytical-note-1199-v1-vs-v2.md`](analytical-note-1199-v1-vs-v2.md).

**Служебные колонки исходника.** Форма отчёта переносит только «№ пункта» и «Требования»,
поэтому остальные колонки листа «Требования к системе» приведены отдельной таблицей без
изменений. Колонки «Факт реализации» и «Срок доработки» заполняет Исполнитель; в исходнике
они пусты (кроме объединённой ячейки `F2:F7` — пометка относится к требованиям 1–6).
Значения выпадающих списков задаёт скрытый «Лист1»: «Реализован», «Частично реализован»,
«Не реализован» — для «Факта реализации»; «До 2 мес», «2-4 мес», «более 4 мес»,
«Невозможна реализация» — для «Срока доработки».

{g484.service_table(src)}

**Трассировка разбиения** — строки исходника и диапазоны «№ пп» отчёта:

{mapping(rows)}

## Отчёт: оценка исполнимости «{source['name']}»

""" + "\n".join(parts)


if __name__ == "__main__":
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(build(), encoding="utf-8")
    _src, rows = evaluate()
    c = stats(rows)
    print(f"written {REPORT.relative_to(ssot.ROOT)} (runtime {ssot.COMMIT})")
    print(summary(c))
    print(f"top {c['top']}, refs {c['refs']}, over90 {over90(rows)}")
