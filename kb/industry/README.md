---
status: active
version: 1.0.0
updated: 2026-06-21
ai-generated: true
type: kb-industry-taxonomy
scope: kb/industry
related_artifacts:
  - "kb/industry/reference-taxonomy.json"
  - "kb/industry/reference-taxonomy.schema.json"
  - "standards/decisions/ADR-011-industry-taxonomy.md"
  - "standards/industry-taxonomy-standard.md"
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/156"
---

# Industry Taxonomy

`kb/industry/` хранит machine-readable Industry Taxonomy для отраслевой
классификации коммуникационных, контакт-центровых и смежных capabilities.
Реестр следует модели `Domain -> Capability -> Feature -> Function` из
ADR-011 и стандарта Industry Taxonomy.

## Артефакты

| Файл | Назначение |
| --- | --- |
| [`kb/industry/reference-taxonomy.json`](reference-taxonomy.json) | Канонический JSON-реестр Industry Taxonomy v1.0.0. |
| [`kb/industry/reference-taxonomy.schema.json`](reference-taxonomy.schema.json) | Локальная JSON Schema для структуры реестра и базовых enum-контрактов. |

## Покрытие

Реестр фиксирует семь canonical domains из ADR-011 v1.0:

- `voice-ucaas`
- `contact-center`
- `digital-channels`
- `ai-automation`
- `analytics`
- `hardware`
- `security`

`platform` вынесен отдельно как cross-domain layer, а не как восьмой domain.
Он содержит общие capabilities: `platform-integration`, `open-api`, `cpaas`,
`service-desk` и `vendor-support-services`.

## Контракт данных

Каждый taxonomy node содержит:

- `id` — canonical slug;
- `level` — один из `domain`, `capability`, `feature`, `function`;
- `name_en` и `name_ru` — человекочитаемые названия;
- `definition` — краткое определение;
- `lifecycle_status` — `proposed`, `active`, `deprecated` или `removed`;
- `evidence_refs` — ссылки на ADR, стандарт или источник decomposition;
- `parent` — путь к родительским уровням для non-domain nodes.

Каждый `function` дополнительно содержит `function_type`
(`business`, `configuration`, `ui-action`) и список `parameters`.

## Facets

Cross-cutting facets хранятся отдельно от иерархии, чтобы не создавать
дублирующие domain-ветки:

- `channel` с полями `channel_kind`, `synchronicity`, `direction`;
- `ai_assisted`;
- `security_compliance`;
- `commercial`;
- `procurement`;
- `industry_vertical`;
- `geography_region`.

`voice-channel` находится внутри `voice-ucaas` как first-class capability.
`sip-connectivity` остаётся инфраструктурной capability и не получает channel
facet, потому что SIP trunking не является пользовательским каналом.

## Источники и границы

Приоритет источников:

1. [`standards/decisions/ADR-011-industry-taxonomy.md`](../../standards/decisions/ADR-011-industry-taxonomy.md)
2. [`standards/industry-taxonomy-standard.md`](../../standards/industry-taxonomy-standard.md)
3. [`docs/analysis/voice-digital-channels-comparison.md`](../../docs/analysis/voice-digital-channels-comparison.md)
4. Reviewed Hub classification v3.0 и draft capability decomposition, указанные
   в `sources` внутри JSON-реестра.

Реестр не содержит Mango product mappings и не добавляет `industry_ref` для
продуктовых документов. Такие связи должны появляться отдельно в Mango
Taxonomy или mapping-артефактах.

Некоторые functions помечены `source_status=derived-completion`: это leaf-level
functions, добавленные для machine-readable полноты там, где источник называл
feature, но не выделял отдельную function. Их lifecycle наследуется от
родительской capability.

## Проверка

Лёгкая проверка Issue #156:

```bash
python3 scripts/validate_issue_156_industry_taxonomy_registry.py
```

Полный лёгкий KB-контур:

```bash
make kb-validate
```
