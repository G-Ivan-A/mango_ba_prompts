---
id: mdialogi-api-51-soobschenie-operatora-dostavleno-klientu
doc_code: MDIALOGIAPI
doc_title: "Манго Диалоги. Справочник по API"
doc_version: "27.02.2026"
type: "api_reference"
product: "Mango Dialogi"
platform: ["API"]
language: "ru"
topics: ["API","диалоги","чат-боты","интеграция","REST API"]
section: "3.5.6"
pdf_section: "3.5.6"
title: "Сообщение оператора доставлено клиенту"
pdf_heading: "3.5.6 Сообщение оператора доставлено клиенту"
pages: "69-70"
source: kb/mango-product-docs/sources/mdialogi-api/Manual_API_Mango_Dialogi.pdf
source_part: "1"
source_pages: "ч.1: 69-70"
source_refs: '[{"source_pdf":"kb/mango-product-docs/sources/mdialogi-api/Manual_API_Mango_Dialogi.pdf","part":1,"pages":"69-70","global_pages":"69-70"}]'
extracted_by: "pdfplumber 0.11.10"
token_method: "tiktoken:cl100k_base"
tokens: 531
status: extracted
ai-generated: true
---
# 3.5.6. Сообщение оператора доставлено клиенту

> Трассировка: PDF §3.5.6 · сквозные стр. 69-70 · источники: ч.1 `kb/mango-product-docs/sources/mdialogi-api/Manual_API_Mango_Dialogi.pdf` с.69-70.

Данный вебхук отправляется во внешнюю систему в том случае, если сообщение оператора доставлено Клиенту. Примечание. Узнать больше о процессе приема и обработки обращений от Клиента вы можете из Примера использования API. HTTP-запрос: POST https://external-system.ru/events/cc/md/session/chat/on_recv_message Параметры вебхука:

| Параметр | Тип | Обяза-<br>тель-<br>ное | Описание |
| --- | --- | --- | --- |
| id | String | Да | Уникальный идентификатор вызова (например, UUID).<br>Формируется внешней системой. Манго Диалоги и ВАТС<br>никак не обрабатывают этот идентификатор, не анализируют<br>и не полагаются на его уникальность. |
| chat_id | String | Да | Идентификатор чата |
| abonent_id | Integer | Да | Идентификатор сотрудника ВАТС, получатель сообщения |
| message_id | String | Да | Идентификатор сообщения в МД.<br>Примечание. Все сообщения c меньшими<br>идентификаторами также считаются полученными |

Пример вебхука:

| { |
| --- |
| "id": "fc30", |
| "chat_id": "847b", |
| "abonent_id": 3645, |
| "message_id": "1678" |
| } |

Манго Диалоги. Справочник по API | Версия от 27.02.2026
