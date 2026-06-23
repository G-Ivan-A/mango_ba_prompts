---
id: vpbx-api-145-obzor
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
section: "3.10.1.1"
pdf_section: "3.10.1.1"
title: "Обзор"
pdf_heading: "3.10.1.1 Обзор"
pages: "199"
source: kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf
source_part: "1"
source_pages: "ч.1: 199"
source_refs: '[{"source_pdf":"kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf","part":1,"pages":"199","global_pages":"199"}]'
extracted_by: "pdfplumber 0.11.10"
token_method: "tiktoken:cl100k_base"
tokens: 457
status: extracted
ai-generated: true
---
# 3.10.1.1. Обзор

> Трассировка: PDF §3.10.1.1 · сквозные стр. 199 · источники: ч.1 `kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf` с.199.

Метод обеспечивает загрузку в ВАТС и распознавание речи в звуковом файле, который должен соответствовать требованиям: - формат: WAV (несжатый аудиопоток); - максимальный размер: 100 МБ; - максимальная длина имени файла: 64 символа латиницей. В результате обработки запроса, будут выполнены следующие действия: - звуковой файл загружен в ВАТС и привязан к сотруднику, указанному в запросе (в параметре "member_id", либо по значению параметра "device_code"); - звуковой файл сохранен в облачное хранилище ВАТС, если оно у вас уже есть. Если у вас еще нет облачного хранилища ВАТС, то звуковой файл не будет сохранен; - автоматически сформировано и передано в сервис "Речевая аналитика" задание на распознавание речи в данном звуковом файле. Примечания: 1) после того, как распознавание речи будет выполнено, в API ВАТС будет сформировано соответсвующее событие; 2) чтобы получить результаты распознавания речи, используйте этот запрос.
