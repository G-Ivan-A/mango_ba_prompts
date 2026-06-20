---
status: draft
version: 0.3
updated: 2026-06-20
ai-generated: true
type: research-dependency-registry
scope: mango_ba_prompts
source_hub: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/tree/038868dd125b4e2d849ff73604890f1d2787ac0f/research/mango"
source_sha: "038868dd125b4e2d849ff73604890f1d2787ac0f"
latest_smart_sync_sha: "b683341d22d4f518618917a02d9c7c394658b156"
latest_issue_127_hub_sha: "73e94c6e69995ccf9e746c19d9c18359971285f2"
issue: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/34"
---

# Реестр зависимостей от исследований Хаба

> **Единственная точка ссылок на research Хаба.** RFC §3.5 запрещает дублировать
> этот реестр: файл `hub-research-links.md` **не создаётся**. Промпты спока и
> контракт классификации не хранят длинные research-URL в своём frontmatter —
> они указывают на якорь этого реестра через поле `research_dep`
> (edge cases E1, E8).

## Политика

- **Research остаётся в Хабе.** Каталог
  [`research/mango/`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/tree/038868dd125b4e2d849ff73604890f1d2787ac0f/research/mango)
  не переносится в спок (RFC §2.5, инвентарь — всё 🔵). Спок регистрирует только
  ссылки.
- **Permalink на SHA (C3).** Все ссылки закреплены за коммитом Хаба
  `038868dd125b4e2d849ff73604890f1d2787ac0f`, чтобы аудит не «поплыл» при
  обновлении ветки `main` источника.
- **Reference only.** Содержимое research не копируется в спок ни целиком, ни
  фрагментами; используется только как доказательная база по ссылке.
