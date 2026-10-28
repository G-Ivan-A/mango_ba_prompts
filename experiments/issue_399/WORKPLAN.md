---
status: review
version: 0.2
updated: 2026-10-28
temperature: 0.1
---

# План проверки issue 399

Источник: https://github.com/G-Ivan-A/mango_ba_prompts/issues/399
Результат: https://github.com/G-Ivan-A/mango_ba_prompts/pull/400

- [x] Прочитать полную постановку, все комментарии и reviews; sub-issues отсутствуют.
- [x] Проверить ветку, clean baseline, contributing и четырёхуровневый контракт.
- [x] Получить runtime-словарь, исторический Product Layer и forensic JSON локально.
- [x] Прочитать весь релевантный forensic-контекст, сохранить обезличенные локаторы и хэш.
- [x] До реализации написать regression tests для границ обхода, извлечения таблиц и маршрутизации.
- [x] Обойти все достижимые HTML-страницы документации; исключить файлы, downloads и tickets.
- [x] Сохранить HTTP-коды, redirect, content hash, таблицы, изображения, метрики и границы полноты.
- [x] Глубоко проверить шесть обязательных разделов и визуальные ограничения без скачивания файлов.
- [x] Сохранить все исторические capabilities/features/functions, расширить atomic coverage с URL evidence.
- [x] Реализовать many-to-many sitemap mapping и адресный поиск с cross-product expansion.
- [x] Описать changelog, deprecated/unknown/gaps, forensic patterns и web/runtime стратегию.
- [x] Проверить каждое требование по acceptance matrix, абсолютные ссылки и provenance.
- [x] Запустить focused tests, затем make validate-full; сохранить полные логи локально.
- [x] Коммитить атомарные результаты; merge upstream/main; push только подготовленной ветки.
- [x] Обновить PR title/body с Fixes #399, перечитать gh pr diff, проверить CI по SHA/времени.
- [x] Проверить CI: списки runs upstream/fork пусты; скачивать failed logs не требуется.
- [x] Проверить clean tree после основного коммита, новые комментарии (все четыре типа пусты), gh pr ready 400.
- [ ] Перевести issue в review: внешний блокер прав; критерий остаётся незавершённым.

## Evidence и внешний блокер

Публичный snapshot: 3918 URL, frontier 0; 7 Domain / 43 Capability / 151 Feature /
152 Atomic Function. Все исторические ключи и параметры сохранены; 74 новых узла
имеют page-level источники. 14 offline regression tests проходят. Неполнота
распознавания шаблонов и визуальная неопределённость явно сохранены в артефактах.
`make validate-full`: 68 валидаторов, 0 из кэша, 0 провалов; исходные и публичные
артефакты воспроизведены побайтно. `make validate-fast` также проходит.
Основной результат опубликован коммитом `7f920e2e`; PR ready, без merge.
Финальное чтение diff выявило silent success пустого плана: добавлены явный
`no-locators-found` и reproducing regression, требующий fallback.

Требование issue status `review` остаётся открытым: у текущего токена нет
`triage`/`push`/`maintain`/`admin` в upstream. Label `review` не существует;
попытка назначения через API вернула HTTP 403 `Must have admin rights to Repository`.
Project items отсутствуют. Это не заменяется статусом review файлов или ready PR.
Остальные пункты финализации выполняются независимо от этого ограничения.

Нельзя считать отсутствие страницы признаком прекращения продукта, Last-Modified —
частотой обновления, HTML-таблицу — доказательством понимания схемы, static tests —
LLM-eval. Сырые чаты не публикуются. PDF, installers и прочие вложения портала
не скачиваются. Одновременные HTTP-запросы ограничены; память и размеры ответов ограничены.
