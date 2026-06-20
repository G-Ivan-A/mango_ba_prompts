---
status: draft
version: 0.1
updated: 2026-06-18
ai-generated: true
type: kb-weblinks-guide
scope: kb/mango-product-docs/sources/web-links
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/111"
---

# `kb/mango-product-docs/sources/web-links/` — источники-ссылки

Не у каждого источника есть файл: иногда это веб-страница (документация вендора,
статья, changelog). Такие источники регистрируются здесь **манифестом**, чтобы
агент мог их цитировать стабильно, а человек — найти оригинал.

## Как добавить веб-ссылку

1. Создайте `kb/mango-product-docs/sources/web-links/<slug>.md` со следующим frontmatter:

   ```markdown
   ---
   type: kb-web-source
   doc_code: VATS-HELP
   title: "Справка ЛК ВАТС — Настройка доступа"
   url: "https://www.mango-office.ru/..."
   accessed: 2026-06-18        # дата обращения (контент в вебе дрейфует)
   status: draft
   ai-generated: true
   ---

   # Справка ЛК ВАТС — Настройка доступа

   Краткая выжимка нужных фактов с цитатами и якорями раздела.
   ```

2. Если страница важна и может измениться/исчезнуть — сохраните в тело файла
   **выжимку** ключевых фактов (как извлечённый раздел в `kb/mango-product-docs/processed/`), чтобы
   БЗ не зависела от доступности сайта.

3. Цитируйте как обычный источник:
   `[VATS-HELP](kb/mango-product-docs/sources/web-links/<slug>.md)` и/или прямой `url` из манифеста.

## Почему не «скачиваем сайт»

Сознательно **не** автоматизируем краулинг: это ломает детерминизм и упирается в
сетевой доступ из CI. Веб-источник фиксируется датой обращения и ручной выжимкой —
надёжнее для воспроизводимой БЗ. Автоматический сбор — возможный следующий шаг
(см. [`docs/kb-experiment-report.md`](../../../../docs/kb-experiment-report.md),
раздел «Следующие шаги»).
