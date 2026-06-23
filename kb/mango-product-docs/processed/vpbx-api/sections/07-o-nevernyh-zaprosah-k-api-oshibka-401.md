---
id: vpbx-api-07-o-nevernyh-zaprosah-k-api-oshibka-401
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
section: "1.4.1"
pdf_section: "1.4.1"
title: "О неверных запросах к API. Ошибка 401"
pdf_heading: "1.4.1 О неверных запросах к API. Ошибка 401"
pages: "9"
source: kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf
source_part: "1"
source_pages: "ч.1: 9"
source_refs: '[{"source_pdf":"kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf","part":1,"pages":"9","global_pages":"9"}]'
extracted_by: "pdfplumber 0.11.10"
token_method: "tiktoken:cl100k_base"
tokens: 240
status: extracted
ai-generated: true
---
# 1.4.1. О неверных запросах к API. Ошибка 401

> Трассировка: PDF §1.4.1 · сквозные стр. 9 · источники: ч.1 `kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf` с.9.

Если ваш запрос к API MANGO OFFICE неверный, вы получаете код ошибки 3ХХХ. API MANGO OFFICE позволяет: - 1 неверный запрос в 2 минуты Если количество неверных запросов превышает эту квоту, то вы получаете ошибку 401. Если вы отправили к API MANGO OFFICE больше 1 неверного запроса, ваш доступ к API MANGO OFFICE блокируется до тех пор, пока не пройдет 2 минуты после получения первой ошибки 3ХХХ.
