---
id: mdialogi-api-29-poluchenie-statusov-otpravlennyh-hsm-soo
doc_code: MDIALOGIAPI
doc_title: "Манго Диалоги. Справочник по API"
doc_version: "27.02.2026"
type: "api_reference"
product: "Mango Dialogi"
platform: ["API"]
language: "ru"
topics: ["API","диалоги","чат-боты","интеграция","REST API"]
section: "3.1.5"
pdf_section: "3.1.5"
title: "Получение статусов отправленных HSM-сообщений"
pdf_heading: "3.1.5 Получение статусов отправленных HSM-сообщений"
pages: "23-25"
source: kb/mango-product-docs/sources/mdialogi-api/Manual_API_Mango_Dialogi.pdf
source_part: "1"
source_pages: "ч.1: 23-25"
source_refs: '[{"source_pdf":"kb/mango-product-docs/sources/mdialogi-api/Manual_API_Mango_Dialogi.pdf","part":1,"pages":"23-25","global_pages":"23-25"}]'
extracted_by: "pdfplumber 0.11.10"
token_method: "tiktoken:cl100k_base"
tokens: 773
status: extracted
ai-generated: true
---
# 3.1.5. Получение статусов отправленных HSM-сообщений

> Трассировка: PDF §3.1.5 · сквозные стр. 23-25 · источники: ч.1 `kb/mango-product-docs/sources/mdialogi-api/Manual_API_Mango_Dialogi.pdf` с.23-25.

Метод позволяет получить статус ранее отправленного HSM-сообщения. HTTP-запрос: POST /cc/get_mcw_message_status Параметры запроса:

| № | Параметры | Тип | Обяза-<br>тель-<br>ный | Описание |
| --- | --- | --- | --- | --- |
| 1 | messageIds | Массив |  | Список сообщений, для которых нужно<br>получить статус |

Примечание. Согласно модели взаимодействия, в POST-запросах отправляются обязательные поля vpbx_api_key и sign. Подробнее об этих обязательных полях… Манго Диалоги. Справочник по API | Версия от 27.02.2026 Пример запроса:

| POST https://app.mango-office.ru/cc/get_mcw_message_status |
| --- |
| vpbx_api_key = 1234567890qwerty, |
| sign = 1234567890qwerty, |
| json = { "messageIds": |
| [ |
| "2135567.007" |
| ] |
| } |

Параметры ответа. Данные возвращаются в теле ответа в формате JSON:

| № | Параметр |  | Тип | Обяза-<br>тель-<br>ный | Описание |
| --- | --- | --- | --- | --- | --- |
|  | 1 | 2 |  |  |  |
| 1 | result |  | Число | Да | Код результата |
| 2 | statuses |  | Массив |  | Статус |
| 3 | result |  | Массив |  | Список объектов |
| 3.1 |  | messageId | Строка |  | id сообщения |
|  |  | status | Строка |  | Статус сообщения. Может иметь значения:<br>□ sended - сообщение принято на<br>доставку;<br>□ delivered - сообщение доставлено;<br>□ read - сообщение прочитано;<br>□ error - возникла ошибка. |
|  |  | time | Вре-<br>менная<br>метка |  | Дата / время события |

Пример ответа:

| { "result": 1000, |
| --- |
| "statuses": { |
| "result": [ |
| { |
| "messageId": "1655452135567.007", |
| "status": "read", |
| "time": "2022-06-17T07:49:38.000Z" |
| } |
| ] } } |

Манго Диалоги. Справочник по API | Версия от 27.02.2026
