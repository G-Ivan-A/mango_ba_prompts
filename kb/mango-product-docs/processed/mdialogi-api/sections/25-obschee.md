---
id: mdialogi-api-25-obschee
doc_code: MDIALOGIAPI
doc_title: "Манго Диалоги. Справочник по API"
doc_version: "27.02.2026"
section: "3.1.1"
pdf_section: "3.1.1"
title: "Общее"
pdf_heading: "3.1.1 Общее"
pages: "17"
source: kb/mango-product-docs/sources/mdialogi-api/Manual_API_Mango_Dialogi.pdf
source_part: "1"
source_pages: "ч.1: 17"
source_refs: '[{"source_pdf":"kb/mango-product-docs/sources/mdialogi-api/Manual_API_Mango_Dialogi.pdf","part":1,"pages":"17","global_pages":"17"}]'
extracted_by: "pdfplumber 0.11.10"
token_method: "tiktoken:cl100k_base"
tokens: 357
status: extracted
ai-generated: true
---
# 3.1.1. Общее

> Трассировка: PDF §3.1.1 · сквозные стр. 17 · источники: ч.1 `kb/mango-product-docs/sources/mdialogi-api/Manual_API_Mango_Dialogi.pdf` с.17.

Если к Вашей Виртуальной АТС подключена услуга "WhatsApp Business API (провайдер Edna)", в API Манго Диалоги становится доступна возможность отправлять Клиентам HSM-сообщения через WhatsApp. Примечание. Подробнее о подключении услуги "WhatsApp (провайдер Edna)" вы можете узнать в Справочнике абонента ВАТС. В данном разделе используются следующие термины: HSM - (highly-structured message) шаблонизированное сервисное сообщение, используемое WhatsApp Business API; WA - WhatsApp канал. При помощи данного API, вы можете: - получить список уже созданных HSM-шаблонов; - выдать команду на отправку Клиенту HSM-сообщения; - получить статус отправленного HSM-сообщения. Примечание. Создавать, редактировать и удалять HSM-шаблоны сообщений при помощи данных методов API нельзя.
