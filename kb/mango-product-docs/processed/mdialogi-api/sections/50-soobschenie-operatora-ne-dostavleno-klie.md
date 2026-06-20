---
id: mdialogi-api-50-soobschenie-operatora-ne-dostavleno-klie
doc_code: MDIALOGIAPI
doc_title: "Манго Диалоги. Справочник по API"
doc_version: "27.02.2026"
section: "3.5.5"
pdf_section: "3.5.5"
title: "Сообщение оператора не доставлено клиенту"
pdf_heading: "3.5.5 Сообщение оператора не доставлено клиенту"
pages: "68-69"
source: kb/mango-product-docs/sources/mdialogi-api/Manual_API_Mango_Dialogi.pdf
source_part: "1"
source_pages: "ч.1: 68-69"
source_refs: '[{"source_pdf":"kb/mango-product-docs/sources/mdialogi-api/Manual_API_Mango_Dialogi.pdf","part":1,"pages":"68-69","global_pages":"68-69"}]'
extracted_by: "pdfplumber 0.11.10"
token_method: "tiktoken:cl100k_base"
tokens: 483
status: extracted
ai-generated: true
---
# 3.5.5. Сообщение оператора не доставлено клиенту

> Трассировка: PDF §3.5.5 · сквозные стр. 68-69 · источники: ч.1 `kb/mango-product-docs/sources/mdialogi-api/Manual_API_Mango_Dialogi.pdf` с.68-69.

Данный вебхук отправляется во внешнюю систему в том случае, если сообщение оператора НЕ доставлено Клиенту. HTTP-запрос: POST https://external-system.ru/events/cc/md/session/on_error_message Параметры вебхука:

| Параметр | Тип | Обяза-<br>тель-<br>ное | Описание |
| --- | --- | --- | --- |
| id | String | Да | Уникальный идентификатор вызова (например, UUID).<br>Формируется внешней системой. Манго Диалоги и<br>ВАТС никак не обрабатывают этот идентификатор, не<br>анализируют и не полагаются на его уникальность. |
| session_id | String | Да | Идентификатор сессии |
| social_user_id | String | Да | Уникальный идентификатор пользователя в соц. сети<br>(Клиента) |
| message_id | String | Да | Идентификатор сообщения в МД |
| error | String | Да | Текст ошибки |

Пример вебхука:

| { |
| --- |
| "id": "fc30", |
| "session_id": "DA0h", |
| "social_user_id": 3645, |
| "message_id": "199a", |
| "error": "error-address-format" |
| } |

Манго Диалоги. Справочник по API | Версия от 27.02.2026
