---
id: vpbx-api-90-udalit-sotrudnika
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
section: "3.7.14"
pdf_section: "3.7.14"
title: "Удалить сотрудника"
pdf_heading: "3.7.14 Удалить сотрудника"
pages: "130"
source: kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf
source_part: "1"
source_pages: "ч.1: 130"
source_refs: '[{"source_pdf":"kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf","part":1,"pages":"130","global_pages":"130"}]'
extracted_by: "pdfplumber 0.11.10"
token_method: "tiktoken:cl100k_base"
tokens: 424
status: extracted
ai-generated: true
---
# 3.7.14. Удалить сотрудника

> Трассировка: PDF §3.7.14 · сквозные стр. 130 · источники: ч.1 `kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf` с.130.

POST /vpbx/member/delete Метод позволяет удалить сотрудника в Виртуальной АТС. Параметры запроса:

| № | Параметры | Тип | Обяза-<br>тель-<br>ный | Описание |
| --- | --- | --- | --- | --- |
| 1 | user_id | integer | Да | ID сотрудника |

Пример запроса: POST https://app.mango-office.ru/vpbx/member/delete vpbx_api_key = 1234567890qwerty, sign = 1234567890qwerty, json = { "user_id":"300051452" } В результате обработки запроса, формируются и передаются JSON-данные, содержащие следующие параметры:

| № | Параметры | Обяза-<br>тель-<br>ный | Описание |
| --- | --- | --- | --- |
| 1 | Result | Да | Код результата:<br>● 1000 - удачное выполнение;<br>● 3100 - переданы неверные параметры команды;<br>● 31XX - неверные параметры;<br>● 3300 - объект не существует;<br>● 5302 - запрещено создание\удаление сотрудника-робота<br>● 5XXX – ошибка сервера. |

Пример ответа: { "result": 1000 }
