---
id: mdialogi-api-21-elektronnaya-podpis-sign
doc_code: MDIALOGIAPI
doc_title: "Манго Диалоги. Справочник по API"
doc_version: "27.02.2026"
section: "0"
pdf_section: "2.3.7"
title: "Электронная подпись (sign)"
pdf_heading: "Электронная подпись (sign)"
pages: "16"
source: kb/mango-product-docs/sources/mdialogi-api/Manual_API_Mango_Dialogi.pdf
source_part: "1"
source_pages: "ч.1: 16"
source_refs: '[{"source_pdf":"kb/mango-product-docs/sources/mdialogi-api/Manual_API_Mango_Dialogi.pdf","part":1,"pages":"16","global_pages":"16"}]'
extracted_by: "pdfplumber 0.11.10"
token_method: "tiktoken:cl100k_base"
tokens: 231
status: extracted
ai-generated: true
---
# Электронная подпись (sign)

> Трассировка: PDF §2.3.7 · сквозные стр. 16 · источники: ч.1 `kb/mango-product-docs/sources/mdialogi-api/Manual_API_Mango_Dialogi.pdf` с.16.

Значение sign рассчитывается следующим образом: sign = sha256(vpbx_api_key + json + vpbx_api_salt) Электронная подпись (sign) должна быть корректной, лучше программно- формируемой по формуле, описанной выше. Однако, при необходимости, вы можете воспользоваться SHA256 генератором MANGO OFFICE для генерации электронной подписи (sign). Важно! Подписываются все запросы — как от внешней системы, так и уведомления от API.
