---
id: vpbx-api-124-poluchit-gruppu-po-id
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
section: "3.9.2.1"
pdf_section: "3.9.2.1"
title: "Получить группу по id"
pdf_heading: "3.9.2.1 Получить группу по id"
pages: "160-161"
source: kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf
source_part: "1"
source_pages: "ч.1: 160-161"
source_refs: '[{"source_pdf":"kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf","part":1,"pages":"160-161","global_pages":"160-161"}]'
extracted_by: "pdfplumber 0.11.10"
token_method: "tiktoken:cl100k_base"
tokens: 456
status: extracted
ai-generated: true
---
# 3.9.2.1. Получить группу по id

> Трассировка: PDF §3.9.2.1 · сквозные стр. 160-161 · источники: ч.1 `kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf` с.160-161.

POST /vpbx/ab/group Метод возвращает информацию о группе. Работа с группами доступна в Контакт-центре. Параметры:

| № | Параметры | Тип | Обяза-<br>тель-<br>ный | Описание |
| --- | --- | --- | --- | --- |
| 1 | group_id |  |  | id группы |

Пример запроса: POST https://app.mango-office.ru/vpbx/ab/group vpbx_api_key = 1234567890qwerty, sign = 1234567890qwerty, json = { "group_id":"10129645" } В результате обработки запроса, формируются и передаются JSON-данные, содержащие следующие параметры:

| № | Параметры с<br>уровнями<br>вложенности |  | Тип | Обяза-<br>тель-<br>ный | Описание |
| --- | --- | --- | --- | --- | --- |
|  | 1 | 2 |  |  |  |
| 1 | result |  |  |  | Код результата |
| 2 | data |  |  |  |  |
|  |  | group_id | string |  | Идентификатор группы |
| 4 |  | group_name | string |  | Название группы |

Пример ответа: { "result": 1000, "data": { "group_id": "10129645", "group_name": "NAMER" } }
