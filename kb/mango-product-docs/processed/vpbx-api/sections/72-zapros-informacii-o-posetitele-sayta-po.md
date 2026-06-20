---
id: vpbx-api-72-zapros-informacii-o-posetitele-sayta-po
doc_code: VPBXAPI
doc_title: "API Mango Office"
doc_version: "1.9"
section: "3.6.1"
pdf_section: "3.6.1"
title: "Запрос информации о посетителе сайта по динамическому номеру"
pdf_heading: "3.6.1 Запрос информации о посетителе сайта по динамическому номеру"
pages: "98-99"
source: kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf
source_part: "1"
source_pages: "ч.1: 98-99"
source_refs: '[{"source_pdf":"kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf","part":1,"pages":"98-99","global_pages":"98-99"}]'
extracted_by: "pdfplumber 0.11.10"
token_method: "tiktoken:cl100k_base"
tokens: 1348
status: extracted
ai-generated: true
---
# 3.6.1. Запрос информации о посетителе сайта по динамическому номеру

> Трассировка: PDF §3.6.1 · сквозные стр. 98-99 · источники: ч.1 `kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf` с.98-99.

POST /vpbx/queries/user_info_by_dct_number По номеру динамического коллтрекинга выдаёт информацию о сессии пользователя, привязанного к номеру. Параметры:

| № | Параметры | Тип | Обяза-<br>тель-<br>ный | Описание |
| --- | --- | --- | --- | --- |
| 1 | number | string | Да | Динамический номер |

Тело запроса должно быть в формате json, например: { "number": "74951112233" } Если привязки к пользователю не обнаружилось, то в ответ вернётся пустой объект. Иначе, в результате обработки запроса, формируются и передаются JSON-данные, содержащие следующие параметры:

| № | Параметры с уровнями<br>вложенности |  | Тип | Обяза-<br>тель-<br>ный | Описание |
| --- | --- | --- | --- | --- | --- |
|  | 1 | 2 |  |  |  |
| 1 | data |  | Object | Да | Объект |
| 2 | uid |  | string | Да | Идентификатор пользователя (уникальная кука из<br>браузера) |

| № | Параметры с уровнями<br>вложенности |  | Тип | Обяза-<br>тель-<br>ный | Описание |
| --- | --- | --- | --- | --- | --- |
|  | 1 | 2 |  |  |  |
| 3 | widget_id |  | Число | Да | Идентификатор виджета динамического коллтрекинга,<br>к которому относится пользователь |
| 4 | widget_name |  | string | Да | Наименование виджета динамического коллтрекинга, к<br>которому относится пользователь |
| 5 | product_id |  | Число | Да | Идентификатор продукта, к которому относится<br>виджет |
| 6 | ga_cid |  | string | Нет | Идентификатор пользователя в Google Analytics |
| 7 | ya_cid |  |  | Нет | Идентификатор пользователя в Яндекс Метрике |
| 8 | rs_cid |  | string | Нет | Идентификатор пользователя в Roistat |
| 9 | ip |  | string | Нет | IP-адрес пользователя |
| 10 | region_id |  | Число | Да | Идентификатор региона из Биллинга, который<br>присвоен пользователю (будут одинаковыми, если в<br>настройках коллтрекинга не включена<br>мультирегиональность) |
| 11 | location |  | Object | Нет | Информация о местоположении пользователя |
| 11.1 |  | type<br>country_code | string | Нет | ISO код страны |
| 11.2 |  | type<br>region_code | string | Нет | Код региона |
| 11.3 |  | type region | string | Нет | Название региона |
| 11.4 |  | type city | string | Нет | Название города |
| 12 | channel |  | Object | Нет | Источник/канал, по которому пользователь пришёл на<br>сайт |
| 12.1 |  | type source | string | Нет | utm source |
| 12.2 |  | type<br>medium | string | Нет | utm medium |
| 12.3 |  | type<br>campaign | string | Нет | utm campaign |
| 12.4 |  | type content | string | Нет | utm content |
| 12.5 |  | type term | string | Нет | utm term |
| 13 | duration |  | Число | Да | Время в секундах с момента захода пользователя на<br>сайт |
| 14 | current_page |  | Object | Да | Текущая страница, на которой находится пользователь |
| 14.1 |  | type url | string | Да | Абсолютный адрес страницы,<br>например, http://example.ru/orders/123?param=1 |
| 14.2 |  | type date | string | Да | Дата и время открытия страницы в формате UTC (по<br>ISO) |
| 14.3 |  | type title | string | Нет | Заголовок страницы |
| 15 | device |  | string | Нет | Устройство посетителя: mobile или desktop |
| 16 | custom |  | string | Нет | Дополнительный параметр от клиента (ограничение по<br>длине 100 символов) |
