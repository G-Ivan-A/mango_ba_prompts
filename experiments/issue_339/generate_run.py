#!/usr/bin/env python3
"""Generate RUN-0062 L0 directly from the three issue #339 XLS files."""

from __future__ import annotations

import hashlib
import pathlib

import xlrd


ROOT = pathlib.Path(__file__).resolve().parents[2]
DOWNLOADS = ROOT / "experiments/issue_339/downloads"
OUT = ROOT / "runs/2026/RUN-0062/outputs/L0-customer-form-with-assessment.md"
FILES = (
    "appendix-5-telephony.xls",
    "appendix-6-quality-control.xls",
    "appendix-7-nfr.xls",
)

ROBOT_AUTH = "[ROBOTFIL, §1, с.5–6](../../../../kb/processed/cov-robot-fil/sections/01-stranica-avtorizacii.md)"
ROBOT_ANALYTICS = "[ROBOTFIL, §3.7, с.36–39](../../../../kb/processed/cov-robot-fil/sections/13-analitika-po-golosovym-robotam.md)"
ROBOT_INTEGRATION = "[ROBOTFIL, §5.12, с.88–116](../../../../kb/processed/cov-robot-fil/sections/31-blok-integraciya.md)"
SA_GENERAL = "[SA, §1, с.4–7](../../../../kb/processed/speech-analytics/user-guide/sections/01-obschie-svedeniya.md)"
SA_RECOGNITION = "[SA, §3.2, с.14–16](../../../../kb/processed/speech-analytics/user-guide/sections/07-nastroyki-raspoznavaniya-zapisey.md)"
SA_SIP = "[SA, §10.4, с.123–124](../../../../kb/processed/speech-analytics/user-guide/sections/72-vkladka-nomera.md)"
SA_ROUTING = "[SA, §10.4.2, с.124–126](../../../../kb/processed/speech-analytics/user-guide/sections/75-nastroyka-shemy-raspredeleniya-zvonkov-v.md)"
LK_SIP = "[LK_manual_v-123, §5 «SIP Trunk», с.520](../../../../kb/processed/mango-lk-manual/sections/320-sip-trunk.md)"
LK_RECORD = "[LK_manual_v-123, §4.5.3.4, с.226–231](../../../../kb/processed/mango-lk-manual/sections/138-nastroyki.md)"
LK_SECURITY = "[LK_manual_v-123, §4.6.3.5, с.467–470](../../../../kb/processed/mango-lk-manual/sections/291-bezopasnost-pro.md)"


def displayed(book: xlrd.book.Book, sheet: xlrd.sheet.Sheet, row: int, col: int) -> str:
    cell = sheet.cell(row, col)
    if cell.ctype == xlrd.XL_CELL_NUMBER:
        if col == 1:
            return f"{cell.value:.1f}"
        if float(cell.value).is_integer():
            return str(int(cell.value))
    return str(cell.value)


def md(value: str) -> str:
    return value.replace("|", "\\|").replace("\r\n", "\n").replace("\r", "\n").replace("\n", "<br>")


def no_data() -> str:
    return "**Нет данных.** Проверено: БЗ [`kb/processed/README.md`](../../../../kb/processed/README.md), затем web только по доверенному домену `mango-office.ru`, запрос по точной формулировке; ни БЗ, ни web не дали результата."


