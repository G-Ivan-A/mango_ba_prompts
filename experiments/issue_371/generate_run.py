#!/usr/bin/env python3
"""Генератор отчёта RUN-0072 (issue #371): L0-оценка исполнимости ТЗ 2026 по BCREQ-1116 (задача 1117).

Отчёт 1 — таблица оценки «Телефония ТЗ 0710 1026 года в анализ.pdf». Колонки 1–2 берутся из
`source_transcription.json` без изменений. Оценки и доказательства — из `research/*.json`
(`{rid: {verdict, why, refs, quotes, audit}}`). Ссылки на БЗ строятся по frontmatter
разделов runtime-репозитория (`MANGO_BA_RUNTIME_MAIN`, commit фиксируется в отчёте),
ссылки на шаблон ТЗ-тендеров-v4 — по `experiments/issue_367/tender_index.json`
(тот же PDF, SHA-256 612e5e09…).

Отчёт 2 — аналитическая записка о дельте ТЗ 2026 к ТЗ 2025 («Телефония ТЗ 2307 2025 года
в анализ.pdf», не оценивается) из `delta.json`; оценка затронутых строк ТЗ 2026
подставляется из Отчёта 1.

Ячейки таблицы выводятся как `| значение |` — ровно один пробел-отступ с каждой стороны.

Запуск:
    MANGO_BA_RUNTIME_MAIN=/tmp/rt-main python3 experiments/issue_371/generate_run.py
"""

from __future__ import annotations

import json
import os
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RUN = ROOT / "runs/2026/RUN-0072"
REPORT = RUN / "outputs/L0-feasibility-assessment-1117.md"
RUNTIME = Path(os.environ.get("MANGO_BA_RUNTIME_MAIN", "/tmp/rt-main"))
COMMIT = subprocess.check_output(["git", "-C", str(RUNTIME), "rev-parse", "HEAD"], text=True).strip()
KB = RUNTIME / "docs/kb"
BLOB = f"https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/{COMMIT}/docs/kb/"
TENDER_URL = "https://github.com/user-attachments/files/33326885/-.-v4.pdf"
TENDER = json.loads((ROOT / "experiments/issue_367/tender_index.json").read_text(encoding="utf-8"))
SIMILARITY = json.loads((HERE / "tender_similarity.json").read_text(encoding="utf-8"))
# Ненумерованный раздел «2. Общие требования к оказанию услуг Исполнителем» (с.5 шаблона).
TENDER_P5_TITLE = "2. Общие требования к оказанию услуг Исполнителем"
TENDER_P5 = (
    "Работоспособность сервиса осуществляется 24 часа в сутки, ежедневно, без перерывов, за исключением "
    "проведения необходимых ремонтных и профилактических работ. Квартальная доступность Услуг должна быть "
    "не менее 99,9%. Технологические перерывы при оказании Услуг в объеме не более 4 (четырех) часов в месяц, "
    "не включаются в показатели доступности Услуг. Записи о программном обеспечении поставщика («Виртуальная АТС», "
    "«Центр обработки вызовов», «Голосовой робот»), применяемого для предоставления сервисов в рамках настоящего "
    "технического задания, должны быть включены в реестр российского программного обеспечения."
)
TZ2025 = "Телефония ТЗ 2307 2025 года в анализ.pdf"
TZ2025_SHA = "0659eeae961a36c302f9b92dc66c3cf5bd2041cedf17b29175d40d1df4602191"

