---
status: review
version: 0.1
updated: 2026-07-03
ai-generated: true
type: kb-state-report
scope: kb/processed
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/259"
---

# Отчет: Состояние БЗ после удаления PDF из LFS

## Executive Summary

База знаний в `kb/processed/` сохранилась как самостоятельный набор
сгенерированных артефактов: 1 126 Markdown-файлов, 1 116 файлов-разделов,
9 индексов, 9 `meta.json` и 3 906 извлеченных изображений. Общий объем
`kb/processed/` составляет 138M; по метаданным это 1 395 страниц источников и
924 795 токенов сгенерированного материала.

PDF-источники в рабочем дереве отсутствуют: `find . -iname '*.pdf'` и
`git ls-files '*.pdf'` не вернули файлов. Поэтому БЗ пригодна для чтения,
поиска, цитирования и анализа уже извлеченных разделов, но не пригодна для
перепарсинга, повторной верификации против оригиналов и обновления без повторного
добавления PDF.

Структура, индексы, метаданные, трассировка и изображения в `kb/processed/`
сохранились. Lightweight-валидация KB pipeline проверяет generated snapshot,
source provenance и manifest wiring без требования локальных PDF-payloads;
локальный `make kb-validate` проходит. Запуск извлечения по-прежнему требует
возврата реальных PDF-файлов.

## Метод проверки

Отчет составлен по состоянию рабочей копии на ветке
`issue-259-c669a0c27b56` 2026-07-03. PDF не восстанавливались, извлечение не
перезапускалось, структура `kb/processed/` не менялась.

Основные проверки:

- инвентаризация `find`, `du`, `ls` по `kb/processed/`;
- анализ `meta.json` через стандартный JSON-парсер Python;
- поиск PDF/LFS-упоминаний через `rg`;
- проверка пустых и минимальных Markdown-файлов через `find`;
- проверка локальных Markdown-ссылок на изображения;
- анализ source manifests в `kb/sources/`;
- локальный запуск `make kb-validate`;
- просмотр текущего лога CI `KB pipeline` для PR #260.

## Что сохранилось

### Общая структура

`kb/processed/` содержит четыре верхнеуровневых набора:

```text
kb/processed/
├── README.md
├── contact-center-manual-sample/
│   ├── index.md
│   ├── meta.json
│   ├── sections/
│   └── images/
├── mango-cc-manual/
│   ├── index.md
│   ├── meta.json
│   ├── sections/
│   └── images/
├── mango-lk-manual/
│   ├── index.md
│   ├── meta.json
│   ├── sections/
│   └── images/
└── mtalker/
    ├── index.md
    ├── meta.json
    ├── quick-start/
    ├── windows-mac-working/
    ├── windows-mac-settings/
    ├── windows-mac-admin/
    └── android-user-guide/
```

Для `mtalker` сохранена multi-document структура: общий индекс продукта и пять
вложенных БЗ, каждая со своим `index.md`, `meta.json`, `sections/` и `images/`.

### Количественная инвентаризация

| Набор | Размер | Markdown | Разделы | Изображения | Страницы | Токены | PDF-источники в метаданных |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `contact-center-manual-sample` | 64K | 8 | 7 | 1 | 7 | 1 923 | 1, отсутствует |
| `mango-cc-manual` | 60M | 233 | 232 | 1 771 | 614 | 429 951 | 6, отсутствуют |
| `mango-lk-manual` | 73M | 349 | 348 | 1 545 | 568 | 311 325 | 5, отсутствуют |
| `mtalker` | 6.1M | 535 | 529 | 589 | 206 | 181 596 | 5, отсутствуют |
| **Итого `kb/processed/`** | **138M** | **1 126** | **1 116** | **3 906** | **1 395** | **924 795** | **17, отсутствуют** |

Дополнительные счетчики:

- всего файлов в `kb/processed/`: 5 041;
- `index.md`: 9;
- `meta.json`: 9;
- файлов-разделов `sections/*.md`: 1 116;
- Markdown-файлов любого типа: 1 126.

