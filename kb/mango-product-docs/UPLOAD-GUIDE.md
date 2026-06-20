---
status: draft
version: 0.1
updated: 2026-06-20
ai-generated: true
type: kb-upload-guide
scope: kb
related_artifacts:
  - "kb/mango-product-docs/sources/README.md"
  - "scripts/kb/process_sources.py"
  - ".github/workflows/kb.yml"
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/131"
---

# KB upload guide

Короткая инструкция для пополнения `kb/mango-product-docs/sources/` и получения результата в
`kb/mango-product-docs/processed/`. Подробный контракт манифеста остаётся в
[`kb/mango-product-docs/sources/README.md`](sources/README.md).

## Как загрузить новый документ

1. Создайте каталог `kb/mango-product-docs/sources/<slug>/`, где `<slug>` короткий, стабильный и
   латиницей.
2. Положите PDF в этот каталог. Для больших PDF используйте Git LFS:

   ```bash
   git lfs install
   git lfs pull
   git lfs track "*.pdf"
   ```

3. Создайте `kb/mango-product-docs/sources/<slug>/meta.json`.
4. Проверьте план:

   ```bash
   make kb-source-plan SOURCE_DIR=kb/mango-product-docs/sources/<slug>
   ```

5. Запустите извлечение и проверку:

   ```bash
   make kb-source-extract SOURCE_DIR=kb/mango-product-docs/sources/<slug>
   make kb-validate
   ```

6. Коммитьте вместе `kb/mango-product-docs/sources/<slug>/`, `kb/mango-product-docs/processed/<slug>/` и изменения
   манифеста.

## Сценарии источников

`single`: один PDF даёт одну БЗ.

```json
{
  "name": "Название документа",
  "version": "1.0",
  "processing_mode": "single",
  "output_slug": "product-manual",
  "doc_code": "PM",
  "source_files": ["manual.pdf"]
}
```

`multi_part`: один логический документ разделён на несколько PDF-частей.

```json
{
  "name": "Название руководства",
  "version": "1.0",
  "processing_mode": "multi_part",
  "output_slug": "product-manual",
  "doc_code": "PM",
  "source_files": ["part-1.pdf", "part-2.pdf"]
}
```

`multi_document`: один продуктовый набор содержит несколько самостоятельных
документов; у каждого будет вложенная БЗ.

```json
{
  "name": "Product docs",
  "version": "1.0",
  "processing_mode": "multi_document",
  "output_slug": "product",
  "documents": [
    {
      "file_name": "quick-start.pdf",
      "output_slug": "quick-start",
      "doc_code": "PRD-QS",
      "title": "Quick start"
    }
  ]
}
```

Каталог без `meta.json` не попадает в manifest-driven pipeline. Если источник
ещё ожидает файл, оставьте это явно в `source.md` со статусом
`pending-source-file`.

## Как обновить существующий документ

Для замены файла:

1. Положите новый PDF в тот же `kb/mango-product-docs/sources/<slug>/`.
2. Обновите `version`, `source_files`, `pages_count` и описание в `meta.json`.
3. Оставьте прежний `output_slug`, если это та же БЗ.
4. Запустите `make kb-source-extract SOURCE_DIR=kb/mango-product-docs/sources/<slug>`.
5. Проверьте diff в `kb/mango-product-docs/processed/<slug>/` и `make kb-validate`.

Для разделения одного PDF на части используйте `multi_part` и перечислите части
в порядке страниц. Для объединения частей обратно в один PDF верните
`processing_mode` в `single` и оставьте тот же `output_slug`.

Для добавления или удаления документа в `multi_document` измените массив
`documents`. Удалённые сгенерированные дочерние каталоги с `meta.json` будут
очищены при следующем запуске `process_sources.py`.

## Как запустить pipeline

Локально для одного источника:

```bash
make kb-source-extract SOURCE_DIR=kb/mango-product-docs/sources/<slug>
```

Локально для всех источников:

```bash
make kb-source-extract-all
```

Через GitHub Actions: **Actions → KB pipeline → Run workflow**.

- `source_dir=all` обрабатывает все `kb/mango-product-docs/sources/*/meta.json`.
- `source_dir=kb/mango-product-docs/sources/<slug>` обрабатывает один источник.
- `commit_result=true` коммитит `kb/mango-product-docs/processed` обратно в текущую ветку.
- При push в `main` с изменениями в `kb/mango-product-docs/sources/` pipeline автоматически
  запускает `python3 scripts/kb/process_sources.py --all`.

## Как проверить результат

1. Убедитесь, что для источника есть каталог результата:
   `kb/mango-product-docs/processed/<output_slug>/`.
2. Для каждой документной БЗ должны быть `index.md`, `meta.json`, `sections/` и
   `images/`.
3. В `meta.json` проверьте `source_pdfs`, `section_count`, `tokens_total` и
   `sections[*].source_refs`.
4. Откройте 1-2 файла из `sections/`: должна быть строка `Трассировка`.
5. Запустите:

   ```bash
   make kb-validate
   ```
