---
id: vpbx-api-152-poluchenie-rezultata-raspoznavaniya-rech
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
section: "3.10.4"
pdf_section: "3.10.4"
title: "Получение результата распознавания речи в WAV-файле"
pdf_heading: "3.10.4 Получение результата распознавания речи в WAV-файле"
pages: "204-206"
source: kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf
source_part: "1"
source_pages: "ч.1: 204-206"
source_refs: '[{"source_pdf":"kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf","part":1,"pages":"204-206","global_pages":"204-206"}]'
extracted_by: "pdfplumber 0.11.10"
token_method: "tiktoken:cl100k_base"
tokens: 1139
status: extracted
ai-generated: true
---
# 3.10.4. Получение результата распознавания речи в WAV-файле

> Трассировка: PDF §3.10.4 · сквозные стр. 204-206 · источники: ч.1 `kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf` с.204-206.

POST /vpbx/transcribes/tasks/ Метод обеспечивает получение массива текстовых данных, содержащих результаты распознавания речи в звуковом файле, выполненного по этому, либо этому запросу. Параметры:

| № | Параметры | Тип | Обяза-<br>тель-<br>ный | Описание |
| --- | --- | --- | --- | --- |
| 1 | request_id | integer |  | id-номер созданного задания (выполненного по этому, либо<br>этому запросу) на распознавание речи в звуковом файле |

Пример запроса: POST https://app.mango-office.ru/vpbx/transcribes/tasks/ vpbx_api_key = 1234567890qwerty, sign = 1234567890qwerty, json = { "request_ids": [ "1532496969", "4317496830089587018", "677044718" ] } В результате обработки запроса, формируются и передаются JSON-данные, содержащие следующие параметры:

| № | Параметры |  | Тип | Обяза-<br>тель-<br>ный | Описание |
| --- | --- | --- | --- | --- | --- |
|  | 1 | 2 |  |  |  |
| 1 | Result |  | integer | Да | Код результата |
| 2 | data |  | array |  | Массив данных с результатами расшифровок<br>разговоров |
| 3 |  | request_id | integer |  | id |
| 4 |  | status | string |  | Статус |
| 5 |  | time_created | integer |  | Время создания задачи распознавания |
|  |  | time_updated | integer |  | Время обновления статуса задачи распознавания |
|  |  | transcribes | array |  |  |
|  |  | channel | integer/string |  | Канал |
|  |  | data | array |  | ■ word (тип string): распознанная речь;<br>■ begin (тип integer): время начала;<br>■ end (тип integer): время окончания. |

Пример ответа: { "result": 1000, "data": { 677044718:

| {<br>"status": "ready",<br>"time_created": 1641473273000, |
| --- |
| "time_updated": 1641889021000,<br>"transcribes": |
| [<br>{ |
| "channel": "client",<br>"data":<br>[ |
| {<br>"word": "Раз",<br>"begin": 1.94,<br>"end": 2.2 |
| },<br>{<br>"word": "двадцать", |
| "begin": 2.99,<br>"end": 3.33 |
| },<br>{<br>"end": 4.1 |
| },<br>{<br>"word": ".", |
| "begin": 4.1,<br>"end": 4.1<br>}<br>]<br>},<br>{<br>"channel": "operator",<br>"data":<br>[<br>{<br>"word": "Раз",<br>"begin": 7.27,<br>"end": 7.47<br>}, |
| {<br>"word": "двадцать",<br>"begin": 8.62, |
| "end": 8.94<br>},<br>{<br>"word": "три",<br>"begin": 9.61,<br>"end": 9.79<br>},<br>{<br>"word": ".",<br>"begin": 13.2,<br>"end": 13.2<br>}<br>]<br>},<br>{<br>"channel": "operator",<br>"data": |
| [<br>{ |
| "word": "На",<br>"begin": 19.45, |

"end": 19.49 { "word": "раз", "begin": 21.15, "end": 21.37 }, { "word": ".", "begin": 23.43, "end": 23.43 } ] } ] }, "1532496969": [], "4317496830089587018": [] } }
