---
id: mango-lk-manual-344-sozdanie-sip-trunk-dlya-fusionpbx-freesw
doc_code: LK
doc_title: "Виртуальная АТС MANGO OFFICE - Справочник абонента"
doc_version: "1.21"
section: "5.7.2"
pdf_section: "5.7.2"
title: "Создание SIP trunk для FusionPBX (Freeswitch)"
pdf_heading: "5.7.2 Создание SIP trunk для FusionPBX (Freeswitch)"
pages: "562-565"
source: kb/sources/mango-lk-manual/LK_manual_v-121часть-5.pdf
source_part: "5"
source_pages: "ч.5: 158-161"
source_refs: '[{"source_pdf":"kb/sources/mango-lk-manual/LK_manual_v-121часть-5.pdf","part":5,"pages":"158-161","global_pages":"562-565"}]'
extracted_by: "pdfplumber 0.11.10"
token_method: "tiktoken:cl100k_base"
tokens: 486
status: extracted
ai-generated: true
---
# 5.7.2. Создание SIP trunk для FusionPBX (Freeswitch)

> Трассировка: PDF §5.7.2 · сквозные стр. 562-565 · источники: ч.5 `kb/sources/mango-lk-manual/LK_manual_v-121часть-5.pdf` с.158-161.

Откройте меню администрирования транков во вкладке Gateways раздела Accounts.

![Изображение, стр. 563](../images/344-sozdanie-sip-trunk-dlya-fusionpbx-freesw-1.jpeg)

![Изображение, стр. 563](../images/344-sozdanie-sip-trunk-dlya-fusionpbx-freesw-2.png)

Для добавления нового транка нажмите пиктограмму “+”.

![Изображение, стр. 563](../images/344-sozdanie-sip-trunk-dlya-fusionpbx-freesw-3.png)

![Изображение, стр. 564](../images/344-sozdanie-sip-trunk-dlya-fusionpbx-freesw-4.jpeg)

![Изображение, стр. 564](../images/344-sozdanie-sip-trunk-dlya-fusionpbx-freesw-5.png)

В открывшейся форме необходимо заполнить поля: Gateway – имя транка. В примере используем имя mango. Username, Password- обязательные поля заполняются любыми значениями Proxy- SIP сервер провайдера Register – выставляем false Context - по умолчанию Public Profile - по умолчанию External Enabled - True

![Изображение, стр. 565](../images/344-sozdanie-sip-trunk-dlya-fusionpbx-freesw-6.jpeg)

Сохраните введенные данные кнопкой Save.

![Изображение, стр. 565](../images/344-sozdanie-sip-trunk-dlya-fusionpbx-freesw-7.png)
