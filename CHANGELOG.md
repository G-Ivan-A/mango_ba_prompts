---
status: draft
version: 0.1
updated: 2026-06-02
ai-generated: true
---

# Changelog — mango_ba_prompts

Все значимые изменения проекта документируются здесь. Формат основан на
[Keep a Changelog](https://keepachangelog.com/ru/1.1.0/); проект придерживается
[Semantic Versioning](https://semver.org/lang/ru/).

## Unreleased

### Added — Initial repository structure based on hybrid-Intelligence-lab templates

- Инициализация спока `mango_ba_prompts` из «ДНК-шаблона» Хаба
  (`templates/spoke/`): базовый геном (governance, quick rules, навигация,
  каркасы `docs/adr/`, `docs/audit/`, база знаний `kb/glossary.md`).
- «Бесплатные» улучшения из анализа рекомендаций команд C и Q:
  fail-closed semantics в `AI_QUICK_RULES.md` и capability taxonomy в
  `AI_GOVERNANCE.md`.
- RFC стратегии миграции проекта Mango из Хаба в спок
  (`docs/analysis/migration-strategy-rfc.md`, issue #8): аудит 23 артефактов
  Хаба по полным URL, фазовая стратегия (Mermaid), edge cases, креативные
  улучшения и триггеры эволюции. Стоп-фактор: физический перенос — после
  Human Review.

### Changed

- Переписан корневой `README.md` под standalone-спок (issue #28, M-001, v2.0):
  README теперь описывает `mango_ba_prompts` как **библиотеку промптов для
  бизнес-аналитиков** (ТЗ-статистика, use-case, user story), а не как базу
  знаний. Добавлены quickstart по чтению frontmatter промптов, структура
  `prompts/` и `standards/`, навигация на `CONTRIBUTING.md` и контакты/роли.
  Удалены унаследованные из «ДНК-шаблона» Хаба прямые и hub-относительные
  ссылки; единственный мост в Хаб — через `docs/hub-research-dependencies.md`.
- Уточнён RFC стратегии миграции (`docs/analysis/migration-strategy-rfc.md`,
  issue #10): добавлена таблица файлов Фазы 1, чек-лист нормализации промптов,
  единый реестр research-зависимостей, корректное разделение
  `standards/GLOSSARY.md` и `standards/product-classification-contract.md`,
  а также правила переноса продуктовых экспериментов.
- Зафиксированы решения фаундера по Q1–Q4 в RFC миграции
  (`docs/analysis/migration-strategy-rfc.md`, issue #21): таблица Фазы 1
  утверждена, Hub-ссылки должны быть permalink на SHA, self-test стал
  обязательным gate для статуса `migrated`, а стандарты, промпты, эксперименты и
  `hub-research-dependencies.md` идут одним PR Фазы 1.
- Завершена доработка RFC (`docs/analysis/migration-strategy-rfc.md`,
  issue #12, v0.3, блоки 3–8): реестр зависимостей от исследований Хаба (§3.5),
  переписка README.md как обязательная задача Фазы 1, согласованные формулировки
  edge cases E5 (все эксперименты — часть продукта) и E6 (разделение
  глоссария и контракта классификации, §4.1), временный workflow промптов P0
  для `CONTRIBUTING.md` (§5.2) и шаблон Migration Manifest (§5.3).
- Human Review доработанного RFC миграции
  (`docs/reviews/migration-rfc-human-review-2026-06.md`, issue #13): сверка
  v0.3 против чек-листа из 11 пунктов (архитектурная целостность, операционная
  готовность, трассируемость) — все пункты пройдены; зафиксированы открытые
  вопросы Q1–Q4 на решение фаундера перед стартом Фазы 0.
- Сформирован операционный бэклог Фазы 1 миграции
  (`governance/BACKLOG.md`, issue #14): 9 атомарных задач (M-001…M-009) с
  приоритетами, зависимостями, DoD и трассировкой на разделы утверждённого RFC,
  плюс Mermaid-диаграмма критического пути. Бэклог = один файл (Anti-Inflation);
  выполнение задач не начато.
- Материализован бэклог Фазы 1 в 9 готовых к созданию GitHub Issues
  (`governance/migration-phase1-issues.md`, issue #23): каждый пункт M-001…M-009
  оформлен по стандарту Хаба `ISSUE_WORKFLOW.md` (шаблон `task.yml`) с явным
  Operating Mode (`Creative`/`Structured`), приоритетом, зависимостями, DoD,
  трассировкой на RFC/бэклог и полными permalink-ссылками на Хаб (SHA
  `038868dd…`, решение Q2). Live-Issues создаёт человек при ревью (среда
  AI-агента имеет только `pull`-доступ; создание Issues — fail-closed,
  outward-facing). Сами задачи бэклога не выполняются.

### Removed

- Удалён технический корневой `.gitkeep`, созданный только для bootstrap PR.
