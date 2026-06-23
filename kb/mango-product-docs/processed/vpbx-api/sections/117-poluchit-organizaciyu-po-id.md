---
id: vpbx-api-117-poluchit-organizaciyu-po-id
doc_code: VPBXAPI
doc_title: "API Mango Office"
doc_version: "1.9"
type: "api_reference"
product: "Mango VPBX"
platform: ["API"]
language: "ru"
topics: ["API","VPBX","интеграция","телефония","REST API","разработка"]
aliases: ["API VPBX","VPBX API","API ВАТС","API виртуальной АТС","Open API Mango Office"]
mango_taxonomy_primary_cluster: "vats-core"
mango_taxonomy_secondary_clusters: ["contact-center-core","platform-integrations"]
mango_taxonomy_product_refs: ["mango-virtual-pbx-official","mango-contact-center-official"]
mango_taxonomy_evidence_refs: ["kb/mango-taxonomy/registry.json","standards/mango-taxonomy-standard.md","kb/mango-product-docs/processed/vpbx-api/index.md"]
section: "3.9.1.1"
pdf_section: "3.9.1.1"
title: "Получить организацию по id"
pdf_heading: "3.9.1.1 Получить организацию по id"
pages: "152-153"
source: kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf
source_part: "1"
source_pages: "ч.1: 152-153"
source_refs: '[{"source_pdf":"kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf","part":1,"pages":"152-153","global_pages":"152-153"}]'
extracted_by: "pdfplumber 0.11.10"
token_method: "tiktoken:cl100k_base"
tokens: 468
status: extracted
ai-generated: true
---
# 3.9.1.1. Получить организацию по id

> Трассировка: PDF §3.9.1.1 · сквозные стр. 152-153 · источники: ч.1 `kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf` с.152-153.

POST /vpbx/ab/organization Метод возвращает информацию об организации. Работа с организациями доступна в Контакт- центре. Параметры:

| № | Параметры | Тип | Обяза-<br>тель-<br>ный | Описание |
| --- | --- | --- | --- | --- |
| 1 | org_id |  |  | id организации |

Пример запроса: POST https://app.mango-office.ru/vpbx/ab/organization vpbx_api_key = 1234567890qwerty, sign = 1234567890qwerty, json = { "org_id":"10182085" } В результате обработки запроса, формируются и передаются JSON-данные, содержащие следующие параметры:

| № | Параметры с уровнями<br>вложенности |  | Тип | Обяза-<br>тель-<br>ный | Описание |
| --- | --- | --- | --- | --- | --- |
|  | 1 | 2 |  |  |  |
| 1 | result |  |  | Да | Код результата |
| 2 | data |  |  |  |  |
|  |  | org_id |  |  | id организации |
|  |  | org_name | string |  | Название организации |

Пример ответа: { "result: 1000, "data: { "org_id: "10182085", "org_name: "компания 2" } }
