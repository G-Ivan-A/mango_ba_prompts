---
status: draft
version: 0.1
updated: 2026-06-05
ai-generated: true
type: migration-manifest
scope: mango_ba_prompts-migration-execution
based_on: "docs/analysis/migration-strategy-rfc.md"
backlog_ref: "governance/BACKLOG.md"
issue: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/36"
hub_snapshot_sha: "038868dd125b4e2d849ff73604890f1d2787ac0f"
hub_snapshot_ref: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/tree/038868dd125b4e2d849ff73604890f1d2787ac0f/projects/mango"
latest_smart_sync_sha: "b683341d22d4f518618917a02d9c7c394658b156"
latest_smart_sync_ref: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/tree/b683341d22d4f518618917a02d9c7c394658b156"
phase: "Фаза 1 (в работе)"
closed_in_phase: 3
---

# Migration Manifest — mango_ba_prompts

> 📸 **Живой снимок миграции Mango из Хаба в спок.** Манифест — это реализация
> творческого улучшения **C6** RFC: таблица «артефакт → категория → действие →
> статус → назначение в споке» (RFC §5.1) плюс минимальный локальный
> чек-лист-трекер «Перенесено / Осталось в Хабе / Требует уточнения» (RFC §5.3).
> Ведётся по ходу Фаз 0–3 и **закрывается в Фазе 3** как воспроизводимый снимок
> миграции для будущего аудита.
>
> **Источник истины** — утверждённый
> [`docs/analysis/migration-strategy-rfc.md`](../docs/analysis/migration-strategy-rfc.md)
> (v0.3, Human Review 2026-06-04). Манифест не вводит новых решений: каждая
> строка трассируется на аудит RFC §2 и таблицу файлов Фазы 1 (§3.2).

## 1. Снимок миграции (snapshot)

- **Хаб (source)**: `hybrid-Intelligence-lab`, монорепо.
- **Спок (target)**: `mango_ba_prompts`, standalone.
- **Зафиксированный коммит Хаба (permalink-pinning, C3 / E7)**:
  [`038868dd125b4e2d849ff73604890f1d2787ac0f`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/tree/038868dd125b4e2d849ff73604890f1d2787ac0f/projects/mango).
- **Permalink-база для blob-ссылок ниже**:
  `https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/038868dd125b4e2d849ff73604890f1d2787ac0f/`
- **Текущая фаза**: Фаза 1 (перенос содержимого) — в работе.

### Легенда

**Категория** (RFC §2.2):

| Знак | Категория | Действие по принципам RFC §1.2 |
| :--- | :--- | :--- |
| 🟢 | **Промпт** | Переносим физически в `prompts/` + нормализация. |
| 🔵 | **Исследование** | Остаётся в Хабе; в споке — ссылка на полный URL (P1). |
| ⚪ | **Стандарт** | Копируем в спок + ссылка на source of truth в Хабе (P2). |
| ⚫ | **Документация / KB / эксперимент** | Решение индивидуально (перенос / ссылка / архивация). |

**Статус**: `migrated` — физически перенесён и нормализован · `referenced` —
зарегистрирован ссылкой (не копируется) · `archived` — рассмотрен, не
переносится, оставлен как архивная ссылка · `pending` — решение принято,
артефакт ещё не создан · `not-migrated` — сознательно не переносится
(Anti-Inflation).

## 2. Таблица «артефакт → категория → действие → статус → назначение в споке» (§5.1)

### 2.1. Промпты (🟢)

