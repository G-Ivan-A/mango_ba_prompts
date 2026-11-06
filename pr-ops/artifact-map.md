---
status: draft
version: 0.22
updated: 2026-11-06
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
| `/.hub-profile.json` | профиль синхронизации | Локальный профиль Smart Sync: тип проекта, Хаб и последний sync snapshot. | Да | `ai-rules/AI_SESSION_HANDOVER_PROMPT.md`, `pr-ops/artifact-map.md` |
| `/ai-governance/ai-governance.md` | контракт | Конституция проекта: принцип «качество системы исполнения > стоимость», ДОД с процессом проверки, роль проекта и инфраструктурная модель, подготовка к приватизации, роли, operating modes, границы AI-assisted work. | Да | `ai-rules/ai-quick-rules.md`, `CONTRIBUTING.md`, `docs/hub-research-dependencies.md` |
| `/ai-rules/ai-quick-rules.md` | исполнимые правила | Короткая инструкция для агента: куда смотреть, чего не делать, когда звать человека. | Да | `ai-governance/ai-governance.md`, `README.md` |
| `/CONTRIBUTING.md` | workflow | Процесс issue → PR → review и чек-лист вклада. | Да | `ai-governance/ai-governance.md`, `CHANGELOG.md` |
| `/ai-rules/AI_SESSION_HANDOVER_PROMPT.md` | исполнимый prompt | Готовый prompt для Runtime-онбординга и передачи контекста между чатами; синхронизирован с Hub v0.5. | Да | `pr-ops/session-digests.md`, `ai-rules/agent-onboarding-protocol.md` |
| `/ai-rules/agent-onboarding-protocol.md` | протокол | Актуальный протокол онбординга агента (v1.5, рабочая копия Хаба). Точка входа для агентов. | Да | `ai-rules/AI_SESSION_HANDOVER_PROMPT.md`, `ai-governance/ai-governance.md` |
| `/.archive/ai-rules/agent-onboarding-protocol_old.md` | протокол (архив) | Локальная адаптация v1.2, `status: superseded`. Хранится только для traceability, точкой входа не является. | Нет (архив) | `ai-rules/agent-onboarding-protocol.md` |
| `/pr-ops/session-digests.md` | журнал / индекс | Индекс суммарий длинных сессий для передачи контекста между чатами; создан в issue #72. | По необходимости | `ai-rules/AI_SESSION_HANDOVER_PROMPT.md` |
| `/pr-ops/artifact-map.md` | навигация | Эта карта активных артефактов и связей. | По необходимости | `README.md`, `.hub-profile.json` |
| `/pr-ops/migration-manifest.md` | manifest | Живой снимок миграции Mango из Хаба и последующих sync snapshots. | Да | `docs/analysis/migration-strategy-rfc.md`, `.hub-profile.json` |
| `/standards/bcreq-manual-classes/` | стандарты спицы, draft | 39 отдельных классов ручных BCREQ-промптов; каталог экземпляров четырёх фаз. | Да для нового маршрута | `docs/contracts/bcreq-manual-state.md`, `docs/rfc/2026-10-bcreq-manual-pipeline.md`, `runs/2026/RUN-0078/` |
| `/docs/rfc/` | каталог | RFC спицы и пакеты передачи знаний в Хаб: процесс RFC, реестр, предложения по промптам, `knowledge-transfer-to-hub/`. | По необходимости | `docs/rfc-hub-integration.md`, `CHANGELOG.md` |
| `/docs/audit/` | каталог | Исторические аудиты контрактов, Хаба и research (2026-06-17, #1027). Не действующая норма — фактура для решений. | По необходимости | `docs/adr/`, `pr-ops/migration-manifest.md` |
| `/pr-ops/BACKLOG.md` | журнал | Входной документ бэклога (issue #418): порядок работ, решения владельца Р-01…Р-12, спринты в формате бэклога Хаба, открытые вопросы, технический долг, архив прежнего плана. | Да | `pr-ops/backlog-ba-model.md`, `pr-ops/backlog-repository.md`, `pr-ops/backlog-instruction.md`, `CONTRIBUTING.md`, `docs/adr/` |
| `/pr-ops/backlog-ba-model.md` | журнал | Карточки задач трека Б `BL-1xx` (модель БА: процессы, промпты, уроки, golden set, этапы 1–5): почему, что меняется, источники с цитатой, когда готово. | Да | `pr-ops/BACKLOG.md`, `docs/rfc/2026-10-bcreq-run-lessons-pipeline.md` |
| `/pr-ops/backlog-repository.md` | журнал | Карточки задач трека А `BL-2xx` (документы и устройство репозитория). | Да | `pr-ops/BACKLOG.md`, `docs/rfc/2026-10-repository-modernization.md` |
| `/pr-ops/backlog-instruction.md` | регламент | Правила ведения бэклога: роли файлов, ID, формат спринта и карточки, статусы, решения владельца, архивация, отличия от бэклога Хаба, проверки. | Да | `pr-ops/BACKLOG.md`, `scripts/validate_issue_418_backlog.py` |
| `/pr-ops/prompt-feedback.json` | данные | Фидбек по промптам; источник для веб-каталога (`scripts/generate-pages-data.mjs`). | По необходимости | `prompts/README.md`, `site/data/` |
| `/docs/hub-research-dependencies.md` | реестр ссылок | Единый мост к research-материалам и решениям Хаба: research PR #229, ADR-009 v0.3, онтология процессов БА (D1–D10), анализ готовности к разделению. Источники не копируются в спок. | Да | `prompts/`, `standards/product-classification-contract.md`, `ai-governance/ai-governance.md` |
| `/docs/ba-ecosystem.md` | методология | Карта экосистемы работы БА Mango, ДОД операции с обязательным процессом проверки, графы связей, сценарии запуска и границы автоматизации спока. | Да | `docs/taxonomy.md`, `docs/ba-processes/00-index.md` |
| `/docs/rfc-hub-integration.md` | RFC | Односторонний неавтоматический поток практик наружу: Хаб (методология) и `ai-ba-playbooks` (универсальные и специализированные плейбуки). | Да | `docs/hub-research-dependencies.md`, `standards/pattern-standard.md` |
| `/docs/taxonomy.md` | стандарт / модель | Таксономия когнитивных операций и процессов БА. | Да | `patterns/`, `prompts/` |
| `/docs/ba-processes/00-index.md` | индекс | Маппинг процесс ↔ операция ↔ паттерн ↔ промпт. | Да | `patterns/`, `prompts/README.md` |
| `/docs/ba-processes/cs-flow-stub.md` | заглушка | Поток CS «клиентский сервис»: выход из BCREQ при результате «Да» проверки исполнимости (issue #464, ADR-019, BL-235). | Да | `docs/ba-processes/bcreq-manual-process.md`, `standards/bcreq-sections/02-business-context.md` |
| `/standards/bcreq-industry-practice.md` | справочник | Индустриальные стандарты BCREQ: BABOK по пунктам, C4, TM Forum ODA, выбор на шаге Ш-А (issue #464). | Да | `site/index.html`, `standards/bcreq-sections/` |
| `/docs/ba-processes/bcreq-run-kit.md` | процесс | Комплект прогона BL-157 (v0.8, issue #464: новый шаг Ш-А; v0.5 — issue #450; v0.3 — issue #446): 14 шагов этапа 1, режим промпта шага (`published` или `by-test`; A-IN — `by-test` по RUN-0083), карточка прогона с `prompt_set.mode`, `prompt_ref`, `notes`. Источник тестового набора на сайте (`site/data/test-kit.json`). v0.4 (issue #448): Ш-В — v0.2 по RUN-0084; «Карточки шагов для БА (сайт)» — 4 этапа и 13 карточек, источник вкладок раздела «Процессы». | Да | `prompts/`, `prompts/drafts/`, `scripts/generate-pages-data.mjs`, `runs/` |
| `/docs/analysis/2026-09-03-hub-backlog-sprint-validation.md` | анализ | Протокол сплошной валидации активных спринтов бэклога Хаба (issue #357): фактическое состояние задач, доказательства абсолютными ссылками, дельта правок для `pr-ops/backlog.md` Хаба. | По необходимости | `docs/hub-research-dependencies.md`, `CHANGELOG.md` |
| `/docs/adr/` | решения | ADR: почему принято конкретное архитектурное или governance-решение. | По необходимости | `CHANGELOG.md`, `ai-governance/ai-governance.md` |
| `/patterns/` | каталог | Паттерны БА как reusable способы решения классов задач. | Да | `standards/pattern-standard.md`, `docs/taxonomy.md` |
| `/prompts/` | каталог | Активные prompt assets для бизнес-аналитиков Mango. | Да | `prompts/README.md`, `standards/prompt-standard.md` |
| `/prompts/archive/` | каталог | Архивные legacy-промпты, выведенные из активного использования. | По необходимости | `prompts/README.md` |
| `/runs/` | каталог | Единый каталог результатов выполнения процессов, экспериментов и self-test прогонов по `runs/YYYY/RUN-XXXX/`. | По необходимости | `standards/runs-contract-standard.md`, `docs/ba-processes/` |
| `/standards/` | каталог | Стандарты спицы и рабочие копии стандартов Хаба; разграничение — в `standards/README.md`. | Да | `standards/README.md`, `docs/adr/` |
| `/standards/README.md` | навигация | Реестр стандартов: что принадлежит спице, что рабочая копия Хаба, и правило «сужать можно, противоречить нельзя». | Да | `standards/GLOSSARY.md`, `docs/adr/0004-hub-resync-2026-08.md` |
| `/standards/bcreq-sections/` | стандарт | Мета-стандарты восьми разделов BCREQ (issue #387): README со стилями и общими правилами, файлы 01–08. | Да | `standards/bcreq-composition-standard.md`, `docs/contracts/bcreq-stage-gates.md`, `docs/adr/2026-10-adr-012-bcreq-meta-standards.md` |
| `/standards/bcreq-composition-standard.md` | стандарт | Композиция стандартов для кросс-продуктовых доработок: К1–К7, ODA-1…ODA-3, профили продуктов, примеры комбинаций. | Да | `standards/bcreq-sections/README.md`, `standards/industry-standards-standard.md` |
| `/standards/bcreq-prompt-architecture.md` | стандарт | Архитектура промптов BCREQ для Задачи 3: Промпт 0, шаблон шага, stepwise / oneshot, 14 файлов набора. | Да | `standards/prompt-standard.md`, `docs/contracts/bcreq-stage-gates.md` |
| `/docs/contracts/bcreq-stage-gates.md` | контракт | Стадии A-IN / A-CORE / A-WORK, гейты Г-IN, Г-С1, Г-W с решающими ролями, правила возврата, связь с П1–П6. | Да | `standards/bcreq-process-standard.md`, `standards/bcreq-prompt-architecture.md` |
| `/docs/analysis/2026-10-23-bcreq-standards-third-opinion.md` | анализ | Третье мнение по достаточности стека стандартов BCREQ (issue #387). | По необходимости | `standards/bcreq-composition-standard.md`, `docs/adr/2026-10-adr-012-bcreq-meta-standards.md` |
| `/docs/analysis/2026-10-28-bcreq-evolution-failure-analysis.md` | анализ | Эволюция требований Founder, разрывы наследования AGENTS, пять гипотез по СПЛИТ/1131 и проект проверенных защит (issue #397). | По необходимости | `experiments/issue_397/README.md`, `docs/reviews/issue-391-bcreq-review.md`, `CHANGELOG.md` |
| `/docs/rfc/2026-10-bcreq-meta-standards-rfc.md` | RFC | RFC-387-01…07 — инициированные изменения с путями отката. | По необходимости | `docs/rfc/rfc-register.md`, `docs/adr/2026-10-adr-012-bcreq-meta-standards.md` |
| `/docs/rfc/2026-11-bcreq-flow-processes-prompts.md` | RFC | RFC-427-DEC-01…13: поток BCREQ и цепочка Поток → Процесс → Операция → Артефакт, процессы потока, набор стандартов «по тесту», исключения ссылок на runtime, промпты по шагам, раздел «Процессы» в форме до 2.0.0, техдолг уровней таксономии операций S-010 (issue #427). | Да для Спринта 9 | `docs/rfc/rfc-register.md`, `docs/analysis/2026-11-02-bcreq-prompts-classes-standards-check.md`, `pr-ops/BACKLOG.md` |
| `/standards/bcreq-flow-glossary.md` | словарь | Термины потока BCREQ (BL-150, issue #430): поток, процесс, подпроцесс, операция, шаг, гейт с типами `человек` / `гибрид` / `llm` / `код` и ключевыми гейтами КГ-1…КГ-4, стадия, артефакт; два пространства номеров «Ш-»; префиксы ID. | Да для Спринта 9 | `docs/rfc/2026-11-bcreq-flow-processes-prompts.md`, `docs/ba-processes/bcreq-manual-process.md`, `docs/contracts/bcreq-stage-gates.md` |
| `/docs/analysis/2026-11-03-gate-types-bl-159-inventory.md` | анализ | Инвентаризация BL-159 (issue #433): где гейт получил тип `человек` / `гибрид` / `llm` / `код`, остаток поиска по категориям A/N/T/O/H/P с причинами, блок Р-16 → BL-162, перенос в BL-122, BL-156, BL-161. | По необходимости | `standards/bcreq-flow-glossary.md`, `scripts/validate_issue_433_gate_types.py`, `pr-ops/backlog-ba-model.md` |
| `/docs/analysis/2026-11-04-bl-157v-chat-analysis.md` | анализ | Разбор шести выгрузок чатов БА (BL-157в, issue #448): 255 правок, актуальность по принципу (176 закрыты, 75 частично, 4 не закрыты), открытые паттерны П-1…П-6, ответ «почему ИИ-агенты не предлагают отраслевую практику сразу», 50 кандидатов во вход BL-112. Данные — `experiments/issue_448/bl157v/` (обезличенная кодировка, свод). | По необходимости | `pr-ops/backlog-ba-model.md`, `standards/bcreq-lessons/lessons.json`, `docs/ba-processes/bcreq-run-kit.md` |
| `/standards/bcreq-runtime-references.md` | стандарт | Справочники runtime для промптов потока BCREQ (BL-154, BL-155, issue #430): И-1…И-10 по закреплённому SHA, ТС-1…ТС-7, каталог продуктов runtime И-2 со сверкой копии (BL-163, issue #442); v0.4 (BL-156а, issue #444) — срез `f31dcde3`, И-5 и И-6 «Да», М-4 — чтение каталога промптом Ш-2, заглушка З-2 (З-1, З-3, З-4 сняты), задачи для runtime РТ-1…РТ-4, РТ-6 (слиты), долг ссылок на `main` закрыт. | Да для Спринта 9 | `docs/rfc/2026-11-bcreq-flow-processes-prompts.md`, `pr-ops/backlog-ba-model.md` |
| `/standards/bcreq-prompt-base-standard.md` | стандарт | Базовый стандарт ручного промпта BCREQ «по тесту» (BL-151, issue #432): правила БС-01…БС-36 с источником, подключение справочников runtime ссылкой, типы гейтов шага, покрытие общей части 39 стандартов классов. | Да для Спринта 9 | `docs/rfc/2026-11-bcreq-flow-processes-prompts.md`, `standards/bcreq-runtime-references.md`, `standards/bcreq-flow-glossary.md` |
| `/standards/bcreq-prompt-profiles.md` | стандарт | Восемь профилей ручного промпта BCREQ «по тесту» (BL-152, issue #432): свои MUST-правила с цитатами из стандартов классов, отнесение 39 операций, шаги и профили, проверка триггера B. | Да для Спринта 9 | `standards/bcreq-prompt-base-standard.md`, `standards/bcreq-manual-classes/catalog.json`, `experiments/issue_425/archetypes.json` |
| `/docs/rfc/2026-11-runtime-product-catalog-golden-set.md` | RFC | RFC-RT-001 (issue #434): готовые к копированию задачи РТ-1 (каталог `taxonomy/mango-products.yaml`) и РТ-3 (golden set по классам) для runtime, ХАБ-1 для Хаба, механизм снятия заглушки З-1 (М-1…М-6), решение Р-17, задача BL-163; v0.2 — исток таксономии в классификации Хаба и индустриальный слой, задача BL-164; v0.3 (`accepted`, issue #442) — проверка готовности и исполнение BL-163, задача РТ-6; v0.4 (issue #444) — исполнение BL-156а, решение по PR #17, задачи BL-165, BL-166. v0.5 (issue #446) — исполнение BL-157б (RUN-0083), пробелы runtime, задача РТ-7; v0.6 (issue #448) — RUN-0084 и Ш-В v0.2 (BL-156б, BL-156в), разбор чатов BL-157в, РТ-7 создана (runtime #22). | Да для Спринта 9 | `standards/bcreq-runtime-references.md`, `docs/rfc/rfc-register.md`, `docs/taxonomy/products.json` |
| `/docs/rfc/2026-11-bcreq-prompts-publication-roadmap.md` | RFC | RFC-PUB-001 (issue #454): роадмэп публикации промптов всех шагов потока BCREQ, покрытие по 13 шагам, пробелы, план на 5–7 ноября, DEC-454-01…04. | Да для Спринта 9 | `pr-ops/BACKLOG.md`, `experiments/issue_454/audit_flow_coverage.py`, `scripts/validate_issue_454_publication_roadmap.py` |
| `/ai-rules/` | рабочие копии Хаба | Правила поведения агента-исполнителя: `agent-work-rules.md`, `agent-onboarding-protocol.md`, `adversarial-stress-testing.md`. Локально не редактируются. | Да | `ai-rules/agent-onboarding-protocol.md`, `ai-governance/ai-governance.md` |
| `/ai-governance/` | рабочие копии Хаба | Политики уровня организации, compliance и ИБ, включая `agent-security-checklist.md`. Локально не редактируются. | Да | `ai-governance/ai-governance.md`, `docs/adr/0004-hub-resync-2026-08.md` |
| `/tools/` | инструмент | Рабочие копии валидаторов Хаба: `validate-frontmatter.sh`, `validate-file-naming.sh`; локальные дельты описаны в `tools/README.md`. Запуск — `make validate`. | Да | `tools/README.md`, `pr-ops/BACKLOG.md` |
| `/scripts/sync_from_hub.py` | инструмент | Воспроизводимый ре-синк по манифесту с переписыванием ссылок; `--check` сверяет копии с Хабом. | Да | `.hub-profile.json`, `scripts/validate_issue_265_hub_sync.py` |
| `/.github/ISSUE_TEMPLATE/` | шаблон | GitHub issue templates для структурированного фидбека. | По необходимости | `CONTRIBUTING.md` |
| `/docs/rfc/2026-11-ttz-feasibility-flow.md` | RFC | RFC-TTZ-001 (issue #466), proposed: постановка/SSOT, практика 8 RUN, обезличенная форма 4 PDF и явные замечания БА; crosswalk, мета-модель, отчётность, F1+F2, план пробного потока и автоматизации. | Да для потока ТТЗ | `docs/rfc/rfc-register.md`, `pr-ops/BACKLOG.md`, `standards/bcreq-runtime-references.md`, `experiments/issue_466/README.md`, `site/index.html` |
| `/docs/rfc/2026-11-a-in-decomposition.md` | RFC | RFC-AIN-001 (#468), proposed v0.3: 24 шага, retrieval loop, provenance, вопросы/гипотезы, роли/бюджет/миграция; §2.3…2.6 — продолжение 1135, методология, P01…P20 и защита прежней практики. Т-11…13 выполнены, BL-179 review. | Да для проектирования A-IN | `docs/ba-processes/bcreq-a-in-route.json`, `docs/rfc/rfc-register.md`, `pr-ops/BACKLOG.md`, `experiments/issue_468/README.md`, `site/index.html` |
| `/docs/ba-processes/bcreq-a-in-route.json` | Модель процесса | SSOT списка и полей 24 проектных контрактов, v0.2: взаимодействие, handover и ссылки на P01…P20; не runtime, не тексты промптов. | Да для RFC-AIN-001 | `experiments/issue_468/route_table.py`, `experiments/issue_468/site_a_in.py`, `scripts/validate_issue_468_a_in.py`, `scripts/test_issue_468_dialogue.py` |
| `/experiments/issue_468/` | Evidence и проверки | Manifest и видимая дельта 28 → 66, ledger практики, baseline прежних контрактов, контрпримеры допуска/review; приватные исходники и извлечения исключены из git. | Да для review RFC-AIN-001 | `docs/rfc/2026-11-a-in-decomposition.md`, `docs/ba-processes/bcreq-a-in-route.json`, `scripts/test_issue_468_dialogue.py` |

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
## Реструктуризация каталогов (issue #265, 2026-08-18)

Каталог `governance/` расформирован; структура репозитория приведена к базовой
структуре Хаба (`ai-governance/`, `ai-rules/`, `pr-ops/`, `docs/adr/`,
`docs/rfc/`, `standards/`):

| Было | Стало |
| --- | --- |
| `governance/artifact-map.md`, `BACKLOG.md`, `session-digests.md`, `migration-*.md`, `sync-matrix-2026-06-17.md`, `prompt-feedback.json` | `pr-ops/` |
| `governance/agent-onboarding-protocol.md` (+ `.executable.md`), v1.2 | `.archive/ai-rules/agent-onboarding-protocol_old.md` (+ `.executable.md`), архив (issue #267) |
| `governance/rfc-*.md`, `governance/rfc/`, `governance/knowledge-transfer-to-hub/` | `docs/rfc/` |
| `governance/audit-*.md` | `docs/audit/` |
| `governance/prompt-debugging-process.md` | `standards/` |

- `research/` **не создаётся**: каталог специфичен для Хаба; research остаётся
  reference-only через [`docs/hub-research-dependencies.md`](../docs/hub-research-dependencies.md).
- Протокол v1.2 сохранён под суффиксом `_old` рядом с рабочей копией Хаба v1.5
  ([`ai-rules/agent-onboarding-protocol.md`](../ai-rules/agent-onboarding-protocol.md)).
  Актуализация выполнена в issue [#267](https://github.com/G-Ivan-A/mango_ba_prompts/issues/267):
  вся навигация ведёт на v1.5, `_old` переведён в `status: superseded`.
- Перенос воспроизводим:
  [`experiments/restructure_governance_dirs.py`](../experiments/restructure_governance_dirs.py)
  (22 пути, 63 файла с переписанными путями, 123 пересчитанные относительные
  ссылки). Permalink'и Хаба на `governance/` старых SHA сохранены как есть.
- Обоснование и сверка манифеста синка с итоговым T-00 —
  [ADR-0004](../docs/adr/0004-hub-resync-2026-08.md).

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
- [`pr-ops/session-digests.md`](session-digests.md) — новый sync-артефакт
  issue #72.
- [`pr-ops/migration-manifest.md`](migration-manifest.md) — исторический
  снимок миграции Mango и запись sync snapshots.
