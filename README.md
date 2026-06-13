---
status: canonical
version: 2.1
updated: 2026-06-11
ai-generated: true
---

# Mango BA Prompts

> **Библиотека готовых промптов для бизнес-аналитиков Mango Office.**
> Не база знаний и не исследования: здесь живут **инструменты** — промпты,
> которыми БА генерирует ТЗ-статистику, use-case'ы и user story.

`mango_ba_prompts` — standalone-проект (спок), выросший из проекта Mango в
монорепо-Хабе и теперь живущий самостоятельно. Спок несёт **исполняемую
ценность** (промпты и их рабочий контекст). Фундаментальные исследования
остаются в Хабе — спок ссылается на них из **одной точки**:
`docs/hub-research-dependencies.md` (единый реестр research-зависимостей).

## 🧭 Стратегия и тактика

- **Стратегическая цель** — автоматизация процессов бизнес-анализа в Mango.
- **Тактика** — библиотека **паттернов** ([`patterns/`](patterns/)) и
  **промптов** ([`prompts/`](prompts/)), организованная таксономией
  13 когнитивных операций и 9 процессов БА
  ([`docs/taxonomy.md`](docs/taxonomy.md)); маппинг процесс ↔ паттерн ↔
  промпт ведётся централизованно в
  [`docs/ba-processes/00-index.md`](docs/ba-processes/00-index.md), а
  граф связей, матрицы, классификации и сценарии запуска — в
  [`docs/ba-ecosystem.md`](docs/ba-ecosystem.md).
- **Стратегическое направление** — перенос лучших практик в Хаб; процесс и
  критерии зафиксированы в RFC
  [`docs/rfc-hub-integration.md`](docs/rfc-hub-integration.md).

## 🎯 Что это за библиотека

| Вопрос | Ответ |
| --- | --- |
| **Что это?** | Набор готовых промптов для типовых задач бизнес-анализа Mango Office: генерация ТЗ-статистики, use-case'ов, user story. |
| **Чем это _не_ является?** | Это **не** база знаний и **не** исследовательский репозиторий. Справочники и практики лежат в `kb/`, стандарты — в `standards/`, а исследования — в Хабе (по ссылке). |
| **Кому полезно?** | Бизнес-аналитикам, которым нужен воспроизводимый промпт «под задачу», и AI-агентам, работающим внутри правил проекта. |

## 🚀 Quickstart: как пользоваться промптами

0. **Открой веб-каталог.** GitHub Pages интерфейс живёт в [`site/`](site/) и
   собирается из Markdown source of truth командой
   `node scripts/generate-pages-data.mjs`. Данные для браузера лежат в
   [`site/data/`](site/data/), деплой в `gh-pages` выполняет
   [`.github/workflows/github-pages.yml`](.github/workflows/github-pages.yml).
1. **Найди промпт.** Активные, готовые к работе ассеты лежат в `prompts/`
   (имена в формате `[biz-process]-[purpose].md`, например
   `prompts/tz-stats-generator.md`).
2. **Прочитай frontmatter.** Каждый промпт начинается с YAML-блока, который
   говорит, как его запускать и откуда он взялся:

   | Поле | Зачем |
   | --- | --- |
   | `status` | Зрелость: `draft` / `canonical` (готов) / `archived`. **Обязательное.** |
   | `version` | Версия содержимого. **Обязательное.** |
   | `updated` | Дата последнего изменения. **Обязательное.** |
   | `temperature` | Рекомендуемая температура запуска (обычно `0.1`). **Обязательное.** |
   | `source_hub` / `source_sha` / `based_on` | Происхождение мигрированного промпта (provenance). *Опциональное.* |

   Только 4 поля обязательны ([`standards/prompt-standard.md`](standards/prompt-standard.md)).
   Маппинг на процессы и паттерны — в
   [`docs/ba-processes/00-index.md`](docs/ba-processes/00-index.md),
   research-зависимости — в
   [`docs/hub-research-dependencies.md`](docs/hub-research-dependencies.md):
   frontmatter ими не перегружается.

3. **Запусти промпт** в своей LLM с указанной температурой и форматом вывода;
   следуй разделу **«ФОРМАТ ВЫВОДА»** внутри промпта.
