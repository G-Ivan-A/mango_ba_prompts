---
id: vpbx-api-195-udalenie-kampanii
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
section: "4.6.11"
pdf_section: "4.6.11"
title: "Удаление кампании"
pdf_heading: "4.6.11 Удаление кампании"
pages: "272"
source: kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf
source_part: "1"
source_pages: "ч.1: 272"
source_refs: '[{"source_pdf":"kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf","part":1,"pages":"272","global_pages":"272"}]'
extracted_by: "pdfplumber 0.11.10"
token_method: "tiktoken:cl100k_base"
tokens: 453
status: extracted
ai-generated: true
---
# 4.6.11. Удаление кампании

> Трассировка: PDF §4.6.11 · сквозные стр. 272 · источники: ч.1 `kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf` с.272.

POST /vpbx/campaign/delete Параметры:

| № | Параметры | Тип | Обяза-<br>тель-<br>ный | Описание |
| --- | --- | --- | --- | --- |
| 1 | campaign_id |  |  | id кампании, обязательное. Компанию можно удалить в<br>следующих статусах: ● 0 – остановлена; ● 4 – завершена |

Пример запроса: POST https://app.mango-office.ru/vpbx/campaign/delete vpbx_api_key = 1234567890qwerty, sign = 1234567890qwerty, json = { "campaign_id":"16340" } В результате обработки запроса, формируются и передаются JSON-данные, содержащие следующие параметры:

| № | Параметр | Тип | Обязательный | Описание |
| --- | --- | --- | --- | --- |
| 1 | result | Число | Да | Код результата |
| 2 | status | Число | Да | Текущий статус кампании.<br>Статус кампании: 0 – остановлена; 1 – запланирована;<br>2 - в работе; 3 – останавливается; 4 – завершена;<br>5 – обрабатывается; 6 - удаляется (удалена). |

Пример ответа: { "result": 1000, "status": 6 }
