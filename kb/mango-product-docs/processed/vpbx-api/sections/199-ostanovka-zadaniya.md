---
id: vpbx-api-199-ostanovka-zadaniya
doc_code: VPBXAPI
doc_title: "API Mango Office"
doc_version: "1.9"
section: "4.6.15"
pdf_section: "4.6.15"
title: "Остановка задания"
pdf_heading: "4.6.15 Остановка задания"
pages: "280"
source: kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf
source_part: "1"
source_pages: "ч.1: 280"
source_refs: '[{"source_pdf":"kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf","part":1,"pages":"280","global_pages":"280"}]'
extracted_by: "pdfplumber 0.11.10"
token_method: "tiktoken:cl100k_base"
tokens: 394
status: extracted
ai-generated: true
---
# 4.6.15. Остановка задания

> Трассировка: PDF §4.6.15 · сквозные стр. 280 · источники: ч.1 `kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf` с.280.

POST /vpbx/task/stop Метод позволяет остановить задание кампании ИО. Параметры запроса:

| № | Параметр | Тип | Обязательный | Описание |
| --- | --- | --- | --- | --- |
| 1 | campaign_id | Число | Да | ID кампании |
| 2 | task_id | Число | Да | ID задания кампании |

Пример запроса: POST https://app.mango-office.ru/vpbx/task/stop vpbx_api_key = 1234567890qwerty, sign = 1234567890qwerty, json = { "campaign_id": 56919, "task_id": 11227830 } В результате обработки запроса, формируются и передаются JSON-данные, содержащие следующие параметры:

| № | Параметр | Тип | Обязательный | Описание |
| --- | --- | --- | --- | --- |
| 1 | result | Число | Да | Код результата |

Пример ответа:

![Изображение, стр. 280](../images/199-ostanovka-zadaniya-1.png)

![Изображение, стр. 280](../images/199-ostanovka-zadaniya-2.png)

{ "result": 1000 }
