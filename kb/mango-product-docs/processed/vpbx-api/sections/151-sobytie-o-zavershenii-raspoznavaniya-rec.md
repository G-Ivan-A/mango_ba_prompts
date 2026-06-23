---
id: vpbx-api-151-sobytie-o-zavershenii-raspoznavaniya-rec
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
section: "3.10.3"
pdf_section: "3.10.3"
title: "Событие о завершении распознавания речи в WAV-файле"
pdf_heading: "3.10.3 Событие о завершении распознавания речи в WAV-файле"
pages: "203"
source: kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf
source_part: "1"
source_pages: "ч.1: 203"
source_refs: '[{"source_pdf":"kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf","part":1,"pages":"203","global_pages":"203"}]'
extracted_by: "pdfplumber 0.11.10"
token_method: "tiktoken:cl100k_base"
tokens: 467
status: extracted
ai-generated: true
---
# 3.10.3. Событие о завершении распознавания речи в WAV-файле

> Трассировка: PDF §3.10.3 · сквозные стр. 203 · источники: ч.1 `kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf` с.203.

POST /events/recognized/offline Событие содержит информацию о статусе выполнения задания на распознавание речи, сформированного в результате выполнения этого, либо этого запроса. Примечание. Событие может приходить с задержкой в 60 секунд из-за ограничения хранилища данных. Параметры:

| № | Параметры | Тип | Обяза-<br>тель-<br>ный | Описание |
| --- | --- | --- | --- | --- |
| 1 | product_id | integer |  | Идентификатор продукта |
| 2 | request_id | string |  | id-номер созданного задания на распознавание речи |
| 3 | recognized | integer |  | Временная метка, опционально, время завершения распознавания |
| 4 | result | integer |  | Результат выполнения команды |
| 5 | message | string |  | Краткое описание результата выполнения команды, опционально<br>(обязательно, если result != 1000). |

Пример запроса: POST https://app.mango-office.ru/events/recognized/offline vpbx_api_key = 1234567890qwerty, sign = 1234567890qwerty, json = { "product_id": 300022532, "request_id": 298842241, "recognized": 1647946810404, "result": 1000 }
