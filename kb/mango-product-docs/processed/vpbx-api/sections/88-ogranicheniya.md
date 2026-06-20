---
id: vpbx-api-88-ogranicheniya
doc_code: VPBXAPI
doc_title: "API Mango Office"
doc_version: "1.9"
section: "3.7.13.1"
pdf_section: "3.7.13.1"
title: "Ограничения"
pdf_heading: "3.7.13.1 Ограничения"
pages: "127"
source: kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf
source_part: "1"
source_pages: "ч.1: 127"
source_refs: '[{"source_pdf":"kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf","part":1,"pages":"127","global_pages":"127"}]'
extracted_by: "pdfplumber 0.11.10"
token_method: "tiktoken:cl100k_base"
tokens: 314
status: extracted
ai-generated: true
---
# 3.7.13.1. Ограничения

> Трассировка: PDF §3.7.13.1 · сквозные стр. 127 · источники: ч.1 `kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf` с.127.

Необходимо учитывать следующие факторы: - номера сотрудника перезаписываются. Если вы отправили параметр numbers в запросе, то исходные номера будут удалены из карточки сотрудника, а на их место будут записаны новые номера (переданные в параметре numbers); - если удалить номер из карточки сотрудника, то соответствующая sip-учетка будет удалена; - указывать поля line_id и trunk_number_id одновременно нельзя; - чтобы установить "Исходящий номер : Не указан номер - Нет исходящей связи", нужно в поле line_id или trunk_number_id передать пустую строку ("", не null); - нельзя редактировать сотрудников, являющихся чат-ботами.
