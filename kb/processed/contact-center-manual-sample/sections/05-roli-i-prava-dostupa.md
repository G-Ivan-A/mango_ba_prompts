---
id: contact-center-manual-sample-05-roli-i-prava-dostupa
doc_code: CC
doc_title: "Контакт-центр MANGO OFFICE"
doc_version: "1.26.23-sample"
section: "5"
title: "Роли и права доступа"
pages: "6"
source: kb/sources/contact-center-manual-sample/CC_manual_sample.fixture.pdf
extracted_by: "pdfplumber 0.11.10"
token_method: "tiktoken:cl100k_base"
tokens: 253
status: extracted
ai-generated: true
---
# 5. Роли и права доступа

Права на модуль «Обращения» и вкладки очереди настраиваются в ЛК ВАТС → Безопасность и ограничения → Настройка доступа. Базовая матрица ролей:

| Роль | Очередь | Распределение | Отчёты | Настройки доступа |
| --- | --- | --- | --- | --- |
| Оператор | Да | Нет | Свои | Нет |
| Супервизор | Да | Частично | Группы | Нет |
| Администратор | Да | Да | Все | Да |
| Руководитель компании | Да | Да | Все | Да |

Настройка автоматического распределения обращений доступна только ролям «Руководитель компании» и «Администратор».
