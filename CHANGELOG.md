---
status: draft
version: 0.1
updated: 2026-06-11
ai-generated: true
---

# Changelog — mango_ba_prompts

Все значимые изменения проекта документируются здесь. Формат основан на
[Keep a Changelog](https://keepachangelog.com/ru/1.1.0/); проект придерживается
[Semantic Versioning](https://semver.org/lang/ru/).

## Unreleased

### Added — Issue #101 разбор эксперимента «Задача 1027» и стандарт фиксации экспериментов

- Добавлен анализ первой реальной сессии БА
  [`docs/analysis/experiment-1027-analysis.md`](docs/analysis/experiment-1027-analysis.md):
  вердикты по 4 гипотезам БА с цитатами из стенограммы, **предложения** правок
  промптов (P1–P5) как кандидаты в RFC и рекомендации по онтологии (без её
  изменения). Сами промпты в этом PR **не меняются** — правки выносятся через
  процесс отладки (см. ниже).
- Добавлен легковесный стандарт фиксации экспериментов (Draft v0.1)
  [`standards/experiment-log-standard.md`](standards/experiment-log-standard.md):
  два уровня фиксации (GitHub Issue / лёгкий Markdown) и ядро из 6 метрик.
- Добавлен первый прогон по стандарту (dogfood на сессии 1027)
  [`prompts/experiments/fr-generation-1027-live_2026-06-16.md`](prompts/experiments/fr-generation-1027-live_2026-06-16.md).
- Добавлен аудит контрактов
  [`governance/audit-contracts-2026-06-17.md`](governance/audit-contracts-2026-06-17.md):
  ревизия `AI_GOVERNANCE.md`, `CONTRIBUTING.md` и стандарта логирования,
  выявленные пробелы (нет процесса отладки/RFC/критериев приёмки правок промптов).
- Добавлен аудит исследования
  [`governance/audit-research-1027.md`](governance/audit-research-1027.md):
  проверка полноты разбора гипотез H1–H4, обоснованности рекомендаций O1–O3 и
  передачи онтологии (ADR #3–#8).
- Добавлен черновик процесса отладки промптов
  [`governance/prompt-debugging-process.md`](governance/prompt-debugging-process.md)
  и реестр RFC [`governance/rfc-register.md`](governance/rfc-register.md):
  порядок «эксперимент → RFC → согласование с пользователем → изменение».

### Added — Issue #97 формализация онтологии БА и стандартов (Creative + Research)

- Формализована онтология БА (артефакт ↔ процесс ↔ операция) и выпущен набор
  стандартов в виде ADR: [ADR-003](docs/adr/003-ba-ontology.md) (онтология),
  [ADR-004](docs/adr/004-operations-taxonomy.md) (таксономия 13 операций,
  `risk_analysis` сохранён), [ADR-005](docs/adr/005-artifact-team-naming.md)
  (нейминг артефактов/команд), [ADR-006](docs/adr/006-prompt-naming.md) (нейминг
  промптов, запрет перегрузки), [ADR-007](docs/adr/007-kb-standard.md) (KB до
  настоящего RAG), [ADR-008](docs/adr/008-industry-standards-standard.md)
  (отраслевые стандарты и best practices),
  [ADR-009](docs/adr/009-bcreq-formation-process.md) (многоуровневый процесс
  BCREQ, механизм незавершённых подпроцессов),
  [ADR-010](docs/adr/010-pages-ux.md) (UX GitHub Pages). Все ADR содержат
  обязательные разделы ФТ-9 (Title, Status, Context, Decision, Consequences,
  References, Examples).
- Добавлены «живые» контракты-стандарты с нормативным словарём RFC 2119 / BCP 14
  и блоком DoD: [`standards/ba-ontology.md`](standards/ba-ontology.md),
  [`standards/artifact-naming-standard.md`](standards/artifact-naming-standard.md),
  [`standards/team-directory.md`](standards/team-directory.md) (ровно две команды
  `BCREQ` и `CCMO` + механизм добавления),
  [`standards/kb-standard.md`](standards/kb-standard.md),
  [`standards/industry-standards-standard.md`](standards/industry-standards-standard.md),
  [`standards/bcreq-process-standard.md`](standards/bcreq-process-standard.md),
  [`standards/pages-ux-standard.md`](standards/pages-ux-standard.md).
- **ФТ-8 (GitHub Pages):** на странице «Процессы» SPA (рядом с карточками
  процессов из issue #99) добавлена секция «Процессы и подпроцессы с промптами».
  Генератор [`scripts/generate-pages-data.mjs`](scripts/generate-pages-data.mjs)
  строит полный список процессов/подпроцессов в
  [`site/data/process-tree.json`](site/data/process-tree.json) (с флагом
  `hasPrompts` и типом покрытия `kind`), а интерфейс
  ([`site/index.html`](site/index.html), [`site/app.js`](site/app.js),
  [`site/styles.css`](site/styles.css)) по жёсткому требованию выводит **только**
  процессы/подпроцессы с промптами. При > 20 показанных подпроцессах используется
  раскрывающееся дерево (`<details>`/`<summary>`). Прототип (скриншоты) — в
  [ADR-010](docs/adr/010-pages-ux.md).
- Доказательная база: эксперименты
  [`prompts/experiments/standards-applied-ab-2026-06-16.md`](prompts/experiments/standards-applied-ab-2026-06-16.md)
  и
  [`prompts/experiments/kb-citation-check-2026-06-16.md`](prompts/experiments/kb-citation-check-2026-06-16.md).
- Добавлена локальная проверка
  [`scripts/validate_issue_97_ontology_standards.py`](scripts/validate_issue_97_ontology_standards.py)
  (ADR-разделы ФТ-9, RFC 2119/DoD стандартов, инварианты `process-tree.json`,
  две команды, отсутствие выдуманных кодов, сохранность `risk_analysis`) и шаг в
  workflow [`.github/workflows/github-pages.yml`](.github/workflows/github-pages.yml).

### Fixed — Issue #103 корректировки UI каталога промптов

- **ФТ-1. Карточка промпта.** Убрана стрелка (↗) из верхней части карточки;
  нижняя стрелка заменена кнопкой «📁 Перейти в репо», ведущей на файл промпта
  в GitHub репозитории.
- **ФТ-2. Фильтр статуса удалён.** Блок «СТАТУС» убран из панели фильтров;
  удалены связанные обработчики и генерация токенов `status:*`.
- **ФТ-3. Визуальное разделение групп фильтров.** Каждая группа фильтров
  получила рамку, тонированный фон и жирные заголовки: процессы — голубой фон,
  операции — зелёный, режимы — фиолетовый (вариант D из предложений).
- **ФТ-4. Сортировка по убыванию даты.** Опция «По дате» отображается со
  стрелкой ↓, сортировка по умолчанию — последние обновлённые сверху.
- **ФТ-5. Тулбар.** Сортировка и кнопка экспорта перемещены выше поля поиска;
  кнопка экспорта получила явный текстовый ярлык «📥 Скачать».
- **ФТ-6. Кнопки очистки.** Добавлены кнопки «✕ Очистить поиск» и
  «↺ Сбросить фильтры» справа от строки поиска; видимы только при активных
  фильтрах или заполненном поиске.

### Added — Issue #99 оптимизация GitHub Pages (многостраничность и UX)

- **ФТ-1. Многостраничность.** Сайт [`site/index.html`](site/index.html) разбит на
  пять разделов с верхним меню: **Каталог** (главная, URL `/`), **Дашборд**,
  **Roadmap**, **Процессы**, **Паттерны**. Переключение реализовано клиентским
  hash-роутером в [`site/app.js`](site/app.js) (SPA), порядок секций сохранён.
- **ФТ-2. Оптимизация карточек.** Из карточки убраны путь к файлу и хэш рядом с
  «Копировать»; вместо хэша показаны версия (`v…`), дата обновления и статус
  тестов (`✅ N тест(ов)`); ID вынесен мелким шрифтом под названием; добавлена
  кнопка «Ссылка» (↗) — копирует deep-link `#prompt=<id>` на карточку; теги
  процессов получили эмодзи-иконки; описания расширены до 150-300 символов
  (генерируются динамически в [`scripts/generate-pages-data.mjs`](scripts/generate-pages-data.mjs)).
- **ФТ-3. Дашборд.** Блок «Проверки» показывает всего проверок, разбивку
  **по процессам БА** (динамически из frontmatter, с бакетом «Прочее»),
  обратную связь (`prompt:feedback`) и покрытие тестами (X/Y, %). Добавлен блок
  «Активность» — топ-5 промптов. Дублирование метрик убрано.
- **ФТ-4. UX.** Быстрый поиск с автодополнением (по названию/ID/описанию/тегам),
  сортировка (дата, популярность, алфавит, статус), фильтр по статусу
  (Draft/Canonical/Archived), карточка процесса по клику (описание, операции,
  связанные промпты, паттерны, known gaps), экспорт каталога в Markdown по
  текущим фильтрам и переключатель тёмной темы (сохраняется в `localStorage`).
- **ФТ-5. Генерация данных.** Генератор формирует дополнительно
  `site/data/processes.json` и `site/data/patterns.json`, расширенные
  `checks.json` (по процессам, покрытие тестами) и длинные описания промптов;
  процессы и эмодзи назначаются динамически — без хардкода типов артефактов.
- **ФТ-6.** Обновлены README и этот CHANGELOG.
- Добавлена локальная проверка
  [`scripts/validate_issue_99_pages_optimization.py`](scripts/validate_issue_99_pages_optimization.py)
  и шаг в workflow [`.github/workflows/github-pages.yml`](.github/workflows/github-pages.yml).

### Fixed — Issue #95 добавить ID промпта в копируемый текст

- Кнопка «Копировать» в карточке промпта теперь добавляет HTML-комментарий с ID
  в начало копируемого текста: формат `<!-- {prompt.id} -->\n\n{body}`.
- HTML-комментарий добавляется **только при копировании** — в отображаемой карточке
  он не появляется (изменения только в [`site/app.js`](site/app.js)).
- LLM игнорирует HTML-комментарий, при этом ID виден в истории чата и позволяет
  отследить, какой промпт был использован.
- Добавлена локальная проверка
  [`scripts/validate_issue_95_prompt_id_in_copy.py`](scripts/validate_issue_95_prompt_id_in_copy.py)
  и шаг в workflow [`.github/workflows/github-pages.yml`](.github/workflows/github-pages.yml).

### Changed — Issue #92 метаданные промптов (`id` + `title`), удаление EXPERIMENTAL

- В обязательный frontmatter всех 30 промптов (`prompts/` и `prompts/archive/`)
  добавлены поля `id` (уникальный токен `mango-[операция]-[режим]`) и `title`
  (человекочитаемое название на русском).
- Из всех 24 активных промптов удалён маркер
  `<!-- EXPERIMENTAL: DO NOT USE IN PRODUCTION -->`: экспериментальность уже
  отражает `status: draft`.
- Обновлён стандарт промптов: ADR-001
  [`docs/adr/001-prompt-standard.md`](docs/adr/001-prompt-standard.md) и контракт
  [`standards/prompt-standard.md`](standards/prompt-standard.md) теперь требуют
  6 обязательных полей frontmatter (добавлены `id` и `title`).
- Генератор [`scripts/generate-pages-data.mjs`](scripts/generate-pages-data.mjs)
  берёт `id`/`title` из frontmatter и формирует поле `body` — текст промпта без
  frontmatter и маркеров для чистого копирования.
- В интерфейсе GitHub Pages ([`site/app.js`](site/app.js),
  [`site/styles.css`](site/styles.css)) карточка промпта выводит `title` жирным
  заголовком и `id` мелкой меткой; кнопка «Копировать» копирует чистый текст без
  frontmatter.
- В матрицу [`prompts/README.md`](prompts/README.md) добавлены колонки
  «Название» (title) и «Токен» (id); парсер матрицы в генераторе переведён на
  поиск колонок по заголовку.
### Changed — Issue #91 улучшение GitHub Pages (порядок, фильтры, аналитика)

- Изменён порядок секций в [`site/index.html`](site/index.html): **Каталог →
  Дашборд → Проверки → Roadmap**. Каталог промптов теперь основной контент и
  виден сразу (ФТ-1).
- Переупорядочены фильтры каталога в [`site/app.js`](site/app.js): **Процессы БА
  → Операции → Режимы**. Внутри одного фильтра действует логика **ИЛИ**, между
  фильтрами — **И** (ФТ-2).
- Реализована умная каскадная фильтрация: при выборе процесса(ов) фильтр
  «Операции» сужается до операций выбранных процессов (недоступные операции
  подсвечиваются как неактивные), а фильтры «Процессы» и «Режимы» не
  сокращаются (ФТ-3).
- Добавлен модуль **«Проверки»** вместо карточки «Мультиагенты»: статус отладки
  (`draft` / `canonical` / `archived`), число зафиксированных тестов в
  [`prompts/experiments/`](prompts/experiments), обратная связь по лейблу
  `prompt:feedback` и активность использования промптов по процессам БА (ФТ-4).
- [`scripts/generate-pages-data.mjs`](scripts/generate-pages-data.mjs) генерирует
  новый артефакт [`site/data/checks.json`](site/data/checks.json) на основе
  тестовых логов и статического среза
  [`governance/prompt-feedback.json`](governance/prompt-feedback.json) (ФТ-6).
- Решение по `experiments/` vs `scripts/`: корневой `experiments/` отсутствует
  (Python-валидаторы уже консолидированы в `scripts/`), `prompts/experiments/`
  сохранён как каноничное место тестовых логов промптов. Назначение директорий
  задокументировано (ФТ-5).
- Добавлена локальная проверка
  [`scripts/validate_issue_91_pages_enhancements.py`](scripts/validate_issue_91_pages_enhancements.py)
  и шаг в workflow
  [`.github/workflows/github-pages.yml`](.github/workflows/github-pages.yml).

### Added — Issue #86 Mango Office Multichannel widget

- В GitHub Pages шаблон [`site/index.html`](site/index.html) добавлен виджет
  Mango Office Multichannel с `id: 23303`: чат поддержки и заказ обратного
  звонка загружаются перед закрывающим тегом `</body>`.
- Добавлена локальная проверка
  [`scripts/validate_issue_86_mango_widget.py`](scripts/validate_issue_86_mango_widget.py),
  закрепляющая наличие скрипта виджета, идентификатора `23303`, расположение
  перед `</body>` и запись в changelog.
- Workflow [`.github/workflows/github-pages.yml`](.github/workflows/github-pages.yml)
  теперь запускает проверку интеграции виджета вместе с проверкой артефакта
  GitHub Pages.
### Added — Issue #85 библиотека MVP-паттернов БА

- Созданы 7 MVP-паттернов в `patterns/`: `glossary-context-generation`,
  `fr-generation`, `fr-validation`, `user-story-generation`,
  `usecase-generation`, `asr-ingestion` и `meeting-summary-generation`. Каждый
  паттерн содержит 8 полей ADR-002, Product Layer, Commercial Layer, правила
  адаптации, LLM-агностичный `prompt_template`, quality gates, output schema,
  обезличенный пример и ссылки на существующие prompt-реализации.
- Обновлён [`patterns/README.md`](patterns/README.md): добавлены навигация по
  MVP-паттернам, матрица "паттерн ↔ процесс ↔ операция ↔ промпты", пример
  маршрута использования и полные URL связанных PR/репозиториев.
- В [`docs/ba-processes/00-index.md`](docs/ba-processes/00-index.md) заполнена
  колонка "Паттерн" для процессов, покрытых MVP-библиотекой, сохранив
  parser-compatible структуру центрального реестра.
- Добавлена локальная проверка
  [`scripts/validate_issue_85_patterns_library.py`](scripts/validate_issue_85_patterns_library.py)
  для воспроизведения требований issue #85: наличие 7 директорий, 8 секций,
  Product/Commercial Layer, примеров, ссылок на существующие prompts, навигации
  и центрального registry mapping.

### Added — Issue #83 карта процессов БА

- Развёрнут центральный индекс
  [`docs/ba-processes/00-index.md`](docs/ba-processes/00-index.md) в детальную
  карту 9 процессов БА с входами, выходами, workflow, cognitive operations,
  direct links на prompt-файлы и явными manual gaps.
- Добавлены рекомендации по режимам `stepwise` / `oneshot` / `legacy`, связь
  маршрутов с Product Layer и Commercial Layer, 3 сценария запуска процессов с
  Mermaid-диаграммами и полный traceability-блок по связанным PR/репозиториям.
- Добавлена локальная проверка
  [`scripts/validate_issue_83_ba_process_map.py`](scripts/validate_issue_83_ba_process_map.py)
  для воспроизведения требований issue #83: наличие 9 процессов, 13 операций,
  ссылок на 24 активных и 6 архивных prompts, known gaps и навигации.

### Added — Issue #78 промпт-суммаризатор сессий БА

- Создан промпт
  [`prompts/session-debug-documentation-oneshot.md`](prompts/session-debug-documentation-oneshot.md):
  one-shot суммаризация длинной сессии работы с LLM в структурированное резюме
  (контекст, ключевые решения с обоснованием, проблемы и обходные пути,
  применённые промпты, открытые вопросы, следующие шаги). Формат совместим с
  шаблоном блока суммарии в
  [`governance/session-digests.md`](governance/session-digests.md).
- Имя файла приведено к схеме ADR-001 `[домен]-[операция]-[режим].md`
  (`session-debug` / `documentation` / `oneshot`) вместо запрошенного в issue
  рабочего названия `session-debug-summarizer.md`, не соответствующего схеме.
- Промпт добавлен в матрицу
  [`prompts/README.md`](prompts/README.md) (новый раздел «Отладка и
  суммаризация сессий», счётчик активных промптов 23 → 24) и в маппинг процесса
  «Помощь ПО/ПМ»
  [`docs/ba-processes/00-index.md`](docs/ba-processes/00-index.md).
- Добавлен зафиксированный прогон
  [`prompts/experiments/session-debug-summarizer-2026-06-13.md`](prompts/experiments/session-debug-summarizer-2026-06-13.md),
  подтверждающий получение структурированного резюме за один запуск.
- Обновлены контрольные счётчики в
  [`scripts/validate_issue_74_github_pages.py`](scripts/validate_issue_74_github_pages.py)
  (24 активных промпта, 30 всего).

### Added — Issue #74 GitHub Pages interface

- Создан dependency-free GitHub Pages интерфейс в [`site/`](site/): дашборд
  фаз внедрения, каталог 23 активных промптов и 6 архивных файлов, OR-фильтры по
  когнитивным операциям / процессам БА / режимам, поиск и копирование prompt
  content в буфер.
- Добавлен генератор [`scripts/generate-pages-data.mjs`](scripts/generate-pages-data.mjs):
  он читает Markdown source of truth (`prompts/*.md`,
  [`prompts/README.md`](prompts/README.md),
  [`docs/taxonomy.md`](docs/taxonomy.md),
  [`docs/ba-processes/00-index.md`](docs/ba-processes/00-index.md),
  [`docs/ba-ecosystem.md`](docs/ba-ecosystem.md)) и формирует статические
  [`site/data/prompts.json`](site/data/prompts.json),
  [`site/data/stats.json`](site/data/stats.json),
  [`site/data/roadmap.json`](site/data/roadmap.json).
- Настроен workflow
  [`.github/workflows/github-pages.yml`](.github/workflows/github-pages.yml):
  при PR выполняется генерация и проверка, при push в `main` артефакт `site/`
  публикуется в ветку `gh-pages` через `GITHUB_TOKEN`, без PAT и без GitHub API
  в клиентском коде.
- Добавлена локальная проверка
  [`scripts/validate_issue_74_github_pages.py`](scripts/validate_issue_74_github_pages.py)
  для воспроизведения и валидации требований issue #74.
### Added — Issue #76 суммария синхронизации сессий Хаба

- structured: зафиксировать суммарию синхронизации сессий Хаба в
  [`governance/session-digests.md`](governance/session-digests.md): добавлены
  индексная запись `2026-06-14` и блок `#2026-06-14` для передачи контекста
  между Чатом Хаба и Чатом БА Манго.
- Локальная проверка [`scripts/validate_issue_72_hub_sync.py`](scripts/validate_issue_72_hub_sync.py)
  больше не требует пустой индекс `session-digests.md`, так как первая суммария
  теперь сохранена.

### Changed — Issue #72 Smart Sync последних обновлений Хаба

- [`AI_SESSION_HANDOVER_PROMPT.md`](AI_SESSION_HANDOVER_PROMPT.md) синхронизирован
  с Hub PR #226 (`templates/htom/AI_SESSION_HANDOVER_PROMPT.md`, SHA
  `f3e8b265b1577d0ee1fe173dbe16728cc3c7e31b`): добавлен механизм периодической
  суммаризации сессий через `governance/session-digests.md`, сохранены локальные
  правила issue #48/#61 про канал работы через Конарда и task template.
- [`governance/agent-onboarding-protocol.md`](governance/agent-onboarding-protocol.md)
  обновлён по source SHA `f3e8b265b1577d0ee1fe173dbe16728cc3c7e31b`: встроенный
  копируемый prompt теперь соответствует handover v0.5 и указывает на
  `governance/session-digests.md`.
- Созданы [`governance/session-digests.md`](governance/session-digests.md) как
  пустой локальный индекс суммарий для `mango_ba_prompts` и
  [`governance/artifact-map.md`](governance/artifact-map.md) как локальная карта
  активных артефактов, адаптированная из хабовой карты PR #224/#226.
- Обновлены [`README.md`](README.md), [`.hub-profile.json`](.hub-profile.json) и
  [`governance/migration-manifest.md`](governance/migration-manifest.md), чтобы
  зафиксировать Smart Sync snapshot, source SHA и терминологию
  Пользователь / Исполнитель.
- Добавлена локальная проверка
  [`scripts/validate_issue_72_hub_sync.py`](scripts/validate_issue_72_hub_sync.py)
  для воспроизведения и валидации требований issue #72.
- Досинхронизированы релевантные части Hub PR #229 и Hub PR #230, latest Hub SHA
  `b683341d22d4f518618917a02d9c7c394658b156`.
- Hub PR #229: Base Registry внешних источников
  `research/external-knowledge/external-sources-registry.md` оставлен
  reference-only в Хабе; для Mango в
  [`docs/hub-research-dependencies.md`](docs/hub-research-dependencies.md)
  зарегистрированы строки `ext-003` (Spec-Driven Development) и `ext-007`
  (Контекст-инжиниринг), без создания локального `research/`.
- Hub PR #230: терминология активных guidance-файлов выровнена на
  `Пользователь / Исполнитель` в [`AI_GOVERNANCE.md`](AI_GOVERNANCE.md),
  [`CONTRIBUTING.md`](CONTRIBUTING.md), [`README.md`](README.md),
  [`docs/task-for-konard-template.md`](docs/task-for-konard-template.md) и
  связанных ADR/исторических ссылках; traceability contracts, Framework vs
  Template и Scope Resolver-а задокументированы как Hub-governance контракты,
  не требующие локальных артефактов в `mango_ba_prompts`.

### Added — Issue #65 README для `prompts/`

- Создан [`prompts/README.md`](prompts/README.md): навигация по 23 активным
  промптам и 6 архивным legacy-файлам, матрица назначение ↔ режим ↔ статус ↔
  версия ↔ когнитивная операция ↔ процесс БА, описание структур Hub-style и
  Mango BA workflow, токенов `stepwise` / `oneshot` / `legacy`, процесса
  отладки и ссылок на таксономию, индекс процессов, стандарты и шаблон фидбека.

### Added — Issue #64 ADR на стандарт паттернов

- Создан [`docs/adr/002-pattern-standard.md`](docs/adr/002-pattern-standard.md):
  ADR фиксирует directory-first структуру `patterns/[operation-name]/README.md`,
  8 обязательных полей паттерна, связь с 13 когнитивными операциями и 9
  процессами БА, маппинг паттерн ↔ prompt только через
  [`docs/ba-processes/00-index.md`](docs/ba-processes/00-index.md),
  LLM-агностичность `prompt_template`, правила создания новых паттернов,
  критерии зрелости, semver-версионирование и совместимость с
  [`docs/adr/001-prompt-standard.md`](docs/adr/001-prompt-standard.md).
- [`patterns/README.md`](patterns/README.md) и
  [`standards/pattern-standard.md`](standards/pattern-standard.md) согласованы
  с ADR: README остаётся краткой справкой, стандарт — операционным контрактом
  для review.
- Добавлена локальная проверка
  [`scripts/validate_issue_64_pattern_adr.py`](scripts/validate_issue_64_pattern_adr.py)
  для воспроизведения и валидации требований issue #64.

### Added — Issue #66 экосистема работы БА с графами связей и картой процессов

- Создан [`docs/ba-ecosystem.md`](docs/ba-ecosystem.md) — единая карта
  экосистемы работы БА Mango: методология на основе research Хаба, Mermaid-граф
  связей, определения сущностей, классификации направлений разработки, стилей и
  пакетов документов, правила/практики, матрицы процесс ↔ операция ↔ промпт,
  направление ↔ стиль ↔ шаблон и артефакт ↔ стиль.
- В документ добавлена подробная карта 9 процессов БА: цель, входы, выходы,
  workflow по когнитивным операциям, рекомендуемые промпты и known gaps по
  каждому процессу. Зафиксированы 3 сценария запуска: клиентский заказ,
  внутренняя доработка продукта и тендерное ТЗ.
- Описана стратегия перехода от библиотеки промптов к системным промптам с
  БЗ/RAG, агентам и мультиагентному контуру, включая критерии перехода между
  уровнями и сохранение human gates.
- [`README.md`](README.md) и
  [`docs/ba-processes/00-index.md`](docs/ba-processes/00-index.md) дополнены
  навигацией на экосистемную карту; реестр
  [`docs/hub-research-dependencies.md`](docs/hub-research-dependencies.md)
  отмечает новый документ как consumer релевантных research-якорей Хаба.
- Удалён авто-сгенерированный корневой `.gitkeep`, созданный только для
  открытия draft PR.
### Added — Issue #63 ADR стандарта промптов

- Создан [`docs/adr/001-prompt-standard.md`](docs/adr/001-prompt-standard.md):
  ADR фиксирует две допустимые структуры промптов (Hub-style и Mango BA workflow),
  токены режимов `stepwise` / `oneshot` / `legacy` с обоснованием отказа от
  `expert` / `express`, 4 обязательных поля frontmatter, правила именования
  `[домен]-[операция]-[режим].md`, суффиксы `-legacy` / `-v2` / `-alt` и процессы
  `draft` -> `canonical` / архивации. Существующие промпты не изменялись.

### Changed — Issue #61 Creative-mode governance без архитектурного долга

- [`AI_GOVERNANCE.md`](AI_GOVERNANCE.md), [`AI_QUICK_RULES.md`](AI_QUICK_RULES.md)
  и [`CONTRIBUTING.md`](CONTRIBUTING.md) обновлены: `Structured` сохраняет
  fail-closed semantics, а `Creative` допускает обоснованный обход scope или
  локального правила, если обход нужен для цели задачи и явно описан в PR.
- Зафиксирована специфика работы с Конардом: **молчание = согласие** при merge
  без комментариев; комментарий + ручной перезапуск задачи = итерация в той же
  ветке PR; close PR = отказ от решения.
- [`docs/rfc-hub-integration.md`](docs/rfc-hub-integration.md) переформулирован
  как рекомендательный маршрут передачи практик в Хаб: Хаб — источник лучших
  практик и обмена опытом, не ограничитель локальных решений `mango_ba_prompts`.
- Созданы [`docs/task-for-konard-template.md`](docs/task-for-konard-template.md)
  и [`docs/adr/0003-creative-mode-governance.md`](docs/adr/0003-creative-mode-governance.md):
  шаблон задачи фиксирует WHAT/WHY без пошагового HOW, ADR описывает практику,
  примеры было/стало, обоснованные обходы и self-test на кейсе PR #57.
- [`AI_SESSION_HANDOVER_PROMPT.md`](AI_SESSION_HANDOVER_PROMPT.md) обновлён до
  локального шаблона постановки задач для Конарда.

### Added — Issue #52 фундамент: концепция, таксономия, RFC Хаба и базовая структура

- Создан [`docs/taxonomy.md`](docs/taxonomy.md) — таксономия **13 когнитивных
  операций** (9 базовых + 4 расширенных: `impact_analysis`,
  `reverse_requirements`, `risk_analysis`, `release_readiness`) и **9 процессов
  БА** с маппингом процессов на операции.
- Создан [`docs/rfc-hub-integration.md`](docs/rfc-hub-integration.md) — RFC
  (сознательно **не** ADR) о стратегическом направлении переноса лучших практик
  спока в Хаб: критерии C1–C5, процесс из 6 шагов, provenance
  `source_spoke`/`source_sha`.
- Создан каталог [`patterns/`](patterns/) с README (паттерн = 8 полей:
  `purpose`, `process_stage`, `context_requirements`, `prompt_template`,
  `quality_gates`, `examples`, `output_schema`, `governance_rules`); сами
  паттерны создаются отдельными задачами.
- Создан [`docs/ba-processes/00-index.md`](docs/ba-processes/00-index.md) —
  централизованный маппинг процесс ↔ операции ↔ паттерн ↔ промпты
  (вместо хранения маппинга во frontmatter).
- Создан шаблон таблицы открытых вопросов (дата | автор | суть | статус |
  решение) с правилом автоматической очистки решённых строк Конардом при
  закрытии связанного issue. В issue #80 механизм заменён единым трекером в
  [`governance/BACKLOG.md`](governance/BACKLOG.md#5-открытые-вопросы).
- Созданы контракты [`standards/prompt-standard.md`](standards/prompt-standard.md)
  (ровно 4 обязательных поля frontmatter: `status` со значениями
  `draft`/`canonical`/`archived`, `version`, `updated`, `temperature`;
  именование `[домен]-[операция]-[режим].md`; RAG-формат ссылок
  `См. [Глоссарий](standards/GLOSSARY.md)`; фиксация прогонов в
  `prompts/experiments/`) и
  [`standards/pattern-standard.md`](standards/pattern-standard.md)
  (8 обязательных полей паттерна, универсальный `prompt_template`).
- Создан шаблон issue
  [`.github/ISSUE_TEMPLATE/prompt-feedback.yml`](.github/ISSUE_TEMPLATE/prompt-feedback.yml)
  для фидбека БА: 2 обязательных поля (имя промпта + результат), чек-боксы
  типовых проблем, явный запрет ссылок на закрытые корпоративные документы;
  label `prompt:feedback` проставляется автоматически.
- `README.md` (v2.1): добавлен раздел «Стратегия и тактика» (цель —
  автоматизация БА Mango; тактика — библиотека паттернов и промптов; ссылка
  на RFC), исправлена повреждённая таблица структуры, таблица frontmatter
  приведена к 4 обязательным полям, обновлена навигация.

### Changed — Issue #56 разбиение draft-файла на 23 промпта со стандартизованной схемой именования

- Файл `prompts/drafts/Промпт+для+БА (1).md` (созданный в issue #54 как единый
  draft) разбит на **23 отдельных промпта** по схеме `[домен]-[операция]-[режим].md`
  (kebab-case). **18 новых** промптов размещены в [`prompts/`](prompts/)
  (`status: draft`, `version: 0.1`); **5 legacy-промптов из PDF** также размещены
  в [`prompts/`](prompts/) с суффиксом `-legacy` (`status: draft`, `version: 1.0`),
  так как продолжают использоваться; **6 старых canonical-промптов** перенесены в
  [`prompts/archive/`](prompts/archive/) с суффиксом `-legacy` (`status: archived`,
  `version: 1.0`). Текст каждого промпта скопирован **дословно** (проверено
  побайтово против исходного среза); добавлены обязательный frontmatter (`status`,
  `version`, `updated: 2026-06-11`, `temperature: 0.1`) и experimental marker сразу
  после него.
- **Операции** взяты из таксономии 13 когнитивных операций БА: `understanding`
  (контекст/глоссарий §2, уточняющие вопросы §9.1), `documentation` (ФТ §3.1,
  ограничения §4, резюме встреч §7–8, сопроводительное письмо §9.2), `validation`
  (валидация ФТ §3.2), `solution-design` (системно-технические требования §5),
  `modeling` (User Story §6.1, Use Case §6.2), `ingestion` (пост-обработка ASR §10).
- **Режимы.** Токены `stepwise` (Экспертный, пошаговое согласование) / `oneshot`
  (Экспресс, one-shot) / `legacy` (архивный) выбраны по результатам международного
  исследования (Пользователь допустил «другой режим по результатам исследования»):
  `expert`/`express` не являются стандартной терминологией, а «expert» коллидирует
  с role-prompting-идиомой «act as an expert»; `stepwise` уже используется в
  репозитории (`usecase-stepwise-generator-simple.md`) и совпадает с формулировками
  источника («пошаговый» / «one-shot»). Обоснование и ссылки — в описании PR #57.
- **Removed.** Исходный файл `prompts/drafts/Промпт+для+БА (1).md` удалён **только
  после** успешного создания и побайтовой верификации всех 23 файлов; опустевший
  каталог `prompts/drafts/` удалён. Запись CHANGELOG issue #54 о создании draft
  сохранена как исторический факт — данный шаг её сознательно замещает.

### Added — Issue #54 миграция прикреплённого файла промптов в `prompts/drafts/`

- Создан [`prompts/drafts/Промпт+для+БА (1).md`](prompts/drafts/) — миграция
  единственного файла, прикреплённого к issue #54 (`Промпт+для+БА (1).pdf`, СПИСОК
  ПРОМПТОВ для бизнес-анализа в Телеком SaaS). По правилу issue «один прикреплённый
  файл = один файл в репозитории» PDF перенесён как один draft без разбиения на
  отдельные промпты. Текст промптов скопирован из PDF без изменений; добавлены
  обязательный frontmatter (`status: draft`, `version: 0.1`, `updated: 2026-06-10`,
  `temperature: 0.1`) и experimental marker `<!-- EXPERIMENTAL: DO NOT USE IN PRODUCTION -->`.
- Для draft-файла требуется issue `prompt:review` (labels `prompt:review`, `draft`).
  Создание выполняется мейнтейнером: у автоматизации нет прав `triage`/`push` на
  upstream для применения labels (заготовка issue приведена в описании PR).

### Changed — Issue #48 обогащение `AI_SESSION_HANDOVER_PROMPT.md` (роль члена команды и проверка шаблонов)

- [`AI_SESSION_HANDOVER_PROMPT.md`](AI_SESSION_HANDOVER_PROMPT.md) дополнен командной
  рамкой (issue #48), `version` 0.3 → 0.4. Готовый prompt теперь открывается рамкой
  «ИИ в чате — **член команды** (C, Q, G, D, O), а не «исполнитель без доступа»;
  прямые изменения в репо — через Конарда». В Шаг 2 (ЧЕК-ЛИСТ КОНТЕКСТА) добавлена
  проверка предыдущего контекста чата; в Шаг 3 (READBACK) — учёт канала взаимодействия
  с репо и проверки шаблонов. Добавлены разделы «💬 Контекст чата диалога»,
  «🤝 Роль и канал взаимодействия с репо», «🔍 Проверка шаблонов» и «📝 Формат
  постановки задач для Конарда».
- **Осознанное расхождение с Хабом.** Правки внесены локально поверх базового шаблона
  Хаба [`templates/htom/AI_SESSION_HANDOVER_PROMPT.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/117e4a553815af9b05d841c81dd725dd4a4c4d44/templates/htom/AI_SESSION_HANDOVER_PROMPT.md)
  (SHA `117e4a55`), который этих разделов пока не содержит (проверено: шаблон в `main`
  Хаба идентичен закреплённому SHA). По политике source-of-truth расширение подлежит
  переносу в Хаб с последующей синхронизацией сюда. Ссылка на `templates/task-for-konard.md`
  указывает на ещё не созданный артефакт Хаба (см. PR-описание и issue #48). Провенанс
  (`source_hub`/`source_sha`) и структура EXECUTION/EXPLANATION сохранены.
- Создан [`docs/adr/0002-issue48-handover-local-enrichment.md`](docs/adr/0002-issue48-handover-local-enrichment.md):
  ADR фиксирует осознанные отклонения от буквы issue #48 (аддитивное обогащение вместо
  замены файла, реализация намерения в фактической структуре, условные ссылки на
  отсутствующие шаблоны) и follow-up на перенос расширения в Хаб (Hub-first).

### Added — Issue #46 governance sync with Hub (PR #208)

- Создан корневой артефакт онбординга
  [`AI_SESSION_HANDOVER_PROMPT.md`](AI_SESSION_HANDOVER_PROMPT.md) — готовый к
  копированию *Handover Prompt* для запуска ИИ-агента в новой сессии. Источник —
  Хаб `templates/htom/AI_SESSION_HANDOVER_PROMPT.md`, закреплён permalink-ом на
  merge-SHA PR #208 `117e4a553815af9b05d841c81dd725dd4a4c4d44`. Плейсхолдеры
  `{{REPO_NAME}}`/`{{project_name}}`/`{{hub_url}}` инстанцированы под mango; Шаг 1
  читает реально присутствующие локальные контракты команды, фундаментальные
  governance-контракты Хаба — по permalink-ам.
- Создан протокол онбординга
  [`governance/agent-onboarding-protocol.md`](governance/agent-onboarding-protocol.md)
  (kebab-case, адаптированная копия канонического протокола Хаба v1.2): семантическое
  разделение «артефакт ↔ протокол» из PR #208. Раздел Design Rationale сжат,
  полная история вынесена ссылкой на Хаб.
- Создан профиль Smart Sync [`.hub-profile.json`](.hub-profile.json) с ключами,
  которые фактически читает `tools/sync-from-hub.sh` Хаба
  (`target_type` / `phase` / `stack` / `hub_url` / `last_sync`).
- Создан [`docs/adr/0001-hub-sync-pr208.md`](docs/adr/0001-hub-sync-pr208.md):
  ADR фиксирует 8 осознанных отклонений от буквы issue (схема профиля, путь
  онбординга, терминология HTOM, подстановка `{{REPO_NAME}}`, Anti-Inflation по
  `tools/`, DoD без валидатора, исправление пути глоссария, permalink-провенанс) и
  сохранённые mango-специфичные правила.
- Добавлены строки навигации в [`README.md`](README.md) на оба новых
  онбординг-файла.

### Changed — sync `AI_GOVERNANCE.md` / `AI_QUICK_RULES.md` from `templates/htom/`

- [`AI_GOVERNANCE.md`](AI_GOVERNANCE.md) синхронизирован с Хабом
  `templates/htom/AI_GOVERNANCE.md` (SHA `117e4a55`): принята терминология
  **«HTOM-команда»**, добавлен provenance (`source_hub`/`source_sha`). Сохранена
  mango-специфичная taxonomy **«Capability Boundaries»** (с реальными путями и
  ссылкой на fail-closed) поверх общей хабовой рубрики. Исправлен стэйл-путь
  `kb/glossary.md` → `standards/GLOSSARY.md`. Строка DoD про
  `./tools/validate-repository-structure.sh` заменена на ориентир
  `docs/audit/initial-state-2026-06.md` (валидатора в mango нет — Anti-Inflation).
- [`AI_QUICK_RULES.md`](AI_QUICK_RULES.md) синхронизирован с Хабом
  `templates/htom/AI_QUICK_RULES.md` (SHA `117e4a55`): терминология
  **«HTOM-команда»**, provenance, различение HTOM-команда ↔ spoke-репозиторий.
  Сохранена явная секция **«Fail-Closed Semantics (КРИТИЧНО)»** (шаблон Хаба её
  свернул), чтобы оставалась резолвимой перекрёстная ссылка из `AI_GOVERNANCE.md`.

### Added — M-009 migration manifest

- Создан живой снимок миграции `governance/migration-manifest.md` (творческое
  улучшение C6 RFC). Содержит таблицу «артефакт → категория → действие → статус →
  назначение в споке» (RFC §5.1) и чек-лист-трекер «Перенесено / Осталось в
  Хабе / Требует уточнения» (RFC §5.3). Зафиксированы 6 промптов, 2 стандарта и
  5 экспериментов как `migrated`, 11 research-артефактов как `referenced`,
  монорепо-`README.md` как `archived` (E3) и 4 пустых плейсхолдера как
  `not-migrated` (P5). Все ссылки на Хаб закреплены permalink-ом на snapshot
  `038868dd125b4e2d849ff73604890f1d2787ac0f` (C3). Манифест ведётся по ходу
  Фаз 0–3 и закрывается в Фазе 3.
### Added — M-007 hub research dependency registry

- Создан единый реестр зависимостей от research Хаба
  `docs/hub-research-dependencies.md` (заголовок «Реестр зависимостей от
  исследований Хаба»). Файл-дубль `hub-research-links.md` не создаётся
  (запрет RFC §3.5).
- Заведены якоря на каждый артефакт `research/mango/*` (`#classification`,
  `#classification-tz`, `#taxonomy-concept`, `#requirements-flow`,
  `#requirements-lifecycle`, `#capability-decomposition`, `#rag-mapping`,
  `#research-readme`) с полным permalink на SHA
  `038868dd125b4e2d849ff73604890f1d2787ac0f` и списком consumers. Промпты и
  контракт классификации резолвят `research_dep` через эти якоря (E1, E8).

### Added — M-006 prompt frontmatter normalization

- Перенесены и нормализованы 6 prompt assets Mango в `prompts/`:
  `tz-stats-generator.md`, `tz-stats-generator-simple.md`,
  `user-story-generator.md`, `user-story-generator-simple.md`,
  `usecase-stepwise-generator.md` и `usecase-stepwise-generator-simple.md`.
  Каждый файл получил 7 обязательных frontmatter-полей, provenance
  (`source_hub`, `source_sha`, `based_on`), явные настройки запуска
  (`temperature: 0.1`, `output_format: markdown`) и отметку
  `migration_status: migrated` после self-test gate.
- Для `_exp`/canonical-вариантов добавлен явный раздел «ФОРМАТ ВЫВОДА»; для
  standalone `_simple`-вариантов с `research_dep: none` добавлен комментарий о
  бизнес-задаче и отсутствии формальной research-зависимости.

### Added — M-004 product classification contract

- Перенесён Mango-only контракт классификации из Хаба в
  `standards/product-classification-contract.md` (переименование из
  `projects/mango/standards/classification-glossary.md`, snapshot
  `038868dd125b4e2d849ff73604890f1d2787ac0f`). Контракт отделён от
  `standards/GLOSSARY.md`, содержит provenance (`source_hub`, `source_sha`) и
  использует `research_dep`-якоря будущего реестра
  `docs/hub-research-dependencies.md` вместо Hub-relative research-ссылок.

### Added — Phase 1 migration scaffold

- Перенесены 5 продуктовых экспериментов Mango из зафиксированного snapshot
  Хаба (`038868dd125b4e2d849ff73604890f1d2787ac0f`) в
  `prompts/experiments/` для M-005: прототип ТЗ-статистики, stepwise alignment
  use-case генератора, генератор user story из raw request, аудит промптов и
  self-test сценарий `prompts-selftest-2026-05-26.md`.
- Создан базовый каркас каталогов Фазы 1 (`prompts/`,
  `prompts/experiments/`, `prompts/archive/`, `standards/`, `kb/`, `docs/`,
  `docs/adr/`, `docs/audit/`) с поясняющими `.gitkeep`-файлами для M-002.
- Скопирован `standards/GLOSSARY.md` из Хаба для M-003: файл закреплён за
  permalink на SHA `038868dd125b4e2d849ff73604890f1d2787ac0f`, содержит
  `source_hub`/`source_sha` и фиксирует, что source of truth остаётся в Хабе,
  а синхронизация выполняется явным действием спока.

### Added — Initial repository structure based on hybrid-Intelligence-lab templates

- Инициализация спока `mango_ba_prompts` из «ДНК-шаблона» Хаба
  (`templates/spoke/`): базовый геном (governance, quick rules, навигация,
  каркасы `docs/adr/`, `docs/audit/`, база знаний `kb/glossary.md`).
- «Бесплатные» улучшения из анализа рекомендаций команд C и Q:
  fail-closed semantics в `AI_QUICK_RULES.md` и capability taxonomy в
  `AI_GOVERNANCE.md`.
- RFC стратегии миграции проекта Mango из Хаба в спок
  (`docs/analysis/migration-strategy-rfc.md`, issue #8): аудит 23 артефактов
  Хаба по полным URL, фазовая стратегия (Mermaid), edge cases, креативные
  улучшения и триггеры эволюции. Стоп-фактор: физический перенос — после
  Human Review.

### Changed

- Добавлен временный workflow создания промптов в `CONTRIBUTING.md` (issue #35,
  M-008): ровно 5 шагов `draft → frontmatter → marker → prompt:review →
  canonical`, capability boundary `prompts/drafts/` и минимальный пример
  frontmatter для черновика без введения матрицы или ADR-процесса.
- Переписан корневой `README.md` под standalone-спок (issue #28, M-001, v2.0):
  README теперь описывает `mango_ba_prompts` как **библиотеку промптов для
  бизнес-аналитиков** (ТЗ-статистика, use-case, user story), а не как базу
  знаний. Добавлены quickstart по чтению frontmatter промптов, структура
  `prompts/` и `standards/`, навигация на `CONTRIBUTING.md` и контакты/роли.
  Удалены унаследованные из «ДНК-шаблона» Хаба прямые и hub-относительные
  ссылки; единственный мост в Хаб — через `docs/hub-research-dependencies.md`.
- Уточнён RFC стратегии миграции (`docs/analysis/migration-strategy-rfc.md`,
  issue #10): добавлена таблица файлов Фазы 1, чек-лист нормализации промптов,
  единый реестр research-зависимостей, корректное разделение
  `standards/GLOSSARY.md` и `standards/product-classification-contract.md`,
  а также правила переноса продуктовых экспериментов.
- Зафиксированы решения Пользователя по Q1–Q4 в RFC миграции
  (`docs/analysis/migration-strategy-rfc.md`, issue #21): таблица Фазы 1
  утверждена, Hub-ссылки должны быть permalink на SHA, self-test стал
  обязательным gate для статуса `migrated`, а стандарты, промпты, эксперименты и
  `hub-research-dependencies.md` идут одним PR Фазы 1.
- Завершена доработка RFC (`docs/analysis/migration-strategy-rfc.md`,
  issue #12, v0.3, блоки 3–8): реестр зависимостей от исследований Хаба (§3.5),
  переписка README.md как обязательная задача Фазы 1, согласованные формулировки
  edge cases E5 (все эксперименты — часть продукта) и E6 (разделение
  глоссария и контракта классификации, §4.1), временный workflow промптов P0
  для `CONTRIBUTING.md` (§5.2) и шаблон Migration Manifest (§5.3).
- Human Review доработанного RFC миграции
  (`docs/reviews/migration-rfc-human-review-2026-06.md`, issue #13): сверка
  v0.3 против чек-листа из 11 пунктов (архитектурная целостность, операционная
  готовность, трассируемость) — все пункты пройдены; зафиксированы открытые
  вопросы Q1–Q4 на решение Пользователя перед стартом Фазы 0.
- Сформирован операционный бэклог Фазы 1 миграции
  (`governance/BACKLOG.md`, issue #14): 9 атомарных задач (M-001…M-009) с
  приоритетами, зависимостями, DoD и трассировкой на разделы утверждённого RFC,
  плюс Mermaid-диаграмма критического пути. Бэклог = один файл (Anti-Inflation);
  выполнение задач не начато.
- Материализован бэклог Фазы 1 в 9 готовых к созданию GitHub Issues
  (`governance/migration-phase1-issues.md`, issue #23): каждый пункт M-001…M-009
  оформлен по стандарту Хаба `ISSUE_WORKFLOW.md` (шаблон `task.yml`) с явным
  Operating Mode (`Creative`/`Structured`), приоритетом, зависимостями, DoD,
  трассировкой на RFC/бэклог и полными permalink-ссылками на Хаб (SHA
  `038868dd…`, решение Q2). Live-Issues создаёт человек при ревью (среда
  AI-агента имеет только `pull`-доступ; создание Issues — fail-closed,
  outward-facing). Сами задачи бэклога не выполняются.

### Removed

- Удалён `kb/glossary.md`: каталог `kb/` сохранён для практик, примеров и
  справочников; глоссарий будет заменён стандартом `standards/GLOSSARY.md` в
  M-003.
- Удалён placeholder `prompts/.gitkeep`: каталог `prompts/` теперь содержит
  реальные нормализованные prompt assets.
- Удалён placeholder `standards/.gitkeep`: каталог `standards/` теперь содержит
  реальный стандарт `standards/GLOSSARY.md`.
- Удалён технический корневой `.gitkeep`, созданный только для bootstrap PR.