def assessment(sheet: str, number: str, requirement: str) -> tuple[str, str, str]:
    robot = speech = twin = no_data()
    if not number or not requirement:
        return ("**Не оценивается.** Заголовок раздела исходной формы.",) * 3

    low = requirement.lower()
    if sheet == "Телефония":
        robot = f"**Да, частично.** Полная БЗ содержит контур ВАТС/LK: SIP Trunk, номера и маршрутизацию; параметры конкретной строки требуют сверки: {LK_SIP}."
        if number in {"1.0", "1.2.", "1.3.", "2.0", "3.0", "4.0", "5.0", "6.0", "7.0", "8.0"}:
            speech = f"**Нет данных.** Документация подтверждает настройку SIP Trunk и номеров, но не заявленный канал, протокол, кодек, SLA или ёмкость: {SA_SIP}."
        if number == "1.0":
            speech = f"**Да, частично.** Подключение и направления SIP Trunk описаны; разные физические каналы не подтверждены: {SA_SIP}."
        elif number == "1.2.":
            speech = f"**Да, частично.** Настройка SIP Trunk по IP и порту подтверждена, но термин `public intenet` явно не заявлен: {SA_SIP}."
        elif number == "4.0":
            speech = f"**Да, частично.** Для транка задаются номера и направления входящих/исходящих вызовов; передача A/B в сигнализации не специфицирована: {SA_SIP}."
        elif number == "9.0":
            robot = f"**Да, частично.** Документация подтверждает управление кампаниями и статусами задач, но не отсутствие закрепления лицензий за сценариями: {ROBOT_INTEGRATION}."
            twin = "**Да, частично.** Кампании и сценарии обзвона описаны, но лицензионная модель не подтверждена: [TWIN, кампании](https://wiki.twin24.ai/ru/voice-bots/campaigns)."
        elif number in {"10.0", "10.1.", "10.2.", "11.0"}:
            robot = f"**Да, частично.** Статусы АнтиРобот зафиксированы, но этап и время распознавания не специфицированы: {ROBOT_INTEGRATION}."
            twin = "**Да, частично.** Платформа описывает распознавание автоответчиков, но не все заявленные этапы/SLA: [TWIN, автоответчики](https://wiki.twin24.ai/ru/voice-bots/use-cases/answering-machines)."
        elif number in {"13.0", "13.1.", "13.2.", "13.3.", "13.4."}:
            robot = f"**Да, частично.** API кампаний, повторные статусы задач и замена номеров подтверждены; все детали строки отдельно не гарантированы: {ROBOT_INTEGRATION}."
            twin = "**Да, частично.** Настройки кампаний подтверждают повторные попытки и параметры обзвона; полное совпадение строки не доказано: [TWIN, кампании](https://wiki.twin24.ai/ru/voice-bots/campaigns)."
        elif number == "14.0":
            robot = f"**Да.** Блок интеграции передаёт данные клиента/взаимодействия и поддерживает HTTP/API-интеграции: {ROBOT_INTEGRATION}."
            twin = "**Да.** Контекст может передаваться через блок HTTP-запроса: [TWIN, HTTP-запрос](https://wiki.twin24.ai/ru/scripts/blocks/http-request)."
    elif sheet == "Quality Control":
        if number in {"1.0", "1.1.", "2.0", "2.4.", "2.6.", "2.7.", "2.11."}:
            speech = f"**Да, частично.** Речевая аналитика поддерживает отчёты, поиск/выборки и статистику, но конкретная метрика строки подтверждена не всегда: {SA_GENERAL}."
        if number in {"1.2.", "1.3."}:
            speech = f"**Да, частично.** Чек-листы и статистика контроля качества есть; отдельный лог ошибок/постановка задачи в SSOT не подтверждены: {SA_GENERAL}."
        if number in {"2.8.", "2.9."}:
            speech = f"**Да, частично.** Распознавание разговоров и отчёты подтверждены, но отдельный отчёт пауз после реплик не найден: {SA_RECOGNITION}."
        if number == "2.10.":
            speech = f"**Да, частично.** Отчётность по звонкам поддерживается, но распределение именно по операторам связи не заявлено: {SA_GENERAL}."
        robot = robot if not robot.startswith("**Нет данных") else f"**Нет данных.** Аналитика голосовых роботов описывает KPI звонков, но не требуемую QC-функцию: {ROBOT_ANALYTICS}."
    else:
        if number == "1.0":
            robot = "**Да.** Руководство описывает облачный веб-модуль по адресу robot.mango-office.ru: " + ROBOT_AUTH + "."
            speech = "**Да.** Подключение услуги выполняется в Личном кабинете MANGO OFFICE: " + SA_GENERAL + "."
        elif number in {"12.0", "18.0"}:
            robot = f"**Да, частично.** Пользовательский GUI и самостоятельная настройка сценариев подтверждены, но полный перечень конфигурации не заявлен: {ROBOT_AUTH}."
            speech = f"**Да, частично.** Пользовательский интерфейс и настройки описаны, но требование целиком не специфицировано: {SA_GENERAL}."
        elif number in {"20.0", "21.0", "24.0"}:
            robot = f"**Да, частично.** Авторизация и отдельная учётная запись сотрудника подтверждены; полный контракт ролей не приведён: {ROBOT_AUTH}."
            speech = f"**Да, частично.** Модуль доступен пользователям через Личный кабинет; полный контракт ролей не приведён: {SA_GENERAL}."
        elif number in {"19.0", "23.0"}:
            robot = f"**Да, частично.** Оперативный мониторинг KPI кампаний подтверждён; инфраструктурные компоненты и загрузка не раскрыты: {ROBOT_ANALYTICS}."
        elif number in {"35.0", "36.0", "37.0", "38.0", "39.0"}:
            robot = f"**Да, частично.** HTTP/API-интеграции описаны, но не весь набор SOAP/REST/gRPC: {ROBOT_INTEGRATION}."
            twin = "**Да, частично.** Блок HTTP-запроса подтверждает WEB API/HTTPS-интеграцию; SOAP и gRPC не подтверждены: [TWIN, HTTP-запрос](https://wiki.twin24.ai/ru/scripts/blocks/http-request)."
        if number in {"37.0", "38.0", "39.0"} and ("документ" in low or "руководств" in low or "обучен" in low):
            robot = f"**Да, частично.** Руководство пользователя существует; API-документация и очное обучение этой строкой не подтверждены: {ROBOT_AUTH}."
            speech = f"**Да, частично.** Наличие пользовательского руководства подтверждено; API-документация и очное обучение отдельно не подтверждены: {SA_GENERAL}."
            twin = no_data()
        if any(token in low for token in ("запис", "хранен", "ftp", "стерео")):
            robot = f"**Да, частично.** Полная БЗ ВАТС подтверждает запись, многоканальный режим и внешнее FTP/SFTP-хранилище: {LK_RECORD}."
        if any(token in low for token in ("безопас", "аутентиф", "доступ")):
            speech = f"**Да, частично.** Полная БЗ LK подтверждает двухфакторную аутентификацию и настройки безопасности; точный охват строки требует проверки: {LK_SECURITY}."
    return robot, speech, twin


