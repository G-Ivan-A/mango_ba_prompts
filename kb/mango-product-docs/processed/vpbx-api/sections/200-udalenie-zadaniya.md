---
id: vpbx-api-200-udalenie-zadaniya
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
section: "4.6.16"
pdf_section: "4.6.16"
title: "Удаление задания"
pdf_heading: "4.6.16 Удаление задания"
pages: "280-281"
source: kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf
source_part: "1"
source_pages: "ч.1: 280-281"
source_refs: '[{"source_pdf":"kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf","part":1,"pages":"280-281","global_pages":"280-281"}]'
extracted_by: "pdfplumber 0.11.10"
token_method: "tiktoken:cl100k_base"
tokens: 332
status: extracted
ai-generated: true
---
# 4.6.16. Удаление задания

> Трассировка: PDF §4.6.16 · сквозные стр. 280-281 · источники: ч.1 `kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf` с.280-281.

POST /vpbx/task/delete Метод предназначен для удаления задания кампании ИО. Параметры запроса:

| № | Параметр | Тип | Обязательный | Описание |
| --- | --- | --- | --- | --- |
| 1 | campaign_id | Число | Да | ID кампании |
| 2 | task_id | Число | Да | ID задания кампании |

Пример запроса: POST https://app.mango-office.ru/vpbx/task/delete vpbx_api_key = 1234567890qwerty, sign = 1234567890qwerty, json = {"campaign_id": 56919, "task_id": 11227830 } В результате обработки запроса, формируются и передаются JSON-данные, содержащие следующие параметры:

| № | Параметр | Тип | Обязательный | Описание |
| --- | --- | --- | --- | --- |
| 1 | result | Число | Да | Код результата |
