---
status: draft
version: 0.3
updated: 2026-06-20
ai-generated: true
type: kb-sources-guide
scope: kb/mango-product-docs/sources
related_artifacts:
  - "scripts/kb/extract.py"
  - "kb/mango-product-docs/processed/README.md"
  - "docs/kb-experiment-report.md"
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/111"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/117"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/119"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/121"
---

# `kb/mango-product-docs/sources/` — ручной ввод источников + инструкция по пополнению БЗ

Это **единственная человекочитаемая инструкция** конвейера БЗ (issue #111, ФТ-7):
как добавить документ, запустить обработку, проверить результат, обновить версию,
добавить веб-ссылку. Сами артефакты БЗ (`kb/mango-product-docs/processed/`) предназначены для чтения
**агентами**, а не людьми — для людей собирается сайт (GitHub Pages).

> **Почему имя `kb/`, а не `mango-kc`.** Имя выбрано **нейтральным и
> универсальным** (knowledge base), без привязки к продукту/бренду — по
> требованию ФТ-4. Подкаталоги тоже нейтральны: `sources` (вход), `processed`
> (результат извлечения), `fragments` (будущие атомарные чанки для RAG).

## Куда что класть

```
kb/mango-product-docs/sources/                      ← ВЫ кладёте файлы сюда (ручной ввод)
├── README.md                    ← этот файл (инструкция)
├── contact-center-manual/       ← один каталог = один документ-источник
│   └── source.md                ← манифест: что за документ, версия, веб-ссылка
├── contact-center-manual-sample/← синтетическая фикстура для эксперимента
│   └── CC_manual_sample.fixture.pdf
└── web-links/                   ← источники-ссылки (без файла), см. его README
```

Один подкаталог в `kb/mango-product-docs/sources/<slug>/` теперь означает **один управляемый набор
источников**. Он может быть:

- `single` — один PDF = одна БЗ;
- `multi_part` — несколько PDF-частей = один логический документ и одна БЗ;
- `multi_document` — несколько самостоятельных руководств по продукту = общий
  индекс продукта и отдельная БЗ на каждый документ.

Файл `meta.json` является управляющим манифестом. `source.md` остаётся допустимым
человекочитаемым описанием для старых/простых источников, но автоматический
конвейер `scripts/kb/process_sources.py` читает именно `meta.json`.
PDF-файлы в репозитории ведутся через Git LFS (`.gitattributes`:
`*.pdf filter=lfs ...`).

---

## `meta.json`: обязательная логика обработки

### Сценарий 1: `single`

```json
{
  "name": "Название руководства",
  "version": "1.0",
  "processing_mode": "single",
  "output_slug": "product-manual",
  "doc_code": "PM",
  "source_files": ["manual.pdf"]
}
```

Результат: `kb/mango-product-docs/processed/product-manual/`.

### Сценарий 2: `multi_part`

```json
{
  "name": "Контакт-центр MANGO OFFICE - Руководство пользователя",
  "version": "1.26.23",
  "processing_mode": "multi_part",
  "output_slug": "mango-cc-manual",
  "doc_code": "CC",
  "source_files": [
    "CC_manual_1.26.23-part-1.pdf",
    "CC_manual_1.26.23-part-2.pdf",
    "CC_manual_1.26.23-part-3.pdf"
  ],
  "parts": 3,
  "split_method": "logical_chapters"
}
```

Результат: один каталог `kb/mango-product-docs/processed/mango-cc-manual/`, сквозная пагинация,
`source_refs` на конкретную часть и локальные страницы.

### Сценарий 3: `multi_document`

```json
{
  "name": "Mango Talker - Комплект документации",
  "version": "23.08.2024",
  "processing_mode": "multi_document",
  "output_slug": "mtalker",
  "documents": [
    {
      "file_name": "mTalker_Quick_start.pdf",
      "output_slug": "quick-start",
      "doc_code": "MTALKER-QS",
      "title": "Mango Talker для Windows/Mac - Быстрый старт"
    },
    {
      "file_name": "UserGuide_mTalker_4Mobile.pdf",
      "output_slug": "android-user-guide",
      "doc_code": "MTALKER-MOB",
      "title": "Mango Talker для Android - Руководство пользователя"
    }
  ]
}
```

Результат:

```
kb/mango-product-docs/processed/mtalker/
├── index.md
├── meta.json
├── quick-start/
│   ├── index.md
│   ├── meta.json
│   └── sections/
└── android-user-guide/
    ├── index.md
    ├── meta.json
    └── sections/
```

Это гибридная стратегия: есть общая мета-информация по продукту, но каждый
самостоятельный документ остаётся отдельной БЗ с собственными цитатами,
страницами, токенами и трассировкой.

---

## Как pipeline выбирает логику

1. Если в `meta.json` задан `processing_mode`, используется он.
2. Если режим не задан, но есть ровно один объект `documents`, режим считается
   `single` и результат пишется в `kb/mango-product-docs/processed/<slug>/`.
3. Если режим не задан, но есть несколько объектов `documents`, режим считается
   `multi_document`.
4. Если есть `parts > 1` или несколько `source_files`, режим считается
   `multi_part`.
5. Иначе режим считается `single`.

Для новых источников всегда задавайте `processing_mode` явно. Автоопределение
оставлено только для обратной совместимости.

---

## Сценарии обновления

### Сценарий 4: 1 → N

Было:

```json
{
  "processing_mode": "single",
  "output_slug": "mango-lk-manual",
  "source_files": ["LK_manual.pdf"]
}
```

Стало:

```json
{
  "processing_mode": "multi_part",
  "output_slug": "mango-lk-manual",
  "source_files": [
    "LK_manual_part-1.pdf",
    "LK_manual_part-2.pdf",
    "LK_manual_part-3.pdf"
  ]
}
```

`output_slug` не меняется, поэтому старая БЗ перегенерируется в том же каталоге.
Историю изменения хранит git, дублей в `kb/mango-product-docs/processed/` не появляется.

### Сценарий 5: N → 1

Меняется только `processing_mode` и список `source_files`, `output_slug` остаётся
прежним. Pipeline снова пишет в тот же `kb/mango-product-docs/processed/<slug>/` и заменяет
содержимое `sections/`, `images/`, `index.md`, `meta.json`.

### Сценарий 6: добавление или удаление файла в `multi_document`

Добавьте или удалите объект в массиве `documents`. При запуске
`process_sources.py`:

- новые документы получают новые вложенные каталоги;
- существующие документы с тем же `output_slug` перегенерируются без потери
  истории;
- удалённые/переименованные сгенерированные дочерние каталоги с `meta.json`
  удаляются из коллекции, чтобы не оставалось устаревших БЗ.

---

## Команды для manifest-driven режима

Проверить план без чтения PDF:

```bash
make kb-source-plan SOURCE_DIR=kb/mango-product-docs/sources/mtalker
```

Проверить план для всех `meta.json`:

```bash
make kb-source-plan-all
```

Запустить извлечение по `meta.json`:

```bash
make kb-source-extract SOURCE_DIR=kb/mango-product-docs/sources/mtalker
```

Запустить извлечение всех источников:

```bash
make kb-source-extract-all
```

Готовый target для текущего комплекта Mango Talker:

```bash
make kb-mtalker
```

Если локально PDF отображаются как текст `version https://git-lfs.github.com/...`,
это LFS pointer, а не PDF. Выполните `git lfs pull` или запускайте workflow
**KB pipeline** с checkout `lfs: true`.

---

## Как добавить новый файл в БЗ (пошагово)

1. **Создайте каталог документа** с нейтральным slug-именем (латиница, дефисы):

   ```bash
   mkdir -p kb/mango-product-docs/sources/cc-manual
   ```

2. **Положите файл** в этот каталог, например `kb/mango-product-docs/sources/cc-manual/CC_manual_1.26.23.pdf`.

3. **Создайте манифест** `kb/mango-product-docs/sources/cc-manual/source.md` (скопируйте шаблон из
   [`contact-center-manual/source.md`](contact-center-manual/source.md)): название,
   версия, дата, веб-ссылка на оригинал, кратко о содержании.

4. **Запустите обработку** (см. следующий раздел).

5. **Проверьте результат** и закоммитьте `kb/mango-product-docs/sources/<slug>/` **и**
   `kb/mango-product-docs/processed/<slug>/` одним PR.

---

## Как обновлять PDF через Git LFS

Большие PDF нельзя загружать через веб-интерфейс GitHub: так легко получить
обычный blob или сломать LFS-указатель. Используйте Codespace или локальный Git
с установленным Git LFS.

```bash
git lfs install
git lfs pull
git lfs ls-files
```

Если LFS ещё не был включён для PDF, выполните один раз:

```bash
git lfs track "*.pdf"
git add .gitattributes
```

При замене руководства:

1. Скопируйте новый PDF или все PDF-части в `kb/mango-product-docs/sources/<slug>/`.
2. Обновите `meta.json` или `source.md`: `version`, `upload_date`, `parts`,
   `total_pages`, `file_size_mb`, `split_method`.
3. Проверьте, что PDF попали в LFS: `git lfs ls-files kb/mango-product-docs/sources/<slug>`.
4. Перезапустите извлечение в тот же `kb/mango-product-docs/processed/<slug>/`.
5. Закоммитьте источник, метаданные и регенерированный `kb/mango-product-docs/processed/<slug>/`.

Если один PDF заменён несколькими частями, перечисляйте части в порядке страниц:
`part-1.pdf part-2.pdf ...`. Сквозная пагинация появится в `meta.json.sections`
и `source_refs`, а локальные страницы каждой части сохранятся отдельно.

---

## Как запустить обработку

### Локально (Makefile)

```bash
python3 -m pip install -r scripts/kb/requirements.txt

make kb-extract SRC=kb/mango-product-docs/sources/cc-manual/CC_manual_1.26.23.pdf \
                OUT=kb/mango-product-docs/processed/cc-manual \
                CODE=CC TITLE="Контакт-центр MANGO OFFICE" VERSION=1.26.23
```

Для multi-part PDF:

```bash
make kb-extract \
    SRCS="kb/mango-product-docs/sources/lk-manual/part-1.pdf kb/mango-product-docs/sources/lk-manual/part-2.pdf" \
    OUT=kb/mango-product-docs/processed/lk-manual \
    CODE=LK TITLE="Виртуальная АТС MANGO OFFICE" VERSION=1.21
```

### Локально (напрямую)

```bash
python3 scripts/kb/extract.py kb/mango-product-docs/sources/cc-manual/CC_manual_1.26.23.pdf \
    --out kb/mango-product-docs/processed/cc-manual \
    --doc-code CC --doc-title "Контакт-центр MANGO OFFICE" --doc-version 1.26.23
```

Скрипт также принимает несколько PDF-путей перед `--out`; страницы в результате
будут сквозными, а `source_refs` сохранит точный файл-часть и локальные страницы.

### Через GitHub Actions (без локального окружения)

Actions → **KB pipeline** → *Run workflow* → укажите `source`, `out`, `doc_code`,
`doc_title`, `doc_version`. Для multi-part PDF перечислите пути в `source` через
пробел в порядке страниц. По умолчанию workflow настроен на реальное руководство
КЦ из issue #119:

- `source`: `kb/mango-product-docs/sources/mango-cc-manual/CC_manual_1.26.23-part-1.pdf ... part-6.pdf`
- `out`: `kb/mango-product-docs/processed/mango-cc-manual`

Workflow делает checkout с `lfs: true`, поставит зависимости, выполнит извлечение
и приложит результат артефактом запуска. Если нужно сразу закоммитить результат в
текущую ветку, установите `commit_result=true`; иначе скачайте артефакт и
закоммитьте его отдельным PR либо запустите извлечение локально. Детали —
[`.github/workflows/kb.yml`](../../.github/workflows/kb.yml).

---

## Как проверить результат (качество извлечения)

1. **Структурная проверка** (как в CI, только stdlib):

   ```bash
   make kb-validate            # = python3 scripts/validate_issue_111_kb_pipeline.py
   ```

2. **Глазами откройте** `kb/mango-product-docs/processed/<slug>/index.md` — это карта разделов. Все
   разделы на месте? Номера/страницы верны?

3. **Откройте 1–2 раздела** `kb/mango-product-docs/processed/<slug>/sections/*.md`: кириллица
   читаема (не «мусор»)? Таблицы — настоящими Markdown-таблицами? Картинки
   подхватились в `images/`?

4. **Сверьте токены**: `cat kb/mango-product-docs/processed/<slug>/meta.json` — поля `tokens_total`,
   `tokens_index`, `token_method`. Так измеряется экономия «весь документ vs
   один раздел» (см. [`kb/mango-product-docs/USAGE.md`](../USAGE.md)).

5. **Сверьте трассировку**: в `meta.json` проверьте `sources`, `source_pdfs`,
   `part_count`, а в любом `sections/*.md` — frontmatter `pdf_section`,
   `source_refs` и строку `Трассировка`.

> ⚠️ **Кириллица как «мусор» (nnnn).** Если текст извлёкся набором квадратов/
> «n» — у PDF нет ToUnicode-карты шрифтов (типично для сканов и некоторых
> экспортов). Это известная ловушка; способы обхода (OCR/иной экстрактор) — в
> [`docs/kb-experiment-report.md`](../../../docs/kb-experiment-report.md).

---

## Как обновить документ (новая версия PDF)

1. Положите новый файл или PDF-части рядом со старым набором, обновите
   `version`/`date` в `source.md` или `meta.json`.
2. Если изменилась разбивка на части, обновите `parts`, `total_pages`,
   `split_method` и команду/Actions input `source`.
3. Перезапустите извлечение **в тот же** `--out` (каталог пересоздаётся целиком —
   diff покажет ровно, что изменилось между версиями).
4. Проверьте и закоммитьте. Историю версий хранит git; при необходимости
   зафиксируйте изменения в `CHANGELOG.md`.

---

## Как добавить ссылку на веб-ресурс

Если источник — веб-страница (а не файл), оформите его в
[`kb/mango-product-docs/sources/web-links/`](web-links/README.md): создайте `*.md`-манифест со
ссылкой, датой обращения и (при необходимости) сохранённой выжимкой. Подробности
и шаблон — в README этого каталога.

---

## Troubleshooting

- `Git LFS pointer checked out instead of PDF bytes`: локально нет реального PDF,
  только LFS pointer. Установите Git LFS и выполните `git lfs pull` или запустите
  workflow **KB pipeline**, где checkout настроен с `lfs: true`.
- `single mode requires exactly one PDF`: в `processing_mode: "single"` должен
  быть ровно один путь в `source_files`.
- `multi_part mode requires 2+ PDFs`: для физически разделённого руководства
  перечислите все части в `source_files` в порядке страниц.
- `duplicate output_slug`: в `multi_document` каждый документ должен иметь
  уникальный `output_slug`, потому что это имя вложенной БЗ.
- БЗ устарела после удаления файла: удалите документ из `documents` и запустите
  `make kb-source-extract SOURCE_DIR=...`; сгенерированный дочерний каталог с
  `meta.json` будет удалён.

---

## Что НЕ нужно делать

- ❌ Не кладите большие исходные PDF в произвольные места репозитория — только в
  `kb/mango-product-docs/sources/<slug>/` (так их найдут конвейер и `.gitignore`-правила).
- ❌ Не редактируйте `kb/mango-product-docs/processed/**` вручную — это генерируемый артефакт;
  правьте источник и перезапускайте извлечение.

## Источники

- Конвейер: [`scripts/kb/README.md`](../../../scripts/kb/README.md)
- Структура результата: [`kb/mango-product-docs/processed/README.md`](../processed/README.md)
- Отчёт об эксперименте: [`docs/kb-experiment-report.md`](../../../docs/kb-experiment-report.md)
