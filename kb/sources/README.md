---
status: draft
version: 0.1
updated: 2026-06-18
ai-generated: true
type: kb-sources-guide
scope: kb/sources
related_artifacts:
  - "scripts/kb/extract.py"
  - "kb/processed/README.md"
  - "docs/kb-experiment-report.md"
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/111"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/117"
---

# `kb/sources/` — ручной ввод источников + инструкция по пополнению БЗ

Это **единственная человекочитаемая инструкция** конвейера БЗ (issue #111, ФТ-7):
как добавить документ, запустить обработку, проверить результат, обновить версию,
добавить веб-ссылку. Сами артефакты БЗ (`kb/processed/`) предназначены для чтения
**агентами**, а не людьми — для людей собирается сайт (GitHub Pages).

> **Почему имя `kb/`, а не `mango-kc`.** Имя выбрано **нейтральным и
> универсальным** (knowledge base), без привязки к продукту/бренду — по
> требованию ФТ-4. Подкаталоги тоже нейтральны: `sources` (вход), `processed`
> (результат извлечения), `fragments` (будущие атомарные чанки для RAG).

## Куда что класть

```
kb/sources/                      ← ВЫ кладёте файлы сюда (ручной ввод)
├── README.md                    ← этот файл (инструкция)
├── contact-center-manual/       ← один каталог = один документ-источник
│   └── source.md                ← манифест: что за документ, версия, веб-ссылка
├── contact-center-manual-sample/← синтетическая фикстура для эксперимента
│   └── CC_manual_sample.fixture.pdf
└── web-links/                   ← источники-ссылки (без файла), см. его README
```

Один документ — один подкаталог в `kb/sources/<slug>/`. Туда же кладётся исходный
файл (`*.pdf`, в перспективе `*.docx`) и манифест `source.md` (см. шаблон в
[`contact-center-manual/source.md`](contact-center-manual/source.md)). Если
документ разделён на несколько PDF из-за размера, все части лежат в том же
подкаталоге и передаются в обработку в порядке страниц.

---

## Как добавить новый файл в БЗ (пошагово)

1. **Создайте каталог документа** с нейтральным slug-именем (латиница, дефисы):

   ```bash
   mkdir -p kb/sources/cc-manual
   ```

2. **Положите файл** в этот каталог, например `kb/sources/cc-manual/CC_manual_1.26.23.pdf`.

3. **Создайте манифест** `kb/sources/cc-manual/source.md` (скопируйте шаблон из
   [`contact-center-manual/source.md`](contact-center-manual/source.md)): название,
   версия, дата, веб-ссылка на оригинал, кратко о содержании.

4. **Запустите обработку** (см. следующий раздел).

5. **Проверьте результат** и закоммитьте `kb/sources/<slug>/` **и**
   `kb/processed/<slug>/` одним PR.

---

## Как запустить обработку

### Локально (Makefile)

```bash
python3 -m pip install -r scripts/kb/requirements.txt

make kb-extract SRC=kb/sources/cc-manual/CC_manual_1.26.23.pdf \
                OUT=kb/processed/cc-manual \
                CODE=CC TITLE="Контакт-центр MANGO OFFICE" VERSION=1.26.23
```

Для multi-part PDF:

```bash
make kb-extract \
    SRCS="kb/sources/lk-manual/part-1.pdf kb/sources/lk-manual/part-2.pdf" \
    OUT=kb/processed/lk-manual \
    CODE=LK TITLE="Виртуальная АТС MANGO OFFICE" VERSION=1.21
```

### Локально (напрямую)

```bash
python3 scripts/kb/extract.py kb/sources/cc-manual/CC_manual_1.26.23.pdf \
    --out kb/processed/cc-manual \
    --doc-code CC --doc-title "Контакт-центр MANGO OFFICE" --doc-version 1.26.23
```

Скрипт также принимает несколько PDF-путей перед `--out`; страницы в результате
будут сквозными, а `source_refs` сохранит точный файл-часть и локальные страницы.

### Через GitHub Actions (без локального окружения)

Actions → **KB pipeline** → *Run workflow* → укажите `source`, `out`, `doc_code`,
`doc_title`, `doc_version`. Для multi-part PDF перечислите пути в `source` через
пробел в порядке страниц. По умолчанию workflow настроен на реальное руководство
из issue #115:

- `source`: `kb/sources/mango-cc-manual/CC_manual_1.26.23_compressed.pdf`
- `out`: `kb/processed/mango-cc-manual`

Workflow поставит зависимости, выполнит извлечение и приложит результат артефактом
запуска. Если нужно сразу закоммитить результат в текущую ветку, установите
`commit_result=true`; иначе скачайте артефакт и закоммитьте его отдельным PR либо
запустите извлечение локально. Детали — [`.github/workflows/kb.yml`](../../.github/workflows/kb.yml).

---

## Как проверить результат (качество извлечения)

1. **Структурная проверка** (как в CI, только stdlib):

   ```bash
   make kb-validate            # = python3 scripts/validate_issue_111_kb_pipeline.py
   ```

2. **Глазами откройте** `kb/processed/<slug>/index.md` — это карта разделов. Все
   разделы на месте? Номера/страницы верны?

3. **Откройте 1–2 раздела** `kb/processed/<slug>/sections/*.md`: кириллица
   читаема (не «мусор»)? Таблицы — настоящими Markdown-таблицами? Картинки
   подхватились в `images/`?

4. **Сверьте токены**: `cat kb/processed/<slug>/meta.json` — поля `tokens_total`,
   `tokens_index`, `token_method`. Так измеряется экономия «весь документ vs
   один раздел» (см. [`kb/USAGE.md`](../USAGE.md)).

5. **Сверьте трассировку**: в `meta.json` проверьте `sources`, `source_pdfs`,
   `part_count`, а в любом `sections/*.md` — frontmatter `pdf_section`,
   `source_refs` и строку `Трассировка`.

> ⚠️ **Кириллица как «мусор» (nnnn).** Если текст извлёкся набором квадратов/
> «n» — у PDF нет ToUnicode-карты шрифтов (типично для сканов и некоторых
> экспортов). Это известная ловушка; способы обхода (OCR/иной экстрактор) — в
> [`docs/kb-experiment-report.md`](../../docs/kb-experiment-report.md).

---

## Как обновить документ (новая версия PDF)

1. Положите новый файл рядом со старым (или замените), обновите `version`/`date`
   в `source.md`.
2. Перезапустите извлечение **в тот же** `--out` (каталог пересоздаётся целиком —
   diff покажет ровно, что изменилось между версиями).
3. Проверьте и закоммитьте. Историю версий хранит git; при необходимости
   зафиксируйте изменения в `CHANGELOG.md`.

---

## Как добавить ссылку на веб-ресурс

Если источник — веб-страница (а не файл), оформите его в
[`kb/sources/web-links/`](web-links/README.md): создайте `*.md`-манифест со
ссылкой, датой обращения и (при необходимости) сохранённой выжимкой. Подробности
и шаблон — в README этого каталога.

---

## Что НЕ нужно делать

- ❌ Не кладите большие исходные PDF в произвольные места репозитория — только в
  `kb/sources/<slug>/` (так их найдут конвейер и `.gitignore`-правила).
- ❌ Не редактируйте `kb/processed/**` вручную — это генерируемый артефакт;
  правьте источник и перезапускайте извлечение.

## Источники

- Конвейер: [`scripts/kb/README.md`](../../scripts/kb/README.md)
- Структура результата: [`kb/processed/README.md`](../processed/README.md)
- Отчёт об эксперименте: [`docs/kb-experiment-report.md`](../../docs/kb-experiment-report.md)