4. **Нужен черновик?** Экспериментальные и ещё не утверждённые промпты —
   в `prompts/drafts/`. Их можно создавать без human review
   (см. capability boundaries в [`AI_GOVERNANCE.md`](AI_GOVERNANCE.md)).
   Перевод в `prompts/` (canonical) — через issue → PR → review.

## 🗂️ Структура `prompts/`

| Путь | Роль |
| --- | --- |
| `prompts/` | Активные, утверждённые промпты — основной инструментарий БА. |
| `prompts/drafts/` | Черновики и экспериментальные варианты (без human review). |
| `prompts/experiments/` | Продуктовые эксперименты: источники `based_on` промптов и self-test сценарии, сохраняющие операционную историю. |
| `prompts/archive/` | Устаревшие промпты, выведенные из активного использования. |

## 📐 Структура репозитория

| Путь | Роль |
| --- | --- |
| `AI_GOVERNANCE.md` | Конституция проекта: роли, правила, эскалация, capability taxonomy, DoD. |
| `AI_QUICK_RULES.md` | Одностраничная инструкция для AI-агента (включая fail-closed semantics). |
| `AI_SESSION_HANDOVER_PROMPT.md` | Готовый prompt для Runtime-онбординга и передачи контекста между чатами. |
| `CONTRIBUTING.md` | Workflow вклада: issue → PR → review. |
| `CHANGELOG.md` | Память проекта: журнал значимых изменений. |
| `LICENSE` | Лицензия проекта (MIT). |
| `governance/artifact-map.md` | Локальная карта активных артефактов, связей и Smart Sync snapshot. |
| `governance/BACKLOG.md` | Операционный бэклог и единый трекер открытых вопросов проекта. |
| `governance/session-digests.md` | Индекс суммарий длинных сессий для передачи контекста между чатами. |
| `.gitignore` | Игнорируемые артефакты редакторов и ОС. |
| `.github/workflows/github-pages.yml` | Генерация данных и публикация статического интерфейса в `gh-pages`. |
| `scripts/` | Локальные генераторы, включая сборку JSON для GitHub Pages. |
| `site/` | Статический интерфейс каталога промптов, дашборда и roadmap. |
| `patterns/` | Паттерны БА: воспроизводимые способы решения классов задач (8 полей, [`standards/pattern-standard.md`](standards/pattern-standard.md)). |
| `prompts/` | Активные prompt assets бизнес-аналитика Mango. |
| `prompts/experiments/` | Продуктовые эксперименты, self-test сценарии и результаты прогонов промптов. |
| `prompts/archive/` | Архивные версии промптов и устаревшие варианты. |
| `standards/` | Стандарты проекта: глоссарий, контракт классификации, стандарты промпта и паттерна. |
| `kb/` | Практики, примеры и справочники, не являющиеся стандартами. |
| `docs/taxonomy.md` | Таксономия: 13 когнитивных операций и 9 процессов БА. |
| `docs/ba-ecosystem.md` | Экосистема работы БА: граф связей, матрицы, процессная карта, классификации, примеры запуска и стратегия перехода к агентам. |
| `docs/rfc-hub-integration.md` | RFC: процесс и критерии переноса практик в Хаб. |
| `docs/ba-processes/` | Индекс процессов БА и центральный маппинг процесс ↔ паттерн ↔ промпт. |
| `docs/adr/` | Architecture Decision Records — «почему», а не только «что». |
| `docs/audit/` | Ревизии, аудиты и проверки соответствия. |
| `docs/analysis/` | RFC и аналитические отчёты (например, стратегия миграции из Хаба). |

`standards/` — рабочие копии стандартов. Source of truth для общих стандартов
остаётся в Хабе; синхронизация копии — **осознанное** действие спока
(фиксируется в [`CHANGELOG.md`](CHANGELOG.md)).

| Путь | Роль |
| --- | --- |
| `standards/GLOSSARY.md` | Словарь терминов (рабочая копия общего глоссария Хаба). |
| `standards/product-classification-contract.md` | Контракт классификации Mango: `Domain → Capability → Feature → Atomic Function`. Это спецификация, **не** глоссарий. |
| `standards/prompt-standard.md` | Контракт промпта: 4 обязательных поля frontmatter, именование, RAG-формат ссылок. |
| `standards/pattern-standard.md` | Контракт паттерна: 8 обязательных полей, универсальный `prompt_template`. |

