---
id: mdialogi-api-43-otpravit-soobschenie-operatora-k-klientu
doc_code: MDIALOGIAPI
doc_title: "Манго Диалоги. Справочник по API"
doc_version: "27.02.2026"
section: "3.4.5"
pdf_section: "3.4.5"
title: "Отправить сообщение оператора к Клиенту"
pdf_heading: "3.4.5 Отправить сообщение оператора к Клиенту"
pages: "45-48"
source: kb/mango-product-docs/sources/mdialogi-api/Manual_API_Mango_Dialogi.pdf
source_part: "1"
source_pages: "ч.1: 45-48"
source_refs: '[{"source_pdf":"kb/mango-product-docs/sources/mdialogi-api/Manual_API_Mango_Dialogi.pdf","part":1,"pages":"45-48","global_pages":"45-48"}]'
extracted_by: "pdfplumber 0.11.10"
token_method: "tiktoken:cl100k_base"
tokens: 1570
status: extracted
ai-generated: true
---
# 3.4.5. Отправить сообщение оператора к Клиенту

> Трассировка: PDF §3.4.5 · сквозные стр. 45-48 · источники: ч.1 `kb/mango-product-docs/sources/mdialogi-api/Manual_API_Mango_Dialogi.pdf` с.45-48.

Метод позволяет отправить Клиенту сообщение от имени оператора. С помощью этого метода, вы можете отправить Клиенту не только текстовое сообщение (длиной не более 10 000 символов), но также и произвольный файл или изображение (размер файла не должен превышать 50 МБ). Важно! Если передается файл используется multipart/form-data Манго Диалоги. Справочник по API | Версия от 27.02.2026 HTTP-запрос: POST https://app.mango-office.ru/cc/md/session/chat/send_message Параметры запроса:

| Параметр |  | Тип | Обяза-<br>тель-<br>ное | Описание |
| --- | --- | --- | --- | --- |
| 1 | 2 |  |  |  |
| id |  | String | Да | Уникальный идентификатор вызова (например,<br>UUID). Формируется внешней системой. Манго<br>Диалоги и ВАТС никак не обрабатывают этот<br>идентификатор, не анализируют и не полагаются на<br>его уникальность |
| chat_id |  | String | Да | Уникальный идентификатор чата.<br>Узнать идентификатор чата вы можете при помощи<br>запроса "Получить список виджетов" или API<br>Realtime |
| abonent_id |  | Integer | Да | Идентификатор сотрудника ВАТС, отправителя<br>сообщения.<br>Узнать список сотрудников ВАТС и их<br>идентификаторы вы можете при помощи API<br>MANGO OFFICE или API Realtime |
| local_messag<br>e_id |  | String | Да | Уникальный локальный идентификатор сообщения.<br>Формируется внешней системой. Манго Диалоги и<br>ВАТС полагаются на уникальность его значения. |
| payload |  | Object | Да | Информация о сообщении |
|  | type | String | Да | Тип сообщения, перечисление. Возможные<br>значения:<br>■ text - текстовое сообщение;<br>■ file - произвольный файл, размер до 50 МБ;<br>■ image – изображение, размер до 50 МБ. |
|  | text | String | Да | Текст сообщение, ограничение 10 000 символов.<br>Обязательный, если параметру type присвоено<br>значение text. |
|  | name | String | Да | Имя файла.<br>Обязательный, если параметру type присвоено<br>значение file или image. |

Манго Диалоги. Справочник по API | Версия от 27.02.2026 Примеры запроса. 1) Если передается текстовое сообщение:

| { |
| --- |
| "id": "fc30", |
| "chat_id": "847b", |
| "abonent_id": 3645, |
| "local_message_id": "1678", |
| "payload": { |
| "type": "text", |
| "text": "Hello world!" |
| } |
| } |

2) Если передается файл используется multipart/form-data:

| Content-Type: multipart/form-data;boundary="1234567890-boundary" |
| --- |
| --1234567890-boundary |
| Content-Disposition: form-data; name="request" |
| Content-Type: application/json |
| { |
| "id": "fc30", |
| "chat_id": "847b", |
| "abonent_id": 3645, |
| "local_message_id": "1678", |
| "payload": { |
| "type": "file", |
| "name": "data.zip" |
| } |
| } |
|  |
| --1234567890-boundary |
| Content-Disposition: form-data; name="file"; filename="data.zip" |
| Content-Type: application/octet-stream |
|  |
| <...........................binary data...........................> |
| --1234567890-boundary-- |

Манго Диалоги. Справочник по API | Версия от 27.02.2026 Параметры ответа:

| Параметры |  | Тип | Обяза-<br>тель-<br>ное | Описание |
| --- | --- | --- | --- | --- |
| 1 | 2 |  |  |  |
| name |  | String | Да | Наименование статуса HTTP |
| status |  | Integer | Да | Код ответа HTTP |
| code |  | Integer | Да | Код результата (список) |
| error |  | String | Нет | Текст ошибки, если она произошла |
| message |  | Array | Нет | Некоторые данные МД о сообщении |
|  | local_message<br>_id | String | Да | Уникальный локальный идентификатор<br>сообщения. Формируется внешней системой.<br>Манго Диалоги и ВАТС полагаются на<br>уникальность его значения. |
|  | message_id | String | Да | Идентификатор сообщения. Формируется МД.<br>Примечание. Рекомендуется сохранять это<br>значение для дальнейшей работы с<br>некоторыми методами API |
|  | time | Integer | Да | Время отправки сообщения в Unix Time |

Пример ответа:

| { "name": "OK", |
| --- |
| "status": 200, |
| "code": 1000, |
| "message": { |
| "local_message_id": "1678", |
| "message_id": "1678", |
| "time": 1678 |
| } |
| } |
