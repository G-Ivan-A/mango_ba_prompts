---
id: vpbx-api-172-izmenenie-statusa-polzovatelya
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
section: "4.4.2.1"
pdf_section: "4.4.2.1"
title: "Изменение статуса пользователя"
pdf_heading: "4.4.2.1 Изменение статуса пользователя"
pages: "225"
source: kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf
source_part: "1"
source_pages: "ч.1: 225"
source_refs: '[{"source_pdf":"kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf","part":1,"pages":"225","global_pages":"225"}]'
extracted_by: "pdfplumber 0.11.10"
token_method: "tiktoken:cl100k_base"
tokens: 431
status: extracted
ai-generated: true
---
# 4.4.2.1. Изменение статуса пользователя

> Трассировка: PDF §4.4.2.1 · сквозные стр. 225 · источники: ч.1 `kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf` с.225.

POST /events/user/status_changed Событие о смене статуса пользователя. Параметры:

| № | Параметры | Тип | Обяза-<br>тель-<br>ный | Описание |
| --- | --- | --- | --- | --- |
| 1 | abonent_id | целое | Нет | Идентификатор абонента |
| 2 | status | целое | Да | Статус оператора |
| 3 | status_alias | string | Нет | Псевдоним/синоним статуса |
| 4 | parent_status | целое | Нет | Базовый статус оператора (влияющий на телефонию) |
| 5 | when | целое | Нет | Время смены статуса в UTC в миллисекундах |
| 6 | timestamp | целое | Нет | Текущее время сервера в UTC на момент отправки пакета в<br>миллисекундах |

Пример события: POST https://app.mango-office.ru/events/user/status_changed vpbx_api_key = 1234567890qwerty, sign = 1234567890qwerty, json = { "abonent_id": 787585, "status": 10, "parent_status":1, "status_alias": qwe123, "when": 109822219823, "timestamp": 109822219877 }
