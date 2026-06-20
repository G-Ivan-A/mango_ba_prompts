---
id: vpbx-api-165-chto-oznachaet-status-polzovatelya
doc_code: VPBXAPI
doc_title: "API Mango Office"
doc_version: "1.9"
section: "4.4.1.1"
pdf_section: "4.4.1.1"
title: "Что означает статус пользователя"
pdf_heading: "4.4.1.1 Что означает статус пользователя"
pages: "218-219"
source: kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf
source_part: "1"
source_pages: "ч.1: 218-219"
source_refs: '[{"source_pdf":"kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf","part":1,"pages":"218-219","global_pages":"218-219"}]'
extracted_by: "pdfplumber 0.11.10"
token_method: "tiktoken:cl100k_base"
tokens: 461
status: extracted
ai-generated: true
---
# 4.4.1.1. Что означает статус пользователя

> Трассировка: PDF §4.4.1.1 · сквозные стр. 218-219 · источники: ч.1 `kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf` с.218-219.

Статус - это атрибут пользователя, который определяет его готовность к приему вызовов. КЦ позволяет в любой момент времени выбрать нужный статус пользователя. Для выбора доступны: - предустановленные статусы - 6 статусов; - На линии; - Не беспокоить; - Перерыв; - Оффлайн; - Исходящий обзвон; - Все звонки. - пользовательский статус, созданный на основе предустановленных статусов. В КЦ можно создать до 30 пользовательских статусов, чтобы более гибко определять готовность оператора к приему вызовов. Обратите внимание, что вы можете работать через API только с теми пользовательскими статусами, которым в настройках КЦ присвоен синоним. В свою очередь, синоним соответствует параметру status_alias в методах API. Чтобы узнать, как присвоить синоним пользовательскому статусу, ознакомьтесь со справочными материалами КЦ.

![Изображение, стр. 219](../images/165-chto-oznachaet-status-polzovatelya-1.jpeg)

Рисунок 6
