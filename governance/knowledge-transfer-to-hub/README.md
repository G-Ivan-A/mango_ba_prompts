---
status: draft
version: 0.1
updated: 2026-06-16
ai-generated: true
type: navigation
scope: governance
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/105"
related_artifacts:
  - "governance/rfc-to-hub-001-knowledge-transfer.md"
  - "governance/sync-matrix-2026-06-17.md"
  - "docs/rfc-hub-integration.md"
---

# Передача знаний в Хаб — уникальные практики mango_ba_prompts

> **Что это.** Каталог уникальных практик спока `mango_ba_prompts`, которых **нет
> в Хабе** ([`audit-hub-2026-06-17.md`](../audit-hub-2026-06-17.md)) и которые
> являются кандидатами на перенос в Хаб по обратному потоку «спок → Хаб»
> ([`docs/rfc-hub-integration.md`](../../docs/rfc-hub-integration.md)). Это **ФТ-5**
> задачи [#105](https://github.com/G-Ivan-A/mango_ba_prompts/issues/105).
>
> **Статус.** Документы передачи — **предложения**. Сам перенос — отдельная
> follow-up задача и решение пользователя/Хаба
> ([`rfc-to-hub-001-knowledge-transfer.md`](../rfc-to-hub-001-knowledge-transfer.md)).
> До утверждения практики остаются локальными контрактами Mango.

## Как выявлены уникальные практики

Источник — [`audit-contracts-mango-2026-06-17.md`](../audit-contracts-mango-2026-06-17.md)
(колонка «Отличается от Хаба» = «нет аналога») и
[`sync-matrix-2026-06-17.md`](../sync-matrix-2026-06-17.md) (действие = «Передача
знаний →»). Критерий уникальности: в Хабе на снимке
[`6ddffdf`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/tree/6ddffdfff693d8279792cd1e9c4c5d94ee0dffcf)
нет ни стандарта, ни RFC, ни practice node по этой теме.

## Каталог практик-кандидатов

| Практика | ADR / стандарт | Документ передачи | Почему полезно другим |
| --- | --- | --- | --- |
| Онтология БА (Артефакт↔Процесс↔Операция) | [ADR #003](../../docs/adr/003-ba-ontology.md) | [`ba-ontology.md`](ba-ontology.md) | переиспользуемая модель графа знаний для любого BA-/knowledge-проекта |
| Таксономия когнитивных операций БА | [ADR #004](../../docs/adr/004-operations-taxonomy.md) | [`operations-taxonomy.md`](operations-taxonomy.md) | маппинг операций на BABOK/ISO — общий язык для BA-команд |
| Процесс формирования BCREQ (human gates) | [ADR #009](../../docs/adr/009-bcreq-formation-process.md) | [`bcreq-process.md`](bcreq-process.md) | каркас многоуровневого процесса с human-in-the-loop |
| UX дерева процессов GitHub Pages | [ADR #010](../../docs/adr/010-pages-ux.md) | [`pages-ux.md`](pages-ux.md) | паттерн «слой данных / слой отображения» для документ-сайтов |

> Процесс отладки промптов — тоже уникальная практика, но передаётся отдельным RFC
> [`rfc-to-hub-002-prompt-debugging-process.md`](../rfc-to-hub-002-prompt-debugging-process.md)
> (он про процесс, а не про BA-контент).

## Формат документа передачи

Каждый документ в этом каталоге содержит: **название**, **описание (что/как/зачем)**,
**обоснование** (почему полезно другим проектам), **примеры использования**,
**ссылки** на ADR/стандарты-носители и **что обобщить** перед переносом (убрать
Mango-специфику, критерий C2 обратного потока).
