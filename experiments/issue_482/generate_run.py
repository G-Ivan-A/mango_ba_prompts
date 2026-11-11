#!/usr/bin/env python3
"""Генератор отчёта RUN-0093 (issue #482): L0-оценка исполнимости ТЗ BCREQ-1140.

Исходник Заказчика — «ТЗ газификация ХХХ области.pdf» (33 с., правки рецензирования Word):
два документа в одном PDF, в отчёте разделены `### Документ N из 2: «…»`.

Колонки 1–2 берутся из `source_transcription.json` без изменений (зачёркнутый правкой текст —
`~~…~~`, перевод строки — `<br>`). Колонка 3 — `Оценка: <br>[оценка Исполнителя] | [ ] | [ ]`
(колонки оценки поставщика в исходнике нет — средняя часть пустая).

Оценки строятся так (по порядку приоритета):
1. `research/*.json` (`{rid: {verdict, why, refs, quotes, audit}}`) — ручная оценка с
   цитатами SSOT (вложенное ТЗ ВДГО/ВКГО и пункты v4, в которых WhatsApp заменён на MAX);
2. строка целиком зачёркнута правкой (принятый текст пуст) — требование не предъявляется;
3. заголовок раздела (`HEADINGS`) — оценивается построчно в подпунктах;
4. сходство с пунктом шаблона ТЗ-тендеров-v4 > 90 % (`tender_similarity.json`) — `Да`,
   «Не требует обоснования» со ссылкой на п/п. Генератор дополнительно требует, чтобы
   принятый текст совпадал с пунктом дословно после нормализации (пробелы, маркеры,
   конечная пунктуация, артефакт «слово- слово» текстового слоя шаблона), иначе — ошибка:
   такая строка обязана быть разобрана вручную в `research/`.

Ссылки на БЗ строятся по frontmatter разделов runtime-репозитория (`MANGO_BA_RUNTIME_MAIN`,
commit фиксируется в отчёте), ссылки на шаблон — по `experiments/issue_367/tender_index.json`
(тот же PDF, SHA-256 612e5e09…).

    MANGO_BA_RUNTIME_MAIN=/tmp/rt-main python3 -I experiments/issue_482/generate_run.py
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from tender_similarity import ITEM, P5, PAGE, low  # noqa: E402

ROOT = HERE.parents[1]
RUN = ROOT / "runs/2026/RUN-0093"
REPORT = RUN / "outputs/L0-feasibility-assessment-1140.md"
RUNTIME = Path(os.environ.get("MANGO_BA_RUNTIME_MAIN", "/tmp/rt-main"))
COMMIT = subprocess.check_output(["git", "-C", str(RUNTIME), "rev-parse", "HEAD"], text=True).strip()
KB = RUNTIME / "docs/kb"
BLOB = f"https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/{COMMIT}/docs/kb/"
SOURCE_URL = "https://github.com/user-attachments/files/34651826/default.pdf"
TENDER_URL = "https://github.com/user-attachments/files/34651817/-.-v4.pdf"
TENDER_SHA = "612e5e0938b9d4edad8e341f7fb03ba8498f7ec12dea0fe88f71e6817169d4cc"
SIMILARITY = json.loads((HERE / "tender_similarity.json").read_text(encoding="utf-8"))
TENDER_P5_TITLE = "2. Общие требования к оказанию услуг Исполнителем"

NO_DATA = "Нет данных"
OK = "Архитектурных противоречий не выявлено, трассировка подтверждена."
OUT = "вне функционального контура"
VERDICTS = ("Да", "Частично", "Нет", "")
HEADER = (
    "| № | Требование | Оценка | Обоснование и ссылка | Цитата источника и технический аудит | Комментарий БА |\n"
    "| --- | --- | --- | --- | --- | --- |\n"
)
DOCS_TITLES = {
    1: ("Функциональные требования", "с.1–31"),
    2: ("Техническое задание на оказание услуг по автоматизации рабочих процессов по выполнению технического "
        "обслуживания (ТО) внутридомового (ВДГО) и внутриквартирного (ВКГО) газового оборудования, а также "
        "выполнения ремонтных заявок", "с.32–33"),
}
# Строки-заголовки: только название раздела / вводная фраза перечня подпунктов.
HEADINGS = {
    "R001", "R006", "R010", "R170", "R224", "R240", "R250", "R262", "R270", "R274", "R282", "R294",
    "R295", "R310", "R312", "R317",
    "R323", "R324", "R331", "R339", "R342", "R349",
}


def front(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines()[1:]:
        if line.strip() == "---":
            break
        key, _, value = line.partition(":")
        if ":" in line and not line.startswith((" ", "-")):
            value = value.strip()
            # YAML-скаляр в кавычках: снимается только внешняя пара ("Группа отчетов 'Продажи'")
            if len(value) > 1 and value[0] == value[-1] and value[0] in "\"'":
                value = value[1:-1]
            data[key.strip()] = value
    return data


def doc_dirs() -> dict[str, str]:
    """doc_code -> каталог документа БЗ (по frontmatter первого раздела)."""
    dirs: dict[str, str] = {}
    for sections in sorted(KB.glob("**/sections")):
        first = next(iter(sorted(sections.glob("*.md"))), None)
        if first is not None:
            dirs[front(first)["doc_code"]] = str(sections.parent.relative_to(KB))
    return dirs


DOCS = doc_dirs()


def kb_path(ref: str) -> Path:
    doc, _, section_file = ref.partition("/")
    return KB / DOCS[doc] / "sections" / section_file


def kb(ref: str) -> str:
    """Атомарная ссылка `[ДОК, §X «Заголовок», с.Y](url)` по frontmatter раздела."""
    doc, _, section_file = ref.partition("/")
    fm = front(kb_path(ref))
    assert fm["doc_code"] == doc, ref
    number = fm.get("pdf_section", "")
    if number in ("", "0", "-", "—"):
        number = fm.get("section", "")
    if number in ("", "0", "-", "—"):
        number = ""
    sect = f"§{number} " if number else ""
    return f"[{doc}, {sect}«{fm['title']}», с.{fm['pages']}]({BLOB}{DOCS[doc]}/sections/{section_file})"


def tender_text(item: str) -> str:
    """Текст пункта шаблона без колонки «наличие» (`p5` — весь раздел с.5, `p5:N` — абзац N)."""
    if item == "p5":
        return " ".join(P5)
    if item.startswith("p5:"):
        return P5[int(item[3:]) - 1]
    return ITEM[item]


def tv4(item: str) -> str:
    if item.startswith("p5"):
        return f"[ТЗ-тендеров-v4, разд. «{TENDER_P5_TITLE}», с.5]({TENDER_URL})"
    return f"[ТЗ-тендеров-v4, п/п {item}, с.{PAGE[item]}]({TENDER_URL})"


def link(ref: str) -> str:
    kind, _, value = ref.partition(":")
    if kind == "kb":
        return kb(value)
    if kind == "tv4":
        return tv4(value)
    if kind == "portal":
        url, _, title = value.partition("|")
        return f"[Портал_Mango - {title}]({url})"
    raise ValueError(ref)


def load() -> dict[str, dict]:
    data: dict[str, dict] = {}
    for path in sorted((HERE / "research").glob("*.json")):
        part = json.loads(path.read_text(encoding="utf-8"))
        overlap = data.keys() & part.keys()
        assert not overlap, (path, overlap)
        data.update(part)
    return data


def esc(text: str) -> str:
    return text.replace("|", "\\|")


def num(value: float) -> str:
    return f"{value:.2f}".replace(".", ",")


def hyphen(text: str) -> str:
    """Артефакт текстового слоя шаблона: перенос «чат-|ботов» извлекается как «чат- ботов»."""
    return re.sub(r"(?<=\w)- (?=\w)", "-", text)


def auto(rid: str, accepted: str) -> dict:
    """Оценка строки без ручного разбора: удалённая правкой, заголовок или > 90 % с шаблоном v4."""
    if not accepted:
        return {
            "kind": "deleted", "verdict": "", "refs": [], "quotes": [],
            "why": f"Пункт целиком зачёркнут правкой рецензирования исходника — требование не предъявляется, "
                   f"{OUT}.",
            "audit": "Текст сохранён в колонках 1–2 зачёркнутым для переноса байт-в-байт; оценивать нечего. " + OK,
        }
    if rid in HEADINGS:
        return {
            "kind": "heading", "verdict": "", "refs": [], "quotes": [],
            "why": f"Заголовок раздела / вводная фраза перечня — {OUT}; подпункты оценены построчно.",
            "audit": OK,
        }
    raw, item, core, _cn, dice, _dn = SIMILARITY[rid]
    assert max(raw, core, dice) > 0.9, (rid, SIMILARITY[rid])
    text = tender_text(item)
    same = low(accepted) == low(text)
    assert same or low(accepted) == low(hyphen(text)), (rid, item, "нужен ручной разбор в research/")
    if same:
        note = "Текст совпадает дословно; отличия только в пробелах, маркерах списка и конечной пунктуации."
    else:
        word = re.search(r"[\w-]*\w- \w+", text).group(0)
        note = ("Текст совпадает дословно; кроме пунктуации, отличие только в артефакте текстового слоя "
                f"шаблона (перенос со знаком «-»: «{word}»).")
    ref = "tv4:" + item
    return {
        "kind": "over90", "verdict": "Да", "refs": [ref],
        "quotes": [text.replace("", "•")],
        "why": f"Не требует обоснования: совпадение с ТЗ-тендеров-v4 > 90 % "
               f"({'разд. с.5' if item.startswith('p5') else 'п/п ' + item}) [1]",
        "audit": f"Сходство с пунктом шаблона: raw {num(raw)}, core {num(core)}, dice {num(dice)}. {note} {OK}",
    }


def cells(entry: dict) -> tuple[str, str, str]:
    verdict, why, refs, quotes = entry["verdict"], entry["why"], entry["refs"], entry["quotes"]
    assert verdict in VERDICTS, verdict
    assert len(refs) == len(quotes), entry
    for i, ref in enumerate(refs, start=1):
        marker = f"[{i}]"
        assert why.count(marker) == 1, (marker, why)
        why = why.replace(marker, f"{marker} {link(ref)}")
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


def plural(n: int) -> str:
    if n % 10 == 1 and n % 100 != 11:
        return "строка"
    return "строки" if 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14 else "строк"


def evaluate() -> tuple[dict, list]:
    """(source, [(row, entry)]) — оценка каждой строки транскрипции."""
    src = json.loads((HERE / "source_transcription.json").read_text(encoding="utf-8"))
    data = load()
    rids = {row[0] for row in src["rows"]}
    assert data.keys() <= rids, data.keys() - rids
    out = []
    for row in src["rows"]:
        rid, accepted = row[0], row[4]
        if rid in data:
            assert accepted and rid not in HEADINGS, rid
            entry = dict(data[rid], kind="research")
        else:
            entry = auto(rid, accepted)
        out.append((row, entry))
    return src, out


def stats(pairs: list) -> dict[str, int]:
    c = {k: 0 for k in ("rows", "Да", "Частично", "Нет", "nodata", "пусто", "heading", "deleted", "out", "over90")}
    for _row, entry in pairs:
        c["rows"] += 1
        v = entry["verdict"]
        c[v or "пусто"] += 1
        if v == "Нет" and (NO_DATA in entry["why"] or not entry["quotes"]):
            c["nodata"] += 1
        if not v:
            c[{"heading": "heading", "deleted": "deleted"}.get(entry["kind"], "out")] += 1
        if entry["kind"] == "over90":
            c["over90"] += 1
    return c


def summary(c: dict[str, int]) -> str:
    rated = c["rows"] - c["пусто"]
    pct = lambda n: f"{n / rated * 100:.1f}".replace(".", ",") + " %" if rated else "—"
    return (f"{c['rows']} {plural(c['rows'])}: пусто — {c['пусто']} (заголовки — {c['heading']}, зачёркнуты "
            f"правкой — {c['deleted']}, вне функционального контура — {c['out']}); оценено — {rated}: "
            f"`Да` — {c['Да']} ({pct(c['Да'])}), `Частично` — {c['Частично']} ({pct(c['Частично'])}), "
            f"`Нет` — {c['Нет']} ({pct(c['Нет'])}, из них «Нет данных» — {c['nodata']}); "
            f"по правилу > 90 % с шаблоном v4 — {c['over90']} из {rated}")


def build() -> str:
    src, pairs = evaluate()
    parts, totals = [], []
    total = stats(pairs)
    for doc in (1, 2):
        mine = [(row, entry) for row, entry in pairs if row[6] == doc]
        title, pages = DOCS_TITLES[doc]
        rows = []
        for (rid, number, visible, _page, _acc, _value, _doc), entry in mine:
            why, quote, verdict = cells(entry)
            rows.append(f"| {number} | {esc(visible)} | Оценка: <br>{verdict} \\| \\|  | {why} | {quote} |  |")
        s = summary(stats(mine))
        totals.append(f"Документ {doc} из 2 ({pages}) — {s}")
        parts.append(f"### Документ {doc} из 2: «{title}»\n\nСтраницы исходника: {pages}. Итог: {s}.\n\n"
                     + HEADER + "\n".join(rows) + "\n")
    total_lines = "\n".join(f"- {t};" for t in totals)
    return f"""---
