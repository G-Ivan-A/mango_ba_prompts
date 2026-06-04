---
status: canonical
version: 1.0
updated: 2026-06-02
ai-generated: true
---

# mango_ba_prompts

> Spoke-проект, рождённый из Хаба `hybrid-Intelligence-lab` по «ДНК-шаблону»
> (`templates/spoke/`). Минимальный, но «правильный» геном: правила, контакт с
> Хабом и каркас для роста по запросу.

Prompt assets и knowledge base бизнес-аналитика Mango Office (spoke Хаба).

## 🧬 Связь с Хабом

| Что | Где |
| --- | --- |
| Источник истины (governance, стандарты, research) | [hybrid-Intelligence-lab](https://github.com/G-Ivan-A/hybrid-Intelligence-lab) |
| Фундаментальные знания | `research/` Хаба (в споке `research/` **не создаётся**) |
| Операционный контракт проекта | [AI_GOVERNANCE.md](AI_GOVERNANCE.md) |
| Быстрые правила для агента | [AI_QUICK_RULES.md](AI_QUICK_RULES.md) |

## 🗂️ Структура (сейчас)

| Путь | Роль |
| --- | --- |
| `AI_GOVERNANCE.md` | Конституция проекта: роли, правила, эскалация, capability taxonomy, DoD. |
| `AI_QUICK_RULES.md` | Одностраничная инструкция для AI-агента (включая fail-closed semantics). |
| `CONTRIBUTING.md` | Workflow вклада: issue → PR → review. |
| `CHANGELOG.md` | Память проекта: журнал значимых изменений. |
| `LICENSE` | Лицензия проекта (MIT). |
| `.gitignore` | Игнорируемые артефакты редакторов и ОС. |
| `prompts/` | Активные prompt assets бизнес-аналитика Mango. |
| `prompts/experiments/` | Продуктовые эксперименты и self-test сценарии для промптов. |
| `prompts/archive/` | Архивные версии промптов и устаревшие варианты. |
| `standards/` | Стандарты проекта: глоссарий и контракт классификации. |
| `kb/` | Практики, примеры и справочники, не являющиеся стандартами. |
| `docs/adr/` | Architecture Decision Records — «почему», а не только «что». |
| `docs/audit/` | Ревизии, аудиты и проверки соответствия. |
| `docs/analysis/` | RFC и аналитические отчёты (например, стратегия миграции из Хаба). |

Базовые каталоги Фазы 1 созданы для миграции по M-002. Содержательные артефакты
переносятся отдельными задачами M-003…M-009.

## 🧭 Навигация для участника

| Нужно понять | Куда идти |
| --- | --- |
| Что за проект и зачем он существует | Этот `README.md` |
| Как ИИ может помогать и где границы | [AI_GOVERNANCE.md](AI_GOVERNANCE.md) |
| Правила выживания агента | [AI_QUICK_RULES.md](AI_QUICK_RULES.md) |
| Как вносить изменения | [CONTRIBUTING.md](CONTRIBUTING.md) |
| Где появятся стандарты и глоссарий | `standards/` |
| Почему проект связан с лабораторией | Раздел [«Связь с Хабом»](#-связь-с-хабом) |