> ℹ️ Каталог появляется **только** под реальный артефакт — спок не носит с
> собой пустых «органелл» (Anti-Inflation principle).

## 🔗 Связь с Хабом — единственный мост

Спок **не копирует** исследования Хаба, чтобы избежать дрейфа. Все зависимости
от research-материалов Хаба регистрируются в **одном** файле —
`docs/hub-research-dependencies.md`, — и промпты ссылаются на них через
`research_dep: docs/hub-research-dependencies.md#<anchor>`.
Это **единственный** канонический мост между споком и Хабом; прямых
hub-относительных ссылок (`../../standards/...`, `../../research/...`) в споке
быть не должно.

## 🧭 Навигация для участника

| Нужно понять | Куда идти |
| --- | --- |
| Что за проект и зачем он существует | Этот `README.md` |
| Таксономия операций и процессов БА | [`docs/taxonomy.md`](docs/taxonomy.md) |
| Как связаны направления, шаблоны, процессы, операции и промпты | [`docs/ba-ecosystem.md`](docs/ba-ecosystem.md) |
| Какой промпт брать под мой процесс | [`docs/ba-processes/00-index.md`](docs/ba-processes/00-index.md) |
| Как практики попадают в Хаб | [`docs/rfc-hub-integration.md`](docs/rfc-hub-integration.md) |
| Требования к промпту / паттерну | [`standards/prompt-standard.md`](standards/prompt-standard.md), [`standards/pattern-standard.md`](standards/pattern-standard.md) |
| Куда записать открытый вопрос | [`governance/BACKLOG.md`](governance/BACKLOG.md#5-открытые-вопросы) |
| Как ИИ может помогать и где границы | [AI_GOVERNANCE.md](AI_GOVERNANCE.md) |
| Как вносить изменения | [CONTRIBUTING.md](CONTRIBUTING.md) |
| Где появятся стандарты и глоссарий | `standards/` |
| Почему проект связан с лабораторией | Раздел [«Связь с Хабом»](#-связь-с-хабом) |
| Как вносить вклад (временный workflow) | [`CONTRIBUTING.md`](CONTRIBUTING.md) |
| Как ИИ может помогать и где границы | [`AI_GOVERNANCE.md`](AI_GOVERNANCE.md) |
| Правила выживания агента (fail-closed) | [`AI_QUICK_RULES.md`](AI_QUICK_RULES.md) |
| Как запустить ИИ-агента в новой сессии (готовый промпт) | [`AI_SESSION_HANDOVER_PROMPT.md`](AI_SESSION_HANDOVER_PROMPT.md) |
| Протокол онбординга агента (чек-лист перед стартом) | [`governance/agent-onboarding-protocol.md`](governance/agent-onboarding-protocol.md) |
| Карта активных артефактов и связей | [`governance/artifact-map.md`](governance/artifact-map.md) |
| Суммарии длинных сессий для передачи контекста | [`governance/session-digests.md`](governance/session-digests.md) |
| Журнал значимых изменений | [`CHANGELOG.md`](CHANGELOG.md) |
| Снимок миграции из Хаба (что перенесено / осталось / архивировано) | [`governance/migration-manifest.md`](governance/migration-manifest.md) |

## 👥 Контакты и ответственные

Распределение ролей и право финального решения — в
[`AI_GOVERNANCE.md`](AI_GOVERNANCE.md).

| Роль | Кто | Ответственность |
| --- | --- | --- |
| Пользователь | Иван Гулиенко ([@G-Ivan-A](https://github.com/G-Ivan-A)) | Vision, приоритеты, границы публикации и финальные решения. |
| Human reviewer | назначается на issue/PR | Проверяет структуру, источники, риски и полезность до merge. |
| Contributor | любой участник | Создаёт issues, артефакты и pull requests внутри модели проекта. |
| Исполнитель / AI agent | по issue | Готовит черновики, проверки и summaries в пределах scope issue. |

Вопросы и предложения — через [GitHub Issues](https://github.com/G-Ivan-A/mango_ba_prompts/issues).

## 📄 Лицензия

[MIT](LICENSE).
