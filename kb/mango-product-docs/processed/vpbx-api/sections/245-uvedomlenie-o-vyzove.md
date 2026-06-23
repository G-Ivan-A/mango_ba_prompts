---
id: vpbx-api-245-uvedomlenie-o-vyzove
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
title: "Уведомление о вызове"
pdf_heading: "Уведомление о вызове"
pages: "328-329"
source: kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf
source_part: "1"
source_pages: "ч.1: 328-329"
source_refs: '[{"source_pdf":"kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf","part":1,"pages":"328-329","global_pages":"328-329"}]'
extracted_by: "pdfplumber 0.11.10"
token_method: "tiktoken:cl100k_base"
tokens: 513
status: extracted
ai-generated: true
---
# Уведомление о вызове

> Трассировка: PDF §— · сквозные стр. 328-329 · источники: ч.1 `kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf` с.328-329.

Сотрудник ВАТС с внутренним номером "1234" вызывает с номера "74955404444" внешнего абонента с номером "12345678". POST https://external-system.com/events/call vpbx_api_key = qwerty123 sign = qwerty123 json = { "call_id": "100:500:256", "entry_id": "232wc3e3w3s222", "timestamp": "1399906976", "seq": "1", "location": "abonent", "call_state": "Appeared", "from": { "extension": "1234" }, "to": { "number": "12345678" } } Произошло соединение абонентов. POST https://external-system.com/events/call vpbx_api_key = qwerty123 sign = qwerty123 json = { "call_id": "100:500:256", "entry_id": "232wc3e3w3s222", "timestamp": "1399906988", "seq": "2", "location": "abonent", "call_state": "Connected", "from": { "extension": "1234", "number": "74955404444" }, "to": { "number": "12345678" } } Вызов завершен, внешний абонент повесил трубку. POST https://external-system.com/events/call vpbx_api_key = qwerty123 sign = qwerty123 json = { "call_id": "100:500:256", "entry_id": "232wc3e3w3s222", "timestamp": "1399907008", "seq": "3", "location": "abonent", "call_state": "Disconnected", "from": { "extension": "1234", "number": "74955404444" }, "to": { "number": "12345678" }, "disconnect_reason": "1120" }
