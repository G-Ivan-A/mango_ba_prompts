---
status: canonical
version: 1.3
updated: 2026-05-27
ai-generated: false
---

# Mango

Версия: 1.3

Дата: 2026-05-27

`projects/mango/` связывает практики `hybrid-Intelligence-lab` с пилотным
проектом Mango. Этот файл является навигацией: где лежит проектный контекст,
какие стандарты лаборатории применяются и как развивать подход мини-агента без
усложнения системного промпта.

## О проекте

| Поле | Значение |
| --- | --- |
| Репозиторий | [G-Ivan-A/mango](https://github.com/G-Ivan-A/mango) |
| Контекст | Mango - пилотный продуктовый проект, на котором проверяются стандарты лаборатории для навигации, базы знаний, промптов и правил совместной работы human + AI команды. |
| Проблема | Участникам нужен предсказуемый AI-assisted workflow: правила, термины и примеры должны быть доступны ИИ-чату и людям без разрастания одного большого промпта. |
| Стадия | Pilot |

Mango рассматривается как spoke-проект: продуктовый контекст, prompt assets и
knowledge base живут рядом с проектом, а лаборатория остается governance hub и
источником стандартов.

## Применяемые стандарты

| Стандарт | Как используется в Mango | Адаптация под проект |
| --- | --- | --- |
| [standards/PRODUCT_PROFILE.md](../../standards/PRODUCT_PROFILE.md) | Задает продуктовый профиль и минимальный набор артефактов. | В корне репозитория Mango должен быть `PRODUCT_VISION.md`: проблема, аудитория, ценность, границы и метрики стадии Pilot. |
| [standards/TEAM_CONTRACT.md](../../standards/TEAM_CONTRACT.md) | Дает шаблон командного соглашения для human contributors и AI agents. | На его основе в Mango создаются `CONTRIBUTING.md` и `AI_GOVERNANCE.md` с реальными ролями, review rules и границами ИИ. |
| [standards/ISSUE_WORKFLOW.md](../../standards/ISSUE_WORKFLOW.md) | Описывает lifecycle задач и связи issue -> artifact -> PR. | Изменения в правилах, prompts или `kb/` начинаются с issue и заканчиваются reviewed PR. |
| [standards/FILE_NAMING.md](../../standards/FILE_NAMING.md) | Помогает держать имена файлов предсказуемыми. | `prompts/system.md`, `kb/glossary.md`, `kb/policies.md` и примеры получают стабильные lower-case имена. |
| [standards/classification-glossary.md](standards/classification-glossary.md) | Фиксирует Mango-only уровни `Domain`, `Capability`, `Feature` и `Atomic Function`. | Все исследования Mango используют термины из `standards/classification-glossary.md`. |
| [governance/REPO_MODEL.md](../../governance/REPO_MODEL.md) | Объясняет, что лаборатория является hub, а продуктовый репозиторий - spoke. | В лаборатории хранится навигация и стандарты; production-код и проектный lifecycle остаются в Mango. |

Правило: все исследования Mango используют термины из
`standards/classification-glossary.md`.

## Концепция мини-агента

Мини-агент - это легкая конфигурация ИИ-чата для конкретного проекта:
системный промпт задает роль и правила маршрутизации контекста, а фактические
знания хранятся во внешней базе знаний `kb/`.

```text
Проблема:
Нужна предсказуемость промпта, но без программирования полноценного агента.

Решение:
- системный промпт хранится в prompts/system.md;
- промпт ссылается на kb/, а не встраивает все примеры внутрь себя;
- база знаний хранит glossary, policies и examples;
- ИИ-чат подгружает релевантный контекст из kb/;
- результат остается предсказуемым, а сам промпт - коротким.
```

Рабочий принцип:

| Компонент | Ответственность | Что не делать |
| --- | --- | --- |
| `prompts/system.md` | Роль мини-агента, operating mode, порядок чтения `kb/`, правила отказа и escalation. | Не копировать внутрь весь glossary, policies и длинные примеры. |
| `kb/glossary.md` | Термины предметной области, допустимые формулировки, связи между сущностями. | Не хранить процессные правила, которые должны быть в `policies.md`. |
| `kb/policies.md` | Правила валидации, форматы ответа, ограничения данных, Definition of Done для ответов. | Не смешивать с обучающими примерами и черновиками. |
| `kb/examples/` | Примеры хороших ответов, edge cases, anti-patterns. | Не превращать examples в единственный источник правил. |

Мини-агент полезен, когда нужно быстро повысить качество ответов без
разработки отдельного runtime, tool orchestration или agent framework. Если
появятся повторяющиеся действия с внешними системами, их нужно вынести в
отдельное решение и описать через `AI_GOVERNANCE.md`.

## Готовые prompt assets

`projects/mango/prompts/` содержит готовые тексты для копирования во внешний
ИИ-чат. Вариант `_exp` рассчитан на работу с выдержками из репозитория, а
`_simple` работает без доступа к репозиторию и переводит недостающий контекст в
уточняющие вопросы.

| Prompt | Назначение |
| --- | --- |
| `tz-stats-generator_exp-2026-05.md` | Статистика по ТЗ с опорой на `research/mango/classification.md`. |
| `tz-stats-generator_simple-2026-05.md` | Статистика по ТЗ через согласование классов в диалоге. |
| `user-story-generator_exp-2026-05.md` | User Story из сырого запроса с RAG-навигацией по Mango taxonomy. |
| `user-story-generator_simple-2026-05.md` | User Story из сырого запроса без доступа к репозиторию. |
| `usecase-stepwise-generator_exp-2026-05.md` | Пошаговый Use Case с согласованием акторов и компонентов через RAG-контекст. |
| `usecase-stepwise-generator_simple-2026-05.md` | Пошаговый Use Case в обычном чате без внутренних ссылок. |

Аудит исходных экспериментов зафиксирован в
`experiments/prompts-audit-2026-05-26.md`, self-test - в
`experiments/prompts-selftest-2026-05-26.md`.

## Шаблон структуры

```text
projects/mango/
├── README.md                 # Этот файл
├── standards/                # Mango-only стандарты и глоссарии
│   └── classification-glossary.md
├── prompts/                  # Готовые prompt assets для внешнего ИИ-чата
│   ├── tz-stats-generator_exp-2026-05.md
│   ├── tz-stats-generator_simple-2026-05.md
│   ├── user-story-generator_exp-2026-05.md
│   ├── user-story-generator_simple-2026-05.md
│   ├── usecase-stepwise-generator_exp-2026-05.md
│   └── usecase-stepwise-generator_simple-2026-05.md
├── kb/                       # База знаний (placeholder, .gitkeep)
│   ├── glossary.md           # Термины предметной области
│   ├── policies.md           # Правила валидации и форматы
│   └── examples/             # Примеры хороших ответов (опционально)
├── docs/                     # Документация для промптов (placeholder, .gitkeep)
│   └── analysis.md           # Анализ текущих процессов, не research report
├── experiments/              # Тесты и эксперименты (placeholder, .gitkeep)
│   └── prompt-ab-test/       # Тесты эффективности подхода
└── decisions/                # Зафиксированные решения по проекту (placeholder, .gitkeep)
```

Подкаталоги `standards/`, `prompts/`, `kb/`, `docs/`, `experiments/` и
`decisions/` уже созданы как точки расширения. Пустые каталоги отслеживаются в
Git через `.gitkeep`; `prompts/` уже содержит шесть активных prompt assets, а
`standards/classification-glossary.md` является активным Mango-only глоссарием.
Имена файлов внутри `kb/` показывают целевое наполнение, а не существующие
артефакты.

Эта структура является шаблоном для Mango. Создавайте новые файлы только когда
они снижают конкретную операционную боль: путаницу в терминах, повторяющиеся
review comments, нестабильные ответы ИИ или неясные правила изменения контекста.

## Навигация для участника

| Нужно понять | Куда идти |
| --- | --- |
| Что за продукт и зачем он существует | `PRODUCT_VISION.md` в репозитории Mango |
| Как вносить изменения | `CONTRIBUTING.md` в Mango, созданный по [TEAM_CONTRACT.md](../../standards/TEAM_CONTRACT.md) |
| Как ИИ может помогать | `AI_GOVERNANCE.md` в Mango и готовые prompt assets в `prompts/` |
| Какие термины использовать | `standards/classification-glossary.md`, затем `kb/glossary.md` |
| Какие правила ответа соблюдать | `kb/policies.md` |
| Где примеры хороших ответов | `kb/examples/` |
| Почему проект связан с лабораторией | [governance/REPO_MODEL.md](../../governance/REPO_MODEL.md) |

## Как внести изменения

1. Создайте issue в этом репозитории, если изменение затрагивает стандарт,
   governance rule или общий подход лаборатории.
2. Создайте issue в Mango, если изменение касается только продукта, его `kb/`,
   `prompts/`, процесса или примеров.
3. Для нового правила сначала опишите проблему: какой повторяющийся сбой,
   review comment или неясность оно устраняет.
4. После review обновите один источник истины: `kb/`, `prompts/`,
   `CONTRIBUTING.md`, `AI_GOVERNANCE.md` или стандарт лаборатории.
5. В PR укажите, какие проверки или ручная валидация подтверждают изменение.

Правило: если участник хочет изменить поведение мини-агента, он не правит
промпт и базу знаний одновременно без объяснения связи. Изменение должно
показывать, что относится к роли агента, а что относится к знаниям проекта.

## Связанные артефакты

- [projects/README.md](../README.md)
- [research/mango/README.md](../../research/mango/README.md)
- [projects/mango/prompts/tz-stats-generator_exp-2026-05.md](prompts/tz-stats-generator_exp-2026-05.md)
- [projects/mango/prompts/user-story-generator_exp-2026-05.md](prompts/user-story-generator_exp-2026-05.md)
- [projects/mango/prompts/usecase-stepwise-generator_exp-2026-05.md](prompts/usecase-stepwise-generator_exp-2026-05.md)
- [standards/PRODUCT_PROFILE.md](../../standards/PRODUCT_PROFILE.md)
- [standards/TEAM_CONTRACT.md](../../standards/TEAM_CONTRACT.md)
- [standards/ISSUE_WORKFLOW.md](../../standards/ISSUE_WORKFLOW.md)
- [governance/REPO_MODEL.md](../../governance/REPO_MODEL.md)
