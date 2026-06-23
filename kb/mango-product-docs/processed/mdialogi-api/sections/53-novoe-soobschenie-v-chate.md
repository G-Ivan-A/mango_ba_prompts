---
id: mdialogi-api-53-novoe-soobschenie-v-chate
doc_code: MDIALOGIAPI
doc_title: "Манго Диалоги. Справочник по API"
doc_version: "27.02.2026"
type: "api_reference"
product: "Mango Dialogi"
platform: ["API"]
language: "ru"
topics: ["API","диалоги","чат-боты","интеграция","REST API"]
section: "3.5.8"
pdf_section: "3.5.8"
title: "Новое сообщение в чате"
pdf_heading: "3.5.8 Новое сообщение в чате"
pages: "71-74"
source: kb/mango-product-docs/sources/mdialogi-api/Manual_API_Mango_Dialogi.pdf
source_part: "1"
source_pages: "ч.1: 71-74"
source_refs: '[{"source_pdf":"kb/mango-product-docs/sources/mdialogi-api/Manual_API_Mango_Dialogi.pdf","part":1,"pages":"71-74","global_pages":"71-74"}]'
extracted_by: "pdfplumber 0.11.10"
token_method: "tiktoken:cl100k_base"
tokens: 1509
status: extracted
ai-generated: true
---
# 3.5.8. Новое сообщение в чате

> Трассировка: PDF §3.5.8 · сквозные стр. 71-74 · источники: ч.1 `kb/mango-product-docs/sources/mdialogi-api/Manual_API_Mango_Dialogi.pdf` с.71-74.

Данный вебхук отправляется во внешнюю систему, когда Клиент либо оператор отправил сообщение. Примечание. Узнать больше о процессе приема и обработки обращений от Клиента вы можете из Примера использования API. HTTP-запрос: POST https://external-system.ru/events/cc/md/session/chat/on_message Параметры вебхука:

| Параметр |  |  | Тип | Обяза-<br>тель-<br>ное | Описание |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | 3 |  |  |  |
| id |  |  | String | Да | Уникальный идентификатор вызова<br>(например, UUID). Формируется внешней<br>системой. Манго Диалоги и ВАТС никак не<br>обрабатывают этот идентификатор, не<br>анализируют и не полагаются на его<br>уникальность. |
| session_id |  |  | String | Да | Идентификатор сессии |
| chat_id |  |  | String | Да | Идентификатор чата |
| message |  |  | Object | Да | Сообщение |
|  | local_mes<br>sage_id |  | String | Да | Уникальный локальный идентификатор<br>сообщения. Формируется внешней<br>системой. Манго Диалоги и ВАТС<br>полагаются на уникальность его значения. |
|  | time |  | integer | Да | Время отправки сообщения, Unix<br>Timestamp в мс |
|  | direction |  | String | Да | направление сообщение, перечисление:<br>■ incoming - от клиента к оператору<br>■ outgoing - от оператора к клиенту |
|  | client_id |  | String | Да | Идентификатор клиента в чате.<br>Отображается, если параметру direction<br>присвоено значение incoming. |
|  | abonent_i<br>d |  | String | Да | Идентификатор сотрудника ВАТС,<br>отправителя сообщений.<br>Отображается, если параметру direction<br>присвоено значение outgoing. |
|  | payload |  | Object | Да | Содержимое (тело) сообщения. Объект, |

Манго Диалоги. Справочник по API | Версия от 27.02.2026

| Параметр |  |  | Тип | Обяза-<br>тель- | Описание |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  | ное | структура которого зависит от типа<br>сообщения (type). |
|  |  | type | String | Да | Тип сообщения, перечисление. Возможные<br>значения:<br>■ text - текстовое сообщение;<br>■ file - произвольный файл;<br>■ image – изображение;<br>■ video - сообщение с видео;<br>■ audio - сообщение с аудио;<br>■ button_click - пользователь<br>соцсети/мессенджера нажал на кнопку. |
|  |  | text | String | Да | Текст сообщения.<br>Отображается, если параметру type<br>присвоено значение text. |
|  |  | name | String | Да | Имя файла.<br>Отображается, если параметру type<br>присвоены значения file, image, video или<br>audio. |
|  |  | link | String | Да | Ссылка на файл.<br>Отображается, если параметру type<br>присвоены значения file, image, video или<br>audio. |
|  |  | file_siz<br>e | integer | Да | Размер файла, байты.<br>Отображается, если параметру type<br>присвоены значения file, image, video или<br>audio. |
|  |  | width | integer | Да | Ширина изображения.<br>Отображается, если параметру type<br>присвоено значение image. |
|  |  | height | integer | Да | Высота изображения.<br>Отображается, если параметру type<br>присвоено значение image. |
|  |  | captio<br>n | String | Да | Текст кнопки.<br>Отображается, если параметру type<br>присвоено значение button_click. |
|  |  | button<br>_id | String | Да | Идентификатор кнопки.<br>Отображается, если параметру type<br>присвоено значение button_click. |

Манго Диалоги. Справочник по API | Версия от 27.02.2026 Пример вебхука:

| { |
| --- |
| "id": "fc30", |
| "chat_id": "847b", |
| "client_id": "9e49", |
| "message": { |
| "message_id": "4336", |
| "local_message_id": "NoRn", |
| "time": 1678107546702, |
| "direction": "incoming", |
| "client_id": "9e49", |
| "payload": { |
| "type": "text", |
| "text": "Вам видны товары в моей корзине?" |
| } |
| } |
| } |

Манго Диалоги. Справочник по API | Версия от 27.02.2026
