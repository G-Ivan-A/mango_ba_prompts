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
  - "governance/prompt-debugging-process.md"
  - "governance/rfc-process.md"
  - "governance/audit-hub-2026-06-17.md"
  - "docs/rfc-hub-integration.md"
---

# RFC в Хаб 002: процесс отладки промптов как общая практика

> **Адресат: `hybrid-Intelligence-lab` (Хаб).** Это **предложение** спока
> `mango_ba_prompts` к Хабу, оформленное по обратному потоку «спок → Хаб»
> ([`docs/rfc-hub-integration.md`](../docs/rfc-hub-integration.md)). Финальное
> решение — за пользователем по правилам Хаба (`AI_GOVERNANCE.md`, правило
> «финальные решения за человеком»). До утверждения практика остаётся локальной.

## 1. Проблема (зачем Хабу это)

Аудит Хаба ([`audit-hub-2026-06-17.md`](audit-hub-2026-06-17.md)) показал: Хаб
имеет жизненный цикл знаний
([`knowledge-lifecycle-proposal.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/6ddffdfff693d8279792cd1e9c4c5d94ee0dffcf/governance/rfc/knowledge-lifecycle-proposal.md))
и Research Memory
([`research-memory-source-intelligence.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/6ddffdfff693d8279792cd1e9c4c5d94ee0dffcf/governance/rfc/research-memory-source-intelligence.md)),
но **не описывает процесс отладки и изменения уже существующих исполнимых
артефактов** (промптов, runbook-ов). Это пробел, общий для любой Prompt & Pattern
Library и любой HTOM-команды, эксплуатирующей промпты.

**Прецедент.** В Mango (issue #101 / PR #102) попытка поднять версии 6 промптов
`0.1 → 0.2` напрямую, «по факту убедительного эксперимента», оказалась нарушением
контракта отладки. Корень — отсутствие формализованного порядка превращения
наблюдения в правку.

## 2. Предложение

Принять в Хаб (как стандарт или practice node) процесс отладки исполнимых
артефактов с контрактом порядка:

> **эксперимент → RFC → согласование с человеком → изменение**

Полная локальная реализация — в
[`governance/prompt-debugging-process.md`](prompt-debugging-process.md). Ключевые
элементы, предлагаемые к обобщению:

1. **Принцип «диагноз ≠ право на правку».** Зафиксированный эксперимент даёт
   *основание предложить* RFC, но не *право внести* правку. Согласуется с правилом
   Хаба «молчание = согласие лишь с текущим состоянием».
2. **Сбор обратной связи** из воспроизводимых сигналов (прогоны с цитатой,
   issue-фидбек) — Tier-2-совместимо с Research Memory (Knowledge Object со
   статусом Observed/Candidate).
3. **RFC-реестр** со статусами `proposed → in-review → accepted/rejected →
   implemented` — отображается на стадию RFC жизненного цикла знаний Хаба.
4. **Инициатива человека** на правку (не агента, не эксперимента).
5. **Связка «правка ⇄ версия ⇄ CHANGELOG»** (Minor/Major/Breaking).

## 3. Совместимость с контрактами Хаба

| Контракт Хаба | Как соотносится |
| --- | --- |
| `knowledge-lifecycle-proposal.md` | процесс = детализация перехода Hypothesis → RFC → (обновлённый) executable artifact |
| `research-memory-source-intelligence.md` | сигналы отладки = Knowledge Objects (Observed/Candidate/Applied) |
| `executable-contract-standard.md` | объект отладки = исполнимый документ (`executable: true`) |
| `AI_GOVERNANCE.md` | «финальные решения за человеком» — тот же контур приёмки |

## 4. Что предлагается разместить в Хабе

- **Вариант A (предпочтительный):** practice node
  `practices/agent-work/executable-artifact-debugging.md` (по
  `executable-documentation-standard.md`) — обобщённая, без Mango-специфики.
- **Вариант B:** раздел в `standards/` как стандарт отладки исполнимых артефактов.

Источник (provenance): permalink на
[`governance/prompt-debugging-process.md`](prompt-debugging-process.md) спока с
полями `source_spoke` + `source_sha` (по практике обратного потока).

## 5. Что этот RFC не делает

- Не меняет контракты Хаба сам по себе (только предложение).
- Не блокирует локальное использование процесса в Mango (он уже действует).
- Не требует переписывать существующие промпты Хаба.

## 6. Критерии готовности к переносу (C1–C5 обратного потока)

См. [`docs/rfc-hub-integration.md`](../docs/rfc-hub-integration.md): практика
применена в ≥2 отладках (C1 — после валидации на 2–3 ближайших), обобщаема (C2),
зрелость после human review (C3), чистота данных (C4), документированность (C5).
На 2026-06-17 процесс — Draft v0.1; перенос предлагается **после** валидации C1.

## 7. Открытые вопросы

1. Где разместить в Хабе — `practices/` (node) или `standards/`?
2. Объединить ли с моделью Knowledge Object (статусы отладки = статусы объекта)?
3. Ведутся в [`governance/BACKLOG.md`](BACKLOG.md).
