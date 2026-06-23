---
id: mdialogi-api-49-hsm-soobschenie-operatora-prochitano-kli
doc_code: MDIALOGIAPI
doc_title: "Манго Диалоги. Справочник по API"
doc_version: "27.02.2026"
type: "api_reference"
product: "Mango Dialogi"
platform: ["API"]
language: "ru"
topics: ["API","диалоги","чат-боты","интеграция","REST API"]
section: "3.5.4"
pdf_section: "3.5.4"
title: "HSM-сообщение оператора прочитано клиентом"
pdf_heading: "3.5.4 HSM-сообщение оператора прочитано клиентом"
pages: "67-68"
source: kb/mango-product-docs/sources/mdialogi-api/Manual_API_Mango_Dialogi.pdf
source_part: "1"
source_pages: "ч.1: 67-68"
source_refs: '[{"source_pdf":"kb/mango-product-docs/sources/mdialogi-api/Manual_API_Mango_Dialogi.pdf","part":1,"pages":"67-68","global_pages":"67-68"}]'
extracted_by: "pdfplumber 0.11.10"
token_method: "tiktoken:cl100k_base"
tokens: 571
status: extracted
ai-generated: true
---
# 3.5.4. HSM-сообщение оператора прочитано клиентом

> Трассировка: PDF §3.5.4 · сквозные стр. 67-68 · источники: ч.1 `kb/mango-product-docs/sources/mdialogi-api/Manual_API_Mango_Dialogi.pdf` с.67-68.

В МД существует возможность отправлять Клиентам HSM-сообщения через WhatsApp, при подключении к Виртуальной АТС услуги "WhatsApp Business API (провайдер Edna)". HSM - (highly-structured message) шаблонизированное сервисное сообщение, отправляемое Клиентам через WhatsApp Business. Данный вебхук отправляется во внешнюю систему после того, как из МД было отправлено Клиенту HSM-сообщение и данное сообщение было прочитано Клиентом. HTTP-запрос: POST https://external-system.ru/events/cc/md/session/on_read_message Параметры вебхука:

| Параметр | Тип | Обяза-<br>тель-<br>ное | Описание |
| --- | --- | --- | --- |
| id | String | Да | Уникальный идентификатор вызова (например, UUID).<br>Формируется внешней системой. Манго Диалоги и<br>ВАТС никак не обрабатывают этот идентификатор, не<br>анализируют и не полагаются на его уникальность |
| session_id | String | Да | Идентификатор сессии |
| social_user_id | String | Да | Уникальный идентификатор пользователя в соц. сети<br>(Клиента) |
| message_id | String | Да | Идентификатор сообщения в МД |

Пример вебхука:

| { |
| --- |
| "id": "fc30", |
| "session_id": "DA0h", |
| "social_user_id": 3645, |
| "message_id": "199a" |
| } |

Манго Диалоги. Справочник по API | Версия от 27.02.2026
