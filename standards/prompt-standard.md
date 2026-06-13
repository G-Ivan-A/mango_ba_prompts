---
status: draft
version: 0.1
updated: 2026-06-11
ai-generated: true
type: contract
scope: prompts
related_artifacts:
  - "standards/pattern-standard.md"
  - "docs/taxonomy.md"
  - "docs/ba-processes/00-index.md"
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/52"
---

# Стандарт промпта

> Предложен на утверждение Пользователю (issue #52). До утверждения —
> рекомендация. Формат — по практике Хаба: обязательства сверху,
> обоснование в конце; нормативный словарь
> [RFC 2119](https://www.rfc-editor.org/info/bcp14)
> (**ДОЛЖНО** / **СЛЕДУЕТ** / **МОЖНО**).

## Стороны и область

Контракт обязывает всех contributors и AI-агентов, создающих или изменяющих
файлы в `prompts/` (включая `prompts/archive/`). Не распространяется на
`prompts/experiments/` (см. §Тестирование) и `patterns/`
(см. [pattern-standard.md](pattern-standard.md)).

## Обязательства

### Frontmatter — ровно 4 обязательных поля

1. Промпт **ДОЛЖЕН** начинаться с YAML-frontmatter, содержащего ровно
   4 обязательных поля:

   | Поле | Значения | Назначение |
   | --- | --- | --- |
   | `status` | `draft` \| `canonical` \| `archived` | Зрелость промпта. |
   | `version` | semver (`0.1`, `1.0`, …) | Версия содержимого. |
   | `updated` | `YYYY-MM-DD` | Дата последнего изменения. |
   | `temperature` | число (обычно `0.1`) | Рекомендуемая температура запуска. |

2. `status: archived` — валидное терминальное значение. Архивация
   промпта **НЕ ДОЛЖНА** требовать создания issue: перенос файла в
   `prompts/archive/` + `status: archived` выполняется в обычном PR.
3. Frontmatter **НЕ ДОЛЖЕН** расширяться маппингами и ссылками:
   маппинг паттерн ↔ промпт ↔ процесс живёт централизованно в
   [docs/ba-processes/00-index.md](../docs/ba-processes/00-index.md),
   research-зависимости — в
   [docs/hub-research-dependencies.md](../docs/hub-research-dependencies.md).
4. Provenance-поля (`source_hub`, `source_sha`, `based_on`) **МОЖНО**
   сохранять для мигрированных артефактов; для новых промптов они
   не обязательны.

### Именование

5. Имя файла **ДОЛЖНО** следовать схеме `[домен]-[операция]-[режим].md`
   (kebab-case): операция — из
   [docs/taxonomy.md](../docs/taxonomy.md) (§1, `_` → `-`), режим —
   `stepwise` \| `oneshot` \| `legacy`. Пример: `fr-validation-stepwise.md`.

### Ссылки (формат для RAG)

6. Ссылки на стандарты и глоссарий внутри тела промпта **ДОЛЖНЫ** быть
   Markdown-ссылками с путём от корня репозитория:
   `См. [Глоссарий](standards/GLOSSARY.md)`. Относительные пути
   (`../standards/...`) и голые упоминания без ссылки **НЕ СЛЕДУЕТ**
   использовать — RAG-индексация опирается на единый формат.

### Жизненный цикл

7. Новый промпт **ДОЛЖЕН** проходить временный workflow из
   [CONTRIBUTING.md](../CONTRIBUTING.md): draft → review issue →
   `canonical`.
8. Промпт со `status: canonical` **ДОЛЖЕН** содержать явный раздел
   «ФОРМАТ ВЫВОДА».

### Тестирование

9. Результаты прогонов промпта **СЛЕДУЕТ** фиксировать в
   `prompts/experiments/` файлом
   `[имя-промпта]-[сценарий]-[YYYY-MM-DD].md` (практика продуктовых
   экспериментов, унаследованная из `projects/mango/experiments/` Хаба).
   Перевод `draft → canonical` **ДОЛЖЕН** опираться минимум на один
   зафиксированный прогон.

## Критерии соответствия (DoD)

- [ ] Frontmatter содержит ровно `status`, `version`, `updated`,
      `temperature` (+ опциональные provenance-поля для мигрированных).
- [ ] Имя файла соответствует `[домен]-[операция]-[режим].md`; операция
      существует в таксономии.
- [ ] Внутренние ссылки — Markdown от корня репозитория.
- [ ] Промпт отражён в маппинге
      [docs/ba-processes/00-index.md](../docs/ba-processes/00-index.md).

## Обоснование

- **4 поля, а не 7.** Migration-era frontmatter (7 полей: +`output_format`,
  `glossary_ref`, `research_dep`) перегружал файлы и дублировал
  централизованные реестры. Минимальный frontmatter снижает трение для БА
  и AI-агентов (решение Пользователя, issue #52); всё остальное выносится в
  `docs/ba-processes/00-index.md` и `docs/hub-research-dependencies.md`.
- **`archived` без issue.** Архив — операция низкого риска (файл не
  удаляется); обязательный issue создавал бы лишний процессный шум.
- **RAG-формат ссылок.** Единый предсказуемый формат позволяет резолвить
  ссылки при индексации промптов в RAG без эвристик.
