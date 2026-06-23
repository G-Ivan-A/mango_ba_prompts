---
id: vpbx-api-01-opredeleniya-i-sokrascheniya
doc_code: VPBXAPI
doc_title: "API Mango Office"
doc_version: "1.9"
type: "api_reference"
product: "Mango VPBX"
platform: ["API"]
language: "ru"
topics: ["API","VPBX","интеграция","телефония","REST API","разработка"]
aliases: ["API VPBX","VPBX API","API ВАТС","API виртуальной АТС","Open API Mango Office"]
mango_taxonomy_primary_cluster: "vats-core"
mango_taxonomy_secondary_clusters: ["contact-center-core","platform-integrations"]
mango_taxonomy_product_refs: ["mango-virtual-pbx-official","mango-contact-center-official"]
mango_taxonomy_evidence_refs: ["kb/mango-taxonomy/registry.json","standards/mango-taxonomy-standard.md","kb/mango-product-docs/processed/vpbx-api/index.md"]
section: "0"
pdf_section: "—"
title: "Определения и сокращения"
pdf_heading: "Определения и сокращения"
pages: "7"
source: kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf
source_part: "1"
source_pages: "ч.1: 7"
source_refs: '[{"source_pdf":"kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf","part":1,"pages":"7","global_pages":"7"}]'
extracted_by: "pdfplumber 0.11.10"
token_method: "tiktoken:cl100k_base"
tokens: 562
status: extracted
ai-generated: true
---
# Определения и сокращения

> Трассировка: PDF §— · сквозные стр. 7 · источники: ч.1 `kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf` с.7.

АК — адресная книга MANGO OFFICE, используется в Контакт-центр, M.TALKER. ВАТС (Виртуальная АТС) - программно-аппаратный комплекс MANGO OFFICE для обслуживания клиентов, предоставляющий возможности телефонии и управления ими. Внешняя система - любое приложение, CRM-система, облачный сервис и пр., имеющий публичный WEB-интерфейс, и реализующий протокол взаимодействия с ВАТС, описанный ниже, в полном объеме либо некоторую, достаточную для ее нужд, часть. Идентификатор сотрудника ВАТС — соответствует внутреннему (короткому) номеру сотрудника ВАТС, который устанавливается в Личном кабинете. Также служит для идентификации сотрудника внешней системой. ИО — исходящий обзвон. Сервис "Контакт-центр". КЦ - Контакт-центр MANGO OFFICE Личный кабинет — WEB-интерфейс управления ВАТС и настройки параметров API с помощью браузера. Доступен клиентам MANGO OFFICE по адресу: https://lk.mango-office.ru Номер абонента — цифровой номер ТфОП, SIP-ID, внутренний номер сотрудника ВАТС. Сотрудник ВАТС — абонент, имеющий учетную запись в ВАТС, которая, в частности, содержит список контактных номеров, а также внутренний номер.
