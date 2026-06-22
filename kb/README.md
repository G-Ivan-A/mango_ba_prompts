---
status: draft
version: 0.2
updated: 2026-06-21
ai-generated: true
type: kb-index
scope: kb
related_artifacts:
  - "standards/kb-standard.md"
  - "docs/adr/007-kb-standard.md"
  - "kb/mango-product-docs/README.md"
  - "kb/industry-taxonomy/README.md"
  - "kb/mango-taxonomy/README.md"
  - "docs/audit/issue-144-kb-structure.md"
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/97"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/111"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/144"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/156"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/160"
---

# База знаний (KB)

`kb/` — централизованное хранилище знаний проекта: ручные практики, фрагменты
для будущего RAG и извлечённая документация Mango Office. Каталог отделяет
знания от стандартов, ADR, run records и продуктового кода.

## Что это?

KB регулируется [kb-standard.md](../standards/kb-standard.md) и
[ADR-007](../docs/adr/007-kb-standard.md). Термины хранятся в
[глоссарии](../standards/GLOSSARY.md), стандарты — в `standards/`, а этот
каталог отвечает за применимые знания, примеры и источники для ответов агентов.

## Структура

| Каталог | Назначение | Статус |
| --- | --- | --- |
| [`kb/mango-product-docs/`](mango-product-docs/README.md) | База знаний продуктов Mango Office: PDF/веб-источники, обработанные Markdown-чанки и инструкции использования. | Рабочий product-docs namespace |
| [`kb/fragments/`](fragments/README.md) | Задел под атомарные фрагменты будущего векторного RAG; сейчас product-docs чанки живут в `kb/mango-product-docs/processed/`. | Оставить в `kb/`, не переносить в product-docs |
| [`kb/practices/`](practices/README.md) | Ручные практики и методики анализа, не привязанные к конкретному продукту Mango Office. | Оставить в `kb/`, не переносить в product-docs |
| [`kb/industry-taxonomy/`](industry-taxonomy/README.md) | Industry Taxonomy: machine-readable реестр отраслевой классификации `Domain -> Capability -> Feature -> Function`. | Рабочий industry taxonomy namespace |
| [`kb/mango-taxonomy/`](mango-taxonomy/README.md) | Mango Taxonomy Registry: Official Layer, Internal Layer и mapping к Industry Taxonomy. | Рабочий mango taxonomy namespace |

## Как использовать?

Для фактов о продуктах Mango Office идите в
[`kb/mango-product-docs/README.md`](mango-product-docs/README.md): там описаны
`sources/`, `processed/`, [`USAGE.md`](mango-product-docs/USAGE.md) и
[`UPLOAD-GUIDE.md`](mango-product-docs/UPLOAD-GUIDE.md).

Для классификации продуктов Mango Office используйте
[`kb/mango-taxonomy/README.md`](mango-taxonomy/README.md): там описаны публичный Official Layer,
внутренний Internal Layer `Product -> Service -> Module -> Function` и mapping к
Industry Taxonomy.

Для отраслевой классификации используйте
[`kb/industry-taxonomy/README.md`](industry-taxonomy/README.md): там описан machine-readable
реестр `Domain -> Capability -> Feature -> Function`, на который ссылается
Mango mapping.

Для ручных практик используйте `kb/practices/` и цитируйте запись стабильным
адресом вида:

```markdown
[KB: <slug>](kb/<path>#<anchor>)
```

Для будущих атомарных чанков используйте `kb/fragments/`; пока этот слой пуст,
потому что разделы в `kb/mango-product-docs/processed/` уже являются
достаточными pre-RAG чанками.

## Быстрый старт

Проверить структуру KB README после миграции product docs:

```bash
python3 scripts/validate_issue_144_kb_structure_readmes.py
```

Проверить весь лёгкий KB-контур:

```bash
make kb-validate
```

Проверить планы обработки всех product-docs источников без чтения PDF:

```bash
make kb-source-plan-all
```

## Индекс записей

| Тема | Файл | Когда применять |
| --- | --- | --- |
| Анализ с опорой на источники | [practices/source-backed-analysis.md](practices/source-backed-analysis.md) | Любой нормативный вывод; проверка существования цитируемого стандарта. |

## Добавление записи

Для ручной практики создайте файл в `kb/practices/` с frontmatter (`id`,
`status`, `sources`) и добавьте строку в индекс выше. Если запись вводит новый
термин, предложите его в глоссарий через issue, а не определяйте локально в KB.

Для продуктовой документации используйте
[`kb/mango-product-docs/UPLOAD-GUIDE.md`](mango-product-docs/UPLOAD-GUIDE.md):
новые источники добавляются в `kb/mango-product-docs/sources/`, а результат
генерируется в `kb/mango-product-docs/processed/`.

## Решение по границам

История Git для `kb/fragments/` и `kb/practices/` проверена в
[`docs/audit/issue-144-kb-structure.md`](../docs/audit/issue-144-kb-structure.md).
Оба каталога остаются независимыми материалами KB: `fragments/` — будущий слой
RAG, `practices/` — ручные практики. Их не нужно переносить в
`kb/mango-product-docs/`, потому что product-docs namespace отвечает только за
документацию продуктов Mango Office и её pipeline.

## Связанные документы

- [`kb/mango-product-docs/README.md`](mango-product-docs/README.md) — структура
  продуктовой БЗ.
- [`kb/mango-product-docs/USAGE.md`](mango-product-docs/USAGE.md) — как агент
  читает извлечённую БЗ.
- [`kb/mango-product-docs/UPLOAD-GUIDE.md`](mango-product-docs/UPLOAD-GUIDE.md) —
  как добавлять и обновлять документы.
- [`kb/industry-taxonomy/README.md`](industry-taxonomy/README.md) — machine-readable Industry
  Taxonomy registry.
- [`kb/mango-taxonomy/README.md`](mango-taxonomy/README.md) — machine-readable Mango Taxonomy
  Registry и crosswalk к Industry Taxonomy.
- [`docs/audit/issue-144-kb-structure.md`](../docs/audit/issue-144-kb-structure.md) —
  проверка истории `fragments/` и `practices/`.
- [`docs/kb-experiment-report.md`](../docs/kb-experiment-report.md) —
  методология и оценка качества извлечения PDF в БЗ.
- [`standards/kb-standard.md`](../standards/kb-standard.md) — правила цитат,
  границы KB и pre-RAG retrieval.
