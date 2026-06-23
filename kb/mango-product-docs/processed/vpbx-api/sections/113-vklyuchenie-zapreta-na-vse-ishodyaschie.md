---
id: vpbx-api-113-vklyuchenie-zapreta-na-vse-ishodyaschie
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
section: "3.8.3.7"
pdf_section: "3.8.3.7"
title: "Включение запрета на все исходящие коммуникации"
pdf_heading: "3.8.3.7 Включение запрета на все исходящие коммуникации"
pages: "151"
source: kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf
source_part: "1"
source_pages: "ч.1: 151"
source_refs: '[{"source_pdf":"kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf","part":1,"pages":"151","global_pages":"151"}]'
extracted_by: "pdfplumber 0.11.10"
token_method: "tiktoken:cl100k_base"
tokens: 489
status: extracted
ai-generated: true
---
# 3.8.3.7. Включение запрета на все исходящие коммуникации

> Трассировка: PDF §3.8.3.7 · сквозные стр. 151 · источники: ч.1 `kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf` с.151.

POST /vpbx/outbound_blacklist/enable Включение опции запрета на исходящие коммуникации. Примечание. Для вызова метода требуется в ВАТС наличие подключенной услуги "Черный и белый списки". Параметры запроса: пустой json. Примечание. Согласно модели взаимодействия, в POST-запросах отправляются обязательные поля vpbx_api_key и sign. Пример запроса: POST https://app.mango-office.ru/vpbx/outbound_blacklist/enable vpbx_api_key = 1234567890qwerty, sign = 1234567890qwerty, json = { } В результате обработки запроса, формируются и передаются JSON-данные, содержащие код ошибки:

| № | Параметры | Тип | Обяза-<br>тель-<br>ный | Описание |
| --- | --- | --- | --- | --- |
| 1 | Result |  | Да | Код результата:<br>● 1000 - команда выполнена успешно;<br>● 5000 - внутренняя ошибка сервера;<br>● 5008 - не подлючена услуга "Черный и белый списки" в ВАТС<br>или услуга Контакт-центра "Исходящий обзвон PRO", или опция<br>блокировки исходящих номеров. |

Пример ответа: { "result": 1000 }
