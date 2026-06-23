---
id: integration-bitrix24-37-na-chto-vliyaet-eta-nastroyka
doc_code: INTEGRATIONB
doc_title: "Интеграция Виртуальной АТС и Битрикс24. Инструкция по настройке"
doc_version: "03.03.2026"
type: "integration_guide"
product: "Mango Office"
platform: ["Web"]
language: "ru"
topics: ["интеграция","Битрикс24","CRM","ВАТС","настройка","синхронизация"]
section: "0"
pdf_section: "2.3"
title: "На что влияет эта настройка"
pdf_heading: "На что влияет эта настройка"
pages: "39"
source: kb/mango-product-docs/sources/integration-bitrix24/Mango_office_integration_Bitrix24.pdf
source_part: "1"
source_pages: "ч.1: 39"
source_refs: '[{"source_pdf":"kb/mango-product-docs/sources/integration-bitrix24/Mango_office_integration_Bitrix24.pdf","part":1,"pages":"39","global_pages":"39"}]'
extracted_by: "pdfplumber 0.11.10"
token_method: "tiktoken:cl100k_base"
tokens: 319
status: extracted
ai-generated: true
---
# На что влияет эта настройка

> Трассировка: PDF §2.3 · сквозные стр. 39 · источники: ч.1 `kb/mango-product-docs/sources/integration-bitrix24/Mango_office_integration_Bitrix24.pdf` с.39.

- если настройка включена, то при входящем звонке от нового номера, не заведенного в Битрикс24, если автоматически создается новый лид, то ответственным за созданный лид будет сотрудник, который последним обрабатывал входящий звонок. К примеру, поступил звонок от нового Клиента, его принял оператор, который далее перевел на одного из менеджеров. Именно менеджер и будет ответственным за данный лид; - если настройка выключена, то при входящем звонке от нового номера (не заведенного в Битрикс24), если автоматически создается новый лид, то ответственным за созданный лид будет сотрудник, который первым обрабатывал входящий звонок.
