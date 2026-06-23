---
id: vpbx-api-251-prilozhenie-1-opisanie-polya-sip-headers
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
title: "Приложение 1 – Описание поля sip-headers"
pdf_heading: "Приложение 1 – Описание поля sip-headers"
pages: "344"
source: kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf
source_part: "1"
source_pages: "ч.1: 344"
source_refs: '[{"source_pdf":"kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf","part":1,"pages":"344","global_pages":"344"}]'
extracted_by: "pdfplumber 0.11.10"
token_method: "tiktoken:cl100k_base"
tokens: 625
status: extracted
ai-generated: true
---
# Приложение 1 – Описание поля sip-headers

> Трассировка: PDF §— · сквозные стр. 344 · источники: ч.1 `kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf` с.344.

Опциональный параметр, содержащий вложенные SIP заголовки и их значения. Принимается как входной параметр некоторыми методами API (при поддержке данного поля указывается в описании метода). При заполнении этих заголовков со стороны внешней системы, ВАТС после прохождения валидации переданных полей заполнит соответствующие заголовки в SIP INVITE переданными значениями. Для каждого метода в API имеется свой набор разрешенных заголовков. При передаче заголовка, который не поддерживается в данном методе либо не прошел валидацию - он будет проигнорирован ВАТС. Для гарантированного прохождения валидации при заполнении каждого параметра значениями нужно руководствоваться рекомендациями соответствующего стандарта RFC. Формальное описание грамматики поля sip_headers:

| sip_headers = { fields }<br>fields = "param":"value"<br>param = "sip_header/sip_header_part" |
| --- |
| sip_header = string token ## Сип заголовок из стандартных<br>заголовков сип<br>sip_header_part = string token ## Изменяемый раздел заголовка<br>из стандартных<br>разделов заголовков сип<br>value = string ## Подставляемое значение |
| string = ALPHA\|DIGIT exclude ";" / "/" / "?" / ":" / "@" / "&" / "=" / "+"<br>/ "$" / "," |

![Изображение, стр. 344](../images/251-prilozhenie-1-opisanie-polya-sip-headers-1.png)

![Изображение, стр. 344](../images/251-prilozhenie-1-opisanie-polya-sip-headers-2.png)

![Изображение, стр. 344](../images/251-prilozhenie-1-opisanie-polya-sip-headers-3.png)

Примеры: "sip_headers": { "From/display-name": "Santa Claus", "Call-Info/answer-after": "0", }
