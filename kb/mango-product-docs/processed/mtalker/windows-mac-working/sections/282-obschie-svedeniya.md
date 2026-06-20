---
id: windows-mac-working-282-obschie-svedeniya
doc_code: MTALKER-WORK
doc_title: "Mango Talker для Windows/Mac - Руководство пользователя (Работа)"
doc_version: "23.08.2024"
section: "0"
pdf_section: "17.6"
title: "Общие сведения"
pdf_heading: "Общие сведения"
pages: "111-112"
source: kb/mango-product-docs/sources/mtalker/mTalker_User_Guide_ch1_Working.pdf
source_part: "1"
source_pages: "ч.1: 111-112"
source_refs: '[{"source_pdf":"kb/mango-product-docs/sources/mtalker/mTalker_User_Guide_ch1_Working.pdf","part":1,"pages":"111-112","global_pages":"111-112"}]'
extracted_by: "pdfplumber 0.11.10"
token_method: "tiktoken:cl100k_base"
tokens: 308
status: extracted
ai-generated: true
---
# Общие сведения

> Трассировка: PDF §17.6 · сквозные стр. 111-112 · источники: ч.1 `kb/mango-product-docs/sources/mtalker/mTalker_User_Guide_ch1_Working.pdf` с.111-112.

В MTalker реализована проверка номера перед совершением вызова. Целью этой проверки является, поиск и удаление НЕ цифровых символов в набранном вами номере телефона. Пример работы MTalker при включенной функции проверки номера: на закладке “Телефон” пользователь ввел номер “123а” при помощи клавиатуры, далее нажал кнопку вызов. В результате: • если проверка включена, из введенного номера будет удалена буква а и выполнен вызов номера 123; • иначе, если проверка выключена, будет выполнен вызов номера 123а. Вы можете включить / выключить проверку лишних символов при вводе номера. Mango Talker для сред ОС Windows и Mac. Руководство пользователя | Версия от 23.08.2024
