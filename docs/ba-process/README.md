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

# Прогоны BA-процесса (архивный указатель)

> **Статус после issue #123.** Результаты реальных прогонов больше не хранятся в
> `docs/ba-process/`. Единый каталог результатов выполнения процессов —
> [`runs/`](../../runs/README.md). Этот файл оставлен как навигационный указатель
> для старых ссылок и объясняет границу между картой процесса и результатом run.

## Где теперь хранить результаты

- Маршруты, операции и рекомендуемые промпты: [`docs/ba-processes/00-index.md`](../ba-processes/00-index.md).
- Результаты выполнения: [`runs/YYYY/RUN-XXXX/`](../../runs/README.md).
- Контракт записи результата: [`standards/runs-contract-standard.md`](../../standards/runs-contract-standard.md).

## Перенесённые кейсы

| Кейс | Требование (кратко) | Тип результата | Источник |
| --- | --- | --- | --- |
| [Многоканальная нагрузка агента](../../runs/2026/RUN-0011/outputs/README.md) | Одновременная работа агента с обращениями голос/чат/e-mail, лимит 3, приоритет | Ранний разбор (нормализация + вопросы + US/UC + варианты, Раздел 3) | [issue #109](https://github.com/G-Ivan-A/mango_ba_prompts/issues/109) |

## Структура Run-записи

```
runs/YYYY/RUN-XXXX/
  metadata.yaml   — run_id, process, version, date, author, model, status
  inputs/         — сырой вход + выжимка БЗ
  outputs/        — итоговые и промежуточные артефакты
  feedback/       — обратная связь
  logs/           — логи эксперимента и метрики
```

## Связанные документы

- Карта процессов и промптов: [`docs/ba-processes/00-index.md`](../ba-processes/00-index.md)
- Реестр runs: [`runs/README.md`](../../runs/README.md)
- Стандарт Run: [`standards/runs-contract-standard.md`](../../standards/runs-contract-standard.md)
- Стандарт фиксации экспериментов: [`standards/experiment-log-standard.md`](../../standards/experiment-log-standard.md)
- Реестр RFC: [`docs/rfc/rfc-register.md`](../../docs/rfc/rfc-register.md)
- Стандарт работы с БЗ: [`standards/kb-standard.md`](../../standards/kb-standard.md) ([ADR-007](../adr/007-kb-standard.md))
