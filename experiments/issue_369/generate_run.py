#!/usr/bin/env python3
"""Генератор отчёта RUN-0071 (issue #369): L0-оценка исполнимости ТЗ BCREQ-1116.

Два исходника Заказчика — два блока одного отчёта с явным разделителем
(заголовок с именем документа). Колонки 1–2 берутся из `source_transcription.json`
без изменений. Оценки и доказательства — из `research/*.json`
(`{rid: {verdict, why, refs, quotes, audit}}`). Ссылки на БЗ строятся по frontmatter
разделов runtime-репозитория (`MANGO_BA_RUNTIME_MAIN`, commit фиксируется в отчёте),
ссылки на шаблон ТЗ-тендеров-v4 — по `experiments/issue_367/tender_index.json`
(тот же PDF, SHA-256 612e5e09…).

Ячейки таблицы выводятся как `| значение |` — ровно один пробел-отступ с каждой
стороны, чтобы хвостовые пробелы и неразрывные пробелы исходника сохранялись.

Запуск:
    MANGO_BA_RUNTIME_MAIN=/tmp/rt-main python3 experiments/issue_369/generate_run.py
"""

from __future__ import annotations

import json
import os
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RUN = ROOT / "runs/2026/RUN-0071"
REPORT = RUN / "outputs/L0-feasibility-assessment-1116.md"
RUNTIME = Path(os.environ.get("MANGO_BA_RUNTIME_MAIN", "/tmp/rt-main"))
COMMIT = subprocess.check_output(["git", "-C", str(RUNTIME), "rev-parse", "HEAD"], text=True).strip()
KB = RUNTIME / "docs/kb"
BLOB = f"https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/{COMMIT}/docs/kb/"
TENDER_URL = "https://github.com/user-attachments/files/33303264/-.-v4.pdf"
TENDER = json.loads((ROOT / "experiments/issue_367/tender_index.json").read_text(encoding="utf-8"))
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

