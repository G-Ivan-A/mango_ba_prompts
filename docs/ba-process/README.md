---
status: draft
version: 0.1
updated: 2026-06-18
ai-generated: true
type: index
scope: mango-only
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/109"
---

# Прогоны BA-процесса (живые кейсы)

> **Что это.** Каталог **реальных прогонов** цепочек промптов на конкретных
> требованиях заказчика — от сырого входа до набора ранних артефактов. В отличие от
> [`docs/ba-processes/`](../ba-processes/00-index.md) (карта *какие* промпты и в каком
> порядке использовать), этот каталог хранит *результаты их применения* на кейсах.

## Зачем отдельный каталог

- Один кейс = одна папка со всеми артефактами и логом эксперимента → воспроизводимость.
- Накапливает доказательную базу для [реестра RFC](../../governance/rfc-register.md)
  по улучшению промптов (см. [`standards/experiment-log-standard.md`](../../standards/experiment-log-standard.md)).
- Демонстрирует «dogfooding»: библиотека промптов проверяется на собственных задачах.

## Кейсы

| Кейс | Требование (кратко) | Тип результата | Источник |
| --- | --- | --- | --- |
| [Многоканальная нагрузка агента](./multichannel-agent-workload/README.md) | Одновременная работа агента с обращениями голос/чат/e-mail, лимит 3, приоритет | Ранний разбор (нормализация + вопросы + US/UC + варианты, Раздел 3) | [issue #109](https://github.com/G-Ivan-A/mango_ba_prompts/issues/109) |

## Структура папки кейса (конвенция)

```
<кейс>/
  README.md            — навигация и TL;DR
  inputs/              — сырой вход + выжимка БЗ (с цитатами)
  prompts-chain.md     — выбранная цепочка промптов + обоснование
  steps/               — промежуточный результат каждого шага
  final-artifact.md    — консолидация + рекомендация БА
  experiment-log.md    — лог по experiment-log-standard (6 метрик)
```

## Связанные документы

- Карта процессов и промптов: [`docs/ba-processes/00-index.md`](../ba-processes/00-index.md)
- Стандарт фиксации экспериментов: [`standards/experiment-log-standard.md`](../../standards/experiment-log-standard.md)
- Реестр RFC: [`governance/rfc-register.md`](../../governance/rfc-register.md)
- Стандарт работы с БЗ: [`standards/kb-standard.md`](../../standards/kb-standard.md) ([ADR-007](../adr/007-kb-standard.md))
