---
status: draft
version: 0.1
updated: 2026-06-16
ai-generated: true
type: process
scope: governance
source_hub: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/6ddffdfff693d8279792cd1e9c4c5d94ee0dffcf/governance/rfc/knowledge-lifecycle-proposal.md"
source_sha: "6ddffdfff693d8279792cd1e9c4c5d94ee0dffcf"
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/105"
related_artifacts:
  - "docs/rfc/rfc-register.md"
  - "standards/prompt-debugging-process.md"
  - "pr-ops/sync-matrix-2026-06-17.md"
  - "AI_GOVERNANCE.md"
---

# RFC-процесс mango_ba_prompts (интеграция процесса Хаба)

> **Статус: Draft.** Документ закрывает **ФТ-4 (часть 1)** задачи
> [#105](https://github.com/G-Ivan-A/mango_ba_prompts/issues/105): интегрировать
> RFC-процесс **из Хаба**, а не изобретать свой. Источник истины процесса —
> [`knowledge-lifecycle-proposal.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/6ddffdfff693d8279792cd1e9c4c5d94ee0dffcf/governance/rfc/knowledge-lifecycle-proposal.md)
> Хаба. Этот документ **ссылается** на него и описывает локальное применение в
> споке, не дублируя содержание (критическое ограничение задачи: не дублировать,
> а ссылаться).

## 1. Зачем

Чтобы любое предложение изменить контракт, промпт или стандарт спока проходило
**предсказуемый путь до решения человека**, единый с экосистемой Хаба. RFC
(Request for Comments) — предложение, а не правило: оно становится обязательным
только после явного решения пользователя.

Ключевой принцип Хаба, который спок наследует дословно:

> **Молчание = согласие лишь с текущим состоянием, не с повышением статуса.**
> (`knowledge-lifecycle-proposal.md`)

То есть зафиксированное наблюдение/эксперимент даёт *основание предложить* RFC, но
не *право внести* изменение — право даёт только решение человека.

## 2. Жизненный цикл знаний Хаба (upstream)

Спок наследует цепочку зрелости артефактов из Хаба
([`knowledge-lifecycle-proposal.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/6ddffdfff693d8279792cd1e9c4c5d94ee0dffcf/governance/rfc/knowledge-lifecycle-proposal.md)):

```
Observation → Research → Hypothesis → RFC → Pattern → Standard → Template → Framework → Deprecation/Archive
```

С правилом **обратной трассируемости**: каждый Standard ссылается на Pattern,
Pattern — на RFC, RFC — на Research/Observation. RFC — обязательное звено между
гипотезой и принятой практикой.

## 3. Локальное применение в споке

В `mango_ba_prompts` цепочка отображается на реальные артефакты:

| Стадия Хаба | Артефакт спока | Где живёт |
| --- | --- | --- |
| Observation | сигнал из прогона БА, issue `prompt:feedback` | issues, `pr-ops/prompt-feedback.json` |
| Research / Hypothesis | анализ эксперимента, гипотеза правки | `docs/analysis/*`, `runs/*` |
| **RFC** | запись в реестре RFC | [`docs/rfc/rfc-register.md`](rfc-register.md) |
| Pattern | паттерн | `patterns/` ([`pattern-standard.md`](../../standards/pattern-standard.md)) |
| Standard | стандарт / ADR | `standards/`, `docs/adr/` |
| Deprecation/Archive | архив | `prompts/archive/`, `superseded` в frontmatter |

**Два класса RFC в споке:**

1. **RFC по промптам** — предложение изменить существующий промпт. Детальный
   порядок — в [`prompt-debugging-process.md`](../../standards/prompt-debugging-process.md)
   (эксперимент → RFC → согласование → изменение). Этот документ — общий слой над ним.
2. **RFC по контрактам/стандартам/синхронизации** — предложение изменить
   governance-контракт, стандарт или согласовать расхождение с Хабом
   (см. [`sync-matrix-2026-06-17.md`](../../pr-ops/sync-matrix-2026-06-17.md)).

Оба класса ведутся в **одном реестре** [`rfc-register.md`](rfc-register.md).

## 4. Статусы RFC (локальный реестр)

Локальный реестр использует операционные статусы, совместимые с правилом Хаба
«повышение статуса — только по решению человека»:

```
proposed → in-review → accepted  → implemented
                     ↘ rejected
```

| Статус | Значение | Кто переводит |
| --- | --- | --- |
| `proposed` | оформлен, ждёт рассмотрения | автор RFC (БА/агент) |
| `in-review` | рассматривается пользователем | пользователь |
| `accepted` | принят к реализации | **только пользователь** |
| `rejected` | отклонён (с причиной, остаётся в реестре) | **только пользователь** |
| `implemented` | внесён, связан с PR | исполнитель после merge |

> Соответствие со статусами знаний Хаба (research-memory): `proposed/in-review` ≈
> *Candidate*, `accepted/implemented` ≈ *Applied*, `rejected` ≈ *Rejected*,
> вытесненный RFC ≈ *Superseded*.

## 5. Поток: от RFC к стандарту

```
[Observation/сигнал]
      │  фиксируется с цитатой/источником
      ▼
[RFC: proposed]  ── автор оформляет запись в rfc-register.md
      │
      ▼
[in-review]      ── пользователь рассматривает
      │
   ┌──┴───────────┐
   ▼              ▼
[rejected]    [accepted]  ── ТОЛЬКО решение пользователя
(с причиной)      │
      ▼          ▼
[остаётся    [реализация в малом PR]
 в реестре]      │  правка промпта/стандарта + bump версии + CHANGELOG + artifact-map
                 ▼
            [implemented]  ── связан с PR; при необходимости → Pattern/Standard
```

Это **тот же** контур приёмки, что в `AI_GOVERNANCE.md` (финальные решения за
человеком, правило 3) и в `knowledge-lifecycle-proposal.md` Хаба.

## 6. Когда нужен RFC (а когда нет)

| Ситуация | Нужен RFC? |
| --- | --- |
| Изменить существующий промпт | **Да** (см. `prompt-debugging-process.md`) |
| Изменить governance-контракт / стандарт | **Да** |
| Согласовать расхождение с Хабом (sync-matrix) | **Да** |
| Передать уникальную практику в Хаб | **Да** (RFC в Хаб, см. `rfc-to-hub-*`) |
| Создать **новый** draft-артефакт (Creative mode) | Нет — по правилу 8 `AI_GOVERNANCE.md`, фиксируется в PR |
| Опечатка, ссылка, форматирование | Нет |

## 7. Связь с реестром и существующими контрактами

- **Реестр**: [`rfc-register.md`](rfc-register.md) — живой список всех RFC спока.
- **Промпты**: [`prompt-debugging-process.md`](../../standards/prompt-debugging-process.md) —
  детализация для промптов.
- **Синхронизация**: [`sync-matrix-2026-06-17.md`](../../pr-ops/sync-matrix-2026-06-17.md) —
  откуда берутся RFC-SYNC-*.
- **Governance**: [`AI_GOVERNANCE.md`](../../ai-governance/ai-governance.md) — финальные решения за
  человеком; Creative Override оформляется как RFC/ADR.

## 8. Открытые вопросы

1. Нужен ли отдельный файл RFC для крупных предложений (vs строка в реестре)?
   (наследуется как открытый вопрос из `prompt-debugging-process.md`).
2. Принимать ли frontmatter-контракт трассируемости Хаба (`based_on`,
   `supersedes`, `used_by`) для ADR/стандартов спока? — кандидат на RFC-SYNC.
3. Ведутся в [`pr-ops/BACKLOG.md`](../../pr-ops/BACKLOG.md).
