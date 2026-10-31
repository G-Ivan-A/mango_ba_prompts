---
status: draft
version: 0.7
updated: 2026-10-31
ai-generated: true
type: register
scope: governance
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/101"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/107"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/109"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/387"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/409"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/413"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/411"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/415"
related_artifacts:
  - "docs/rfc/rfc-process.md"
  - "standards/prompt-debugging-process.md"
  - "pr-ops/sync-matrix-2026-06-17.md"
  - "docs/analysis/experiment-1027-analysis.md"
  - "docs/audit/audit-contracts-2026-06-17.md"
  - "runs/2026/RUN-0010/outputs/analysis-bcreq-1025-2026-06-17.md"
  - "docs/rfc/prompt-improvement-bcreq-1025-proposal.md"
  - "docs/rfc/prompt-improvement-multichannel-proposal.md"
  - "docs/rfc/2026-10-bcreq-meta-standards-rfc.md"
  - "docs/rfc/2026-10-repository-modernization.md"
  - "docs/rfc/2026-10-bcreq-run-lessons-pipeline.md"
  - "docs/rfc/2026-10-ba-automation-strategy.md"
---

# Реестр RFC (живой документ)

> **Что это.** Единый список предложений изменить промпты или governance-контракты.
> Каждый RFC движется по статусам и **не удаляется** из реестра (rejected остаётся
> с причиной). Общий процесс — в [`docs/rfc/rfc-process.md`](rfc-process.md)
> (интеграция жизненного цикла знаний Хаба); детализация для промптов — в
> [`standards/prompt-debugging-process.md`](../../standards/prompt-debugging-process.md).

## Статусы

```
proposed → in-review → accepted  → implemented
                     ↘ rejected
```

| Статус | Значение | Кто переводит |
| --- | --- | --- |
| `proposed` | оформлен, ждёт рассмотрения | автор RFC |
| `in-review` | рассматривается пользователем | пользователь |
| `accepted` | принят к реализации | **только пользователь** |
| `rejected` | отклонён (с причиной) | **только пользователь** |
| `implemented` | внесён, связан с PR | исполнитель после merge |

## Открытые RFC по промптам (источник: эксперимент 1027, issue #101)

Все правки ниже — **предложения** из разбора
[`docs/analysis/experiment-1027-analysis.md`](../analysis/experiment-1027-analysis.md).
Промпты в PR #102 **не изменены** (остаются v0.1); записи ждут инициативы
пользователя (часть 3 процесса).

| RFC | Промпт(ы) | Суть предложения | Источник-сигнал | Тип версии | Статус | PR реализации |
| --- | --- | --- | --- | --- | --- | --- |
| RFC-1027-P1 | `glossary-context-understanding-stepwise.md`, `…-oneshot.md` | Явный запрос документации/БЗ + правило «документация = верификация As-Is, не источник скоупа» (H1) | анализ 1027 §H1; прогон 1027 | Minor | `proposed` | — |
| RFC-1027-P2 | `fr-documentation-stepwise.md`, `…-oneshot.md` | Читаемость 4.x.1 (анти-канцелярит с примером), явный субъект 4.x, явная реконструкция US/UC (H2 + позитив) | анализ 1027 §H2 | Minor | `proposed` | — |
| RFC-1027-P3 | `constraints-documentation-oneshot.md` | Канонический текст 6.1.1–6.1.3 (как в stepwise) (H3) | анализ 1027 §H3 | Minor | `proposed` | — |
| RFC-1027-P4 | `constraints-documentation-oneshot.md`, `…-stepwise.md` | Фильтр против ограничений, описывающих текущее поведение или дублирующих ФТ; смягчение квоты «4-6» (H4) | анализ 1027 §H4 | Minor | `proposed` | — |
| RFC-1027-P5 | `fr-documentation-stepwise.md` | Сверка каждого ФТ с фактами As-Is/документацией в Шаге 4 (доп. находка) | анализ 1027 §доп. находка | Minor | `proposed` | — |

## Открытые RFC по контрактам (источник: аудит контрактов 2026-06-17)

