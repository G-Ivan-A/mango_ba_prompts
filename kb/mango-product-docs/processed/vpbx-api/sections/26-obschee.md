---
id: vpbx-api-26-obschee
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
section: "3.1.1"
pdf_section: "3.1.1"
title: "Общее"
pdf_heading: "3.1.1 Общее"
pages: "16"
source: kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf
source_part: "1"
source_pages: "ч.1: 16"
source_refs: '[{"source_pdf":"kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf","part":1,"pages":"16","global_pages":"16"}]'
extracted_by: "pdfplumber 0.11.10"
token_method: "tiktoken:cl100k_base"
tokens: 275
status: extracted
ai-generated: true
---
# 3.1.1. Общее

> Трассировка: PDF §3.1.1 · сквозные стр. 16 · источники: ч.1 `kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf` с.16.

API Realtime представляет собой набор запросов (уведомлений), которые направляются к внешней системе от внешнего API ВАТС. Часть запросов может предполагать синхронный ответ. Адреса, с которых API отправляет на внешние системы уведомления: - 81.88.80.132 - 81.88.80.133 - 81.88.82.36 - 81.88.82.44 - 81.88.82.45 Для успешного получения уведомлений данным адресам необходимо предоставить доступ к внешней системе, добавить в белый список настроек сетевой безопасности на сетевом оборудовании.
