---
id: vpbx-api-140-dlya-grupp
doc_code: VPBXAPI
doc_title: "API Mango Office"
doc_version: "1.9"
section: "3.9.4.3"
pdf_section: "3.9.4.3"
title: "Для групп"
pdf_heading: "3.9.4.3 Для групп"
pages: "192-194"
source: kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf
source_part: "1"
source_pages: "ч.1: 192-194"
source_refs: '[{"source_pdf":"kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf","part":1,"pages":"192-194","global_pages":"192-194"}]'
extracted_by: "pdfplumber 0.11.10"
token_method: "tiktoken:cl100k_base"
tokens: 906
status: extracted
ai-generated: true
---
# 3.9.4.3. Для групп

> Трассировка: PDF §3.9.4.3 · сквозные стр. 192-194 · источники: ч.1 `kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf` с.192-194.

Параметры:

| № | Параметры | Тип | Обяза- | Описание |
| --- | --- | --- | --- | --- |

|  | 1 | 2 |  | тель-<br>ный |  |
| --- | --- | --- | --- | --- | --- |
| 1 | action |  |  | Да | Название события |
| 2 | data |  |  | Да | Массив – группа |
|  |  | group_id | string | Нет | Идентификатор группы в БД |
|  |  | group_name | string | Нет | Название группы |

Событие о добавлении группы Параметры события:

| № | Параметры | Тип | Обяза-<br>тель-<br>ный | Описание |
| --- | --- | --- | --- | --- |
| 1 | action |  | Да | Название события = new |
| 2 | data |  | Да | Массив групп. В массиве объектов может быть один либо несколько<br>групп, принадлежащих одному источнику |

Пример события: POST https://external-system.com/events/ab/contacts vpbx_api_key = 1234567890qwerty, sign = 1234567890qwerty, json = { "action": "new", "data": [ { "contact_id": "43851054", "type": 0, "name": "dfgdfgdfgdfg", "office": "dgdfgdfg", "site": null, "org": { "org_id": "14642887", "org_name": "dfgdfgdfg" }, "importance": null, "comment": "dfgdfgdfg", "birthday": null, "sex": null, "avatar": "", "manager_id": null, "url": null, "phones": [], "emails": [], "groups": [], "nets": [], "messengers": [], "in_favorites": [], "custom_values": [ { "custom_value_id": 28494, "custom_field_id": 5453, "type": 1, "text": ""новое значение аш"" }, { "custom_value_id": 28248, "custom_field_id": 5443, "type": 1, "text": "" }, "when_created": 1574415396, "last_used": null, "last_call": null } ] } Событие об изменении группы Параметры события:

| № | Параметры | Тип | Обяза-<br>тель-<br>ный | Описание |
| --- | --- | --- | --- | --- |
| 1 | action |  | Да | Название события = updated |
| 2 | data |  | Да | Массив групп. В массиве объектов может быть одна либо несколько<br>групп, принадлежащих одному источнику |

Событие об удалении группы Параметры события:

| № | Параметры | Тип | Обяза-<br>тель-<br>ный | Описание |
| --- | --- | --- | --- | --- |
| 1 | action |  | Да | Название события = deleted |
| 2 | data |  | Да | Массив id групп. В массиве объектов может быть одна либо несколько id<br>групп, принадлежащих одному источнику |
