---
status: draft
version: 0.2
updated: 2026-06-21
ai-generated: true
type: kb-registry
scope: mango-taxonomy
related_artifacts:
  - "../../standards/mango-taxonomy-standard.md"
  - "../../standards/decisions/ADR-012-mango-taxonomy.md"
  - "../../standards/industry-taxonomy-standard.md"
  - "mango-registry.json"
  - "mango-registry.schema.json"
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/160"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/170"
---

# Mango Taxonomy Registry

`kb/mango/` хранит machine-readable реестр Mango Taxonomy по стандарту
[`standards/mango-taxonomy-standard.md`](../../standards/mango-taxonomy-standard.md)
и ADR
[`standards/decisions/ADR-012-mango-taxonomy.md`](../../standards/decisions/ADR-012-mango-taxonomy.md).

Начиная с issue #170 реестр — единый JSON-файл
[`mango-registry.json`](mango-registry.json), валидируемый JSON Schema
[`mango-registry.schema.json`](mango-registry.schema.json) (draft 2020-12).
Прежние три YAML-файла (`official-products.yaml`, `internal-registry.yaml` и
crosswalk `product-mapping.yaml`) свёрнуты в этот документ: crosswalk дублировал
`maps_to.industry_alignment` из каждой сущности и удалён, чтобы устранить
рассинхрон между реестром и отдельным mapping-файлом.

## Структура документа

Корень — единственный ключ `taxonomy` (по §8.1 стандарта), внутри — `version`
(SemVer-строка) и пять плоских массивов сущностей. Структура плоская: связи
между уровнями выражены явными ссылками по `id`, что допускает many-to-many.

| Массив | Уровень | Назначение |
| --- | --- | --- |
| `official_products` | `official-product` | Публичные продукты Mango Office. |
| `products` | `product` | Восемь внутренних продуктов (ADR-012). |
| `internal_services` | `service` | Сервисы внутри продуктов. |
| `modules` | `module` | Модули внутри сервисов. |
| `functions` | `function` | Функции внутри модулей. |

Каждая сущность несёт явную ссылку на родителя (`parent_products`,
`parent_services`, `parent_module`) и зеркальный список детей
(`services`, `modules`, `functions`) — валидатор проверяет их согласованность в
обе стороны.

## Official Layer

`official_products` фиксирует публичные продукты Mango Office: Виртуальная АТС,
Контакт-центр, Текстовые коммуникации, Mango Talker, Коллтрекинг, Речевая
аналитика, Роботы, Интеграции и связанные телефонные/инфраструктурные
предложения. Для каждого продукта указаны официальные URL, evidence refs,
поддерживающие внутренние сервисы (`supported_by_services`) и mapping к Industry
Taxonomy.

## Internal Layer

`products` / `internal_services` / `modules` / `functions` нормализуют
внутреннюю модель в иерархию `Product -> Service -> Module -> Function`. Реестр
покрывает все кластеры Mango Taxonomy:

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

`maps_to.industry_alignment` каждой Mango-сущности выравнивается на
[`standards/industry-taxonomy-standard.md`](../../standards/industry-taxonomy-standard.md)
и использует только канонические `industry_ref`, которые резолвятся против
canonical registry
[`kb/industry/reference-taxonomy.json`](../industry/reference-taxonomy.json).
Если Industry Taxonomy не содержит нужный Feature или Function, alignment несёт
`mapping_gap` с предлагаемым slug и причиной — отдельный crosswalk-файл больше не
нужен.

## AI-agent Contract

AI-agent должен:

- читать [`mango-registry.json`](mango-registry.json), когда нужен продуктовый
  слой Mango или внутренняя декомпозиция `Product -> Service -> Module ->
  Function` и её crosswalk к Industry Taxonomy;
- цитировать `evidence_refs` из записей, а не выводить продуктовые факты из
  названий сущностей;
- при добавлении или изменении сущностей держать `industry_ref` резолвящимися
  против Industry registry, а недостающие уровни фиксировать через
  `mapping_gap`, а не выдумывать отраслевые узлы.

## Validation

Лёгкая проверка без внешних зависимостей (резолвит каждый `industry_ref` против
живого Industry registry, проверяет JSON Schema, целостность родитель/ребёнок и
полноту иерархии):

```bash
python3 scripts/validate_issue_170_mango_registry.py
```

Полный KB-контур:

```bash
make kb-validate
```
