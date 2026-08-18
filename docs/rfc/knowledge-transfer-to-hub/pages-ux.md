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
  - "docs/adr/010-pages-ux.md"
  - "standards/pages-ux-standard.md"
  - "docs/rfc/rfc-to-hub-001-knowledge-transfer.md"
---

# Передача знаний: UX дерева процессов на GitHub Pages

## Название практики

Разделение **слоя данных** и **слоя отображения** для документ-сайта: дерево
процессов из `process-tree.json` (с флагом покрытия) рендерится так, что
пользователь видит только реально покрытые узлы.

## Описание (что, как, зачем)

- **Что.** UX-паттерн для навигации по графу знаний: данные (структура +
  метаданные покрытия) отделены от представления (что и как показывать).
- **Как.** [ADR #010](../../adr/010-pages-ux.md) и стандарт
  [`standards/pages-ux-standard.md`](../../../standards/pages-ux-standard.md):
  - **слой данных** — `process-tree.json`: каждый узел несёт `hasPrompts` и
    `coverage.kind` ∈ {`direct`, `support`, `gap`, `archive`, `manual`};
  - **слой отображения** — показывает только узлы с промптами; порог дерева
    (> 20 узлов) переключает компактный режим отображения.
- **Зачем.** Сайт не «тонет» в незаполненных узлах: видно покрытое, помечено
  отсутствующее (gap), архив скрыт. Прозрачное покрытие промптами без ручной
  поддержки списков.

## Обоснование (почему полезно другим проектам)

Любой спок/Хаб с графом знаний на GitHub Pages сталкивается с тем же: как
показать большой граф, не перегружая, и как честно отметить пробелы. Паттерн
«данные с метаданными покрытия / отображение по покрытию» — переиспользуемый
рецепт визуализации graph-of-practices Хаба
([`executable-documentation-standard.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/6ddffdfff693d8279792cd1e9c4c5d94ee0dffcf/standards/executable-documentation-standard.md)).
`coverage.kind` = gap прямо поддерживает анти-инфляционный принцип Хаба: пробелы
видны, а не маскируются пустыми страницами.

## Примеры использования

- **Сайт каталога промптов Mango:** дерево операций/процессов показывает только
  покрытые узлы; gap-узлы маркируют, чего не хватает.
- **Хаб-навигатор practices:** тот же подход для отображения узлов графа практик
  с метаданными зрелости (Pattern/Standard) вместо `coverage.kind`.

## Что обобщить перед переносом (критерий C2)

Передавать **схему данных** (`hasPrompts` / `coverage.kind` / порог дерева) и
правило отображения, а конкретный `process-tree.json` Mango — как пример. Обобщить
`coverage.kind` так, чтобы значения настраивались под домен (для Хаба — статусы
жизненного цикла знаний).

## Ссылки

- ADR-носитель: [`docs/adr/010-pages-ux.md`](../../adr/010-pages-ux.md)
- Стандарт: [`standards/pages-ux-standard.md`](../../../standards/pages-ux-standard.md)
- Онтология (источник данных): [`ba-ontology.md`](ba-ontology.md)
- Umbrella-RFC: [`rfc-to-hub-001-knowledge-transfer.md`](../rfc-to-hub-001-knowledge-transfer.md)
