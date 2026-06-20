---
status: draft
version: 0.1
updated: 2026-06-20
ai-generated: true
type: kb-practices-readme
scope: kb/practices
related_artifacts:
  - "kb/practices/source-backed-analysis.md"
  - "standards/kb-standard.md"
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/97"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/144"
---

# KB Practices

`kb/practices/` хранит ручные практики и методики анализа, которые можно
применять в разных задачах проекта. Это не продуктовая документация Mango Office
и не generated output pipeline из `kb/mango-product-docs/`.

## Что это?

Практика KB — это компактная, цитируемая запись с правилом, чек-листом или
методикой. Она отличается от стандарта тем, что описывает рабочий приём, а не
обязательный контракт; точные правила цитирования остаются в
[`standards/kb-standard.md`](../../standards/kb-standard.md).

## Как использовать?

1. Найдите подходящую практику в этом каталоге или в индексе
   [`kb/README.md`](../README.md).
2. Примените правило к задаче.
3. Сошлитесь на запись стабильным адресом `kb/practices/<file>.md#<anchor>`.

Текущая запись:

- [`source-backed-analysis.md`](source-backed-analysis.md) — проверка
  существования источника перед нормативным выводом.

## Быстрый старт

Проверить, что каталог описан в общей структуре KB:

```bash
python3 scripts/validate_issue_144_kb_structure_readmes.py
```

## Связанные документы

- [`kb/README.md`](../README.md) — общий индекс и границы KB.
- [`kb/mango-product-docs/README.md`](../mango-product-docs/README.md) —
  отдельный namespace продуктовой документации.
- [`standards/kb-standard.md`](../../standards/kb-standard.md) — контракт
  цитирования и pre-RAG retrieval.
