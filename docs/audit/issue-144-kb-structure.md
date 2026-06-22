---
status: draft
version: 0.1
updated: 2026-06-20
ai-generated: true
type: audit
scope: kb
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/144"
related_artifacts:
  - "kb/README.md"
  - "kb/mango-product-docs/README.md"
  - "kb/fragments/README.md"
  - "kb/practices/README.md"
---

# Аудит структуры `kb/` после миграции product docs

Проверка фиксирует решение по `kb/fragments/` и `kb/practices/` после переноса
продуктовой документации в `kb/mango-product-docs/`.

## Что проверено?

Команды истории:

```bash
git log --follow -- kb/fragments/
git log --follow -- kb/practices/
```

Дополнительно проверены `git log --all --name-status -- kb/fragments/` и
`git log --all --name-status -- kb/practices/`, чтобы увидеть изменения после
миграции issue #137.

## Находки

| Каталог | История | Вывод |
| --- | --- | --- |
| `kb/fragments/` | `2c766812695a1163b2e7f9cf4c4878dce9a75a1f` создал `kb/fragments/README.md` в issue #111 как будущий слой атомарных фрагментов/vector RAG. `f361fd5b91cec0493b39a3ed73f3322bb3d7d165` только обновил ссылку README при миграции product docs в issue #137. | Оставить в `kb/`: каталог не хранит product-docs источники или generated output, а описывает будущий RAG-слой поверх KB. |
| `kb/practices/` | `37dc51c0c2bb1e89642e841e4962407be02e445b` добавил `source-backed-analysis.md` в рамках ADR-007 / KB standard до миграции product docs. | Оставить в `kb/`: это ручная практика анализа, независимая от документации продуктов Mango Office. |

## Решение

Оставить в kb/ оба каталога:

- `kb/fragments/` — задел под будущие атомарные RAG-фрагменты;
- `kb/practices/` — ручные практики и методики, цитируемые по `kb-standard`.

Переносить их в `kb/mango-product-docs/` не нужно: product-docs namespace
отвечает за документацию Mango Office, `sources/`, `processed/`, `USAGE.md` и
`UPLOAD-GUIDE.md`.

История Git сохранена: в рамках issue #144 файлы не перемещались, поэтому
`git mv` не требовался.

## Чек-лист целостности

- [x] `kb/README.md` описывает `mango-product-docs/`, `fragments/`, `practices/`
      и taxonomy namespaces `industry-taxonomy/`, `mango-taxonomy/`.
- [x] `kb/mango-product-docs/README.md` создан и описывает product-docs
      структуру.
- [x] `kb/practices/README.md` создан для независимых ручных практик.
- [x] `kb/fragments/README.md` явно отделён от продуктовой документации.
- [x] История Git сохранена без перемещений.