### Содержимое ключевых каталогов

`mango-cc-manual` сохранил 232 раздела, 1 771 изображение, индекс на 72 816 байт
и `meta.json` на 129 775 байт. Начало `sections/` содержит ожидаемые файлы
`00-titulnaya-chast.md`, `01-nachalo-raboty.md`,
`02-registraciya-novogo-polzovatelya.md`, `03-vhod-v-sistemu.md`,
`04-glavnoe-okno-programmy.md`.

`mango-lk-manual` сохранил 348 разделов, 1 545 изображений, индекс на 99 341 байт
и `meta.json` на 194 462 байт.

`mtalker` сохранил общий product index и пять вложенных документов:

- `quick-start`: 7 разделов, 4 страницы, 16 изображений;
- `windows-mac-working`: 317 разделов, 122 страницы, 396 изображений;
- `windows-mac-settings`: 55 разделов, 19 страниц, 42 изображения;
- `windows-mac-admin`: 15 разделов, 9 страниц, 10 изображений;
- `android-user-guide`: 135 разделов, 52 страницы, 125 изображений.

`contact-center-manual-sample` сохранил синтетическую фикстуру: 7 разделов,
7 страниц, 1 изображение. В `meta.json` явно указано, что это синтетическая
фикстура, созданная потому что реальный `CC_manual_1.26.23.pdf` не загрузился
для issue #111.

### Индексы и метаданные

Сохранились:

- `kb/processed/README.md` с описанием контракта generated KB;
- `index.md` для каждого документа и вложенного документа;
- `meta.json` для каждого документа и product collection;
- трассировка из разделов к исходным PDF-путям, частям и страницам;
- счетчики страниц, разделов, изображений, токенов и источников;
- `source_sha256` в метаданных сгенерированных документов.

Секции остаются самодостаточными chunks: в frontmatter есть `pdf_section`,
`pdf_heading`, `pages`, `source`, `source_refs`, а в теле есть строка
`Трассировка`.

## Проверка целостности

### PDF-ссылки и source references

В `kb/processed/**/*.md` найдено 3 378 упоминаний `.pdf`. Это не Markdown-ссылки
на PDF: отдельная проверка Markdown-гиперссылок вида `[...](...pdf)` вернула 0.
Найденные упоминания являются provenance-полями и человекочитаемой трассировкой,
например:

- `source: kb/sources/mango-cc-manual/CC_manual_1.26.23-part-*.pdf`;
- `source_refs: [{"source_pdf": "...pdf", ...}]`;
- строки `Трассировка` в разделах;
- блоки `Источник БЗ` в `index.md`.

Все 17 уникальных PDF-источников, на которые ссылается `kb/processed/`, сейчас
отсутствуют в рабочем дереве:

- 1 synthetic/sample source PDF;
- 6 частей `mango-cc-manual`;
- 5 частей `mango-lk-manual`;
- 5 документов `mtalker`.

### LFS-упоминания

В `kb/processed/**/*.md` не найдено упоминаний `lfs`.

`.gitattributes` продолжает объявлять PDF как LFS-файлы:

```text
*.pdf filter=lfs diff=lfs merge=lfs -text
```

Локально команда `git lfs ls-files` недоступна, потому что `git lfs` не
установлен в контейнере. При этом `git ls-files '*.pdf'` и поиск по файловой
системе не нашли ни одного PDF.

### Пустые и минимальные файлы

Проблем не найдено:

- пустых `*.md` в `kb/processed/`: 0;
- `*.md` меньше 100 байт: 0.

### Изображения

Локальная проверка Markdown image references в `kb/processed/**/*.md` не нашла
битых ссылок на изображения: 0 missing image references. Файлы `images/`
сохранились и соответствуют ссылкам из Markdown-разделов.

## Анализ зависимостей

### Manifest-файлы

Сохранились 23 JSON-файла в `kb/`: 9 в `kb/processed/` и 14 в `kb/sources/`.
YAML-manifest в `kb/` не найден.

