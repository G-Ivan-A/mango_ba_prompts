---
status: draft
version: 0.1
updated: 2026-11-05
temperature: 0.1
---

# Вход RUN-0089

## Что проверяется

Хватает ли набора шагов сайта, чтобы пройти задачу от запроса до выпускного комплекта по контрактам 8 разделов,
если БА только копирует тексты с карточек и работает в чате с моделью. Основание —
[комментарий владельца к PR #455](https://github.com/G-Ivan-A/mango_ba_prompts/pull/455#issuecomment-6653026839).

| Файл | Что внутри |
| --- | --- |
| [`input-pack.md`](input-pack.md) | Задача SIM-1106 и параметры прогона |
| [`customer-materials.md`](customer-materials.md) | Материалы Заказчика для новых чатов |
| [`ba-script.md`](ba-script.md) | Заранее записанные реплики БА, Заказчика и команды |

Правила решения записаны до запуска: [`../logs/preregistration.md`](../logs/preregistration.md).
