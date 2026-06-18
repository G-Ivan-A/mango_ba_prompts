---
status: draft
version: 0.1
updated: 2026-06-18
ai-generated: true
type: kb-processed-guide
scope: kb/processed
related_artifacts:
  - "scripts/kb/extract.py"
  - "kb/USAGE.md"
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/111"
---

# `kb/processed/` — результаты извлечения (для агентов)

Сгенерированный, **machine-readable** слой БЗ: вывод
[`scripts/kb/extract.py`](../../scripts/kb/extract.py). Эти файлы **не правят
руками** — правят источник в `kb/sources/` и перезапускают извлечение.

> Как промпт читает этот слой (индекс → выбор раздела → загрузка одного раздела →
> цитата → сравнение токенов) — c реальными сниппетами в
> [`kb/USAGE.md`](../USAGE.md).

## Структура одного документа

```
kb/processed/<doc-slug>/
├── index.md            ← карта разделов: раздел → файл → стр. → токены → «когда обращаться»
├── meta.json           ← метаданные: инструмент, sha256 источника, счётчики, токены
├── sections/
│   ├── 00-...md        ← титульная часть
│   ├── 01-...md        ← раздел = чанк (frontmatter: id, pages, tokens, source)
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
pages: "5"                         # страницы источника (для цитаты [CC, §4, с.5])
tokens: 378                        # реальные токены (метод — token_method)
source: kb/sources/.../*.pdf       # откуда извлечено
status: extracted
ai-generated: true
```

Это соответствует pre-RAG-механике стандарта БЗ (ADR-007, правила R1–R4):
каждый раздел = файл = чанк; `index.md` = retrieval-шаг; адреса `path#anchor`
станут chunk-id без переписывания, когда появится векторный RAG.

## Каталоги

| Документ | Статус |
| --- | --- |
| [`contact-center-manual-sample/`](contact-center-manual-sample/index.md) | извлечён из синтетической фикстуры (эксперимент issue #111) |
| `contact-center-manual/` | появится, когда добавят реальный `CC_manual_1.26.23.pdf` (см. [манифест](../sources/contact-center-manual/source.md)) |

## Источники

- Конвейер и оценка качества: [`docs/kb-experiment-report.md`](../../docs/kb-experiment-report.md)
- Пополнение БЗ: [`kb/sources/README.md`](../sources/README.md)
