---
status: draft
version: 0.1
updated: 2026-06-16
ai-generated: true
type: matrix
scope: governance
source_hub: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/tree/6ddffdfff693d8279792cd1e9c4c5d94ee0dffcf"
source_sha: "6ddffdfff693d8279792cd1e9c4c5d94ee0dffcf"
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/105"
related_artifacts:
  - "docs/audit/audit-contracts-mango-2026-06-17.md"
  - "docs/audit/audit-hub-2026-06-17.md"
  - "docs/rfc/rfc-process.md"
  - "docs/rfc/rfc-register.md"
---

# Матрица синхронизации mango_ba_prompts ↔ Хаб (2026-06-17)

> **Повод.** Задача [#105](https://github.com/G-Ivan-A/mango_ba_prompts/issues/105),
> **ФТ-3**: свести контракты спока ([аудит mango](../docs/audit/audit-contracts-mango-2026-06-17.md))
> и Хаба ([аудит Хаба](../docs/audit/audit-hub-2026-06-17.md)) в единую матрицу соответствия —
> что синхронизировать, что оставить локальным, где требуется RFC.
>
> **Правило синхронизации (критическое).** Если в Хабе есть аналог, но у нас иначе —
> **не менять сразу**, а создать RFC ([`rfc-process.md`](../docs/rfc/rfc-process.md)). Если у
> нас уникальная практика — подготовить **передачу знаний** в Хаб
> ([`knowledge-transfer-to-hub/`](../docs/rfc/knowledge-transfer-to-hub/)). Все ссылки на Хаб —
> permalink на снимок [`6ddffdf`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/tree/6ddffdfff693d8279792cd1e9c4c5d94ee0dffcf).

## Легенда действий

| Действие | Значение |
| --- | --- |
| **Локальный** | Оставить в споке, не синхронизировать. |
| **Smart Sync ←** | Источник истины — Хаб; обновлять осознанным Smart Sync. |
| **Сверить → RFC** | Сверить с Хабом; при расхождении оформить RFC (не править напрямую). |
| **Передача знаний →** | Уникальная практика; подготовить документ передачи + RFC в Хаб. |
| **Интегрировать** | Принять процесс Хаба в спок (ссылкой, не копией). |

---

## 1. Матрица контрактов

| Контракт mango_ba_prompts | Контракт Хаба (snapshot 6ddffdf) | Отличается? | Действие | RFC |
| --- | --- | --- | --- | --- |
| ADR #003 (онтология БА) | — нет в Хабе | — | **Передача знаний →** | RFC-HUB-001 |
| ADR #004 (таксономия операций) | PR #246 (методологии, BABOK-маппинг) | частично | **Сверить → RFC** | RFC-SYNC-004 |
| ADR #005 (нейминг артефактов + Team Directory) | `standards/file-naming.md` (другой предмет) | да (разные предметы) | **Сверить → RFC** (только нейминг файлов-стандартов) | RFC-SYNC-005 |
| ADR #006 (нейминг промптов) | — нет прямого аналога | — | **Локальный** | — |
| ADR #007 (стандарт БЗ, цитирование) | PR #242 (Research Memory, Knowledge Object) | частично | **Сверить → RFC** | RFC-SYNC-007 |
| ADR #008 (отраслевые стандарты, реестр) | `external-knowledge-integration.md` (Tier 1/Local Extension) | частично | **Сверить → RFC** | RFC-SYNC-008 |
| ADR #009 (процесс BCREQ) | — нет в Хабе | — | **Передача знаний →** | RFC-HUB-001 |
| ADR #010 (UX GitHub Pages) | — нет в Хабе | — | **Передача знаний →** | RFC-HUB-001 |
| `standards/product-classification-contract.md` | — нет (явно «только Mango») | — | **Локальный** | — |
| `standards/prompt-standard.md` | `executable-contract-standard.md` | частично | **Сверить → RFC** | RFC-SYNC-PR |
| `standards/pattern-standard.md` | `executable-documentation-standard.md` | частично | **Сверить → RFC** | RFC-SYNC-PT |
| `standards/experiment-log-standard.md` | — нет в Хабе | — | **Локальный** | — |
| `standards/team-directory.md` | — нет в Хабе | — | **Локальный** | — |
| `standards/GLOSSARY.md` | `standards/glossary.md` (canonical, 56+ терминов) | да (копия Хаба, отстаёт) | **Smart Sync ←** | — |
| `AI_GOVERNANCE.md` | `AI_GOVERNANCE.md` (canonical) | да (локальная адаптация) | **Smart Sync ←** (геном) | — |
| `CONTRIBUTING.md` | `CONTRIBUTING.md` | да | **Smart Sync ←** | — |
| `AI_QUICK_RULES.md`, `AI_SESSION_HANDOVER_PROMPT.md` | HTOM-геном (`templates/htom/`, `session-handover-standard.md`) | да | **Smart Sync ←** | — |
| `pr-ops/artifact-map.md` | `pr-ops/artifact-map.md` | да (уже синхронизирован) | **Smart Sync ←** | — |
| `.archive/ai-rules/agent-onboarding-protocol_old.md` | `.archive/ai-rules/agent-onboarding-protocol_old.md` | да | **Smart Sync ←** | — |
| `pr-ops/BACKLOG.md` | `governance/backlog.md` | да | **Smart Sync ←** | — |
| `pr-ops/session-digests.md` | `pr-ops/session-digests.md` | да | **Smart Sync ←** | — |
| `.hub-profile.json` | формат Smart Sync (Хаб PR #208) | да | **Smart Sync ←** | — |
| `standards/prompt-debugging-process.md` | — нет в Хабе | — | **Передача знаний →** | RFC-HUB-002 |
| RFC-процесс (`docs/rfc/rfc-register.md`) | `knowledge-lifecycle-proposal.md` (lifecycle) | да (нужна привязка) | **Интегрировать** | см. `rfc-process.md` |
| (нет) — архетип/структура | `htom-vs-spoke-clarification` (canonical), `repo-model.md`, `repository-archetypes` (PR #243) | — | **Следовать** (структура — PR #244) | — |
| (нет) — issue lifecycle | `standards/issue-workflow.md` (7 статусов) | — | **Сверить → RFC** (опционально принять статусы) | RFC-SYNC-IW |

---

## 2. Реестр RFC синхронизации (открыт этой задачей)

Эти RFC — **предложения сверки**, заведены в [`rfc-register.md`](../docs/rfc/rfc-register.md)
в статусе `proposed`. Контракты Mango в этой задаче **не меняются**; решение о
правке — за пользователем (правило синхронизации).

| RFC | Контракт Mango | С чем сверять (Хаб) | Гипотеза расхождения |
| --- | --- | --- | --- |
| RFC-SYNC-004 | ADR #004 таксономия | PR #246 методологии | согласовать набор операций ↔ Knowledge Areas BABOK Хаба |
| RFC-SYNC-005 | ADR #005 нейминг | `file-naming.md` | имена файлов-стандартов (`*-standard.md`) — совместить с правилом Хаба |
| RFC-SYNC-007 | ADR #007 БЗ | PR #242 Research Memory | ввести модель Knowledge Object (Tier 2) поверх формата цитирования |
| RFC-SYNC-008 | ADR #008 отраслевые | `external-knowledge-integration.md` | согласовать tier-модель и Base Registry / Local Extension |
| RFC-SYNC-PR | `prompt-standard.md` | `executable-contract-standard.md` | маркировка `executable: true` для исполнимых промптов |
| RFC-SYNC-PT | `pattern-standard.md` | `executable-documentation-standard.md` | атомизация практик (graph-of-practices) |
| RFC-SYNC-IW | issue-процесс | `issue-workflow.md` | принять ли 7 статусов задач Хаба |

## 3. Реестр передачи знаний (спок → Хаб)

Уникальные практики Mango (нет аналогов в Хабе) — кандидаты на перенос в Хаб по
обратному потоку (см. [`docs/rfc-hub-integration.md`](../docs/rfc-hub-integration.md)
и [`knowledge-transfer-to-hub/`](../docs/rfc/knowledge-transfer-to-hub/)).

| RFC в Хаб | Практика Mango | Документ передачи |
| --- | --- | --- |
| RFC-HUB-001 | Онтология БА (#003), таксономия (#004), BCREQ (#009), Pages UX (#010) | [`rfc-to-hub-001-knowledge-transfer.md`](../docs/rfc/rfc-to-hub-001-knowledge-transfer.md) + `knowledge-transfer-to-hub/` |
| RFC-HUB-002 | Процесс отладки промптов | [`rfc-to-hub-002-prompt-debugging-process.md`](../docs/rfc/rfc-to-hub-002-prompt-debugging-process.md) |

## 4. Что НЕ синхронизируется (осознанно локальное)

- `product-classification-contract.md` — привязан к продукту Mango.
- `experiment-log-standard.md` — операционная модель фиксации прогонов Mango.
- `team-directory.md` — оргструктура Mango (2 команды).
- ADR #006 (нейминг промптов) — конвенция библиотеки промптов.

Эти контракты не дублируются в Хаб и не требуют RFC: они не пересекаются с общими
практиками экосистемы.

## 5. Вывод

Матрица разбивает 30+ контрактов спока на пять режимов: **локальные** (4),
**Smart Sync из Хаба** (9 — геном + глоссарий), **сверка → RFC** (7),
**передача знаний → Хаб** (5 практик в 2 RFC) и **интеграция процесса** (RFC-процесс).
Принцип соблюдён: **ни один контракт не правится напрямую** — расхождения
оформлены как RFC `proposed`, уникальные практики — как документы передачи знаний.
