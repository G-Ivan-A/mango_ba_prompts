---
id: mdialogi-api-56-vozmozhnye-kody-oshibok-api
doc_code: MDIALOGIAPI
doc_title: "Манго Диалоги. Справочник по API"
doc_version: "27.02.2026"
type: "api_reference"
product: "Mango Dialogi"
platform: ["API"]
language: "ru"
topics: ["API","диалоги","чат-боты","интеграция","REST API"]
section: "4.2"
pdf_section: "4.2"
title: "Возможные коды ошибок API"
pdf_heading: "4.2 Возможные коды ошибок API"
pages: "74-76"
source: kb/mango-product-docs/sources/mdialogi-api/Manual_API_Mango_Dialogi.pdf
source_part: "1"
source_pages: "ч.1: 74-76"
source_refs: '[{"source_pdf":"kb/mango-product-docs/sources/mdialogi-api/Manual_API_Mango_Dialogi.pdf","part":1,"pages":"74-76","global_pages":"74-76"}]'
extracted_by: "pdfplumber 0.11.10"
token_method: "tiktoken:cl100k_base"
tokens: 656
status: extracted
ai-generated: true
---
# 4.2. Возможные коды ошибок API

> Трассировка: PDF §4.2 · сквозные стр. 74-76 · источники: ч.1 `kb/mango-product-docs/sources/mdialogi-api/Manual_API_Mango_Dialogi.pdf` с.74-76.

| Код ошибки | Текст ошибки |
| --- | --- |
| Запрос выполнен успешно |  |
| 1000 | Запрос выполнен успешно |
| Ошибка сервера |  |
| 3100 | Ошибка авторизации |
| 5000 | Канал с указанным channel_id не найден! |
|  | Оператор с указанным abonent_id не найден! |
|  | Группа с указанным group_id не найдена! |
|  | Сообщение с указанным message_id не найдено! |
|  | Указанная сессия уже взята в работу |
|  | Данная сессия была завершена |
|  | Данная сессия не существует |
|  | Сессия с указанным chat_id не существует либо не взята в работу |
|  | Сессия с указанным session_id не была взята в работу |
|  | Сессию нельзя взять в работу. Отсутствует ответ клиента WhatsApp |
|  | Для указанного клиента уже было создано обращение через |

Манго Диалоги. Справочник по API | Версия от 27.02.2026

| Код ошибки | Текст ошибки |
| --- | --- |
|  | указанный канал! |
|  | Данный тип канала не поддерживает исходящие сообщения! |
|  | Виджет, к которому относится указанный канал, отключен! |
|  | Указанный канал отключен! |
|  | Чат-бот не может обрабатывать сессию по каналу E-mail. Укажите<br>abonent_id оператора |
|  | [VALIDATION] Оператор с указанным abonent_id не обрабатывает<br>данную сессию |
|  | [VALIDATION] Оператор с указанным abonent_id уже обрабатывает<br>данную сессию |
|  | [VALIDATION] Параметр local_message_id должен иметь уникальное<br>значение |

Манго Диалоги. Справочник по API | Версия от 27.02.2026