NO_DATA = "Нет данных"
OK = "Архитектурных противоречий не выявлено, трассировка подтверждена."
OUT = "вне функционального контура"
VERDICTS = ("Да", "Частично", "Нет", "")
KINDS = ("Изменено", "Добавлено", "Исключено")
HEADER = (
    "| № | Требование | Оценка | Обоснование и ссылка | Цитата источника и технический аудит | Комментарий БА |\n"
    "| --- | --- | --- | --- | --- | --- |\n"
)
DELTA_HEADER = (
    "| № | Изменение | ТЗ 2025, п. | ТЗ 2026: строка Отчёта 1 — оценка | Было (ТЗ 2025) | Стало (ТЗ 2026) "
    "| Влияние на оценку ТЗ 2026 |\n"
    "| --- | --- | --- | --- | --- | --- | --- |\n"
)
# Правки ТЗ 2025 → 2026, найденные delta_align.py, но не влияющие на оценку (формулировки,
# перенос между разделами, договорные условия) — перечисляются в Отчёте 2 без разбора.
MINOR = (
    ("R005", "2.2: «оказание услуг» → «предоставление доступа» — формулировка"),
    ("R007", "2.4: «Услуги предоставляются» → «Доступ к Системе предоставляется» — формулировка"),
    ("R008", "2.5: параметры SLA устанавливаются ТЗ и Регламентом Исполнителя — договорное условие"),
    ("R012", "2.9 (в 2025 — 2.10): открытие доступа «на основании Приложения 2» — договорное условие"),
    ("R019", "3.1: из состава документации исключён перечень номеров и доступов — следствие исключения номеров"),
    ("R020", "3.1: подключение и активация номеров → настройка маршрутизации — следствие исключения номеров"),
    ("R050", "3.10: правка формулировки, требования не изменены"),
    ("R077", "Прил.: «работников» → «пользователей»; последняя фраза вынесена в отдельную строку 78"),
    ("R084", "Прил.: «Отчетность» → «Отчётность» — орфография"),
    ("R087", "Прил.: «Контроль работников» → «Контроль пользователей» — формулировка"),
    ("R096", "Прил.: «Сопровождение на всё время оказания услуг» уточнено «по предоставлению доступа к Системе»"),
)


