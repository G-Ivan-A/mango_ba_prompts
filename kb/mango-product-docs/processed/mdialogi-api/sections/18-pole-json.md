---
id: mdialogi-api-18-pole-json
doc_code: MDIALOGIAPI
doc_title: "Манго Диалоги. Справочник по API"
doc_version: "27.02.2026"
section: "0"
pdf_section: "2.3.7"
title: "Поле json"
pdf_heading: "Поле json"
pages: "15"
source: kb/mango-product-docs/sources/mdialogi-api/Manual_API_Mango_Dialogi.pdf
source_part: "1"
source_pages: "ч.1: 15"
source_refs: '[{"source_pdf":"kb/mango-product-docs/sources/mdialogi-api/Manual_API_Mango_Dialogi.pdf","part":1,"pages":"15","global_pages":"15"}]'
extracted_by: "pdfplumber 0.11.10"
token_method: "tiktoken:cl100k_base"
tokens: 286
status: extracted
ai-generated: true
---
# Поле json

> Трассировка: PDF §2.3.7 · сквозные стр. 15 · источники: ч.1 `kb/mango-product-docs/sources/mdialogi-api/Manual_API_Mango_Dialogi.pdf` с.15.

Это поле можно рассматривать как ассоциативный массив любой вложенности и размера (действуют только системные ограничения на размер всего POST- запроса). JSON-строка должна быть корректной, лучше программно- формируемой из ассоциативного массива, без искусственных пробелов и переносов строк. Например:

| json = { |
| --- |
| "id": "123qwerty", |
| "channel_id": 123, |
| "social_user_id": "123ytrewqAns", |
| "message": "Здравствуйте!", |
| "abonent_id": 5555555 |
| } |

Важно! Примеры в данном документе будут форматироваться с добавлением пробелов и переводов строк для лучшей читаемости.