NO_DATA = "Нет данных"
OK = "Архитектурных противоречий не выявлено, трассировка подтверждена."
OUT = "вне функционального контура"
VERDICTS = ("Да", "Частично", "Нет", "")
HEADER = (
    "| № | Требование | Оценка | Обоснование и ссылка | Цитата источника и технический аудит | Комментарий БА |\n"
    "| --- | --- | --- | --- | --- | --- |\n"
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


def plural(n: int) -> str:
    if n % 10 == 1 and n % 100 != 11:
        return "строка"
    return "строки" if 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14 else "строк"


def block_title(index: int, total: int, block: dict) -> str:
    """Явный разделитель блока: имя документа-исходника."""
    return f"## Документ {index} из {total}: «{block['title']}»"


def build() -> str:
    src = json.loads((HERE / "source_transcription.json").read_text(encoding="utf-8"))
    blocks = src["blocks"]
    data = load()
    expected = [row[0] for block in blocks for row in block["rows"]]
    assert sorted(data) == sorted(expected), set(expected) ^ set(data)
    parts, totals = [], []
    for index, block in enumerate(blocks, start=1):
        counts = {key: 0 for key in ("Да", "Частично", "Нет", "пусто")}
        rows = []
        for rid, num, req, _loc in block["rows"]:
            why, quote, verdict = cells(data[rid])
            counts[verdict or "пусто"] += 1
            rows.append(f"| {num} | {esc(req)} | Оценка: <br>{verdict} \\| \\|  | {why} | {quote} |  |")
        summary = ", ".join(f"`{k}` — {v}" for k, v in counts.items())
        totals.append(f"«{block['title']}» — {len(rows)} {plural(len(rows))}: {summary}")
        parts.append(
            f"{block_title(index, len(blocks), block)}\n\n"
            f"Исходник: {block['title']} (sha256 `{block['sha256']}`). Итог: {summary}.\n\n"
            + HEADER + "\n".join(rows) + "\n"
        )
    total_lines = "\n".join(f"- {t};" for t in totals)
    return f"""---
status: draft
version: "1.0"
updated: 2026-10-11
ai-generated: true
type: analysis
scope: bcreq-1116-only
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/369"
---

# L0 — оценка исполнимости ТЗ BCREQ-1116

Исходники Заказчика — два документа, оценены в одном результате двумя блоками с
явным разделителем (заголовок `## Документ N из 2: «имя файла»`); контрольные суммы —
в [`inputs/README.md`](../inputs/README.md):

{total_lines}
- Колонки 1–2 перенесены из исходников без правок, включая опечатки («ппрослушать»,
  «Назанчение», «приоритезиации», «интреграцию», «Передаресовано»), хвостовые и
  неразрывные пробелы. Пустые абзацы и пустые строки листа пропущены.
  - DOC: номер в колонке 1 — литеральный номер абзаца исходника («1.1.», «2.1.3.»,
    «1.» …), элементы маркированных списков Word — `•`, ненумерованные абзацы — без
    номера. Строка таблицы исходника — одна строка отчёта: ячейки слева направо через
    `<br>`, знак сноски — `<sup>1</sup>` (сноска исходника: «См.Требования к доступности ПО
    (Приложение 2).»). Титул и «Глоссарий ключевых терминов и определений системы»
    (определения) требованиями не являются и в таблицу не включены. Раздел «1.
    Существующая проблема и обоснование необходимости закупки» удалён Заказчиком в
    режиме исправлений и в итоговой редакции отсутствует — не переносится.
  - XLSX: собственной нумерации требований нет — колонка 1 = номер строки листа
    «функционал», колонка 2 = ячейка столбца A; столбец B («Ответ», «да (если есть)/ нет
    (если отсутствует)») — графа ответа участника, требованием не является.
- Колонка 3 — формат `Оценка: <br>[Оценка Исполнителя] | [ ] | [ ]`, оценка только
  по шкале `Да / Частично / Нет / пусто`.
- SSOT: шаблон «ТЗ-тендеров-v4» (высший приоритет) и БЗ
  [`mango-ba-ai-runtime/docs/kb`](https://github.com/G-Ivan-A/mango-ba-ai-runtime/tree/{COMMIT}/docs/kb)
  на commit `{COMMIT}`. Совпадений >90% с пунктами шаблона нет (максимум 0,667 —
  `experiments/issue_369/tender_similarity.py`), поэтому подтверждение по номеру п/п
  без обоснования не применялось: компоненты шаблона цитируются в колонке 5 с
  вероятностной оценкой.
- Шаблон v4 п/п 9.1: ПО Mango предоставляется по модели SaaS (облачное ПО на
  серверах в РФ). Требования поставки бессрочных лицензий, установки на инфраструктуре
  Заказчика, хранения данных только в контуре Заказчика и работы в изолированном
  сегменте сети противоречат SSOT и оценены `Нет` (или `Частично` по атомарным частям).
- Правило базового движка («Да (базовая функция Yandex SpeechKit)») не применялось:
  официального источника вендора в разрешённых доменах нет.
- Интеграции со сторонними системами без готового коннектора в SSOT (Mindbox, Talkme,
  робот «Мия», сайт Заказчика, stream telecom, конфигурации 1С кроме «1С: Управление
  торговлей» ред. 11) — только общий механизм (API ВАТС, HTTP-запросы), конкретная
  интеграция требует разработки: `Нет` (или `Частично`, если остальные атомарные части
  подтверждены).
- Сроки реакции и устранения инцидентов поддержки, проценты инцидентов (Приложение 1)
  в SSOT не заданы — `Нет` («Нет данных»); доступность, RTO и RPO сравнены с п/п
  9.2–9.4 шаблона v4.
- Строки-заголовки, только вводящие перечень подпунктов (оцениваются отдельно),
  строки-шапки таблиц, отсылки к Приложению 1, цели проекта (бизнес-результат
  Заказчика), проектные услуги и договорные условия (адаптация и ввод в эксплуатацию,
  гарантийный срок, порядок расчёта SLA, исключения ответственности) и вопрос
  участнику о сроке внедрения — пустая оценка, «{OUT}».
- Платные опции, лимиты и тарифные ограничения указаны в аудите колонки 5 — оценка
  `Да` не означает включения в базовый тариф.
- Колонка 6 «Комментарий БА» оставлена пустой для бизнес-аналитика.

""" + "\n".join(parts)


if __name__ == "__main__":
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(build(), encoding="utf-8")
    print(f"written {REPORT.relative_to(ROOT)} (runtime {COMMIT})")
