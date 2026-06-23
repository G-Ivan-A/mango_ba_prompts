---
id: vpbx-api-12-model-avtorizacii
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
section: "2.1"
pdf_section: "2.1"
title: "Модель авторизации"
pdf_heading: "2.1 Модель авторизации"
pages: "11"
source: kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf
source_part: "1"
source_pages: "ч.1: 11"
source_refs: '[{"source_pdf":"kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf","part":1,"pages":"11","global_pages":"11"}]'
extracted_by: "pdfplumber 0.11.10"
token_method: "tiktoken:cl100k_base"
tokens: 301
status: extracted
ai-generated: true
---
# 2.1. Модель авторизации

> Трассировка: PDF §2.1 · сквозные стр. 11 · источники: ч.1 `kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf` с.11.

API предоставляет внешней системе доступ к своим функциям без ограничений. Если внешней системе требуется разграничение доступа на уровне пользователей внешней системы, то это разграничение обеспечивает сама внешняя система. Внешняя система действует от имени сотрудника ВАТС в следующих случаях: инициирование вызова, отправка SMS. Для этого внешняя система указывает идентификатор сотрудника ВАТС или один из его номеров в качестве номера вызывающего абонента. Действие будет выполняться в соответствии с логикой и возможными ограничениями для сотрудника ВАТС.