status: draft
version: "1.0"
updated: 2026-11-10
ai-generated: true
type: analysis
scope: bcreq-1140-only
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/482"
---

# L0 — оценка исполнимости ТЗ BCREQ-1140

Исходник Заказчика — «{src['title']}» ({src['pages']} с., sha256 `{src['sha256']}`,
[вложение issue #482]({SOURCE_URL})); контрольные суммы всех входов — в
[`inputs/README.md`](../inputs/README.md). PDF содержит два документа, они разделены
заголовками `### Документ N из 2`.

**Статистика** (знаменатель процентов — оценённые строки, без пустых оценок):

- всего — {summary(total)};
{total_lines}

**Методика.**

- Колонки 1–2 перенесены из текстового слоя PDF без правок (опечатки и пробелы исходника
  сохранены); переводы строк внутри ячейки — `<br>`. Номер в колонке 1 — литеральный
  номер пункта исходника («2.14.20.», «1.1»), у строк без номера колонка 1 пустая.
  Исходник содержит правки рецензирования Word: зачёркнутый (удалённый) текст перенесён
  как `~~…~~` — так колонка 2 остаётся байт-в-байт равной видимому тексту PDF, а
  оценивается текст после принятия правок. Глоссарий «1. Термины и определения»,
  повторяющиеся шапки таблицы, титул вложенного документа и служебная выноска Word
  требованиями не являются и в таблицу не включены. Транскрипцию независимо сверяет
  `experiments/issue_482/check_source.py` (другая библиотека — pdfplumber): полнота
  символов, порядок строк, колонка «№ п/п» и множество зачёркнутых символов.
- Колонка 3 — формат `Оценка: <br>[Оценка Исполнителя] | [ ] | [ ]`; оценка только по
  шкале `Да / Частично / Нет / пусто`. Колонки «Оценка Внутр» / «Комментарий поставщика»
  в исходнике нет (колонка «Требуемое значение» содержит требование Заказчика «наличие»),
  поэтому средняя часть пустая.
- SSOT: шаблон «ТЗ-тендеров-v4» ([вложение issue #482]({TENDER_URL}), sha256
  `{TENDER_SHA}`, высший приоритет) и БЗ
  [`mango-ba-ai-runtime/docs/kb`](https://github.com/G-Ivan-A/mango-ba-ai-runtime/tree/{COMMIT}/docs/kb)
  на commit `{COMMIT}`; веб — только домены Mango Office (ссылки «Портал_Mango»).
- Документ 1 построен на шаблоне v4 (та же нумерация разделов 1–12). Совпадение > 90 %
  (`experiments/issue_482/tender_similarity.py`, максимум из метрик raw / core / dice) —
  `Да`, «Не требует обоснования» со ссылкой на п/п шаблона; цитата пункта и значения
  метрик — в колонке 5. Генератор допускает автоматическую оценку только при дословном
  совпадении принятого текста с пунктом (после нормализации пробелов, маркеров и
  конечной пунктуации).
- Критик-гейт по правилу > 90 %: в 8 пунктах шаблона Заказчик заменил WhatsApp на
  мессенджер MAX (сходство остаётся > 90 %, но предмет требования изменён). Эти строки
  оценены по существу: части, совпадающие с шаблоном, подтверждены пунктом v4, MAX —
  только прямой цитатой БЗ для конкретной функции; если её нет — `Частично`.
- Документ 2 (автоматизация информирования и приёма заявок ТО ВДГО/ВКГО) в шаблоне v4
  отсутствует (сходство < 90 %): каждая строка разобрана на атомарные части (объёмы,
  сроки, число попыток и интервалы, каналы, отчётность); числовые условия подтверждаются
  только прямым утверждением SSOT. Бизнес-логика Заказчика (районы, бригады, свободные
  слоты) и интеграция с базой данных Заказчика по API — проектная доработка поверх
  общего механизма, без доработки не подтверждается.
- Правило базового движка («Да (базовая функция Yandex SpeechKit)») не применялось:
  официального источника вендора в разрешённых доменах нет.
- Трактовки неоднозначных формулировок в пользу Mango указаны в аудите колонки 5
  («Трактовка в пользу Mango: …»). Платные опции, лимиты, отдельные продукты и тарифные
  ограничения указаны там же — оценка `Да` не означает включения в базовый тариф.
- Строки-заголовки и строки, целиком зачёркнутые правкой, — пустая оценка, «{OUT}».
- Колонка 6 «Комментарий БА» оставлена пустой для бизнес-аналитика.

## Отчёт: оценка исполнимости «{src['title']}»

""" + "\n".join(parts)


if __name__ == "__main__":
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(build(), encoding="utf-8")
    print(f"written {REPORT.relative_to(ROOT)} (runtime {COMMIT})")
