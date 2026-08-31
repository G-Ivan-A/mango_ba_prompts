#!/usr/bin/env python3
"""Generate the issue #347 L0 assessment directly from its XLSX workbook."""

from __future__ import annotations

import hashlib
from pathlib import Path
import re
import xml.etree.ElementTree as ET
import zipfile


ROOT = Path(__file__).resolve().parents[2]
SOURCE = Path(__file__).with_name("requirements.xlsx")
OUT = ROOT / "runs/2026/RUN-0065/outputs/L0-customer-form-with-assessment.md"
NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
EXPECTED_SHA256 = "4806288a13f03b4e972b726e92e267c4c627cab42ad4ade3929607c0fd4287ba"

SIP = "[SIP Trunk, раздел «Что такое SIP Trunk»](../../../../kb/processed/sip-trunk/sections/02-chto-takoe-sip-trunk.md)"
SIP_NUMBERS = "[SIP Trunk, раздел «Номера»](../../../../kb/processed/sip-trunk/sections/16-nomera.md)"
SIP_ROUTING = "[SIP Trunk, схема распределения звонков](../../../../kb/processed/sip-trunk/sections/30-nastroyka-shemy-raspredeleniya-zvonkov-v.md)"
VPBX_API = "[API ВАТС, обзор](../../../../kb/processed/vpbx-api/sections/08-api-vats.md)"
ROBOT = "[Роботы, блок интеграции](../../../../kb/processed/cov-robot-fil/sections/31-blok-integraciya.md)"
SA = "[Речевая аналитика, общие сведения](../../../../kb/processed/speech-analytics/user-guide/sections/01-obschie-svedeniya.md)"


def rows() -> list[tuple[int, str, str, str]]:
    data = SOURCE.read_bytes()
    assert hashlib.sha256(data).hexdigest() == EXPECTED_SHA256
    with zipfile.ZipFile(SOURCE) as book:
        strings_root = ET.fromstring(book.read("xl/sharedStrings.xml"))
        strings = ["".join(node.text or "" for node in item.iter(NS + "t")) for item in strings_root.findall(NS + "si")]
        sheet = ET.fromstring(book.read("xl/worksheets/sheet1.xml"))
        result = []
        for row in sheet.findall(f".//{NS}sheetData/{NS}row"):
            cells: dict[str, str] = {}
            for cell in row.findall(NS + "c"):
                column = re.match(r"[A-Z]+", cell.attrib["r"])
                value_node = cell.find(NS + "v")
                value = "" if value_node is None else value_node.text or ""
                if cell.attrib.get("t") == "s" and value:
                    value = strings[int(value)]
                if column:
                    cells[column.group()] = value
            source = (cells.get("B", ""), cells.get("C", ""), cells.get("D", ""))
            if any(source):
                result.append((int(row.attrib["r"]), *source))
        return result


def md(value: str) -> str:
    return value.replace("|", "\\|").replace("\r\n", "\n").replace("\r", "\n").replace("\n", "<br>")


