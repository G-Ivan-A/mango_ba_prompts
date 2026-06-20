---
id: mango-cc-manual-228-prilozhenie-5-blokirovka-kontakt-centra
doc_code: CC
doc_title: "Контакт-центр MANGO OFFICE - Руководство пользователя"
doc_version: "1.26.23"
section: "22"
pdf_section: "22"
title: "Приложение 5: Блокировка Контакт-центра"
pdf_heading: "22. Приложение 5: Блокировка Контакт-центра"
pages: "601"
source: kb/mango-product-docs/sources/mango-cc-manual/CC_manual_1.26.23-part-6.pdf
source_part: "6"
source_pages: "ч.6: 96"
source_refs: '[{"source_pdf":"kb/mango-product-docs/sources/mango-cc-manual/CC_manual_1.26.23-part-6.pdf","part":6,"pages":"96","global_pages":"601"}]'
extracted_by: "pdfplumber 0.11.10"
token_method: "tiktoken:cl100k_base"
tokens: 329
status: extracted
ai-generated: true
---
# 22. Приложение 5: Блокировка Контакт-центра

> Трассировка: PDF §22 · сквозные стр. 601 · источники: ч.6 `kb/mango-product-docs/sources/mango-cc-manual/CC_manual_1.26.23-part-6.pdf` с.96.

Для того, чтобы основные и дочерние процессы Контакт-центра MANGO OFFICE не блокировались службами безопасности вашей компании, в диспетчере задач Windows следующие процессы приложения следует добавить в исключения:

![Изображение, стр. 601](../images/228-prilozhenie-5-blokirovka-kontakt-centra-1.png)

• mpoint (корневой) – главное приложение; • mpoint (дочерний) – проигрыватель mp3 записей; • QtWebEngineProcess.exe – браузер для отображения Web-содержимого в клиентском приложении (количество процессов определяется количеством загруженных страниц и их содержимого); • u.mpoint – установщик обновлений (запускается только при автоматическом обновлении).
