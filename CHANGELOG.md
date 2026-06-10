---
status: draft
version: 0.1
updated: 2026-06-02
ai-generated: true
---

# Changelog — mango_ba_prompts

Все значимые изменения проекта документируются здесь. Формат основан на
[Keep a Changelog](https://keepachangelog.com/ru/1.1.0/); проект придерживается
[Semantic Versioning](https://semver.org/lang/ru/).

## Unreleased

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
- Зафиксированы решения фаундера по Q1–Q4 в RFC миграции
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
  вопросы Q1–Q4 на решение фаундера перед стартом Фазы 0.
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