def assess(requirement: str, blocker: str) -> tuple[str, str, str, str, str]:
    low = requirement.lower()
    is_heading = (
        not blocker
        and not re.search(r"\d", requirement)
        and len(requirement) < 100
        and not any(word in low for word in ("долж", "возможност", "предоставлен", "поддерж"))
    )
    if is_heading:
        return "**Не оценивается.** Заголовок или раздел исходной формы.", "Высокая", "Структурная строка XLSX.", "Не применимо", "Нет"

    verdict = "**Нет данных.** В доступной БЗ нет прямого подтверждения полного составного требования."
    confidence = "Низкая"
    evidence = "Требуется проверка владельцем продукта, эксплуатации или договорного SLA; отсутствие данных не означает отсутствие функции."
    gap = "Недостаточно SSOT для решения о выполнимости."
    review = "Да"

    if any(token in low for token in ("skillaz", "api", "интеграц", "webhook", "вебхук")):
        verdict = f"**Доработка.** API ВАТС предоставляет интеграционные операции, но контракт Skillaz и сквозной сценарий в БЗ отсутствуют: {VPBX_API}."
        confidence = "Средняя"
        evidence = "Техническая точка интеграции есть; соответствие внешнему контракту не доказано."
        gap = "Получить API/событийный контракт Skillaz и выполнить L2/L3 gap-анализ."
    elif any(token in low for token in ("доступност", "24 часа", "sla", "нагруз", "100 оператор", "150 000", "не менее 200", "50 штук", "неограниченн")):
        verdict = "**Нет данных.** Пользовательская БЗ не является договорным SSOT для доступности, производительности, ёмкости или SLA."
        confidence = "Высокая"
        evidence = "Требуются договор, отчёт нагрузочного тестирования и эксплуатационные метрики."
        gap = "Провести performance/SLA due diligence до обязательства в заявке."
    elif "sip" in low or "внешн" in low and "лини" in low:
        verdict = f"**Реализовано.** Базовая возможность SIP Trunk и внешних линий описана в SSOT: {SIP}."
        confidence = "Средняя"
        evidence = "Подтверждена capability; заявленные объёмы, операторские условия и интеграция требуют отдельной проверки."
        gap = "Проверить количественные ограничения и схему подключения."
    elif "номерн" in low or "did" in low or "def-номер" in low:
        verdict = f"**Реализовано.** Управление номерами в составе SIP Trunk документировано: {SIP_NUMBERS}."
        confidence = "Средняя"
        evidence = "Наличие capability подтверждено; конкретный пул, оформление и объём не подтверждены."
        gap = "Проверить доступность и договорные условия требуемого пула."
    elif any(token in low for token in ("маршрут", "переадрес", "распределен", "очеред")):
        verdict = f"**Реализовано.** Настройка схем распределения звонков описана: {SIP_ROUTING}."
        confidence = "Средняя"
        evidence = "Базовая маршрутизация подтверждена; сложные условия и предельные нагрузки требуют проектирования."
        gap = "Сопоставить каждый сценарий с правилами маршрутизации и API."
    elif any(token in low for token in ("автодозвон", "предиктив", "робот", "кампан")):
        verdict = f"**Доработка.** Документация роботов подтверждает кампании и интеграционный блок, но не весь состав требования: {ROBOT}."
        confidence = "Средняя"
        evidence = "Часть capability подтверждена, составное требование требует декомпозиции и нагрузочного подтверждения."
        gap = "Декомпозировать режимы обзвона и проверить лимиты/лицензирование."
    elif any(token in low for token in ("речев", "транскриб", "распознав", "запис")):
        verdict = f"**Доработка.** Речевая аналитика подтверждает анализ записей, но не весь заявленный workflow: {SA}."
        confidence = "Средняя"
        evidence = "Capability подтверждена частично; сроки, качество, хранение и интеграция требуют проверки."
        gap = "Согласовать метрики качества, сроки обработки и правила хранения."
    if blocker.strip().lower() == "да":
        review = "Да"
        gap = "БЛОК-ФАКТОР: " + gap
    return verdict, confidence, evidence, gap, review


def render() -> str:
    body = """---
status: draft
version: 0.1
updated: 2026-08-31
ai-generated: true
type: analysis
scope: mango-only
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/347"
---

# L0 — оценка исполнимости ТЗ «Телефония»

Отчёт сохраняет исходные колонки листа «Требования к системе» посимвольно и
добавляет пять аудиторских колонок. Вердикты являются предварительной оценкой,
а не коммерческим обязательством. По CBAP составные требования требуют
декомпозиции и трассируемости до SSOT; `Нет данных` означает отсутствие прямого
подтверждения в доступной БЗ, но не отсутствие функции в продукте.

Контроль источника: `sha256:4806288a13f03b4e972b726e92e267c4c627cab42ad4ade3929607c0fd4287ba`.

| Строка XLSX | Требования к системе | Блок-фактор (источник) | Исходная колонка D | Оценка исполнимости | Уверенность | Основание / технический комментарий | Фокус human review |
| --- | --- | --- | --- | --- | --- | --- | --- |
"""
    lines = [body.rstrip()]
    for row_number, requirement, blocker, source_d in rows():
        verdict, confidence, evidence, gap, review = assess(requirement, blocker)
        lines.append("| " + " | ".join((str(row_number), md(requirement), md(blocker), md(source_d), verdict, confidence, evidence + " " + gap, review)) + " |")
    return "\n".join(lines) + "\n"


def main() -> int:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render(), encoding="utf-8")
    print(f"generated {OUT.relative_to(ROOT)} from {len(rows())} source rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
