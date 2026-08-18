---
status: accepted
version: 1.0
updated: 2026-06-10
ai-generated: true
type: adr
scope: mango_ba_prompts-governance-sync
issue: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/46"
hub_pr: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/208"
hub_sync_sha: "117e4a553815af9b05d841c81dd725dd4a4c4d44"
supersedes_sha: "038868dd125b4e2d849ff73604890f1d2787ac0f"
---

# ADR-0001: Синхронизация governance-файлов с Хабом после PR #208

> **Статус:** Accepted · **Дата:** 2026-06-10 · **Issue:**
> [#46](https://github.com/G-Ivan-A/mango_ba_prompts/issues/46) · **Источник:** Хаб
> [PR #208](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/208)
> (Smart Sync + семантическое разделение онбординга), merge-SHA
> [`117e4a55`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/tree/117e4a553815af9b05d841c81dd725dd4a4c4d44).

## Контекст

Хаб `hybrid-Intelligence-lab` в PR #208 внёс три изменения, затрагивающие
downstream-репозитории:

1. **Реклассификация.** RFC
   [`governance/rfc/htom-vs-spoke-clarification-2026-06.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/117e4a553815af9b05d841c81dd725dd4a4c4d44/governance/rfc/htom-vs-spoke-clarification-2026-06.md)
   разделил два типа downstream-репозиториев: **spoke** (production-продукт с
   `src/`, `tests/`, CI/CD) и **HTOM-команда** (гибридная команда человек+ИИ с
   минимальной структурой governance, без кода). `mango_ba_prompts` явно отнесён к
   **HTOM-командам**. Каталог шаблонов в Хабе переименован `templates/spoke/` →
   `templates/htom/`.
2. **Smart Sync.** Добавлен `tools/sync-from-hub.sh`, который читает
   `templates/manifest.json` Хаба и локальный профиль `.hub-profile.json` команды.
3. **Семантическое разделение онбординга.** *Артефакт* (готовый к копированию
   `AI_SESSION_HANDOVER_PROMPT.md`) отделён от *протокола*
   (`ai-rules/agent-onboarding-protocol_old.md` — процесс и чек-лист).

Issue #46 поставил 6 задач: создать `AI_SESSION_HANDOVER_PROMPT.md`,
онбординг-протокол и `.hub-profile.json`; синхронизировать `AI_GOVERNANCE.md` и
`AI_QUICK_RULES.md` из `templates/htom/`; проверить структуру каталогов. При
жёстких ограничениях: **не** создавать новых папок без необходимости, **не**
удалять промпты, **не** менять workflow промптов, **сохранить** все
mango-специфичные правила, все новые файлы — в kebab-case.

**Ядро проблемы.** Часть буквального текста issue (имена ключей, имена файлов)
расходится с **фактической** инфраструктурой Хаба и с уже сложившейся культурой
mango (permalink-pinning, отсутствие валидатора структуры). Слепое следование
букве сломало бы либо Smart Sync, либо собственные правила mango. Поэтому
отклонения приняты **сознательно** и зафиксированы здесь.

## Решение

1. Синхронизировать четыре файла из `templates/htom/` Хаба, **закрепив каждый
   permalink-ом** на merge-SHA PR #208
   [`117e4a55`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/tree/117e4a553815af9b05d841c81dd725dd4a4c4d44)
   через поля `source_hub` / `source_sha` во frontmatter.
2. **Сохранить** mango-специфичные правила поверх шаблона Хаба (не затирать их
   обновлением).
3. Принять терминологию **«HTOM-команда»** в синхронизируемых governance- и
   онбординг-файлах.
4. Все осознанные расхождения с буквой issue зафиксировать в этом ADR (маршрут
   эскалации из `AI_GOVERNANCE.md` / `AI_QUICK_RULES.md`: «осознанное отклонение —
   ADR в `docs/adr/`»).

## Отклонения от буквы issue (и почему)

| # | Сказано в issue / шаблоне Хаба | Что сделано | Почему |
| :--- | :--- | :--- | :--- |
| D1 | `.hub-profile.json` с ключами `project_type` / `current_phase` | Ключи `target_type` / `phase` (+ `project_name`, `stack`, `hub_url`, `last_sync`) | `tools/sync-from-hub.sh` Хаба фактически читает `target_type` / `phase`. Ключи из issue молча игнорировались бы — Smart Sync не заработал бы. Имена приведены к контракту инструмента. |
| D2 | Файл `AGENT_ONBOARDING_PROTOCOL.md` (UPPER_SNAKE, корень) | [`ai-rules/agent-onboarding-protocol_old.md`](../../ai-rules/agent-onboarding-protocol_old.md) (kebab-case, в `governance/`) | Само же требование issue: «все новые файлы в kebab-case». Канонический путь в Хабе — тоже `ai-rules/agent-onboarding-protocol_old.md`. UPPER-имя в корне нарушило бы и kebab-правило, и трассируемость к Хабу. |
| D3 | (Унаследованная терминология «спок») | Терминология **«HTOM-команда»** в 4 синхронизированных файлах | PR #208 переклассифицировал mango как HTOM-команду (RFC выше). Источник шаблона — `templates/htom/`, где терминология уже HTOM. Миграция терминологии в `README.md` / `CONTRIBUTING.md` **отложена** (они вне sync-списка issue; полный rewrite — отдельная задача, см. «Последствия»). |
| D4 | Заменить `{{REPO_NAME}}` → `mango_ba_prompts` | Подставлено | Шаблон Хаба намеренно **не** трогает `{{REPO_NAME}}` через `init.sh` (это забота валидатора/инициализатора Хаба). У mango такого валидатора нет, поэтому полная подстановка безопасна и соответствует задаче issue. |
| D5 | `templates/htom/` Хаба содержит `tools/`, `.github/ISSUE_TEMPLATE/`, `init.sh` | **Не** переносим их | Anti-Inflation + прямой запрет issue «не создавать новых папок без необходимости». Операционной боли нет; mango никогда не заводил `tools/`. |
| D6 | Хабовый `AI_GOVERNANCE.md` → DoD со строкой `./tools/validate-repository-structure.sh` (exit 0) | Строка заменена на «структура соответствует целевой из [`docs/audit/initial-state-2026-06.md`](../audit/initial-state-2026-06.md)» | Следствие D5: валидатора в mango нет, ссылка на него в DoD была бы битой. Заменена на **существующий** в mango структурный ориентир. |
| D7 | (Стэйл в текущем mango-файле) `AI_GOVERNANCE.md` ссылался на `kb/glossary.md` | Исправлено на [`standards/GLOSSARY.md`](../../standards/GLOSSARY.md) | `kb/glossary.md` удалён в M-003 (см. `CHANGELOG.md`); глоссарий живёт в `standards/GLOSSARY.md`. Битый путь исправлен попутно при синхронизации. |
| D8 | Хабовый шаблон ссылается на Хаб как `{{hub_url}}/blob/main/...` (mutable branch) | Все ссылки на Хаб — **полные permalink-и** на SHA `117e4a55` | Культура mango (README): hub-относительные и mutable-branch ссылки запрещены; provenance закрепляется permalink-ом на коммит. |

### Сохранённые mango-специфичные правила (по требованию issue)

| Файл | Что сохранено поверх шаблона |
| :--- | :--- |
| [`AI_GOVERNANCE.md`](../../AI_GOVERNANCE.md) | Конкретная taxonomy **«Capability Boundaries»** (с реальными путями репозитория и ссылкой на fail-closed) вместо общей прозы «Границы действий» из шаблона Хаба. Добавлена связка-примечание: это «конкретная инстанциация хабовой рубрики под mango». |
| [`AI_QUICK_RULES.md`](../../AI_QUICK_RULES.md) | Явная секция **«Fail-Closed Semantics (КРИТИЧНО)»** (шаблон Хаба её свернул). Нужна и как mango-правило, и чтобы оставалась резолвимой перекрёстная ссылка `AI_GOVERNANCE.md#fail-closed-semantics-критично`. |
| [`agent-onboarding-protocol.md`](../../ai-rules/agent-onboarding-protocol_old.md) | Раздел «Design Rationale & History» **сжат** до операционно важной выжимки (авиа-аналогия + таблица зафиксированных решений); полная история вынесена ссылкой на канонический протокол Хаба, чтобы локальная копия оставалась лёгкой. |

## Что НЕ делали (negative checks)

- **Не создавали** `research/` и `templates/` — подтверждено проверкой структуры
  (задача #6 issue). Фундаментальные знания остаются в `research/` Хаба.
- **Не добавляли** `tools/`, `.github/ISSUE_TEMPLATE/`, `init.sh` из
  `templates/htom/` (D5).
- **Не трогали** промпты в `prompts/` и их workflow `draft → canonical`.
- **Не удаляли** существующие файлы.

## Последствия

**Положительные:**

- `.hub-profile.json` совместим со Smart Sync Хаба — будущие синки автоматизируемы.
- Онбординг-артефакт и протокол семантически разделены, как в Хабе.
- Provenance каждого синхронизированного файла закреплён permalink-ом на SHA —
  воспроизводимый снимок синхронизации.

**Отрицательные / технический долг (follow-up):**

- **Терминологический разрыв.** `README.md` и `CONTRIBUTING.md` всё ещё описывают
  mango как «спок», а governance-файлы — уже как «HTOM-команду». Полная миграция
  терминологии — **отдельная задача** (вне scope issue #46). До неё оба термина
  сосуществуют; для читателя это поясняется здесь.
- **SHA-дрейф провенанса.** Предыдущие артефакты (`pr-ops/migration-manifest.md`,
  промпты) закреплены на старом snapshot `038868dd`; новые governance-файлы — на
  `117e4a55`. Это ожидаемо (разные акты синхронизации), но при будущем аудите
  важно не путать снимки.
- **Ручной Smart Sync.** `last_sync` в профиле пуст: клиент Smart Sync в mango
  ещё не запускался; первая синхронизация выполнена вручную в рамках issue #46.

## Альтернативы (отклонены)

- **Буквально следовать issue** (`project_type`/`current_phase`, root
  `AGENT_ONBOARDING_PROTOCOL.md`, перенос валидатора). Отклонено: сломало бы Smart
  Sync (D1), нарушило бы kebab-правило (D2) и Anti-Inflation (D5).
- **Полностью затереть mango-файлы шаблоном Хаба.** Отклонено: нарушило бы
  требование «сохранить все специфичные правила mango» и сломало бы внутренние
  перекрёстные ссылки (fail-closed).
- **Заодно мигрировать терминологию во всех файлах** (`README.md`,
  `CONTRIBUTING.md`). Отклонено: выходит за scope issue #46; крупный rewrite
  заслуживает отдельного issue и review.

## Связанные артефакты

- Issue: <https://github.com/G-Ivan-A/mango_ba_prompts/issues/46>
- Хаб, PR #208: <https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/208>
- Хаб, RFC HTOM↔spoke: [`governance/rfc/htom-vs-spoke-clarification-2026-06.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/117e4a553815af9b05d841c81dd725dd4a4c4d44/governance/rfc/htom-vs-spoke-clarification-2026-06.md)
- Хаб, шаблоны HTOM-команды: [`templates/htom/`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/tree/117e4a553815af9b05d841c81dd725dd4a4c4d44/templates/htom)
- Синхронизированные файлы: [`AI_GOVERNANCE.md`](../../AI_GOVERNANCE.md),
  [`AI_QUICK_RULES.md`](../../AI_QUICK_RULES.md),
  [`AI_SESSION_HANDOVER_PROMPT.md`](../../AI_SESSION_HANDOVER_PROMPT.md),
  [`ai-rules/agent-onboarding-protocol_old.md`](../../ai-rules/agent-onboarding-protocol_old.md),
  [`.hub-profile.json`](../../.hub-profile.json)
- Целевая структура (negative check): [`docs/audit/initial-state-2026-06.md`](../audit/initial-state-2026-06.md)
- Снимок предыдущей миграции: [`pr-ops/migration-manifest.md`](../../pr-ops/migration-manifest.md)
