---
id: vpbx-api-68-poluchenie-spiska-rasshifrovok-raspoznan
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
section: "3.5.5"
pdf_section: "3.5.5"
title: "Получение списка расшифровок распознанных разговоров"
pdf_heading: "3.5.5 Получение списка расшифровок распознанных разговоров"
pages: "93-95"
source: kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf
source_part: "1"
source_pages: "ч.1: 93-95"
source_refs: '[{"source_pdf":"kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf","part":1,"pages":"93-95","global_pages":"93-95"}]'
extracted_by: "pdfplumber 0.11.10"
token_method: "tiktoken:cl100k_base"
tokens: 961
status: extracted
ai-generated: true
---
# 3.5.5. Получение списка расшифровок распознанных разговоров

> Трассировка: PDF §3.5.5 · сквозные стр. 93-95 · источники: ч.1 `kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf` с.93-95.

POST /vpbx/queries/recording_transcripts Метод позволяет получить результаты распознавания речи в виде массива текстовых данных. Параметры:

| № | Параметры | Тип | Обяза-<br>тель-<br>ный | Описание |
| --- | --- | --- | --- | --- |
| 1 | recording_id |  |  | Массив идентификаторов записи разговора (не более 500) |

Пример запроса: POST https://app.mango-office.ru/vpbx/queries/recording_transcripts vpbx_api_key = 1234567890qwerty, sign = 1234567890qwerty. json = { "recording_id":"[\"MToxMDAwNzM4ODo1MDA5NzI0NjE3OjA=\"]" } В результате обработки запроса ВАТС возвращает JSON-данные, содержащие список расшифровок. Эти JSON-данные содержат следующие параметры:

| № | Параметры с<br>уровнями<br>вложенности |  | Тип | Обяза-<br>тель-<br>ный | Описание |
| --- | --- | --- | --- | --- | --- |
|  | 1 | 2 |  |  |  |
| 1 | result |  |  |  | Код результата |
| 2 | data |  |  |  | Массив данных с результатами расшифровок разговоров |
|  |  | recording_id |  |  | Идентификатор записи разговора |
|  |  | names |  |  | Имя/номер телефона участников разговора |
|  |  | phrases |  |  | Список фраз по очереди |

Примечание. Правила установки значений client и operator: □ если оба параметра известны (vpbx.from_member_id > 0 и vpbx.to_member_id > 0): client - имя сотрудника (или "Канал 1", если имя не найдено); operator - имя сотрудника (или "Канал 2", если имя не найдено); □ если оба параметра неизвестны (vpbx.from_member_id > 0 и vpbx.to_member_id > 0): client - "Канал 1"; operator - "Канал 2"; □ для остальных случаев: client - "Клиент"; operator - "Сотрудник". Пример ответа: { "result": 1000, "data": [ { "recording_id": "MToxMDAwNzM4ODo1MDA5NzI0NjE3OjA=", "names": { "client": "Клиент", "operator": "Микросип_хост" }, "phrases": [ [ "operator", "здравствуйте вас приветствует компания Манго Телеком"

![Изображение, стр. 95](../images/68-poluchenie-spiska-rasshifrovok-raspoznan-1.png)

| ],<br>[<br>"client", |
| --- |
| "спасибо до свидания"<br>] |
| ] } ]} |

![Изображение, стр. 95](../images/68-poluchenie-spiska-rasshifrovok-raspoznan-2.png)

![Изображение, стр. 95](../images/68-poluchenie-spiska-rasshifrovok-raspoznan-3.png)