В `kb/sources/` сохранены source manifests, включая:

- `kb/sources/mango-cc-manual/meta.json`;
- `kb/sources/mango-lk-manual/meta.json`;
- `kb/sources/mtalker/meta.json`;
- manifests для интеграций, SSO, SIP trunk, speech analytics, wallboard и других
  источников.

Среди `kb/sources/*/meta.json` восемь manifest-групп перечисляют 24 ожидаемых
PDF-файла. Ни один из этих PDF-файлов сейчас не присутствует. Отдельный
`kb/sources/contact-center-manual/source.md` также описывает ожидаемый
`CC_manual_1.26.23.pdf` со статусом `pending-source-file`.

### Скрипты и workflow

Сохранились:

- `scripts/kb/extract.py`: PDF -> `sections/*.md`, `index.md`, `meta.json`,
  `images/`;
- `scripts/kb/process_sources.py`: manifest-driven запуск для `single`,
  `multi_part`, `multi_document`;
- `scripts/kb/tokens.py`;
- `scripts/kb/make_sample_pdf.py`;
- `scripts/kb/requirements.txt`;
- validators `scripts/validate_issue_111_*`, `115_*`, `117_*`, `121_*`;
- Make targets `kb-extract`, `kb-source-plan`, `kb-source-extract`, `kb-mango`,
  `kb-lk`, `kb-mtalker`, `kb-validate`;
- workflow `.github/workflows/kb.yml`.

### Документация процесса

Сохранились README-файлы:

- `kb/README.md`;
- `kb/processed/README.md`;
- `kb/sources/README.md`;
- `kb/fragments/README.md`;
- `kb/sources/web-links/README.md`;
- `scripts/kb/README.md`.

`kb/sources/README.md` по-прежнему описывает, что PDF должны лежать в
`kb/sources/<slug>/`, управляться через Git LFS и обрабатываться через локальный
Makefile или workflow `KB pipeline`.

## Что потеряно

### PDF-источники

Подтверждено отсутствие PDF-файлов:

- в рабочем дереве нет `*.pdf`;
- в `git ls-files '*.pdf'` нет tracked PDF;
- source manifests и processed metadata указывают на PDF-пути, которых нет на
  диске.

Для текущей `kb/processed/` потеряны исходные байты 17 PDF-файлов, на основании
которых были созданы сохраненные generated artifacts.

### Возможность перепарсинга

Без PDF нельзя воспроизвести текущую БЗ через:

- `make kb-mango`;
- `make kb-lk`;
- `make kb-mtalker`;
- `make kb-source-extract SOURCE_DIR=...`;
- workflow `KB pipeline` в режиме извлечения.

Manifest-файлы подсказывают ожидаемые имена, порядок частей, версии и страницы,
но не заменяют сами PDF.

### Возможность верификации

Сохраненная БЗ содержит трассировку до путей, частей и страниц, но оригинальные
страницы недоступны. Поэтому нельзя:

- сверить извлеченный текст с PDF;
- проверить полноту таблиц и изображений против оригинала;
- подтвердить корректность outline boundaries на исходном документе;
- пересчитать или проверить `source_sha256` против локальных PDF-байтов.

### Возможность обновления

Обновление БЗ при выходе новой версии PDF невозможно в текущем состоянии без
повторного добавления новых PDF-источников. При этом существующие `output_slug`
и manifests позволяют понять, куда должна быть перегенерирована БЗ после
возврата источников.

## Последствия

### Что можно делать сейчас

- Читать `kb/processed/*/index.md` как карту разделов.
- Использовать `sections/*.md` как chunks для анализа, поиска и цитирования.
- Ссылаться на стабильные Markdown-пути и заголовки.
- Использовать извлеченные изображения, потому что локальные image references
  не битые.
- Определять происхождение разделов по сохраненным `source_refs`, номерам частей
  и страницам.
- Оценивать объем БЗ по сохраненным счетчикам страниц, секций, изображений и
  токенов.

