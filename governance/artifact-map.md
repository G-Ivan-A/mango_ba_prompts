---
status: draft
version: 0.1
updated: 2026-06-13
temperature: 0.1
ai-generated: true
executable: false
source_hub: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/b683341d22d4f518618917a02d9c7c394658b156/governance/artifact-map.md"
source_sha: "b683341d22d4f518618917a02d9c7c394658b156"
---

# Artifact Map — mango_ba_prompts

Локальная карта активных артефактов `mango_ba_prompts`. Она адаптирует хабовую
`governance/artifact-map.md` под HTOM-команду Mango BA Prompts: показывает, где
лежит рабочий контекст, какие файлы являются входными точками и какие артефакты
нужно обновлять при Smart Sync.

> **Источник синхронизации:** Hub PR #224 + PR #226 + PR #229 + PR #230, latest
> Hub SHA `b683341d22d4f518618917a02d9c7c394658b156`. Хабовая карта остаётся источником
> общих правил, а эта карта отражает фактическое состояние локального репозитория.

## Терминология ролей

| Термин | Значение в этом репозитории |
| --- | --- |
| **Пользователь** | Человек, который ставит задачу, утверждает решения и передаёт контекст между чатами. |
| **Исполнитель** | Агент или человек, который выполняет задачу через issue → PR → review. |
| **Внешний агент** | LLM-чат, которому Пользователь передаёт контекст для анализа, планирования или подготовки задачи. |
| **Агент-исполнитель** | Исполнитель автоматизированной задачи, например Конард; он не использует session digests во время исполнения. |

## Карта артефактов

