#!/usr/bin/env python3
"""Generate corrected RUN-0065 directly from the task 1099 XLSX."""
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
EVIDENCE = {
 "sip": ("[LK_manual_v-123, §5 «SIP Trunk», с.520](../../../../kb/processed/mango-lk-manual/sections/320-sip-trunk.md)", "БЗ подтверждает SIP Trunk; количественные и операторские параметры следует сверить с договором."),
 "carousel": ("[LK_manual_v-123, §4.5.19 «Карусель номеров», с.414–416](../../../../kb/processed/mango-lk-manual/sections/252-karusel-nomerov.md)", "БЗ подтверждает ротацию номеров и несколько одновременных каруселей."),
 "record": ("[LK_manual_v-123, §4.5.3.4 «Настройки записи», с.226–231](../../../../kb/processed/mango-lk-manual/sections/138-nastroyki.md)", "БЗ подтверждает многоканальную стереозапись, запись ВКС и внешнее FTP/SFTP-хранилище."),
 "2fa": ("[LK_manual_v-123, §4.6.3.5 «Безопасность PRO», с.467–470](../../../../kb/processed/mango-lk-manual/sections/291-bezopasnost-pro.md)", "БЗ подтверждает двухфакторную аутентификацию; способ и охват сверяются с формулировкой строки."),
 "mobile": ("[LK_manual_v-123, §4 «Приложение Личный кабинет», с.69–70](../../../../kb/processed/mango-lk-manual/sections/70-prilozhenie-lichnyy-kabinet.md)", "БЗ подтверждает ссылки на приложения в Google Play и App Store."),
 "address": ("[LK_manual_v-123, §4.5.10 «Адресная книга контрагентов», с.275–276](../../../../kb/processed/mango-lk-manual/sections/177-adresnaya-kniga-kontragentov.md)", "БЗ подтверждает адресную книгу и операции с контактами."),
 "blacklist": ("[LK_manual_v-123, §4.4.5 «Черный/белый список», с.108–110](../../../../kb/processed/mango-lk-manual/sections/110-chernyy-belyy-spisok.md)", "БЗ подтверждает управление черным и белым списками."),
 "avito": ("[LK_manual_v-123, §4.5.11.2.2 «Авито Работа», с.339–345](../../../../kb/processed/mango-lk-manual/sections/210-avito-rabota.md)", "БЗ подтверждает канал «Авито Работа» в текстовых коммуникациях."),
 "api": ("[API_VPBX_v2, §1.2 «Требования совместимости», с.7](../../../../kb/processed/vpbx-api/sections/04-trebovaniya-sovmestimosti-i-spisok-podde.md)", "БЗ подтверждает HTTPS/TLS 1.2 и API-коннектор; внешний контракт интеграции отдельно не доказан."),
 "speech": ("[API_VPBX_v2, §4.10 «Speech2Text», с.327–339](../../../../kb/processed/vpbx-api/sections/67-poluchenie-tematik-razgovora-speech2text.md)", "БЗ подтверждает распознавание и каналы стереозаписи; полный workflow требует декомпозиции."),
}
FALLBACK = ("[KB_index, §«Состав БЗ», с.n/a](../../../../kb/processed/README.md)", "Полная БЗ проверена, но однозначного подтверждения составного или договорного требования нет; требуется владелец продукта, договор/SLA либо нагрузочное испытание.")

def rows():
 assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == EXPECTED_SHA256
 with zipfile.ZipFile(SOURCE) as book:
  root = ET.fromstring(book.read("xl/sharedStrings.xml")); strings = ["".join(n.text or "" for n in i.iter(NS+"t")) for i in root.findall(NS+"si")]
  sheet = ET.fromstring(book.read("xl/worksheets/sheet1.xml")); result=[]
  for row in sheet.findall(f".//{NS}sheetData/{NS}row"):
   cells={}
   for cell in row.findall(NS+"c"):
    match=re.match(r"[A-Z]+",cell.attrib["r"]); node=cell.find(NS+"v"); value="" if node is None else node.text or ""
    if cell.attrib.get("t")=="s" and value: value=strings[int(value)]
    if match: cells[match.group()]=value
   source=(cells.get("B",""),cells.get("C",""),cells.get("D",""))
   if any(source): result.append((int(row.attrib["r"]),*source))
  return result

def md(value): return value.replace("|","\\|").replace("\r\n","\n").replace("\r","\n").replace("\n","<br>")

def assess(requirement):
 low=requirement.lower(); heading=not re.search(r"долж|обеспеч|возможност|поддерж|налич|предостав|не менее|работа",low) and len(requirement)<110
 if heading: return "","","Структурная строка исходного XLSX; оценка не выполняется."
 rules=((("карусел","ротаци"),"carousel"),(("sip","транк"),"sip"),(("стерео","ftp","запис"),"record"),(("двухфактор","2fa"),"2fa"),(("google play","app store","мобильн"),"mobile"),(("адресн","контакт"),"address"),(("черн","белый список"),"blacklist"),(("авито работа",),"avito"),(("api","webhook","tls","srtp","интеграц"),"api"),(("транскриб","распознав","речев"),"speech"))
 matches=[key for tokens,key in rules if any(token in low for token in tokens)]; citation,basis=EVIDENCE[matches[0]] if matches else FALLBACK
 compound=len(requirement)>280 or len(matches)>1; verdict="Частично" if matches and compound else "Да" if matches else "Нет"
 if verdict=="Частично": basis+=" Подтвержденная атомарная часть отделена от неподтвержденных ограничений строки."
 elif verdict=="Нет": basis+=" До подтверждения обязательство считается требующим доработки."
 audit="Критик-аудит: "+("декомпозировать строку и проверить неподтвержденные ограничения; " if compound else "проверить применимость к точному контуру; ")+"не подменять capability договорной гарантией."
 return f"**{verdict}.**",f"{basis} {citation}",audit

def render():
 lines=["""---
status: draft
version: 0.2
updated: 2026-09-01
ai-generated: true
type: analysis
scope: task-1099-only
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/349"
---

# L0 — оценка исполнимости ТЗ «Телефония»

Изменение существующего RUN-0065. Колонки 1–3 воспроизводятся из исходного XLSX
(переносы представлены `<br>`). Колонка 4 использует только `Да / Частично / Нет / пусто`;
`Частично` применяется к атомарно декомпозируемым составным требованиям, заголовки
остаются пустыми. Поиск начинался со всей БЗ через `kb/processed/README.md`.

| Требования к системе | Блок-фактор (источник) | Исходная колонка D | Оценка | Обоснование + атомарная ссылка | Технический критик-аудит |
| --- | --- | --- | --- | --- | --- |"""]
 for num,requirement,blocker,source_d in rows():
  verdict,basis,audit=assess(requirement)
  if blocker.strip().lower()=="да" and verdict: audit+=" БЛОК-ФАКТОР: human decision до принятия обязательства."
  lines.append("| "+" | ".join((md(requirement),md(blocker),md(source_d),verdict,basis,audit))+" |")
 return "\n".join(lines)+"\n"

if __name__=="__main__":
 OUT.write_text(render(),encoding="utf-8"); print(f"generated {OUT.relative_to(ROOT)} from {len(rows())} source rows")
