---
status: draft
version: 0.1
updated: 2026-06-16
ai-generated: true
type: kb-index
scope: kb
related_artifacts:
  - "standards/kb-standard.md"
  - "docs/adr/007-kb-standard.md"
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/97"
---

# База знаний (KB) — индекс-карта

> Регулируется [kb-standard.md](../standards/kb-standard.md) /
> [ADR-007](../docs/adr/007-kb-standard.md). KB хранит **практики, примеры и
> справочники, не являющиеся стандартами** (см. границы в ADR-007 §4). Термины —
> в [глоссарии](../standards/GLOSSARY.md), не здесь.

## Два слоя БЗ

| Слой | Что это | Где |
| --- | --- | --- |
| **Ручные записи** (этот файл) | Практики/примеры/справочники, написанные руками (правило R1) | таблица ниже, `practices/` · `examples/` · `references/` |
| **Извлечённые документы** (issue #111) | Машиночитаемые чанки из PDF/веб-источников: индекс → раздел → цитата | [`sources/`](sources/README.md) (ручной ввод) → [`processed/`](processed/README.md) → [`fragments/`](fragments/README.md) |

Слой извлечения документов: как пополнять — [`sources/README.md`](sources/README.md)
(**ФТ-7**); как промпт обращается к нему — [`USAGE.md`](USAGE.md) (**ФТ-6**);
методология и оценка качества — [`docs/kb-experiment-report.md`](../docs/kb-experiment-report.md).
Оба слоя используют один формат цитат/адресации и готовятся к одному будущему RAG
(правила R1–R4 [kb-standard](../standards/kb-standard.md)).

## Зачем этот файл (pre-RAG)

До внедрения настоящего RAG этот индекс заменяет retrieval-шаг (правило R2
[kb-standard](../standards/kb-standard.md)): агент или человек находит нужную
запись по таблице ниже и цитирует её стабильным адресом
`kb/<path>#<anchor>`. Когда появится векторный RAG, те же адреса станут chunk-id
без переписывания артефактов (R4).

## Как цитировать запись KB

```markdown
[KB: <slug>](kb/<path>#<anchor>)
```

и продублировать в разделе `## Источники` артефакта (правило C3).

## Индекс записей

| Тема | Файл | Когда применять |
| --- | --- | --- |
| Анализ с опорой на источники (source-backed analysis) | [practices/source-backed-analysis.md](practices/source-backed-analysis.md) | Любой нормативный вывод; проверка существования цитируемого стандарта. |

## Добавление записи

1. Создать файл в `practices/`, `examples/` или `references/` с frontmatter
   (`id`, `status`, `sources`) — правило R1.
2. Добавить строку в индекс выше — правило R2.
3. Если вводится новый термин — предложить его в глоссарий через issue (K2),
   а не определять в KB (K1).

## Источники

- [kb-standard.md](../standards/kb-standard.md)
- [ADR-007](../docs/adr/007-kb-standard.md)
