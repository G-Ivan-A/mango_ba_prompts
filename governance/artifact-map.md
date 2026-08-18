---
status: draft
version: 0.4
updated: 2026-08-18
owner: G-Ivan-A
temperature: 0.1
ai-generated: true
executable: false
source_hub: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/3bfa4103c9efbbd59bc951814884920e406982e2/pr-ops/artifact-map.md"
source_sha: "3bfa4103c9efbbd59bc951814884920e406982e2"
---

# Artifact Map — mango_ba_prompts

Локальная карта активных артефактов `mango_ba_prompts`. Она адаптирует хабовую
карту артефактов (в Хабе она переехала в `pr-ops/artifact-map.md`) под HTOM-команду Mango BA Prompts: показывает, где
лежит рабочий контекст, какие файлы являются входными точками и какие артефакты
нужно обновлять при Smart Sync.

> **Источник синхронизации:** ре-синк issue #265, Hub SHA
> `3bfa4103c9efbbd59bc951814884920e406982e2` (предыдущая точка —
> `b683341d22d4f518618917a02d9c7c394658b156`, issue #72; история точек синка —
> `sync_history` в [`.hub-profile.json`](../.hub-profile.json)). Хабовая карта
> остаётся источником общих правил, а эта карта отражает фактическое состояние
> локального репозитория.

## Терминология ролей

| Термин | Значение в этом репозитории |
| --- | --- |
| **Пользователь** | Человек, который ставит задачу, утверждает решения и передаёт контекст между чатами. |
| **Исполнитель** | Агент или человек, который выполняет задачу через issue → PR → review. |
| **Внешний агент** | LLM-чат, которому Пользователь передаёт контекст для анализа, планирования или подготовки задачи. |
| **Агент-исполнитель** | AI-исполнитель автоматизированной задачи; он не использует session digests во время исполнения. |

## Карта артефактов

