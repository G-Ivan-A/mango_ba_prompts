---
status: draft
version: 0.1
updated: 2026-06-16
ai-generated: true
type: rfc
scope: strategic
target_repo: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab"
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/105"
related_artifacts:
  - "docs/rfc/knowledge-transfer-to-hub/README.md"
  - "docs/audit/audit-hub-2026-06-17.md"
  - "pr-ops/sync-matrix-2026-06-17.md"
  - "docs/rfc-hub-integration.md"
---

# RFC в Хаб 001: передача уникальных практик БА (онтология, таксономия, BCREQ, Pages UX)

> **Адресат: `hybrid-Intelligence-lab` (Хаб).** Это **предложение** спока
> `mango_ba_prompts` к Хабу по обратному потоку «спок → Хаб»
> ([`docs/rfc-hub-integration.md`](../rfc-hub-integration.md)). Это **ФТ-5**
> задачи [#105](https://github.com/G-Ivan-A/mango_ba_prompts/issues/105).
> Финальное решение — за пользователем по правилам Хаба
> (`AI_GOVERNANCE.md`, «финальные решения за человеком»). До утверждения практики
> остаются локальными контрактами Mango — этот RFC ничего не меняет ни в Хабе, ни
> в споке.

## 1. Проблема (зачем Хабу это)

Аудит Хаба ([`audit-hub-2026-06-17.md`](../audit/audit-hub-2026-06-17.md)) на снимке
[`6ddffdf`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/tree/6ddffdfff693d8279792cd1e9c4c5d94ee0dffcf)
показал: у Хаба есть жизненный цикл знаний, Research Memory и стандарты исполнимых
артефактов, но **нет доменной модели бизнес-анализа**. При этом Хаб поощряет
обратный поток зрелых практик из споков. У Mango есть 4 практики БА, которых в
Хабе нет (см. [`sync-matrix-2026-06-17.md`](../../pr-ops/sync-matrix-2026-06-17.md), действие
«Передача знаний →»).

## 2. Предложение

Рассмотреть к принятию в Хаб (как стандарты или practice nodes graph-of-practices)
4 уникальные практики БА Mango. Для каждой подготовлен документ передачи в
[`knowledge-transfer-to-hub/`](knowledge-transfer-to-hub/) (что/как/зачем,
обоснование, примеры, что обобщить):

| # | Практика | Документ передачи | Носитель в Mango |
| --- | --- | --- | --- |
| 1 | Онтология БА (Артефакт↔Процесс↔Операция) | [`ba-ontology.md`](knowledge-transfer-to-hub/ba-ontology.md) | [ADR #003](../adr/003-ba-ontology.md) |
| 2 | Таксономия 13 операций БА (BABOK/ISO-маппинг) | [`operations-taxonomy.md`](knowledge-transfer-to-hub/operations-taxonomy.md) | [ADR #004](../adr/004-operations-taxonomy.md) |
| 3 | Процесс формирования BCREQ (human gates) | [`bcreq-process.md`](knowledge-transfer-to-hub/bcreq-process.md) | [ADR #009](../adr/009-bcreq-formation-process.md) |
| 4 | UX дерева процессов GitHub Pages | [`pages-ux.md`](knowledge-transfer-to-hub/pages-ux.md) | [ADR #010](../adr/010-pages-ux.md) |

> Процесс отладки промптов — отдельный RFC
> [`rfc-to-hub-002-prompt-debugging-process.md`](rfc-to-hub-002-prompt-debugging-process.md)
> (это процесс, а не BA-контент).

## 3. Совместимость с контрактами Хаба

| Контракт Хаба (snapshot 6ddffdf) | Как соотносятся практики |
| --- | --- |
| [`knowledge-lifecycle-proposal.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/6ddffdfff693d8279792cd1e9c4c5d94ee0dffcf/governance/rfc/knowledge-lifecycle-proposal.md) | практики — зрелые Pattern/Standard споков, кандидаты на Standard Хаба |
| [`executable-documentation-standard.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/6ddffdfff693d8279792cd1e9c4c5d94ee0dffcf/standards/executable-documentation-standard.md) | онтология и Pages UX ложатся на graph-of-practices (атомарные узлы) |
| [`methodology-research-and-proposals.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/6ddffdfff693d8279792cd1e9c4c5d94ee0dffcf/governance/rfc/methodology-research-and-proposals.md) | таксономия операций — вклад в методологический маппинг (BABOK/ISO) |
| [`external-knowledge-integration.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/6ddffdfff693d8279792cd1e9c4c5d94ee0dffcf/governance/rfc/external-knowledge-integration.md) | таксономия как Base Registry, споки — Local Extension |
| [`AI_GOVERNANCE.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/6ddffdfff693d8279792cd1e9c4c5d94ee0dffcf/AI_GOVERNANCE.md) | BCREQ human gates = «финальные решения за человеком» |

## 4. Критерии готовности к переносу (C1–C5 обратного потока)

См. [`docs/rfc-hub-integration.md`](../rfc-hub-integration.md):

| Критерий | Состояние на 2026-06-17 |
| --- | --- |
| C1 — применена ≥2 раз | да (онтология/таксономия/BCREQ/Pages UX действуют в Mango) |
| C2 — обобщаема (без спок-специфики) | требует работы: в каждом документе есть раздел «что обобщить» |
| C3 — зрелость после human review | **открыто** — ждёт решения пользователя/Хаба |
| C4 — чистота данных | да (нет секретов, только governance-контент) |
| C5 — документированность | да (ADR + стандарт + документ передачи на каждую) |

Перенос предлагается **после** обобщения (C2) и human review (C3).

## 5. Что этот RFC НЕ делает

- Не меняет контракты Хаба и не правит контракты Mango.
- Не переносит практики автоматически — это решение Хаба/пользователя.
- Не дублирует процессы Хаба: практики предлагаются как вклад в существующие
  механизмы (graph-of-practices, methodology RFC), а не как параллельные.

## 6. Связанные записи

- Реестр: RFC-HUB-001 в [`rfc-register.md`](rfc-register.md) (`proposed`).
- Матрица: раздел «Передача знаний» в [`sync-matrix-2026-06-17.md`](../../pr-ops/sync-matrix-2026-06-17.md).
- Каталог практик: [`knowledge-transfer-to-hub/README.md`](knowledge-transfer-to-hub/README.md).

## 7. Открытые вопросы

1. Куда в Хабе размещать BA-онтологию — `standards/` или новый раздел `domains/ba/`?
2. Принимать ли таксономию операций как Base Registry (один на экосистему) или
   как практику-референс?
3. Ведутся в [`pr-ops/BACKLOG.md`](../../pr-ops/BACKLOG.md).
