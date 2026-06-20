---
id: mdialogi-api-12-vidy-zaprosov
doc_code: MDIALOGIAPI
doc_title: "Манго Диалоги. Справочник по API"
doc_version: "27.02.2026"
section: "2.3.3"
pdf_section: "2.3.3"
title: "Виды запросов"
pdf_heading: "2.3.3 Виды запросов"
pages: "12-13"
source: kb/mango-product-docs/sources/mdialogi-api/Manual_API_Mango_Dialogi.pdf
source_part: "1"
source_pages: "ч.1: 12-13"
source_refs: '[{"source_pdf":"kb/mango-product-docs/sources/mdialogi-api/Manual_API_Mango_Dialogi.pdf","part":1,"pages":"12-13","global_pages":"12-13"}]'
extracted_by: "pdfplumber 0.11.10"
token_method: "tiktoken:cl100k_base"
tokens: 354
status: extracted
ai-generated: true
---
# 2.3.3. Виды запросов

> Трассировка: PDF §2.3.3 · сквозные стр. 12-13 · источники: ч.1 `kb/mango-product-docs/sources/mdialogi-api/Manual_API_Mango_Dialogi.pdf` с.12-13.

Запросы между системами условимся разделять на асинхронные и синхронные: - Асинхронные запросы, обращаясь к какому-либо методу API, ограничиваются только передачей данных, не требуя и не ожидая данные в ответ. Единственная информация, принимаемая в ответ — код состояния HTTP, т.е. код ответа, информирующий об успешности выполнения самого запроса; - Синхронные запросы, это ожидающие какие-либо данные в теле ответа. Тело ответа должно представлять сплошную json-строку, если не оговорено Манго Диалоги. Справочник по API | Версия от 27.02.2026 иное, например, mp3-файл или csv-файл. Параметры и данные, описывающие json-объект, специфичны и описаны для каждого метода отдельно.