def front(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    lines = path.read_text(encoding="utf-8").splitlines()
    for line in lines[1:]:
        if line.strip() == "---":
            break
        key, _, value = line.partition(":")
        if ":" in line and not line.startswith((" ", "-")):
            data[key.strip()] = value.strip().strip('"')
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
    path = kb_path(ref)
    fm = front(path)
    assert fm["doc_code"] == doc, path
    number = fm.get("pdf_section", "")
    if number in ("", "0", "-", "—"):
        number = fm.get("section", "")
    if number in ("", "0", "-", "—"):
        number = ""
    sect = f"§{number} " if number else ""
    return f"[{doc}, {sect}«{fm['title']}», с.{fm['pages']}]({BLOB}{DOCS[doc]}/sections/{section_file})"


def tender_text(item: str) -> str:
    """Текст пункта шаблона без хвоста «наличие» и следующего заголовка."""
    if item == "p5":
        return TENDER_P5
    return re.sub(r"\s+наличие\b.*$", "", TENDER[item][1], flags=re.S).strip()


def tv4(item: str) -> str:
    if item == "p5":
        return f"[ТЗ-тендеров-v4, разд. «{TENDER_P5_TITLE}», с.5]({TENDER_URL})"
    return f"[ТЗ-тендеров-v4, п/п {item}, с.{TENDER[item][0]}]({TENDER_URL})"


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


def cells(entry: dict) -> tuple[str, str, str]:
    verdict, why, refs, quotes = entry["verdict"], entry["why"], entry["refs"], entry["quotes"]
    assert verdict in VERDICTS, verdict
    assert len(refs) == len(quotes), entry
    for i, ref in enumerate(refs, start=1):
        marker = f"[{i}]"
        assert why.count(marker) == 1, (marker, why)
        why = why.replace(marker, f"{marker} {link(ref)}")
    quote = " ".join(f"[{i}] «{q}»" for i, q in enumerate(quotes, start=1))
    if verdict == "":
        quote = " ".join(filter(None, [OUT[0].upper() + OUT[1:] + ".", quote]))
    elif verdict == "Нет" and (NO_DATA in why or not quotes):
        quote = " ".join(filter(None, [NO_DATA + ".", quote]))
    audit = entry["audit"].strip()
    audit = OK if audit == "OK" else audit
    return esc(why), esc(f"{quote}<br>Аудит: {audit}"), verdict


def plural(n: int, forms: tuple[str, str, str] = ("строка", "строки", "строк")) -> str:
    if n % 10 == 1 and n % 100 != 11:
        return forms[0]
    return forms[1] if 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14 else forms[2]


def sections(rows: list[list[str]]) -> dict[str, str]:
    """rid -> пункт ТЗ 2026, к которому относится строка (для маркеров — ближайший номер выше)."""
    out, current = {}, ""
    for rid, num, req, _ in rows:
        if re.fullmatch(r"\d+\.(\d+\.)?", num):
            current = num.rstrip(".")
        elif req.startswith("Приложение 2"):
            current = "Прил. 2"
        out[rid] = current
    return out


def delta_rows(rows: list[list[str]], data: dict[str, dict]) -> tuple[str, dict[str, int]]:
    delta = json.loads((HERE / "delta.json").read_text(encoding="utf-8"))
    where = sections(rows)
    order = {rid: i for i, (rid, *_rest) in enumerate(rows)}
    delta.sort(key=lambda d: (d["kind"] == "Исключено", min((order[r] for r in d["rows"]), default=0)))
    counts = {kind: 0 for kind in KINDS}
    lines = []
    for n, entry in enumerate(delta, start=1):
        assert entry["kind"] in KINDS, entry
        assert bool(entry["rows"]) == (entry["kind"] != "Исключено"), entry
        assert bool(entry["was"]) == (entry["kind"] != "Добавлено"), entry
        counts[entry["kind"]] += 1
        targets = "<br>".join(
            f"строка {int(r[1:])} (п. {where[r]}) — {data[r]['verdict'] or 'пусто'}" for r in entry["rows"]
        ) or "— (в ТЗ 2026 нет)"
        was = f"«{entry['was']}»" if entry["was"] else "—"
        now = f"«{entry['now']}»" if entry["now"] else "—"
        lines.append(
            f"| {n} | {entry['kind']} | {entry['p2025']} | {targets} | {esc(was)} | {esc(now)} | {esc(entry['impact'])} |"
        )
    return DELTA_HEADER + "\n".join(lines) + "\n", counts


def report2(rows: list[list[str]], data: dict[str, dict]) -> str:
    table, counts = delta_rows(rows, data)
    alignment = json.loads((HERE / "delta_alignment.json").read_text(encoding="utf-8"))
    assert alignment["tz2025_sha256"] == TZ2025_SHA
    a = alignment["counts"]
    summary = ", ".join(f"{k.lower()} — {v}" for k, v in counts.items())
    minor = "\n".join(f"- строка {int(rid[1:])} — {text};" for rid, text in MINOR)
    return f"""## Отчёт 2: анализ дельты ТЗ 2026 к ТЗ 2025

Аналитическая записка. Сравниваются ТЗ Заказчика 2026 («{REPORT_SOURCE}», оценено в Отчёте 1)
и ТЗ Заказчика 2025 («{TZ2025}», sha256 `{TZ2025_SHA}`). ТЗ 2025 не оценивалось — файл
использован только для определения дельты.

### Метод

1. Текст ТЗ 2025 (с. 1–6 — абзацы по номерам пунктов и маркерам, с. 7–9 — строки таблицы
   Приложения 1) выровнен со строками Отчёта 1 скриптом
   `experiments/issue_371/delta_align.py` (difflib, нормализованный текст):
   {a['same']} {plural(a['same'])} ТЗ 2026 совпадают с ТЗ 2025 (ratio ≥ 0,95), {a['changed']} изменены
   (0,55–0,95), {a['new']} новые (< 0,55); {len(alignment['removed_candidates'])} абзацев ТЗ 2025
   без пары — кандидаты в исключённые. Результат — `experiments/issue_371/delta_alignment.json`.
2. Все кандидаты разобраны вручную (`experiments/issue_371/delta.json`). В записку включены
   только явные изменения требований, влияющие на оценку: новое или исключённое требование,
   изменение числового параметра, объёма, условия или состава. Цитаты «Было» / «Стало»
   дословные; `verify_quotes.py` проверяет их по тексту ТЗ 2025 и по транскрипции ТЗ 2026.
3. Колонка «ТЗ 2026» даёт строку Отчёта 1 (порядковый номер строки таблицы), пункт ТЗ 2026 и
   оценку из Отчёта 1.

### Итог

Явных изменений, влияющих на оценку: {sum(counts.values())} ({summary}).

- **Предмет и вендор.** ТЗ 2025 закупало услуги связи «на базе программного обеспечения
  Mango Office» с номерами 495/499, пулом 300 номеров, пакетом минут и 100 каналами; ТЗ 2026
  закупает право использования ПО (доступ к Системе) без указания вендора. Требования
  оператора связи (номера, минуты, нагрузка 20 000 звонков и 8 000 SMS в месяц, протоколы VoIP)
  исключены — их исполнимость больше не оценивается.
- **Уровень сервиса.** Доступность приведена к шаблону v4 (99,9 % в квартал вместо
  «круглосуточно» в 2.6 и 99,95 % в 3.11 — теперь подтверждается п/п 9.2). Добавлено время
  восстановления после критического инцидента не более 120 минут — строже RTO 240 минут
  шаблона v4, и время реакции 15 минут, которого нет в SSOT. Ночные регламентные работы
  стали обязательными.
- **Новый функционал контакт-центра.** Блок 3.2 почти дословно взят из шаблона v4 (пять
  строк со сходством > 90 %), добавлены WFM (3.3), голосовые роботы и чат-боты, статусная
  модель, десктопное приложение под MACOS / WINDOWS / Astra Linux, методы API (3.17),
  маршрутизация по выбору в IVR, IVR и не менее 5 очередей.
- **Интеграции.** SberCRM заменена CRM Заказчика собственной разработки, добавлена
  интеграция стороннего сервиса речевой аналитики с отображением в десктопном
  приложении — обе требуют разработки поверх API.
- **Хранение и объёмы.** Хранение записей: «не менее 6 месяцев» → «бессрочное» (3.1) при
  «в течение срока действия Договора» (3.4, Прил. 2) — противоречие внутри ТЗ 2026;
  расширение хранилища — за счёт Исполнителя. Пользователей 56 → до 500, одновременных
  пользователей десктопного приложения 30 → 55, каналов SIP-транка 50 → не менее 50.

### Изменения, влияющие на оценку

{table}
### Не влияют на оценку

Правки, найденные выравниванием, но не меняющие оценку (формулировки, перенос между
разделами, договорные условия):

{minor}
- новые строки-заголовки (строки 13, 14, 28, 63, 68, 70, 72, 74, 75) и пометки «Не оценивается»
  (строки 2, 69, 71, 73) — структура документа.
"""


REPORT_SOURCE = "Телефония ТЗ 0710 1026 года в анализ.pdf"


def build() -> str:
    src = json.loads((HERE / "source_transcription.json").read_text(encoding="utf-8"))
    assert src["title"] == REPORT_SOURCE
    data = load()
    expected = [row[0] for row in src["rows"]]
    assert sorted(data) == sorted(expected), set(expected) ^ set(data)
    counts = {key: 0 for key in ("Да", "Частично", "Нет", "пусто")}
    rows = []
    for rid, num, req, _page in src["rows"]:
        why, quote, verdict = cells(data[rid])
        counts[verdict or "пусто"] += 1
        rows.append(f"| {num} | {esc(req)} | Оценка: <br>{verdict} \\| \\|  | {why} | {quote} |  |")
    summary = ", ".join(f"`{k}` — {v}" for k, v in counts.items())
    over90 = sorted(
        (rid, max((m[i], m[i + 1]) for i in (0, 2, 4)))
        for rid, m in SIMILARITY.items()
        if max(m[0], m[2], m[4]) > 0.9
    )
    over90_text = ", ".join(
        f"строка {int(rid[1:])} → п/п {item} ({str(score).replace('.', ',')})" for rid, (score, item) in over90
    )
    return f"""---
status: draft
version: "1.0"
updated: 2026-10-12
ai-generated: true
type: analysis
scope: bcreq-1116-task-1117-only
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/371"
---

# L0 — оценка исполнимости ТЗ 2026 по BCREQ-1116 (задача 1117)

Исходник Заказчика — «{REPORT_SOURCE}» (sha256 `{src['sha256']}`); контрольные суммы
всех входов — в [`inputs/README.md`](../inputs/README.md). Результат состоит из двух
отчётов: Отчёт 1 — оценка исполнимости ТЗ 2026, Отчёт 2 — анализ дельты ТЗ 2026 к
ТЗ 2025 («{TZ2025}», не оценивается).

- Отчёт 1 — {len(rows)} {plural(len(rows))}: {summary}.
- Колонки 1–2 перенесены из текстового слоя PDF без правок (переносы строк PDF внутри
  абзаца склеены пробелом, перенос со знаком «-» внутри слова — без пробела). Номер в
  колонке 1 — литеральный номер пункта («2.6.», «3.17.»); маркеры списков — символ
  исходника: «−» (SymbolMT U+F02D) и «•» (U+F0B7). Пометки «Не оценивается», строка
  «Приложение 2 к Техническому заданию» и вводная фраза приложения — без номера. Титул
  и раздел «Термины и определения» (определения) требованиями не являются и в таблицу
  не включены. Соответствие колонок 1–2 исходнику независимо проверяет
  `experiments/issue_371/check_source.py` (другая библиотека — pypdf).
- Колонка 3 — формат `Оценка: <br>[Оценка Исполнителя] | [ ] | [ ]`, оценка только
  по шкале `Да / Частично / Нет / пусто`.
- SSOT: шаблон «ТЗ-тендеров-v4» (высший приоритет) и БЗ
  [`mango-ba-ai-runtime/docs/kb`](https://github.com/G-Ivan-A/mango-ba-ai-runtime/tree/{COMMIT}/docs/kb)
  на commit `{COMMIT}`; веб — только домены Mango Office.
- Совпадение > 90 % с пунктами шаблона v4 (`experiments/issue_371/tender_similarity.py`,
  максимум из трёх метрик): {over90_text}. Эти строки оценены `Да` с указанием номера п/п
  без дополнительного обоснования; для остальных строк компоненты шаблона цитируются в
  колонке 5 с вероятностной оценкой.
- Шаблон v4 п/п 9.1: ПО Mango предоставляется по модели SaaS. Доступность сравнена с
  п/п 9.2 и общими требованиями с.5 (99,9 % в квартал, перерывы не более 4 ч в месяц),
  время восстановления — с RTO п/п 9.3 (не более 240 минут), резервное копирование — с
  RPO п/п 9.4. Сроки реакции поддержки в SSOT не заданы — «Нет данных».
- Правило базового движка («Да (базовая функция Yandex SpeechKit)») не применялось:
  официального источника вендора в разрешённых доменах нет.
- Интеграции со сторонними системами без готового коннектора в SSOT (CRM Заказчика
  собственной разработки, сервис речевой аналитики Заказчика) — только общий механизм
  (API ВАТС, HTTP-запросы, SIP-транк), конкретная интеграция требует разработки: `Нет`
  (или `Частично`, если остальные атомарные части подтверждены).
- Перечни ОС, каналов и событий проверены по атомарным частям; открытые перечни («иные
  каналы, используемые Заказчиком») целиком не подтверждаются. Трактовки в пользу Mango
  указаны в аудите колонки 5.
- Строки-заголовки, только вводящие перечень подпунктов (оцениваются отдельно), разделы,
  помеченные Заказчиком «Не оценивается», договорные условия и обязанности сторон — пустая
  оценка, «{OUT}».
- Платные опции, лимиты и тарифные ограничения указаны в аудите колонки 5 — оценка
  `Да` не означает включения в базовый тариф.
- Колонка 6 «Комментарий БА» оставлена пустой для бизнес-аналитика.

## Отчёт 1: оценка исполнимости «{REPORT_SOURCE}»

{HEADER}""" + "\n".join(rows) + "\n\n" + report2(src["rows"], data)


if __name__ == "__main__":
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(build(), encoding="utf-8")
    print(f"written {REPORT.relative_to(ROOT)} (runtime {COMMIT})")
