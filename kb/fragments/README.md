---
status: draft
version: 0.2
updated: 2026-06-20
ai-generated: true
type: kb-fragments-guide
scope: kb/fragments
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/111"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/144"
---

# `kb/fragments/` — атомарные фрагменты (задел под RAG)

**Опциональный** слой (ФТ-4) и **точка эволюции БЗ к векторному RAG**. Сейчас
пуст намеренно: разделы из [`kb/mango-product-docs/processed/`](../mango-product-docs/processed/README.md) уже работают
как чанки (раздел = файл = адрес), и дробить их мельче без реального RAG —
преждевременная оптимизация (приоритет issue: **качество > экономия токенов**).

Каталог создан в issue #111 как будущий слой атомарных фрагментов. Он не хранит продуктовую документацию,
исходные PDF или generated output pipeline; это
остаётся зоной ответственности `kb/mango-product-docs/`.

## Когда он понадобится

Когда появится векторная БЗ / эмбеддинги, разделы-чанки можно будет нарезать на
более мелкие атомарные фрагменты (абзац/таблица/определение) и складывать сюда
вместе с метаданными для индексации:

```
kb/fragments/<doc-slug>/
├── <doc-slug>-04-2-pravila-raspredeleniya.md   # один факт/абзац = один фрагмент
└── fragments.jsonl                              # {id, text, source, pages, embedding?}
```

## Почему это «бесшовно»

Стабильные адреса уже заложены: `id` и путь `kb/mango-product-docs/processed/<doc>/sections/NN#anchor`
из текущего слоя становятся `chunk_id` будущего индекса **без переписывания
артефактов** (ADR-007, правило R4). То есть переход на RAG — это добавление слоя
`fragments/` + индекса, а не переделка БЗ. Подробнее — раздел «Следующие шаги» в
[`docs/kb-experiment-report.md`](../../docs/kb-experiment-report.md).
