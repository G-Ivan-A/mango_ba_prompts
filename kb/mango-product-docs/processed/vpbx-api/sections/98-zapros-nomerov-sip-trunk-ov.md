---
id: vpbx-api-98-zapros-nomerov-sip-trunk-ov
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
section: "3.7.22"
pdf_section: "3.7.22"
title: "Запрос номеров sip-trunk'ов"
pdf_heading: "3.7.22 Запрос номеров sip-trunk'ов"
pages: "138-139"
source: kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf
source_part: "1"
source_pages: "ч.1: 138-139"
source_refs: '[{"source_pdf":"kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf","part":1,"pages":"138-139","global_pages":"138-139"}]'
extracted_by: "pdfplumber 0.11.10"
token_method: "tiktoken:cl100k_base"
tokens: 588
status: extracted
ai-generated: true
---
# 3.7.22. Запрос номеров sip-trunk'ов

> Трассировка: PDF §3.7.22 · сквозные стр. 138-139 · источники: ч.1 `kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf` с.138-139.

POST /vpbx/trunks/numbers Метод позволяет получить информацию о sip-trunk'ах. Параметры запроса: пустой json. Примечание. Согласно модели взаимодействия, в POST-запросах отправляются обязательные поля vpbx_api_key и sign. Пример запроса: POST https://app.mango-office.ru/vpbx/trunks/numbers vpbx_api_key = 1234567890qwerty, sign = 1234567890qwerty, json = { } В результате обработки запроса, формируются и передаются JSON-данные, содержащие следующие параметры:

| № | Параметры |  | Тип | Обяза-<br>тель-<br>ный | Описание |
| --- | --- | --- | --- | --- | --- |
| 1 | result |  |  |  | Код результата:<br>● 1000 - удачное выполнение;<br>● 3300 - объект не существует;<br>● 5XXX – ошибка сервера |

| № | Параметры |  | Тип | Обяза-<br>тель-<br>ный | Описание |
| --- | --- | --- | --- | --- | --- |
| 2 | data |  |  | Да | Данные |
|  |  | trunk_number_id | integer |  | ID номера sip-trunk'а |
|  |  | trunk_id | integer |  | SIP trunk id |
|  |  | number | string |  | Номер |
|  |  | options | integer |  | Опции: 2 - принять, 4 - звонить, 6 - и принять и<br>звонить |
|  |  | desc | string |  | Описание |

Пример ответа: { "result": 1000, "data": [ { "trunk_number_id": 787, "trunk_id": 460, "number": "74955358853", "options": 2, "desc": "Номер для TrunkYou 3" }, ] }
