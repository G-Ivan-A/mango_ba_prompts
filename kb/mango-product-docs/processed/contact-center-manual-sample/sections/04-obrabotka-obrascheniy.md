---
id: contact-center-manual-sample-04-obrabotka-obrascheniy
doc_code: CC
doc_title: "Контакт-центр MANGO OFFICE"
doc_version: "1.26.23-sample"
section: "4"
pdf_section: "4"
title: "Обработка обращений"
pdf_heading: "4 Обработка обращений"
pages: "5"
source: kb/mango-product-docs/sources/contact-center-manual-sample/CC_manual_sample.fixture.pdf
source_part: "1"
source_pages: "ч.1: 5"
source_refs: '[{"source_pdf":"kb/mango-product-docs/sources/contact-center-manual-sample/CC_manual_sample.fixture.pdf","part":1,"pages":"5","global_pages":"5"}]'
extracted_by: "pdfplumber 0.11.10"
token_method: "tiktoken:cl100k_base"
tokens: 426
status: extracted
ai-generated: true
---
# 4. Обработка обращений

> Трассировка: PDF §4 · сквозные стр. 5 · источники: ч.1 `kb/mango-product-docs/sources/contact-center-manual-sample/CC_manual_sample.fixture.pdf` с.5.

## 4.1 Контроль обращений

Контроль ведётся в разрезе вызовов и текстовых обращений на панели очереди.

## 4.2 Правила распределения

Задаётся максимальное количество текстовых обращений, которые может обрабатывать один сотрудник. При достижении показателя обращения не распределяются на сотрудника, пока он не закроет одно из текущих. Если указан 0 — обращения распределяются всегда. Доступны алгоритмы «на наименее загруженного оператора» и «равномерное распределение». Чекбокс «Не распределять текстовые обращения на операторов, которые находятся в звонке» — единственная сегодня кросс-канальная связь между голосом и текстом. Сквозного межканального счётчика и приоритета каналов нет.

![Изображение, стр. 5](../images/04-obrabotka-obrascheniy-1.png)

## 4.3 Каналы обращений

Перечень подключённых каналов и их настройки задаются в Личном кабинете ВАТС.
