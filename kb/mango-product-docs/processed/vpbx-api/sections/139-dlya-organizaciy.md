---
id: vpbx-api-139-dlya-organizaciy
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
section: "3.9.4.2"
pdf_section: "3.9.4.2"
title: "Для организаций"
pdf_heading: "3.9.4.2 Для организаций"
pages: "191-192"
source: kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf
source_part: "1"
source_pages: "ч.1: 191-192"
source_refs: '[{"source_pdf":"kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf","part":1,"pages":"191-192","global_pages":"191-192"}]'
extracted_by: "pdfplumber 0.11.10"
token_method: "tiktoken:cl100k_base"
tokens: 664
status: extracted
ai-generated: true
---
# 3.9.4.2. Для организаций

> Трассировка: PDF §3.9.4.2 · сквозные стр. 191-192 · источники: ч.1 `kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf` с.191-192.

Параметры:

| № | Параметры | Тип | Обяза-<br>тель-<br>ный | Описание |
| --- | --- | --- | --- | --- |
| 1 | action |  | Да | Название события зависит от действия:<br>● при создании – new;<br>● при редактировании – updated; |

| № | Параметры | Тип | Обяза-<br>тель-<br>ный | Описание |
| --- | --- | --- | --- | --- |
|  |  |  |  | ● при удалении – deleted |
| 2 | data |  |  | Данные зависят от объекта. Набор данных идентичен получаемым<br>данным в методах «получить <объект> по id». Для контакта<br>указывается дополнительный параметр last_used |

Событие о добавлении организации Параметры события:

| № | Параметры | Тип | Обяза-<br>тель-<br>ный | Описание |
| --- | --- | --- | --- | --- |
| 1 | action |  | Да | Название события = new |
| 2 | data |  | Да | Массив организации. В массиве объектов может быть один либо<br>несколько организаций, принадлежащих одному источнику |

Пример события: POST https://external-system.com/events/ab/organizations vpbx_api_key = 1234567890qwerty, sign = 1234567890qwerty, json = { "action": "new", "data": [ { "org_id": "14642887", "org_name": "dfgdfgdfg" } ] } Событие об удалении организации Параметры события:

| № | Параметры | Тип | Обяза-<br>тель-<br>ный | Описание |
| --- | --- | --- | --- | --- |
| 1 | action |  | Да | Название события = deleted |
| 2 | data |  | Да | Массив id организации. В массиве объектов может быть одна либо<br>несколько id организаций, принадлежащих одному источнику. |
