---
id: vpbx-api-237-obschie-parametry-dlya-kazhdogo-sobytiya
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
section: "4.10.3.1"
pdf_section: "4.10.3.1"
title: "Общие параметры для каждого события"
pdf_heading: "4.10.3.1 Общие параметры для каждого события"
pages: "318"
source: kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf
source_part: "1"
source_pages: "ч.1: 318"
source_refs: '[{"source_pdf":"kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf","part":1,"pages":"318","global_pages":"318"}]'
extracted_by: "pdfplumber 0.11.10"
token_method: "tiktoken:cl100k_base"
tokens: 239
status: extracted
ai-generated: true
---
# 4.10.3.1. Общие параметры для каждого события

> Трассировка: PDF §4.10.3.1 · сквозные стр. 318 · источники: ч.1 `kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf` с.318.

Перечень общих параметров события:

| № | Параметры с уровнями<br>вложенности |  | Тип | Описание |
| --- | --- | --- | --- | --- |
|  | 1 | 2 |  |  |
| 1 | point_id |  | Число |  |
| 2 | path |  | Строка |  |
| 3 | data |  | Объект |  |
|  |  | userId | Строка | Id клиента на стороне внешней системы |
|  |  | type | Строка | Тип события |
