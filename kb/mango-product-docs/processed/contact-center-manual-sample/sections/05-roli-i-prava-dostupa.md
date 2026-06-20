---
id: contact-center-manual-sample-05-roli-i-prava-dostupa
doc_code: CC
doc_title: "Контакт-центр MANGO OFFICE"
doc_version: "1.26.23-sample"
section: "5"
pdf_section: "5"
title: "Роли и права доступа"
pdf_heading: "5 Роли и права доступа"
pages: "6"
source: kb/mango-product-docs/sources/contact-center-manual-sample/CC_manual_sample.fixture.pdf
source_part: "1"
source_pages: "ч.1: 6"
source_refs: '[{"source_pdf":"kb/mango-product-docs/sources/contact-center-manual-sample/CC_manual_sample.fixture.pdf","part":1,"pages":"6","global_pages":"6"}]'
extracted_by: "pdfplumber 0.11.10"
token_method: "tiktoken:cl100k_base"
tokens: 301
status: extracted
ai-generated: true
---
# 5. Роли и права доступа

> Трассировка: PDF §5 · сквозные стр. 6 · источники: ч.1 `kb/mango-product-docs/sources/contact-center-manual-sample/CC_manual_sample.fixture.pdf` с.6.

Права на модуль «Обращения» и вкладки очереди настраиваются в ЛК ВАТС → Безопасность и ограничения → Настройка доступа. Базовая матрица ролей:

| Роль | Очередь | Распределение | Отчёты | Настройки доступа |
| --- | --- | --- | --- | --- |
| Оператор | Да | Нет | Свои | Нет |
| Супервизор | Да | Частично | Группы | Нет |
| Администратор | Да | Да | Все | Да |
| Руководитель компании | Да | Да | Все | Да |

Настройка автоматического распределения обращений доступна только ролям «Руководитель компании» и «Администратор».