Правки в сами governance-контракты тоже идут через RFC — тот же порядок, что и
для промптов.

| RFC | Документ | Суть предложения | Источник-сигнал | Статус | PR реализации |
| --- | --- | --- | --- | --- | --- |
| RFC-GOV-D4 | `AI_GOVERNANCE.md` | В Capability Boundaries уточнить, что изменение существующего промпта идёт через процесс отладки (ссылка) | аудит контрактов §Д4 | `proposed` | — |
| RFC-GOV-D5 | `CONTRIBUTING.md` | Дополнить «Временный workflow промптов» разделом про изменение существующих (не только создание) | аудит контрактов §Д5 | `proposed` | — |
| RFC-GOV-D6 | `standards/experiment-log-standard.md` | Добавить оговорку «эксперимент ≠ право на правку без RFC» | аудит контрактов §Д6 | `proposed` | — |

## Открытые RFC синхронизации с Хабом (источник: issue #105, sync-matrix 2026-06-17)

Предложения сверить контракты спока с Хабом
([`sync-matrix-2026-06-17.md`](../../pr-ops/sync-matrix-2026-06-17.md)). Контракты спока в
PR #105 **не изменены** — сверка и правка идут только после решения пользователя.

| RFC | Контракт Mango | С чем сверять (Хаб, snapshot 6ddffdf) | Суть предложения | Статус | PR реализации |
| --- | --- | --- | --- | --- | --- |
| RFC-SYNC-004 | ADR #004 (таксономия операций) | PR #246 `methodology-research-and-proposals.md` | согласовать набор 13 операций ↔ Knowledge Areas BABOK Хаба | `proposed` | — |
| RFC-SYNC-005 | ADR #005 (нейминг) | `standards/file-naming.md` | совместить нейминг файлов-стандартов с правилом Хаба | `proposed` | — |
| RFC-SYNC-007 | ADR #007 (БЗ) | PR #242 `research-memory-source-intelligence.md` | ввести модель Knowledge Object (Tier 2) поверх формата цитирования | `proposed` | — |
| RFC-SYNC-008 | ADR #008 (отраслевые) | `external-knowledge-integration.md` | согласовать tier-модель и Base Registry / Local Extension | `proposed` | — |
| RFC-SYNC-PR | `standards/prompt-standard.md` | `executable-contract-standard.md` | маркировка `executable: true` для исполнимых промптов | `proposed` | — |
| RFC-SYNC-PT | `standards/pattern-standard.md` | `executable-documentation-standard.md` | атомизация практик (graph-of-practices) | `proposed` | — |
| RFC-SYNC-IW | issue-процесс | `standards/issue-workflow.md` | принять ли 7 статусов задач Хаба | `proposed` | — |

## Открытые RFC передачи знаний в Хаб (источник: issue #105, ФТ-5)

Уникальные практики Mango (нет аналогов в Хабе) — предложения к переносу по
обратному потоку спок → Хаб. Документы передачи — в
[`knowledge-transfer-to-hub/`](knowledge-transfer-to-hub/).

