---
status: draft
version: 0.1
updated: 2026-06-16
ai-generated: true
type: register
scope: governance
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/101"
related_artifacts:
  - "governance/rfc-process.md"
  - "governance/prompt-debugging-process.md"
  - "governance/sync-matrix-2026-06-17.md"
  - "docs/analysis/experiment-1027-analysis.md"
  - "governance/audit-contracts-2026-06-17.md"
---

# Реестр RFC (живой документ)

> **Что это.** Единый список предложений изменить промпты или governance-контракты.
> Каждый RFC движется по статусам и **не удаляется** из реестра (rejected остаётся
> с причиной). Общий процесс — в [`governance/rfc-process.md`](rfc-process.md)
> (интеграция жизненного цикла знаний Хаба); детализация для промптов — в
> [`governance/prompt-debugging-process.md`](prompt-debugging-process.md).

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
[`docs/analysis/experiment-1027-analysis.md`](../docs/analysis/experiment-1027-analysis.md).
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
([`sync-matrix-2026-06-17.md`](sync-matrix-2026-06-17.md)). Контракты спока в
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

## Журнал изменений реестра

- **2026-06-16** — реестр создан; внесены RFC-1027-P1…P5 (промпты) и
  RFC-GOV-D4…D6 (контракты) в статусе `proposed` по итогам issue #101 / PR #102.
- **2026-06-17** — добавлены RFC-SYNC-004…IW (сверка с Хабом) и RFC-HUB-001/002
  (передача знаний в Хаб) в статусе `proposed` по итогам issue #105 (синхронизация
  контрактов с Хабом). Реестр привязан к общему [`rfc-process.md`](rfc-process.md).
