---
id: mdialogi-api-42-zakryt-sessiyu
doc_code: MDIALOGIAPI
doc_title: "Манго Диалоги. Справочник по API"
doc_version: "27.02.2026"
section: "3.4.4"
pdf_section: "3.4.4"
title: "Закрыть сессию"
pdf_heading: "3.4.4 Закрыть сессию"
pages: "44-45"
source: kb/mango-product-docs/sources/mdialogi-api/Manual_API_Mango_Dialogi.pdf
source_part: "1"
source_pages: "ч.1: 44-45"
source_refs: '[{"source_pdf":"kb/mango-product-docs/sources/mdialogi-api/Manual_API_Mango_Dialogi.pdf","part":1,"pages":"44-45","global_pages":"44-45"}]'
extracted_by: "pdfplumber 0.11.10"
token_method: "tiktoken:cl100k_base"
tokens: 686
status: extracted
ai-generated: true
---
# 3.4.4. Закрыть сессию

> Трассировка: PDF §3.4.4 · сквозные стр. 44-45 · источники: ч.1 `kb/mango-product-docs/sources/mdialogi-api/Manual_API_Mango_Dialogi.pdf` с.44-45.

Метод позволяет принудительно закрыть сессию в статусе "dialog". Закрыть сессию в статусе "pending" невозможно. HTTP-запрос: POST https://app.mango-office.ru/cc/md/session/close Параметры запроса:

| Параметр | Тип | Обяза-<br>тель-<br>ное | Описание |
| --- | --- | --- | --- |
| id | String | Да | Уникальный идентификатор вызова (например, UUID).<br>Формируется внешней системой. Манго Диалоги и ВАТС<br>никак не обрабатывают этот идентификатор, не анализируют<br>и не полагаются на его уникальность. |
| session_id | String | Да | Идентификатор сессии (этот идентификатор можно получить<br>при помощи запроса "Получить список активных<br>сессий"). |

Манго Диалоги. Справочник по API | Версия от 27.02.2026

| Параметр | Тип | Обяза-<br>тель-<br>ное | Описание |
| --- | --- | --- | --- |
| abonent_id | Integer | Да | Идентификатор сотрудника ВАТС, закрывающего сессию.<br>Узнать список сотрудников ВАТС и их идентификаторы вы<br>можете при помощи API MANGO OFFICE или API Realtime. |

Пример запроса:

| { "id": "fc30", |
| --- |
| "session_id": "3xJn", |
| "abonent_id": 3645 |
| } |

Параметры ответа:

| Параметр | Тип | Обяза-<br>тель-<br>ное | Описание |
| --- | --- | --- | --- |
| name | String | Да | Наименование статуса HTTP |
| status | Integer | Да | Код ответа HTTP |
| code | Integer | Да | Код результата (список) |
| error | String | Нет | Текст ошибки, если она произошла |

Пример ответа:

| { "name": "OK", |
| --- |
| "status": 200, |
| "code": 1000 |
| } |
