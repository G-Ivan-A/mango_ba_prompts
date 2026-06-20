---
id: mdialogi-api-52-soobschenie-operatora-prochitano-kliento
doc_code: MDIALOGIAPI
doc_title: "Манго Диалоги. Справочник по API"
doc_version: "27.02.2026"
section: "3.5.7"
pdf_section: "3.5.7"
title: "Сообщение оператора прочитано клиентом"
pdf_heading: "3.5.7 Сообщение оператора прочитано клиентом"
pages: "70-71"
source: kb/mango-product-docs/sources/mdialogi-api/Manual_API_Mango_Dialogi.pdf
source_part: "1"
source_pages: "ч.1: 70-71"
source_refs: '[{"source_pdf":"kb/mango-product-docs/sources/mdialogi-api/Manual_API_Mango_Dialogi.pdf","part":1,"pages":"70-71","global_pages":"70-71"}]'
extracted_by: "pdfplumber 0.11.10"
token_method: "tiktoken:cl100k_base"
tokens: 534
status: extracted
ai-generated: true
---
# 3.5.7. Сообщение оператора прочитано клиентом

> Трассировка: PDF §3.5.7 · сквозные стр. 70-71 · источники: ч.1 `kb/mango-product-docs/sources/mdialogi-api/Manual_API_Mango_Dialogi.pdf` с.70-71.

Данный вебхук отправляется во внешнюю систему в том случае, если сообщение оператора прочитано Клиентом. Примечание. Узнать больше о процессе приема и обработки обращений от Клиента вы можете из Примера использования API. HTTP-запрос: POST https://external-system.ru/events/cc/md/session/chat/on_read_message Параметры вебхука:

| Параметр | Тип | Обяза-<br>тель-<br>ное | Описание |
| --- | --- | --- | --- |
| id | String | Да | Уникальный идентификатор вызова (например, UUID).<br>Формируется внешней системой. Манго Диалоги и ВАТС никак<br>не обрабатывают этот идентификатор, не анализируют и не<br>полагаются на его уникальность. |
| chat_id | String | Да | Идентификатор чата |
| abonent_id | Integer | Да | Идентификатор сотрудника ВАТС, получатель сообщения |
| message_id | String | Да | Идентификатор сообщения в МД.<br>Примечание. Все сообщения c меньшими идентификаторами<br>также считаются прочитанными. |

Пример вебхука:

| { |
| --- |
| "id": "fc30", |
| "chat_id": "847b", |
| "client_id": "9e49", |
| "message_id": "1678" |
| } |

Манго Диалоги. Справочник по API | Версия от 27.02.2026