| Артефакт (Хаб) | Категория | Действие | Статус | Назначение в споке |
| :--- | :--- | :--- | :--- | :--- |
| [`prompts/tz-stats-generator_exp-2026-05.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/038868dd125b4e2d849ff73604890f1d2787ac0f/projects/mango/prompts/tz-stats-generator_exp-2026-05.md) | 🟢 | migrate+normalize | `migrated` | [`prompts/tz-stats-generator.md`](../prompts/tz-stats-generator.md) |
| [`prompts/tz-stats-generator_simple-2026-05.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/038868dd125b4e2d849ff73604890f1d2787ac0f/projects/mango/prompts/tz-stats-generator_simple-2026-05.md) | 🟢 | migrate+normalize | `migrated` | [`prompts/tz-stats-generator-simple.md`](../prompts/tz-stats-generator-simple.md) |
| [`prompts/usecase-stepwise-generator_exp-2026-05.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/038868dd125b4e2d849ff73604890f1d2787ac0f/projects/mango/prompts/usecase-stepwise-generator_exp-2026-05.md) | 🟢 | migrate+normalize | `migrated` | [`prompts/usecase-stepwise-generator.md`](../prompts/usecase-stepwise-generator.md) |
| [`prompts/usecase-stepwise-generator_simple-2026-05.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/038868dd125b4e2d849ff73604890f1d2787ac0f/projects/mango/prompts/usecase-stepwise-generator_simple-2026-05.md) | 🟢 | migrate+normalize | `migrated` | [`prompts/usecase-stepwise-generator-simple.md`](../prompts/usecase-stepwise-generator-simple.md) |
| [`prompts/user-story-generator_exp-2026-05.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/038868dd125b4e2d849ff73604890f1d2787ac0f/projects/mango/prompts/user-story-generator_exp-2026-05.md) | 🟢 | migrate+normalize | `migrated` | [`prompts/user-story-generator.md`](../prompts/user-story-generator.md) |
| [`prompts/user-story-generator_simple-2026-05.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/038868dd125b4e2d849ff73604890f1d2787ac0f/projects/mango/prompts/user-story-generator_simple-2026-05.md) | 🟢 | migrate+normalize | `migrated` | [`prompts/user-story-generator-simple.md`](../prompts/user-story-generator-simple.md) |

### 2.2. Стандарты (⚪)

| Артефакт (Хаб) | Категория | Действие | Статус | Назначение в споке |
| :--- | :--- | :--- | :--- | :--- |
| [`projects/mango/standards/classification-glossary.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/038868dd125b4e2d849ff73604890f1d2787ac0f/projects/mango/standards/classification-glossary.md) | ⚪ | rename+copy | `migrated` | [`standards/product-classification-contract.md`](../standards/product-classification-contract.md) |
| [`standards/GLOSSARY.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/038868dd125b4e2d849ff73604890f1d2787ac0f/standards/GLOSSARY.md) | ⚪ | copy+link | `migrated` | [`standards/GLOSSARY.md`](../standards/GLOSSARY.md) |

### 2.3. Эксперименты (⚫ — часть продукта, E5)

