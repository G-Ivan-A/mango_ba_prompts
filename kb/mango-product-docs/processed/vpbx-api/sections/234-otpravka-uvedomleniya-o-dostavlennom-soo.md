---
id: vpbx-api-234-otpravka-uvedomleniya-o-dostavlennom-soo
doc_code: VPBXAPI
doc_title: "API Mango Office"
doc_version: "1.9"
section: "4.10.2.4"
pdf_section: "4.10.2.4"
title: "Отправка уведомления о доставленном сообщении"
pdf_heading: "4.10.2.4 Отправка уведомления о доставленном сообщении"
pages: "315-316"
source: kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf
source_part: "1"
source_pages: "ч.1: 315-316"
source_refs: '[{"source_pdf":"kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf","part":1,"pages":"315-316","global_pages":"315-316"}]'
extracted_by: "pdfplumber 0.11.10"
token_method: "tiktoken:cl100k_base"
tokens: 527
status: extracted
ai-generated: true
---
# 4.10.2.4. Отправка уведомления о доставленном сообщении

> Трассировка: PDF §4.10.2.4 · сквозные стр. 315-316 · источники: ч.1 `kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf` с.315-316.

POST /cc/event_message_received Позволяет отправлять уведомления о доставленном сообщении из внешнего приложения в Контакт-центр MANGO OFFICE. Параметры:

| № | Параметр | Тип | Обязательный | Описание |
| --- | --- | --- | --- | --- |
| 1 | channelId | Число | Да | Id текстового канала Манго Диалогов, через<br>который отправится уведомление |
| 2 | userId | Строка | Да | Id клиента на стороне внешней системы |
| 3 | time | Число | Да | Время, когда сообщение было доставлено |
| 4 | serverMessageId | Строка | Да | Id сообщения |

Примечание. Согласно модели взаимодействия, в POST-запросах отправляются обязательные поля vpbx_api_key и sign. Подробнее об этих обязательных полях… Пример запроса: POST https://app.mango-office.ru/cc/event_message_received vpbx_api_key = 1234567890qwerty, sign = 1234567890qwerty, json = { "channelId": 40771, "userId": "KdpikRr7aLbBheMGnFAk", "time": 1690290852274, "serverMessageId": "436829657578282400" } В результате обработки запроса, формируются и передаются JSON-данные, содержащие код ошибки. Примеры ответа. Пример успешного ответа: { "result": 1000 } Пример ответа с ошибкой: { "result": 5000 }
