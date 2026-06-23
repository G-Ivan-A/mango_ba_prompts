---
id: vpbx-api-63-api-zapisi-razgovorov-rechevaya-analitik
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
section: "3.5"
pdf_section: "3.5"
title: "API Записи разговоров, Речевая Аналитика"
pdf_heading: "3.5 API Записи разговоров, Речевая Аналитика"
pages: "88-89"
source: kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf
source_part: "1"
source_pages: "ч.1: 88-89"
source_refs: '[{"source_pdf":"kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf","part":1,"pages":"88-89","global_pages":"88-89"}]'
extracted_by: "pdfplumber 0.11.10"
token_method: "tiktoken:cl100k_base"
tokens: 557
status: extracted
ai-generated: true
---
# 3.5. API Записи разговоров, Речевая Аналитика

> Трассировка: PDF §3.5 · сквозные стр. 88-89 · источники: ч.1 `kb/mango-product-docs/sources/vpbx-api/MangoOffice_VPBX_API_v1.9.pdf` с.88-89.

Речевая Аналитика (далее по тексту – РА) – это сервис, который позволяет расшифровывать и анализировать содержание телефонных разговоров. РА распознает записанные разговоры и производит поиск заданной пользователем информации. Обратите внимание, чтобы работать с расшифровками телефонны разговоров, необходимо подключить услугу «Речевая аналитика» к вашей ВАТС. Тогда вам будет доступен API Записи разговоров. API Записи разговоров позволяет получать записи разговоров несколькими способами. Следует учитывать некоторые особенности сохранения записей разговоров ВАТС: - После окончания разговора сохранение занимает некоторое время, поэтому, если сразу после завершения разговора запись получить не удалось, рекомендуется повторять запрос с некоторым интервалом (например, 1 минута). - Записи разговоров должны храниться в «Облачном хранилище» в Личном кабинете Виртуальной АТС. - Если запись разговора была удалена посредством интерфейса Личного кабинета, то получить ее через API будет невозможно. Для получения записей разговоров необходимо знать их идентификаторы. Получить их можно из запроса статистики вызовов или из уведомления о записи разговора.
