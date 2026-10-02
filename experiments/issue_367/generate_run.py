#!/usr/bin/env python3
"""Генератор отчёта RUN-0070 (issue #367): L0-оценка исполнимости ТЗ BCREQ-1115.

Колонки 1–2 берутся из `source_transcription.json` без изменений. Оценки и
доказательства — из `research/*.json` (`{rid: {verdict, why, refs, quotes, audit}}`).
Ссылки на БЗ строятся по frontmatter разделов runtime-репозитория
(`MANGO_BA_RUNTIME_MAIN`, commit фиксируется в отчёте), ссылки на шаблон
ТЗ-тендеров-v4 — по `tender_index.json` (п/п -> страница).

Запуск:
    MANGO_BA_RUNTIME_MAIN=/tmp/rt-main python3 experiments/issue_367/generate_run.py
"""

from __future__ import annotations

import json
import os
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RUN = ROOT / "runs/2026/RUN-0070"
REPORT = RUN / "outputs/L0-feasibility-assessment-1115.md"
RUNTIME = Path(os.environ.get("MANGO_BA_RUNTIME_MAIN", "/tmp/rt-main"))
COMMIT = subprocess.check_output(["git", "-C", str(RUNTIME), "rev-parse", "HEAD"], text=True).strip()
KB = RUNTIME / "docs/kb"
BLOB = f"https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/{COMMIT}/docs/kb/"
TENDER_URL = "https://github.com/user-attachments/files/32929383/-.-v4.pdf"
TENDER = json.loads((HERE / "tender_index.json").read_text(encoding="utf-8"))
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

DOCS = {
    "ROBOTFIL": "cov-robot-fil",
    "LK": "mango-lk-manual",
    "CC": "mango-cc-manual",
    "ROLES": "rolevaya-model-vats",
    "VPBXAPI": "vpbx-api",
    "MDAPI": "mdialogi-api",
    "QM": "quality-management",
    "SIPT": "sip-trunk",
    "LKSSO": "lk-vats-sso",
    "SA-VATS-SCORE": "speech-analytics/vats-offline-scoring",
    "SA": "speech-analytics/user-guide",
    "SA-KATS": "speech-analytics/kats",
    "SA-SCORE": "speech-analytics/offline-scoring",
    "INTB24": "integration-bitrix24",
    "INTAMO": "integration-amocrm",
    "INTBPM": "integration-bpmsoft",
    "INT1C": "integration-1c",
}

NO_DATA = "Нет данных"
OK = "Архитектурных противоречий не выявлено, трассировка подтверждена."
OUT = "вне функционального контура"
VERDICTS = ("Да", "Частично", "Нет", "")


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


def build() -> str:
    src = json.loads((HERE / "source_transcription.json").read_text(encoding="utf-8"))
    data = load()
    expected = [row[0] for row in src["rows"]]
    assert sorted(data) == sorted(expected), set(expected) ^ set(data)
    counts = {key: 0 for key in ("Да", "Частично", "Нет", "пусто")}
    rows = []
    for rid, num, req, _para in src["rows"]:
        why, quote, verdict = cells(data[rid])
        counts[verdict or "пусто"] += 1
        rows.append(f"| {num} | {esc(req)} | Оценка: <br>{verdict} \\| \\|  | {why} | {quote} |  |")
    summary = ", ".join(f"`{k}` — {v}" for k, v in counts.items())
    return f"""---
status: draft
version: "1.0"
updated: 2026-10-01
ai-generated: true
type: analysis
scope: bcreq-1115-only
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/367"
---

# L0 — оценка исполнимости ТЗ BCREQ-1115

Исходник: {src["title"]} (sha256 `{src["sha256"]}`, контрольные суммы — в
[`inputs/README.md`](../inputs/README.md)).

- Колонки 1–2 перенесены из исходника без правок: номера и маркеры `•` как в
  исходнике (включая пропуск номера `13.` в разделе «Общие технические
  характеристики услуг»), опечатки сохранены («DEF/ABS», «по различным средам
  анализа», «уполномоченными пользователям»). Пустые абзацы исходника пропущены.
- Раздел «Термины и определения» (определения) требованиями не является и в
  таблицу не включён.
- Колонка 3 — формат `Оценка: <br>[Оценка Исполнителя] | [ ] | [ ]`, оценка только
  по шкале `Да / Частично / Нет / пусто`; итог: {summary}.
- SSOT: шаблон «ТЗ-тендеров-v4» (высший приоритет) и БЗ
  [`mango-ba-ai-runtime/docs/kb`](https://github.com/G-Ivan-A/mango-ba-ai-runtime/tree/{COMMIT}/docs/kb)
  на commit `{COMMIT}`. Совпадение >90% с пунктом шаблона — одна строка (• «Пользователь с
  ролью «Администратор»…» ↔ п/п 6.7, коэффициент Дайса по основам слов 0,933,
  `experiments/issue_367/tender_similarity.py`) — подтверждена по номеру п/п. Для
  остальных строк компоненты шаблона цитируются в колонке 5 с вероятностной оценкой.
- Правило базового движка («Да (базовая функция Yandex SpeechKit)») не применялось:
  официального источника вендора в разрешённых доменах нет.
- Строки-заголовки, только вводящие перечень подпунктов (оцениваются отдельно), и
  обязательства Заказчика — пустая оценка, «{OUT}».
- Колонка 6 «Комментарий БА» оставлена пустой для бизнес-аналитика.

| № | Требование | Оценка | Обоснование и ссылка | Цитата источника и технический аудит | Комментарий БА |
| --- | --- | --- | --- | --- | --- |
""" + "\n".join(rows) + "\n"


if __name__ == "__main__":
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(build(), encoding="utf-8")
    print(f"written {REPORT.relative_to(ROOT)} (runtime {COMMIT})")