| Артефакт (Хаб) | Категория | Действие | Статус | Назначение в споке |
| :--- | :--- | :--- | :--- | :--- |
| [`experiments/tz-stats-prototype-2026-05.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/038868dd125b4e2d849ff73604890f1d2787ac0f/projects/mango/experiments/tz-stats-prototype-2026-05.md) | ⚫ | migrate | `migrated` | [`prompts/experiments/tz-stats-prototype-2026-05.md`](../prompts/experiments/tz-stats-prototype-2026-05.md) |
| [`experiments/usecase_gen-stepwise-alignment_2026-05-26.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/038868dd125b4e2d849ff73604890f1d2787ac0f/projects/mango/experiments/usecase_gen-stepwise-alignment_2026-05-26.md) | ⚫ | migrate | `migrated` | [`prompts/experiments/usecase_gen-stepwise-alignment_2026-05-26.md`](../prompts/experiments/usecase_gen-stepwise-alignment_2026-05-26.md) |
| [`experiments/user-story_gen-from-raw-request_2026-05-26.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/038868dd125b4e2d849ff73604890f1d2787ac0f/projects/mango/experiments/user-story_gen-from-raw-request_2026-05-26.md) | ⚫ | migrate | `migrated` | [`prompts/experiments/user-story_gen-from-raw-request_2026-05-26.md`](../prompts/experiments/user-story_gen-from-raw-request_2026-05-26.md) |
| [`experiments/prompts-audit-2026-05-26.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/038868dd125b4e2d849ff73604890f1d2787ac0f/projects/mango/experiments/prompts-audit-2026-05-26.md) | ⚫ | migrate | `migrated` | [`prompts/experiments/prompts-audit-2026-05-26.md`](../prompts/experiments/prompts-audit-2026-05-26.md) |
| [`experiments/prompts-selftest-2026-05-26.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/038868dd125b4e2d849ff73604890f1d2787ac0f/projects/mango/experiments/prompts-selftest-2026-05-26.md) | ⚫ | migrate | `migrated` | [`prompts/experiments/prompts-selftest-2026-05-26.md`](../prompts/experiments/prompts-selftest-2026-05-26.md) (self-test gate, C2) |

### 2.4. Исследования (🔵 — остаются в Хабе, P1)

Research **не копируется**; спок ссылается через единый реестр
[`docs/hub-research-dependencies.md`](../docs/hub-research-dependencies.md)
(создаётся в M-007, см. §4 «Требует уточнения»). Статус `referenced` фиксирует
**решение** (категория + якорь реестра); сам файл-реестр на момент этой записи
ещё формируется.

| Артефакт (Хаб) | Категория | Действие | Статус | Назначение в споке (якорь реестра) |
| :--- | :--- | :--- | :--- | :--- |
| [`research/mango/classification.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/038868dd125b4e2d849ff73604890f1d2787ac0f/research/mango/classification.md) | 🔵 | register | `referenced` | `docs/hub-research-dependencies.md#classification` |
| [`research/mango/classification-tz.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/038868dd125b4e2d849ff73604890f1d2787ac0f/research/mango/classification-tz.md) | 🔵 | register | `referenced` | `docs/hub-research-dependencies.md#classification-tz` |
| [`research/mango/taxonomy-concept-2026-05.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/038868dd125b4e2d849ff73604890f1d2787ac0f/research/mango/taxonomy-concept-2026-05.md) | 🔵 | register | `referenced` | `docs/hub-research-dependencies.md#taxonomy-concept` |
| [`research/mango/README.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/038868dd125b4e2d849ff73604890f1d2787ac0f/research/mango/README.md) | 🔵 | register | `referenced` | точка входа в research Хаба (реестр) |
| [`research/mango/requirements-flow.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/038868dd125b4e2d849ff73604890f1d2787ac0f/research/mango/requirements-flow.md) | 🔵 | register | `referenced` | реестр (по факту потребления) |
| [`research/mango/requirements-lifecycle-uncertainty-2026-05.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/038868dd125b4e2d849ff73604890f1d2787ac0f/research/mango/requirements-lifecycle-uncertainty-2026-05.md) | 🔵 | register | `referenced` | реестр (по факту потребления) |
| [`research/mango/rag-mapping-roadmap-2026-05.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/038868dd125b4e2d849ff73604890f1d2787ac0f/research/mango/rag-mapping-roadmap-2026-05.md) | 🔵 | register | `referenced` | реестр (по факту потребления) |
| [`research/mango/capability-decomposition-2026-05.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/038868dd125b4e2d849ff73604890f1d2787ac0f/research/mango/capability-decomposition-2026-05.md) | 🔵 | register | `referenced` | реестр (по факту потребления) |

> `*.html`-экспорты research (`classification.html`, `classification-tz.html`,
> `requirements-flow.html`) **не ссылаются** — это дубли соответствующих `.md`
> (RFC §2.5).

### 2.5. Документация и плейсхолдеры (⚫)

| Артефакт (Хаб) | Категория | Действие | Статус | Назначение в споке |
| :--- | :--- | :--- | :--- | :--- |
| [`projects/mango/README.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/038868dd125b4e2d849ff73604890f1d2787ac0f/projects/mango/README.md) | ⚫ | archive | `archived` | **Не переносим** — заменён spoke-[`README.md`](../README.md) (E3). Архивная ссылка сохранена в этой строке. |
| `projects/mango/{decisions,docs,kb,experiments}/.gitkeep` | ⚫ | — | `not-migrated` | Anti-Inflation (P5): пустые плейсхолдеры спок «с собой не носит». |

## 3. Чек-лист-трекер (§5.3)

### ✅ Перенесено (физически в спок)

- [x] `prompts/tz-stats-generator.md` — 2026-06-04 — `status: canonical` — self-test `passed`
- [x] `prompts/tz-stats-generator-simple.md` — 2026-06-04 — `status: canonical` — self-test `passed`
- [x] `prompts/usecase-stepwise-generator.md` — 2026-06-04 — `status: canonical` — self-test `passed`
- [x] `prompts/usecase-stepwise-generator-simple.md` — 2026-06-04 — `status: canonical` — self-test `passed`
- [x] `prompts/user-story-generator.md` — 2026-06-04 — `status: canonical` — self-test `passed`
- [x] `prompts/user-story-generator-simple.md` — 2026-06-04 — `status: canonical` — self-test `passed`
- [x] `standards/GLOSSARY.md` — 2026-06-04 — `status: canonical` — copy+link (P2)
- [x] `standards/product-classification-contract.md` — 2026-06-04 — `status: draft` — rename из `classification-glossary.md` (E2/E6)
- [x] `prompts/experiments/tz-stats-prototype-2026-05.md` — часть продукта (E5)
- [x] `prompts/experiments/usecase_gen-stepwise-alignment_2026-05-26.md` — часть продукта (E5)
- [x] `prompts/experiments/user-story_gen-from-raw-request_2026-05-26.md` — часть продукта (E5)
- [x] `prompts/experiments/prompts-audit-2026-05-26.md` — часть продукта (E5)
- [x] `prompts/experiments/prompts-selftest-2026-05-26.md` — acceptance-сценарий self-test gate (C2)

### 🔵 Осталось в Хабе (зависимости задекларированы)

- [x] `research/mango/classification.md` → [полный URL](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/038868dd125b4e2d849ff73604890f1d2787ac0f/research/mango/classification.md) — якорь `#classification`
- [x] `research/mango/classification-tz.md` → [полный URL](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/038868dd125b4e2d849ff73604890f1d2787ac0f/research/mango/classification-tz.md) — якорь `#classification-tz`
- [x] `research/mango/taxonomy-concept-2026-05.md` → [полный URL](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/038868dd125b4e2d849ff73604890f1d2787ac0f/research/mango/taxonomy-concept-2026-05.md) — якорь `#taxonomy-concept`
- [x] Остальные `research/mango/*` (`README.md`, `requirements-flow.md`,
  `requirements-lifecycle-uncertainty-2026-05.md`, `rag-mapping-roadmap-2026-05.md`,
  `capability-decomposition-2026-05.md`) — остаются в Хабе (P1), регистрируются по
  факту потребления.
- [x] `projects/mango/README.md` → [архивная ссылка](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/038868dd125b4e2d849ff73604890f1d2787ac0f/projects/mango/README.md) — `archived` (E3), заменён spoke-README.

### ⚠️ Требует уточнения / В работе

- [ ] `docs/hub-research-dependencies.md` — единый реестр research-зависимостей
  (M-007, [issue #34](https://github.com/G-Ivan-A/mango_ba_prompts/issues/34)) **ещё
  не создан**. До его появления `research_dep`-якоря в промптах и контракте
  указывают на будущие секции реестра. **Блокирует** перевод research-строк §2.4 из
  «решение принято» в «реестр заполнен».
- [ ] **Фаза 2** (RFC §3.2): сверка, что все `research/mango/*`-ссылки спока идут
  через реестр, ни одной hub-относительной/битой ссылки. Выполняется после M-007.
- [ ] **Фаза 3** (RFC §3.2): убрать технический корневой `.gitkeep`, финальная
  запись в `CHANGELOG.md`, **закрытие этого манифеста** как воспроизводимого снимка
  (смена `status: draft → canonical`, `phase → Фаза 3 (закрыт)`).

## 4. Сводка снимка

| Категория | Кол-во | Статус |
| :--- | :--- | :--- |
| 🟢 Промпты | 6 | `migrated` |
| ⚪ Стандарты | 2 | `migrated` |
| ⚫ Эксперименты | 5 | `migrated` |
| 🔵 Исследования | 11 | `referenced` (реестр M-007 в работе) |
| ⚫ Монорепо-`README.md` | 1 | `archived` (E3) |
| ⚫ Пустые плейсхолдеры | 4 | `not-migrated` (P5) |

**Итого рассмотрено**: 23 артефакта Хаба (12 в `projects/mango/`, 11 в
`research/mango/`) + внешний `standards/GLOSSARY.md`. **Недоступных и
непрослеженных артефактов нет** — манифест показывает, что каждый артефакт
**рассмотрен**, а не потерян (E3).

## 5. Smart Sync snapshots

Эта секция фиксирует последующие точечные синхронизации governance-генома из
Хаба после исходной миграции Mango.

| Дата | Issue | Хаб PR / SHA | Локальные артефакты | Статус |
| :--- | :--- | :--- | :--- | :--- |
| 2026-06-13 | [#72](https://github.com/G-Ivan-A/mango_ba_prompts/issues/72) | PR [#224](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/224) + PR [#226](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/226), SHA [`f3e8b265b1577d0ee1fe173dbe16728cc3c7e31b`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/tree/f3e8b265b1577d0ee1fe173dbe16728cc3c7e31b) | [`AI_SESSION_HANDOVER_PROMPT.md`](../AI_SESSION_HANDOVER_PROMPT.md), [`governance/agent-onboarding-protocol.md`](agent-onboarding-protocol.md), [`governance/session-digests.md`](session-digests.md), [`governance/artifact-map.md`](artifact-map.md), [`.hub-profile.json`](../.hub-profile.json) | `synced` |
| 2026-06-13 | [#72](https://github.com/G-Ivan-A/mango_ba_prompts/issues/72) | PR [#229](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/229) + PR [#230](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/230), SHA [`b683341d22d4f518618917a02d9c7c394658b156`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/tree/b683341d22d4f518618917a02d9c7c394658b156) | [`docs/hub-research-dependencies.md`](../docs/hub-research-dependencies.md), [`AI_GOVERNANCE.md`](../AI_GOVERNANCE.md), [`CONTRIBUTING.md`](../CONTRIBUTING.md), [`README.md`](../README.md), [`docs/task-for-konard-template.md`](../docs/task-for-konard-template.md), [`docs/adr/0002-issue48-handover-local-enrichment.md`](../docs/adr/0002-issue48-handover-local-enrichment.md), [`docs/adr/0003-creative-mode-governance.md`](../docs/adr/0003-creative-mode-governance.md), [`governance/artifact-map.md`](artifact-map.md), [`.hub-profile.json`](../.hub-profile.json) | `synced / reference-only` |

**Примечание по локальной специфике:** `governance/session-digests.md` создан как
пустой локальный индекс `mango_ba_prompts`; хабовая первая суммария про
архитектуру документации не копировалась как контекст Mango. Handover prompt
сохраняет локальные правила issue #48/#61 про канал работы через Конарда и
терминологию Пользователь / Исполнитель.

**Примечание по PR #229/#230:** `research/external-knowledge/external-sources-registry.md`
из Хаба имеет статус `not-migrated` как локальный файл: Base Registry остаётся
reference-only, а релевантные для Mango строки `ext-003` и `ext-007`
зарегистрированы в [`docs/hub-research-dependencies.md`](../docs/hub-research-dependencies.md).
Traceability contracts, Framework vs Template и Scope Resolver-а из PR #230
рассмотрены как Hub-governance контракты и не создают новых локальных артефактов
без отдельного решения Пользователя.
Терминологическая часть PR #230 также обновляет связанные task-template, ADR,
review и migration-era ссылки, чтобы текущий репозиторий использовал единый
контракт ролей `Пользователь / Исполнитель`.

## Связанные артефакты

- Issue (M-009): <https://github.com/G-Ivan-A/mango_ba_prompts/issues/36>
- Утверждённый RFC (источник истины): [`docs/analysis/migration-strategy-rfc.md`](../docs/analysis/migration-strategy-rfc.md)
- Операционный бэклог Фазы 1: [`governance/BACKLOG.md`](BACKLOG.md)
- Реестр issues Фазы 1: [`governance/migration-issues-registry.md`](migration-issues-registry.md)
- Реестр research-зависимостей (M-007): [`docs/hub-research-dependencies.md`](../docs/hub-research-dependencies.md) *(создаётся)*
- Контракт и правила: [`AI_GOVERNANCE.md`](../AI_GOVERNANCE.md), [`AI_QUICK_RULES.md`](../AI_QUICK_RULES.md)
- Хаб, проект Mango (snapshot): <https://github.com/G-Ivan-A/hybrid-Intelligence-lab/tree/038868dd125b4e2d849ff73604890f1d2787ac0f/projects/mango>
- Хаб, исследования Mango: <https://github.com/G-Ivan-A/hybrid-Intelligence-lab/tree/038868dd125b4e2d849ff73604890f1d2787ac0f/research/mango>
