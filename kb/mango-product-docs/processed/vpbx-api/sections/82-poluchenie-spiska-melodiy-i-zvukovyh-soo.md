---
id: vpbx-api-82-poluchenie-spiska-melodiy-i-zvukovyh-soo
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
section: "3.7.8"
pdf_section: "3.7.8"
title: "Получение списка мелодий и звуковых сообщений"
pdf_heading: "3.7.8 Получение списка мелодий и звуковых сообщений"
pages: "119-120"
source: kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf
source_part: "1"
source_pages: "ч.1: 119-120"
source_refs: '[{"source_pdf":"kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf","part":1,"pages":"119-120","global_pages":"119-120"}]'
extracted_by: "pdfplumber 0.11.10"
token_method: "tiktoken:cl100k_base"
tokens: 595
status: extracted
ai-generated: true
---
# 3.7.8. Получение списка мелодий и звуковых сообщений

> Трассировка: PDF §3.7.8 · сквозные стр. 119-120 · источники: ч.1 `kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf` с.119-120.

POST /vpbx/audiofiles Данная функция возвращает список мелодий общих и продукта. Общими являются мелодии, не принадлежащие конкретному продукту, для кампаний ИО могут использоваться всеми. Мелодиями продукта являются аудиофайлы, установленные от лица продукта, используются только самим продуктом. Параметры запроса: пустой json. Примечание. Согласно модели взаимодействия, в POST-запросах отправляются обязательные поля vpbx_api_key и sign. Пример запроса: POST https://app.mango-office.ru/vpbx/audiofiles vpbx_api_key = 1234567890qwerty, sign = 1234567890qwerty, json = { } В результате обработки запроса, формируются и передаются JSON-данные, содержащие следующие параметры:

| № | Параметры |  | Тип | Обязательный | Описание |
| --- | --- | --- | --- | --- | --- |
|  | 1 | 2 |  |  |  |
| 1 | result |  |  | Да | Код результата |
| 2 | audiofiles |  |  |  |  |
|  |  | id |  |  | id аудиофайла |

| № | Параметры |  | Тип | Обязательный | Описание |
| --- | --- | --- | --- | --- | --- |
|  |  | name |  |  | Название аудиофайла |

Пример ответа: { "result": 1000, "audiofiles": [ { "id": 17, "name": "Abandoned" }, { "id": 20, "name": "Aisle 9 Please" }, { "id": 56, "name": "Aventura Love Story" }, { "id": 57, "name": "Bad boys blue Only one breath away" }, ... ] }
