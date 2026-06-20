---
status: draft
version: 0.2
updated: 2026-06-19
ai-generated: true
type: kb-processed-guide
scope: kb/mango-product-docs/processed
related_artifacts:
  - "scripts/kb/extract.py"
  - "kb/mango-product-docs/USAGE.md"
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/111"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/117"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/119"
---

# `kb/mango-product-docs/processed/` — результаты извлечения (для агентов)

Сгенерированный, **machine-readable** слой БЗ: вывод
[`scripts/kb/extract.py`](../../../scripts/kb/extract.py). Эти файлы **не правят
руками** — правят источник в `kb/mango-product-docs/sources/` и перезапускают извлечение.

> Как промпт читает этот слой (индекс → выбор раздела → загрузка одного раздела →
> цитата → сравнение токенов) — c реальными сниппетами в
> [`kb/mango-product-docs/USAGE.md`](../USAGE.md).

## Структура одного документа

```
kb/mango-product-docs/processed/<doc-slug>/
├── index.md            ← карта разделов: раздел → файл → стр. → источник → токены
├── meta.json           ← метаданные: источники/части, sha256, счётчики, токены
├── sections/
│   ├── 00-...md        ← титульная часть
│   ├── 01-...md        ← раздел = чанк (frontmatter: id, pages, source_refs)
│   └── NN-...md
└── images/
    └── NN-...-1.png    ← извлечённые растровые изображения, ссылки — внутри разделов
```

## Контракт раздела-чанка

Каждый `sections/NN-slug.md` — самодостаточный фрагмент со стабильным адресом
(путь + якорь Markdown-заголовка) и frontmatter:

```yaml
id: <doc-slug>-NN-<section-slug>   # стабильный идентификатор (будущий chunk-id для RAG)
doc_code: CC                       # короткий код документа для цитат
section: "4"                       # номер раздела в документе
pdf_section: "4"                   # номер из PDF/outline или ближайший родитель
pdf_heading: "4 Обращения"         # исходный заголовок PDF/bookmark
pages: "5"                         # сквозные страницы документа
source_part: "1"                   # часть split-документа
source_pages: "ч.1: 5"             # локальные страницы внутри PDF-части
source_refs: '[{"source_pdf":"kb/mango-product-docs/sources/.../*.pdf","part":1,"pages":"5","global_pages":"5"}]'
tokens: 378                        # реальные токены (метод — token_method)
source: kb/mango-product-docs/sources/.../*.pdf       # первичный PDF-источник раздела
status: extracted
ai-generated: true
```

Сразу под H1 раздела выводится человекочитаемая строка `Трассировка` с номером
PDF-раздела, сквозными страницами, PDF-частями и локальными страницами. Для
multi-part документов `pages` остаётся сквозной пагинацией всего руководства, а
`source_refs` хранит точный путь к части и локальный диапазон страниц.

Это соответствует pre-RAG-механике стандарта БЗ (ADR-007, правила R1–R4):
каждый раздел = файл = чанк; `index.md` = retrieval-шаг; адреса `path#anchor`
станут chunk-id без переписывания, когда появится векторный RAG.

## Каталоги

| Документ | Статус |
| --- | --- |
| [`contact-center-manual-sample/`](contact-center-manual-sample/index.md) | извлечён из синтетической фикстуры (эксперимент issue #111) |
| [`mango-cc-manual/`](mango-cc-manual/index.md) | извлечён из 6 PDF-частей руководства КЦ v1.26.23 |
| [`mango-lk-manual/`](mango-lk-manual/index.md) | извлечён из 5 PDF-частей руководства ЛК ВАТС v1.21 |

## Источники

- Конвейер и оценка качества: [`docs/kb-experiment-report.md`](../../../docs/kb-experiment-report.md)
- Пополнение БЗ: [`kb/mango-product-docs/sources/README.md`](../sources/README.md)
