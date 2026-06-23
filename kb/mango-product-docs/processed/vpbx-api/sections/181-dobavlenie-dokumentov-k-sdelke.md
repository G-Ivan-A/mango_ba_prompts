---
id: vpbx-api-181-dobavlenie-dokumentov-k-sdelke
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
section: "4.5.7"
pdf_section: "4.5.7"
title: "Добавление документов к сделке"
pdf_heading: "4.5.7 Добавление документов к сделке"
pages: "238-239"
source: kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf
source_part: "1"
source_pages: "ч.1: 238-239"
source_refs: '[{"source_pdf":"kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf","part":1,"pages":"238-239","global_pages":"238-239"}]'
extracted_by: "pdfplumber 0.11.10"
token_method: "tiktoken:cl100k_base"
tokens: 622
status: extracted
ai-generated: true
---
# 4.5.7. Добавление документов к сделке

> Трассировка: PDF §4.5.7 · сквозные стр. 238-239 · источники: ч.1 `kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf` с.238-239.

POST /cc/deal/documents.add Назначение: добавление документов к сделке. Параметры уведомления:

| № | Параметры | Тип | Обяза-<br>тель-<br>ный | Описание |
| --- | --- | --- | --- | --- |
| 1 | deal_id | Число | Да | Уникальный номер сделки |
| 2 | file | Файл | Да | Файл для загрузки |
| 3 | member_id | Число | См.<br>описа-<br>ние | Идентификатор мембера, создающего документ.<br>Обязательно указывать одно из значений: member_id или<br>abonent_id. Если указать оба - приоритет будет у abonent_id. |
| 4 | abonent_id | Число | См.<br>описа-<br>ние | Сотрудник, создающий документ.<br>Обязательно указывать одно из значений: member_id или<br>abonent_id. Если указать оба - приоритет будет у abonent_id. |

Пример запроса: POST https://app.mango-office.ru/cc/deal/documents.add vpbx_api_key = 1234567890qwerty, sign = 1234567890qwerty, json = { "deal_id":233132, "abonent_id":10068839 } ///сам файл отправляется в отдельной переменной file В результате обработки запроса, формируются и передаются JSON-данные, содержащие следующие параметры:

| № | Параметры | Тип | Обяза-<br>тель-<br>ный | Описание |
| --- | --- | --- | --- | --- |
| 1 | result |  | Да | Код результата (см. Список кодов результата) |
| 2 | error |  |  | Сообщение поясняющее код результата |
| 3 | document_id |  |  | Уникальный номер документа, присвоенный системой |

Пример ответа: { "result": 1000, "document_id": 2809 }
