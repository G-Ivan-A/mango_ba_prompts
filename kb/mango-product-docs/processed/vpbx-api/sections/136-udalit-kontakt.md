---
id: vpbx-api-136-udalit-kontakt
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
section: "3.9.3.6"
pdf_section: "3.9.3.6"
title: "Удалить контакт"
pdf_heading: "3.9.3.6 Удалить контакт"
pages: "190-191"
source: kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf
source_part: "1"
source_pages: "ч.1: 190-191"
source_refs: '[{"source_pdf":"kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf","part":1,"pages":"190-191","global_pages":"190-191"}]'
extracted_by: "pdfplumber 0.11.10"
token_method: "tiktoken:cl100k_base"
tokens: 403
status: extracted
ai-generated: true
---
# 3.9.3.6. Удалить контакт

> Трассировка: PDF §3.9.3.6 · сквозные стр. 190-191 · источники: ч.1 `kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf` с.190-191.

POST /vpbx/ab/contacts/delete Метод позволяет удалить контакт. Также можно удалить несколько контактов, до 500. Параметры:

| № | Параметры | Тип | Обяза- | Описание |
| --- | --- | --- | --- | --- |

|  | 1 | 2 |  | тель-<br>ный |  |
| --- | --- | --- | --- | --- | --- |
| 1 | data |  |  |  | Массив удаляемых контактов, разделитель «;» |
| 1.1 |  | contact_id |  |  | id контакта |

Пример запроса: POST https://app.mango-office.ru/vpbx/ab/contacts/delete vpbx_api_key = 1234567890qwerty, sign = 1234567890qwerty, json = { "data": [ "10433913" ] } В результате обработки запроса, формируются и передаются JSON-данные, содержащие код результата:

| № | Параметры | Тип | Обяза-<br>тель-<br>ный | Описание |
| --- | --- | --- | --- | --- |
| 1 | result |  | Да | Код результата |

Пример ответа: { "result": 1000 }
