---
id: mdialogi-api-55-vazhnaya-informaciya
doc_code: MDIALOGIAPI
doc_title: "Манго Диалоги. Справочник по API"
doc_version: "27.02.2026"
section: "4.1"
pdf_section: "4.1"
title: "Важная информация"
pdf_heading: "4.1 Важная информация"
pages: "74"
source: kb/mango-product-docs/sources/mdialogi-api/Manual_API_Mango_Dialogi.pdf
source_part: "1"
source_pages: "ч.1: 74"
source_refs: '[{"source_pdf":"kb/mango-product-docs/sources/mdialogi-api/Manual_API_Mango_Dialogi.pdf","part":1,"pages":"74","global_pages":"74"}]'
extracted_by: "pdfplumber 0.11.10"
token_method: "tiktoken:cl100k_base"
tokens: 380
status: extracted
ai-generated: true
---
# 4.1. Важная информация

> Трассировка: PDF §4.1 · сквозные стр. 74 · источники: ч.1 `kb/mango-product-docs/sources/mdialogi-api/Manual_API_Mango_Dialogi.pdf` с.74.

1) Если ваш запрос к API неверный, то вы получите ошибку в коде 3ХХХ. Обратите внимание: API позволяет 1 неверный запрос в 2 минуты Если количество неверных запросов превышает эту квоту, то вы получаете ошибку 401. Если вы отправили к API больше 1 (одного) неверного запроса, ваш доступ к API блокируется до тех пор, пока не пройдет 2 минуты с момента получения первой ошибки в коде 3ХХХ. 2) В API есть лимиты на количество одновременных запросов в секунду. Если вы превысили это ограничение, API выдаст ошибку 429. Примечание. Если получили ошибку 3ХХХ или 401, или 429, сделайте паузу или уменьшите интенсивность передачи запросов, или удалите лишние запросы к API. 3) В случае ошибок HTTP-протокола передаются стандартные ошибки HTTP 4xx или 5xx без дополнительных данных.