| Путь | Тип | Назначение | Обязательный? | Связанные артефакты |
| --- | --- | --- | --- | --- |
| `/README.md` | навигация | Визитка проекта: роль (автоматизация процессов БА в проекте Манго), границы (GitHub + AI-исполнитель, без инфраструктуры), стратегия, структура и быстрые ссылки. | Да | `CHANGELOG.md`, `docs/ba-ecosystem.md`, `prompts/README.md` |
| `/CHANGELOG.md` | журнал | История значимых изменений, включая Smart Sync из Хаба. | Да | `README.md`, `.hub-profile.json` |
| `/.hub-profile.json` | профиль синхронизации | Локальный профиль Smart Sync: тип проекта, Хаб и последний sync snapshot. | Да | `AI_SESSION_HANDOVER_PROMPT.md`, `governance/artifact-map.md` |
| `/AI_GOVERNANCE.md` | контракт | Конституция проекта: принцип «качество системы исполнения > стоимость», ДОД с процессом проверки, роль проекта и инфраструктурная модель, подготовка к приватизации, роли, operating modes, границы AI-assisted work. | Да | `AI_QUICK_RULES.md`, `CONTRIBUTING.md`, `docs/hub-research-dependencies.md` |
| `/AI_QUICK_RULES.md` | исполнимые правила | Короткая инструкция для агента: куда смотреть, чего не делать, когда звать человека. | Да | `AI_GOVERNANCE.md`, `README.md` |
| `/CONTRIBUTING.md` | workflow | Процесс issue → PR → review и чек-лист вклада. | Да | `AI_GOVERNANCE.md`, `CHANGELOG.md` |
| `/AI_SESSION_HANDOVER_PROMPT.md` | исполнимый prompt | Готовый prompt для Runtime-онбординга и передачи контекста между чатами; синхронизирован с Hub v0.5. | Да | `governance/session-digests.md`, `governance/agent-onboarding-protocol.md` |
| `/governance/agent-onboarding-protocol.md` | протокол | Локальная адаптация протокола онбординга агента. | Да | `AI_SESSION_HANDOVER_PROMPT.md`, `AI_GOVERNANCE.md` |
| `/governance/session-digests.md` | журнал / индекс | Индекс суммарий длинных сессий для передачи контекста между чатами; создан в issue #72. | По необходимости | `AI_SESSION_HANDOVER_PROMPT.md` |
| `/governance/artifact-map.md` | навигация | Эта карта активных артефактов и связей. | По необходимости | `README.md`, `.hub-profile.json` |
| `/governance/migration-manifest.md` | manifest | Живой снимок миграции Mango из Хаба и последующих sync snapshots. | Да | `docs/analysis/migration-strategy-rfc.md`, `.hub-profile.json` |
| `/docs/hub-research-dependencies.md` | реестр ссылок | Единый мост к research-материалам и решениям Хаба: research PR #229, ADR-009 v0.3, онтология процессов БА (D1–D10), анализ готовности к разделению. Источники не копируются в спок. | Да | `prompts/`, `standards/product-classification-contract.md`, `AI_GOVERNANCE.md` |
| `/docs/ba-ecosystem.md` | методология | Карта экосистемы работы БА Mango, ДОД операции с обязательным процессом проверки, графы связей, сценарии запуска и границы автоматизации спока. | Да | `docs/taxonomy.md`, `docs/ba-processes/00-index.md` |
| `/docs/rfc-hub-integration.md` | RFC | Односторонний неавтоматический поток практик наружу: Хаб (методология) и `ai-ba-playbooks` (универсальные и специализированные плейбуки). | Да | `docs/hub-research-dependencies.md`, `standards/pattern-standard.md` |
| `/docs/taxonomy.md` | стандарт / модель | Таксономия когнитивных операций и процессов БА. | Да | `patterns/`, `prompts/` |
| `/docs/ba-processes/00-index.md` | индекс | Маппинг процесс ↔ операция ↔ паттерн ↔ промпт. | Да | `patterns/`, `prompts/README.md` |
| `/docs/adr/` | решения | ADR: почему принято конкретное архитектурное или governance-решение. | По необходимости | `CHANGELOG.md`, `AI_GOVERNANCE.md` |
| `/patterns/` | каталог | Паттерны БА как reusable способы решения классов задач. | Да | `standards/pattern-standard.md`, `docs/taxonomy.md` |
| `/prompts/` | каталог | Активные prompt assets для бизнес-аналитиков Mango. | Да | `prompts/README.md`, `standards/prompt-standard.md` |
| `/prompts/archive/` | каталог | Архивные legacy-промпты, выведенные из активного использования. | По необходимости | `prompts/README.md` |
| `/runs/` | каталог | Единый каталог результатов выполнения процессов, экспериментов и self-test прогонов по `runs/YYYY/RUN-XXXX/`. | По необходимости | `standards/runs-contract-standard.md`, `docs/ba-processes/` |
| `/standards/` | каталог | Стандарты спицы и рабочие копии стандартов Хаба; разграничение — в `standards/README.md`. | Да | `standards/README.md`, `docs/adr/` |
| `/standards/README.md` | навигация | Реестр стандартов: что принадлежит спице, что рабочая копия Хаба, и правило «сужать можно, противоречить нельзя». | Да | `standards/GLOSSARY.md`, `docs/adr/0004-hub-resync-2026-08.md` |
| `/ai-rules/` | рабочие копии Хаба | Правила поведения агента-исполнителя: `agent-work-rules.md`, `agent-onboarding-protocol.md`, `adversarial-stress-testing.md`. Локально не редактируются. | Да | `governance/agent-onboarding-protocol.md`, `AI_GOVERNANCE.md` |
| `/ai-governance/` | рабочие копии Хаба | Политики уровня организации, compliance и ИБ, включая `agent-security-checklist.md`. Локально не редактируются. | Да | `AI_GOVERNANCE.md`, `docs/adr/0004-hub-resync-2026-08.md` |
| `/scripts/sync_from_hub.py` | инструмент | Воспроизводимый ре-синк по манифесту с переписыванием ссылок; `--check` сверяет копии с Хабом. | Да | `.hub-profile.json`, `scripts/validate_issue_265_hub_sync.py` |
| `/.github/ISSUE_TEMPLATE/` | шаблон | GitHub issue templates для структурированного фидбека. | По необходимости | `CONTRIBUTING.md` |

