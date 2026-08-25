---
status: draft
version: 0.1
updated: 2026-08-25
ai-generated: true
type: output
scope: mango-only
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/317"
---

# Результат прогона RUN-0056

Рабочие артефакты прогона лежат вне каталога прогона — в `kb/`, как того
требует постановка (`результирующий каталоги в kb/`). Здесь фиксируется, что
именно получилось.

## Обновлённые разделы (кластер «Обновление»)

| Раздел БЗ | `doc_version` | Разделов | Границы разделов | `confidence_level` |
| --- | --- | --- | --- | --- |
| [`mango-cc-manual`](../../../../kb/processed/mango-cc-manual/index.md) | 1.26.28.1 (было 1.26.23) | 139 | typography-heuristic | requires_review |
| [`mango-lk-manual`](../../../../kb/processed/mango-lk-manual/index.md) | 1.23 | 351 | pdf-outline | requires_review |
| [`cov-robot-fil`](../../../../kb/processed/cov-robot-fil/index.md) | 1.26.28 | 75 | typography-heuristic | high |
| [`mtalker/windows-mac-working`](../../../../kb/processed/mtalker/windows-mac-working/index.md) | 11.06.2026 | 143 | typography-heuristic | high |
| [`mtalker/android-user-guide`](../../../../kb/processed/mtalker/android-user-guide/index.md) | 11.06.2026 | 99 | typography-heuristic | high |

## Новый раздел (кластер «Новые»)

| Раздел БЗ | `doc_code` | Разделов | Страниц | `confidence_level` |
| --- | --- | --- | --- | --- |
| [`mdialogi-api`](../../../../kb/processed/mdialogi-api/index.md) | MDAPI | 70 | 96 | high |

Каждый раздел содержит `index.md`, `meta.json`, `sections/`, `images/` и
`verification.md`.

## Предложение по структуре `kb/`

Отдельный документ: [`outputs/structure-proposal.md`](structure-proposal.md);
рабочая версия предложения зафиксирована в
[`kb/STRUCTURE_REVIEW.md`](../../../../kb/STRUCTURE_REVIEW.md).