- **External knowledge registry — reference-only.** Hub PR #229 добавил Base
  Registry внешних источников:
  [`research/external-knowledge/external-sources-registry.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/b683341d22d4f518618917a02d9c7c394658b156/research/external-knowledge/external-sources-registry.md).
  Для `mango_ba_prompts` он не копируется в локальный `research/`: релевантные
  строки регистрируются ниже как компактный срез.
- **HTML-экспорты не регистрируются.** Файлы `*.html` — дубли соответствующих
  `*.md` (RFC §2.5) и якорей-потребителей не получают.
- **Issue #127 sync.** RFC `requirements-engineering-ai-era-2026.md` и
  `ai-classifications-formalization-2026-06.md` закреплены на SHA
  `73e94c6e69995ccf9e746c19d9c18359971285f2` и используются reference-only для
  C1/C2/C3 синхронизации онтологии.

## Сводная таблица

| Якорь | Hub-файл (permalink на SHA) | Размер | Потребители в споке | Статус синхронизации |
| :--- | :--- | :--- | :--- | :--- |
| [`#classification`](#classification) | [`research/mango/classification.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/038868dd125b4e2d849ff73604890f1d2787ac0f/research/mango/classification.md) | 122.6 KB | `prompts/tz-stats-generator.md`, `prompts/user-story-generator.md`, `prompts/usecase-stepwise-generator.md`, `standards/product-classification-contract.md`, `docs/ba-ecosystem.md` | 🔵 reference-only @ `038868d` |
| [`#classification-tz`](#classification-tz) | [`research/mango/classification-tz.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/038868dd125b4e2d849ff73604890f1d2787ac0f/research/mango/classification-tz.md) | 58.7 KB | `prompts/tz-stats-generator.md`, `docs/ba-ecosystem.md` | 🔵 reference-only @ `038868d` |
| [`#taxonomy-concept`](#taxonomy-concept) | [`research/mango/taxonomy-concept-2026-05.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/038868dd125b4e2d849ff73604890f1d2787ac0f/research/mango/taxonomy-concept-2026-05.md) | 30.8 KB | `standards/product-classification-contract.md`, `docs/ba-ecosystem.md` | 🔵 reference-only @ `038868d` (draft до canonical в Хабе) |
| [`#requirements-flow`](#requirements-flow) | [`research/mango/requirements-flow.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/038868dd125b4e2d849ff73604890f1d2787ac0f/research/mango/requirements-flow.md) | 47.5 KB | `docs/ba-ecosystem.md` | 🔵 reference-only @ `038868d` |
| [`#requirements-lifecycle`](#requirements-lifecycle) | [`research/mango/requirements-lifecycle-uncertainty-2026-05.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/038868dd125b4e2d849ff73604890f1d2787ac0f/research/mango/requirements-lifecycle-uncertainty-2026-05.md) | 52.8 KB | `docs/ba-ecosystem.md` | 🔵 reference-only @ `038868d` |
| [`#capability-decomposition`](#capability-decomposition) | [`research/mango/capability-decomposition-2026-05.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/038868dd125b4e2d849ff73604890f1d2787ac0f/research/mango/capability-decomposition-2026-05.md) | 90.1 KB | `docs/ba-ecosystem.md` | 🔵 reference-only @ `038868d` |
| [`#rag-mapping`](#rag-mapping) | [`research/mango/rag-mapping-roadmap-2026-05.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/038868dd125b4e2d849ff73604890f1d2787ac0f/research/mango/rag-mapping-roadmap-2026-05.md) | 44.8 KB | `docs/ba-ecosystem.md` | 🔵 reference-only @ `038868d` |
| [`#requirements-engineering-ai-era`](#requirements-engineering-ai-era) | [`research/mango/requirements-engineering-ai-era-2026.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/73e94c6e69995ccf9e746c19d9c18359971285f2/research/mango/requirements-engineering-ai-era-2026.md) | 414 lines | `standards/ba-ontology.md`, `docs/adr/003-ba-ontology.md`, `docs/adr/004-operations-taxonomy.md`, `docs/requirements-engineering-crosswalk.md`, `docs/taxonomy.md`, `README.md` | 🔵 reference-only @ `73e94c6` |
| [`#ai-classifications-formalization`](#ai-classifications-formalization) | [`research/mango/ai-classifications-formalization-2026-06.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/73e94c6e69995ccf9e746c19d9c18359971285f2/research/mango/ai-classifications-formalization-2026-06.md) | 474 lines | `standards/ba-ontology.md`, `docs/adr/003-ba-ontology.md`, `docs/adr/004-operations-taxonomy.md`, `docs/requirements-engineering-crosswalk.md`, `docs/taxonomy.md`, `README.md` | 🔵 reference-only @ `73e94c6` |
| [`#research-readme`](#research-readme) | [`research/mango/README.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/038868dd125b4e2d849ff73604890f1d2787ac0f/research/mango/README.md) | 2.8 KB | — (точка входа по навигации) | 🔵 reference-only @ `038868d` |
| [`#external-sources-registry`](#external-sources-registry) | [`research/external-knowledge/external-sources-registry.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/b683341d22d4f518618917a02d9c7c394658b156/research/external-knowledge/external-sources-registry.md) | 105 lines | `docs/ba-ecosystem.md`, future requirements-flow pilots | 🔵 reference-only @ `b683341` |
| [`#external-spec-driven`](#external-spec-driven) | `ext-003` in [`external-sources-registry.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/b683341d22d4f518618917a02d9c7c394658b156/research/external-knowledge/external-sources-registry.md) | row | future spec-driven requirements experiments | 🔵 reference-only @ `b683341` |
| [`#external-context-engineering`](#external-context-engineering) | `ext-007` in [`external-sources-registry.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/b683341d22d4f518618917a02d9c7c394658b156/research/external-knowledge/external-sources-registry.md) | row | context engineering for long BA prompt sessions | 🔵 reference-only @ `b683341` |

> HTML-экспорты `classification.html`, `classification-tz.html`,
> `requirements-flow.html` присутствуют в Хабе, но **не регистрируются** как
> отдельные зависимости — это дубли `.md` (RFC §2.5).

## Якоря

<a id="classification"></a>

### `#classification` — Классификация продуктов

- **Hub URL:** <https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/038868dd125b4e2d849ff73604890f1d2787ac0f/research/mango/classification.md>
- **Описание:** ключевое исследование классификации `Domain → Capability →
  Feature → Atomic Function`; главная research-зависимость спока (RFC §2.5).
- **Потребители (`research_dep`):**
  - `prompts/tz-stats-generator.md`
  - `prompts/user-story-generator.md`
  - `prompts/usecase-stepwise-generator.md`
  - `standards/product-classification-contract.md`
  - `docs/ba-ecosystem.md`
- **Политика:** reference only; не копировать.

<a id="classification-tz"></a>

### `#classification-tz` — Проверка классификатора на корпусе ТЗ

- **Hub URL:** <https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/038868dd125b4e2d849ff73604890f1d2787ac0f/research/mango/classification-tz.md>
- **Описание:** прогон классификатора на корпусе из 30 ТЗ; референс для
  `tz-stats-*`.
- **Потребители (`research_dep`):**
  - `prompts/tz-stats-generator.md`
  - `docs/ba-ecosystem.md`
- **Политика:** reference only; не копировать.

<a id="taxonomy-concept"></a>

### `#taxonomy-concept` — Концепция Unified Capability Taxonomy

- **Hub URL:** <https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/038868dd125b4e2d849ff73604890f1d2787ac0f/research/mango/taxonomy-concept-2026-05.md>
- **Описание:** draft-концепция Unified Capability Taxonomy; на неё ссылается
  контракт классификации. Релевантна триггеру эволюции P4 (RFC §6).
- **Потребители (`research_dep`):**
  - `standards/product-classification-contract.md`
  - `docs/ba-ecosystem.md`
- **Политика:** reference only до получения canonical-статуса в Хабе.

<a id="requirements-flow"></a>

### `#requirements-flow` — Flow требований

- **Hub URL:** <https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/038868dd125b4e2d849ff73604890f1d2787ac0f/research/mango/requirements-flow.md>
- **Описание:** flow требований для AI-анализа ТЗ.
- **Потребители (`research_dep`):**
  - `docs/ba-ecosystem.md`
- **Политика:** reference only; не копировать.

<a id="requirements-lifecycle"></a>

### `#requirements-lifecycle` — Жизненный цикл требования и неопределённость

- **Hub URL:** <https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/038868dd125b4e2d849ff73604890f1d2787ac0f/research/mango/requirements-lifecycle-uncertainty-2026-05.md>
- **Описание:** жизненный цикл требования и обработка неопределённости.
- **Потребители (`research_dep`):**
  - `docs/ba-ecosystem.md`
- **Политика:** reference only; не копировать.

<a id="capability-decomposition"></a>

### `#capability-decomposition` — Декомпозиция capabilities

- **Hub URL:** <https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/038868dd125b4e2d849ff73604890f1d2787ac0f/research/mango/capability-decomposition-2026-05.md>
- **Описание:** справочник атомарных функций пилотных доменов.
- **Потребители (`research_dep`):**
  - `docs/ba-ecosystem.md`
- **Политика:** reference only; не копировать.

<a id="rag-mapping"></a>

### `#rag-mapping` — RAG-навигатор и roadmap автоматизации БА

- **Hub URL:** <https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/038868dd125b4e2d849ff73604890f1d2787ac0f/research/mango/rag-mapping-roadmap-2026-05.md>
- **Описание:** RAG-навигатор и roadmap автоматизации бизнес-анализа.
- **Потребители (`research_dep`):**
  - `docs/ba-ecosystem.md`
- **Политика:** reference only; не копировать.

<a id="requirements-engineering-ai-era"></a>

### `#requirements-engineering-ai-era` — Вигерс ↔ mango, C1/C2/C3

- **Hub URL:** <https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/73e94c6e69995ccf9e746c19d9c18359971285f2/research/mango/requirements-engineering-ai-era-2026.md>
- **Описание:** RFC сравнивает модель Вигерса с ADR #003-#010 mango и выделяет
  C1 (`requirement_level`), C2 (`business-rule`) и C3 (crosswalk Вигерс ↔ mango ↔
  BCREQ) как синхронизацию issue #127.
- **Потребители (`research_dep`):**
  - `standards/ba-ontology.md`
  - `docs/adr/003-ba-ontology.md`
  - `docs/adr/004-operations-taxonomy.md`
  - `docs/requirements-engineering-crosswalk.md`
  - `docs/taxonomy.md`
  - `README.md`
- **Политика:** reference only; не копировать RFC в спок.

<a id="ai-classifications-formalization"></a>

### `#ai-classifications-formalization` — AI-классификации Mango

- **Hub URL:** <https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/73e94c6e69995ccf9e746c19d9c18359971285f2/research/mango/ai-classifications-formalization-2026-06.md>
- **Описание:** companion RFC формализует AI-классификации и подтверждает
  подготовку C1/C2/C3 для `mango_ba_prompts`; AI-практики остаются `Candidate` и
  не внедряются как стандарт в issue #127.
- **Потребители (`research_dep`):**
  - `standards/ba-ontology.md`
  - `docs/adr/003-ba-ontology.md`
  - `docs/adr/004-operations-taxonomy.md`
  - `docs/requirements-engineering-crosswalk.md`
  - `docs/taxonomy.md`
  - `README.md`
- **Политика:** reference only; не копировать RFC в спок.

<a id="research-readme"></a>

### `#research-readme` — Навигация по исследованиям

- **Hub URL:** <https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/038868dd125b4e2d849ff73604890f1d2787ac0f/research/mango/README.md>
- **Описание:** точка входа по навигации в каталоге `research/mango/`.
- **Потребители (`research_dep`):** — (используется как навигационная ссылка).
- **Политика:** reference only; не копировать.

<a id="external-sources-registry"></a>

### `#external-sources-registry` — Base Registry внешних источников

- **Hub URL:** <https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/b683341d22d4f518618917a02d9c7c394658b156/research/external-knowledge/external-sources-registry.md>
- **Описание:** Base Registry из Hub PR #229: карта внешних источников с
  минимальными метаданными (`id`, тип, теги, stage, проекты, инсайт).
- **Релевантные строки Mango:** `ext-003` и `ext-007`.
- **Политика:** reference-only; Base Registry не копируется в локальный
  `research/`. Local Extension для Mango не создаётся, пока нет отдельной
  операционной боли и набора локальных источников.

<a id="external-spec-driven"></a>

### `#external-spec-driven` — `ext-003` Spec-Driven Development

- **Hub URL:** <https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/b683341d22d4f518618917a02d9c7c394658b156/research/external-knowledge/external-sources-registry.md>
- **Источник:** `ext-003`, GitHub Spec Kit (Spec-Driven Development).
- **Релевантность Mango:** гипотеза для требований, executable-spec и будущих
  экспериментов по ТЗ-flow.
- **Политика:** reference-only; не копировать первоисточник и не повышать в
  practice без отдельного issue/PR.

<a id="external-context-engineering"></a>

### `#external-context-engineering` — `ext-007` Контекст-инжиниринг

- **Hub URL:** <https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/b683341d22d4f518618917a02d9c7c394658b156/research/external-knowledge/external-sources-registry.md>
- **Источник:** `ext-007`, Habr: Контекст-инжиниринг для AI-агентов.
- **Релевантность Mango:** русскоязычная практика context engineering для
  длинных диалогов, prompt assets и handover/session-digest workflow.
- **Политика:** reference-only; не копировать первоисточник и не создавать
  локальный `research/` без отдельного решения Пользователя.
