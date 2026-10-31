---
status: draft
version: 0.1
updated: 2026-10-31
temperature: 0.1
analysis-subtype: inventory
source: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/409"
scope: repo
based_on: "https://github.com/G-Ivan-A/mango_ba_prompts/tree/6f6cbc477f4b482d3c10bd4d941cbfb481fccf1f"
---

# Реестр диспозиции файлов: актуален, обновить, история, архив

Файл сгенерирован скриптом [`experiments/issue_409/build_disposition.py`](../../experiments/issue_409/build_disposition.py) из дерева коммита [`6f6cbc47`](https://github.com/G-Ivan-A/mango_ba_prompts/tree/6f6cbc477f4b482d3c10bd4d941cbfb481fccf1f); вручную не правится. Машиночитаемая копия — [`experiments/issue_409/disposition.json`](../../experiments/issue_409/disposition.json). Выводы и обоснования — в [аудите репозитория](../audit/2026-10-31-repository-audit.md).

Реестр отвечает на требование issue #409 «файлы репозитория или актуальны, или вынесены в архив; исторические файлы размечены». Диспозиция — **предложение**: ни один файл этим PR не перемещён и не изменён. Исполнение — задачи T-01…T-09 после согласования RFC.

## Словарь диспозиций

| Диспозиция | Что означает | Файлов |
| --- | --- | ---: |
| `current` | Актуален: роль и содержание соответствуют текущим требованиям; оставить как есть. | 233 |
| `update` | Актуальная роль, устаревшее содержание: актуализировать отдельной задачей по RFC/ADR. | 113 |
| `relocate` | Содержание актуально, но дом или имя нарушают структуру Хаба: перенести отдельной задачей с редиректом ссылок. | 4 |
| `historical` | Историческое свидетельство: оставить на месте, не актуализировать; разметка — правилом каталога или блоком перехода. | 370 |
| `archive-candidate` | Не используется или заменён: active → deprecated/superseded → archived по стандарту депрекации Хаба. | 38 |
| `archived` | Уже в архиве: только metadata и обязательные ссылки. | 28 |
| `generated` | Производный файл: SSOT — генератор и его источники; руками не правится. | 23 |
| `statistics` | Статистика runs/: заморожена по ограничению issue #409; не изменяется и не актуализируется. | 806 |
| **Итого** | Все отслеживаемые файлы базового коммита | **1615** |

Метод доказательства использования: «входящие ссылки» — число нестатистических файлов (вне `runs/`), содержащих полный путь файла; «машинные» — то же только среди `scripts/`, `tools/`, `.github/` и `Makefile`. Это нижняя граница: относительные ссылки внутри каталога по одному имени файла не учитываются. Ноль ссылок не доказывает ненужность, но снижает риск архивирования; ненулевые машинные ссылки означают, что перенос требует правки потребителя.

## Сводка по областям

| Область | `current` | `update` | `relocate` | `historical` | `archive-candidate` | `archived` | `generated` | `statistics` | Всего |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `(корень)` | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 8 |
| `.archive` | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 3 |
| `.github` | 5 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 6 |
| `ai-governance` | 3 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 4 |
| `ai-rules` | 4 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 6 |
| `docs` | 46 | 27 | 4 | 78 | 13 | 0 | 0 | 0 | 168 |
| `experiments` | 0 | 0 | 0 | 285 | 17 | 0 | 0 | 0 | 302 |
| `kb` | 0 | 39 | 0 | 1 | 1 | 0 | 0 | 0 | 41 |
| `patterns` | 0 | 15 | 0 | 0 | 0 | 0 | 0 | 0 | 15 |
| `pr-ops` | 1 | 2 | 0 | 0 | 5 | 0 | 0 | 0 | 8 |
| `prompts` | 20 | 1 | 0 | 0 | 2 | 25 | 0 | 0 | 48 |
| `runs` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 806 | 806 |
| `scripts` | 71 | 15 | 0 | 0 | 0 | 0 | 0 | 0 | 86 |
| `site` | 8 | 0 | 0 | 6 | 0 | 0 | 23 | 0 | 37 |
| `standards` | 66 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 72 |
| `tools` | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 5 |

## Сводка по задачам

| Задача | Содержание | Файлов |
| --- | --- | ---: |
| T-01 | Bootstrap Хаба: AGENTS.md, archetype/environment в .hub-profile.json, docs/README.md | 1 |
| T-02 | Стратегические документы: docs/vision.md, concept.md, architecture.md, roadmap.md + ADR, заменяющий границы #263 | 5 |
| T-03 | Разделение docs/ba-ecosystem.md и перевод дорожной карты сайта на docs/roadmap.md | 3 |
| T-04 | Актуализация карты процессов, таксономии и паттернов под BCREQ A-IN/A-CORE | 22 |
| T-05 | Вывод локального KB-конвейера после переезда KB в mango-ba-ai-runtime (#361) | 58 |
| T-06 | Структура docs/: docs/contracts, файлы корня docs/, дубли, регистрация RFC | 11 |
| T-07 | Разметка истории: блоки перехода, политика датированных свидетельств, статусы ADR, архив логов | 41 |
| T-08 | SSOT и связи: синхронизация с Хабом, mango-ba-ai-runtime, видимость (ADR-009), ссылки на ветки форка | 12 |
| T-09 | Этап 2: единый источник пакета OpenCode (ADR-016 ↔ dist/execution-package-opencode Хаба) | 2 |

## Запрещённое поле ai-generated

Хаб запрещает `ai-generated` во frontmatter (AGENTS.md Хаба, раздел запретов; локальный `tools/validate-frontmatter.sh` отклоняет поле, но проверяет только корень, `ai-rules/` и `tools/`). Поле найдено в 741 файлах; из них 628 — в `runs/` (статистика, не исправляется). Вне `runs/` (задача T-07, удаление поля — правка metadata, допустимая и для исторических файлов):

- `docs/adr/0001-hub-sync-pr208.md`
- `docs/adr/0002-issue48-handover-local-enrichment.md`
- `docs/adr/0003-creative-mode-governance.md`
- `docs/adr/0004-hub-resync-2026-08.md`
- `docs/adr/001-prompt-standard.md`
- `docs/adr/002-pattern-standard.md`
- `docs/adr/003-ba-ontology.md`
- `docs/adr/004-operations-taxonomy.md`
- `docs/adr/005-artifact-team-naming.md`
- `docs/adr/006-prompt-naming.md`
- `docs/adr/007-kb-standard.md`
- `docs/adr/008-industry-standards-standard.md`
- `docs/adr/009-bcreq-formation-process.md`
- `docs/adr/010-pages-ux.md`
- `docs/adr/2026-08-adr-011-integration-task-artifacts.md`
- `docs/adr/2026-10-adr-012-bcreq-meta-standards.md`
- `docs/analysis/2026-09-03-hub-backlog-sprint-validation.md`
- `docs/analysis/experiment-1027-analysis.md`
- `docs/analysis/migration-strategy-rfc.md`
- `docs/audit/audit-contracts-2026-06-17.md`
- `docs/audit/audit-contracts-mango-2026-06-17.md`
- `docs/audit/audit-hub-2026-06-17.md`
- `docs/audit/audit-research-1027.md`
- `docs/audit/audit-run-scope-boundary-2026-08-21.md`
- `docs/audit/initial-state-2026-06.md`
- `docs/audit/issue-115-kb-pipeline.md`
- `docs/ba-ecosystem.md`
- `docs/ba-process/README.md`
- `docs/ba-processes/00-index.executable.md`
- `docs/ba-processes/00-index.md`
- `docs/ba-processes/README.md`
- `docs/ba-processes/bcreq-manual-process.md`
- `docs/contracts/bcreq-stage-gates.md`
- `docs/contracts/kb-citations.md`
- `docs/hub-research-dependencies.md`
- `docs/kb-experiment-report.md`
- `docs/report/2026-07-03-kb-state-after-lfs-cleanup.md`
- `docs/report/2026-09-01-kb-assessment-error-analysis.md`
- `docs/report/2026-09-01-run-0065-vs-0066-ab-rca.md`
- `docs/report/evidence/README.md`
- `docs/reviews/issue-391-bcreq-review.md`
- `docs/reviews/issue-393-bcreq-filters.md`
- `docs/reviews/migration-rfc-human-review-2026-06.md`
- `docs/rfc-hub-integration.md`
- `docs/rfc/2026-08-task-taxonomy.md`
- `docs/rfc/2026-10-bcreq-meta-standards-rfc.md`
- `docs/rfc/knowledge-transfer-to-hub/README.md`
- `docs/rfc/knowledge-transfer-to-hub/ba-ontology.md`
- `docs/rfc/knowledge-transfer-to-hub/bcreq-process.md`
- `docs/rfc/knowledge-transfer-to-hub/operations-taxonomy.md`
- `docs/rfc/knowledge-transfer-to-hub/pages-ux.md`
- `docs/rfc/prompt-improvement-bcreq-1025-proposal.md`
- `docs/rfc/prompt-improvement-multichannel-proposal.md`
- `docs/rfc/rfc-process.md`
- `docs/rfc/rfc-register.md`
- `docs/rfc/rfc-to-hub-001-knowledge-transfer.md`
- `docs/rfc/rfc-to-hub-002-prompt-debugging-process.md`
- `docs/site-access.md`
- `docs/task-for-konard-template.md`
- `docs/taxonomy.md`
- `experiments/issue_325/README.md`
- `experiments/run-0014-chat-export/README.md`
- `kb/README.md`
- `kb/STRUCTURE_REVIEW.md`
- `kb/USAGE.md`
- `kb/fragments/README.md`
- `kb/practices/source-backed-analysis.md`
- `kb/processed/README.md`
- `kb/sources/README.md`
- `kb/sources/contact-center-manual/source.md`
- `kb/sources/web-links/README.md`
- `patterns/README.md`
- `pr-ops/BACKLOG.md`
- `pr-ops/artifact-map.md`
- `pr-ops/migration-manifest.md`
- `pr-ops/migration-phase1-issues.md`
- `pr-ops/session-digests.md`
- `pr-ops/sync-matrix-2026-06-17.md`
- `prompts/README.executable.md`
- `prompts/README.md`
- `prompts/archive/tz-stats-generator-legacy.md`
- `prompts/archive/tz-stats-generator-simple-legacy.md`
- `prompts/archive/usecase-stepwise-generator-legacy.md`
- `prompts/archive/usecase-stepwise-generator-simple-legacy.md`
- `prompts/archive/user-story-generator-legacy.md`
- `prompts/archive/user-story-generator-simple-legacy.md`
- `standards/README.md`
- `standards/artifact-naming-standard.md`
- `standards/ba-ontology.executable.md`
- `standards/ba-ontology.md`
- `standards/bcreq-composition-standard.md`
- `standards/bcreq-process-standard.md`
- `standards/bcreq-prompt-architecture.md`
- `standards/bcreq-sections/01-glossary.md`
- `standards/bcreq-sections/02-business-context.md`
- `standards/bcreq-sections/03-functional-requirements.md`
- `standards/bcreq-sections/04-non-functional-requirements.md`
- `standards/bcreq-sections/05-solution-description.md`
- `standards/bcreq-sections/06-implementation-constraints.md`
- `standards/bcreq-sections/07-use-cases.md`
- `standards/bcreq-sections/08-supplementary.md`
- `standards/bcreq-sections/README.md`
- `standards/cascading-context-loading-standard.md`
- `standards/experiment-log-standard.md`
- `standards/industry-standards-standard.md`
- `standards/kb-standard.md`
- `standards/pages-ux-standard.md`
- `standards/pattern-standard.md`
- `standards/product-classification-contract.md`
- `standards/prompt-debugging-process.md`
- `standards/prompt-standard.md`
- `standards/runs-contract-standard.md`
- `standards/team-directory.md`

## Статистика runs/

Каталог `runs/` целиком имеет диспозицию `statistics`: он не актуализируется, не переносится и не размечается заново. Новая статистика по изменившимся требованиям накапливается новыми RUN; сравнение со старыми RUN — задача анализа, а не правки.

| Каталог RUN | Файлов |
| --- | ---: |
| `runs/2026/RUN-0001` | 5 |
| `runs/2026/RUN-0002` | 5 |
| `runs/2026/RUN-0003` | 5 |
| `runs/2026/RUN-0004` | 5 |
| `runs/2026/RUN-0005` | 5 |
| `runs/2026/RUN-0006` | 5 |
| `runs/2026/RUN-0007` | 5 |
| `runs/2026/RUN-0008` | 5 |
| `runs/2026/RUN-0009` | 5 |
| `runs/2026/RUN-0010` | 6 |
| `runs/2026/RUN-0011` | 13 |
| `runs/2026/RUN-0012` | 13 |
| `runs/2026/RUN-0013` | 16 |
| `runs/2026/RUN-0014` | 14 |
| `runs/2026/RUN-0015` | 12 |
| `runs/2026/RUN-0016` | 31 |
| `runs/2026/RUN-0017` | 22 |
| `runs/2026/RUN-0018` | 19 |
| `runs/2026/RUN-0019` | 11 |
| `runs/2026/RUN-0020` | 25 |
| `runs/2026/RUN-0021` | 24 |
| `runs/2026/RUN-0022` | 25 |
| `runs/2026/RUN-0023` | 14 |
| `runs/2026/RUN-0024` | 16 |
| `runs/2026/RUN-0025` | 18 |
| `runs/2026/RUN-0026` | 22 |
| `runs/2026/RUN-0027` | 17 |
| `runs/2026/RUN-0028` | 15 |
| `runs/2026/RUN-0029` | 19 |
| `runs/2026/RUN-0030` | 7 |
| `runs/2026/RUN-0031` | 7 |
| `runs/2026/RUN-0032` | 7 |
| `runs/2026/RUN-0033` | 7 |
| `runs/2026/RUN-0034` | 7 |
| `runs/2026/RUN-0035` | 7 |
| `runs/2026/RUN-0036` | 7 |
| `runs/2026/RUN-0037` | 7 |
| `runs/2026/RUN-0038` | 7 |
| `runs/2026/RUN-0039` | 7 |
| `runs/2026/RUN-0040` | 7 |
| `runs/2026/RUN-0041` | 7 |
| `runs/2026/RUN-0042` | 7 |
| `runs/2026/RUN-0043` | 7 |
| `runs/2026/RUN-0044` | 7 |
| `runs/2026/RUN-0045` | 7 |
| `runs/2026/RUN-0046` | 7 |
| `runs/2026/RUN-0047` | 7 |
| `runs/2026/RUN-0048` | 7 |
| `runs/2026/RUN-0049` | 7 |
| `runs/2026/RUN-0050` | 7 |
| `runs/2026/RUN-0051` | 7 |
| `runs/2026/RUN-0052` | 7 |
| `runs/2026/RUN-0053` | 7 |
| `runs/2026/RUN-0054` | 7 |
| `runs/2026/RUN-0055` | 9 |
| `runs/2026/RUN-0056` | 11 |
| `runs/2026/RUN-0057` | 13 |
| `runs/2026/RUN-0058` | 11 |
| `runs/2026/RUN-0059` | 8 |
| `runs/2026/RUN-0060` | 10 |
| `runs/2026/RUN-0061` | 10 |
| `runs/2026/RUN-0062` | 6 |
| `runs/2026/RUN-0063` | 6 |
| `runs/2026/RUN-0064` | 7 |
| `runs/2026/RUN-0065` | 6 |
| `runs/2026/RUN-0066` | 7 |
| `runs/2026/RUN-0067` | 6 |
| `runs/2026/RUN-0068` | 7 |
| `runs/2026/RUN-0069` | 7 |
| `runs/2026/RUN-0070` | 7 |
| `runs/2026/RUN-0071` | 7 |
| `runs/2026/RUN-0072` | 7 |
| `runs/2026/RUN-0073` | 18 |
| `runs/2026/RUN-0074` | 18 |
| `runs/2026/RUN-0075` | 17 |
| `runs/2026/RUN-0076` | 16 |
| `runs/2026/RUN-0077` | 7 |
| `runs/2026/RUN-0078` | 12 |
| `runs/README.md` | 1 |

## Пофайловый реестр (вне runs/)

| Путь | status | updated | Диспозиция | Основание | Задача | Ссылки (всего / машинные) |
| --- | --- | --- | --- | --- | --- | --- |
| `.archive/README.md` | canonical | 2026-08-21 | `archived` | Каталог .archive/ — канонический архив (issue #291) | — | 9 / 2 |
| `.archive/ai-rules/agent-onboarding-protocol_old.executable.md` | superseded | 2026-08-21 | `archived` | Каталог .archive/ — канонический архив (issue #291) | — | 9 / 3 |
| `.archive/ai-rules/agent-onboarding-protocol_old.md` | superseded | 2026-08-21 | `archived` | Каталог .archive/ — канонический архив (issue #291) | — | 21 / 4 |
| `.gitattributes` | — | — | `current` | Служебный файл корня | — | 7 / 1 |
| `.github/ISSUE_TEMPLATE/prompt-feedback.yml` | — | — | `current` | CI и шаблоны issue | — | 3 / 0 |
| `.github/ISSUE_TEMPLATE/run-execution.yml` | — | — | `current` | CI и шаблоны issue | — | 3 / 0 |
| `.github/ISSUE_TEMPLATE/run-statistics.yml` | — | — | `current` | CI и шаблоны issue | — | 2 / 0 |
| `.github/workflows/github-pages.yml` | — | — | `current` | CI и шаблоны issue | — | 14 / 5 |
| `.github/workflows/kb.yml` | — | — | `update` | CI KB-конвейера целится в kb/processed после переезда | T-05 | 11 / 3 |
| `.github/workflows/validate.yml` | — | — | `current` | CI и шаблоны issue | — | 11 / 3 |
| `.gitignore` | — | — | `current` | Служебный файл корня | — | 18 / 6 |
| `.hub-profile.json` | — | — | `update` | Нет archetype/environment (bootstrap v2.0); last_sync 3bfa4103 от 2026-08-17 | T-01 | 22 / 5 |
| `CHANGELOG.md` | draft | 2026-10-30 | `current` | Служебный файл корня | — | 58 / 32 |
| `CONTRIBUTING.md` | draft | 2026-10-20 | `update` | 4 ссылки на kb/processed после переезда | T-05 | 47 / 6 |
| `LICENSE` | — | — | `current` | Служебный файл корня | — | 5 / 1 |
| `Makefile` | — | — | `update` | Цели kb-* пишут в kb/processed (MANGO_OUT, LK_OUT), который перенесён | T-05 | 25 / 7 |
| `README.md` | canonical | 2026-08-21 | `update` | Видение #263 «только уровни 1–2, без сервера и агентов», «evals и golden-set отсутствуют», ссылка на ветку форка, ai-ba-playbooks как публичная витрина | T-02 | 260 / 49 |
| `ai-governance/README.md` | canonical | 2026-07-16 | `current` | Правила работы AI (canonical) | — | 7 / 1 |
| `ai-governance/agent-security-checklist.md` | accepted | 2026-07-10 | `current` | Правила работы AI (accepted) | — | 5 / 1 |
| `ai-governance/ai-governance.md` | draft | 2026-08-21 | `update` | Закреплено «GitHub — единственная платформа» и приватизация по ADR-009; противоречит этапам 3–4 | T-02 | 40 / 6 |
| `ai-governance/hub-ai-governance.md` | canonical | 2026-08-11 | `current` | Правила работы AI (canonical) | — | 8 / 1 |
| `ai-rules/AI_SESSION_HANDOVER_PROMPT.md` | draft | 2026-08-21 | `update` | Шаблон передачи сессии ссылается на ворота видения #263; синхронизировать после T-02 | T-02 | 23 / 5 |
| `ai-rules/README.md` | canonical | 2026-07-16 | `current` | Правила работы AI (canonical) | — | 9 / 1 |
| `ai-rules/adversarial-stress-testing.md` | accepted | 2026-08-07 | `current` | Правила работы AI (accepted) | — | 5 / 1 |
| `ai-rules/agent-onboarding-protocol.md` | canonical | 2026-08-11 | `current` | Правила работы AI (canonical) | — | 24 / 3 |
| `ai-rules/agent-work-rules.md` | canonical | 2026-08-11 | `current` | Правила работы AI (canonical) | — | 8 / 1 |
| `ai-rules/ai-quick-rules.md` | draft | 2026-08-21 | `update` | Краткие правила наследуют формулировки видения #263; синхронизировать после T-02 | T-02 | 22 / 3 |
| `docs/.gitkeep` | — | — | `archive-candidate` | Каталог docs/ не пуст; маркер не нужен | T-06 | 2 / 0 |
| `docs/adr/.gitkeep` | — | — | `archive-candidate` | Каталог docs/adr/ не пуст; маркер не нужен | T-06 | 2 / 0 |
| `docs/adr/0001-hub-sync-pr208.md` | accepted | 2026-06-10 | `current` | Решение в статусе accepted; действует | — | 7 / 1 |
| `docs/adr/0002-issue48-handover-local-enrichment.md` | accepted | 2026-06-10 | `current` | Решение в статусе accepted; действует | — | 9 / 3 |
| `docs/adr/0003-creative-mode-governance.md` | accepted | 2026-06-11 | `current` | Решение в статусе accepted; действует | — | 12 / 3 |
| `docs/adr/0004-hub-resync-2026-08.md` | accepted | 2026-08-18 | `current` | Решение в статусе accepted; действует | — | 10 / 1 |
| `docs/adr/001-prompt-standard.md` | accepted | 2026-06-11 | `current` | Решение в статусе accepted; действует | — | 14 / 2 |
| `docs/adr/002-pattern-standard.md` | accepted | 2026-06-11 | `current` | Решение в статусе accepted; действует | — | 17 / 2 |
| `docs/adr/003-ba-ontology.md` | proposed | 2026-06-16 | `update` | ADR в статусе proposed с 2026-06: нужно решение accept / reject / supersede | T-07 | 13 / 2 |
| `docs/adr/004-operations-taxonomy.md` | proposed | 2026-06-16 | `update` | ADR в статусе proposed с 2026-06: нужно решение accept / reject / supersede | T-07 | 7 / 2 |
| `docs/adr/005-artifact-team-naming.md` | proposed | 2026-06-16 | `update` | ADR в статусе proposed с 2026-06: нужно решение accept / reject / supersede | T-07 | 11 / 2 |
| `docs/adr/006-prompt-naming.md` | proposed | 2026-06-16 | `update` | ADR в статусе proposed с 2026-06: нужно решение accept / reject / supersede | T-07 | 9 / 2 |
| `docs/adr/007-kb-standard.md` | proposed | 2026-06-16 | `update` | ADR в статусе proposed с 2026-06: нужно решение accept / reject / supersede | T-07 | 15 / 3 |
| `docs/adr/008-industry-standards-standard.md` | proposed | 2026-06-16 | `update` | ADR в статусе proposed с 2026-06: нужно решение accept / reject / supersede | T-07 | 6 / 2 |
| `docs/adr/009-bcreq-formation-process.md` | proposed | 2026-06-16 | `archive-candidate` | proposed 2026-06; процесс BCREQ заменён ADR-012/015 и стадиями A-IN…A-RELEASE; номер конфликтует с ADR-009 Хаба | T-07 | 12 / 2 |
| `docs/adr/010-pages-ux.md` | proposed | 2026-06-16 | `update` | ADR в статусе proposed с 2026-06: нужно решение accept / reject / supersede | T-07 | 7 / 2 |
| `docs/adr/2026-08-adr-011-integration-task-artifacts.md` | proposed | 2026-08-28 | `current` | Решение в статусе proposed; действует | — | 5 / 1 |
| `docs/adr/2026-10-adr-012-bcreq-meta-standards.md` | proposed | 2026-10-23 | `current` | Решение в статусе proposed; действует | — | 18 / 0 |
| `docs/adr/2026-10-adr-013-product-portal-mapping.md` | proposed | 2026-10-28 | `update` | Ссылки на временную ветку форка konard/G-Ivan-A-mango_ba_prompts; цели существуют в main (F-19) | T-08 | 1 / 0 |
| `docs/adr/2026-10-adr-014-documentation-source-validation.md` | proposed | 2026-10-29 | `update` | Ссылки на временную ветку форка konard/G-Ivan-A-mango_ba_prompts; цели существуют в main (F-19) | T-08 | 2 / 0 |
| `docs/adr/2026-10-adr-015-bcreq-manual-classes.md` | draft | 2026-10-29 | `current` | Решение в статусе draft; действует | — | 1 / 0 |
| `docs/adr/2026-10-adr-016-ide-client-process.md` | draft | 2026-10-30 | `update` | Не связан с dist/execution-package-opencode Хаба (#652) и средами 1–4 | T-09 | 4 / 1 |
| `docs/analysis/2026-08-21-runs-type-gap-analysis.md` | draft | 2026-08-21 | `historical` | Анализ — снимок на дату; выводы перенесены в стандарты/ADR или устарели | — | 6 / 1 |
| `docs/analysis/2026-08-22-validator-optimization.md` | draft | 2026-08-22 | `historical` | Анализ — снимок на дату; выводы перенесены в стандарты/ADR или устарели | — | 5 / 1 |
| `docs/analysis/2026-08-26-architecture-spike-format-research.md` | draft | 2026-08-26 | `historical` | Анализ — снимок на дату; выводы перенесены в стандарты/ADR или устарели | — | 3 / 0 |
| `docs/analysis/2026-08-28-human-review-accessibility.md` | draft | 2026-08-28 | `historical` | Анализ — снимок на дату; выводы перенесены в стандарты/ADR или устарели | — | 7 / 1 |
| `docs/analysis/2026-09-03-hub-backlog-sprint-validation.md` | draft | 2026-09-03 | `historical` | Анализ — снимок на дату; выводы перенесены в стандарты/ADR или устарели | — | 4 / 1 |
| `docs/analysis/2026-10-20-bcreq-fr-section-prompts.md` | draft | 2026-10-20 | `historical` | Анализ — снимок на дату; выводы перенесены в стандарты/ADR или устарели | — | 11 / 1 |
| `docs/analysis/2026-10-20-parallel-pr-merge-conflicts.md` | draft | 2026-10-20 | `historical` | Анализ — снимок на дату; выводы перенесены в стандарты/ADR или устарели | — | 3 / 0 |
| `docs/analysis/2026-10-23-bcreq-standards-third-opinion.md` | draft | 2026-10-23 | `historical` | Анализ — снимок на дату; выводы перенесены в стандарты/ADR или устарели | — | 7 / 0 |
| `docs/analysis/2026-10-23-prompts-catalog-audit.md` | draft | 2026-10-23 | `historical` | Анализ — снимок на дату; выводы перенесены в стандарты/ADR или устарели | — | 10 / 1 |
| `docs/analysis/2026-10-28-bcreq-evolution-failure-analysis.md` | draft | 2026-10-28 | `historical` | Анализ — снимок на дату; выводы перенесены в стандарты/ADR или устарели | — | 11 / 1 |
| `docs/analysis/2026-10-29-bcreq-checkpoint.md` | draft | 2026-10-29 | `historical` | Анализ — снимок на дату; выводы перенесены в стандарты/ADR или устарели | — | 46 / 1 |
| `docs/analysis/2026-10-30-ecosystem-compliance.md` | draft | 2026-10-30 | `current` | Аналитика, на которую опирается открытое RFC модернизации / ADR-016 | — | 2 / 0 |
| `docs/analysis/2026-10-30-ide-clients-stage-2.md` | draft | 2026-10-30 | `update` | Рекомендация OpenCode V1 без сверки с пакетом Хаба; дополнить по T-09 | T-09 | 8 / 1 |
| `docs/analysis/2026-10-30-october-requirements-evolution.md` | draft | 2026-10-30 | `current` | Аналитика, на которую опирается открытое RFC модернизации / ADR-016 | — | 3 / 0 |
| `docs/analysis/2026-10-30-repository-current-state.md` | draft | 2026-10-30 | `current` | Аналитика, на которую опирается открытое RFC модернизации / ADR-016 | — | 2 / 0 |
| `docs/analysis/2026-10-30-repository-inventory.md` | draft | 2026-10-30 | `current` | Аналитика, на которую опирается открытое RFC модернизации / ADR-016 | — | 3 / 0 |
| `docs/analysis/experiment-1027-analysis.md` | draft | 2026-06-16 | `historical` | Анализ — снимок на дату; выводы перенесены в стандарты/ADR или устарели | — | 10 / 1 |
| `docs/analysis/ide-clients-stage-2/2026-10-30-comparison.md` | draft | 2026-10-30 | `current` | Аналитика, на которую опирается открытое RFC модернизации / ADR-016 | — | 2 / 0 |
| `docs/analysis/ide-clients-stage-2/2026-10-30-goose-guide.md` | draft | 2026-10-30 | `current` | Аналитика, на которую опирается открытое RFC модернизации / ADR-016 | — | 2 / 0 |
| `docs/analysis/ide-clients-stage-2/2026-10-30-mapping.md` | draft | 2026-10-30 | `current` | Аналитика, на которую опирается открытое RFC модернизации / ADR-016 | — | 2 / 0 |
| `docs/analysis/ide-clients-stage-2/2026-10-30-meta-model.md` | draft | 2026-10-30 | `current` | Аналитика, на которую опирается открытое RFC модернизации / ADR-016 | — | 2 / 0 |
| `docs/analysis/ide-clients-stage-2/2026-10-30-operations.md` | draft | 2026-10-30 | `current` | Аналитика, на которую опирается открытое RFC модернизации / ADR-016 | — | 2 / 0 |
| `docs/analysis/ide-clients-stage-2/2026-10-30-sources.md` | draft | 2026-10-30 | `current` | Аналитика, на которую опирается открытое RFC модернизации / ADR-016 | — | 2 / 0 |
| `docs/analysis/migration-strategy-rfc.md` | draft | 2026-06-03 | `historical` | Анализ — снимок на дату; выводы перенесены в стандарты/ADR или устарели | — | 11 / 2 |
| `docs/audit/.gitkeep` | — | — | `historical` | Датированное свидетельство (HTOM: audit/reviews — evidence) | — | 2 / 0 |
| `docs/audit/2026-08-21-root-structure-audit.md` | canonical | 2026-08-22 | `historical` | Датированное свидетельство (HTOM: audit/reviews — evidence) | — | 10 / 3 |
| `docs/audit/audit-contracts-2026-06-17.md` | draft | 2026-06-16 | `historical` | Датированное свидетельство (HTOM: audit/reviews — evidence) | — | 7 / 0 |
| `docs/audit/audit-contracts-mango-2026-06-17.md` | draft | 2026-06-16 | `historical` | Датированное свидетельство (HTOM: audit/reviews — evidence) | — | 6 / 0 |
| `docs/audit/audit-hub-2026-06-17.md` | draft | 2026-06-16 | `historical` | Датированное свидетельство (HTOM: audit/reviews — evidence) | — | 9 / 0 |
| `docs/audit/audit-research-1027.md` | draft | 2026-06-16 | `historical` | Датированное свидетельство (HTOM: audit/reviews — evidence) | — | 4 / 0 |
| `docs/audit/audit-run-scope-boundary-2026-08-21.md` | draft | 2026-08-21 | `historical` | Датированное свидетельство (HTOM: audit/reviews — evidence) | — | 2 / 0 |
| `docs/audit/initial-state-2026-06.md` | draft | 2026-06-02 | `historical` | Датированное свидетельство (HTOM: audit/reviews — evidence) | — | 6 / 0 |
| `docs/audit/issue-115-kb-pipeline.md` | draft | 2026-06-19 | `historical` | Датированное свидетельство (HTOM: audit/reviews — evidence) | — | 2 / 0 |
| `docs/ba-ecosystem.md` | draft | 2026-08-17 | `update` | Сборный документ: методология + дорожная карта L1–L4 + границы «уровни 3–4 не план»; ai-generated во frontmatter; источник roadmap.json сайта | T-03 | 30 / 5 |
| `docs/ba-process/README.md` | draft | 2026-06-18 | `archive-candidate` | Дубль docs/ba-processes/ (2026-06-18) | T-06 | 4 / 1 |
| `docs/ba-processes/00-index.executable.md` | draft | 2026-06-20 | `update` | Исполняемый спутник 00-index.md; синхронно с T-04 | T-04 | 7 / 1 |
| `docs/ba-processes/00-index.md` | draft | 2026-06-15 | `update` | Процессы «Формирование/Валидация ФТ/ТЗ» заменены стадиями A-IN/A-CORE; источник дерева процессов сайта | T-04 | 46 / 5 |
| `docs/ba-processes/README.md` | draft | 2026-06-20 | `update` | Навигация по процессам 2026-06; синхронно с T-04 | T-04 | 3 / 1 |
| `docs/ba-processes/bcreq-manual-process.md` | draft | 2026-10-24 | `current` | Процесс BCREQ (источник вкладки «Процессы» сайта) | — | 10 / 2 |
| `docs/contracts/bcreq-manual-state.md` | draft | 2026-10-29 | `relocate` | Хаб запрещает docs/contracts/; дом — standards/ или docs/ba-processes/ | T-06 | 46 / 0 |
| `docs/contracts/bcreq-stage-gates.md` | draft | 2026-10-23 | `relocate` | Хаб запрещает docs/contracts/; дом — standards/ или docs/ba-processes/; на файл ссылается сайт | T-06 | 30 / 1 |
| `docs/contracts/kb-citations.md` | active | 2026-09-01 | `update` | Контракт цитирования KB ссылается на kb/processed; дом docs/contracts запрещён | T-05 | 6 / 1 |
| `docs/hub-research-dependencies.md` | draft | 2026-10-30 | `update` | Мост к Хабу актуален, но не называет mango-ba-ai-runtime и projects/ba-ai-process | T-08 | 37 / 5 |
| `docs/kb-experiment-report.md` | draft | 2026-06-18 | `relocate` | Отчёт в корне docs/; дом — docs/report/ (историческое свидетельство) | T-06 | 13 / 5 |
| `docs/report/2026-07-03-kb-state-after-lfs-cleanup.md` | review | 2026-07-03 | `historical` | Датированное свидетельство (HTOM: audit/reviews — evidence) | — | 2 / 0 |
| `docs/report/2026-09-01-kb-assessment-error-analysis.md` | draft | 2026-09-01 | `historical` | Датированное свидетельство (HTOM: audit/reviews — evidence) | — | 3 / 1 |
| `docs/report/2026-09-01-run-0065-vs-0066-ab-rca.md` | complete | 2026-09-01 | `historical` | Датированное свидетельство (HTOM: audit/reviews — evidence) | — | 3 / 1 |
| `docs/report/data/2026-09-01-run-0065-acb6c7bc.fixture` | — | — | `historical` | Датированное свидетельство (HTOM: audit/reviews — evidence) | — | 3 / 1 |
| `docs/report/data/2026-09-01-run-0065-vs-0066-sample.json` | — | — | `historical` | Датированное свидетельство (HTOM: audit/reviews — evidence) | — | 2 / 1 |
| `docs/report/evidence/2026-09-01-run-0065-acb6c7bc-redacted.txt` | — | — | `historical` | Датированное свидетельство (HTOM: audit/reviews — evidence) | — | 5 / 1 |
| `docs/report/evidence/README.md` | complete | 2026-09-01 | `historical` | Датированное свидетельство (HTOM: audit/reviews — evidence) | — | 2 / 1 |
| `docs/reviews/issue-391-bcreq-review.md` | draft | 2026-10-24 | `historical` | Датированное свидетельство (HTOM: audit/reviews — evidence) | — | 6 / 0 |
| `docs/reviews/issue-391-golden-inventory.md` | — | — | `historical` | Датированное свидетельство (HTOM: audit/reviews — evidence) | — | 7 / 0 |
| `docs/reviews/issue-393-bcreq-filters.md` | draft | 2026-10-26 | `historical` | Датированное свидетельство (HTOM: audit/reviews — evidence) | — | 2 / 0 |
| `docs/reviews/migration-rfc-human-review-2026-06.md` | draft | 2026-06-03 | `historical` | Датированное свидетельство (HTOM: audit/reviews — evidence) | — | 7 / 1 |
| `docs/rfc-hub-integration.md` | draft | 2026-08-17 | `update` | RFC в корне docs/ (нарушение HTOM) и описание ai-ba-playbooks как публичной методологии | T-06 | 17 / 2 |
| `docs/rfc/2026-08-task-taxonomy.md` | proposed | 2026-08-28 | `current` | RFC в статусе proposed; ожидает решения владельца | — | 5 / 1 |
| `docs/rfc/2026-10-bcreq-manual-pipeline.md` | draft | 2026-10-29 | `current` | RFC в статусе draft; ожидает решения владельца | — | 47 / 0 |
| `docs/rfc/2026-10-bcreq-meta-standards-rfc.md` | proposed | 2026-10-23 | `current` | RFC в статусе proposed; ожидает решения владельца | — | 11 / 0 |
| `docs/rfc/2026-10-repository-modernization.md` | draft | 2026-10-30 | `current` | RFC в статусе draft; ожидает решения владельца | — | 3 / 0 |
| `docs/rfc/knowledge-transfer-to-hub/README.md` | draft | 2026-06-16 | `archive-candidate` | Передача знаний в Хаб 2026-06 выполнена через research/ba-requirements Хаба | T-07 | 3 / 0 |
| `docs/rfc/knowledge-transfer-to-hub/ba-ontology.md` | draft | 2026-06-16 | `archive-candidate` | Передача знаний в Хаб 2026-06 выполнена через research/ba-requirements Хаба | T-07 | 2 / 1 |
| `docs/rfc/knowledge-transfer-to-hub/bcreq-process.md` | draft | 2026-06-16 | `archive-candidate` | Передача знаний в Хаб 2026-06 выполнена через research/ba-requirements Хаба | T-07 | 2 / 1 |
| `docs/rfc/knowledge-transfer-to-hub/operations-taxonomy.md` | draft | 2026-06-16 | `archive-candidate` | Передача знаний в Хаб 2026-06 выполнена через research/ba-requirements Хаба | T-07 | 2 / 1 |
| `docs/rfc/knowledge-transfer-to-hub/pages-ux.md` | draft | 2026-06-16 | `archive-candidate` | Передача знаний в Хаб 2026-06 выполнена через research/ba-requirements Хаба | T-07 | 2 / 1 |
| `docs/rfc/prompt-improvement-bcreq-1025-proposal.md` | proposed | 2026-06-18 | `current` | RFC в статусе proposed; ожидает решения владельца | — | 5 / 1 |
| `docs/rfc/prompt-improvement-multichannel-proposal.md` | proposed | 2026-06-18 | `current` | RFC в статусе proposed; ожидает решения владельца | — | 6 / 1 |
| `docs/rfc/rfc-process.md` | draft | 2026-06-16 | `current` | RFC в статусе draft; ожидает решения владельца | — | 9 / 1 |
| `docs/rfc/rfc-register.md` | draft | 2026-10-23 | `update` | Реестр не содержит RFC 2026-10 (manual pipeline, modernization); ai-generated во frontmatter | T-06 | 13 / 1 |
| `docs/rfc/rfc-to-hub-001-knowledge-transfer.md` | draft | 2026-06-16 | `archive-candidate` | RFC в Хаб 2026-06; результат поглощён метамоделью Хаба | T-07 | 10 / 1 |
| `docs/rfc/rfc-to-hub-002-prompt-debugging-process.md` | draft | 2026-06-16 | `current` | RFC в статусе draft; ожидает решения владельца | — | 5 / 1 |
| `docs/screenshots/issue-335-password-gate.png` | — | — | `historical` | Скриншоты приёмки PR; свидетельство | — | 1 / 0 |
| `docs/screenshots/issue-335-report-diagram.png` | — | — | `historical` | Скриншоты приёмки PR; свидетельство | — | 1 / 0 |
| `docs/screenshots/issue-335-report-unlocked.png` | — | — | `historical` | Скриншоты приёмки PR; свидетельство | — | 1 / 0 |
| `docs/screenshots/issue-335-reports-index.png` | — | — | `historical` | Скриншоты приёмки PR; свидетельство | — | 1 / 0 |
| `docs/screenshots/issue-388-01-locked.png` | — | — | `historical` | Скриншоты приёмки PR; свидетельство | — | 1 / 0 |
| `docs/screenshots/issue-388-02-wrong-password.png` | — | — | `historical` | Скриншоты приёмки PR; свидетельство | — | 1 / 0 |
| `docs/screenshots/issue-388-03-catalog.png` | — | — | `historical` | Скриншоты приёмки PR; свидетельство | — | 1 / 0 |
| `docs/screenshots/issue-388-04-bcreq-filter.png` | — | — | `historical` | Скриншоты приёмки PR; свидетельство | — | 1 / 0 |
| `docs/screenshots/issue-388-05-bcreq-manual-process.png` | — | — | `historical` | Скриншоты приёмки PR; свидетельство | — | 1 / 0 |
| `docs/screenshots/issue-388-06-bcreq-approval.png` | — | — | `historical` | Скриншоты приёмки PR; свидетельство | — | 1 / 0 |
| `docs/screenshots/issue-388-07-report-locked.png` | — | — | `historical` | Скриншоты приёмки PR; свидетельство | — | 1 / 0 |
| `docs/screenshots/issue-391/after-catalog.png` | — | — | `historical` | Скриншоты приёмки PR; свидетельство | — | 1 / 0 |
| `docs/screenshots/issue-391/after-login-error.png` | — | — | `historical` | Скриншоты приёмки PR; свидетельство | — | 1 / 0 |
| `docs/screenshots/issue-391/after-login.png` | — | — | `historical` | Скриншоты приёмки PR; свидетельство | — | 1 / 0 |
| `docs/screenshots/issue-391/after-mobile.png` | — | — | `historical` | Скриншоты приёмки PR; свидетельство | — | 1 / 0 |
| `docs/screenshots/issue-391/after-processes-mcp.png` | — | — | `historical` | Скриншоты приёмки PR; свидетельство | — | 1 / 0 |
| `docs/screenshots/issue-391/after-processes.png` | — | — | `historical` | Скриншоты приёмки PR; свидетельство | — | 1 / 0 |
| `docs/screenshots/issue-391/before-catalog.png` | — | — | `historical` | Скриншоты приёмки PR; свидетельство | — | 2 / 0 |
| `docs/screenshots/issue-391/before-login.png` | — | — | `historical` | Скриншоты приёмки PR; свидетельство | — | 2 / 0 |
| `docs/screenshots/issue-391/before-mobile.png` | — | — | `historical` | Скриншоты приёмки PR; свидетельство | — | 1 / 0 |
| `docs/screenshots/issue-391/before-processes.png` | — | — | `historical` | Скриншоты приёмки PR; свидетельство | — | 2 / 0 |
| `docs/screenshots/issue-391/live-before-deployment.png` | — | — | `historical` | Скриншоты приёмки PR; свидетельство | — | 1 / 0 |
| `docs/screenshots/issue-393/after-catalog.png` | — | — | `historical` | Скриншоты приёмки PR; свидетельство | — | 2 / 0 |
| `docs/screenshots/issue-393/after-local-mcp.png` | — | — | `historical` | Скриншоты приёмки PR; свидетельство | — | 2 / 0 |
| `docs/screenshots/issue-393/after-mobile.png` | — | — | `historical` | Скриншоты приёмки PR; свидетельство | — | 2 / 0 |
| `docs/screenshots/issue-393/after-operation-cascade.png` | — | — | `historical` | Скриншоты приёмки PR; свидетельство | — | 2 / 0 |
| `docs/screenshots/issue-393/after-process-cascade.png` | — | — | `historical` | Скриншоты приёмки PR; свидетельство | — | 2 / 0 |
| `docs/screenshots/issue-393/after-processes.png` | — | — | `historical` | Скриншоты приёмки PR; свидетельство | — | 2 / 0 |
| `docs/screenshots/issue-393/before-catalog.png` | — | — | `historical` | Скриншоты приёмки PR; свидетельство | — | 2 / 0 |
| `docs/screenshots/issue-74-pages-desktop.png` | — | — | `historical` | Скриншоты приёмки PR; свидетельство | — | 1 / 0 |
| `docs/screenshots/issue-74-pages-mobile.png` | — | — | `historical` | Скриншоты приёмки PR; свидетельство | — | 1 / 0 |
| `docs/screenshots/issue-86-mango-widget-local.png` | — | — | `historical` | Скриншоты приёмки PR; свидетельство | — | 1 / 0 |
| `docs/screenshots/issue-91-cascade.png` | — | — | `historical` | Скриншоты приёмки PR; свидетельство | — | 1 / 0 |
| `docs/screenshots/issue-91-checks.png` | — | — | `historical` | Скриншоты приёмки PR; свидетельство | — | 1 / 0 |
| `docs/screenshots/issue-91-full.png` | — | — | `historical` | Скриншоты приёмки PR; свидетельство | — | 1 / 0 |
| `docs/screenshots/issue-91-mobile-filters.png` | — | — | `historical` | Скриншоты приёмки PR; свидетельство | — | 1 / 0 |
| `docs/screenshots/issue-92-prompt-cards.png` | — | — | `historical` | Скриншоты приёмки PR; свидетельство | — | 1 / 0 |
| `docs/screenshots/issue-97-process-tree-collapsed.png` | — | — | `historical` | Скриншоты приёмки PR; свидетельство | — | 1 / 0 |
| `docs/screenshots/issue-97-process-tree-expanded.png` | — | — | `historical` | Скриншоты приёмки PR; свидетельство | — | 1 / 0 |
| `docs/screenshots/issue-97-spa-processes-page.png` | — | — | `historical` | Скриншоты приёмки PR; свидетельство | — | 1 / 0 |
| `docs/screenshots/issue-99-catalog-dark.png` | — | — | `historical` | Скриншоты приёмки PR; свидетельство | — | 1 / 0 |
| `docs/screenshots/issue-99-catalog.png` | — | — | `historical` | Скриншоты приёмки PR; свидетельство | — | 1 / 0 |
| `docs/screenshots/issue-99-dashboard.png` | — | — | `historical` | Скриншоты приёмки PR; свидетельство | — | 1 / 0 |
| `docs/screenshots/issue-99-patterns.png` | — | — | `historical` | Скриншоты приёмки PR; свидетельство | — | 1 / 0 |
| `docs/screenshots/issue-99-process-modal.png` | — | — | `historical` | Скриншоты приёмки PR; свидетельство | — | 1 / 0 |
| `docs/site-access.md` | draft | 2026-10-24 | `relocate` | Инструкция доступа к сайту в корне docs/; дом определяет docs/README.md | T-06 | 7 / 2 |
| `docs/superpowers/plans/2026-08-31-issue-339-followup.md` | — | — | `archive-candidate` | План инструмента без frontmatter, задача закрыта | T-07 | 2 / 0 |
| `docs/superpowers/plans/2026-08-31-issue-343-run-0063.md` | — | — | `archive-candidate` | План инструмента без frontmatter, задача закрыта | T-07 | 2 / 0 |
| `docs/task-for-konard-template.md` | draft | 2026-06-13 | `archive-candidate` | Шаблон постановки на конкретного исполнителя (2026-06-13); шаблоны не хранятся как документы (HTOM) | T-06 | 12 / 2 |
| `docs/taxonomy.md` | draft | 2026-06-11 | `update` | Таксономия операций 2026-06 — источник сайта; сверить с BCREQ и метамоделью Хаба | T-04 | 46 / 3 |
| `docs/taxonomy/README.md` | review | 2026-10-29 | `update` | Ссылки на временную ветку форка konard/G-Ivan-A-mango_ba_prompts; цели существуют в main (F-19) | T-08 | 9 / 0 |
| `docs/taxonomy/catalog-diff.json` | — | — | `current` | Данные каталога продуктов и документации (#399, #401; ADR-013/014) | — | 2 / 0 |
| `docs/taxonomy/cc-difference-checks.json` | — | — | `update` | Ссылки на временную ветку форка konard/G-Ivan-A-mango_ba_prompts; цели существуют в main (F-19) | T-08 | 2 / 0 |
| `docs/taxonomy/cc-pdf-manifest.json` | — | — | `current` | Данные каталога продуктов и документации (#399, #401; ADR-013/014) | — | 4 / 0 |
| `docs/taxonomy/cc-section-differences.md` | review | 2026-10-29 | `update` | Ссылки на временную ветку форка konard/G-Ivan-A-mango_ba_prompts; цели существуют в main (F-19) | T-08 | 2 / 0 |
| `docs/taxonomy/cc-source-comparison.json` | — | — | `update` | Ссылки на временную ветку форка konard/G-Ivan-A-mango_ba_prompts; цели существуют в main (F-19) | T-08 | 5 / 0 |
| `docs/taxonomy/coverage.json` | — | — | `current` | Данные каталога продуктов и документации (#399, #401; ADR-013/014) | — | 2 / 0 |
| `docs/taxonomy/crawl-summary.json` | — | — | `current` | Данные каталога продуктов и документации (#399, #401; ADR-013/014) | — | 2 / 0 |
| `docs/taxonomy/docs-browser-checks.json` | — | — | `current` | Данные каталога продуктов и документации (#399, #401; ADR-013/014) | — | 2 / 0 |
| `docs/taxonomy/docs-crawl-summary.json` | — | — | `current` | Данные каталога продуктов и документации (#399, #401; ADR-013/014) | — | 2 / 0 |
| `docs/taxonomy/docs-readability-checks.json` | — | — | `current` | Данные каталога продуктов и документации (#399, #401; ADR-013/014) | — | 2 / 0 |
| `docs/taxonomy/docs.mango-map.jsonl` | — | — | `current` | Данные каталога продуктов и документации (#399, #401; ADR-013/014) | — | 2 / 0 |
| `docs/taxonomy/documentation-audit.md` | review | 2026-10-29 | `update` | Ссылки на временную ветку форка konard/G-Ivan-A-mango_ba_prompts; цели существуют в main (F-19) | T-08 | 7 / 0 |
| `docs/taxonomy/documentation-sources.json` | — | — | `current` | Данные каталога продуктов и документации (#399, #401; ADR-013/014) | — | 2 / 0 |
| `docs/taxonomy/forensic-evidence.json` | — | — | `current` | Данные каталога продуктов и документации (#399, #401; ADR-013/014) | — | 2 / 0 |
| `docs/taxonomy/portal-audit.jsonl` | — | — | `current` | Данные каталога продуктов и документации (#399, #401; ADR-013/014) | — | 4 / 0 |
| `docs/taxonomy/portal-comparison-audit.jsonl` | — | — | `current` | Данные каталога продуктов и документации (#399, #401; ADR-013/014) | — | 2 / 0 |
| `docs/taxonomy/portal-comparison-summary.json` | — | — | `current` | Данные каталога продуктов и документации (#399, #401; ADR-013/014) | — | 2 / 0 |
| `docs/taxonomy/portal-index.json` | — | — | `update` | Ссылки на временную ветку форка konard/G-Ivan-A-mango_ba_prompts; цели существуют в main (F-19) | T-08 | 2 / 0 |
| `docs/taxonomy/portal-map.jsonl` | — | — | `current` | Данные каталога продуктов и документации (#399, #401; ADR-013/014) | — | 9 / 0 |
| `docs/taxonomy/product-layer.md` | review | 2026-10-28 | `update` | Ссылки на временную ветку форка konard/G-Ivan-A-mango_ba_prompts; цели существуют в main (F-19) | T-08 | 2 / 0 |
| `docs/taxonomy/products.json` | — | — | `current` | Данные каталога продуктов и документации (#399, #401; ADR-013/014) | — | 5 / 2 |
| `docs/taxonomy/readability-checks.json` | — | — | `current` | Данные каталога продуктов и документации (#399, #401; ADR-013/014) | — | 2 / 0 |
| `docs/taxonomy/routing-examples.json` | — | — | `current` | Данные каталога продуктов и документации (#399, #401; ADR-013/014) | — | 2 / 0 |
| `docs/taxonomy/web-source-pairs.json` | — | — | `current` | Данные каталога продуктов и документации (#399, #401; ADR-013/014) | — | 2 / 0 |
| `experiments/amocrm_widget_grounding_probe.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 3 / 0 |
| `experiments/analyze_chat_metrics.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 2 / 0 |
| `experiments/apply-prompt-metadata.mjs` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/bench_validators.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 3 / 0 |
| `experiments/chat_export_probe.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 3 / 0 |
| `experiments/chat_export_usage_metrics.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 3 / 0 |
| `experiments/extract_chat_artifacts.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue-272-validator-negative-check.sh` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_309_fixate_runs.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 3 / 0 |
| `experiments/issue_309_manifest.json` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 4 / 0 |
| `experiments/issue_309_run_stats.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 9 / 0 |
| `experiments/issue_313_extract_pdf_text.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 3 / 0 |
| `experiments/issue_319/L0-preamble.md.in` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 2 / 0 |
| `experiments/issue_319/L4-epilogue.md.in` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 2 / 0 |
| `experiments/issue_319/L4-preamble.md.in` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_319_build_source_mirror.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 4 / 0 |
| `experiments/issue_319_extract_xls_requirements.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 3 / 0 |
| `experiments/issue_319_requirements_statistics.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 4 / 0 |
| `experiments/issue_325/README.md` | active | 2026-08-26 | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 2 / 0 |
| `experiments/issue_325/fetch_wiki.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_325/twin-wiki-pages.tsv` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_325/verify_cols.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 2 / 0 |
| `experiments/issue_325_add_doc_columns.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 2 / 0 |
| `experiments/issue_325_doc_columns_data.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_333_hh_api_source_index.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 5 / 0 |
| `experiments/issue_335_build_report_site.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 3 / 0 |
| `experiments/issue_335_footnote_audit.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 5 / 0 |
| `experiments/issue_335_human_review_checklist.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 2 / 0 |
| `experiments/issue_335_rewrite_footnotes.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_336_fixate_run.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 2 / 0 |
| `experiments/issue_336_link_audit.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 3 / 0 |
| `experiments/issue_339/downloads/appendix-5-telephony.xls` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 2 / 0 |
| `experiments/issue_339/downloads/appendix-6-quality-control.xls` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 2 / 0 |
| `experiments/issue_339/downloads/appendix-7-nfr.xls` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 2 / 0 |
| `experiments/issue_339/generate_run.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 4 / 0 |
| `experiments/issue_339/kbgrep.sh` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 2 / 0 |
| `experiments/issue_339/kbsearch.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 2 / 0 |
| `experiments/issue_347/generate_run.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 4 / 0 |
| `experiments/issue_347/requirements.xlsx` | — | — | `historical` | Данные эксперимента, читаемые валидатором/скриптом; свидетельство задачи | — | 3 / 1 |
| `experiments/issue_351/ab_compare.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_351/assess_part1.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_351/assess_part2.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_351/assess_part3.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_351/assess_part4.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_351/assessments.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_351/cite.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_351/evidence.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_351/extract.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_351/generate_run.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_351/kb_index.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_351/kbsearch.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_351/pagination_audit.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_351/requirements.xlsx` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_351/verify_source_fidelity.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_353/analyze_runs.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 3 / 0 |
| `experiments/issue_353/redact_trace.py` | — | — | `historical` | Данные эксперимента, читаемые валидатором/скриптом; свидетельство задачи | — | 3 / 1 |
| `experiments/issue_353/render_report.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_353/replay_acb_generator.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 3 / 0 |
| `experiments/issue_363/generate_run.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_363/source_transcription.json` | — | — | `historical` | Данные эксперимента, читаемые валидатором/скриптом; свидетельство задачи | — | 3 / 1 |
| `experiments/issue_363/verify_quotes.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_365/check_source.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_365/generate_run.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_365/make_transcription.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_365/source_transcription.json` | — | — | `historical` | Данные эксперимента, читаемые валидатором/скриптом; свидетельство задачи | — | 3 / 1 |
| `experiments/issue_365/tender_similarity.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 2 / 0 |
| `experiments/issue_365/verify_quotes.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_367/check_source.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_367/generate_run.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_367/make_transcription.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_367/research/A_robot.json` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_367/research/A_robot_rows.txt` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_367/research/BRIEF.md` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_367/research/B_chatbot.json` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_367/research/B_chatbot_rows.txt` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_367/research/C_sa.json` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_367/research/C_sa_rows.txt` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_367/research/D_vats.json` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_367/research/D_vats_rows.txt` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_367/source_transcription.json` | — | — | `historical` | Данные эксперимента, читаемые валидатором/скриптом; свидетельство задачи | — | 3 / 1 |
| `experiments/issue_367/tender_index.json` | — | — | `historical` | Данные эксперимента, читаемые валидатором/скриптом; свидетельство задачи | — | 15 / 4 |
| `experiments/issue_367/tender_index.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_367/tender_similarity.json` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_367/tender_similarity.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 6 / 0 |
| `experiments/issue_367/verify_quotes.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_369/check_source.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_369/doc_text.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 2 / 0 |
| `experiments/issue_369/generate_run.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_369/make_transcription.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_369/research/A_doc_func.json` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_369/research/A_doc_func_rows.txt` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_369/research/BRIEF.md` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_369/research/B_doc_integr.json` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_369/research/B_doc_integr_rows.txt` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_369/research/C_doc_sla.json` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_369/research/C_doc_sla_rows.txt` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_369/research/D_xlsx_1.json` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_369/research/D_xlsx_1_rows.txt` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_369/research/E_xlsx_2.json` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_369/research/E_xlsx_2_rows.txt` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_369/source_transcription.json` | — | — | `historical` | Данные эксперимента, читаемые валидатором/скриптом; свидетельство задачи | — | 4 / 1 |
| `experiments/issue_369/tender_similarity.json` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 2 / 0 |
| `experiments/issue_369/tender_similarity.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 2 / 0 |
| `experiments/issue_369/verify_quotes.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_371/check_source.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 2 / 0 |
| `experiments/issue_371/delta.json` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 2 / 0 |
| `experiments/issue_371/delta_align.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 2 / 0 |
| `experiments/issue_371/delta_alignment.json` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 2 / 0 |
| `experiments/issue_371/generate_run.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_371/make_transcription.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_371/research/A_sec1_3_1.json` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_371/research/A_sec1_3_1_rows.txt` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_371/research/BRIEF.md` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_371/research/B_sec3_2_3_3.json` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_371/research/B_sec3_2_3_3_rows.txt` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_371/research/C_sec3_4_4.json` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_371/research/C_sec3_4_4_rows.txt` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_371/research/D_sec5_app2.json` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_371/research/D_sec5_app2_rows.txt` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_371/source_transcription.json` | — | — | `historical` | Данные эксперимента, читаемые валидатором/скриптом; свидетельство задачи | — | 4 / 1 |
| `experiments/issue_371/tender_similarity.json` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 2 / 0 |
| `experiments/issue_371/tender_similarity.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 2 / 0 |
| `experiments/issue_371/verify_quotes.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 2 / 0 |
| `experiments/issue_373/quote-check.json` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 4 / 0 |
| `experiments/issue_373/section-prompts-check.json` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 3 / 0 |
| `experiments/issue_373/stats.json` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 3 / 0 |
| `experiments/issue_373_golden_data.py` | — | — | `historical` | Данные эксперимента, читаемые валидатором/скриптом; свидетельство задачи | — | 4 / 1 |
| `experiments/issue_373_golden_set.py` | — | — | `historical` | Данные эксперимента, читаемые валидатором/скриптом; свидетельство задачи | — | 3 / 1 |
| `experiments/issue_373_section_prompts_check.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 2 / 0 |
| `experiments/issue_373_verify_quotes.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 3 / 0 |
| `experiments/issue_375/quote-check.json` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 4 / 0 |
| `experiments/issue_375/section-prompts-check.json` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 3 / 0 |
| `experiments/issue_375/stats.json` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 3 / 0 |
| `experiments/issue_375_dump.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_375_golden_data.py` | — | — | `historical` | Данные эксперимента, читаемые валидатором/скриптом; свидетельство задачи | — | 3 / 1 |
| `experiments/issue_375_golden_set.py` | — | — | `historical` | Данные эксперимента, читаемые валидатором/скриптом; свидетельство задачи | — | 2 / 1 |
| `experiments/issue_375_section_prompts_check.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 2 / 0 |
| `experiments/issue_375_verify_quotes.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 3 / 0 |
| `experiments/issue_377/cross-run-stats.json` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 5 / 0 |
| `experiments/issue_377/quote-check.json` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 4 / 0 |
| `experiments/issue_377/registry-merge-replay.json` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 4 / 0 |
| `experiments/issue_377/simulate_registry_merges.py` | — | — | `historical` | Данные эксперимента, читаемые валидатором/скриптом; свидетельство задачи | — | 4 / 1 |
| `experiments/issue_377/stats.json` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 3 / 0 |
| `experiments/issue_377_cross_run_stats.py` | — | — | `historical` | Данные эксперимента, читаемые валидатором/скриптом; свидетельство задачи | — | 4 / 1 |
| `experiments/issue_377_golden_data.py` | — | — | `historical` | Данные эксперимента, читаемые валидатором/скриптом; свидетельство задачи | — | 4 / 1 |
| `experiments/issue_377_golden_set.py` | — | — | `historical` | Данные эксперимента, читаемые валидатором/скриптом; свидетельство задачи | — | 3 / 1 |
| `experiments/issue_377_section_prompts_mutations.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 3 / 0 |
| `experiments/issue_377_verify_quotes.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 3 / 0 |
| `experiments/issue_378/quote-check.json` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 3 / 0 |
| `experiments/issue_378/stats.json` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 2 / 0 |
| `experiments/issue_378_golden_data.py` | — | — | `historical` | Данные эксперимента, читаемые валидатором/скриптом; свидетельство задачи | — | 3 / 1 |
| `experiments/issue_378_golden_set.py` | — | — | `historical` | Данные эксперимента, читаемые валидатором/скриптом; свидетельство задачи | — | 2 / 1 |
| `experiments/issue_378_verify_quotes.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 3 / 0 |
| `experiments/issue_382/check_source.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_382/generate_run.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_382/make_transcription.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_382/research/A1_kc1_voice.json` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_382/research/A1_kc1_voice_rows.txt` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_382/research/A2_kc1_chat_email.json` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_382/research/A2_kc1_chat_email_rows.txt` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_382/research/BRIEF.md` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_382/research/B_kc2_admin_voice.json` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_382/research/B_kc2_admin_voice_rows.txt` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_382/research/C_kc2_chat_email.json` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_382/research/C_kc2_chat_email_rows.txt` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_382/research/D_ft1_ft2.json` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_382/research/D_ft1_ft2_rows.txt` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_382/research/E_ft3.json` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_382/research/E_ft3_rows.txt` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_382/source_transcription.json` | — | — | `historical` | Данные эксперимента, читаемые валидатором/скриптом; свидетельство задачи | — | 4 / 1 |
| `experiments/issue_382/tender_similarity.json` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 2 / 0 |
| `experiments/issue_382/tender_similarity.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 2 / 0 |
| `experiments/issue_382/verify_quotes.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 2 / 0 |
| `experiments/issue_384/chat-2026-10-22-23-register.md` | — | — | `historical` | Данные эксперимента, читаемые валидатором/скриптом; свидетельство задачи | — | 6 / 1 |
| `experiments/issue_384/chat-quote-check.json` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 5 / 0 |
| `experiments/issue_384/inventory.json` | — | — | `historical` | Данные эксперимента, читаемые валидатором/скриптом; свидетельство задачи | — | 5 / 1 |
| `experiments/issue_384/prompt-provenance.json` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 4 / 0 |
| `experiments/issue_384_chat_window_dump.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 2 / 0 |
| `experiments/issue_384_check_anchors.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 2 / 0 |
| `experiments/issue_384_prompt_provenance.py` | — | — | `historical` | Данные эксперимента, читаемые валидатором/скриптом; свидетельство задачи | — | 4 / 1 |
| `experiments/issue_384_prompts_inventory.py` | — | — | `historical` | Данные эксперимента, читаемые валидатором/скриптом; свидетельство задачи | — | 4 / 1 |
| `experiments/issue_384_validator_negative.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 2 / 0 |
| `experiments/issue_384_verify_chat_quotes.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 5 / 0 |
| `experiments/issue_387/chat-2026-10-22-23-register.md` | — | — | `historical` | Данные эксперимента, читаемые валидатором/скриптом; свидетельство задачи | — | 19 / 1 |
| `experiments/issue_387/chat-quote-check.json` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 3 / 0 |
| `experiments/issue_387_chat_dump.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_387_expand_quote_refs.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_387_validator_negative.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_388/archive-run.log` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_388/archive_prompts.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_388/archived-prompts.txt` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 3 / 0 |
| `experiments/issue_388/prompt_links_scan.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_388/remap_process_index.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_388/update_patterns.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_388/update_prompts_readme.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_388/validate-full-1.log` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_388/validate-full-2.log` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_388/validate-full-3.log` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_391/browser-before.cjs` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_391/browser-check.cjs` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 2 / 0 |
| `experiments/issue_391/build_review_inventory.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_391/golden_changes.py` | — | — | `historical` | Данные эксперимента, читаемые валидатором/скриптом; свидетельство задачи | — | 2 / 1 |
| `experiments/issue_391/plan.md` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_391/prompt-baseline.json` | — | — | `historical` | Данные эксперимента, читаемые валидатором/скриптом; свидетельство задачи | — | 2 / 1 |
| `experiments/issue_391/review_sources.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_393/browser-check.cjs` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 2 / 0 |
| `experiments/issue_393/catalog.test.cjs` | — | — | `historical` | Данные эксперимента, читаемые валидатором/скриптом; свидетельство задачи | — | 2 / 1 |
| `experiments/issue_393/plan.md` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_393/prompt-baseline.json` | — | — | `historical` | Данные эксперимента, читаемые валидатором/скриптом; свидетельство задачи | — | 2 / 1 |
| `experiments/issue_395/browser-check.cjs` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 2 / 0 |
| `experiments/issue_395/plan.md` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_395/prompt-baseline.json` | — | — | `historical` | Данные эксперимента, читаемые валидатором/скриптом; свидетельство задачи | — | 2 / 1 |
| `experiments/issue_395/site-baseline.json` | — | — | `historical` | Данные эксперимента, читаемые валидатором/скриптом; свидетельство задачи | — | 2 / 1 |
| `experiments/issue_395/source-notes.md` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_395/verification.md` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_397/README.md` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 3 / 0 |
| `experiments/issue_397/build_replay_cases.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 2 / 0 |
| `experiments/issue_397/build_report_refs.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 2 / 0 |
| `experiments/issue_397/curate.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 2 / 0 |
| `experiments/issue_397/evidence.json` | — | — | `historical` | Данные эксперимента, читаемые валидатором/скриптом; свидетельство задачи | — | 2 / 1 |
| `experiments/issue_397/evidence.md` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 2 / 0 |
| `experiments/issue_397/extract.py` | — | — | `historical` | Данные эксперимента, читаемые валидатором/скриптом; свидетельство задачи | — | 3 / 1 |
| `experiments/issue_397/inventory.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 2 / 0 |
| `experiments/issue_397/probe.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 2 / 0 |
| `experiments/issue_397/prompt-probe.json` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 2 / 0 |
| `experiments/issue_397/replay-cases.json` | — | — | `historical` | Данные эксперимента, читаемые валидатором/скриптом; свидетельство задачи | — | 3 / 1 |
| `experiments/issue_397/replay-results.json` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 2 / 0 |
| `experiments/issue_397/replay.py` | — | — | `historical` | Данные эксперимента, читаемые валидатором/скриптом; свидетельство задачи | — | 3 / 1 |
| `experiments/issue_397/run-inventory.json` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 2 / 0 |
| `experiments/issue_397/verify.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 3 / 0 |
| `experiments/issue_399/WORKPLAN.md` | review | 2026-10-28 | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_399/additions.json` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_399/audit.py` | — | — | `historical` | Данные эксперимента, читаемые валидатором/скриптом; свидетельство задачи | — | 4 / 1 |
| `experiments/issue_399/baseline.json` | — | — | `historical` | Данные эксперимента, читаемые валидатором/скриптом; свидетельство задачи | — | 2 / 1 |
| `experiments/issue_399/build.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 2 / 0 |
| `experiments/issue_399/check_evidence.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 2 / 0 |
| `experiments/issue_399/curate.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 2 / 0 |
| `experiments/issue_399/prepare_sources.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 2 / 0 |
| `experiments/issue_399/route.py` | — | — | `historical` | Данные эксперимента, читаемые валидатором/скриптом; свидетельство задачи | — | 3 / 1 |
| `experiments/issue_401/WORKPLAN.md` | review | 2026-10-29 | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_401/audit.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 2 / 0 |
| `experiments/issue_401/browser_probe.js` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 2 / 0 |
| `experiments/issue_401/build_comparison.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 2 / 0 |
| `experiments/issue_401/build_evidence.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 2 / 0 |
| `experiments/issue_401/collect_portal.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 2 / 0 |
| `experiments/issue_401/compare.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_401/compare_pairs.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 2 / 0 |
| `experiments/issue_401/extract_pdf.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 2 / 0 |
| `experiments/issue_401/inspect_differences.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_401/probe_matches.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_401/probe_pdf.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_401/requirements.txt` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 2 / 0 |
| `experiments/issue_403/build_catalog.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_403/check_replay.py` | — | — | `historical` | Данные эксперимента, читаемые валидатором/скриптом; свидетельство задачи | — | 3 / 2 |
| `experiments/issue_403/plan.md` | draft | 2026-10-29 | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_405/acceptance.md` | draft | 2026-10-30 | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 4 / 0 |
| `experiments/issue_405/class-mapping.json` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 2 / 0 |
| `experiments/issue_405/comparison.json` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_405/examples/README.md` | draft | 2026-10-30 | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 4 / 0 |
| `experiments/issue_405/examples/contract-fixture.json` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_405/examples/goose-review.json` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_405/examples/opencode-v1.json` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_405/examples/rule-template.md` | draft | 2026-10-30 | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_405/examples/skill-template.md` | draft | 2026-10-30 | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/issue_405/fetch_sources.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 2 / 0 |
| `experiments/issue_405/plan.md` | draft | 2026-10-30 | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 4 / 0 |
| `experiments/issue_405/requirements.json` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 2 / 0 |
| `experiments/issue_405/source-observations.json` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 3 / 0 |
| `experiments/kb-heading-size-probe.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/kb-refresh-collection-index.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/kb-validate-317.log` | — | — | `archive-candidate` | Несвязанный лог эксперимента в корне experiments/ (issue #317) | T-07 | 1 / 0 |
| `experiments/kb-validate-317d.log` | — | — | `archive-candidate` | Несвязанный лог эксперимента в корне experiments/ (issue #317) | T-07 | 1 / 0 |
| `experiments/kb-validate-317f.log` | — | — | `archive-candidate` | Несвязанный лог эксперимента в корне experiments/ (issue #317) | T-07 | 1 / 0 |
| `experiments/kb-verify-detects-hallucination.py` | — | — | `historical` | Данные эксперимента, читаемые валидатором/скриптом; свидетельство задачи | — | 3 / 1 |
| `experiments/okdesk_citation_grounding_probe.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 3 / 0 |
| `experiments/parse_58093_chat_export.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 3 / 0 |
| `experiments/parse_765_chat_export.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 3 / 0 |
| `experiments/parse_qwen_chat_export.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 3 / 0 |
| `experiments/re-extract-cc.log` | — | — | `archive-candidate` | Несвязанный лог эксперимента в корне experiments/ (issue #317) | T-07 | 1 / 0 |
| `experiments/re-extract-cc2.log` | — | — | `archive-candidate` | Несвязанный лог эксперимента в корне experiments/ (issue #317) | T-07 | 1 / 0 |
| `experiments/re-extract-fil.log` | — | — | `archive-candidate` | Несвязанный лог эксперимента в корне experiments/ (issue #317) | T-07 | 1 / 0 |
| `experiments/re-extract-fil2.log` | — | — | `archive-candidate` | Несвязанный лог эксперимента в корне experiments/ (issue #317) | T-07 | 1 / 0 |
| `experiments/re-extract-mtalker2.log` | — | — | `archive-candidate` | Несвязанный лог эксперимента в корне experiments/ (issue #317) | T-07 | 1 / 0 |
| `experiments/re-extract-mtalker3.log` | — | — | `archive-candidate` | Несвязанный лог эксперимента в корне experiments/ (issue #317) | T-07 | 1 / 0 |
| `experiments/restructure_governance_dirs.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 8 / 0 |
| `experiments/restructure_governance_to_canonical_homes.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 3 / 0 |
| `experiments/restructure_root_and_archive.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 4 / 0 |
| `experiments/run-0014-chat-export/README.md` | draft | 2026-08-21 | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 4 / 0 |
| `experiments/run-0014-chat-export/render_chat_export.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 2 / 0 |
| `experiments/run-0014-chat-export/transcript-front-matter.yaml` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 2 / 0 |
| `experiments/scan_broken_links.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/signature_citation_grounding_probe.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 3 / 0 |
| `experiments/test_sync_link_rewrite.py` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/typo-probe-317.log` | — | — | `archive-candidate` | Несвязанный лог эксперимента в корне experiments/ (issue #317) | T-07 | 1 / 0 |
| `experiments/update-readme-matrix.mjs` | — | — | `historical` | Скрипт или данные эксперимента закрытой задачи; свидетельство | — | 1 / 0 |
| `experiments/validate-full-317.log` | — | — | `archive-candidate` | Несвязанный лог эксперимента в корне experiments/ (issue #317) | T-07 | 1 / 0 |
| `experiments/validate-full-317b.log` | — | — | `archive-candidate` | Несвязанный лог эксперимента в корне experiments/ (issue #317) | T-07 | 1 / 0 |
| `experiments/validate-full-317c.log` | — | — | `archive-candidate` | Несвязанный лог эксперимента в корне experiments/ (issue #317) | T-07 | 1 / 0 |
| `experiments/validate-full-317d.log` | — | — | `archive-candidate` | Несвязанный лог эксперимента в корне experiments/ (issue #317) | T-07 | 1 / 0 |
| `experiments/validate-full-317e.log` | — | — | `archive-candidate` | Несвязанный лог эксперимента в корне experiments/ (issue #317) | T-07 | 1 / 0 |
| `experiments/validate-full-317f.log` | — | — | `archive-candidate` | Несвязанный лог эксперимента в корне experiments/ (issue #317) | T-07 | 1 / 0 |
| `experiments/verify-317-round2.log` | — | — | `archive-candidate` | Несвязанный лог эксперимента в корне experiments/ (issue #317) | T-07 | 1 / 0 |
| `kb/.gitkeep` | — | — | `archive-candidate` | Каталог kb/ не пуст; маркер не нужен | T-05 | 2 / 0 |
| `kb/README.md` | draft | 2026-06-16 | `update` | Описывает локальную KB до переезда (#361) | T-05 | 28 / 2 |
| `kb/STRUCTURE_REVIEW.md` | draft | 2026-08-25 | `historical` | Ревью структуры KB 2026-08 до переезда | — | 3 / 0 |
| `kb/USAGE.md` | draft | 2026-08-22 | `update` | 9 ссылок на kb/processed после переезда KB | T-05 | 10 / 3 |
| `kb/fragments/README.md` | draft | 2026-06-18 | `update` | Локальная KB после переезда в mango-ba-ai-runtime | T-05 | 5 / 1 |
| `kb/practices/source-backed-analysis.md` | draft | 2026-06-16 | `update` | Локальная KB после переезда в mango-ba-ai-runtime | T-05 | 5 / 0 |
| `kb/processed/README.md` | canonical | 2026-09-26 | `update` | Указатель актуален, но frontmatter содержит запрещённый Хабом ai-generated | T-05 | 20 / 4 |
| `kb/sources/README.md` | draft | 2026-06-20 | `update` | 21 ссылка на kb/processed после переезда KB | T-05 | 11 / 4 |
| `kb/sources/Rolevaya-model-vats/.gitkeep` | — | — | `update` | Метаданные источников KB; SSOT KB теперь mango-ba-ai-runtime/docs/kb | T-05 | 1 / 0 |
| `kb/sources/Rolevaya-model-vats/meta.json` | — | — | `update` | Метаданные источников KB; SSOT KB теперь mango-ba-ai-runtime/docs/kb | T-05 | 1 / 0 |
| `kb/sources/contact-center-manual/source.md` | pending-source-file | 2026-06-18 | `update` | Метаданные источников KB; SSOT KB теперь mango-ba-ai-runtime/docs/kb | T-05 | 7 / 2 |
| `kb/sources/cov-robot-fil/meta.json` | — | — | `update` | Метаданные источников KB; SSOT KB теперь mango-ba-ai-runtime/docs/kb | T-05 | 1 / 0 |
| `kb/sources/integration-bitrix24/.gitkeep` | — | — | `update` | Метаданные источников KB; SSOT KB теперь mango-ba-ai-runtime/docs/kb | T-05 | 1 / 0 |
| `kb/sources/integration-bitrix24/meta.json` | — | — | `update` | Метаданные источников KB; SSOT KB теперь mango-ba-ai-runtime/docs/kb | T-05 | 1 / 0 |
| `kb/sources/integration-bpmsoft/.gitkeep` | — | — | `update` | Метаданные источников KB; SSOT KB теперь mango-ba-ai-runtime/docs/kb | T-05 | 1 / 0 |
| `kb/sources/integration-bpmsoft/meta.json` | — | — | `update` | Метаданные источников KB; SSOT KB теперь mango-ba-ai-runtime/docs/kb | T-05 | 1 / 0 |
| `kb/sources/integration_1c/.gitkeep` | — | — | `update` | Метаданные источников KB; SSOT KB теперь mango-ba-ai-runtime/docs/kb | T-05 | 1 / 0 |
| `kb/sources/integration_1c/meta.json` | — | — | `update` | Метаданные источников KB; SSOT KB теперь mango-ba-ai-runtime/docs/kb | T-05 | 1 / 0 |
| `kb/sources/integration_amocrm/.gitkeep` | — | — | `update` | Метаданные источников KB; SSOT KB теперь mango-ba-ai-runtime/docs/kb | T-05 | 1 / 0 |
| `kb/sources/integration_amocrm/meta.json` | — | — | `update` | Метаданные источников KB; SSOT KB теперь mango-ba-ai-runtime/docs/kb | T-05 | 1 / 0 |
| `kb/sources/lk-vats-sso/.gitkeep` | — | — | `update` | Метаданные источников KB; SSOT KB теперь mango-ba-ai-runtime/docs/kb | T-05 | 1 / 0 |
| `kb/sources/lk-vats-sso/meta.json` | — | — | `update` | Метаданные источников KB; SSOT KB теперь mango-ba-ai-runtime/docs/kb | T-05 | 1 / 0 |
| `kb/sources/mango-cc-manual/.gitkeep` | — | — | `update` | Метаданные источников KB; SSOT KB теперь mango-ba-ai-runtime/docs/kb | T-05 | 1 / 0 |
| `kb/sources/mango-cc-manual/meta.json` | — | — | `update` | Метаданные источников KB; SSOT KB теперь mango-ba-ai-runtime/docs/kb | T-05 | 4 / 1 |
| `kb/sources/mango-lk-manual/.gitkeep` | — | — | `update` | Метаданные источников KB; SSOT KB теперь mango-ba-ai-runtime/docs/kb | T-05 | 1 / 0 |
| `kb/sources/mango-lk-manual/meta.json` | — | — | `update` | Метаданные источников KB; SSOT KB теперь mango-ba-ai-runtime/docs/kb | T-05 | 4 / 1 |
| `kb/sources/mdialogi-api/.gitkeep` | — | — | `update` | Метаданные источников KB; SSOT KB теперь mango-ba-ai-runtime/docs/kb | T-05 | 1 / 0 |
| `kb/sources/mdialogi-api/meta.json` | — | — | `update` | Метаданные источников KB; SSOT KB теперь mango-ba-ai-runtime/docs/kb | T-05 | 1 / 0 |
| `kb/sources/mtalker/.gitkeep` | — | — | `update` | Метаданные источников KB; SSOT KB теперь mango-ba-ai-runtime/docs/kb | T-05 | 1 / 0 |
| `kb/sources/mtalker/meta.json` | — | — | `update` | Метаданные источников KB; SSOT KB теперь mango-ba-ai-runtime/docs/kb | T-05 | 5 / 1 |
| `kb/sources/quality-managment/.gitkeep` | — | — | `update` | Метаданные источников KB; SSOT KB теперь mango-ba-ai-runtime/docs/kb | T-05 | 1 / 0 |
| `kb/sources/quality-managment/meta.json` | — | — | `update` | Метаданные источников KB; SSOT KB теперь mango-ba-ai-runtime/docs/kb | T-05 | 1 / 0 |
| `kb/sources/sip-trunk/.gitkeep` | — | — | `update` | Метаданные источников KB; SSOT KB теперь mango-ba-ai-runtime/docs/kb | T-05 | 1 / 0 |
| `kb/sources/sip-trunk/meta.json` | — | — | `update` | Метаданные источников KB; SSOT KB теперь mango-ba-ai-runtime/docs/kb | T-05 | 1 / 0 |
| `kb/sources/speech-analytics/.gitkeep` | — | — | `update` | Метаданные источников KB; SSOT KB теперь mango-ba-ai-runtime/docs/kb | T-05 | 1 / 0 |
| `kb/sources/speech-analytics/meta.json` | — | — | `update` | Метаданные источников KB; SSOT KB теперь mango-ba-ai-runtime/docs/kb | T-05 | 1 / 0 |
| `kb/sources/vpbx-api/.gitkeep` | — | — | `update` | Метаданные источников KB; SSOT KB теперь mango-ba-ai-runtime/docs/kb | T-05 | 1 / 0 |
| `kb/sources/vpbx-api/meta.json` | — | — | `update` | Метаданные источников KB; SSOT KB теперь mango-ba-ai-runtime/docs/kb | T-05 | 1 / 0 |
| `kb/sources/wallboard/.gitkeep` | — | — | `update` | Метаданные источников KB; SSOT KB теперь mango-ba-ai-runtime/docs/kb | T-05 | 1 / 0 |
| `kb/sources/wallboard/meta.json` | — | — | `update` | Метаданные источников KB; SSOT KB теперь mango-ba-ai-runtime/docs/kb | T-05 | 1 / 0 |
| `kb/sources/web-links/README.md` | draft | 2026-06-18 | `update` | Метаданные источников KB; SSOT KB теперь mango-ba-ai-runtime/docs/kb | T-05 | 5 / 1 |
| `patterns/README.md` | draft | 2026-06-15 | `update` | Матрица паттернов привязана к процессам «Формирование/Валидация ФТ/ТЗ» | T-04 | 17 / 3 |
| `patterns/asr-ingestion/README.md` | draft | 2026-06-15 | `update` | Пример паттерна 2026-06 для до-BCREQ процесса; синхронно с T-04 | T-04 | 2 / 0 |
| `patterns/asr-ingestion/examples/basic-example.md` | — | — | `update` | Пример паттерна 2026-06 для до-BCREQ процесса; синхронно с T-04 | T-04 | 1 / 0 |
| `patterns/fr-generation/README.md` | draft | 2026-06-15 | `update` | Пример паттерна 2026-06 для до-BCREQ процесса; синхронно с T-04 | T-04 | 4 / 0 |
| `patterns/fr-generation/examples/basic-example.md` | — | — | `update` | Пример паттерна 2026-06 для до-BCREQ процесса; синхронно с T-04 | T-04 | 1 / 0 |
| `patterns/fr-validation/README.md` | draft | 2026-06-15 | `update` | Пример паттерна 2026-06 для до-BCREQ процесса; синхронно с T-04 | T-04 | 4 / 0 |
| `patterns/fr-validation/examples/basic-example.md` | — | — | `update` | Пример паттерна 2026-06 для до-BCREQ процесса; синхронно с T-04 | T-04 | 1 / 0 |
| `patterns/glossary-context-generation/README.md` | draft | 2026-06-15 | `update` | Пример паттерна 2026-06 для до-BCREQ процесса; синхронно с T-04 | T-04 | 3 / 0 |
| `patterns/glossary-context-generation/examples/basic-example.md` | — | — | `update` | Пример паттерна 2026-06 для до-BCREQ процесса; синхронно с T-04 | T-04 | 1 / 0 |
| `patterns/meeting-summary-generation/README.md` | draft | 2026-06-15 | `update` | Пример паттерна 2026-06 для до-BCREQ процесса; синхронно с T-04 | T-04 | 2 / 0 |
| `patterns/meeting-summary-generation/examples/basic-example.md` | — | — | `update` | Пример паттерна 2026-06 для до-BCREQ процесса; синхронно с T-04 | T-04 | 1 / 0 |
| `patterns/usecase-generation/README.md` | draft | 2026-06-15 | `update` | Пример паттерна 2026-06 для до-BCREQ процесса; синхронно с T-04 | T-04 | 3 / 0 |
| `patterns/usecase-generation/examples/basic-example.md` | — | — | `update` | Пример паттерна 2026-06 для до-BCREQ процесса; синхронно с T-04 | T-04 | 1 / 0 |
| `patterns/user-story-generation/README.md` | draft | 2026-06-15 | `update` | Пример паттерна 2026-06 для до-BCREQ процесса; синхронно с T-04 | T-04 | 3 / 0 |
| `patterns/user-story-generation/examples/basic-example.md` | — | — | `update` | Пример паттерна 2026-06 для до-BCREQ процесса; синхронно с T-04 | T-04 | 1 / 0 |
| `pr-ops/BACKLOG.md` | draft | 2026-08-21 | `update` | Маркеры «evals отсутствуют» устарели после golden-set #373–#378 | T-08 | 30 / 6 |
| `pr-ops/artifact-map.md` | draft | 2026-10-28 | `update` | Карта артефактов: ADR-009 Хаба смешан с локальным ADR 009; нет mango-ba-ai-runtime | T-08 | 31 / 4 |
| `pr-ops/migration-issues-registry.md` | — | — | `archive-candidate` | Миграция 2026-06 завершена; нет frontmatter | T-07 | 4 / 0 |
| `pr-ops/migration-manifest.md` | draft | 2026-06-05 | `archive-candidate` | Миграция 2026-06 завершена | T-07 | 11 / 1 |
| `pr-ops/migration-phase1-issues.md` | draft | 2026-06-04 | `archive-candidate` | Миграция 2026-06 завершена | T-07 | 6 / 1 |
| `pr-ops/prompt-feedback.json` | — | — | `current` | Операционный реестр | — | 12 / 2 |
| `pr-ops/session-digests.md` | draft | 2026-06-13 | `archive-candidate` | Дайджесты сессий 2026-06; заменены runs/ и CHANGELOG | T-07 | 18 / 1 |
| `pr-ops/sync-matrix-2026-06-17.md` | draft | 2026-06-16 | `archive-candidate` | Матрица синхронизации на 2026-06-17; заменена ADR-0004 и .hub-profile.json | T-07 | 10 / 0 |
| `prompts/AI_SESSION_HANDOVER_PROMPT.executable.md` | draft | 2026-08-21 | `current` | Промпт или навигация каталога | — | 17 / 3 |
| `prompts/README.executable.md` | draft | 2026-10-24 | `current` | Промпт или навигация каталога | — | 12 / 1 |
| `prompts/README.md` | draft | 2026-10-24 | `update` | Навигация актуальна; ai-generated во frontmatter и ссылка на docs/contracts | T-06 | 36 / 4 |
| `prompts/archive/.gitkeep` | — | — | `archived` | Каталог архивных промптов (issue #388); источник раздела «архив» на сайте | — | 4 / 0 |
| `prompts/archive/constraints-documentation-oneshot.md` | archived | 2026-06-11 | `archived` | Каталог архивных промптов (issue #388); источник раздела «архив» на сайте | — | 9 / 0 |
| `prompts/archive/constraints-documentation-stepwise.md` | archived | 2026-06-11 | `archived` | Каталог архивных промптов (issue #388); источник раздела «архив» на сайте | — | 10 / 0 |
| `prompts/archive/fr-documentation-oneshot.md` | archived | 2026-06-11 | `archived` | Каталог архивных промптов (issue #388); источник раздела «архив» на сайте | — | 11 / 0 |
| `prompts/archive/fr-documentation-stepwise.md` | archived | 2026-06-11 | `archived` | Каталог архивных промптов (issue #388); источник раздела «архив» на сайте | — | 14 / 1 |
| `prompts/archive/fr-validation-legacy.md` | archived | 2026-06-11 | `archived` | Каталог архивных промптов (issue #388); источник раздела «архив» на сайте | — | 12 / 0 |
| `prompts/archive/fr-validation-oneshot.md` | archived | 2026-06-11 | `archived` | Каталог архивных промптов (issue #388); источник раздела «архив» на сайте | — | 11 / 0 |
| `prompts/archive/fr-validation-stepwise.md` | archived | 2026-06-11 | `archived` | Каталог архивных промптов (issue #388); источник раздела «архив» на сайте | — | 11 / 0 |
| `prompts/archive/glossary-context-understanding-oneshot.md` | archived | 2026-06-11 | `archived` | Каталог архивных промптов (issue #388); источник раздела «архив» на сайте | — | 11 / 0 |
| `prompts/archive/glossary-context-understanding-stepwise.md` | archived | 2026-06-11 | `archived` | Каталог архивных промптов (issue #388); источник раздела «архив» на сайте | — | 15 / 0 |
| `prompts/archive/questions-customer-understanding-legacy.md` | archived | 2026-06-11 | `archived` | Каталог архивных промптов (issue #388); источник раздела «архив» на сайте | — | 8 / 0 |
| `prompts/archive/questions-customer-understanding-stepwise.md` | archived | 2026-06-11 | `archived` | Каталог архивных промптов (issue #388); источник раздела «архив» на сайте | — | 10 / 0 |
| `prompts/archive/technical-details-solution-design-legacy.md` | archived | 2026-06-11 | `archived` | Каталог архивных промптов (issue #388); источник раздела «архив» на сайте | — | 8 / 0 |
| `prompts/archive/technical-details-solution-design-oneshot.md` | archived | 2026-06-11 | `archived` | Каталог архивных промптов (issue #388); источник раздела «архив» на сайте | — | 8 / 0 |
| `prompts/archive/technical-details-solution-design-stepwise.md` | archived | 2026-06-11 | `archived` | Каталог архивных промптов (issue #388); источник раздела «архив» на сайте | — | 9 / 0 |
| `prompts/archive/tz-stats-generator-legacy.md` | archived | 2026-06-04 | `archived` | Каталог архивных промптов (issue #388); источник раздела «архив» на сайте | — | 9 / 0 |
| `prompts/archive/tz-stats-generator-simple-legacy.md` | archived | 2026-06-04 | `archived` | Каталог архивных промптов (issue #388); источник раздела «архив» на сайте | — | 8 / 0 |
| `prompts/archive/uc-modeling-oneshot.md` | archived | 2026-06-11 | `archived` | Каталог архивных промптов (issue #388); источник раздела «архив» на сайте | — | 10 / 0 |
| `prompts/archive/uc-modeling-stepwise.md` | archived | 2026-06-11 | `archived` | Каталог архивных промптов (issue #388); источник раздела «архив» на сайте | — | 10 / 0 |
| `prompts/archive/us-modeling-oneshot.md` | archived | 2026-06-11 | `archived` | Каталог архивных промптов (issue #388); источник раздела «архив» на сайте | — | 10 / 0 |
| `prompts/archive/us-modeling-stepwise.md` | archived | 2026-06-11 | `archived` | Каталог архивных промптов (issue #388); источник раздела «архив» на сайте | — | 10 / 0 |
| `prompts/archive/usecase-stepwise-generator-legacy.md` | archived | 2026-06-04 | `archived` | Каталог архивных промптов (issue #388); источник раздела «архив» на сайте | — | 9 / 0 |
| `prompts/archive/usecase-stepwise-generator-simple-legacy.md` | archived | 2026-06-04 | `archived` | Каталог архивных промптов (issue #388); источник раздела «архив» на сайте | — | 8 / 0 |
| `prompts/archive/user-story-generator-legacy.md` | archived | 2026-06-04 | `archived` | Каталог архивных промптов (issue #388); источник раздела «архив» на сайте | — | 9 / 0 |
| `prompts/archive/user-story-generator-simple-legacy.md` | archived | 2026-06-04 | `archived` | Каталог архивных промптов (issue #388); источник раздела «архив» на сайте | — | 8 / 0 |
| `prompts/asr-ingestion-legacy.md` | draft | 2026-06-11 | `archive-candidate` | Режим legacy 2026-06; в каталоге сайта BCREQ-only (#391); заменён asr-ingestion-oneshot | T-07 | 9 / 0 |
| `prompts/asr-ingestion-oneshot.md` | draft | 2026-06-11 | `current` | Промпт или навигация каталога | — | 10 / 0 |
| `prompts/bcreq-constitution-governance-oneshot.md` | draft | 2026-10-24 | `current` | Промпт или навигация каталога | — | 36 / 0 |
| `prompts/bcreq-constraints-documentation-stepwise.md` | draft | 2026-10-24 | `current` | Промпт или навигация каталога | — | 21 / 0 |
| `prompts/bcreq-context-understanding-stepwise.md` | draft | 2026-10-24 | `current` | Промпт или навигация каталога | — | 32 / 0 |
| `prompts/bcreq-core-documentation-oneshot.md` | draft | 2026-10-24 | `current` | Промпт или навигация каталога | — | 23 / 0 |
| `prompts/bcreq-extra-risk-analysis-stepwise.md` | draft | 2026-10-24 | `current` | Промпт или навигация каталога | — | 20 / 0 |
| `prompts/bcreq-fr-documentation-stepwise.md` | draft | 2026-10-24 | `current` | Промпт или навигация каталога | — | 26 / 1 |
| `prompts/bcreq-in-understanding-oneshot.md` | draft | 2026-10-24 | `current` | Промпт или навигация каталога | — | 26 / 0 |
| `prompts/bcreq-nfr-documentation-stepwise.md` | draft | 2026-10-24 | `current` | Промпт или навигация каталога | — | 18 / 0 |
| `prompts/bcreq-orr-solution-design-stepwise.md` | draft | 2026-10-24 | `current` | Промпт или навигация каталога | — | 25 / 0 |
| `prompts/bcreq-products-impact-analysis-stepwise.md` | draft | 2026-10-24 | `current` | Промпт или навигация каталога | — | 24 / 0 |
| `prompts/bcreq-review-validation-oneshot.md` | draft | 2026-10-24 | `current` | Промпт или навигация каталога | — | 32 / 0 |
| `prompts/bcreq-scenarios-modeling-oneshot.md` | draft | 2026-10-24 | `current` | Промпт или навигация каталога | — | 27 / 0 |
| `prompts/bcreq-uc-modeling-stepwise.md` | draft | 2026-10-24 | `current` | Промпт или навигация каталога | — | 27 / 0 |
| `prompts/bcreq-work-solution-design-oneshot.md` | draft | 2026-10-24 | `current` | Промпт или навигация каталога | — | 19 / 0 |
| `prompts/letter-customer-documentation-legacy.md` | draft | 2026-06-11 | `archive-candidate` | Режим legacy 2026-06; в каталоге сайта BCREQ-only (#391) | T-07 | 12 / 0 |
| `prompts/meeting-customer-documentation-stepwise.md` | draft | 2026-06-11 | `current` | Промпт или навигация каталога | — | 10 / 0 |
| `prompts/meeting-team-documentation-stepwise.md` | draft | 2026-06-11 | `current` | Промпт или навигация каталога | — | 10 / 0 |
| `prompts/session-debug-documentation-oneshot.md` | draft | 2026-06-20 | `current` | Промпт или навигация каталога | — | 9 / 1 |
| `scripts/_validator_trace.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 6 / 2 |
| `scripts/chat_export_to_markdown.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 13 / 2 |
| `scripts/chat_export_to_transcript.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 4 / 1 |
| `scripts/data/runs-legacy-moved-paths.txt` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 4 / 1 |
| `scripts/generate-pages-data.mjs` | — | — | `update` | Дорожная карта сайта парсится из docs/ba-ecosystem.md; ссылки на docs/contracts/ | T-03 | 25 / 3 |
| `scripts/kb/README.md` | — | — | `update` | Скрипт KB-конвейера пишет в kb/processed, перенесённый в mango-ba-ai-runtime | T-05 | 8 / 2 |
| `scripts/kb/extract.py` | — | — | `update` | Скрипт KB-конвейера пишет в kb/processed, перенесённый в mango-ba-ai-runtime | T-05 | 15 / 8 |
| `scripts/kb/make_sample_pdf.py` | — | — | `update` | Скрипт KB-конвейера пишет в kb/processed, перенесённый в mango-ba-ai-runtime | T-05 | 10 / 4 |
| `scripts/kb/process_sources.py` | — | — | `update` | Скрипт KB-конвейера пишет в kb/processed, перенесённый в mango-ba-ai-runtime | T-05 | 16 / 5 |
| `scripts/kb/requirements.txt` | — | — | `update` | Скрипт KB-конвейера пишет в kb/processed, перенесённый в mango-ba-ai-runtime | T-05 | 11 / 5 |
| `scripts/kb/runtime_snapshot.py` | — | — | `update` | Скрипт KB-конвейера пишет в kb/processed, перенесённый в mango-ba-ai-runtime | T-05 | 2 / 0 |
| `scripts/kb/tokens.py` | — | — | `update` | Скрипт KB-конвейера пишет в kb/processed, перенесённый в mango-ba-ai-runtime | T-05 | 10 / 3 |
| `scripts/kb/verify_extraction.py` | — | — | `update` | Скрипт KB-конвейера пишет в kb/processed, перенесённый в mango-ba-ai-runtime | T-05 | 4 / 1 |
| `scripts/resolve_registry_conflicts.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 10 / 3 |
| `scripts/set-site-password.mjs` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 5 / 2 |
| `scripts/sync_from_hub.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 23 / 3 |
| `scripts/test_issue_323_issue_forms.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 3 / 0 |
| `scripts/test_issue_353_redact_trace.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 1 / 0 |
| `scripts/test_issue_361_kb_migration.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 1 / 0 |
| `scripts/test_issue_391_lessons.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 3 / 0 |
| `scripts/test_issue_391_site.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 2 / 0 |
| `scripts/test_issue_393_site.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 2 / 0 |
| `scripts/test_issue_395_bcreq.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 2 / 0 |
| `scripts/test_issue_395_site.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 3 / 0 |
| `scripts/test_issue_397_evidence.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 2 / 0 |
| `scripts/test_issue_399_taxonomy.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 2 / 0 |
| `scripts/test_issue_401_documentation.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 2 / 0 |
| `scripts/test_resolve_registry_conflicts.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 3 / 0 |
| `scripts/test_runs_contract_run_type.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 8 / 1 |
| `scripts/test_runs_registry_tools_table.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 3 / 0 |
| `scripts/test_validate_all.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 5 / 1 |
| `scripts/test_validate_pagination_shift.py` | — | — | `update` | Тест ссылается на kb/processed | T-05 | 1 / 0 |
| `scripts/validate_all.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 19 / 4 |
| `scripts/validate_issue_103_ui_fixes.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 3 / 1 |
| `scripts/validate_issue_111_kb_pipeline.py` | — | — | `update` | Валидатор KB-конвейера ссылается на kb/processed | T-05 | 11 / 3 |
| `scripts/validate_issue_115_kb_mango_pipeline.py` | — | — | `update` | Валидатор KB-конвейера ссылается на kb/processed | T-05 | 9 / 2 |
| `scripts/validate_issue_117_kb_traceability.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 8 / 2 |
| `scripts/validate_issue_121_kb_multi_file.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 8 / 2 |
| `scripts/validate_issue_123_runs_contract.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 9 / 1 |
| `scripts/validate_issue_125_cascading_context.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 5 / 1 |
| `scripts/validate_issue_263_vision_alignment.py` | — | — | `update` | Валидатор запирает видение #263 (REQUIRED_TEXT/CONCEPT_DOCS); меняется вместе с ADR из T-02 | T-02 | 4 / 1 |
| `scripts/validate_issue_265_hub_sync.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 7 / 2 |
| `scripts/validate_issue_267_onboarding_v15.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 5 / 1 |
| `scripts/validate_issue_272_run_0019.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 5 / 1 |
| `scripts/validate_issue_291_root_structure.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 6 / 1 |
| `scripts/validate_issue_310_kb_pdf_ingestion.py` | — | — | `update` | Валидатор KB-конвейера ссылается на kb/processed | T-05 | 8 / 2 |
| `scripts/validate_issue_323_issue_forms.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 3 / 0 |
| `scripts/validate_issue_335_report_site.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 3 / 0 |
| `scripts/validate_issue_339_run.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 5 / 0 |
| `scripts/validate_issue_343_run.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 4 / 0 |
| `scripts/validate_issue_345_run.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 3 / 0 |
| `scripts/validate_issue_347_run.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 3 / 0 |
| `scripts/validate_issue_349_critical_fix.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 2 / 0 |
| `scripts/validate_issue_351_run.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 2 / 0 |
| `scripts/validate_issue_353_ab_rca.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 4 / 0 |
| `scripts/validate_issue_355_run.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 2 / 0 |
| `scripts/validate_issue_357_hub_backlog_validation.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 2 / 0 |
| `scripts/validate_issue_363_run.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 2 / 0 |
| `scripts/validate_issue_365_run.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 2 / 0 |
| `scripts/validate_issue_367_run.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 2 / 0 |
| `scripts/validate_issue_369_run.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 2 / 0 |
| `scripts/validate_issue_371_run.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 2 / 0 |
| `scripts/validate_issue_373_run.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 2 / 0 |
| `scripts/validate_issue_375_run.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 2 / 0 |
| `scripts/validate_issue_377_merge_hygiene.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 4 / 0 |
| `scripts/validate_issue_377_run.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 2 / 0 |
| `scripts/validate_issue_377_section_prompts.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 4 / 0 |
| `scripts/validate_issue_378_run.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 2 / 0 |
| `scripts/validate_issue_382_run.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 2 / 0 |
| `scripts/validate_issue_384_prompts_audit.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 4 / 0 |
| `scripts/validate_issue_387_bcreq_meta_standards.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 5 / 0 |
| `scripts/validate_issue_388_bcreq_site.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 4 / 1 |
| `scripts/validate_issue_403_manual_pipeline.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 1 / 0 |
| `scripts/validate_issue_405_ide_research.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 5 / 0 |
| `scripts/validate_issue_61_governance.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 3 / 0 |
| `scripts/validate_issue_64_pattern_adr.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 4 / 0 |
| `scripts/validate_issue_72_hub_sync.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 4 / 0 |
| `scripts/validate_issue_74_github_pages.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 5 / 1 |
| `scripts/validate_issue_83_ba_process_map.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 3 / 0 |
| `scripts/validate_issue_85_patterns_library.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 4 / 0 |
| `scripts/validate_issue_86_mango_widget.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 4 / 1 |
| `scripts/validate_issue_91_pages_enhancements.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 4 / 1 |
| `scripts/validate_issue_95_prompt_id_in_copy.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 4 / 1 |
| `scripts/validate_issue_97_ontology_standards.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 19 / 1 |
| `scripts/validate_issue_99_pages_optimization.py` | — | — | `current` | Валидатор, тест или инструмент, подключённый к validate_all/CI | — | 4 / 1 |
| `scripts/validate_pagination_shift.py` | — | — | `update` | Проверка пагинации KB работает с kb/processed | T-05 | 7 / 2 |
| `site/app.js` | — | — | `current` | Код сайта Этапа 1 (GitHub Pages) | — | 16 / 8 |
| `site/data/bcreq-flow.json` | — | — | `generated` | Генерирует scripts/generate-pages-data.mjs (github-pages.yml) | — | 4 / 1 |
| `site/data/checks.json` | — | — | `generated` | Генерирует scripts/generate-pages-data.mjs (github-pages.yml) | — | 8 / 3 |
| `site/data/patterns.json` | — | — | `generated` | Генерирует scripts/generate-pages-data.mjs (github-pages.yml) | — | 6 / 2 |
| `site/data/process-tree.json` | — | — | `generated` | Генерирует scripts/generate-pages-data.mjs (github-pages.yml) | — | 9 / 2 |
| `site/data/processes.json` | — | — | `generated` | Генерирует scripts/generate-pages-data.mjs (github-pages.yml) | — | 6 / 2 |
| `site/data/prompts.json` | — | — | `generated` | Генерирует scripts/generate-pages-data.mjs (github-pages.yml) | — | 17 / 8 |
| `site/data/roadmap.json` | — | — | `generated` | Генерирует scripts/generate-pages-data.mjs (github-pages.yml) | — | 5 / 2 |
| `site/data/stats.json` | — | — | `generated` | Генерирует scripts/generate-pages-data.mjs (github-pages.yml) | — | 5 / 2 |
| `site/favicon.svg` | — | — | `current` | Код сайта Этапа 1 (GitHub Pages) | — | 1 / 0 |
| `site/gate.js` | — | — | `current` | Код сайта Этапа 1 (GitHub Pages) | — | 8 / 3 |
| `site/index.html` | — | — | `current` | Код сайта Этапа 1 (GitHub Pages) | — | 18 / 9 |
| `site/login.css` | — | — | `current` | Код сайта Этапа 1 (GitHub Pages) | — | 2 / 0 |
| `site/login.html` | — | — | `current` | Код сайта Этапа 1 (GitHub Pages) | — | 3 / 1 |
| `site/password-hashes.json` | — | — | `generated` | Генерирует scripts/set-site-password.mjs (issue #388) | — | 12 / 3 |
| `site/reports/index.html` | — | — | `generated` | Статический отчётный сайт issue #335 (experiments/issue_335_build_report_site.py) | — | 4 / 1 |
| `site/reports/run-0060/detailed-gap-report.html` | — | — | `generated` | Статический отчётный сайт issue #335 (experiments/issue_335_build_report_site.py) | — | 3 / 1 |
| `site/reports/run-0060/diagrams/diagram-00.svg` | — | — | `generated` | Статический отчётный сайт issue #335 (experiments/issue_335_build_report_site.py) | — | 1 / 0 |
| `site/reports/run-0060/diagrams/diagram-01.svg` | — | — | `generated` | Статический отчётный сайт issue #335 (experiments/issue_335_build_report_site.py) | — | 1 / 0 |
| `site/reports/run-0060/diagrams/diagram-02.svg` | — | — | `generated` | Статический отчётный сайт issue #335 (experiments/issue_335_build_report_site.py) | — | 1 / 0 |
| `site/reports/run-0060/diagrams/diagram-03.svg` | — | — | `generated` | Статический отчётный сайт issue #335 (experiments/issue_335_build_report_site.py) | — | 1 / 0 |
| `site/reports/run-0060/diagrams/diagram-04.svg` | — | — | `generated` | Статический отчётный сайт issue #335 (experiments/issue_335_build_report_site.py) | — | 1 / 0 |
| `site/reports/run-0060/diagrams/diagram-05.svg` | — | — | `generated` | Статический отчётный сайт issue #335 (experiments/issue_335_build_report_site.py) | — | 1 / 0 |
| `site/reports/run-0060/diagrams/diagram-06.svg` | — | — | `generated` | Статический отчётный сайт issue #335 (experiments/issue_335_build_report_site.py) | — | 1 / 0 |
| `site/reports/run-0060/diagrams/diagram-07.svg` | — | — | `generated` | Статический отчётный сайт issue #335 (experiments/issue_335_build_report_site.py) | — | 1 / 0 |
| `site/reports/run-0060/diagrams/diagram-08.svg` | — | — | `generated` | Статический отчётный сайт issue #335 (experiments/issue_335_build_report_site.py) | — | 1 / 0 |
| `site/reports/run-0060/diagrams/diagram-09.svg` | — | — | `generated` | Статический отчётный сайт issue #335 (experiments/issue_335_build_report_site.py) | — | 1 / 0 |
| `site/reports/run-0060/diagrams/diagram-10.svg` | — | — | `generated` | Статический отчётный сайт issue #335 (experiments/issue_335_build_report_site.py) | — | 1 / 0 |
| `site/reports/run-0060/index.html` | — | — | `generated` | Статический отчётный сайт issue #335 (experiments/issue_335_build_report_site.py) | — | 3 / 1 |
| `site/screenshots/issue-395/after-criteria.png` | — | — | `historical` | Скриншоты приёмки сайта; свидетельство PR | — | 1 / 0 |
| `site/screenshots/issue-395/after-dark.png` | — | — | `historical` | Скриншоты приёмки сайта; свидетельство PR | — | 1 / 0 |
| `site/screenshots/issue-395/after-desktop.png` | — | — | `historical` | Скриншоты приёмки сайта; свидетельство PR | — | 1 / 0 |
| `site/screenshots/issue-395/after-full.png` | — | — | `historical` | Скриншоты приёмки сайта; свидетельство PR | — | 1 / 0 |
| `site/screenshots/issue-395/after-mobile.png` | — | — | `historical` | Скриншоты приёмки сайта; свидетельство PR | — | 1 / 0 |
| `site/screenshots/issue-395/before.png` | — | — | `historical` | Скриншоты приёмки сайта; свидетельство PR | — | 1 / 0 |
| `site/standards.css` | — | — | `current` | Код сайта Этапа 1 (GitHub Pages) | — | 2 / 0 |
| `site/styles.css` | — | — | `current` | Код сайта Этапа 1 (GitHub Pages) | — | 7 / 3 |
| `standards/GLOSSARY.md` | accepted | 2026-08-17 | `current` | Локальный стандарт (accepted) | — | 36 / 1 |
| `standards/README.md` | draft | 2026-10-23 | `update` | Перечень стандартов: отметить исторические стандарты 2026-06 после T-04/T-05 | T-07 | 14 / 1 |
| `standards/analysis-standard.md` | draft | 2026-07-17 | `current` | Локальный стандарт (draft) | — | 13 / 4 |
| `standards/artifact-naming-standard.md` | draft | 2026-06-16 | `current` | Локальный стандарт (draft) | — | 10 / 1 |
| `standards/ba-ontology.executable.md` | draft | 2026-06-20 | `current` | Локальный стандарт (draft) | — | 7 / 1 |
| `standards/ba-ontology.md` | draft | 2026-06-16 | `current` | Локальный стандарт (draft) | — | 20 / 2 |
| `standards/bcreq-composition-standard.md` | draft | 2026-10-23 | `current` | Стандарт BCREQ (#387, #395, #403) | — | 21 / 0 |
| `standards/bcreq-manual-classes/01-intake.md` | draft | 2026-10-29 | `current` | Стандарт BCREQ (#387, #395, #403) | — | 3 / 0 |
| `standards/bcreq-manual-classes/02-normalize.md` | draft | 2026-10-29 | `current` | Стандарт BCREQ (#387, #395, #403) | — | 3 / 0 |
| `standards/bcreq-manual-classes/03-ambiguity.md` | draft | 2026-10-29 | `current` | Стандарт BCREQ (#387, #395, #403) | — | 3 / 0 |
| `standards/bcreq-manual-classes/04-questions.md` | draft | 2026-10-29 | `current` | Стандарт BCREQ (#387, #395, #403) | — | 3 / 0 |
| `standards/bcreq-manual-classes/05-taxonomy.md` | draft | 2026-10-29 | `current` | Стандарт BCREQ (#387, #395, #403) | — | 3 / 0 |
| `standards/bcreq-manual-classes/06-scope.md` | draft | 2026-10-29 | `current` | Стандарт BCREQ (#387, #395, #403) | — | 3 / 0 |
| `standards/bcreq-manual-classes/07-web-evidence.md` | draft | 2026-10-29 | `current` | Стандарт BCREQ (#387, #395, #403) | — | 3 / 0 |
| `standards/bcreq-manual-classes/08-document-evidence.md` | draft | 2026-10-29 | `current` | Стандарт BCREQ (#387, #395, #403) | — | 3 / 0 |
| `standards/bcreq-manual-classes/09-ba-enrichment.md` | draft | 2026-10-29 | `current` | Стандарт BCREQ (#387, #395, #403) | — | 3 / 0 |
| `standards/bcreq-manual-classes/10-source-conflicts.md` | draft | 2026-10-29 | `current` | Стандарт BCREQ (#387, #395, #403) | — | 3 / 0 |
| `standards/bcreq-manual-classes/11-dependency-check.md` | draft | 2026-10-29 | `current` | Стандарт BCREQ (#387, #395, #403) | — | 3 / 0 |
| `standards/bcreq-manual-classes/12-phase-assembly.md` | draft | 2026-10-29 | `current` | Стандарт BCREQ (#387, #395, #403) | — | 3 / 0 |
| `standards/bcreq-manual-classes/13-handoff-check.md` | draft | 2026-10-29 | `current` | Стандарт BCREQ (#387, #395, #403) | — | 3 / 0 |
| `standards/bcreq-manual-classes/14-glossary.md` | draft | 2026-10-29 | `current` | Стандарт BCREQ (#387, #395, #403) | — | 3 / 0 |
| `standards/bcreq-manual-classes/15-business-context.md` | draft | 2026-10-29 | `current` | Стандарт BCREQ (#387, #395, #403) | — | 3 / 0 |
| `standards/bcreq-manual-classes/16-fr-delta.md` | draft | 2026-10-29 | `current` | Стандарт BCREQ (#387, #395, #403) | — | 3 / 0 |
| `standards/bcreq-manual-classes/17-fr-new.md` | draft | 2026-10-29 | `current` | Стандарт BCREQ (#387, #395, #403) | — | 3 / 0 |
| `standards/bcreq-manual-classes/18-nfr.md` | draft | 2026-10-29 | `current` | Стандарт BCREQ (#387, #395, #403) | — | 3 / 0 |
| `standards/bcreq-manual-classes/19-uc-coverage.md` | draft | 2026-10-29 | `current` | Стандарт BCREQ (#387, #395, #403) | — | 3 / 0 |
| `standards/bcreq-manual-classes/20-gate-evidence.md` | draft | 2026-10-29 | `current` | Стандарт BCREQ (#387, #395, #403) | — | 3 / 0 |
| `standards/bcreq-manual-classes/21-solution-l1.md` | draft | 2026-10-29 | `current` | Стандарт BCREQ (#387, #395, #403) | — | 3 / 0 |
| `standards/bcreq-manual-classes/22-solution-l2.md` | draft | 2026-10-29 | `current` | Стандарт BCREQ (#387, #395, #403) | — | 3 / 0 |
| `standards/bcreq-manual-classes/23-constraints.md` | draft | 2026-10-29 | `current` | Стандарт BCREQ (#387, #395, #403) | — | 3 / 0 |
| `standards/bcreq-manual-classes/24-uc-boundaries.md` | draft | 2026-10-29 | `current` | Стандарт BCREQ (#387, #395, #403) | — | 3 / 0 |
| `standards/bcreq-manual-classes/25-risks.md` | draft | 2026-10-29 | `current` | Стандарт BCREQ (#387, #395, #403) | — | 3 / 0 |
| `standards/bcreq-manual-classes/26-delivery-dependencies.md` | draft | 2026-10-29 | `current` | Стандарт BCREQ (#387, #395, #403) | — | 3 / 0 |
| `standards/bcreq-manual-classes/27-acceptance.md` | draft | 2026-10-29 | `current` | Стандарт BCREQ (#387, #395, #403) | — | 3 / 0 |
| `standards/bcreq-manual-classes/28-independent-review.md` | draft | 2026-10-29 | `current` | Стандарт BCREQ (#387, #395, #403) | — | 3 / 0 |
| `standards/bcreq-manual-classes/29-impact.md` | draft | 2026-10-29 | `current` | Стандарт BCREQ (#387, #395, #403) | — | 3 / 0 |
| `standards/bcreq-manual-classes/30-targeted-edit.md` | draft | 2026-10-29 | `current` | Стандарт BCREQ (#387, #395, #403) | — | 3 / 0 |
| `standards/bcreq-manual-classes/31-conformance.md` | draft | 2026-10-29 | `current` | Стандарт BCREQ (#387, #395, #403) | — | 3 / 0 |
| `standards/bcreq-manual-classes/32-audience-projection.md` | draft | 2026-10-29 | `current` | Стандарт BCREQ (#387, #395, #403) | — | 3 / 0 |
| `standards/bcreq-manual-classes/33-release-audit.md` | draft | 2026-10-29 | `current` | Стандарт BCREQ (#387, #395, #403) | — | 3 / 0 |
| `standards/bcreq-manual-classes/34-human-record.md` | draft | 2026-10-29 | `current` | Стандарт BCREQ (#387, #395, #403) | — | 3 / 0 |
| `standards/bcreq-manual-classes/35-baseline-handover.md` | draft | 2026-10-29 | `current` | Стандарт BCREQ (#387, #395, #403) | — | 3 / 0 |
| `standards/bcreq-manual-classes/36-rule-bundle.md` | draft | 2026-10-29 | `current` | Стандарт BCREQ (#387, #395, #403) | — | 4 / 0 |
| `standards/bcreq-manual-classes/37-user-story.md` | draft | 2026-10-29 | `current` | Стандарт BCREQ (#387, #395, #403) | — | 3 / 0 |
| `standards/bcreq-manual-classes/38-requested-uc.md` | draft | 2026-10-29 | `current` | Стандарт BCREQ (#387, #395, #403) | — | 3 / 0 |
| `standards/bcreq-manual-classes/39-manifest-alignment.md` | draft | 2026-10-29 | `current` | Стандарт BCREQ (#387, #395, #403) | — | 3 / 0 |
| `standards/bcreq-manual-classes/README.md` | draft | 2026-10-29 | `current` | Стандарт BCREQ (#387, #395, #403) | — | 9 / 0 |
| `standards/bcreq-manual-classes/catalog.json` | — | — | `current` | Стандарт BCREQ (#387, #395, #403) | — | 7 / 1 |
| `standards/bcreq-process-standard.md` | draft | 2026-06-16 | `current` | Стандарт BCREQ (#387, #395, #403) | — | 17 / 1 |
| `standards/bcreq-prompt-architecture.md` | draft | 2026-10-23 | `current` | Стандарт BCREQ (#387, #395, #403) | — | 17 / 0 |
| `standards/bcreq-sections/01-glossary.md` | draft | 2026-10-23 | `current` | Стандарт BCREQ (#387, #395, #403) | — | 11 / 0 |
| `standards/bcreq-sections/02-business-context.md` | draft | 2026-10-23 | `current` | Стандарт BCREQ (#387, #395, #403) | — | 10 / 0 |
| `standards/bcreq-sections/03-functional-requirements.md` | draft | 2026-10-23 | `current` | Стандарт BCREQ (#387, #395, #403) | — | 9 / 0 |
| `standards/bcreq-sections/04-non-functional-requirements.md` | draft | 2026-10-23 | `current` | Стандарт BCREQ (#387, #395, #403) | — | 9 / 0 |
| `standards/bcreq-sections/05-solution-description.md` | draft | 2026-10-23 | `current` | Стандарт BCREQ (#387, #395, #403) | — | 7 / 0 |
| `standards/bcreq-sections/06-implementation-constraints.md` | draft | 2026-10-23 | `current` | Стандарт BCREQ (#387, #395, #403) | — | 9 / 0 |
| `standards/bcreq-sections/07-use-cases.md` | draft | 2026-10-23 | `current` | Стандарт BCREQ (#387, #395, #403) | — | 10 / 0 |
| `standards/bcreq-sections/08-supplementary.md` | draft | 2026-10-23 | `current` | Стандарт BCREQ (#387, #395, #403) | — | 8 / 0 |
| `standards/bcreq-sections/README.md` | draft | 2026-10-23 | `current` | Стандарт BCREQ (#387, #395, #403) | — | 27 / 0 |
| `standards/cascading-context-loading-standard.md` | draft | 2026-08-21 | `current` | Локальный стандарт (draft) | — | 17 / 4 |
| `standards/evals-contract-standard.md` | draft | 2026-07-17 | `current` | Локальный стандарт (draft) | — | 15 / 1 |
| `standards/experiment-log-standard.md` | draft | 2026-06-16 | `current` | Локальный стандарт (draft) | — | 13 / 1 |
| `standards/industry-standards-standard.md` | draft | 2026-10-23 | `current` | Локальный стандарт (draft) | — | 13 / 1 |
| `standards/kb-standard.md` | draft | 2026-06-16 | `update` | Стандарт KB описывает локальный kb/processed, который перенесён в mango-ba-ai-runtime | T-05 | 17 / 2 |
| `standards/pages-ux-standard.md` | draft | 2026-06-16 | `update` | UX сайта 2026-06 (дерево процессов); сайт стал BCREQ-only (#391) | T-03 | 7 / 1 |
| `standards/pattern-standard.md` | draft | 2026-06-11 | `update` | Паттерны 2026-06 до BCREQ; синхронно с T-04 | T-04 | 18 / 1 |
| `standards/product-classification-contract.md` | draft | 2026-06-04 | `update` | Контракт 2026-06-04; сверить с таксономией #399 и ADR-013 | T-04 | 30 / 0 |
| `standards/prompt-debugging-process.md` | draft | 2026-06-16 | `current` | Локальный стандарт (draft) | — | 12 / 0 |
| `standards/prompt-standard.md` | draft | 2026-06-11 | `current` | Локальный стандарт (draft) | — | 27 / 1 |
| `standards/research-standard.md` | draft | 2026-07-17 | `current` | Локальный стандарт (draft) | — | 11 / 1 |
| `standards/runs-contract-standard.md` | draft | 2026-08-21 | `current` | Локальный стандарт (draft) | — | 24 / 3 |
| `standards/team-directory.md` | draft | 2026-06-16 | `update` | Справочник команд 2026-06; сверить с portal-маппингом ADR-013 | T-04 | 12 / 1 |
| `tools/README.md` | canonical | 2026-08-22 | `current` | Валидаторы Хаба и локальная дельта | — | 13 / 3 |
| `tools/file-naming-legacy-allowlist.txt` | — | — | `current` | Валидаторы Хаба и локальная дельта | — | 6 / 2 |
| `tools/validate-file-naming.sh` | — | — | `current` | Валидаторы Хаба и локальная дельта | — | 14 / 4 |
| `tools/validate-frontmatter.sh` | — | — | `current` | Валидаторы Хаба и локальная дельта | — | 17 / 4 |
| `tools/validate-repository-structure.sh` | — | — | `current` | Валидаторы Хаба и локальная дельта | — | 19 / 3 |
