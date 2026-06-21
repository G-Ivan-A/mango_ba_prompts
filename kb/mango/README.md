---
status: draft
version: 0.1
updated: 2026-06-21
ai-generated: true
type: kb-registry
scope: mango-taxonomy
related_artifacts:
  - "../../standards/mango-taxonomy-standard.md"
  - "../../standards/decisions/ADR-012-mango-taxonomy.md"
  - "../../standards/industry-taxonomy-standard.md"
  - "official-products.yaml"
  - "internal-registry.yaml"
  - "product-mapping.yaml"
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/160"
---

# Mango Taxonomy Registry

`kb/mango/` хранит machine-readable реестр Mango Taxonomy по стандарту
[`standards/mango-taxonomy-standard.md`](../../standards/mango-taxonomy-standard.md)
и ADR
[`standards/decisions/ADR-012-mango-taxonomy.md`](../../standards/decisions/ADR-012-mango-taxonomy.md).
Файлы сериализованы как JSON-compatible YAML: это валидный YAML, который можно
проверять без внешних Python-зависимостей.

## Official Layer

[`official-products.yaml`](official-products.yaml) фиксирует публичные продукты
Mango Office: Виртуальная АТС, Контакт-центр, Текстовые коммуникации, Mango
Talker, Коллтрекинг, Речевая аналитика, Роботы, Интеграции и связанные
телефонные/инфраструктурные предложения. Для каждого продукта указаны
официальные URL, evidence refs, поддерживающие внутренние сервисы и mapping к
Industry Taxonomy.

## Internal Layer

[`internal-registry.yaml`](internal-registry.yaml) нормализует внутреннюю модель
в иерархию `Product -> Service -> Module -> Function`. Реестр покрывает все
кластеры Mango Taxonomy:

| Cluster | Назначение |
| --- | --- |
| `vats-core` | Входящая маршрутизация, IVR, номера и записи ВАТС. |
| `contact-center-core` | Операторское рабочее место, очереди, кампании и WFM. |
| `digital-channels` | Текстовые каналы, чат сайта, мессенджеры и Dialog API. |
| `mango-talker` | Софтфон, командные чаты, видео и контакты Mango Talker. |
| `ai-speech-quality` | Речевая аналитика, AI-конспекты, качество и роботы. |
| `analytics-marketing` | Коллтрекинг, сквозная аналитика, отчёты и Wallboard. |
| `platform-integrations` | Open API, webhooks и CRM/ERP-интеграции. |
| `security-access` | Роли, SSO, безопасность записей и аудит. |

Function-level записи используют `function_type` (`business`, `configuration`,
`ui-action`) и `interaction_surface`, чтобы AI-agent мог отличать бизнесовое
действие, настройку и пользовательскую UI-операцию.

## Industry Taxonomy

[`product-mapping.yaml`](product-mapping.yaml) дублирует
`maps_to.industry_alignment` из каждой Mango-сущности в отдельном crosswalk
файле. Mapping выравнивается на
[`standards/industry-taxonomy-standard.md`](../../standards/industry-taxonomy-standard.md)
и использует только канонические `industry_ref`. Если Industry Taxonomy не
содержит нужный Feature или Function, запись содержит `mapping_gap` с
предлагаемым slug и причиной.

## AI-agent Contract

AI-agent должен:

- читать `official-products.yaml`, когда нужен публичный продуктовый слой Mango;
- читать `internal-registry.yaml`, когда нужна внутренняя декомпозиция
  `Product -> Service -> Module -> Function`;
- читать `product-mapping.yaml`, когда нужен полный crosswalk Mango Taxonomy к
  Industry Taxonomy;
- цитировать `evidence_refs` из записей, а не выводить продуктовые факты из
  названий сущностей;
- сохранять `maps_to.industry_alignment` и mapping file синхронными.

## Validation

Лёгкая проверка без внешних зависимостей:

```bash
python3 scripts/validate_issue_160_mango_registry.py
```

Полный KB-контур:

```bash
make kb-validate
```
