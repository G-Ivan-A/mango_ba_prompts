---
id: mango-cc-manual-39-http-zaprosy
doc_code: CC
doc_title: "Контакт-центр MANGO OFFICE - Руководство пользователя"
doc_version: "1.26.23"
section: "2.5.1.3.19"
pdf_section: "2.5.1.3.19"
title: "HTTP Запросы"
pdf_heading: "2.5.1.3.19. HTTP Запросы"
pages: "88-89"
source: kb/mango-product-docs/sources/mango-cc-manual/CC_manual_1.26.23-part-1.pdf
source_part: "1"
source_pages: "ч.1: 88-89"
source_refs: '[{"source_pdf":"kb/mango-product-docs/sources/mango-cc-manual/CC_manual_1.26.23-part-1.pdf","part":1,"pages":"88-89","global_pages":"88-89"}]'
extracted_by: "pdfplumber 0.11.10"
token_method: "tiktoken:cl100k_base"
tokens: 562
status: extracted
ai-generated: true
---
# 2.5.1.3.19. HTTP Запросы

> Трассировка: PDF §2.5.1.3.19 · сквозные стр. 88-89 · источники: ч.1 `kb/mango-product-docs/sources/mango-cc-manual/CC_manual_1.26.23-part-1.pdf` с.88-89.

Функция предназначена для быстрого заполнения внешней базы данных, а также поиска по базе. При внешнем входящем вызове в браузере открывается заданная ссылка.

![Изображение, стр. 89](../images/39-http-zaprosy-1.png)

![Изображение, стр. 89](../images/39-http-zaprosy-2.png)

Последовательность настройки функции пользователем: • проставить галочку в чекбоксе, включающем/выключающем работу функции; • прописать целевой url. Сохраните внесенные изменения кнопкой Сохранить. При входящем вызове в заданном по умолчанию браузере будет открыт URL, содержащий вместо переменных следующие номера телефонов: • {ex_phone} – номер телефона внешнего абонента, совершающего вызов; • {in_phone} – внутренний номер пользователя, на который поступает вызов; • {context_id} – уникальный идентификатор звонка; • {call_id_a} – уникальный идентификатор первого плеча звонка ; • {call_id_b}- уникальный идентификатор второго плеча звонка; • {switch_id} – уникальный идентификатор коммутатора, обработавшего звонок.

| Примеры заполнения пользователем поля URL |
| --- |
| http://консалтинг.рф/?ключ1={ex_phone}&ключ2={in_phone} |
| https://investproekt.ru/contact/?ключ1={ex_phone}&ключ2={in_phone} |
