---
status: draft
version: 0.1
updated: 2026-06-19
ai-generated: true
type: audit
scope: kb-pipeline
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/115"
related_artifacts:
  - "../../.github/workflows/kb.yml"
  - "../../kb/processed/mango-cc-manual/index.md"
  - "../../scripts/validate_issue_115_kb_mango_pipeline.py"
---

# Issue #115 — аудит KB Pipeline #11

## Симптом

После загрузки `kb/sources/mango-cc-manual/CC_manual_1.26.23_compressed.pdf` и
`meta.json` ручной запуск **KB Pipeline #11** завершился успешно, но каталог
`kb/processed/mango-cc-manual/` в репозитории отсутствовал.

## Найденная причина

Лог запуска `27819999447` показал, что job `extract` выполнял:

```text
make kb-sample
make kb-extract
```

То есть workflow всегда пересобирал синтетическую фикстуру
`contact-center-manual-sample`, а не новый источник `mango-cc-manual`.
Дополнительно workflow имел `permissions: contents: read` и только загружал
`kb/processed/` как artifact; коммита результата в репозиторий не было.

## Исправление

- `Makefile` принимает `SRC`, `OUT`, `CODE`, `TITLE`, `VERSION`, `NOTE` и добавляет
  цель `kb-mango`.
- `workflow_dispatch` получил inputs с дефолтами для `mango-cc-manual`; extract job
  передает эти inputs в `make kb-extract`.
- Результат всегда загружается artifact-ом, а при `commit_result=true` может быть
  закоммичен обратно в текущую ветку.
- Реальная БЗ создана в `kb/processed/mango-cc-manual/`.
- Добавлен validator `scripts/validate_issue_115_kb_mango_pipeline.py`, который
  проверяет наличие реальной БЗ и защиту от возврата к hardcoded sample workflow.

## Качество извлечения

Руководство содержит встроенное PDF outline. `extract.py` теперь использует outline
как источник границ разделов, если он доступен. Это убирает ложные чанки из жирных
нумерованных пунктов списков, которые появлялись при одной только эвристике по
кеглю/жирности.

Результат для `mango-cc-manual`:

- 614 страниц;
- 232 раздела, включая титульную часть и outline-разделы;
- 1 771 изображение;
- 524 таблицы;
- `index.md`, `meta.json`, `sections/`, `images/` созданы в нужном каталоге.