| Путь | Тип | Назначение | Обязательный? | Связанные артефакты |
| --- | --- | --- | --- | --- |
| `/README.md` | навигация | Визитка проекта, стратегия, структура и быстрые ссылки. | Да | `CHANGELOG.md`, `docs/ba-ecosystem.md`, `prompts/README.md` |
| `/CHANGELOG.md` | журнал | История значимых изменений, включая Smart Sync из Хаба. | Да | `README.md`, `.hub-profile.json` |
| `/.hub-profile.json` | профиль синхронизации | Локальный профиль Smart Sync: тип проекта, Хаб и последний sync snapshot. | Да | `AI_SESSION_HANDOVER_PROMPT.md`, `governance/artifact-map.md` |
| `/AI_GOVERNANCE.md` | контракт | Роли, operating modes, границы AI-assisted work и Definition of Done. | Да | `AI_QUICK_RULES.md`, `CONTRIBUTING.md` |
| `/AI_QUICK_RULES.md` | исполнимые правила | Короткая инструкция для агента: куда смотреть, чего не делать, когда звать человека. | Да | `AI_GOVERNANCE.md`, `README.md` |
| `/CONTRIBUTING.md` | workflow | Процесс issue → PR → review и чек-лист вклада. | Да | `AI_GOVERNANCE.md`, `CHANGELOG.md` |
| `/AI_SESSION_HANDOVER_PROMPT.md` | исполнимый prompt | Готовый prompt для Runtime-онбординга и передачи контекста между чатами; синхронизирован с Hub v0.5. | Да | `governance/session-digests.md`, `governance/agent-onboarding-protocol.md` |
| `/governance/agent-onboarding-protocol.md` | протокол | Локальная адаптация протокола онбординга агента. | Да | `AI_SESSION_HANDOVER_PROMPT.md`, `AI_GOVERNANCE.md` |
| `/governance/session-digests.md` | журнал / индекс | Индекс суммарий длинных сессий для передачи контекста между чатами; создан в issue #72. | По необходимости | `AI_SESSION_HANDOVER_PROMPT.md` |
| `/governance/artifact-map.md` | навигация | Эта карта активных артефактов и связей. | По необходимости | `README.md`, `.hub-profile.json` |
| `/governance/approval-contract.md` | контракт процесса | Исполнимый governance-контракт AI-агента для атомарного согласования документов. | По необходимости | `AI_GOVERNANCE.md`, `CONTRIBUTING.md`, `governance/rfc-process.md` |
| `/governance/bcreq-fr-generation-contract.md` | контракт процесса | Исполнимый контракт AI-агента для генерации комплексного BCREQ-FR: разделы 1-7, локальные scope rules `BCREQ-FR-GEN-SCOPE-01/02`, taxonomy/product-doc traceability и итоговая валидация. | По необходимости | `kb/industry-taxonomy/registry.json`, `kb/mango-taxonomy/registry.json` |
| `/governance/rfc-generation-contract.md` | контракт процесса | Исполнимый L1-контракт генерации RFC: L3 Markdown с YAML frontmatter, полные входы, machine-readable problem/proposal structure, traceability и impact fields. | По необходимости | `governance/contracts-registry.md`, `governance/rfc-process.md`, `standards/executable-contract-standard.md` |
| `/governance/contracts-registry.md` | реестр | L2 YAML-реестр source/provenance исполнимых контрактов; runtime/L1-контракты ссылаются на записи только через `contract_registry_id`. | По необходимости | `standards/executable-contract-standard.md`, `governance/bcreq-fr-generation-contract.md`, `governance/rfc-generation-contract.md`, `runs/CONTRACT.md`, `kb/golden-examples/CONTRACT.md`, `CHANGELOG.md` |
| `/governance/migration-manifest.md` | manifest | Живой снимок миграции Mango из Хаба и последующих sync snapshots. | Да | `docs/analysis/migration-strategy-rfc.md`, `.hub-profile.json` |
| `/docs/hub-research-dependencies.md` | реестр ссылок | Единый мост к research-материалам Хаба, включая reference-only срез external sources registry из Hub PR #229; research не копируется в спок. | Да | `prompts/`, `standards/product-classification-contract.md` |
| `/docs/ba-ecosystem.md` | методология | Карта экосистемы работы БА Mango, графы связей и сценарии запуска. | Да | `docs/taxonomy.md`, `docs/ba-processes/00-index.md` |
| `/docs/taxonomy.md` | стандарт / модель | Таксономия когнитивных операций и процессов БА. | Да | `patterns/`, `prompts/` |
| `/docs/ba-processes/00-index.md` | индекс | Маппинг процесс ↔ операция ↔ паттерн ↔ промпт. | Да | `patterns/`, `prompts/README.md` |
| `/docs/adr/` | решения | ADR: почему принято конкретное архитектурное или governance-решение. | По необходимости | `CHANGELOG.md`, `AI_GOVERNANCE.md` |
| `/patterns/` | каталог | Паттерны БА как reusable способы решения классов задач. | Да | `standards/pattern-standard.md`, `docs/taxonomy.md` |
| `/prompts/` | каталог | Активные prompt assets для бизнес-аналитиков Mango. | Да | `prompts/README.md`, `standards/prompt-standard.md` |
| `/prompts/archive/` | каталог | Архивные legacy-промпты, выведенные из активного использования. | По необходимости | `prompts/README.md` |
| `/kb/golden-examples/` | контракт и каталог | Lifecycle Golden Examples: хранение будущих approved examples, `path + sha`, `no-golden-standard` placeholders и 2-факторное подтверждение для BCREQ-FR. | По необходимости | `governance/bcreq-fr-generation-contract.md`, `governance/approval-contract.md` |
| `/runs/` | каталог | Единый каталог результатов выполнения процессов, экспериментов и self-test прогонов по `runs/YYYY/RUN-XXXX/`. | По необходимости | `standards/runs-contract-standard.md`, `docs/ba-processes/` |
| `/standards/` | каталог | Локальные рабочие копии стандартов и контрактов. | Да | `README.md`, `docs/adr/` |
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

- Хаб [`governance/artifact-map.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/b683341d22d4f518618917a02d9c7c394658b156/governance/artifact-map.md)
  — источник общей карты артефактов.
- [`governance/session-digests.md`](session-digests.md) — новый sync-артефакт
  issue #72.
- [`governance/migration-manifest.md`](migration-manifest.md) — исторический
  снимок миграции Mango и запись sync snapshots.
