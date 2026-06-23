---
id: mdialogi-api-28-otpravlenie-hsm
doc_code: MDIALOGIAPI
doc_title: "Манго Диалоги. Справочник по API"
doc_version: "27.02.2026"
type: "api_reference"
product: "Mango Dialogi"
platform: ["API"]
language: "ru"
topics: ["API","диалоги","чат-боты","интеграция","REST API"]
section: "3.1.4"
pdf_section: "3.1.4"
title: "Отправление HSM"
pdf_heading: "3.1.4 Отправление HSM"
pages: "21-23"
source: kb/mango-product-docs/sources/mdialogi-api/Manual_API_Mango_Dialogi.pdf
source_part: "1"
source_pages: "ч.1: 21-23"
source_refs: '[{"source_pdf":"kb/mango-product-docs/sources/mdialogi-api/Manual_API_Mango_Dialogi.pdf","part":1,"pages":"21-23","global_pages":"21-23"}]'
extracted_by: "pdfplumber 0.11.10"
token_method: "tiktoken:cl100k_base"
tokens: 1378
status: extracted
ai-generated: true
---
# 3.1.4. Отправление HSM

> Трассировка: PDF §3.1.4 · сквозные стр. 21-23 · источники: ч.1 `kb/mango-product-docs/sources/mdialogi-api/Manual_API_Mango_Dialogi.pdf` с.21-23.

Метод позволяет отправить Клиенту сообщение в соответствии с тем или иным уже созданным HSM-шаблоном (HSM-сообщение). HTTP-запрос: POST /cc/md/hsm/send_message Параметры запроса:

| № | Параметр |  |  | Тип | Обяза-<br>тель-<br>ный | Описание |
| --- | --- | --- | --- | --- | --- | --- |
|  | 1 | 2 | 3 |  |  |  |
| 1 | id |  |  | Строка | Да | Уникальный идентификатор<br>вызова, например UUID,<br>используется для логирования и<br>отладки |
| 2 | social_user_i<br>d |  |  | Строка | Да | Номер телефона в WhatsApp |
| 3 | channel_id |  |  | Целое | Да | Идентификатор канала |
| 4 | template_id |  |  | Целое | Да | Идентификатор шаблона,<br>используемого при<br>формировании HSM |
| 5 | creator_abo<br>nent_id |  |  | Целое | Да | Идентификатор сотрудника<br>MANGO OFFICE, отправитель<br>сообщения |
| 6 | parameters |  |  | Объект | Да | динамические данные HSM |
| 6.1 |  | bindings |  | Массив<br>строк | Да | Переменные основного текста<br>шаблона |
| 6.2 |  | header |  | Объект | Нет | Данные заголовка |
|  |  |  | Content | Строка | Нет | Ссылка на файл для заголовка |
|  |  |  | bindings | Массив<br>строк | Нет | Переменные текста заголовка<br>шаблона |

Примечание. Согласно модели взаимодействия, в POST-запросах отправляются обязательные поля vpbx_api_key и sign. Подробнее об этих обязательных полях… Манго Диалоги. Справочник по API | Версия от 27.02.2026 Пример запроса:

| POST https://app.mango-office.ru/cc/send_hsm |
| --- |
| { |
| "vpbx_api_key": "qwerty123", |
| "sign": "qwerty123", |
| "json": { |
| "id": "qwerty123", |
| "social_user_id": "74955404444", |
| "channel_id": 11111, |
| "template_id": 22222, |
| "creator_abonent_id": 33333, |
| "parameters": { |
| "bindings": ["Иванов Иван"], |
| "header": { |
| "content": "https://image.png", |
| "bindings": ["Иванов Иван"] |
| } |
| } |
| } |

Параметры ответа:

| № | Параметры |  | Тип | Обя-<br>зате-<br>льный | Описание |
| --- | --- | --- | --- | --- | --- |
|  | 1 | 2 |  |  |  |
| 1 | name |  | Строка | Да | Наименование статуса HTTP |
| 2 | status |  | Целое | Да | Статус HTTP |
| 3 | code |  | Целое | Да | Код результата |
| 4 | error |  | Строка | Нет | Текст ошибки, если она произошла |
| 5 | message |  | Объект | Да | Некоторые данные о сообщении<br>на сервере |
| 5.1 |  | local_messa<br>ge_id | Строка | Да | Локальный идентификатор<br>отправляемого сообщения. |
| 5.2 |  | message_id | Строка | Да | Идентификатор сообщения на<br>сервере |
| 5.3 |  | time | Целое | Да | Время отправки сообщения в Unix<br>Time в миллисекундах |
| 5.4 |  | session_id | Строка |  | Идентификатор сессии |

Манго Диалоги. Справочник по API | Версия от 27.02.2026 Пример успешного ответа:

| { |
| --- |
| "name": "OK", |
| "status": 200, |
| "code": 1000, |
| "message": { |
| "local_message_id": "92f7cc123000ecadfe6f0f680972098e", |
| "message_id": "449026466343509280", |
| "time": 1738009633316, |
| "session_id": "mFv5u7SUXl6N+FE/pOsAIMd+" |
| } |
| } |

Пример неуспешного ответа:

| { "result": 3000, |
| --- |
| "error": "error-address-format" |
| } |
