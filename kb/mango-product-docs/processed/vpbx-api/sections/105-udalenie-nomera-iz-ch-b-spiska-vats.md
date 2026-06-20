---
id: vpbx-api-105-udalenie-nomera-iz-ch-b-spiska-vats
doc_code: VPBXAPI
doc_title: "API Mango Office"
doc_version: "1.9"
section: "3.8.2.4"
pdf_section: "3.8.2.4"
title: "Удаление номера из ч/б списка ВАТС"
pdf_heading: "3.8.2.4 Удаление номера из ч/б списка ВАТС"
pages: "143"
source: kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf
source_part: "1"
source_pages: "ч.1: 143"
source_refs: '[{"source_pdf":"kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf","part":1,"pages":"143","global_pages":"143"}]'
extracted_by: "pdfplumber 0.11.10"
token_method: "tiktoken:cl100k_base"
tokens: 435
status: extracted
ai-generated: true
---
# 3.8.2.4. Удаление номера из ч/б списка ВАТС

> Трассировка: PDF §3.8.2.4 · сквозные стр. 143 · источники: ч.1 `kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf` с.143.

POST /vpbx/bwlists/number/delete/ Метод позволяет удалить номер из ч/б списка Виртуальной АТС. Параметры запроса:

| № | Параметры | Тип | Обяза-<br>тель-<br>ный | Описание |
| --- | --- | --- | --- | --- |
| 1 | number_id |  |  | id номера, см. Получить список номеров в ч/б списке. |

Пример запроса: POST https://app.mango-office.ru/vpbx/bwlists/number/delete/ vpbx_api_key = 1234567890qwerty, sign = 1234567890qwerty, json = { "number_id":"10088582" } В результате обработки запроса, формируются и передаются JSON-данные, содержащий код результата:

| № | Параметры | Тип | Обяза-<br>тель-<br>ный | Описание |
| --- | --- | --- | --- | --- |
| 1 | Result |  | Да | Код результата:<br>● 1000 - удачное выполнение;<br>● 3100 - переданы неверные параметры команды;<br>● 31XX - неверные параметры;<br>● 3300 - объект не существует;<br>● 5XXX – ошибка сервера. |

Пример ответа: { "result": 1000 }