| RFC | Практика Mango | Документ / RFC в Хаб | Статус | Реализация |
| --- | --- | --- | --- | --- |
| RFC-HUB-001 | Онтология БА (#003), таксономия (#004), BCREQ (#009), Pages UX (#010) | [`rfc-to-hub-001-knowledge-transfer.md`](rfc-to-hub-001-knowledge-transfer.md) | `proposed` | — |
| RFC-HUB-002 | Процесс отладки промптов | [`rfc-to-hub-002-prompt-debugging-process.md`](rfc-to-hub-002-prompt-debugging-process.md) | `proposed` | — |

## Открытые RFC по промптам (источник: эксперимент BCREQ-1025, issue #107)

Правки ниже — **предложения** из разбора
[`runs/2026/RUN-0010/outputs/analysis-bcreq-1025-2026-06-17.md`](../../runs/2026/RUN-0010/outputs/analysis-bcreq-1025-2026-06-17.md).
Промпты **не изменены** (остаются v0.1); записи ждут инициативы пользователя.
Полный RFC: [`docs/rfc/prompt-improvement-bcreq-1025-proposal.md`](prompt-improvement-bcreq-1025-proposal.md).

| RFC | Промпт(ы) | Суть предложения | Источник-сигнал | Тип версии | Статус | PR реализации |
| --- | --- | --- | --- | --- | --- | --- |
| RFC-1025-P1 | `glossary-context-understanding-stepwise.md` | Явный запрос архитектурных компонентов/связок на Шаге 0 (паттерн Б5). **#413:** фиксированная пара продуктов не отражает 7 доменов и 43 Capability таксономии; обобщить до паттерна «слой настройки и слой исполнения по каждой затронутой Capability» (C05), передано в [#411](https://github.com/G-Ivan-A/mango_ba_prompts/issues/411) | анализ BCREQ-1025 §2.2 Б5 | Minor | `proposed` | — |
| RFC-1025-P2 | `fr-documentation-stepwise.md` | Явная матрица ролей + фиксация архитектурных границ в суммаризации Шага 1 (паттерны Б1+Б4) | анализ BCREQ-1025 §2.2 Б4, §2.3 Б1 | Minor | `proposed` | — |
| RFC-1025-P3 | `fr-documentation-stepwise.md` | Пример-эталон стиля 4.x.1 (анти-канцелярит); усиление RFC-1027-P2 (паттерн Б3) | анализ BCREQ-1025 §2.1 Б3 | Minor | `proposed` | — |
| RFC-1025-P4 | `fr-documentation-stepwise.md` | Явный запрет на 4-й уровень иерархии + правило раскладки многоусловных требований (паттерн Б2) | анализ BCREQ-1025 §2.1 Б2 | Minor | `proposed` | — |
| RFC-1025-P5 | `constraints-documentation-stepwise.md` | Явный запрос архитектурных связок и границ между компонентами на Шаге 1 (паттерн Б5) | анализ BCREQ-1025 §2.2 Б5 | Minor | `proposed` | — |

## Открытые RFC по промптам (источник: эксперимент «Многоканальная нагрузка агента», issue #109)

Правки ниже — **предложения** из разбора
[`runs/2026/RUN-0011/logs/experiment-log.md`](../../runs/2026/RUN-0011/logs/experiment-log.md).
Промпты **не изменены** (остаются v0.1); записи ждут инициативы пользователя.
Полный RFC: [`docs/rfc/prompt-improvement-multichannel-proposal.md`](prompt-improvement-multichannel-proposal.md).

| RFC | Промпт(ы) | Суть предложения | Источник-сигнал | Тип версии | Статус | PR реализации |
| --- | --- | --- | --- | --- | --- | --- |
| RFC-MCH-P1 | `glossary-context-understanding-stepwise.md` | Явная фиксация архитектурного слоя (ЛК ВАТС vs КЦ) в ШАГ 0 (повтор Б1/Б5). **#413:** фиксированная пара продуктов не отражает 7 доменов и 43 Capability таксономии; обобщить до паттерна «слой настройки и слой исполнения по каждой затронутой Capability» (C05), передано в [#411](https://github.com/G-Ivan-A/mango_ba_prompts/issues/411) | эксперимент #109 §М1 | Minor | `proposed` | — |
| RFC-MCH-P2 | цепочка `understanding` (glossary↔questions) | Под-шаг/промпт «нормализация требования» (атомы + боль/решение + первичный gap) | эксперимент #109 §М2 | Minor | `proposed` | — |
| RFC-MCH-P3 | `technical-details-solution-design-stepwise.md` (+ новый `options-*`) | Отдельный промпт «early-options» (варианты доработки, Раздел 3) отдельно от Раздела 7 | эксперимент #109 §М3 | Major | `proposed` | — |

## Инициированные изменения мета-стандартов BCREQ (источник: issue #387)

Изменения применены в новых draft-артефактах PR #389 (карт-бланш Creative-режима
issue #387). Существующие стандарты и контракты **не изменены**: правки к ним ждут
решения пользователя. Путь отката каждого RFC — в RFC-документе
[`2026-10-bcreq-meta-standards-rfc.md`](2026-10-bcreq-meta-standards-rfc.md).

| RFC | Документ | Суть предложения | Источник-сигнал | Статус | PR реализации |
| --- | --- | --- | --- | --- | --- |
| [RFC-387-01](2026-10-bcreq-meta-standards-rfc.md#rfc-387-01) | `standards/prompt-standard.md` | Семантика режимов stepwise / oneshot; режимонезависимый промпт помечается `oneshot`; напоминание конституции в каждом промпте кроме Промпта 0 | issue #387, чат р. 796 (Ч-44…Ч-47) | `proposed` | — |
| [RFC-387-02](2026-10-bcreq-meta-standards-rfc.md#rfc-387-02) | структура 2.1–2.14 (предложение БА) | Пространство шагов `Ш-`, слияния файлов М1–М4, шаг Ш-В «валидация второй ролью» | аудит Задачи 1 Н7, Н8; чат р. 778 (Ч-35) | `proposed` | — |
| [RFC-387-03](2026-10-bcreq-meta-standards-rfc.md#rfc-387-03) | `docs/analysis/2026-10-20-bcreq-fr-section-prompts.md` (О8, О10) | Индустриальная практика — отдельным блоком «Рекомендация — на решение БА»; исключение О10 для 5 L2 | issue #387; чат р. 748, 796 (Ч-08, Ч-38) | `proposed` | — |
| [RFC-387-04](2026-10-bcreq-meta-standards-rfc.md#rfc-387-04) | `standards/bcreq-process-standard.md` | Ссылка на контракт стадий и гейтов; таблица «П1–П6 ↔ стадия» | чат р. 746 (Ч-01…Ч-03, Ч-51…Ч-53) | `proposed` | — |
| [RFC-387-05](2026-10-bcreq-meta-standards-rfc.md#rfc-387-05) | состав разделов 2 и 8 (issue #387) | Подразделы ＋2.5 «Продукты и стейкхолдеры», ＋8.4 «Реестр вопросов Заказчику», ＋8.5 «Журнал решений» | чат р. 746, 748 (Ч-08, Ч-55) | `proposed` | — |
| [RFC-387-06](2026-10-bcreq-meta-standards-rfc.md#rfc-387-06) | стили разделов (issue #387) | Раздел 4 — бюрократический стиль; короткий — 2, 5 L1, 6 (канон issue, расхождение с чатом) | чат р. 764 (Ч-29, Ч-30) | `proposed` | — |
| [RFC-387-07](2026-10-bcreq-meta-standards-rfc.md#rfc-387-07) | `docs/analysis/2026-10-20-bcreq-fr-section-prompts.md` (А2.4) | Ограничения платформы и версий — в 2.4.2 для новых задач; 6.2 — внешние ограничения решения | чат р. 760 (Ч-27) | `proposed` | — |

## Модернизация репозитория (источник: issue #409)

RFC [`2026-10-repository-modernization.md`](2026-10-repository-modernization.md)
v0.3 выносит на согласование десять решений. После решений владельца
изменения выполняются задачами T-01…T-09 из
[реестра задач](../analysis/2026-10-31-follow-up-tasks.md). В v0.4 (#413)
владелец принял DEC-05; DEC-02, DEC-05 и DEC-08 реализованы в PR #414.

| RFC | Документ | Суть предложения | Источник-сигнал | Статус | PR реализации |
| --- | --- | --- | --- | --- | --- |
| [RFC-409-DEC-01](2026-10-repository-modernization.md#dec-01-статус-репозитория-в-экосистеме-f-01-f-11) | Статус в экосистеме Хаба | Гибрид: спица — практика этапа 1 и сайт, `mango-ba-ai-runtime` — исполнение этапов 2–4 | [аудит #409](../audit/2026-10-31-repository-audit.md#реестр-находок) F-01, F-11 | `proposed` | — |
| [RFC-409-DEC-02](2026-10-repository-modernization.md#dec-02-замена-границ-263-f-03-f-14) | Границы #263, валидатор #263 | [ADR-017](../adr/2026-10-adr-017-four-stages-n8n-orchestration.md) заменяет границы #263; валидатор изменён в том же PR | [аудит #409](../audit/2026-10-31-repository-audit.md#реестр-находок) F-03, F-14 | `implemented` | [#414](https://github.com/G-Ivan-A/mango_ba_prompts/pull/414) |
| [RFC-409-DEC-03](2026-10-repository-modernization.md#dec-03-видимость-f-05) | Видимость репозитория | Public до решения по ADR-009 Хаба | [аудит #409](../audit/2026-10-31-repository-audit.md#реестр-находок) F-05 | `proposed` | — |
| [RFC-409-DEC-04](2026-10-repository-modernization.md#dec-04-роль-mango-ba-ai-runtime-f-04) | Роль runtime | Runtime — исполнение и KB; спица — практика и сайт | [аудит #409](../audit/2026-10-31-repository-audit.md#реестр-находок) F-04 | `proposed` | — |
| [RFC-409-DEC-05](2026-10-repository-modernization.md#dec-05-роль-n8n-на-этапе-3-f-07) | Этап 3 | n8n — оркестратор этапа 3; риски Хаба — требования к потокам ([ADR-017](../adr/2026-10-adr-017-four-stages-n8n-orchestration.md), решение владельца в #413) | [аудит #409](../audit/2026-10-31-repository-audit.md#реестр-находок) F-07 | `implemented` | [#414](https://github.com/G-Ivan-A/mango_ba_prompts/pull/414) |
| [RFC-409-DEC-06](2026-10-repository-modernization.md#dec-06-ssot-пакета-этапа-2-f-06) | ADR-016, пакет этапа 2 | Пакет Хаба — источник сборки, runtime — место установки, ADR-016 — профиль применения | [аудит #409](../audit/2026-10-31-repository-audit.md#реестр-находок) F-06 | `proposed` | — |
| [RFC-409-DEC-07](2026-10-repository-modernization.md#dec-07-архетип-и-среда-f-08) | `AGENTS.md`, `.hub-profile.json` | `archetype: B`, `environment: local` | [аудит #409](../audit/2026-10-31-repository-audit.md#реестр-находок) F-08 | `proposed` | — |
| [RFC-409-DEC-08](2026-10-repository-modernization.md#dec-08-размещение-четырёх-документов-f-02) | Четыре стратегических документа | `docs/vision.md`, `docs/concept.md`, `docs/architecture.md`, `docs/roadmap.md` (на сайте — после принятия DEC-11, отдельной задачей) | [аудит #409](../audit/2026-10-31-repository-audit.md#реестр-находок) F-02 | `implemented` | [#414](https://github.com/G-Ivan-A/mango_ba_prompts/pull/414) |
| [RFC-409-DEC-09](2026-10-repository-modernization.md#dec-09-политика-разметки-истории-f-10-f-16) | Разметка истории | Правило каталога и блок перехода; `.archive/` — только `superseded` с преемником | [аудит #409](../audit/2026-10-31-repository-audit.md#реестр-находок) F-10, F-16 | `proposed` | — |
| [RFC-409-DEC-10](2026-10-repository-modernization.md#dec-10-вывод-локального-kb-конвейера-f-12) | KB-конвейер | Депрекация после проверки потребителей; `kb/` остаётся на месте | [аудит #409](../audit/2026-10-31-repository-audit.md#реестр-находок) F-12 | `proposed` | — |
| [RFC-409-DEC-11](2026-10-repository-modernization.md#dec-11-структура-сайта-413) | Структура сайта | О проекте (видение, концепция, архитектура, roadmap), Каталог (только промпты), Стандарты (структура документа BCREQ), Процессы и Дашборд без изменений; правки сайта — отдельными задачами после принятия | указание владельца в PR #414 | `proposed` | — |

## Уроки прогонов в конвейере промптов (источник: issue #411)

RFC [`2026-10-bcreq-run-lessons-pipeline.md`](2026-10-bcreq-run-lessons-pipeline.md) v0.1 выносит на согласование двенадцать решений. Этап 1
(реестр уроков, генератор, golden set, рубрика, прогон RUN-0079) реализован в
PR #412; промпты, классы, сайт и процесс БА не изменены и меняются отдельными задачами после принятия RFC/ADR, по [ADR-017](../adr/2026-10-adr-017-run-lessons-ssot.md) и ждёт
утверждения DEC-411-01. Изменения замороженных контрактов (DEC-411-02,
-08, -10) не выполнены.

| RFC | Документ | Суть предложения | Источник-сигнал | Статус | PR реализации |
| --- | --- | --- | --- | --- | --- |
| [RFC-411-DEC-01](2026-10-bcreq-run-lessons-pipeline.md#dec-411-01-утвердить-adr-017-реестр-уроков--ssot) | ADR-017, `standards/bcreq-lessons/` | Реестр уроков — единственный источник правил «как делать и как не делать»; блоки промптов генерируются | [отчёт #411](../analysis/2026-10-31-bcreq-pipeline-run-experience-review.md) | `proposed` | PR #412 (реализация этапа 1) |
| [RFC-411-DEC-02](2026-10-bcreq-run-lessons-pipeline.md#dec-411-02-четыре-поля-контракта-прогона) | `standards/runs-contract-standard.md` | Поля `prompt_ref`, `lessons[]`, `golden_promotion`, `ba_reviewed` для новых прогонов | [отчёт #411](../analysis/2026-10-31-bcreq-pipeline-run-experience-review.md) | `proposed` | — |
| [RFC-411-DEC-03](2026-10-bcreq-run-lessons-pipeline.md#dec-411-03-единый-словарь-кодов-ошибок) | Реестры ошибок новых прогонов | Коды ошибок — ID уроков; локальные коды только с колонкой «урок» | [отчёт #411](../analysis/2026-10-31-bcreq-pipeline-run-experience-review.md) | `proposed` | — |
| [RFC-411-DEC-04](2026-10-bcreq-run-lessons-pipeline.md#dec-411-04-порог-приёмки-по-golden-set) | Рубрика этапа 1 | Порог: ядро 11 из 11; полный набор не ниже 90% по K1–K3; K5 без исключений | [отчёт #411](../analysis/2026-10-31-bcreq-pipeline-run-experience-review.md) | `proposed` | — |
| [RFC-411-DEC-05](2026-10-bcreq-run-lessons-pipeline.md#dec-411-05-урок-l-42-канонические-пункты-раздела-6) | Стандарт раздела 6 | Вернуть или отклонить канонические пункты раздела 6 | [отчёт #411](../analysis/2026-10-31-bcreq-pipeline-run-experience-review.md) | `proposed` | — |
| [RFC-411-DEC-06](2026-10-bcreq-run-lessons-pipeline.md#dec-411-06-бюджет-токенов-промптов-этапа-1) | `prompts/bcreq-*.md` | Полные блоки уроков на этапе 1; сокращение только по данным прогонов | [отчёт #411](../analysis/2026-10-31-bcreq-pipeline-run-experience-review.md) | `proposed` | — |
| [RFC-411-DEC-07](2026-10-bcreq-run-lessons-pipeline.md#dec-411-07-39-классов--цель-этапов-23) | `standards/bcreq-manual-classes/` | Общий шаблон в один файл, переименование ID классов, явные правила 17 ослабленных уроков | [отчёт #411](../analysis/2026-10-31-bcreq-pipeline-run-experience-review.md) | `proposed` | — |
| [RFC-411-DEC-08](2026-10-bcreq-run-lessons-pipeline.md#dec-411-08-восстановить-контракт-жизненного-цикла-эталонов) | Контракт эталонов | Восстановить утраченный контракт Golden Examples и сверить с контрактом evals | [отчёт #411](../analysis/2026-10-31-bcreq-pipeline-run-experience-review.md) | `proposed` | — |
| [RFC-411-DEC-09](2026-10-bcreq-run-lessons-pipeline.md#dec-411-09-правило-сессии-п-9-и-его-проверка) | Клиент этапа 2 | Клиент сам подставляет правила сессии из 8.5 в каждый запрос | [отчёт #411](../analysis/2026-10-31-bcreq-pipeline-run-experience-review.md) | `proposed` | — |
| [RFC-411-DEC-10](2026-10-bcreq-run-lessons-pipeline.md#dec-411-10-навигация-readme-промптов-и-стандартов) | `prompts/README.md`, `standards/README.md` | Ссылки на реестр уроков при обновлении базового снимка | [отчёт #411](../analysis/2026-10-31-bcreq-pipeline-run-experience-review.md) | `proposed` | — |
| [RFC-411-DEC-11](2026-10-bcreq-run-lessons-pipeline.md#dec-411-11-поправки-к-rfc-модернизации-репозитория) | RFC модернизации | Цикл качества промптов в критериях выхода этапов, исправления путей и DoD | [отчёт #411](../analysis/2026-10-31-bcreq-pipeline-run-experience-review.md) | `proposed` | — |
| [RFC-411-DEC-12](2026-10-bcreq-run-lessons-pipeline.md#dec-411-12-метаданные-adr-015) | ADR-015 | Исправить `decision-type` | [отчёт #411](../analysis/2026-10-31-bcreq-pipeline-run-experience-review.md) | `proposed` | — |

## Стратегия автоматизации БА команды крупных клиентов (источник: issue #415)

RFC [`2026-10-ba-automation-strategy.md`](2026-10-ba-automation-strategy.md) v0.1 собирает видение, концепцию, архитектуру и
дорожную карту в одном документе для руководителей разработки и маркетинга
и выносит на согласование восемь решений. Канонические документы `docs/`
меняются отдельной задачей после принятия.

| RFC | Документ | Суть предложения | Источник-сигнал | Статус | PR реализации |
| --- | --- | --- | --- | --- | --- |
| [RFC-415-DEC-01](2026-10-ba-automation-strategy.md#dec-415-01) | Форма документа | RFC с четырьмя разделами; перенос в `docs/` отдельной задачей после принятия | [постановка #415](https://github.com/G-Ivan-A/mango_ba_prompts/issues/415) | `proposed` | — |
| [RFC-415-DEC-02](2026-10-ba-automation-strategy.md#dec-415-02) | Область этапов 1–4 | Команда БА крупных клиентов (КК); остальные команды — этап 5 | [постановка #415](https://github.com/G-Ivan-A/mango_ba_prompts/issues/415) | `proposed` | — |
| [RFC-415-DEC-03](2026-10-ba-automation-strategy.md#dec-415-03) | Этап 2 | Агентный клиент + оценка исполнимости ТЗ заказчика; RUN-0077 — пример, не эталон | [постановка #415](https://github.com/G-Ivan-A/mango_ba_prompts/issues/415) | `proposed` | — |
| [RFC-415-DEC-04](2026-10-ba-automation-strategy.md#dec-415-04) | Этап 5 | Масштабирование на продуктовые команды и аналитиков после ворот 3, параллельно этапу 4 | [постановка #415](https://github.com/G-Ivan-A/mango_ba_prompts/issues/415) | `proposed` | — |
| [RFC-415-DEC-05](2026-10-ba-automation-strategy.md#dec-415-05) | `docs/roadmap.md` | Stage-gate + Now/Next/Later + карточка «что — зачем — как — сколько»; оценки — гипотезы | [постановка #415](https://github.com/G-Ivan-A/mango_ba_prompts/issues/415) | `proposed` | — |
| [RFC-415-DEC-06](2026-10-ba-automation-strategy.md#dec-415-06) | `docs/vision.md` | Метрики для руководства с базовой линией этапа 1 | [постановка #415](https://github.com/G-Ivan-A/mango_ba_prompts/issues/415) | `proposed` | — |
| [RFC-415-DEC-07](2026-10-ba-automation-strategy.md#dec-415-07) | Агентный клиент этапа 2 | OpenCode — базовый кандидат; выбор квалификацией ADR-016 (CH-1) | [постановка #415](https://github.com/G-Ivan-A/mango_ba_prompts/issues/415) | `proposed` | — |
| [RFC-415-DEC-08](2026-10-ba-automation-strategy.md#dec-415-08) | Сайт, «О проекте» | Показ четырёх разделов после принятия DEC-11 | [постановка #415](https://github.com/G-Ivan-A/mango_ba_prompts/issues/415) | `proposed` | — |

## Журнал изменений реестра

- **2026-06-16** — реестр создан; внесены RFC-1027-P1…P5 (промпты) и
  RFC-GOV-D4…D6 (контракты) в статусе `proposed` по итогам issue #101 / PR #102.
- **2026-06-17** — добавлены RFC-SYNC-004…IW (сверка с Хабом) и RFC-HUB-001/002
  (передача знаний в Хаб) в статусе `proposed` по итогам issue #105 (синхронизация
  контрактов с Хабом). Реестр привязан к общему [`rfc-process.md`](rfc-process.md).
- **2026-06-17** — добавлены RFC-1025-P1…P5 (промпты) в статусе `proposed` по
  итогам эксперимента BCREQ-1025 (issue #107). Полный анализ —
  [`runs/2026/RUN-0010/outputs/analysis-bcreq-1025-2026-06-17.md`](../../runs/2026/RUN-0010/outputs/analysis-bcreq-1025-2026-06-17.md);
  RFC-документ — [`docs/rfc/prompt-improvement-bcreq-1025-proposal.md`](prompt-improvement-bcreq-1025-proposal.md).
- **2026-06-18** — добавлены RFC-MCH-P1…P3 (промпты) в статусе `proposed` по
  итогам эксперимента «Многоканальная нагрузка агента» (issue #109). RFC-документ —
  [`docs/rfc/prompt-improvement-multichannel-proposal.md`](prompt-improvement-multichannel-proposal.md).
  P1 — повтор паттернов Б1/Б5 из BCREQ-1025 (рекомендация объединить с RFC-1025-P1).
- **2026-10-23** — добавлены RFC-387-01…07 в статусе `proposed` по итогам issue #387
  (мета-стандарты разделов BCREQ, PR #389). RFC-документ —
  [`docs/rfc/2026-10-bcreq-meta-standards-rfc.md`](2026-10-bcreq-meta-standards-rfc.md);
  решение — [ADR-012](../adr/2026-10-adr-012-bcreq-meta-standards.md).
- **2026-10-31** — добавлены RFC-409-DEC-01…10 в статусе `proposed` по итогам
  аудита issue #409 (PR #410). RFC-документ —
  [`docs/rfc/2026-10-repository-modernization.md`](2026-10-repository-modernization.md) v0.3.
- **2026-10-31** — по решению владельца в issue #413 (PR #414): RFC модернизации
  v0.4; RFC-409-DEC-02, DEC-05 (n8n — оркестратор этапа 3,
  [ADR-017](../adr/2026-10-adr-017-four-stages-n8n-orchestration.md)) и DEC-08 →
  `implemented`. RFC-MCH-P1 и RFC-1025-P1 получили пометку #413: пара
  «ЛК ВАТС / КЦ» обобщается до паттерна по Domain→Capability и передана в
  трек промптов #411; статусы не изменены. Предложения следующего шага —
  [отчёт #413](../report/2026-10-31-repository-action-plan.md).
- **2026-10-31** — добавлены RFC-411-DEC-01…12 в статусе `proposed` по итогам
  issue #411 (PR #412). RFC-документ —
  [`docs/rfc/2026-10-bcreq-run-lessons-pipeline.md`](2026-10-bcreq-run-lessons-pipeline.md) v0.1; решение —
  [ADR-017](../adr/2026-10-adr-017-run-lessons-ssot.md).
- **2026-10-31** — добавлены RFC-415-DEC-01…08 в статусе `proposed` по итогам
  issue #415 (PR #416). RFC-документ —
  [`docs/rfc/2026-10-ba-automation-strategy.md`](2026-10-ba-automation-strategy.md) v0.1.
