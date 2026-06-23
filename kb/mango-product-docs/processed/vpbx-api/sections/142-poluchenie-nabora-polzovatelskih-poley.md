---
id: vpbx-api-142-poluchenie-nabora-polzovatelskih-poley
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
section: "3.9.5"
pdf_section: "3.9.5"
title: "Получение набора пользовательских полей"
pdf_heading: "3.9.5 Получение набора пользовательских полей"
pages: "196-198"
source: kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf
source_part: "1"
source_pages: "ч.1: 196-198"
source_refs: '[{"source_pdf":"kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf","part":1,"pages":"196-198","global_pages":"196-198"}]'
extracted_by: "pdfplumber 0.11.10"
token_method: "tiktoken:cl100k_base"
tokens: 1189
status: extracted
ai-generated: true
---
# 3.9.5. Получение набора пользовательских полей

> Трассировка: PDF §3.9.5 · сквозные стр. 196-198 · источники: ч.1 `kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf` с.196-198.

POST /vpbx/ab/custom_fields/ Используя этот запрос, вы можете получить только набор пользовательских полей из контакта, в отличии от запроса «Получить контакт по ID», в котором вы получаете сразу все данные контакта. Параметры запроса: пустой json. Примечание. Согласно модели взаимодействия, в POST-запросах отправляются обязательные поля vpbx_api_key и sign. Пример запроса: POST https://app.mango-office.ru/vpbx/ab/custom_fields/ vpbx_api_key = 1234567890qwerty, sign = 1234567890qwerty, json = { } В результате обработки запроса, формируются и передаются JSON-данные, содержащие следующие параметры:

| № | Параметры | Тип | Обяза-<br>тель-<br>ный | Описание |
| --- | --- | --- | --- | --- |
| 1 | result |  | Да | Код результата |
| Общие атрибуты |  |  |  |  |
| 2 | custom_field_id |  |  | Идентификатор пользовательского поля |
| 3 | type |  |  | Тип поля (1 - текст, 2 - список, 3 - мультисписок) |
| 4 | order |  |  | Порядковый номер поля |
| 5 | name |  |  | Наименование пользовательского поля |
| 6 | required |  |  | Признак обязательно ли к заполнению |
| 7 | api_only |  |  | Признак. что поле не может редактировать пользователь,<br>заполнение поля доступно только через импорт контактов |
| Атрибуты типа "Текст" |  |  |  |  |
| 8 | unique |  |  | Проверка уникальности при сохранении |
| 9 | check_mode |  |  | Тип проверки длины поля:<br>0 - без проверки,<br>1 - '<'<br>2 - '=='<br>3 - '>' |
| 10 | check_lengt |  |  | Длина строки используемая при check_mode != 0 ; |
| Атрибуты типа "Список" и "Мультисписок" |  |  |  |  |
| 11 | Items |  | Да | Массив объектов «Пункт списка». Элемент для атрибутов типа<br>"Список" и "Мультисписок" |
| 12 | enum_id |  |  | Идентификатор пункта списка |
| 13 | order |  |  | Порядковый номер поля |
| 14 | name |  |  | Название пункта |

Пример ответа: {"result": 1000, "data": [ { "custom_field_id": 5396, "name: "тест", "type: 3,

| "order: 0,<br>"required: false,<br>"api_only: false, |
| --- |
| "items:<br>[ |
| {<br>"enum_id: 6725, |
| "name: "1",<br>"order: 0<br>}, |
| {<br>"enum_id: 6747,<br>"name: "4",<br>"order: 1 |
| },<br>{<br>"enum_id: 6756, |
| "name: "ОдинИзмен",<br>"order: 2 |
| },<br>]<br>}, |
| {<br>"custom_field_id": 3262,<br>"name": "Притве Андрей", |
| "type": 2,<br>"order": 1,<br>"required": false,<br>"api_only": false,<br>"items":<br>[<br>{<br>"enum_id": 6553,<br>"name": "Кока",<br>"order": 0<br>},<br>{<br>"enum_id": 6554,<br>"name": "Квок", |
| "order": 1<br>},<br>] |
| },<br>{<br>"custom_field_id": 5453,<br>"name": "Пользовательское поле 2",<br>"type"": 1,<br>"order: 8,<br>"required": false,<br>"api_only": true,<br>"unique": false,<br>"check_mode": 0,<br>"check_length": 10<br>}<br>]} |
