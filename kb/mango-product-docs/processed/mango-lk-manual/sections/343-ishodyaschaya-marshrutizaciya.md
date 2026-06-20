---
id: mango-lk-manual-343-ishodyaschaya-marshrutizaciya
doc_code: LK
doc_title: "Виртуальная АТС MANGO OFFICE - Справочник абонента"
doc_version: "1.21"
section: "5.7.1.2"
pdf_section: "5.7.1.2"
title: "Исходящая маршрутизация"
pdf_heading: "5.7.1.2. Исходящая маршрутизация"
pages: "559-562"
source: kb/mango-product-docs/sources/mango-lk-manual/LK_manual_v-121часть-5.pdf
source_part: "5"
source_pages: "ч.5: 155-158"
source_refs: '[{"source_pdf":"kb/mango-product-docs/sources/mango-lk-manual/LK_manual_v-121часть-5.pdf","part":5,"pages":"155-158","global_pages":"559-562"}]'
extracted_by: "pdfplumber 0.11.10"
token_method: "tiktoken:cl100k_base"
tokens: 1012
status: extracted
ai-generated: true
---
# 5.7.1.2. Исходящая маршрутизация

> Трассировка: PDF §5.7.1.2 · сквозные стр. 559-562 · источники: ч.5 `kb/mango-product-docs/sources/mango-lk-manual/LK_manual_v-121часть-5.pdf` с.155-158.

Outbound Routes - исходящая маршрутизация FreePBX. На основании набранного номера выбирается направление (транк) для исходящего вызова. Набираемый номер делится на префикс и паттерн и может модифицироваться после набора. Connectivity > Outbound Routes (Подключения > Исходящая Маршрутизация)

![Изображение, стр. 560](../images/343-ishodyaschaya-marshrutizaciya-1.jpeg)

![Изображение, стр. 560](../images/343-ishodyaschaya-marshrutizaciya-2.png)

![Изображение, стр. 560](../images/343-ishodyaschaya-marshrutizaciya-3.png)

![Изображение, стр. 560](../images/343-ishodyaschaya-marshrutizaciya-4.jpeg)

![Изображение, стр. 561](../images/343-ishodyaschaya-marshrutizaciya-5.png)

![Изображение, стр. 561](../images/343-ishodyaschaya-marshrutizaciya-6.jpeg)

Route name – имя маршрута Trunk Sequence for Matched Routes – выбор транка для данного маршрута Вкладка Dial Pattern Шаблон набора номера (Dial Pattern) – это уникальный набор цифр, который позволяет отправить вызов в нужный SIP–транк. Если шаблон совпадает, то вызов отправляется через SIP–транк в сторону провайдера. Шаблон набора номера имеет 4 поля настройки: Prepend, Prefix, Match Pattern и CallerID. Формат шаблона: (prepend) prefix | [ match pattern / caller ID ], где

![Изображение, стр. 562](../images/343-ishodyaschaya-marshrutizaciya-7.png)

● X - любое целое число от 0 до 9 ● Z - любое целое число от 1 до 9 ● N - любое целое число от 2 до 9 ● [#####] - любое целое число в скобках. Например, перечисление – [1.2.7], или диапазон чисел –[1.2.6-9], в который попадают числа 1,2,6,7,8,9 ● .(точка) -любой набор символов

<!-- изображение на стр. 562: байты не извлечены (PyMuPDF недоступен) -->

Поля, доступные для заполнения: Prepend - данная часть будет добавлена к номеру, перед отправкой в SIP – транк в случае совпадения шаблона. Prefix - префикс – это часть шаблона, которая будет удалена Match Pattern - Набранный номер. ВАЖНО: Asterisk ищет совпадения сопоставляя поле Prefix и Match Pattern. CallerID - данный звонок будет выполнен только в случае, если звонок инициирован с указанного CallerID. В данном поле можно использовать шаблоны. Полезно, если компания имеет несколько офисов с нумерацией виду 1XXX, 2XXX и так далее. Указанный на скриншоте шаблон 795ХХХХХХХ соответствует номерам из 10 цифр начинающимся на 795.