### Что нельзя делать без восстановления источников

- Перегенерировать БЗ из PDF.
- Проверить, что Markdown точно соответствует PDF-оригиналу.
- Исправить ошибки парсинга через корректный rerun pipeline.
- Обновить БЗ на новую версию руководства.
- Выполнить source-backed проверку, которая читает оригинальные PDF-payloads.

## Риски

### Критические

- **Невоспроизводимость БЗ.** Generated artifacts сохранены, но source -> output
  цепочка разорвана из-за отсутствия PDF.
- **Невозможность source-backed верификации.** Ссылки на страницы и части
  сохранены, но проверить их против оригинала нельзя.

### Средние

- **Риск накопления ошибок парсинга.** Если в текущих chunks есть ошибки
  извлечения, исправлять их без PDF можно только вручную, что противоречит
  контракту `kb/processed/` как generated layer.
- **Риск устаревания.** При новой версии руководств невозможно обновить
  `kb/processed/<slug>/` тем же процессом, пока не появятся источники.
- **Риск неполной dependency-карты.** Manifests сохранили имена и параметры, но
  не все source manifests имеют локальные payloads или web URL.

### Низкие

- **Битые image references не обнаружены.** Риск потери изображений внутри
  `kb/processed/` сейчас низкий.
- **Пустые Markdown-файлы не обнаружены.** Риск очевидной деградации generated
  Markdown слоя сейчас низкий.

## Рекомендации

### Немедленные действия

1. Зафиксировать этот отчет как текущий baseline состояния после LFS cleanup.
2. Считать `kb/processed/` последним сохраненным snapshot, а не воспроизводимым
   output, пока PDF отсутствуют.
3. Не редактировать `kb/processed/**` вручную: текущая документация уже задает
   правило менять источник и перезапускать извлечение.
4. Сохранять разделение lightweight-валидации generated artifacts и
   source-backed проверок, которые требуют реальные PDF-payloads.

### Долгосрочные considerations для будущей задачи

- Определить политику хранения source payloads и external source locations для
  БЗ, чтобы source-backed верификация не зависела только от Git LFS history.
- Хранить machine-readable manifest состояния: какие sources обязательны для
  rerun, какие optional, какие intentionally removed.
- Разделить проверки generated artifacts и проверки source availability, чтобы
  cleanup источников не маскировал состояние уже извлеченной БЗ.

## Локальная и CI-валидация

Локально:

```text
make kb-validate
issue-111 KB pipeline validation: PASS
issue-115 KB mango pipeline validation: PASS
issue-117 KB traceability validation: PASS
issue-121 KB multi-file validation: PASS
```

CI до исправления validation contract:

- workflow: `KB pipeline`;
- run: `28657113496`;
- created at: `2026-07-03T11:18:10Z`;
- head SHA: `8feff699ffc72847083ad13b16c47a53ed925b26`;
- result: failure;
- root cause in log: the same six missing `mango-cc-manual` PDF parts.

После исправления lightweight validation contract `make kb-validate` не требует
локальные PDF-payloads и продолжает проверять generated artifacts, manifest
source paths и provenance. Реальный запуск `scripts/kb/process_sources.py`
без `--dry-run` по-прежнему завершается ошибкой, если PDF-файлы отсутствуют.

## Definition of Done

- [x] Инвентаризация `kb/processed/` выполнена.
- [x] Проверка целостности выполнена.
- [x] Анализ зависимостей выполнен.
- [x] Отчет составлен в формате Executive Summary + детали.
- [x] Отчет зафиксирован как
  `docs/report/2026-07-03-kb-state-after-lfs-cleanup.md`.
- [x] Локальная проверка отчета `git diff --check` прошла.
- [x] Полный `make kb-validate` проходит после разделения lightweight checks и
  source-backed payload checks.
- [x] Структура `kb/processed/` не изменялась.
- [x] PDF не восстанавливались и БЗ не перепарсивалась.
- [x] Задача переведена в состояние `review` через frontmatter отчета.