def render() -> str:
    chunks = ["""---
status: draft
version: 0.1
updated: 2026-08-31
ai-generated: true
type: analysis
scope: mango-only
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/339"
---

# L0 — Форма Заказчика с оценками Приложений № 5–7

Таблицы сгенерированы непосредственно из приложенных к issue #339 файлов `.xls`.
Колонки `№`, `Требование`, `Комментарий участника` сохраняют значения ячеек исходника;
единственное представительное преобразование — перенос строки в ячейке записывается как `<br>`.
Колонки 4–6 содержат оценки по полной БЗ, включая ВАТС/LK, Роботов и QM/Речевую
аналитику, а также публичную документацию TWIN. Точка входа поиска —
[`kb/processed/README.md`](../../../../kb/processed/README.md). Вердикт **«Нет данных»**
допустим только после зафиксированной эскалации на web по доверенным доменам Mango.

Посимвольная проверка значений исходных ячеек и шестиколоночного контракта:

```bash
pip install xlrd
python3 experiments/issue_339/generate_run.py
python3 scripts/validate_issue_339_run.py
```
"""]
    for filename in FILES:
        path = DOWNLOADS / filename
        data = path.read_bytes()
        book = xlrd.open_workbook(str(path), formatting_info=True)
        sheet = book.sheet_by_index(0)
        header = next(r for r in range(sheet.nrows) if displayed(book, sheet, r, 1).strip() == "№")
        title = [displayed(book, sheet, r, 1) for r in range(header) if displayed(book, sheet, r, 1)]
        chunks.append(f"\n## Лист «{sheet.name}» — файл `{filename}`\n")
        chunks.append(f"Контрольные суммы: `md5:{hashlib.md5(data).hexdigest()}`, `sha256:{hashlib.sha256(data).hexdigest()}`.\n")
        chunks.append("Шапка листа (дословно):\n")
        chunks.extend(f"> {md(line)}\n>" for line in title)
        chunks.append("\n\n| № | Требование | Комментарий участника | Оценка по док. Mango «Роботы» | Оценка по док. Mango «Речевая аналитика» | Оценка по публичной док. TWIN |")
        chunks.append("| --- | --- | --- | --- | --- | --- |")
        for row in range(header + 1, sheet.nrows):
            source = [displayed(book, sheet, row, col) for col in (1, 2, 3)]
            if not any(source):
                continue
            evaluations = assessment(sheet.name, source[0], source[1])
            chunks.append("| " + " | ".join([*(md(cell) for cell in source), *evaluations]) + " |")
    return "\n".join(chunks) + "\n"


def main() -> int:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render(), encoding="utf-8")
    print(f"generated {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