## Smart Sync decisions: Hub PR #229/#230

- **Hub PR #229:** `research/external-knowledge/external-sources-registry.md`
  релевантен для Mango только как Base Registry. Он зарегистрирован в
  [`docs/hub-research-dependencies.md`](../docs/hub-research-dependencies.md)
  как reference-only срез (`ext-003`, `ext-007`) и не копируется в локальный
  `research/`.
- **Hub PR #230:** активная терминология `Пользователь / Исполнитель` применена
  к текущим guidance-файлам. Traceability contracts, Framework vs Template и
  Scope Resolver-а остаются Hub-governance контрактами и не создают новых
  локальных артефактов в `mango_ba_prompts`.

## Ре-синк issue #265 (2026-08-17)

- **Перенесено:** `ai-rules/` (4 файла), `ai-governance/` (3 файла),
  `standards/GLOSSARY.md`, `standards/evals-contract-standard.md`,
  `standards/analysis-standard.md`, `standards/research-standard.md` — все на
  одном `source_sha`.
- **Сознательно не перенесено:** реестр стандартов Хаба, контракты frontmatter и
  именования, `*-structure-standard.md`, клиент Smart Sync `tools/`. Обоснование
  по каждому пункту — [ADR-0004](../docs/adr/0004-hub-resync-2026-08.md).
- **Приоритет норм:** рабочая копия Хаба — базовая норма; локальный артефакт
  спицы может её сужать, но не противоречить. Копии не редактируются локально.
- **Проверка:** `python3 scripts/validate_issue_265_hub_sync.py` (0 битых
  относительных ссылок, единый `source_sha`, нет путей за корень репозитория).
## Решения ADR-009 v0.3: место спока в модели 2-х репозиториев

- **`mango_ba_prompts` остаётся собой** и меняет видимость на Private; новый
  приватный репозиторий не создаётся, `mango-ba-prompt-library` — тоже.
- **`ai-ba-playbooks`** создаётся отдельно как публичная витрина методологии;
  его артефакты не регистрируются в этой карте — она отражает только локальный
  репозиторий.
- **Синхронизация односторонняя и ручная:** артефакты уходят наружу через
  [`docs/rfc-hub-integration.md`](../docs/rfc-hub-integration.md); входящих
  потоков из `ai-ba-playbooks` нет.
- **Инфраструктурных артефактов не добавляется:** серверная инфраструктура,
  оркестраторы и мультиагентные контуры в карту не попадают — их здесь нет.
- Источник решения — [`#adr-009-repo-split`](../docs/hub-research-dependencies.md#adr-009-repo-split).

## Как обновлять карту

- При создании нового активного артефакта добавь строку в таблицу и обнови
  `README.md`, если это новая точка входа.
- При Smart Sync из Хаба обнови `source_sha`, `updated`, связанные строки
  таблицы и `.hub-profile.json`.
- Не добавляй в карту файлы «на вырост»: карта отражает фактическое состояние,
  а не планы.
- Если Хаб предлагает общий артефакт, адаптируй его под локальные пути
  `mango_ba_prompts` и сохраняй traceability на source SHA.

## См. также

- Хаб [`pr-ops/artifact-map.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/3bfa4103c9efbbd59bc951814884920e406982e2/pr-ops/artifact-map.md)
  — источник общей карты артефактов.
- [`governance/session-digests.md`](session-digests.md) — новый sync-артефакт
  issue #72.
- [`governance/migration-manifest.md`](migration-manifest.md) — исторический
  снимок миграции Mango и запись sync snapshots.
