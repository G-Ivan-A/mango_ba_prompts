---
status: draft
version: 0.1
updated: 2026-06-04
ai-generated: true
type: issue-set
scope: mango_ba_prompts-migration-execution
based_on: "pr-ops/BACKLOG.md"
rfc: "docs/analysis/migration-strategy-rfc.md"
issue: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/23"
hub_snapshot_sha: "038868dd125b4e2d849ff73604890f1d2787ac0f"
---

# Migration Phase 1 — 9 executable issues (M-001 … M-009)

> 📋 **Это «материализация» бэклога, а не его выполнение.** Файл превращает
> 9 пунктов [`pr-ops/BACKLOG.md`](BACKLOG.md) в готовые к созданию GitHub
> Issues по стандарту Хаба
> [`standards/ISSUE_WORKFLOW.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/038868dd125b4e2d849ff73604890f1d2787ac0f/standards/ISSUE_WORKFLOW.md)
> (шаблон
> [`.github/ISSUE_TEMPLATE/task.yml`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/038868dd125b4e2d849ff73604890f1d2787ac0f/.github/ISSUE_TEMPLATE/task.yml)).
> Сам перенос файлов из Хаба **не выполняется** здесь (Anti-Inflation, RFC §1.2;
> Stop-factor бэклога). Каждый раздел ниже — точный текст одной будущей Issue.

## Как использовать этот файл

1. Этот PR проходит **Human Review** (режим задачи — `Creative`, см.
   [issue #23](https://github.com/G-Ivan-A/mango_ba_prompts/issues/23)).
2. После апрува Пользователь/мейнтейнер (у кого есть write-доступ) создаёт 9 Issues,
   копируя блоки `M-001 … M-009` как тело каждой Issue.
3. AI-агент намеренно **не создаёт** живые Issues автоматически: у среды
   исполнения только `pull`-доступ к `G-Ivan-A/mango_ba_prompts`, а создание
   Issues/меток — outward-facing действие, которое по
   [`AI_GOVERNANCE.md`](../AI_GOVERNANCE.md) (fail-closed) подтверждается
   человеком.

## Соглашения для всех 9 задач

- **Snapshot Хаба (Q2 — permalink на SHA).** Все ссылки на Хаб — абсолютные
  permalink'и на коммит
  `038868dd125b4e2d849ff73604890f1d2787ac0f`; ссылки на `main` запрещены
  (RFC §8 / Q2). Относительные пути на Хаб (`../...`, `projects/mango/...`)
  запрещены (issue #23, «ТЕХНИЧЕСКОЕ ТРЕБОВАНИЕ»).
- **Имя контракта.** Везде только `standards/product-classification-contract.md`
  (kebab-case, не CAPS LOCK).
- **Operating Mode.** Указан в каждой задаче (`Creative` / `Structured`) — см.
  таблицу-сводку.
- **Трассируемость.** Каждая задача ссылается на раздел RFC и пункт бэклога.
- **Anti-Inflation.** Ровно 9 задач, без «задач на вырост».

## Сводная таблица

| ID | Название | Mode | Приоритет | Зависимости | Бэклог |
|----|----------|------|-----------|-------------|--------|
| M-001 | Переписать `README.md` спока | `Creative` | P0 | — | [§3 M-001](BACKLOG.md) |
| M-002 | Создать базовую структуру папок | `Structured` | P0 | — | [§3 M-002](BACKLOG.md) |
| M-003 | Скопировать `standards/GLOSSARY.md` из Хаба | `Structured` | P0 | M-002 | [§3 M-003](BACKLOG.md) |
| M-004 | Перенести → `standards/product-classification-contract.md` | `Structured` | P0 | M-002 | [§3 M-004](BACKLOG.md) |
| M-005 | Перенести эксперименты в `prompts/experiments/` | `Structured` | P0 | M-002 | [§3 M-005](BACKLOG.md) |
| M-006 | Нормализовать frontmatter промптов (7 полей + provenance) | `Creative` | P1 | M-002, M-003, M-004, M-005 | [§3 M-006](BACKLOG.md) |
| M-007 | Создать `docs/hub-research-dependencies.md` | `Structured` | P1 | M-006 | [§3 M-007](BACKLOG.md) |
| M-008 | Добавить временный workflow в `CONTRIBUTING.md` | `Creative` | P0 | — | [§3 M-008](BACKLOG.md) |
| M-009 | Создать Migration Manifest (`docs/migration-manifest.md`) | `Creative` | P2 | M-006 | [§3 M-009](BACKLOG.md) |

**Критический путь:** `M-002 → (M-003 ∥ M-004 ∥ M-005) → M-006 → (M-007 ∥ M-009)`.
M-001 и M-008 независимы и идут параллельно.

---

## M-001 — Переписать `README.md` спока

**Title:** `[M-001] docs: переписать README.md спока с нуля под Mango BA Prompts`

**Labels:** `migration` | `creative` | `priority:P0`
**Milestone:** `Sprint 3 — Hybrid Minimum Bootstrap`
**User Story / ФТ:** `project:mango_ba_prompts-migration-execution`
**Linked Backlog:** [`pr-ops/BACKLOG.md` → M-001](BACKLOG.md)
**Depends On:** —
**Operating Mode:** `Creative`

### 🎯 Контекст

Текущий `README.md` унаследован из «ДНК-шаблона» Хаба и неактуален для спока:
он не объясняет, что `mango_ba_prompts` — это **библиотека промптов для
бизнес-аналитиков**, а не база знаний. Трассируемость: RFC §3.2 (строка
`README.md` — действие «Не переносить», обновить навигацию) и edge case E3 (§4);
бэклог M-001.

**Креативная рекомендация (mode `Creative`).** Спроектируй структуру README так,
чтобы она сразу отвечала на 3 вопроса читателя:
1. «Что это за библиотека?» — назначение: готовые промпты для БА (ТЗ, use-case,
   user story), а не исследования.
2. «Как начать использовать промпты?» — короткий quickstart: где лежат
   `prompts/`, как читать frontmatter, где `prompts/experiments/`.
3. «Где искать правила?» — навигация на `CONTRIBUTING.md` (временный workflow),
   `standards/`, `AI_GOVERNANCE.md`, `AI_QUICK_RULES.md`.

Подчеркни: `prompts/` = **инструменты для БА**, `kb/` = практики/справочники, а
**не** стандарт; единственный мост в Хаб — через
[`docs/hub-research-dependencies.md`](../docs/hub-research-dependencies.md) (M-007).

### 📄 Артефакты для создания/изменения

- [ ] Переписать корневой `README.md` (назначение, структура `prompts/` и
      `standards/`, ссылка на временный workflow `CONTRIBUTING.md`, контакты).
- [ ] Удалить все hub-относительные и битые ссылки.

### ✅ Готово, когда

- [ ] `README.md` описывает назначение спока и структуру `prompts/`/`standards/`.
- [ ] Нет hub-относительных и битых ссылок (`../../standards/...` и т. п.).
- [ ] Единственная ссылка на Хаб — через `docs/hub-research-dependencies.md`.
- [ ] Есть ссылка на `CONTRIBUTING.md` (временный workflow).
- [ ] Запись добавлена в `CHANGELOG.md` (`## Unreleased`).

---

## M-002 — Создать базовую структуру папок проекта

**Title:** `[M-002] structure: создать базовую структуру каталогов спока`

**Labels:** `migration` | `structured` | `priority:P0`
**Milestone:** `Sprint 3 — Hybrid Minimum Bootstrap`
**User Story / ФТ:** `project:mango_ba_prompts-migration-execution`
**Linked Backlog:** [`pr-ops/BACKLOG.md` → M-002](BACKLOG.md)
**Depends On:** —
**Operating Mode:** `Structured`

### 🎯 Контекст

Базовый каркас Фазы 1. Трассируемость: RFC §3.1, edge case E6; бэклог M-002.
Каталог `kb/` уже существует (содержит `kb/glossary.md`) — его нельзя дублировать
и нельзя превращать в стандарт (E6). Существующий `kb/glossary.md` удаляется в
этой задаче и будет заменён копией глоссария Хаба в `standards/GLOSSARY.md`
после M-003.

### 📄 Артефакты для создания/изменения

- [ ] Создать каталоги: `prompts/`, `prompts/experiments/`, `prompts/archive/`,
      `standards/`, `kb/`, `docs/`, `docs/adr/`, `docs/audit/`.
- [ ] В каждом каталоге создать `.gitkeep` с поясняющим комментарием о
      назначении.
- [ ] Если `kb/glossary.md` существует — удалить его.
- [ ] Убедиться, что `standards/` создан как отдельный каталог для стандартов
      (глоссарий + контракт классификации).
- [ ] `kb/` сохранить как каталог практик/справочников (не стандарт, E6).

### ✅ Готово, когда

- [ ] Все 8 каталогов существуют, каждый с `.gitkeep` и комментарием.
- [ ] `kb/glossary.md` удалён, если существовал.
- [ ] `kb/` существует и пуст, готов для будущих практик.
- [ ] `standards/` существует и готов для M-003/M-004.
- [ ] Запись добавлена в `CHANGELOG.md` (`## Unreleased`).

---

## M-003 — Скопировать `standards/GLOSSARY.md` из Хаба

**Title:** `[M-003] standards: скопировать standards/GLOSSARY.md из Хаба (permalink на SHA)`

**Labels:** `migration` | `structured` | `priority:P0`
**Milestone:** `Sprint 3 — Hybrid Minimum Bootstrap`
**User Story / ФТ:** `project:mango_ba_prompts-migration-execution`
**Linked Backlog:** [`pr-ops/BACKLOG.md` → M-003](BACKLOG.md)
**Depends On:** M-002
**Operating Mode:** `Structured`

### 🎯 Контекст

Синхронизация единого словаря терминов. Source of truth остаётся в Хабе;
копия в споке — снимок на зафиксированный SHA (принцип P2, RFC §2.4; edge case
E6 / §4.1; бэклог M-003).

**Источник (permalink на SHA, Q2):**
`https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/038868dd125b4e2d849ff73604890f1d2787ac0f/standards/GLOSSARY.md`

### 📄 Артефакты для создания/изменения

- [ ] Скопировать содержимое из источника выше в `standards/GLOSSARY.md` спока.
- [ ] Обновить frontmatter (`version`, `updated`).
- [ ] Добавить provenance: `source_hub` (полный permalink) + `source_sha:
      038868dd125b4e2d849ff73604890f1d2787ac0f`.

### ✅ Готово, когда

- [ ] Файл `standards/GLOSSARY.md` присутствует в споке.
- [ ] Указаны `source_hub` и `source_sha` (permalink на коммит, не `main`).
- [ ] Файл — словарь терминов; классификация в него не смешана (E6).
- [ ] Запись добавлена в `CHANGELOG.md` (`## Unreleased`).

---

## M-004 — Перенести и переименовать `classification-glossary` → `standards/product-classification-contract.md`

**Title:** `[M-004] standards: перенести классификацию в standards/product-classification-contract.md (kebab-case)`

**Labels:** `migration` | `structured` | `priority:P0`
**Milestone:** `Sprint 3 — Hybrid Minimum Bootstrap`
**User Story / ФТ:** `project:mango_ba_prompts-migration-execution`
**Linked Backlog:** [`pr-ops/BACKLOG.md` → M-004](BACKLOG.md)
**Depends On:** M-002
**Operating Mode:** `Structured`

### 🎯 Контекст

Перенос контракта классификации с переименованием в kebab-case. Трассируемость:
RFC принцип P4 (§1.2), §2.3, edge cases E2 и E6 / §4.1; бэклог M-004. Контракт
и глоссарий не сливаются (E6): контракт ссылается на `standards/GLOSSARY.md`.

**Источник (permalink на SHA, Q2):**
`https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/038868dd125b4e2d849ff73604890f1d2787ac0f/projects/mango/standards/classification-glossary.md`

### 📄 Артефакты для создания/изменения

- [ ] Перенести файл-источник в `standards/product-classification-contract.md`
      (переименование, kebab-case; **не** в `kb/`, **не** `glossary`).
- [ ] Внутренние ссылки на research заменить на `research_dep`/якоря реестра
      [`docs/hub-research-dependencies.md`](../docs/hub-research-dependencies.md)
      (см. M-007; E1, E8) — без относительных путей.
- [ ] Добавить взаимную ссылку на `standards/GLOSSARY.md` («Для значений
      терминов см. …», E6).
- [ ] Добавить provenance (`source_hub`, `source_sha:
      038868dd125b4e2d849ff73604890f1d2787ac0f`).

### ✅ Готово, когда

- [ ] Файл размещён как `standards/product-classification-contract.md`.
- [ ] Контракт ссылается на `standards/GLOSSARY.md`; слияние не выполнено (E6).
- [ ] Ссылки на research идут через `research_dep`/реестр, не относительными
      путями (E1).
- [ ] Указаны `source_hub` и `source_sha`.
- [ ] Запись добавлена в `CHANGELOG.md` (`## Unreleased`).

---

## M-005 — Перенести эксперименты в `prompts/experiments/`

**Title:** `[M-005] migration: перенести 5 экспериментов Mango в prompts/experiments/`

**Labels:** `migration` | `structured` | `priority:P0`
**Milestone:** `Sprint 3 — Hybrid Minimum Bootstrap`
**User Story / ФТ:** `project:mango_ba_prompts-migration-execution`
**Linked Backlog:** [`pr-ops/BACKLOG.md` → M-005](BACKLOG.md)
**Depends On:** M-002
**Operating Mode:** `Structured`

### 🎯 Контекст

Эксперименты — **часть продукта** спока, а не исследования Хаба (edge case E5,
RFC §4.1; §2.3, §2.6; бэклог M-005). Поэтому переносятся физически в
`prompts/experiments/`, а не регистрируются как research-ссылки.

**Источники (permalink на SHA, Q2) — 5 файлов из
`https://github.com/G-Ivan-A/hybrid-Intelligence-lab/tree/038868dd125b4e2d849ff73604890f1d2787ac0f/projects/mango/experiments`:**

- `…/blob/038868dd125b4e2d849ff73604890f1d2787ac0f/projects/mango/experiments/tz-stats-prototype-2026-05.md`
- `…/blob/038868dd125b4e2d849ff73604890f1d2787ac0f/projects/mango/experiments/usecase_gen-stepwise-alignment_2026-05-26.md`
- `…/blob/038868dd125b4e2d849ff73604890f1d2787ac0f/projects/mango/experiments/user-story_gen-from-raw-request_2026-05-26.md`
- `…/blob/038868dd125b4e2d849ff73604890f1d2787ac0f/projects/mango/experiments/prompts-audit-2026-05-26.md`
- `…/blob/038868dd125b4e2d849ff73604890f1d2787ac0f/projects/mango/experiments/prompts-selftest-2026-05-26.md`

> Полный базовый URL:
> `https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/038868dd125b4e2d849ff73604890f1d2787ac0f/projects/mango/experiments/<file>`

### 📄 Артефакты для создания/изменения

- [ ] Перенести все 5 файлов в `prompts/experiments/` спока.
- [ ] **Не** размещать `prompts-selftest-2026-05-26.md` в корневом
      `experiments/` — только в `prompts/experiments/` (RFC §3.2).
- [ ] Добавить provenance-поля (`source_hub`, `source_sha`).
- [ ] Если фактическое имя в snapshot отличается — заменить на подтверждённый
      Hub-путь (Q1, RFC §7/§8).

### ✅ Готово, когда

- [ ] Все 5 экспериментов присутствуют в `prompts/experiments/`.
- [ ] `prompts-selftest-2026-05-26.md` доступен как acceptance-сценарий для
      M-006 (self-test gate, C2).
- [ ] Эксперименты **не** зарегистрированы как research-ссылки (E5).
- [ ] Provenance заполнен у каждого файла.
- [ ] Запись добавлена в `CHANGELOG.md` (`## Unreleased`).

---

## M-006 — Нормализовать frontmatter у всех промптов (7 полей + provenance)

**Title:** `[M-006] prompts: нормализовать frontmatter (7 полей + provenance + self-test gate)`

**Labels:** `migration` | `creative` | `priority:P1`
**Milestone:** `Sprint 3 — Hybrid Minimum Bootstrap`
**User Story / ФТ:** `project:mango_ba_prompts-migration-execution`
**Linked Backlog:** [`pr-ops/BACKLOG.md` → M-006](BACKLOG.md)
**Depends On:** M-002, M-003, M-004, M-005
**Operating Mode:** `Creative`

### 🎯 Контекст

Приведение промптов к единому стандарту RFC §2.3 / §3.2 («Чек-лист нормализации
промпта»); креативные улучшения C1 (provenance + dependency frontmatter, §5) и
C2 (self-test gate); бэклог M-006. Self-test (Q3) — **обязательный** критерий
пометки промпта `migrated`.

**Источники (permalink на SHA, Q2) — 6 промптов из
`https://github.com/G-Ivan-A/hybrid-Intelligence-lab/tree/038868dd125b4e2d849ff73604890f1d2787ac0f/projects/mango/prompts`:**

- `tz-stats-generator_exp-2026-05.md`, `tz-stats-generator_simple-2026-05.md`
- `usecase-stepwise-generator_exp-2026-05.md`, `usecase-stepwise-generator_simple-2026-05.md`
- `user-story-generator_exp-2026-05.md`, `user-story-generator_simple-2026-05.md`

> Базовый URL:
> `https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/038868dd125b4e2d849ff73604890f1d2787ac0f/projects/mango/prompts/<file>`

**Креативная рекомендация (mode `Creative`).** Если промпт не зависит от
исследований — явно проставь `research_dep: none` **и** добавь комментарий о
бизнес-задаче (зачем промпт нужен). Для зависимых промптов — `research_dep:
docs/hub-research-dependencies.md#<anchor>` (anchors заводятся в M-007). Прогон
self-test из `runs/2026/RUN-0005/outputs/prompts-selftest-2026-05-26.md` — обязательный
gate перед статусом `migrated` (Q3).

### 📄 Артефакты для создания/изменения

- [ ] Перенести 6 промптов в `prompts/` (нормализованные имена — Q1, RFC §7/§8).
- [ ] У каждого файла — 7 обязательных полей frontmatter: `status`, `version`,
      `updated`, `temperature`, `output_format`, `glossary_ref`, `research_dep`.
- [ ] Provenance-поля: `source_hub`, `source_sha`, `based_on` (C1).
- [ ] `_exp`/canonical-варианты содержат явный раздел «ФОРМАТ ВЫВОДА».
- [ ] Прогнать self-test, зафиксировать результат.

### ✅ Готово, когда

- [ ] Все промпты в `prompts/` имеют 7 полей frontmatter + provenance.
- [ ] Нет промптов без `glossary_ref` или `research_dep`; `temperature` явный.
- [ ] `research_dep: none` сопровождается комментарием о бизнес-задаче.
- [ ] `_exp`/canonical-промпты содержат раздел «ФОРМАТ ВЫВОДА».
- [ ] Self-test пройден; промпты помечены `migrated` только после прохождения.
- [ ] Запись добавлена в `CHANGELOG.md` (`## Unreleased`).

---

## M-007 — Создать `docs/hub-research-dependencies.md`

**Title:** `[M-007] docs: создать единый реестр docs/hub-research-dependencies.md`

**Labels:** `migration` | `structured` | `priority:P1`
**Milestone:** `Sprint 3 — Hybrid Minimum Bootstrap`
**User Story / ФТ:** `project:mango_ba_prompts-migration-execution`
**Linked Backlog:** [`pr-ops/BACKLOG.md` → M-007](BACKLOG.md)
**Depends On:** M-006
**Operating Mode:** `Structured`

### 🎯 Контекст

Единый реестр зависимостей спока от исследований Хаба. Трассируемость: RFC §3.5
(носитель — **только** `docs/hub-research-dependencies.md`), §2.5 (инвентарь
research), креативное улучшение C4 (§5); edge cases E1, E8; бэклог M-007.
⚠️ **Не** создавать `hub-research-links.md` — это запрещённый дубль (RFC §3.5).

**Источник аудита (research/mango, permalink на SHA, Q2):**
`https://github.com/G-Ivan-A/hybrid-Intelligence-lab/tree/038868dd125b4e2d849ff73604890f1d2787ac0f/research/mango`

Кандидаты-якоря (заполняются по §2.5; каждый — с полным Hub-permalink и списком
consumers):
`#classification`, `#classification-tz`, `#taxonomy-concept`,
`#requirements-flow`, `#requirements-lifecycle`, `#capability-decomposition`,
`#rag-mapping`.

### 📄 Артефакты для создания/изменения

- [ ] Создать `docs/hub-research-dependencies.md` с заголовком
      `# Реестр зависимостей от исследований Хаба`.
- [ ] Таблица: `Название | Полный URL в Хабе (permalink на SHA) | Тип
      зависимости | Версия/Дата | Статус синхронизации | Затронутые артефакты
      спока | Примечание`.
- [ ] Завести якоря, на которые ссылаются промпты (M-006) и контракт (M-004)
      через `research_dep`.

### ✅ Готово, когда

- [ ] Файл `docs/hub-research-dependencies.md` создан как единая точка ссылок.
- [ ] Файл `hub-research-links.md` **не** создан (RFC §3.5).
- [ ] Каждый якорь имеет полный Hub-permalink (на SHA, C3) и список consumers.
- [ ] Каждый промпт/контракт с зависимостью ссылается на якорь через
      `research_dep` (E1, E8).
- [ ] Запись добавлена в `CHANGELOG.md` (`## Unreleased`).

---

## M-008 — Добавить временный workflow в `CONTRIBUTING.md`

**Title:** `[M-008] docs: добавить временный prompt-workflow в CONTRIBUTING.md`

**Labels:** `migration` | `creative` | `priority:P0`
**Milestone:** `Sprint 3 — Hybrid Minimum Bootstrap`
**User Story / ФТ:** `project:mango_ba_prompts-migration-execution`
**Linked Backlog:** [`pr-ops/BACKLOG.md` → M-008](BACKLOG.md)
**Depends On:** —
**Operating Mode:** `Creative`

### 🎯 Контекст

Операционная инструкция для команды до появления ADR. Трассируемость: RFC §5.2
(содержание временного workflow), креативное улучшение C5, edge case E4; бэклог
M-008. Workflow опирается на capability boundary `prompts/drafts/` и **не**
вводит матрицу/ADR (E4, C5).

**Креативная рекомендация (mode `Creative`).** Сформулируй 5 нумерованных шагов
как явный чек-лист: `draft → frontmatter → issue → review → canonical`. Явно
напиши: «Это единственный разрешённый способ создания промптов до появления
ADR». Добавь пример файла с корректным frontmatter (`status: draft`,
`version: 0.1`, `updated`, `temperature: 0.1`).

### 📄 Артефакты для создания/изменения

- [ ] Добавить в `CONTRIBUTING.md` ровно 5 шагов временного workflow промптов:
      1. Создать файл в `prompts/drafts/` с именем `[biz-process]-[purpose].md`.
      2. Обязательный frontmatter: `status: draft`, `version: 0.1`,
         `updated: {{date}}`, `temperature: 0.1`.
      3. Добавить комментарий
         `<!-- Experimental: for [task/link], no formal research yet -->`.
      4. Создать issue `prompt:review` с бизнес-контекстом.
      5. После human review → переместить в `prompts/`, `status: canonical`,
         `version: 1.0`.
- [ ] Добавить пример файла с правильным frontmatter.

### ✅ Готово, когда

- [ ] В `CONTRIBUTING.md` присутствуют ровно 5 шагов workflow из RFC §5.2.
- [ ] Явно указано, что это единственный разрешённый способ до ADR.
- [ ] Раздел согласован со структурой `prompts/` из M-002; матрица/ADR не
      вводятся (E4, C5).
- [ ] Запись добавлена в `CHANGELOG.md` (`## Unreleased`).

---

## M-009 — Создать Migration Manifest

**Title:** `[M-009] docs: создать локальный Migration Manifest (docs/migration-manifest.md)`

**Labels:** `migration` | `creative` | `priority:P2`
**Milestone:** `Sprint 3 — Hybrid Minimum Bootstrap`
**User Story / ФТ:** `project:mango_ba_prompts-migration-execution`
**Linked Backlog:** [`pr-ops/BACKLOG.md` → M-009](BACKLOG.md)
**Depends On:** M-006
**Operating Mode:** `Creative`

### 🎯 Контекст

Локальный трекер миграции (**не** общий стандарт). Трассируемость: RFC §5.1
(таблица «артефакт → действие → статус → ссылка») и §5.3 (минимальный
чек-лист-трекер); креативное улучшение C6 (manifest как живой снимок); бэклог
M-009. Размещение: `docs/migration-manifest.md`.

**Креативная рекомендация (mode `Creative`).** Сделай минимальный, но «живой»
шаблон из двух частей: (1) таблица «артефакт → категория → действие → статус →
назначение в споке» (§5.1); (2) чек-лист-трекер «Перенесено / Осталось в Хабе /
Требует уточнения» (§5.3). Зафиксируй монорепо-`README.md` Хаба как `archived`
(E3), research — как `referenced`.

### 📄 Артефакты для создания/изменения

- [ ] Создать `docs/migration-manifest.md` с таблицей §5.1 и чек-листом §5.3.
- [ ] Подготовить структуру к заполнению по ходу Фаз 0–3.

### ✅ Готово, когда

- [ ] Manifest содержит таблицу «артефакт → категория → действие → статус →
      назначение в споке» (§5.1).
- [ ] Присутствует чек-лист «Перенесено / Осталось в Хабе / Требует уточнения»
      (§5.3).
- [ ] Монорепо-`README.md` зафиксирован как `archived` (E3), research — как
      `referenced`.
- [ ] Запись добавлена в `CHANGELOG.md` (`## Unreleased`).

---

## Связанные артефакты

- Issue: <https://github.com/G-Ivan-A/mango_ba_prompts/issues/23>
- Бэклог: [`pr-ops/BACKLOG.md`](BACKLOG.md)
- Утверждённый RFC: [`docs/analysis/migration-strategy-rfc.md`](../docs/analysis/migration-strategy-rfc.md)
- Human Review: [`docs/reviews/migration-rfc-human-review-2026-06.md`](../docs/reviews/migration-rfc-human-review-2026-06.md)
- Стандарт Issue (Хаб): <https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/038868dd125b4e2d849ff73604890f1d2787ac0f/standards/ISSUE_WORKFLOW.md>
- Шаблон задачи (Хаб): <https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/038868dd125b4e2d849ff73604890f1d2787ac0f/.github/ISSUE_TEMPLATE/task.yml>
