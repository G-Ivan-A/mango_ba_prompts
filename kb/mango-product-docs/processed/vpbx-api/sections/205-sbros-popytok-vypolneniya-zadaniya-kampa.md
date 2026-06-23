---
id: vpbx-api-205-sbros-popytok-vypolneniya-zadaniya-kampa
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
section: "4.6.19"
pdf_section: "4.6.19"
title: "Сброс попыток выполнения задания кампании ИО"
pdf_heading: "4.6.19 Сброс попыток выполнения задания кампании ИО"
pages: "286"
source: kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf
source_part: "1"
source_pages: "ч.1: 286"
source_refs: '[{"source_pdf":"kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf","part":1,"pages":"286","global_pages":"286"}]'
extracted_by: "pdfplumber 0.11.10"
token_method: "tiktoken:cl100k_base"
tokens: 372
status: extracted
ai-generated: true
---
# 4.6.19. Сброс попыток выполнения задания кампании ИО

> Трассировка: PDF §4.6.19 · сквозные стр. 286 · источники: ч.1 `kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf` с.286.

POST /vpbx/tasks/reset Возвращает на повторное выполнение переданные задания кампании. Параметры запроса:

| Параметр | Тип | Обяза-<br>тель-<br>ный | Описание |
| --- | --- | --- | --- |
| campaign_id | Число | Да | ID кампании |
| task_ids | Массив<br>чисел | Да | Массив идентификаторов заданий, которые нужно вернуть на<br>повторное выполнение |

Пример запроса: POST https://app.mango-office.ru/vpbx/tasks/reset vpbx_api_key = 1234567890qwerty, sign = 1234567890qwerty, json = { "task_id": "2489649" } В результате обработки запроса, формируются и передаются JSON-данные, содержащие следующие параметры:

| № | Параметр | Тип | Обязательный | Описание |
| --- | --- | --- | --- | --- |
| 1 | result | Число | Да | Код результата |

Пример ответа: { "result": 1000 }
