---
id: mdialogi-api-27-poluchenie-spiska-hsm-shablonov
doc_code: MDIALOGIAPI
doc_title: "Манго Диалоги. Справочник по API"
doc_version: "27.02.2026"
section: "3.1.3"
pdf_section: "3.1.3"
title: "Получение списка HSM-шаблонов"
pdf_heading: "3.1.3 Получение списка HSM-шаблонов"
pages: "18-21"
source: kb/mango-product-docs/sources/mdialogi-api/Manual_API_Mango_Dialogi.pdf
source_part: "1"
source_pages: "ч.1: 18-21"
source_refs: '[{"source_pdf":"kb/mango-product-docs/sources/mdialogi-api/Manual_API_Mango_Dialogi.pdf","part":1,"pages":"18-21","global_pages":"18-21"}]'
extracted_by: "pdfplumber 0.11.10"
token_method: "tiktoken:cl100k_base"
tokens: 1628
status: extracted
ai-generated: true
---
# 3.1.3. Получение списка HSM-шаблонов

> Трассировка: PDF §3.1.3 · сквозные стр. 18-21 · источники: ч.1 `kb/mango-product-docs/sources/mdialogi-api/Manual_API_Mango_Dialogi.pdf` с.18-21.

Метод позволяет получить список HSM-шаблонов, имеющих статус "APPROVED" и не отправленных в архив. HTTP-запрос: POST /cc/md/hsm/templates Параметры метода:

| № | Пара-<br>метры | Тип | Обяза-<br>тель-<br>ный | Описание |
| --- | --- | --- | --- | --- |
| 1 | id | Строка | Да | Уникальный идентификатор вызова, например UUID,<br>используется для логирования и отладки |
| 2 | channel_id | Целое | Да | Идентификатор канала |

Примечание. Согласно модели взаимодействия, в POST-запросах отправляются обязательные поля vpbx_api_key и sign. Подробнее об этих обязательных полях… Пример запроса:

| POST https://app.mango-office.ru/cc/md/hsm/templates |
| --- |
| vpbx_api_key = 1234567890qwerty, |
| sign = 1234567890qwerty, |
| json = { "id": "qwerty123", |
| "channel_id": 32680 |
| } |

Параметры ответа:

| № | Параметры |  |  |  | Тип | Обяза-<br>тель-<br>ный | Описание |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  | 1 | 2 | 3 | 4 |  |  |  |
| 1 | name |  |  |  | Строка | Да | ID HSM-шаблона |
| 2 | status |  |  |  | Число | Да | id канала с подключенным<br>WA |
| 3 | code |  |  |  | Число | Да | Текст шаблона |
| 4 | error |  |  |  | Строка | Нет | Текст ошибки, если она<br>произошла |

Манго Диалоги. Справочник по API | Версия от 27.02.2026

| 5 | templates |  |  |  | Массив<br>объектов | Да |  |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 5.1 |  | id |  |  | Целое | Да | Идентификатор<br>шаблона |
| 5.2 |  | name |  |  | Строка | Да | Название шаблона |
| 5.3 |  | content |  |  | Объект | Да |  |
|  |  |  | text |  | Строка | Да | Основной текст шаблона |
|  |  |  | buttons |  | Массив<br>объектов | Нет |  |
|  |  |  |  | buttonType | Строка | Нет | Тип кнопки. Возможные<br>значения:<br>- URL: открывает<br>указанную ссылку<br>- PHONE: набирает<br>указанный номер<br>телефона<br>- QUICK_REPLY:<br>отправляет готовый<br>ответ |
|  |  |  |  | text | Строка | Нет | Текст кнопки (для всех<br>типов) |
|  |  |  |  | url | Строка | Нет | Ссылка (для кнопки типа<br>URL) |
|  |  |  |  | phone | Строка | Нет | Номер телефона (для<br>кнопки типа PHONE) |
|  |  |  |  | payload | Строка | Нет | Код кнопки (для кнопки<br>типа QUICK_REPLY) |
|  |  |  | header |  | Объект | Нет |  |
|  |  |  |  | headerType | Строка | Нет | Тип заголовка шаблона.<br>Возможные значения:<br>- TEXT: заголовок-текст<br>- IMAGE: заголовок-<br>изображение<br>- VIDEO: заголовок-<br>видео<br>- DOCUMENT: заголовок-<br>файл |
|  |  |  |  | text | Строка | Да | Обязательное, если<br>headerType == TEXT |
|  |  |  | footer |  | Объект | Нет |  |
|  |  |  |  | text | Строка | Да | Текст подписи шаблона |
| 5.4 |  | category |  |  | Строка | Да | Категория шаблона |

Манго Диалоги. Справочник по API | Версия от 27.02.2026 Пример ответа:

| { |
| --- |
| "name": "OK", |
| "status": 200, |
| "code": 1000, |
| "templates": [{ |
| "id": qwerty123, |
| "name": "example_template", |
| "content": { |
| "text": "Добрый день, {{1}}! Переходи по ссылке для просмотра всех позиций.", |
| "buttons": [{ |
| "text": "Чудо-ссылка", |
| "buttonType": "URL", |
| "url": "https://www.mango-office.ru/shop/devices/1610/" |
| }], |
| "header": null, |
| "footer": null |
| }, |
| "category": "MARKETING" |
| }, { |
| "id": qwerty456, |
| "name": "yet_another_template", |
| "content": { |
| "text": "{{1}}, for more information, please call the phone 108.", |
| "buttons": [], |
| "header": { |
| "headerType": "TEXT", |
| "text": "Very Important Title" |
| }, |
| "footer": "Best regards, A5" |
| }, |
| "category": "UTILITY" |
| }] |
| } |

Манго Диалоги. Справочник по API | Версия от 27.02.2026
