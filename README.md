---
status: canonical
version: 2.5
updated: 2026-10-31
temperature: 0.1
owner: G-Ivan-A
research_deps:
  - "docs/hub-research-dependencies.md#adr-009-repo-split"
  - "docs/hub-research-dependencies.md#separation-readiness"
---

# Mango BA Prompts

> **Автоматизация процессов бизнес-анализа в проекте Манго (телеком).**
> Здесь живут **рабочие инструменты и их операционная память**: промпты,
> паттерны, база знаний и прогоны на реальных задачах БА.

`mango_ba_prompts` — standalone-проект (спок), выросший из проекта Mango в
монорепо-Хабе и теперь живущий самостоятельно. Спок несёт **исполняемую
ценность** (промпты и их рабочий контекст). Фундаментальные исследования
остаются в Хабе — спок ссылается на них из **одной точки**:
`docs/hub-research-dependencies.md` (единый реестр research-зависимостей).

## 🔒 Роль проекта и границы

| Вопрос | Ответ |
| --- | --- |
| Что это за проект? | Автоматизация процессов бизнес-анализа в проекте Манго (телеком). Решения по видению и границам принимает Пользователь. |
| Публичный или приватный? | Целевая видимость — **Private** (решение ADR-009 v0.3). Смена видимости — решение Пользователя; до неё репозиторий считается публичным, и правила публикации применяются строго. |
| На чём работает? | Этапы 1–2 — GitHub (issues, PR, Markdown), сайт и **AI-исполнитель** как основной инструмент. Этап 3 добавляет оркестрацию в n8n, этап 4 — выделенный сервер ([ADR-017](docs/adr/2026-10-adr-017-four-stages-n8n-orchestration.md)). |
| Что уже работает? | Этап 1: промпты процесса и инструкция БА на сайте. Агентный клиент, потоки n8n и сервер — план этапов 2–4 в [`docs/roadmap.md`](docs/roadmap.md), а не работающая система. |
| Где публичная методология? | В отдельном репозитории [`ai-ba-playbooks`](https://github.com/G-Ivan-A/ai-ba-playbooks): универсальные и специализированные плейбуки для БА. |
| Как практики попадают туда? | **Односторонний неавтоматический** поток `приватный → публичный` с отбором Пользователем; обратный поток запрещён. Процесс — в [`docs/rfc-hub-integration.md`](docs/rfc-hub-integration.md). |
| Что будет с веб-каталогом после Private? | GitHub Pages на бесплатном плане для приватных репозиториев не работает — это блокер Q1. Варианты решения (внешний портал, поэтапная миграция, вывод через `ai-ba-playbooks`) зафиксированы в [`ai-governance/ai-governance.md`](ai-governance/ai-governance.md#веб-ресурс-app-после-приватизации); выбор — решение Пользователя. |

Полные нормы и карта «что публично / что приватно» — в
[`ai-governance/ai-governance.md`](ai-governance/ai-governance.md) (разделы «Роль проекта и инфраструктурная
модель» и «Подготовка к приватизации»).

## ⚖️ Принцип «качество системы исполнения > стоимость»

Надёжность, верифицируемость и отсутствие галлюцинаций важнее экономии токенов
и упрощения структуры. Практическое следствие зафиксировано в ДОД:

> Каждая операция БА обязана иметь зафиксированный механизм проверки —
> чек-лист, evals-метрику или human-in-the-loop gate.
> **Операция без процесса проверки считается незавершённой.**

Фактический статус: чек-листы и human-in-the-loop gate в репозитории есть,
**evals и golden-set отсутствуют** — пробел зафиксирован честно в
[`ai-governance/ai-governance.md`](ai-governance/ai-governance.md#статус-механизмов-проверки-на-сегодня) и
[`pr-ops/BACKLOG.md`](pr-ops/BACKLOG.md).

Норма и допустимые механизмы проверки — в
[`ai-governance/ai-governance.md`](ai-governance/ai-governance.md#принцип-качество-системы-исполнения--стоимость);
источник требований к ДОД (чек-лист D1–D10) — онтология процессов БА Хаба через
[`docs/hub-research-dependencies.md#ba-process-ontology`](docs/hub-research-dependencies.md#ba-process-ontology).

## 🧭 Стратегия и тактика

- **Стратегическая цель** — автоматизация процессов бизнес-анализа в Mango.
- **Стратегические документы** — [видение](docs/vision.md),
  [концепция](docs/concept.md), [архитектура](docs/architecture.md) и
  [roadmap четырёх этапов](docs/roadmap.md): промпты в чате LLM → агентный
  клиент → оркестрация в n8n → промышленная эксплуатация на сервере.
  Как начать этап 1 — [«Запуск этапа 1»](docs/roadmap.md#запуск-этапа-1).
- **Тактика** — библиотека **паттернов** ([`patterns/`](patterns/)) и
  **промптов** ([`prompts/`](prompts/)), организованная таксономией
  13 когнитивных операций и 9 процессов БА
  ([`docs/taxonomy.md`](docs/taxonomy.md)); маппинг процесс ↔ паттерн ↔
  промпт ведётся централизованно в
  [`docs/ba-processes/00-index.md`](docs/ba-processes/00-index.md), а
  граф связей, матрицы, классификации и сценарии запуска — в
  [`docs/ba-ecosystem.md`](docs/ba-ecosystem.md).
- **Стратегическое направление** — перенос зрелых практик наружу: методология —
  в Хаб, универсальные и специализированные плейбуки — в `ai-ba-playbooks`.
  Оба потока
  односторонние и неавтоматические; процесс и критерии зафиксированы в RFC
  [`docs/rfc-hub-integration.md`](docs/rfc-hub-integration.md).

## 🎯 Что это за библиотека

| Вопрос | Ответ |
| --- | --- |
| **Что это?** | Набор готовых промптов для типовых задач бизнес-анализа Mango Office: генерация ТЗ-статистики, use-case'ов, user story. |
| **Чем это _не_ является?** | Это **не** исследовательский репозиторий и **не** публичная витрина методологии. Исследования — в Хабе (по ссылке), публичные плейбуки — в `ai-ba-playbooks`; здесь остаются рабочие артефакты автоматизации БА в Манго. |
| **Кому полезно?** | Бизнес-аналитикам, которым нужен воспроизводимый промпт «под задачу», и AI-агентам, работающим внутри правил проекта. |

## 🚀 Quickstart: как пользоваться промптами

0. **Открой веб-каталог.** GitHub Pages интерфейс живёт в [`site/`](site/) и
   собирается из Markdown source of truth командой
   `node scripts/generate-pages-data.mjs`. Данные для браузера лежат в
   [`site/data/`](site/data/), деплой в `gh-pages` выполняет
   [`.github/workflows/github-pages.yml`](.github/workflows/github-pages.yml).
   Верхнее меню: **Каталог** (главная), **Дашборд**, **Процессы**, выход и тема.
   Отчёты доступны по прямым ссылкам под общим парольным входом. В каталоге
   доступны поиск с автодополнением, сортировка, фильтры (набор, стадии BCREQ,
   операции, режимы), экспорт выборки в Markdown и тёмная тема; кнопка «Ссылка» на
   карточке копирует прямую ссылку вида `#prompt=<id>`. Вход на сайт закрыт
   системным паролем (issue #388); пароль выдаёт владелец репозитория, порядок
   смены — [`docs/site-access.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/site-access.md).
   Процессы и операции связаны в обе стороны; счётчики учитывают другие фильтры
   и поиск. Для BCREQ `processes` (список текстовых стадий) и `operation`
   (одна из 13 когнитивных операций) берутся из frontmatter промптов;
   [контракт стадий](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/contracts/bcreq-stage-gates.md)
   задаёт распределение шагов.
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
   (см. capability boundaries в [`ai-governance/ai-governance.md`](ai-governance/ai-governance.md)).
   Перевод в `prompts/` (canonical) — через issue → PR → review.

## 🗂️ Структура `prompts/`

| Путь | Роль |
| --- | --- |
| `prompts/` | Активные, утверждённые промпты — основной инструментарий БА. |
| `prompts/drafts/` | Черновики и экспериментальные варианты (без human review). |
| `prompts/archive/` | Устаревшие промпты, выведенные из активного использования. |

Единый каталог результатов выполнения процессов, тестовых прогонов и
self-test evidence живёт в [`runs/`](runs/).

## 📐 Структура репозитория

| Путь | Роль |
| --- | --- |
| `ai-governance/ai-governance.md` | Конституция проекта: роли, правила, эскалация, capability taxonomy, DoD. |
| `ai-rules/ai-quick-rules.md` | Одностраничная инструкция для AI-агента (включая fail-closed semantics). |
| `ai-rules/AI_SESSION_HANDOVER_PROMPT.md` | Готовый prompt для Runtime-онбординга и передачи контекста между чатами (full-слой). |
| `prompts/AI_SESSION_HANDOVER_PROMPT.executable.md` | Executable-слой того же prompt: грузится первым, full — только по escalation triggers. |
| `ai-rules/agent-onboarding-protocol.md` | Актуальный протокол онбординга агента (v1.5, рабочая копия Хаба). |
| `CONTRIBUTING.md` | Workflow вклада: issue → PR → review. |
| `CHANGELOG.md` | Память проекта: журнал значимых изменений. |
| `LICENSE` | Лицензия проекта (MIT). |
| `pr-ops/artifact-map.md` | Локальная карта активных артефактов, связей и Smart Sync snapshot. |
| `pr-ops/BACKLOG.md` | Операционный бэклог и единый трекер открытых вопросов проекта. |
| `pr-ops/session-digests.md` | Индекс суммарий длинных сессий для передачи контекста между чатами. |
| `.gitignore` | Игнорируемые артефакты редакторов и ОС. |
| `.github/workflows/github-pages.yml` | Генерация данных и публикация статического интерфейса в `gh-pages`. |
| `scripts/` | Локальные генераторы, включая сборку JSON для GitHub Pages. |
| `tools/` | Рабочие копии валидаторов Хаба (`make validate`): frontmatter, именование файлов и базовая структура репозитория. Дельты — [`tools/README.md`](tools/README.md). |
| `.archive/` | Скрытый архив `superseded`-артефактов: сохраняются ради traceability, точками входа не являются ([`.archive/README.md`](.archive/README.md)). |
| `.github/workflows/validate.yml` | CI: прогон валидаторов Хаба на каждый PR и push в `main`. |
| `site/` | Статический SPA-интерфейс: Каталог, Дашборд, Roadmap, Процессы и Паттерны. |
| `patterns/` | Паттерны БА: воспроизводимые способы решения классов задач (8 полей, [`standards/pattern-standard.md`](standards/pattern-standard.md)). |
| `prompts/` | Активные prompt assets бизнес-аналитика Mango. |
| `prompts/archive/` | Архивные версии промптов и устаревшие варианты. |
| `runs/` | Единый каталог результатов выполнения процессов: `runs/YYYY/RUN-XXXX/` с `metadata.yaml`, `inputs/`, `outputs/`, `feedback/`, `logs/`. |
| [Ручной BCREQ pipeline](standards/bcreq-manual-classes/README.md) | 39 проектных стандартов, четыре фазы, [Mermaid и RFC](docs/rfc/2026-10-bcreq-manual-pipeline.md), [новый RUN-0078](runs/2026/RUN-0078/outputs/README.md). |
| [IDE-клиенты Этапа 2](docs/analysis/2026-10-30-ide-clients-stage-2.md) | Сравнение Goose/OpenCode V1/Cline, обучение Goose, перенос 39 классов без Python в работе БА, безопасность и мета-модель. |
| `standards/` | Стандарты проекта: глоссарий, контракт классификации, стандарты промпта и паттерна. |
| `kb/` | Практики, примеры и справочники, не являющиеся стандартами. |
| `docs/taxonomy.md` | Таксономия: 13 когнитивных операций и 9 процессов БА. |
| [Продуктовая таксономия Mango](https://github.com/konard/G-Ivan-A-mango_ba_prompts/blob/issue-399-c3c0e96510d8/docs/taxonomy/README.md) | Полный Product Layer до Atomic Function, HTML-аудит портала и машиночитаемая карта поиска БЗ. |
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
| `standards/ba-ontology.md` *(+ `artifact-naming`, `team-directory`, `kb`, `industry-standards`, `bcreq-process`, `pages-ux`)* | Формализованная онтология БА и стандарты (issue #97); контракты-носители — [ADR-003…010](docs/adr/). |

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
| Видение, концепция, архитектура и этапы | [`docs/vision.md`](docs/vision.md), [`docs/concept.md`](docs/concept.md), [`docs/architecture.md`](docs/architecture.md), [`docs/roadmap.md`](docs/roadmap.md) |
| Что предлагается сделать дальше (один отчёт) | [`docs/report/2026-10-31-repository-action-plan.md`](docs/report/2026-10-31-repository-action-plan.md) |
| Таксономия операций и процессов БА | [`docs/taxonomy.md`](docs/taxonomy.md) |
| Как связаны направления, шаблоны, процессы, операции и промпты | [`docs/ba-ecosystem.md`](docs/ba-ecosystem.md) |
| Какой промпт брать под мой процесс | [`docs/ba-processes/00-index.md`](docs/ba-processes/00-index.md) |
| Как практики попадают в Хаб и в `ai-ba-playbooks` | [`docs/rfc-hub-integration.md`](docs/rfc-hub-integration.md) |
| Роль проекта, инфраструктурная модель и приватизация | [`ai-governance/ai-governance.md`](ai-governance/ai-governance.md) |
| Почему операция без проверки не завершена | [`ai-governance/ai-governance.md`](ai-governance/ai-governance.md#принцип-качество-системы-исполнения--стоимость), [`docs/ba-ecosystem.md`](docs/ba-ecosystem.md) |
| Требования к промпту / паттерну | [`standards/prompt-standard.md`](standards/prompt-standard.md), [`standards/pattern-standard.md`](standards/pattern-standard.md) |
| Онтология БА, операции, нейминг, KB, процессы, UX Pages | [`standards/ba-ontology.md`](standards/ba-ontology.md), [`docs/adr/`](docs/adr/) |
| Куда записать открытый вопрос | [`pr-ops/BACKLOG.md`](pr-ops/BACKLOG.md#5-открытые-вопросы) |
| Как ИИ может помогать и где границы | [`ai-governance/ai-governance.md`](ai-governance/ai-governance.md) |
| Как вносить изменения | [CONTRIBUTING.md](CONTRIBUTING.md) |
| Где появятся стандарты и глоссарий | `standards/` |
| Почему проект связан с лабораторией | Раздел [«Связь с Хабом»](#-связь-с-хабом) |
| Как вносить вклад (временный workflow) | [`CONTRIBUTING.md`](CONTRIBUTING.md) |
| Как ИИ может помогать и где границы | [`ai-governance/ai-governance.md`](ai-governance/ai-governance.md) |
| Правила выживания агента (fail-closed) | [`ai-rules/ai-quick-rules.md`](ai-rules/ai-quick-rules.md) |
| Как запустить ИИ-агента в новой сессии (готовый промпт) | [`ai-rules/AI_SESSION_HANDOVER_PROMPT.md`](ai-rules/AI_SESSION_HANDOVER_PROMPT.md) |
| Протокол онбординга агента (чек-лист перед стартом), v1.5 | [`ai-rules/agent-onboarding-protocol.md`](ai-rules/agent-onboarding-protocol.md) |
| Архив протокола онбординга v1.2 (superseded, для traceability) | [`.archive/ai-rules/agent-onboarding-protocol_old.md`](.archive/ai-rules/agent-onboarding-protocol_old.md) |
| Почему корневые `AI_*.md` остаются в корне, а архив ушёл в `.archive/` | [`docs/audit/2026-08-21-root-structure-audit.md`](docs/audit/2026-08-21-root-structure-audit.md) |
| Карта активных артефактов и связей | [`pr-ops/artifact-map.md`](pr-ops/artifact-map.md) |
| Суммарии длинных сессий для передачи контекста | [`pr-ops/session-digests.md`](pr-ops/session-digests.md) |
| Журнал значимых изменений | [`CHANGELOG.md`](CHANGELOG.md) |
| Снимок миграции из Хаба (что перенесено / осталось / архивировано) | [`pr-ops/migration-manifest.md`](pr-ops/migration-manifest.md) |

## 👥 Контакты и ответственные

Распределение ролей и право финального решения — в
[`ai-governance/ai-governance.md`](ai-governance/ai-governance.md).

| Роль | Кто | Ответственность |
| --- | --- | --- |
| Пользователь | Иван Гулиенко ([@G-Ivan-A](https://github.com/G-Ivan-A)) | Vision, приоритеты, границы публикации и финальные решения. |
| Human reviewer | назначается на issue/PR | Проверяет структуру, источники, риски и полезность до merge. |
| Contributor | любой участник | Создаёт issues, артефакты и pull requests внутри модели проекта. |
| Исполнитель / AI agent | по issue | Готовит черновики, проверки и summaries в пределах scope issue. |

Вопросы и предложения — через [GitHub Issues](https://github.com/G-Ivan-A/mango_ba_prompts/issues).

## 📄 Лицензия

[MIT](LICENSE).
