---
id: vpbx-api-100-obschee
doc_code: VPBXAPI
doc_title: "API Mango Office"
doc_version: "1.9"
section: "3.8.1"
pdf_section: "3.8.1"
title: "Общее"
pdf_heading: "3.8.1 Общее"
pages: "139"
source: kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf
source_part: "1"
source_pages: "ч.1: 139"
source_refs: '[{"source_pdf":"kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf","part":1,"pages":"139","global_pages":"139"}]'
extracted_by: "pdfplumber 0.11.10"
token_method: "tiktoken:cl100k_base"
tokens: 365
status: extracted
ai-generated: true
---
# 3.8.1. Общее

> Трассировка: PDF §3.8.1 · сквозные стр. 139 · источники: ч.1 `kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf` с.139.

При помощи данных методов API вы можете ограничить прием и совершение вызовов через вашу ВАТС, то есть контролировать совершение и прием звонков с нужных вам номеров. При помощи этих методов вы можете создавать "черные" списки номеров отдельно как для входящих, так и для исходящих коммуникаций. Кроме этого, вы можете составить отдельный "черный" список номеров для исходящих коммуникаций в рамках кампании исходящего обзвона. Как это работает: если номер внесен в черный список кампаний ИО, то этот номер не будет добавлен в новую кампанию ИО, а также будет удален из всех списков обзвона ранее созданных кампаний ИО. Примечание. Для работы с данными методами в вашей Виртуальной АТС должна быть подключена услуга "Черный список и белый список".
