---
status: draft
version: 0.1
updated: 2026-06-20
ai-generated: true
type: kb-product-docs-readme
scope: kb/mango-product-docs
related_artifacts:
  - "kb/mango-product-docs/sources/README.md"
  - "kb/mango-product-docs/processed/README.md"
  - "kb/mango-product-docs/USAGE.md"
  - "kb/mango-product-docs/UPLOAD-GUIDE.md"
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/137"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/144"
---

# База знаний продуктов Mango Office

`kb/mango-product-docs/` хранит продуктовую документацию Mango Office: исходные
PDF/веб-источники, обработанные Markdown-чанки и инструкции для агентов и людей.
Каталог отделён от общих практик KB и будущих taxonomy namespaces.

## Что это?

Это product-docs namespace после миграции issue #137. Здесь живёт только
документация продуктов и сервисов Mango Office вместе с pipeline-артефактами:
исходники, обработанные разделы, usage examples и upload guide.

## Структура

```
kb/mango-product-docs/
├── README.md
├── USAGE.md
├── UPLOAD-GUIDE.md
├── sources/
└── processed/
```

### `sources/`

Исходные PDF и source manifests. Каждый подкаталог описывает один управляемый
набор источников: `single`, `multi_part` или `multi_document`. PDF-файлы
хранятся через Git LFS, а правила пополнения описаны в
[`sources/README.md`](sources/README.md).

### `processed/`

Сгенерированные Markdown-артефакты для агентов: `index.md`, `meta.json`,
`sections/` и `images/`. Эти файлы не редактируются вручную; обновляйте
`sources/` и перезапускайте pipeline. Контракт результата описан в
[`processed/README.md`](processed/README.md).

### Инструкции

- [`USAGE.md`](USAGE.md) — как промпт или агент читает БЗ: индекс, выбор
  раздела, загрузка чанка, цитата.
- [`UPLOAD-GUIDE.md`](UPLOAD-GUIDE.md) — короткая инструкция загрузки и
  обновления документов.

## Как использовать?

Для ответа на вопрос о продукте агент сначала читает `processed/<doc>/index.md`,
выбирает релевантный раздел и загружает только нужный файл из `sections/`.
Факты цитируются по frontmatter и `meta.json`; полный пример есть в
[`USAGE.md`](USAGE.md).

Для добавления или обновления документа человек меняет `sources/<slug>/`,
проверяет план обработки и коммитит вместе source changes и generated
`processed/<slug>/`.

## Быстрый старт

Проверить планы всех source manifests без чтения PDF:

```bash
make kb-source-plan-all
```

Проверить лёгкий KB-контур:

```bash
make kb-validate
```

## Связанные каталоги

- [`kb/fragments/`](../fragments/README.md) — будущие атомарные фрагменты RAG; не
  является хранилищем product-docs источников.
- [`kb/practices/`](../practices/README.md) — ручные практики и методики; это не
  продуктовая документация.
- `kb/industry/` — будущая Industry Taxonomy.
- `kb/mango/` — будущая Mango Taxonomy.

## Как помочь?

Создайте GitHub Issue с контекстом, ожидаемым результатом и ссылкой на источник
или Pull Request по правилам [`CONTRIBUTING.md`](../../CONTRIBUTING.md).
