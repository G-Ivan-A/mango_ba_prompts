---
id: contact-center-manual-sample-03-kanaly-kommunikacii
doc_code: CC
doc_title: "Контакт-центр MANGO OFFICE"
doc_version: "1.26.23-sample"
section: "3"
title: "Каналы коммуникации"
pages: "4"
source: kb/sources/contact-center-manual-sample/CC_manual_sample.fixture.pdf
extracted_by: "pdfplumber 0.11.10"
token_method: "tiktoken:cl100k_base"
tokens: 294
status: extracted
ai-generated: true
---
# 3. Каналы коммуникации

## 3.1 Голосовые вызовы

Входящие и исходящие вызовы, кампании обзвона, заказы обратного звонка с сайта.

## 3.2 Текстовые каналы

Текстовые каналы подключаются через омни-/мультиканальные виджеты MANGO Диалоги и мессенджеры: Telegram, VK, WhatsApp, Max, Авито. Все они образуют единую «текстовую» очередь.

## 3.3 Электронная почта (e-mail)

E-mail обрабатывается как текстовый канал в редакторе писем КЦ. Если в письме распознан адрес сотрудника ВАТС — обращение сразу переходит в «В работе»; иначе попадает в очередь. E-mail-обращение, не распределённое за заданное время, автоматически закрывается.
