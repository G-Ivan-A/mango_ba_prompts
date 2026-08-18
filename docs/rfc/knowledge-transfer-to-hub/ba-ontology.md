---
status: draft
version: 0.1
updated: 2026-06-16
ai-generated: true
type: knowledge-transfer
scope: strategic
target_repo: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab"
source_spoke: "https://github.com/G-Ivan-A/mango_ba_prompts"
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/105"
related_artifacts:
  - "docs/adr/003-ba-ontology.md"
  - "standards/ba-ontology.md"
  - "docs/rfc/rfc-to-hub-001-knowledge-transfer.md"
---

# Передача знаний: онтология бизнес-анализа (граф Артефакт↔Процесс↔Операция)

## Название практики

Онтология предметной области БА как граф из трёх связанных сущностей:
**Артефакт** (результат — что производим), **Процесс** (как производим),
**Операция** (когнитивное действие внутри процесса).

## Описание (что, как, зачем)

- **Что.** Единая модель знаний БА: ~30 типов артефактов с состояниями
  жизненного цикла (включая `needs-clarification` и `partial` baseline), 13
  когнитивных операций, процессы, связывающие операции с артефактами. Связи
  направленные: процесс *производит* артефакт, процесс *состоит из* операций,
  артефакт *является входом* операции.
- **Как.** Онтология зафиксирована в [ADR #003](../../adr/003-ba-ontology.md)
  и стандарте [`standards/ba-ontology.md`](../../../standards/ba-ontology.md);
  машиночитаемое представление — в данных дерева процессов
  (`process-tree.json`), что позволяет навигацию и проверку покрытия промптами.
- **Зачем.** Даёт общий словарь и навигацию «от результата к способу его
  получения». Промпт перестаёт быть изолированным текстом — он привязан к
  операции, операция к процессу, процесс к артефакту.

## Обоснование (почему полезно другим проектам)

Любая knowledge-/BA-команда экосистемы сталкивается с теми же вопросами: «какой
артефакт мы производим», «каким процессом», «какие шаги мышления внутри». Граф
Артефакт↔Процесс↔Операция — переиспользуемый каркас графа знаний, совместимый с
идеей Хаба об **атомарных узлах знаний** (graph-of-practices,
`executable-documentation-standard.md`) и обратной трассируемостью жизненного
цикла знаний. Хаб получает готовую доменную онтологию для класса BA-споков.

## Примеры использования

- **Навигация GitHub Pages** (см. [`pages-ux.md`](pages-ux.md)): дерево процессов
  строится прямо из онтологии; видно, какие узлы покрыты промптами, какие — gap.
- **Проверка покрытия:** аудит «для каких операций нет промпта» — это обход графа.
- **Состояние `needs-clarification`:** артефакт в неполном baseline явно
  отмечается, что связывает онтологию с процессом BCREQ ([`bcreq-process.md`](bcreq-process.md)).

## Что обобщить перед переносом (критерий C2)

Убрать Mango-специфику набора артефактов; оставить **мета-модель** (три сущности +
типы связей + состояния ЖЦ) как шаблон, который каждый BA-спок наполняет своими
типами. Конкретный набор из 13 операций передаётся отдельно
([`operations-taxonomy.md`](operations-taxonomy.md)).

## Ссылки

- ADR-носитель: [`docs/adr/003-ba-ontology.md`](../../adr/003-ba-ontology.md)
- Стандарт: [`standards/ba-ontology.md`](../../../standards/ba-ontology.md)
- Umbrella-RFC: [`rfc-to-hub-001-knowledge-transfer.md`](../rfc-to-hub-001-knowledge-transfer.md)
- Контракт Хаба (родственный): [`executable-documentation-standard.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/6ddffdfff693d8279792cd1e9c4c5d94ee0dffcf/standards/executable-documentation-standard.md)
